"""OpenCC (claude-js) spawn backend for MateBot.

Replaces the tmux + transcript-polling architecture for a single chat with a
persistent claude-js subprocess that emits stream-json events. This eliminates
the timing race between bridge.py's ResponseMonitor and the Stop hook, and
enables true streaming intermediate feedback.

Inspired by a5c-ai/claude-code-telegram-bot's ClaudeCodeProcess.ts.
"""

from __future__ import annotations

import json
import os
import queue
import subprocess
import threading
import time
from pathlib import Path
from typing import Callable, Optional


DEFAULT_CLI_PATH = Path(__file__).parent / "vendor" / "opencc" / "cli.js"


class OpenccSession:
    """One persistent claude-js subprocess per logical conversation.

    Reads stream-json from stdout, writes stream-json to stdin. Each parsed
    stdout JSON line is dispatched to `on_event(event_dict)`. Stderr is
    captured into `on_stderr(line)` for debugging.

    The process is spawned lazily on first `send()`. If `session_id` is
    provided, the process resumes the existing session.
    """

    def __init__(
        self,
        on_event: Callable[[dict], None],
        on_stderr: Optional[Callable[[str], None]] = None,
        on_close: Optional[Callable[[Optional[int]], None]] = None,
        cli_path: Optional[Path] = None,
        bun_path: str = "bun",
        cwd: Optional[str] = None,
        session_id: Optional[str] = None,
        model: Optional[str] = None,
        extra_args: Optional[list[str]] = None,
    ):
        self.on_event = on_event
        self.on_stderr = on_stderr or (lambda _l: None)
        self.on_close = on_close or (lambda _c: None)
        self.cli_path = Path(cli_path) if cli_path else DEFAULT_CLI_PATH
        self.bun_path = bun_path
        self.cwd = cwd or os.getcwd()
        self.session_id = session_id
        self.model = model
        self.extra_args = list(extra_args or [])

        self._proc: Optional[subprocess.Popen] = None
        self._stdout_thread: Optional[threading.Thread] = None
        self._stderr_thread: Optional[threading.Thread] = None
        self._spawn_lock = threading.Lock()
        self._stdin_lock = threading.Lock()
        self._spawned = False
        self._closing = False
        # Messages queued before process is fully spawned
        self._pending: queue.Queue[str] = queue.Queue()

    # -- public API -------------------------------------------------------

    @property
    def is_running(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    def send(self, text: str) -> None:
        """Send a user prompt to the persistent process."""
        if not self._spawned:
            self._spawn()
        msg = {
            "type": "user",
            "message": {
                "role": "user",
                "content": [{"type": "text", "text": text}],
            },
        }
        line = json.dumps(msg, ensure_ascii=False) + "\n"
        if not self.is_running:
            # Process hasn't fully come up yet; queue the message.
            self._pending.put(line)
            return
        self._write_stdin(line)

    def send_interrupt(self) -> None:
        """Send SIGINT to ask claude-js to stop generation gracefully."""
        if self.is_running and self._proc:
            try:
                self._proc.send_signal(2)  # SIGINT
            except Exception:
                pass

    def close(self) -> None:
        """Terminate the process and join reader threads."""
        self._closing = True
        if self._proc and self.is_running:
            try:
                self._proc.stdin and self._proc.stdin.close()
            except Exception:
                pass
            try:
                self._proc.terminate()
                self._proc.wait(timeout=3)
            except Exception:
                try:
                    self._proc.kill()
                except Exception:
                    pass
        for t in (self._stdout_thread, self._stderr_thread):
            if t and t.is_alive():
                t.join(timeout=1)

    # -- internals --------------------------------------------------------

    def _spawn(self) -> None:
        with self._spawn_lock:
            if self._spawned:
                return
            args = [
                self.bun_path,
                str(self.cli_path),
                "--print",
                "--verbose",
                "--input-format", "stream-json",
                "--output-format", "stream-json",
                "--include-partial-messages",
                "--include-hook-events",
                "--dangerously-skip-permissions",
            ]
            if self.model:
                args += ["--model", self.model]
            if self.session_id:
                args += ["--resume", self.session_id]
            args += self.extra_args

            env = os.environ.copy()
            # claude-js inherits its own state envs; strip parent's to avoid
            # accidentally resuming a different session.
            for v in ("CLAUDE_SESSION_ID", "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT"):
                env.pop(v, None)
            env["FORCE_COLOR"] = "0"

            self._proc = subprocess.Popen(
                args,
                cwd=self.cwd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                bufsize=0,
            )
            self._spawned = True

            self._stdout_thread = threading.Thread(
                target=self._read_stdout, daemon=True
            )
            self._stderr_thread = threading.Thread(
                target=self._read_stderr, daemon=True
            )
            self._stdout_thread.start()
            self._stderr_thread.start()

            # Drain pending messages now that stdin is open.
            threading.Thread(target=self._drain_pending, daemon=True).start()

    def _drain_pending(self) -> None:
        # Tiny grace period for the process to settle (mirrors the reference repo).
        time.sleep(0.1)
        while not self._pending.empty():
            try:
                line = self._pending.get_nowait()
            except queue.Empty:
                break
            self._write_stdin(line)

    def _write_stdin(self, line: str) -> None:
        if not self._proc or not self._proc.stdin:
            return
        with self._stdin_lock:
            try:
                self._proc.stdin.write(line.encode("utf-8"))
                self._proc.stdin.flush()
            except (BrokenPipeError, ValueError) as e:
                self.on_stderr(f"[opencc] stdin write failed: {e}")

    def _read_stdout(self) -> None:
        assert self._proc and self._proc.stdout
        try:
            for raw in iter(self._proc.stdout.readline, b""):
                line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    self.on_stderr(f"[opencc] non-JSON stdout: {line[:200]}")
                    continue
                # Auto-capture session_id from init / assistant frames so we
                # can resume next time.
                sid = event.get("session_id")
                if sid and not self.session_id:
                    self.session_id = sid
                try:
                    self.on_event(event)
                except Exception as e:
                    self.on_stderr(f"[opencc] on_event handler error: {e}")
        finally:
            code = self._proc.poll() if self._proc else None
            try:
                self.on_close(code)
            except Exception:
                pass

    def _read_stderr(self) -> None:
        assert self._proc and self._proc.stderr
        for raw in iter(self._proc.stderr.readline, b""):
            line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
            if line.strip():
                self.on_stderr(line)


# ----------------------------------------------------------------------------
# Stream → Telegram bridge


class TelegramStreamRenderer:
    """Accumulates stream-json events into a per-turn TG message that is
    edit-updated in place. Avoids hammering Telegram's edit API by throttling
    updates and chunking when content exceeds the 4096 char limit.

    A "turn" begins on the first content of a new user message and ends on
    the `result` event. Multiple chunks may be sent as separate messages when
    content overflows; only the *last* chunk is the live editable draft.
    """

    EDIT_THROTTLE_S = 0.4   # at most one edit every 400ms
    MAX_TG_LEN = 4000

    def __init__(
        self,
        chat_id: int | str,
        telegram_api: Callable[[str, dict], Optional[dict]],
    ):
        self.chat_id = str(chat_id)
        self.telegram_api = telegram_api

        self._text = ""           # current live-chunk content
        self._prior_text = ""     # content already shipped in earlier chunks
        self._live_msg_id: Optional[int] = None
        self._last_edit_ts = 0.0
        self._pending_flush = False
        self._timer: Optional[threading.Timer] = None
        self._tool_lines: list[str] = []  # extra tool_use blurbs to flush together
        self._closed = False
        # RLock so _append_text → _schedule_flush → _flush can re-acquire from
        # the same thread without deadlocking.
        self._lock = threading.RLock()

    # -- event entry points ----------------------------------------------

    def on_event(self, event: dict) -> None:
        et = event.get("type")
        if et == "stream_event":
            self._handle_stream_event(event)
        elif et == "assistant":
            self._handle_assistant_message(event)
        elif et == "user":
            # Echoed tool_result inputs; emit a compact note so users see
            # tool execution happened.
            self._handle_tool_result(event)
        elif et == "result":
            self._handle_result(event)
        elif et == "system":
            # init / status frames; nothing user-visible by default.
            pass

    # -- partial streaming -----------------------------------------------

    def _handle_stream_event(self, event: dict) -> None:
        """Token-level streaming deltas from --include-partial-messages."""
        ev = event.get("event") or {}
        ev_type = ev.get("type")
        if ev_type == "content_block_delta":
            delta = ev.get("delta") or {}
            if delta.get("type") == "text_delta":
                self._append_text(delta.get("text", ""))
            elif delta.get("type") == "thinking_delta":
                pass  # internal reasoning, skip
        # Other event types (message_start, content_block_start, ...) ignored.

    def _handle_assistant_message(self, event: dict) -> None:
        """Full assistant message frame. With partial streaming, the text
        has already been emitted token-by-token, so we only synthesize
        tool_use notices here.
        """
        message = event.get("message") or {}
        for block in message.get("content") or []:
            if not isinstance(block, dict):
                continue
            bt = block.get("type")
            if bt == "tool_use":
                name = block.get("name", "?")
                self._tool_lines.append(f"🔧 {name}")
                self._schedule_flush(force=False)
            # text already handled by stream_event deltas

    def _handle_tool_result(self, event: dict) -> None:
        message = event.get("message") or {}
        content = message.get("content")
        if not isinstance(content, list):
            return
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_result":
                is_err = bool(block.get("is_error"))
                tag = "❌" if is_err else "✓"
                self._tool_lines.append(f"  {tag}")
                self._schedule_flush(force=False)

    def _handle_result(self, event: dict) -> None:
        is_error = bool(event.get("is_error"))
        # If there's been no streamed text, fall back to the result field.
        if not (self._text.strip() or self._prior_text.strip()) and event.get("result"):
            self._append_text(str(event.get("result")))
        if is_error and event.get("result"):
            self._append_text(f"\n\n⚠️ {event.get('result')[:300]}")
        self._closed = True
        self._schedule_flush(force=True)

    # -- buffered TG edit logic ------------------------------------------

    def _append_text(self, fragment: str) -> None:
        if not fragment:
            return
        with self._lock:
            self._text += fragment
            self._schedule_flush(force=False)

    def _schedule_flush(self, force: bool) -> None:
        now = time.time()
        elapsed = now - self._last_edit_ts
        if force or elapsed >= self.EDIT_THROTTLE_S:
            self._flush()
        elif not self._pending_flush:
            delay = max(0.0, self.EDIT_THROTTLE_S - elapsed)
            self._pending_flush = True
            self._timer = threading.Timer(delay, self._timed_flush)
            self._timer.daemon = True
            self._timer.start()

    def _timed_flush(self) -> None:
        self._pending_flush = False
        self._flush()

    def _flush(self) -> None:
        with self._lock:
            self._last_edit_ts = time.time()
            # Merge tool lines as a header above text content.
            tool_prefix = ""
            if self._tool_lines:
                # Compact repeated tool names: "🔧 Bash 🔧 Bash" → "🔧 Bash ×2"
                tool_prefix = " ".join(self._tool_lines) + "\n\n"
            body = (tool_prefix + self._text).rstrip()
            if not body:
                return
            self._render(body)

    def _render(self, body: str) -> None:
        # Strategy: keep ONE active edit-target message. When content grows
        # past MAX_TG_LEN, freeze the current message (move its content to
        # _prior_text) and start a fresh one.
        if len(body) <= self.MAX_TG_LEN:
            self._upsert_live(body)
            return

        # Overflow: split off the first MAX_TG_LEN as a frozen chunk.
        head, tail = body[: self.MAX_TG_LEN], body[self.MAX_TG_LEN :]
        # Finalize current live message with head.
        self._upsert_live(head)
        self._live_msg_id = None
        self._prior_text += head
        self._text = tail
        # Tool_lines were already rendered in head; clear so they don't
        # repeat in the new chunk.
        self._tool_lines.clear()
        # Send the tail as a new live message.
        self._upsert_live(tail)

    def _upsert_live(self, text: str) -> None:
        if not text.strip():
            return
        if self._live_msg_id is None:
            resp = self.telegram_api("sendMessage", {
                "chat_id": self.chat_id,
                "text": text,
                "disable_notification": True,
            })
            if resp and resp.get("ok"):
                self._live_msg_id = resp["result"]["message_id"]
        else:
            self.telegram_api("editMessageText", {
                "chat_id": self.chat_id,
                "message_id": self._live_msg_id,
                "text": text,
            })


__all__ = ["OpenccSession", "TelegramStreamRenderer", "DEFAULT_CLI_PATH"]
