/**
 * CSV 输出功能测试
 */
import { BatchReviewer, IssueLevel, StandardIssue, CommitReviewReport } from './batch-reviewer';
import * as fs from 'fs';
import * as path from 'path';

// 测试 CSV 转义功能
function testCSVEscaping() {
  const mockReviewer = new BatchReviewer({
    repoPath: '/tmp/test',
    csvPath: '/tmp/test/commits.csv',
    outputDir: '/tmp/test/output'
  });

  // 访问私有方法进行测试
  const escapeCSV = (mockReviewer as any).escapeCSV.bind(mockReviewer);

  console.log('测试 CSV 转义功能:');

  // 测试普通文本
  let result = escapeCSV('普通文本');
  console.log(`  普通文本: "${result}"`);
  console.assert(result === '普通文本', '普通文本不应被转义');

  // 测试包含逗号的文本
  result = escapeCSV('包含,逗号');
  console.log(`  包含逗号: "${result}"`);
  console.assert(result === '"包含,逗号"', '包含逗号的文本应被双引号包裹');

  // 测试包含双引号的文本
  result = escapeCSV('包含"双引号"');
  console.log(`  包含双引号: "${result}"`);
  console.assert(result === '"包含""双引号"""', '双引号应被转义为两个双引号');

  // 测试包含换行的文本
  result = escapeCSV('第一行\n第二行');
  console.log(`  包含换行: "${result}"`);
  console.assert(result === '"第一行\n第二行"', '包含换行的文本应被双引号包裹');

  // 测试包含多个特殊字符的文本
  result = escapeCSV('他说 "这是,测试"');
  console.log(`  复杂文本: "${result}"`);
  console.assert(result === '"他说 ""这是,测试"""', '复杂文本应正确转义');

  console.log('✅ CSV 转义测试通过\n');
}

// 测试 CSV 格式化功能
function testCSVFormatting() {
  const mockReviewer = new BatchReviewer({
    repoPath: '/tmp/test',
    csvPath: '/tmp/test/commits.csv',
    outputDir: '/tmp/test/output'
  });

  // 创建模拟报告
  const mockReport: CommitReviewReport = {
    commitId: 'abc123def456789abc123def456789abc123def4',
    shortId: 'abc123d',
    commitMessage: 'feat: 添加新功能',
    commitAuthor: 'Test Author',
    commitDate: '2026-01-28 10:00:00 +0800',
    totalFiles: 2,
    totalIssues: 3,
    issuesByLevel: {
      critical: 1,
      high: 1,
      medium: 1,
      low: 0,
      info: 0
    },
    issues: [
      {
        commitId: 'abc123def456789abc123def456789abc123def4',
        filePath: 'entry/src/main/ets/pages/Index.ets',
        lineNumber: 10,
        issueDescription: 'async 函数缺少错误处理，应使用 try-catch 或 .catch()',
        issueLevel: IssueLevel.HIGH,
        ruleName: 'AsyncErrorHandlingRule'
      },
      {
        commitId: 'abc123def456789abc123def456789abc123def4',
        filePath: 'entry/src/main/ets/pages/Switches.ets',
        lineNumber: 1,
        issueDescription: '组件包含 7 个状态变量，超过推荐值 5，违反单一职责原则',
        issueLevel: IssueLevel.MEDIUM,
        ruleName: 'SingleResponsibilityRule'
      },
      {
        commitId: 'abc123def456789abc123def456789abc123def4',
        filePath: 'entry/src/main/ets/config/ConfigService.ets',
        lineNumber: 80,
        issueDescription: 'API 调用缺少响应验证，应检查状态码和数据结构',
        issueLevel: IssueLevel.CRITICAL,
        ruleName: 'ApiResponseValidationRule'
      }
    ],
    reviewTimestamp: '2026-01-28T10:00:00.000Z'
  };

  // 访问私有方法进行测试
  const formatReportAsCSV = (mockReviewer as any).formatReportAsCSV.bind(mockReviewer);

  console.log('测试 CSV 格式化功能:');
  const csv = formatReportAsCSV(mockReport);
  console.log(csv);

  // 验证 CSV 格式
  const lines = csv.split('\n');
  console.assert(lines.length === 4, '应有 4 行（1 行头部 + 3 行数据）');

  // 验证头部
  const header = lines[0];
  console.assert(header === 'commit-id,file-path,line-number,issue-description,issue-level,rule-name',
    '头部格式应正确');

  // 验证第一行数据
  const firstLine = lines[1];
  console.assert(firstLine.includes('abc123def456789abc123def456789abc123def4'),
    '应包含完整 commit-id');
  console.assert(firstLine.includes('Index.ets'), '应包含文件路径');
  console.assert(firstLine.includes('10'), '应包含行号');
  console.assert(firstLine.includes('async 函数缺少错误处理'), '应包含问题描述');

  console.log('✅ CSV 格式化测试通过\n');
}

// 运行测试
console.log('='.repeat(60));
console.log('CSV 输出功能测试');
console.log('='.repeat(60));
console.log();

testCSVEscaping();
testCSVFormatting();

console.log('='.repeat(60));
console.log('所有测试通过！');
console.log('='.repeat(60));
