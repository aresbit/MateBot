# macOS Electron App → Linux 转换详细流程

## 前置条件

- Node.js 20+
- npm / npx
- python3
- 7z (推荐 7zz 24.09+，旧版 p7zip 可能无法解压 APFS DMG)
- curl, unzip
- make, g++
- Rust + cargo (若需要 updater 服务)

## 通用转换步骤

1. **获取 macOS DMG**
   - 从官方 CDN 或手动下载 `Codex.dmg`。

2. **解压 DMG 提取 .app**
   ```bash
   7zz x -y Codex.dmg
   # 找到 Codex.app
   ```

3. **提取 app.asar**
   ```bash
   npx asar extract "Codex.app/Contents/Resources/app.asar" app-extracted
   ```

4. **编译 Linux 原生模块**
   -  determinate Electron 版本（通常是 DMG 中自带的 `electron` 版本）。
   - 在干净目录安装相同版本的 `better-sqlite3`、`node-pty`。
   - 使用 `@electron/rebuild` 针对目标 Electron 版本强制编译：
     ```bash
     npx @electron/rebuild -v <ELECTRON_VERSION> --force
     ```
   - 将编译产物复制回 `app-extracted/node_modules/...`。

5. **移除 macOS 专有模块**
   ```bash
   rm -rf app-extracted/node_modules/sparkle-darwin
   find app-extracted -name "sparkle.node" -delete
   ```

6. **打 Linux UI patch**
   - 修改 main bundle 中的 `BrowserWindow` 选项：
     - 为 Linux 添加 `icon`
     - 隐藏菜单栏 (`autoHideMenuBar`)
     - 将透明背景替换为不透明颜色（防止 Linux 下闪烁）
   - **关键**：新版 Vite bundle 中 `path` 模块的变量名可能被压缩为任意名称，patch 时必须**运行时检测**，不能硬编码 `t.join`。

7. **重新打包 app.asar**
   ```bash
   npx asar pack app-extracted app.asar --unpack "{*.node,*.so,*.dylib}"
   ```

8. **下载 Linux Electron runtime**
   - 从 `https://github.com/electron/electron/releases/download/v<VERSION>/electron-v<VERSION>-linux-x64.zip` 下载。
   - 解压到输出目录（如 `codex-app/`）。

9. **整合资源**
   - 复制新的 `app.asar` 到 `codex-app/resources/`
   - 复制 webview 静态资源到 `codex-app/content/webview/`
   - 生成启动脚本 `start.sh`

10. **打包分发**
    - `.deb`：使用 `dpkg-deb`
    - `.rpm` / `pacman`：对应打包工具

## 目录结构示例

```
codex-app/
├── Codex              # Linux Electron 可执行文件
├── resources/
│   ├── app.asar
│   └── app.asar.unpacked/
├── content/webview/   # HTML/CSS/JS 前端资源
└── start.sh
```
