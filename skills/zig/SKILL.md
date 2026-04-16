---
name: zig
description: Up-to-date Zig programming language patterns for version 0.16.0. Use when writing, reviewing, or debugging Zig code, working with build.zig and build.zig.zon files, or using comptime metaprogramming. Critical for avoiding outdated patterns from training data - especially build system APIs (root_module instead of root_source_file), I/O APIs (buffered writer pattern), container initialization (.empty/.init), allocator selection (DebugAllocator), and removed language features (@Type, @cImport, async/await, usingnamespace).
---

# Zig Language Reference (v0.16.0)

Zig evolves rapidly. Training data contains outdated patterns that cause compilation errors. This skill documents breaking changes and correct modern patterns.

## Critical: 0.16.0 Breaking Changes

### `@Type` - REMOVED
Replaced with individual type-creating builtins.

```zig
// WRONG - removed builtin
const T = @Type(.{ .int = .{ .signedness = .unsigned, .bits = 10 } });

// CORRECT
const T = @Int(.unsigned, 10);
const E = @Enum(.{ .tag_type = u8, .fields = &.{...}, .decls = &.{...}, .is_exhaustive = true });
const S = @Struct(.{ .layout = .auto, .fields = &.{...}, .decls = &.{...}, .is_tuple = false });
const U = @Union(.{ .layout = .auto, .tag_mode = .enum, .fields = &.{...}, .decls = &.{...} });
const P = @Pointer(.{ .size = .One, .is_const = false, .child = u8 });
const F = @Fn(.{ .calling_convention = .Unspecified, .is_var_args = false, .return_type = void, .params = &.{...} });
const L = @EnumLiteral("name"); // or just .name in most contexts
```

### `@cImport` - DEPRECATED
C translation now happens in the build system. `@cImport` and `@cInclude` are deprecated.

```zig
// WRONG - deprecated
pub const c = @cImport({
    @cInclude("stdio.h");
});

// CORRECT - use addTranslateC in build.zig
const c_translate = b.addTranslateC(.{
    .root_source_file = b.path("src/c.h"),
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("c", c_translate.createModule());
```

### `@intFromFloat` - DEPRECATED
`@floor`, `@ceil`, `@round`, `@trunc` now convert floats directly to integers.

```zig
// WRONG - deprecated
const n: u8 = @intFromFloat(@floor(value));

// CORRECT
const n: u8 = @floor(value);
const m: i32 = @round(value);
```

### Runtime Vector Indexing - REMOVED
Vector indexing with runtime indices is no longer allowed. Coerce to array first.

```zig
// WRONG - compile error
_ = vector[i];

// CORRECT
const array: [vector_type.len]vector_type.child = vector;
for (&array) |elem| { _ = elem; }
```

### Returning Address of Local Variable - REMOVED
Returning `&x` where `x` is a local variable is now a compile error.

```zig
// WRONG - "returning address of expired local variable"
fn getX() *i32 {
    var x: i32 = 5;
    return &x;
}

// CORRECT - allocate on heap or use static storage
```

### Pointers in Packed Structs/Unions - REMOVED
Pointer fields are no longer allowed in `packed struct` or `packed union`.

```zig
// WRONG
const S = packed struct { ptr: *u8 };

// CORRECT - use usize and convert with @ptrFromInt/@intFromPtr
const S = packed struct { ptr: usize };
```

### Vectors and Arrays No Longer Support In-Memory Coercion
Use direct coercion instead of `@ptrCast` between array and vector memory.

### Extern Contexts Require Explicit Backing Types
`enum`, `packed struct`, and `packed union` with inferred backing types are invalid in `extern` contexts.

```zig
// WRONG
const E = enum { a, b };
export var e: E = .a;

// CORRECT
const E = enum(u8) { a, b };
export var e: E = .a;
```

### Packed Union Field Size Constraints
All fields of a packed union must have the same `@bitSizeOf` as the backing integer. Use explicit backing integer `packed union(T)` and padding structs where needed.

