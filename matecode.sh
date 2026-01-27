#!/bin/bash

# =============================================================================
# Claude Code Telegram Bridge - One-Click Startup Script
# 保姆级一键启动脚本
# =============================================================================

set -e  # 遇到错误立即退出

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
TMUX_SESSION="claude"
BRIDGE_PORT="8081"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
HOOKS_DIR="$HOME/.claude/hooks"
SETTINGS_FILE="$HOME/.claude/settings.json"
POLLING_MODE=false
FORCE_POLLING=false

# Print colored message
print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[→]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_info "检查环境依赖..."

    local missing_deps=()

    if ! command_exists tmux; then
        missing_deps+=("tmux")
    fi

    if ! command_exists cloudflared; then
        missing_deps+=("cloudflared")
    fi

    if ! command_exists python3; then
        missing_deps+=("python3")
    fi

    # Skip pip check - not needed
    # if ! command_exists pip; then
    #     missing_deps+=("pip")
    # fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "缺少依赖: ${missing_deps[*]}"
        echo ""
        echo "请安装缺失的依赖:"
        echo "  Ubuntu/Debian: sudo apt-get install tmux python3-pip"
        echo "  macOS: brew install tmux cloudflared"
        echo "  然后访问 https://github.com/cloudflare/cloudflared/releases 安装 cloudflared"
        exit 1
    fi

    print_success "所有依赖已满足"
}

# Setup Python virtual environment
setup_venv() {
    print_info "配置 Python 虚拟环境..."

    if [ ! -d "$VENV_DIR" ]; then
        print_warning "虚拟环境不存在，正在创建..."
        python3 -m venv "$VENV_DIR"
        print_success "虚拟环境已创建"
    fi

    # source "$VENV_DIR/bin/activate"

    # Skip pip install - bridge.py only uses standard libraries
    # if [ -f "$PROJECT_DIR/setup.py" ] || [ -f "$PROJECT_DIR/pyproject.toml" ]; then
    #     print_info "安装 Python 依赖..."
    #     pip install -e . >/dev/null 2>&1
    #     print_success "Python 依赖已安装"
    # fi
}

# Setup Claude hooks
setup_claude_hooks() {
    print_info "配置 Claude 钩子..."

    # Create hooks directory if not exists
    mkdir -p "$HOOKS_DIR"

    # Copy hook script
    if [ -f "$PROJECT_DIR/hooks/send-to-telegram.sh" ]; then
        cp "$PROJECT_DIR/hooks/send-to-telegram.sh" "$HOOKS_DIR/"
        chmod +x "$HOOKS_DIR/send-to-telegram.sh"
        print_success "钩子脚本已安装"
    else
        print_error "钩子脚本不存在: $PROJECT_DIR/hooks/send-to-telegram.sh"
        exit 1
    fi

    # Update bot token in hook script
    if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
        sed -i "s/TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=\"$TELEGRAM_BOT_TOKEN\"/" "$HOOKS_DIR/send-to-telegram.sh"
        print_success "Bot token 已配置"
    else
        print_warning "TELEGRAM_BOT_TOKEN 未设置，请手动配置 ~/.claude/hooks/send-to-telegram.sh"
    fi

    # Check or create settings.json
    if [ ! -f "$SETTINGS_FILE" ]; then
        print_warning "Claude 配置文件不存在，正在创建..."
        mkdir -p "$(dirname "$SETTINGS_FILE")"
        cat > "$SETTINGS_FILE" << EOF
{
  "hooks": {
    "Stop": [{"hooks": [{"type": "command", "command": "$HOOKS_DIR/send-to-telegram.sh"}]}]
  }
}
EOF
        print_success "Claude 配置文件已创建"
    else
        print_success "Claude 配置文件已存在"
    fi
}

# Start tmux session with Claude
start_tmux_claude() {
    print_info "启动 tmux + Claude Code..."

    if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        print_success "tmux 会话 '$TMUX_SESSION' 已存在"
    else
        print_info "创建新的 tmux 会话..."
        tmux new-session -d -s "$TMUX_SESSION"

        # Wait for session to be ready
        sleep 1

        # Start claude
        print_info "启动 Claude Code..."
        tmux send-keys -t "$TMUX_SESSION" "claude --dangerously-skip-permissions" C-m

        # Wait for Claude to start
        sleep 2

        print_success "Claude Code 已在 tmux 中启动"
    fi
}

