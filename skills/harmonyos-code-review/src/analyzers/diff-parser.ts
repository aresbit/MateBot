/**
 * Diff 解析器
 *
 * 支持从多种来源解析 Git diff：
 * - GitLab Merge Request URL
 * - GitHub Pull Request URL
 * - 本地 diff 文件
 * - Git 命令输出
 */
import * as fs from 'fs';
import { FileChange } from '../types';

export class DiffParser {
  private gitlabToken?: string;
  private githubToken?: string;

  constructor(tokens?: { gitlab?: string; github?: string }) {
    this.gitlabToken = tokens?.gitlab;
    this.githubToken = tokens?.github;
  }

  /**
   * 从 URL 解析 MR/PR
   */
  async parseFromUrl(url: string): Promise<FileChange[]> {
    const parsed = this.parseRepositoryUrl(url);

    if (parsed.type === 'gitlab') {
      return this.parseGitLabMR(parsed);
    } else if (parsed.type === 'github') {
      return this.parseGitHubPR(parsed);
    }

    throw new Error(`Unsupported URL: ${url}`);
  }

  /**
   * 从本地文件解析 diff
   */
  async parseFromFile(filePath: string): Promise<FileChange[]> {
    try {
      const diffContent = fs.readFileSync(filePath, 'utf-8');
      return this.parseDiffFile(diffContent);
    } catch (error) {
      throw new Error(`Failed to read diff file: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * 解析 diff 内容
   */
  parseDiffFile(diffContent: string): FileChange[] {
    const changes: FileChange[] = [];
    const files = this.splitDiffByFile(diffContent);

    for (const fileDiff of files) {
      const change = this.parseSingleFileDiff(fileDiff);
      if (change) {
        changes.push(change);
      }
    }

    return changes;
  }

  /**
   * 解析仓库 URL
   */
  private parseRepositoryUrl(url: string): {
    type: 'gitlab' | 'github';
    host: string;
    owner: string;
    repo: string;
    mergeRequestId?: number;
    pullRequestId?: number;
  } {
    // GitLab MR: https://gitlab.com/group/project/-/merge_requests/123
    const gitlabMRMatch = url.match(/https?:\/\/([^\/]+)\/(.+?)\/(.+?)\/-\/merge_requests\/(\d+)/);
    if (gitlabMRMatch) {
      return {
        type: 'gitlab',
        host: gitlabMRMatch[1],
        owner: gitlabMRMatch[2],
        repo: gitlabMRMatch[3],
        mergeRequestId: parseInt(gitlabMRMatch[4], 10)
      };
    }

    // GitHub PR: https://github.com/owner/repo/pull/42
    const githubPRMatch = url.match(/https?:\/\/([^\/]+)\/(.+?)\/(.+?)\/pull\/(\d+)/);
    if (githubPRMatch) {
      return {
        type: 'github',
        host: githubPRMatch[1],
        owner: githubPRMatch[2],
        repo: githubPRMatch[3],
        pullRequestId: parseInt(githubPRMatch[4], 10)
      };
    }

    throw new Error(`Invalid MR/PR URL: ${url}`);
  }

  /**
   * 解析 GitLab MR
   */
  private async parseGitLabMR(parsed: {
    host: string;
    owner: string;
    repo: string;
    mergeRequestId?: number;
  }): Promise<FileChange[]> {
    if (!parsed.mergeRequestId) {
      throw new Error('GitLab MR ID is required');
    }

    const apiUrl = `https://${parsed.host}/api/v4/projects/${encodeURIComponent(`${parsed.owner}/${parsed.repo}`)}/merge_requests/${parsed.mergeRequestId}/changes`;

    const response = await fetch(apiUrl, {
      headers: this.gitlabToken ? {
        'PRIVATE-TOKEN': this.gitlabToken
      } : {}
    });

    if (!response.ok) {
      throw new Error(`GitLab API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json() as any;
    const changes: FileChange[] = [];

    for (const change of data.changes || []) {
      changes.push({
        path: change.new_path,
        oldContent: change.diff || '',
        newContent: this.reconstructNewContent(change.diff || ''),
        changeType: this.getChangeType(change.new_file, change.deleted_file, change.renamed_file)
      });
    }

    return changes;
  }

  /**
   * 解析 GitHub PR
   */
  private async parseGitHubPR(parsed: {
    host: string;
    owner: string;
    repo: string;
    pullRequestId?: number;
  }): Promise<FileChange[]> {
    if (!parsed.pullRequestId) {
      throw new Error('GitHub PR ID is required');
    }

    const apiUrl = `https://api.github.com/repos/${parsed.owner}/${parsed.repo}/pulls/${parsed.pullRequestId}/files`;

    const response = await fetch(apiUrl, {
      headers: {
        'Accept': 'application/vnd.github.v3+json',
        ...(this.githubToken ? { 'Authorization': `token ${this.githubToken}` } : {})
      }
    });

    if (!response.ok) {
      throw new Error(`GitHub API error: ${response.status} ${response.statusText}`);
    }

    const files = await response.json() as any[];
    const changes: FileChange[] = [];

    for (const file of files) {
      changes.push({
        path: file.filename,
        oldContent: file.patch || '',
        newContent: this.reconstructNewContent(file.patch || ''),
        changeType: file.status as 'added' | 'modified' | 'deleted'
      });
    }

    return changes;
  }

  /**
   * 按文件分割 diff
   */
  private splitDiffByFile(diffContent: string): string[] {
    const files: string[] = [];
    const lines = diffContent.split('\n');
    let currentFile: string[] = [];

    for (const line of lines) {
      if (line.startsWith('diff --git')) {
        if (currentFile.length > 0) {
          files.push(currentFile.join('\n'));
        }
        currentFile = [line];
      } else {
        currentFile.push(line);
      }
    }

    if (currentFile.length > 0) {
      files.push(currentFile.join('\n'));
    }

    return files;
  }

  /**
   * 解析单个文件的 diff
   */
  private parseSingleFileDiff(fileDiff: string): FileChange | null {
    const lines = fileDiff.split('\n');

    let filePath = '';
    let changeType: 'added' | 'modified' | 'deleted' = 'modified';
    let newContent = '';
    let oldContent = '';

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // 提取文件路径
      if (line.startsWith('diff --git')) {
        const match = line.match(/diff --git\s+a\/(.+?)\s+b\/(.+)/);
        if (match) {
          filePath = match[2]; // 使用新路径
        }
      }

      // 检测文件状态
      if (line.startsWith('new file mode')) {
        changeType = 'added';
      } else if (line.startsWith('deleted file mode')) {
        changeType = 'deleted';
      }

      // 提取内容
      if (line.startsWith('+') && !line.startsWith('+++')) {
        newContent += line.substring(1) + '\n';
      } else if (line.startsWith('-') && !line.startsWith('---')) {
        oldContent += line.substring(1) + '\n';
      } else if (!line.startsWith('diff') &&
                 !line.startsWith('index') &&
                 !line.startsWith('---') &&
                 !line.startsWith('+++') &&
                 !line.startsWith('@@') &&
                 !line.startsWith('new file') &&
                 !line.startsWith('deleted file') &&
                 !line.startsWith('Binary')) {
        // 上下文行（既不是添加也不是删除）
        newContent += line.substring(1) + '\n';
        oldContent += line.substring(1) + '\n';
      }
    }

    if (!filePath) {
      return null;
    }

    return {
      path: filePath,
      oldContent: oldContent || undefined,
      newContent,
      changeType
    };
  }

  /**
   * 从 patch 重建新内容
   */
  private reconstructNewContent(patch: string): string {
    const lines = patch.split('\n');
    let newContent = '';

    for (const line of lines) {
      if (line.startsWith('+') && !line.startsWith('+++')) {
        newContent += line.substring(1) + '\n';
      } else if (!line.startsWith('diff') &&
                 !line.startsWith('index') &&
                 !line.startsWith('---') &&
                 !line.startsWith('+++') &&
                 !line.startsWith('@@') &&
                 !line.startsWith('-') &&
                 !line.startsWith('new file') &&
                 !line.startsWith('deleted file') &&
                 !line.startsWith('Binary')) {
        // 上下文行
        newContent += line.substring(1) + '\n';
      }
    }

    return newContent;
  }

  /**
   * 获取变更类型
   */
  private getChangeType(
    isNewFile: boolean,
    isDeletedFile: boolean,
    isRenamedFile: boolean
  ): 'added' | 'modified' | 'deleted' {
    if (isDeletedFile) {
      return 'deleted';
    }
    if (isNewFile || isRenamedFile) {
      return 'added';
    }
    return 'modified';
  }
}

/**
 * 导出便捷函数
 */
export function createDiffParser(tokens?: { gitlab?: string; github?: string }): DiffParser {
  return new DiffParser(tokens);
}
