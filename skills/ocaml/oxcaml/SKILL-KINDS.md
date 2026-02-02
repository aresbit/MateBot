# OxCaml Kinds: Detailed Guide

Kinds classify types by their runtime representation (layout). They determine
how values are stored, passed, and what operations are valid.

## Kind Hierarchy

```
any                              (* Top kind - any layout *)
├── value                        (* Standard OCaml boxed values *)
│   └── immediate                (* Unboxed integers, no GC scanning *)
│       └── immediate64          (* Immediate on 64-bit only *)
├── void                         (* Uninhabited, zero size *)
├── float64                      (* Unboxed 64-bit float *)
├── float32                      (* Unboxed 32-bit float *)
├── bits32                       (* Unboxed 32-bit integer *)
├── bits64                       (* Unboxed 64-bit integer *)
├── word                         (* Native word size *)
└── vec128 / vec256              (* SIMD vectors *)
```

## Basic Kind Annotations

### On Type Definitions

```ocaml
(* Abstract type with specific layout *)
type t : float64

(* Type alias preserving layout *)
type my_float : float64 = float#

(* Parameterized with kind constraint *)
type ('a : value) boxed_list = 'a list
type ('a : float64) float_pair = 'a * 'a
```

### On Type Parameters

```ocaml
(* Single parameter *)
type ('a : bits32) container = { value : 'a }

(* Multiple parameters with different kinds *)
type ('a : value, 'b : float64) mixed = {
  boxed : 'a;
  unboxed : 'b;
}
```

### In Signatures

```ocaml
(* Kind-annotated polymorphism *)
val id : ('a : value). 'a -> 'a
val id_float : ('a : float64). 'a -> 'a

(* Mixed *)
val convert : ('a : bits32). 'a -> ('b : bits64). 'b
```

### On Locally Abstract Types

```ocaml
let process (type a : float64) (x : a) : a = x

let example () =
  process #3.14  (* a instantiated to float# *)
```

---

## Kind Abbreviations

Common kind patterns have shorthand names:

```ocaml
value           (* Boxed OCaml values, GC-managed *)
immediate       (* Tagged integers: int, char, bool, etc. *)
immediate64     (* Immediate on 64-bit, boxed on 32-bit *)
mutable_data    (* value mod non_float - records with mutable fields *)
immutable_data  (* value mod non_float immutable *)
```

### What Types Have Which Kinds?

| Type | Kind |
|------|------|
| `int`, `char`, `bool`, `unit` | `immediate` |
| `float` | `value` (but special float array optimization) |
| `string`, `'a list`, `'a option` | `value` |
| `int32`, `int64`, `nativeint` | `value` (boxed) |
| `float#` | `float64` |
| `int32#` | `bits32` |
| `int64#` | `bits64` |
| `float32#` | `float32` |
| `nativeint#` | `word` |
| `int8x16#`, etc. | `vec128` |
| `int8x32#`, etc. | `vec256` |
| `int8# array` | `value` (specialized subkind) |
| `int16# array` | `value` (specialized subkind) |
| `int# array` | `value` (specialized subkind) |

---

## Kind Products

Unboxed tuples have product kinds:

```ocaml
(* Unboxed pair of float# and int32# *)
type pair : float64 & bits32

(* Three-element product *)
type triple : float64 & float64 & bits32

(* In type parameters *)
type ('a : float64 & bits32) wrapper = { data : 'a }
```

### Creating Product Values

```ocaml
let p : #(float# * int32#) = #(#3.14, #42l)
(* p has kind float64 & bits32 *)
```

---

## Mode Bounds on Kinds

Kinds can include mode constraints:

```ocaml
(* Type that must be global *)
type t : value mod global

(* Type that is always portable *)
type portable_t : value mod portable

(* Type that crosses locality *)
type crosser : value mod global local
```

### Mode Bound Meanings

| Bound | Meaning |
|-------|---------|
| `mod global` | Cannot be local |
| `mod portable` | Safe for cross-thread |
| `mod external_` | GC ignores it (immediate) |
| `mod non_float` | Not a float (for array optimization) |
| `mod immutable` | No mutable fields |

---

## Computing Kinds of User Types

### Records

```ocaml
(* Immutable record with value fields *)
type point = { x : int; y : int }
(* Kind: immutable_data with x, y *)

(* Mutable record *)
type counter = { mutable count : int }
(* Kind: mutable_data with count *)

(* Unboxed record *)
type vec2 = #{ x : float#; y : float# }
(* Kind: float64 & float64 mod everything *)
```

### Variants

