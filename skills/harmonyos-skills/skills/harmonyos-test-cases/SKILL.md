---
name: harmonyos-test-cases
description: HarmonyOS UI 自动化测试用例管理和执行技能。用于存储、管理和执行 UI 测试用例，验证应用功能是否正常。支持通过组件文本/ID定位元素，自动适配不同屏幕尺寸。使用场景：(1) 执行已保存的测试用例 (2) 保存新的测试用例 (3) 列出所有测试用例 (4) 用户说"运行测试"、"执行测试用例"、"验证XX功能"、"把这个测试流程保存下来"。
---

# HarmonyOS 测试用例管理

## 功能概述

- **存储测试用例**: JSON 格式保存测试步骤和预期结果
- **执行测试用例**: 自动化执行 UI 操作并验证结果
- **屏幕适配**: 通过组件文本/ID 定位，而非固定坐标
- **易于扩展**: 添加新测试用例只需创建 JSON 文件

## 快速开始

### 列出所有测试用例

```bash
python3 $SKILL_DIR/scripts/run_test.py --list
```

### 执行测试用例

```bash
python3 $SKILL_DIR/scripts/run_test.py photos_favorite

# 多设备场景建议显式指定
python3 $SKILL_DIR/scripts/run_test.py photos_favorite --device 127.0.0.1:5555

# 失败即停，便于快速定位
python3 $SKILL_DIR/scripts/run_test.py photos_favorite --fail-fast
```

### 保存当前操作为测试用例

当用户教你一步步执行完一个测试流程后，可以说"把这个测试用例保存下来"，我会：
1. 将操作步骤转换为 JSON 格式
2. 使用组件文本/ID 定位（非固定坐标）
3. 保存到 `testcases/` 目录

## 测试用例格式

```json
{
  "id": "test_id",
  "name": "测试名称",
  "description": "测试描述",
  "app": "com.example.app",
  "tags": ["标签1", "标签2"],
  "steps": [
    {
      "step": 1,
      "action": "click",
      "description": "点击按钮",
      "params": {
        "locator": {
          "type": "text",
          "value": "确定"
        }
      },
      "expected": "应该跳转到下一页"
    }
  ],
  "teardown_steps": []
}
```

### 支持的操作类型

| action | 说明 | params |
|--------|------|--------|
| `launch_app` | 启动应用 | `locator` - 应用图标定位 |
| `click` | 点击 | `locator` - 组件定位 |
| `wait` | 等待 | `duration` - 秒数 |
| `key_event` | 按键 | `value` - Back/Home 等 |
| `swipe` | 滑动 | `coords` 或 `start_locator`/`end_locator` |
| `verify` | 验证 | `locator` - 要验证的组件 |
| `capture_count` | 记录组件数量基线 | `key` + `locator` |
| `verify_count_delta` | 验证数量变化 | `key` + `locator` + `allowed_deltas` |

### 定位器类型

| type | 说明 | 示例 |
|------|------|------|
| `text` | 按文本查找 | `{"type": "text", "value": "设置"}` |
| `id` | 按ID查找 | `{"type": "id", "value": "ToolBarButtonFavor"}` |

## 已有测试用例

| 用例 | 描述 |
|------|------|
| `photos_favorite` | 图库收藏/取消收藏功能测试 |

## 添加新测试用例

1. 在 `testcases/` 目录创建 JSON 文件
2. 按格式编写测试步骤
3. 使用 `run_test.py` 执行验证

## 工作流程

当用户完成一个测试流程后，我会：

1. **记录步骤**: 将每一步操作转换为标准格式
2. **提取定位器**: 使用 harmonyos-ui-automator 技能获取组件的 text 或 id
3. **保存用例**: 写入 JSON 文件到 `testcases/` 目录
4. **验证格式**: 确保用例可以正常执行

## 注意事项

- 多设备同时在线时，建议传 `--device`，避免操作到错误设备
- 定位器优先使用 `text`，其次是 `id`
- `coords` 仅作为兜底（动态页面或无稳定 locator 时），优先用 `locator`
- 每个步骤应包含清晰的 `description` 和 `expected`
- `teardown_steps` 用于测试后恢复环境

## 快速自检

```bash
bash $SKILL_DIR/scripts/smoke_test.sh
```
