#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/references/huawei-migration"
FETCH="$HOME/.claude/skills/fetch-skill/scripts/fetch.py"
API_FETCH="$ROOT/scripts/fetch_huawei_migration_api.py"

mkdir -p "$OUT"

if python3 "$API_FETCH" --out-dir "$OUT"; then
  echo "Fetched via Huawei documentPortal API."
else
  echo "API fetch failed, fallback to fetch-skill."
  python3 "$FETCH" "https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-migration-background" \
    -o "$OUT/01-arkts-migration-background.md" -q
  python3 "$FETCH" "https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/typescript-to-arkts-migration-guide" \
    -o "$OUT/02-typescript-to-arkts-migration-guide.md" -q
  python3 "$FETCH" "https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-more-cases" \
    -o "$OUT/03-arkts-more-cases.md" -q
fi

echo "Updated:"
ls -lh "$OUT"/*.md
