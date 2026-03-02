# HarmonyOS 游戏 MVVM 架构模式

## 架构概述

```
entry/src/main/ets/
├── common/                      # 公共模块
│   ├── constants/
│   │   └── GameConstants.ets    # 游戏常量
│   └── utils/
│       └── MathUtils.ets        # 工具函数
│
├── model/                       # Model层 - 数据与实体
│   ├── entities/                # 游戏实体（纯数据类）
│   │   ├── Player.ets           # 玩家/主角
│   │   ├── Enemy.ets            # 敌人/障碍物
│   │   └── GameState.ets        # 游戏状态枚举
│   └── repository/
│       └── ScoreRepository.ets  # 分数存储
│
├── viewmodel/                   # ViewModel层 - 业务逻辑
│   ├── GameEngine.ets           # 游戏引擎（核心逻辑）
│   └── GameViewModel.ets        # 游戏状态管理
│
├── view/                        # View层 - UI展示
│   ├── pages/
│   │   ├── HomePage.ets         # 首页
│   │   └── GamePage.ets         # 游戏页
│   └── components/
│       └── GameRenderer.ets     # Canvas渲染器
│
└── pages/
    └── Index.ets                # 入口页
```

## 分层职责

| 层 | 职责 | 依赖方向 |
|---|------|---------|
| **Model** | 数据结构定义、持久化 | 无依赖 |
| **ViewModel** | 游戏逻辑、状态管理 | 依赖Model |
| **View** | UI渲染、用户交互 | 依赖ViewModel |

## 迭代开发流程

### 迭代1: 基础架构
- 创建目录结构
- 定义游戏常量
- 定义游戏状态枚举
- **验收**: 编译通过

### 迭代2: Model层
- 定义玩家实体
- 定义敌人/障碍物实体
- **验收**: 实体可实例化

### 迭代3: ViewModel层
- 实现游戏引擎
- 实现状态管理
- **验收**: 逻辑可运行

### 迭代4: View层
- 实现Canvas渲染器
- **验收**: 可绘制静态场景

### 迭代5: 页面整合
- 首页和游戏页
- 分数持久化
- **验收**: 游戏可玩

## 常用 ArkTS 模式

### 响应式状态
```typescript
@Observed
export class GameViewModel {
  @Track score: number = 0;
  @Track gameState: GameState = GameState.IDLE;
}
```

### Canvas 渲染
```typescript
Canvas(this.canvasContext)
  .width(GameConstants.CANVAS_WIDTH)
  .height(GameConstants.CANVAS_HEIGHT)
  .onReady(() => this.startRenderLoop())
  .onClick(() => this.onCanvasClick())
```

### 游戏循环
```typescript
private startRenderLoop(): void {
  setInterval(() => {
    this.render();
  }, 1000 / 60); // 60 FPS
}
```

### 碰撞检测
```typescript
export interface Rect {
  x: number;
  y: number;
  width: number;
  height: number;
}

static checkRectCollision(rect1: Rect, rect2: Rect): boolean {
  return rect1.x < rect2.x + rect2.width &&
         rect1.x + rect1.width > rect2.x &&
         rect1.y < rect2.y + rect2.height &&
         rect1.y + rect1.height > rect2.y;
}
```

### Preferences 持久化
```typescript
import { preferences } from '@kit.ArkData';

this.preferencesStore = await preferences.getPreferences(context, 'game_data');
await this.preferencesStore.put('high_score', score);
await this.preferencesStore.flush();
```
