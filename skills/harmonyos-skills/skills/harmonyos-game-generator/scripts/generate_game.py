#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HarmonyOS 游戏生成器 - 主生成脚本
根据游戏主题自动生成 MVVM 架构的鸿蒙游戏代码
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='HarmonyOS Game Generator - 生成 MVVM 架构的鸿蒙游戏'
    )
    parser.add_argument(
        'project_path',
        help='项目路径 (HarmonyOS 元服务工程根目录)'
    )
    parser.add_argument(
        '--theme', '-t',
        required=True,
        help='游戏主题 (如: snake, tetris, breakout, flappy)'
    )
    parser.add_argument(
        '--name', '-n',
        help='游戏名称 (默认使用主题名)'
    )
    parser.add_argument(
        '--package',
        help='包名 (默认自动生成)'
    )
    return parser.parse_args()


def get_game_config(theme: str) -> dict:
    """根据游戏主题获取配置"""
    configs = {
        'flappy': {
            'name': 'FlappyBird',
            'entities': ['Bird', 'Pipe'],
            'mechanics': ['gravity', 'jump', 'obstacle_avoid'],
            'controls': 'tap',
        },
        'snake': {
            'name': 'SnakeGame',
            'entities': ['Snake', 'Food'],
            'mechanics': ['direction_move', 'grow', 'self_collision'],
            'controls': 'swipe',
        },
        'tetris': {
            'name': 'TetrisGame',
            'entities': ['Tetromino', 'GameBoard'],
            'mechanics': ['fall', 'rotate', 'line_clear'],
            'controls': 'swipe',
        },
        'breakout': {
            'name': 'BreakoutGame',
            'entities': ['Paddle', 'Ball', 'Brick'],
            'mechanics': ['paddle_move', 'ball_bounce', 'brick_break'],
            'controls': 'swipe',
        },
        'runner': {
            'name': 'RunnerGame',
            'entities': ['Runner', 'Obstacle', 'Collectible'],
            'mechanics': ['auto_scroll', 'jump', 'slide', 'collect'],
            'controls': 'tap',
        },
        'shooter': {
            'name': 'ShooterGame',
            'entities': ['Player', 'Bullet', 'Enemy'],
            'mechanics': ['move', 'shoot', 'enemy_spawn'],
            'controls': 'tap_swipe',
        },
    }

    # 尝试匹配已知主题
    theme_lower = theme.lower()
    for key, config in configs.items():
        if key in theme_lower or theme_lower in key:
            return config

    # 未知主题，返回通用配置
    return {
        'name': theme.capitalize() + 'Game',
        'entities': ['Player', 'Enemy'],
        'mechanics': ['move', 'collision'],
        'controls': 'tap',
    }


def create_directory_structure(project_path: str) -> dict:
    """创建 MVVM 目录结构"""
    ets_path = Path(project_path) / 'entry/src/main/ets'

    dirs = {
        'common_constants': ets_path / 'common/constants',
        'common_utils': ets_path / 'common/utils',
        'model_entities': ets_path / 'model/entities',
        'model_repository': ets_path / 'model/repository',
        'viewmodel': ets_path / 'viewmodel',
        'view_pages': ets_path / 'view/pages',
        'view_components': ets_path / 'view/components',
    }

    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)

    return dirs


def generate_game_constants(dirs: dict, config: dict, theme: str):
    """生成游戏常量文件"""
    content = f'''/**
 * {config['name']} 游戏常量定义
 */
export class GameConstants {{
  // 画布尺寸
  static readonly CANVAS_WIDTH: number = 360;
  static readonly CANVAS_HEIGHT: number = 640;

  // 玩家属性
  static readonly PLAYER_SIZE: number = 30;
  static readonly PLAYER_SPEED: number = 200;

  // 游戏规则
  static readonly SCORE_PER_HIT: number = 1;

  // 颜色定义
  static readonly COLOR_BACKGROUND: string = '#1a1a2e';
  static readonly COLOR_PLAYER: string = '#FFD700';
  static readonly COLOR_ENEMY: string = '#FF6B6B';
  static readonly COLOR_TEXT: string = '#FFFFFF';
}}
'''
    filepath = dirs['common_constants'] / 'GameConstants.ets'
    filepath.write_text(content, encoding='utf-8')
    print(f"✓ 生成: {filepath}")


