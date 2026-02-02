# OxCaml Unboxed Types: Detailed Guide

Unboxed types store values directly without heap allocation or pointer
indirection. They provide C-like performance for numeric code while maintaining
OCaml's type safety.

## Built-in Unboxed Types

### Numeric Types

| Boxed | Unboxed | Kind | Size | Literal |
|-------|---------|------|------|---------|
| `float` | `float#` | `float64` | 64-bit | `#3.14` |
| `int32` | `int32#` | `bits32` | 32-bit | `#42l` |
| `int64` | `int64#` | `bits64` | 64-bit | `#100L` |
| `nativeint` | `nativeint#` | `word` | native | `#50n` |
| `float32` | `float32#` | `float32` | 32-bit | `#1.0s` |
| `int8` | `int8#` | - | 8-bit | `#42s` |
| `int16` | `int16#` | - | 16-bit | `#42S` |
| `int` | `int#` | - | native | `#42` (untagged) |
| - | `char#` | - | 8-bit | `#'a'` |

### Creating Unboxed Values

```ocaml
(* Literals use # prefix *)
let x : float# = #3.14159
let y : int32# = #42l
let z : int64# = #1_000_000L
let w : float32# = #2.5s
let c : char# = #'x'

(* From boxed values *)
let a : float# = Float_u.of_float 3.14
let b : int32# = Int32_u.of_int32 42l
```

---

## Unboxed Records

Records with all unboxed fields are stored flat without indirection:

```ocaml
(* Unboxed record syntax: #{ } *)
type vec3 = #{ x : float#; y : float#; z : float# }

(* Create *)
let v : vec3 = #{ x = #1.0; y = #2.0; z = #3.0 }

(* Access uses .# *)
let get_x (v : vec3) : float# = v.#x

(* Pattern matching *)
let magnitude #{ x; y; z } =
  Float_u.sqrt (
    Float_u.add (Float_u.mul x x)
      (Float_u.add (Float_u.mul y y) (Float_u.mul z z))
  )
```

### Unboxed Record Characteristics

- No heap allocation for the record itself
- Passed by value (copied) to functions
- Cannot be recursive (no self-references)
- All fields must have known layout

---

## Unboxed Tuples

```ocaml
(* Unboxed tuple syntax: #( ) *)
type pair = #(float# * int32#)

let p : #(float# * int32#) = #(#1.0, #42l)

(* Destructure *)
let #(f, i) = p

(* In function signatures *)
let process : #(float# * float#) -> float# = fun #(a, b) ->
  Float_u.add a b
```

---

## Mixed Blocks

Records can mix boxed and unboxed fields:

```ocaml
type particle = {
  name : string;        (* boxed, on heap *)
  mass : float#;        (* unboxed, inline *)
  velocity : float#;    (* unboxed, inline *)
  charge : int32#;      (* unboxed, inline *)
}

let electron = {
  name = "electron";
  mass = #9.109e-31;
  velocity = #0.0;
  charge = #(-1l);
}
```

### Memory Layout

```
┌─────────────────────────────────┐
│ Header                          │
├─────────────────────────────────┤
│ name (pointer to string)        │  ← Boxed field
├─────────────────────────────────┤
│ mass (float64, 8 bytes)         │  ← Unboxed, inline
├─────────────────────────────────┤
│ velocity (float64, 8 bytes)     │  ← Unboxed, inline
├─────────────────────────────────┤
│ charge (int32, 4 bytes + pad)   │  ← Unboxed, inline
└─────────────────────────────────┘
```

---

## The `or_null` Type

A non-allocating option for nullable unboxed values:

```ocaml
type 'a or_null = Null | This of 'a

(* Use with unboxed types - no allocation! *)
let find_float (arr : float# array) idx : float# or_null =
  if idx >= 0 && idx < Array.length arr then
    This arr.(idx)
  else
    Null

(* Pattern match *)
let get_or_default result default =
  match result with
  | Null -> default
  | This x -> x
```

### or_null vs option

```ocaml
(* option allocates Some constructor *)
let f () : float# option = Some #3.14  (* Allocates! *)

(* or_null doesn't allocate *)
let g () : float# or_null = This #3.14  (* No allocation *)
```

---

## Unboxed and Untagged Arrays

Arrays of unboxed and untagged types are packed for memory efficiency:

```ocaml
(* Unboxed float array - tightly packed *)
let floats : float# array = [| #1.0; #2.0; #3.0 |]

(* Access *)
let first = floats.(0)  (* Returns float# *)

(* Unboxed int32/int64 arrays *)
let ints32 : int32# array = [| #1l; #2l; #3l |]
let ints64 : int64# array = [| #1L; #2L; #3L |]

(* Untagged small int arrays (NEW in 5.2.0minus-25) *)
let bytes : int8# array = [| #0s; #1s; #255s |]
let shorts : int16# array = [| #0S; #1S; #32767S |]
let ints : int# array = [| #0; #1; #42 |]
let chars : char# array = [| #'a'; #'b'; #'c' |]
```

### Array Memory Layout

