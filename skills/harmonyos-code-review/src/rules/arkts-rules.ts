/**
 * ArkTS 特性规则实现
 *
 * 包含 5 条核心规则：
 * 1. AsyncErrorHandlingRule: async 函数必须有错误处理
 * 2. ForEachKeyRule: ForEach 必须有 key 参数
 * 3. TypeDefinitionRule: 禁止使用 any 类型
 * 4. SingleResponsibilityRule: 组件遵循单一职责
 * 5. ApiResponseValidationRule: API 响应必须验证
 */
import { BaseRule } from './base-rule';
import { CodeFeatures, CheckContext } from '../types';

/**
 * Async 函数错误处理规则
 */
export class AsyncErrorHandlingRule extends BaseRule {
  constructor() {
    super({
      id: 'arkts-async-error-handling',
      name: 'Async 函数错误处理',
      category: 'arkts',
      severity: 'high',
      description: 'async 函数必须包含错误处理机制（try-catch 或 .catch()）'
    });
  }

  check(ast: any, features: CodeFeatures, context: CheckContext): any {
    const issues: any[] = [];
    const code = context.fileContent;

    // 查找所有 async 函数
    const asyncFunctionPattern = /async\s+(function\s+\w+|const\s+\w+\s*=\s*(?:\([^)]*\)\s*=>|\w+)|\w+\s*\([^)]*\))/g;
    const matches = code.matchAll(asyncFunctionPattern);

    for (const match of matches) {
      const funcStart = match.index || 0;
      const funcEnd = this.findFunctionEnd(code, funcStart);

      if (funcEnd === -1) continue;

      const funcBody = code.substring(funcStart, funcEnd);

      // 检查是否有 try-catch 或 .catch()
      const hasTryCatch = /\btry\s*{/.test(funcBody) && /\}\s*catch/.test(funcBody);
      const hasCatchCall = /\.catch\s*\(/.test(funcBody);

      if (!hasTryCatch && !hasCatchCall && funcBody.includes('await')) {
        issues.push(this.createIssue({
          file: context.filePath,
          line: this.getLineNumber(code, funcStart),
          message: 'async 函数缺少错误处理，应使用 try-catch 或 .catch()',
          confidence: 0.9
        }));
      }
    }

    return {
      passed: issues.length === 0,
      issues
    };
  }

  private findFunctionEnd(code: string, start: number): number {
    let depth = 0;
    let inString = false;
    let stringChar = '';

    for (let i = start; i < code.length; i++) {
      const char = code[i];

      // 处理字符串
      if ((char === '"' || char === "'" || char === '`') && code[i - 1] !== '\\') {
        if (!inString) {
          inString = true;
          stringChar = char;
        } else if (char === stringChar) {
          inString = false;
        }
      }

      if (!inString) {
        if (char === '{') depth++;
        if (char === '}') {
          depth--;
          if (depth === 0) return i;
        }
      }
    }

    return -1;
  }

  private getLineNumber(code: string, index: number): number {
    return code.substring(0, index).split('\n').length;
  }
}

/**
 * ForEach key 参数规则
 */
export class ForEachKeyRule extends BaseRule {
  constructor() {
    super({
      id: 'arkts-foreach-key',
      name: 'ForEach Key 参数',
      category: 'arkts',
      severity: 'critical',
      description: 'ForEach 必须提供 key 生成函数以避免渲染性能问题'
    });
  }

  check(ast: any, features: CodeFeatures, context: CheckContext): any {
    const issues: any[] = [];
    const code = context.fileContent;

    // 查找 ForEach 调用
    const forEachPattern = /ForEach\s*\(/g;
    const matches = code.matchAll(forEachPattern);

    for (const match of matches) {
      const forEachStart = match.index || 0;
      const forEachEnd = this.findMatchingParen(code, forEachStart + 'ForEach('.length);

      if (forEachEnd === -1) continue;

      const forEachCall = code.substring(forEachStart, forEachEnd);

      // 检查参数数量（应该有 3 个参数）
      const paramCount = this.countParameters(forEachCall);

      if (paramCount < 3) {
        issues.push(this.createIssueWithFix({
          file: context.filePath,
          line: this.getLineNumber(code, forEachStart),
          message: 'ForEach 缺少 key 生成函数，可能导致列表渲染性能问题',
          confidence: 1.0,
          fix: {
            description: '添加 key 生成函数作为第三个参数',
            codeSnippet: 'ForEach(items, (item: Item) => { ... }, (item: Item, index: number) => item.id)',
            estimatedTime: '5 分钟'
          }
        }));
      }
    }

    return {
      passed: issues.length === 0,
      issues
    };
  }

  private findMatchingParen(code: string, start: number): number {
    let depth = 1;
    for (let i = start; i < code.length; i++) {
      if (code[i] === '(') depth++;
      if (code[i] === ')') depth--;
      if (depth === 0) return i;
    }
    return -1;
  }

  private countParameters(forEachCall: string): number {
    const params = forEachCall
      .substring(forEachCall.indexOf('(') + 1, forEachCall.lastIndexOf(')'))
      .split(',');

    // 过滤掉空参数
    return params.filter(p => p.trim().length > 0).length;
  }

  private getLineNumber(code: string, index: number): number {
    return code.substring(0, index).split('\n').length;
  }
}

/**
 * 类型定义规则
 */
export class TypeDefinitionRule extends BaseRule {
  constructor() {
    super({
      id: 'arkts-type-definition',
      name: '禁止使用 any 类型',
      category: 'arkts',
      severity: 'medium',
      description: '禁止使用 any 类型，应使用明确的类型定义或接口'
    });
  }

