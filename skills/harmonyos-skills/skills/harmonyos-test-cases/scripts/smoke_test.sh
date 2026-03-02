#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

python3 - <<'PY' "$SCRIPT_DIR" "$SKILL_DIR"
import ast
import json
import pathlib
import sys

script_dir = pathlib.Path(sys.argv[1])
skill_dir = pathlib.Path(sys.argv[2])
run_test = script_dir / "run_test.py"
ast.parse(run_test.read_text(encoding="utf-8"), filename=str(run_test))

testcases = sorted((skill_dir / "testcases").glob("*.json"))
for tc in testcases:
    json.loads(tc.read_text(encoding="utf-8"))
print(f"AST/JSON OK: run_test.py + {len(testcases)} testcase(s)")
PY

python3 "$SCRIPT_DIR/run_test.py" -h >/dev/null
python3 "$SCRIPT_DIR/run_test.py" --list >/dev/null

if python3 "$SCRIPT_DIR/run_test.py" >/dev/null 2>&1; then
  echo "Expected run_test.py without args to fail, but it succeeded" >&2
  exit 1
fi

if python3 "$SCRIPT_DIR/run_test.py" __not_exists__ >/dev/null 2>&1; then
  echo "Expected non-existing testcase to fail, but it succeeded" >&2
  exit 1
fi

echo "Smoke test passed"
