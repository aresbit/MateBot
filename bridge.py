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
from typing import Dict, List, Optional, Any
import queue

from memory import get_memory
from attention_manager import AttentionManager, StablePromptBuilder
from failure_memory import get_failure_memory
from opencc_backend import OpenccSession, TelegramStreamRenderer, DEFAULT_CLI_PATH


class Config:
    """Centralized configuration management."""

    TMUX_SESSION = os.environ.get("TMUX_SESSION", "claude")
    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

    # File paths
    CLAUDE_DIR = Path.home() / ".claude"
    CHAT_ID_FILE = CLAUDE_DIR / "telegram_chat_id"
    PENDING_FILE = CLAUDE_DIR / "telegram_pending"
    HISTORY_FILE = CLAUDE_DIR / "history.jsonl"
    UPDATE_OFFSET_FILE = CLAUDE_DIR / "telegram_offset"
    SENT_OFFSET_FILE = CLAUDE_DIR / "telegram_sent_offset"

    # Memory settings
    MEMORY_ENABLED = os.environ.get("MEMORY_ENABLED", "true").lower() == "true"
    MEMORY_MAX_RESULTS = int(os.environ.get("MEMORY_MAX_RESULTS", "5"))
    MEMORY_MAX_CONTEXT = int(os.environ.get("MEMORY_MAX_CONTEXT", "2000"))

    # KV-Cache settings
    KV_CACHE_ENABLED = os.environ.get("KV_CACHE_ENABLED", "true").lower() == "true"
    KV_CACHE_TTL = int(os.environ.get("KV_CACHE_TTL", "3600"))  # 1 hour default

    # Telegram settings - disable attention manager for raw messages
    TELEGRAM_RAW_MESSAGES = os.environ.get("TELEGRAM_RAW_MESSAGES", "true").lower() == "true"

    # Delivery mode:
    #   HOOK_DELIVERY_ENABLED=true (default) — the Claude Code Stop hook
    #   (hooks/send-to-telegram.sh) owns TG delivery. The polling-based
    #   ResponseMonitor only saves memory and tracks state; it does NOT call
    #   reply() or remove the pending file. This eliminates the race where
    #   polling sent partial output and deleted the pending file before Stop
    #   fired, causing the hook to bail out.
    #
    #   HOOK_DELIVERY_ENABLED=false — legacy behavior: polling sends to TG.
    HOOK_DELIVERY_ENABLED = os.environ.get("HOOK_DELIVERY_ENABLED", "true").lower() == "true"

    # OpenCC spawn mode: bypass tmux entirely and spawn vendor/opencc/cli.js
    # (reverse-engineered Claude CLI) with stream-json I/O. Enables true
    # event-driven streaming intermediate feedback to Telegram via
    # editMessageText. When enabled:
    #   - MessageQueue routes user messages to a persistent OpenccSession
    #     instead of tmux_send.
    #   - ResponseMonitor (transcript polling) is bypassed for chats served by
    #     spawn; the Stop hook is also bypassed (no pending file written).
    #   - One subprocess per chat_id, resumed across messages via --resume.
    OPENCC_SPAWN_MODE = os.environ.get("OPENCC_SPAWN_MODE", "false").lower() == "true"
    OPENCC_CLI_PATH = os.environ.get("OPENCC_CLI_PATH", str(DEFAULT_CLI_PATH))
    OPENCC_BUN_PATH = os.environ.get("OPENCC_BUN_PATH", "bun")
    OPENCC_MODEL = os.environ.get("OPENCC_MODEL", "")  # "" = CLI default
    OPENCC_CWD = os.environ.get("OPENCC_CWD", os.getcwd())

    # Bot commands
    BOT_COMMANDS = [
        {"command": "clear", "description": "Clear conversation"},
        {"command": "resume", "description": "Resume session (shows picker)"},
        {"command": "continue_", "description": "Continue most recent session"},
        {"command": "stop", "description": "Interrupt Claude (Escape)"},
        {"command": "status", "description": "Check tmux status"},
        {"command": "remember", "description": "Save to memory: /remember <text>"},
        {"command": "recall", "description": "Search memories: /recall <query>"},
        {"command": "forget", "description": "Delete memory: /forget <query>"},
        {"command": "task", "description": "Manage tasks: /task [goal]"},
        {"command": "todo", "description": "View/update todo: /todo [update]"},
        {"command": "failures", "description": "View failure lessons: /failures [stats|resolve ID]"},
        {"command": "lessons", "description": "View learned lessons: /lessons [query]"},
        {"command": "kvcache", "description": "KV-Cache statistics: /kvcache [clear]"},
    ]

    BLOCKED_COMMANDS = {
        "/mcp", "/help", "/settings", "/config", "/model", "/compact", "/cost",
        "/doctor", "/init", "/login", "/logout", "/memory", "/permissions",
        "/pr", "/review", "/terminal", "/vim", "/approved-tools", "/listen"
    }

    # Auto-memory instruction
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


# Global state
recent_messages: Dict[str, str] = {}
recent_full_prompts: Dict[str, str] = {}

# Function aliases for backward compatibility
def tmux_exists() -> bool:
    """Check if tmux session exists."""
    return TmuxManager.exists()

def reply(chat_id: int, text: str) -> bool:
    """Send a text message to a chat. Returns True on success."""
    return TelegramAPI.reply(chat_id, text)

def telegram_api(method: str, data: Optional[Dict] = None) -> Optional[Dict]:
    """Make a request to the Telegram Bot API."""
    return TelegramAPI.call(method, data)

def tmux_send(text: str, literal: bool = True) -> None:
    """Send text to tmux session."""
    TmuxManager.send(text, literal)

def tmux_send_enter() -> None:
    """Send Enter key to tmux."""
    TmuxManager.send_enter()

def tmux_send_escape() -> None:
    """Send Escape key to tmux."""
    TmuxManager.send_escape()

def send_typing_loop(chat_id: int) -> None:
    """Send typing action in a loop."""
    while os.path.exists(Config.PENDING_FILE):
        TelegramAPI.send_typing(chat_id)
        time.sleep(5)


def send_typing_loop_until(chat_id: int, done_predicate) -> None:
    """Like send_typing_loop, but stops when done_predicate() returns truthy.

    Used in OPENCC_SPAWN_MODE where there is no pending file — the renderer's
    `_closed` flag is the natural completion signal.
    """
    # Hard cap so a stuck process can't leak typing actions forever.
    deadline = time.time() + 600
    while time.time() < deadline:
        try:
            if done_predicate():
                return
        except Exception:
            return
        TelegramAPI.send_typing(chat_id)
        time.sleep(5)

def get_updates(offset: Optional[int] = None) -> Optional[Dict]:
    """Fetch updates from Telegram."""
    return TelegramAPI.get_updates(offset)

def setup_bot_commands() -> None:
    """Register bot commands with Telegram."""
    TelegramAPI.setup_bot_commands()


