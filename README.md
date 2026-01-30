# MateCode - Claude Code Telegram Bridge

通过 Telegram 远程控制 Claude Code。

![demo](demo.gif)

## 功能

- 📱 在 Telegram 上与 Claude 对话
- 🧠 **长期记忆**：自动保存和召回对话历史
- 🔄 会话管理（清空、恢复、继续）
- 📝 代码高亮和格式化回复
- 🔒 纯 Polling 模式，无需公网暴露

## 快速开始

```bash
# 1. 安装依赖 (macOS)
brew install tmux

# 2. 设置 token（从 @BotFather 获取）
export TELEGRAM_BOT_TOKEN="your_token"

# 3. 启动
./matecode.sh start
```

## 配置

### 1. 创建 Telegram Bot

在 Telegram 搜索 @BotFather，发送 `/newbot` 创建 bot。

### 2. 配置 Claude 钩子

```bash
cp hooks/send-to-telegram.sh ~/.claude/hooks/
# 编辑设置 bot token
nano ~/.claude/hooks/send-to-telegram.sh
chmod +x ~/.claude/hooks/send-to-telegram.sh
```

添加 hook 到 `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [{"hooks": [{"type": "command", "command": "~/.claude/hooks/send-to-telegram.sh"}]}]
  }
}
```

## 命令

```bash
./matecode.sh start      # 启动服务
./matecode.sh stop       # 停止服务
./matecode.sh restart    # 重启服务
./matecode.sh status     # 查看状态
./matecode.sh logs       # 查看日志
```

## Telegram Bot 命令

| 命令 | 功能 |
|------|------|
| `/status` | 检查 tmux 状态 |
| `/clear` | 清空对话 |
| `/continue_` | 继续最近会话 |
| `/resume` | 选择会话恢复 |
| `/loop <prompt>` | Ralph 循环模式 |
| `/stop` | 中断 Claude |
| `/remember <text>` | 保存内容到记忆 |
| `/recall [query]` | 搜索/查看记忆 |
| `/forget <query/all>` | 删除记忆 |

### 记忆功能

MateCode 内置了基于 SQLite 的本地记忆系统：

- **自动记忆**：每次对话自动保存到本地数据库
- **智能召回**：发送消息时自动搜索相关历史记忆并注入上下文
- **隐私安全**：所有数据存储在本地 `~/.matecode/memory.db`，不上传云端
- **手动管理**：使用 `/remember`、`/recall`、`/forget` 命令管理记忆

**环境变量配置：**
```bash
export MEMORY_ENABLED=true        # 启用/禁用记忆功能
export MEMORY_MAX_RESULTS=5       # 每次查询最大记忆数
export MEMORY_MAX_CONTEXT=2000    # 注入上下文的最大字符数
```

## 常见命令

    tmux a -t claude
    tmux source-file ~/.tmux.conf
    claude --dangerously-skip-permissions
    tmux kill-session -t claude
    # 关闭所有 bridge 相关进程
    pkill -f "bridge\.py|bridge-polling\.py"

## 技术特点

- **纯标准库**: 无外部 Python 依赖
- **长轮询**: 30 秒超时，低延迟
- **实时响应**: 监控 transcript 即时推送
- **安全**: 只向外连接，不接收入站

## 文件说明

| 文件 | 用途 |
|------|------|
| `matecode.sh` | 主启动脚本 |
| `bridge.py` | 桥接服务器 |
| `memory.py` | 本地记忆系统 (SQLite FTS5) |
| `start_bridge.sh` | 单独启动 bridge |
| `stop_bridge.sh` | 单独停止 bridge |
| `hooks/send-to-telegram.sh` | Claude Stop 钩子 |

## License

MIT
