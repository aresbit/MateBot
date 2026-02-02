# OxCaml Modes: Detailed Guide

Modes are compile-time properties that track runtime characteristics of values.
They enable memory safety, thread safety, and performance optimizations without
runtime overhead.

## Mode Axes Overview

OxCaml has five independent mode axes:

| Axis | Modes | Tracks |
|------|-------|--------|
| Locality | `local` / `global` | Stack vs heap allocation |
| Uniqueness | `unique` / `aliased` | Single vs multiple references |
| Linearity | `once` / `many` | Closure invocation count |
| Portability | `portable` / `shareable` / `nonportable` | Cross-thread safety |
| Contention | `contended` / `shared` / `uncontended` | Concurrent access |

Each axis is independent - a value can be `local unique once` or `global aliased many`.

---

## Syntax Reference

### On Function Parameters

```ocaml
(* Single mode *)
let f (x @ local) = ...
let g (x @ unique) = ...

(* Multiple modes *)
let h (x @ local unique once) = ...

(* With type annotation *)
let process (data @ local : int array) = ...
```

### On Return Types (Signatures)

```ocaml
(* Arrow syntax in signatures *)
val f : t @ local -> t @ global
val g : t @ unique -> t @ aliased
val h : t @ local unique -> t @ global aliased

(* Multiple arrows *)
val compose : ('a -> 'b) @ once -> ('b -> 'c) @ once -> ('a -> 'c) @ once
```

### On Expressions

```ocaml
(* Type annotation with mode *)
let x = (some_expr : t @ local)

(* Cast to weaker mode *)
let y = (unique_val : t @ aliased)
```

### On Let Bindings

```ocaml
(* Shorthand for common modes *)
let local_ x = (1, 2)       (* x is local *)
let global_ y = (3, 4)      (* y is global - explicit *)
let stack_ z = (5, 6)       (* z is stack-allocated local *)
```

### On Record Fields (Modalities)

Modalities specify the mode of field contents relative to the record:

```ocaml
type t = {
  global_ name : string;           (* always global, even if record is local *)
  mutable count : int @@ aliased;  (* always aliased *)
  callback : (unit -> unit) @@ many; (* always many, not once *)
}
```

**Important**: For modalities, `@@ global` always implies `@@ aliased`. You cannot
use `@@ global unique` together - this restriction ensures soundness of the
upcoming borrowing feature. If you need a global field in a unique context,
use `@@ global aliased` explicitly.

---

## Subtyping (Mode Coercion)

Modes have a subtyping relationship. You can use a "stronger" mode where a
"weaker" one is expected:

```
Locality:    global ≤ local     (global values can be used as local)
Uniqueness:  unique ≤ aliased   (unique values can be used as aliased)
Linearity:   many ≤ once        (many closures can be used as once)
Portability: portable ≤ shareable ≤ nonportable
Contention:  uncontended ≤ shared ≤ contended
```

### Examples

```ocaml
(* OK: using global where local expected *)
let use_local (x @ local) = ...
let _ = use_local global_value

(* OK: using unique where aliased expected *)
let use_aliased (x @ aliased) = ...
let _ = use_aliased unique_value

(* ERROR: using local where global expected *)
let use_global (x @ global) = ...
let _ = use_global local_value  (* Type error! *)
```

---

## Deep vs Shallow Modes

Modes are **deep** - they apply to the entire value structure:

```ocaml
(* If a tuple is local, all its components are local *)
let local_ pair = (make_a (), make_b ())
(* Both components are local *)

(* If a record is unique, all its (non-modality) fields are unique *)
let use_unique (r @ unique) =
  free r.field1;  (* field1 is also unique *)
  free r.field2   (* ERROR: r already partially consumed *)
```

### Breaking Depth with Modalities

```ocaml
type container = {
  global_ data : string;  (* data is always global *)
  local_stuff : int list; (* follows container's mode *)
}

let f (c @ local) =
  let s = c.data in   (* s is global! *)
  let l = c.local_stuff in  (* l is local *)
  s  (* can return s *)
```

---

## Mode Inference

The compiler infers modes when not specified:

```ocaml
(* Compiler infers: val f : 'a -> 'a @ global aliased many *)
let f x = x

(* Explicit local forces local inference *)
let g (x @ local) = x
(* Inferred: val g : 'a @ local -> 'a @ local *)
```

### Inference from Usage

```ocaml
(* If result is used locally, function inferred as returning local *)
let make () = (1, 2)

let use () =
  let local_ p = make () in  (* forces make to return local *)
  fst p

(* Now make is inferred as: unit -> (int * int) @ local *)
```

