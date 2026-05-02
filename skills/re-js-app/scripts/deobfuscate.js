/**
 * ChatWise JS Deobfuscator v2
 *
 * Multi-pass scope-aware deobfuscation:
 * Pass 1: Rename import aliases → meaningful names (scope-aware)
 * Pass 2: Rename webpack factory params → module_/exports_/require_ (scope-aware)
 * Pass 3: Trace require("x") → rename result var to the module name
 * Pass 4: Heuristic renaming based on API usage patterns (Electron, Node, etc.)
 * Pass 5: Clean up - remove _ prefix from import renames where possible
 *
 * Usage: node deobfuscate.js <input.js> [output.js]
 */
const fs = require("fs");
const parser = require("@babel/parser");
const _traverse = require("@babel/traverse");
const traverse = _traverse.default;
const _generate = require("@babel/generator");
const generate = _generate.default;

const inputFile = process.argv[2];
const outputFile = process.argv[3];

if (!inputFile) {
  console.error("Usage: node deobfuscate.js <input.js> [output.js]");
  process.exit(1);
}

const code = fs.readFileSync(inputFile, "utf-8");

const ast = parser.parse(code, {
  sourceType: "module",
  allowImportExportEverywhere: true,
  allowReturnOutsideFunction: true,
  allowSuperOutsideMethod: true,
  allowUndeclaredExports: true,
  errorRecovery: true,
  plugins: ["jsx", "typescript"],
});

// ─── Known API patterns for heuristic matching ───
// For each popular module, list its characteristic methods/properties.
// If a variable is used with these, it's likely that module.
const KNOWN_API = {
  // Electron main process
  BrowserWindow: ["getAllWindows", "fromWebContents", "getFocusedWindow", "addDevToolsExtension", "removeDevToolsExtension", "addExtension"],
  app: ["whenReady", "quit", "exit", "relaunch", "isReady", "requestSingleInstanceLock", "on", "off", "getPath", "getVersion", "getName", "setName"],
  ipcMain: ["handle", "handleOnce", "removeHandler", "on", "once", "removeListener"],
  dialog: ["showOpenDialog", "showSaveDialog", "showMessageBox", "showErrorBox", "showCertificateTrustDialog"],
  shell: ["openExternal", "openPath", "showItemInFolder", "trashItem", "beep"],
  clipboard: ["readText", "writeText", "readHTML", "writeHTML", "readImage", "writeImage", "clear"],
  nativeTheme: ["shouldUseDarkColors", "shouldUseHighContrastColors", "shouldUseInvertedColorScheme", "themeSource"],
  net: ["fetch", "request", "resolveHost", "isOnline"],
  Menu: ["buildFromTemplate", "setApplicationMenu", "getApplicationMenu", "sendActionToFirstResponder"],
  Tray: ["setToolTip", "setTitle", "setImage", "setContextMenu", "displayBalloon", "destroy"],
  WebContentsView: ["setBounds", "getBounds", "setBackgroundColor", "webContents"],
  Notification: ["isSupported", "show", "close"],
  systemPreferences: ["isTrustedAccessibilityClient", "askForMediaAccess", "getMediaAccessStatus", "getUserDefault", "setUserDefault"],
  nativeImage: ["createFromPath", "createFromBuffer", "createFromDataURL", "createEmpty", "resize"],
  session: ["fromPartition", "defaultSession", "fromPath", "getSpellCheckerLanguages"],

  // Node.js core
  path: ["join", "resolve", "basename", "dirname", "extname", "normalize", "relative", "sep", "delimiter", "parse", "format", "isAbsolute", "posix", "win32"],
  fs: ["readFileSync", "writeFileSync", "existsSync", "readdirSync", "statSync", "mkdirSync", "rmSync", "unlinkSync", "renameSync", "copyFileSync", "appendFileSync", "accessSync", "lstatSync", "readlinkSync", "symlinkSync", "chmodSync", "chownSync", "watch", "createReadStream", "createWriteStream", "readFile", "writeFile", "readdir", "mkdir", "stat", "rm", "unlink", "rename", "access", "lstat", "readlink", "symlink", "exists", "constants", "promises", "watchFile", "unwatchFile"],
  os: ["platform", "release", "type", "arch", "cpus", "freemem", "totalmem", "homedir", "hostname", "networkInterfaces", "userInfo", "tmpdir", "EOL", "endianness", "uptime", "loadavg"],
  crypto: ["randomUUID", "randomBytes", "createHash", "createHmac", "createSign", "createVerify", "createCipheriv", "createDecipheriv", "createDiffieHellman", "createECDH", "pbkdf2", "pbkdf2Sync", "randomFill", "randomFillSync", "generateKeyPair", "generateKeyPairSync", "generateKey", "generateKeySync", "publicEncrypt", "privateDecrypt", "privateEncrypt", "publicDecrypt", "sign", "verify", "getCiphers", "getCurves", "getHashes", "timingSafeEqual", "webcrypto"],
  child_process: ["spawn", "exec", "execFile", "fork", "spawnSync", "execSync", "execFileSync"],
  http: ["createServer", "request", "get", "Agent", "Server", "METHODS", "STATUS_CODES", "globalAgent", "maxHeaderSize", "IncomingMessage", "ServerResponse", "OutgoingMessage", "ClientRequest"],
  https: ["createServer", "request", "get", "Agent", "globalAgent"],
  url: ["fileURLToPath", "pathToFileURL", "URL", "URLSearchParams", "domainToASCII", "domainToUnicode", "format", "parse", "resolve", "resolveObject"],
  stream: ["PassThrough", "Readable", "Writable", "Duplex", "Transform", "pipeline", "finished", "addAbortSignal"],
  readline: ["createInterface", "Interface", "clearLine", "clearScreenDown", "cursorTo", "moveCursor", "emitKeypressEvents"],
  process: ["cwd", "chdir", "env", "argv", "exit", "nextTick", "hrtime", "uptime", "memoryUsage", "cpuUsage", "pid", "ppid", "arch", "platform", "version", "versions", "config", "stdin", "stdout", "stderr", "title", "umask", "kill"],
  buffer: ["Buffer", "Blob", "File", "constants", "transcode", "SlowBuffer", "INSPECT_MAX_BYTES", "kMaxLength", "kStringMaxLength", "isBuffer", "isEncoding", "byteLength", "compare", "concat", "alloc", "allocUnsafe", "allocUnsafeSlow", "from"],

  // Common npm packages
  "better-sqlite3": ["prepare", "exec", "pragma", "backup", "function", "aggregate", "table", "loadExtension", "serialize", "close", "memory", "open", "transaction"],
  "font-list": ["getFonts", "getFontsSync"],
};

