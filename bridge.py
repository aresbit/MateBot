#!/usr/bin/env python3
"""MateCode - Claude Code Telegram Bridge (Polling Mode)"""

import json
import os
import re
import subprocess
import threading
import time
import urllib.request
from pathlib import Path

from memory import get_memory

# Configuration
TMUX_SESSION = os.environ.get("TMUX_SESSION", "claude")
CHAT_ID_FILE = os.path.expanduser("~/.claude/telegram_chat_id")
PENDING_FILE = os.path.expanduser("~/.claude/telegram_pending")
HISTORY_FILE = os.path.expanduser("~/.claude/history.jsonl")
UPDATE_OFFSET_FILE = os.path.expanduser("~/.claude/telegram_offset")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

MEMORY_ENABLED = os.environ.get("MEMORY_ENABLED", "true").lower() == "true"
MEMORY_MAX_RESULTS = int(os.environ.get("MEMORY_MAX_RESULTS", "5"))
MEMORY_MAX_CONTEXT = int(os.environ.get("MEMORY_MAX_CONTEXT", "2000"))

DEFAULT_AUTO_MEMORY_INSTRUCTION = """【记忆模式 - 系统编程优化版】

仅在以下场景触发记忆（避免无意义内容）：
- 架构决策、API设计、性能优化
- Bug发现及修复方案
- 引入新依赖/工具/技术栈
- 安全/并发/内存管理相关

格式 (-- memory 块会自动过滤，用户不可见)：
-- memory
ctx  = 项目上下文或文件路径
type = decision|bug|perf|security|api|tool|refactor
key  = 关键信息（一句话摘要）
--

多行值缩进示例：
-- memory
ctx  = src/memory.py
type = bugfix
key  = FTS5删除顺序错误，需先删索引再删主表
     = 原因是 content_rowid=rowid 的外键约束
--

无记忆内容时输出空标记：
-- memory
--"""

BOT_COMMANDS = [
    {"command": "clear", "description": "Clear conversation"},
    {"command": "resume", "description": "Resume session (shows picker)"},
    {"command": "continue_", "description": "Continue most recent session"},
    {"command": "stop", "description": "Interrupt Claude (Escape)"},
    {"command": "status", "description": "Check tmux status"},
    {"command": "remember", "description": "Save to memory: /remember <text>"},
    {"command": "recall", "description": "Search memories: /recall <query>"},
    {"command": "forget", "description": "Delete memory: /forget <query>"},
]

BLOCKED_COMMANDS = {
    "/mcp", "/help", "/settings", "/config", "/model", "/compact", "/cost",
    "/doctor", "/init", "/login", "/logout", "/memory", "/permissions",
    "/pr", "/review", "/terminal", "/vim", "/approved-tools", "/listen"
}

# Global state
recent_messages = {}
recent_full_prompts = {}


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


def tmux_exists():
    """Check if tmux session exists."""
    return subprocess.run(
        ["tmux", "has-session", "-t", TMUX_SESSION],
        capture_output=True
    ).returncode == 0


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


def load_claude_md() -> str:
    """Load .CLAUDE.md from project or home directory."""
    paths = [Path(".CLAUDE.md"), Path.home() / ".claude" / ".CLAUDE.md"]
    for path in paths:
        if path.exists():
            try:
                return path.read_text(encoding="utf-8")
            except Exception as e:
                print(f"Error reading {path}: {e}")
    return ""


def extract_meta_prompt(claude_md_content: str) -> str:
    """Extract the meta-prompt section from .CLAUDE.md content."""
    if not claude_md_content:
        return ""

    lines = claude_md_content.split("\n")
    in_initial_prompt = False
    prompt_lines = []

    for line in lines:
        if line.strip() == "## 初始提示词":
            in_initial_prompt = True
            continue
        if in_initial_prompt:
            if line.startswith("## "):
                break
            prompt_lines.append(line)

    return "\n".join(prompt_lines).strip()


