# MoonBit IDE Tools

**ALWAYS use `moon ide` for code navigation in MoonBit projects instead of manual file searching, grep, or semantic search.**

## Core Commands

### `moon ide goto-definition`

Find where a symbol is defined.

### `moon ide find-references`

Find all usages of a symbol.

### `moon ide peek-def`

Display definitions inline. More accurate than grep (semantic search).

```bash
# Top-level symbol definition
$ moon ide peek-def String::rev
Found 1 symbols matching 'String::rev':
`pub fn String::rev` in package moonbitlang/core/builtin at ...

# Local symbol definition with location
$ moon ide peek-def Parser -loc src/parse.mbt:46:4
Definition found at file src/parse.mbt
  | ///|
2 | priv struct Parser {
  |             ^^^^^^
  |   bytes : Bytes
  |   mut pos : Int
  | }
```

### `moon ide outline`

List top-level symbols in a package or file.

```bash
# Directory (package) outline
$ moon ide outline .
spec.mbt:
 L003 | pub(all) enum CStandard {
       ...
 L013 | pub(all) struct Position {
       ...

# Single file outline
$ moon ide outline parser.mbt
```

### `moon ide find-references`

Find all references to a symbol.

```bash
$ moon ide find-references TranslationUnit
```

### `moon ide rename`

Rename a symbol project-wide. Prefer `--loc` when symbol names are ambiguous.

```bash
$ moon ide rename compute_sum calculate_sum --loc math_utils.mbt:2

*** Begin Patch
*** Update File: cmd/main/main.mbt
@@
 ///|
 fn main {
-  println(@math_utils.compute_sum(1, 2))
+  println(@math_utils.calculate_sum(1, 2))
 }
*** Update File: math_utils.mbt
@@
 ///|
-pub fn compute_sum(a: Int, b: Int) -> Int {
+pub fn calculate_sum(a: Int, b: Int) -> Int {
   a + b
 }
*** Update File: math_utils_test.mbt
@@
 ///|
 test {
-  inspect(@math_utils.compute_sum(1, 2))
+  inspect(@math_utils.calculate_sum(1, 2))
 }
*** End Patch
```

### `moon ide hover`

Get type information at a specific location.

```bash
$ moon ide hover filter --loc hover.mbt:14
test {
  let a: Array[Int] = [1]
  inspect(a.filter((x) => {x > 1}))
            ^^^^^^
            ```moonbit
            fn[T] Array::filter(self : Array[T], f : (T) -> Bool raise?) -> Array[T] raise?
            ```
            ...
}
```

## Query Syntax

Symbol lookup uses a two-part query system:

### 1. Symbol Name Query (`-query`)

Fuzzy search for symbol names with package filtering support:

```bash
# Find any symbol named 'symbol'
moon ide goto-definition -query 'symbol'

# Find methods of a specific type
moon ide goto-definition -query 'Type::method'

# Find symbol in specific package using @pkg prefix
moon ide goto-definition -query '@moonbitlang/x encode'

# Find symbol in multiple packages (searches in pkg1 OR pkg2)
moon ide goto-definition -query '@username/mymodule/pkg1 @username/mymodule/pkg2 helper'

# Find symbol in nested package
moon ide goto-definition -query '@username/mymodule/mypkg helper'
```

**Supported symbols**: functions, constants, let bindings, types, structs, enums, traits

### 2. Tag-based Filtering (`-tags`)

Pre-filter symbols by characteristics:

**Visibility tags**:
- `pub` - Public symbols
- `pub all` - Public structs with all public fields
- `pub open` - Public traits with all methods public
- `priv` - Private symbols

**Symbol type tags**:
- `type` - Type definitions (struct, enum, typealias, abstract)
- `error` - Error type definitions
- `enum` - Enum definitions and variants
- `struct` - Struct definitions
- `alias` - Type/function/trait aliases
- `let` - Top-level let bindings
- `const` - Constant definitions
- `fn` - Function definitions
- `trait` - Trait definitions
- `impl` - Trait implementations
- `test` - Named test functions

**Combine tags with logical operators**:

```bash
# Public functions only
moon ide goto-definition -tags 'pub fn' -query 'my_func'

# Functions or constants
moon ide goto-definition -tags 'fn | const' -query 'helper'

# Public functions or constants
moon ide goto-definition -tags 'pub (fn | const)' -query 'api'

# Public types or traits
moon ide goto-definition -tags 'pub (type | trait)' -query 'MyType'
```

### Practical Examples

```bash
# Find public function definition
moon ide goto-definition -tags 'pub fn' -query 'maximum'

# Find all references to a struct
moon ide find-references -tags 'struct' -query 'Rectangle'

# Find trait implementations
moon ide goto-definition -tags 'impl' -query 'Show for MyType'

# Find errors in specific package
moon ide goto-definition -tags 'error' -query '@mymodule/parser ParseError'

# Find symbol across multiple packages
moon ide goto-definition -query '@moonbitlang/x @moonbitlang/core encode'

# Combine package filtering with tags
moon ide goto-definition -tags 'pub fn' -query '@username/myapp helper'
```

### Query Processing Order

1. Filter symbols by `-tags` conditions
2. Extract package scope from `@pkg` prefixes in `-query`
3. Fuzzy match remaining symbols by name
4. Return top 3 best matches with location information

**Best Practice**: Start with `-tags` to reduce noise, then use `@pkg` prefixes in `-query` to scope by package.
