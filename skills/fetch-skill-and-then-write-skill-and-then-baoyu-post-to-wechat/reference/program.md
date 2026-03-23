# Program

## Goal

fetch-skill 是一个统一的 URL 内容抓取工具，目标是：
**无论什么 URL，输入进去，输出干净可读的 Markdown。**

## Constraints

- 零依赖核心：单条推文、普通网页的抓取不依赖任何第三方包（仅用 Python stdlib）
- 渐进增强：Camofox 和 wechat-article-exporter 为可选增强，未配置时优雅降级
- stderr/stdout 分离：进度信息到 stderr，内容到 stdout，方便管道和脚本使用
- 不存储凭据：环境变量或命令行参数传入，不写入磁盘

## Core Axes

- **覆盖率**：能处理的 URL 类型越多越好（普通网页 / Twitter / 微信 / ...）
- **质量**：输出的 Markdown 干净、可读，保留原文结构
- **可靠性**：回退链确保高成功率，不因单一服务故障而整体失败

## Signals

- 普通网页抓取成功率 > 95%（四级回退）
- 单条推文抓取无需任何配置即可工作
- 微信文章在无 API 时仍可通过 Jina 获取正文

## Near-Term Priorities

- Priority 1：完善 Camofox 回复/时间线解析（parse_timeline_snapshot）
- Priority 2：微信文章增加 wespy/sogou 搜索联动（批量获取账号文章列表）
- Priority 3：增加 `--batch FILE` 支持，从文件中批量抓取 URL 列表