def generate_math_utils(dirs: dict):
    """生成数学工具类"""
    content = '''/**
 * 矩形接口
 */
export interface Rect {
  x: number;
  y: number;
  width: number;
  height: number;
}

/**
 * 数学工具类
 */
export class MathUtils {
  static randomInt(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  static randomFloat(min: number, max: number): number {
    return Math.random() * (max - min) + min;
  }

  static checkRectCollision(rect1: Rect, rect2: Rect): boolean {
    return (
      rect1.x < rect2.x + rect2.width &&
      rect1.x + rect1.width > rect2.x &&
      rect1.y < rect2.y + rect2.height &&
      rect1.y + rect1.height > rect2.y
    );
  }

  static clamp(value: number, min: number, max: number): number {
    return Math.max(min, Math.min(max, value));
  }

  static distance(x1: number, y1: number, x2: number, y2: number): number {
    const dx = x2 - x1;
    const dy = y2 - y1;
    return Math.sqrt(dx * dx + dy * dy);
  }
}
'''
    filepath = dirs['common_utils'] / 'MathUtils.ets'
    filepath.write_text(content, encoding='utf-8')
    print(f"✓ 生成: {filepath}")


def generate_game_state(dirs: dict):
    """生成游戏状态枚举"""
    content = '''/**
 * 游戏状态枚举
 */
export enum GameState {
  IDLE = 'IDLE',
  PLAYING = 'PLAYING',
  GAME_OVER = 'GAME_OVER'
}
'''
    filepath = dirs['model_entities'] / 'GameState.ets'
    filepath.write_text(content, encoding='utf-8')
    print(f"✓ 生成: {filepath}")


def generate_player_entity(dirs: dict, config: dict):
    """生成玩家实体"""
    content = f'''import {{ GameConstants }} from '../../common/constants/GameConstants';
import {{ Rect }} from '../../common/utils/MathUtils';

/**
 * 玩家实体类
 */
export class Player {{
  x: number;
  y: number;
  width: number;
  height: number;
  velocityX: number;
  velocityY: number;

  constructor() {{
    this.x = GameConstants.CANVAS_WIDTH / 2 - GameConstants.PLAYER_SIZE / 2;
    this.y = GameConstants.CANVAS_HEIGHT / 2;
    this.width = GameConstants.PLAYER_SIZE;
    this.height = GameConstants.PLAYER_SIZE;
    this.velocityX = 0;
    this.velocityY = 0;
  }}

  reset(): void {{
    this.x = GameConstants.CANVAS_WIDTH / 2 - GameConstants.PLAYER_SIZE / 2;
    this.y = GameConstants.CANVAS_HEIGHT / 2;
    this.velocityX = 0;
    this.velocityY = 0;
  }}

  update(deltaTime: number): void {{
    this.x += this.velocityX * deltaTime;
    this.y += this.velocityY * deltaTime;

    // 边界限制
    this.x = Math.max(0, Math.min(GameConstants.CANVAS_WIDTH - this.width, this.x));
    this.y = Math.max(0, Math.min(GameConstants.CANVAS_HEIGHT - this.height, this.y));
  }}

  getCollisionRect(): Rect {{
    const rect: Rect = {{
      x: this.x,
      y: this.y,
      width: this.width,
      height: this.height
    }};
    return rect;
  }}
}}
'''
    filepath = dirs['model_entities'] / 'Player.ets'
    filepath.write_text(content, encoding='utf-8')
    print(f"✓ 生成: {filepath}")


def generate_game_engine(dirs: dict, config: dict):
    """生成游戏引擎"""
    content = f'''import {{ Player }} from '../model/entities/Player';
import {{ GameState }} from '../model/entities/GameState';
import {{ GameConstants }} from '../common/constants/GameConstants';

/**
 * 游戏引擎 - 核心游戏逻辑
 */
export class GameEngine {{
  private player: Player;
  private gameState: GameState;
  private score: number;

  constructor() {{
    this.player = new Player();
    this.gameState = GameState.IDLE;
    this.score = 0;
  }}

  getPlayer(): Player {{
    return this.player;
  }}

  getGameState(): GameState {{
    return this.gameState;
  }}

  getScore(): number {{
    return this.score;
  }}

  startGame(): void {{
    this.gameState = GameState.PLAYING;
    this.player.reset();
    this.score = 0;
  }}

  update(deltaTime: number): void {{
    if (this.gameState !== GameState.PLAYING) {{
      return;
    }}
    this.player.update(deltaTime);
    this.checkCollision();
  }}

  private checkCollision(): void {{
    // TODO: 根据游戏类型实现碰撞检测
  }}

  private gameOver(): void {{
    this.gameState = GameState.GAME_OVER;
  }}

  reset(): void {{
    this.player.reset();
    this.score = 0;
    this.gameState = GameState.IDLE;
  }}
}}
'''
    filepath = dirs['viewmodel'] / 'GameEngine.ets'
    filepath.write_text(content, encoding='utf-8')
    print(f"✓ 生成: {filepath}")


