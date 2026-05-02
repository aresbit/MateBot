---
name: re-js-app
description: Reverse engineer and deobfuscate bundled JavaScript/Electron applications. Extracts DMG/AppImage/pkg archives, unpacks app.asar, deobfuscates webpack/Vite/browserify bundles with scope-aware Babel-based variable renaming, and outputs readable source code. Use when the user wants to reverse engineer, deobfuscate, unminify, or analyze a bundled JS application (Electron, web app, Node.js), extract readable source from minified bundles, unpack app.asar, or understand how a third-party JS app works internally.
---

# JS App Reverse Engineer

Deobfuscate bundled JavaScript applications: extract archives, unpack asar, deobfuscate webpack/Vite bundles with scope-aware renaming.

## Pipeline

```
Archive (.dmg/.AppImage/.pkg) → 7z extraction → .app → npx asar extract → JS
  → webcrack (unpack + format) → deobfuscate.js (scope rename) → readable source
```

## Phase 1: Extract

### DMG (macOS)

```bash
7zz x -y App.dmg          # Use 7zz 24.09+, not old p7zip
# Find: App.app/Contents/Resources/app.asar
```

### AppImage (Linux)

```bash
./App.AppImage --appimage-extract
# Find: squashfs-root/resources/app.asar
```

### pkg (macOS flat package)

```bash
pkgutil --expand App.pkg extracted_pkg/
# Or: xar -xf App.pkg && gunzip -c Payload | cpio -i
```

### Extract asar

```bash
npx asar extract app.asar extracted_app
# For native modules, keep them unpacked:
npx asar extract app.asar extracted_app --unpack '*.node'
```

**Common output structure:**
```
extracted_app/
├── out/              # Bundled JS (main/ + client/)
├── node_modules/     # Server-side node_modules (framework clues)
├── package.json      # Dependencies, Electron version
└── resources/        # Icons, assets
```

## Phase 2: Identify Bundle Type

Look at the JS output to determine the bundler:

| Pattern | Bundler | Strategy |
|---------|---------|----------|
| `__webpack_require__`, `webpackChunk` | webpack | Full webcrack pass |
| `__vite__mapDeps`, `_app/immutable/chunks/` | Vite/SvelteKit | webcrack format, skip chunk rename |
| `__esModule`, `Object.defineProperty(exports` | TypeScript/esbuild | webcrack + deobfuscate |
| `require("./chunk-")`, `__browserify_` | browserify | webcrack unpack |

## Phase 3: webcrack

```bash
npm install -g webcrack
webcrack input.js -o output_dir/
```

webcrack handles: webpack unpacking, JSX transpilation, string array deobfuscation, control flow unminify, formatting. Output file: `output_dir/deobfuscated.js`.

## Phase 4: Scope-Aware Rename (deobfuscate.js)

```bash
cd <skill-dir>
npm install @babel/parser @babel/traverse @babel/generator @babel/types
node scripts/deobfuscate.js <webcrack_output.js> [output.js]
```

This script performs three scope-aware passes:

1. **Import alias rename**: `import { BrowserWindow as n }` → `_BrowserWindow`. Only triggers when imported name is meaningful (>2 chars) and local name is short (<4 chars). Uses Babel `scope.rename()` to avoid cross-scope conflicts.

2. **Webpack factory param rename**: `(e, t) => { t.exports = ... }` → `(module_, exports_)`. Detects factory pattern by checking for `exports` property assignment and `require("literal")` calls. Only applies within the factory function scope.

3. **Utility pattern rename**: `var se = Object.create` → `var Object_create = Object.create`. Renames at program scope.

## Phase 5: Statistical Local Variable Rename (rename-locals.js)

```bash
node scripts/rename-locals.js <deobfuscated.js> [output.js]
```

Heuristic-based local variable renaming using context analysis:

- **Type detection**: `.push()`/`.forEach()` → array, `.replace()` → string, `.then()` → Promise
- **Role detection**: `new X()` → constructor, `X++` → counter/index, `typeof X=="function"` → callback
- **Assignment source**: `X = require("y")` → module, `X = path.join()` → filePath, `X = Object.keys()` → propNames
- **Param position**: `(err, result)` callback convention, `(req, res)` pattern
- **Scope neighbor context**: If nearby binding is "callback", this one is likely also a callback

## Key Files to Target

| File | Size | Content |
|------|------|---------|
| `main/index.js` | 200-500KB | Main process: IPC handlers, window management, tray, menus |
| `client/*.js` or `_app/` | 1-10MB | Renderer/UI bundle (SvelteKit/React/Vue) |
| `preload.js` | 1-50KB | Preload script: contextBridge API exposure |
| `*.node` | Binary | Native addons (skip, not JS) |

## Reading the Output

**Import lines = API surface:**
```js
import { BrowserWindow as _BrowserWindow, ipcMain as _ipcMain } from "electron";
```

**Webpack module boundaries:**
```js
var SomeModule = wrapper((module_, exports_) => {
  exports_.exports = { someExport };
});
```

**IPC handlers = main↔renderer communication:**
```js
_ipcMain.handle("channel-name", (event, input) => { ... });
```

**Naming convention:**
- `_Xxx` — Import alias, restored from original name
- `module_`/`exports_`/`require_` — Webpack factory params
- Short names remaining after Phase 4 — Application-level locals (need Phase 5 or manual reading)

## Resources

- `scripts/deobfuscate.js` — Scope-aware variable renamer (Phase 4 runner)
- `scripts/rename-locals.js` — Statistical local variable renamer (Phase 5 runner)
- `references/api-patterns.md` — Electron/Node.js API method catalog for heuristic matching
- `references/workflow.md` — Detailed step-by-step workflow with troubleshooting
