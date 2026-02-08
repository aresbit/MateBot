# MoonBit Testing Guide

## Snapshot Tests

`moon test -u` auto-updates `content=""` in `inspect(val)`.

```moonbit
///|
test "snapshot" {
  inspect([1, 2, 3], content="")  // auto-filled by moon test -u
}
```

After running:

```moonbit
test "snapshot" {
  inspect([1, 2, 3], content="[1, 2, 3]")
}
```

### For Complex Structures

Use `@json.inspect()` for complex nested structures:

```moonbit
///|
test "complex snapshot" {
  let data = { "name": "test", "values": [1, 2, 3] }
  @json.inspect(data, content={ "name": "test", "values": [1, 2, 3] })
}
```

### Update Workflow

1. After changing code that affects output, run `moon test --update`
2. Regenerate snapshots
3. Review diffs in test files
4. The `content=` parameter will be updated automatically

## Test Organization

### Black-box Tests (Default)

Call only public APIs via `@package.fn`.

```moonbit
// In mylib_test.mbt
test "public api" {
  let result = @mylib.public_function()
  inspect(result, content="expected")
}
```

### White-box Tests

Use when private members matter. File named `*_wbtest.mbt`.

```moonbit
// In mylib_wbtest.mbt
test "private implementation" {
  // Can access private functions in the same package
  let result = private_helper()
  inspect(result, content="expected")
}
```

### Grouping

Combine related checks in one test block for speed and clarity:

```moonbit
test "comprehensive" {
  // Test multiple related things
  inspect(fn_a(), content="result_a")
  inspect(fn_b(), content="result_b")
  inspect(fn_c(), content="result_c")
}
```

### Panic Tests

Name tests with prefix `test "panic ..."`. If the call returns a value, wrap with `ignore(...)`.

```moonbit
test "panic on empty" {
  ignore(maximum([]))  // Should panic
}
```

### Error Tests

Use `try? f()` to get `Result[...]` and `inspect` it when a function may raise:

```moonbit
///|
test "error handling" {
  let result : Result[Int, ParseError] = try? parse("invalid")
  inspect(result, content="Err(InvalidFormat)")
}
```

## Docstring Tests

Public APIs are encouraged to have docstring tests.

```moonbit
///|
/// Get the largest element of a non-empty `Array`.
///
/// # Example
/// ```mbt check
/// test {
///   inspect(sum_array([1, 2, 3, 4, 5, 6]), content="21")
/// }
/// ```
///
/// # Panics
/// Panics if the `xs` is empty.
pub fn sum_array(xs : Array[Int]) -> Int {
  xs.fold(init=0, (a, b) => a + b)
}
```

### Code Block Types

| Code Block | Behavior |
|------------|----------|
| ` ```mbt check ` | Checked by LSP |
| ` ```mbt test ` | Executed as `test {...}` |
| ` ```moonbit ` | Display only (not executed) |

## Test Commands

```bash
# Run all tests
moon test

# Update snapshots
moon test --update
moon test -u

# Verbose output
moon test -v

# Test specific directory
moon test dirname

# Test specific file
moon test filename

# Filter tests
moon test --filter 'glob'
moon test float/float_test.mbt --filter "Float::*"
moon test float -F "Float::*"  // shortcut

# Coverage
moon coverage analyze
```

## Spec-driven Development

The spec can be written in a readonly `spec.mbt` file with stub code marked as declarations:

```moonbit
///|
declare pub type Yaml

///|
declare pub fn Yaml::to_string(y : Yaml) -> String raise

///|
declare pub impl Eq for Yaml

///|
declare pub fn parse_yaml(s : String) -> Yaml raise
```

Add `spec_easy_test.mbt`, `spec_difficult_test.mbt`, etc. to test the spec functions; everything will be type-checked.

- `declare` is supported for functions, methods, and types
- The `pub type Yaml` line is an intentionally opaque placeholder; the implementer chooses its representation
- Note the spec file can also contain normal code, not just declarations
