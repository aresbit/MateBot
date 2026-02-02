# OxCaml Base Library Extensions

Jane Street's Base library (116 modules) includes comprehensive OxCaml-specific
extensions for modes, local allocation, and unboxed types. This guide covers
which Base modules are particularly useful with OxCaml features.

## Module Overview by Category

### Core Data Structures

| Module | Description | OxCaml Features |
|--------|-------------|-----------------|
| `Array`, `Array0` | Mutable arrays | `@local_opt`, `@layout_poly`, `%%template`, stack alloc |
| `Iarray`, `Iarray0` | Immutable arrays | Local submodule, Unique submodule, stack init |
| `List`, `List0`, `List1` | Linked lists | `__local` variants, `%%template` |
| `Nonempty_list` | Non-empty lists | `@local_opt`, local variants |
| `Option_array` | Optional element arrays | Layout-polymorphic access |
| `Obj_array` | Object arrays | Low-level layout support |

### Hash-Based Collections

| Module | Description | OxCaml Features |
|--------|-------------|-----------------|
| `Hashtbl` | Hash tables | `__local` find/iter variants |
| `Hash_set` | Hash sets | Local iteration |
| `Hashable` | Hashable interface | Portable functor variants |

### Ordered Collections

| Module | Description | OxCaml Features |
|--------|-------------|-----------------|
| `Set` | Immutable sets | `__local` fold/find variants |
| `Map` | Immutable maps | `__local` fold/find variants |
| `Avltree` | AVL tree implementation | `@local_opt`, `%%template` |
| `Dictionary_immutable` | Dictionary abstraction | Mode-aware operations |
| `Dictionary_mutable` | Mutable dictionary | Mode-aware operations |

### Queues and Stacks

| Module | Description | OxCaml Features |
|--------|-------------|-----------------|
| `Queue` | Double-ended queue | Mode-aware operations |
| `Stack` | LIFO stack | Mode-aware operations |
| `Linked_queue` | Linked queue | Local iteration |

### Container Abstractions

| Module | Description | OxCaml Features |
|--------|-------------|-----------------|
| `Container` | Container interface | Base iteration patterns |
| `Container_with_local` | Local-aware containers | **Key for local iteration** |
| `Indexed_container` | Indexed access | `exclave_if_stack` patterns |

### Type Abstractions

| Module | Description | OxCaml Features |
|--------|-------------|-----------------|
| `Comparable` | Comparison interface | Portable functor variants |
| `Comparator` | Comparator witnesses | Mode-aware |
| `Comparisons` | Comparison operators | `@local_opt` |
| `Type_equal` | Type equality witnesses | Mode-safe |

---

## The Modes Module (Critical for OxCaml)

The `Modes` module is the cornerstone of OxCaml support in Base. It provides
zero-cost wrappers for crossing between mode contexts.

### Five Orthogonal Modalities

```ocaml
(* Locality: where values live *)
g = (local, global)

(* Portability: cross-thread safety *)
p = (nonportable, portable)

(* Contention: thread access patterns *)
c = (uncontended, shared, contended)

(* Multiplicity: how often used *)
m = (once, many)

(* Aliasing: reference count *)
a = (unique, aliased)
```

### Key Wrapper Submodules

```ocaml
(* All wrappers are [@@unboxed] - zero runtime cost *)

module Global : sig
  type 'a t [@@unboxed]
  external wrap : 'a -> 'a t = "%identity"
  external unwrap : 'a t -> 'a = "%identity"
end

module Portable : sig
  type 'a t [@@unboxed]
  external wrap : 'a -> 'a t = "%identity"
  external unwrap : 'a t -> 'a = "%identity"
end

module Contended : sig
  type 'a t [@@unboxed]
  (* Wraps values for contended access *)
end

module Shared : sig
  type 'a t [@@unboxed]
  (* Wraps values for shared (read) access *)
end

(* Combined wrapper *)
module Portended : sig
  type 'a t [@@unboxed]
  (* portable & contended - for thread-safe sharing *)
end
```

### Usage Pattern

```ocaml
(* Cross from local to global context *)
let make_global (x @ local) : 'a Modes.Global.t =
  Modes.Global.wrap x

(* Access global value locally *)
let use_globally (g : 'a Modes.Global.t) =
  let x = Modes.Global.unwrap g in
  process x
```

---

## Modules with Local/Exclave Support

### Tier 1: Extensive OxCaml Support (use these first)

**`Iarray` - Immutable Arrays**

The most OxCaml-friendly array module:

```ocaml
module Iarray : sig
  type 'a t  (* immutable, covariant *)

  (* Standard access *)
  val get : 'a t -> int -> 'a
  val length : 'a t -> int

  (* Local submodule - stack-allocated results *)
  module Local : sig
    val init : int -> f:(int -> 'a) -> 'a t
    (* Uses O(n) function-call stack space *)

    val init_with_globals : int -> f:(int -> 'a) -> 'a t
    (* Elements must be global - avoids extra stack space *)
  end

  (* Unique submodule - for unique-mode optimizations *)
  module Unique : sig
    val init : int -> f:(int -> 'a) -> 'a t
    val map : 'a t -> f:('a -> 'b) -> 'b t
    val mapi : 'a t -> f:(int -> 'a -> 'b) -> 'b t
    val unzip : ('a * 'b) t -> 'a t * 'b t
    val zip_exn : 'a t -> 'b t -> ('a * 'b) t
  end
end
```

