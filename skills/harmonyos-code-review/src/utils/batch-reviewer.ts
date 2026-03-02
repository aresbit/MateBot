/**
 * 批量代码检视器
 * 从 CSV 文件读取 commit-id 列表，逐个检视并生成报告
 */
import * as fs from 'fs';
import * as path from 'path';
import * as child_process from 'child_process';
import { RuleEngine } from '../rules/rule-engine';
import { ASTParser } from '../utils/ast-parser';
import { CommitInfo } from './commit-collector';
import {
  AsyncErrorHandlingRule,
  ForEachKeyRule,
  TypeDefinitionRule,
  SingleResponsibilityRule,
  ApiResponseValidationRule
} from '../rules/arkts-rules';

/**
 * 问题级别
 */
export enum IssueLevel {
  CRITICAL = '🔴 严重',
  HIGH = '🟠 高',
  MEDIUM = '🟡 中等',
  LOW = '🟢 轻微',
  INFO = '🔵 提示'
}

/**
 * 标准化问题记录
 */
export interface StandardIssue {
  commitId: string;          // commit-id（完整长ID）
  filePath: string;          // 文件路径
  lineNumber: number;        // 问题代码行号（起始行号）
  issueDescription: string;  // 问题描述
  issueLevel: IssueLevel;    // 问题级别
  ruleName?: string;         // 规则名称
  fixSuggestion?: string;    // 修复建议
}

/**
 * Commit 检视报告
 */
export interface CommitReviewReport {
  commitId: string;          // commit-id
  shortId: string;           // 短ID
  commitMessage: string;     // 提交消息
  commitAuthor: string;      // 提交作者
  commitDate: string;        // 提交日期
  totalFiles: number;        // 检视的文件总数
  totalIssues: number;       // 问题总数
  issuesByLevel: {           // 按级别统计
    critical: number;
    high: number;
    medium: number;
    low: number;
    info: number;
  };
  issues: StandardIssue[];   // 问题列表
  reviewTimestamp: string;   // 检视时间戳
}

/**
 * 批量检视选项
 */
export interface BatchReviewOptions {
  repoPath: string;          // 仓库路径
  csvPath: string;           // CSV 文件路径
  outputDir: string;         // 报告输出目录
  fileExtensions?: string[]; // 要检视的文件扩展名，默认 ['.ets', '.ts']
  maxCommits?: number;       // 最大检视数量
  startFromIndex?: number;   // 从第几个 commit 开始（用于断点续检）
}

/**
 * 从 CSV 读取 commit 列表
 */
