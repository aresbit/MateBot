# sp.h API Reference Index

> Use Ctrl+F to search for specific APIs. All public functions are marked with `SP_API`.
> Function signatures use the actual types from sp.h for copy-paste accuracy.

## Table of Contents

- [Type Aliases](#type-aliases)
- [Constants & Macros](#constants--macros)
- [String (sp_str)](#string-sp_str)
- [C String (sp_cstr)](#c-string-sp_cstr)
- [Dynamic Array (sp_dyn_array)](#dynamic-array-sp_dyn_array)
- [Hash Table (sp_ht)](#hash-table-sp_ht)
- [Memory (sp_alloc)](#memory-sp_alloc)
- [IO (sp_io)](#io-sp_io)
- [Filesystem (sp_fs)](#filesystem-sp_fs)
- [Process (sp_ps)](#process-sp_ps)
- [Time (sp_tm)](#time-sp_tm)
- [Thread (sp_thread)](#thread-sp_thread)
- [Mutex (sp_mutex)](#mutex-sp_mutex)
- [Formatting (sp_format)](#formatting-sp_format)
- [Logging (SP_LOG)](#logging-sp_log)
- [Error Handling](#error-handling)
- [Atomics (sp_atomic)](#atomics-sp_atomic)
- [Context (sp_context)](#context-sp_context)
- [UTF-8 (sp_utf8)](#utf-8-sp_utf8)
- [Ring Buffer (sp_rb)](#ring-buffer-sp_rb)
- [Environment (sp_env)](#environment-sp_env)
- [Platform (sp_os)](#platform-sp_os)
- [Quick Lookup by Task](#quick-lookup-by-task)

---

## Type Aliases

### Integer Types
```c
typedef int8_t   s8;   // 8-bit signed
typedef int16_t  s16;  // 16-bit signed
typedef int32_t  s32;  // 32-bit signed
typedef int64_t  s64;  // 64-bit signed
typedef uint8_t  u8;   // 8-bit unsigned
typedef uint16_t u16;  // 16-bit unsigned
typedef uint32_t u32;  // 32-bit unsigned
typedef uint64_t u64;  // 64-bit unsigned
```

### Float Types
```c
typedef float    f32;  // 32-bit float
typedef double   f64;  // 64-bit float
```

### Char Types
```c
typedef char     c8;   // UTF-8 character
typedef wchar_t  c16;  // Wide character
```

### Core Structs
```c
// String type (ptr + len, no null termination)
typedef struct {
  const c8* data;
  u32 len;
} sp_str_t;

// IO Writer
typedef struct {
  sp_write_fn write;
  void* ctx;
} sp_io_writer_t;

// IO Reader
typedef struct {
  sp_read_fn read;
  void* ctx;
} sp_io_reader_t;

// Process result
typedef struct {
  sp_str_t stdout;
  sp_str_t stderr;
  s32 status;
} sp_ps_result_t;

// Time
typedef struct {
  s32 year;
  s32 month;
  s32 day;
  s32 hour;
  s32 minute;
  s32 second;
  s32 millisecond;
  s32 microsecond;
  s32 nanosecond;
} sp_tm_datetime_t;

// Thread
typedef struct sp_thread_s sp_thread_t;
typedef void (*sp_thread_fn)(void* arg);

// Mutex
typedef struct sp_mutex_s sp_mutex_t;

// Semaphore
typedef struct sp_semaphore_s sp_semaphore_t;

// Atomic types
typedef _Atomic s32 sp_atomic_s32_t;
typedef _Atomic s64 sp_atomic_s64_t;
```

---

## Constants & Macros

### Null Values
```c
#define SP_NULL     0
#define SP_NULLPTR  ((void*)0)
```

### Initialization
```c
#define SP_ZERO_INITIALIZE()  {0}           // Zero init struct
#define SP_ZERO_STRUCT(T)     (T){0}        // Return zero struct of type T
```

### Utility Macros
```c
#define SP_MAX(a, b)          ((a) > (b) ? (a) : (b))
#define SP_MIN(a, b)          ((a) < (b) ? (a) : (b))
#define SP_SWAP(T, a, b)      { T _tmp = (a); (a) = (b); (b) = _tmp; }
#define SP_UNUSED(x)          ((void)(x))
#define SP_CARR_LEN(arr)      (sizeof(arr) / sizeof((arr)[0]))
```

### Loop Macros
```c
#define sp_for(it, n)         for (u32 it = 0; it < (n); it++)
#define sp_for_range(it, lo, hi) for (u32 it = (lo); it < (hi); it++)
#define sp_carr_for(arr, it)  for (u32 it = 0; it < SP_CARR_LEN(arr); it++)
```

### Alignment
```c
#define SP_MEM_ALIGNMENT      16
#define sp_align_up(ptr, align) ((void*)(((uintptr_t)(ptr) + ((align) - 1)) & ~((align) - 1)))
```

---

## String (sp_str)

### String Creation
```c
SP_API sp_str_t sp_str_lit(const c8* str);                    // Compile-time literal
SP_API sp_str_t sp_str_view(const c8* str);                   // View from C string (calculates len)
SP_API sp_str_t sp_str_from_cstr(const c8* str);              // Allocates and copies
SP_API sp_str_t sp_str_copy(sp_str_t str);                    // Deep copy
SP_API sp_str_t sp_str_sub(sp_str_t str, u32 index, u32 len); // Substring
```

### String Query
```c
SP_API u32  sp_str_len(sp_str_t str);                         // Get length
SP_API bool sp_str_empty(sp_str_t str);                       // Check if empty
SP_API bool sp_str_equal(sp_str_t a, sp_str_t b);             // Compare equality
SP_API s32  sp_str_compare(sp_str_t a, sp_str_t b);           // Compare (strcmp style)
SP_API bool sp_str_starts_with(sp_str_t str, sp_str_t prefix);
SP_API bool sp_str_ends_with(sp_str_t str, sp_str_t suffix);
SP_API u32  sp_str_find(sp_str_t str, sp_str_t substr);       // Find substring (returns index or SP_NULL)
SP_API u32  sp_str_find_char(sp_str_t str, c8 ch);            // Find character
SP_API u32  sp_str_rfind_char(sp_str_t str, c8 ch);           // Find char from end
```

### String Manipulation
```c
SP_API sp_str_t sp_str_trim(sp_str_t str);                    // Trim whitespace both ends
SP_API sp_str_t sp_str_trim_left(sp_str_t str);               // Trim left whitespace
SP_API sp_str_t sp_str_trim_right(sp_str_t str);              // Trim right whitespace
SP_API sp_str_t sp_str_to_upper(sp_str_t str);                // Uppercase (allocates)
SP_API sp_str_t sp_str_to_lower(sp_str_t str);                // Lowercase (allocates)
SP_API sp_dyn_array(sp_str_t) sp_str_split(sp_str_t str, sp_str_t delim);
```

### String Builder
```c
SP_API sp_str_builder_t sp_str_builder_make(void);            // Create builder
SP_API void sp_str_builder_append(sp_str_builder_t* b, sp_str_t str);
SP_API void sp_str_builder_append_cstr(sp_str_builder_t* b, const c8* str);
SP_API void sp_str_builder_append_char(sp_str_builder_t* b, c8 ch);
SP_API sp_str_t sp_str_builder_to_str(sp_str_builder_t* b);   // Finalize to string
SP_API void sp_str_builder_free(sp_str_builder_t* b);
```

---

## C String (sp_cstr)

```c
SP_API u32  sp_cstr_len(const c8* str);                       // strlen replacement
SP_API bool sp_cstr_equal(const c8* a, const c8* b);          // strcmp == 0
SP_API s32  sp_cstr_compare(const c8* a, const c8* b);        // strcmp replacement
SP_API bool sp_cstr_starts_with(const c8* str, const c8* prefix);
SP_API bool sp_cstr_ends_with(const c8* str, const c8* suffix);
SP_API void sp_cstr_copy(const c8* src, c8* dst, u32 dst_size);
SP_API c8*  sp_cstr_dup(const c8* str);                       // strdup replacement
```

---

## Dynamic Array (sp_dyn_array)

### Type Declaration
```c
sp_dyn_array(T) name = SP_NULLPTR;   // Declare dynamic array of type T
sp_da(T) name = SP_NULLPTR;          // Short alias
```

### Core Operations
```c
#define sp_dyn_array_push(arr, val)      // Append element
#define sp_dyn_array_pop(arr)            // Remove and return last
#define sp_dyn_array_back(arr)           // Get last element (no remove)
#define sp_dyn_array_front(arr)          // Get first element
#define sp_dyn_array_clear(arr)          // Clear (keep capacity)
#define sp_dyn_array_free(arr)           // Free memory
#define sp_dyn_array_size(arr)           // Get element count
#define sp_dyn_array_capacity(arr)       // Get capacity
#define sp_dyn_array_reserve(arr, n)     // Reserve capacity
#define sp_dyn_array_resize(arr, n)      // Resize (new elements zeroed)
#define sp_dyn_array_shrink_to_fit(arr)  // Shrink capacity to size
```

### Iteration
```c
sp_dyn_array_for(arr, it) {           // Iterate with index
  // arr[it] to access
}
```

---

## Hash Table (sp_ht)

### Type Declaration
```c
sp_ht(key_type, value_type) name = SP_NULLPTR;
```

### Core Operations
```c
#define sp_ht_set_fns(ht, hash_fn, cmp_fn)   // Set hash/compare functions
#define sp_ht_insert(ht, key, val)           // Insert key-value
#define sp_ht_getp(ht, key)                  // Get value pointer (NULL if not found)
#define sp_ht_get(ht, key)                   // Get value (0 if not found)
#define sp_ht_remove(ht, key)                // Remove key
#define sp_ht_key_exists(ht, key)            // Check if key exists
#define sp_ht_clear(ht)                      // Clear all entries
#define sp_ht_free(ht)                       // Free hash table
#define sp_ht_size(ht)                       // Get entry count
#define sp_ht_capacity(ht)                   // Get bucket count
```

### Iteration
```c
sp_ht_for(ht, it) {
  key_type* key = sp_ht_it_getkp(ht, it);   // Get key pointer
  val_type* val = sp_ht_it_getp(ht, it);    // Get value pointer
}
```

### Built-in Hash Functions
```c
SP_API u64 sp_ht_hash_str(const void* key);           // String hash
SP_API bool sp_ht_compare_str(const void* a, const void* b);  // String compare
SP_API u64 sp_ht_hash_ptr(const void* key);           // Pointer hash
SP_API bool sp_ht_compare_ptr(const void* a, const void* b);  // Pointer compare
```

---

## Memory (sp_alloc)

### Allocation
```c
SP_API void* sp_alloc(u64 size);                    // Allocate zeroed memory
SP_API void* sp_alloc_n(u64 count, u64 size);       // Allocate n * size (checks overflow)
SP_API void* sp_realloc(void* ptr, u64 new_size);   // Reallocate
SP_API void  sp_free(void* ptr);                    // Free memory
SP_API c8*   sp_strdup(const c8* str);              // Duplicate C string
SP_API c8*   sp_strndup(const c8* str, u32 len);    // Duplicate n chars
```

### Memory Operations
```c
SP_API void* sp_memset(void* dest, s32 val, u64 n);
SP_API void* sp_memcpy(void* dest, const void* src, u64 n);
SP_API void* sp_memmove(void* dest, const void* src, u64 n);
SP_API s32   sp_memcmp(const void* a, const void* b, u64 n);
SP_API void* sp_memchr(const void* ptr, s32 ch, u64 n);
```

### Memory Info
```c
SP_API u64 sp_mem_get_total_allocated(void);        // Total bytes allocated
SP_API u64 sp_mem_get_allocation_count(void);       // Number of allocations
```

---

## IO (sp_io)

### Writer
```c
SP_API sp_io_writer_t sp_io_writer_from_file(const c8* path);
SP_API sp_io_writer_t sp_io_writer_from_fd(s32 fd, sp_io_close_mode_t close_mode);
SP_API sp_io_writer_t sp_io_writer_from_dyn_mem(void);  // Write to growable buffer
SP_API sp_io_writer_t sp_io_stdout(void);
SP_API sp_io_writer_t sp_io_stderr(void);
SP_API void sp_io_writer_close(sp_io_writer_t* writer);
SP_API bool sp_io_write(sp_io_writer_t writer, const void* data, u64 len);
SP_API bool sp_io_write_str(sp_io_writer_t writer, sp_str_t str);
SP_API bool sp_io_write_cstr(sp_io_writer_t writer, const c8* str);
SP_API bool sp_io_write_fmt(sp_io_writer_t writer, const c8* fmt, ...);
```

### Reader
```c
SP_API sp_io_reader_t sp_io_reader_from_file(const c8* path);
SP_API sp_io_reader_t sp_io_reader_from_fd(s32 fd, sp_io_close_mode_t close_mode);
SP_API sp_io_reader_t sp_io_reader_from_str(sp_str_t str);
SP_API void sp_io_reader_close(sp_io_reader_t* reader);
SP_API bool sp_io_read(sp_io_reader_t reader, void* buf, u64 len);
SP_API sp_str_t sp_io_read_all(sp_io_reader_t reader);
```

### File Operations
```c
SP_API sp_str_t sp_io_read_file(const c8* path);    // Read entire file
SP_API bool sp_io_write_file(const c8* path, sp_str_t content);
SP_API bool sp_io_append_file(const c8* path, sp_str_t content);
```

---

## Filesystem (sp_fs)

### Path Operations
```c
SP_API sp_str_t sp_fs_get_cwd(void);                // Current working directory
SP_API sp_str_t sp_fs_path_join(sp_str_t a, sp_str_t b);
SP_API sp_str_t sp_fs_path_dirname(sp_str_t path);  // Get directory part
SP_API sp_str_t sp_fs_path_basename(sp_str_t path); // Get filename part
SP_API sp_str_t sp_fs_path_stem(sp_str_t path);     // Filename without extension
SP_API sp_str_t sp_fs_path_ext(sp_str_t path);      // Extension only
SP_API sp_str_t sp_fs_path_absolute(sp_str_t path);
SP_API sp_str_t sp_fs_path_normalize(sp_str_t path);
SP_API sp_str_t sp_fs_replace_ext(sp_str_t path, sp_str_t ext);  // Replace extension
```

### Path Queries
```c
SP_API bool sp_fs_exists(sp_str_t path);
SP_API bool sp_fs_is_file(sp_str_t path);
SP_API bool sp_fs_is_dir(sp_str_t path);
SP_API bool sp_fs_is_symlink(sp_str_t path);
SP_API u64  sp_fs_get_size(sp_str_t path);
SP_API u64  sp_fs_get_modified_time(sp_str_t path);
```

### Directory Operations
```c
SP_API bool sp_fs_mkdir(sp_str_t path);
SP_API bool sp_fs_mkdir_p(sp_str_t path);           // Create parent dirs too
SP_API bool sp_fs_rmdir(sp_str_t path);
SP_API bool sp_fs_rmrf(sp_str_t path);              // Remove recursively
SP_API sp_dyn_array(sp_str_t) sp_fs_list_dir(sp_str_t path);
SP_API sp_dyn_array(sp_str_t) sp_fs_list_dir_recursive(sp_str_t path);
```

### Directory Iterator
```c
// Iterator types
typedef struct {
#if defined(SP_WIN32)
  sp_win32_handle_t handle;
  sp_win32_find_data_t find_data;
  bool first;
#elif defined(SP_MACOS)
  DIR* dir;
#else
  s32 fd;
  u8 buf[SP_FS_IT_BUF_SIZE];
  s32 buf_pos;
  s32 buf_end;
#endif
  sp_str_t path;
} sp_fs_it_frame_t;

typedef struct {
  sp_fs_entry_t entry;
  sp_da(sp_fs_it_frame_t) stack;    // Stack for recursive iteration
  bool recursive;
} sp_fs_it_t;

// Iterator functions
SP_API sp_fs_it_t sp_fs_it_new(sp_str_t path);
SP_API sp_fs_it_t sp_fs_it_new_recursive(sp_str_t path);
SP_API void sp_fs_it_next(sp_fs_it_t* it);
SP_API bool sp_fs_it_valid(sp_fs_it_t* it);
SP_API void sp_fs_it_deinit(sp_fs_it_t* it);

// Iterator convenience macros
#define sp_fs_for(dir, it) \
  for (sp_fs_it_t it = sp_fs_it_new(dir); \
       sp_fs_it_valid(&it); \
       sp_fs_it_next(&it))

#define sp_fs_for_recursive(dir, it) \
  for (sp_fs_it_t it = sp_fs_it_new_recursive(dir); \
       sp_fs_it_valid(&it); \
       sp_fs_it_next(&it))
```

### File Operations
```c
SP_API bool sp_fs_copy(sp_str_t src, sp_str_t dst);
SP_API bool sp_fs_move(sp_str_t src, sp_str_t dst);
SP_API bool sp_fs_remove(sp_str_t path);
```

### Special Paths
```c
SP_API sp_str_t sp_fs_get_home_dir(void);
SP_API sp_str_t sp_fs_get_config_dir(sp_str_t app_name);
SP_API sp_str_t sp_fs_get_data_dir(sp_str_t app_name);
SP_API sp_str_t sp_fs_get_cache_dir(sp_str_t app_name);
SP_API sp_str_t sp_fs_get_temp_dir(void);
```

---

## Process (sp_ps)

### Run Commands
```c
SP_API sp_ps_result_t sp_ps_run(sp_str_t command);
SP_API sp_ps_result_t sp_ps_run_async(sp_str_t command);
SP_API sp_ps_result_t sp_ps_run_with_env(sp_str_t command, sp_str_t* env, u32 env_count);
```

### Process Management
```c
SP_API sp_ps_t* sp_ps_spawn(sp_str_t command);
SP_API sp_ps_t* sp_ps_spawn_with_env(sp_str_t command, sp_str_t* env, u32 env_count);
SP_API s32 sp_ps_wait(sp_ps_t* ps);
SP_API bool sp_ps_kill(sp_ps_t* ps);
SP_API bool sp_ps_is_running(sp_ps_t* ps);
SP_API void sp_ps_free(sp_ps_t* ps);
```

---

## Time (sp_tm)

### High Resolution Time
```c
SP_API u64 sp_tm_now_ns(void);                      // Nanoseconds
SP_API u64 sp_tm_now_us(void);                      // Microseconds
SP_API u64 sp_tm_now_ms(void);                      // Milliseconds
```

### Date/Time
```c
SP_API sp_tm_datetime_t sp_tm_now_local(void);
SP_API sp_tm_datetime_t sp_tm_now_utc(void);
SP_API u64 sp_tm_to_unix_ms(sp_tm_datetime_t dt);
SP_API sp_tm_datetime_t sp_tm_from_unix_ms(u64 ms);
```

### Sleep
```c
SP_API void sp_tm_sleep_ms(u32 ms);
SP_API void sp_tm_sleep_us(u32 us);
SP_API void sp_tm_sleep_ns(u64 ns);
```

### Formatting
```c
SP_API sp_str_t sp_tm_format(sp_tm_datetime_t dt, sp_str_t fmt);
SP_API sp_str_t sp_tm_format_iso8601(sp_tm_datetime_t dt);
```

---

## Thread (sp_thread)

```c
SP_API sp_thread_t sp_thread_create(sp_thread_fn fn, void* arg);
SP_API void sp_thread_join(sp_thread_t thread);
SP_API void sp_thread_detach(sp_thread_t thread);
SP_API u64 sp_thread_current_id(void);
SP_API u64 sp_thread_get_id(sp_thread_t thread);
SP_API void sp_thread_yield(void);
```

---

## Mutex (sp_mutex)

```c
SP_API void sp_mutex_init(sp_mutex_t* mutex);
SP_API void sp_mutex_lock(sp_mutex_t* mutex);
SP_API bool sp_mutex_try_lock(sp_mutex_t* mutex);
SP_API void sp_mutex_unlock(sp_mutex_t* mutex);
SP_API void sp_mutex_destroy(sp_mutex_t* mutex);
```

---

## Formatting (sp_format)

```c
SP_API sp_str_t sp_format(const c8* fmt, ...);
SP_API sp_str_t sp_format_va(const c8* fmt, va_list args);
```

### Format Specifiers
- `{}` - Default formatting
- `{:width}` - Minimum width
- `{:0width}` - Zero-padded width
- `{:precision}` - Float precision
- `{:fg color}` - Foreground color
- `{:bg color}` - Background color
- `{:reset}` - Reset formatting

### Colors
- black, red, green, yellow, blue, magenta, cyan, white
- bright-red, bright-green, bright-yellow, bright-blue, etc.

---

## Logging (SP_LOG)

```c
SP_LOG(fmt, ...);                                   // Log with formatting
SP_LOG_INFO(fmt, ...);                              // Info level
SP_LOG_WARN(fmt, ...);                              // Warning level
SP_LOG_ERROR(fmt, ...);                             // Error level
SP_LOG_DEBUG(fmt, ...);                             // Debug level (stripped in release)
```

### Format Macros
```c
SP_FMT_S32(val)     // s32
SP_FMT_U32(val)     // u32
SP_FMT_S64(val)     // s64
SP_FMT_U64(val)     // u64
SP_FMT_F32(val)     // f32
SP_FMT_F64(val)     // f64
SP_FMT_CSTR(val)    // const c8*
SP_FMT_STR(val)     // sp_str_t
SP_FMT_BOOL(val)    // bool
SP_FMT_CHAR(val)    // c8
SP_FMT_PTR(val)     // void*
```

---

## Error Handling

### Assertions
```c
SP_ASSERT(condition);                               // Assert condition
SP_ASSERT_FMT(cond, fmt, ...);                      // Assert with message
SP_UNREACHABLE();                                   // Mark unreachable code
SP_UNREACHABLE_CASE();                              // Use in switch default
SP_FATAL(fmt, ...);                                 // Log and exit
```

### Error Propagation
```c
sp_try(expr);                                       // Return if expr != 0
sp_try_as(expr, err);                               // Return err if expr != 0
sp_try_as_null(expr);                               // Return NULL if expr != 0
sp_try_goto(expr);                                  // goto sp_try_label if expr != 0
sp_try_as_goto(expr, label);                        // goto label if expr != 0
sp_require(cond);                                   // Return if !cond
sp_require_as(cond, err);                           // Return err if !cond
sp_require_as_null(cond);                           // Return NULL if !cond
```

---

## Atomics (sp_atomic)

```c
SP_API s32 sp_atomic_load(sp_atomic_s32_t* val);
SP_API void sp_atomic_store(sp_atomic_s32_t* val, s32 new_val);
SP_API s32 sp_atomic_inc(sp_atomic_s32_t* val);
SP_API s32 sp_atomic_dec(sp_atomic_s32_t* val);
SP_API s32 sp_atomic_add(sp_atomic_s32_t* val, s32 add);
SP_API s32 sp_atomic_sub(sp_atomic_s32_t* val, s32 sub);
SP_API s32 sp_atomic_and(sp_atomic_s32_t* val, s32 mask);
SP_API s32 sp_atomic_or(sp_atomic_s32_t* val, s32 mask);
SP_API s32 sp_atomic_xor(sp_atomic_s32_t* val, s32 mask);
SP_API bool sp_atomic_cas(sp_atomic_s32_t* val, s32 expected, s32 new_val);
```

---

## Context (sp_context)

```c
SP_API sp_context_t* sp_context_get(void);          // Get thread-local context
SP_API void sp_context_push(sp_context_t* ctx);
SP_API void sp_context_pop(void);
SP_API void* sp_context_alloc(sp_context_t* ctx, u64 size);
SP_API void sp_context_free_all(sp_context_t* ctx); // Free all allocations in context
```

---

## UTF-8 (sp_utf8)

```c
SP_API u32 sp_utf8_decode(const c8* str, u32* out_codepoint);  // Decode one char, returns bytes consumed
SP_API u32 sp_utf8_encode(u32 codepoint, c8* out);             // Encode one char, returns bytes written
SP_API u32 sp_utf8_strlen(sp_str_t str);                       // Count UTF-8 characters (not bytes)
SP_API bool sp_utf8_valid(sp_str_t str);                       // Validate UTF-8
SP_API sp_str_t sp_utf8_substr(sp_str_t str, u32 start, u32 len); // Substring by char count
```

---

## Ring Buffer (sp_rb)

### Type Declaration
```c
sp_ring_buffer(T) name = SP_ZERO_INITIALIZE();
```

### Operations
```c
#define sp_rb_init(rb, capacity)         // Initialize with capacity
#define sp_rb_push(rb, val)              // Push to back
#define sp_rb_pop(rb)                    // Pop from front
#define sp_rb_peek(rb)                   // Peek front
#define sp_rb_clear(rb)                  // Clear buffer
#define sp_rb_empty(rb)                  // Check if empty
#define sp_rb_full(rb)                   // Check if full
#define sp_rb_size(rb)                   // Get size
#define sp_rb_capacity(rb)               // Get capacity
#define sp_rb_free(rb)                   // Free buffer
```

---

## Environment (sp_env)

```c
SP_API sp_str_t sp_env_get(const c8* name);         // Get environment variable
SP_API bool sp_env_set(const c8* name, const c8* value);
SP_API bool sp_env_unset(const c8* name);
SP_API sp_dyn_array(sp_str_t) sp_env_get_all(void); // Get all env vars

// Platform-specific
SP_API sp_str_t sp_os_get_executable_ext(void);     // Get platform executable extension (".exe" on Windows, "" on Unix)
```

---

## Platform (sp_os)

Platform-specific utilities:

```c
SP_API sp_str_t sp_os_get_executable_ext(void);     // Platform executable extension: ".exe" on Windows, "" on Unix/macOS
```

---

## Quick Lookup by Task

| Task | API |
|------|-----|
| Create string literal | `sp_str_lit("text")` |
| Compare strings | `sp_str_equal(a, b)` |
| Check empty string | `sp_str_empty(str)` |
| Allocate memory | `sp_alloc(size)` |
| Allocate array | `sp_alloc_n(count, size)` |
| Add to dynamic array | `sp_dyn_array_push(arr, val)` |
| Iterate dynamic array | `sp_dyn_array_for(arr, i)` |
| Insert to hash table | `sp_ht_insert(ht, key, val)` |
| Get from hash table | `sp_ht_getp(ht, key)` |
| Read file | `sp_io_read_file(path)` / `sp_fs_read(path)` |
| Write file | `sp_io_write_file(path, content)` |
| Check path exists | `sp_fs_exists(path)` |
| Join paths | `sp_fs_path_join(a, b)` |
| Run command | `sp_ps_run(cmd)` |
| Get current time | `sp_tm_now_ms()` |
| Log message | `SP_LOG("msg {}", SP_FMT_S32(x))` |
| Create thread | `sp_thread_create(fn, arg)` |
| Lock mutex | `sp_mutex_lock(&mutex)` |
| Format string | `sp_format("{}", SP_FMT_STR(s))` |
| Zero initialize | `SP_ZERO_INITIALIZE()` |
| Array length | `SP_CARR_LEN(arr)` |
| Iterate directory | `sp_fs_for(dir, it)` |
| Iterate directory recursively | `sp_fs_for_recursive(dir, it)` |
| Get executable extension | `sp_os_get_executable_ext()` |

---

## Prefix Reference

| Prefix | Meaning |
|--------|---------|
| `sp_` | Public API function/type |
| `sp_str_` | String operations (sp_str_t) |
| `sp_cstr_` | C string operations (const c8*) |
| `sp_dyn_array_` / `sp_da` | Dynamic arrays |
| `sp_ht_` | Hash tables |
| `sp_io_` | Input/output |
| `sp_fs_` | Filesystem |
| `sp_ps_` | Process/subprocess |
| `sp_tm_` | Time/date |
| `sp_thread_` | Threads |
| `sp_mutex_` | Mutexes |
| `sp_atomic_` | Atomic operations |
| `sp_context_` | Memory contexts |
| `sp_utf8_` | UTF-8 handling |
| `sp_env_` | Environment variables |
| `sp_os_` | Platform-specific APIs |
| `SP_` | Macro constant |
| `SP_FMT_` | Format macro |
