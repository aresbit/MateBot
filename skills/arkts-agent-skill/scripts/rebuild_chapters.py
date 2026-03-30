#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = ROOT / "arktsspecification_ocr_full.md"
OUT_DIR = ROOT / "references" / "chapters"
INDEX_FILE = ROOT / "references" / "CHAPTER_INDEX.md"


def split_pages(text: str) -> dict[int, str]:
    page_re = re.compile(r"^## Page\s+(\d+)\s*$", re.M)
    parts = page_re.split(text)
    pages: dict[int, str] = {}
    for i in range(1, len(parts), 2):
        pnum = int(parts[i])
        body = parts[i + 1].lstrip("\n")
        pages[pnum] = f"## Page {pnum}\n\n{body}".rstrip() + "\n"
    return pages


def parse_chapter_starts(text: str, max_page: int) -> list[tuple[int, str, int]]:
    # Parse top-level chapter entries from the TOC area.
    chapter_re = re.compile(
        r"^\s*(\d{1,2})\s+([A-Za-z][A-Za-z0-9 ,&()\-/]+?)\s+(?:\.{2,}\s*)?(\d{1,3})\s*$"
    )
    raw: list[tuple[int, str, int]] = []
    for line in text.splitlines()[:1200]:
        m = chapter_re.match(line.rstrip())
        if not m:
            continue
        num = int(m.group(1))
        title = m.group(2).strip()
        start = int(m.group(3))
        if start <= max_page:
            raw.append((num, title, start))

    # Keep unique (chapter number, start page), sorted by start page.
    seen: set[tuple[int, int]] = set()
    chapters: list[tuple[int, str, int]] = []
    for num, title, start in sorted(raw, key=lambda x: (x[2], x[0])):
        key = (num, start)
        if key in seen:
            continue
        seen.add(key)
        chapters.append((num, title, start))
    return chapters


def main() -> None:
    if not SOURCE_MD.exists():
        raise SystemExit(f"Missing source markdown: {SOURCE_MD}")

    text = SOURCE_MD.read_text(encoding="utf-8", errors="ignore")
    pages = split_pages(text)
    if not pages:
        raise SystemExit("No page markers found in OCR markdown.")
    max_page = max(pages.keys())

    chapters = parse_chapter_starts(text, max_page)
    if not chapters:
        raise SystemExit("No chapter starts parsed from TOC area.")

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    index_lines = [
        "# ArkTS OCR Chapter Index",
        "",
        f"Source: `{SOURCE_MD.name}`",
        f"Detected OCR pages: 1-{max_page}",
        "",
        "Use `rg` on `references/chapters/` for fast targeted search.",
        "",
        "## Chapters",
        "",
    ]

    for i, (num, title, start) in enumerate(chapters):
        end = chapters[i + 1][2] - 1 if i + 1 < len(chapters) else max_page
        if end < start:
            end = start

        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        fname = f"ch{num:02d}-p{start:03d}-{slug}.md"
        target = OUT_DIR / fname

        body = [f"# Chapter {num}: {title}", "", f"Page range: {start}-{end}", ""]
        for p in range(start, end + 1):
            if p in pages:
                body.append(pages[p])
        target.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")

        index_lines.append(
            f"- Chapter {num}: `{title}` -> `references/chapters/{fname}` (pages {start}-{end})"
        )

    index_lines.extend(
        [
            "",
            "## Search Examples",
            "",
            '- `rg -n "union|narrow|keyof" references/chapters`',
            '- `rg -n "generic|type parameter" references/chapters`',
            '- `rg -n "annotation|decorator" references/chapters`',
        ]
    )
    INDEX_FILE.write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print(f"Rebuilt chapters: {len(chapters)}")
    print(f"Output: {OUT_DIR}")
    print(f"Index: {INDEX_FILE}")


if __name__ == "__main__":
    main()
