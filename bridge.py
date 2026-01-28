#!/usr/bin/env python3
"""MateCode - Claude Code Telegram Bridge (Polling Mode)"""

import os
import json
import subprocess
import threading
import time
import urllib.request
from pathlib import Path

# Configuration
TMUX_SESSION = os.environ.get("TMUX_SESSION", "claude")
CHAT_ID_FILE = os.path.expanduser("~/.claude/telegram_chat_id")
PENDING_FILE = os.path.expanduser("~/.claude/telegram_pending")
HISTORY_FILE = os.path.expanduser("~/.claude/history.jsonl")
UPDATE_OFFSET_FILE = os.path.expanduser("~/.claude/telegram_offset")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

BOT_COMMANDS = [
    {"command": "clear", "description": "Clear conversation"},
    {"command": "resume", "description": "Resume session (shows picker)"},
    {"command": "continue_", "description": "Continue most recent session"},
    {"command": "loop", "description": "Ralph Loop: /loop <prompt>"},
    {"command": "stop", "description": "Interrupt Claude (Escape)"},
    {"command": "status", "description": "Check tmux status"},
]

BLOCKED_COMMANDS = [
    "/mcp", "/help", "/settings", "/config", "/model", "/compact", "/cost",
    "/doctor", "/init", "/login", "/logout", "/memory", "/permissions",
    "/pr", "/review", "/terminal", "/vim", "/approved-tools", "/listen"
]


def telegram_api(method, data):
    """Make a request to the Telegram Bot API."""
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set")
        return None
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode() if data else None,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"Telegram API error: {e}")
        return None


def get_updates(offset=None):
    """Fetch updates from Telegram."""
    data = {"timeout": 30}
    if offset:
        data["offset"] = offset
    return telegram_api("getUpdates", data)


def setup_bot_commands():
    """Register bot commands with Telegram."""
    result = telegram_api("setMyCommands", {"commands": BOT_COMMANDS})
    if result and result.get("ok"):
        print("Bot commands registered")


def send_typing_loop(chat_id):
    """Send typing action periodically while pending."""
    while os.path.exists(PENDING_FILE):
        telegram_api("sendChatAction", {"chat_id": chat_id, "action": "typing"})
        time.sleep(4)


def reply(chat_id, text):
    """Send a text message to a chat."""
    telegram_api("sendMessage", {"chat_id": chat_id, "text": text})


# ============ Tmux Functions ============

def tmux_exists():
    """Check if tmux session exists."""
    return subprocess.run(["tmux", "has-session", "-t", TMUX_SESSION], capture_output=True).returncode == 0


def tmux_send(text, literal=True):
    """Send text to tmux session."""
    cmd = ["tmux", "send-keys", "-t", TMUX_SESSION]
    if literal:
        cmd.append("-l")
    cmd.append(text)
    subprocess.run(cmd)


def tmux_send_enter():
    """Send Enter key to tmux."""
    subprocess.run(["tmux", "send-keys", "-t", TMUX_SESSION, "Enter"])


def tmux_send_escape():
    """Send Escape key to tmux."""
    subprocess.run(["tmux", "send-keys", "-t", TMUX_SESSION, "Escape"])


# ============ Session Management ============

def get_recent_sessions(limit=5):
    """Get list of recent Claude sessions."""
    if not os.path.exists(HISTORY_FILE):
        return []
    sessions = []
    try:
        with open(HISTORY_FILE) as f:
            for line in f:
                try:
                    sessions.append(json.loads(line.strip()))
                except:
                    continue
    except:
        return []
    sessions.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
    return sessions[:limit]


def get_session_id(project_path):
    """Get session ID from project path."""
    encoded = project_path.replace("/", "-").lstrip("-")
    for prefix in [f"-{encoded}", encoded]:
        project_dir = Path.home() / ".claude" / "projects" / prefix
        if project_dir.exists():
            jsonls = list(project_dir.glob("*.jsonl"))
            if jsonls:
                return max(jsonls, key=lambda p: p.stat().st_mtime).stem
    return None


# ============ Response Monitor ============

def find_latest_transcript():
    """Find the most recent Claude transcript file."""
    transcripts_dir = Path.home() / ".claude" / "transcripts"
    if not transcripts_dir.exists():
        return None
    transcript_files = list(transcripts_dir.glob("*.jsonl"))
    if not transcript_files:
        return None
    return max(transcript_files, key=lambda p: p.stat().st_mtime)


