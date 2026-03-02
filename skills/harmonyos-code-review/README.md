# HarmonyOS Code Review Skill

从代码质量、bug、性能和安全角度系统审查 HarmonyOS (ArkTS/ArkUI) 项目代码。

## 功能特点

- 🔍 **系统性审查流程** - 按照编译→错误处理→性能→安全→架构的顺序检查
- 🎯 **HarmonyOS 专用** - 针对 ArkTS 和 ArkUI 的特定模式和最佳实践
- 📋 **结构化报告** - 清晰的问题分类和优先级
- ⚡ **快速参考** - 常见问题和修复方案的快速查找表
- 📊 **CSV 导出** - 支持 CSV 格式导出，方便数据分析和处理

## 何时使用

当你需要审查 HarmonyOS 项目代码时:

- ✅ 文件扩展名是 `.ets` 或 `.ts` (在 HarmonyOS 上下文中)
- ✅ 检查 ArkUI 组件实现
- ✅ 审查 async/await 模式
- ✅ 评估状态管理 (`@State`、`@Prop`、`@Provide`)

## 核心审查类别

### 1. 编译与类型(会运行吗?)
- 缺失的接口/类型定义
- 未定义的类型引用
- Props 类型不匹配

### 2. 错误处理(会崩溃吗?)
- async 函数缺少 try-catch
- 状态标志未在 `finally` 中重置
- 缺少错误日志
- 无用户错误反馈

### 3. 性能(会卡顿吗?)
- ForEach 缺少 key 生成器
- 大数据集未分页
- 缺少缓存机制
- 不必要的重新渲染

### 4. 安全(安全吗?)
- API 响应未验证
- 缺少权限检查
- 日志包含敏感信息
- 用户输入未清理

### 5. 架构(可维护吗?)
- 组件职责不明确
- 业务逻辑与展示层混合
- 缺少可复用组件
- 状态管理不当

## 快速示例

### 常见问题 1:缺少错误处理

❌ **错误代码:**
```arkts
async loadData() {
  this.isLoading = true;
  const data = await apiCall();
  this.data = data;
  this.isLoading = false;  // 如果 apiCall 失败,这行永远不执行
}
```

✅ **正确代码:**
```arkts
async loadData() {
  try {
    this.isLoading = true;
    const data = await apiCall();
    this.data = data;
  } catch (error) {
    Logger.error('Failed to load data', error);
  } finally {
    this.isLoading = false;  // 总是执行
  }
}
```

### 常见问题 2:ForEach 缺少 Key

❌ **错误代码:**
```arkts
ForEach(this.items, (item: Item) => {
  ListItem() { Text(item.name) }
})
```

✅ **正确代码:**
```arkts
ForEach(this.items, (item: Item) => {
  ListItem() { Text(item.name) }
}, (item: Item) => item.id)  // 添加 key 生成器
```

### 常见问题 3:缺少数据验证

❌ **错误代码:**
```arkts
this.userList = await UserService.getUsers();  // 直接信任 API 响应
```

✅ **正确代码:**
```arkts
const rawUsers = await UserService.getUsers();
this.userList = this.validateUsers(rawUsers);

private validateUsers(users: any[]): User[] {
  return users.filter(u => u && u.id && u.name);
}
```

## 审查报告格式

```markdown
## 代码审查:[文件名]

### 🔴 严重问题(必须修复)
- **问题**: async 函数缺少错误处理
  - **位置**: 第 15 行
  - **风险**: API 调用失败时应用崩溃
  - **修复**: 添加 try-catch-finally

### 🟡 中等问题(应该修复)
- **问题**: ForEach 缺少 key 生成器
  - **位置**: 第 32 行
  - **风险**: 列表更新时性能差
  - **修复**: 添加第三个参数作为 key 函数

### 🟢 轻微问题(建议修复)
...

### 总结
文件评分:7/10
前 3 个需要解决的问题:
1. 添加错误处理
2. 优化列表性能
3. 验证 API 响应
```

## 使用方法

### 在 Claude Code 中

当你在审查 HarmonyOS 代码时,Claude Code 会自动加载此 skill 并按照结构化流程进行审查。

### 手动参考

1. 阅读 SKILL.md 了解审查原则
2. 使用 review-template.md 创建审查报告
3. 按照优先级修复问题

### 批量审查与 CSV 导出

使用 CLI 工具进行批量审查并导出 CSV 格式:

```bash
# 步骤 1: 收集 commits
npm run collect -- --repo /path/to/repo --output commits.csv --since "1 week ago"

# 步骤 2: 批量审查并生成报告
npm run review -- --repo /path/to/repo --csv commits.csv --output reports/

# 或一键执行
npm run run -- --repo /path/to/repo --output review-output --since "1 week ago"
```

**输出文件**:
- `commit-{id}.md` - 单个 commit 的 Markdown 报告
- `commit-{id}.csv` - 单个 commit 的 CSV 问题清单
- `summary-{timestamp}.md` - 汇总 Markdown 报告
- `issues-all-{timestamp}.csv` - 所有问题汇总 CSV

**CSV 格式**:
```csv
commit-id,commit-short-id,commit-message,commit-author,commit-date,file-path,line-number,issue-description,issue-level,rule-name
580cfbb71afad6c603c1677ad283b91bd4607c73,580cfbb,feat: MVVM 架构重构,Claude Code,2026-01-25 17:53:03 +0800,entry/src/main/ets/pages/Index.ets,10,"async 函数缺少错误处理",🟠 高,AsyncErrorHandlingRule
```

详细说明请参考 [CSV_OUTPUT_GUIDE.md](CSV_OUTPUT_GUIDE.md)

## 文件结构

```
harmonyos-code-review/
├── SKILL.md              # Skill 主文档
├── README.md             # 本文件
└── review-template.md    # 审查报告模板
```

## 常见误区

### ❌ 不要:

- 审查代码时脱离上下文
- 只关注代码风格而忽略功能问题
- 应用其他框架的模式(React/Vue)到 ArkUI
- 只列出问题而不指出好的实践

### ✅ 应该:

- 理解组件层次结构和数据流
- 优先关注崩溃、安全、性能问题
- 遵循 ArkUI 特定模式
- 同时指出好的实践和需要改进的地方

## 高级模式

### ViewModel 模式(推荐)

```arkts
export class UserListViewModel extends Observable {
  @Track userList: User[] = [];
  @Track isLoading: boolean = false;

  async loadUsers(): Promise<void> {
    try {
      this.isLoading = true;
      const rawUsers = await this.userService.getUsers();
      this.userList = this.validateAndTransform(rawUsers);
    } catch (error) {
      Logger.error('Failed to load users', error);
    } finally {
      this.isLoading = false;
    }
  }
}
```

### 自定义 Hooks 模式

```arkts
export function useUserData() {
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  const loadUsers = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await UserService.getUsers();
      setUsers(data);
    } catch (err) {
      setError(err as Error);
      Logger.error('Failed to load users', err);
    } finally {
      setIsLoading(false);
    }
  };

  return { users, isLoading, error, loadUsers };
}
```

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个 skill!

## 许可证

MIT License