def generate_game_viewmodel(dirs: dict, config: dict):
    """生成游戏视图模型"""
    content = '''import { GameEngine } from './GameEngine';
import { Player } from '../model/entities/Player';
import { GameState } from '../model/entities/GameState';

@Observed
export class GameViewModel {
  private engine: GameEngine;
  @Track gameState: GameState;
  @Track score: number;
  @Track highScore: number;
  @Track player: Player;

  private intervalId: number | null = null;
  private lastFrameTime: number = 0;
  private readonly FRAME_TIME: number = 1000 / 60;

  constructor() {
    this.engine = new GameEngine();
    this.gameState = GameState.IDLE;
    this.score = 0;
    this.highScore = 0;
    this.player = this.engine.getPlayer();
  }

  startGame(): void {
    this.engine.startGame();
    this.gameState = this.engine.getGameState();
    this.startGameLoop();
  }

  private startGameLoop(): void {
    this.lastFrameTime = Date.now();
    this.intervalId = setInterval(() => {
      this.gameLoop();
    }, this.FRAME_TIME);
  }

  private gameLoop(): void {
    const now = Date.now();
    const deltaTime = Math.min((now - this.lastFrameTime) / 1000, 0.1);
    this.lastFrameTime = now;

    this.engine.update(deltaTime);
    this.syncState();
  }

  private syncState(): void {
    this.gameState = this.engine.getGameState();
    this.score = this.engine.getScore();

    if (this.gameState === GameState.GAME_OVER) {
      this.stopGameLoop();
    }
  }

  private stopGameLoop(): void {
    if (this.intervalId !== null) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  destroy(): void {
    this.stopGameLoop();
  }
}
'''
    filepath = dirs['viewmodel'] / 'GameViewModel.ets'
    filepath.write_text(content, encoding='utf-8')
    print(f"✓ 生成: {filepath}")


def generate_game_renderer(dirs: dict, config: dict):
    """生成游戏渲染器"""
    content = f'''import {{ Player }} from '../../model/entities/Player';
import {{ GameState }} from '../../model/entities/GameState';
import {{ GameConstants }} from '../../common/constants/GameConstants';

export class GameRenderer {{
  private canvasWidth: number = GameConstants.CANVAS_WIDTH;
  private canvasHeight: number = GameConstants.CANVAS_HEIGHT;

  render(
    canvas: CanvasRenderingContext2D,
    player: Player,
    score: number,
    gameState: GameState
  ): void {{
    this.clearCanvas(canvas);
    this.drawBackground(canvas);
    this.drawPlayer(canvas, player);
    this.drawScore(canvas, score);

    if (gameState === GameState.IDLE) {{
      this.drawStartPrompt(canvas);
    }} else if (gameState === GameState.GAME_OVER) {{
      this.drawGameOver(canvas, score);
    }}
  }}

  private clearCanvas(canvas: CanvasRenderingContext2D): void {{
    canvas.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
  }}

  private drawBackground(canvas: CanvasRenderingContext2D): void {{
    canvas.fillStyle = GameConstants.COLOR_BACKGROUND;
    canvas.fillRect(0, 0, this.canvasWidth, this.canvasHeight);
  }}

  private drawPlayer(canvas: CanvasRenderingContext2D, player: Player): void {{
    canvas.fillStyle = GameConstants.COLOR_PLAYER;
    canvas.fillRect(player.x, player.y, player.width, player.height);
  }}

  private drawScore(canvas: CanvasRenderingContext2D, score: number): void {{
    canvas.fillStyle = '#FFFFFF';
    canvas.strokeStyle = '#000000';
    canvas.lineWidth = 3;
    canvas.font = 'bold 36px sans-serif';
    canvas.textAlign = 'center';
    canvas.strokeText(score.toString(), this.canvasWidth / 2, 50);
    canvas.fillText(score.toString(), this.canvasWidth / 2, 50);
  }}

  private drawStartPrompt(canvas: CanvasRenderingContext2D): void {{
    canvas.fillStyle = 'rgba(0, 0, 0, 0.5)';
    canvas.fillRect(0, 0, this.canvasWidth, this.canvasHeight);

    canvas.fillStyle = '#FFFFFF';
    canvas.font = 'bold 28px sans-serif';
    canvas.textAlign = 'center';
    canvas.fillText('点击开始', this.canvasWidth / 2, this.canvasHeight / 2);
  }}

  private drawGameOver(canvas: CanvasRenderingContext2D, score: number): void {{
    canvas.fillStyle = 'rgba(0, 0, 0, 0.6)';
    canvas.fillRect(0, 0, this.canvasWidth, this.canvasHeight);

    canvas.fillStyle = '#FFFFFF';
    canvas.font = 'bold 36px sans-serif';
    canvas.textAlign = 'center';
    canvas.fillText('游戏结束', this.canvasWidth / 2, this.canvasHeight / 2 - 30);

    canvas.font = '24px sans-serif';
    canvas.fillText('分数: ' + score, this.canvasWidth / 2, this.canvasHeight / 2 + 20);
    canvas.fillText('点击重新开始', this.canvasWidth / 2, this.canvasHeight / 2 + 60);
  }}
}}
'''
    filepath = dirs['view_components'] / 'GameRenderer.ets'
    filepath.write_text(content, encoding='utf-8')
    print(f"✓ 生成: {filepath}")


