# HarmonyOS Skills Collection

HarmonyOS/OpenHarmony 相关的 AI 技能集合，用于 Claude Code 和其他 AI 助手开发 HarmonyOS 应用。

## 📦 包含的技能

### 🎮 harmonyos-game-generator
**HarmonyOS 鸿蒙元服务游戏生成器**

**功能**：
- 创建 MVVM 架构的鸿蒙游戏项目
- 生成完整的游戏框架代码
- 支持多种游戏类型（贪吃蛇、俄罗斯方块、打砖块等）

**使用场景**：
- 创建鸿蒙游戏元服务
- 快速搭建游戏项目框架
- 生成 MVVM 架构代码

**触发场景**：
- "创建一个鸿蒙游戏"
- "生成贪吃蛇游戏代码"
- "帮我搭建俄罗斯方块项目"

### 🧪 harmonyos-test-cases
**HarmonyOS UI 自动化测试用例管理和执行技能**

**功能**：
- 管理自动化测试用例
- 执行测试并生成报告
- 保存测试流程和结果

**使用场景**：
- 运行测试
- 执行测试用例
- 验证功能
- 保存测试流程

**触发场景**：
- "运行 HarmonyOS 测试"
- "执行所有测试用例"
- "验证这个功能"

### 🤖 harmonyos-ui-automator
**HarmonyOS UI 自动化交互技能**

**功能**：
- UI 自动化测试
- 应用操作自动化
- 布局 dump
- 点击、滑动等交互操作

**使用场景**：
- UI 自动化测试
- 应用操作自动化
- dump 布局
- 点击、滑动

**触发场景**：
- "自动化点击这个按钮"
- "dump 当前布局"
- "滑动屏幕"

### 🔧 ohos-app-build-debug
**OHOS 应用编译和调试工具**

**功能**：
- 编译 HarmonyOS 应用
- 安装到设备/模拟器
- 启动应用
- 调试和截图
- 解析崩溃日志

**使用场景**：
- 编译、安装、启动
- 调试
- 截图
- 解析崩溃日志

**触发场景**：
- "编译我的应用"
- "安装到模拟器"
- "启动应用"
- "截图看看效果"

## 🚀 安装到 AI 助手

### 克隆整个技能集合

```bash
git clone https://github.com/aresbit/Matebot.git ~/.claude/skills
```

### 只安装 HarmonyOS 技能

```bash
cd ~/.claude/skills
git clone https://github.com/aresbit/Matebot.git
cp -r ai-skills/harmonyos-skills/* .
```

## 📝 技能结构

```
harmonyos-skills/
├── skills/
│   ├── harmonyos-game-generator/    # 游戏生成器
│   ├── harmonyos-test-cases/        # 测试用例管理
│   ├── harmonyos-ui-automator/      # UI 自动化
│   └── ohos-app-build-debug/       # 编译调试工具
└── README.md
```

## 🔧 技术要求

- HarmonyOS SDK
- DevEco Studio
- hdc 工具（用于设备连接和调试）
- Node.js（某些技能需要）

**最后更新**: 2026-02-25