def extract_memory_update(response: str) -> tuple[str, str]:
    """Extract memory update from Claude's response using CCL-style format."""
    pattern = r"--\s*memory\s*\n(.*?)\n--"
    match = re.search(pattern, response, re.DOTALL)

    if match:
        memory_content = match.group(1).strip()
        cleaned_response = re.sub(pattern + r"\s*", "", response, flags=re.DOTALL).strip()
        return cleaned_response, memory_content

    return response, ""


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


def find_latest_transcript():
    """Find the most recent Claude transcript file."""
    search_paths = [
        Path.home() / ".claude" / "transcripts",
        Path.home() / ".claude" / "projects",
    ]

    all_transcripts = []

    for path in search_paths:
        if not path.exists():
            continue
        if path.name == "projects":
            for project_dir in path.iterdir():
                if project_dir.is_dir():
                    all_transcripts.extend(project_dir.glob("*.jsonl"))
        else:
            all_transcripts.extend(path.glob("*.jsonl"))

    return max(all_transcripts, key=lambda p: p.stat().st_mtime) if all_transcripts else None


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
                        for block in message.get("content", []):
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

        responses, new_position = extract_assistant_responses(transcript_path, self.last_position)

        if not responses or new_position <= self.last_position:
            return

        if not os.path.exists(CHAT_ID_FILE):
            return

        try:
            with open(CHAT_ID_FILE) as f:
                chat_id = int(f.read().strip())

            cleaned_responses, memory_update = extract_memory_update(responses)
            print(f"Sending response to {chat_id}: {cleaned_responses[:50]}...")
            reply(chat_id, cleaned_responses)

            self._save_to_memory(chat_id, cleaned_responses, memory_update)

            if os.path.exists(PENDING_FILE):
                os.remove(PENDING_FILE)

        except Exception as e:
            print(f"Error sending response: {e}")

        self.last_position = new_position

    def _save_to_memory(self, chat_id, cleaned_responses, memory_update):
        """Save conversation to memory."""
        if not MEMORY_ENABLED:
            return

        try:
            memory = get_memory()
            chat_id_str = str(chat_id)

            if chat_id_str in recent_messages:
                user_msg = recent_messages[chat_id_str]
                memory.add(
                    chat_id_str,
                    f"Q: {user_msg}\nA: {cleaned_responses[:2000]}",
                    metadata={"type": "conversation"}
                )
                print(f"Saved conversation to memory for {chat_id}")
                recent_messages.pop(chat_id_str, None)
                recent_full_prompts.pop(chat_id_str, None)

            if memory_update:
                memory.add(
                    chat_id_str,
                    memory_update[:5000],
                    metadata={"type": "meta_update", "auto": True},
                    message_type="meta_update"
                )
                print(f"Saved meta-update to memory for {chat_id}")

        except Exception as e:
            print(f"Error saving to memory: {e}")


response_monitor = ResponseMonitor()


