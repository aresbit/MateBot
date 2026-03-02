# MoonBit Language Fundamentals

## Core Facts

- **Expression-oriented**: `if`, `match`, loops return values; last expression is the return value
- **References by default**: Arrays/Maps/structs mutate via reference; use `Ref[T]` for primitive mutability
- **Errors**: Functions declare `raise ...`; use `try?` for `Result` or `try { } catch { }` to handle
- **Blocks**: Separate top-level items with `///|`. Generate code block-by-block
- **Visibility**: `fn` private by default; `pub` exposes read/construct as allowed; `pub(all)` allows external construction
- **Naming convention**: lower_snake for values/functions; UpperCamel for types/enums; enum variants start UpperCamel
- **Packages**: No `import` in code files; call via `@alias.fn`. Configure imports in `moon.pkg`
- **Placeholders**: `...` is a valid placeholder in MoonBit code for incomplete implementations
- **Global values**: immutable by default and generally require type annotations
- **Garbage collection**: MoonBit has a GC, there is no lifetime annotation, there's no ownership system

## Integers, Char

MoonBit supports `Byte`, `Int16`, `Int`, `UInt16`, `UInt`, `Int64`, `UInt64`, etc. When the type is known, the literal can be overloaded:

```moonbit
///|
test "integer and char literal overloading" {
  let a0 = 1 // a is Int by default
  let (int, uint, uint16, int64, byte) : (Int, UInt, UInt16, Int64, Byte) = (
    1, 1, 1, 1, 1,
  )
  assert_eq(int, uint16.to_int())
  let a1 : Int = 'b' // unicode value
  let a2 : Char = 'b'
}
```

## Bytes (Immutable)

```moonbit
///|
test "bytes literals overloading and indexing" {
  let b0 : Bytes = b"abcd"
  let b1 : Bytes = "abcd" // b" prefix is optional when type is known
  let b2 : Bytes = [0xff, 0x00, 0x01] // Array literal overloading
  guard b0 is [b'a', ..] && b0[1] is b'b' else {
    // Bytes can be pattern matched as BytesView and indexed
    fail("unexpected bytes content")
  }
}
```

## Array (Resizable)

```moonbit
///|
test "array literals overloading" {
  let a0 : Array[Int] = [1, 2, 3] // resizable
  let a1 : FixedArray[Int] = [1, 2, 3] // Fixed size
  let a2 : ReadOnlyArray[Int] = [1, 2, 3]
  let a3 : ArrayView[Int] = [1, 2, 3]
}
```

## String (Immutable UTF-16)

`s[i]` returns a code unit (`UInt16`), `s.get_char(i)` returns `Char?`.

```moonbit
///|
test "string indexing and utf8 encode/decode" {
  let s = "hello world"
  let b0 : UInt16 = s[0]
  guard b0 is ('\n' | 'h' | 'b' | 'a'..='z') && s is [.. "hello", .. rest] else {
    fail("unexpected string content")
  }
  guard rest is " world"  // otherwise will crash (guard without else)

  // Using get_char for Option handling
  let b1 : Char? = s.get_char(0)
  assert_true(b1 is Some('a'..='z'))

  // ⚠️ Important: Variables won't work with direct indexing
  let eq_char : Char = '='
  // s[0] == eq_char // ❌ Won't compile - eq_char is not a literal
  // Use: s[0] == '=' or s.get_char(0) == Some(eq_char)
  let bytes = @utf8.encode("中文") // utf8 encode package is in stdlib
  assert_true(bytes is [0xe4, 0xb8, 0xad, 0xe6, 0x96, 0x87])
  let s2 : String = @utf8.decode(bytes)
  assert_true(s2 is "中文")
  for c in "中文" {
    let _ : Char = c // unicode safe iteration
    println("char: \{c}")
  }
}
```

### String Interpolation && StringBuilder

MoonBit uses `\{}` for string interpolation, for custom types, they need to implement trait `Show`.

```moonbit
///|
test "string interpolation basics" {
  let name : String = "Moon"
  let config = { "cache": 123 }
  let version = 1.0
  println("Hello \{name} v\{version}") // "Hello Moon v1.0"
  // ❌ Wrong - quotes inside interpolation not allowed:
  // println("  - Checking if 'cache' section exists: \{config["cache"]}")
  // ✅ Correct - extract to variable first:
  let has_key = config["cache"]
  println("  - Checking if 'cache' section exists: \{has_key}")
  let sb = StringBuilder::new()
  sb
  ..write_char('[') // dotdot for imperative method chaining
  ..write_view([1, 2, 3].map(x => "\{x}").join(","))
  ..write_char(']')
  inspect(sb.to_string(), content="[1,2,3]")
}
```

**Important**: Expressions inside `\{}` can only be _basic expressions_ (no quotes, newlines, or nested interpolations).

### Multiple line strings

