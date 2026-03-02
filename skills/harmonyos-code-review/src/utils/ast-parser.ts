/**
 * AST 解析器
 *
 * 使用 TypeScript Compiler API 解析 ArkTS 代码，
 * 提取组件特征、装饰器、API 调用和性能风险点
 */
import * as ts from 'typescript';
import { CodeFeatures, ComponentFeature, DecoratorUsage, ApiCall, PerformanceRisk } from '../types';

export class ASTParser {
  /**
   * 提取代码特征
   */
  extractFeatures(code: string, filePath: string): CodeFeatures {
    try {
      const sourceFile = this.createSourceFile(code, filePath);

      return {
        components: this.extractComponents(code),
        decorators: this.extractDecorators(code),
        apiCalls: this.extractApiCalls(code),
        performanceRisks: this.extractPerformanceRisks(code)
      };
    } catch (error) {
      console.error(`Failed to parse ${filePath}:`, error);
      return {
        components: [],
        decorators: [],
        apiCalls: [],
        performanceRisks: []
      };
    }
  }

  /**
   * 提取组件特征
   */
  extractComponents(code: string): ComponentFeature[] {
    const components: ComponentFeature[] = [];
    const sourceFile = this.createSourceFile(code, 'temp.ets');

    const visit = (node: ts.Node) => {
      // ArkTS struct 使用 class 声明
      if (ts.isClassDeclaration(node)) {
        const component = this.analyzeComponent(node);
        if (component) {
          components.push(component);
        }
      }
      ts.forEachChild(node, visit);
    };

    visit(sourceFile);
    return components;
  }

  /**
   * 分析单个组件
   */
  private analyzeComponent(node: ts.ClassDeclaration): ComponentFeature | null {
    const name = node.name?.getText() || 'Anonymous';
    const decorators = ts.getDecorators(node) || [];

    // 判断组件类型
    let type: 'page' | 'component' | 'service' = 'service';
    const hasEntry = decorators.some(d => d.getText().includes('@Entry'));
    const hasComponent = decorators.some(d => d.getText().includes('@Component'));

    if (hasEntry) {
      type = 'page';
    } else if (hasComponent) {
      type = 'component';
    }

    // 检查生命周期方法
    let hasAboutToAppear = false;
    let hasAboutToDisappear = false;

    const members = node.members;
    members.forEach(member => {
      if (ts.isMethodDeclaration(member)) {
        const methodName = member.name?.getText();
        if (methodName === 'aboutToAppear') hasAboutToAppear = true;
        if (methodName === 'aboutToDisappear') hasAboutToDisappear = true;
      }
    });

    // 统计状态管理变量
    let stateVars = 0;
    let propVars = 0;
    let linkVars = 0;

    members.forEach((member: ts.ClassElement) => {
      if (ts.isPropertyDeclaration(member)) {
        const memberDecorators = ts.getDecorators(member) || [];
        memberDecorators.forEach(dec => {
          const text = dec.getText();
          if (text.includes('@State')) stateVars++;
          if (text.includes('@Prop')) propVars++;
          if (text.includes('@Link')) linkVars++;
        });
      }
    });

    return {
      name,
      type,
      lifecycle: {
        hasAboutToAppear,
        hasAboutToDisappear
      },
      stateManagement: {
        stateVars,
        propVars,
        linkVars
      }
    };
  }

  /**
   * 提取装饰器使用
   */
  extractDecorators(code: string): DecoratorUsage[] {
    const decorators: DecoratorUsage[] = [];
    const sourceFile = this.createSourceFile(code, 'temp.ets');

    const visit = (node: ts.Node, line: number = 1) => {
      if (ts.canHaveDecorators(node)) {
        const nodeDecorators = ts.getDecorators(node);
        if (nodeDecorators) {
          nodeDecorators.forEach(dec => {
            const text = dec.getText();
            const type = this.extractDecoratorType(text);
            if (type) {
              let target = '';
              if (ts.isPropertyDeclaration(node) || ts.isMethodDeclaration(node)) {
                target = node.name?.getText() || '';
              }

              decorators.push({
                type: type as any,
                line: sourceFile.getLineAndCharacterOfPosition(dec.getStart()).line + 1,
                target
              });
            }
          });
        }
      }

      const currentLine = sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1;
      ts.forEachChild(node, (child) => visit(child, currentLine));
    };

    visit(sourceFile);
    return decorators;
  }

  /**
   * 提取装饰器类型
   */
  private extractDecoratorType(text: string): string | null {
    const types = ['@State', '@Prop', '@Link', '@Provide', '@Consume', '@Watch', '@Reusable', '@Entry', '@Component', '@Builder'];
    for (const type of types) {
      if (text.includes(type)) {
        return type;
      }
    }
    return null;
  }