class BotHandler:
    """Handle Telegram bot updates."""

    def __init__(self):
        self.offset = self._load_offset()
        self._session_initialized = False

    def _load_offset(self):
        """Load update offset from file."""
        if os.path.exists(UPDATE_OFFSET_FILE):
            try:
                with open(UPDATE_OFFSET_FILE) as f:
                    return int(f.read().strip())
            except:
                pass
        return 0

    def _save_offset(self, offset):
        """Save update offset to file."""
        with open(UPDATE_OFFSET_FILE, "w") as f:
            f.write(str(offset))

    def _require_tmux(self, chat_id):
        """Check if tmux exists, reply with error if not."""
        if not tmux_exists():
            reply(chat_id, "tmux not found")
            return False
        return True

    def _start_typing(self, chat_id):
        """Start typing indicator."""
        with open(PENDING_FILE, "w") as f:
            f.write(str(int(time.time())))
        threading.Thread(target=send_typing_loop, args=(chat_id,), daemon=True).start()

    def _get_or_init_auto_memory_instruction(self) -> str:
        """Get auto-memory instruction from DB, initialize if not exists."""
        if not MEMORY_ENABLED:
            return DEFAULT_AUTO_MEMORY_INSTRUCTION

        try:
            memory = get_memory()
            results = memory.get_by_type("system", "meta_instruction", limit=1)
            if results:
                return results[0]["content"]

            memory.add(
                "system",
                DEFAULT_AUTO_MEMORY_INSTRUCTION,
                metadata={"type": "self_referential", "auto": False},
                message_type="meta_instruction"
            )
            print("Initialized self-referential meta-instruction in DB")
            return DEFAULT_AUTO_MEMORY_INSTRUCTION
        except Exception as e:
            print(f"Error loading meta-instruction: {e}")
            return DEFAULT_AUTO_MEMORY_INSTRUCTION

    def _build_full_prompt(self, text, chat_id, is_new_session=False):
        """Build full prompt with memory context, meta-prompt, and auto-memory instruction."""
        prompt_parts = []

        instruction = self._get_or_init_auto_memory_instruction()
        prompt_parts.append(instruction)

        if MEMORY_ENABLED:
            try:
                memory = get_memory()
                memories = memory.search(str(chat_id), text, limit=MEMORY_MAX_RESULTS)
                if memories:
                    memory_text = memory.format_for_prompt(memories, max_chars=MEMORY_MAX_CONTEXT)
                    if memory_text:
                        prompt_parts.append(memory_text)
                        print(f"Injected {len(memories)} memories into context")
            except Exception as e:
                print(f"Memory search error: {e}")

        if is_new_session or not hasattr(self, '_session_initialized'):
            claude_md_content = load_claude_md()
            meta_prompt = extract_meta_prompt(claude_md_content)
            if meta_prompt:
                prompt_parts.append(f"【系统指令】\n{meta_prompt}")
                print(f"Injected CLAUDE.md meta-prompt ({len(meta_prompt)} chars)")
            self._session_initialized = True

        if prompt_parts:
            return "\n\n---\n\n".join(prompt_parts) + f"\n\n---\n\n{text}"
        return text

    def handle_message(self, msg):
        """Process incoming message from Telegram."""
        text = msg.get("text", "")
        chat_id = msg.get("chat", {}).get("id")
        msg_id = msg.get("message_id")

        if not text or not chat_id:
            return

        with open(CHAT_ID_FILE, "w") as f:
            f.write(str(chat_id))

        if text.startswith("/"):
            return self._handle_command(text, chat_id)

        print(f"[{chat_id}] {text[:50]}...")

        full_prompt = self._build_full_prompt(text, chat_id)

        with open(PENDING_FILE, "w") as f:
            f.write(str(int(time.time())))

        if msg_id:
            telegram_api("setMessageReaction", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "reaction": [{"type": "emoji", "emoji": "✅"}]
            })

        if not self._require_tmux(chat_id):
            os.remove(PENDING_FILE)
            return

        self._start_typing(chat_id)

        recent_messages[str(chat_id)] = text
        recent_full_prompts[str(chat_id)] = full_prompt

        tmux_send(full_prompt)
        tmux_send_enter()

    def _handle_command(self, text, chat_id):
        """Handle bot commands."""
        parts = text.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        handlers = {
            "/status": self._cmd_status,
            "/stop": self._cmd_stop,
            "/clear": self._cmd_clear,
            "/continue_": self._cmd_continue,
            "/resume": self._cmd_resume,
            "/remember": self._cmd_remember,
            "/recall": self._cmd_recall,
            "/forget": self._cmd_forget,
            "/memstats": self._cmd_memstats,
        }

        if cmd in handlers:
            handlers[cmd](chat_id, args)
        elif cmd in BLOCKED_COMMANDS:
            reply(chat_id, f"'{cmd}' not supported (interactive)")

    def _cmd_status(self, chat_id, _):
        status = "running" if tmux_exists() else "not found"
        reply(chat_id, f"tmux '{TMUX_SESSION}': {status}")

    def _cmd_stop(self, chat_id, _):
        if tmux_exists():
            tmux_send_escape()
        if os.path.exists(PENDING_FILE):
            os.remove(PENDING_FILE)
        reply(chat_id, "Interrupted")

    def _cmd_clear(self, chat_id, _):
        if not self._require_tmux(chat_id):
            return
        self._session_initialized = False
        tmux_send_escape()
        time.sleep(0.2)
        tmux_send("/clear")
        tmux_send_enter()
        reply(chat_id, "Cleared")

    def _cmd_continue(self, chat_id, _):
        if not self._require_tmux(chat_id):
            return
        self._session_initialized = False
        tmux_send_escape()
        time.sleep(0.2)
        tmux_send("/exit")
        tmux_send_enter()
        time.sleep(0.5)
        tmux_send("claude --continue --dangerously-skip-permissions")
        tmux_send_enter()
        reply(chat_id, "Continuing...")

    def _cmd_resume(self, chat_id, _):
        self._session_initialized = False
        sessions = get_recent_sessions()
        if not sessions:
            reply(chat_id, "No sessions")
            return

        kb = [[{"text": "Continue most recent", "callback_data": "continue_recent"}]]
        for s in sessions:
            sid = get_session_id(s.get("project", ""))
            if sid:
                kb.append([{"text": s.get("display", "?")[:40] + "...", "callback_data": f"resume:{sid}"}])

        telegram_api("sendMessage", {
            "chat_id": chat_id,
            "text": "Select session:",
            "reply_markup": {"inline_keyboard": kb}
        })

    def _cmd_remember(self, chat_id, args):
        if not args:
            reply(chat_id, "Usage: /remember <text>")
            return

        memory = get_memory()
        if memory.add(str(chat_id), args, metadata={"type": "manual"}):
            reply(chat_id, "✅ Saved to memory")
        else:
            reply(chat_id, "❌ Failed to save")

    def _cmd_recall(self, chat_id, args):
        memory = get_memory()

        if args:
            results = memory.search(str(chat_id), args, limit=10)
        else:
            results = memory.get_recent(str(chat_id), limit=10)

        if not results:
            reply(chat_id, "No memories found")
            return

        lines = ["📚 Your memories:", ""]
        for i, mem in enumerate(results[:10], 1):
            content = mem["content"][:100]
            if len(mem["content"]) > 100:
                content += "..."
            lines.append(f"{i}. {content}")

        reply(chat_id, "\n".join(lines))

    def _cmd_forget(self, chat_id, args):
        if not args:
            reply(chat_id, "Usage: /forget <query or 'all'>")
            return

        memory = get_memory()

        if args.lower() == "all":
            if memory.clear_all(str(chat_id)):
                reply(chat_id, "🗑️ All memories cleared")
            else:
                reply(chat_id, "❌ Failed to clear")
        else:
            count = memory.delete_by_query(str(chat_id), args)
            reply(chat_id, f"🗑️ Deleted {count} memory(s)")

    def _cmd_memstats(self, chat_id, _):
        memory = get_memory()
        stats = memory.get_stats(str(chat_id))
        type_info = "\n".join([f"  {t}: {c}" for t, c in stats.get("by_type", {}).items()])
        reply(chat_id,
            f"📊 Memory Stats:\n"
            f"Total: {stats['count']} memories\n"
            f"Newest: {stats['newest'] or 'N/A'}\n"
            f"Oldest: {stats['oldest'] or 'N/A'}\n"
            f"By type:\n{type_info or '  N/A'}")

    def handle_callback_query(self, callback_query):
        """Process callback queries (inline button clicks)."""
        query_id = callback_query.get("id")
        chat_id = callback_query.get("message", {}).get("chat", {}).get("id")
        data = callback_query.get("data", "")

        telegram_api("answerCallbackQuery", {"callback_query_id": query_id})

        if not chat_id or not data:
            return

        if not self._require_tmux(chat_id):
            return

        print(f"Callback from {chat_id}: {data}")

        try:
            if data.startswith("resume:"):
                self._session_initialized = False
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
                self._session_initialized = False
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
                        self._save_offset(self.offset)

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
