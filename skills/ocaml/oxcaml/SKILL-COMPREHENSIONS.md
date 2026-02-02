# OxCaml Comprehensions: Detailed Guide

Comprehensions provide concise syntax for building lists and arrays, inspired by
Python and Haskell.

## Basic Syntax

### List Comprehensions

```ocaml
(* Basic: generate values *)
[ x * 2 for x = 1 to 10 ]
(* [2; 4; 6; 8; 10; 12; 14; 16; 18; 20] *)

(* With filter *)
[ x for x = 1 to 20 when x mod 3 = 0 ]
(* [3; 6; 9; 12; 15; 18] *)

(* Iterate over list *)
[ String.uppercase_ascii s for s in ["hello"; "world"] ]
(* ["HELLO"; "WORLD"] *)

(* Downto *)
[ x for x = 10 downto 1 ]
(* [10; 9; 8; 7; 6; 5; 4; 3; 2; 1] *)
```

### Array Comprehensions

```ocaml
(* Same syntax with [| |] *)
[| x * x for x = 1 to 5 |]
(* [|1; 4; 9; 16; 25|] *)

(* From array *)
[| f elem for elem in source_array |]
```

### Immutable Array Comprehensions

```ocaml
(* Use [: :] for iarray *)
[: x for x = 1 to 10 when x mod 2 = 0 :]
(* Returns int iarray *)
```

### Unboxed/Untagged Array Comprehensions

Comprehensions work with unboxed and untagged arrays:

```ocaml
(* Unboxed float array comprehension *)
[| #(Float.of_int x) for x = 1 to 10 |] : float# array

(* Untagged int8 array comprehension *)
[| #(Int8.of_int x) for x = 0 to 255 |] : int8# array
```

---

## Iterators

### Range Iterators

```ocaml
(* Counting up *)
[ x for x = start to stop ]

(* Counting down *)
[ x for x = stop downto start ]

(* Empty if start > stop (for to) or start < stop (for downto) *)
[ x for x = 5 to 3 ]  (* [] *)
```

### Collection Iterators

```ocaml
(* Iterate over list *)
[ f x for x in some_list ]

(* Iterate over array (in array comprehension) *)
[| f x for x in some_array |]

(* With pattern matching *)
[ a + b for (a, b) in pairs ]
```

---

## Nested vs Parallel Iteration

### Nested Iteration (`for ... for ...`)

Nested `for` clauses create cartesian product - inner re-evaluated each outer:

```ocaml
[ (x, y) for x = 1 to 3 for y = 1 to 2 ]
(* [(1,1); (1,2); (2,1); (2,2); (3,1); (3,2)] *)
(* 3 * 2 = 6 elements *)

(* Inner can depend on outer *)
[ (x, y) for x = 1 to 3 for y = 1 to x ]
(* [(1,1); (2,1); (2,2); (3,1); (3,2); (3,3)] *)
```

### Parallel Iteration (`for ... and ...`)

Parallel `and` iterates in lockstep - all sources evaluated once upfront:

```ocaml
[ (x, y) for x = 1 to 3 and y = 10 to 12 ]
(* [(1,10); (2,11); (3,12)] *)
(* min(3, 3) = 3 elements *)

(* Cannot depend on each other *)
[ (x, y) for x = 1 to 3 and y = 1 to x ]  (* ERROR: x not in scope *)
```

### Key Differences

| Aspect | `for ... for ...` | `for ... and ...` |
|--------|-------------------|-------------------|
| Result size | Product | Minimum |
| Re-evaluation | Inner re-evaluated | All evaluated once |
| Dependencies | Inner can use outer | Independent |
| Optimization | Standard | Fixed-size array opt |

---

## Filter Clauses

### Basic When

```ocaml
[ x for x = 1 to 100 when x mod 7 = 0 ]
(* Multiples of 7 from 1 to 100 *)
```

### Multiple When Clauses

```ocaml
[ x for x = 1 to 100 when x mod 2 = 0 when x mod 3 = 0 ]
(* Same as: when x mod 2 = 0 && x mod 3 = 0 *)
(* Multiples of 6 *)
```

### When Position Matters

```ocaml
(* Filter before inner loop *)
[ (x, y) for x = 1 to 10 when x mod 2 = 0 for y = 1 to 3 ]
(* Only even x values, all y for each *)

(* Filter after inner loop *)
[ (x, y) for x = 1 to 10 for y = 1 to 3 when y > x ]
(* All x, only y > x *)
```

---

## Complex Examples

### Pythagorean Triples

```ocaml
[ (a, b, c)
  for a = 1 to 20
  for b = a to 20      (* b >= a to avoid duplicates *)
  for c = b to 20      (* c >= b to avoid duplicates *)
  when a * a + b * b = c * c ]
(* [(3,4,5); (5,12,13); (6,8,10); (8,15,17); (9,12,15)] *)
```

