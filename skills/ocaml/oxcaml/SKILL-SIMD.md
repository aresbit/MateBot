# OxCaml SIMD: Detailed Guide

OxCaml provides built-in SIMD vector types and intrinsics for high-performance
parallel numeric operations on x86-64 (SSE/AVX).

## Vector Types

### 128-bit Vectors (SSE)

| Type | Unboxed | Elements | Element Type |
|------|---------|----------|--------------|
| `int8x16` | `int8x16#` | 16 | 8-bit int |
| `int16x8` | `int16x8#` | 8 | 16-bit int |
| `int32x4` | `int32x4#` | 4 | 32-bit int |
| `int64x2` | `int64x2#` | 2 | 64-bit int |
| `float32x4` | `float32x4#` | 4 | 32-bit float |
| `float64x2` | `float64x2#` | 2 | 64-bit float |

### 256-bit Vectors (AVX)

| Type | Unboxed | Elements | Element Type |
|------|---------|----------|--------------|
| `int8x32` | `int8x32#` | 32 | 8-bit int |
| `int16x16` | `int16x16#` | 16 | 16-bit int |
| `int32x8` | `int32x8#` | 8 | 32-bit int |
| `int64x4` | `int64x4#` | 4 | 64-bit int |
| `float32x8` | `float32x8#` | 8 | 32-bit float |
| `float64x4` | `float64x4#` | 4 | 64-bit float |

---

## Boxed vs Unboxed Vectors

### Unboxed (`#` suffix)

- Passed in XMM/YMM registers
- Stored flat in records
- Can be in flat arrays
- No heap allocation for the vector itself

```ocaml
let process (v : float32x4#) : float32x4# =
  Float32x4.sqrt v  (* All in registers *)
```

### Boxed (no suffix)

- Heap-allocated when passed to non-inlined functions
- May generate unaligned load/store
- Easier to use in polymorphic code

```ocaml
let store_vector (v : float32x4) : unit =
  global_ref := v  (* Allocates *)
```

---

## Library Setup

Add to your dune file:

```lisp
(libraries ocaml_simd ocaml_simd_sse ppx_simd)
; Or for AVX:
(libraries ocaml_simd ocaml_simd_avx ppx_simd)
```

---

## Basic Operations

### Creating Vectors

```ocaml
open Ocaml_simd_sse

(* Set individual elements (high to low order) *)
let v = Float32x4.set 4.0 3.0 2.0 1.0
(* v = [1.0, 2.0, 3.0, 4.0] *)

(* Broadcast single value to all lanes *)
let v = Float32x4.broadcast 5.0
(* v = [5.0, 5.0, 5.0, 5.0] *)

(* From tuple *)
let v = Float32x4.of_tuple (1.0, 2.0, 3.0, 4.0)
```

### Extracting Values

```ocaml
(* Extract to tuple *)
let (a, b, c, d) = Float32x4.to_tuple v

(* Extract single element *)
let first = Float32x4.extract v 0
let last = Float32x4.extract v 3
```

### Arithmetic

```ocaml
let a = Float32x4.set 1.0 2.0 3.0 4.0
let b = Float32x4.set 5.0 6.0 7.0 8.0

let sum = Float32x4.add a b       (* [6, 8, 10, 12] *)
let diff = Float32x4.sub a b      (* [-4, -4, -4, -4] *)
let prod = Float32x4.mul a b      (* [5, 12, 21, 32] *)
let quot = Float32x4.div a b      (* [0.2, 0.33, 0.43, 0.5] *)

(* Math functions *)
let roots = Float32x4.sqrt a      (* [1, 1.41, 1.73, 2] *)
let recip = Float32x4.rcp a       (* Approximate reciprocal *)
let rsqrt = Float32x4.rsqrt a     (* Approximate 1/sqrt *)
```

### Comparisons

```ocaml
(* Returns mask vector *)
let mask = Float32x4.cmplt a b    (* a < b per element *)
let mask = Float32x4.cmpeq a b    (* a == b per element *)
let mask = Float32x4.cmpgt a b    (* a > b per element *)
```

