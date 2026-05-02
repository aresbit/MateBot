/**
 * Local Variable Renamer - Statistical/heuristic variable name inference
 *
 * Run AFTER webcrack + deobfuscate.js.
 * Uses context clues to rename single-letter local variables with meaningful names.
 *
 * Heuristics (word frequency + semantic analysis - 词频+语义学):
 * 1. Usage pattern: new X() → constructor; X.push() → array; X.replace() → string
 * 2. Assignment source: X = require("y") → module name; X = path.join() → filePath
 * 3. Control flow role: loop var → i/index; accumulator → result/acc; callback → cb
 * 4. Parameter position: (err, result) pattern; (req, res) pattern
 * 5. API context: X.handle() → ipcMain; X.whenReady() → app
 *
 * Usage: node rename-locals.js <deobfuscated.js> [output.js]
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
  console.error("Usage: node rename-locals.js <input.js> [output.js]");
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

// ─── Feature extraction ────────────────────────────────────
function analyzeVariable(binding, path) {
  const features = {
    isNewed: false,        // new X()
    isCalled: false,       // X()
    isCallback: false,     // typeof X === "function"  or  X(err, result)
    methodsCalled: new Set(),
    propsAccessed: new Set(),
    assignedFrom: null,    // e.g., "require", "path.join", "new ClassName"
    passedToNodeAPI: new Set(),
    isCounter: false,      // X++, X += 1, X = 0 followed by X++
    isAccumulator: false,  // X = X.concat(...), X.push(...), result construction
    isString: false,
    isArray: false,
    isObject: false,
    isPromise: false,
    isError: false,
    isNumber: false,
    isBoolean: false,
    isTemp: false,        // used only once then passed to something
    inCondition: false,   // used in if/while/ternary condition
    assignCount: 0,
    callCount: 0,
    refCount: 0,
  };

  path.traverse({
    // new X()
    NewExpression(inner) {
      if (inner.node.callee.type === "Identifier" && inner.node.callee.name === binding.name) {
        features.isNewed = true;
        features.assignCount++;
      }
    },
    // X.method() or X.prop
    MemberExpression(inner) {
      if (inner.node.object.type === "Identifier" && inner.node.object.name === binding.name && !inner.node.computed) {
        features.propsAccessed.add(inner.node.property.name);
        const parent = inner.parentPath;
        if (parent && parent.node.type === "CallExpression" && parent.node.callee === inner.node) {
          features.methodsCalled.add(inner.node.property.name);
        }
      }
    },
    // X() called as function
    CallExpression(inner) {
      if (inner.node.callee.type === "Identifier" && inner.node.callee.name === binding.name) {
        features.isCalled = true;
        features.callCount++;
      }
    },
    // X = ... (assignment)
    AssignmentExpression(inner) {
      if (inner.node.left.type === "Identifier" && inner.node.left.name === binding.name) {
        features.assignCount++;
        const right = inner.node.right;
        if (right.type === "CallExpression") {
          if (right.callee.type === "Identifier") {
            features.assignedFrom = right.callee.name;
          } else if (right.callee.type === "MemberExpression" && right.callee.property.type === "Identifier") {
            features.assignedFrom = `${right.callee.object.name || "?"}.${right.callee.property.name}`;
          }
        }
      }
    },
    // X++ or X += 1
    UpdateExpression(inner) {
      if (inner.node.argument.type === "Identifier" && inner.node.argument.name === binding.name) {
        features.isCounter = true;
      }
    },
    // typeof X === "function"
    UnaryExpression(inner) {
      if (inner.node.operator === "typeof" && inner.node.argument.type === "Identifier" && inner.node.argument.name === binding.name) {
        features.isCallback = true;
      }
    },
    // if (X) or while (X) or X ? ... : ...
    IfStatement(inner) { checkInCondition(inner.node.test, binding.name, features); },
    ConditionalExpression(inner) { checkInCondition(inner.node.test, binding.name, features); },
    WhileStatement(inner) { checkInCondition(inner.node.test, binding.name, features); },
    // X in simple references
    Identifier(inner) {
      if (inner.node.name === binding.name) features.refCount++;
    },
  });

  // Check types from litmus tests
  for (const method of features.methodsCalled) {
    if (["push", "pop", "shift", "unshift", "splice", "forEach", "map", "filter", "reduce", "find", "findIndex", "some", "every", "indexOf", "includes"].includes(method)) {
      features.isArray = true;
    }
    if (["replace", "match", "search", "split", "substring", "slice", "toLowerCase", "toUpperCase", "trim", "startsWith", "endsWith", "charAt", "charCodeAt", "indexOf", "includes"].includes(method) && !features.isArray) {
      features.isString = true;
    }
    if (["then", "catch", "finally"].includes(method)) {
      features.isPromise = true;
    }
  }
  for (const prop of features.propsAccessed) {
    if (["length"].includes(prop) && !features.isString) features.isArray = true;
  }
  if (features.methodsCalled.has("test") || features.methodsCalled.has("exec")) {
    features.isString = true; // regex test
  }

  // Infer type from assigned source
  if (features.assignedFrom) {
    if (features.assignedFrom.includes("Error")) features.isError = true;
    if (features.assignedFrom.startsWith("new ")) features.isObject = true;
  }

  // Detect temp variable pattern (assigned once, used once)
  if (features.assignCount === 1 && features.refCount <= 3) {
    features.isTemp = true;
  }

  // Check if used in condition
  if (features.isArray && features.methodsCalled.has("length")) features.inCondition = false; // array length check

  return features;
}

function checkInCondition(test, name, features) {
  if (!test) return;
  if (test.type === "Identifier" && test.name === name) {
    features.inCondition = true;
  } else if (test.type === "BinaryExpression" || test.type === "LogicalExpression") {
    checkInCondition(test.left, name, features);
    checkInCondition(test.right, name, features);
  } else if (test.type === "UnaryExpression") {
    checkInCondition(test.argument, name, features);
  }
}

// ─── Name inference from features ──────────────────────────
function inferName(name, features, paramIndex, totalParams, scopeBindings) {
  const scores = {};

  // Rule: param position patterns
  if (paramIndex >= 0) {
    if (totalParams === 2 && paramIndex === 0) {
      scores["err"] = 5;
      scores["error"] = 2;
    }
    if (totalParams === 2 && paramIndex === 1) {
      scores["result"] = 5;
      scores["data"] = 2;
    }
    if (totalParams === 3 && paramIndex === 0) {
      scores["err"] = 3;
      scores["req"] = 2;
    }
    if (totalParams === 3 && paramIndex === 2) {
      scores["cb"] = 5;
      scores["callback"] = 2;
    }
  }

  // Rule: type-based naming
  if (features.isArray) {
    if (features.methodsCalled.has("filter") || features.methodsCalled.has("map")) {
      scores["items"] = 3;
      scores["results"] = 2;
    }
    scores["arr"] = 1;
  }
  if (features.isString) {
    scores["str"] = 2;
    if (features.methodsCalled.has("replace")) scores["pattern"] = 2;
  }
  if (features.isPromise) scores["promise"] = 3;
  if (features.isError) scores["err"] = 5;
  if (features.isBoolean || features.inCondition) {
    scores["ok"] = 2;
    scores["flag"] = 1;
  }

  // Rule: role-based naming
  if (features.isCounter) {
    scores["idx"] = 5;
    scores["index"] = 3;
    scores["i"] = 3;
    // Keep i, j, k for nested loops
    if (name === "i" || name === "j" || name === "k") scores[name] = 10;
  }
  if (features.isCallback || features.isCalled) {
    if (features.callCount >= 2) scores["cb"] = 3;
    if (!features.isTemp) scores["fn"] = 2;
  }
  if (features.isNewed) {
    if (features.assignedFrom && features.assignedFrom.startsWith("new ")) {
      scores["instance"] = 2;
    }
  }
  if (features.isTemp) {
    scores["tmp"] = 3;
  }

  // Rule: specific method patterns
  for (const method of features.methodsCalled) {
    // File/path operations
    if (["join", "resolve", "basename", "dirname", "extname", "relative", "normalize", "parse", "format"].includes(method)) {
      scores["filePath"] = (scores["filePath"] || 0) + 2;
      scores["path"] = (scores["path"] || 0) + 1;
    }
    // File system operations
    if (["readFile", "writeFile", "readFileSync", "writeFileSync", "existsSync", "readdirSync", "statSync", "mkdirSync"].includes(method)) {
      scores["fs"] = 3;
    }
    // Child process
    if (["spawn", "exec", "fork", "execSync", "spawnSync"].includes(method)) {
      scores["childProcess"] = 2;
      scores["cp"] = 1;
    }
    // Object/Map
    if (["keys", "values", "entries", "has", "get", "set"].includes(method)) {
      scores["obj"] = (scores["obj"] || 0) + 1;
      scores["map"] = (scores["map"] || 0) + 1;
    }
  }

  // Rule: assigned from require
  if (features.assignedFrom) {
    if (features.assignedFrom === "require" || features.assignedFrom === "createRequire") {
      // Can't determine the module name from features alone, but mark it
      scores["mod"] = 2;
    }
  }

  // Rule: look for meaningful context from scope neighbors
  // If a nearby variable is named "callback", and this one is called like a function, it's likely also a callback
  for (const [otherName] of Object.entries(scopeBindings)) {
    if (otherName.toLowerCase().includes("callback") && features.isCalled) {
      scores["cb"] = (scores["cb"] || 0) + 2;
    }
    if (otherName.toLowerCase().includes("error") && features.isCalled) {
      scores["err"] = (scores["err"] || 0) + 2;
    }
  }

  // Pick the highest scoring name
  let bestName = null;
  let bestScore = 0;
  for (const [candidate, score] of Object.entries(scores)) {
    if (score > bestScore) {
      bestScore = score;
      bestName = candidate;
    }
  }

  // Only rename if score is high enough
  if (bestScore >= 3 && bestName && bestName !== name) {
    return bestName;
  }

  return null;
}

// ─── Main processing ───────────────────────────────────────
const renamesToApply = []; // { path, oldName, newName }

traverse(ast, {
  Function(path) {
    if (!path.scope || !path.node.body) return;
    if (path.node.body.type !== "BlockStatement" && path.node.body.type !== "FunctionBody") return;

    const params = path.node.params || [];
    const paramNames = new Set(params.filter(p => p.type === "Identifier").map(p => p.name));
    const scopeBindings = path.scope.bindings || {};

    // For each single-letter LOCAL variable (not a param, not from outer scope)
    for (const [name, binding] of Object.entries(scopeBindings)) {
      // Only process single-letter or very short names (skip already-long names)
      if (name.length > 3) continue;
      // Skip params (handled by deobfuscate.js)
      if (paramNames.has(name) && binding.path.isIdentifier() && binding.path.parent === path.node) continue;
      // Skip if it's an import (handled)
      if (binding.path.isImportSpecifier() || binding.path.isImportDefaultSpecifier() || binding.path.isImportNamespaceSpecifier()) continue;
      // Skip webpack-level names
      if (["module", "exports", "require"].includes(name)) continue;

      const paramIndex = params.findIndex(p => p.type === "Identifier" && p.name === name);
      const features = analyzeVariable(binding, path);
      const newName = inferName(name, features, paramIndex, params.length, scopeBindings);

      if (newName) {
        renamesToApply.push({ path, oldName: name, newName });
      }
    }
  },
});

// ─── Apply renames (scope-aware) ───────────────────────────
let appliedCount = 0;
const applied = new Map(); // scope → { oldName → newName }

for (const { path, oldName, newName } of renamesToApply) {
  if (!path.scope) continue;

  // Check for conflicts within same scope
  const scopeKey = path.scope.uid;
  if (!applied.has(scopeKey)) applied.set(scopeKey, new Map());
  const scopeApplied = applied.get(scopeKey);

  if (scopeApplied.has(oldName)) continue; // already renamed

  try {
    // Use a unique suffix to avoid conflicts
    let finalName = newName;
    if (path.scope.getBinding(finalName)) {
      finalName = `${newName}_`;
    }
    if (oldName !== finalName) {
      path.scope.rename(oldName, finalName);
      scopeApplied.set(oldName, finalName);
      appliedCount++;
    }
  } catch (e) {
    // Name conflict, skip
  }
}

console.error(`[rename-locals] Candidates found: ${renamesToApply.length}`);
console.error(`[rename-locals] Applied: ${appliedCount}`);
if (appliedCount > 0 && appliedCount <= 20) {
  for (const [, scopeApplied] of applied) {
    for (const [oldName, newName] of scopeApplied) {
      console.error(`  ${oldName} → ${newName}`);
    }
  }
}

const result = generate(ast, {
  retainLines: false,
  compact: false,
  comments: true,
  jsescOption: { minimal: true },
});

fs.writeFileSync(outputFile || inputFile.replace(/\.js$/, ".renamed.js"), result.code);
console.error(`[rename-locals] Wrote ${outputFile || inputFile.replace(/\.js$/, ".renamed.js")}`);
