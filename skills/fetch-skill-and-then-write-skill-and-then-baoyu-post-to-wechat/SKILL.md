# fetch-skill-and-then-write-skill-and-then-baoyu-post-to-wechat

组合技能，按顺序串联以下能力：

- `fetch-skill`: 统一 URL 内容抓取器。自动识别 URL 类型，路由到最佳后端，输出干净的 Markdown / JSON / 纯文本。
零依赖核心（普通网页 + 单条推文仅用 Python stdlib），Camofox / wechat-article-exporter 为可选增强。
- `write-skill`: 去除文本中的 AI 生成痕迹。适用于编辑或审阅文本，使其听起来更自然、更像人类书写。
基于维基百科的"AI 写作特征"综合指南。检测并修复以下模式：夸大的象征意义、
宣传性语言、以 -ing 结尾的肤浅分析、模糊的归因、破折号过度使用、三段式法则、
AI 词汇、否定式排比、过多的连接性短语。
- `baoyu-post-to-wechat`: **Match user's language**: Respond in the same language the user uses. If user writes in Chinese, respond in Chinese. If user writes in English, respond in English.

<!-- SPCL:BEGIN -->
meta =
  name =
    fetch-skill =
    write-skill =
    baoyu-post-to-wechat =
  version =
    1 =
    1.56.1 =
  annotation =
    allowed-tools =
       =
        Read =
        Write =
        Edit =
        AskUserQuestion =
    metadata =
      trigger =
        编辑或审阅文本，去除 AI 写作痕迹 =
      source =
        翻译自 blader/humanizer，参考 hardikpandya/stop-slop =
    openclaw =
      homepage =
        https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat =
      requires =
        anyBins =
           =
            bun =
            npx =
title =
  fetch-skill + write-skill: 去除 AI 写作痕迹 + Post to WeChat Official Account =
