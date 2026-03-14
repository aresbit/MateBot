---
name: lecture-skill
description: Use skill-seekers to build a unified lecture skill from local PDFs, package for Claude, and troubleshoot common config/CLI errors.
---

# Lecture Skill

Create a reusable skill from many lecture PDFs with `skill-seekers unified`.

## When To Use

Use this skill when you need to:
- Build one merged skill from many lecture PDFs.
- Avoid `create --target` errors in modern `skill-seekers`.
- Write or fix a unified `config.json`.
- Package and install the final skill for Claude.

## Quick Workflow

1. Prepare config from template:
- See [references/config.unified.template.json](references/config.unified.template.json)

2. Run unified build:
```bash
skill-seekers unified --config arch-config.json
```

3. Package for Claude:
```bash
skill-seekers package output/<skill-name> --target claude
```

4. Install to Claude:
```bash
skill-seekers install-agent output/<skill-name> --agent claude
```

## Important Rules

- `--target` belongs to `package`, not `create`.
- For folders of PDFs, prefer `unified` config with `sources` array.
- Unified build now cleans per-lecture intermediates by default.
- If you want to keep intermediates:
```bash
skill-seekers unified --config arch-config.json --keep-pdf-intermediates
```

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for common failures and fixes.
