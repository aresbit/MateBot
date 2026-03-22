#!/usr/bin/env python3
"""Unified content fetcher — routes by URL type to the best available backend.

URL routing:
  X / Twitter  https://x.com/* https://twitter.com/*
               -> FxTwitter API (zero-dep) for single tweets
               -> Camofox + Nitter for timelines / replies / articles
  WeChat       https://mp.weixin.qq.com/s/*
               -> wechat-article-exporter API (if WECHAT_API_URL set)
               -> Jina Reader fallback
  General      everything else
               -> Jina Reader -> defuddle.md -> markdown.new -> raw HTML

Usage:
    python3 fetch.py <url> [options]
    python3 fetch.py --user USERNAME [--limit N]   # timeline mode
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

FXTWITTER_API = "https://api.fxtwitter.com"
CAMOFOX_DEFAULT_PORT = 9377


# ---------------------------------------------------------------------------
# DraftJS blocks → Markdown  (used for X Articles)
# ---------------------------------------------------------------------------

def _apply_inline_styles(text: str, ranges: List[Dict]) -> str:
    """Apply Bold/Italic inline style ranges to a text string."""
    if not ranges:
        return text
    # Build a list of chars with tags
    chars = list(text)
    opens:  Dict[int, List[str]] = {}
    closes: Dict[int, List[str]] = {}
    for r in sorted(ranges, key=lambda x: x.get("offset", 0)):
        style  = r.get("style", "")
        start  = r.get("offset", 0)
        length = r.get("length", 0)
        end    = start + length
        tag = "**" if style == "Bold" else ("*" if style == "Italic" else "")
        if not tag:
            continue
        opens.setdefault(start, []).append(tag)
        closes.setdefault(end, []).insert(0, tag)
    out = []
    for i, ch in enumerate(chars):
        out.extend(opens.get(i, []))
        out.append(ch)
        out.extend(closes.get(i, []))
    out.extend(closes.get(len(chars), []))
    return "".join(out)


def _draftjs_to_md(article: Dict) -> str:
    """Convert FxTwitter article.content (DraftJS) to Markdown."""
    content = article.get("content", {})
    blocks  = content.get("blocks", [])
    entity_list = content.get("entityMap", [])
    media_ents  = article.get("media_entities", [])

    # Build entity_map: key (str) -> entity value
    entity_map: Dict[str, Dict] = {}
    for ent in entity_list:
        entity_map[str(ent.get("key", ""))] = ent.get("value", {})

    # Build media lookup: media_id (str) -> original_img_url
    media_lookup: Dict[str, str] = {}
    for me in media_ents:
        mid  = str(me.get("media_id", ""))
        url  = me.get("media_info", {}).get("original_img_url", "")
        if mid and url:
            media_lookup[mid] = url

    title = article.get("title", "")
    lines = [f"# {title}", ""] if title else []

    for block in blocks:
        btype  = block.get("type", "unstyled")
        text   = block.get("text", "")
        ranges = block.get("inlineStyleRanges", [])
        eranges = block.get("entityRanges", [])

        if btype == "atomic":
            # Image block: resolve via entityRanges -> entityMap -> media_entities
            for er in eranges:
                ent_key = str(er.get("key", ""))
                ent_val = entity_map.get(ent_key, {})
                ent_data = ent_val.get("data", {})
                caption = ent_data.get("caption", "")
                items = ent_data.get("mediaItems", [])
                for item in items:
                    mid = str(item.get("mediaId", ""))
                    img_url = media_lookup.get(mid, "")
                    if img_url:
                        alt = caption or "image"
                        lines.append(f"\n![{alt}]({img_url})\n")
            continue

        styled = _apply_inline_styles(text, ranges)

        if btype == "header-one":
            lines.append(f"# {styled}")
        elif btype == "header-two":
            lines.append(f"\n## {styled}")
        elif btype == "header-three":
            lines.append(f"\n### {styled}")
        elif btype == "unordered-list-item":
            lines.append(f"- {styled}")
        elif btype == "ordered-list-item":
            lines.append(f"1. {styled}")
        elif btype == "blockquote":
            lines.append(f"> {styled}")
        elif btype == "code-block":
            lines.append(f"```\n{text}\n```")
        else:  # unstyled or unknown
            lines.append(styled if styled.strip() else "")

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg: str, verbose: bool) -> None:
    if verbose:
        print(msg, file=sys.stderr)


def http_get(url: str, headers: Optional[Dict] = None, timeout: int = 30) -> str:
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def http_json(url: str, headers: Optional[Dict] = None, timeout: int = 30) -> Any:
    return json.loads(http_get(url, headers=headers, timeout=timeout))


# ---------------------------------------------------------------------------
# URL detection
# ---------------------------------------------------------------------------

_RE_TWITTER = re.compile(r"https?://(www\.)?(twitter|x)\.com/", re.I)
_RE_TWEET   = re.compile(r"https?://(www\.)?(twitter|x)\.com/\w+/status/(\d+)", re.I)
_RE_ARTICLE = re.compile(r"https?://(www\.)?(twitter|x)\.com/i/(article|web/article)/(\d+)", re.I)
_RE_WECHAT  = re.compile(r"https?://mp\.weixin\.qq\.com/", re.I)


def detect_mode(url: str) -> str:
    if _RE_TWITTER.search(url):
        return "twitter"
    if _RE_WECHAT.search(url):
        return "wechat"
    return "web"


# ---------------------------------------------------------------------------
# Web fetcher  (Jina -> defuddle.md -> markdown.new -> raw)
# ---------------------------------------------------------------------------

def fetch_web(url: str, timeout: int = 30, skip_jina: bool = False, verbose: bool = True) -> str:
    strategies: List[Tuple[str, str, Optional[Dict]]] = []
    if not skip_jina:
        strategies.append(("Jina Reader",  f"https://r.jina.ai/{url}",   {"Accept": "text/markdown"}))
    strategies += [
        ("defuddle.md",  f"https://defuddle.md/{url}",   None),
        ("markdown.new", f"https://markdown.new/{url}",  None),
        ("Raw HTML",     url,                             None),
    ]
    errors: List[str] = []
    for name, fetch_url, hdrs in strategies:
        try:
            log(f"[web/{name}] fetching...", verbose)
            content = http_get(fetch_url, headers=hdrs, timeout=timeout)
            log(f"[web/{name}] ok ({len(content)} chars)", verbose)
            return content
        except Exception as e:
            log(f"[web/{name}] failed: {e}", verbose)
            errors.append(f"{name}: {e}")
    raise RuntimeError("All web strategies failed:\n  " + "\n  ".join(errors))


# ---------------------------------------------------------------------------
# Twitter / X fetcher
# ---------------------------------------------------------------------------

def _camofox_rpc(method: str, params: Dict, port: int, timeout: int = 60) -> Any:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(
        f"http://localhost:{port}/api",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _camofox_ok(port: int) -> bool:
    try:
        _camofox_rpc("ping", {}, port=port, timeout=3)
        return True
    except Exception:
        return False


def _camofox_snapshot(url: str, port: int, timeout: int, verbose: bool) -> str:
    key = f"fetch-{int(time.time())}"
    log(f"[Camofox] opening {url}", verbose)
    r = _camofox_rpc("openTab", {"url": url, "sessionKey": key}, port=port, timeout=timeout)
    tab_id = r.get("result", {}).get("tabId", "")
    try:
        time.sleep(4)
        r2 = _camofox_rpc("getSnapshot", {"tabId": tab_id, "sessionKey": key}, port=port, timeout=timeout)
        snap = r2.get("result", {}).get("snapshot", "")
        log(f"[Camofox] snapshot {len(snap)} chars", verbose)
        return snap
    finally:
        try:
            _camofox_rpc("closeTab", {"tabId": tab_id, "sessionKey": key}, port=port, timeout=10)
        except Exception:
            pass


def fetch_twitter(url: str, args: argparse.Namespace) -> str:
    verbose = args.verbose
    port    = args.port
    timeout = args.timeout
    pretty  = args.pretty
    text    = args.text_only

    def _json(obj: Any) -> str:
        return json.dumps(obj, ensure_ascii=False, indent=2 if pretty else None)

    # X Article
    if _RE_ARTICLE.search(url):
        if not _camofox_ok(port):
            raise RuntimeError(f"X Articles require Camofox on port {port}.")
        snap = _camofox_snapshot(url, port, timeout, verbose)
        return snap if text else _json({"type": "article", "url": url, "content": snap})

    # User timeline
    if args.user:
        if not _camofox_ok(port):
            raise RuntimeError(f"User timeline requires Camofox on port {port}.")
        username = args.user.lstrip("@")
        nitter_url = f"https://nitter.net/{username}"
        snap = _camofox_snapshot(nitter_url, port, timeout, verbose)
        return snap if text else _json({"type": "timeline", "user": username, "snapshot": snap})

    # Single tweet via FxTwitter (zero dependencies)
    if _RE_TWEET.search(url):
        m = _RE_TWEET.search(url)
        tweet_id = m.group(3)
        # extract username from URL path: /{user}/status/{id}
        user_m = re.search(r"\.com/([^/]+)/status/", url, re.I)
        username = user_m.group(1) if user_m else "_"
        # FxTwitter requires /{username}/status/{id}
        for api_path in [f"/{username}/status/{tweet_id}", f"/status/{tweet_id}"]:
            try:
                api_url = f"{FXTWITTER_API}{api_path}"
                log(f"[twitter/FxTwitter] {api_url}", verbose)
                data = http_json(api_url, timeout=timeout)
                break
            except urllib.error.HTTPError as exc:
                if exc.code == 404:
                    continue
                raise
        else:
            log("[twitter/FxTwitter] 404, falling back to web fetch", verbose)
            return fetch_web(url, timeout=timeout, verbose=verbose)
        t = data.get("tweet", {})

        # X Article: tweet body is empty, real content is in article{}
        article = t.get("article")
        if article:
            art_title = article.get("title", "(no title)")
            log(f"[twitter] X Article detected: {art_title}", verbose)
            log("[twitter] parsing article.content.blocks (DraftJS)…", verbose)
            md = _draftjs_to_md(article)
            log(f"[twitter/article] parsed ({len(md)} chars)", verbose)
            if text:
                author  = t.get("author", {}).get("name", "")
                handle  = t.get("author", {}).get("screen_name", "")
                created = t.get("created_at", "")
                likes   = t.get("likes", 0)
                views   = t.get("views", 0)
                rts     = t.get("retweets", 0)
                bmarks  = t.get("bookmarks", 0)
                header  = (f"> **{author}** (@{handle})  {created}\n"
                           f"> ❤️ {likes}  👁 {views}  🔁 {rts}  🔖 {bmarks}\n\n---\n\n")
                return header + md
            return md

        if text:
            author  = t.get("author", {}).get("name", "")
            handle  = t.get("author", {}).get("screen_name", "")
            body    = t.get("text", "")
            likes   = t.get("likes", 0)
            views   = t.get("views", 0)
            rts     = t.get("retweets", 0)
            bmarks  = t.get("bookmarks", 0)
            created = t.get("created_at", "")
            lines = [f"**{author}** (@{handle})  {created}", "", body, "",
                     f"❤️ {likes}  👁 {views}  🔁 {rts}  🔖 {bmarks}"]
            media = (t.get("media") or {})
            for item in (media.get("photos") or []) + (media.get("videos") or []):
                src = item.get("url") or item.get("thumbnail_url", "")
                if src:
                    lines.append(f"\n![]({src})")
            quote = t.get("quote")
            if quote:
                lines += ["", "---", "Quoted:", "",
                          f"> **{quote.get('author',{}).get('name','')}**: {quote.get('text','')}"]
            return "\n".join(lines)
        return _json(data)

    # Replies via Camofox + Nitter
    if args.replies:
        if not _camofox_ok(port):
            raise RuntimeError(f"Reply fetching requires Camofox on port {port}.")
        nitter = re.sub(r"https?://(www\.)?(twitter|x)\.com", "https://nitter.net", url)
        snap = _camofox_snapshot(nitter, port, timeout, verbose)
        return snap if text else _json({"type": "replies", "url": url, "snapshot": snap})

    # Fallback: generic web fetch
    log("[twitter] no specific pattern matched, using web fallback", verbose)
    return fetch_web(url, timeout=timeout, verbose=verbose)


# ---------------------------------------------------------------------------
# WeChat fetcher
# ---------------------------------------------------------------------------

_WESPY_DIR  = Path.home() / "Documents" / "QNSZ" / "project" / "WeSpy"
_WESPY_REPO = "https://github.com/tianchangNorth/WeSpy.git"


def _unwrap_captcha_url(url: str) -> str:
    """从微信 captcha 跳转页提取真实文章 URL。
    wappoc_appmsgcaptcha?poc_token=...&target_url=<real_url>
    """
    parsed = urllib.parse.urlparse(url)
    if "wappoc_appmsgcaptcha" in parsed.path:
        params = urllib.parse.parse_qs(parsed.query)
        target = params.get("target_url", [""])[0]
        if target:
            return target
    return url


def _ensure_wespy(verbose: bool) -> Optional[str]:
    """确保 WeSpy 仓库存在，返回目录路径；失败返回 None。"""
    if not _WESPY_DIR.exists():
        log(f"[wespy] 未找到 WeSpy，正在克隆到 {_WESPY_DIR}…", verbose)
        try:
            _WESPY_DIR.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", "clone", _WESPY_REPO, str(_WESPY_DIR)],
                check=True, capture_output=True,
            )
        except Exception as exc:
            log(f"[wespy] 克隆失败: {exc}", verbose)
            return None
    if not (_WESPY_DIR / "wespy" / "main.py").exists():
        log(f"[wespy] 目录结构无效: {_WESPY_DIR}", verbose)
        return None
    return str(_WESPY_DIR)


def _fetch_via_wespy(url: str, verbose: bool = True) -> str:
    """通过 WeSpy（微信移动端 UA）抓取微信公众号文章，返回 Markdown 字符串。"""
    wespy_path = _ensure_wespy(verbose)
    if not wespy_path:
        raise RuntimeError("WeSpy 不可用")

    if wespy_path not in sys.path:
        sys.path.insert(0, wespy_path)

    from wespy.main import ArticleFetcher  # type: ignore
    fetcher = ArticleFetcher()

    log(f"[wespy] 抓取 {url}", verbose)
    # 直接调内部方法，避免写文件
    article_info = fetcher._fetch_wechat_article(
        url, output_dir="/tmp",
        save_html=False, save_json=False, save_markdown=False,
    )
    if not article_info:
        raise RuntimeError("WeSpy 未返回文章数据")

    title      = article_info.get("title", "")
    author     = article_info.get("author", "")
    pub_time   = article_info.get("publish_time", "")
    content_html = article_info.get("content_html", "")

    md_body = fetcher._convert_to_markdown(content_html) if content_html else ""
    log(f"[wespy] ok  {title!r}  ({len(md_body)} chars)", verbose)

    return "\n".join([
        f"# {title}", "",
        f"**作者**: {author}",
        f"**发布时间**: {pub_time}",
        f"**原文链接**: {url}",
        "", "---", "",
        md_body,
    ])


def fetch_wechat(url: str, args: argparse.Namespace) -> str:
    verbose  = args.verbose
    timeout  = args.timeout
    api_base = getattr(args, "wechat_api", None) or os.environ.get("WECHAT_API_URL", "")

    # ① WeSpy — 最优先（微信移动端 UA，成功率最高）
    try:
        return _fetch_via_wespy(url, verbose)
    except Exception as e:
        log(f"[wechat/wespy] 失败: {e}", verbose)

    # ② wechat-article-exporter REST API
    if api_base:
        try:
            endpoint = api_base.rstrip("/") + "/api/article?url=" + urllib.parse.quote(url, safe="")
            log(f"[wechat/exporter] {endpoint}", verbose)
            data = http_json(endpoint, timeout=timeout)
            content = (
                data.get("markdown")
                or data.get("content")
                or data.get("html")
                or json.dumps(data, ensure_ascii=False, indent=2)
            )
            log(f"[wechat/exporter] ok ({len(content)} chars)", verbose)
            return content
        except Exception as e:
            log(f"[wechat/exporter] 失败: {e}", verbose)

    # ③ Jina Reader
    try:
        log("[wechat/Jina] fetching...", verbose)
        c = http_get(f"https://r.jina.ai/{url}", headers={"Accept": "text/markdown"}, timeout=timeout)
        log(f"[wechat/Jina] ok ({len(c)} chars)", verbose)
        return c
    except Exception as e:
        log(f"[wechat/Jina] 失败: {e}", verbose)

    # ④ defuddle.md
    try:
        log("[wechat/defuddle] fetching...", verbose)
        c = http_get(f"https://defuddle.md/{url}", timeout=timeout)
        log(f"[wechat/defuddle] ok ({len(c)} chars)", verbose)
        return c
    except Exception as e:
        log(f"[wechat/defuddle] 失败: {e}", verbose)

    # ⑤ Raw HTML
    log("[wechat/raw] fetching...", verbose)
    return http_get(url, timeout=timeout)


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

def fetch(url: str, args: argparse.Namespace) -> str:
    # 自动解包微信 captcha 跳转 URL
    unwrapped = _unwrap_captcha_url(url)
    if unwrapped != url:
        log(f"[fetch] captcha URL 解包 -> {unwrapped}", args.verbose)
        url = unwrapped

    mode = args.mode if args.mode != "auto" else detect_mode(url)
    log(f"[fetch] mode={mode}  url={url}", args.verbose)

    if mode == "twitter":
        return fetch_twitter(url, args)
    if mode == "wechat":
        return fetch_wechat(url, args)
    return fetch_web(url, timeout=args.timeout,
                     skip_jina=args.no_jina, verbose=args.verbose)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Unified content fetcher: web / X/Twitter / WeChat",
    )
    p.add_argument("url", nargs="?", help="URL to fetch")
    p.add_argument("-o", "--output", help="Save output to file")
    p.add_argument("-m", "--mode",
                   choices=["auto", "web", "twitter", "wechat"], default="auto",
                   help="Force mode (default: auto-detect)")

    # web
    p.add_argument("--no-jina", action="store_true", help="Skip Jina Reader")

    # twitter
    p.add_argument("-r", "--replies", action="store_true",
                   help="Fetch tweet replies (needs Camofox)")
    p.add_argument("--user", metavar="USERNAME", help="Fetch user timeline (needs Camofox)")
    p.add_argument("--limit", type=int, default=50, help="Max tweets for timeline (default 50)")
    p.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    p.add_argument("-t", "--text-only", action="store_true",
                   help="Human-readable output instead of JSON")
    p.add_argument("--port", type=int, default=CAMOFOX_DEFAULT_PORT,
                   help=f"Camofox port (default {CAMOFOX_DEFAULT_PORT})")
    p.add_argument("--lang", choices=["zh", "en"], default="zh")

    # wechat
    p.add_argument("--wechat-api", metavar="URL",
                   help="wechat-article-exporter base URL (or set WECHAT_API_URL env)")

    # common
    p.add_argument("--timeout", type=int, default=30, help="HTTP timeout seconds (default 30)")
    p.add_argument("-v", "--verbose", action="store_true", default=True)
    p.add_argument("-q", "--quiet", action="store_true", help="Suppress progress messages")
    return p


def main() -> None:
    args = build_parser().parse_args()
    if args.quiet:
        args.verbose = False

    url = args.url or (f"https://x.com/{args.user.lstrip('@')}" if args.user else None)
    if not url:
        print("Error: provide a URL or --user USERNAME", file=sys.stderr)
        sys.exit(1)

    try:
        content = fetch(url, args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(content)
        log(f"Saved to {args.output}", args.verbose)
    else:
        print(content)


if __name__ == "__main__":
    main()
