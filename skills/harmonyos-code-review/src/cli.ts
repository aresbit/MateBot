#!/usr/bin/env node
/**
 * HarmonyOS Code Review CLI
 *
 * 使用方式:
 *   1. 收集 commits 到 CSV:
 *      node dist/cli.js collect --repo <path> --output commits.csv --since "1 week ago"
 *
 *   2. 批量检视 commits:
 *      node dist/cli.js review --repo <path> --csv commits.csv --output reports/
 */
import * as commander from 'commander';
import { collectCommitsToCSV, CollectOptions } from './utils/commit-collector';
import { batchReviewCommits, BatchReviewOptions } from './utils/batch-reviewer';

const program = new commander.Command();

program
  .name('harmonyos-code-review')
  .description('HarmonyOS 代码批量检视工具')
  .version('1.0.0');

/**
 * 收集 commits 命令
 */
program
  .command('collect')
  .description('收集 git commits 并导出到 CSV 文件')
  .requiredOption('--repo <path>', 'Git 仓库路径')
  .requiredOption('--output <path>', '输出 CSV 文件路径')
  .option('--branch <name>', '分支名称', 'HEAD')
  .option('--since <date>', '起始日期 (如 "2024-01-01" 或 "1 week ago")')
  .option('--until <date>', '结束日期')
  .option('--max <number>', '最大收集数量', '100')
  .action(async (options: any) => {
    try {
      const collectOptions: CollectOptions = {
        repoPath: options.repo,
        outputPath: options.output,
        branch: options.branch,
        since: options.since,
        until: options.until,
        maxCount: parseInt(options.max, 10)
      };

      console.log('🔍 开始收集 commits...');
      const commits = collectCommitsToCSV(collectOptions);

      console.log(`\n✅ 成功收集 ${commits.length} 个 commits`);
      console.log(`📄 CSV 文件: ${options.output}`);

    } catch (error) {
      console.error('❌ 收集失败:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

/**
 * 批量检视命令
 */
program
  .command('review')
  .description('从 CSV 文件读取 commit-id 列表并批量检视')
  .requiredOption('--repo <path>', 'Git 仓库路径')
  .requiredOption('--csv <path>', 'CSV 文件路径')
  .requiredOption('--output <dir>', '报告输出目录')
  .option('--exts <extensions>', '文件扩展名 (逗号分隔)', '.ets,.ts')
  .option('--max <number>', '最大检视数量', '50')
  .option('--from <index>', '从第几个开始 (用于断点续检)', '0')
  .action(async (options: any) => {
    try {
      const reviewOptions: BatchReviewOptions = {
        repoPath: options.repo,
        csvPath: options.csv,
        outputDir: options.output,
        fileExtensions: options.exts.split(',').map((e: string) => e.trim()),
        maxCommits: parseInt(options.max, 10),
        startFromIndex: parseInt(options.from, 10)
      };

      console.log('🔍 开始批量检视...');
      const reports = await batchReviewCommits(reviewOptions);

      console.log(`\n✅ 检视完成！`);
      console.log(`📊 共检视 ${reports.length} 个 commits`);
      console.log(`📁 报告目录: ${options.output}`);

    } catch (error) {
      console.error('❌ 检视失败:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

/**
 * 一键执行命令：收集 + 检视
 */
program
  .command('run')
  .description('一键执行：收集 commits 并批量检视')
  .requiredOption('--repo <path>', 'Git 仓库路径')
  .option('--output <dir>', '输出目录', './review-output')
  .option('--since <date>', '起始日期', '1 week ago')
  .option('--max-collect <number>', '最大收集数量', '100')
  .option('--max-review <number>', '最大检视数量', '50')
  .action(async (options: any) => {
    try {
      const csvPath = `${options.output}/commits.csv`;
      const reportDir = `${options.output}/reports`;

      console.log('🚀 一键执行模式\n');

      // 步骤 1: 收集 commits
      console.log('步骤 1/2: 收集 commits...');
      const collectOptions: CollectOptions = {
        repoPath: options.repo,
        outputPath: csvPath,
        since: options.since,
        maxCount: parseInt(options.maxCollect, 10)
      };
      const commits = collectCommitsToCSV(collectOptions);
      console.log(`✅ 收集到 ${commits.length} 个 commits\n`);

      // 步骤 2: 批量检视
      console.log('步骤 2/2: 批量检视...');
      const reviewOptions: BatchReviewOptions = {
        repoPath: options.repo,
        csvPath: csvPath,
        outputDir: reportDir,
        maxCommits: parseInt(options.maxReview, 10)
      };
      const reports = await batchReviewCommits(reviewOptions);
      console.log(`✅ 检视完成！共 ${reports.length} 个 commits\n`);

      console.log('📁 输出文件:');
      console.log(`  - CSV: ${csvPath}`);
      console.log(`  - 报告: ${reportDir}`);

    } catch (error) {
      console.error('❌ 执行失败:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

// 解析命令行参数
program.parse(process.argv);
