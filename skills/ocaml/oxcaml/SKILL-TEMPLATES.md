# OxCaml Templates (ppx_template): Detailed Guide

`ppx_template` generates multiple copies of code with different modes, kinds, or
modalities. It's a workaround until OxCaml has native polymorphism over these
axes.

## Basic Concept

Instead of runtime polymorphism, templates create compile-time copies:

```ocaml
(* Single source *)
let%template[@mode m = (global, local)] id x = x

(* Generates two functions *)
let id x = x              (* global version *)
let id__local x = x       (* local version *)
```

---

## Extension Points

### On Definitions

```ocaml
(* On let *)
let%template ...

(* On val *)
val%template ...

(* On type *)
type%template ...

(* On module *)
module%template ...
```

### Block Form

```ocaml
(* Structure items *)
[%%template
  let f x = x
  let g x = x + 1
]

(* Signature items - note colon *)
[%%template:
  val f : 'a -> 'a
  val g : int -> int
]
```

### Expression Form

```ocaml
let x = [%template fun x -> x]
```

---

## Mode Templates

### Defining Mode-Polymorphic Functions

```ocaml
let%template[@mode m = (global, local)] identity
  : 'a @ m -> 'a @ m
  = fun x -> x

(* Generates:
   val identity : 'a -> 'a
   val identity__local : 'a @ local -> 'a @ local
*)
```

### Instantiating

```ocaml
(* Inside %template context *)
let f x = (identity [@mode local]) x

(* Or using mangled name directly (not recommended) *)
let f x = identity__local x
```

### Multiple Mode Variables

```ocaml
let%template[@mode m1 = (global, local), m2 = (portable, nonportable)]
  process (x @ m1) (y @ m2) = ...

(* Generates 2 × 2 = 4 versions *)
```

### The exclave_if_local Attribute

Conditionally add `exclave_` for local returns:

```ocaml
let%template[@mode m = (global, local)] make_pair x y =
  (x, y) [@exclave_if_local m]

(* global version: just returns (x, y) *)
(* local version: exclave_ (x, y) *)
```

**Restrictions**: Only valid on:
- Pure syntactic allocations (tuples, records, arrays)
- Tailcalls with only identifiers

---

## Kind Templates

### Defining Kind-Polymorphic Functions

```ocaml
let%template[@kind k = (value, float64, bits32, bits64)]
  id (type a : k) (x : a) : a = x

(* Generates:
   val id : 'a -> 'a
   val id__float64 : ('a : float64). 'a -> 'a
   val id__bits32 : ('a : bits32). 'a -> 'a
   val id__bits64 : ('a : bits64). 'a -> 'a
*)
```

### Kind Products

```ocaml
let%template[@kind k = (value, value & value, (value & value) & value)]
  wrap (type a : k) (x : a) = { contents = x }
```

### Kind with Mode Modifier

```ocaml
let%template[@kind k = (value, value mod portable)]
  f (type a : k) (x : a) = x
```

---

## Alloc Templates

For ad-hoc polymorphism over allocation behavior (heap vs stack):

```ocaml
let%template[@alloc a @ m = (heap_global, stack_local)]
  make_pair x y =
    (x, y) [@exclave_if_stack a]

(* heap_global version: (x, y) *)
(* stack_local version: exclave_ stack_ (x, y) *)
```

### Alloc Variable Alone

```ocaml
let%template[@alloc a = (heap, stack)]
  f x = x [@exclave_if_stack a]
```

### With zero_alloc_if_stack

```ocaml
let%template[@alloc a = (heap, stack)]
  process x = compute x
[@@zero_alloc_if_stack a]

(* stack version gets [@zero_alloc] attribute *)
```

---

## Modality Templates

For portable/nonportable functor patterns:

```ocaml
module%template[@modality p = (nonportable, portable)]
  Make (M : sig @@ p include S end) : sig @@ p include T end
  = struct ... end
```

### Shorthand: %template.portable

```ocaml
(* Long form *)
module%template[@modality p = (nonportable, portable)]
  F (M : sig @@ p include S end) : sig @@ p include T end = ...

(* Short form *)
module%template.portable F (M : S) : T = ...
```

---

## Floating Attributes

Apply to all subsequent items in scope:

