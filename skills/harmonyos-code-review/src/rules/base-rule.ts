/**
 * 规则基类
 *
 * 所有代码检查规则都应该继承此类
 */
import { Rule, RuleIssue, RuleCheckResult, CodeFeatures, CheckContext } from '../types';

export abstract class BaseRule implements Rule {
  readonly id: string;
  readonly name: string;
  readonly category: Rule['category'];
  readonly severity: Rule['severity'];
  readonly description: string;
  private issueCounter = 0;

  constructor(config: {
    id: string;
    name: string;
    category: Rule['category'];
    severity: Rule['severity'];
    description: string;
  }) {
    this.id = config.id;
    this.name = config.name;
    this.category = config.category;
    this.severity = config.severity;
    this.description = config.description;
  }

  /**
   * 检查代码（由子类实现）
   */
  abstract check(
    ast: any,
    features: CodeFeatures,
    context: CheckContext
  ): RuleCheckResult;

  /**
   * 创建问题
   */
  protected createIssue(params: {
    file: string;
    line: number;
    message: string;
    confidence: number;
  }): RuleIssue {
    this.issueCounter++;

    return {
      id: `${this.id}-${this.issueCounter}`,
      rule: this.id,
      severity: this.severity,
      category: this.category,
      file: params.file,
      line: params.line,
      message: params.message,
      confidence: params.confidence
    };
  }

  /**
   * 创建带修复建议的问题
   */
  protected createIssueWithFix(params: {
    file: string;
    line: number;
    message: string;
    confidence: number;
    fix: {
      description: string;
      codeSnippet: string;
      verification?: string;
      estimatedTime?: string;
    };
  }): RuleIssue {
    const issue = this.createIssue({
      file: params.file,
      line: params.line,
      message: params.message,
      confidence: params.confidence
    });

    issue.fix = {
      description: params.fix.description,
      codeSnippet: params.fix.codeSnippet,
      verification: params.fix.verification,
      estimatedTime: params.fix.estimatedTime
    };

    return issue;
  }

  /**
   * 获取规则信息
   */
  getInfo() {
    return {
      id: this.id,
      name: this.name,
      category: this.category,
      severity: this.severity,
      description: this.description
    };
  }
}
