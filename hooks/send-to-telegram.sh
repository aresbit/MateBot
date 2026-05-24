#!/bin/bash
# Claude Code Stop hook - authoritative sender for TG-initiated responses.
# Install: copy to ~/.claude/hooks/ and reference it from ~/.claude/settings.json
#   under hooks.Stop.
#
# Replaces the old polling-based delivery in bridge.py (which raced this hook
# and deleted the pending file before Stop fired). bridge.py's ResponseMonitor
# now only tracks state + saves memory; this hook owns TG delivery.

TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-YOUR_BOT_TOKEN_HERE}"
INPUT=$(cat)

export TELEGRAM_BOT_TOKEN
export CLAUDE_HOOK_INPUT="$INPUT"

exec python3 - <<'PYEOF'
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID_FILE = Path.home() / ".claude" / "telegram_chat_id"
PENDING_FILE = Path.home() / ".claude" / "telegram_pending"
SENT_OFFSET_FILE = Path.home() / ".claude" / "telegram_sent_offset"
MAX_TG_LENGTH = 4000
PENDING_TIMEOUT = 600  # seconds


def log(msg):
    print(f"[hook] {msg}", file=sys.stderr)


def telegram_send(chat_id, text):
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        log("TELEGRAM_BOT_TOKEN not configured")
        return False

    chunks = []
    if len(text) <= MAX_TG_LENGTH:
        chunks = [text]
    else:
        current = ""
        for line in text.split("\n"):
            if len(current) + len(line) + 1 > MAX_TG_LENGTH:
                if current:
                    chunks.append(current)
                current = line
            else:
                current = (current + "\n" + line) if current else line
        if current:
            chunks.append(current)

    all_ok = True
    for i, chunk in enumerate(chunks):
        prefix = f"[{i+1}/{len(chunks)}] " if len(chunks) > 1 else ""
        data = {"chat_id": chat_id, "text": prefix + chunk}
        try:
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data=json.dumps(data).encode(),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                result = json.loads(r.read())
                if not result.get("ok"):
                    log(f"TG send failed: {result}")
                    all_ok = False
        except Exception as e:
            log(f"TG request error: {e}")
            all_ok = False
    return all_ok


def find_last_real_user_line(transcript_path):
    """Index (0-based) of the last actual user prompt line.

    Tool results are wrapped as user-role messages in Claude's transcript, so a
    naive grep '"type":"user"' picks the most recent tool_result and truncates
    the response. We require at least one text content block.
    """
    last_line = -1
    try:
        with open(transcript_path, "r") as f:
            for i, line in enumerate(f):
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("type") != "user":
                    continue
                msg = entry.get("message", {})
                content = msg.get("content")
                if isinstance(content, str) and content.strip():
                    last_line = i
                elif isinstance(content, list):
                    if any(
                        isinstance(b, dict) and b.get("type") == "text"
                        for b in content
                    ):
                        last_line = i
    except Exception as e:
        log(f"transcript read error: {e}")
    return last_line


def format_tool_use(block):
    name = block.get("name", "?")
    tinput = block.get("input", {})
    try:
        input_str = json.dumps(tinput, indent=2, ensure_ascii=False)
    except Exception:
        input_str = str(tinput)
    if len(input_str) > 800:
        input_str = input_str[:800] + "\n... (truncated)"
    return f"🔧 {name}\n```json\n{input_str}\n```"


def extract_assistant_content(transcript_path, after_line):
    blocks = []
    try:
        with open(transcript_path, "r") as f:
            for i, line in enumerate(f):
                if i <= after_line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("type") != "assistant":
                    continue
                content_blocks = entry.get("message", {}).get("content", [])
                if not isinstance(content_blocks, list):
                    continue
                for block in content_blocks:
                    if not isinstance(block, dict):
                        continue
                    bt = block.get("type")
                    if bt == "text":
                        text = block.get("text", "").strip()
                        if not text:
                            continue
                        # Skip pure XML observation tags
                        if text.startswith("<") and text.endswith(">") and "/" in text[1:]:
                            continue
                        blocks.append(text)
                    elif bt == "tool_use":
                        blocks.append(format_tool_use(block))
                    # thinking / tool_result skipped
    except Exception as e:
        log(f"extract error: {e}")
    return "\n\n".join(blocks).strip()


def strip_memory_block(text):
    pattern = r"--\s*memory\s*\n.*?\n--\s*"
    return re.sub(pattern, "", text, flags=re.DOTALL).strip()


def load_sent_offset(transcript_path):
    """Return how many response chars have already been sent for this transcript."""
    if not SENT_OFFSET_FILE.exists():
        return 0
    try:
        state = json.loads(SENT_OFFSET_FILE.read_text())
        if state.get("transcript") == str(transcript_path):
            return int(state.get("sent_chars", 0))
    except Exception:
        pass
    return 0


def save_sent_offset(transcript_path, sent_chars):
    try:
        SENT_OFFSET_FILE.write_text(json.dumps({
            "transcript": str(transcript_path),
            "sent_chars": sent_chars,
            "ts": int(time.time()),
        }))
    except Exception as e:
        log(f"offset save error: {e}")


def main():
    raw = os.environ.get("CLAUDE_HOOK_INPUT") or sys.stdin.read()
    try:
        payload = json.loads(raw) if raw else {}
    except Exception as e:
        log(f"stdin parse error: {e}")
        payload = {}

    transcript_path_str = payload.get("transcript_path") or ""
    transcript_path = Path(transcript_path_str)

    if not PENDING_FILE.exists():
        sys.exit(0)

    try:
        pending_ts = int(PENDING_FILE.read_text().strip())
        if time.time() - pending_ts > PENDING_TIMEOUT:
            PENDING_FILE.unlink(missing_ok=True)
            sys.exit(0)
    except Exception:
        PENDING_FILE.unlink(missing_ok=True)
        sys.exit(0)

    if not CHAT_ID_FILE.exists() or not transcript_path.exists():
        PENDING_FILE.unlink(missing_ok=True)
        sys.exit(0)

    chat_id = CHAT_ID_FILE.read_text().strip()
    if not chat_id:
        PENDING_FILE.unlink(missing_ok=True)
        sys.exit(0)

    last_user = find_last_real_user_line(transcript_path)
    if last_user < 0:
        PENDING_FILE.unlink(missing_ok=True)
        sys.exit(0)

    full_text = extract_assistant_content(transcript_path, last_user)
    full_text = strip_memory_block(full_text)
    if not full_text:
        PENDING_FILE.unlink(missing_ok=True)
        sys.exit(0)

    # Send only the delta since the last send for this transcript/turn,
    # so streaming PostToolUse hooks (if installed) don't duplicate Stop output.
    already_sent = load_sent_offset(transcript_path)
    if already_sent and already_sent <= len(full_text) and full_text[:already_sent].strip():
        delta = full_text[already_sent:].strip()
    else:
        delta = full_text

    if not delta:
        PENDING_FILE.unlink(missing_ok=True)
        sys.exit(0)

    if telegram_send(chat_id, delta):
        save_sent_offset(transcript_path, len(full_text))
        PENDING_FILE.unlink(missing_ok=True)
    else:
        # Keep pending file so the bridge.py fallback path can retry.
        log("send failed; pending file preserved for fallback")

    sys.exit(0)


if __name__ == "__main__":
    main()
PYEOF