# Check port availability
check_port() {
    local port=$1
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "
import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', $port))
sock.close()
sys.exit(0 if result != 0 else 1)
" 2>/dev/null
        return $?
    else
        # Fallback to netstat/ss
        if command -v netstat >/dev/null 2>&1; then
            ! netstat -tuln 2>/dev/null | grep -q ":$port "
        elif command -v ss >/dev/null 2>&1; then
            ! ss -tuln 2>/dev/null | grep -q ":$port "
        else
            # Can't check, assume available
            return 0
        fi
    fi
}

# Start bridge server
start_bridge() {
    print_info "启动 Bridge 服务器..."

    # Check if port is available
    if [ "$POLLING_MODE" = false ] && ! check_port "$BRIDGE_PORT"; then
        print_error "端口 $BRIDGE_PORT 已被占用"
        print_info "尝试查找可用端口..."

        # Try to find an alternative port
        found_port=false
        for alt_port in $(seq $((BRIDGE_PORT + 1)) 8099); do
            if check_port "$alt_port"; then
                print_info "找到可用端口: $alt_port"
                BRIDGE_PORT=$alt_port
                found_port=true
                break
            fi
        done

        if [ "$found_port" = false ]; then
            print_warning "未找到可用端口 (8081-8099)，将使用轮询模式"
            POLLING_MODE=true
        fi
    fi

    # Register bot commands
    if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
        print_info "注册 bot 命令..."
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setMyCommands" \
            -H "Content-Type: application/json" \
            -d @- <<EOF >/dev/null 2>&1
{
  "commands": [
    {"command": "clear", "description": "清空对话"},
    {"command": "resume", "description": "恢复会话"},
    {"command": "continue_", "description": "继续最近会话"},
    {"command": "loop", "description": "Ralph 循环: /loop <提示词>"},
    {"command": "stop", "description": "中断 Claude"},
    {"command": "status", "description": "检查 tmux 状态"}
  ]
}
EOF
        print_success "Bot 命令已注册"
    fi

    # Start bridge in background
    print_info "启动 bridge.py (端口 $BRIDGE_PORT)..."
    export PORT="$BRIDGE_PORT"  # Ensure bridge uses the correct port

    if [ "$POLLING_MODE" = true ] || [ "$FORCE_POLLING" = true ]; then
        print_info "使用轮询模式 (无 Cloudflare Tunnel)..."
        nohup python3 "$PROJECT_DIR/bridge.py" --mode polling >"$PROJECT_DIR/bridge.log" 2>&1 &
    else
        nohup python3 "$PROJECT_DIR/bridge.py" >"$PROJECT_DIR/bridge.log" 2>&1 &
    fi

    BRIDGE_PID=$!
    echo $BRIDGE_PID > "$PROJECT_DIR/bridge.pid"

    sleep 3

    if kill -0 $BRIDGE_PID 2>/dev/null; then
        print_success "Bridge 服务器已启动 (PID: $BRIDGE_PID)"

        # Check if bridge encountered port issues and check the log
        sleep 2
        if grep -q "Error: Port" "$PROJECT_DIR/bridge.log" 2>/dev/null; then
            print_warning "检测到端口问题，检查日志..."
            if grep -q "Falling back to polling mode" "$PROJECT_DIR/bridge.log" 2>/dev/null; then
                print_success "Bridge 已自动切换到轮询模式"
                POLLING_MODE=true
            fi
        fi
    else
        print_error "Bridge 启动失败，请查看 bridge.log"
        exit 1
    fi
}

# Start Cloudflare tunnel
start_tunnel() {
    # Skip tunnel if in polling mode
    if [ "$POLLING_MODE" = true ] || [ "$FORCE_POLLING" = true ]; then
        print_info "轮询模式已启用，跳过 Cloudflare Tunnel"
        return 0
    fi

    print_info "启动 Cloudflare Tunnel..."

    # Start tunnel in background
    nohup cloudflared tunnel --url "http://localhost:$BRIDGE_PORT" >"$PROJECT_DIR/tunnel.log" 2>&1 &
    TUNNEL_PID=$!
    echo $TUNNEL_PID > "$PROJECT_DIR/tunnel.pid"

    # Wait a bit for tunnel to establish
    sleep 3

    # Extract tunnel URL from log
    TUNNEL_URL=$(grep -o 'https://[^"]*\.trycloudflare\.com' "$PROJECT_DIR/tunnel.log" | head -1)

    if [ -n "$TUNNEL_URL" ]; then
        print_success "Tunnel 已启动: $TUNNEL_URL"
        echo "$TUNNEL_URL" > "$PROJECT_DIR/tunnel.url"
    else
        print_warning "Tunnel 可能已启动，但无法获取 URL"
        print_warning "请稍等片刻后查看: tail -f $PROJECT_DIR/tunnel.log"
    fi

    # Set Telegram webhook if bot token is available
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TUNNEL_URL" ]; then
        print_info "设置 Telegram webhook..."
        WEBHOOK_URL="${TUNNEL_URL}/"
        RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook?url=${WEBHOOK_URL}")

        if echo "$RESPONSE" | grep -q '"ok":true'; then
            print_success "Telegram webhook 已设置"
        else
            print_warning "Webhook 设置可能失败: $RESPONSE"
            print_warning "将使用轮询模式作为备用方案"
        fi
    fi
}

