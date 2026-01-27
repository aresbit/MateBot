#!/bin/bash
# Stop all bridge-related processes

echo "Stopping all bridge processes..."

# Kill bridge.py processes
pkill -f "bridge\.py" 2>/dev/null

# Kill bridge-polling.py processes
pkill -f "bridge-polling\.py" 2>/dev/null

# Wait for processes to terminate
sleep 2

# Force kill if still running
if pgrep -f "bridge\.py" >/dev/null 2>&1; then
    echo "Force killing bridge.py processes..."
    pgrep -f "bridge\.py" | xargs -r kill -9
fi

if pgrep -f "bridge-polling\.py" >/dev/null 2>&1; then
    echo "Force killing bridge-polling.py processes..."
    pgrep -f "bridge-polling\.py" | xargs -r kill -9
fi

# Clean up pending files
echo "Cleaning up pending files..."
rm -f ~/.claude/telegram_pending
rm -f ~/.claude/telegram_chat_id

echo "All bridge processes stopped."