| Array Type | Bytes per Element | Notes |
|------------|-------------------|-------|
| `float# array` | 8 | Custom block, packed |
| `float32# array` | 4 | Custom block, packed |
| `int64# array` | 8 | Custom block, packed |
| `int32# array` | 4 | Custom block, packed |
| `int# array` | native word | Untagged, packed |
| `int16# array` | 2 | Untagged, packed |
| `int8# array` | 1 | Untagged, packed |
| `char# array` | 1 | Same as int8# array |

The untagged int arrays use special block tags to encode the exact length
when the element count doesn't fill a whole word.

---

## Operations on Unboxed Types

### Float Operations (Float_u module)

```ocaml
open Stdlib_stable.Float_u

let compute x y =
  let sum = add x y in
  let product = mul x y in
  let root = sqrt sum in
  div root product
```

### Int32 Operations (Int32_u module)

```ocaml
open Stdlib_stable.Int32_u

let hash x y =
  let a = mul x #31l in
  add a y
```

### Conversion Functions

```ocaml
(* To/from boxed *)
let box (x : float#) : float = Float_u.to_float x
let unbox (x : float) : float# = Float_u.of_float x

(* Between sizes *)
let widen (x : int32#) : int64# = Int64_u.of_int32 (Int32_u.to_int32 x)
```

---

## Kinds and Unboxed Types

Unboxed types have non-`value` kinds:

```ocaml
(* Kind annotations *)
type ('a : float64) float_container = { f : 'a }
type ('a : bits32) int32_container = { i : 'a }

(* Polymorphic over layout *)
type ('a : any) wrapper = { data : 'a }  (* Accepts any layout *)
```

### Kind Constraints

```ocaml
(* Function polymorphic over float64 kind *)
val process : ('a : float64). 'a -> 'a

(* Can be called with float# *)
let result = process #3.14
```

---

## Common Patterns

### High-Performance Numeric Loop

```ocaml
let dot_product (a : float# array) (b : float# array) : float# =
  let len = Array.length a in
  let mutable acc = #0.0 in
  for i = 0 to len - 1 do
    acc <- Float_u.add acc (Float_u.mul a.(i) b.(i))
  done;
  acc
```

### Unboxed Pair Return

```ocaml
let minmax (arr : float# array) : #(float# * float#) =
  let mutable min_val = arr.(0) in
  let mutable max_val = arr.(0) in
  for i = 1 to Array.length arr - 1 do
    let v = arr.(i) in
    if Float_u.compare v min_val < 0 then min_val <- v;
    if Float_u.compare v max_val > 0 then max_val <- v
  done;
  #(min_val, max_val)
```

### Nullable Lookup

```ocaml
type cache = {
  data : float# array;
  valid : bool array;
}

let lookup (c : cache) idx : float# or_null =
  if idx >= 0 && idx < Array.length c.data && c.valid.(idx) then
    This c.data.(idx)
  else
    Null
```

### Mixed Block with Methods

```ocaml
type complex = {
  re : float#;
  im : float#;
}

let complex_add a b = {
  re = Float_u.add a.re b.re;
  im = Float_u.add a.im b.im;
}

let complex_mul a b = {
  re = Float_u.sub (Float_u.mul a.re b.re) (Float_u.mul a.im b.im);
  im = Float_u.add (Float_u.mul a.re b.im) (Float_u.mul a.im b.re);
}
```

---

## C Interop

### External Declarations

```ocaml
(* Unboxed externals - no boxing overhead *)
external sin : (float[@unboxed]) -> (float[@unboxed]) =
  "caml_sin_float" "sin" [@@unboxed] [@@noalloc]

(* With float# directly *)
external fast_sin : float# -> float# =
  "boxed_sin" "unboxed_sin"
```

### C Implementation

```c
#include <caml/mlvalues.h>

// Unboxed version - called directly
double unboxed_sin(double x) {
  return sin(x);
}

// Boxed wrapper
CAMLprim value boxed_sin(value v) {
  return caml_copy_double(unboxed_sin(Double_val(v)));
}
```

---

## Pitfalls

### Cannot Use Unboxed in Polymorphic Context

```ocaml
(* ERROR: 'a defaults to kind value *)
let id x = x
let _ = id #3.14  (* Type error! *)

(* FIX: Add kind annotation *)
let id (type a : float64) (x : a) = x
let _ = id #3.14  (* OK *)
```

### Cannot Store Unboxed in Regular Option

```ocaml
(* ERROR: option expects value kind *)
let bad : float# option = Some #3.14

(* FIX: Use or_null *)
let good : float# or_null = This #3.14
```

### Unboxed Records Are Copied

```ocaml
type point = #{ x : float#; y : float# }

let modify (p : point) : point =
  (* This creates a new point, doesn't modify p *)
  #{ x = Float_u.add p.#x #1.0; y = p.#y }
```

---

## Performance Tips

1. **Use unboxed types in hot loops** - eliminates allocation
2. **Prefer `let mutable` over `ref` for unboxed accumulators**
3. **Use unboxed arrays for numeric data**
4. **Use `or_null` instead of `option` for nullable unboxed**
5. **Use `[@unboxed]` on external declarations**

See also: [SKILL-KINDS.md](SKILL-KINDS.md) for the kind system,
[SKILL-ZERO-ALLOC.md](SKILL-ZERO-ALLOC.md) for allocation-free code.