### Min/Max

```ocaml
let mins = Float32x4.min a b      (* Element-wise min *)
let maxs = Float32x4.max a b      (* Element-wise max *)
```

---

## Load and Store

### From Arrays

```ocaml
let arr = [| 1.0; 2.0; 3.0; 4.0; 5.0; 6.0; 7.0; 8.0 |]

(* Load 4 floats starting at index 0 *)
let v1 = Float32x4.Float_array.get arr ~idx:0
let v2 = Float32x4.Float_array.get arr ~idx:4

(* Store back *)
Float32x4.Float_array.set arr ~idx:0 result
```

### From Strings/Bytes

```ocaml
let bytes = Bytes.create 64

(* Load 16 bytes as int8x16 *)
let v = Int8x16.Bytes.get bytes ~byte:0

(* Store 16 bytes *)
Int8x16.Bytes.set bytes ~byte:0 v
```

### From Bigstring

```ocaml
open Bigstring

let buf = Bigstring.create 128

let v = Float64x2.Bigstring.get buf ~byte:0
Float64x2.Bigstring.set buf ~byte:16 result
```

---

## Shuffles and Blends

### Shuffle (ppx_simd required)

```ocaml
open Ppx_simd

(* Rearrange elements within vector *)
let v = Float32x4.set 4.0 3.0 2.0 1.0  (* [1, 2, 3, 4] *)

(* Shuffle: indices 0-3 select from source *)
let shuffled = Float32x4.shuffle [%shuffle 3, 2, 1, 0] v v
(* Result: [4, 3, 2, 1] - reversed *)

let broadcast_first = Float32x4.shuffle [%shuffle 0, 0, 0, 0] v v
(* Result: [1, 1, 1, 1] *)
```

### Blend (ppx_simd required)

```ocaml
(* Select elements from two vectors based on mask *)
let a = Float32x4.set 4.0 3.0 2.0 1.0  (* [1, 2, 3, 4] *)
let b = Float32x4.set 8.0 7.0 6.0 5.0  (* [5, 6, 7, 8] *)

(* Mask: 0 = from a, 1 = from b *)
let blended = Float32x4.blend [%blend 0, 1, 0, 1] a b
(* Result: [1, 6, 3, 8] *)
```

---

## Integer Operations

```ocaml
open Ocaml_simd_sse

let a = Int32x4.set 4l 3l 2l 1l
let b = Int32x4.set 8l 7l 6l 5l

(* Arithmetic *)
let sum = Int32x4.add a b
let diff = Int32x4.sub a b

(* Bitwise *)
let anded = Int32x4.and_ a b
let ored = Int32x4.or_ a b
let xored = Int32x4.xor a b

(* Shifts *)
let left = Int32x4.slli a 2    (* Shift left by 2 bits *)
let right = Int32x4.srli a 1   (* Logical shift right *)
let arith = Int32x4.srai a 1   (* Arithmetic shift right *)
```

---

## Horizontal Operations

```ocaml
(* Sum all elements *)
let v = Float32x4.set 4.0 3.0 2.0 1.0
let sum = Float32x4.hadd v v  (* Horizontal add pairs *)
let sum = Float32x4.hadd sum sum  (* Complete sum in element 0 *)

(* For complete horizontal sum, often need multiple steps *)
```

---

## AVX Operations

```ocaml
open Ocaml_simd_avx

(* 256-bit vectors - double the width *)
let v = Float64x4.set 4.0 3.0 2.0 1.0
let w = Float64x4.set 8.0 7.0 6.0 5.0

let sum = Float64x4.add v w  (* 4 doubles in parallel *)

(* Can also use 256-bit integer vectors *)
let i = Int32x8.set 8l 7l 6l 5l 4l 3l 2l 1l
```

---

## SIMD Load/Store Intrinsics (NEW in 5.2.0minus-25)

Direct memory operations with proper alignment handling:

```ocaml
(* Aligned load/store - requires 16/32-byte alignment *)
external vec128_load_aligned : bytes -> int -> int8x16#
external vec128_store_aligned : bytes -> int -> int8x16# -> unit

(* Unaligned load/store - works with any alignment *)
external vec128_load_unaligned : bytes -> int -> int8x16#
external vec128_store_unaligned : bytes -> int -> int8x16# -> unit

(* Non-temporal stores - bypass cache, good for streaming writes *)
external vec128_store_aligned_uncached : bytes -> int -> int8x16# -> unit

(* Partial loads *)
external vec128_load_low64 : bytes -> int -> int64x2#  (* Load 64 bits to low lane *)
external vec128_load_low32 : bytes -> int -> int32x4#  (* Load 32 bits to low lane *)
```

---

## AVX2 Gather Intrinsics (NEW in 5.2.0minus-25)

Gather operations load multiple values from non-contiguous memory addresses:

```ocaml
(* Gather 32-bit integers using int32 indices *)
(* Base address + indices * scale, masked by mask *)
external gather_int32x4 :
  base:nativeint -> indices:int32x4# -> scale:int -> mask:int32x4# -> int32x4#

(* Gather 64-bit integers *)
external gather_int64x2 :
  base:nativeint -> indices:int64x2# -> scale:int -> mask:int64x2# -> int64x2#

(* Gather floats *)
external gather_float32x4 :
  base:nativeint -> indices:int32x4# -> scale:int -> mask:float32x4# -> float32x4#

external gather_float64x2 :
  base:nativeint -> indices:int64x2# -> scale:int -> mask:float64x2# -> float64x2#

(* Scale must be 1, 2, 4, or 8 *)
```

---

## BMI/BMI2 Intrinsics (NEW in 5.2.0minus-25)

Bit manipulation instructions for efficient bit operations:

### BMI (Bit Manipulation Instruction Set 1)

```ocaml
(* ANDN: Bitwise AND of inverted first operand with second *)
external bmi_andn_int32 : int32# -> int32# -> int32#
external bmi_andn_int64 : int64# -> int64# -> int64#

(* BEXTR: Bit field extract *)
external bmi_bextr_int32 : int32# -> int32# -> int32#
external bmi_bextr_int64 : int64# -> int64# -> int64#

(* BLSI: Extract lowest set bit *)
external bmi_blsi_int32 : int32# -> int32#
external bmi_blsi_int64 : int64# -> int64#

(* BLSMSK: Get mask up to lowest set bit *)
external bmi_blsmsk_int32 : int32# -> int32#
external bmi_blsmsk_int64 : int64# -> int64#

(* BLSR: Reset lowest set bit *)
external bmi_blsr_int32 : int32# -> int32#
external bmi_blsr_int64 : int64# -> int64#

(* TZCNT: Count trailing zero bits *)
external bmi_tzcnt_int32 : int32# -> int32#
external bmi_tzcnt_int64 : int64# -> int64#
```

### BMI2 (Bit Manipulation Instruction Set 2)

```ocaml
(* BZHI: Zero high bits starting at specified position *)
external bmi2_bzhi_int32 : int32# -> int32# -> int32#
external bmi2_bzhi_int64 : int64# -> int64# -> int64#

(* MULX: Unsigned multiply without affecting flags *)
external bmi2_mulx_int32 : int32# -> int32# -> #(int32# * int32#)
external bmi2_mulx_int64 : int64# -> int64# -> #(int64# * int64#)

(* PDEP: Parallel bits deposit *)
external bmi2_pdep_int32 : int32# -> int32# -> int32#
external bmi2_pdep_int64 : int64# -> int64# -> int64#

(* PEXT: Parallel bits extract *)
external bmi2_pext_int32 : int32# -> int32# -> int32#
external bmi2_pext_int64 : int64# -> int64# -> int64#

(* RORX: Rotate right without affecting flags *)
external bmi2_rorx_int32 : int32# -> int -> int32#
external bmi2_rorx_int64 : int64# -> int -> int64#

(* SARX/SHRX/SHLX: Shift without affecting flags *)
external bmi2_sarx_int32 : int32# -> int32# -> int32#
external bmi2_shrx_int64 : int64# -> int64# -> int64#
external bmi2_shlx_int32 : int32# -> int32# -> int32#
```

