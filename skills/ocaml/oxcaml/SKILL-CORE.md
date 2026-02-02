# OxCaml Core Library Extensions

Jane Street's Core library builds on Base with additional OxCaml-specific
features for I/O, concurrency, and system programming.

## Mode-Aware I/O

### In_channel and Out_channel

```ocaml
open Core

(* Read with local buffer *)
val In_channel.input__local : t -> buf:bytes @ local -> pos:int -> len:int -> int

(* Fold over lines with local accumulator *)
val In_channel.fold_lines__local
  :  t
  -> init:'acc
  -> f:('acc -> string -> 'acc @ local)
  -> 'acc
```

### Bigstring I/O

```ocaml
(* Read directly into bigstring - no copy *)
val In_channel.really_input_bigstring
  :  t
  -> Bigstring.t
  -> pos:int
  -> len:int
  -> unit

(* Write from bigstring *)
val Out_channel.output_bigstring
  :  t
  -> Bigstring.t
  -> pos:int
  -> len:int
  -> unit
```

---

## Time with Unboxed Types

### Time_ns

```ocaml
module Time_ns : sig
  (* Unboxed time representation *)
  type t  (* boxed *)
  type t_unboxed = int64#  (* unboxed nanoseconds since epoch *)

  val to_int63_ns_since_epoch : t -> Int63.t
  val of_int63_ns_since_epoch : Int63.t -> t

  (* Unboxed operations *)
  module Unboxed : sig
    val now : unit -> t_unboxed
    val diff : t_unboxed -> t_unboxed -> int64#
    val add : t_unboxed -> int64# -> t_unboxed
  end
end
```

### Time_ns.Span

```ocaml
module Time_ns.Span : sig
  type t

  (* Unboxed span operations *)
  val to_int63_ns : t -> Int63.t
  val of_int63_ns : Int63.t -> t

  (* Direct nanosecond access *)
  val to_ns_unboxed : t -> int64#
  val of_ns_unboxed : int64# -> t
end
```

---

## Command with Modes

### Local Argument Parsing

```ocaml
open Core

let command =
  Command.basic
    ~summary:"Process files"
    (let%map_open.Command
       files = anon (sequence ("FILE" %: Filename_unix.arg_type))
     and verbose = flag "-v" no_arg ~doc:"Verbose output"
     in
     fun () ->
       (* Argument processing can use local *)
       let local_ processed = List.map__local files ~f:process_file in
       output_results processed)
```

---

## Iobuf with Modes

Zero-copy buffer manipulation:

```ocaml
module Iobuf : sig
  type ('rw, 'seek) t

  (* Create local iobuf *)
  val create__local : len:int -> (read_write, seek) t @ local

  (* Consume with local return *)
  val Consume.stringo__local
    :  (read, _) t
    -> len:int
    -> string @ local

  (* Peek without consuming *)
  val Peek.int64_le : (read, _) t -> pos:int -> int64
  val Peek.int64_le_unboxed : (read, _) t -> pos:int -> int64#
end
```

### Iobuf Patterns

```ocaml
let parse_packet iobuf =
  (* Peek header without consuming *)
  let msg_type = Iobuf.Peek.int8 iobuf ~pos:0 in
  let msg_len = Iobuf.Peek.int32_le iobuf ~pos:1 in

  (* Consume the message *)
  let local_ payload = Iobuf.Consume.stringo__local iobuf ~len:msg_len in
  process_message msg_type payload
```

---

## Core_unix with Modes

### File Operations

```ocaml
module Core_unix : sig
  (* Read with local buffer *)
  val read__local
    :  File_descr.t
    -> buf:bytes @ local
    -> pos:int
    -> len:int
    -> int

  (* Stat returning local record *)
  val stat__local : string -> stats @ local
  val lstat__local : string -> stats @ local
end
```

### Socket Operations

