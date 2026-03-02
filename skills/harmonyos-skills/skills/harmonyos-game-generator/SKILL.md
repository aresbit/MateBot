---
name: harmonyos-game-generator
description: |
  HarmonyOS 鸿蒙元服务游戏生成器。根据指定游戏主题，自动创建 MVVM 架构的鸿蒙游戏项目。

  使用场景:
  - 用户想要创建新的鸿蒙游戏元服务
  - 用户提到游戏主题如 "贪吃蛇"、"俄罗斯方块"、"打砖块" 等
  - 用户说 "帮我创建一个XX游戏"
  - 用户想要基于 MVVM 架构开发鸿蒙游戏

  触发词: 创建游戏、鸿蒙游戏、元服务游戏、HarmonyOS 游戏、MVVM 游戏
---

# HarmonyOS 游戏生成器

自动生成 MVVM 架构的鸿蒙元服务游戏，支持任意游戏主题。

## 工作流程

```
用户输入游戏主题
    ↓
1. 创建 MVVM 目录结构
    ↓
2. 生成基础代码框架 (5次迭代)
    ↓
3. 根据主题定制游戏逻辑
    ↓
4. 编译验证
    ↓
5. 部署到模拟器
    ↓
6. 初始化 Git 并推送到 GitHub
```

## 快速开始

```bash
# 用户请求示例
"帮我创建一个贪吃蛇鸿蒙游戏"
"创建一个俄罗斯方块元服务"
```

执行步骤:

### 1. 生成游戏框架

```bash
python3 $SKILL_DIR/scripts/generate_game.py <项目路径> --theme <游戏主题>
```

参数说明:
- `项目路径`: HarmonyOS 元服务工程根目录
- `--theme/-t`: 游戏主题 (snake, tetris, breakout, flappy, runner, shooter 或任意主题)
- `--name/-n`: 游戏名称 (可选)

### 2. 完善游戏逻辑

根据游戏主题，完善以下内容:
- 游戏实体 (Model层)
- 游戏引擎逻辑 (ViewModel层)
- 渲染器绘制 (View层)

参考 `references/game-patterns.md` 了解不同游戏类型的核心机制。

### 3. 编译部署

```bash
python3 $SKILL_DIR/scripts/build_and_deploy.py <项目路径>
```

### 4. Git 和 GitHub

```bash
python3 $SKILL_DIR/scripts/git_setup.py <项目路径> --name <游戏名称>
```

## MVVM 架构

详细架构说明见 `references/mvvm-architecture.md`

```
entry/src/main/ets/
├── common/
│   ├── constants/GameConstants.ets    # 游戏常量
│   └── utils/MathUtils.ets            # 工具函数
├── model/
│   ├── entities/                       # 游戏实体
│   └── repository/ScoreRepository.ets  # 分数持久化
├── viewmodel/
│   ├── GameEngine.ets                  # 游戏引擎
│   └── GameViewModel.ets               # 状态管理
├── view/
│   ├── pages/                          # 页面
│   └── components/GameRenderer.ets     # 渲染器
└── pages/Index.ets                     # 入口页
```

## 迭代开发

采用小步快跑，5次迭代:

| 迭代 | 内容 | 验收标准 |
|-----|------|---------|
| 1 | 基础架构 | 编译通过 |
| 2 | Model层 | 实体可实例化 |
| 3 | ViewModel层 | 逻辑可运行 |
| 4 | View层 | 可绘制静态场景 |
| 5 | 页面整合 | 游戏可玩 |

## 游戏类型参考

见 `references/game-patterns.md`，包含:
- 飞行/跳跃类 (FlappyBird)
- 贪吃蛇类
- 俄罗斯方块类
- 打砖块类
- 射击类
- 跑酷类
- 卡片匹配类

## 脚本说明

| 脚本 | 用途 |
|-----|------|
| `generate_game.py` | 生成 MVVM 架构代码框架 |
| `build_and_deploy.py` | 编译并部署到设备 |
| `git_setup.py` | Git 初始化和 GitHub 推送 |

## 依赖

- DevEco Studio (提供 hvigorw, hdc 工具)
- GitHub CLI (gh 命令)
- Python 3.7+
