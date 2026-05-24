# MateCode - Claude Code Telegram Bridge

通过 Telegram 远程控制 Claude Code。

## 功能

- 📱 Telegram 上与 Claude 对话，支持代码高亮和格式化回复
- 🚀 **双模式**：Hook 模式（tmux 多路复用）和 Spawn 模式（OpenCC 子进程流式输出）
- 📡 **流式推送**：Token 级别实时流式输出，独立 worker 线程避免代理延迟阻塞
- 🧠 **记忆系统**：SQLite FTS5 自动记忆 + 外部记忆 + 失败记忆
- 📊 **KV-Cache 优化**：复用 Claude 上下文减少 token 消耗

## 快速开始

```bash
# 1. 安装依赖
brew install tmux

# 2. 配置 token
export TELEGRAM_BOT_TOKEN="your_token"

# 3. 启动（默认 hook 模式）
./matecode.sh start

# 4. 使用 spawn 模式（流式输出）
./matecode.sh start --backend opencc
```

## 配置

### Telegram Bot

在 Telegram 搜索 @BotFather，发送 `/newbot` 创建 bot，获取 token。

### Hook 模式（默认）

```bash
cp hooks/send-to-telegram.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/send-to-telegram.sh
```

在 `~/.claude/settings.json` 中配置：
```json
{
  "hooks": {
    "Stop": [{"hooks": [{"type": "command", "command": "~/.claude/hooks/send-to-telegram.sh"}]}]
  }
}
```

### Spawn 模式

无需配置 hook，直接通过 `claude-js` spawn 子进程通信。支持：
- Token 级流式输出（`--include-partial-messages`）
- 消息原地编辑（Telegram editMessageText）
- 自动消息分片（>4000 字符）

## 命令

```bash
./matecode.sh start       # 启动
./matecode.sh stop        # 停止
./matecode.sh restart     # 重启
./matecode.sh status      # 状态
./matecode.sh logs        # 日志
```

## Bot 命令

| 命令 | 功能 |
|------|------|
| `/status` | 检查会话状态 |
| `/clear` | 清空会话 |
| `/continue_` | 继续最近会话 |
| `/resume` | 选择历史会话恢复 |
| `/stop` | 中断当前生成 |
| `/remember <text>` | 保存记忆 |
| `/recall [query]` | 搜索记忆 |
| `/forget <query/all>` | 删除记忆 |

## 记忆系统

基于 SQLite FTS5 的本地记忆，包含三层：

| 模块 | 文件 | 用途 |
|------|------|------|
| 自动记忆 | `memory.py` | 自动提取 + 智能召回 |
| 外部记忆 | `external_memory.py` | 外部知识注入 |
| 失败记忆 | `failure_memory.py` | 错误模式学习 |

```bash
export MEMORY_ENABLED=true         # 启用记忆
export MEMORY_MAX_RESULTS=5        # 最大召回数
export MEMORY_MAX_CONTEXT=2000     # 上下文最大字符
export KV_CACHE_ENABLED=true       # KV-Cache 优化
export TELEGRAM_RAW_MESSAGES=true  # 原始消息模式
```

## 技术架构

- **纯标准库**：无外部 Python 依赖
- **长轮询**：30s 超时 Telegram getUpdates
- **流式渲染**：独立 worker 线程，节流编辑合并，避免代理延迟（2-5s）阻塞生成
- **安全**：只向外连接，无需公网暴露

## 文件

| 文件 | 用途 |
|------|------|
| `matecode.sh` | 主启动脚本 |
| `bridge.py` | 消息桥接 + 命令路由 |
| `opencc_backend.py` | Spawn 模式：OpenCC 子进程 + 流式渲染 |
| `memory.py` | 自动记忆 (SQLite FTS5) |
| `kv_cache.py` | KV-Cache 优化 |

## 常见命令

    tmux a -t claude
    tmux source-file ~/.tmux.conf
    claude --dangerously-skip-permissions
    tmux kill-session -t claude
    pkill -f "bridge\.py"

## License

MIT
