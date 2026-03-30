---
name: hm-fetch-skill
description: Fetch Huawei HarmonyOS developer document正文 by calling documentPortal getDocumentById API with slug objectId, convert HTML content to Markdown, and maintain local-first migration references. Use when scraping Huawei HarmonyOS docs that are SPA-rendered and not directly readable by generic web fetchers.
---

# HM Fetch Skill

Fetch HarmonyOS docs through API first, then fallback to generic fetch.

## API-First Rule

Use API route first for正文:

- Endpoint: `https://svc-drcn.developer.huawei.com/community/servlet/consumer/cn/documentPortal/getDocumentById`
- Request body: `{"objectId":"<slug>","language":"cn"}`
- Important: `objectId` is the document slug, not `docId`.

## Scripts

- Single page by slug:
  - `python3 scripts/fetch_huawei_doc_api.py --slug typescript-to-arkts-migration-guide --out /tmp/doc.md`
- Preset migration pages:
  - `python3 scripts/fetch_huawei_doc_api.py --preset migration --out-dir references/huawei-migration`
- One-shot refresh (API first, fallback to fetch-skill):
  - `bash scripts/fetch_huawei_migration_refs.sh`

## Local-First Workflow

1. Refresh local cache by `bash scripts/fetch_huawei_migration_refs.sh`.
2. Answer questions from `references/huawei-migration/*.md`.
3. Only if local cache is insufficient, refetch specific slug by API script.

## Outputs

- `references/huawei-migration/01-arkts-migration-background.md`
- `references/huawei-migration/02-typescript-to-arkts-migration-guide.md`
- `references/huawei-migration/03-arkts-more-cases.md`
