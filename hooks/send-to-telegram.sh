#!/bin/bash
# Claude Code Stop hook - sends response back to Telegram
# Install: copy to ~/.claude/hooks/ and add to ~/.claude/settings.json

TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-YOUR_BOT_TOKEN_HERE}"
INPUT=$(cat)
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path')
CHAT_ID_FILE=~/.claude/telegram_chat_id
PENDING_FILE=~/.claude/telegram_pending

# Only respond to Telegram-initiated messages
[ ! -f "$PENDING_FILE" ] && exit 0

PENDING_TIME=$(cat "$PENDING_FILE" 2>/dev/null)
NOW=$(date +%s)
[ -z "$PENDING_TIME" ] || [ $((NOW - PENDING_TIME)) -gt 600 ] && rm -f "$PENDING_FILE" && exit 0
[ ! -f "$CHAT_ID_FILE" ] || [ ! -f "$TRANSCRIPT_PATH" ] && rm -f "$PENDING_FILE" && exit 0

CHAT_ID=$(cat "$CHAT_ID_FILE")
LAST_USER_LINE=$(grep -n '"type":"user"' "$TRANSCRIPT_PATH" | tail -1 | cut -d: -f1)
[ -z "$LAST_USER_LINE" ] && rm -f "$PENDING_FILE" && exit 0

TMPFILE=$(mktemp)
tail -n "+$LAST_USER_LINE" "$TRANSCRIPT_PATH" | \
  grep '"type":"assistant"' | \
  jq -rs '[.[].message.content[] | select(.type == "text") | .text] | join("\n\n")' > "$TMPFILE" 2>/dev/null

[ ! -s "$TMPFILE" ] && rm -f "$TMPFILE" "$PENDING_FILE" && exit 0

python3 - "$TMPFILE" "$CHAT_ID" "$TELEGRAM_BOT_TOKEN" << 'PYEOF'
import sys, re, json, urllib.request

tmpfile, chat_id, token = sys.argv[1], sys.argv[2], sys.argv[3]
with open(tmpfile) as f:
    text = f.read().strip()

if not text or text == "null":
    sys.exit(0)

# Extract and remove memory block (CCL-style format) before sending
memory_pattern = r'--\s*memory\s*\n(.*?)\n--'
if re.search(memory_pattern, text, re.DOTALL):
    text = re.sub(memory_pattern, '', text, flags=re.DOTALL).strip()

if len(text) > 4000:
    text = text[:4000] + "\n..."

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

blocks, inlines = [], []
text = re.sub(r'```(\w*)\n?(.*?)```', lambda m: (blocks.append((m.group(1) or '', m.group(2))), f"\x00B{len(blocks)-1}\x00")[1], text, flags=re.DOTALL)
text = re.sub(r'`([^`\n]+)`', lambda m: (inlines.append(m.group(1)), f"\x00I{len(inlines)-1}\x00")[1], text)
text = esc(text)
text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)

for i, (lang, code) in enumerate(blocks):
    text = text.replace(f"\x00B{i}\x00", f'<pre><code class="language-{lang}">{esc(code.strip())}</code></pre>' if lang else f'<pre>{esc(code.strip())}</pre>')
for i, code in enumerate(inlines):
    text = text.replace(f"\x00I{i}\x00", f'<code>{esc(code)}</code>')

def send(txt, mode=None):
    data = {"chat_id": chat_id, "text": txt}
    if mode:
        data["parse_mode"] = mode
    try:
        req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", json.dumps(data).encode(), {"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=10).read()).get("ok")
    except:
        return False

if not send(text, "HTML"):
    with open(tmpfile) as f:
        send(f.read()[:4096])
PYEOF

rm -f "$TMPFILE" "$PENDING_FILE"
exit 0
