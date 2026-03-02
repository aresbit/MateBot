/**
 * 规则引擎单元测试
 */
import { describe, it, expect, beforeEach } from '@jest/globals';
import { RuleEngine } from '../src/rules/rule-engine';
import { BaseRule } from '../src/rules/base-rule';
import { Rule, RuleIssue, CodeFeatures } from '../src/types';

// 测试规则实现
class TestRule extends BaseRule {
  public testCreateIssue(params: {
    file: string;
    line: number;
    message: string;
    confidence: number;
  }) {
    return this.createIssue(params);
  }

  public testCreateIssueWithFix(params: {
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
  }) {
    return this.createIssueWithFix(params);
  }

  constructor() {
    super({
      id: 'test-rule-1',
      name: '测试规则',
      category: 'arkts',
      severity: 'medium',
      description: '这是一个测试规则'
    });
  }

  check(ast: any, features: CodeFeatures, context: any): any {
    const issues: any[] = [];

    // 简单的检查逻辑
    if (context.fileContent.includes('bad-pattern')) {
      issues.push(this.createIssue({
        file: context.filePath,
        line: 1,
        message: '发现了不好的模式',
        confidence: 1.0
      }));
    }

    return {
      passed: issues.length === 0,
      issues
    };
  }
}

class HighSeverityRule extends BaseRule {
  constructor() {
    super({
      id: 'test-rule-2',
      name: '高严重性规则',
      category: 'security',
      severity: 'high',
      description: '这是一个高严重性规则'
    });
  }

  check(ast: any, features: CodeFeatures, context: any): any {
    return {
      passed: true,
      issues: []
    };
  }
}

describe('BaseRule', () => {
  let rule: TestRule;

  beforeEach(() => {
    rule = new TestRule();
  });

  it('应该创建基本问题', () => {
    const issue = rule.testCreateIssue({
      file: 'test.ets',
      line: 10,
      message: '测试问题',
      confidence: 0.9
    });

    expect(issue.id).toBeDefined();
    expect(issue.rule).toBe('test-rule-1');
    expect(issue.file).toBe('test.ets');
    expect(issue.line).toBe(10);
    expect(issue.message).toBe('测试问题');
    expect(issue.confidence).toBe(0.9);
    expect(issue.severity).toBe('medium');
    expect(issue.category).toBe('arkts');
  });

  it('应该创建带修复建议的问题', () => {
    const issue = rule.testCreateIssueWithFix({
      file: 'test.ets',
      line: 10,
      message: '需要修复',
      confidence: 0.8,
      fix: {
        description: '修复方法',
        codeSnippet: 'const x = 1;',
        verification: '运行测试',
        estimatedTime: '10 分钟'
      }
    });

    expect(issue.fix).toBeDefined();
    expect(issue.fix?.description).toBe('修复方法');
    expect(issue.fix?.codeSnippet).toBe('const x = 1;');
    expect(issue.fix?.verification).toBe('运行测试');
    expect(issue.fix?.estimatedTime).toBe('10 分钟');
  });

  it('应该生成唯一的问题 ID', () => {
    const issue1 = rule.testCreateIssue({
      file: 'test.ets',
      line: 10,
      message: '问题1',
      confidence: 0.9
    });

    const issue2 = rule.testCreateIssue({
      file: 'test.ets',
      line: 11,
      message: '问题2',
      confidence: 0.9
    });

    expect(issue1.id).not.toBe(issue2.id);
  });

  it('应该正确设置规则元数据', () => {
    expect(rule.id).toBe('test-rule-1');
    expect(rule.name).toBe('测试规则');
    expect(rule.category).toBe('arkts');
    expect(rule.severity).toBe('medium');
    expect(rule.description).toBe('这是一个测试规则');
  });
});

