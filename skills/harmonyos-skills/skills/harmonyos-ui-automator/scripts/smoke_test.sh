#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 - <<'PY' "$SCRIPT_DIR"
import ast
import pathlib
import sys

script_dir = pathlib.Path(sys.argv[1])
files = [
    script_dir / "hdc_utils.py",
    script_dir / "dump_layout.py",
    script_dir / "find_component.py",
    script_dir / "interact.py",
    script_dir / "shortcut.py",
]
for file in files:
    ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
print(f"AST OK: {len(files)} files")
PY

python3 "$SCRIPT_DIR/dump_layout.py" -h >/dev/null
python3 "$SCRIPT_DIR/find_component.py" -h >/dev/null
python3 "$SCRIPT_DIR/interact.py" -h >/dev/null
python3 "$SCRIPT_DIR/shortcut.py" -h >/dev/null

if python3 "$SCRIPT_DIR/find_component.py" --text "any" >/dev/null 2>&1; then
  echo "Expected find_component.py without layout to fail, but it succeeded" >&2
  exit 1
fi

echo "Smoke test passed"
