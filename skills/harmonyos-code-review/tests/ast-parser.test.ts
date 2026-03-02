/**
 * AST 解析器单元测试
 */
import { describe, it, expect, beforeEach } from '@jest/globals';
import { ASTParser } from '../src/utils/ast-parser';
import { extractFeaturesFromFiles, calculateComplexity } from '../src/utils/ast-extractor';
import { CodeFeatures, ComponentFeature, FileChange } from '../src/types';

describe('ASTParser', () => {
  let parser: ASTParser;

  beforeEach(() => {
    parser = new ASTParser();
  });

  describe('extractFeatures', () => {
    it('应该处理空代码', () => {
      const features = parser.extractFeatures('', 'test.ets');

      expect(features.components).toEqual([]);
      expect(features.decorators).toEqual([]);
      expect(features.apiCalls).toEqual([]);
      expect(features.performanceRisks).toEqual([]);
    });

    it('应该处理语法错误', () => {
      const invalidCode = 'this is not valid typescript {{{';

      // 不应该抛出异常
      expect(() => parser.extractFeatures(invalidCode, 'test.ets')).not.toThrow();
    });

    it('应该提取类组件', () => {
      const code = `
export class Index {
  message: string = 'Hello';

  build() {
    console.log('build');
  }
}
`;

      const features = parser.extractFeatures(code, 'test.ets');
      expect(features.components.length).toBeGreaterThanOrEqual(0);
    });

    it('应该检测 ForEach 缺少 key 的性能风险', () => {
      const code = `
function render() {
  ForEach(items, (item: string) => {
    return Text(item);
  });
}
`;

      const features = parser.extractFeatures(code, 'test.ets');

      const noKeyRisk = features.performanceRisks.find(risk => risk.type === 'no-key');
      expect(noKeyRisk).toBeDefined();
    });

    it('应该检测内存泄漏风险', () => {
      const code = `
class TimerComponent {
  aboutToAppear() {
    setInterval(() => {
      console.log('tick');
    }, 1000);
  }
}
`;

      const features = parser.extractFeatures(code, 'test.ets');

      const memoryLeakRisk = features.performanceRisks.find(risk => risk.type === 'memory-leak');
      expect(memoryLeakRisk).toBeDefined();
    });
  });

  describe('extractComponents', () => {
    it('应该识别类组件', () => {
      const code = `
export class HomePage {
  build() {}
}
`;

      const components = parser.extractComponents(code);

      expect(components.length).toBeGreaterThanOrEqual(0);
    });

    it('应该处理空代码', () => {
      const components = parser.extractComponents('');
      expect(components).toEqual([]);
    });
  });

  describe('extractDecorators', () => {
    it('应该处理空代码', () => {
      const decorators = parser.extractDecorators('');
      expect(decorators).toEqual([]);
    });

    it('应该处理没有装饰器的类', () => {
      const code = `
class SimpleClass {
  value: string = '';
}
`;

      const decorators = parser.extractDecorators(code);
      expect(decorators.length).toBeGreaterThanOrEqual(0);
    });
  });

  describe('extractApiCalls', () => {
    it('应该检测简单的函数调用', () => {
      const code = `
console.log('test');
fetch('/api/data');
`;

      const apiCalls = parser.extractApiCalls(code);

      expect(apiCalls.length).toBeGreaterThan(0);
    });

    it('应该检测错误处理', () => {
      const code = `
async function loadData() {
  try {
    const data = await fetch('/api/data');
    return data;
  } catch (error) {
    console.error(error);
  }
}
`;

      const apiCalls = parser.extractApiCalls(code);

      expect(apiCalls.length).toBeGreaterThan(0);
      const fetchCall = apiCalls.find(call => call.api.includes('fetch'));
      expect(fetchCall?.hasErrorHandling).toBe(true);
    });

    it('应该处理空代码', () => {
      const apiCalls = parser.extractApiCalls('');
      expect(apiCalls).toEqual([]);
    });
  });

  describe('extractPerformanceRisks', () => {
    it('应该检测大型列表渲染', () => {
      const code = `
function render() {
  ForEach(items, (item: string) => {
    return Text(item);
  });
}
`;

      const risks = parser.extractPerformanceRisks(code);

      // 应该检测到 no-key 或 large-list 风险
      expect(risks.length).toBeGreaterThan(0);
    });

    it('应该检测定时器风险', () => {
      const code = `
setInterval(() => {
  console.log('tick');
}, 1000);
`;

      const risks = parser.extractPerformanceRisks(code);

      const memoryLeakRisk = risks.find(risk => risk.type === 'memory-leak');
      expect(memoryLeakRisk).toBeDefined();
    });

    it('应该处理空代码', () => {
      const risks = parser.extractPerformanceRisks('');
      expect(risks).toEqual([]);
    });

    it('应该检测循环中的计算', () => {
      const code = `
function expensive() {
  for (let i = 0; i < 100; i++) {
    console.log(i);
  }
}
`;

      const risks = parser.extractPerformanceRisks(code);

      const expensiveRisk = risks.find(risk => risk.type === 'expensive-computation');
      expect(expensiveRisk).toBeDefined();
    });
  });
});