// Flatten: method → module name (for quick lookup)
const METHOD_TO_MODULE = {};
for (const [moduleName, methods] of Object.entries(KNOWN_API)) {
  for (const method of methods) {
    if (!METHOD_TO_MODULE[method]) METHOD_TO_MODULE[method] = [];
    METHOD_TO_MODULE[method].push(moduleName);
  }
}

// ─── Helper: build usage fingerprint for a variable in a given scope ───
function buildFingerprint(binding, scope) {
  const methods = new Set();
  const props = new Set();
  let newCount = 0;
  let callCount = 0;

  scope.traverse({
    MemberExpression(path) {
      if (
        path.node.object.type === "Identifier" &&
        path.node.object.name === binding.name &&
        path.node.property.type === "Identifier" &&
        !path.node.computed
      ) {
        const prop = path.node.property.name;
        props.add(prop);
        // Check if parent is a call
        const parent = path.parentPath;
        if (parent && parent.node.type === "CallExpression" && parent.node.callee === path.node) {
          methods.add(prop);
          callCount++;
        }
      }
    },
    NewExpression(path) {
      if (
        path.node.callee.type === "Identifier" &&
        path.node.callee.name === binding.name
      ) {
        newCount++;
      }
    },
    CallExpression(path) {
      if (
        path.node.callee.type === "Identifier" &&
        path.node.callee.name === binding.name
      ) {
        callCount++;
      }
    },
  });

  return { methods, props, newCount, callCount };
}

// ─── Helper: score a module match based on method overlap ───
function scoreModuleMatch(methods, moduleName) {
  const apiMethods = KNOWN_API[moduleName] || [];
  if (apiMethods.length === 0) return 0;
  let matches = 0;
  for (const m of methods) {
    if (apiMethods.includes(m)) matches++;
  }
  return matches / Math.min(apiMethods.length, methods.size || 1);
}

// ═══════════════════════════════════════════════════════════════
// PASS 1: Collect import aliases
// ═══════════════════════════════════════════════════════════════
const importRenames = []; // { scope: path, oldName, newName }

