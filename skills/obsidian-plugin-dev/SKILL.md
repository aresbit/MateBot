---
name: obsidian-plugin-dev
description: Build and maintain Obsidian community plugins end-to-end using official docs. Use when tasks involve Obsidian plugin scaffolding, TypeScript implementation, `manifest.json`, desktop/mobile compatibility, debugging/reload workflow, release automation, or submission/review in the Obsidian community plugins registry.
---

# Obsidian Plugin Dev

## Overview

Use this skill to deliver Obsidian plugin work from first scaffold to community submission, with defaults aligned to Obsidian official documentation.

## Workflow

1. Confirm the task type.
2. Collect the minimum required project context.
3. Execute the matching implementation path.
4. Run build and verification steps.
5. If needed, package and submit release artifacts.

### 1) Confirm the task type

Classify the request first and follow only the relevant path:

- New plugin scaffold or first-time setup: use `references/getting-started.md`.
- Feature development or bug fixing in an existing plugin: use `references/getting-started.md` and `references/manifest-and-api.md`.
- Release, submission, or review comment handling: use `references/release-and-review.md`.

### 2) Collect minimum context

Before editing code, gather these facts:

- Vault path and plugin path: `<vault>/.obsidian/plugins/<plugin-id>/`.
- Whether `manifest.json` exists and whether folder name matches `manifest.id`.
- Build tooling (`package.json` scripts, `tsconfig.json`, bundler config).
- Target platforms: desktop only or desktop + mobile.
- Current release status: unpublished, submitted, or already listed.

If the request lacks these details, infer from repository files first instead of asking immediately.

### 3) Implement by path

For new or early-stage plugins:

- Start from the official sample plugin pattern.
- Keep `onload()` for setup and `onunload()` for cleanup.
- Add commands/ribbon/settings with APIs that auto-clean on unload.
- Keep class names and identifiers project-specific; remove sample placeholders.

For active development and debugging:

- Use incremental build (`npm run dev`) when available.
- Reload plugin after code changes (toggle plugin or use reload command).
- Restart Obsidian after `manifest.json` changes.
- Prefer Editor/Vault high-level APIs over low-level adapter operations.

For compatibility and safety:

- Set `isDesktopOnly: true` when using Node.js/Electron APIs.
- Avoid global `app` usage; use `this.app` from plugin instance.
- Avoid `innerHTML`/`outerHTML`/`insertAdjacentHTML` for user-controlled input.
- Prefer atomic file updates (`Vault.process`, `FileManager.processFrontMatter`) where applicable.

### 4) Validate before finishing

Run the smallest useful verification set:

- Build check: compile without errors.
- Runtime check: plugin loads and unloads cleanly.
- UX check: commands/settings text follows sentence case and concise naming.
- Manifest check: required fields present and semver format is `x.y.z`.
- Mobile check (if supported): avoid Node/Electron APIs and test platform guards.

### 5) Release and submission path

When user asks to publish or prepare listing:

- Ensure release assets include `main.js`, `manifest.json`, and optional `styles.css`.
- Ensure tag matches `manifest.version`.
- Verify repository metadata for submission JSON (`id`, `name`, `author`, `description`, `repo`).
- Follow review workflow on existing PR; do not open a replacement PR for fixes.

Use `references/release-and-review.md` for exact submission and review expectations.

## References

- Development basics and lifecycle: `references/getting-started.md`
- Manifest fields and API entry points: `references/manifest-and-api.md`
- Release, submission, and review checklist: `references/release-and-review.md`

Load only the reference file required by the current task.

## Source scope

This skill is based on `https://docs.obsidian.md/Home` and linked plugin-development pages under `Plugins/*` and `Reference/*`.