**`Container_with_local` - Local-Aware Iteration**

Interface for containers that support local closures:

```ocaml
module type S = sig
  type 'a t

  val iter__local : 'a t -> f:('a -> unit @ local) -> unit
  val fold__local : 'a t -> init:'acc -> f:('acc -> 'a -> 'acc @ local) -> 'acc
  val exists__local : 'a t -> f:('a -> bool @ local) -> bool
  val for_all__local : 'a t -> f:('a -> bool @ local) -> bool
  val find__local : 'a t -> f:('a -> bool @ local) -> 'a option @ local
  val find_map__local : 'a t -> f:('a -> 'b option @ local) -> 'b option @ local
end
```

**`Array` / `Array0` - Mutable Arrays**

```ocaml
(* Layout-polymorphic operations *)
external length : 'a. ('a array[@local_opt]) -> int = "%array_length"
  [@@layout_poly]

external get : 'a. ('a array[@local_opt]) -> (int[@local_opt]) -> 'a = "%array_safe_get"
  [@@layout_poly]

(* Template-enabled operations *)
[%%template:
val init : int -> f:(int -> 'a) -> 'a array
  [@@alloc __ @ m = (heap_global, stack_local)]]
```

### Tier 2: Good OxCaml Support

**`List`**

```ocaml
(* Local-returning variants via %%template *)
val map__local : 'a list -> f:('a -> 'b @ local) -> 'b list @ local
val filter__local : 'a list -> f:('a -> bool @ local) -> 'a list @ local
val filter_map__local : 'a list -> f:('a -> 'b option @ local) -> 'b list @ local
val concat_map__local : 'a list -> f:('a -> 'b list @ local) -> 'b list @ local
val fold__local : 'a list -> init:'acc -> f:('acc -> 'a -> 'acc @ local) -> 'acc
```

**`Option`**

```ocaml
val map__local : 'a option -> f:('a -> 'b @ local) -> 'b option @ local
val bind__local : 'a option -> f:('a -> 'b option @ local) -> 'b option @ local
val value__local : 'a option -> default:'a @ local -> 'a @ local
```

**`Result`**

```ocaml
val map__local : ('a, 'e) t -> f:('a -> 'b @ local) -> ('b, 'e) t @ local
val map_error__local : ('a, 'e) t -> f:('e -> 'f @ local) -> ('a, 'f) t @ local
val bind__local : ('a, 'e) t -> f:('a -> ('b, 'e) t @ local) -> ('b, 'e) t @ local
```

**`Or_error`**

Mode-aware error handling combining Result with Error.t:

```ocaml
val map__local : 'a t -> f:('a -> 'b @ local) -> 'b t @ local
val bind__local : 'a t -> f:('a -> 'b t @ local) -> 'b t @ local
```

**`Or_null`**

Non-allocating option alternative (uses null representation):

```ocaml
type 'a t = Null | This of 'a

(* Zero allocation for None case *)
val to_option__local : 'a t -> 'a option @ local
```

### Tier 3: Primitive Types with Local Support

These modules have `@local_opt` annotations on many functions:

| Module | Key Local Features |
|--------|-------------------|
| `Bool`, `Bool0` | Comparison with local args |
| `Char` | Local-safe character ops |
| `Int`, `Int32`, `Int64`, `Nativeint` | Conversions with `@local_opt` |
| `Float`, `Float0` | Math ops with local support |
| `String`, `String0` | Split/concat local variants |
| `Bytes`, `Bytes0` | Local buffer creation |
| `Unit` | Local returns |

---

## Template/Rederive Patterns

66 Base modules use `%%template` and `%%rederive` for mode polymorphism:

### Common Patterns

```ocaml
(* Mode-templated function *)
[%%template:
[@@@mode.default m = (global, local)]
val map : 'a t -> f:('a -> 'b @ m) -> 'b t @ m]

(* Generates: map (global) and map__local *)

(* Kind-templated function *)
[%%template:
[@@@kind.default k = (value, float64)]
external get : ('a : k). 'a array -> int -> 'a = "%array_safe_get"
  [@@layout_poly]]

(* Alloc-templated for stack/heap choice *)
[%%template:
val init : int -> f:(int -> 'a) -> 'a t
  [@@alloc __ @ m = (heap_global, stack_local)]]

(* Portable module variant *)
module%template.portable Make (M : S) : T
```

### Using Templates in Your Code

```ocaml
(* Call the local variant explicitly *)
let process lst =
  let local_ mapped = List.map__local lst ~f:transform in
  List.fold mapped ~init:0 ~f:(+)

(* Or use template instantiation *)
let%template[@mode m = (global, local)] my_map lst ~f =
  (List.map [@mode m]) lst ~f
```

