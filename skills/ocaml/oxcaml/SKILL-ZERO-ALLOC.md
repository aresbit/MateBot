# OxCaml Zero-Alloc Checking: Detailed Guide

The `[@zero_alloc]` attribute enables compile-time verification that functions
don't allocate on the OCaml heap, ensuring predictable performance in hot paths.

## Basic Usage

### Annotating Functions

```ocaml
(* Simple zero-alloc function *)
let[@zero_alloc] add x y = x + y

(* With explicit type *)
let[@zero_alloc] multiply : int -> int -> int = fun x y -> x * y
```

### What Counts as Allocation?

**Forbidden** (causes check failure):
- Heap allocation: tuples, records, variants, closures, etc.
- Boxing: `int64`, `float` operations that box
- Raising exceptions with backtrace (unless in error path)
- Indirect calls (function passed as argument)

**Allowed**:
- Stack allocation: `stack_`, `local_`
- Immediate values: `int`, `bool`, `char`
- Unboxed operations: `float#`, `int32#`, etc.
- Direct calls to known zero-alloc functions

---

## Annotation Variants

### Basic `[@zero_alloc]`

- Checked in all builds
- Uses "relaxed" semantics (allows allocation on exception paths)

```ocaml
let[@zero_alloc] find arr idx =
  if idx < 0 || idx >= Array.length arr then
    raise (Invalid_argument "out of bounds")  (* Allowed - exception path *)
  else
    arr.(idx)
```

### `[@zero_alloc strict]`

- No allocation on any path, including exceptions

```ocaml
let[@zero_alloc strict] add x y = x + y  (* Must not allocate anywhere *)
```

### `[@zero_alloc opt]`

- Only checked in optimized builds (`-zero-alloc-check all`)
- Useful when inlining is required

```ocaml
let[@zero_alloc opt] complex_op x =
  (* Requires inlining to be zero-alloc *)
  helper1 x |> helper2 |> helper3
```

### `[@zero_alloc assume]`

- Not checked - trusted to be zero-alloc
- Use sparingly

```ocaml
let[@cold][@zero_alloc assume] log_error msg =
  Printf.eprintf "Error: %s\n" msg

let[@zero_alloc] process x =
  if is_error x then log_error "bad input";  (* Allowed due to assume *)
  compute x
```

### `[@zero_alloc assume error]`

- Marks function as error path - all code after it ignored

```ocaml
let[@cold][@zero_alloc assume error] fatal msg =
  Printf.eprintf "Fatal: %s\n" msg;
  exit 1

let[@zero_alloc] process x =
  if is_fatal x then fatal "unrecoverable";
  (* Code after fatal () is ignored for zero_alloc purposes *)
  compute x
```

### `[@zero_alloc assume_unless_opt]`

- Assumed in debug builds, checked in optimized builds

```ocaml
let[@zero_alloc assume_unless_opt] helper x =
  (* Assumed zero-alloc in debug, checked with -zero-alloc-check all *)
  ...
```

---

## Stack Allocation is Allowed

```ocaml
let[@zero_alloc] with_pair x y f =
  let local_ p = stack_ (x, y) in  (* OK: stack allocation *)
  f p

let[@zero_alloc] sum_pairs arr =
  let local_ total = ref 0 in  (* OK: local ref *)
  for i = 0 to Array.length arr / 2 - 1 do
    total := !total + arr.(i * 2) + arr.(i * 2 + 1)
  done;
  !total
```

---

## In Signatures

### Basic Signature Annotation

```ocaml
val[@zero_alloc] fast_hash : string -> int

(* Implementation must be zero-alloc *)
let fast_hash s = ...  (* Checked even without annotation here *)
```

### With Arity

```ocaml
(* Specify how many arguments before zero-alloc applies *)
val[@zero_alloc arity 2] partial_apply : int -> int -> int

(* Only fully applied calls are zero-alloc *)
let f = partial_apply 1  (* May allocate closure *)
let x = partial_apply 1 2  (* Zero-alloc *)
```

### Hidden Type Aliases

```ocaml
type t = int -> int
val[@zero_alloc arity 1] f : t  (* Need arity since t hides arrow *)
```

---

## Interaction with Other Features

### With Unboxed Types

```ocaml
let[@zero_alloc] unboxed_add (x : float#) (y : float#) : float# =
  Float_u.add x y  (* No boxing - zero-alloc *)
```

### With Inlining

```ocaml
let[@inline always][@zero_alloc] helper x = x + 1

let[@zero_alloc] process arr =
  for i = 0 to Array.length arr - 1 do
    arr.(i) <- helper arr.(i)  (* Inlined, so zero-alloc *)
  done
```

### With External Functions

```ocaml
(* [@@noalloc] on externals is trusted *)
external fast_memcpy : bytes -> bytes -> int -> unit =
  "caml_fast_memcpy" [@@noalloc]

let[@zero_alloc] copy src dst len =
  fast_memcpy dst src len  (* OK: external marked noalloc *)
```

---

## File-Level Annotations

### `[@@@zero_alloc all]`

All functions in file must be zero-alloc:

```ocaml
[@@@zero_alloc all]

let add x y = x + y      (* Checked *)
let mul x y = x * y      (* Checked *)

let[@zero_alloc ignore] debug x =
  Printf.printf "%d\n" x  (* Exempted *)
```

### `[@@@zero_alloc check]` / `[@@@zero_alloc check_all]`

Control checking mode for file:

```ocaml
[@@@zero_alloc check_all]  (* Check opt annotations too *)
```

---

## On Applications

Annotate specific call sites:

```ocaml
let[@zero_alloc] process x =
  (* Assume this specific call is zero-alloc *)
  (external_func [@zero_alloc assume]) x
```

---

## Common Patterns

### Zero-Alloc Hot Loop

```ocaml
let[@zero_alloc] sum_array arr =
  let mutable total = 0 in  (* No allocation *)
  for i = 0 to Array.length arr - 1 do
    total <- total + arr.(i)
  done;
  total
```

### Zero-Alloc with Error Handling

```ocaml
let[@cold][@zero_alloc assume error] report_error code =
  Printf.eprintf "Error %d\n" code;
  Error code

let[@zero_alloc] parse_packet buf =
  if Buffer.length buf < 4 then report_error 1
  else
    let header = ... in
    Ok header
```

### Zero-Alloc Option Handling with or_null

```ocaml
let[@zero_alloc] find_value (arr : float# array) idx : float# or_null =
  if idx >= 0 && idx < Array.length arr then
    This arr.(idx)  (* No allocation with or_null *)
  else
    Null
```

### Zero-Alloc Record Update

```ocaml
type state = { x : int; y : int; z : int }

(* ERROR: record update allocates *)
let[@zero_alloc] bad_update s = { s with x = s.x + 1 }

(* OK: use mutable fields or unboxed *)
type mutable_state = { mutable x : int; mutable y : int; mutable z : int }

let[@zero_alloc] good_update s =
  s.x <- s.x + 1;
  s
```

---

## Understanding Failures

When check fails, compiler shows all allocations:

```
Error: Annotation check for zero_alloc failed on function M.f

File "m.ml", line 5, characters 10-15:
5 |     match bar x with
              ^^^^^
Error: called function may allocate (direct call to bar)

File "m.ml", line 9, characters 6-12:
9 |       (a, a)
          ^^^^^^
Error: allocation of 24 bytes
```

### Controlling Detail Level

```bash
# Show all allocations (default)
-zero-alloc-checker-details-cutoff -1

# Show only first N
-zero-alloc-checker-details-cutoff 5

# Show none (just fail)
-zero-alloc-checker-details-cutoff 0
```

---

## Common Errors and Fixes

### "Called function may allocate (indirect call)"

```ocaml
(* ERROR: f is indirect *)
let[@zero_alloc] apply f x = f x

(* FIX: Can't fix without knowing f is zero-alloc *)
(* Options:
   1. Use [@zero_alloc assume] on the call
   2. Make f an inline function
   3. Accept that this can't be zero-alloc
*)
```

### "Allocation of N bytes"

```ocaml
(* ERROR: tuple allocation *)
let[@zero_alloc] bad x y = (x, y)

(* FIX: Use stack allocation *)
let[@zero_alloc] good x y = exclave_ stack_ (x, y)

(* OR return unboxed *)
let[@zero_alloc] good2 (x : int) (y : int) : #(int * int) = #(x, y)
```

### "Called function may allocate (external call)"

```ocaml
(* ERROR: external without [@@noalloc] *)
external process : int -> int = "caml_process"

(* FIX: Add noalloc if truly non-allocating *)
external process : int -> int = "caml_process" [@@noalloc]

(* OR assume at call site *)
let[@zero_alloc] f x = (process [@zero_alloc assume]) x
```

---

## Build Configuration

### dune

```lisp
(library
 (name mylib)
 (ocamlopt_flags (:standard -zero-alloc-check all)))
```

### Compiler Flags

| Flag | Effect |
|------|--------|
| `-zero-alloc-check default` | Check non-opt annotations (default) |
| `-zero-alloc-check all` | Check all including opt |
| `-zero-alloc-check none` | Disable checking |
| `-disable-zero-alloc-checker` | Disable entirely (no summaries) |

---

## Limitations

- Conservative - may reject valid zero-alloc code
- Higher-order functions often fail (indirect calls)
- Requires cross-module info for accurate checking
- Flat float optimization can cause false positives
- Safepoints not considered allocating (may context switch)

---

## Best Practices

1. **Start with `[@zero_alloc opt]`** until code stabilizes
2. **Use `[@cold]` on error paths** to hint to optimizer
3. **Combine with `[@inline always]`** for small helpers
4. **Use unboxed types** for numeric hot paths
5. **Use `or_null` instead of `option`** for nullable unboxed
6. **Annotate signatures** for cross-module checking

See also: [SKILL-STACK-ALLOCATION.md](SKILL-STACK-ALLOCATION.md) for local allocation,
[SKILL-UNBOXED.md](SKILL-UNBOXED.md) for unboxed types.