def generate_index_page(dirs: dict, config: dict):
    """生成入口页面"""
    content = f'''import {{ GameViewModel }} from '../viewmodel/GameViewModel';
import {{ GameRenderer }} from '../view/components/GameRenderer';
import {{ GameState }} from '../model/entities/GameState';
import {{ GameConstants }} from '../common/constants/GameConstants';

@Entry
@Component
struct Index {{
  @State isPlaying: boolean = false;
  @State highScore: number = 0;
  @State viewModel: GameViewModel = new GameViewModel();
  private renderer: GameRenderer = new GameRenderer();
  private settings: RenderingContextSettings = new RenderingContextSettings(true);
  private canvasContext: CanvasRenderingContext2D = new CanvasRenderingContext2D(this.settings);
  private renderInterval: number | null = null;

  aboutToDisappear(): void {{
    this.cleanup();
  }}

  build() {{
    Column() {{
      if (!this.isPlaying) {{
        this.HomeView();
      }} else {{
        this.GameView();
      }}
    }}
    .width('100%')
    .height('100%')
  }}

  @Builder
  HomeView() {{
    Column() {{
      Text('{config['name']}')
        .fontSize(40)
        .fontWeight(FontWeight.Bold)
        .fontColor('#FFD700')
        .margin({{ top: 100, bottom: 20 }})

      Text('🎮')
        .fontSize(70)
        .margin({{ bottom: 40 }})

      Text('最高分: ' + this.highScore)
        .fontSize(22)
        .fontColor('#333333')
        .margin({{ bottom: 50 }})

      Button('开始游戏')
        .fontSize(22)
        .fontColor('#FFFFFF')
        .backgroundColor('#4CAF50')
        .borderRadius(25)
        .width(180)
        .height(45)
        .onClick(() => {{ this.startGame(); }})

      Text('点击屏幕开始游戏')
        .fontSize(14)
        .fontColor('#666666')
        .margin({{ top: 30 }})
    }}
    .width('100%')
    .height('100%')
    .linearGradient({{
      angle: 180,
      colors: [['#667eea', 0.0], ['#764ba2', 1.0]]
    }})
  }}

  @Builder
  GameView() {{
    Column() {{
      Canvas(this.canvasContext)
        .width(GameConstants.CANVAS_WIDTH)
        .height(GameConstants.CANVAS_HEIGHT)
        .backgroundColor(GameConstants.COLOR_BACKGROUND)
        .onReady(() => {{ this.onCanvasReady(); }})
        .onClick(() => {{ this.onCanvasClick(); }})
    }}
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .backgroundColor('#1a1a2e')
  }}

  private startGame(): void {{
    this.isPlaying = true;
    this.viewModel = new GameViewModel();
  }}

  private onCanvasReady(): void {{
    if (this.renderInterval !== null) {{
      clearInterval(this.renderInterval);
    }}
    this.renderInterval = setInterval(() => {{ this.render(); }}, 1000 / 60);
  }}

  private onCanvasClick(): void {{
    const state = this.viewModel.gameState;
    if (state === GameState.IDLE) {{
      this.viewModel.startGame();
    }} else if (state === GameState.GAME_OVER) {{
      this.cleanup();
      this.isPlaying = false;
    }}
  }}

  private render(): void {{
    this.renderer.render(
      this.canvasContext,
      this.viewModel.player,
      this.viewModel.score,
      this.viewModel.gameState
    );
  }}

  private cleanup(): void {{
    if (this.renderInterval !== null) {{
      clearInterval(this.renderInterval);
      this.renderInterval = null;
    }}
    this.viewModel.destroy();
  }}
}}
'''
    filepath = Path(dirs['view_pages'].parent.parent.parent) / 'pages/Index.ets'
    filepath.write_text(content, encoding='utf-8')
    print(f"✓ 生成: {filepath}")


