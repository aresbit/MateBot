#!/usr/bin/env python3
import json
import sys

def extract_content(content, thinking_full=False, tools_full=False):
    """Extract text from message content which can be string or array of objects

    Args:
        content: content field from message
        thinking_full: if True, include full thinking text without truncation
        tools_full: if True, include full tool call details
    """
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict) and item.get('type') == 'text':
                texts.append(item.get('text', ''))
            elif isinstance(item, dict) and item.get('type') == 'thinking':
                thinking = item.get('thinking', '')
                if thinking_full:
                    texts.append(f"=== THINKING ===\n{thinking}")
                else:
                    texts.append(f"[Thinking: {thinking[:100]}...]")
            elif isinstance(item, dict) and item.get('type') == 'tool_use':
                name = item.get('name', '')
                input_data = item.get('input', {})
                if tools_full:
                    texts.append(f"=== TOOL CALL: {name} ===\n{json.dumps(input_data, indent=2, ensure_ascii=False)}")
                else:
                    texts.append(f"[Tool call: {name} {input_data}]")
        return '\n'.join(texts)
    else:
        return str(content)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_session.py <jsonl_file> [--thinking-full] [--tools-full] [--role <user|assistant>]")
        print("Extracts conversation from Claude Code session JSONL file.")
        print("Options:")
        print("  --thinking-full   Show full thinking text instead of truncation")
        print("  --tools-full      Show full tool call details")
        print("  --role <role>     Filter by role (user or assistant)")
        sys.exit(1)

    jsonl_file = sys.argv[1]
    thinking_full = False
    tools_full = False
    role_filter = None  # 'user', 'assistant', or None for both

    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--thinking-full':
            thinking_full = True
            i += 1
        elif arg == '--tools-full':
            tools_full = True
            i += 1
        elif arg == '--role':
            if i + 1 < len(sys.argv):
                role_filter = sys.argv[i + 1]
                if role_filter not in ('user', 'assistant'):
                    print(f"Error: role must be 'user' or 'assistant', got '{role_filter}'", file=sys.stderr)
                    sys.exit(1)
                i += 2
            else:
                print("Error: --role requires a value", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Error: Unknown argument '{arg}'", file=sys.stderr)
            sys.exit(1)

    try:
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    msg_type = data.get('type')
                    if msg_type == 'user' or msg_type == 'assistant':
                        # Apply role filter
                        if role_filter and msg_type != role_filter:
                            continue

                        role = 'User' if msg_type == 'user' else 'Assistant'
                        message = data.get('message', {})
                        content = message.get('content', '')
                        text = extract_content(content, thinking_full, tools_full)
                        # Skip empty messages
                        if text.strip():
                            print(f"=== {role} ===")
                            print(text[:5000])  # Limit output
                            print()
                    elif msg_type == 'file-history-snapshot':
                        # Skip metadata
                        pass
                except json.JSONDecodeError as e:
                    print(f"Error parsing line {line_num}: {e}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: File '{jsonl_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()