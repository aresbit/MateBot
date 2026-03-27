# Getting Started

## Scope

Use this file for scaffolding, local development, reload workflow, plugin lifecycle, and mobile compatibility.

## Baseline setup

- Use an isolated vault for plugin development; do not develop in a primary vault.
- Place plugin source under `<vault>/.obsidian/plugins/<plugin-id>/`.
- Typical first-run sequence:
  - clone/copy plugin source into `.obsidian/plugins`
  - install dependencies
  - run watch build (`npm run dev`) or production build (`npm run build`)

## Essential lifecycle model

- Extend `Plugin` from `obsidian`.
- Implement `onload()` to register commands, views, events, and settings.
- Implement `onunload()` to release resources not auto-managed by registration helpers.
- Prefer registration helpers like `registerEvent`, `addCommand`, `addSettingTab`, `registerView` to get automatic cleanup behavior.

## Reload and test loop

- After TypeScript/code changes:
  - reload plugin by toggling it in Community plugins, or
  - use Obsidian reload command/hot-reload workflow.
- After `manifest.json` changes:
  - restart Obsidian.

## Development guardrails

- Keep plugin folder name equal to `manifest.id`.
- Rename sample placeholders (`MyPlugin`, `SampleSettingTab`, etc.).
- Avoid noisy console logging in default runtime path.
- Prefer sentence case for commands and settings UI text.

## Mobile compatibility

- Node.js/Electron APIs are desktop-only.
- If used, set `isDesktopOnly` to `true`.
- Use `Platform` checks for platform-specific behavior.
- For mobile debugging:
  - desktop emulation: `this.app.emulateMobile(true/false)`
  - Android: `chrome://inspect`
  - iOS: Web Inspector (iOS 16.4+)

## Source pages

- Plugins/Getting started/Build a plugin
- Plugins/Getting started/Anatomy of a plugin
- Plugins/Getting started/Development workflow
- Plugins/Getting started/Mobile development
- Plugins/Releasing/Plugin guidelines (development-related parts)