### POPCNT/LZCNT

```ocaml
(* Population count: count set bits *)
external popcnt_int32 : int32# -> int32#
external popcnt_int64 : int64# -> int64#

(* Leading zero count *)
external lzcnt_int32 : int32# -> int32#
external lzcnt_int64 : int64# -> int64#
```

---

## 128-bit Integer Arithmetic (NEW in 5.2.0minus-25)

Support for wide integer operations using SIMD registers:

```ocaml
(* 128-bit add/subtract carried through register pairs *)
external int128_add : int64# -> int64# -> int64# -> int64# -> #(int64# * int64#)
external int128_sub : int64# -> int64# -> int64# -> int64# -> #(int64# * int64#)
```

---

## C FFI

### External Declarations

```ocaml
(* Unboxed external - no allocation overhead *)
external simd_process : (float32x4#[@unboxed]) -> (float32x4#[@unboxed]) =
  "boxed_simd_process" "unboxed_simd_process"

(* For 256-bit *)
external avx_process : (float64x4#[@unboxed]) -> (float64x4#[@unboxed]) =
  "boxed_avx_process" "unboxed_avx_process"
```

### C Implementation

```c
#include <caml/simd.h>
#include <immintrin.h>

// Unboxed version - efficient
__m128 unboxed_simd_process(__m128 v) {
  return _mm_sqrt_ps(v);
}

// Boxed wrapper
CAMLprim value boxed_simd_process(value v) {
  return caml_copy_vec128(unboxed_simd_process(Vec128_val(v)));
}

// For 256-bit
__m256d unboxed_avx_process(__m256d v) {
  return _mm256_sqrt_pd(v);
}

CAMLprim value boxed_avx_process(value v) {
  return caml_copy_vec256d(unboxed_avx_process(Vec256_vald(v)));
}
```

---

## Common Patterns

### Vector Dot Product

```ocaml
let dot4 (a : float32x4#) (b : float32x4#) : float =
  let prod = Float32x4.mul a b in
  let sum1 = Float32x4.hadd prod prod in
  let sum2 = Float32x4.hadd sum1 sum1 in
  Float32x4.extract sum2 0
```

### Process Array in Chunks

```ocaml
let process_array (arr : float array) : unit =
  let len = Array.length arr in
  let vec_len = len / 4 * 4 in

  (* Process 4 elements at a time *)
  for i = 0 to vec_len / 4 - 1 do
    let v = Float32x4.Float_array.get arr ~idx:(i * 4) in
    let result = Float32x4.sqrt v in
    Float32x4.Float_array.set arr ~idx:(i * 4) result
  done;

  (* Handle remainder *)
  for i = vec_len to len - 1 do
    arr.(i) <- Float.sqrt arr.(i)
  done
```

### SIMD-friendly Record

```ocaml
type vec4 = {
  data : float32x4#;
}

let add_vec4 a b = {
  data = Float32x4.add a.data b.data
}
```

---

## Performance Tips

1. **Use unboxed vectors** (`#` suffix) in hot loops
2. **Align data** for better load/store performance
3. **Avoid horizontal operations** when possible (they're slower)
4. **Process in chunks** matching vector width
5. **Use `[@inline always]`** on small SIMD functions
6. **Prefer AVX2** for 256-bit operations when available

---

## Limitations

- x86-64 only (ARM NEON coming soon)
- Requires SSE2 minimum, AVX/AVX2 for 256-bit
- BMI/BMI2 require specific CPU support (Haswell+)
- No auto-vectorization (explicit SIMD required)
- Alignment not automatically guaranteed

---

## Checking CPU Features

```ocaml
(* Runtime check for AVX support *)
external has_avx : unit -> bool = "caml_has_avx" [@@noalloc]

let use_best_implementation () =
  if has_avx () then
    process_avx data
  else
    process_sse data
```

See also: [SKILL-UNBOXED.md](SKILL-UNBOXED.md) for unboxed types,
[SKILL-ZERO-ALLOC.md](SKILL-ZERO-ALLOC.md) for allocation-free SIMD code.
