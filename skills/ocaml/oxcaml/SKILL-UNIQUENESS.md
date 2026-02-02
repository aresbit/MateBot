# OxCaml Uniqueness: Detailed Guide

Uniqueness tracking ensures values have exactly one reference, enabling safe
in-place mutation and resource management without runtime checks.

## Core Concepts

### Uniqueness Mode

- **`unique`**: Exactly one reference to this value exists
- **`aliased`**: Multiple references may exist

### Linearity Mode (Related)

- **`once`**: Closure can be called at most once
- **`many`**: Closure can be called any number of times

These are related because a closure capturing a unique value can only be called
once (otherwise it would use the unique value twice).

---

## Syntax

### On Parameters

```ocaml
(* Unique parameter - function consumes the only reference *)
let free (x @ unique) = External.free x

(* Aliased parameter - multiple references allowed *)
let copy (x @ aliased) = clone x
```

### On Return Types

```ocaml
(* Return unique value *)
val allocate : unit -> t @ unique

(* Return aliased (duplicated) *)
val duplicate : t -> (t * t) @ aliased
```

### On Closures

```ocaml
(* Once closure - can only be invoked once *)
val register_callback : (unit -> unit) @ once -> unit

(* Many closure - can be invoked repeatedly *)
val set_handler : (event -> unit) @ many -> unit
```

### Combining with Locality

```ocaml
(* Local and unique *)
val borrow : t @ unique -> (t @ local -> 'a) -> 'a * t @ unique

(* All combinations possible *)
let f (x @ local unique once) = ...
```

---

## Uniqueness Subtyping

Unique values can be used where aliased are expected (you can forget uniqueness):

```ocaml
unique ≤ aliased

(* OK: use unique where aliased expected *)
let store (x @ aliased) = global_ref := x
let _ = store unique_value  (* OK *)

(* ERROR: use aliased where unique expected *)
let consume (x @ unique) = free x
let _ = consume aliased_value  (* Type error! *)
```

---

## Aliased Modality on Fields

Store aliased values in unique containers:

```ocaml
(* Contents are aliased even if container is unique *)
type 'a aliased_box = { value : 'a @@ aliased } [@@unboxed]

(* Container is unique, contents are aliased *)
type 'a collection = {
  data : 'a aliased_box array;  (* elements aliased *)
}

(* Can free container while elements remain accessible elsewhere *)
val insert : 'a @ aliased -> 'a collection @ unique -> 'a collection @ unique
val free_container : 'a collection @ unique -> unit
```

### Reading Aliased Fields

```ocaml
type t = {
  metadata : string @@ aliased;
  payload : data;
}

let get_metadata (t @ unique) : string (* aliased *) =
  t.metadata  (* Reading aliased field returns aliased value *)
```

---

## Uniqueness Analysis

The compiler tracks which values are unique through:

### Aliasing via Binding

```ocaml
let x = make_unique () in
let y = x in  (* Now both x and y reference same value *)
(* x and y are both aliased *)
free x  (* ERROR: x is aliased, not unique *)
```

### Field Access Tracking

```ocaml
type t = { a : sub; b : sub }

let ok (r @ unique) =
  free r.a;
  free r.b  (* OK: different fields *)

let bad (r @ unique) =
  free r.a;
  free r    (* ERROR: r.a already freed, r contains it *)
```

### Renaming is Tracked

```ocaml
let ok (r @ unique) =
  let s = r in  (* s and r are aliases, both tracked *)
  free s.a;
  free r.b      (* OK: compiler knows s = r *)
```

### Complex Aliases Not Tracked

```ocaml
let bad (r @ unique) =
  let s = Fun.id r in  (* s is not tracked as alias of r *)
  free s.a;
  free r.b             (* ERROR: can't prove safety *)
```

---

## Branch Uniqueness

Different branches can use unique values differently:

```ocaml
let ok (x @ unique) =
  if condition then
    free x           (* Use uniquely in this branch *)
  else
    (store x; store x)  (* Use as aliased in this branch *)
  (* OK: mutually exclusive *)

let ok2 (x @ unique) =
  match x with
  | A -> free x
  | B -> ignore x  (* aliased use *)
  (* OK: different branches *)
```

---

## Once Closures

Closures capturing unique values are `once`:

```ocaml
let make_callback (resource @ unique) : (unit -> unit) @ once =
  fun () -> free resource

(* Can only call once *)
let callback = make_callback resource in
callback ();
callback ()  (* ERROR: once closure called twice *)
```

### Many Modality on Captured Values