```ocaml
(* Recv with local buffer *)
val recv__local
  :  File_descr.t
  -> buf:bytes @ local
  -> pos:int
  -> len:int
  -> recv_flag list
  -> int

(* Recvfrom returning local address *)
val recvfrom__local
  :  File_descr.t
  -> buf:bytes @ local
  -> pos:int
  -> len:int
  -> recv_flag list
  -> int * sockaddr @ local
```

---

## Async with Modes (Async_kernel)

### Deferred with Local

```ocaml
module Deferred : sig
  (* Map with local function *)
  val map__local : 'a t -> f:('a -> 'b @ local) -> 'b t @ local

  (* Bind with local continuation *)
  val bind__local : 'a t -> f:('a -> 'b t @ local) -> 'b t @ local
end
```

### Pipe with Modes

```ocaml
module Pipe : sig
  (* Read with local return *)
  val read__local : 'a Reader.t -> [ `Ok of 'a | `Eof ] @ local Deferred.t

  (* Fold with local accumulator *)
  val fold__local
    :  'a Reader.t
    -> init:'acc
    -> f:('acc -> 'a -> 'acc @ local Deferred.t)
    -> 'acc Deferred.t
end
```

---

## Portable Async

For multicore Async:

```ocaml
(* Portable job scheduling *)
module Scheduler : sig
  val schedule__portable
    :  (unit -> unit) @ portable
    -> unit
end

(* Portable deferred operations *)
val Deferred.map__portable
  :  'a t
  -> f:('a -> 'b) @ portable
  -> 'b t @ portable
```

---

## Bigstring Extensions

Core's `Bigstring` module provides optimized operations on `Bigarray.Array1.t`
with OxCaml extensions for unboxed access and local operations.

### Type and Creation

```ocaml
module Bigstring : sig
  (* Bigstring is a char bigarray with C layout *)
  type t = (char, int8_unsigned_elt, c_layout) Bigarray.Array1.t

  (* Creation *)
  val create : int -> t
  val init : int -> f:(int -> char) -> t

  (* Local creation - stack allocated *)
  val create__local : int -> t @ local

  (* From existing data *)
  val of_string : ?pos:int -> ?len:int -> string -> t
  val of_bytes : ?pos:int -> ?len:int -> bytes -> t

  (* Sub-view (shares memory) *)
  val sub_shared : ?pos:int -> ?len:int -> t -> t
end
```

### Basic Access (Boxed)

```ocaml
(* Single byte access *)
val get : t -> int -> char
val set : t -> int -> char -> unit
val unsafe_get : t -> int -> char
val unsafe_set : t -> int -> char -> unit

(* Multi-byte access - little endian *)
val get_int16_le : t -> pos:int -> int
val get_int32_le : t -> pos:int -> int32
val get_int64_le : t -> pos:int -> int64
val get_float : t -> pos:int -> float  (* IEEE 754 double *)

(* Multi-byte access - big endian *)
val get_int16_be : t -> pos:int -> int
val get_int32_be : t -> pos:int -> int32
val get_int64_be : t -> pos:int -> int64

(* Setters follow same pattern *)
val set_int32_le : t -> pos:int -> int32 -> unit
val set_int64_le : t -> pos:int -> int64 -> unit
val set_float : t -> pos:int -> float -> unit
(* etc. *)
```

### Unboxed Access (Zero Allocation)

These functions avoid boxing overhead for numeric types:

```ocaml
(* Unboxed getters - no heap allocation *)
val get_int32_le_unboxed : t -> pos:int -> int32#
val get_int32_be_unboxed : t -> pos:int -> int32#
val get_int64_le_unboxed : t -> pos:int -> int64#
val get_int64_be_unboxed : t -> pos:int -> int64#
val get_float_unboxed : t -> pos:int -> float#

(* Unboxed setters *)
val set_int32_le_unboxed : t -> pos:int -> int32# -> unit
val set_int32_be_unboxed : t -> pos:int -> int32# -> unit
val set_int64_le_unboxed : t -> pos:int -> int64# -> unit
val set_int64_be_unboxed : t -> pos:int -> int64# -> unit
val set_float_unboxed : t -> pos:int -> float# -> unit

(* Unsafe unboxed variants (no bounds check) *)
val unsafe_get_int64_le_unboxed : t -> pos:int -> int64#
val unsafe_set_int64_le_unboxed : t -> pos:int -> int64# -> unit
(* etc. *)
```

### Bulk Operations

```ocaml
(* Memory operations *)
val length : t -> int
val blit : src:t -> src_pos:int -> dst:t -> dst_pos:int -> len:int -> unit
val memset : t -> pos:int -> len:int -> char -> unit
val memcmp : t -> pos1:int -> t -> pos2:int -> len:int -> int

(* With bytes/string *)
val blit_string_bigstring : string -> src_pos:int -> t -> dst_pos:int -> len:int -> unit
val blit_bigstring_string : t -> src_pos:int -> bytes -> dst_pos:int -> len:int -> unit
val blit_bigstring_bytes : t -> src_pos:int -> bytes -> dst_pos:int -> len:int -> unit
val blit_bytes_bigstring : bytes -> src_pos:int -> t -> dst_pos:int -> len:int -> unit
```

### String/Bytes Conversion

```ocaml
(* To string/bytes - copies data *)
val to_string : ?pos:int -> ?len:int -> t -> string
val to_bytes : ?pos:int -> ?len:int -> t -> bytes

(* Local variants - result is stack-allocated *)
val to_string__local : ?pos:int -> ?len:int -> t -> string @ local
val to_bytes__local : ?pos:int -> ?len:int -> t -> bytes @ local

(* Substring extraction *)
val get_string : t -> pos:int -> len:int -> string
val get_string__local : t -> pos:int -> len:int -> string @ local
```

### Local Operations

```ocaml
(* Find with local predicate *)
val find__local : t -> pos:int -> len:int -> f:(char -> bool @ local) -> int option

(* Iterate with local closure *)
val iter__local : t -> f:(char -> unit @ local) -> unit
val iteri__local : t -> f:(int -> char -> unit @ local) -> unit

(* Fold with local accumulator function *)
val fold__local : t -> init:'a -> f:('a -> char -> 'a @ local) -> 'a
```

### I/O Operations

```ocaml
(* File I/O - zero-copy where possible *)
val read : Unix.file_descr -> ?pos:int -> ?len:int -> t -> int
val write : Unix.file_descr -> ?pos:int -> ?len:int -> t -> int
val really_read : Unix.file_descr -> ?pos:int -> ?len:int -> t -> unit
val really_write : Unix.file_descr -> ?pos:int -> ?len:int -> t -> unit

(* With In_channel/Out_channel *)
val input : In_channel.t -> ?pos:int -> ?len:int -> t -> int
val output : Out_channel.t -> ?pos:int -> ?len:int -> t -> unit
```

### Zero-Copy Patterns

```ocaml
(* Parse binary protocol without allocation *)
let[@zero_alloc] parse_header bigstring ~pos =
  let magic = Bigstring.get_int32_le_unboxed bigstring ~pos in
  let version = Bigstring.get_int16_le bigstring ~pos:(pos + 4) in
  let length = Bigstring.get_int32_le_unboxed bigstring ~pos:(pos + 6) in
  let timestamp = Bigstring.get_int64_le_unboxed bigstring ~pos:(pos + 10) in
  #{ magic; version; length; timestamp }  (* unboxed record *)

(* Process packet stream *)
let process_packets bigstring =
  let len = Bigstring.length bigstring in
  let rec loop pos =
    if pos >= len then ()
    else begin
      let pkt_len = Bigstring.get_int32_le_unboxed bigstring ~pos in
      let pkt_len_int = Int32_u.to_int pkt_len in
      (* Process without copying *)
      handle_packet bigstring ~pos:(pos + 4) ~len:pkt_len_int;
      loop (pos + 4 + pkt_len_int)
    end
  in
  loop 0

(* Local string extraction for temporary use *)
let find_field bigstring ~field_pos ~field_len =
  let local_ field_str = Bigstring.get_string__local bigstring
    ~pos:field_pos ~len:field_len in
  lookup_field field_str  (* result escapes, string doesn't *)
```

### Comparison with Bytes

| Operation | `Bytes` | `Bigstring` | Notes |
|-----------|---------|-------------|-------|
| Allocation | OCaml heap | C heap | Bigstring avoids GC pressure |
| Max size | ~16MB (32-bit) | System limit | Bigstring for large buffers |
| Access speed | Fast | Fast | Both have optimized primitives |
| Unboxed access | No | Yes | Bigstring has `_unboxed` variants |
| mmap compatible | No | Yes | Bigstring can wrap mmap'd memory |
| Local creation | Yes | Yes | Both support stack allocation |

---

## Bin_prot with Modes

Binary protocol serialization:

```ocaml
module Bin_prot : sig
  (* Write to local buffer *)
  val write__local : 'a Type_class.writer -> buf:bytes @ local -> 'a -> int

  (* Read with local intermediate *)
  val read__local
    :  'a Type_class.reader
    -> buf:bytes @ local
    -> pos_ref:int ref
    -> 'a
end
```

---

## Sexp with Modes

### Local Sexp Operations

```ocaml
module Sexp : sig
  (* Parse to local sexp *)
  val of_string__local : string -> t @ local

  (* Convert with local intermediate *)
  val to_string__local : t -> string @ local
end
```

### Sexp_of with Local

```ocaml
(* For types with local sexp_of *)
type t [@@deriving sexp_of__local]

val sexp_of_t__local : t -> Sexp.t @ local
```

---

## Error Handling

### Or_error with Modes

```ocaml
module Or_error : sig
  val map__local : 'a t -> f:('a -> 'b @ local) -> 'b t @ local
  val bind__local : 'a t -> f:('a -> 'b t @ local) -> 'b t @ local

  (* Error creation *)
  val error_s__local : Sexp.t @ local -> _ t
end
```

### Error with Local Message

```ocaml
let validate x =
  if x < 0 then
    let local_ msg = sprintf "Invalid value: %d" x in
    Or_error.error_string__local msg
  else
    Ok x
```

---

## Common Patterns

### Zero-Copy Network Processing

```ocaml
let handle_connection fd =
  let buf = Bigstring.create 4096 in
  let rec loop () =
    match Core_unix.read_bigstring fd buf ~pos:0 ~len:4096 with
    | 0 -> ()
    | n ->
      (* Process without copying *)
      let msg_type = Bigstring.get_int8 buf ~pos:0 in
      let payload_len = Bigstring.get_int32_le_unboxed buf ~pos:1 in
      process_message buf ~msg_type ~len:(Int32_u.to_int payload_len);
      loop ()
  in
  loop ()
```

### Portable Async Pipeline

```ocaml
let%template.portable process_stream reader =
  Pipe.fold reader ~init:0 ~f:(fun count item ->
    let result = process_item item in
    log_result result;
    return (count + 1)
  )
```

### Local Buffer Reuse

```ocaml
let process_many_files files =
  (* Reuse local buffer across iterations *)
  let local_ buf = Bytes.create 8192 in
  List.iter files ~f:(fun filename ->
    In_channel.with_file filename ~f:(fun ic ->
      let n = In_channel.input__local ic ~buf ~pos:0 ~len:8192 in
      process_chunk buf ~len:n
    )
  )
```

---

## Migration Checklist

When updating Core code for OxCaml:

1. **Replace heap buffers with local** where possible
2. **Use unboxed Bigstring accessors** for binary data
3. **Use `__local` variants** for intermediate collections
4. **Add `@@portable`** annotations for multicore code
5. **Use `Iobuf`** for zero-copy buffer manipulation
6. **Use unboxed Time_ns** operations in hot paths

See also: [SKILL-BASE.md](SKILL-BASE.md) for Base extensions,
[SKILL-ZERO-ALLOC.md](SKILL-ZERO-ALLOC.md) for allocation-free patterns.