```ocaml
[%%template:
[@@@mode.default m = (global, local)]

val min : t @ m -> t @ m -> t @ m
val max : t @ m -> t @ m -> t @ m
val clamp : t @ m -> low:t @ m -> high:t @ m -> t @ m
]

(* All three functions get both global and local versions *)
```

### Available Floating Attributes

- `[@@@mode.default ...]`
- `[@@@kind.default ...]`
- `[@@@modality.default ...]`
- `[@@@alloc.default ...]`

Without `.default`, names aren't mangled:

```ocaml
[@@@mode m = (global, local)]  (* No mangling *)
[@@@mode.default m = (global, local)]  (* With mangling *)
```

---

## Name Mangling

**WARNING: Mangling scheme may change. Don't rely on specific names.**

### General Pattern

```
base_name[__kind_suffix][__mode_suffix][__modality_suffix][__alloc_suffix]
```

### Defaults (No Suffix)

| Axis | Default (no suffix) |
|------|---------------------|
| Kind | `value` |
| Mode | `global`, `nonportable`, `uncontended`, `aliased` |
| Modality | `local`, `nonportable`, `uncontended`, `unique` |
| Alloc | `heap` |

### Examples

```ocaml
id                      (* default everything *)
id__local               (* mode local *)
id__float64             (* kind float64 *)
id__float64__local      (* kind float64, mode local *)
id__portable            (* modality portable *)
id__'value_value'       (* kind value & value - product *)
id__'value_mod_portable' (* kind value mod portable *)
```

---

## Punning

Shorthand when you just want mangling without new binding:

```ocaml
(* Long form *)
let f x = x [@@kind k = k]

(* Punned form *)
let f x = x [@@kind k]

(* For monomorphic instances *)
let%template f x = x [@@kind float64]  (* Just mangles to f__float64 *)
```

---

## Common Patterns

### Layout-Polymorphic Float Module

```ocaml
open [%template
  module [@kind value] Float = Float
  module [@kind float64] Float = Float_u
]

module%template[@kind k = (value, float64)] Float : sig
  type t : k
  val add : t -> t -> t
  val mul : t -> t -> t
end = Float [@kind k]
```

### Include with Mangling

```ocaml
include%template[@kind k = (value, float64)] struct
  open Float [@kind k]

  let[@kind k] double x = add x x
  let[@kind k] square x = mul x x
end
```

### Functor over Kinds

```ocaml
module%template[@kind k = (value, float64)] Make = struct
  open Float [@kind k]

  let[@kind k] process = ...
end

include%template Make [@kind value]
include%template Make [@kind float64]
```

---

## Type and Module Substitutions

Type substitutions work but have scoping limitations:

```ocaml
(* Works *)
module type%template A = sig
  [@@@kind.default k = (bits64, float64)]

  type ('a : k) t := 'a
  type nonrec 'a t = 'a t [@kind k]
end

(* May not work - substitution crosses [%%template] boundary *)
module type B = sig
  [%%template:
  [@@@kind.default k = (bits64, float64)]
  type ('a : k) t := 'a]

  (* t__bits64 not visible here! *)
end
```

---

## Type Variables vs Locally Abstract Types

Use locally abstract types for kind polymorphism:

```ocaml
(* ERROR: type variables unify across same block *)
let%template f (x : ('a : k)) : 'a = x
[@@kind k = (value, float64)]

(* CORRECT: locally abstract types are independent *)
let%template f (type a : k) (x : a) : a = x
[@@kind k = (value, float64)]
```

---

## Debugging

### See Expanded Code

Use `dune describe pp` or similar to see what templates expand to.

### Check Mangled Names

```ocaml
(* If unsure of mangling, test with explicit instantiation *)
let test = (some_function [@kind float64] [@mode local])
(* If it compiles, mangling is correct *)
```

---

## Performance Notes

- Templates are expanded at compile time - no runtime overhead
- Each instance is fully optimized independently
- Code size increases with number of instances
- Unused instances may still be generated (no SFINAE)

---

## Limitations

- No SFINAE - all instances generated eagerly
- No dependent types - can't compute kinds from values
- Mangling scheme unstable
- Right-nested kind products not supported: `value & (value & value)`

See also: [SKILL-MODES.md](SKILL-MODES.md) for mode details,
[SKILL-KINDS.md](SKILL-KINDS.md) for kind details.