```ocaml
type callback_data = {
  f : (unit -> unit) @@ many;  (* Always many *)
}

let store (cb @ once) : callback_data @ unique =
  { f = cb }  (* ERROR: cb is once, field requires many *)
```

---

## Mode Crossing

Some types cross uniqueness (can be treated as unique even when aliased):

```ocaml
(* Immediates cross uniqueness *)
let f (x @ aliased) : int @ unique = x  (* OK: int crosses *)

(* Immutable data without refs crosses *)
let g (lst @ aliased) : int list @ unique = lst  (* OK if truly immutable *)

(* Functions don't cross *)
let h (f @ aliased) : (int -> int) @ unique = f  (* ERROR *)
```

### Checking Mode Crossing

A type crosses uniqueness if:
- It's an immediate (int, bool, char, etc.)
- It's immutable data without functions or mutable fields

---

## Patterns

### Resource Management

```ocaml
type handle

val open_file : string -> handle @ unique
val read : handle @ unique -> string * handle @ unique
val close : handle @ unique -> unit

let process_file path =
  let h = open_file path in
  let content, h = read h in
  close h;  (* Safe: h is unique *)
  content
```

### Unique Mutable Phase

```ocaml
type 'a builder

val create : unit -> 'a builder @ unique
val add : 'a -> 'a builder @ unique -> 'a builder @ unique
val freeze : 'a builder @ unique -> 'a array (* aliased, immutable *)

let build_array items =
  let b = create () in
  let b = List.fold_left (fun b x -> add x b) b items in
  freeze b  (* Returns immutable array *)
```

### Threading Unique Values

```ocaml
(* BAD: can't use unique in loop directly *)
let bad (arr @ unique) =
  for i = 0 to 10 do
    set arr i 0  (* ERROR: arr used multiple times *)
  done

(* GOOD: thread unique through *)
let rec set_all (arr @ unique) i =
  if i >= length arr then arr
  else set_all (set arr i 0) (i + 1)

let good (arr @ unique) = set_all arr 0
```

### Borrowing Pattern

```ocaml
(* Temporarily use unique value, get it back *)
val with_ref : t @ unique -> (t @ local -> 'a) -> 'a * t @ unique

let example (data @ unique) =
  let result, data = with_ref data (fun d ->
    compute_something d
  ) in
  free data;
  result
```

---

## Common Errors and Solutions

### "This value is aliased but expected to be unique"

```ocaml
(* ERROR *)
let bad x =
  let y = x in
  free x  (* x is aliased due to y *)

(* FIX: Don't alias before unique use *)
let good x =
  free x

(* FIX: Use the alias *)
let good2 x =
  let y = x in
  free y
```

### "Cannot use value uniquely after pattern match"

```ocaml
(* ERROR: pattern match aliases *)
let bad (t @ unique) =
  match t with
  | { field } ->
    use_field field;
    free t  (* ERROR: t aliased by pattern *)

(* FIX: Use with_ref pattern *)
let good (t @ unique) =
  let result, t = with_ref t (fun t ->
    match t with
    | { field } -> use_field field
  ) in
  free t;
  result
```

### "This closure is once but expected to be many"

```ocaml
(* ERROR *)
let bad (r @ unique) =
  let f () = free r in
  register_handler f  (* handler expects many *)

(* FIX: Don't capture unique in many closure *)
let good () =
  let f () = () in  (* No unique captures *)
  register_handler f
```

### "Cannot call once closure multiple times"

```ocaml
(* ERROR *)
let bad (f @ once) =
  f (); f ()

(* FIX: Only call once, or require many *)
let good (f @ once) = f ()
let good2 (f @ many) = f (); f ()
```

---

## Uniqueness with Aliased Fields

```ocaml
type container = {
  handle : handle;  (* unique with container *)
  cache : data @@ aliased;  (* aliased, shared elsewhere *)
}

let close_container (c @ unique) =
  (* Can free handle, cache may still be used elsewhere *)
  free_handle c.handle
  (* cache is not freed *)

let get_cache (c @ unique) : data (* aliased *) =
  c.cache  (* Returns aliased copy *)
```

---

## Summary

| Mode | Meaning | Subtyping | Crosses |
|------|---------|-----------|---------|
| `unique` | Single reference | ≤ `aliased` | Immediates, imm. data |
| `aliased` | Multiple references | (top) | - |
| `once` | Call at most once | ≤ `many` | Non-function types |
| `many` | Call any times | (top) | - |

See also: [SKILL-MODES.md](SKILL-MODES.md) for full mode system,
[SKILL-STACK-ALLOCATION.md](SKILL-STACK-ALLOCATION.md) for locality.
