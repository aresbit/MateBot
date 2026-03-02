#!/usr/bin/env python3
import json
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_thinking.py <jsonl_file>")
        print("Extracts thinking content from Claude Code session JSONL file.")
        sys.exit(1)

    jsonl_file = sys.argv[1]

    try:
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    msg_type = data.get('type')
                    if msg_type == 'assistant':
                        message = data.get('message', {})
                        content = message.get('content', [])
                        if isinstance(content, list):
                            for item in content:
                                if isinstance(item, dict) and item.get('type') == 'thinking':
                                    thinking = item.get('thinking', '')
                                    if thinking:
                                        print("=== THINKING ===")
                                        print(thinking[:2000])  # Limit output
                                        print()
                except json.JSONDecodeError:
                    # Silently skip malformed lines
                    pass
    except FileNotFoundError:
        print(f"Error: File '{jsonl_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()