def generate_score_repository(dirs: dict, config: dict):
    """生成分数仓库"""
    content = '''import { preferences } from '@kit.ArkData';
import { common } from '@kit.AbilityKit';
import { hilog } from '@kit.PerformanceAnalysisKit';

const PREFERENCES_NAME = 'game_scores';
const KEY_HIGH_SCORE = 'high_score';

export class ScoreRepository {
  private preferencesStore: preferences.Preferences | null = null;
  private context: common.UIAbilityContext;

  constructor(context: common.UIAbilityContext) {
    this.context = context;
  }

  async init(): Promise<void> {
    try {
      this.preferencesStore = await preferences.getPreferences(this.context, PREFERENCES_NAME);
    } catch (error) {
      hilog.error(0x0000, 'ScoreRepository', 'Failed to init: %{public}s', JSON.stringify(error));
    }
  }

  async getHighScore(): Promise<number> {
    try {
      if (this.preferencesStore === null) {
        await this.init();
      }
      return await this.preferencesStore!.get(KEY_HIGH_SCORE, 0) as number;
    } catch (error) {
      return 0;
    }
  }

  async saveHighScore(score: number): Promise<boolean> {
    try {
      if (this.preferencesStore === null) {
        await this.init();
      }
      const current = await this.getHighScore();
      if (score > current) {
        await this.preferencesStore!.put(KEY_HIGH_SCORE, score);
        await this.preferencesStore!.flush();
        return true;
      }
      return false;
    } catch (error) {
      return false;
    }
  }
}
'''
    filepath = dirs['model_repository'] / 'ScoreRepository.ets'
    filepath.write_text(content, encoding='utf-8')
    print(f"✓ 生成: {filepath}")


def main():
    args = parse_args()

    print(f"\n🎮 HarmonyOS 游戏生成器")
    print(f"   项目路径: {args.project_path}")
    print(f"   游戏主题: {args.theme}")

    # 获取游戏配置
    config = get_game_config(args.theme)
    if args.name:
        config['name'] = args.name

    print(f"   游戏名称: {config['name']}")
    print()

    # 创建目录结构
    print("📁 创建目录结构...")
    dirs = create_directory_structure(args.project_path)

    # 生成文件
    print("\n📝 生成代码文件...")

    # 迭代1: 基础架构
    generate_game_constants(dirs, config, args.theme)
    generate_math_utils(dirs)
    generate_game_state(dirs)

    # 迭代2: Model层
    generate_player_entity(dirs, config)
    generate_score_repository(dirs, config)

    # 迭代3: ViewModel层
    generate_game_engine(dirs, config)
    generate_game_viewmodel(dirs, config)

    # 迭代4: View层
    generate_game_renderer(dirs, config)

    # 迭代5: 页面整合
    generate_index_page(dirs, config)

    print(f"\n✅ 游戏框架生成完成!")
    print(f"\n📋 后续步骤:")
    print(f"   1. 根据游戏主题完善游戏逻辑和渲染")
    print(f"   2. 运行: python3 scripts/build_and_deploy.py {args.project_path}")
    print(f"   3. 推送: gh repo create && git push")


if __name__ == '__main__':
    main()