function parseCommitCSV(csvPath: string): CommitInfo[] {
  const content = fs.readFileSync(csvPath, 'utf-8');
  const lines = content.split('\n');

  if (lines.length < 2) {
    throw new Error('CSV 文件为空或格式不正确');
  }

  // 跳过头部
  const dataLines = lines.slice(1);
  const commits: CommitInfo[] = [];

  for (const line of dataLines) {
    if (!line.trim()) continue;

    // 解析 CSV 行（处理引号包裹的字段）
    const matches = line.match(/(".*?"|[^",]+)(?=\s*,|\s*$)/g);
    if (!matches || matches.length < 6) continue;

    const cleanField = (field: string) => {
      const trimmed = field.trim();
      if (trimmed.startsWith('"') && trimmed.endsWith('"')) {
        return trimmed.slice(1, -1).replace(/""/g, '"');
      }
      return trimmed;
    };

    commits.push({
      shortId: cleanField(matches[0]),
      longId: cleanField(matches[1]),
      author: cleanField(matches[2]),
      date: cleanField(matches[3]),
      message: cleanField(matches[4]),
      filesChanged: parseInt(cleanField(matches[5]), 10)
    });
  }

  return commits;
}

/**
 * 获取 commit 修改的文件列表
 */
function getCommitFiles(repoPath: string, commitId: string): string[] {
  try {
    const output = child_process.execSync(
      `git diff-tree --no-commit-id --name-only -r ${commitId}`,
      {
        cwd: repoPath,
        encoding: 'utf-8',
        maxBuffer: 100 * 1024 * 1024
      }
    );
    return output.trim().split('\n').filter(f => f);
  } catch (error) {
    console.error(`获取 commit ${commitId} 的文件列表失败:`, error);
    return [];
  }
}

/**
 * 获取文件在指定 commit 中的内容
 */
function getFileAtCommit(repoPath: string, commitId: string, filePath: string): string | null {
  try {
    const output = child_process.execSync(
      `git show ${commitId}:${filePath}`,
      {
        cwd: repoPath,
        encoding: 'utf-8',
        maxBuffer: 50 * 1024 * 1024
      }
    );
    return output;
  } catch (error) {
    // 文件可能在那个 commit 中不存在或被删除
    return null;
  }
}

/**
 * 批量检视器类
 */
export class BatchReviewer {
  private options: Required<BatchReviewOptions>;
  private ruleEngine: RuleEngine;
  private parser: ASTParser;

  constructor(options: BatchReviewOptions) {
    this.options = {
      repoPath: options.repoPath,
      csvPath: options.csvPath,
      outputDir: options.outputDir,
      fileExtensions: options.fileExtensions || ['.ets', '.ts'],
      maxCommits: options.maxCommits || Infinity,
      startFromIndex: options.startFromIndex || 0
    };

    // 确保输出目录存在
    if (!fs.existsSync(this.options.outputDir)) {
      fs.mkdirSync(this.options.outputDir, { recursive: true });
    }

    this.ruleEngine = new RuleEngine();
    this.parser = new ASTParser();

    // 注册所有规则
    this.registerDefaultRules();
  }

  /**
   * 注册默认规则
   */
  private registerDefaultRules(): void {
    this.ruleEngine.registerRule(new AsyncErrorHandlingRule());
    this.ruleEngine.registerRule(new ForEachKeyRule());
    this.ruleEngine.registerRule(new TypeDefinitionRule());
    this.ruleEngine.registerRule(new SingleResponsibilityRule());
    this.ruleEngine.registerRule(new ApiResponseValidationRule());
  }

  /**
   * 检视单个 commit
   */
  async reviewCommit(commit: CommitInfo): Promise<CommitReviewReport> {
    console.log(`\n开始检视 commit: ${commit.shortId} - ${commit.message.substring(0, 50)}...`);

    const issues: StandardIssue[] = [];
    const files = getCommitFiles(this.options.repoPath, commit.longId);

    // 过滤相关文件
    const relevantFiles = files.filter(file => {
      const ext = path.extname(file);
      return this.options.fileExtensions.includes(ext);
    });

    console.log(`  找到 ${relevantFiles.length} 个相关文件`);

    // 检视每个文件
    for (const filePath of relevantFiles) {
      const fileContent = getFileAtCommit(this.options.repoPath, commit.longId, filePath);

      if (!fileContent) {
        console.log(`  跳过 ${filePath} (无法获取内容)`);
        continue;
      }

      console.log(`  检视文件: ${filePath}`);

      try {
        // 提取特征
        const features = this.parser.extractFeatures(fileContent, filePath);

        // 执行所有规则（传入 null 作为 AST，因为规则引擎可能不需要完整的 AST）
        const ruleIssues = await this.ruleEngine.runAllRules(null, features, {
          filePath,
          fileContent,
          repoPath: this.options.repoPath,
          config: {}
        });

        // 转换为标准格式
        for (const issue of ruleIssues) {
          issues.push({
            commitId: commit.longId,
            filePath,
            lineNumber: issue.line || 0,
            issueDescription: issue.message,
            issueLevel: this.mapSeverity(issue.severity),
            ruleName: issue.rule,
            fixSuggestion: issue.fix ? JSON.stringify(issue.fix) : undefined
          });
        }

      } catch (error) {
        console.error(`    检视 ${filePath} 时出错:`, error instanceof Error ? error.message : error);
      }
    }

    // 生成报告
    const report: CommitReviewReport = {
      commitId: commit.longId,
      shortId: commit.shortId,
      commitMessage: commit.message,
      commitAuthor: commit.author,
      commitDate: commit.date,
      totalFiles: relevantFiles.length,
      totalIssues: issues.length,
      issuesByLevel: {
        critical: issues.filter(i => i.issueLevel === IssueLevel.CRITICAL).length,
        high: issues.filter(i => i.issueLevel === IssueLevel.HIGH).length,
        medium: issues.filter(i => i.issueLevel === IssueLevel.MEDIUM).length,
        low: issues.filter(i => i.issueLevel === IssueLevel.LOW).length,
        info: issues.filter(i => i.issueLevel === IssueLevel.INFO).length
      },
      issues,
      reviewTimestamp: new Date().toISOString()
    };

    return report;
  }

  /**
   * 映射严重程度到问题级别
   */
  private mapSeverity(severity: string): IssueLevel {
    switch (severity.toLowerCase()) {
      case 'critical':
      case 'error':
        return IssueLevel.CRITICAL;
      case 'high':
      case 'warning':
        return IssueLevel.HIGH;
      case 'medium':
        return IssueLevel.MEDIUM;
      case 'low':
      case 'info':
        return IssueLevel.LOW;
      default:
        return IssueLevel.INFO;
    }
  }

  /**
   * 保存单个 commit 的检视报告
   */
  saveReport(report: CommitReviewReport): string[] {
    const savedFiles: string[] = [];

    // 保存 Markdown 格式
    const mdFilename = `commit-${report.shortId}-${Date.now()}.md`;
    const mdFilePath = path.join(this.options.outputDir, mdFilename);
    const mdContent = this.formatReportAsMarkdown(report);
    fs.writeFileSync(mdFilePath, mdContent, 'utf-8');
    savedFiles.push(mdFilePath);

    // 保存 CSV 格式（如果有问题）
    if (report.issues.length > 0) {
      const csvFilename = `commit-${report.shortId}-${Date.now()}.csv`;
      const csvFilePath = path.join(this.options.outputDir, csvFilename);
      const csvContent = this.formatReportAsCSV(report);
      fs.writeFileSync(csvFilePath, csvContent, 'utf-8');
      savedFiles.push(csvFilePath);
      console.log(`  CSV 报告已保存: ${csvFilePath}`);
    }

    console.log(`  报告已保存: ${mdFilePath}`);
    return savedFiles;
  }

  /**
   * 格式化为 CSV
   * CSV 格式: commit-id,文件路径,行号,问题描述,问题级别,规则名称
   */
  private formatReportAsCSV(report: CommitReviewReport): string {
    const lines: string[] = [];

    // CSV 头部
    lines.push('commit-id,file-path,line-number,issue-description,issue-level,rule-name');

    // 每个问题一行
    for (const issue of report.issues) {
      // 转义 CSV 字段（处理逗号、引号、换行）
      const commitId = issue.commitId;
      const filePath = this.escapeCSV(issue.filePath);
      const lineNumber = issue.lineNumber;
      const description = this.escapeCSV(issue.issueDescription);
      const level = this.escapeCSV(issue.issueLevel);
      const ruleName = this.escapeCSV(issue.ruleName || 'N/A');

      lines.push(`${commitId},${filePath},${lineNumber},${description},${level},${ruleName}`);
    }

    return lines.join('\n');
  }

  /**
   * 转义 CSV 特殊字符
   * 如果字段包含逗号、引号或换行，用双引号包裹，并转义内部的双引号
   */
  private escapeCSV(text: string): string {
    if (!text) return '""';

    // 如果包含逗号、双引号、换行符，需要用双引号包裹
    if (text.includes(',') || text.includes('"') || text.includes('\n') || text.includes('\r')) {
      // 将内部的双引号转义为两个双引号
      const escaped = text.replace(/"/g, '""');
      return `"${escaped}"`;
    }

    return text;
  }

  /**
   * 格式化为 Markdown
   */
  private formatReportAsMarkdown(report: CommitReviewReport): string {
    const lines: string[] = [];

    // 标题
    lines.push(`# Commit 检视报告`);
    lines.push();
    lines.push(`## Commit 信息`);
    lines.push();
    lines.push(`| 字段 | 值 |`);
    lines.push(`|------|-----|`);
    lines.push(`| **Commit ID** | \`${report.commitId}\` |`);
    lines.push(`| **短 ID** | \`${report.shortId}\` |`);
    lines.push(`| **提交消息** | ${this.escapeMarkdown(report.commitMessage)} |`);
    lines.push(`| **提交作者** | ${this.escapeMarkdown(report.commitAuthor)} |`);
    lines.push(`| **提交日期** | ${report.commitDate} |`);
    lines.push(`| **检视时间** | ${report.reviewTimestamp} |`);
    lines.push();

    // 统计
    lines.push(`## 检视统计`);
    lines.push();
    lines.push(`| 指标 | 数量 |`);
    lines.push(`|------|------|`);
    lines.push(`| **检视文件数** | ${report.totalFiles} |`);
    lines.push(`| **问题总数** | ${report.totalIssues} |`);
    lines.push(`| **🔴 严重** | ${report.issuesByLevel.critical} |`);
    lines.push(`| **🟠 高** | ${report.issuesByLevel.high} |`);
    lines.push(`| **🟡 中等** | ${report.issuesByLevel.medium} |`);
    lines.push(`| **🟢 轻微** | ${report.issuesByLevel.low} |`);
    lines.push(`| **🔵 提示** | ${report.issuesByLevel.info} |`);
    lines.push();

    // 问题列表
    if (report.issues.length > 0) {
      lines.push(`## 问题清单`);
      lines.push();

      // CSV 格式表格
      lines.push(`| Commit ID | 文件路径 | 行号 | 问题描述 | 问题级别 |`);
      lines.push(`|-----------|----------|------|----------|----------|`);

      for (const issue of report.issues) {
        lines.push(
          `| ${issue.commitId.substring(0, 8)} | ` +
          `\`${issue.filePath}\` | ` +
          `${issue.lineNumber} | ` +
          `${this.escapeMarkdown(issue.issueDescription)} | ` +
          `${issue.issueLevel} |`
        );
      }

      lines.push();

      // 按级别分组的问题详情
      const grouped = this.groupIssuesByLevel(report.issues);

      for (const [level, issues] of Object.entries(grouped)) {
        if (issues.length > 0) {
          lines.push(`### ${level}`);
          lines.push();

          for (const issue of issues) {
            lines.push(`#### ${issue.filePath}:${issue.lineNumber}`);
            lines.push();
            lines.push(`- **Commit ID**: \`${issue.commitId}\``);
            lines.push(`- **行号**: ${issue.lineNumber}`);
            lines.push(`- **规则**: ${issue.ruleName || 'N/A'}`);
            lines.push(`- **级别**: ${issue.issueLevel}`);
            lines.push(`- **问题描述**: ${issue.issueDescription}`);
            if (issue.fixSuggestion) {
              lines.push(`- **修复建议**: ${issue.fixSuggestion}`);
            }
            lines.push();
          }
        }
      }
    } else {
      lines.push(`## ✅ 未发现问题`);
      lines.push();
      lines.push(`该 commit 的所有检视文件均未发现明显问题。`);
      lines.push();
    }

    return lines.join('\n');
  }

  /**
   * 转义 Markdown 特殊字符
   */
  private escapeMarkdown(text: string): string {
    return text.replace(/[|*`\\_{}[\]()#+\-.!]/g, '\\$&');
  }

  /**
   * 按级别分组问题
   */
  private groupIssuesByLevel(issues: StandardIssue[]): Record<string, StandardIssue[]> {
    const grouped: Record<string, StandardIssue[]> = {
      '🔴 严重问题': [],
      '🟠 高危问题': [],
      '🟡 中等问题': [],
      '🟢 轻微问题': [],
      '🔵 提示': []
    };

    for (const issue of issues) {
      const key = issue.issueLevel;
      if (key in grouped) {
        grouped[key].push(issue);
      }
    }

    return grouped;
  }

  /**
   * 运行批量检视
   */
  async run(): Promise<CommitReviewReport[]> {
    console.log(`开始批量检视...`);
    console.log(`CSV 文件: ${this.options.csvPath}`);
    console.log(`输出目录: ${this.options.outputDir}`);
    console.log();

    // 读取 commit 列表
    const commits = parseCommitCSV(this.options.csvPath);
    console.log(`从 CSV 读取到 ${commits.length} 个 commits`);

    // 应用范围限制
    const startIndex = Math.max(0, this.options.startFromIndex);
    const endIndex = Math.min(commits.length, startIndex + this.options.maxCommits);
    const commitsToReview = commits.slice(startIndex, endIndex);

    console.log(`将检视第 ${startIndex + 1} 到第 ${endIndex} 个 commit（共 ${commitsToReview.length} 个）`);
    console.log();

    // 逐个检视
    const reports: CommitReviewReport[] = [];

    for (let i = 0; i < commitsToReview.length; i++) {
      const commit = commitsToReview[i];
      console.log(`[${i + 1}/${commitsToReview.length}] 检视 commit ${commit.shortId}`);

      try {
        const report = await this.reviewCommit(commit);
        reports.push(report);

        // 立即保存报告
        this.saveReport(report);

      } catch (error) {
        console.error(`检视 commit ${commit.shortId} 失败:`, error);
      }
    }

    // 生成汇总报告
    this.generateSummaryReport(reports);

    // 生成汇总 CSV 文件
    this.generateCSVSummary(reports);

    console.log();
    console.log(`批量检视完成！共生成 ${reports.length} 份报告`);
    console.log(`报告目录: ${this.options.outputDir}`);

    return reports;
  }

  /**
   * 生成汇总报告
   */
  private generateSummaryReport(reports: CommitReviewReport[]): void {
    const summaryPath = path.join(this.options.outputDir, `summary-${Date.now()}.md`);

    const lines: string[] = [];
    lines.push(`# 批量检视汇总报告`);
    lines.push();
    lines.push(`## 概览`);
    lines.push();
    lines.push(`| 指标 | 数量 |`);
    lines.push(`|------|------|`);
    lines.push(`| **检视 Commit 数** | ${reports.length} |`);
    lines.push(`| **总文件数** | ${reports.reduce((sum, r) => sum + r.totalFiles, 0)} |`);
    lines.push(`| **总问题数** | ${reports.reduce((sum, r) => sum + r.totalIssues, 0)} |`);
    lines.push();

    // 按级别统计
    const totalByLevel = {
      critical: reports.reduce((sum, r) => sum + r.issuesByLevel.critical, 0),
      high: reports.reduce((sum, r) => sum + r.issuesByLevel.high, 0),
      medium: reports.reduce((sum, r) => sum + r.issuesByLevel.medium, 0),
      low: reports.reduce((sum, r) => sum + r.issuesByLevel.low, 0),
      info: reports.reduce((sum, r) => sum + r.issuesByLevel.info, 0)
    };

    lines.push(`### 问题级别分布`);
    lines.push();
    lines.push(`| 级别 | 数量 |`);
    lines.push(`|------|------|`);
    lines.push(`| 🔴 严重 | ${totalByLevel.critical} |`);
    lines.push(`| 🟠 高 | ${totalByLevel.high} |`);
    lines.push(`| 🟡 中等 | ${totalByLevel.medium} |`);
    lines.push(`| 🟢 轻微 | ${totalByLevel.low} |`);
    lines.push(`| 🔵 提示 | ${totalByLevel.info} |`);
    lines.push();

    // 每个 commit 的摘要
    lines.push(`## Commit 检视摘要`);
    lines.push();
    lines.push(`| Commit ID | 消息 | 作者 | 文件数 | 问题数 | 严重 | 高 | 中 | 低 |`);
    lines.push(`|-----------|------|------|--------|--------|------|-----|-----|-----|`);

    for (const report of reports) {
      const msg = report.commitMessage.substring(0, 30) + (report.commitMessage.length > 30 ? '...' : '');
      lines.push(
        `| ${report.shortId} | ` +
        `${this.escapeMarkdown(msg)} | ` +
        `${this.escapeMarkdown(report.commitAuthor)} | ` +
        `${report.totalFiles} | ` +
        `${report.totalIssues} | ` +
        `${report.issuesByLevel.critical} | ` +
        `${report.issuesByLevel.high} | ` +
        `${report.issuesByLevel.medium} | ` +
        `${report.issuesByLevel.low} |`
      );
    }

    fs.writeFileSync(summaryPath, lines.join('\n'), 'utf-8');
    console.log(`汇总报告已保存: ${summaryPath}`);
  }

  /**
   * 生成汇总 CSV 文件
   * 包含所有 commit 的所有问题
   */
  generateCSVSummary(reports: CommitReviewReport[]): string {
    const csvPath = path.join(this.options.outputDir, `issues-all-${Date.now()}.csv`);

    const lines: string[] = [];

    // CSV 头部
    lines.push('commit-id,commit-short-id,commit-message,commit-author,commit-date,file-path,line-number,issue-description,issue-level,rule-name');

    // 收集所有问题
    for (const report of reports) {
      if (report.issues.length === 0) continue;

      for (const issue of report.issues) {
        const commitId = issue.commitId;
        const shortId = report.shortId;
        const message = this.escapeCSV(report.commitMessage);
        const author = this.escapeCSV(report.commitAuthor);
        const date = report.commitDate;
        const filePath = this.escapeCSV(issue.filePath);
        const lineNumber = issue.lineNumber;
        const description = this.escapeCSV(issue.issueDescription);
        const level = this.escapeCSV(issue.issueLevel);
        const ruleName = this.escapeCSV(issue.ruleName || 'N/A');

        lines.push(`${commitId},${shortId},${message},${author},${date},${filePath},${lineNumber},${description},${level},${ruleName}`);
      }
    }

    // 保存汇总 CSV
    const content = lines.join('\n');
    fs.writeFileSync(csvPath, content, 'utf-8');
    console.log(`汇总 CSV 文件已保存: ${csvPath}`);

    return csvPath;
  }
}

/**
 * 快捷函数：批量检视 commits
 */
export async function batchReviewCommits(options: BatchReviewOptions): Promise<CommitReviewReport[]> {
  const reviewer = new BatchReviewer(options);
  return await reviewer.run();
}