# Show status
show_status() {
    echo ""
    echo "==================================="
    echo "          服务状态"
    echo "==================================="

    # Check tmux
    if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        print_success "tmux 会话 '$TMUX_SESSION' 正在运行"
    else
        print_error "tmux 会话 '$TMUX_SESSION' 未运行"
    fi

    # Check bridge
    if [ -f "$PROJECT_DIR/bridge.pid" ] && kill -0 "$(cat "$PROJECT_DIR/bridge.pid")" 2>/dev/null; then
        print_success "Bridge 正在运行 (PID: $(cat "$PROJECT_DIR/bridge.pid"))"
        if [ "$POLLING_MODE" = true ] || [ "$FORCE_POLLING" = true ]; then
            print_info "模式: 轮询模式 (无 Cloudflare Tunnel)"
        else
            print_info "模式: Webhook 模式"
        fi
    else
        print_error "Bridge 未运行"
    fi

    # Check tunnel
    if [ "$POLLING_MODE" = true ] || [ "$FORCE_POLLING" = true ]; then
        print_info "Cloudflare Tunnel: 已跳过 (轮询模式)"
    elif [ -f "$PROJECT_DIR/tunnel.pid" ] && kill -0 "$(cat "$PROJECT_DIR/tunnel.pid")" 2>/dev/null; then
        if [ -f "$PROJECT_DIR/tunnel.url" ]; then
            print_success "Tunnel 正在运行: $(cat "$PROJECT_DIR/tunnel.url")"
        else
            print_success "Tunnel 正在运行 (URL 未知)"
        fi
    else
        print_error "Tunnel 未运行"
    fi

    if [ -f "$PROJECT_DIR/tunnel.url" ]; then
        echo ""
        print_info "Telegram Bot Webhook URL:"
        echo "  $(cat "$PROJECT_DIR/tunnel.url")/"
    fi
}

# Stop all services
stop_services() {
    print_info "停止所有服务..."

    # Stop bridge
    if [ -f "$PROJECT_DIR/bridge.pid" ]; then
        BRIDGE_PID=$(cat "$PROJECT_DIR/bridge.pid")
        if kill -0 "$BRIDGE_PID" 2>/dev/null; then
            kill "$BRIDGE_PID"
            print_success "Bridge 已停止"
        fi
        rm -f "$PROJECT_DIR/bridge.pid"
    fi

    # Stop tunnel
    if [ -f "$PROJECT_DIR/tunnel.pid" ]; then
        TUNNEL_PID=$(cat "$PROJECT_DIR/tunnel.pid")
        if kill -0 "$TUNNEL_PID" 2>/dev/null; then
            kill "$TUNNEL_PID"
            print_success "Tunnel 已停止"
        fi
        rm -f "$PROJECT_DIR/tunnel.pid"
    fi

    # Kill claude in tmux (optional, we keep tmux running)
    if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        print_warning "tmux 会话 '$TMUX_SESSION' 仍然运行 (Claude Code 在内部运行)"
        print_warning "如需关闭，请运行: tmux attach -t $TMUX_SESSION，然后按 Ctrl+C 退出 Claude"
    fi

    rm -f "$PROJECT_DIR/tunnel.url"
    # Reset polling mode flag
    POLLING_MODE=false
}

# Show logs
show_logs() {
    echo ""
    echo "=== Bridge 日志 ==="
    if [ -f "$PROJECT_DIR/bridge.log" ]; then
        tail -n 20 "$PROJECT_DIR/bridge.log"
    else
        print_warning "bridge.log 不存在"
    fi

    echo ""
    echo "=== Tunnel 日志 ==="
    if [ -f "$PROJECT_DIR/tunnel.log" ]; then
        tail -n 20 "$PROJECT_DIR/tunnel.log"
    else
        print_warning "tunnel.log 不存在"
    fi

    echo ""
    echo "=== tmux 会话 (最新 20 行) ==="
    if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
        tmux capture-pane -t "$TMUX_SESSION" -p | tail -n 20
    else
        print_warning "tmux 会话不存在"
    fi
}

