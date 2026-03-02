/**
 * 规则引擎
 *
 * 负责管理和执行所有代码检查规则
 */
import { BaseRule } from './base-rule';
import { RuleIssue, CodeFeatures, CheckContext } from '../types';

export class RuleEngine {
  private rules: Map<string, BaseRule> = new Map();

  /**
   * 注册规则
   */
  registerRule(rule: BaseRule): void {
    if (this.rules.has(rule.id)) {
      throw new Error(`Rule with id '${rule.id}' already registered`);
    }
    this.rules.set(rule.id, rule);
  }

  /**
   * 批量注册规则
   */
  registerRules(rules: BaseRule[]): void {
    for (const rule of rules) {
      this.registerRule(rule);
    }
  }

  /**
   * 运行所有规则
   */
  async runAllRules(
    ast: any,
    features: CodeFeatures,
    context: CheckContext
  ): Promise<RuleIssue[]> {
    const allIssues: RuleIssue[] = [];

    for (const rule of this.rules.values()) {
      try {
        const result = await this.runRule(rule, ast, features, context);
        allIssues.push(...result);
      } catch (error) {
        console.error(`Error running rule ${rule.id}:`, error);
        // 继续执行其他规则
      }
    }

    return allIssues;
  }

  /**
   * 按类别运行规则
   */
  async runRulesByCategory(
    category: BaseRule['category'],
    ast: any,
    features: CodeFeatures,
    context: CheckContext
  ): Promise<RuleIssue[]> {
    const categoryRules = this.getRulesByCategory(category);
    const issues: RuleIssue[] = [];

    for (const rule of categoryRules) {
      try {
        const result = await this.runRule(rule, ast, features, context);
        issues.push(...result);
      } catch (error) {
        console.error(`Error running rule ${rule.id}:`, error);
      }
    }

    return issues;
  }

  /**
   * 运行指定 ID 的规则
   */
  async runSpecificRules(
    ruleIds: string[],
    ast: any,
    features: CodeFeatures,
    context: CheckContext
  ): Promise<RuleIssue[]> {
    const issues: RuleIssue[] = [];

    for (const ruleId of ruleIds) {
      const rule = this.getRuleById(ruleId);

      if (!rule) {
        console.warn(`Rule '${ruleId}' not found, skipping`);
        continue;
      }

      try {
        const result = await this.runRule(rule, ast, features, context);
        issues.push(...result);
      } catch (error) {
        console.error(`Error running rule ${rule.id}:`, error);
      }
    }

    return issues;
  }

  /**
   * 运行单个规则
   */
  private async runRule(
    rule: BaseRule,
    ast: any,
    features: CodeFeatures,
    context: CheckContext
  ): Promise<RuleIssue[]> {
    const result = rule.check(ast, features, context);

    if (!result.passed && result.issues.length > 0) {
      // 转换为完整的 RuleIssue
      return result.issues.map(issue => ({
        id: `${rule.id}-${Date.now()}-${Math.random()}`,
        rule: rule.id,
        category: rule.category,
        ...issue
      }));
    }

    return [];
  }

  /**
   * 按类别获取规则
   */
  getRulesByCategory(category: BaseRule['category']): BaseRule[] {
    return Array.from(this.rules.values()).filter(rule => rule.category === category);
  }

  /**
   * 按 ID 获取规则
   */
  getRuleById(id: string): BaseRule | undefined {
    return this.rules.get(id);
  }

  /**
   * 获取所有规则
   */
  getAllRules(): BaseRule[] {
    return Array.from(this.rules.values());
  }

  /**
   * 获取规则数量
   */
  getRuleCount(): number {
    return this.rules.size;
  }

  /**
   * 清除所有规则
   */
  clearRules(): void {
    this.rules.clear();
  }

  /**
   * 移除指定规则
   */
  removeRule(id: string): boolean {
    return this.rules.delete(id);
  }

  /**
   * 检查规则是否已注册
   */
  hasRule(id: string): boolean {
    return this.rules.has(id);
  }

  /**
   * 获取所有类别
   */
  getCategories(): BaseRule['category'][] {
    const categories = new Set<BaseRule['category']>();
    for (const rule of this.rules.values()) {
      categories.add(rule.category);
    }
    return Array.from(categories);
  }

  /**
   * 按严重性获取规则
   */
  getRulesBySeverity(severity: BaseRule['severity']): BaseRule[] {
    return Array.from(this.rules.values()).filter(rule => rule.severity === severity);
  }

  /**
   * 获取规则统计信息
   */
  getStatistics() {
    const stats = {
      total: this.rules.size,
      byCategory: {} as Record<string, number>,
      bySeverity: {} as Record<string, number>
    };

    for (const rule of this.rules.values()) {
      // 按类别统计
      stats.byCategory[rule.category] = (stats.byCategory[rule.category] || 0) + 1;
      // 按严重性统计
      stats.bySeverity[rule.severity] = (stats.bySeverity[rule.severity] || 0) + 1;
    }

    return stats;
  }
}