### Flatten Nested Structure

```ocaml
let matrix = [[1;2;3]; [4;5;6]; [7;8;9]]
[ x for row in matrix for x in row ]
(* [1; 2; 3; 4; 5; 6; 7; 8; 9] *)
```

### Cross Product with Filter

```ocaml
let colors = ["red"; "green"; "blue"]
let sizes = ["S"; "M"; "L"]
[ Printf.sprintf "%s-%s" c s
  for c in colors
  for s in sizes
  when not (c = "red" && s = "S") ]  (* Exclude red-S *)
```

### Indexed Iteration

```ocaml
let items = [|"a"; "b"; "c"; "d"|]
[| (i, items.(i)) for i = 0 to Array.length items - 1 |]
(* [|(0,"a"); (1,"b"); (2,"c"); (3,"d")|] *)
```

### Zip with Index

```ocaml
let xs = [1; 2; 3]
let ys = ["a"; "b"; "c"]
[ (i, x, y)
  for i = 0 to min (List.length xs) (List.length ys) - 1
  and x in xs
  and y in ys ]
(* [(0,1,"a"); (1,2,"b"); (2,3,"c")] *)
```

---

## Pattern Matching in Iterators

```ocaml
(* Destructure tuples *)
[ a + b for (a, b) in [(1,2); (3,4); (5,6)] ]
(* [3; 7; 11] *)

(* Destructure records *)
type point = { x : int; y : int }
[ p.x + p.y for p in points ]

(* Partial patterns (may raise) *)
[ x for Some x in options ]  (* Raises if None encountered! *)
```

### Safe Filtering Instead

```ocaml
(* Better: filter explicitly *)
[ x for opt in options when Option.is_some opt
    for x in [Option.get opt] ]

(* Or use intermediate binding *)
let get_some = function Some x -> [x] | None -> []
[ x for opt in options for x in get_some opt ]
```

---

## Evaluation Order

1. Clauses evaluated left to right
2. `for ... and ...` evaluates all sources before iterating
3. `when` checked before proceeding to right clauses
4. Body evaluated for each combination passing all filters

```ocaml
(* Evaluation order example *)
[ (Printf.printf "%d,%d\n" x y; (x,y))
  for x = 1 to 2
  for y = 1 to 2 ]
(* Prints: 1,1  1,2  2,1  2,2 *)
```

---

## Array Optimization

For array comprehensions with single `for ... and ...` clause, the compiler
pre-allocates exact-size array:

```ocaml
(* Optimized: single and clause, size known *)
[| x + y for x = 1 to 1000 and y = 1 to 1000 |]
(* Pre-allocates 1,000,000 element array *)

(* Not optimized: nested for *)
[| x + y for x = 1 to 1000 for y = 1 to 1000 |]
(* Grows array dynamically *)

(* Not optimized: has when clause *)
[| x for x = 1 to 1000 and y = 1 to 1000 when x > y |]
(* Can't predict size due to filter *)
```

---

## Common Patterns

### Map

```ocaml
let map f lst = [ f x for x in lst ]
let map_array f arr = [| f x for x in arr |]
```

### Filter

```ocaml
let filter pred lst = [ x for x in lst when pred x ]
```

### Filter-Map

```ocaml
let filter_map f lst =
  [ y for x in lst for y in (match f x with Some v -> [v] | None -> []) ]
```

### Enumerate

```ocaml
let enumerate lst =
  [ (i, x) for i = 0 to List.length lst - 1 and x in lst ]
```

### Cartesian Product

```ocaml
let product xs ys = [ (x, y) for x in xs for y in ys ]
```

### Take While

```ocaml
(* Note: comprehensions don't short-circuit, so this processes all *)
let take_while pred lst =
  let rec go acc = function
    | [] -> List.rev acc
    | x :: _ when not (pred x) -> List.rev acc
    | x :: xs -> go (x :: acc) xs
  in go [] lst
(* Comprehensions not ideal for take_while *)
```

---

## Performance Tips

1. **Prefer `and` over nested `for`** when iteration is parallel and size is fixed
2. **Put restrictive `when` clauses early** to skip work
3. **Array comprehensions** are generally faster than list (no cons overhead)
4. **For very large results**, consider alternative approaches (iterators, sequences)

---

## Limitations

- Cannot break out early (no `break` or `return`)
- Partial patterns may raise exceptions
- Local allocations in comprehensions follow normal rules
- Nested comprehensions can be memory-intensive

See also: [SKILL.md](SKILL.md) for quick reference,
[SKILL-STACK-ALLOCATION.md](SKILL-STACK-ALLOCATION.md) for local list building.
