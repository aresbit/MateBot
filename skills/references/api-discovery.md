# MoonBit API Discovery

**CRITICAL**: `moon doc '<query>'` is your PRIMARY tool for discovering available APIs, functions, types, and methods in MoonBit.

## Why moon doc Over Other Tools

- **More powerful and accurate** than `grep_search`, `semantic_search`, or any file-based searching tools
- **Semantic understanding** - knows about packages, types, and methods
- **Always prefer `moon doc`** over other approaches when exploring what APIs are available

## Query Syntax

### Empty Query

```bash
# In a module: shows all available packages in current module
# In a package: shows all symbols in current package
# Outside package: shows all available packages
moon doc ''
```

### Function/Value Lookup

```bash
# Find function or value
moon doc "[@pkg.]value_or_function_name"

# Example
moon doc "sum"
moon doc "@json.parse"
```

### Type Lookup

```bash
# Find type and its methods
moon doc "[@pkg.]Type_name"

# Example
moon doc "String"
moon doc "@buffer.Buffer"
```

### Method/Field Lookup

```bash
# Find methods on a type
moon doc "[@pkg.]Type_name::method_or_field_name"

# Example
moon doc "String::rev"
moon doc "Array::map"
```

### Package Exploration

```bash
# Show all symbols in a package
moon doc "@pkg"

# Examples
moon doc "@json"           # Explore @json package
moon doc "@encoding/utf8"  # Explore nested package
```

### Globbing

Use `*` wildcard for partial matches:

```bash
# Find all String methods with "rev" in name
moon doc "String::*rev*"
```

## Examples

### Search for String Methods

```bash
$ moon doc "String"

type String

  pub fn String::add(String, String) -> String
  pub fn String::at(String, Int) -> Int
  pub fn String::rev(String) -> String
  # ... more methods omitted ...
```

### List Symbols in Package

```bash
$ moon doc "@buffer"
moonbitlang/core/buffer

fn from_array(ArrayView[Byte]) -> Buffer
fn from_bytes(Bytes) -> Buffer
pub fn new(size_hint? : Int) -> Buffer
  Creates a new extensible buffer with specified initial capacity...
```

### Specific Function Details

```bash
$ moon doc "@buffer.new"
package "moonbitlang/core/buffer"

pub fn new(size_hint? : Int) -> Buffer
  Creates a new extensible buffer with specified initial capacity.
  If the initial capacity is less than 1, the buffer will be
  initialized with capacity 1.
```

### Glob Pattern

```bash
$ moon doc "String::*rev*"
package "moonbitlang/core/string"

pub fn String::rev(String) -> String
  Returns a new string with the characters in reverse order...

pub fn String::rev_find(String, StringView) -> Int?
  Returns the offset of the last occurrence of the substring...
```

## Workflow for API Discovery

1. **Finding functions**: Use `moon doc "@pkg.function_name"` before grep searching
2. **Exploring packages**: Use `moon doc "@pkg"` to see what's available
3. **Method discovery**: Use `moon doc "Type::method"` to find methods
4. **Type inspection**: Use `moon doc "TypeName"` to see type definition
5. **Package exploration**: Use `moon doc ""` at module root to see all packages
6. **Globbing**: Use `*` wildcard for partial matches

## Best Practice

When implementing a feature, **start with `moon doc` queries** to discover available APIs before writing code. This is faster and more accurate than searching through files.
