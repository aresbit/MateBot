---
name: harmonyos-ui-automator
description: HarmonyOS UI 自动化交互技能。通过 hdc dump ArkUI 布局树，理解当前界面状态，根据用户意图找到目标组件位置，并执行点击、长按、滑动、输入等交互操作。适用于 UI 自动化测试、应用操作自动化等场景。
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# HarmonyOS UI Automator

## 功能概述

本技能实现 HarmonyOS 设备的 UI 自动化交互：

1. **Dump 布局树** - 获取当前界面的完整 ArkUI 组件树
2. **界面理解** - 分析布局树，提取所有可交互组件及其位置
3. **组件定位** - 根据用户意图（文本、ID、类型等）精准定位目标组件
4. **交互执行** - 通过 hdc 命令注入点击、长按、滑动、输入等操作

## 使用场景

- UI 自动化测试
- 应用操作流程自动化
- 界面状态验证
- 组件定位与调试

## 快速开始

### 1. 获取当前界面布局

```bash
# 默认输出到 /tmp/harmonyos_layout_<timestamp>.json
python3 $SKILL_DIR/scripts/dump_layout.py

# 指定输出路径
python3 $SKILL_DIR/scripts/dump_layout.py --output /tmp/current_layout.json
```

返回布局文件路径和界面摘要。

### 2. 查找组件

```bash
# 按文本查找
python3 $SKILL_DIR/scripts/find_component.py --text "设置"

# 按 ID 查找
python3 $SKILL_DIR/scripts/find_component.py --id "AppIcon_Image"

# 按类型查找
python3 $SKILL_DIR/scripts/find_component.py --type "Button"

# 组合条件
python3 $SKILL_DIR/scripts/find_component.py --text "登录" --clickable true
```

### 3. 执行交互操作

```bash
# 点击坐标
python3 $SKILL_DIR/scripts/interact.py click 660 416

# 点击组件（自动计算中心点；至少提供一个选择器）
python3 $SKILL_DIR/scripts/interact.py click-component --text "设置"

# 长按
python3 $SKILL_DIR/scripts/interact.py long-click 660 416

# 双击
python3 $SKILL_DIR/scripts/interact.py double-click 660 416

# 滑动
python3 $SKILL_DIR/scripts/interact.py swipe 100 500 100 200

# 输入文本（先点击获取焦点）
python3 $SKILL_DIR/scripts/interact.py input-text 200 300 "Hello World"

# 按键事件
python3 $SKILL_DIR/scripts/interact.py key-event Back

# 方向甩动（0=left, 1=right, 2=up, 3=down）
python3 $SKILL_DIR/scripts/interact.py dirc-fling 2
```

### 4. 执行系统快捷手势

```bash
# 返回桌面
python3 $SKILL_DIR/scripts/shortcut.py home

# 下拉通知栏
python3 $SKILL_DIR/scripts/shortcut.py notification

# 多任务中心
python3 $SKILL_DIR/scripts/shortcut.py recent
```

## 工作流程

当用户请求执行某个 UI 操作时，按以下流程执行：

### Step 1: 获取布局树

```bash
python3 $SKILL_DIR/scripts/dump_layout.py
```

这会返回：
- 布局文件路径
- 界面整体描述
- 可交互组件列表

### Step 2: 分析界面并定位组件

根据用户的意图，在布局树中搜索目标组件：
- 用户说"点击设置" → 搜索 text="设置" 的可点击组件
- 用户说"点击搜索框" → 搜索 type 包含 "TextInput" 或 "Search" 的组件
- 用户说"向下滑动" → 执行向下滑动手势

### Step 3: 执行操作

找到组件后，计算其中心坐标，执行相应操作：

```bash
# 假设找到的组件 bounds 为 "[100,200][300,400]"
# 中心点为 ((100+300)/2, (200+400)/2) = (200, 300)
python3 $SKILL_DIR/scripts/interact.py click 200 300
```

## 布局树结构说明

ArkUI 布局树为 JSON 格式，每个节点包含：

```json
{
  "attributes": {
    "bounds": "[left,top][right,bottom]",  // 组件边界坐标
    "text": "按钮文字",                     // 显示文本
    "type": "Button",                      // 组件类型
    "id": "button_id",                     // 组件 ID
    "clickable": "true/false",             // 是否可点击
    "longClickable": "true/false",         // 是否可长按
    "scrollable": "true/false",            // 是否可滚动
    "enabled": "true/false",               // 是否可用
    "visible": "true/false",               // 是否可见
    "description": "描述"                   // 无障碍描述
  },
  "children": [...]                        // 子组件
}
```

## 常用组件类型

| 类型 | 说明 |
|------|------|
| Text | 文本组件 |
| Image | 图片组件 |
| Button | 按钮组件 |
| TextInput | 输入框 |
| Toggle | 开关组件 |
| Checkbox | 复选框 |
| List | 列表 |
| Grid | 网格 |
| Swiper | 轮播 |
| Stack | 堆叠容器 |
| Row/Column | 行/列容器 |

## 注意事项

1. 确保设备已通过 hdc 连接
2. 多设备同时在线时，必须显式传 `--device`，避免操作到错误设备
3. 对于动态加载的内容，可能需要等待后重新 dump
4. 坐标基于设备屏幕像素，不同分辨率设备坐标不同
5. `click-component` / `long-click-component` 至少要提供一个选择器（`--text/--id/--type/--regex`）
6. 组件点击默认只匹配 `clickable=true`、`enabled=true`、`visible=true`，避免误点不可交互节点

## 快速自检

```bash
bash $SKILL_DIR/scripts/smoke_test.sh
```

## 环境要求

- Python 3.x
- hdc 工具（通常位于 DevEco Studio SDK 目录）
- 设备已开启调试模式
