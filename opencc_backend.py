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
    edit-updated in place.

    Concurrency model: stream-json events arrive on the OpenccSession stdout
    reader thread. Those handlers must NOT call Telegram synchronously —
    `api.telegram.org` is routed through the user's HTTP proxy and a
    round-trip is typically 2–5s in China. Blocking the reader thread
    back-pressures claude-js's stdout, which stalls generation and was the
    cause of the "messages arriving super slow" symptom after the spawn-mode
    switch.

    Design: a single per-renderer worker thread owns ALL Telegram I/O.
    Event handlers only mutate buffered state under a lock and set a
    `_dirty` event. The worker:
      - waits for `_dirty` (or a short timeout)
      - enforces a min interval between TG round-trips (`EDIT_THROTTLE_S`)
      - snapshots the current body and edits / sends in place
      - coalesces: many appends + one network call
    """

    # Min seconds between consecutive editMessageText calls. The proxy adds
    # 2–5s per round-trip; smaller values just queue useless work.
    EDIT_THROTTLE_S = 1.5
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
        self._tool_lines: list[str] = []
        self._closed = False
        self._lock = threading.Lock()

        # Worker thread that owns ALL network I/O.
        self._dirty = threading.Event()
        self._worker = threading.Thread(target=self._render_worker, daemon=True)
        self._worker.start()

    # -- event entry points ----------------------------------------------

    def on_event(self, event: dict) -> None:
        et = event.get("type")
        if et == "stream_event":
            self._handle_stream_event(event)
        elif et == "assistant":
            self._handle_assistant_message(event)
        elif et == "user":
            self._handle_tool_result(event)
        elif et == "result":
            self._handle_result(event)
        # "system" init / status frames: nothing user-visible.

    def _handle_stream_event(self, event: dict) -> None:
        ev = event.get("event") or {}
        if ev.get("type") == "content_block_delta":
            delta = ev.get("delta") or {}
            if delta.get("type") == "text_delta":
                self._append_text(delta.get("text", ""))
            # thinking_delta: internal reasoning, skip.

    def _handle_assistant_message(self, event: dict) -> None:
        message = event.get("message") or {}
        added = False
        with self._lock:
            for block in message.get("content") or []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    self._tool_lines.append(f"🔧 {block.get('name', '?')}")
                    added = True
        if added:
            self._dirty.set()

    def _handle_tool_result(self, event: dict) -> None:
        message = event.get("message") or {}
        content = message.get("content")
        if not isinstance(content, list):
            return
        added = False
        with self._lock:
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    tag = "❌" if block.get("is_error") else "✓"
                    self._tool_lines.append(f"  {tag}")
                    added = True
        if added:
            self._dirty.set()

    def _handle_result(self, event: dict) -> None:
        is_error = bool(event.get("is_error"))
        with self._lock:
            if not (self._text.strip() or self._prior_text.strip()) and event.get("result"):
                self._text += str(event.get("result"))
            if is_error and event.get("result"):
                self._text += f"\n\n⚠️ {str(event.get('result'))[:300]}"
            self._closed = True
        self._dirty.set()

    def _append_text(self, fragment: str) -> None:
        if not fragment:
            return
        with self._lock:
            self._text += fragment
        self._dirty.set()

    def close(self) -> None:
        """Signal the worker to exit. Idempotent; safe to call when an
        already-finished renderer is being replaced for a new turn."""
        with self._lock:
            self._closed = True
        self._dirty.set()

    # -- worker loop -----------------------------------------------------

    def _render_worker(self) -> None:
        last_sent_ts = 0.0
        last_sent_body = ""
        while True:
            # Wake on new content or periodically (so close detection isn't
            # delayed if `_closed` is set while `_dirty` is already cleared).
            self._dirty.wait(timeout=1.0)
            self._dirty.clear()

            gap = time.time() - last_sent_ts
            if gap < self.EDIT_THROTTLE_S:
                time.sleep(self.EDIT_THROTTLE_S - gap)

            with self._lock:
                tool_prefix = (" ".join(self._tool_lines) + "\n\n") if self._tool_lines else ""
                text_snapshot = self._text
                tool_lines_snap_count = len(self._tool_lines)
                closed = self._closed

            body = (tool_prefix + text_snapshot).rstrip()

            if not body:
                if closed:
                    return
                continue

            try:
                if len(body) <= self.MAX_TG_LEN:
                    if body != last_sent_body:
                        self._upsert_live(body)
                        last_sent_body = body
                        last_sent_ts = time.time()
                else:
                    head = body[: self.MAX_TG_LEN]
                    self._upsert_live(head)
                    last_sent_ts = time.time()
                    with self._lock:
                        shipped_text_chars = max(0, self.MAX_TG_LEN - len(tool_prefix))
                        self._text = self._text[shipped_text_chars:]
                        del self._tool_lines[:tool_lines_snap_count]
                        self._prior_text += head
                        self._live_msg_id = None
                    last_sent_body = ""
                    # Tail must be sent — wake immediately on next loop.
                    self._dirty.set()
                    continue
            except Exception as e:
                # Don't kill the worker on transient TG/proxy errors; leave
                # last_sent_body untouched so we retry on next wake-up.
                print(f"[opencc-renderer] send error: {e}")

            if closed and not self._dirty.is_set():
                return

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
