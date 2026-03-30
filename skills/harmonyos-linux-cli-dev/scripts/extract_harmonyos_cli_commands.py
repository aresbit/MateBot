#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import OrderedDict
from pathlib import Path

TOOL_PATTERNS = OrderedDict(
    {
        "codelinter": re.compile(r"^codelinter\b.*"),
        "hstack": re.compile(r"^hstack\b.*"),
        "hvigorw": re.compile(r"^(?:\./)?hvigorw\b.*"),
        "ohpm": re.compile(r"^ohpm\b.*"),
        "hdc": re.compile(r"^hdc\b.*"),
        "aa": re.compile(r"^aa\b.*"),
        "bm": re.compile(r"^bm\b.*"),
        "hilog": re.compile(r"^hilog\b.*"),
        "param": re.compile(r"^param\b.*"),
        "atm": re.compile(r"^atm\b.*"),
        "anm": re.compile(r"^anm\b.*"),
        "cem": re.compile(r"^cem\b.*"),
        "edm": re.compile(r"^edm\b.*"),
        "devicedebug": re.compile(r"^devicedebug\b.*"),
        "mediatool": re.compile(r"^mediatool\b.*"),
        "packing": re.compile(r"^java -jar app_packing_tool\.jar\b.*"),
        "unpacking": re.compile(r"^java -jar app_unpacking_tool\.jar\b.*"),
    }
)

# Commands that appear in hdc command table without hdc prefix.
HDC_BARE = {
    "list targets",
    "wait",
    "tmode usb",
    "tmode port",
    "tmode port close",
    "tconn",
    "shell",
    "install",
    "uninstall",
    "file send",
    "file recv",
    "fport",
    "rport",
    "start",
    "kill",
    "hilog",
    "jpid",
    "track-jpid",
    "target boot",
    "sideload",
    "smode",
    "keygen",
    "version",
    "checkserver",
    "bugreport",
}


def classify(line: str) -> str | None:
    raw = line.strip().strip("`")
    if not raw:
        return None

    if raw in HDC_BARE:
        return "hdc"

    for tool, pattern in TOOL_PATTERNS.items():
        if pattern.match(raw):
            return tool
    return None


def normalize(tool: str, line: str) -> str:
    cmd = line.strip().strip("`")
    if tool == "hdc" and cmd in HDC_BARE:
        return f"hdc {cmd}"
    return cmd


def extract_commands(md_path: Path) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        tool = classify(line)
        if not tool:
            continue
        cmd = normalize(tool, line)
        out.append((tool, cmd))
    return out


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for x in items:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract HarmonyOS CLI commands from fetched markdown docs.")
    parser.add_argument("--docs-dir", default="references/harmonyos-commandline-docs")
    parser.add_argument("--out", default="references/harmonyos-commandline-docs/COMMANDS.md")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    grouped: dict[str, list[str]] = {k: [] for k in TOOL_PATTERNS.keys()}

    for md in sorted(docs_dir.glob("*.md")):
        if md.name in {"README.md", Path(args.out).name}:
            continue
        for tool, cmd in extract_commands(md):
            grouped.setdefault(tool, []).append(cmd)

    lines = ["# HarmonyOS Linux CLI 命令清单", "", "来源：`ide-commandline-get` 入口页递归抓取子页面后自动提取。", ""]

    for tool in TOOL_PATTERNS.keys():
        cmds = dedupe_keep_order(grouped.get(tool, []))
        if not cmds:
            continue
        lines.append(f"## {tool}")
        lines.append("")
        for c in cmds:
            lines.append(f"- `{c}`")
        lines.append("")

    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print(f"[ok] wrote {args.out}")


if __name__ == "__main__":
    main()
