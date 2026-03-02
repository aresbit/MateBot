/**
 * ArkTS 特性规则单元测试
 */
import { describe, it, expect, beforeEach } from '@jest/globals';
import { AsyncErrorHandlingRule } from '../src/rules/arkts-rules';
import { ForEachKeyRule } from '../src/rules/arkts-rules';
import { TypeDefinitionRule } from '../src/rules/arkts-rules';
import { SingleResponsibilityRule } from '../src/rules/arkts-rules';
import { ApiResponseValidationRule } from '../src/rules/arkts-rules';
import { CodeFeatures, CheckContext } from '../src/types';

describe('AsyncErrorHandlingRule', () => {
  let rule: AsyncErrorHandlingRule;

  beforeEach(() => {
    rule = new AsyncErrorHandlingRule();
  });

  it('应该检测缺少错误处理的 async 函数', () => {
    const code = `
async function fetchData() {
  const result = await fetch('/api/data');
  return result;
}
`;

    const features: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context: CheckContext = {
      filePath: 'test.ets',
      fileContent: code,
      config: {}
    };

    const result = rule.check(null, features, context);

    expect(result.passed).toBe(false);
    expect(result.issues.length).toBeGreaterThan(0);
    expect(result.issues[0].message).toContain('错误处理');
  });

  it('应该通过有 try-catch 的 async 函数', () => {
    const code = `
async function fetchData() {
  try {
    const result = await fetch('/api/data');
    return result;
  } catch (error) {
    console.error(error);
    throw error;
  }
}
`;

    const features: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context: CheckContext = {
      filePath: 'test.ets',
      fileContent: code,
      config: {}
    };

    const result = rule.check(null, features, context);

    expect(result.passed).toBe(true);
    expect(result.issues.length).toBe(0);
  });

  it('应该通过有 .catch() 的 async 函数', () => {
    const code = `
async function fetchData() {
  return fetch('/api/data')
    .then(res => res.json())
    .catch(error => {
      console.error(error);
    });
}
`;

    const features: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context: CheckContext = {
      filePath: 'test.ets',
      fileContent: code,
      config: {}
    };

    const result = rule.check(null, features, context);

    expect(result.passed).toBe(true);
  });
});

describe('ForEachKeyRule', () => {
  let rule: ForEachKeyRule;

  beforeEach(() => {
    rule = new ForEachKeyRule();
  });

  it('应该检测缺少 key 的 ForEach', () => {
    const code = `
ForEach(items, (item: string) => {
  Text(item)
})
`;

    const features: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context: CheckContext = {
      filePath: 'test.ets',
      fileContent: code,
      config: {}
    };

    const result = rule.check(null, features, context);

    expect(result.passed).toBe(false);
    expect(result.issues.length).toBeGreaterThan(0);
    expect(result.issues[0].message).toContain('key');
  });

  it('应该通过有 key 参数的 ForEach', () => {
    const code = `
ForEach(items, (item: string, index: number) => {
  Text(item)
}, (item: string, index: number) => item.id)
`;

    const features: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context: CheckContext = {
      filePath: 'test.ets',
      fileContent: code,
      config: {}
    };

    const result = rule.check(null, features, context);

    expect(result.passed).toBe(true);
  });
});

describe('TypeDefinitionRule', () => {
  let rule: TypeDefinitionRule;

  beforeEach(() => {
    rule = new TypeDefinitionRule();
  });

  it('应该检测 any 类型', () => {
    const code = `
const data: any = fetchSomething();
function process(item: any) {
  return item.value;
}
`;

    const features: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context: CheckContext = {
      filePath: 'test.ets',
      fileContent: code,
      config: {}
    };

    const result = rule.check(null, features, context);

    expect(result.passed).toBe(false);
    expect(result.issues.length).toBeGreaterThan(0);
  });

  it('应该通过明确定义类型的代码', () => {
    const code = `
interface Data {
  value: string;
}
const data: Data = { value: 'test' };
function process(item: Data): string {
  return item.value;
}
`;

    const features: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context: CheckContext = {
      filePath: 'test.ets',
      fileContent: code,
      config: {}
    };

    const result = rule.check(null, features, context);

    expect(result.passed).toBe(true);
  });
});

describe('SingleResponsibilityRule', () => {
  let rule: SingleResponsibilityRule;

  beforeEach(() => {
    rule = new SingleResponsibilityRule();
  });

  it('应该检测职责过多的组件', () => {
    const code = `
class ComplexComponent {
  @State data: string[] = [];
  @State loading: boolean = false;
  @State error: string = '';
  @State currentUser: User | null = null;
  @State settings: Settings = new Settings();
  @State filter: Filter = new Filter();
  @State pagination: Pagination = new Pagination();
  @State selection: Selection = new Selection();
  @State sorting: Sorting = new Sorting();
  @State searchQuery: string = '';
  @State viewMode: 'list' | 'grid' = 'list';
  @State theme: Theme = Theme.Light;

  build() {}
}
`;

    const features: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context: CheckContext = {
      filePath: 'test.ets',
      fileContent: code,
      config: {}
    };

    const result = rule.check(null, features, context);

    expect(result.passed).toBe(false);
    expect(result.issues.length).toBeGreaterThan(0);
    expect(result.issues[0].message).toContain('单一职责');
  });

  it('应该通过职责简单的组件', () => {
    const code = `
class SimpleComponent {
  @State message: string = '';

  build() {}
}
`;

    const features: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context: CheckContext = {
      filePath: 'test.ets',
      fileContent: code,
      config: {}
    };

    const result = rule.check(null, features, context);

    expect(result.passed).toBe(true);
  });
});

describe('ApiResponseValidationRule', () => {
  let rule: ApiResponseValidationRule;

  beforeEach(() => {
    rule = new ApiResponseValidationRule();
  });

  it('应该检测缺少验证的 API 调用', () => {
    const code = `
async function loadData() {
  const response = await fetch('/api/data');
  const data = await response.json();
  return data; // 直接使用，未验证
}
`;

    const features: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context: CheckContext = {
      filePath: 'test.ets',
      fileContent: code,
      config: {}
    };

    const result = rule.check(null, features, context);

    expect(result.passed).toBe(false);
    expect(result.issues.length).toBeGreaterThan(0);
  });

  it('应该通过有验证的 API 调用', () => {
    const code = `
async function loadData() {
  const response = await fetch('/api/data');
  if (!response.ok) {
    throw new Error('Network error');
  }
  const data = await response.json();

  // 验证数据
  if (!data || !data.id) {
    throw new Error('Invalid data');
  }

  return data;
}
`;

    const features: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context: CheckContext = {
      filePath: 'test.ets',
      fileContent: code,
      config: {}
    };

    const result = rule.check(null, features, context);

    expect(result.passed).toBe(true);
  });

  it('应该通过有类型断言的 API 调用', () => {
    const code = `
interface ApiResponse {
  id: number;
  name: string;
}

async function loadData() {
  const response = await fetch('/api/data');
  const data = await response.json() as ApiResponse;

  // 类型断言后使用
  return data.id;
}
`;

    const features: CodeFeatures = {
      components: [],
      decorators: [],
      apiCalls: [],
      performanceRisks: []
    };

    const context: CheckContext = {
      filePath: 'test.ets',
      fileContent: code,
      config: {}
    };

    const result = rule.check(null, features, context);

    expect(result.passed).toBe(true);
  });
});
