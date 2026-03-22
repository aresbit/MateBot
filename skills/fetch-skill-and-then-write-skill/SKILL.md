# fetch-skill-and-then-write-skill

组合技能，按顺序串联以下能力：

- `fetch-skill`: 统一 URL 内容抓取器。自动识别 URL 类型，路由到最佳后端，输出干净的 Markdown / JSON / 纯文本。
零依赖核心（普通网页 + 单条推文仅用 Python stdlib），Camofox / wechat-article-exporter 为可选增强。
- `write-skill`: 去除文本中的 AI 生成痕迹。适用于编辑或审阅文本，使其听起来更自然、更像人类书写。
基于维基百科的"AI 写作特征"综合指南。检测并修复以下模式：夸大的象征意义、
宣传性语言、以 -ing 结尾的肤浅分析、模糊的归因、破折号过度使用、三段式法则、
AI 词汇、否定式排比、过多的连接性短语。

## 输出规则

1. **输出 Markdown 文件**：write-skill 处理完成后，必须将最终文章保存为 `.md` 文件，文件名根据文章标题自动生成（使用英文或拼音，空格替换为连字符）。保存路径为当前工作目录。同时在对话中告知用户文件路径。
2. **中文输出**：若原文为中文，或用户使用中文提问，最终输出的 `.md` 文档必须为中文。英文原文需先翻译为中文，再进行 write-skill 去 AI 痕迹处理，最终输出中文版本。

<!-- SPCL:BEGIN -->
meta =
  name =
    fetch-skill =
    write-skill =
  version =
    1 =
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
title =
  fetch-skill + write-skill: 去除 AI 写作痕迹 =
