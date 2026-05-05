---
name: macos2linuxapp
description: Convert a macOS Electron app (from .dmg) into a runnable Linux Electron app. Use when the user needs to port a macOS-only Electron desktop application to Linux, build a .deb/.rpm package from a macOS DMG, patch app.asar for Linux window behavior, or fix startup crashes after such conversion (e.g., missing chunks, t.join errors, transparent background flickering, deb dependency issues).
---

# macOS Electron App → Linux Converter

This skill guides the conversion of a macOS Electron app (distributed as `.dmg`) into a native Linux app, including packaging as `.deb`.

## When this skill triggers

- Porting a macOS-only Electron app to Linux
- Building `app.asar` and native modules for Linux from a macOS DMG
- Patching Linux window behavior (icon, menu bar, background color)
- Fixing post-conversion startup crashes (`product-name` missing, `t.join is not a function`, flickering)
- Packaging the result as `.deb`, `.rpm`, or running directly from a folder

## High-level workflow

1. **Check dependencies**: Node.js 20+, npm, python3, modern 7zz (24.09+), curl, unzip, make, g++.
2. **Extract the DMG** → locate `.app` → extract `app.asar` with `npx asar`.
3. **Rebuild native modules** (`better-sqlite3`, `node-pty`, etc.) for the target Linux/Electron version using `@electron/rebuild`.
4. **Remove macOS-only modules** (`sparkle-darwin`, `sparkle.node`).
5. **Patch Linux UI**: use `scripts/patch-linux-window-ui.js`.
   - **Critical**: do not hardcode `t.join`; detect the minified `path` variable name at patch time. See the bundled script for the exact regex.
6. **Repack `app.asar`** with `npx asar pack`.
7. **Download Linux Electron runtime** and assemble the app directory.
8. **Package** (`.deb` via `dpkg-deb`, or other formats).

## Bundled resources

- **scripts/patch-linux-window-ui.js** — fixed Linux window patch script that detects the minified `path` variable dynamically.
- **references/workflow.md** — detailed step-by-step conversion instructions.
- **references/troubleshooting.md** — fixes for common post-conversion errors (`t.join`, missing chunks, deb dependencies, flickering, 7zip failures).

## Quick fix reminders

| Symptom | Typical cause | Fix |
|---------|---------------|-----|
| `Cannot find module './product-name-XXXX.js'` | Broken/incomplete asar | Re-extract from original DMG and repack |
| `t.join is not a function` | Hardcoded `t.join` in patch script against new bundle | Use dynamic `path` var detection (see bundled script) |
| `dpkg: depends on nodejs/npm/p7zip-full` | Build tools listed in `control` `Depends:` | Remove `build-essential`, `nodejs`, `npm`, `p7zip-full`, `python3`, `unzip` from `Depends:` |
| Transparent window flickering on Linux | `backgroundColor: #00000000` | Patch to opaque dark/light colors for Linux |
| 7z cannot open DMG | Old p7zip (16.02) | Use 7zz 24.09+ |