  check(ast: any, features: CodeFeatures, context: CheckContext): any {
    const issues: any[] = [];
    const code = context.fileContent;

    // 查找 any 类型
    const anyPattern = /:\s*any\b/g;
    const matches = code.matchAll(anyPattern);

    for (const match of matches) {
      const index = match.index || 0;

      // 排除注释中的 any
      if (this.isInComment(code, index)) {
        continue;
      }

      issues.push(this.createIssueWithFix({
        file: context.filePath,
        line: this.getLineNumber(code, index),
        message: '禁止使用 any 类型，请定义明确的类型或接口',
        confidence: 1.0,
        fix: {
          description: '定义接口或使用具体类型替代 any',
          codeSnippet: 'interface DataType { ... }\nconst data: DataType = ...',
          estimatedTime: '10 分钟'
        }
      }));
    }

    return {
      passed: issues.length === 0,
      issues
    };
  }

  private isInComment(code: string, index: number): boolean {
    const before = code.substring(0, index);
    const lines = before.split('\n');
    const currentLine = lines[lines.length - 1];

    return currentLine.trim().startsWith('//');
  }

  private getLineNumber(code: string, index: number): number {
    return code.substring(0, index).split('\n').length;
  }
}

/**
 * 单一职责规则
 */
export class SingleResponsibilityRule extends BaseRule {
  private readonly MAX_STATE_VARS = 5;

  constructor() {
    super({
      id: 'arkts-single-responsibility',
      name: '组件单一职责原则',
      category: 'arkts',
      severity: 'medium',
      description: '组件应遵循单一职责原则，避免管理过多状态'
    });
  }

  check(ast: any, features: CodeFeatures, context: CheckContext): any {
    const issues: any[] = [];
    const code = context.fileContent;

    // 统计 @State 变量数量
    const statePattern = /@State/g;
    const stateCount = (code.match(statePattern) || []).length;

    if (stateCount > this.MAX_STATE_VARS) {
      issues.push(this.createIssueWithFix({
        file: context.filePath,
        line: 1,
        message: `组件包含 ${stateCount} 个状态变量，超过推荐值 ${this.MAX_STATE_VARS}，违反单一职责原则`,
        confidence: 0.8,
        fix: {
          description: '考虑将组件拆分为多个更小的组件，每个组件只负责一个功能',
          codeSnippet: '// 将大组件拆分为多个小组件\n// 使用 @Provide/@Inject 在父子组件间共享状态',
          estimatedTime: '30 分钟'
        }
      }));
    }

    return {
      passed: issues.length === 0,
      issues
    };
  }
}

/**
 * API 响应验证规则
 */
export class ApiResponseValidationRule extends BaseRule {
  constructor() {
    super({
      id: 'arkts-api-response-validation',
      name: 'API 响应验证',
      category: 'arkts',
      severity: 'high',
      description: 'API 响应必须验证状态码和数据结构'
    });
  }

  check(ast: any, features: CodeFeatures, context: CheckContext): any {
    const issues: any[] = [];
    const code = context.fileContent;

    // 查找 fetch 调用
    const fetchPattern = /fetch\s*\(/g;
    const matches = code.matchAll(fetchPattern);

    for (const match of matches) {
      const fetchStart = match.index || 0;

      // 找到包含 fetch 的整个语句块
      const fetchEnd = this.findFetchBlockEnd(code, fetchStart);

      if (fetchEnd === -1) continue;

      const fetchBlock = code.substring(fetchStart, fetchEnd);

      // 检查是否有 response.ok 检查
      const hasResponseCheck = /\b(response|res)\.ok\b/.test(fetchBlock) ||
                              /\.\s*status\s*===?\s*200/.test(fetchBlock);

      // 检查是否有数据验证
      const hasValidation = /\bif\s*\([^)]*\b(data|result)\b/.test(fetchBlock) ||
                           (/\bif\s*\(/.test(fetchBlock) &&
                            (fetchBlock.includes('null') || fetchBlock.includes('undefined') || fetchBlock.includes('!')));

      // 检查是否有类型断言
      const hasTypeAssertion = /\s+as\s+/.test(fetchBlock);

      if (!hasResponseCheck && !hasValidation && !hasTypeAssertion) {
        issues.push(this.createIssueWithFix({
          file: context.filePath,
          line: this.getLineNumber(code, fetchStart),
          message: 'API 调用缺少响应验证，应检查状态码和数据结构',
          confidence: 0.7,
          fix: {
            description: '添加 response 状态检查和数据验证',
            codeSnippet: `const response = await fetch('/api/data');
if (!response.ok) {
  throw new Error('Request failed');
}
const data = await response.json();
if (!data || !data.id) {
  throw new Error('Invalid data');
}`,
            estimatedTime: '15 分钟'
          }
        }));
      }
    }

    return {
      passed: issues.length === 0,
      issues
    };
  }

  private findFetchBlockEnd(code: string, start: number): number {
    // 向前查找函数开始
    let funcStart = start;
    while (funcStart > 0 && !code.substring(funcStart - 100, funcStart).includes('async')) {
      funcStart--;
    }

    // 向后查找函数结束
    let depth = 0;
    let inFunc = false;

    for (let i = funcStart; i < code.length; i++) {
      const char = code[i];

      if (char === '{') {
        depth++;
        inFunc = true;
      }
      if (char === '}') {
        depth--;
        if (inFunc && depth === 0) {
          return i;
        }
      }
    }

    // 如果找不到函数结束，返回一定范围
    return Math.min(start + 1000, code.length);
  }

  private findStatementEnd(code: string, start: number): number {
    // 查找语句结束位置（分号或右括号）
    for (let i = start; i < code.length; i++) {
      if (code[i] === ';') return i;
      if (code[i] === '}') return i;
    }
    return -1;
  }

  private getLineNumber(code: string, index: number): number {
    return code.substring(0, index).split('\n').length;
  }
}