class TelegramAPI:
    """Telegram Bot API wrapper."""

    @staticmethod
    def call(method: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Make a request to the Telegram Bot API."""
        if not Config.BOT_TOKEN:
            print("Error: TELEGRAM_BOT_TOKEN not set")
            return None

        url = f"https://api.telegram.org/bot{Config.BOT_TOKEN}/{method}"
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

    @staticmethod
    def get_updates(offset: Optional[int] = None) -> Optional[Dict]:
        """Fetch updates from Telegram."""
        data = {"timeout": 30}
        if offset:
            data["offset"] = offset
        return TelegramAPI.call("getUpdates", data)

    @staticmethod
    def setup_bot_commands() -> None:
        """Register bot commands with Telegram."""
        result = TelegramAPI.call("setMyCommands", {"commands": Config.BOT_COMMANDS})
        if result and result.get("ok"):
            print("Bot commands registered")

    @staticmethod
    def send_typing(chat_id: int) -> None:
        """Send typing action."""
        TelegramAPI.call("sendChatAction", {"chat_id": chat_id, "action": "typing"})

    @staticmethod
    def reply(chat_id: int, text: str) -> bool:
        """Send a text message to a chat. Returns True on success, False on failure."""
        # Telegram has a 4096 character limit per message
        MAX_LENGTH = 4000  # Leave some margin

        if len(text) <= MAX_LENGTH:
            result = TelegramAPI.call("sendMessage", {"chat_id": chat_id, "text": text})
            return result is not None and result.get("ok", False)

        # Split long messages into chunks
        chunks = []
        current_chunk = ""

        for line in text.split('\n'):
            if len(current_chunk) + len(line) + 1 > MAX_LENGTH:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += '\n' + line if current_chunk else line

        if current_chunk:
            chunks.append(current_chunk)

        # Send chunks
        all_success = True
        for i, chunk in enumerate(chunks):
            prefix = f"[{i+1}/{len(chunks)}] " if len(chunks) > 1 else ""
            result = TelegramAPI.call("sendMessage", {"chat_id": chat_id, "text": prefix + chunk})
            if result is None or not result.get("ok", False):
                all_success = False

        return all_success


class TmuxManager:
    """Tmux session management."""

    @staticmethod
    def exists() -> bool:
        """Check if tmux session exists."""
        return subprocess.run(
            ["tmux", "has-session", "-t", Config.TMUX_SESSION],
            capture_output=True
        ).returncode == 0

    @staticmethod
    def send(text: str, literal: bool = True) -> None:
        """Send text to tmux session."""
        cmd = ["tmux", "send-keys", "-t", Config.TMUX_SESSION]
        if literal:
            cmd.append("-l")
        cmd.append(text)
        subprocess.run(cmd)

    @staticmethod
    def send_enter() -> None:
        """Send Enter key to tmux."""
        subprocess.run(["tmux", "send-keys", "-t", Config.TMUX_SESSION, "Enter"])

    @staticmethod
    def send_escape() -> None:
        """Send Escape key to tmux."""
        subprocess.run(["tmux", "send-keys", "-t", Config.TMUX_SESSION, "Escape"])


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
    # First, extract -- memory blocks
    memory_pattern = r"--\s*memory\s*\n(.*?)\n--"
    memory_match = re.search(memory_pattern, response, re.DOTALL)

    memory_content = ""
    cleaned_response = response

    if memory_match:
        memory_content = memory_match.group(1).strip()
        cleaned_response = re.sub(memory_pattern + r"\s*", "", response, flags=re.DOTALL).strip()

    # Extract and remove XML observation blocks (claude-mem output)
    # Pattern matches <observation>, <memory>, <fact>, <narrative>, <concept> tags
    # and their corresponding closing tags
    xml_pattern = r'<(observation|memory|fact|narrative|concept)\b.*?>.*?</\1>'
    xml_matches = list(re.finditer(xml_pattern, cleaned_response, re.DOTALL))

    if xml_matches:
        # Extract XML content for memory storage
        xml_contents = []
        for match in xml_matches:
            xml_contents.append(match.group(0).strip())  # Keep the full XML

        # Remove all XML observation blocks from the response
        cleaned_response = re.sub(xml_pattern, '', cleaned_response, flags=re.DOTALL).strip()

        # Add XML content to memory content
        if xml_contents:
            xml_text = '\n\n'.join(xml_contents)
            if memory_content:
                memory_content = f"{memory_content}\n\n{xml_text}"
            else:
                memory_content = xml_text

    # Clean up excessive blank lines (3 or more newlines -> 2 newlines)
    if cleaned_response:
        cleaned_response = re.sub(r'\n{3,}', '\n\n', cleaned_response)

    return cleaned_response, memory_content


def get_recent_sessions(limit=5):
    """Get list of recent Claude sessions."""
    if not os.path.exists(Config.HISTORY_FILE):
        return []

    sessions = []
    try:
        with open(Config.HISTORY_FILE) as f:
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


def extract_assistant_responses(transcript_path, last_response_pos=0, seen_message_ids=None):
    """Extract assistant responses from transcript starting from a position.

    Uses incremental reading - only processes new lines since last_position.
    Tracks seen line positions to avoid duplicates (not message IDs, because
    Claude transcript splits one message into multiple lines with different content types).
    """
    if not transcript_path or not transcript_path.exists():
        return "", 0, seen_message_ids or set()

    # We use seen_positions to track which lines we've already processed
    # This is more reliable than message IDs because one message can span multiple lines
    if seen_message_ids is None:
        seen_message_ids = set()

    responses = []
    current_pos = 0
    found_new_content = False

    try:
        with open(transcript_path, 'r') as f:
            lines = f.readlines()

        for line_idx, line in enumerate(lines):
            line_start_pos = current_pos
            current_pos += len(line)

            # Skip lines we've already processed
            if line_start_pos < last_response_pos:
                continue

            # Also skip if we've seen this exact line position before
            line_pos_key = f"{transcript_path}:{line_start_pos}"
            if line_pos_key in seen_message_ids:
                continue

            try:
                entry = json.loads(line.strip())
                if entry.get("type") == "assistant":
                    message = entry.get("message", {})

                    # Extract text blocks from this line only
                    text_content = []

                    # Extract content from all block types
                    content_blocks = message.get("content", [])
                    if not isinstance(content_blocks, list):
                        print(f"[DEBUG] Unexpected content type: {type(content_blocks)}")
                        content_blocks = []

                    for block in content_blocks:
                        if not isinstance(block, dict):
                            continue

                        block_type = block.get("type")

                        if block_type == "text":
                            text = block.get("text", "").strip()
                            # Skip XML observation blocks and empty text
                            if not text:
                                continue
                            # Skip pure XML blocks (like <observation> or <memory>)
                            # but allow text that happens to start with < (like code examples)
                            if text.startswith("<") and text.endswith(">") and "/" in text[1:]:
                                continue
                            # Skip markdown XML code blocks only
                            if text.startswith("```xml") or text.startswith("```\n<"):
                                continue
                            text_content.append(text)

                        elif block_type == "thinking":
                            # Skip thinking blocks - they are internal reasoning, not user-facing
                            continue

                        elif block_type == "tool_use":
                            # Format tool_use as Markdown code block
                            tool_name = block.get("name", "unknown_tool")
                            tool_input = block.get("input", {})
                            tool_id = block.get("id", "")
                            try:
                                input_str = json.dumps(tool_input, indent=2, ensure_ascii=False)
                            except Exception:
                                input_str = str(tool_input)
                            tool_text = f"🔧 Tool Use: `{tool_name}` (ID: `{tool_id}`)\n\n```json\n{input_str}\n```"
                            text_content.append(tool_text)

                        elif block_type == "tool_result":
                            # Format tool_result as Markdown code block
                            tool_content = block.get("content", "")
                            tool_use_id = block.get("tool_use_id", "")
                            is_error = block.get("is_error", False)

                            # Handle content that might be a list of blocks or a string
                            if isinstance(tool_content, list):
                                # Extract text from content blocks
                                content_parts = []
                                for item in tool_content:
                                    if isinstance(item, dict):
                                        if item.get("type") == "text":
                                            content_parts.append(item.get("text", ""))
                                        else:
                                            content_parts.append(str(item))
                                    else:
                                        content_parts.append(str(item))
                                tool_content_str = "\n".join(content_parts)
                            elif isinstance(tool_content, str):
                                tool_content_str = tool_content
                            else:
                                tool_content_str = str(tool_content)

                            # Truncate very long content
                            if len(tool_content_str) > 3000:
                                tool_content_str = tool_content_str[:3000] + "\n\n... (truncated)"

                            error_prefix = "❌ " if is_error else ""
                            tool_text = f"{error_prefix}📤 Tool Result (ID: `{tool_use_id}`):\n\n```\n{tool_content_str}\n```"
                            text_content.append(tool_text)

                        elif block_type == "artifact":
                            # Format artifact with metadata
                            artifact_id = block.get("id", "")
                            artifact_type = block.get("artifact_type", "")
                            artifact_title = block.get("title", "")
                            artifact_content = block.get("content", "")

                            # Determine language hint from artifact type
                            language_hint = ""
                            if artifact_type == "application/vnd.chat.code":
                                # Try to infer from title extension
                                if artifact_title.endswith(".py"):
                                    language_hint = "python"
                                elif artifact_title.endswith((".js", ".ts")):
                                    language_hint = "javascript"
                                elif artifact_title.endswith(".html"):
                                    language_hint = "html"
                                elif artifact_title.endswith(".css"):
                                    language_hint = "css"
                                elif artifact_title.endswith(".json"):
                                    language_hint = "json"
                                elif artifact_title.endswith(".sh"):
                                    language_hint = "bash"
                                elif artifact_title.endswith((".yml", ".yaml")):
                                    language_hint = "yaml"
                            elif artifact_type == "text/markdown":
                                language_hint = "markdown"
                            elif artifact_type == "text/html":
                                language_hint = "html"
                            elif artifact_type == "image/svg+xml":
                                language_hint = "svg"

                            artifact_text = f"📄 Artifact: {artifact_title}\nType: `{artifact_type}` | ID: `{artifact_id}`\n\n```{language_hint}\n{artifact_content}\n```"
                            text_content.append(artifact_text)

                    # Mark this line as processed
                    seen_message_ids.add(line_pos_key)

                    # Add content from this line
                    if text_content:
                        full_text = "\n".join(text_content)
                        responses.append(full_text)
                        found_new_content = True

            except (json.JSONDecodeError, KeyError):
                # Skip malformed lines
                continue

    except Exception as e:
        print(f"Error reading transcript: {e}")
        return "", last_response_pos, seen_message_ids

    # 如果没有找到新内容，保持原位置不变
    if not found_new_content:
        return "", last_response_pos, seen_message_ids

    return "\n\n".join(responses).strip(), current_pos, seen_message_ids


class PendingFileHandler:
    """Handle pending file creation events."""

    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event):
        if event.src_path.endswith('telegram_pending'):
            self.callback()

    def on_modified(self, event):
        if event.src_path.endswith('telegram_pending'):
            self.callback()


class ResponseMonitor:
    """Monitor Claude responses and send them to Telegram."""

    def __init__(self, check_interval=0.1):
        self.check_interval = check_interval
        self.monitor_thread = None
        self.running = False
        self.last_transcript_path = None
        self.last_position = 0
        self.response_queue = queue.Queue()
        self.observer = None
        self._checking = False
        self._seen_message_ids = set()  # Track processed message IDs for current file
        self._file_states = {}  # Track read positions per transcript file: {path: {'position': int, 'seen_ids': set}}
        self._cumulative_sent = {}  # Per-transcript cumulative sent char count for hook dedup

    def start(self):
        """Start the response monitor with file watching."""
        if self.running:
            return
        self.running = True

        # Start file watcher for immediate response detection
        self._start_file_watcher()

        # Also start the polling thread as backup
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("Response monitor started with file watching")

    def _start_file_watcher(self):
        """Start watching for transcript file updates using polling."""
        def file_watcher():
            last_transcript_mtime = 0
            pending_existed = False
            while self.running:
                try:
                    current_time = time.time()

                    # Check if pending file exists (indicates active request)
                    if os.path.exists(Config.PENDING_FILE):
                        # Find latest transcript and check its modification time
                        transcript_path = find_latest_transcript()
                        if transcript_path and transcript_path.exists():
                            mtime = transcript_path.stat().st_mtime
                            # Trigger check if transcript is new or modified
                            if mtime > last_transcript_mtime or not pending_existed:
                                print(f"[DEBUG] File watcher detected transcript update")
                                self._immediate_response_check()
                                last_transcript_mtime = mtime
                        pending_existed = True
                    else:
                        # Reset when request is complete
                        pending_existed = False
                        last_transcript_mtime = 0

                    time.sleep(0.05)  # 50ms polling interval
                except Exception as e:
                    print(f"[DEBUG] File watcher error: {e}")
                    time.sleep(0.1)

        watcher_thread = threading.Thread(target=file_watcher, daemon=True)
        watcher_thread.start()
        print(f"[DEBUG] File watcher started polling for transcript updates")

    def _immediate_response_check(self):
        """Immediate response check when pending file is detected."""
        try:
            # Wait a tiny bit for file to be fully written
            time.sleep(0.05)
            print(f"[DEBUG] Immediate response check triggered")
            self._check_for_responses()
        except Exception as e:
            print(f"[DEBUG] Immediate response check error: {e}")

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
        pending_exists = os.path.exists(Config.PENDING_FILE)

        # 如果没有 pending 文件，先检查是否还有未发送的响应（延迟发送问题）
        if not pending_exists:
            # 检查当前 transcript 是否还有新内容
            transcript_path = find_latest_transcript()
            if transcript_path and self.last_transcript_path == transcript_path:
                # 同一文件，检查是否有新内容
                responses, new_position, self._seen_message_ids = extract_assistant_responses(
                    transcript_path, self.last_position, self._seen_message_ids
                )
                if responses:
                    # 还有未发送的响应，继续发送
                    print(f"[DEBUG] Found pending response after pending file removed")
                    self._process_responses(transcript_path, responses, new_position)
                    return
            # 确实没有待发送内容，重置状态
            self.last_transcript_path = None
            self.last_position = 0
            self._seen_message_ids.clear()
            return
        else:
            print(f"[DEBUG] Response monitor found pending file, checking for responses...")

        # 添加锁机制，避免并发检查
        if hasattr(self, '_checking') and self._checking:
            print(f"[DEBUG] Already checking responses, skipping")
            return

        self._checking = True

        try:
            transcript_path = find_latest_transcript()
            if not transcript_path:
                return

            # 修复全量发送问题：使用持久化的位置跟踪
            # 为每个 transcript 文件维护独立的读取位置和已处理消息ID
            if self.last_transcript_path != transcript_path:
                # 切换到了新文件，保存旧文件的状态
                if self.last_transcript_path:
                    self._file_states[self.last_transcript_path] = {
                        'position': self.last_position,
                        'seen_ids': self._seen_message_ids.copy()
                    }
                # 加载新文件的状态（如果存在）
                self.last_transcript_path = str(transcript_path)
                if self.last_transcript_path in self._file_states:
                    saved_state = self._file_states[self.last_transcript_path]
                    self.last_position = saved_state['position']
                    self._seen_message_ids = saved_state['seen_ids'].copy()
                    print(f"[DEBUG] Restored state for {transcript_path.name}: pos={self.last_position}")
                else:
                    # 新文件，从头开始
                    self.last_position = 0
                    self._seen_message_ids.clear()
                    print(f"[DEBUG] New transcript file: {transcript_path.name}")

            # 使用增量读取，从上次位置开始读取新内容
            responses, new_position, self._seen_message_ids = extract_assistant_responses(
                transcript_path, self.last_position, self._seen_message_ids
            )

            print(f"[DEBUG] extract_assistant_responses: responses_len={len(responses)}, new_pos={new_position}, seen_ids={len(self._seen_message_ids)}")

            # 即使没有找到文本响应，也要更新位置（可能已经处理了工具调用）
            self.last_position = new_position
            # 保存当前状态
            if self.last_transcript_path:
                self._file_states[self.last_transcript_path] = {
                    'position': self.last_position,
                    'seen_ids': self._seen_message_ids.copy()
                }

            if not responses:
                return

            self._process_responses(transcript_path, responses, new_position)

        except Exception as e:
            print(f"Error sending response: {e}")
            import traceback
            traceback.print_exc()
            # 保留pending文件以便重试，但避免无限循环，最多保留10分钟
            pending_time = 0
            if os.path.exists(Config.PENDING_FILE):
                try:
                    with open(Config.PENDING_FILE) as f:
                        pending_time = int(f.read().strip())
                except:
                    pass
                if time.time() - pending_time > 600:  # 10 minutes
                    os.remove(Config.PENDING_FILE)
                    print(f"[DEBUG] Pending file removed after 10min timeout")
        finally:
            # 释放锁
            self._checking = False

    def stop(self):
        """Stop the response monitor."""
        self.running = False
        if self.observer:
            try:
                self.observer.stop()
                self.observer.join()
            except Exception as e:
                print(f"[DEBUG] Error stopping observer: {e}")
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        print("Response monitor stopped")

    def _process_responses(self, transcript_path, responses, new_position):
        """Process and send responses to Telegram."""
        if not os.path.exists(Config.CHAT_ID_FILE):
            print(f"[DEBUG] CHAT_ID_FILE not found: {Config.CHAT_ID_FILE}")
            return

        with open(Config.CHAT_ID_FILE) as f:
            chat_id = int(f.read().strip())

        print(f"[DEBUG] Processing responses for chat {chat_id}, raw length={len(responses)}")
        print(f"[DEBUG] Raw responses preview: {responses[:200]}...")

        cleaned_responses, memory_update = extract_memory_update(responses)

        print(f"[DEBUG] Cleaned responses length={len(cleaned_responses)}, memory length={len(memory_update)}")

        # Skip empty responses (e.g., when only XML observations were present)
        if not cleaned_responses or not cleaned_responses.strip():
            print(f"[DEBUG] Skipping empty response for chat {chat_id}")
            # 仅在 legacy 模式下清理 pending；hook 模式由 Stop hook 自行处理
            if not Config.HOOK_DELIVERY_ENABLED and os.path.exists(Config.PENDING_FILE):
                os.remove(Config.PENDING_FILE)
                print(f"[DEBUG] Pending file removed for empty response")
            return

        # 先保存到内存
        self._save_to_memory(chat_id, cleaned_responses, memory_update)

        if Config.HOOK_DELIVERY_ENABLED:
            # Stream intermediate responses to Telegram even in hook mode.
            # This gives the user real-time feedback instead of waiting for
            # the Stop hook to fire at the very end.  The Stop hook still
            # handles final cleanup (pending file deletion) and sends any
            # remaining delta via the sent_offset file.
            result = reply(chat_id, cleaned_responses)
            if result is not False:
                print(f"[DEBUG] Streamed to chat {chat_id} (hook mode, {len(cleaned_responses)} chars)")
                self._update_sent_offset(transcript_path, cleaned_responses)
            else:
                print(f"[DEBUG] Failed to stream, keeping pending for hook")
            # Never delete pending file here — the Stop hook owns cleanup
            return

        # Legacy path: polling 自己发送（仅在 HOOK_DELIVERY_ENABLED=false 时启用）
        result = reply(chat_id, cleaned_responses)
        if result is not False:
            print(f"[DEBUG] Response sent to chat {chat_id}")
            if os.path.exists(Config.PENDING_FILE):
                os.remove(Config.PENDING_FILE)
                print(f"[DEBUG] Pending file removed after sending response")
        else:
            print(f"[DEBUG] Failed to send response, keeping pending file for retry")

    def _save_to_memory(self, chat_id, cleaned_responses, memory_update):
        """Save conversation to memory."""
        if not Config.MEMORY_ENABLED:
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
                recent_messages.pop(chat_id_str, None)
                recent_full_prompts.pop(chat_id_str, None)

            if memory_update:
                memory.add(
                    chat_id_str,
                    memory_update[:5000],
                    metadata={"type": "meta_update", "auto": True},
                    message_type="meta_update"
                )

            # Record failures if lesson extracted or error detected
            self._record_failures_if_any(chat_id_str, cleaned_responses)

        except Exception as e:
            print(f"Error saving to memory: {e}")

    def _record_failures_if_any(self, chat_id_str: str, response: str):
        """记录失败经验（如果响应中包含教训或错误）"""
        try:
            failure_memory = get_failure_memory()

            # 获取用户输入（如果有）
            user_msg = recent_messages.get(chat_id_str)
            if not user_msg:
                return

            # 尝试提取教训
            lesson = failure_memory.extract_lesson_from_response(response)
            if lesson:
                # 记录失败，用户输入作为 action，response 作为 error_message
                failure_memory.record_failure(
                    user_id=chat_id_str,
                    action=user_msg[:100],  # 截取前100字符作为action
                    error_message=response[:500],  # 截取前500字符作为错误信息
                    context=f"用户输入: {user_msg[:200]}",
                    lesson=lesson
                )
                print(f"Recorded failure lesson for user {chat_id_str}")
                return

            # 如果没有明确教训，但检测到错误关键词，也记录
            error_keywords = ["错误", "失败", "bug", "error", "exception", "failed", "invalid", "cannot", "unable"]
            if any(keyword in response.lower() for keyword in error_keywords):
                failure_memory.record_failure(
                    user_id=chat_id_str,
                    action=user_msg[:100],
                    error_message=response[:500],
                    context=f"用户输入: {user_msg[:200]}",
                    lesson="检测到错误关键词，建议手动总结教训"
                )
                print(f"Recorded failure based on error keywords for user {chat_id_str}")

        except Exception as e:
            print(f"Error recording failure: {e}")

    def _update_sent_offset(self, transcript_path, new_chunk):
        """Track cumulative sent chars per transcript for Stop hook dedup."""
        key = str(transcript_path)
        prev = self._cumulative_sent.get(key, 0)
        self._cumulative_sent[key] = prev + len(new_chunk)
        try:
            Config.SENT_OFFSET_FILE.write_text(json.dumps({
                "transcript": key,
                "sent_chars": self._cumulative_sent[key],
                "ts": int(time.time()),
            }))
        except Exception as e:
            print(f"[DEBUG] sent_offset save error: {e}")


response_monitor = ResponseMonitor(check_interval=0.1)  # Faster response check


class OpenccSessionRegistry:
    """One persistent claude-js (OpenCC) process per chat, with streaming TG render."""

    def __init__(self):
        self._sessions: Dict[str, OpenccSession] = {}
        self._renderers: Dict[str, TelegramStreamRenderer] = {}
        self._lock = threading.Lock()

    def get_or_create(self, chat_id: int) -> tuple[OpenccSession, TelegramStreamRenderer]:
        key = str(chat_id)
        with self._lock:
            sess = self._sessions.get(key)
            rend = self._renderers.get(key)
            if sess and sess.is_running and rend is not None:
                return sess, rend

            # New renderer for each session (fresh state).
            rend = TelegramStreamRenderer(chat_id, telegram_api=TelegramAPI.call)

            sess = OpenccSession(
                on_event=rend.on_event,
                on_stderr=lambda l: print(f"[opencc:{key}] {l}"),
                on_close=lambda c: print(f"[opencc:{key}] process closed code={c}"),
                cli_path=Path(Config.OPENCC_CLI_PATH),
                bun_path=Config.OPENCC_BUN_PATH,
                cwd=Config.OPENCC_CWD,
                model=(Config.OPENCC_MODEL or None),
            )
            self._sessions[key] = sess
            self._renderers[key] = rend
            return sess, rend

    def new_turn(self, chat_id: int) -> tuple[OpenccSession, TelegramStreamRenderer]:
        """Reset the renderer (start a fresh edit-target message) but keep
        the underlying process alive so conversation state persists."""
        key = str(chat_id)
        with self._lock:
            sess = self._sessions.get(key)
            if sess is None or not sess.is_running:
                # Force a full create.
                pass
            # Tear down the previous renderer's worker thread before
            # replacing it, so we don't leak threads on turns where the
            # prior `result` event never arrived (e.g. user interrupted).
            prev = self._renderers.get(key)
            if prev is not None:
                try:
                    prev.close()
                except Exception:
                    pass
            rend = TelegramStreamRenderer(chat_id, telegram_api=TelegramAPI.call)
            self._renderers[key] = rend
            if sess is None or not sess.is_running:
                sess = OpenccSession(
                    on_event=rend.on_event,
                    on_stderr=lambda l: print(f"[opencc:{key}] {l}"),
                    on_close=lambda c: print(f"[opencc:{key}] process closed code={c}"),
                    cli_path=Path(Config.OPENCC_CLI_PATH),
                    bun_path=Config.OPENCC_BUN_PATH,
                    cwd=Config.OPENCC_CWD,
                    model=(Config.OPENCC_MODEL or None),
                )
                self._sessions[key] = sess
            else:
                # Rebind on_event to the new renderer.
                sess.on_event = rend.on_event
            return sess, rend

    def interrupt(self, chat_id: int) -> bool:
        key = str(chat_id)
        with self._lock:
            sess = self._sessions.get(key)
        if sess and sess.is_running:
            sess.send_interrupt()
            return True
        return False

    def close(self, chat_id: int) -> None:
        key = str(chat_id)
        with self._lock:
            sess = self._sessions.pop(key, None)
            rend = self._renderers.pop(key, None)
        if rend:
            try:
                rend.close()
            except Exception:
                pass
        if sess:
            sess.close()

    def close_all(self) -> None:
        with self._lock:
            keys = list(self._sessions.keys())
        for k in keys:
            self.close(int(k) if k.lstrip("-").isdigit() else k)


opencc_registry = OpenccSessionRegistry()


class MessageQueue:
    """Ensure messages are processed in order."""

    def __init__(self):
        self.queue = queue.Queue()
        self.processing = False
        self.lock = threading.Lock()

    def add_message(self, chat_id, text, full_prompt):
        """Add a message to the queue."""
        with self.lock:
            self.queue.put((chat_id, text, full_prompt))
            if not self.processing:
                self.processing = True
                threading.Thread(target=self._process_queue, daemon=True).start()

    def _process_queue(self):
        """Process messages in the queue."""
        while True:
            try:
                # 等待新消息，超时1秒
                chat_id, text, full_prompt = self.queue.get(timeout=1)

                # 检查是否有更新的消息在等待
                while not self.queue.empty():
                    try:
                        # 尝试获取更新的消息（非阻塞）
                        chat_id, text, full_prompt = self.queue.get_nowait()
                    except queue.Empty:
                        break

                # 处理最新的消息
                self._handle_message(chat_id, text, full_prompt)

            except queue.Empty:
                # 队列为空，退出处理循环
                with self.lock:
                    self.processing = False
                break
            except Exception as e:
                print(f"Error processing message queue: {e}")

    def _handle_message(self, chat_id, text, full_prompt):
        """Handle a single message."""
        try:
            # 存储消息用于跟踪和记忆
            recent_messages[str(chat_id)] = text
            recent_full_prompts[str(chat_id)] = full_prompt

            # OpenCC spawn 路径：直接 stream-json，不走 tmux/transcript/hook
            if Config.OPENCC_SPAWN_MODE:
                sess, rend = opencc_registry.new_turn(chat_id)
                threading.Thread(
                    target=send_typing_loop_until,
                    args=(chat_id, lambda: rend._closed),
                    daemon=True,
                ).start()
                sess.send(full_prompt)
                print(f"[DEBUG] Routed chat={chat_id} via opencc spawn (model={Config.OPENCC_MODEL or 'default'})")
                return

            # 确保目录存在
            Config.PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)

            # 创建pending文件
            with open(Config.PENDING_FILE, "w") as f:
                f.write(str(int(time.time())))

            print(f"[DEBUG] Message queued and processing started for chat_id={chat_id}")

            # 检查tmux是否存在
            if not tmux_exists():
                reply(chat_id, "tmux not found")
                if os.path.exists(Config.PENDING_FILE):
                    os.remove(Config.PENDING_FILE)
                return

            # 启动输入指示器
            threading.Thread(target=send_typing_loop, args=(chat_id,), daemon=True).start()

            # 发送到tmux
            tmux_send(full_prompt)
            tmux_send_enter()

            print(f"[DEBUG] Message sent to tmux, response_monitor will handle the response asynchronously")

        except Exception as e:
            print(f"Error handling queued message: {e}")
            if os.path.exists(Config.PENDING_FILE):
                os.remove(Config.PENDING_FILE)


message_queue = MessageQueue()


class BotHandler:
    """Handle Telegram bot updates."""

    def __init__(self):
        self.offset = self._load_offset()
        self._session_initialized = False
        self._attention_manager = AttentionManager()
        self._prompt_builder = StablePromptBuilder(self._attention_manager)

    def _load_offset(self):
        """Load update offset from file."""
        if os.path.exists(Config.UPDATE_OFFSET_FILE):
            try:
                with open(Config.UPDATE_OFFSET_FILE) as f:
                    return int(f.read().strip())
            except:
                pass
        return 0

    def _save_offset(self, offset):
        """Save update offset to file."""
        with open(Config.UPDATE_OFFSET_FILE, "w") as f:
            f.write(str(offset))

    def _require_tmux(self, chat_id):
        """Check if tmux exists, reply with error if not."""
        if not tmux_exists():
            reply(chat_id, "tmux not found")
            return False
        return True

    def _start_typing(self, chat_id):
        """Start typing indicator."""
        with open(Config.PENDING_FILE, "w") as f:
            f.write(str(int(time.time())))
        threading.Thread(target=send_typing_loop, args=(chat_id,), daemon=True).start()

    def _get_or_init_auto_memory_instruction(self) -> str:
        """Get auto-memory instruction from DB, initialize if not exists."""
        if not Config.MEMORY_ENABLED:
            return Config.DEFAULT_AUTO_MEMORY_INSTRUCTION

        try:
            memory = get_memory()
            results = memory.get_by_type("system", "meta_instruction", limit=1)
            if results:
                return results[0]["content"]

            memory.add(
                "system",
                Config.DEFAULT_AUTO_MEMORY_INSTRUCTION,
                metadata={"type": "self_referential", "auto": False},
                message_type="meta_instruction"
            )
            return Config.DEFAULT_AUTO_MEMORY_INSTRUCTION
        except Exception as e:
            print(f"Error loading meta-instruction: {e}")
            return Config.DEFAULT_AUTO_MEMORY_INSTRUCTION

    def _build_full_prompt(self, text, chat_id, is_new_session=False):
        """Build full prompt with AttentionManager for KV-Cache optimization.

        Implements Manus-style attention redirection:
        - Static prefix (cacheable)
        - Retrieved memories + working memory
        - User input
        - Task state at the END (recency bias for goal focus)
        """
        # Prepare memories
        memories = None
        if Config.MEMORY_ENABLED:
            try:
                memory = get_memory()
                memories = memory.search(str(chat_id), text, limit=Config.MEMORY_MAX_RESULTS)
            except Exception as e:
                print(f"Memory search error: {e}")

        # Get meta prompt for new sessions
        claude_md_content = None
        include_meta = is_new_session or not self._session_initialized
        if include_meta:
            claude_md_content = load_claude_md()
            self._session_initialized = True

        # Build optimized prompt using AttentionManager
        if Config.KV_CACHE_ENABLED:
            # Use KV-Cache enabled prompt builder
            full_prompt, cache_info = self._attention_manager.build_optimized_prompt_with_cache(
                user_input=text,
                chat_id=str(chat_id),
                memories=memories,
                include_meta_prompt=include_meta,
                claude_md_content=claude_md_content,
                ttl_seconds=Config.KV_CACHE_TTL,
            )
            # Optionally log cache info for debugging
            if cache_info.get("cache_hit"):
                print(f"[KV-Cache] Hit for chat {chat_id}, key: {cache_info.get('cache_key', 'unknown')}")
        else:
            # Original method (backward compatibility)
            full_prompt = self._attention_manager.build_optimized_prompt(
                user_input=text,
                chat_id=str(chat_id),
                memories=memories,
                include_meta_prompt=include_meta,
                claude_md_content=claude_md_content,
            )

        return full_prompt

    def _wait_for_claude_response(self, timeout=30):
        """Wait for Claude to generate a response with timeout."""
        start_time = time.time()
        check_count = 0

        while time.time() - start_time < timeout:
            # 检查是否已经有响应文件生成
            transcript_path = find_latest_transcript()
            if transcript_path and transcript_path.exists():
                # 检查文件中是否有新的assistant响应（使用增量检查）
                responses, _, _ = extract_assistant_responses(transcript_path, response_monitor.last_position, response_monitor._seen_message_ids)
                if responses and responses.strip():
                    print(f"[DEBUG] Found Claude response after {check_count} checks")
                    return True

            check_count += 1
            time.sleep(0.1)  # 短间隔快速检查

        print(f"[DEBUG] Timeout waiting for Claude response after {timeout}s")
        return False

    def handle_message(self, msg):
        """Process incoming message from Telegram."""
        # Handle different message types
        text = msg.get("text", "")
        chat_id = msg.get("chat", {}).get("id")
        msg_id = msg.get("message_id")

        print(f"[DEBUG] Received message: chat_id={chat_id}, text='{text[:50]}...', msg_id={msg_id}")

        if not chat_id:
            return

        # Handle non-text messages (documents, photos, etc.)
        if not text:
            # Check for document
            if msg.get("document"):
                file_info = msg.get("document", {})
                file_name = file_info.get("file_name", "unknown")
                file_size = file_info.get("file_size", 0)
                text = f"[Document: {file_name} ({file_size} bytes)]"
            # Check for photo (take the largest size)
            elif msg.get("photo"):
                photos = msg.get("photo", [])
                if photos:
                    largest_photo = photos[-1]  # Telegram sends multiple sizes, last is largest
                    file_size = largest_photo.get("file_size", 0)
                    text = f"[Photo: {file_size} bytes]"
            # Check for video
            elif msg.get("video"):
                video_info = msg.get("video", {})
                duration = video_info.get("duration", 0)
                file_size = video_info.get("file_size", 0)
                text = f"[Video: {duration}s, {file_size} bytes]"
            # Check for audio/voice
            elif msg.get("audio"):
                audio_info = msg.get("audio", {})
                duration = audio_info.get("duration", 0)
                text = f"[Audio: {duration}s]"
            elif msg.get("voice"):
                voice_info = msg.get("voice", {})
                duration = voice_info.get("duration", 0)
                text = f"[Voice: {duration}s]"
            # Check for other media types
            elif msg.get("sticker"):
                text = "[Sticker]"
            elif msg.get("location"):
                loc = msg.get("location", {})
                lat, lon = loc.get("latitude"), loc.get("longitude")
                text = f"[Location: {lat}, {lon}]"
            elif msg.get("contact"):
                contact = msg.get("contact", {})
                name = contact.get("first_name", "") + " " + contact.get("last_name", "")
                text = f"[Contact: {name.strip()}]"
            else:
                # Unknown message type, skip processing
                print(f"[DEBUG] Unknown message type, skipping: {msg.keys()}")
                return

        # Add caption if present (for media messages)
        caption = msg.get("caption", "")
        if caption:
            text = f"{text}\n\nCaption: {caption}"

        with open(Config.CHAT_ID_FILE, "w") as f:
            f.write(str(chat_id))

        if text.startswith("/"):
            return self._handle_command(text, chat_id)

        print(f"[{chat_id}] {text[:50]}...")

        # Send raw message if TELEGRAM_RAW_MESSAGES is enabled
        if Config.TELEGRAM_RAW_MESSAGES:
            # Send just the user's raw input without any wrappers
            full_prompt = text
        else:
            # Use attention manager with all the wrappers
            full_prompt = self._build_full_prompt(text, chat_id)

        # Store message ID for reaction
        if msg_id:
            telegram_api("setMessageReaction", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "reaction": [{"type": "emoji", "emoji": "✅"}]
            })

        # 使用消息队列确保顺序处理
        message_queue.add_message(chat_id, text, full_prompt)

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
            "/task": self._cmd_task,
            "/todo": self._cmd_todo,
            "/failures": self._cmd_failures,
            "/lessons": self._cmd_lessons,
            "/kvcache": self._cmd_kvcache,
        }

        if cmd in handlers:
            handlers[cmd](chat_id, args)
        elif cmd in Config.BLOCKED_COMMANDS:
            reply(chat_id, f"'{cmd}' not supported (interactive)")

    def _cmd_status(self, chat_id, _):
        status = "running" if tmux_exists() else "not found"
        reply(chat_id, f"tmux '{Config.TMUX_SESSION}': {status}")

    def _cmd_stop(self, chat_id, _):
        """Stop/interrupt Claude and send any partial response."""
        if Config.OPENCC_SPAWN_MODE:
            interrupted = opencc_registry.interrupt(chat_id)
            reply(chat_id, "Interrupted (opencc)" if interrupted else "No active session")
            return

        # First, check if there's already a response generated
        # and send it before interrupting
        if os.path.exists(Config.PENDING_FILE):
            try:
                transcript_path = find_latest_transcript()
                if transcript_path:
                    responses, new_position, _ = extract_assistant_responses(
                        transcript_path, response_monitor.last_position, response_monitor._seen_message_ids
                    )
                    if responses and responses.strip():
                        cleaned_responses, _ = extract_memory_update(responses)
                        if cleaned_responses and cleaned_responses.strip():
                            reply(chat_id, cleaned_responses)
                            response_monitor.last_position = new_position
                            print(f"[DEBUG] Sent partial response before stop")
            except Exception as e:
                print(f"[DEBUG] Error checking for partial response: {e}")

        # Now send escape to interrupt Claude
        if tmux_exists():
            tmux_send_escape()

        # Clean up pending file
        if os.path.exists(Config.PENDING_FILE):
            os.remove(Config.PENDING_FILE)

        reply(chat_id, "Interrupted")

    def _cmd_clear(self, chat_id, _):
        if Config.OPENCC_SPAWN_MODE:
            # Close the persistent process; next message will start a fresh
            # session (no --resume).
            opencc_registry.close(chat_id)
            self._session_initialized = False
            reply(chat_id, "Cleared (opencc session reset)")
            return

        if not self._require_tmux(chat_id):
            return
        self._session_initialized = False
        tmux_send_escape()
        time.sleep(0.2)
        tmux_send("/clear")
        tmux_send_enter()
        reply(chat_id, "Cleared")

    def _start_claude_with_command(self, chat_id, command, message):
        """Start Claude with a specific command."""
        if not self._require_tmux(chat_id):
            return False

        self._session_initialized = False
        tmux_send_escape()
        time.sleep(0.2)
        tmux_send("/exit")
        tmux_send_enter()
        time.sleep(0.5)
        tmux_send(command)
        tmux_send_enter()
        reply(chat_id, message)
        return True

    def _cmd_continue(self, chat_id, _):
        """Continue most recent session."""
        self._start_claude_with_command(
            chat_id,
            "claude --continue --dangerously-skip-permissions",
            "Continuing..."
        )

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

    def _cmd_task(self, chat_id, args):
        """Create or manage tasks with todo.md tracking."""
        if args:
            # Create new task
            task_id = self._attention_manager.create_task(str(chat_id), args)
            reply(chat_id,
                f"🎯 Task created!\n"
                f"Goal: {args}\n"
                f"Task ID: {task_id}\n\n"
                f"The task goal will be appended to every prompt.\n"
                f"Use /todo to view or update progress.")
        else:
            # Show current task
            tasks = self._attention_manager._external.list_tasks(str(chat_id))
            if not tasks:
                reply(chat_id, "No active tasks. Create one with /task \u003cgoal\u003e")
                return

            lines = ["🎯 Active Tasks:", ""]
            for t in tasks[:5]:
                task_name = t['task_id'].replace('_todo.md', '').replace('_', ' ')
                lines.append(f"• {task_name}")

            current = self._attention_manager.get_task_id(str(chat_id))
            lines.append(f"\nCurrent: {current}")
            reply(chat_id, "\n".join(lines))

    def _cmd_todo(self, chat_id, args):
        """View or update todo.md for current task."""
        if args:
            # Update todo.md
            task_id = self._attention_manager.get_task_id(str(chat_id))
            if self._attention_manager._external.update_todo_md(
                str(chat_id), args, task_id, append=True
            ):
                reply(chat_id, "✅ Todo updated")
            else:
                reply(chat_id, "❌ Failed to update")
        else:
            # Show current todo
            task_id = self._attention_manager.get_task_id(str(chat_id))
            todo = self._attention_manager._external.get_todo_md(str(chat_id), task_id)

            if not todo or todo.startswith("# 当前任务目标"):
                reply(chat_id, "No active todo. Create a task first with /task \u003cgoal\u003e")
                return

            # Truncate if too long
            if len(todo) > 3000:
                todo = todo[:3000] + "\n\n... (truncated)"

            reply(chat_id, f"📝 Current Todo ({task_id}):\n\n{todo}")

    def _cmd_failures(self, chat_id, args):
        """View failure lessons or mark as resolved"""
        try:
            fm = get_failure_memory()
            chat_id_str = str(chat_id)

            if not args:
                # Show failure stats and recent unresolved failures
                stats = fm.get_stats(chat_id_str)
                failures = fm.get_user_failures(chat_id_str, resolved_only=False, limit=5)

                lines = [
                    "📊 失败经验统计",
                    f"总计: {stats['total_unique']} 个独立失败",
                    f"已解决: {stats['resolved']}，未解决: {stats['unresolved']}",
                    f"总发生次数: {stats['total_occurrences']}",
                    f"平均重复: {stats['avg_recurrence']:.1f} 次/失败",
                    "",
                    "📝 最近的未解决失败:",
                ]

                if failures:
                    for i, f in enumerate(failures, 1):
                        lines.append(f"{i}. {f.action[:50]}")
                        lines.append(f"   错误: {f.error_message[:80]}")
                        if f.recurrence_count > 1:
                            lines.append(f"   重复: {f.recurrence_count} 次")
                        lines.append(f"   ID: {f.failure_id[:8]}")
                        lines.append("")
                else:
                    lines.append("暂无未解决失败")

                lines.append("\n使用 /failures stats 查看详细统计")
                lines.append("使用 /failures resolve <ID> 标记为已解决")
                reply(chat_id, "\n".join(lines))
                return

            args_lower = args.lower().strip()
            if args_lower == "stats":
                stats = fm.get_stats(chat_id_str)
                lines = ["📊 失败经验详细统计", ""]
                for key, value in stats.items():
                    if key == "by_type":
                        lines.append("按错误类型分类:")
                        for err_type, count in value.items():
                            lines.append(f"  {err_type}: {count}")
                    else:
                        lines.append(f"{key}: {value}")
                reply(chat_id, "\n".join(lines))
                return

            if args_lower.startswith("resolve "):
                failure_id = args_lower[8:].strip()
                if fm.mark_resolved(chat_id_str, failure_id):
                    reply(chat_id, f"✅ 失败记录 {failure_id[:8]} 标记为已解决")
                else:
                    reply(chat_id, f"❌ 未找到失败记录 {failure_id[:8]}")
                return

            # If query provided, search failures
            failures = fm.get_user_failures(chat_id_str, resolved_only=False, limit=20)
            filtered = [f for f in failures if args.lower() in f.action.lower() or args.lower() in f.error_message.lower()]
            if not filtered:
                reply(chat_id, f"未找到包含 '{args}' 的失败记录")
                return

            lines = [f"🔍 找到 {len(filtered)} 个相关失败:", ""]
            for i, f in enumerate(filtered[:5], 1):
                lines.append(f"{i}. {f.action[:60]}")
                lines.append(f"   错误: {f.error_message[:80]}")
                if f.lesson and f.lesson != "待总结":
                    lines.append(f"   教训: {f.lesson[:80]}")
                lines.append(f"   ID: {f.failure_id[:8]}")
                lines.append("")
            if len(filtered) > 5:
                lines.append(f"... 还有 {len(filtered)-5} 个未显示")
            reply(chat_id, "\n".join(lines))

        except Exception as e:
            print(f"Error handling /failures: {e}")
            reply(chat_id, f"❌ 处理失败记录时出错: {e}")

    def _cmd_lessons(self, chat_id, args):
        """View learned lessons from failures"""
        try:
            fm = get_failure_memory()
            chat_id_str = str(chat_id)

            failures = fm.get_user_failures(chat_id_str, resolved_only=False, limit=50)
            # Filter failures with meaningful lessons
            lessons = [f for f in failures if f.lesson and f.lesson != "待总结"]

            if args:
                query = args.lower()
                lessons = [f for f in lessons if query in f.lesson.lower() or query in f.action.lower()]

            if not lessons:
                reply(chat_id, f"📭 暂无已总结的教训{f' (查询: {args})' if args else ''}")
                return

            lines = [f"📚 学到的教训 ({len(lessons)} 个):", ""]
            for i, f in enumerate(lessons[:10], 1):
                lines.append(f"{i}. 【{f.action[:50]}】")
                lines.append(f"   教训: {f.lesson[:100]}")
                if f.recurrence_count > 1:
                    lines.append(f"   (重复 {f.recurrence_count} 次)")
                lines.append("")

            if len(lessons) > 10:
                lines.append(f"... 还有 {len(lessons)-10} 个未显示")
            reply(chat_id, "\n".join(lines))

        except Exception as e:
            print(f"Error handling /lessons: {e}")
            reply(chat_id, f"❌ 处理教训记录时出错: {e}")

    def _cmd_kvcache(self, chat_id, args):
        """Display KV-Cache statistics or clear cache"""
        try:
            stats = self._attention_manager.get_cache_stats()

            if args.strip().lower() == "clear":
                # Clear cache
                cleared = self._attention_manager._kv_cache.clear_cache()
                reply(chat_id, f"🗑️ 已清除 {cleared} 个缓存条目")
                return

            # Display statistics
            lines = [
                "🔧 KV-Cache 统计信息",
                f"命中率: {stats['hit_rate']:.1%}",
                f"总查询: {stats['total_queries']}",
                f"命中: {stats['hit_count']}",
                f"未命中: {stats['miss_count']}",
                f"缓存条目: {stats['cache_size']}",
                f"缓存目录: {stats['cache_dir']}",
                "",
                "使用 /kvcache clear 清除缓存"
            ]

            reply(chat_id, "\n".join(lines))

        except Exception as e:
            print(f"Error handling /kvcache: {e}")
            reply(chat_id, f"❌ 处理KV-Cache统计时出错: {e}")

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
                session_id = data.split(":", 1)[1]
                self._start_claude_with_command(
                    chat_id,
                    f"claude --resume {session_id} --dangerously-skip-permissions",
                    f"Resuming: {session_id[:8]}..."
                )
            elif data == "continue_recent":
                self._start_claude_with_command(
                    chat_id,
                    "claude --continue --dangerously-skip-permissions",
                    "Continuing most recent..."
                )
        except Exception as e:
            print(f"Error handling callback: {e}")
            reply(chat_id, f"Error: {str(e)}")

    def poll_updates(self):
        """Main polling loop."""
        setup_bot_commands()
        print(f"MateCode Bridge started | tmux: {Config.TMUX_SESSION}")
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
    if not Config.BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set")
        return 1

    handler = BotHandler()
    handler.poll_updates()
    return 0


if __name__ == "__main__":
    exit(main())
