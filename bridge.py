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

    # Memory settings
    MEMORY_ENABLED = os.environ.get("MEMORY_ENABLED", "true").lower() == "true"
    MEMORY_MAX_RESULTS = int(os.environ.get("MEMORY_MAX_RESULTS", "5"))
    MEMORY_MAX_CONTEXT = int(os.environ.get("MEMORY_MAX_CONTEXT", "2000"))

    # KV-Cache settings
    KV_CACHE_ENABLED = os.environ.get("KV_CACHE_ENABLED", "true").lower() == "true"
    KV_CACHE_TTL = int(os.environ.get("KV_CACHE_TTL", "3600"))  # 1 hour default

    # Telegram settings - disable attention manager for raw messages
    TELEGRAM_RAW_MESSAGES = os.environ.get("TELEGRAM_RAW_MESSAGES", "true").lower() == "true"

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

def reply(chat_id: int, text: str) -> None:
    """Send a text message to a chat."""
    TelegramAPI.reply(chat_id, text)

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
    def reply(chat_id: int, text: str) -> None:
        """Send a text message to a chat."""
        TelegramAPI.call("sendMessage", {"chat_id": chat_id, "text": text})


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


def extract_assistant_responses(transcript_path, last_response_pos=0):
    """Extract assistant responses from transcript starting from a position."""
    if not transcript_path or not transcript_path.exists():
        return "", 0

    responses = []
    seen_message_ids = set()  # Track processed message IDs to avoid duplicates
    current_pos = 0
    found_new_content = False

    try:
        with open(transcript_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            current_pos += len(line)
            if current_pos <= last_response_pos:
                continue

            try:
                entry = json.loads(line.strip())
                if entry.get("type") == "assistant":
                    message = entry.get("message", {})
                    msg_id = message.get("id")

                    # Skip if we've already processed this message ID
                    if msg_id and msg_id in seen_message_ids:
                        continue

                    # Extract text blocks (including those after tool_use)
                    text_content = []
                    has_tool_use = False

                    # First pass: check if there's any tool_use
                    for block in message.get("content", []):
                        if block.get("type") == "tool_use":
                            has_tool_use = True
                            break

                    # Extract text content
                    for block in message.get("content", []):
                        if block.get("type") == "text":
                            text = block.get("text", "").strip()
                            # Skip XML observation blocks and empty text
                            if not text:
                                continue
                            # Skip pure XML blocks
                            if text.startswith("<") and ">" in text:
                                continue
                            # Skip markdown code blocks containing XML/observation
                            if text.startswith("```") and ("</" in text or "observation" in text.lower()):
                                continue
                            text_content.append(text)

                    # Only include responses that have actual text content
                    # This helps avoid empty tool_use-only messages
                    if text_content:
                        if msg_id:
                            seen_message_ids.add(msg_id)
                        responses.append("\n".join(text_content))
                        found_new_content = True

            except (json.JSONDecodeError, KeyError):
                # Skip malformed lines
                continue

    except Exception as e:
        print(f"Error reading transcript: {e}")
        return "", last_response_pos

    # 如果没有找到新内容，保持原位置不变
    if not found_new_content:
        return "", last_response_pos

    return "\n\n".join(responses).strip(), current_pos


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

        try:
            event_handler = PendingFileHandler(self._immediate_response_check)
            self.observer = watchdog.observers.Observer()
            self.observer.schedule(event_handler, str(Config.PENDING_FILE.parent), recursive=False)
            self.observer.start()
            print(f"[DEBUG] File watcher started watching {Config.PENDING_FILE.parent}")
        except Exception as e:
            print(f"[WARN] Could not start file watcher: {e}")

    def _start_file_watcher(self):
        """Start watching for pending file creation using polling."""
        def file_watcher():
            last_check = 0
            while self.running:
                try:
                    current_time = time.time()
                    if current_time - last_check >= 0.1:  # Check every 100ms
                        if os.path.exists(Config.PENDING_FILE):
                            mtime = os.path.getmtime(Config.PENDING_FILE)
                            if mtime > last_check:
                                print(f"[DEBUG] File watcher detected pending file update")
                                self._immediate_response_check()
                                last_check = current_time
                    time.sleep(0.05)
                except Exception as e:
                    print(f"[DEBUG] File watcher error: {e}")
                    time.sleep(0.1)

        watcher_thread = threading.Thread(target=file_watcher, daemon=True)
        watcher_thread.start()
        print(f"[DEBUG] File watcher started polling for {Config.PENDING_FILE}")

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
        if not pending_exists:
            self.last_transcript_path = None
            self.last_position = 0
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

            # 正确处理文件切换：当切换到新文件时重置位置
            if self.last_transcript_path != transcript_path:
                self.last_transcript_path = transcript_path
                self.last_position = 0

            # 使用增量读取，从上次位置开始读取新内容
            responses, new_position = extract_assistant_responses(transcript_path, self.last_position)

            if not responses:
                return

            # 更新读取位置
            self.last_position = new_position

            if not os.path.exists(Config.CHAT_ID_FILE):
                return

            with open(Config.CHAT_ID_FILE) as f:
                chat_id = int(f.read().strip())

            cleaned_responses, memory_update = extract_memory_update(responses)

            # Skip empty responses (e.g., when only XML observations were present)
            if not cleaned_responses or not cleaned_responses.strip():
                print(f"Skipping empty response for chat {chat_id}")
                # 空响应也清理pending文件，避免卡住
                if os.path.exists(Config.PENDING_FILE):
                    os.remove(Config.PENDING_FILE)
                    print(f"[DEBUG] Pending file removed for empty response")
                return

            # 先保存到内存，再发送消息
            self._save_to_memory(chat_id, cleaned_responses, memory_update)

            # 发送消息到Telegram
            reply(chat_id, cleaned_responses)
            print(f"[DEBUG] Response sent to chat {chat_id}")

            # 只有在成功发送响应后才移除pending文件
            if os.path.exists(Config.PENDING_FILE):
                os.remove(Config.PENDING_FILE)
                print(f"[DEBUG] Pending file removed after sending response")

        except Exception as e:
            print(f"Error sending response: {e}")
            # 发生错误时也清理pending文件，避免无限等待
            if os.path.exists(Config.PENDING_FILE):
                os.remove(Config.PENDING_FILE)
                print(f"[DEBUG] Pending file removed due to error")
        finally:
            # 释放锁
            self._checking = False

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


response_monitor = ResponseMonitor(check_interval=0.1)  # Faster response check


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

            # 等待Claude生成响应
            print(f"[DEBUG] Waiting for Claude response...")
            # 等待响应生成
            start_time = time.time()
            timeout = 30
            check_count = 0

            while time.time() - start_time < timeout:
                transcript_path = find_latest_transcript()
                if transcript_path and transcript_path.exists():
                    responses, _ = extract_assistant_responses(transcript_path, response_monitor.last_position)
                    if responses and responses.strip():
                        print(f"[DEBUG] Found Claude response after {check_count} checks")
                        # 触发响应检查
                        response_monitor._check_for_responses()
                        return

                check_count += 1
                time.sleep(0.1)

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
                responses, _ = extract_assistant_responses(transcript_path, response_monitor.last_position)
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
        if tmux_exists():
            tmux_send_escape()
        if os.path.exists(Config.PENDING_FILE):
            os.remove(Config.PENDING_FILE)
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