describe('RuleEngine', () => {
  let engine: RuleEngine;
  let testRule: TestRule;
  let highSeverityRule: HighSeverityRule;

  beforeEach(() => {
    engine = new RuleEngine();
    testRule = new TestRule();
    highSeverityRule = new HighSeverityRule();
  });

  it('应该注册规则', () => {
    engine.registerRule(testRule);

    const allRules = engine.getAllRules();
    expect(allRules).toHaveLength(1);
    expect(allRules[0]).toBe(testRule);
  });

  it('应该注册多个规则', () => {
    engine.registerRule(testRule);
    engine.registerRule(highSeverityRule);

    const allRules = engine.getAllRules();
    expect(allRules).toHaveLength(2);
  });

  it('应该运行所有规则', async () => {
    engine.registerRule(testRule);
    engine.registerRule(highSeverityRule);

    const mockFeatures: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context = {
      filePath: 'test.ets',
      fileContent: 'good code',
      config: {}
    };

    const issues = await engine.runAllRules(null, mockFeatures, context);

    expect(Array.isArray(issues)).toBe(true);
  });

  it('应该运行指定类别的规则', async () => {
    engine.registerRule(testRule);
    engine.registerRule(highSeverityRule);

    const mockFeatures: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context = {
      filePath: 'test.ets',
      fileContent: 'good code',
      config: {}
    };

    // 只运行 arkts 类别的规则
    const issues = await engine.runRulesByCategory('arkts', null, mockFeatures, context);

    expect(Array.isArray(issues)).toBe(true);
  });

  it('应该运行指定 ID 的规则', async () => {
    engine.registerRule(testRule);
    engine.registerRule(highSeverityRule);

    const mockFeatures: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context = {
      filePath: 'test.ets',
      fileContent: 'good code',
      config: {}
    };

    // 只运行特定规则
    const issues = await engine.runSpecificRules(['test-rule-1'], null, mockFeatures, context);

    expect(Array.isArray(issues)).toBe(true);
  });

  it('应该按类别获取规则', () => {
    engine.registerRule(testRule);
    engine.registerRule(highSeverityRule);

    const arktsRules = engine.getRulesByCategory('arkts');
    expect(arktsRules).toHaveLength(1);
    expect(arktsRules[0]).toBe(testRule);

    const securityRules = engine.getRulesByCategory('security');
    expect(securityRules).toHaveLength(1);
    expect(securityRules[0]).toBe(highSeverityRule);
  });

  it('应该按 ID 获取规则', () => {
    engine.registerRule(testRule);
    engine.registerRule(highSeverityRule);

    const rule = engine.getRuleById('test-rule-1');
    expect(rule).toBe(testRule);

    const notFound = engine.getRuleById('non-existent');
    expect(notFound).toBeUndefined();
  });

  it('应该检测到问题', async () => {
    engine.registerRule(testRule);

    const mockFeatures: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context = {
      filePath: 'test.ets',
      fileContent: 'this has bad-pattern in it',
      config: {}
    };

    const issues = await engine.runAllRules(null, mockFeatures, context);

    expect(issues.length).toBeGreaterThan(0);
    expect(issues[0].message).toBe('发现了不好的模式');
  });

  it('应该处理空规则列表', async () => {
    const mockFeatures: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context = {
      filePath: 'test.ets',
      fileContent: 'code',
      config: {}
    };

    const issues = await engine.runAllRules(null, mockFeatures, context);

    expect(issues).toEqual([]);
  });

  it('应该处理规则检查异常', async () => {
    // 创建一个会抛出异常的规则
    class BadRule extends BaseRule {
      constructor() {
        super({
          id: 'bad-rule',
          name: '坏规则',
          category: 'arkts',
          severity: 'low',
          description: '会抛出异常的规则'
        });
      }

      check(ast: any, features: CodeFeatures, context: any): any {
        throw new Error('检查失败');
        return { passed: true, issues: [] }; // unreachable
      }
    }

    engine.registerRule(new BadRule());

    const mockFeatures: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context = {
      filePath: 'test.ets',
      fileContent: 'code',
      config: {}
    };

    // 不应该抛出异常，应该返回空数组或记录错误
    const issues = await engine.runAllRules(null, mockFeatures, context);

    expect(Array.isArray(issues)).toBe(true);
  });

  it('应该统计规则数量', () => {
    expect(engine.getRuleCount()).toBe(0);

    engine.registerRule(testRule);
    expect(engine.getRuleCount()).toBe(1);

    engine.registerRule(highSeverityRule);
    expect(engine.getRuleCount()).toBe(2);
  });

  it('应该清除所有规则', () => {
    engine.registerRule(testRule);
    engine.registerRule(highSeverityRule);

    expect(engine.getRuleCount()).toBe(2);

    engine.clearRules();
    expect(engine.getRuleCount()).toBe(0);
  });
});