---

## Portable Functors

For multicore OCaml, many Base functors have portable variants:

```ocaml
(* Standard Comparable *)
module Comparable.Make (T : sig
  type t [@@deriving compare, sexp_of]
end) : Comparable.S with type t := T.t

(* Portable variant for cross-domain use *)
module Comparable.Make__portable (T : sig
  type t [@@deriving compare, sexp_of] @@ portable
end) : Comparable.S with type t := T.t @@ portable

(* Same pattern for Hashable *)
module Hashable.Make__portable (T : sig
  type t [@@deriving hash, compare, sexp_of] @@ portable
end) : Hashable.S with type t := T.t @@ portable
```

### Shorthand with %template.portable

```ocaml
module%template.portable My_key = struct
  type t = { id : int; name : string }
  [@@deriving compare, sexp_of, hash]

  include functor Comparable.Make
  include functor Hashable.Make
end
```

---

## Lazy Evaluation

**`Lazy`**

```ocaml
external force : ('a t[@local_opt]) -> 'a = "%lazy_force"
(* Can force local lazy values *)
```

**`Portable_lazy`**

Thread-safe lazy evaluation for portable values:

```ocaml
module Portable_lazy : sig
  type 'a t

  val from_fun : (unit -> 'a) -> 'a t
  (* Function must be portable - can run on any domain *)

  val force : 'a t -> 'a
end
```

---

## Utility Modules

**`With_return`**

```ocaml
val with_return__local : ('a return -> 'b @ local) -> 'b @ local
(* Early return with local value *)
```

**`Staged`**

```ocaml
external unstage : ('a staged[@local_opt]) -> 'a = "%identity"
(* Zero-cost staging with local support *)
```

**`Fn`**

```ocaml
external ( |> ) : 'a 'b. 'a -> (('a -> 'b)[@local_opt]) -> 'b = "%revapply"
(* Pipe with local function support *)
```

---

## Unboxed Numeric Modules

Base provides operations on unboxed numeric types:

```ocaml
(* Available unboxed operations *)
module Float_u : sig
  type t = float#
  val add : t -> t -> t
  val sub : t -> t -> t
  val mul : t -> t -> t
  val div : t -> t -> t
  val neg : t -> t
  val abs : t -> t
  val sqrt : t -> t
  (* etc. *)
end

module Int32_u : sig
  type t = int32#
  val add : t -> t -> t
  val sub : t -> t -> t
  val mul : t -> t -> t
  val div : t -> t -> t
  (* etc. *)
end

module Int64_u : sig
  type t = int64#
  (* same pattern *)
end
```

---

## Common Patterns

### Local List Processing Pipeline

```ocaml
let process_items items =
  let local_ filtered = List.filter__local items ~f:is_valid in
  let local_ mapped = List.map__local filtered ~f:transform in
  List.fold mapped ~init:0 ~f:(+)  (* Final result is global *)
```

### Stack-Allocated Temporary Structures

```ocaml
let group_and_count items ~key =
  let local_ groups = Hashtbl.create (module String) in
  List.iter items ~f:(fun item ->
    Hashtbl.update groups (key item) ~f:(function
      | None -> 1
      | Some n -> n + 1)
  );
  Hashtbl.to_alist groups  (* Convert to global at the end *)
```

### Local Iteration with Early Exit

```ocaml
let find_first_valid items =
  With_return.with_return__local (fun { return } ->
    List.iter__local items ~f:(fun item ->
      if is_valid item then return (Some item)
    );
    None
  )
```

### Immutable Array with Local Init

```ocaml
let make_lookup_table size =
  Iarray.Local.init size ~f:(fun i ->
    compute_entry i
  )
```

### Portable Module for Multicore

```ocaml
module%template.portable Cache_key = struct
  type t = { domain : string; path : string }
  [@@deriving compare, sexp_of, hash]

  include functor Comparable.Make
  include functor Hashable.Make
end

(* Can now safely use Cache_key across domains *)
```

---

## Quick Reference: Finding Local Variants

Most Base collection functions follow these naming patterns:

| Standard | Local Variant | Purpose |
|----------|---------------|---------|
| `map` | `map__local` | Returns local result |
| `filter` | `filter__local` | Returns local result |
| `fold` | `fold__local` | Closure can be local |
| `iter` | `iter__local` | Closure can be local |
| `find` | `find__local` | Returns local option |
| `find_map` | `find_map__local` | Returns local option |
| `exists` | `exists__local` | Closure can be local |
| `for_all` | `for_all__local` | Closure can be local |

---

## See Also

- [SKILL-MODES.md](SKILL-MODES.md) - Detailed mode system documentation
- [SKILL-STACK-ALLOCATION.md](SKILL-STACK-ALLOCATION.md) - Stack allocation patterns
- [SKILL-TEMPLATES.md](SKILL-TEMPLATES.md) - ppx_template usage and mangling
- [SKILL-CORE.md](SKILL-CORE.md) - Core library OxCaml extensions
