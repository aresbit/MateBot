# Electron & Node.js API Method Catalog

For heuristic variable identification. When a single-letter variable is used with these methods, infer its identity.

## Electron Main Process

### app
`whenReady`, `quit`, `exit`, `relaunch`, `isReady`, `requestSingleInstanceLock`,
`on`, `off`, `getPath`, `getVersion`, `getName`, `setName`, `setPath`,
`getAppPath`, `setAppUserModelId`, `commandLine`, `dock`, `disableHardwareAcceleration`

### BrowserWindow
`getAllWindows`, `fromWebContents`, `getFocusedWindow`, `addExtension`,
`removeExtension`, `addDevToolsExtension`, `removeDevToolsExtension`,
`loadURL`, `loadFile`, `webContents`, `setBounds`, `getBounds`, `center`,
`setTitle`, `getTitle`, `show`, `hide`, `close`, `destroy`, `minimize`,
`maximize`, `restore`, `focus`, `isMinimized`, `isMaximized`, `isVisible`,
`setMenu`, `setMenuBarVisibility`, `setBackgroundColor`, `setWindowButtonVisibility`

### ipcMain
`handle`, `handleOnce`, `removeHandler`, `on`, `once`, `removeListener`,
`removeAllListeners`

### dialog
`showOpenDialog`, `showSaveDialog`, `showMessageBox`, `showErrorBox`,
`showCertificateTrustDialog`

### shell
`openExternal`, `openPath`, `showItemInFolder`, `trashItem`, `beep`

### clipboard
`readText`, `writeText`, `readHTML`, `writeHTML`, `readImage`, `writeImage`,
`clear`, `availableFormats`

### nativeTheme
`shouldUseDarkColors`, `shouldUseHighContrastColors`,
`shouldUseInvertedColorScheme`, `themeSource`

### net
`fetch`, `request`, `resolveHost`, `isOnline`

### Menu
`buildFromTemplate`, `setApplicationMenu`, `getApplicationMenu`,
`sendActionToFirstResponder`

### Tray
`setToolTip`, `setTitle`, `setImage`, `setContextMenu`, `displayBalloon`,
`destroy`, `popUpContextMenu`, `closeContextMenu`

### WebContentsView / BrowserView
`setBounds`, `getBounds`, `setBackgroundColor`, `webContents`

### Notification
`isSupported`, `show`, `close`

### systemPreferences
`isTrustedAccessibilityClient`, `askForMediaAccess`, `getMediaAccessStatus`,
`getUserDefault`, `setUserDefault`, `registerDefaults`

### nativeImage
`createFromPath`, `createFromBuffer`, `createFromDataURL`, `createEmpty`,
`resize`, `crop`, `toBitmap`, `toDataURL`, `toJPEG`, `toPNG`, `getSize`

### session
`fromPartition`, `defaultSession`, `fromPath`, `getSpellCheckerLanguages`,
`setSpellCheckerLanguages`, `setProxy`, `resolveProxy`, `clearCache`,
`clearStorageData`, `clearAuthCache`, `cookies`, `webRequest`,
`setPermissionRequestHandler`

## Node.js Core

### path
`join`, `resolve`, `basename`, `dirname`, `extname`, `normalize`, `relative`,
`sep`, `delimiter`, `parse`, `format`, `isAbsolute`, `posix`, `win32`

### fs (sync)
`readFileSync`, `writeFileSync`, `existsSync`, `readdirSync`, `statSync`,
`mkdirSync`, `rmSync`, `unlinkSync`, `renameSync`, `copyFileSync`,
`appendFileSync`, `accessSync`, `lstatSync`, `readlinkSync`, `symlinkSync`,
`chmodSync`, `chownSync`

### fs (async)
`readFile`, `writeFile`, `readdir`, `mkdir`, `stat`, `rm`, `unlink`,
`rename`, `access`, `lstat`, `readlink`, `symlink`, `chmod`, `chown`,
`createReadStream`, `createWriteStream`, `watch`, `constants`, `promises`

### fs/promises
`readFile`, `writeFile`, `readdir`, `mkdir`, `stat`, `rm`, `unlink`,
`rename`, `access`, `lstat`, `readlink`, `symlink`, `chmod`, `chown`,
`copyFile`, `mkdtemp`, `watch`, `open`, `close`, `read`, `write`,
`appendFile`, `truncate`, `utimes`, `realpath`

### os
`platform`, `release`, `type`, `arch`, `cpus`, `freemem`, `totalmem`,
`homedir`, `hostname`, `networkInterfaces`, `userInfo`, `tmpdir`, `EOL`,
`endianness`, `uptime`, `loadavg`

### crypto
`randomUUID`, `randomBytes`, `createHash`, `createHmac`, `createSign`,
`createVerify`, `createCipheriv`, `createDecipheriv`, `createDiffieHellman`,
`createECDH`, `pbkdf2`, `generateKeyPair`, `publicEncrypt`, `privateDecrypt`,
`sign`, `verify`, `getCiphers`, `getCurves`, `getHashes`, `timingSafeEqual`,
`webcrypto`

### child_process
`spawn`, `exec`, `execFile`, `fork`, `spawnSync`, `execSync`, `execFileSync`

### http / https
`createServer`, `request`, `get`, `Agent`, `Server`, `METHODS`,
`STATUS_CODES`, `globalAgent`, `maxHeaderSize`

### url
`fileURLToPath`, `pathToFileURL`, `URL`, `URLSearchParams`,
`domainToASCII`, `domainToUnicode`, `format`, `parse`, `resolve`

### stream
`PassThrough`, `Readable`, `Writable`, `Duplex`, `Transform`,
`pipeline`, `finished`, `addAbortSignal`

### process
`cwd`, `chdir`, `env`, `argv`, `exit`, `nextTick`, `hrtime`, `uptime`,
`memoryUsage`, `cpuUsage`, `pid`, `ppid`, `arch`, `platform`, `version`,
`versions`, `stdin`, `stdout`, `stderr`, `kill`

### buffer
`Buffer`, `Blob`, `File`, `constants`, `transcode`, `isBuffer`,
`isEncoding`, `byteLength`, `compare`, `concat`, `alloc`, `allocUnsafe`,
`from`

## Common npm Packages

### better-sqlite3
`prepare`, `exec`, `pragma`, `backup`, `function`, `aggregate`, `table`,
`loadExtension`, `serialize`, `close`, `memory`, `open`, `transaction`

### font-list
`getFonts`, `getFontsSync`

### axios / node-fetch
`get`, `post`, `put`, `delete`, `patch`, `head`, `request`, `create`

### sharp (image processing)
`resize`, `rotate`, `extract`, `trim`, `flatten`, `toFormat`, `toBuffer`,
`toFile`, `metadata`, `stats`, `jpeg`, `png`, `webp`, `raw`, `composite`

### electron-updater
`checkForUpdates`, `checkForUpdatesAndNotify`, `downloadUpdate`,
`quitAndInstall`, `autoUpdater`

## Method-Based Variable Identification

When a single-letter variable `x` has multiple methods from one category, it's likely the corresponding module:

```javascript
// x = BrowserWindow
new x({...})
x.loadURL(...)
x.webContents.send(...)

// x = app
x.on('ready', ...)
x.whenReady().then(...)
x.getPath('userData')

// x = ipcMain
x.handle('channel', ...)
x.on('event', ...)

// x = path
x.join(base, name)
x.resolve(relPath)
x.basename(file)

// x = fs (promises)
x.readFile(path, 'utf-8')
x.mkdir(dir)
x.writeFile(path, data)
```