  /**
   * 提取 API 调用
   */
  extractApiCalls(code: string): ApiCall[] {
    const apiCalls: ApiCall[] = [];
    const sourceFile = this.createSourceFile(code, 'temp.ets');

    const visit = (node: ts.Node) => {
      // 检测函数调用
      if (ts.isCallExpression(node)) {
        const expression = node.expression;
        let api = '';
        let module = '';

        // 提取 API 名称
        if (ts.isPropertyAccessExpression(expression)) {
          api = expression.name.getText();
          // 尝试提取模块名
          if (ts.isPropertyAccessExpression(expression.expression)) {
            module = expression.expression.name.getText();
          }
        } else if (ts.isIdentifier(expression)) {
          api = expression.getText();
        }

        if (api) {
          const line = sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1;

          // 检查权限检查
          const hasPermissionCheck = this.checkPermissionCheck(node, sourceFile);

          // 检查错误处理
          const hasErrorHandling = this.checkErrorHandling(node, sourceFile);

          apiCalls.push({
            api,
            module,
            line,
            hasPermissionCheck,
            hasErrorHandling
          });
        }
      }

      ts.forEachChild(node, visit);
    };

    visit(sourceFile);
    return apiCalls;
  }

  /**
   * 检查权限检查
   */
  private checkPermissionCheck(node: ts.CallExpression, sourceFile: ts.SourceFile): boolean {
    const text = node.getText();
    return text.includes('checkAccessToken') ||
           text.includes('requestPermissionsFromUser') ||
           text.includes('verifyAccessToken');
  }

  /**
   * 检查错误处理
   */
  private checkErrorHandling(node: ts.CallExpression, sourceFile: ts.SourceFile): boolean {
    // 查找父级 try-catch
    let parent: ts.Node | undefined = node.parent;
    while (parent) {
      if (ts.isTryStatement(parent)) {
        return true;
      }
      // 检查是否有 .catch() 调用
      if (ts.isCallExpression(parent)) {
        const text = parent.expression.getText();
        if (text.includes('.catch') || text.includes('then')) {
          return true;
        }
      }
      parent = parent.parent;
    }
    return false;
  }

  /**
   * 提取性能风险点
   */
  extractPerformanceRisks(code: string): PerformanceRisk[] {
    const risks: PerformanceRisk[] = [];
    const sourceFile = this.createSourceFile(code, 'temp.ets');

    const visit = (node: ts.Node) => {
      // 检测 ForEach 缺少 key
      if (ts.isCallExpression(node)) {
        const expression = node.expression;
        if (ts.isIdentifier(expression) && expression.getText() === 'ForEach') {
          const args = node.arguments;
          if (args.length < 3) {
            risks.push({
              type: 'no-key',
              line: sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1,
              description: 'ForEach 缺少 key 生成函数，可能导致渲染性能问题'
            });
          }

          // 检测大型列表
          if (args.length > 0) {
            const firstArg = args[0];
            const text = firstArg.getText();
            if (text.includes('Array') || text.includes('length') || text.includes('filter')) {
              // 可能是大型数组操作
              risks.push({
                type: 'large-list',
                line: sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1,
                description: '使用 ForEach 渲染大型列表，建议使用 LazyForEach'
              });
            }
          }
        }
      }

      // 检测定时器但缺少清理
      if (ts.isCallExpression(node)) {
        const text = node.expression.getText();
        if (text === 'setInterval' || text === 'setTimeout') {
          risks.push({
            type: 'memory-leak',
            line: sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1,
            description: '使用了定时器但未在 aboutToDisappear 中清理，可能导致内存泄漏'
          });
        }
      }

      // 检测深层嵌套的 UI 结构
      if (ts.isCallExpression(node)) {
        const depth = this.calculateNestingDepth(node);
        if (depth > 5) {
          risks.push({
            type: 'complex-build',
            line: sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1,
            description: `UI 结构嵌套层级过深 (${depth} 层)，建议拆分组件`
          });
        }
      }

      // 检测昂贵的计算
      if (ts.isFunctionDeclaration(node) || ts.isArrowFunction(node)) {
        const hasLoop = this.containsLoop(node);
        if (hasLoop) {
          const line = sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1;
          risks.push({
            type: 'expensive-computation',
            line,
            description: '函数中包含循环，避免在 build() 方法中进行复杂计算'
          });
        }
      }

      ts.forEachChild(node, visit);
    };

    visit(sourceFile);

    // 去重
    const uniqueRisks: PerformanceRisk[] = [];
    const seen = new Set<string>();
    for (const risk of risks) {
      const key = `${risk.line}-${risk.type}`;
      if (!seen.has(key)) {
        seen.add(key);
        uniqueRisks.push(risk);
      }
    }

    return uniqueRisks;
  }

  /**
   * 计算嵌套深度
   */
  private calculateNestingDepth(node: ts.Node, currentDepth: number = 0): number {
    let maxDepth = currentDepth;

    if (ts.isCallExpression(node)) {
      node.arguments.forEach(arg => {
        const depth = this.calculateNestingDepth(arg, currentDepth + 1);
        maxDepth = Math.max(maxDepth, depth);
      });
    }

    return maxDepth;
  }

  /**
   * 检查是否包含循环
   */
  private containsLoop(node: ts.Node): boolean {
    let found = false;
    const visit = (n: ts.Node) => {
      if (ts.isForStatement(n) || ts.isForInStatement(n) || ts.isForOfStatement(n) || ts.isWhileStatement(n)) {
        found = true;
        return;
      }
      ts.forEachChild(n, visit);
    };
    visit(node);
    return found;
  }

  /**
   * 创建 SourceFile
   */
  private createSourceFile(code: string, filePath: string): ts.SourceFile {
    return ts.createSourceFile(
      filePath,
      code,
      ts.ScriptTarget.Latest,
      true,
      ts.ScriptKind.TS
    );
  }
}