```ocaml
(* All-constant constructors *)
type color = Red | Green | Blue
(* Kind: immediate *)

(* With data *)
type 'a option = None | Some of 'a
(* Kind: immutable_data with 'a *)

(* Mutable field in constructor *)
type 'a ref = { mutable contents : 'a }
(* Kind: mutable_data with contents *)
```

### Tuples

```ocaml
(* Boxed tuple *)
type pair = int * int
(* Kind: immutable_data with int, int *)

(* Unboxed tuple *)
type upair = #(int * int)
(* Kind: value & value mod everything *)
```

---

## Kind Polymorphism with Templates

Since OxCaml doesn't yet have first-class kind polymorphism, use `ppx_template`:

```ocaml
(* Define for multiple kinds *)
let%template id (type a : k) (x : a) : a = x
[@@kind k = (value, float64, bits32, bits64)]

(* Generates: id, id__float64, id__bits32, id__bits64 *)

(* Use with kind attribute *)
let f x = (id [@kind float64]) x
```

---

## Kind Inference

The compiler infers kinds when possible:

```ocaml
(* 'a inferred as value (default) *)
let f x = x
(* val f : 'a -> 'a *)

(* 'a inferred from context *)
let g (x : float#) = x
(* val g : float# -> float# *)
(* Internally: ('a : float64). 'a -> 'a instantiated *)
```

### Flexible vs Rigid Variables

```ocaml
(* Flexible: infers kind from usage *)
let f x = (x : float#)
(* x must have kind float64 *)

(* Rigid: kind specified at binding *)
let g (type a : float64) (x : a) = x
(* a is exactly float64 *)
```

---

## Subkinding

More specific kinds can be used where general ones are expected:

```ocaml
immediate ≤ immediate64 ≤ value ≤ any
float64 ≤ any
bits32 ≤ any
(* etc. *)

(* Can pass immediate where value expected *)
val f : ('a : value). 'a -> 'a
let _ = f 42  (* int is immediate, which ≤ value *)
```

---

## Kind Errors and Solutions

### "This type has kind X but was expected to have kind Y"

```ocaml
(* ERROR: float# has kind float64, not value *)
let f (x : 'a) = x
let _ = f #3.14

(* FIX: Add kind annotation *)
let f (type a : float64) (x : a) = x
let _ = f #3.14

(* OR use template *)
let%template f (type a : k) (x : a) = x
[@@kind k = (value, float64)]
```

### "Cannot use type with kind X in this context"

```ocaml
(* ERROR: list elements must be value *)
let bad : float# list = [#1.0; #2.0]

(* FIX: Box the values *)
let good : float list = [1.0; 2.0]

(* OR use unboxed array *)
let also_good : float# array = [| #1.0; #2.0 |]
```

### "The layout of 'a is X because..."

```ocaml
(* ERROR: conflicting kind constraints *)
let bad (type a : value) (x : a) : float# = x

(* The error explains: 'a has kind value, but float# needs float64 *)
```

---

## Common Patterns

### Kind-Polymorphic Wrapper

```ocaml
type%template ('a : k) cell = { mutable value : 'a }
[@@kind k = (value, float64, bits32)]

let%template get (type a : k) (c : a cell) : a = c.value
[@@kind k = (value, float64, bits32)]

let%template set (type a : k) (c : a cell) (v : a) : unit = c.value <- v
[@@kind k = (value, float64, bits32)]
```

### Constraint Propagation

```ocaml
(* Container constrains element kind *)
type ('a : value) box = { contents : 'a }

(* Function inherits constraint *)
let unbox (b : 'a box) : 'a = b.contents
(* 'a implicitly has kind value *)
```

### Mixed Kind Records

```ocaml
type measurement = {
  label : string;        (* value *)
  value : float#;        (* float64, stored unboxed *)
  precision : int32#;    (* bits32, stored unboxed *)
}

(* Efficient: unboxed fields inline, no extra indirection *)
```

---

## Summary Table

| Kind | Examples | GC Scanned | Size |
|------|----------|------------|------|
| `value` | `int list`, `string` | Yes | 1 word |
| `immediate` | `int`, `bool`, `char` | No | 1 word |
| `float64` | `float#` | No | 8 bytes |
| `float32` | `float32#` | No | 4 bytes |
| `bits32` | `int32#` | No | 4 bytes |
| `bits64` | `int64#` | No | 8 bytes |
| `word` | `nativeint#` | No | native |
| `void` | (uninhabited) | - | 0 |
| `any` | (any of above) | Varies | Varies |

See also: [SKILL-UNBOXED.md](SKILL-UNBOXED.md) for unboxed types,
[SKILL-TEMPLATES.md](SKILL-TEMPLATES.md) for kind polymorphism.
