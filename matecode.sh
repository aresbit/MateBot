#!/bin/bash

# =============================================================================
# MateCode - Claude Code Telegram Bridge
# 一键启动脚本
# =============================================================================

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
TMUX_SESSION="claude"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$HOME/.claude/hooks"
SETTINGS_FILE="$HOME/.claude/settings.json"

print_success() { echo -e "${GREEN}[✓]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
print_error() { echo -e "${RED}[✗]${NC} $1"; }
print_info() { echo -e "${YELLOW}[→]${NC} $1"; }

check_prerequisites() {
    print_info "检查环境依赖..."
    local missing_deps=()
    if ! command -v tmux &>/dev/null; then missing_deps+=("tmux"); fi
    if ! command -v python3 &>/dev/null; then missing_deps+=("python3"); fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "缺少依赖: ${missing_deps[*]}"
        echo "请安装: tmux, python3"
        exit 1
    fi
    print_success "所有依赖已满足"
}

setup_claude_hooks() {
    print_info "配置 Claude 钩子..."
    mkdir -p "$HOOKS_DIR"

    if [ -f "$PROJECT_DIR/hooks/send-to-telegram.sh" ]; then
        cp "$PROJECT_DIR/hooks/send-to-telegram.sh" "$HOOKS_DIR/"
        chmod +x "$HOOKS_DIR/send-to-telegram.sh"
        print_success "钩子脚本已安装"
    else
        print_error "钩子脚本不存在"
        exit 1
    fi

    # Update bot token in hook script
    if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=\"$TELEGRAM_BOT_TOKEN\"/" "$HOOKS_DIR/send-to-telegram.sh"
        else
            sed -i "s/TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=\"$TELEGRAM_BOT_TOKEN\"/" "$HOOKS_DIR/send-to-telegram.sh"
        fi
        print_success "Bot token 已配置"
    fi

    # Create settings.json if not exists
    if [ ! -f "$SETTINGS_FILE" ]; then
        mkdir -p "$(dirname "$SETTINGS_FILE")"
        cat > "$SETTINGS_FILE" << EOF
{
  "hooks": {
    "Stop": [{"hooks": [{"type": "command", "command": "$HOOKS_DIR/send-to-telegram.sh"}]}]
  }
}
EOF
        print_success "Claude 配置文件已创建"
    fi
}

start_tmux_claude() {
    print_info "启动 tmux + Claude Code..."

    if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        print_success "tmux 会话 '$TMUX_SESSION' 已存在"
    else
        tmux new-session -d -s "$TMUX_SESSION"
        sleep 1
        tmux send-keys -t "$TMUX_SESSION" "claude --dangerously-skip-permissions" C-m
        sleep 2
        print_success "Claude Code 已启动"
    fi
}

start_bridge() {
    print_info "启动 Bridge..."

    # Register bot commands
    if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setMyCommands" \
            -H "Content-Type: application/json" \
            -d @- <<EOF >/dev/null 2>&1
{
  "commands": [
    {"command": "clear", "description": "清空对话"},
    {"command": "resume", "description": "恢复会话"},
    {"command": "continue_", "description": "继续最近会话"},
    {"command": "loop", "description": "Ralph 循环"},
    {"command": "stop", "description": "中断 Claude"},
    {"command": "status", "description": "检查 tmux 状态"}
  ]
}
EOF
        print_success "Bot 命令已注册"
    fi

    # Start bridge
    nohup python3 "$PROJECT_DIR/bridge.py" >"$PROJECT_DIR/bridge.log" 2>&1 &
    BRIDGE_PID=$!
    echo $BRIDGE_PID > "$PROJECT_DIR/bridge.pid"

    sleep 2
    if kill -0 $BRIDGE_PID 2>/dev/null; then
        print_success "Bridge 已启动 (PID: $BRIDGE_PID)"
    else
        print_error "Bridge 启动失败"
        exit 1
    fi
}

show_status() {
    echo ""
    echo "==================================="
    echo "          服务状态"
    echo "==================================="

    if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        print_success "tmux 会话: 运行中"
    else
        print_error "tmux 会话: 未运行"
    fi

    if [ -f "$PROJECT_DIR/bridge.pid" ] && kill -0 "$(cat "$PROJECT_DIR/bridge.pid")" 2>/dev/null; then
        print_success "Bridge: 运行中 (PID: $(cat "$PROJECT_DIR/bridge.pid"))"
    else
        print_error "Bridge: 未运行"
    fi
}

stop_services() {
    print_info "停止服务..."

    if [ -f "$PROJECT_DIR/bridge.pid" ]; then
        BRIDGE_PID=$(cat "$PROJECT_DIR/bridge.pid")
        if kill -0 "$BRIDGE_PID" 2>/dev/null; then
            kill "$BRIDGE_PID" 2>/dev/null
            print_success "Bridge 已停止"
        fi
        rm -f "$PROJECT_DIR/bridge.pid"
    fi

    rm -f ~/.claude/telegram_pending
    rm -f ~/.claude/telegram_chat_id

    if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        print_warning "tmux 会话仍然运行 (如需关闭: tmux attach -t $TMUX_SESSION)"
    fi
}

show_logs() {
    echo "=== Bridge 日志 ==="
    if [ -f "$PROJECT_DIR/bridge.log" ]; then
        tail -n 20 "$PROJECT_DIR/bridge.log"
    else
        print_warning "bridge.log 不存在"
    fi
}

usage() {
    cat << EOF
使用方法: ./matecode.sh [命令]

命令:
    start      启动服务 (默认)
    stop       停止服务
    restart    重启服务
    status     显示状态
    logs       查看日志
    --help     显示帮助

环境变量:
    TELEGRAM_BOT_TOKEN    Telegram Bot Token (必需)

示例:
    export TELEGRAM_BOT_TOKEN="your_token"
    ./matecode.sh start

EOF
}

main() {
    echo ""
    echo "=========================================="
    echo "   MateCode - Claude Telegram Bridge"
    echo "=========================================="
    echo ""

    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        print_error "TELEGRAM_BOT_TOKEN 未设置"
        echo "请先设置: export TELEGRAM_BOT_TOKEN='your_token'"
        exit 1
    fi

    case "${1:-start}" in
        start)
            check_prerequisites
            setup_claude_hooks
            start_tmux_claude
            start_bridge
            show_status
            ;;
        stop)
            stop_services
            ;;
        restart)
            stop_services
            sleep 2
            check_prerequisites
            setup_claude_hooks
            start_tmux_claude
            start_bridge
            show_status
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        --help|-h)
            usage
            ;;
        *)
            print_error "未知命令: $1"
            usage
            exit 1
            ;;
    esac

    echo ""
    echo "=========================================="

    if [ "${1:-start}" = "start" ] || [ "${1:-start}" = "restart" ]; then
        echo ""
        print_info "启动完成！在 Telegram 中给 bot 发送消息即可使用"
        echo ""
        echo "常用命令:"
        echo "  /clear     - 清空对话"
        echo "  /continue_ - 继续最近会话"
        echo "  /resume    - 选择会话恢复"
        echo "  /status    - 检查状态"
    fi
    echo ""
}

main "$@"
