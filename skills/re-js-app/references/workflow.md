# Detailed Workflow

## Prerequisites

- Node.js 18+ with npm
- `7zz` (7-Zip 24.09+) for DMG extraction — old `p7zip` cannot handle APFS DMGs
- Or `pkgutil`/`xar` for .pkg files
- `unzip`, `curl`, `make`, `g++` (optional, for native modules)

## Step-by-Step

### 1. Extract the archive

**DMG:**
```bash
7zz x -y App.dmg
# Output: App.app/
# The .app is a directory. Find the asar:
ls App.app/Contents/Resources/app.asar
```

If `7zz` fails: install from https://7-zip.org/download.html or `apt install 7zip` (24.09+).
Older `p7zip-full` (16.02) cannot read APFS DMGs — upgrade or use a macOS VM.

**AppImage:**
```bash
chmod +x App.AppImage
./App.AppImage --appimage-extract
# Output: squashfs-root/
ls squashfs-root/resources/app.asar
```

**.pkg:**
```bash
# Method 1: pkgutil (macOS only)
pkgutil --expand App.pkg extracted/

# Method 2: xar + cpio (Linux)
xar -xf App.pkg
gunzip -c Payload | cpio -i
# Then search for app.asar inside the extracted .app bundle
```

### 2. Extract app.asar

```bash
npx asar extract app.asar extracted_app

# If the app uses native modules (.node), keep them unpacked:
npx asar extract app.asar extracted_app --unpack '*.node'
```

### 3. Map the bundle structure

```bash
# Identify main process entry
ls extracted_app/out/main/
# Common: index.js, preload.js

# Identify renderer
ls extracted_app/out/client/
# Common: _app/ (SvelteKit), assets/, index.html

# Check dependencies for framework clues
cat extracted_app/package.json | jq '.dependencies'
```

### 4. Classify each file

| Pattern | Type | Action |
|---------|------|--------|
| Large single file (200KB+, webpack bootstrap at top) | webpack bundle | Full deobfuscation pipeline |
| `__vite__mapDeps` at top | Vite/SvelteKit | webcrack only, skip chunk import rename |
| `< 50KB, `contextBridge` | preload script | Light deobfuscation |
| Binary `.node` | Native addon | Skip |

### 5. Run the deobfuscation pipeline

For each bundle file:

```bash
# Step A: webcrack
webcrack bundle.js -o wc_output/

# Step B: scope-aware rename
node scripts/deobfuscate.js wc_output/deobfuscated.js bundle.deobf.js

# Step C (optional): local variable rename
node scripts/rename-locals.js bundle.deobf.js bundle.final.js
```

### 6. Read and analyze

Key things to find in main process:
- `ipcMain.handle(...)` — IPC API endpoints
- `new BrowserWindow(...)` — Window creation config
- `Menu.buildFromTemplate(...)` — Menu structure
- `shell.openExternal(...)` — External URL handling
- `better-sqlite3` — Database schema and queries

In renderer:
- API call patterns (fetch, WebSocket)
- UI component tree (Svelte/React component names often preserved)
- Event handlers

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| webcrack hangs on huge file (>5MB) | Too many AST nodes | Split into chunks or increase Node.js memory: `NODE_OPTIONS="--max-old-space-size=8192"` |
| `Duplicate declaration` error | Import alias collision | deobfuscate.js v2+ handles this via `getBinding()` check |
| Chunk imports still meaningless (`_A`, `_B`) | Vite exports single-letter names | Expected for Vite bundles. Skip chunk import renaming (importedName.length ≤ 2) |
| `scope.rename()` throws | Name conflict in scope | Caught by try/catch, rename skipped |
| Output file won't re-parse | Duplicate declarations in generated code | Run deobfuscate.js >= v2.1 which checks for conflicts before renaming |

## Output Conventions

After full pipeline, code uses these conventions:

- `_BrowserWindow`, `_ipcMain` — Import aliases restored from minified `n`, `d`
- `module_`, `exports_`, `require_` — Webpack factory parameters
- `Object_create`, `Object_defineProperty` — Utility wrappers
- `propNames`, `keys`, `descriptor` — Variables inferred from `Object.*` assignments
- `filePath`, `str`, `arr`, `idx`, `cb`, `err` — Heuristically named locals
