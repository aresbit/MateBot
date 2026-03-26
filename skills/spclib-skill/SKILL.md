---
name: spclib
description: |
  This skill should be used when the user asks to "write C code with sp.h", "use spclib", "sp.h API", "single-header C library",
  "modern C programming", "sp_str_t usage", "sp_alloc memory", "SP_LOG formatting", "dynamic array in C", "hash table in C",
  "cross-platform C code", or when working with the sp.h single-header C standard library replacement.
license: MIT
---

# spclib - sp.h Programming Guide

sp.h is a single-header C standard library replacement providing modern, type-safe APIs for memory management, strings, containers, IO, and cross-platform system operations.

## Core Principles

**Always follow these rules when using sp.h:**

| Never Use | Use Instead |
|-----------|-------------|
| `malloc`/`calloc`/`realloc` | `sp_alloc()` |
| `const char*` | `sp_str_t` (ptr+len string) |
| `strcmp`/`strlen` | `sp_str_equal()` / `sp_str_len()` |
| `printf` | `SP_LOG()` |
| `memset(&obj, 0, sizeof(obj))` | `SP_ZERO_INITIALIZE()` |
| `for(i=0; i<n; i++)` on arrays | `sp_dyn_array_for()` / `sp_carr_for()` |

## Quick Reference

### Setup
```c
// In ONE C file only:
#define SP_IMPLEMENTATION
#include "sp.h"
```

### Types
- `s8/s16/s32/s64` - signed integers
- `u8/u16/u32/u64` - unsigned integers
- `f32/f64` - floats
- `c8` - char (UTF-8)
- `sp_str_t` - {data, len} string (no null terminator)

### String Operations
```c
sp_str_t s = sp_str_lit("hello");     // Compile-time literal
sp_str_t v = sp_str_view(cstr);       // View from C string
bool eq = sp_str_equal(a, b);         // Compare
bool empty = sp_str_empty(s);         // Check empty
```

### Dynamic Arrays
```c
sp_dyn_array(int) arr = SP_NULLPTR;
sp_dyn_array_push(arr, 42);
sp_dyn_array_for(arr, i) { /* use arr[i] */ }
```

### Directory Iteration
```c
// Simple directory traversal
sp_fs_for(dir, it) {
  SP_LOG("Entry: {}", SP_FMT_STR(it.entry.name));
}

// Recursive directory traversal
sp_fs_for_recursive(dir, it) {
  SP_LOG("Path: {}", SP_FMT_STR(it.entry.path));
}
```

### Hash Tables
```c
sp_ht(sp_str_t, s32) map = SP_NULLPTR;
sp_ht_set_fns(map, sp_ht_hash_str, sp_ht_compare_str);
sp_ht_insert(map, sp_str_lit("key"), 100);
s32* val = sp_ht_getp(map, sp_str_lit("key"));
```

### Logging
```c
SP_LOG("Value: {}", SP_FMT_S32(x));
SP_LOG("{:fg green}Success{:reset}", SP_FMT_CSTR(""));
```

## Module Namespaces

Search `references/index.md` for detailed API signatures:

| Namespace | Purpose | Key Functions |
|-----------|---------|---------------|
| `sp_str_*` | String operations | `sp_str_lit`, `sp_str_equal`, `sp_str_empty` |
| `sp_cstr_*` | C string operations | `sp_cstr_len`, `sp_cstr_equal` |
| `sp_dyn_array_*` / `sp_da` | Dynamic arrays | `sp_dyn_array_push`, `sp_dyn_array_for` |
| `sp_ht_*` | Hash tables | `sp_ht_insert`, `sp_ht_getp`, `sp_ht_for` |
| `sp_alloc` / `sp_free` | Memory allocation | `sp_alloc`, `sp_realloc`, `sp_free` |
| `sp_io_*` | File IO | `sp_io_read_file`, `sp_io_write_file` |
| `sp_fs_*` | Filesystem | `sp_fs_exists`, `sp_fs_read`, `sp_fs_write`, `sp_fs_for`, `sp_fs_for_recursive` |
| `sp_ps_*` | Processes | `sp_ps_run`, `sp_ps_spawn` |
| `sp_tm_*` | Time | `sp_tm_now_ns`, `sp_tm_sleep_ms` |
| `sp_thread_*` | Threads | `sp_thread_create`, `sp_thread_join` |
| `sp_mutex_*` | Mutexes | `sp_mutex_init`, `sp_mutex_lock` |
| `sp_env_*` | Environment | `sp_env_get`, `sp_env_set` |
| `sp_os_*` | Platform | `sp_os_get_executable_ext` |
| `SP_LOG` / `SP_FMT_*` | Logging | `SP_LOG`, `SP_FMT_STR`, `SP_FMT_S32` |

## Common Patterns

### Zero Initialization
```c
my_struct_t obj = SP_ZERO_INITIALIZE();
```

### Error Handling
```c
sp_try(expr);                    // Return if expr fails
sp_try_goto(expr);               // goto sp_try_label if expr fails
sp_try_as_goto(expr, label);     // goto label if expr fails
sp_require(ptr != NULL);         // Return if condition false
SP_ASSERT(condition);            // Assert
SP_FATAL("msg {}", SP_FMT(...)); // Log and exit
```

### Switch Statements
```c
switch (val) {
  case A: { break; }
  case B: { break; }
  default: { SP_UNREACHABLE_CASE(); }
}
```

## Reference Files

For complete API documentation with full function signatures:
- **`references/index.md`** - Comprehensive API reference with all function signatures, types, and macros

## Examples

Example code demonstrating sp.h usage:

| File | Description |
|------|-------------|
| `references/example/msvc.c` | MSVC compiler specific examples |
| `references/example/cli/palette.c` | Terminal color palette demo |
| `references/example/cli/prompt.c` | Interactive CLI prompt example |
| `references/example/freestanding/jit.c` | Just-in-time compilation example |
| `references/example/freestanding/embed.c` | Embedded usage example |

## Finding APIs

When looking for a specific function:
1. Check the namespace table above
2. Search `references/index.md` for the pattern
3. All public APIs are prefixed with `SP_API` in the source
