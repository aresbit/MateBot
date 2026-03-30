---
name: arkts-skill
description: ArkTS language specification guidance for syntax, types, semantics, and diagnostics based on ArkTS Specification 1.2.0. Use when handling ArkTS grammar questions, compiler/type errors, feature compliance checks, TypeScript-to-ArkTS adaptation, or HarmonyOS ArkTS code modernization.
---

# ArkTS Skill

Use this skill to answer ArkTS language and type-system questions with spec-backed guidance.

## Workflow

1. Read the user problem and classify it as one of: syntax, type system, declarations, expressions/statements, classes/interfaces, or migration/compatibility.
2. If the question is TypeScript-to-ArkTS migration related (especially "why not supported", including destructuring-assignment concerns), read `references/huawei-migration-priority.md` first.
3. For migration questions, use local files in `references/huawei-migration/*.md` first (local-first).
4. If local migration files are stale or insufficient, refresh them via `bash scripts/fetch_huawei_migration_refs.sh`.
5. Search chapter files, then open only the matched files.
6. Cite the exact section/topic names in your answer.
7. Prefer minimal, directly compilable ArkTS examples.
8. Keep recommendations simple and deterministic. If multiple options exist, present the simplest compliant one first.

## Fast Search Patterns

Use targeted search on the chapter directory:

- `bash scripts/search_chapters.sh "union|narrow|keyof"`
- `rg -n "type|union|interface|class|function|async|decorator|generic" references/chapters`
- `rg -n "assignment|narrow|overload|extends|implements|readonly|tuple|array|literal" references/chapters`
- `rg -n "error|diagnostic|restriction|forbidden|not allowed|shall|must" references/chapters`

## Maintenance

- Rebuild chapter split from full OCR markdown:
  - `python3 scripts/rebuild_chapters.py`
- Refresh migration local references:
  - `bash scripts/fetch_huawei_migration_refs.sh`
- Keep `references/CHAPTER_INDEX.md` in sync with chapter files after rebuild.

## Output Rules

- Prefer short explanations with one concrete fix.
- For compiler/type errors, include:
  - Root cause in one sentence.
  - Smallest valid code change.
  - Why this matches spec behavior.
- For migration questions, produce a before/after snippet and list breaking points.

## Reference

- Full OCR markdown: `arktsspecification_ocr_full.md`
- Chapter index: `references/CHAPTER_INDEX.md`
- OCR chapter files: `references/chapters/*.md`
- Migration-first references: `references/huawei-migration-priority.md`
- Migration local files: `references/huawei-migration/*.md`
