# MateCode 使用指南

通过 Telegram 远程控制 Claude Code。

---

## 快速开始

```bash
# 1. 设置环境变量
export TELEGRAM_BOT_TOKEN="你的token"

# 2. 启动
./matecode.sh start
```

然后在 Telegram 中给你的 bot 发送消息即可。

---

## 获取 Telegram Bot Token

1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot` 创建新 bot
3. 复制得到的 token（格式：`123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`）

---

## 安装依赖

**macOS:**
```bash
brew install tmux
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tmux python3
```

---

## 配置

### 1. 配置 Claude 钩子

```bash
cp hooks/send-to-telegram.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/send-to-telegram.sh
```

编辑 `~/.claude/hooks/send-to-telegram.sh`，设置你的 bot token。

### 2. 配置 Claude settings

在 `~/.claude/settings.json` 中添加：

```json
{
  "hooks": {
    "Stop": [{"hooks": [{"type": "command", "command": "~/.claude/hooks/send-to-telegram.sh"}]}]
  }
}
```

---

## 使用

### 启动服务

```bash
./matecode.sh start
```

### 查看状态

```bash
./matecode.sh status
```

### 查看日志

```bash
./matecode.sh logs
```

### 停止服务

```bash
./matecode.sh stop
```

---

## Telegram 命令

| 命令 | 功能 |
|------|------|
| `/status` | 检查 tmux 状态 |
| `/clear` | 清空对话 |
| `/continue_` | 继续最近会话 |
| `/resume` | 选择会话恢复 |
| `/loop <提示词>` | Ralph 循环模式 |
| `/stop` | 中断 Claude |

---

## 故障排除

### Bot 不回复

1. 检查 token: `echo $TELEGRAM_BOT_TOKEN`
2. 查看日志: `./matecode.sh logs`
3. 检查网络连接

### Claude 没有回复

1. 检查 tmux: `tmux ls`
2. 确认 Claude 在运行: `tmux attach -t claude`

### 重复回复

```bash
rm -f ~/.claude/telegram_pending
./matecode.sh restart
```

---

## 技术说明

- **纯 Polling 模式**: 无需公网 IP，不暴露端口
- **长轮询**: 30 秒超时，低延迟低消耗
- **零依赖**: 只使用 Python 标准库
- **安全**: 只向外连接 Telegram API，不接收入站连接

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `matecode.sh` | 主启动脚本 |
| `bridge.py` | 桥接服务器 |
| `hooks/send-to-telegram.sh` | Claude Stop 钩子 |

---

**祝使用愉快！**
