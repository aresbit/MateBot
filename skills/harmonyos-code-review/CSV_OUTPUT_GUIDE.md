# CSV 输出格式指南

## 概述

HarmonyOS 代码审查工具现在支持 CSV 格式输出，每个问题都会精确记录：
- **完整的 commit-id**（40位）
- **文件路径**
- **行号**
- **问题描述**
- **问题级别**

---

## 输出文件

### 1. 单个 Commit 的 CSV 文件

**文件名格式**: `commit-{shortId}-{timestamp}.csv`

**CSV 列**:
```csv
commit-id,file-path,line-number,issue-description,issue-level,rule-name
```

**示例**:
```csv
commit-id,file-path,line-number,issue-description,issue-level,rule-name
580cfbb71afad6c603c1677ad283b91bd4607c73,"entry/src/main/ets/pages/Index.ets",10,"async 函数缺少错误处理，应使用 try-catch 或 .catch()","🟠 高","AsyncErrorHandlingRule"
580cfbb71afad6c603c1677ad283b91bd4607c73,"entry/src/main/ets/pages/Switches.ets",1,"组件包含 7 个状态变量，超过推荐值 5，违反单一职责原则","🟡 中等","SingleResponsibilityRule"
580cfbb71afad6c603c1677ad283b91bd4607c73,"entry/src/main/ets/config/ConfigService.ets",80,"async 函数缺少错误处理，应使用 try-catch 或 .catch()","🟠 高","AsyncErrorHandlingRule"
```

### 2. 汇总 CSV 文件

**文件名格式**: `issues-all-{timestamp}.csv`

**CSV 列**:
```csv
commit-id,commit-short-id,commit-message,commit-author,commit-date,file-path,line-number,issue-description,issue-level,rule-name
```

**示例**:
```csv
commit-id,commit-short-id,commit-message,commit-author,commit-date,file-path,line-number,issue-description,issue-level,rule-name
580cfbb71afad6c603c1677ad283b91bd4607c73,580cfbb,feat: MVVM 架构重构与安全增强,Claude Code,2026-01-25 17:53:03 +0800,"entry/src/main/ets/pages/Index.ets",10,"async 函数缺少错误处理，应使用 try-catch 或 .catch()","🟠 高","AsyncErrorHandlingRule"
580cfbb71afad6c603c1677ad283b91bd4607c73,580cfbb,feat: MVVM 架构重构与安全增强,Claude Code,2026-01-25 17:53:03 +0800,"entry/src/main/ets/pages/Switches.ets",1,"组件包含 7 个状态变量，超过推荐值 5，违反单一职责原则","🟡 中等","SingleResponsibilityRule"
d200494f6d3365d310970875e2ab164f66f8d950,d200494,docs: 更新AI检视提示词,Claude Code,2026-01-27 23:49:41 +0800,"entry/src/main/ets/logic/HaService.ets",194,"async 函数缺少错误处理，应使用 try-catch 或 .catch()","🟠 高","AsyncErrorHandlingRule"
```

---

## CSV 格式规范

### 字段说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| **commit-id** | string | 完整的 40 位 Git commit ID | `580cfbb71afad6c603c1677ad283b91bd4607c73` |
| **commit-short-id** | string | 短 ID（前 7 位） | `580cfbb` |
| **commit-message** | string | 提交消息 | `feat: MVVM 架构重构与安全增强` |
| **commit-author** | string | 提交作者 | `Claude Code` |
| **commit-date** | string | 提交日期 | `2026-01-25 17:53:03 +0800` |
| **file-path** | string | 文件路径（相对于仓库根目录） | `entry/src/main/ets/pages/Index.ets` |
| **line-number** | number | 问题代码的起始行号 | `10` |
| **issue-description** | string | 问题描述 | `async 函数缺少错误处理...` |
| **issue-level** | enum | 问题级别 | `🟠 高` |
| **rule-name** | string | 规则名称 | `AsyncErrorHandlingRule` |

