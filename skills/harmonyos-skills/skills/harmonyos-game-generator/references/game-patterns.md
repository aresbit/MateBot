# 游戏类型模板

本文档描述常见游戏类型的核心实体和机制，用于指导生成不同主题的游戏。

## 1. 飞行/跳跃类 (如 FlappyBird)

### 核心机制
- 重力下落
- 点击跳跃
- 障碍物躲避
- 通过障碍得分

### 核心实体
```typescript
// 玩家
class Player {
  x: number;
  y: number;
  velocityY: number;  // 垂直速度
  update(deltaTime): void;  // 应用重力
  jump(): void;  // 跳跃
}

// 障碍物
class Obstacle {
  x: number;
  gapY: number;  // 间隙位置
  update(deltaTime): void;  // 向左移动
  isOffScreen(): boolean;
}
```

---

## 2. 贪吃蛇类

### 核心机制
- 方向控制
- 身体跟随
- 食物生成
- 碰撞检测（边界/自身）

### 核心实体
```typescript
// 蛇身段
class SnakeSegment {
  x: number;
  y: number;
}

// 蛇
class Snake {
  segments: SnakeSegment[];
  direction: Direction;
  move(): void;  // 移动
  grow(): void;  // 吃食物后增长
  checkSelfCollision(): boolean;
}

// 食物
class Food {
  x: number;
  y: number;
  respawn(): void;  // 随机生成
}
```

---

## 3. 俄罗斯方块类

### 核心机制
- 方块下落
- 左右移动/旋转
- 行消除
- 游戏加速

### 核心实体
```typescript
// 方块形状
class Tetromino {
  shape: number[][];
  x: number;
  y: number;
  rotation: number;
  rotate(): void;
  moveLeft(): void;
  moveRight(): void;
  drop(): void;
}

// 游戏板
class GameBoard {
  grid: number[][];
  checkCollision(tetromino): boolean;
  merge(tetromino): void;
  clearLines(): number;  // 返回消除行数
}
```

---

## 4. 打砖块类

### 核心机制
- 挡板左右移动
- 球反弹
- 砖块消除
- 关卡递进

### 核心实体
```typescript
// 挡板
class Paddle {
  x: number;
  width: number;
  moveLeft(): void;
  moveRight(): void;
}

// 球
class Ball {
  x: number;
  y: number;
  velocityX: number;
  velocityY: number;
  update(): void;
  bounce(): void;
}

// 砖块
class Brick {
  x: number;
  y: number;
  health: number;  // 生命值
  hit(): void;  // 被击中
}
```

---

## 5. 射击类

### 核心机制
- 玩家移动
- 子弹发射
- 敌人生成
- 碰撞检测

### 核心实体
```typescript
// 玩家
class Player {
  x: number;
  y: number;
  health: number;
  move(direction): void;
  shoot(): Bullet;
}

// 子弹
class Bullet {
  x: number;
  y: number;
  velocityY: number;
  update(): void;
}

// 敌人
class Enemy {
  x: number;
  y: number;
  health: number;
  update(): void;  // 移动模式
}
```

---

## 6. 跑酷类

### 核心机制
- 自动前进
- 跳跃/滑行
- 障碍物躲避
- 收集道具

### 核心实体
```typescript
// 玩家
class Runner {
  y: number;
  velocityY: number;
  isSliding: boolean;
  jump(): void;
  slide(): void;
}

// 障碍物
class Obstacle {
  x: number;
  type: 'low' | 'high';  // 需要跳过或滑过
  update(): void;
}

// 道具
class Collectible {
  x: number;
  y: number;
  value: number;
  update(): void;
}
```

---

## 7. 卡片匹配/记忆类

### 核心机制
- 卡片翻转
- 匹配检测
- 计分计时

### 核心实体
```typescript
// 卡片
class Card {
  id: number;
  pairId: number;
  isFlipped: boolean;
  isMatched: boolean;
  flip(): void;
}

// 游戏板
class MemoryBoard {
  cards: Card[];
  flippedCards: Card[];
  checkMatch(): boolean;
}
```

---

## 游戏常量模板

```typescript
export class GameConstants {
  // 画布尺寸
  static readonly CANVAS_WIDTH: number = 360;
  static readonly CANVAS_HEIGHT: number = 640;

  // 游戏特定常量 (根据游戏类型调整)
  static readonly PLAYER_SIZE: number = 30;
  static readonly MOVE_SPEED: number = 200;
  static readonly GRAVITY: number = 800;

  // 颜色
  static readonly COLOR_BACKGROUND: string = '#87CEEB';
  static readonly COLOR_PLAYER: string = '#FFD700';
  static readonly COLOR_ENEMY: string = '#FF0000';
}
```
