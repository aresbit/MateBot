#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHAPTER_DIR="$ROOT/references/chapters"

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <regex>"
  echo "example: $0 'union|narrow|keyof'"
  exit 1
fi

rg -n --glob '*.md' "$1" "$CHAPTER_DIR"
