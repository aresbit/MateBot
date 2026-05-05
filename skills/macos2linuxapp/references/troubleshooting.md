# macOS → Linux Electron App 常见问题修复

## 1. `Cannot find module './product-name-XXXX.js'`

**现象**：直接运行时报错找不到 `product-name-XXXXX.js`。

**原因**：`app.asar` 中缺失 Vite 产物 chunk，说明原 `asar` 是损坏或不完整打包的。

**修复**：
- 重新从官方 DMG 提取 `app.asar`，确保打包时产物完整。
- 不要手动删除 `.vite/build/` 下的任何文件。

---

## 2. `t.join is not a function`

**现象**：应用启动后立刻崩溃，弹出 JS 错误对话框。

**原因**：`patch-linux-window-ui.js` 在修改 `BrowserWindow` 选项时，硬编码使用了 `t.join(...)`。但在新版 Vite/Rollup 压缩后的 bundle 中，`t` 不代表 `path` 模块，导致 `join` 方法不存在。

**修复**：在 patch 脚本中**动态检测** `path` 模块的压缩变量名：

```js
const pathVarMatch = source.match(
  /\blet\s+([A-Za-z_$][\w$]*)=require\(`(?:node:)?path`\)/
);
const pathVar = pathVarMatch ? pathVarMatch[1] : null;
const pathJoinExpr = pathVar
  ? `${pathVar}.join`
  : `require(\`node:path\`).join`;
```

然后使用 `pathJoinExpr` 拼接图标路径：

```js
const iconPathNeedle =
  `icon:${pathJoinExpr}(process.resourcesPath,\`..\`,\`content\`,\`webview\`,\`assets\`,\`${iconAsset}\`)`;
```

---

## 3. `dpkg` 安装时报缺少 `nodejs`、`npm`、`p7zip-full`

**现象**：`sudo dpkg -i codex-desktop_*.deb` 提示依赖未满足。

**原因**：`packaging/linux/control` 的 `Depends:` 把这些**构建/更新**时才需要的工具列为了**运行时依赖**。普通用户只需要运行 Electron 应用，不需要本地重新编译。

**修复**：从 `Depends:` 中移除：
- `build-essential`
- `nodejs`
- `npm`
- `p7zip-full`
- `python3`
- `unzip`

保留：
- `curl`（updater 下载更新用）
- `dpkg`
- 必要的系统 UI/音视频库（`libgtk-3-0`、`libnss3`、`libgbm1` 等）

---

## 4. 7-zip 无法解压 DMG

**现象**：`7z x Codex.dmg` 报错 `Can not open the file as archive`。

**原因**：系统自带的 `p7zip` 16.02 太旧，不支持新版 APFS DMG。

**修复**：
```bash
curl -L -o /tmp/7z.tar.xz https://www.7-zip.org/a/7z2409-linux-x64.tar.xz
tar -C /tmp -xf /tmp/7z.tar.xz
chmod +x /tmp/7zz
# 然后使用 /tmp/7zz 替代系统 7z
```

---

## 5. Linux 窗口透明闪烁

**现象**：移动窗口或悬停侧边栏时，背景出现透明闪烁或桌面壁纸透出。

**原因**：上游在 `BrowserWindow` 中设置了 `backgroundColor: '#00000000'`（全透明），依赖 macOS vibrancy 实现毛玻璃效果。Linux 没有同等合成器支持。

**修复**：在 patch 脚本中把 Linux 下的背景色替换为不透明主题色：
- Dark mode: `#000000`
- Light mode: `#f9f9f9`