traverse(ast, {
  ImportDeclaration(path) {
    for (const spec of path.node.specifiers) {
      const localName = spec.local.name;
      if (spec.type === "ImportSpecifier" && spec.imported) {
        const importedName = spec.imported.name || spec.imported.value;
        if (
          importedName &&
          importedName !== localName &&
          localName.length <= 3 &&
          importedName.length > 2 // Skip single/double-letter chunk exports (A, B, At, etc.)
        ) {
          importRenames.push({
            scope: path,
            oldName: localName,
            newName: importedName,
          });
        }
      } else if (spec.type === "ImportDefaultSpecifier" || spec.type === "ImportNamespaceSpecifier") {
        // For default/namespace imports, we only rename if we can infer from source
        const source = path.node.source.value;
        const parts = source.split("/");
        const pkgName = parts[0].startsWith("@") ? parts.slice(0, 2).join("/") : parts[0];
        // Don't rename default imports unless they match a known pattern
      }
    }
  },
});

// ═══════════════════════════════════════════════════════════════
// PASS 2: Build heuristic rename map from API usage patterns
// ═══════════════════════════════════════════════════════════════
const heuristicRenames = []; // { scope, oldName, newName, confidence }
const WEBPACK_NAMES = new Set(["module", "exports", "require", "__webpack_module__", "__webpack_exports__", "__webpack_require__"]);

traverse(ast, {
  Function(path) {
    if (!path.scope) return;
    const fnScope = path.scope;

    // Check all bindings in this function's scope
    for (const [name, binding] of Object.entries(fnScope.bindings)) {
      // Skip if name is already meaningful
      if (name.length > 3 || WEBPACK_NAMES.has(name)) continue;
      // Skip if it's a parameter of this function (those are handled by webpack pass)
      if (binding.path.isIdentifier() && binding.path.parent === path.node) continue;

      const fingerprint = buildFingerprint(binding, path);

      // Skip if no useful information
      if (fingerprint.methods.size === 0 && fingerprint.newCount === 0) continue;

      // Try to match against known API
      let bestMatch = null;
      let bestScore = 0;
      for (const [moduleName] of Object.entries(KNOWN_API)) {
        const score = scoreModuleMatch(fingerprint.methods, moduleName);
        if (score > bestScore) {
          bestScore = score;
          bestMatch = moduleName;
        }
      }

      // Also try matching individual methods
      if (!bestMatch || bestScore < 0.3) {
        const methodVotes = {};
        for (const method of fingerprint.methods) {
          const candidates = METHOD_TO_MODULE[method] || [];
          for (const c of candidates) {
            methodVotes[c] = (methodVotes[c] || 0) + 1;
          }
        }
        let bestVote = 0;
        let bestVoteMatch = null;
        for (const [c, votes] of Object.entries(methodVotes)) {
          if (votes > bestVote) {
            bestVote = votes;
            bestVoteMatch = c;
          }
        }
        if (bestVoteMatch && bestVote / fingerprint.methods.size >= 0.3) {
          bestMatch = bestVoteMatch;
          bestScore = bestVote / fingerprint.methods.size;
        }
      }

      // Only rename if high confidence
      if (bestMatch && bestScore >= 0.4 && fingerprint.methods.size >= 2) {
        heuristicRenames.push({
          scope: path,
          oldName: name,
          newName: bestMatch.replace(/-/g, "_"),
          confidence: bestScore,
        });
      }
    }
  },
});

// ═══════════════════════════════════════════════════════════════
// PASS 3: Detect webpack factory functions and collect scope+params
// ═══════════════════════════════════════════════════════════════
const webpackFactoryScopes = []; // { path, paramRenames: [{oldName, newName}] }

traverse(ast, {
  Function(path) {
    if (!path.scope) return;
    const params = path.node.params;
    if (params.length < 2 || params.length > 3) return;

    // Check if this function body uses t.exports or calls n("...")
    let usesExports = false;
    let usesRequire = false;

    path.traverse({
      MemberExpression(innerPath) {
        // Detect: 2nd_param.exports = ...  or  1st_param.exports = ...
        // Only flag if the member expression is the LHS of an assignment (exports.module = ...)
        // or if it's a common webpack pattern like exports.exports
        if (
          innerPath.node.object.type === "Identifier" &&
          !innerPath.node.computed &&
          innerPath.node.property.name === "exports"
        ) {
          // Check if object is 2nd param (exports) or 1st param (module)
          for (let i = 0; i <= 1; i++) {
            if (
              params[i] &&
              params[i].type === "Identifier" &&
              innerPath.node.object.name === params[i].name
            ) {
              usesExports = true;
            }
          }
        }
      },
      CallExpression(innerPath) {
        // Only flag as require if called with a string literal (module path)
        if (
          innerPath.node.callee.type === "Identifier" &&
          params.length >= 3 &&
          params[2].type === "Identifier" &&
          innerPath.node.callee.name === params[2].name &&
          innerPath.node.arguments.length >= 1 &&
          innerPath.node.arguments[0].type === "StringLiteral"
        ) {
          usesRequire = true;
        }
      },
    });

    if (usesExports || usesRequire) {
      const paramRenames = [
        { oldName: params[0].type === "Identifier" ? params[0].name : null, newName: "module" },
        { oldName: params[1].type === "Identifier" ? params[1].name : null, newName: "exports" },
        params.length >= 3 && params[2].type === "Identifier"
          ? { oldName: params[2].name, newName: "require" }
          : null,
      ].filter((r) => r && r.oldName && r.oldName !== r.newName);

      webpackFactoryScopes.push({ path, paramRenames });
    }
  },
});