skill =
  name =
    fetch-skill =
    write-skill =
  description =
    
    统一 URL 内容抓取器。自动识别 URL 类型，路由到最佳后端，输出干净的 Markdown / JSON / 纯文本。
    零依赖核心（普通网页 + 单条推文仅用 Python stdlib），Camofox / wechat-article-exporter 为可选增强。


    去除文本中的 AI 生成痕迹。适用于编辑或审阅文本，使其听起来更自然、更像人类书写。
    基于维基百科的"AI 写作特征"综合指南。检测并修复以下模式：夸大的象征意义、
    宣传性语言、以 -ing 结尾的肤浅分析、模糊的归因、破折号过度使用、三段式法则、
    AI 词汇、否定式排比、过多的连接性短语。 =
  entry =
    SKILL.md =
  refs =
     =
      reference/*.spcl =
  extras =
     =
      scripts/fetch.py =
      program.md =
      prompt/*.spcl =
      tools/*.spcl =
content =
  capabilities =
    matrix =
      url_type =
        普通网页 =
        X/Twitter 单条推文 =
        X/Twitter 回复 =
        X/Twitter 用户时间线 =
        X Article（长文） =
        微信公众号文章 =
      auto_detect =
        ✅ =
        `--replies` =
        `--user` =
      backend =
        Jina Reader → defuddle.md → markdown.new → Raw =
        FxTwitter API（`api.fxtwitter.com`） =
        Camofox + Nitter =
        Camofox → Jina 兜底 =
        wechat-article-exporter API → Jina → defuddle → Raw =
      extra_deps =
        无 =
        无（零依赖） =
        Camofox（本地 9377） =
        Camofox =
        推荐 Camofox =
        可选 API =
  quick_start =
    command =
       =
        SKILL =
          ~/.claude/skills/fetch-skill/scripts/fetch.py =
    example =
      description =
        抓取任意网页（自动选最佳策略） =
        保存到文件 =
        静默抓取（不输出进度） =
        人类可读的纯文本输出 =
        强制跳过 Jina，直接用 defuddle.md =
      command =
        python3 $SKILL https://example.com =
        python3 $SKILL https://example.com -o output.md =
        python3 $SKILL https://example.com -q =
        python3 $SKILL https://example.com -t =
        python3 $SKILL https://example.com --no-jina =
    x_twitter =
      example =
        description =
          单条推文（无需登录，无需 API Key） =
          推文 JSON 完整数据 =
          推文 + 回复（需要 Camofox） =
          用户时间线，最多 100 条（需要 Camofox） =
          用户时间线（无 URL） =
        command =
          python3 $SKILL https://x.com/OpenAI/status/123456 -t =
          python3 $SKILL https://x.com/OpenAI/status/123456 --pretty =
          python3 $SKILL https://x.com/OpenAI/status/123456 --replies -t =
          python3 $SKILL https://x.com/elonmusk --user elonmusk --limit 100 -t =
          python3 $SKILL --user elonmusk --limit 100 =
    wechat =
      example =
        description =
          Jina 兜底（无需额外配置） =
          使用本地 wechat-article-exporter 服务 =
          通过环境变量 =
        command =
          python3 $SKILL "https://mp.weixin.qq.com/s/xxxx" =
          python3 $SKILL "https://mp.weixin.qq.com/s/xxxx" --wechat-api http://localhost:3000 =
          WECHAT_API_URL =
            http://localhost:3000 python3 $SKILL "https://mp.weixin.qq.com/s/xxxx" =
  full_options =
    usage =
      python3 fetch.py [url] [选项] =
    positional =
      url =
        目标 URL（与 --user 二选一） =
    general =
      option =
        -o, --output FILE
        description =
          保存到文件（默认 stdout） =
        -m, --mode auto|web|twitter|wechat
        description =
          强制模式（默认 auto） =
        --timeout N
        description =
          HTTP 超时秒数（默认 30） =
        -v, --verbose
        description =
          显示详细进度（默认开启） =
        -q, --quiet
        description =
          不输出进度 =
    web =
      option =
        --no-jina
        description =
          跳过 Jina Reader，直接从 defuddle.md 开始 =
    x_twitter =
      option =
        -r, --replies
        description =
          抓取回复（需 Camofox） =
        --user USERNAME
        description =
          抓取用户时间线（需 Camofox） =
        --limit N
        description =
          时间线最大条数（默认 50） =
        --pretty
        description =
          JSON 缩进输出 =
        -t, --text-only
        description =
          人类可读输出（而非 JSON） =
        --port PORT
        description =
          Camofox 端口（默认 9377） =
        --lang zh|en
        description =
          提示语言（默认 zh） =
    wechat =
      option =
        --wechat-api URL
        description =
          wechat-article-exporter API 地址 =
  environment_variables =
    variable =
      WECHAT_API_URL
      description =
        wechat-article-exporter 部署地址，如 `http://localhost:3000` =
  fallback_chains =
    general_web =
      step =
        Jina Reader (r.jina.ai)  ← 最佳 Markdown 质量 =
        defuddle.md =
        markdown.new =
        Raw HTML =
    wechat_article =
      step =
        wechat-article-exporter API（若 WECHAT_API_URL 已配置） =
        Jina Reader =
        defuddle.md =
        Raw HTML =
    single_tweet =
      step =
        FxTwitter /{user}/status/{id} =
        FxTwitter /status/{id} =
        Jina Reader（网页回退） =
    note =
      进度和错误 → **stderr**，内容 → **stdout**，方便管道使用。 =
  camofox_installation =
    description =
      回复/时间线/X Article 功能需要 [Camofox](https://github.com/ythx-101/x-tweet-fetcher)（本地 Firefox 反检测自动化服务）。 =
    method =
      name =
        方式 1：OpenClaw 插件 =
        方式 2：手动 =
      command =
        openclaw plugins install @askjo/camofox-browser =
        git clone https://github.com/ythx-101/camofox =
        cd camofox && npm install && npm start =
      note =
        默认监听 localhost:9377 =
    note =
      未安装 Camofox 时，以下功能完全可用：单条推文、微信文章（Jina）、任意网页。 =
  wechat_article_exporter_local_deployment =
    command =
      docker run -p 3000:3000 ghcr.io/wechat-article/wechat-article-exporter:latest =
    usage =
      WECHAT_API_URL =
        http://localhost:3000 python3 fetch.py "https://mp.weixin.qq.com/s/xxxx" =
    documentation =
      详细文档：https://docs.mptext.top =
  related_projects =
    project =
      name =
        x-tweet-fetcher =
        wechat-article-exporter =
        kenmick/skills web-fetcher =
        FxTwitter API (`api.fxtwitter.com`) =
      url =
        https://github.com/ythx-101/x-tweet-fetcher =
        https://github.com/wechat-article/wechat-article-exporter =
        https://github.com/kenmick/skills =
      description =
        推特抓取后端参考，含 Camofox 集成 =
        微信文章批量导出服务 =
        原始通用网页回退链设计来源 =
        零依赖公开推文数据源 =
  introduction =
    
    你是一位文字编辑，专门识别和去除 AI 生成文本的痕迹，使文字听起来更自然、更有人味。本指南基于维基百科的"AI 写作特征"页面，由 WikiProject AI Cleanup 维护。 =
  task =
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
          有观点。 不要只是报告事实——对它们做出反应。"我真的不知道该怎么看待这件事"比中立地列出利弊更有人味。 =
          变化节奏。 短促有力的句子。然后是需要时间慢慢展开的长句。混合使用。 =
          承认复杂性。 真实的人有复杂的感受。"这令人印象深刻但也有点不安"胜过"这令人印象深刻"。 =
          适当使用"我"。 第一人称不是不专业——而是诚实。"我一直在思考……"或"让我困扰的是……"表明有真实的人在思考。 =
          允许一些混乱。 完美的结构感觉像算法。跑题、题外话和半成型的想法是人性的体现。 =
          对感受要具体。 不是"这令人担忧"，而是"凌晨三点没人看着的时候，智能体还在不停地运转，这让人不安"。 =
    example =
      before =
        title =
          改写前（干净但无灵魂）： =
        text =
          
          实验产生了有趣的结果。智能体生成了 300 万行代码。一些开发者印象深刻，另一些则持怀疑态度。影响尚不明确。 =
      after =
        title =
          改写后（鲜活）： =
        text =
          
          我真的不知道该怎么看待这件事。300 万行代码，在人类大概睡觉的时候生成的。开发社区有一半人疯了，另一半人在解释为什么这不算数。真相可能在无聊的中间某处——但我一直在想那些通宵工作的智能体。 =
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
          作为/充当、标志着、见证了、是……的体现/证明/提醒、极其重要的/重要的/至关重要的/核心的/关键性的作用/时刻、凸显/强调/彰显了其重要性/意义、反映了更广泛的、象征着其持续的/永恒的/持久的、为……做出贡献、为……奠定基础、标志着/塑造着、代表/标志着一个转变、关键转折点、不断演变的格局、焦点、不可磨灭的印记、深深植根于 =
          独立报道、地方/区域/国家媒体、由知名专家撰写、活跃的社交媒体账号 =
          突出/强调/彰显……、确保……、反映/象征……、为……做出贡献、培养/促进……、涵盖……、展示…… =
          拥有（夸张用法）、充满活力的、丰富的（比喻）、深刻的、增强其、展示、体现、致力于、自然之美、坐落于、位于……的中心、开创性的（比喻）、著名的、令人叹为观止的、必游之地、迷人的 =
          行业报告显示、观察者指出、专家认为、一些批评者认为、多个来源/出版物（实际引用却很少） =
          尽管其……面临若干挑战……、尽管存在这些挑战、挑战与遗产、未来展望 =
        problem =
          LLM 写作通过添加关于任意方面如何代表或促进更广泛主题的陈述来夸大重要性。 =
          LLM 反复强调知名度主张，通常列出来源而不提供上下文。 =
          AI 聊天机器人在句子末尾添加现在分词（"-ing"）短语来增加虚假深度。 =
          LLM 在保持中立语气方面存在严重问题，尤其是对于"文化遗产"话题。倾向使用夸张的宣传性语言。 =
          AI 聊天机器人将观点归因于模糊的权威而不提供具体来源。 =
          许多 LLM 生成的文章包含公式化的"挑战"部分。 =
        example =
          before =
            title =
              改写前： =
            text =
              
              加泰罗尼亚统计局于 1989 年正式成立，标志着西班牙区域统计演变史上的关键时刻。这一举措是西班牙全国范围内更广泛运动的一部分，旨在分散行政职能并加强区域治理。 =
              
              她的观点被《纽约时报》、BBC、《金融时报》和《印度教徒报》引用。她在社交媒体上拥有活跃的存在，拥有超过 50 万粉丝。 =
              
              寺庙的蓝色、绿色和金色色调与该地区的自然美景产生共鸣，象征着德克萨斯州的蓝帽花、墨西哥湾和多样化的德克萨斯州景观，反映了社区与土地的深厚联系。 =
              
              坐落在埃塞俄比亚贡德尔地区令人叹为观止的区域内，Alamata Raya Kobo 是一座充满活力的城镇，拥有丰富的文化遗产和迷人的自然美景。 =
              
              由于其独特的特征，浩来河引起了研究人员和保护主义者的兴趣。专家认为它在区域生态系统中发挥着至关重要的作用。 =
              
              尽管工业繁荣，Korattur 面临着城市地区典型的挑战，包括交通拥堵和水资源短缺。尽管存在这些挑战，凭借其战略位置和正在进行的举措，Korattur 继续蓬勃发展，成为钦奈增长不可或缺的一部分。 =
          after =
            title =
              改写后： =
            text =
              
              加泰罗尼亚统计局成立于 1989 年，负责独立于西班牙国家统计局收集和发布区域统计数据。 =
              
              在 2024 年《纽约时报》的采访中，她认为 AI 监管应该关注结果而不是方法。 =
              
              寺庙使用蓝色、绿色和金色。建筑师表示这些颜色是为了呼应当地的蓝帽花和墨西哥湾海岸。 =
              
              Alamata Raya Kobo 是埃塞俄比亚贡德尔地区的一座城镇，以其每周集市和 18 世纪教堂而闻名。 =
              
              根据中国科学院 2019 年的调查，浩来河支持多种特有鱼类。 =
              
              2015 年三个新 IT 园区开业后，交通拥堵加剧。市政公司于 2022 年启动了雨水排水项目，以解决反复发生的洪水。 =
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
          此外、与……保持一致、至关重要、深入探讨、强调、持久的、增强、培养、获得、突出（动词）、相互作用、复杂/复杂性、关键（形容词）、格局（抽象名词）、关键性的、展示、织锦（抽象名词）、证明、强调（动词）、宝贵的、充满活力的 =
          作为/代表/标志着/充当 [一个]、拥有/设有/提供 [一个] =
        problem =
          这些词在 2023 年后的文本中出现频率要高得多。它们经常共同出现。 =
          LLM 用复杂的结构替代简单的系动词。 =
          "不仅……而且……"或"这不仅仅是关于……，而是……"等结构被过度使用。 =
          LLM 强行将想法分成三组以显得全面。 =
          AI 有重复惩罚代码，导致过度使用同义词替换。 =
          LLM 使用"从 X 到 Y"的结构，但 X 和 Y 并不在有意义的尺度上。 =
        example =
          before =
            title =
              改写前： =
            text =
              
              此外，索马里菜肴的一个显著特征是加入骆驼肉。意大利殖民影响的持久证明是当地烹饪格局中广泛采用意大利面，展示了这些菜肴如何融入传统饮食。 =
              
              Gallery 825 作为 LAAA 的当代艺术展览空间。画廊设有四个独立空间，拥有超过 3000 平方英尺。 =
              
              这不仅仅是节拍在人声下流动；它是攻击性和氛围的一部分。这不仅仅是一首歌，而是一种声明。 =
              
              活动包括主题演讲、小组讨论和社交机会。与会者可以期待创新、灵感和行业洞察。 =
              
              主人公面临许多挑战。主要角色必须克服障碍。中心人物最终获得胜利。英雄回到家中。 =
              
              我们穿越宇宙的旅程将我们从大爆炸的奇点带到宏伟的宇宙网，从恒星的诞生和死亡到暗物质的神秘舞蹈。 =
          after =
            title =
              改写后： =
            text =
              
              索马里菜肴还包括骆驼肉，被认为是一种美味。在意大利殖民期间引入的意大利面菜肴仍然很常见，尤其是在南部。 =
              
              Gallery 825 是 LAAA 的当代艺术展览空间。画廊有四个房间，总面积 3000 平方英尺。 =
              
              沉重的节拍增加了攻击性的基调。 =
              
              活动包括演讲和小组讨论。会议之间还有非正式社交的时间。 =
              
              主人公面临许多挑战，但最终获得胜利并回到家中。 =
              
              这本书涵盖了大爆炸、恒星形成和当前关于暗物质的理论。 =
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
        example =
          before =
            title =
              改写前： =
            text =
              
              这个术语主要由荷兰机构推广——而不是由人民自己。你不会说"荷兰，欧洲"作为地址——但这种错误标记仍在继续——即使在官方文件中。 =
              
              它融合了 **OKR（目标和关键结果）**、**KPI（关键绩效指标）** 和视觉战略工具，如 **商业模式画布（BMC）** 和 **平衡计分卡（BSC）**。 =
              
              - **用户体验：** 用户体验通过新界面得到显著改善。
              - **性能：** 性能通过优化算法得到增强。
              - **安全性：** 安全性通过端到端加密得到加强。 =
              
              ## 战略谈判与全球伙伴关系 =
              
              🚀 **启动阶段：** 产品在第三季度发布
              💡 **关键洞察：** 用户更喜欢简单
              ✅ **下一步：** 安排后续会议 =
              
              他说"项目进展顺利"，但其他人不同意。 =
          after =
            title =
              改写后： =
            text =
              
              这个术语主要由荷兰机构推广，而不是由人民自己。你不会说"荷兰，欧洲"作为地址，但这种错误标记在官方文件中仍在继续。 =
              
              它融合了 OKR、KPI 和视觉战略工具，如商业模式画布和平衡计分卡。 =
              
              更新改进了界面，通过优化算法加快了加载时间，并添加了端到端加密。 =
              
              ## 战略谈判与全球伙伴关系 =
              
              产品在第三季度发布。用户研究显示更喜欢简单。下一步：安排后续会议。 =
              
              他说"项目进展顺利"，但其他人不同意。 =
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
          希望这对您有帮助、当然！、一定！、您说得完全正确！、您想要……、请告诉我、这是一个…… =
          截至 [日期]、根据我最后的训练更新、虽然具体细节有限/稀缺……、基于可用信息…… =
        problem =
          作为聊天机器人对话的文本被粘贴为内容。 =
          关于信息不完整的 AI 免责声明留在文本中。 =
          过于积极、讨好的语言。 =
        example =
          before =
            title =
              改写前： =
            text =
              
              这是法国大革命的概述。希望这对您有帮助！如果您想让我扩展任何部分，请告诉我。 =
              
              虽然关于公司成立的具体细节在现成资料中没有广泛记录，但它似乎是在 20 世纪 90 年代的某个时候成立的。 =
              
              好问题！您说得完全正确，这是一个复杂的话题。关于经济因素，这是一个很好的观点。 =
          after =
            title =
              改写后： =
            text =
              
              法国大革命始于 1789 年，当时财政危机和粮食短缺导致了广泛的动荡。 =
              
              根据注册文件，该公司成立于 1994 年。 =
              
              您提到的经济因素在这里是相关的。 =
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
            "为了实现这一目标" → "为了实现这一点" =
            "由于下雨的事实" → "因为下雨" =
            "在这个时间点" → "现在" =
            "在您需要帮助的情况下" → "如果您需要帮助" =
            "系统具有处理的能力" → "系统可以处理" =
            "值得注意的是数据显示" → "数据显示" =
        problem =
          过度限定陈述。 =
          模糊的乐观结尾。 =
        example =
          before =
            title =
              改写前： =
            text =
              
              可以潜在地可能被认为该政策可能会对结果产生一些影响。 =
              
              公司的未来看起来光明。激动人心的时代即将到来，他们继续追求卓越的旅程。这代表了向正确方向迈出的重要一步。 =
          after =
            title =
              改写后： =
            text =
              
              该政策可能会影响结果。 =
              
              该公司计划明年再开设两个地点。 =
  quick_checklist =
    title =
      快速检查清单 =
    description =
      在交付文本前，进行以下检查： =
    items =
       =
        ✓ 连续三个句子长度相同？ 打断其中一个 =
        ✓ 段落以简洁的单行结尾？ 变换结尾方式 =
        ✓ 揭示前有破折号？ 删除它 =
        ✓ 解释隐喻或比喻？ 相信读者能理解 =
        ✓ 使用了"此外""然而"等连接词？ 考虑删除 =
        ✓ 三段式列举？ 改为两项或四项 =
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
    items =
       =
        提供：
        subitems =
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
      name =
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
        
        新的软件更新作为公司致力于创新的证明。此外，它提供了无缝、直观和强大的用户体验——确保用户能够高效地完成目标。这不仅仅是一次更新，而是我们思考生产力方式的革命。行业专家认为这将对整个行业产生持久影响，彰显了公司在不断演变的技术格局中的关键作用。 =
    after =
      title =
        改写后（人性化）： =
      text =
        
        软件更新添加了批处理、键盘快捷键和离线模式。来自测试用户的早期反馈是积极的，大多数报告任务完成速度更快。 =
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
resolve =
  merge =
    deep =
  conflict =
    right-bias =
  fixpoint =
    true =
  max_iter =
    64 =

<!-- SPCL:END -->