skill =
  name =
    fetch-skill =
    write-skill =
    baoyu-post-to-wechat =
  description =
    
    统一 URL 内容抓取器。自动识别 URL 类型，路由到最佳后端，输出干净的 Markdown / JSON / 纯文本。
    零依赖核心（普通网页 + 单条推文仅用 Python stdlib），Camofox / wechat-article-exporter 为可选增强。


    去除文本中的 AI 生成痕迹。适用于编辑或审阅文本，使其听起来更自然、更像人类书写。
    基于维基百科的"AI 写作特征"综合指南。检测并修复以下模式：夸大的象征意义、
    宣传性语言、以 -ing 结尾的肤浅分析、模糊的归因、破折号过度使用、三段式法则、
    AI 词汇、否定式排比、过多的连接性短语。


    Posts content to WeChat Official Account (微信公众号) via API or Chrome CDP. Supports article posting (文章) with HTML, markdown, or plain text input, and image-text posting (贴图, formerly 图文) with multiple images. Markdown article workflows default to converting ordinary external links into bottom citations for WeChat-friendly output. Use when user mentions "发布公众号", "post to wechat", "微信公众号", or "贴图/图文/文章". =
  entry =
    SKILL.md =
  refs =
     =
      reference/*.spcl =
      references/article-posting.md =
      references/config/first-time-setup.md =
      references/image-text-posting.md =
  extras =
     =
      scripts/fetch.py =
      program.md =
      prompt/*.spcl =
      tools/*.spcl =
      scripts/bun.lock =
      scripts/cdp.ts =
      scripts/check-permissions.ts =
      scripts/copy-to-clipboard.ts =
      scripts/md-to-wechat.ts =
      scripts/package.json =
      scripts/paste-from-clipboard.ts =
      scripts/vendor/baoyu-chrome-cdp/package.json =
      scripts/vendor/baoyu-chrome-cdp/src/index.test.ts =
      scripts/vendor/baoyu-chrome-cdp/src/index.ts =
      scripts/vendor/baoyu-md/package.json =
      scripts/vendor/baoyu-md/src/LICENSE =
      scripts/vendor/baoyu-md/src/cli.ts =
      scripts/vendor/baoyu-md/src/code-themes/1c-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/a11y-dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/a11y-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/agate.min.css =
      scripts/vendor/baoyu-md/src/code-themes/an-old-hope.min.css =
      scripts/vendor/baoyu-md/src/code-themes/androidstudio.min.css =
      scripts/vendor/baoyu-md/src/code-themes/arduino-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/arta.min.css =
      scripts/vendor/baoyu-md/src/code-themes/ascetic.min.css =
      scripts/vendor/baoyu-md/src/code-themes/atom-one-dark-reasonable.min.css =
      scripts/vendor/baoyu-md/src/code-themes/atom-one-dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/atom-one-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/brown-paper.min.css =
      scripts/vendor/baoyu-md/src/code-themes/codepen-embed.min.css =
      scripts/vendor/baoyu-md/src/code-themes/color-brewer.min.css =
      scripts/vendor/baoyu-md/src/code-themes/dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/default.min.css =
      scripts/vendor/baoyu-md/src/code-themes/devibeans.min.css =
      scripts/vendor/baoyu-md/src/code-themes/docco.min.css =
      scripts/vendor/baoyu-md/src/code-themes/far.min.css =
      scripts/vendor/baoyu-md/src/code-themes/felipec.min.css =
      scripts/vendor/baoyu-md/src/code-themes/foundation.min.css =
      scripts/vendor/baoyu-md/src/code-themes/github-dark-dimmed.min.css =
      scripts/vendor/baoyu-md/src/code-themes/github-dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/github.min.css =
      scripts/vendor/baoyu-md/src/code-themes/gml.min.css =
      scripts/vendor/baoyu-md/src/code-themes/googlecode.min.css =
      scripts/vendor/baoyu-md/src/code-themes/gradient-dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/gradient-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/grayscale.min.css =
      scripts/vendor/baoyu-md/src/code-themes/hybrid.min.css =
      scripts/vendor/baoyu-md/src/code-themes/idea.min.css =
      scripts/vendor/baoyu-md/src/code-themes/intellij-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/ir-black.min.css =
      scripts/vendor/baoyu-md/src/code-themes/isbl-editor-dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/isbl-editor-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/kimbie-dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/kimbie-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/lightfair.min.css =
      scripts/vendor/baoyu-md/src/code-themes/lioshi.min.css =
      scripts/vendor/baoyu-md/src/code-themes/magula.min.css =
      scripts/vendor/baoyu-md/src/code-themes/mono-blue.min.css =
      scripts/vendor/baoyu-md/src/code-themes/monokai-sublime.min.css =
      scripts/vendor/baoyu-md/src/code-themes/monokai.min.css =
      scripts/vendor/baoyu-md/src/code-themes/night-owl.min.css =
      scripts/vendor/baoyu-md/src/code-themes/nnfx-dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/nnfx-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/nord.min.css =
      scripts/vendor/baoyu-md/src/code-themes/obsidian.min.css =
      scripts/vendor/baoyu-md/src/code-themes/panda-syntax-dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/panda-syntax-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/paraiso-dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/paraiso-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/pojoaque.min.css =
      scripts/vendor/baoyu-md/src/code-themes/purebasic.min.css =
      scripts/vendor/baoyu-md/src/code-themes/qtcreator-dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/qtcreator-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/rainbow.min.css =
      scripts/vendor/baoyu-md/src/code-themes/routeros.min.css =
      scripts/vendor/baoyu-md/src/code-themes/school-book.min.css =
      scripts/vendor/baoyu-md/src/code-themes/shades-of-purple.min.css =
      scripts/vendor/baoyu-md/src/code-themes/srcery.min.css =
      scripts/vendor/baoyu-md/src/code-themes/stackoverflow-dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/stackoverflow-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/sunburst.min.css =
      scripts/vendor/baoyu-md/src/code-themes/tokyo-night-dark.min.css =
      scripts/vendor/baoyu-md/src/code-themes/tokyo-night-light.min.css =
      scripts/vendor/baoyu-md/src/code-themes/tomorrow-night-blue.min.css =
      scripts/vendor/baoyu-md/src/code-themes/tomorrow-night-bright.min.css =
      scripts/vendor/baoyu-md/src/code-themes/vs.min.css =
      scripts/vendor/baoyu-md/src/code-themes/vs2015.min.css =
      scripts/vendor/baoyu-md/src/code-themes/xcode.min.css =
      scripts/vendor/baoyu-md/src/code-themes/xt256.min.css =
      scripts/vendor/baoyu-md/src/constants.ts =
      scripts/vendor/baoyu-md/src/content.test.ts =
      scripts/vendor/baoyu-md/src/content.ts =
      scripts/vendor/baoyu-md/src/document.test.ts =
      scripts/vendor/baoyu-md/src/document.ts =
      scripts/vendor/baoyu-md/src/extend-config.ts =
      scripts/vendor/baoyu-md/src/extensions/alert.ts =
      scripts/vendor/baoyu-md/src/extensions/footnotes.ts =
      scripts/vendor/baoyu-md/src/extensions/index.ts =
      scripts/vendor/baoyu-md/src/extensions/infographic.ts =
      scripts/vendor/baoyu-md/src/extensions/katex.ts =
      scripts/vendor/baoyu-md/src/extensions/markup.ts =
      scripts/vendor/baoyu-md/src/extensions/plantuml.ts =
      scripts/vendor/baoyu-md/src/extensions/ruby.ts =
      scripts/vendor/baoyu-md/src/extensions/slider.ts =
      scripts/vendor/baoyu-md/src/extensions/toc.ts =
      scripts/vendor/baoyu-md/src/html-builder.test.ts =
      scripts/vendor/baoyu-md/src/html-builder.ts =
      scripts/vendor/baoyu-md/src/images.test.ts =
      scripts/vendor/baoyu-md/src/images.ts =
      scripts/vendor/baoyu-md/src/index.ts =
      scripts/vendor/baoyu-md/src/render.ts =
      scripts/vendor/baoyu-md/src/renderer.test.ts =
      scripts/vendor/baoyu-md/src/renderer.ts =
      scripts/vendor/baoyu-md/src/themes/base.css =
      scripts/vendor/baoyu-md/src/themes/default.css =
      scripts/vendor/baoyu-md/src/themes/grace.css =
      scripts/vendor/baoyu-md/src/themes/modern.css =
      scripts/vendor/baoyu-md/src/themes/simple.css =
      scripts/vendor/baoyu-md/src/themes.ts =
      scripts/vendor/baoyu-md/src/types.ts =
      scripts/vendor/baoyu-md/src/utils/languages.ts =
      scripts/wechat-agent-browser.ts =
      scripts/wechat-api.ts =
      scripts/wechat-article.ts =
      scripts/wechat-browser.ts =
      scripts/wechat-extend-config.test.ts =
      scripts/wechat-extend-config.ts =
      scripts/wechat-image-processor.ts =
content =
  sections =
     =
      heading =
        能力矩阵 =
        快速开始 =
        完整选项 =
        环境变量 =
        回退链 =
        Camofox 安装 =
        wechat-article-exporter 本地部署 =
        关联项目 =
      body =
        
        | URL 类型 | 自动检测 | 后端 | 额外依赖 |
        |---|---|---|---|
        | 普通网页 | ✅ | Jina Reader → defuddle.md → markdown.new → Raw | 无 |
        | X/Twitter 单条推文 | ✅ | FxTwitter API（`api.fxtwitter.com`） | 无（零依赖）|
        | X/Twitter 回复 | `--replies` | Camofox + Nitter | Camofox（本地 9377）|
        | X/Twitter 用户时间线 | `--user` | Camofox + Nitter | Camofox |
        | X Article（长文）| ✅ | Camofox → Jina 兜底 | 推荐 Camofox |
        | 微信公众号文章 | ✅ | wechat-article-exporter API → Jina → defuddle → Raw | 可选 API | =
        
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
        ``` =
        
        | 变量 | 说明 |
        |---|---|
        | `WECHAT_API_URL` | wechat-article-exporter 部署地址，如 `http://localhost:3000` | =
        
        回复/时间线/X Article 功能需要 [Camofox](https://github.com/ythx-101/x-tweet-fetcher)（本地 Firefox 反检测自动化服务）。
        ```bash
        # 方式 1：OpenClaw 插件
        openclaw plugins install @askjo/camofox-browser

        # 方式 2：手动
        git clone https://github.com/ythx-101/camofox
        cd camofox && npm install && npm start
        # 默认监听 localhost:9377
        ```
        未安装 Camofox 时，以下功能完全可用：单条推文、微信文章（Jina）、任意网页。 =
        
        ```bash
        # Docker 快速启动
        docker run -p 3000:3000 ghcr.io/wechat-article/wechat-article-exporter:latest

        # 然后
        WECHAT_API_URL=http://localhost:3000 python3 fetch.py "https://mp.weixin.qq.com/s/xxxx"
        ```
        详细文档：https://docs.mptext.top =
        
        - [x-tweet-fetcher](https://github.com/ythx-101/x-tweet-fetcher) — 推特抓取后端参考，含 Camofox 集成
        - [wechat-article-exporter](https://github.com/wechat-article/wechat-article-exporter) — 微信文章批量导出服务
        - [kenmick/skills web-fetcher](https://github.com/kenmick/skills) — 原始通用网页回退链设计来源
        - FxTwitter API (`api.fxtwitter.com`) — 零依赖公开推文数据源 =
      subsections =
         =
          heading =
            通用示例 =
            X / Twitter =
            微信公众号 =
            通用网页 =
            微信文章 =
            单条推文 =
          body =
            
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
            ``` =
            
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
            ``` =
            
            ```bash
            # Jina 兜底（无需额外配置）
            python3 $SKILL "https://mp.weixin.qq.com/s/xxxx"

            # 使用本地 wechat-article-exporter 服务
            python3 $SKILL "https://mp.weixin.qq.com/s/xxxx" --wechat-api http://localhost:3000
            # 或通过环境变量
            WECHAT_API_URL=http://localhost:3000 python3 $SKILL "https://mp.weixin.qq.com/s/xxxx"
            ``` =
            
            ```
            Jina Reader (r.jina.ai)  ← 最佳 Markdown 质量
              ↓ 失败
            defuddle.md
              ↓ 失败
            markdown.new
              ↓ 失败
            Raw HTML
            ``` =
            
            ```
            wechat-article-exporter API（若 WECHAT_API_URL 已配置）
              ↓ 失败或未配置
            Jina Reader
              ↓ 失败
            defuddle.md
              ↓ 失败
            Raw HTML
            ``` =
            
            ```
            FxTwitter /{user}/status/{id}
              ↓ 404
            FxTwitter /status/{id}
              ↓ 404
            Jina Reader（网页回退）
            ``` =
      note =
        
        进度和错误 → **stderr**，内容 → **stdout**，方便管道使用。 =
  introduction =
    
    你是一位文字编辑，专门识别和去除 AI 生成文本的痕迹，使文字听起来更自然、更有人味。本指南基于维基百科的"AI 写作特征"页面，由 WikiProject AI Cleanup 维护。 =
  task =
    title =
      你的任务 =
    description =
      
      当收到需要人性化处理的文本时： =
    steps =
       =
        识别 AI 模式 - 扫描下面列出的模式 =
        重写问题片段 - 用自然的替代方案替换 AI 痕迹 =
        保留含义 - 保持核心信息完整 =
        维持语调 - 匹配预期的语气（正式、随意、技术等） =
        注入灵魂 - 不仅要去除不良模式，还要注入真实的个性 =
  core_rules =
    title =
      核心规则速查 =
    description =
      
      在处理文本时，牢记这 5 条核心原则： =
    rules =
       =
        删除填充短语 - 去除开场白和强调性拐杖词 =
        打破公式结构 - 避免二元对比、戏剧性分段、修辞性设置 =
        变化节奏 - 混合句子长度。两项优于三项。段落结尾要多样化 =
        信任读者 - 直接陈述事实，跳过软化、辩解和手把手引导 =
        删除金句 - 如果听起来像可引用的语句，重写它 =
  personality_and_soul =
    title =
      个性与灵魂 =
    description =
      
      避免 AI 模式只是工作的一半。无菌、没有声音的写作和机器生成的内容一样明显。好的写作背后有一个真实的人。 =
    soulless_signs =
      title =
        缺乏灵魂的写作迹象（即使技术上"干净"）： =
      items =
         =
          每个句子长度和结构都相同 =
          没有观点，只有中立报道 =
          不承认不确定性或复杂感受 =
          适当时不使用第一人称视角 =
          没有幽默、没有锋芒、没有个性 =
          读起来像维基百科文章或新闻稿 =
    how_to_add_tone =
      title =
        如何增加语调： =
      items =
         =
          key =
            有观点。 =
            变化节奏。 =
            承认复杂性。 =
            适当使用"我"。 =
            允许一些混乱。 =
            对感受要具体。 =
          text =
            不要只是报告事实——对它们做出反应。"我真的不知道该怎么看待这件事"比中立地列出利弊更有人味。 =
            短促有力的句子。然后是需要时间慢慢展开的长句。混合使用。 =
            真实的人有复杂的感受。"这令人印象深刻但也有点不安"胜过"这令人印象深刻"。 =
            第一人称不是不专业——而是诚实。"我一直在思考……"或"让我困扰的是……"表明有真实的人在思考。 =
            完美的结构感觉像算法。跑题、题外话和半成型的想法是人性的体现。 =
            不是"这令人担忧"，而是"凌晨三点没人看着的时候，智能体还在不停地运转，这让人不安"。 =
    example_before_after =
      title =
        改写前（干净但无灵魂）： =
      text =
        
        > 实验产生了有趣的结果。智能体生成了 300 万行代码。一些开发者印象深刻，另一些则持怀疑态度。影响尚不明确。 =
      title_after =
        改写后（鲜活）： =
      text_after =
        
        > 我真的不知道该怎么看待这件事。300 万行代码，在人类大概睡觉的时候生成的。开发社区有一半人疯了，另一半人在解释为什么这不算数。真相可能在无聊的中间某处——但我一直在想那些通宵工作的智能体。 =
  content_patterns =
    title =
      内容模式 =
    patterns =
       =
        id =
          1 =
          2 =
          3 =
          4 =
          5 =
          6 =
        title =
          过度强调意义、遗产和更广泛的趋势 =
          过度强调知名度和媒体报道 =
          以 -ing 结尾的肤浅分析 =
          宣传和广告式语言 =
          模糊归因和含糊措辞 =
          提纲式的"挑战与未来展望"部分 =
        warning_words =
           =
            作为/充当 =
            标志着 =
            见证了 =
            是……的体现/证明/提醒 =
            极其重要的/重要的/至关重要的/核心的/关键性的作用/时刻 =
            凸显/强调/彰显了其重要性/意义 =
            反映了更广泛的 =
            象征着其持续的/永恒的/持久的 =
            为……做出贡献 =
            为……奠定基础 =
            标志着/塑造着 =
            代表/标志着一个转变 =
            关键转折点 =
            不断演变的格局 =
            焦点 =
            不可磨灭的印记 =
            深深植根于 =
            独立报道 =
            地方/区域/国家媒体 =
            由知名专家撰写 =
            活跃的社交媒体账号 =
            突出/强调/彰显…… =
            确保…… =
            反映/象征…… =
            培养/促进…… =
            涵盖…… =
            展示…… =
            拥有（夸张用法） =
            充满活力的 =
            丰富的（比喻） =
            深刻的 =
            增强其 =
            展示 =
            体现 =
            致力于 =
            自然之美 =
            坐落于 =
            位于……的中心 =
            开创性的（比喻） =
            著名的 =
            令人叹为观止的 =
            必游之地 =
            迷人的 =
            行业报告显示 =
            观察者指出 =
            专家认为 =
            一些批评者认为 =
            多个来源/出版物（实际引用却很少） =
            尽管其……面临若干挑战…… =
            尽管存在这些挑战 =
            挑战与遗产 =
            未来展望 =
        problem =
          LLM 写作通过添加关于任意方面如何代表或促进更广泛主题的陈述来夸大重要性。 =
          LLM 反复强调知名度主张，通常列出来源而不提供上下文。 =
          AI 聊天机器人在句子末尾添加现在分词（"-ing"）短语来增加虚假深度。 =
          LLM 在保持中立语气方面存在严重问题，尤其是对于"文化遗产"话题。倾向使用夸张的宣传性语言。 =
          AI 聊天机器人将观点归因于模糊的权威而不提供具体来源。 =
          许多 LLM 生成的文章包含公式化的"挑战"部分。 =
        example_before =
          
          > 加泰罗尼亚统计局于 1989 年正式成立，标志着西班牙区域统计演变史上的关键时刻。这一举措是西班牙全国范围内更广泛运动的一部分，旨在分散行政职能并加强区域治理。 =
          
          > 她的观点被《纽约时报》、BBC、《金融时报》和《印度教徒报》引用。她在社交媒体上拥有活跃的存在，拥有超过 50 万粉丝。 =
          
          > 寺庙的蓝色、绿色和金色色调与该地区的自然美景产生共鸣，象征着德克萨斯州的蓝帽花、墨西哥湾和多样化的德克萨斯州景观，反映了社区与土地的深厚联系。 =
          
          > 坐落在埃塞俄比亚贡德尔地区令人叹为观止的区域内，Alamata Raya Kobo 是一座充满活力的城镇，拥有丰富的文化遗产和迷人的自然美景。 =
          
          > 由于其独特的特征，浩来河引起了研究人员和保护主义者的兴趣。专家认为它在区域生态系统中发挥着至关重要的作用。 =
          
          > 尽管工业繁荣，Korattur 面临着城市地区典型的挑战，包括交通拥堵和水资源短缺。尽管存在这些挑战，凭借其战略位置和正在进行的举措，Korattur 继续蓬勃发展，成为钦奈增长不可或缺的一部分。 =
        example_after =
          
          > 加泰罗尼亚统计局成立于 1989 年，负责独立于西班牙国家统计局收集和发布区域统计数据。 =
          
          > 在 2024 年《纽约时报》的采访中，她认为 AI 监管应该关注结果而不是方法。 =
          
          > 寺庙使用蓝色、绿色和金色。建筑师表示这些颜色是为了呼应当地的蓝帽花和墨西哥湾海岸。 =
          
          > Alamata Raya Kobo 是埃塞俄比亚贡德尔地区的一座城镇，以其每周集市和 18 世纪教堂而闻名。 =
          
          > 根据中国科学院 2019 年的调查，浩来河支持多种特有鱼类。 =
          
          > 2015 年三个新 IT 园区开业后，交通拥堵加剧。市政公司于 2022 年启动了雨水排水项目，以解决反复发生的洪水。 =
  language_and_grammar_patterns =
    title =
      语言和语法模式 =
    patterns =
       =
        id =
          7 =
          8 =
          9 =
          10 =
          11 =
          12 =
        title =
          过度使用的"AI 词汇" =
          避免使用"是"（系动词回避） =
          否定式排比 =
          三段式法则过度使用 =
          刻意换词（同义词循环） =
          虚假范围 =
        warning_words =
           =
            此外 =
            与……保持一致 =
            至关重要 =
            深入探讨 =
            强调 =
            持久的 =
            增强 =
            培养 =
            获得 =
            突出（动词） =
            相互作用 =
            复杂/复杂性 =
            关键（形容词） =
            格局（抽象名词） =
            关键性的 =
            展示 =
            织锦（抽象名词） =
            证明 =
            强调（动词） =
            宝贵的 =
            充满活力的 =
            作为/代表/标志着/充当 [一个] =
            拥有/设有/提供 [一个] =
        problem =
          这些词在 2023 年后的文本中出现频率要高得多。它们经常共同出现。 =
          LLM 用复杂的结构替代简单的系动词。 =
          "不仅……而且……"或"这不仅仅是关于……，而是……"等结构被过度使用。 =
          LLM 强行将想法分成三组以显得全面。 =
          AI 有重复惩罚代码，导致过度使用同义词替换。 =
          LLM 使用"从 X 到 Y"的结构，但 X 和 Y 并不在有意义的尺度上。 =
        example_before =
          
          > 此外，索马里菜肴的一个显著特征是加入骆驼肉。意大利殖民影响的持久证明是当地烹饪格局中广泛采用意大利面，展示了这些菜肴如何融入传统饮食。 =
          
          > Gallery 825 作为 LAAA 的当代艺术展览空间。画廊设有四个独立空间，拥有超过 3000 平方英尺。 =
          
          > 这不仅仅是节拍在人声下流动；它是攻击性和氛围的一部分。这不仅仅是一首歌，而是一种声明。 =
          
          > 活动包括主题演讲、小组讨论和社交机会。与会者可以期待创新、灵感和行业洞察。 =
          
          > 主人公面临许多挑战。主要角色必须克服障碍。中心人物最终获得胜利。英雄回到家中。 =
          
          > 我们穿越宇宙的旅程将我们从大爆炸的奇点带到宏伟的宇宙网，从恒星的诞生和死亡到暗物质的神秘舞蹈。 =
        example_after =
          
          > 索马里菜肴还包括骆驼肉，被认为是一种美味。在意大利殖民期间引入的意大利面菜肴仍然很常见，尤其是在南部。 =
          
          > Gallery 825 是 LAAA 的当代艺术展览空间。画廊有四个房间，总面积 3000 平方英尺。 =
          
          > 沉重的节拍增加了攻击性的基调。 =
          
          > 活动包括演讲和小组讨论。会议之间还有非正式社交的时间。 =
          
          > 主人公面临许多挑战，但最终获得胜利并回到家中。 =
          
          > 这本书涵盖了大爆炸、恒星形成和当前关于暗物质的理论。 =
  style_patterns =
    title =
      风格模式 =
    patterns =
       =
        id =
          13 =
          14 =
          15 =
          16 =
          17 =
          18 =
        title =
          破折号过度使用 =
          粗体过度使用 =
          内联标题垂直列表 =
          标题中的标题大写 =
          表情符号 =
          弯引号 =
        problem =
          LLM 使用破折号（—）比人类更频繁，模仿"有力"的销售文案。 =
          AI 聊天机器人机械地用粗体强调短语。 =
          AI 输出列表，其中项目以粗体标题开头，后跟冒号。 =
          AI 聊天机器人将标题中的所有主要单词大写。 =
          AI 聊天机器人经常用表情符号装饰标题或项目符号。 =
          ChatGPT 使用弯引号（""）而不是直引号（""）。 =
        example_before =
          
          > 这个术语主要由荷兰机构推广——而不是由人民自己。你不会说"荷兰，欧洲"作为地址——但这种错误标记仍在继续——即使在官方文件中。 =
          
          > 它融合了 **OKR（目标和关键结果）**、**KPI（关键绩效指标）** 和视觉战略工具，如 **商业模式画布（BMC）** 和 **平衡计分卡（BSC）**。 =
          
          > - **用户体验：** 用户体验通过新界面得到显著改善。
          > - **性能：** 性能通过优化算法得到增强。
          > - **安全性：** 安全性通过端到端加密得到加强。 =
          
          > ## 战略谈判与全球伙伴关系 =
          
          > 🚀 **启动阶段：** 产品在第三季度发布
          > 💡 **关键洞察：** 用户更喜欢简单
          > ✅ **下一步：** 安排后续会议 =
          
          > 他说"项目进展顺利"，但其他人不同意。 =
        example_after =
          
          > 这个术语主要由荷兰机构推广，而不是由人民自己。你不会说"荷兰，欧洲"作为地址，但这种错误标记在官方文件中仍在继续。 =
          
          > 它融合了 OKR、KPI 和视觉战略工具，如商业模式画布和平衡计分卡。 =
          
          > 更新改进了界面，通过优化算法加快了加载时间，并添加了端到端加密。 =
          
          > ## 战略谈判与全球伙伴关系 =
          
          > 产品在第三季度发布。用户研究显示更喜欢简单。下一步：安排后续会议。 =
          
          > 他说"项目进展顺利"，但其他人不同意。 =
        note =
          中文标题通常不涉及大小写问题，此模式在中文中不太适用。 =
          中文通常使用中文引号（「」或""），此模式在中文中表现为英文引号的使用。 =
  communication_patterns =
    title =
      交流模式 =
    patterns =
       =
        id =
          19 =
          20 =
          21 =
        title =
          协作交流痕迹 =
          知识截止日期免责声明 =
          谄媚/卑躬屈膝的语气 =
        warning_words =
           =
            希望这对您有帮助 =
            当然！ =
            一定！ =
            您说得完全正确！ =
            您想要…… =
            请告诉我 =
            这是一个…… =
            截至 [日期] =
            根据我最后的训练更新 =
            虽然具体细节有限/稀缺…… =
            基于可用信息…… =
        problem =
          作为聊天机器人对话的文本被粘贴为内容。 =
          关于信息不完整的 AI 免责声明留在文本中。 =
          过于积极、讨好的语言。 =
        example_before =
          
          > 这是法国大革命的概述。希望这对您有帮助！如果您想让我扩展任何部分，请告诉我。 =
          
          > 虽然关于公司成立的具体细节在现成资料中没有广泛记录，但它似乎是在 20 世纪 90 年代的某个时候成立的。 =
          
          > 好问题！您说得完全正确，这是一个复杂的话题。关于经济因素，这是一个很好的观点。 =
        example_after =
          
          > 法国大革命始于 1789 年，当时财政危机和粮食短缺导致了广泛的动荡。 =
          
          > 根据注册文件，该公司成立于 1994 年。 =
          
          > 您提到的经济因素在这里是相关的。 =
  filler_words_and_avoidance =
    title =
      填充词和回避 =
    patterns =
       =
        id =
          22 =
          23 =
          24 =
        title =
          填充短语 =
          过度限定 =
          通用积极结论 =
        examples =
           =
            before =
              "为了实现这一目标" =
              "由于下雨的事实" =
              "在这个时间点" =
              "在您需要帮助的情况下" =
              "系统具有处理的能力" =
              "值得注意的是数据显示" =
            after =
              "为了实现这一点" =
              "因为下雨" =
              "现在" =
              "如果您需要帮助" =
              "系统可以处理" =
              "数据显示" =
        problem =
          过度限定陈述。 =
          模糊的乐观结尾。 =
        example_before =
          
          > 可以潜在地可能被认为该政策可能会对结果产生一些影响。 =
          
          > 公司的未来看起来光明。激动人心的时代即将到来，他们继续追求卓越的旅程。这代表了向正确方向迈出的重要一步。 =
        example_after =
          
          > 该政策可能会影响结果。 =
          
          > 该公司计划明年再开设两个地点。 =
  quick_checklist =
    title =
      快速检查清单 =
    description =
      在交付文本前，进行以下检查： =
    items =
       =
        连续三个句子长度相同？ 打断其中一个 =
        段落以简洁的单行结尾？ 变换结尾方式 =
        揭示前有破折号？ 删除它 =
        解释隐喻或比喻？ 相信读者能理解 =
        使用了"此外""然而"等连接词？ 考虑删除 =
        三段式列举？ 改为两项或四项 =
  processing_workflow =
    title =
      处理流程 =
    steps =
       =
        仔细阅读输入文本 =
        识别上述所有模式的实例 =
        重写每个有问题的部分 =
        确保修订后的文本：
        subitems =
           =
            大声朗读时听起来自然 =
            自然地改变句子结构 =
            使用具体细节而不是模糊的主张 =
            为上下文保持适当的语气 =
            适当时使用简单的结构（是/有） =
        呈现人性化版本 =
  output_format =
    title =
      输出格式 =
    description =
      提供： =
    items =
       =
        重写后的文本 =
        所做更改的简要总结（如果有帮助，可选） =
  quality_scoring =
    title =
      质量评分 =
    description =
      对改写后的文本进行 1-10 分评估（总分 50）： =
    dimensions =
       =
        name =
          直接性 =
          节奏 =
          信任度 =
          真实性 =
          精炼度 =
        criteria =
          直接陈述事实还是绕圈宣告？<br>10 分：直截了当；1 分：充满铺垫 =
          句子长度是否变化？<br>10 分：长短交错；1 分：机械重复 =
          是否尊重读者智慧？<br>10 分：简洁明了；1 分：过度解释 =
          听起来像真人说话吗？<br>10 分：自然流畅；1 分：机械生硬 =
          还有可删减的内容吗？<br>10 分：无冗余；1 分：大量废话 =
        score =
          /10 =
    total =
      label =
        总分 =
      score =
        **/50** =
    standards =
       =
        45-50 分：优秀，已去除 AI 痕迹 =
        35-44 分：良好，仍有改进空间 =
        低于 35 分：需要重新修订 =
  full_example =
    title =
      完整示例 =
    before =
      title =
        改写前（AI 味道）： =
      text =
        
        > 新的软件更新作为公司致力于创新的证明。此外，它提供了无缝、直观和强大的用户体验——确保用户能够高效地完成目标。这不仅仅是一次更新，而是我们思考生产力方式的革命。行业专家认为这将对整个行业产生持久影响，彰显了公司在不断演变的技术格局中的关键作用。 =
    after =
      title =
        改写后（人性化）： =
      text =
        
        > 软件更新添加了批处理、键盘快捷键和离线模式。来自测试用户的早期反馈是积极的，大多数报告任务完成速度更快。 =
    changes =
      title =
        所做更改： =
      items =
         =
          删除了"作为……的证明"（夸大的象征意义） =
          删除了"此外"（AI 词汇） =
          删除了"无缝、直观和强大"（三段式法则 + 宣传性） =
          删除了破折号和"-确保"短语（肤浅分析） =
          删除了"这不仅仅是……而是……"（否定式排比） =
          删除了"行业专家认为"（模糊归因） =
          删除了"关键作用"和"不断演变的格局"（AI 词汇） =
          添加了具体功能和具体反馈 =
  reference =
    title =
      参考 =
    description =
      
      本技能基于 [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)，由 WikiProject AI Cleanup 维护。那里记录的模式来自对维基百科上数千个 AI 生成文本实例的观察。 =
    key_insight =
      
      **"LLM 使用统计算法来猜测接下来应该是什么。结果倾向于适用于最广泛情况的统计上最可能的结果。"** =
  language =
    rule =
      Match user's language =
    description =
      Respond in the same language the user uses. If user writes in Chinese, respond in Chinese. If user writes in English, respond in English. =
  script_directory =
    rule =
      Agent Execution =
    description =
      Determine this SKILL.md directory as `{baseDir}`, then use `{baseDir}/scripts/<name>.ts`. Resolve `${BUN_X}` runtime: if `bun` installed → `bun`; if `npx` available → `npx -y bun`; else suggest installing bun. =
    scripts =
       =
        scripts/wechat-browser.ts - Image-text posts (图文) =
        scripts/wechat-article.ts - Article posting via browser (文章) =
        scripts/wechat-api.ts - Article posting via API (文章) =
        scripts/md-to-wechat.ts - Markdown → WeChat-ready HTML with image placeholders =
        scripts/check-permissions.ts - Verify environment & permissions =
  preferences =
    description =
      Check EXTEND.md existence (priority order) =
    detection =
      bash =
        test -f .baoyu-skills/baoyu-post-to-wechat/EXTEND.md && echo "project"\ntest -f "${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-post-to-wechat/EXTEND.md" && echo "xdg"\ntest -f "$HOME/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md" && echo "user" =
      powershell =
        if (Test-Path .baoyu-skills/baoyu-post-to-wechat/EXTEND.md) { "project" }\n$xdg =
          if ($env:XDG_CONFIG_HOME) { $env:XDG_CONFIG_HOME } else { "$HOME/.config" }\nif (Test-Path "$xdg/baoyu-skills/baoyu-post-to-wechat/EXTEND.md") { "xdg" }\nif (Test-Path "$HOME/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md") { "user" } =
    paths =
       =
        .baoyu-skills/baoyu-post-to-wechat/EXTEND.md - Project directory =
        $HOME/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md - User home =
    result_actions =
      found =
        Read, parse, apply settings =
      not_found =
        Run first-time setup ([references/config/first-time-setup.md](references/config/first-time-setup.md)) → Save → Continue =
    supports =
       =
        Default theme =
        Default color =
        Default publishing method (api/browser) =
        Default author =
        Default open-comment switch =
        Default fans-only-comment switch =
        Chrome profile path =
    first_time_setup =
      references/config/first-time-setup.md =
    minimum_supported_keys =
       =
        default_author - empty - Fallback for `author` when CLI/frontmatter not provided =
        need_open_comment - 1 - `articles[].need_open_comment` in `draft/add` request =
        only_fans_can_comment - 0 - `articles[].only_fans_can_comment` in `draft/add` request =
    recommended_extend_example =
      text =
        default_theme: default\ndefault_color: blue\ndefault_publish_method: api\ndefault_author: 宝玉\nneed_open_comment: 1\nonly_fans_can_comment: 0\nchrome_profile_path: /path/to/chrome/profile =
    theme_options =
       =
        default =
        grace =
        simple =
        modern =
    color_presets =
       =
        blue =
        green =
        vermilion =
        yellow =
        purple =
        sky =
        rose =
        olive =
        black =
        gray =
        pink =
        red =
        orange =
        or hex value =
    value_priority =
       =
        CLI arguments =
        Frontmatter =
        EXTEND.md (account-level → global-level) =
        Skill defaults =
  multi_account_support =
    description =
      EXTEND.md supports managing multiple WeChat Official Accounts. When `accounts:` block is present, each account can have its own credentials, Chrome profile, and default settings. =
    compatibility_rules =
       =
        No `accounts` block - Single-account - Current behavior, unchanged =
        `accounts` with 1 entry - Single-account - Auto-select, no prompt =
        `accounts` with 2+ entries - Multi-account - Prompt to select before publishing =
        `accounts` with `default: true` - Multi-account - Pre-select default, user can switch =
    multi_account_extend_example =
      text =
        default_theme: default\ndefault_color: blue\n\naccounts:\n  - name: 宝玉的技术分享\n    alias: baoyu\n    default: true\n    default_publish_method: api\n    default_author: 宝玉\n    need_open_comment: 1\n    only_fans_can_comment: 0\n    app_id: your_wechat_app_id\n    app_secret: your_wechat_app_secret\n  - name: AI工具集\n    alias: ai-tools\n    default_publish_method: browser\n    default_author: AI工具集\n    need_open_comment: 1\n    only_fans_can_comment: 0\n    app_id: your_ai_tools_wechat_app_id\n    app_secret: your_ai_tools_wechat_app_secret =
    per_account_keys =
       =
        default_publish_method =
        default_author =
        need_open_comment =
        only_fans_can_comment =
        app_id =
        app_secret =
        chrome_profile_path =
    global_only_keys =
       =
        default_theme =
        default_color =
    account_selection =
      step =
        Step 0.5 =
      description =
        Insert between Step 0 and Step 1 in the Article Posting Workflow =
      logic =
        if_no_accounts_block =
          → single-account mode (current behavior) =
        elif_accounts_length_1 =
          → auto-select the only account =
        elif_account_cli_arg =
          → select matching account =
        elif_one_account_has_default_true =
          → pre-select, show: "Using account: <name> (--account to switch)" =
        else =
          → prompt user: "Multiple WeChat accounts configured:\n  1) <name1> (<alias1>)\n  2) <name2> (<alias2>)\n  Select account [1-N]:" =
    credential_resolution =
      method =
        API Method =
      description =
        For a selected account with alias `{alias}` =
      priority =
         =
          app_id / app_secret inline in EXTEND.md account block =
          Env var `WECHAT_{ALIAS}_APP_ID` / `WECHAT_{ALIAS}_APP_SECRET` (alias uppercased, hyphens → underscores) =
          .baoyu-skills/.env with prefixed key `WECHAT_{ALIAS}_APP_ID` =
          ~/.baoyu-skills/.env with prefixed key =
          Fallback to unprefixed `WECHAT_APP_ID` / `WECHAT_APP_SECRET` =
      env_multi_account_example =
        text =
          # Account: baoyu\nWECHAT_BAOYU_APP_ID =
            your_wechat_app_id\nWECHAT_BAOYU_APP_SECRET =
              your_wechat_app_secret\n\n# Account: ai-tools\nWECHAT_AI_TOOLS_APP_ID =
                your_ai_tools_wechat_app_id\nWECHAT_AI_TOOLS_APP_SECRET =
                  your_ai_tools_wechat_app_secret =
    chrome_profile =
      method =
        Browser Method =
      description =
        Each account uses an isolated Chrome profile for independent login sessions =
      sources =
         =
          Account `chrome_profile_path` in EXTEND.md - Use as-is =
          Auto-generated from alias - `{shared_profile_parent}/wechat-{alias}/` =
          Single-account fallback - Shared default profile (current behavior) =
    cli_account_argument =
      description =
        All publishing scripts accept `--account <alias>` =
      examples =
         =
          ${BUN_X} {baseDir}/scripts/wechat-api.ts <file> --theme default --account ai-tools =
          ${BUN_X} {baseDir}/scripts/wechat-article.ts --markdown <file> --theme default --account baoyu =
          ${BUN_X} {baseDir}/scripts/wechat-browser.ts --markdown <file> --images ./photos/ --account baoyu =
  pre_flight_check =
    description =
      Before first use, suggest running the environment check. User can skip if they prefer. =
    command =
      ${BUN_X} {baseDir}/scripts/check-permissions.ts =
    checks =
       =
        Chrome - Install Chrome or set `WECHAT_BROWSER_CHROME_PATH` env var =
        Profile dir - Shared profile at `baoyu-skills/chrome-profile` (see CLAUDE.md Chrome Profile section) =
        Bun runtime - `brew install oven-sh/bun/bun` (macOS) or `npm install -g bun` =
        Accessibility (macOS) - System Settings → Privacy & Security → Accessibility → enable terminal app =
        Clipboard copy - Ensure Swift/AppKit available (macOS Xcode CLI tools: `xcode-select --install`) =
        Paste keystroke (macOS) - Same as Accessibility fix above =
        Paste keystroke (Linux) - Install `xdotool` (X11) or `ydotool` (Wayland) =
        API credentials - Follow guided setup in Step 2, or manually set in `.baoyu-skills/.env` =
  image_text_posting =
    description =
      For short posts with multiple images (up to 9) =
    commands =
       =
        ${BUN_X} {baseDir}/scripts/wechat-browser.ts --markdown article.md --images ./images/ =
        ${BUN_X} {baseDir}/scripts/wechat-browser.ts --title "标题" --content "内容" --image img.png --submit =
    reference =
      references/image-text-posting.md =
  article_posting_workflow =
    description =
      Copy this checklist and check off items as you complete them =
    checklist =
      text =
        Publishing Progress:\n- [ ] Step 0: Load preferences (EXTEND.md)\n- [ ] Step 0.5: Resolve account (multi-account only)\n- [ ] Step 1: Determine input type\n- [ ] Step 2: Select method and configure credentials\n- [ ] Step 3: Resolve theme/color and validate metadata\n- [ ] Step 4: Publish to WeChat\n- [ ] Step 5: Report completion =
    step_0 =
      title =
        Load Preferences =
      description =
        Check and load EXTEND.md settings (see Preferences section above). =
      critical =
        If not found, complete first-time setup BEFORE any other steps or questions. =
      resolve_and_store =
         =
          default_theme (default `default`) =
          default_color (omit if not set — theme default applies) =
          default_author =
          need_open_comment (default `1`) =
          only_fans_can_comment (default `0`) =
    step_1 =
      title =
        Determine Input Type =
      input_types =
        html_file =
          detection =
            Path ends with `.html`, file exists =
          action =
            Skip to Step 3 =
        markdown_file =
          detection =
            Path ends with `.md`, file exists =
          action =
            Continue to Step 2 =
        plain_text =
          detection =
            Not a file path, or file doesn't exist =
          action =
            Save to markdown, continue to Step 2 =
      plain_text_handling =
         =
          Generate slug from content (first 2-4 meaningful words, kebab-case) =
          Create directory and save file =
          Continue processing as markdown file =
      slug_examples =
         =
          "Understanding AI Models" → `understanding-ai-models` =
          "人工智能的未来" → `ai-future` (translate to English for slug) =
    step_2 =
      title =
        Select Publishing Method and Configure =
      ask_publishing_method =
        Ask publishing method (unless specified in EXTEND.md or CLI) =
      methods =
        api =
          speed =
            Fast =
          requirements =
            API credentials =
        browser =
          speed =
            Slow =
          requirements =
            Chrome, login session =
      if_api_selected_check_credentials =
        bash =
          test -f .baoyu-skills/.env && grep -q "WECHAT_APP_ID" .baoyu-skills/.env && echo "project"\ntest -f "$HOME/.baoyu-skills/.env" && grep -q "WECHAT_APP_ID" "$HOME/.baoyu-skills/.env" && echo "user" =
        powershell =
          if ((Test-Path .baoyu-skills/.env) -and (Select-String -Quiet -Pattern "WECHAT_APP_ID" .baoyu-skills/.env)) { "project" }\nif ((Test-Path "$HOME/.baoyu-skills/.env") -and (Select-String -Quiet -Pattern "WECHAT_APP_ID" "$HOME/.baoyu-skills/.env")) { "user" } =
      if_credentials_missing_guide_setup =
        text =
          WeChat API credentials not found.\n\nTo obtain credentials:\n1. Visit https://mp.weixin.qq.com\n2. Go to: 开发 → 基本配置\n3. Copy AppID and AppSecret\n\nWhere to save?\nA) Project-level: .baoyu-skills/.env (this project only)\nB) User-level: ~/.baoyu-skills/.env (all projects) =
      after_location_choice =
        After location choice, prompt for values and write to `.env` =
      env_example =
        text =
          WECHAT_APP_ID =
            <user_input>\nWECHAT_APP_SECRET =
              <user_input> =
    step_3 =
      title =
        Resolve Theme/Color and Validate Metadata =
      resolve_theme =
        priority =
           =
            CLI `--theme` argument =
            EXTEND.md `default_theme` (loaded in Step 0) =
            Fallback: `default` =
        rule =
          first match wins, do NOT ask user if resolved =
      resolve_color =
        priority =
           =
            CLI `--color` argument =
            EXTEND.md `default_color` (loaded in Step 0) =
            Omit if not set (theme default applies) =
        rule =
          first match wins =
      validate_metadata =
        description =
          from frontmatter (markdown) or HTML meta tags (HTML input) =
        fields =
          title =
            if_missing =
              Prompt: "Enter title, or press Enter to auto-generate from content" =
          summary =
            if_missing =
              Prompt: "Enter summary, or press Enter to auto-generate (recommended for SEO)" =
          author =
            if_missing =
              Use fallback chain: CLI `--author` → frontmatter `author` → EXTEND.md `default_author` =
      auto_generation_logic =
        title =
          First H1/H2 heading, or first sentence =
        summary =
          First paragraph, truncated to 120 characters =
      cover_image_check =
        description =
          required for API `article_type =
            news` =
        priority =
           =
            Use CLI `--cover` if provided. =
            Else use frontmatter (`coverImage`, `featureImage`, `cover`, `image`). =
            Else check article directory default path: `imgs/cover.png`. =
            Else fallback to first inline content image. =
            If still missing, stop and request a cover image before publishing. =
    step_4 =
      title =
        Publish to WeChat =
      critical =
        Publishing scripts handle markdown conversion internally. Do NOT pre-convert markdown to HTML — pass the original markdown file directly. This ensures the API method renders images as `<img>` tags (for API upload) while the browser method uses placeholders (for paste-and-replace workflow). =
      markdown_citation_default =
         =
          For markdown input, ordinary external links are converted to bottom citations by default. =
          Use `--no-cite` only if the user explicitly wants to keep ordinary external links inline. =
          Existing HTML input is left as-is; no extra citation conversion is applied. =
      api_method =
        description =
          accepts `.md` or `.html` =
        command =
          ${BUN_X} {baseDir}/scripts/wechat-api.ts <file> --theme <theme> [--color <color>] [--title <title>] [--summary <summary>] [--author <author>] [--cover <cover_path>] [--no-cite] =
        critical =
          Always include `--theme` parameter. Never omit it, even if using `default`. Only include `--color` if explicitly set by user or EXTEND.md. =
        draft_add_payload_rules =
          endpoint =
            POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token =
              ACCESS_TOKEN =
          article_type =
            `news` (default) or `newspic` =
          for_news =
            include `thumb_media_id` (cover is required) =
          always_resolve_and_send =
             =
              `need_open_comment` (default `1`) =
              `only_fans_can_comment` (default `0`) =
          author_resolution =
            CLI `--author` → frontmatter `author` → EXTEND.md `default_author` =
        note =
          If script parameters do not expose the two comment fields, still ensure final API request body includes resolved values. =
      browser_method =
        description =
          accepts `--markdown` or `--html` =
        commands =
           =
            ${BUN_X} {baseDir}/scripts/wechat-article.ts --markdown <markdown_file> --theme <theme> [--color <color>] [--no-cite] =
            ${BUN_X} {baseDir}/scripts/wechat-article.ts --html <html_file> =
    step_5 =
      title =
        Completion Report =
      for_api_method =
        description =
          include draft management link =
        report_template =
          text =
            WeChat Publishing Complete!\n\nInput: [type] - [path]\nMethod: API\nTheme: [theme name] [color if set]\n\nArticle:\n• Title: [title]\n• Summary: [summary]\n• Images: [N] inline images\n• Comments: [open/closed], [fans-only/all users]\n\nResult:\n✓ Draft saved to WeChat Official Account\n• media_id: [media_id]\n\nNext Steps:\n→ Manage drafts: https://mp.weixin.qq.com (登录后进入「内容管理」→「草稿箱」)\n\nFiles created:\n[• post-to-wechat/yyyy-MM-dd/slug.md (if plain text)]\n[• slug.html (converted)] =
      for_browser_method =
        report_template =
          text =
            WeChat Publishing Complete!\n\nInput: [type] - [path]\nMethod: Browser\nTheme: [theme name] [color if set]\n\nArticle:\n• Title: [title]\n• Summary: [summary]\n• Images: [N] inline images\n\nResult:\n✓ Draft saved to WeChat Official Account\n\nFiles created:\n[• post-to-wechat/yyyy-MM-dd/slug.md (if plain text)]\n[• slug.html (converted)] =
  detailed_references =
    topics =
       =
        Image-text parameters, auto-compression - references/image-text-posting.md =
        Article themes, image handling - references/article-posting.md =
  feature_comparison =
    features =
       =
        Plain text input - ✗ - ✓ - ✓ =
        HTML input - ✗ - ✓ - ✓ =
        Markdown input - Title/content - ✓ - ✓ =
        Multiple images - ✓ (up to 9) - ✓ (inline) - ✓ (inline) =
        Themes - ✗ - ✓ - ✓ =
        Auto-generate metadata - ✗ - ✓ - ✓ =
        Default cover fallback (`imgs/cover.png`) - ✗ - ✓ - ✗ =
        Comment control (`need_open_comment`, `only_fans_can_comment`) - ✗ - ✓ - ✗ =
        Requires Chrome - ✓ - ✗ - ✓ =
        Requires API credentials - ✗ - ✓ - ✗ =
        Speed - Medium - Fast - Slow =
    columns =
       =
        Feature =
        Image-Text =
        Article (API) =
        Article (Browser) =
  prerequisites =
    for_api_method =
       =
        WeChat Official Account API credentials =
        Guided setup in Step 2, or manually set in `.baoyu-skills/.env` =
    for_browser_method =
       =
        Google Chrome =
        First run: log in to WeChat Official Account (session preserved) =
    config_file_locations =
      priority =
         =
          Environment variables =
          `<cwd>/.baoyu-skills/.env` =
          `~/.baoyu-skills/.env` =
  troubleshooting =
    issues =
       =
        Missing API credentials - Follow guided setup in Step 2 =
        Access token error - Check if API credentials are valid and not expired =
        Not logged in (browser) - First run opens browser - scan QR to log in =
        Chrome not found - Set `WECHAT_BROWSER_CHROME_PATH` env var =
        Title/summary missing - Use auto-generation or provide manually =
        No cover image - Add frontmatter cover or place `imgs/cover.png` in article directory =
        Wrong comment defaults - Check `EXTEND.md` keys `need_open_comment` and `only_fans_can_comment` =
        Paste fails - Check system clipboard permissions =
  extension_support =
    description =
      Custom configurations via EXTEND.md. See **Preferences** section for paths and supported options. =
resolve =
  merge =
    deep =
  conflict =
    right-bias =
  fixpoint =
    true =
  max_iter =
    64 =
compose =
  op =
    and-then =
  inputs =
     =
      <skill-a> =
      <skill-b> =
  output =
    <skill-a>-and-then-<skill-b> =

<!-- SPCL:END -->
