# MoonBit Refactoring Guide

## Safe Refactoring Workflow

### Step 1: Establish Invariants

Before refactoring, confirm behavior/API invariants:

1. Run all tests: `moon test`
2. Review current API: `moon info`
3. Check `.mbti` files for public surface

### Step 2: Use Semantic Tools

**ALWAYS prefer semantic refactoring tools over manual edits.**

#### Rename Symbol

```bash
# Rename project-wide
moon ide rename old_name new_name

# With location (when symbol names are ambiguous)
moon ide rename compute_sum calculate_sum --loc math_utils.mbt:2
```

This updates:
- Definition site
- All call sites
- References in tests

#### Find References Before Changes

```bash
# Check what will be affected
moon ide find-references SymbolName
```

### Step 3: Keep Edits Package-Local

MoonBit packages are per directory. Keep refactoring changes within package boundaries when possible.

### Step 4: File Organization

#### Splitting Large Files

```moonbit
// Before: large_file.mbt (500 lines with mixed concerns)

// After: http_client.mbt
fn request(...) { ... }
fn get(...) { ... }

// After: http_response.mbt
fn parse_response(...) { ... }
fn handle_error(...) { ... }
```

Rules:
- Group related types and functions into focused files
- File names describe features, not rigidly mirror type names
- Move declarations freely between files in the same package

#### Moving Declarations

```moonbit
// File A: utils.mbt
///|
pub fn helper() -> Int { 42 }

// File B: main.mbt  
///|
fn main {
  println(helper())  // Works - same package
}
```

Moving `helper()` from `utils.mbt` to `helpers.mbt` is safe - semantics unchanged.

### Step 5: Deprecation Pattern

When refactoring public APIs:

```moonbit
///|
/// #deprecated
/// Use `new_function` instead
pub fn old_function() -> Int { ... }

///|
/// #alias(old_function, deprecated)
pub fn new_function() -> Int { ... }
```

1. Mark old API with `#deprecated`
2. Use `#alias` for temporary backward compatibility
3. Remove `#deprecated` and `#alias` after migration

### Step 6: Validation

After refactoring, validate:

```bash
# Type check
moon check

# Run tests
moon test

# Check API unchanged (for behavior-preserving refactoring)
moon info
git diff *.mbti  # Should be minimal/no changes

# Format
moon fmt
```

## Refactoring Checklist

### Behavior-Preserving Refactor

- [ ] Tests pass before and after
- [ ] `.mbti` files unchanged (or changes reviewed)
- [ ] `moon check` passes
- [ ] `moon fmt` applied

### API Changes

- [ ] `#deprecated` added to old APIs
- [ ] `#alias` for backward compatibility (temporary)
- [ ] Tests updated for new API
- [ ] `.mbti` changes reviewed and intentional
- [ ] Migration path documented

## Common Refactoring Patterns

### Extract Function

```moonbit
// Before
fn process(data: Data) -> Result {
  // 20 lines of validation
  // 15 lines of transformation
  // 10 lines of output
}

// After
fn validate(data: Data) -> Result { ... }
fn transform(data: Data) -> Data { ... }
fn output(data: Data) -> Result { ... }

fn process(data: Data) -> Result {
  validate(data)?
  let transformed = transform(data)
  output(transformed)
}
```

### Rename Type

```bash
# Use semantic rename
moon ide rename OldType NewType

# Or manually with search/replace if local
moon ide find-references OldType  # Check scope
```

### Change Method Signature

```moonbit
// Before
fn process(x: Int, y: Int) -> Int

// After - with backward compatibility
///| #deprecated
fn process(x: Int, y: Int) -> Int {
  process(x, y, default_z)
}

fn process(x: Int, y: Int, z: Int) -> Int { ... }
```

## Anti-patterns to Avoid

### ❌ Don't Use grep for Refactoring

```bash
# ❌ Dangerous - catches comments, strings
sed -i 's/old_name/new_name/g' *.mbt

# ✅ Safe - semantic understanding
moon ide rename old_name new_name
```

### ❌ Don't Break Package Boundaries Unnecessarily

Moving code across packages changes import requirements and may break consumers.

### ❌ Don't Mix Refactoring with Feature Changes

Separate commits:
1. Refactor (behavior-preserving)
2. Feature changes (with tests)

This makes review easier and rollback safer.