```zig
// WRONG
const U = packed union { x: u8, y: u16 };

// CORRECT
const U = packed union(u16) {
    x: packed struct(u16) { data: u8, padding: u8 = 0 },
    y: u16,
};
```

## Critical: Removed Features (0.15.x)

### `usingnamespace` - REMOVED
```zig
// WRONG - compile error
pub usingnamespace @import("other.zig");

// CORRECT - explicit re-export
const other = @import("other.zig");
pub const foo = other.foo;
```

### `async`/`await` - REMOVED
Keywords removed from language. Async I/O support is planned for future releases.

## Critical: I/O API Rewrite ("Writergate")

The entire `std.io` API changed. New `std.Io.Writer` and `std.Io.Reader` are **non-generic** with buffer in the interface.

### Writing
```zig
// WRONG - old API
const stdout = std.io.getStdOut().writer();
try stdout.print("Hello\n", .{});

// CORRECT - new API: provide buffer, access .interface, flush
var buf: [4096]u8 = undefined;
var stdout_writer = std.fs.File.stdout().writer(&buf);
const stdout = &stdout_writer.interface;
try stdout.print("Hello\n", .{});
try stdout.flush();  // REQUIRED!
```

### Reading
```zig
// Reading from file
var buf: [4096]u8 = undefined;
var file_reader = file.reader(&buf);
const r = &file_reader.interface;

// Read line by line (takeDelimiter returns null at EOF)
while (try r.takeDelimiter('\n')) |line| {
    // process line (doesn't include '\n')
}

// Read binary data
const header = try r.takeStruct(Header, .little);
const value = try r.takeInt(u32, .big);
```

### Fixed Buffer Writer (no file)
```zig
var buf: [256]u8 = undefined;
var w: std.Io.Writer = .fixed(&buf);
try w.print("Hello {s}", .{"world"});
const result = w.buffered();  // "Hello world"
```

### Fixed Reader (from slice)
```zig
var r: std.Io.Reader = .fixed("hello\nworld");
const line = (try r.takeDelimiter('\n')).?;  // "hello" (returns null at EOF)
```

**Deprecated:** `BufferedWriter`, `CountingWriter`, `std.io.bufferedWriter()`

**Deprecated:** `GenericWriter`, `GenericReader`, `AnyWriter`, `AnyReader`, `FixedBufferStream`

**New:** `std.Io.Writer`, `std.Io.Reader` - non-generic, buffer in interface

**Replacements:**
- `CountingWriter` → `std.Io.Writer.Discarding` (has `.fullCount()`)
- `BufferedWriter` → buffer provided to `.writer(&buf)` call
- Allocating output → `std.Io.Writer.Allocating`

## Critical: Build System (0.15.x)

`root_source_file` is REMOVED from `addExecutable`/`addLibrary`/`addTest`. Use `root_module`:

```zig
// WRONG - removed field
b.addExecutable(.{
    .name = "app",
    .root_source_file = b.path("src/main.zig"),  // ERROR
    .target = target,
});

// CORRECT
b.addExecutable(.{
    .name = "app",
    .root_module = b.createModule(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    }),
});
```

**Module imports changed:**
```zig
// WRONG (old API)
exe.addModule("helper", helper_mod);

// CORRECT
exe.root_module.addImport("helper", helper_mod);
```

**Adding dependency modules:**
```zig
const dep = b.dependency("lib", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("lib", dep.module("lib"));
```

**Compile-level methods deprecated:** `exe.linkSystemLibrary()`, `exe.addCSourceFiles()`,
`exe.addIncludePath()`, `exe.linkLibC()` are deprecated — use `exe.root_module.*` equivalents instead.

See **[std.Build reference](references/std-build.md)** for complete build system documentation.

## Critical: Container Initialization

**Never use `.{}` for containers.** Use `.empty` or `.init`:

```zig
// WRONG - deprecated
var list: std.ArrayList(u32) = .{};
var gpa: std.heap.DebugAllocator(.{}) = .{};

// CORRECT - use .empty for empty collections
var list: std.ArrayList(u32) = .empty;
var map: std.AutoHashMapUnmanaged(u32, u32) = .empty;

// CORRECT - use .init for stateful types with internal config
var gpa: std.heap.DebugAllocator(.{}) = .init;
var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
```

### Naming Changes
- **`std.ArrayListUnmanaged` → `std.ArrayList`** (Unmanaged is now default, old name deprecated)
- **`std.heap.GeneralPurposeAllocator` → `std.heap.DebugAllocator`** (GPA alias still works)

**`std.BoundedArray` - REMOVED.** Use:
```zig
var buffer: [8]i32 = undefined;
var stack = std.ArrayList(i32).initBuffer(&buffer);
```

## Critical: Format Strings (0.15.x)

`{f}` required to call format methods:
```zig
// WRONG - ambiguous error
std.debug.print("{}", .{std.zig.fmtId("x")});

// CORRECT
std.debug.print("{f}", .{std.zig.fmtId("x")});
```

Format method signature changed:
```zig
// OLD - wrong
pub fn format(self: @This(), comptime fmt: []const u8, opts: std.fmt.FormatOptions, writer: anytype) !void

// NEW - correct
pub fn format(self: @This(), writer: *std.Io.Writer) std.Io.Writer.Error!void
```

## Breaking Changes (0.14.0+)

### `@branchHint` replaces `@setCold`
```zig
// WRONG
@setCold(true);

// CORRECT
@branchHint(.cold);  // Must be first statement in block
```

### `@export` takes pointer
```zig
// WRONG
@export(foo, .{ .name = "bar" });

// CORRECT
@export(&foo, .{ .name = "bar" });
```

### Inline asm clobbers are typed
```zig
// WRONG
: "rcx", "r11"

// CORRECT
: .{ .rcx = true, .r11 = true }
```

### `@fence` - REMOVED
Use stronger atomic orderings or RMW operations instead.

## Decl Literals (0.14.0+)

`.identifier` syntax works for declarations:
```zig
const S = struct {
    x: u32,
    const default: S = .{ .x = 0 };
    fn init(v: u32) S { return .{ .x = v }; }
};

const a: S = .default;      // S.default
const b: S = .init(42);     // S.init(42)
const c: S = try .init(1);  // works with try
```

## Labeled Switch (0.14.0+)

State machines use `continue :label`:
```zig
state: switch (initial) {
    .idle => continue :state .running,
    .running => if (done) break :state result else continue :state .running,
    .error => return error.Failed,
}
```

## Non-exhaustive Enum Switch (0.15.x)

Can mix explicit tags with `_` and `else`:
```zig
switch (value) {
    .a, .b => {},
    else => {},  // other named tags
    _ => {},     // unnamed integer values
}
```

## 0.16.0 Additive Changes

### Switch Enhancements
`packed struct` and `packed union` can now be used as switch prongs. Decl literals and `@enumFromInt` work in prongs. Union tag captures allowed for all prongs. Captures may no longer all be discarded.

### Small Integers Coerce to Floats
Integers that fit exactly in a float's significand coerce implicitly.

```zig
var f: f32 = foo_int; // u24 coerces safely; u25 still needs @floatFromInt
```

### Unary Float Builtins Forward Result Type
`@sqrt`, `@sin`, `@cos`, `@tan`, `@exp`, `@exp2`, `@log`, `@log2`, `@log10`, `@floor`, `@ceil`, `@trunc`, `@round` now forward result type.

```zig
const x: f64 = @sqrt(@floatFromInt(N)); // now works directly
```

### Explicit Backing Integers on Packed Unions
`packed union(T)` syntax now supported, matching `packed struct(T)`.

```zig
const Split16 = packed union(u16) { raw: MaybeSigned16, split: packed struct { low: u8, high: u8 } };
```

