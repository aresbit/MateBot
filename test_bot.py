#!/usr/bin/env python3
import os
import urllib.request
import json

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

def test_bot():
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req, timeout=30)
        result = json.loads(response.read())
        print(f"Bot info: {json.dumps(result, indent=2)}")
        return result.get('ok', False)
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing bot connection...")
    if test_bot():
        print("Bot is working!")
    else:
        print("Bot connection failed!")
