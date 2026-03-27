# Manifest And API

## Manifest quick schema

Required common fields:

- `author: string`
- `minAppVersion: string`
- `name: string`
- `version: string` in semver `x.y.z`

Required plugin-specific fields:

- `description: string`
- `id: string` (must not contain `obsidian`)
- `isDesktopOnly: boolean`

Optional fields frequently used:

- `authorUrl: string`
- `fundingUrl: string | object`

## Manifest constraints and checks

- Keep `id` unique and stable.
- Keep plugin directory name identical to `id` during local dev.
- Use a realistic `minAppVersion` that matches actual API usage.
- Keep `description` concise and plain; avoid keyword stuffing and decorative characters.

## API usage defaults

- Use `this.app` from plugin instance, not global `app`.
- Prefer high-level APIs:
  - active editor updates: Editor API
  - background file edits: `Vault.process`
  - frontmatter updates: `FileManager.processFrontMatter`
- For workspace access, prefer `getActiveViewOfType()` and optional chaining on `activeEditor`.

## Command and view patterns

- Command callbacks:
  - `callback` for unconditional commands
  - `checkCallback` for conditional commands
  - `editorCallback` / `editorCheckCallback` for editor-dependent commands
- Do not set default hotkeys unless explicitly required by product design.
- Avoid storing long-lived direct references to custom views unless required.

## Security defaults

- Avoid `innerHTML`, `outerHTML`, `insertAdjacentHTML` with user input.
- Construct DOM with safe APIs (`createEl`, `createDiv`, `createSpan`, standard DOM APIs).

## Source pages

- Reference/Manifest
- Reference/TypeScript API/Plugin
- Reference/TypeScript API/PluginManifest
- Reference/TypeScript API/index
- Plugins/Releasing/Plugin guidelines