def extract_assistant_responses(transcript_path, last_response_pos=0):
    """Extract assistant responses from transcript starting from a position."""
    if not transcript_path or not transcript_path.exists():
        return "", 0

    responses = []
    current_pos = 0

    try:
        with open(transcript_path, 'r') as f:
            for line in f:
                current_pos += len(line)
                if current_pos <= last_response_pos:
                    continue

                try:
                    entry = json.loads(line.strip())
                    if entry.get("type") == "assistant":
                        message = entry.get("message", {})
                        content_blocks = message.get("content", [])
                        for block in content_blocks:
                            if block.get("type") == "text":
                                responses.append(block.get("text", ""))
                except:
                    continue
    except Exception as e:
        print(f"Error reading transcript: {e}")
        return "", last_response_pos

    return "\n\n".join(responses).strip(), current_pos


class ResponseMonitor:
    """Monitor Claude responses and send them to Telegram."""

    def __init__(self, check_interval=1.0):
        self.check_interval = check_interval
        self.monitor_thread = None
        self.running = False
        self.last_transcript_path = None
        self.last_position = 0

    def start(self):
        """Start the response monitor."""
        if self.running:
            return
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("Response monitor started")

    def stop(self):
        """Stop the response monitor."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)

    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.running:
            try:
                self._check_for_responses()
            except Exception as e:
                print(f"Response monitor error: {e}")
            time.sleep(self.check_interval)

    def _check_for_responses(self):
        """Check for new assistant responses and send to Telegram."""
        if not os.path.exists(PENDING_FILE):
            self.last_transcript_path = None
            self.last_position = 0
            return

        transcript_path = find_latest_transcript()
        if not transcript_path:
            return

        if self.last_transcript_path != transcript_path:
            self.last_transcript_path = transcript_path
            self.last_position = 0

        responses, new_position = extract_assistant_responses(
            transcript_path, self.last_position
        )

        if responses and new_position > self.last_position:
            if not os.path.exists(CHAT_ID_FILE):
                return

            try:
                with open(CHAT_ID_FILE) as f:
                    chat_id = int(f.read().strip())

                print(f"Sending response to {chat_id}: {responses[:50]}...")
                reply(chat_id, responses)

                if os.path.exists(PENDING_FILE):
                    os.remove(PENDING_FILE)

            except Exception as e:
                print(f"Error sending response: {e}")

            self.last_position = new_position


# Global response monitor instance
response_monitor = ResponseMonitor()


# ============ Bot Handler ============

class BotHandler:
    """Handle Telegram bot updates."""

    def __init__(self):
        self.offset = self.load_offset()

    def load_offset(self):
        """Load update offset from file."""
        if os.path.exists(UPDATE_OFFSET_FILE):
            try:
                with open(UPDATE_OFFSET_FILE) as f:
                    return int(f.read().strip())
            except:
                pass
        return 0

    def save_offset(self, offset):
        """Save update offset to file."""
        with open(UPDATE_OFFSET_FILE, "w") as f:
            f.write(str(offset))

    def handle_message(self, msg):
        """Process incoming message from Telegram."""
        text = msg.get("text", "")
        chat_id = msg.get("chat", {}).get("id")
        msg_id = msg.get("message_id")

        if not text or not chat_id:
            return

        # Save chat ID for hook script
        with open(CHAT_ID_FILE, "w") as f:
            f.write(str(chat_id))

        # Handle commands
        if text.startswith("/"):
            cmd = text.split()[0].lower()

            if cmd == "/status":
                status = "running" if tmux_exists() else "not found"
                reply(chat_id, f"tmux '{TMUX_SESSION}': {status}")
                return

            if cmd == "/stop":
                if tmux_exists():
                    tmux_send_escape()
                if os.path.exists(PENDING_FILE):
                    os.remove(PENDING_FILE)
                reply(chat_id, "Interrupted")
                return

            if cmd == "/clear":
                if not tmux_exists():
                    reply(chat_id, "tmux not found")
                    return
                tmux_send_escape()
                time.sleep(0.2)
                tmux_send("/clear")
                tmux_send_enter()
                reply(chat_id, "Cleared")
                return

            if cmd == "/continue_":
                if not tmux_exists():
                    reply(chat_id, "tmux not found")
                    return
                tmux_send_escape()
                time.sleep(0.2)
                tmux_send("/exit")
                tmux_send_enter()
                time.sleep(0.5)
                tmux_send("claude --continue --dangerously-skip-permissions")
                tmux_send_enter()
                reply(chat_id, "Continuing...")
                return

            if cmd == "/loop":
                if not tmux_exists():
                    reply(chat_id, "tmux not found")
                    return
                parts = text.split(maxsplit=1)
                if len(parts) < 2:
                    reply(chat_id, "Usage: /loop <prompt>")
                    return
                prompt = parts[1].replace('"', '\\"')
                full = f'{prompt} Output <promise>DONE</promise> when complete.'
                with open(PENDING_FILE, "w") as f:
                    f.write(str(int(time.time())))
                threading.Thread(target=send_typing_loop, args=(chat_id,), daemon=True).start()
                tmux_send(f'/ralph-loop:ralph-loop "{full}" --max-iterations 5 --completion-promise "DONE"')
                time.sleep(0.3)
                tmux_send_enter()
                reply(chat_id, "Ralph Loop started (max 5 iterations)")
                return

            if cmd == "/resume":
                sessions = get_recent_sessions()
                if not sessions:
                    reply(chat_id, "No sessions")
                    return
                kb = [[{"text": "Continue most recent", "callback_data": "continue_recent"}]]
                for s in sessions:
                    sid = get_session_id(s.get("project", ""))
                    if sid:
                        kb.append([{"text": s.get("display", "?")[:40] + "...", "callback_data": f"resume:{sid}"}])
                telegram_api("sendMessage", {"chat_id": chat_id, "text": "Select session:", "reply_markup": {"inline_keyboard": kb}})
                return

            if cmd in BLOCKED_COMMANDS:
                reply(chat_id, f"'{cmd}' not supported (interactive)")
                return

        # Regular message
        print(f"[{chat_id}] {text[:50]}...")
        with open(PENDING_FILE, "w") as f:
            f.write(str(int(time.time())))

        if msg_id:
            telegram_api("setMessageReaction", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "reaction": [{"type": "emoji", "emoji": "\u2705"}]
            })

        if not tmux_exists():
            reply(chat_id, "tmux not found")
            os.remove(PENDING_FILE)
            return

        threading.Thread(target=send_typing_loop, args=(chat_id,), daemon=True).start()
        tmux_send(text)
        tmux_send_enter()

    def handle_callback_query(self, callback_query):
        """Process callback queries (inline button clicks)."""
        query_id = callback_query.get("id")
        chat_id = callback_query.get("message", {}).get("chat", {}).get("id")
        data = callback_query.get("data", "")

        telegram_api("answerCallbackQuery", {"callback_query_id": query_id})

        if not chat_id or not data:
            return

        if not tmux_exists():
            reply(chat_id, "tmux session not found")
            return

        print(f"Callback from {chat_id}: {data}")

        try:
            if data.startswith("resume:"):
                session_id = data.split(":", 1)[1]
                tmux_send_escape()
                time.sleep(0.2)
                tmux_send("/exit")
                tmux_send_enter()
                time.sleep(0.5)
                tmux_send(f"claude --resume {session_id} --dangerously-skip-permissions")
                tmux_send_enter()
                reply(chat_id, f"Resuming: {session_id[:8]}...")
            elif data == "continue_recent":
                tmux_send_escape()
                time.sleep(0.2)
                tmux_send("/exit")
                tmux_send_enter()
                time.sleep(0.5)
                tmux_send("claude --continue --dangerously-skip-permissions")
                tmux_send_enter()
                reply(chat_id, "Continuing most recent...")
        except Exception as e:
            print(f"Error handling callback: {e}")
            reply(chat_id, f"Error: {str(e)}")

    def poll_updates(self):
        """Main polling loop."""
        setup_bot_commands()
        print(f"MateCode Bridge started | tmux: {TMUX_SESSION}")
        print(f"Offset: {self.offset}")

        # Start response monitor
        response_monitor.start()

        try:
            while True:
                try:
                    result = get_updates(self.offset)
                    if not result or not result.get("ok"):
                        time.sleep(5)
                        continue

                    updates = result.get("result", [])
                    for update in updates:
                        update_id = update.get("update_id", 0)

                        try:
                            if "message" in update:
                                self.handle_message(update["message"])
                            elif "callback_query" in update:
                                self.handle_callback_query(update["callback_query"])
                        except Exception as e:
                            print(f"Error handling update {update_id}: {e}")

                        self.offset = update_id + 1
                        self.save_offset(self.offset)

                    if not updates:
                        time.sleep(1)

                except KeyboardInterrupt:
                    print("\nStopping...")
                    break
                except Exception as e:
                    print(f"Polling error: {e}")
                    time.sleep(5)
        finally:
            response_monitor.stop()


def main():
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set")
        return 1

    handler = BotHandler()
    handler.poll_updates()
    return 0


if __name__ == "__main__":
    exit(main())
