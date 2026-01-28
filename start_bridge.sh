#!/bin/bash
# Start the bridge (polling mode)

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "Error: TELEGRAM_BOT_TOKEN not set"
    exit 1
fi

./stop_bridge.sh 2>/dev/null

nohup python3 bridge.py > bridge.log 2>&1 &
echo "Bridge started. PID: $!"
