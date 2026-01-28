#!/bin/bash
# Stop the bridge

echo "Stopping bridge..."
pkill -f "bridge.py" 2>/dev/null
sleep 1
rm -f bridge.pid ~/.claude/telegram_pending ~/.claude/telegram_chat_id
echo "Bridge stopped."
