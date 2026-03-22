# fetch-skill

**Name:** `fetch-skill`

**Description:** 统一 URL 内容抓取器。自动识别 URL 类型，路由到最佳后端，输出干净的 Markdown / JSON / 纯文本。
零依赖核心（普通网页 + 单条推文仅用 Python stdlib），Camofox / wechat-article-exporter 为可选增强。

---

## 能力矩阵

| URL 类型 | 自动检测 | 后端 | 额外依赖 |
|---|---|---|---|
| 普通网页 | ✅ | Jina Reader → defuddle.md → markdown.new → Raw | 无 |
| X/Twitter 单条推文 | ✅ | FxTwitter API（`api.fxtwitter.com`） | 无（零依赖）|
| X/Twitter 回复 | `--replies` | Camofox + Nitter | Camofox（本地 9377）|
| X/Twitter 用户时间线 | `--user` | Camofox + Nitter | Camofox |
| X Article（长文）| ✅ | Camofox → Jina 兜底 | 推荐 Camofox |
| 微信公众号文章 | ✅ | wechat-article-exporter API → Jina → defuddle → Raw | 可选 API |

---

## 快速开始

```bash
SKILL=~/yyscode/fetch-skill/scripts/fetch.py

# 抓取任意网页（自动选最佳策略）
python3 $SKILL https://example.com

# 保存到文件
python3 $SKILL https://example.com -o output.md

# 静默抓取（不输出进度）
python3 $SKILL https://example.com -q

# 人类可读的纯文本输出
python3 $SKILL https://example.com -t

# 强制跳过 Jina，直接用 defuddle.md
python3 $SKILL https://example.com --no-jina
```

### X / Twitter

```bash
# 单条推文（无需登录，无需 API Key）
python3 $SKILL https://x.com/OpenAI/status/123456 -t

# 推文 JSON 完整数据
python3 $SKILL https://x.com/OpenAI/status/123456 --pretty

# 推文 + 回复（需要 Camofox）
python3 $SKILL https://x.com/OpenAI/status/123456 --replies -t

# 用户时间线，最多 100 条（需要 Camofox）
python3 $SKILL https://x.com/elonmusk --user elonmusk --limit 100 -t
# 或
python3 $SKILL --user elonmusk --limit 100
```

### 微信公众号

```bash
# Jina 兜底（无需额外配置）
python3 $SKILL "https://mp.weixin.qq.com/s/xxxx"

# 使用本地 wechat-article-exporter 服务
python3 $SKILL "https://mp.weixin.qq.com/s/xxxx" --wechat-api http://localhost:3000
# 或通过环境变量
WECHAT_API_URL=http://localhost:3000 python3 $SKILL "https://mp.weixin.qq.com/s/xxxx"
```

---

## 完整选项

```
python3 fetch.py [url] [选项]

定位参数:
  url                    目标 URL（与 --user 二选一）

通用:
  -o, --output FILE      保存到文件（默认 stdout）
  -m, --mode auto|web|twitter|wechat   强制模式（默认 auto）
  --timeout N            HTTP 超时秒数（默认 30）
  -v, --verbose          显示详细进度（默认开启）
  -q, --quiet            不输出进度

网页:
  --no-jina              跳过 Jina Reader，直接从 defuddle.md 开始

X/Twitter:
  -r, --replies          抓取回复（需 Camofox）
  --user USERNAME        抓取用户时间线（需 Camofox）
  --limit N              时间线最大条数（默认 50）
  --pretty               JSON 缩进输出
  -t, --text-only        人类可读输出（而非 JSON）
  --port PORT            Camofox 端口（默认 9377）
  --lang zh|en           提示语言（默认 zh）

微信:
  --wechat-api URL       wechat-article-exporter API 地址
```

---

## 环境变量

| 变量 | 说明 |
|---|---|
| `WECHAT_API_URL` | wechat-article-exporter 部署地址，如 `http://localhost:3000` |

---

## 回退链

### 通用网页
```
Jina Reader (r.jina.ai)  ← 最佳 Markdown 质量
  ↓ 失败
defuddle.md
  ↓ 失败
markdown.new
  ↓ 失败
Raw HTML
```

### 微信文章
```
wechat-article-exporter API（若 WECHAT_API_URL 已配置）
  ↓ 失败或未配置
Jina Reader
  ↓ 失败
defuddle.md
  ↓ 失败
Raw HTML
```

### 单条推文
```
FxTwitter /{user}/status/{id}
  ↓ 404
FxTwitter /status/{id}
  ↓ 404
Jina Reader（网页回退）
```

进度和错误 → **stderr**，内容 → **stdout**，方便管道使用。

---

## Camofox 安装

回复/时间线/X Article 功能需要 [Camofox](https://github.com/ythx-101/x-tweet-fetcher)（本地 Firefox 反检测自动化服务）。

```bash
# 方式 1：OpenClaw 插件
openclaw plugins install @askjo/camofox-browser

# 方式 2：手动
git clone https://github.com/ythx-101/camofox
cd camofox && npm install && npm start
# 默认监听 localhost:9377
```

未安装 Camofox 时，以下功能完全可用：单条推文、微信文章（Jina）、任意网页。

---

## wechat-article-exporter 本地部署

```bash
# Docker 快速启动
docker run -p 3000:3000 ghcr.io/wechat-article/wechat-article-exporter:latest

# 然后
WECHAT_API_URL=http://localhost:3000 python3 fetch.py "https://mp.weixin.qq.com/s/xxxx"
```

详细文档：https://docs.mptext.top

---

## 关联项目

- [x-tweet-fetcher](https://github.com/ythx-101/x-tweet-fetcher) — 推特抓取后端参考，含 Camofox 集成
- [wechat-article-exporter](https://github.com/wechat-article/wechat-article-exporter) — 微信文章批量导出服务
- [kenmick/skills web-fetcher](https://github.com/kenmick/skills) — 原始通用网页回退链设计来源
- FxTwitter API (`api.fxtwitter.com`) — 零依赖公开推文数据源
