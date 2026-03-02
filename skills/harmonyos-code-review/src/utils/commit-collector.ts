/**
 * Git Commit 收集器
 * 用于收集指定时间范围内的 commit 信息并导出到 CSV 文件
 */
import * as child_process from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Commit 信息接口
 */
export interface CommitInfo {
  shortId: string;
  longId: string;
  author: string;
  date: string;
  message: string;
  filesChanged: number;
}

/**
 * 收集选项
 */
export interface CollectOptions {
  repoPath: string;
  branch?: string;
  since?: string; // git date format, e.g. "2024-01-01" or "1 week ago"
  until?: string;
  maxCount?: number;
  outputPath: string;
}

/**
 * Git Commit 收集器类
 */
export class CommitCollector {
  private options: CollectOptions;

  constructor(options: CollectOptions) {
    this.options = {
      branch: 'HEAD',
      ...options
    };
  }

  /**
   * 执行 git 命令
   */
  private execGit(command: string): string {
    try {
      const result = child_process.execSync(command, {
        cwd: this.options.repoPath,
        encoding: 'utf-8',
        maxBuffer: 100 * 1024 * 1024 // 100MB
      });
      return result.trim();
    } catch (error) {
      throw new Error(`Git command failed: ${command}\nError: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * 获取 commit 列表
   */
  collectCommits(): CommitInfo[] {
    const { branch, since, until, maxCount } = this.options;

    // 构建 git log 命令
    let command = `git log ${branch} --pretty=format:"%H|%h|%an|%ad|%s" --date=iso`;

    if (since) {
      command += ` --since="${since}"`;
    }
    if (until) {
      command += ` --until="${until}"`;
    }
    if (maxCount) {
      command += ` -n ${maxCount}`;
    }

    const output = this.execGit(command);

    if (!output) {
      return [];
    }

    const lines = output.split('\n');
    const commits: CommitInfo[] = [];

    for (const line of lines) {
      const parts = line.split('|');
      if (parts.length >= 5) {
        const longId = parts[0];
        const shortId = parts[1];
        const author = parts[2];
        const date = parts[3];
        const message = parts.slice(4).join('|'); // 重建消息（可能包含 |）

        // 获取该 commit 修改的文件数量
        const filesChanged = this.getFilesChangedCount(longId);

        commits.push({
          shortId,
          longId,
          author,
          date,
          message,
          filesChanged
        });
      }
    }

    return commits;
  }

  /**
   * 获取 commit 修改的文件数量
   */
  private getFilesChangedCount(commitId: string): number {
    try {
      const output = this.execGit(`git diff-tree --name-only -r ${commitId}`);
      return output ? output.split('\n').length : 0;
    } catch {
      return 0;
    }
  }

  /**
   * 导出为 CSV 文件
   */
  exportToCSV(commits: CommitInfo[]): void {
    // 确保 CSV 文件的目录存在
    const dir = path.dirname(this.options.outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    // CSV 头部
    const headers = ['short_id', 'long_id', 'author', 'date', 'message', 'files_changed'];

    // CSV 行
    const rows = commits.map(commit => [
      commit.shortId,
      commit.longId,
      this.escapeCSV(commit.author),
      this.escapeCSV(commit.date),
      this.escapeCSV(commit.message),
      commit.filesChanged.toString()
    ]);

    // 写入 CSV
    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n');

    fs.writeFileSync(this.options.outputPath, csvContent, 'utf-8');
  }

  /**
   * 转义 CSV 字段（处理逗号、引号、换行符）
   */
  private escapeCSV(value: string): string {
    // 如果包含逗号、引号或换行符，需要用引号包裹并转义内部引号
    if (value.includes(',') || value.includes('"') || value.includes('\n')) {
      return `"${value.replace(/"/g, '""')}"`;
    }
    return value;
  }

  /**
   * 执行收集并导出
   */
  run(): CommitInfo[] {
    console.log(`开始收集 commits from: ${this.options.repoPath}`);
    const commits = this.collectCommits();
    console.log(`找到 ${commits.length} 个 commits`);

    if (commits.length > 0) {
      this.exportToCSV(commits);
      console.log(`已导出到: ${this.options.outputPath}`);
    }

    return commits;
  }
}

/**
 * 快捷函数：收集 commits 并导出到 CSV
 */
export function collectCommitsToCSV(options: CollectOptions): CommitInfo[] {
  const collector = new CommitCollector(options);
  return collector.run();
}