### 问题级别枚举

| 级别 | Emoji | 英文 | 中文 |
|------|-------|------|------|
| 🔴 严重 | 🔴 严重 | CRITICAL | Critical issues |
| 🟠 高 | 🟠 高 | HIGH | High priority issues |
| 🟡 中等 | 🟡 中等 | MEDIUM | Medium priority issues |
| 🟢 轻微 | 🟢 轻微 | LOW | Low priority issues |
| 🔵 提示 | 🔵 提示 | INFO | Info only |

---

## CSV 转义规则

遵循 RFC 4180 CSV 标准：

1. **如果字段包含以下字符，用双引号包裹**：
   - 逗号 (`,`)
   - 双引号 (`"`)
   - 换行符 (`\n` 或 `\r\n`)

2. **双引号转义**：
   - 内部的双引号替换为两个双引号 (`""`)

**示例**:
```
原始文本: async 函数缺少错误处理，应使用 try-catch
转义后:  "async 函数缺少错误处理，应使用 try-catch"

原始文本: 他说 "这是一个问题"
转义后:  "他说 ""这是一个问题"""
```

---

## 使用场景

### 1. 导入到电子表格
```bash
# 在 Excel 中打开
open issues-all-*.csv

# 或使用 Google Sheets
```

### 2. 数据分析
```python
import pandas as pd

# 读取汇总 CSV
df = pd.read_csv('issues-all-xxx.csv')

# 按问题级别统计
print(df['issue-level'].value_counts())

# 按文件统计问题数
print(df['file-path'].value_counts())

# 查找高危问题
critical_issues = df[df['issue-level'] == '🔴 严重']
```

### 3. 生成统计报告
```bash
# 统计各级别问题数量
awk -F',' 'NR>1 {count[$5]++} END {for (level in count) print level, count[level]}' issues-all-*.csv

# 统计每个 commit 的问题数
awk -F',' 'NR>1 {commits[$1]++} END {for (c in commits) print c, commits[c]}' issues-all-*.csv
```

### 4. 问题追踪集成
```javascript
// 读取 CSV 并创建 GitHub Issues
const csv = fs.readFileSync('issues-all-xxx.csv', 'utf-8');
const lines = csv.split('\n').slice(1); // 跳过头部

for (const line of lines) {
  const [commitId, , message, , , filePath, lineNumber, description, level] = line.split(',');

  // 根据问题创建 Issue
  if (level.includes('🔴')) {
    createGitHubIssue({
      title: `[${level}] ${filePath}:${lineNumber}`,
      body: `${description}\n\nCommit: ${commitId}`
    });
  }
}
```

---

## 输出目录结构

```
review-output/
├── commits.csv                           # 输入的 commit 列表
├── reports/
│   ├── commit-580cfbb-1769595167753.md  # Markdown 报告
│   ├── commit-580cfbb-1769595167753.csv  # CSV 报告（单个 commit）
│   ├── commit-d200494-1769595065393.md
│   ├── commit-d200494-1769595065393.csv
│   └── ...
├── summary-1769595065393.md              # Markdown 汇总
└── issues-all-1769595065393.csv          # CSV 汇总（所有问题）
```

---

## 命令行使用

```bash
# 运行批量审查（自动生成 CSV）
npm run review -- --repo /path/to/repo --csv commits.csv --output reports/

# 输出：
# ✅ 检视完成！共生成 3 份报告
# 📁 报告目录: reports/
# 汇总 CSV 文件已保存: reports/issues-all-xxx.csv
```

---

## 注意事项

1. **字符编码**: 所有 CSV 文件使用 UTF-8 编码
2. **换行符**: 使用 Unix 风格的换行符 (`\n`)
3. **空文件**: 如果某个 commit 没有问题，不会生成对应的 CSV 文件
4. **汇总文件**: 即使所有 commit 都没有问题，也会生成空的汇总 CSV（仅包含头部）