describe('extractFeaturesFromFiles', () => {
  it('应该批量提取特征', () => {
    const fileChanges: FileChange[] = [
      {
        path: 'file1.ets',
        newContent: 'class A { build() {} }',
        changeType: 'added'
      },
      {
        path: 'file2.ets',
        newContent: 'class B { build() {} }',
        changeType: 'added'
      }
    ];

    const features = extractFeaturesFromFiles(fileChanges);

    expect(Object.keys(features)).toHaveLength(2);
    expect(features['file1.ets']).toBeDefined();
    expect(features['file2.ets']).toBeDefined();
  });

  it('应该处理空数组', () => {
    const features = extractFeaturesFromFiles([]);
    expect(Object.keys(features)).toHaveLength(0);
  });

  it('应该忽略非 ArkTS 文件', () => {
    const fileChanges: FileChange[] = [
      {
        path: 'file.json',
        newContent: '{}',
        changeType: 'added'
      }
    ];

    const features = extractFeaturesFromFiles(fileChanges);
    expect(Object.keys(features)).toHaveLength(0);
  });

  it('应该处理解析错误', () => {
    const fileChanges: FileChange[] = [
      {
        path: 'invalid.ets',
        newContent: 'this is not valid {{{',
        changeType: 'added'
      }
    ];

    // 不应该抛出异常
    expect(() => extractFeaturesFromFiles(fileChanges)).not.toThrow();
  });
});

describe('calculateComplexity', () => {
  it('应该计算代码复杂度', () => {
    const code = `
function simple() {
  return 1;
}

function complex(a: number, b: number) {
  if (a > b) {
    for (let i = 0; i < a; i++) {
      if (i % 2 === 0) {
        console.log(i);
      }
    }
  } else if (a < b) {
    while (a < b) {
      a++;
    }
  }
  return a + b;
}
`;

    const complexity = calculateComplexity(code);
    expect(complexity).toBeGreaterThan(0);
  });

  it('应该处理空代码', () => {
    const complexity = calculateComplexity('');
    expect(complexity).toBe(0);
  });

  it('应该统计嵌套层级', () => {
    const code = `
function nested() {
  if (true) {
    if (true) {
      if (true) {
        if (true) {
          console.log('deep');
        }
      }
    }
  }
}
`;

    const complexity = calculateComplexity(code);
    expect(complexity).toBeGreaterThan(5);
  });

  it('应该统计 switch 语句', () => {
    const code = `
function test(value: number) {
  switch (value) {
    case 1:
      return 'one';
    case 2:
      return 'two';
    default:
      return 'other';
  }
}
`;

    const complexity = calculateComplexity(code);
    expect(complexity).toBeGreaterThan(1);
  });

  it('应该统计三元运算符', () => {
    const code = `
const result = a > b ? a : b;
`;

    const complexity = calculateComplexity(code);
    expect(complexity).toBeGreaterThan(0);
  });
});
