#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import deque
from html import unescape
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

API_URL = "https://svc-drcn.developer.huawei.com/community/servlet/consumer/cn/documentPortal/getDocumentById"
DOC_PREFIX = "https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/"
SEEDS = ["ide-commandline-get", "command-line-tools-overview"]
KW_ALLOW = (
    "command-line",
    "tool",
    "hdc",
    "hilog",
    "aa-",
    "bm-",
    "packing",
    "unpacking",
    "ide-commandline",
    "ide-software-install",
)


def post_json(payload: dict) -> dict:
    req = Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_doc(slug: str, language: str = "cn") -> dict:
    data = post_json({"objectId": slug, "language": language})
    if str(data.get("code")) != "0":
        raise RuntimeError(f"Fetch failed: slug={slug} code={data.get('code')} msg={data.get('message')}")
    return data.get("value") or {}


def slug_from_url(url: str) -> str | None:
    if not url.startswith(DOC_PREFIX):
        return None
    raw = url[len(DOC_PREFIX) :]
    raw = raw.split("?", 1)[0].split("#", 1)[0].strip("/")
    if not raw:
        return None
    return raw


def allowed_slug(slug: str) -> bool:
    s = slug.lower()
    return any(k in s for k in KW_ALLOW)


def extract_links(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    out: list[str] = []
    for a in soup.find_all("a"):
        href = (a.get("href") or "").strip()
        if not href:
            continue
        if href.startswith("/"):
            href = "https://developer.huawei.com" + href
        slug = slug_from_url(href)
        if slug and allowed_slug(slug):
            out.append(slug)
    return sorted(set(out))


def html_to_markdown_like(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()

    lines: list[str] = []

    for node in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "pre"]):
        name = node.name or ""
        text = unescape(node.get_text("\n", strip=True))
        if not text:
            continue
        if name.startswith("h") and len(name) == 2 and name[1].isdigit():
            lines.append("#" * int(name[1]) + " " + text)
            lines.append("")
        elif name == "pre":
            lines.append("```bash")
            lines.append(text)
            lines.append("```")
            lines.append("")
        elif name == "li":
            lines.append(f"- {text}")
        else:
            lines.append(text)
            lines.append("")

    # Deduplicate neighboring blank lines.
    cleaned: list[str] = []
    for line in lines:
        if line == "" and cleaned and cleaned[-1] == "":
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip() + "\n"


def render_doc(slug: str, value: dict) -> str:
    title = value.get("title") or slug
    updated = value.get("updatedDate") or ""
    catalog = value.get("catalogName") or ""
    file_name = value.get("fileName") or slug
    nav = value.get("navigationAddress") or ""
    source = f"https://developer.huawei.com/consumer/cn/doc/{catalog}/{file_name}" if catalog else ""

    content = value.get("content")
    html = content if isinstance(content, str) else (content or {}).get("content", "")

    body = html_to_markdown_like(html)
    lines = [f"# {title}", "", f"- slug: `{slug}`"]
    if updated:
        lines.append(f"- updatedDate: `{updated}`")
    if source:
        lines.append(f"- source: {source}")
    if nav:
        lines.append(f"- navigationAddress: `{nav}`")
    lines.extend(["", body])
    return "\n".join(lines)


def crawl(out_dir: Path, language: str = "cn", max_pages: int = 50) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    queue = deque(SEEDS)
    visited: set[str] = set()
    ordered: list[str] = []

    while queue and len(visited) < max_pages:
        slug = queue.popleft()
        if slug in visited:
            continue
        if not allowed_slug(slug):
            continue

        value = fetch_doc(slug, language=language)
        content = value.get("content")
        html = content if isinstance(content, str) else (content or {}).get("content", "")

        md = render_doc(slug, value)
        (out_dir / f"{slug}.md").write_text(md, encoding="utf-8")

        visited.add(slug)
        ordered.append(slug)

        for next_slug in extract_links(html):
            if next_slug not in visited:
                queue.append(next_slug)

    # Write index.
    index = ["# HarmonyOS 命令行文档抓取索引", ""]
    for s in ordered:
        index.append(f"- [{s}]({s}.md)")
    index.append("")
    (out_dir / "README.md").write_text("\n".join(index), encoding="utf-8")

    return ordered


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch HarmonyOS command-line related guide pages as Markdown.")
    parser.add_argument("--out-dir", default="references/harmonyos-commandline-docs")
    parser.add_argument("--language", default="cn")
    parser.add_argument("--max-pages", type=int, default=50)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    pages = crawl(out_dir=out_dir, language=args.language, max_pages=args.max_pages)
    print(f"[ok] fetched {len(pages)} pages")
    for p in pages:
        print(f" - {p}")


if __name__ == "__main__":
    main()
