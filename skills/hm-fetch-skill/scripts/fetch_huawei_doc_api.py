#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://svc-drcn.developer.huawei.com/community/servlet/consumer/cn/documentPortal/getDocumentById"
PRESET_MIGRATION = [
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
    proc = subprocess.run(
        ["pandoc", "-f", "html", "-t", "gfm"],
        input=html.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode == 0:
        return proc.stdout.decode("utf-8", errors="ignore")
    return f"```html\n{html}\n```\n"


def fetch_doc(slug: str, language: str = "cn") -> dict:
    body = {"objectId": slug, "language": language}
    resp = post_json(API_URL, body)
    if str(resp.get("code")) != "0":
        raise RuntimeError(f"API error: code={resp.get('code')} msg={resp.get('message')}")
    value = resp.get("value") or {}
    if not value:
        raise RuntimeError("Empty document payload")
    return value


def extract_html(value: dict) -> str:
    content = value.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        raw = content.get("content")
        if isinstance(raw, str):
            return raw
        text = content.get("text")
        if isinstance(text, str):
            return text
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
    lines = [f"# {title}", "", f"- slug: `{slug}`"]
    if updated:
        lines.append(f"- updatedDate: `{updated}`")
    if source:
        lines.append(f"- source: {source}")
    if nav:
        lines.append(f"- navigationAddress: `{nav}`")
    lines.extend(["", md_body, ""])
    return "\n".join(lines)


def write_one(slug: str, out_path: Path, language: str) -> None:
    value = fetch_doc(slug, language=language)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_doc(value, slug), encoding="utf-8")
    print(f"[ok] {slug} -> {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Huawei documentPortal content by slug and convert to Markdown.")
    parser.add_argument("--slug", help="Single document slug to fetch (objectId in getDocumentById).")
    parser.add_argument(
        "--slug-list",
        help="Path to a text file containing slugs (one slug per line, '#' for comments).",
    )
    parser.add_argument("--out", help="Output markdown path for --slug.")
    parser.add_argument("--language", default="cn", help="Language code (default: cn).")
    parser.add_argument(
        "--preset",
        choices=["migration"],
        help="Fetch a preset group of pages.",
    )
    parser.add_argument(
        "--out-dir",
        default=str(Path(__file__).resolve().parents[1] / "references" / "huawei-migration"),
        help="Output directory for preset mode.",
    )
    args = parser.parse_args()

    if args.slug:
        out = Path(args.out) if args.out else Path(f"{args.slug}.md")
        write_one(args.slug, out, args.language)
        return

    if args.slug_list:
        out_dir = Path(args.out_dir)
        lines = Path(args.slug_list).read_text(encoding="utf-8", errors="ignore").splitlines()
        slugs: list[str] = []
        for raw in lines:
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            slugs.append(s)
        if not slugs:
            raise SystemExit(f"No valid slugs found in {args.slug_list}")
        for slug in slugs:
            write_one(slug, out_dir / f"{slug}.md", args.language)
        return

    if args.preset == "migration":
        out_dir = Path(args.out_dir)
        for slug, name in PRESET_MIGRATION:
            write_one(slug, out_dir / name, args.language)
        return

    parser.error("Provide either --slug or --preset migration")


if __name__ == "__main__":
    main()
