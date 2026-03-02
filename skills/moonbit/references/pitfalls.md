# MoonBit Common Pitfalls

This document lists common mistakes AI makes when generating MoonBit code.

## Syntax Mistakes

### Type Parameter Position

```moonbit
///| NG: fn identity[T] is old syntax
fn identity[T](val: T) -> T { val }

///| OK: Type parameter comes right after fn
fn[T] identity(val: T) -> T { val }
```

### raise Syntax

```moonbit
///|
/// NG: -> T!Error was removed
fn parse(s: String) -> Int!Error { ... }

///|
/// OK: Use raise keyword
fn parse(s: String) -> Int raise Error { ... }
```

`Int raise` is shorthand for `Int raise Error`. async fn implicitly raises by default; use `noraise` to enforce no errors.

### Macro Calls

```moonbit
///|
/// NG: ! suffix was removed
assert_true!(true)

///|
/// OK
assert_true(true)
```

### Multi-line Text

```moonbit
let text =
  #|line 1
  #|line 2
```

### Comments and Block Separators

`///|` is a block separator. `///` comments attach to the following `///|` block.

```moonbit
///|
/// This function is foo
fn foo() -> Unit { ... }

///|
/// This function is bar
fn bar() -> Unit { ... }
```

Avoid consecutive `///|` at the file beginning as they create separate blocks.

## Common Logic Errors

### 1. Don't use uppercase for variables/functions

Uppercase names are reserved for types and enum variants.

```moonbit
// ❌ Wrong
let MyVariable = 10
fn MyFunction() -> Unit { }

// ✅ Correct
let my_variable = 10
fn my_function() -> Unit { }
```

### 2. Don't forget `mut` for mutable record fields

Fields are immutable by default. Note that Arrays typically do NOT need `mut` unless completely reassigning to the variable.

```moonbit
// ❌ Wrong - field is immutable
struct Config {
  value: Int
}

// ✅ Correct
struct Config {
  mut value: Int
}
```

### 3. `mut` is only for reassignment, not field mutation

```moonbit
// ✅ This works - Array methods mutate in place
let arr = [1, 2, 3]
arr.push(4)  // No mut needed!

// ❌ This needs mut
let mut arr = [1, 2, 3]
arr = [4, 5, 6]  // Reassignment needs mut
```

### 4. Don't use `return` unnecessarily

The last expression is the return value.

```moonbit
// ❌ Unnecessary return
fn add(a: Int, b: Int) -> Int {
  return a + b
}

// ✅ Correct
fn add(a: Int, b: Int) -> Int {
  a + b
}
```

### 5. Don't create methods without Type:: prefix

Methods need explicit type prefix.

```moonbit
// ❌ Wrong
fn area(self: Rectangle) -> Double { ... }

// ✅ Correct
fn Rectangle::area(self: Rectangle) -> Double { ... }
```

### 6. Don't forget to handle array bounds

Use `get()` for safe access.

```moonbit
// ❌ May panic
let x = arr[0]

// ✅ Safe access
let x = arr.get(0)  // Returns Option[T]
```

### 7. Don't forget @package prefix when calling functions from other packages

```moonbit
// ❌ Wrong
let result = parse_json(text)

// ✅ Correct
let result = @json.parse(text)
```

### 8. Don't use ++ or -- (not supported)

```moonbit
// ❌ Not supported
i++
i--

// ✅ Use instead
i = i + 1
i += 1
i -= 1
```

### 9. Don't add explicit `try` for error-raising functions

Errors propagate automatically (unlike Swift).

```moonbit
// ❌ Wrong - no try needed
fn process() -> Int raise Error {
  let x = try parse("123")
  x + 1
}

// ✅ Correct - errors propagate automatically
fn process() -> Int raise Error {
  let x = parse("123")  // Error propagates automatically
  x + 1
}
```

### 10. Legacy syntax deprecation

Older code may use `function_name!(...)` or `function_name(...)?` - these are deprecated.

```moonbit
// ❌ Deprecated
assert_true!(condition)
let result = parse()?

// ✅ Correct
assert_true(condition)
let result = try? parse()  // For Result conversion
```

### 11. Prefer range `for` loops over C-style

```moonbit
// ❌ C-style (works but not idiomatic)
let mut i = 0
while i < n {
  ...
  i += 1
}

// ✅ Range for (more idiomatic)
for i in 0..<n { ... }
for j in 0..=6 { ... }  // inclusive
```

### 12. Async

MoonBit has no `await` keyword; do not add it. Async functions and tests are characterized by those which call other async functions.

```moonbit
// ❌ Wrong - no await
async fn fetch_data() -> Data {
  let result = await http_get("/api")
  result
}

// ✅ Correct
async fn fetch_data() -> Data {
  let result = http_get("/api")  // Just call it
  result
}
```

## Pattern Matching

```moonbit
///|
/// Destructure arrays with rest patterns
fn process_array(arr : Array[Int]) -> String {
  match arr {
    [] => "empty"
    [single] => "one: \{single}"
    [first, .. _middle, last] => "first: \{first}, last: \{last}"
  }
}

///|
fn analyze_point(point : Point) -> String {
  match point {
    { x: 0, y: 0 } => "origin"
    { x, y } if x == y => "on diagonal"
    { x, .. } if x < 0 => "left side"
    _ => "other"
  }
}
```

## String Indexing Pitfall

```moonbit
// ❌ Wrong - s[i] returns UInt16, not Char
let c : Char = s[0]

// ✅ Correct - use get_char for Option[Char]
let c : Char? = s.get_char(0)

// Or pattern match
if s[0] == 'a' { ... }  // ✅ Works with char literals
```
