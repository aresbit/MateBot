/**
 * AST 代码提取工具
 *
 * 提供批量提取和复杂度计算功能
 */
import { ASTParser } from './ast-parser';
import { FileChange, CodeFeatures } from '../types';

/**
 * 批量从文件变更中提取特征
 */
export function extractFeaturesFromFiles(fileChanges: FileChange[]): Record<string, CodeFeatures> {
  const parser = new ASTParser();
  const features: Record<string, CodeFeatures> = {};

  for (const change of fileChanges) {
    // 只处理 ArkTS 文件
    if (!change.path.endsWith('.ets') && !change.path.endsWith('.ts')) {
      continue;
    }

    try {
      features[change.path] = parser.extractFeatures(change.newContent, change.path);
    } catch (error) {
      console.error(`Failed to extract features from ${change.path}:`, error);
      features[change.path] = {
        components: [],
        decorators: [],
        apiCalls: [],
        performanceRisks: []
      };
    }
  }

  return features;
}

/**
 * 计算代码复杂度
 *
 * 基于圈复杂度（Cyclomatic Complexity）
 */
export function calculateComplexity(code: string): number {
  if (!code || code.trim().length === 0) {
    return 0;
  }

  let complexity = 1; // 基础复杂度

  // 统计控制流语句
  const patterns = [
    /\bif\b/g,
    /\belse\s+if\b/g,
    /\bfor\b/g,
    /\bwhile\b/g,
    /\bswitch\b/g,
    /\bcase\b/g,
    /\bcatch\b/g,
    /\?\s*:/g, // 三元运算符
    /\&\&/g,   // 逻辑与
    /\|\|/g    // 逻辑或
  ];

  for (const pattern of patterns) {
    const matches = code.match(pattern);
    if (matches) {
      complexity += matches.length;
    }
  }

  // 统计嵌套层级（每层增加复杂度）
  const maxNesting = calculateMaxNestingLevel(code);
  complexity += maxNesting * 0.5;

  return Math.round(complexity);
}

/**
 * 计算最大嵌套层级
 */
function calculateMaxNestingLevel(code: string): number {
  const lines = code.split('\n');
  let maxLevel = 0;
  let currentLevel = 0;

  for (const line of lines) {
    const trimmed = line.trim();

    // 增加层级
    if (/^\s*(if|else|for|while|switch|case|try|catch)\b/.test(trimmed)) {
      currentLevel++;
      maxLevel = Math.max(maxLevel, currentLevel);
    }

    // 减少层级（遇到闭合括号）
    const openBraces = (line.match(/{/g) || []).length;
    const closeBraces = (line.match(/}/g) || []).length;
    currentLevel += openBraces - closeBraces;
    currentLevel = Math.max(0, currentLevel);
  }

  return maxLevel;
}

/**
 * 计算函数数量
 */
export function calculateFunctionCount(code: string): number {
  const patterns = [
    /\bfunction\s+\w+/g,
    /\bconst\s+\w+\s*=\s*\([^)]*\)\s*=>/g,
    /\blet\s+\w+\s*=\s*\([^)]*\)\s*=>/g,
    /\w+\s*\([^)]*\)\s*{/g // 方法声明
  ];

  let count = 0;
  for (const pattern of patterns) {
    const matches = code.match(pattern);
    if (matches) {
      count += matches.length;
    }
  }

  return count;
}

/**
 * 计算代码行数
 */
export function calculateLinesOfCode(code: string): {
  total: number;
  code: number;
  comment: number;
  blank: number;
} {
  const lines = code.split('\n');
  let codeLines = 0;
  let commentLines = 0;
  let blankLines = 0;

  for (const line of lines) {
    const trimmed = line.trim();

    if (trimmed.length === 0) {
      blankLines++;
    } else if (trimmed.startsWith('//') || trimmed.startsWith('/*') || trimmed.startsWith('*')) {
      commentLines++;
    } else {
      codeLines++;
    }
  }

  return {
    total: lines.length,
    code: codeLines,
    comment: commentLines,
    blank: blankLines
  };
}

/**
 * 提取导入语句
 */
export function extractImports(code: string): string[] {
  const imports: string[] = [];
  const importPattern = /import\s+{[^}]*}\s+from\s+['"]([^'"]+)['"]/g;

  let match;
  while ((match = importPattern.exec(code)) !== null) {
    imports.push(match[1]);
  }

  return imports;
}

/**
 * 提取导出语句
 */
export function extractExports(code: string): string[] {
  const exports: string[] = [];

  // export const/name/function
  const exportPattern = /export\s+(?:const|let|var|function|class|struct|interface|type)\s+(\w+)/g;
  let match;
  while ((match = exportPattern.exec(code)) !== null) {
    exports.push(match[1]);
  }

  // export { ... }
  const namedExportPattern = /export\s+{([^}]+)}/g;
  while ((match = namedExportPattern.exec(code)) !== null) {
    const names = match[1].split(',').map(n => n.trim().split('as')[0].trim());
    exports.push(...names);
  }

  return exports;
}

/**
 * 分析代码健康度
 */
export function analyzeCodeHealth(code: string): {
  score: number; // 0-100
  issues: string[];
  suggestions: string[];
} {
  const issues: string[] = [];
  const suggestions: string[] = [];
  let score = 100;

  const complexity = calculateComplexity(code);
  const functions = calculateFunctionCount(code);
  const lines = calculateLinesOfCode(code);

  // 复杂度检查
  if (complexity > 20) {
    issues.push(`代码复杂度过高 (${complexity})，建议拆分函数`);
    score -= 20;
  } else if (complexity > 10) {
    issues.push(`代码复杂度较高 (${complexity})`);
    score -= 10;
  }

  // 函数数量检查
  if (functions === 0 && lines.code > 50) {
    issues.push('代码过长但未拆分函数');
    score -= 10;
  }

  // 代码行数检查
  if (lines.code > 500) {
    issues.push('文件过长，建议拆分');
    score -= 10;
  }

  // 注释比例检查
  const commentRatio = lines.comment / lines.total;
  if (commentRatio < 0.1 && lines.code > 100) {
    suggestions.push('建议增加代码注释');
    score -= 5;
  }

  // 导入检查
  const imports = extractImports(code);
  if (imports.length > 20) {
    issues.push('依赖项过多，考虑重构');
    score -= 10;
  }

  // 确保分数在 0-100 之间
  score = Math.max(0, Math.min(100, score));

  return {
    score,
    issues,
    suggestions
  };
}
