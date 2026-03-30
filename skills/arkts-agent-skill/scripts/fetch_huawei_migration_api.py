#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://svc-drcn.developer.huawei.com/community/servlet/consumer/cn/documentPortal/getDocumentById"
DOCS = [
    ("arkts-migration-background", "01-arkts-migration-background.md"),
    ("typescript-to-arkts-migration-guide", "02-typescript-to-arkts-migration-guide.md"),
    ("arkts-more-cases", "03-arkts-more-cases.md"),
]


def post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def html_to_md(html: str) -> str:
    # Prefer pandoc for stable HTML -> Markdown conversion.
    proc = subprocess.run(
        ["pandoc", "-f", "html", "-t", "gfm"],
        input=html.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode == 0:
        return proc.stdout.decode("utf-8", errors="ignore")
    # Fallback: return raw HTML block if pandoc is unavailable.
    return f"```html\n{html}\n```\n"


def fetch_one(slug: str) -> dict:
    body = {"objectId": slug, "language": "cn"}
    resp = post_json(API_URL, body)
    if str(resp.get("code")) != "0":
        raise RuntimeError(f"API error for {slug}: code={resp.get('code')} msg={resp.get('message')}")
    value = resp.get("value") or {}
    if not value:
        raise RuntimeError(f"Empty value for {slug}")
    return value


def extract_html(value: dict) -> str:
    content = value.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        # Common structures: {"content": "<html...>"} or {"text": "<html...>"}
        raw = content.get("content")
        if isinstance(raw, str):
            return raw
        text = content.get("text")
        if isinstance(text, str):
            return text
        # Fallback: first string field.
        for v in content.values():
            if isinstance(v, str):
                return v
    return ""


def render_doc(value: dict, slug: str) -> str:
    title = value.get("title") or slug
    updated = value.get("updatedDate") or ""
    file_name = value.get("fileName") or slug
    catalog = value.get("catalogName") or ""
    nav = value.get("navigationAddress") or ""
    source = f"https://developer.huawei.com/consumer/cn/doc/{catalog}/{file_name}" if catalog else ""
    html = extract_html(value)
    md_body = html_to_md(html).strip()
    front = [
        f"# {title}",
        "",
        f"- slug: `{slug}`",
        f"- updatedDate: `{updated}`" if updated else "",
        f"- source: {source}" if source else "",
        f"- navigationAddress: `{nav}`" if nav else "",
        "",
    ]
    front = [x for x in front if x != ""]
    return "\n".join(front) + "\n\n" + md_body + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Huawei HarmonyOS migration docs via documentPortal API.")
    parser.add_argument(
        "--out-dir",
        default=str(Path(__file__).resolve().parents[1] / "references" / "huawei-migration"),
        help="Output directory for markdown files",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for slug, filename in DOCS:
        try:
            value = fetch_one(slug)
            md = render_doc(value, slug)
            target = out_dir / filename
            target.write_text(md, encoding="utf-8")
            print(f"[ok] {slug} -> {target}")
        except (HTTPError, URLError, RuntimeError) as e:
            print(f"[err] {slug}: {e}")
            raise


if __name__ == "__main__":
    main()