# Show usage
usage() {
    cat << EOF
使用方法: ./matecode.sh [选项]

选项:
    start      启动所有服务 (默认)
    stop       停止所有服务
    restart    重启所有服务
    status     显示服务状态
    logs       查看日志
    --polling  强制使用轮询模式（无需 Cloudflare）
    --help     显示帮助信息

环境变量:
    TELEGRAM_BOT_TOKEN    Telegram Bot Token (必需)
    TMUX_SESSION          tmux 会话名称 (可选, 默认: claude)
    PORT                  Bridge 端口 (可选, 默认: 8081)

示例:
    export TELEGRAM_BOT_TOKEN="your_token_here"
    ./matecode.sh start

    # 或使用一次性环境变量
    TELEGRAM_BOT_TOKEN="your_token" ./matecode.sh start

    # 使用轮询模式（无需 Cloudflare Tunnel）
    ./matecode.sh start --polling

快速开始:
    1. 获取 Telegram Bot Token (从 @BotFather)
    2. export TELEGRAM_BOT_TOKEN="your_token"
    3. ./matecode.sh start
    4. 查看状态: ./matecode.sh status
    5. 在 Telegram 中开始使用

模式说明:
    Webhook 模式: 需要 Cloudflare Tunnel，响应更快
    轮询模式: 无需 Cloudflare，但响应稍慢

EOF
}

# Main script logic
main() {
    echo ""
    echo "=========================================="
    echo "   Claude Code Telegram Bridge 启动器"
    echo "=========================================="
    echo ""

    # Check TELEGRAM_BOT_TOKEN
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        print_error "TELEGRAM_BOT_TOKEN 环境变量未设置"
        echo ""
        print_info "请先设置你的 Telegram Bot Token:"
        echo "  export TELEGRAM_BOT_TOKEN='your_token_here'"
        echo ""
        print_info "获取方式: 在 Telegram 中搜索 @BotFather，创建新 bot 并获取 token"
        exit 1
    fi

    case "${1:-start}" in
        start)
            # Check for --polling flag
            if [ "$2" = "--polling" ]; then
                FORCE_POLLING=true
                POLLING_MODE=true
                print_info "使用轮询模式（无需 Cloudflare Tunnel）"
            fi
            check_prerequisites
            setup_venv
            setup_claude_hooks
            start_tmux_claude
            start_bridge
            start_tunnel
            show_status
            ;;
        stop)
            stop_services
            ;;
        restart)
            stop_services
            sleep 2
            # Check for --polling flag
            if [ "$2" = "--polling" ]; then
                FORCE_POLLING=true
                POLLING_MODE=true
                print_info "使用轮询模式（无需 Cloudflare Tunnel）"
            fi
            check_prerequisites
            setup_venv
            setup_claude_hooks
            start_tmux_claude
            start_bridge
            start_tunnel
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
            print_error "未知选项: $1"
            usage
            exit 1
            ;;
    esac

    echo ""
    echo "=========================================="

    if [ "${1:-start}" = "start" ] || [ "${1:-start}" = "restart" ]; then
        echo ""
        print_info "启动完成！现在在 Telegram 中给 bot 发送消息即可使用"
        echo ""
        print_info "常用命令:"
        echo "  ./start.sh status     - 查看服务状态"
        echo "  ./start.sh logs       - 查看日志"
        echo "  ./start.sh stop       - 停止服务"
        echo ""
        print_info "Telegram Bot 命令:"
        echo "  /start     - 开始使用"
        echo "  /status    - 检查 tmux 状态"
        echo "  /clear     - 清空对话"
        echo "  /continue_ - 继续最近会话"
        echo "  /resume    - 选择会话恢复"
        echo "  /loop      - Ralph 循环模式"
        echo "  /stop      - 中断 Claude"
    fi
    echo " ===MateCode=== "
    tmux a -t claude
    claude --dangerously-skip-permissions
}

# Check for --polling flag before main function
if [ "$1" = "--polling" ]; then
    FORCE_POLLING=true
    POLLING_MODE=true
    shift
fi

# Run main function
main "$@"