### Explicitly-Aligned Pointer Types Are Distinct
`*u8` and `*align(1) u8` are now distinct types, though they still coerce to each other.

### Lazy Field Analysis
Structs, unions, enums, and opaques are only resolved when size or field type is required. Using types as namespaces no longer pulls in unused fields.

### Pointers to Comptime-Only Types Are Runtime Types
`*comptime_int` and `[]comptime_int` are now runtime types (though dereferencing remains comptime-only).

## Quick Fixes

| Error | Fix |
|-------|-----|
| `@Type was removed from the language` | Use `@Int`, `@Enum`, `@Struct`, `@Union`, `@Pointer`, `@Fn`, `@Tuple`, `@EnumLiteral` |
| `@cImport is deprecated` | Use `b.addTranslateC()` in build.zig |
| `@intFromFloat is deprecated` | Use `@floor`, `@ceil`, `@round`, or `@trunc` directly to integer |
| `runtime index into vector type` | Coerce vector to array first: `const arr: [N]T = vector;` |
| `returning address of expired local variable` | Return by value, use heap allocation, or use static storage |
| `packed structs and unions cannot contain pointers` | Use `usize` with `@ptrFromInt`/`@intFromPtr` |
| `no field 'root_source_file'` | Use `root_module = b.createModule(.{...})` |
| `use of undefined value` | Arithmetic on `undefined` is now illegal |
| `type 'f32' cannot represent integer` | Use float literal: `123_456_789.0` not `123_456_789` |
| `ambiguous format string` | Use `{f}` for format methods |
| `sanitize_c = true` | Type changed to `?std.zig.SanitizeC` — use `.full`, `.trap`, or `.off` |
| `std.fifo.LinearFifo` | Removed — use `std.Io.Reader`/`Writer` patterns |
| `posix.sendfile` | Removed — use `std.fs.File` writer `.sendFileAll()` |
| `std.fmt.Formatter` | Deprecated — renamed to `std.fmt.Alt` |
| `fmtSliceEscapeLower`/`Upper` | Use `std.ascii.hexEscape(bytes, .lower/.upper)` |

## Language References

Load these references when working with core language features:

### Code Style
- **[Style Guide](references/style-guide.md)** - Official Zig naming conventions (TitleCase types, camelCase functions, snake_case variables), whitespace rules, doc comment guidance, redundancy avoidance, `zig fmt`

### Language Basics & Built-ins
- **[Language Basics](references/language.md)** - Core language: types, control flow (if/while/for/switch), error handling (try/catch/errdefer), optionals, structs, enums, unions, pointers, slices, comptime, functions
- **[Built-in Functions](references/builtins.md)** - All `@` built-ins: type casts (@intCast, @bitCast, @ptrCast), arithmetic (@addWithOverflow, @divExact), bit ops (@clz, @popCount), memory (@memcpy, @sizeOf), atomics (@atomicRmw, @cmpxchgWeak), introspection (@typeInfo, @TypeOf, @hasDecl, @Int, @Struct, @Union, @Enum), SIMD (@Vector, @splat, @reduce), C interop (@export, addTranslateC in build system)

## Standard Library References

Load these references when working with specific modules:

### Memory & Slices
- **[std.mem](references/std-mem.md)** - Slice search/compare, split/tokenize, alignment, endianness, byte conversion

### Text & Encoding
- **[std.fmt](references/std-fmt.md)** - Format strings, integer/float parsing, hex encoding, custom formatters, `{f}` specifier (0.15.x)
- **[std.ascii](references/std-ascii.md)** - ASCII character classification (isAlpha, isDigit), case conversion, case-insensitive comparison
- **[std.unicode](references/std-unicode.md)** - UTF-8/UTF-16 encoding/decoding, codepoint iteration, validation, WTF-8 for Windows
- **[std.base64](references/std-base64.md)** - Base64 encoding/decoding (standard, URL-safe, with/without padding)