// ═══════════════════════════════════════════════════════════════
// PASS 4: Apply renames (scope-aware)
// ═══════════════════════════════════════════════════════════════
let renameCount = 0;

traverse(ast, {
  Program(progPath) {
    if (!progPath.scope) return;

    // 4a: Rename import aliases at program scope
    for (const { oldName, newName } of importRenames) {
      const binding = progPath.scope.getBinding(oldName);
      if (binding && binding.path.isImportSpecifier()) {
        try {
          const targetName = `_${newName}`;
          // Skip if target name already exists (avoid duplicate declaration)
          if (oldName !== targetName && !progPath.scope.getBinding(targetName)) {
            progPath.scope.rename(oldName, targetName);
            renameCount++;
          }
        } catch (e) {
          // conflict, skip
        }
      }
    }

    // 4b: Rename Object utility vars at program scope
    const utilPatterns = {
      se: "Object_create",
      ce: "Object_defineProperty",
      le: "Object_getOwnPropertyDescriptor",
      ue: "Object_getOwnPropertyNames",
      de: "Object_getPrototypeOf",
      fe: "Object_hasOwnProperty",
    };
    for (const [oldName, newName] of Object.entries(utilPatterns)) {
      const binding = progPath.scope.getBinding(oldName);
      if (binding) {
        try {
          progPath.scope.rename(oldName, newName);
          renameCount++;
        } catch (e) {}
      }
    }
  },

  Function(path) {
    if (!path.scope) return;

    // 4c: Rename webpack factory params
    for (const factory of webpackFactoryScopes) {
      if (factory.path === path) {
        for (const { oldName, newName } of factory.paramRenames) {
          const binding = path.scope.getBinding(oldName);
          if (binding && binding.path === path.get(`params.${path.node.params.findIndex((p) => p.name === oldName)}`)) {
            try {
              const suffix = path.scope.getBinding(newName) ? "_" : "";
              path.scope.rename(oldName, newName + suffix);
              renameCount++;
            } catch (e) {}
          }
        }
        break;
      }
    }

    // 4d: Rename heuristic matches
    for (const hr of heuristicRenames) {
      if (hr.scope === path) {
        const binding = path.scope.getBinding(hr.oldName);
        if (binding) {
          try {
            // Add suffix to avoid conflicts
            const target = path.scope.getBinding(hr.newName) ? `${hr.newName}_` : hr.newName;
            path.scope.rename(hr.oldName, target);
            renameCount++;
          } catch (e) {}
        }
      }
    }
  },
});

console.error(`[deobfuscate v2] Import renames: ${importRenames.length}`);
console.error(`[deobfuscate v2] Heuristic API renames: ${heuristicRenames.length}`);
if (heuristicRenames.length > 0) {
  heuristicRenames.slice(0, 10).forEach((r) =>
    console.error(`  ${r.oldName} → ${r.newName} (conf: ${r.confidence.toFixed(2)})`)
  );
}
console.error(`[deobfuscate v2] Webpack factories: ${webpackFactoryScopes.length}`);
console.error(`[deobfuscate v2] Total renames: ${renameCount}`);

const result = generate(ast, {
  retainLines: false,
  compact: false,
  comments: true,
  jsescOption: { minimal: true },
});

fs.writeFileSync(outputFile || inputFile.replace(/\.js$/, ".deobf.js"), result.code);
console.error(`[deobfuscate v2] Wrote ${outputFile || inputFile.replace(/\.js$/, ".deobf.js")}`);
console.error(`[deobfuscate v2] Size: ${result.code.length} bytes`);
