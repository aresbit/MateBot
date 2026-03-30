# Huawei Migration Priority Pages (Local First)

Use local markdown files first for TypeScript-to-ArkTS migration issues, especially when the spec is not explicit about migration rationale (for example, destructuring assignment usage differences).

Priority order (local files):

1. `references/huawei-migration/01-arkts-migration-background.md`
2. `references/huawei-migration/02-typescript-to-arkts-migration-guide.md`
3. `references/huawei-migration/03-arkts-more-cases.md`

Source URLs:

1. https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-migration-background
2. https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/typescript-to-arkts-migration-guide
3. https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-more-cases

Practical rule:

- For "why ArkTS cannot use <TypeScript feature>" questions, check these 3 local files first.
- Then use `references/chapters/*.md` to anchor the explanation with language-spec context.
- If local cache is stale or insufficient, refresh by `bash scripts/fetch_huawei_migration_refs.sh`.