### Math & Random
- **[std.math](references/std-math.md)** - Floating-point ops, trig, overflow-checked arithmetic, constants, complex numbers, big integers
- **[std.Random](references/std-random.md)** - PRNGs (Xoshiro256, Pcg), CSPRNGs (ChaCha), random integers/floats/booleans, shuffle, distributions
- **[std.hash](references/std-hash.md)** - Non-cryptographic hash functions (Wyhash, XxHash, FNV, Murmur, CityHash), checksums (CRC32, Adler32), auto-hashing

### SIMD & Vectorization
- **[std.simd](references/std-simd.md)** - SIMD vector utilities: optimal vector length, iota/repeat/join/interlace patterns, element shifting/rotation, parallel searching, prefix scans, branchless selection

### Time & Timing
- **[std.time](references/std-time.md)** - Wall-clock timestamps, monotonic Instant/Timer, epoch conversions, calendar utilities (year/month/day), time unit constants
- **[std.Tz](references/std-tz.md)** - TZif timezone database parsing (RFC 8536), UTC offsets, DST rules, timezone abbreviations, leap seconds

### Sorting & Searching
- **[std.sort](references/std-sort.md)** - Sorting algorithms (pdq, block, heap, insertion), binary search, min/max

### Core Data Structures
- **[std.ArrayList](references/std-arraylist.md)** - Dynamic arrays, vectors, BoundedArray replacement
- **[std.HashMap / AutoHashMap](references/std-hashmap.md)** - Hash maps, string maps, ordered maps
- **[std.ArrayHashMap](references/std-array-hash-map.md)** - Insertion-order preserving hash map, array-style key/value access
- **[std.MultiArrayList](references/std-multi-array-list.md)** - Struct-of-arrays for cache-efficient struct storage
- **[std.SegmentedList](references/std-segmented-list.md)** - Stable pointers, arena-friendly, non-copyable types
- **[std.DoublyLinkedList / SinglyLinkedList](references/std-linked-list.md)** - Intrusive linked lists, O(1) insert/remove
- **[std.PriorityQueue](references/std-priority-queue.md)** - Binary heap, min/max extraction, task scheduling
- **[std.PriorityDequeue](references/std-priority-dequeue.md)** - Min-max heap, double-ended priority extraction
- **[std.Treap](references/std-treap.md)** - Self-balancing BST, ordered keys, min/max/predecessor
- **[std.bit_set](references/std-bit-set.md)** - Bit sets (Static, Dynamic, Integer, Array), set operations, iteration
- **[std.BufMap / BufSet](references/std-buf-map.md)** - String-owning maps and sets, automatic key/value memory management
- **[std.StaticStringMap](references/std-static-string-map.md)** - Compile-time optimized string lookup, perfect hash for keywords
- **[std.enums](references/std-enums.md)** - EnumSet, EnumMap, EnumArray: bit-backed enum collections

### Allocators
- **[std.heap](references/std-allocators.md)** - Allocator selection guide, ArenaAllocator, DebugAllocator, FixedBufferAllocator, MemoryPool, SmpAllocator, ThreadSafeAllocator, StackFallbackAllocator, custom allocator implementation

### I/O & Files
- **[std.io](references/std-io.md)** - Reader/Writer API (0.15.x): buffered I/O, streaming, binary data, format strings
- **[std.fs](references/std-fs.md)** - File system: files, directories, iteration, atomic writes, paths
- **[std.tar](references/std-tar.md)** - Tar archive reading/writing, extraction, POSIX ustar, GNU/pax extensions
- **[std.zip](references/std-zip.md)** - ZIP archive reading/extraction, ZIP64 support, store/deflate compression
- **[std.compress](references/std-compress.md)** - Compression: DEFLATE (gzip, zlib), Zstandard, LZMA, LZMA2, XZ decompression/compression

