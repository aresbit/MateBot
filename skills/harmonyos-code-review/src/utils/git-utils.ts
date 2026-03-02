/**
 * Git 工具函数
 */
import * as child_process from 'child_process';

/**
 * 计算变更行数
 */
export function calculateChangeMetrics(diffContent: string): {
  addedLines: number;
  deletedLines: number;
  totalChanges: number;
} {
  const lines = diffContent.split('\n');
  let addedLines = 0;
  let deletedLines = 0;

  for (const line of lines) {
    // 忽略 diff 头部和元数据
    if (line.startsWith('diff --git') ||
        line.startsWith('index ') ||
        line.startsWith('--- ') ||
        line.startsWith('+++ ') ||
        line.startsWith('@@') ||
        line.startsWith('new file') ||
        line.startsWith('deleted file') ||
        line.startsWith('Binary file')) {
      continue;
    }

    // 统计添加的行（以 + 开头，但不是 +++）
    if (line.startsWith('+') && !line.startsWith('+++')) {
      addedLines++;
    }

    // 统计删除的行（以 - 开头，但不是 ---）
    if (line.startsWith('-') && !line.startsWith('---')) {
      deletedLines++;
    }
  }

  return {
    addedLines,
    deletedLines,
    totalChanges: addedLines + deletedLines
  };
}

/**
 * 过滤相关的文件（.ets/.ts/.json 等）
 */
export function filterRelevantFiles(files: string[]): string[] {
  const relevantExtensions = ['.ets', '.ts', '.json', '.js', '.jsx', '.tsx'];

  return files.filter(file => {
    const ext = file.substring(file.lastIndexOf('.'));
    return relevantExtensions.includes(ext);
  });
}

/**
 * 从 Git 仓库获取 diff
 */
export function getGitDiffFromRepo(
  repoPath: string,
  baseBranch: string,
  targetBranch: string,
  extraArgs: string[] = []
): string {
  try {
    const args = [
      'diff',
      `${baseBranch}...${targetBranch}`,
      '--unified=5',
      ...extraArgs
    ];

    const diff = child_process.execSync(
      `git ${args.join(' ')}`,
      {
        cwd: repoPath,
        encoding: 'utf-8',
        maxBuffer: 50 * 1024 * 1024 // 50MB buffer for large diffs
      }
    );

    return diff;
  } catch (error) {
    throw new Error(`Failed to get git diff: ${error instanceof Error ? error.message : String(error)}`);
  }
}

/**
 * 获取两个提交之间的 diff
 */
export function getGitDiffBetweenCommits(
  repoPath: string,
  fromCommit: string,
  toCommit: string,
  filePath?: string
): string {
  try {
    const pathSpec = filePath ? `-- ${filePath}` : '';
    const diff = child_process.execSync(
      `git diff ${fromCommit}..${toCommit} ${pathSpec}`,
      {
        cwd: repoPath,
        encoding: 'utf-8',
        maxBuffer: 50 * 1024 * 1024
      }
    );

    return diff;
  } catch (error) {
    throw new Error(`Failed to get diff between commits: ${error instanceof Error ? error.message : String(error)}`);
  }
}

/**
 * 获取未暂存的更改
 */
export function getUnstagedChanges(repoPath: string, filePath?: string): string {
  try {
    const pathSpec = filePath ? `-- ${filePath}` : '';
    const diff = child_process.execSync(
      `git diff ${pathSpec}`,
      {
        cwd: repoPath,
        encoding: 'utf-8'
      }
    );

    return diff;
  } catch (error) {
    throw new Error(`Failed to get unstaged changes: ${error instanceof Error ? error.message : String(error)}`);
  }
}

/**
 * 获取已暂存但未提交的更改
 */
export function getStagedChanges(repoPath: string, filePath?: string): string {
  try {
    const pathSpec = filePath ? `-- ${filePath}` : '';
    const diff = child_process.execSync(
      `git diff --cached ${pathSpec}`,
      {
        cwd: repoPath,
        encoding: 'utf-8'
      }
    );

    return diff;
  } catch (error) {
    throw new Error(`Failed to get staged changes: ${error instanceof Error ? error.message : String(error)}`);
  }
}
