#!/bin/bash
# MateBot Bridge Manager - 确保只有一个实例运行

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIDFILE="$SCRIPT_DIR/bridge.pid"
LOGFILE="$SCRIPT_DIR/bridge.log"

# 获取脚本的绝对路径
BRIDGE_SCRIPT="$SCRIPT_DIR/bridge.py"

usage() {
    echo "Usage: $0 {start|stop|restart|status|kill-all}"
    exit 1
}

# 获取所有 bridge.py 进程（全系统）
get_all_bridge_pids() {
    ps aux | grep -E "python.*bridge\.py" | grep -v grep | awk '{print $2}'
}

# 获取当前目录的 bridge.py 进程
get_current_bridge_pid() {
    if [ -f "$PIDFILE" ]; then
        cat "$PIDFILE" 2>/dev/null
    else
        echo ""
    fi
}

# 检查进程是否存在
is_running() {
    local pid=$1
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# 停止所有 bridge 进程（系统级清理）
kill_all() {
    echo "强制停止所有 bridge.py 进程..."
    local count=0
    for pid in $(get_all_bridge_pids); do
        echo "  停止 PID: $pid"
        kill -9 "$pid" 2>/dev/null
        count=$((count + 1))
    done
    rm -f "$PIDFILE" ~/.claude/telegram_pending ~/.claude/telegram_chat_id
    echo "已停止 $count 个进程"
}

# 正常停止
stop() {
    echo "停止 bridge..."
    local pid=$(get_current_bridge_pid)

    if [ -n "$pid" ] && is_running "$pid"; then
        kill "$pid" 2>/dev/null
        sleep 2
        if is_running "$pid"; then
            echo "进程未响应，强制停止..."
            kill -9 "$pid" 2>/dev/null
        fi
    fi

    # 再次检查是否还有其他 bridge 进程
    for other_pid in $(get_all_bridge_pids); do
        echo "发现其他实例 PID: $other_pid，正在停止..."
        kill -9 "$other_pid" 2>/dev/null
    done

    rm -f "$PIDFILE" ~/.claude/telegram_pending ~/.claude/telegram_chat_id
    echo "Bridge 已停止"
}

# 启动
start() {
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        echo "Error: TELEGRAM_BOT_TOKEN not set"
        exit 1
    fi

    # 先停止所有实例确保干净
    stop >/dev/null 2>&1
    sleep 1

    # 再次确认没有其他实例
    local remaining=$(get_all_bridge_pids | wc -l)
    if [ "$remaining" -gt 0 ]; then
        echo "警告：发现 $remaining 个残留进程，强制清理..."
        kill_all
        sleep 1
    fi

    # 启动新实例
    cd "$SCRIPT_DIR" || exit 1
    nohup python3 -u "$BRIDGE_SCRIPT" > "$LOGFILE" 2>&1 &
    local new_pid=$!
    echo "$new_pid" > "$PIDFILE"

    sleep 1
    if is_running "$new_pid"; then
        echo "Bridge 启动成功. PID: $new_pid"
        echo "日志: tail -f $LOGFILE"
    else
        echo "Bridge 启动失败，检查日志: $LOGFILE"
        rm -f "$PIDFILE"
        exit 1
    fi
}

# 状态检查
status() {
    local pid=$(get_current_bridge_pid)
    local all_pids=$(get_all_bridge_pids)
    local total_count=$(echo "$all_pids" | grep -c '^' || echo 0)

    echo "=== Bridge 状态 ==="
    echo "脚本目录: $SCRIPT_DIR"
    echo "PID 文件: $PIDFILE"

    if [ -n "$pid" ] && is_running "$pid"; then
        echo "当前实例: 运行中 (PID: $pid)"
    else
        echo "当前实例: 未运行"
    fi

    echo ""
    echo "系统中所有 bridge.py 进程 ($total_count 个):"
    if [ "$total_count" -gt 0 ]; then
        ps aux | grep -E "python.*bridge\.py" | grep -v grep | awk '{printf "  PID: %s  启动时间: %s %s %s\n", $2, $9, $10, $11}'
    else
        echo "  无"
    fi

    if [ "$total_count" -gt 1 ]; then
        echo ""
        echo "警告: 发现多个实例！这会导致消息重复。"
        echo "建议运行: $0 kill-all 然后 $0 start"
    fi
}

# 主逻辑
case "${1:-}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    status)
        status
        ;;
    kill-all)
        kill_all
        ;;
    *)
        usage
        ;;
esac
