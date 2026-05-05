#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const extractedDir = process.argv[2];

if (!extractedDir) {
  console.error("Usage: patch-linux-window-ui.js <extracted-app-asar-dir>");
  process.exit(1);
}

const assetsDir = path.join(extractedDir, "webview", "assets");
const iconAsset = fs
  .readdirSync(assetsDir)
  .find((name) => /^app-.*\.png$/.test(name));

if (!iconAsset) {
  console.warn(`WARN: Could not find app icon asset in ${assetsDir} — skipping all UI patches`);
  process.exit(0);
}

const buildDir = path.join(extractedDir, ".vite", "build");
const mainBundle = fs
  .readdirSync(buildDir)
  .find((name) => /^main(?:-[^.]+)?\.js$/.test(name));

if (!mainBundle) {
  console.warn(`WARN: Could not find main bundle in ${buildDir} — skipping all UI patches`);
  process.exit(0);
}

const target = path.join(buildDir, mainBundle);
let source = fs.readFileSync(target, "utf8");
const packageJsonPath = path.join(extractedDir, "package.json");
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));

// Detect the actual minified variable name for the path module
const pathVarMatch = source.match(
  /\blet\s+([A-Za-z_$][\w$]*)=require\(`(?:node:)?path`\)/
);
const pathVar = pathVarMatch ? pathVarMatch[1] : null;
const pathJoinExpr = pathVar
  ? `${pathVar}.join`
  : `require(\`node:path\`).join`;

const windowOptionsNeedle =
  "...process.platform===`win32`?{autoHideMenuBar:!0}:{},";
const iconPathNeedle =
  `icon:${pathJoinExpr}(process.resourcesPath,\`..\`,\`content\`,\`webview\`,\`assets\`,\`${iconAsset}\`)`;
const windowOptionsReplacement =
  `...process.platform===\`win32\`||process.platform===\`linux\`?{autoHideMenuBar:!0,...process.platform===\`linux\`?{${iconPathNeedle}}:{}}:{},`;

if (source.includes(windowOptionsNeedle)) {
  source = source.replace(windowOptionsNeedle, windowOptionsReplacement);
} else if (!source.includes(iconPathNeedle)) {
  console.warn("WARN: Could not find BrowserWindow autoHideMenuBar snippet — skipping window options patch");
}

const menuNeedle = "process.platform===`win32`&&D.removeMenu(),";
const menuPatch = "process.platform===`linux`&&D.setMenuBarVisibility(!1),";
const menuReplacement = `${menuPatch}${menuNeedle}`;

if (source.includes(menuNeedle) && !source.includes(menuPatch)) {
  source = source.replace(menuNeedle, menuReplacement);
} else if (!source.includes(menuPatch)) {
  console.warn("WARN: Could not find window menu visibility snippet — skipping menu patch");
}

const setIconNeedle =
  ")}),D.once(`ready-to-show`,()=>{";
const setIconPatch =
  `)}),process.platform===\`linux\`&&D.setIcon(${pathJoinExpr}(process.resourcesPath,\`..\`,\`content\`,\`webview\`,\`assets\`,\`${iconAsset}\`)),D.once(\`ready-to-show\`,()=>{`;

if (source.includes(setIconNeedle) && !source.includes("&&D.setIcon(")) {
  source = source.replace(setIconNeedle, setIconPatch);
} else if (!source.includes("&&D.setIcon(")) {
  console.warn("WARN: Could not find window setIcon insertion point — skipping setIcon patch");
}

// Patch 4: Replace transparent BrowserWindow background with opaque colors on Linux.
// On macOS vibrancy handles transparency; on Linux there is no compositor equivalent,
// so the transparent background causes flickering when the window moves or on hover.
const colorConstRegex = /([A-Za-z_$][\w$]*)=`#00000000`,([A-Za-z_$][\w$]*)=`#000000`,([A-Za-z_$][\w$]*)=`#f9f9f9`/;
const colorMatch = source.match(colorConstRegex);

if (colorMatch) {
  const [, transparentVar, darkVar, lightVar] = colorMatch;

  // Capture the prefersDarkColors parameter name from the background function signature.
  const funcParamRegex = /prefersDarkColors:([A-Za-z_$][\w$]*)\}\)\{return\s*([A-Za-z_$][\w$]*)===`win32`/;
  const funcMatch = source.match(funcParamRegex);

  if (funcMatch) {
    const darkColorsParam = funcMatch[1];

    const bgNeedle =
      `backgroundMaterial:\`mica\`}:{backgroundColor:${transparentVar},backgroundMaterial:null}}`;
    const bgReplacement =
      `backgroundMaterial:\`mica\`}:process.platform===\`linux\`?{backgroundColor:${darkColorsParam}?${darkVar}:${lightVar},backgroundMaterial:null}:{backgroundColor:${transparentVar},backgroundMaterial:null}}`;

    if (source.includes(bgNeedle)) {
      source = source.replace(bgNeedle, bgReplacement);
    } else {
      console.warn("WARN: Could not find BrowserWindow background color needle — skipping background patch");
    }
  } else {
    console.warn("WARN: Could not find prefersDarkColors parameter — skipping background patch");
  }
} else {
  console.warn("WARN: Could not find color constants (#00000000, #000000, #f9f9f9) — skipping background patch");
}

fs.writeFileSync(target, source, "utf8");

if (packageJson.desktopName !== "codex-desktop.desktop") {
  packageJson.desktopName = "codex-desktop.desktop";
  fs.writeFileSync(packageJsonPath, `${JSON.stringify(packageJson, null, 2)}\n`, "utf8");
}

console.log("Patched Linux window icon and menu behavior:", {
  target,
  mainBundle,
  iconAsset,
  desktopName: packageJson.desktopName,
});