```moonbit
///|
test "multi-line string literals" {
  let multi_line_string : String =
    #|Hello "world"
    #|World
    #|
  let multi_line_string_with_interp : String =
    $|Line 1 ""
    $|Line 2 \{1+2}
    $|
  // no escape in `#|`, only escape '\{..}` in `$|`
  assert_eq(multi_line_string, "Hello \"world\"\nWorld\n")
  assert_eq(multi_line_string_with_interp, "Line 1 \"\"\nLine 2 3\n")
}
```

## Map (Mutable, Insertion-Order Preserving)

```moonbit
///|
test "map literals and common operations" {
  // Map literal syntax
  let map : Map[String, Int] = { "a": 1, "b": 2, "c": 3 }

  // Empty map
  let empty : Map[String, Int] = {}

  // From array of pairs
  let from_pairs : Map[String, Int] = Map::from_array([("x", 1), ("y", 2)])

  // Set/update value
  map["new-key"] = 3
  map["a"] = 10 // Updates existing key

  // Get value - returns Option[T]
  guard map is { "new-key": 3, "missing"? : None, .. } else {
    fail("unexpected map contents")
  }

  // Direct access (panics if key missing)
  let value : Int = map["a"] // value = 10

  // Iteration preserves insertion order
  for k, v in map {
    println("\{k}: \{v}")
  }

  // Other common operations
  map.remove("b")
  guard map is { "a": 10, "c": 3, "new-key": 3, .. } && map.length() == 3 else {
    fail("unexpected map contents after removal")
  }
}
```

## View Types

**Key Concept**: View types (`StringView`, `BytesView`, `ArrayView[T]`) are zero-copy, non-owning read-only slices created with the `[:]` syntax.

- `String` → `StringView` via `s[:]` or `s[start:end]` or `s[start:]` or `s[:end]`
- `Bytes` → `BytesView` via `b[:]` or `b[start:end]`, etc.
- `Array[T]`, `FixedArray[T]`, `ReadOnlyArray[T]` → `ArrayView[T]` via `a[:]` or `a[start:end]`, etc.

**Important**: StringView slice is slightly different due to unicode safety: `s[a:b]` may raise an error at surrogate boundaries.

## User defined types(`enum`, `struct`)

```moonbit
///|
enum Tree[T] {
  Leaf(T) // Unlike Rust, no comma here
  Node(left~ : Tree[T], T, right~ : Tree[T]) // enum can use labels
} derive(Show, ToJson) // derive traits for Tree

///|
pub fn Tree::sum(tree : Tree[Int]) -> Int {
  match tree {
    Leaf(x) => x
    Node(left~, x, right~) => left.sum() + x + right.sum()
  }
}

///|
struct Point {
  x : Int
  y : Int
} derive(Show, ToJson) // derive traits for Point

///|
test "user defined types: enum and struct" {
  @json.inspect(Point::{ x: 10, y: 20 }, content={ "x": 10, "y": 20 })
}
```

## Functional `for` loop

```moonbit
///|
pub fn binary_search(arr : ArrayView[Int], value : Int) -> Result[Int, Int] {
  let len = arr.length()
  for i = 0, j = len; i < j; {
    let h = i + (j - i) / 2
    if arr[h] < value {
      continue h + 1, j
    } else {
      continue i, h
    }
  } else {
    if i < len && arr[i] == value {
      Ok(i)
    } else {
      Err(i)
    }
  } where {
    invariant: 0 <= i && i <= j && j <= len,
    invariant: i == 0 || arr[i - 1] < value,
    invariant: j == len || arr[j] >= value,
    reasoning: (
      #|For a sorted array, the boundary invariants are witnesses...
    ),
  }
}
```

You are *STRONGLY ENCOURAGED* to use functional `for` loops instead of imperative loops *WHENEVER POSSIBLE*.

## Label and Optional Parameters

```moonbit
///|
fn g(
  positional : Int,
  required~ : Int,
  optional? : Int, // no default => Option
  optional_with_default? : Int = 42, // default => plain Int
) -> String {
  "\{positional},\{required},\{optional},\{optional_with_default}"
}

///|
test {
  inspect(g(1, required=2), content="1,2,None,42")
  inspect(g(1, required=2, optional=3), content="1,2,Some(3),42")
  inspect(g(1, required=4, optional_with_default=100), content="1,4,None,100")
}
```

## Error Handling

```moonbit
///|
/// Declare error type
suberror ParseError {
  InvalidEof
  InvalidChar(Char)
}

///|
/// Declare with raise, auto-propagates
fn parse(s: String) -> Int raise ParseError {
  if s.is_empty() { raise ParseError::InvalidEof }
  // parsing logic
}

///|
/// Convert to Result
let result : Result[Int, ParseError] = try? parse(s)

///|
/// Handle with try-catch
parse(s) catch {
  ParseError::InvalidEof => -1
  _ => 0
}
```