---

## Mode Crossing

Some types can "cross" modes - be treated as a stronger mode than they have:

```ocaml
(* Immediates (int, char, bool, etc.) cross all modes *)
let f (x @ local) : int @ global = x  (* OK! int crosses locality *)

(* Functions don't cross linearity *)
let g (f @ once) : (int -> int) @ many = f  (* ERROR *)

(* Immutable data without functions crosses uniqueness *)
let h (lst @ aliased) : int list @ unique = lst  (* OK if lst is immutable *)
```

### Checking Mode Crossing

A type crosses a mode if using it at that mode is safe:
- `int`, `bool`, `char`, etc. cross everything (they're immediates)
- Immutable data without closures crosses uniqueness
- Data without mutable state crosses linearity

---

## Practical Patterns

### Local Processing, Global Result

```ocaml
let process_data data =
  (* Use local allocations for intermediate work *)
  let local_ temp = compute_step1 data in
  let local_ temp2 = compute_step2 temp in
  (* Extract global result *)
  extract_result temp2  (* returns global *)
```

### Unique Resource with Aliased Contents

```ocaml
type 'a resource = {
  handle : handle;
  contents : 'a @@ aliased;  (* contents can be shared *)
}

let use (r @ unique) =
  let data = r.contents in  (* data is aliased, can be copied *)
  process data;
  close r.handle  (* safe: r is unique *)
```

### Once Callbacks

```ocaml
type 'a promise

val on_complete : 'a promise -> ('a -> unit) @ once -> unit

let example p =
  let resource = acquire () in
  on_complete p (fun result ->
    use_resource resource result;
    release resource  (* safe: callback runs at most once *)
  )
```

### Portable Data for Threading

```ocaml
(* Data that can be sent across threads *)
type config = {
  max_threads : int;
  timeout : float;
} [@@deriving portable]

val spawn : (unit -> 'a @ portable) @ portable -> 'a promise
```

---

## Common Errors and Solutions

### "This value is local but expected to be global"

```ocaml
(* ERROR *)
let bad () =
  let local_ x = (1, 2) in
  x  (* Cannot return local value *)

(* FIX: Use exclave_ to allocate in caller's frame *)
let good () = exclave_
  stack_ (1, 2)

(* FIX: Or allocate globally *)
let good2 () =
  (1, 2)  (* Global by default *)
```

### "This value is aliased but expected to be unique"

```ocaml
(* ERROR *)
let bad x =
  let y = x in  (* x now aliased *)
  free x        (* Cannot free aliased value *)

(* FIX: Don't alias before unique use *)
let good x =
  free x

(* FIX: Or use the alias instead *)
let good2 x =
  let y = x in
  free y
```

### "This closure is once but expected to be many"

```ocaml
(* ERROR *)
let bad (r @ unique) =
  let f () = free r in
  f ();
  f ()  (* Cannot call once closure twice *)

(* FIX: Thread unique value through *)
let good (r @ unique) =
  let r = use r in
  let r = use r in
  free r
```

---

## Mode Syntax Summary

| Location | Syntax | Example |
|----------|--------|---------|
| Parameter | `(x @ mode)` | `(x @ local unique)` |
| Signature arrow | `t @ mode ->` | `t @ local -> t @ global` |
| Expression | `(e : t @ mode)` | `(x : int @ local)` |
| Let binding | `let mode_ x =` | `let local_ x = ...` |
| Record field | `mode_ field :` | `global_ data : string` |
| Record field | `: t @@ modality` | `: t @@ aliased` |

---

## Portability and Contention (Three-Way Axes)

The portability and contention axes now have three values each:

### Portability Axis

| Mode | Meaning |
|------|---------|
| `nonportable` | Functions capturing uncontended mutable state; cannot escape current thread |
| `shareable` | Functions capturing shared state; may execute in parallel |
| `portable` | Functions capturing all values at contended; may execute concurrently |

### Contention Axis

| Mode | Meaning |
|------|---------|
| `uncontended` | Single-thread access; full read/write |
| `shared` | Multi-thread access; synchronized sharing |
| `contended` | Multi-thread concurrent access |

### Mode Implications

Certain modalities imply others for soundness:

- `@@ global` implies `@@ aliased` (for borrowing soundness)
- `stateless` implies `portable`
- `observing` implies `shareable`
- `immutable` implies `contended`
- `read` implies `shared`

See also: [SKILL-STACK-ALLOCATION.md](SKILL-STACK-ALLOCATION.md) for locality details,
[SKILL-UNIQUENESS.md](SKILL-UNIQUENESS.md) for uniqueness patterns.