### Networking
- **[std.http](references/std-http.md)** - HTTP client/server, TLS, connection pooling, compression, WebSocket
- **[std.net](references/std-net.md)** - TCP/UDP sockets, address parsing, DNS resolution
- **[std.Uri](references/std-uri.md)** - URI parsing/formatting (RFC 3986), percent-encoding/decoding, relative URI resolution

### Process Management
- **[std.process](references/std-process.md)** - Child process spawning, environment variables, argument parsing, exec

### OS-Specific APIs
- **[std.os](references/std-os.md)** - OS-specific APIs: Linux syscalls, io_uring, Windows NT APIs, WASI, direct platform access
- **[std.c](references/std-c.md)** - C ABI types and libc bindings: platform-specific types (fd_t, pid_t, timespec), errno values, socket/signal/memory types, fcntl/open flags, FFI with C libraries

### Concurrency
- **[std.Thread](references/std-thread.md)** - Thread spawning, Mutex, RwLock, Condition, Semaphore, WaitGroup, thread pools
- **[std.atomic](references/std-atomic.md)** - Lock-free atomic operations: Value wrapper, fetch-and-modify (add/sub/and/or/xor), compare-and-swap, atomic ordering semantics, spin loop hints, cache line sizing

### Patterns & Best Practices
- **[Zig Patterns](references/patterns.md)** - **Load when writing new code or reviewing code quality.** Comprehensive best practices extracted from the Zig standard library: quick patterns (memory/allocators, file I/O, HTTP, JSON, testing, build system) plus idiomatic code patterns covering syntax (closures, context pattern, options structs, destructuring), polymorphism (duck typing, generics, custom formatting, dynamic/static dispatch), safety (diagnostics, error payloads, defer/errdefer, compile-time assertions), and performance (const pointer passing)
- **[Code Review](references/code-review.md)** - **Load when reviewing Zig code.** Systematic checklist organized by confidence level: ALWAYS FLAG (removed features, changed syntax, API changes), FLAG WITH CONTEXT (exception safety bugs, missing flush, allocator issues), SUGGEST (style improvements). Includes migration examples for 0.14/0.15 breaking changes

### Serialization
- **[std.json](references/std-json.md)** - JSON parsing, serialization, dynamic values, streaming, custom parse/stringify
- **[std.zon](references/std-zon.md)** - ZON (Zig Object Notation) parsing and serialization for build.zig.zon, config files, data interchange

### Testing & Debug
- **[std.testing](references/std-testing.md)** - Unit test assertions and utilities
- **[std.debug](references/std-debug.md)** - Panic, assert, stack traces, hex dump, format specifiers
- **[std.log](references/std-log.md)** - Scoped logging with configurable levels and output

### Metaprogramming
- **[Comptime Reference](references/comptime.md)** - Comptime fundamentals, type reflection (`@typeInfo`/`@Int`/`@Struct`/`@Union`/`@Enum`/`@TypeOf`), loop variants (`comptime for` vs `inline for`), branch elimination, type generation, comptime limitations
- **[std.meta](references/std-meta.md)** - Type introspection, field iteration, stringToEnum, generic programming

### Compiler Utilities
- **[std.zig](references/std-zig.md)** - AST parsing, tokenization, source analysis, linters, formatters, ZON parsing

### Security & Cryptography
- **[std.crypto](references/std-crypto.md)** - Hashing (SHA2, SHA3, Blake3), AEAD (AES-GCM, ChaCha20-Poly1305), signatures (Ed25519, ECDSA), key exchange (X25519), password hashing (Argon2, scrypt, bcrypt), secure random, timing-safe operations

### Build System
- **[std.Build](references/std-build.md)** - Build system: build.zig, modules, dependencies, build.zig.zon, steps, options, testing, C/C++ integration

### Interoperability
- **[C Interop](references/c-interop.md)** - Exporting C-compatible APIs: `export fn`, C calling convention, building static/dynamic libraries, creating headers, macOS universal binaries, XCFramework for Swift/Xcode, module maps
