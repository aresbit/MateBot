#!/bin/bash
# Start bridge in polling mode

# Check if TELEGRAM_BOT_TOKEN is set
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "Error: TELEGRAM_BOT_TOKEN environment variable not set"
    echo "Please run: export TELEGRAM_BOT_TOKEN=your_token"
    exit 1
fi

# Stop any existing bridge processes
./stop_bridge.sh

# Ask user which version to use
echo "Select bridge version:"
echo "1) bridge.py (supports both webhook and polling)"
echo "2) bridge-polling.py (dedicated polling version)"
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo "Starting bridge.py in polling mode..."
        nohup python3 bridge.py --mode polling > bridge.log 2>&1 &
        ;;
    2)
        echo "Starting bridge-polling.py..."
        nohup python3 bridge-polling.py > bridge-polling.log 2>&1 &
        ;;
    *)
        echo "Invalid choice. Starting bridge.py (default)..."
        nohup python3 bridge.py --mode polling > bridge.log 2>&1 &
        ;;
esac

echo "Bridge started. Check logs for status."
echo "To stop: ./stop_bridge.sh"