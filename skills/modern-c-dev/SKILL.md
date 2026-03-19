---
name: modern-c-dev
description: |
  Claude-optimized modern C skill from sysprog c-prog notes.
  This skill also integrates an external structured C tutorial route map
  for practical learning and debugging workflows.
  Use this skill for modern C language engineering tasks, especially when you need:
  - Memory management, pointer manipulation, and alignment guidance
  - Compiler toolchain behavior, optimization, and ABI understanding
  - Undefined behavior analysis and safety checklists
  - Low-level optimization and bitwise operations
  - Function calling conventions and control flow patterns
  - Stream I/O, EOF handling, and error patterns
  - Object-oriented design patterns in C
  - Preprocessor techniques and macro safety
  - Dynamic linking and ELF format understanding
  - Linked list and non-contiguous memory operations
  - Beginner-to-advanced C learning paths and problem diagnosis patterns

  Trigger this skill whenever the user mentions C programming, memory issues,
  pointer bugs, compiler warnings, undefined behavior, or low-level system programming.
---

# modern-c-dev

## Purpose

This skill provides practical guidance for modern C language engineering tasks,
sourced from the comprehensive "你所不知道的 C 語言" (Things You Don't Know About C)
lecture series by sysprog.
It also fuses an external tutorial-based route map for practice, basics, and expertise progression.

## Quick Reference Index

| Topic | File | When to Use |
|-------|------|-------------|
| Bitwise Operations | `references/01-bitwise-operations.md` | Bit manipulation, flags, masks |
| Floating Point | `references/02-floating-point.md` | FP precision, IEEE 754, NaN/Inf |
| C Intro | `references/03-c-programming-intro.md` | Language overview |
| C Deep Dive | `references/04-c-deep-dive.md` | Advanced concepts |
| CRT | `references/05-c-runtime-library.md` | Runtime library internals |
| C Standards | `references/06-c-standards.md` | C99/C11/C17 differences |
| Stream I/O | `references/07-stream-io.md` | EOF handling, buffering |
| Undefined Behavior | `references/08-undefined-behavior.md` | UB detection and avoidance |
| Control Flow | `references/09-goto-control-flow.md` | goto, switch, coroutines |
| Server Framework | `references/10-server-framework.md` | Network programming patterns |
| Encoding/DS | `references/11-character-encoding-data-structures.md` | UTF-8, data structures |
| Memory Management | `references/12-memory-management-alignment.md` | malloc, alignment, cache |
| Compiler Principles | `references/13-compiler-principles.md` | Compiler internals |
| OOP in C | `references/14-oop-in-c.md` | Object-oriented patterns |
| Dynamic Linker | `references/15-dynamic-linker.md` | dlopen, dlsym, PLT/GOT |
| Tips & Tricks | `references/17-c-tips-and-tricks.md` | Idioms and techniques |
| Preprocessor | `references/18-preprocessor.md` | Macros, conditional compilation |
| Pointers | `references/19-pointers.md` | Pointer arithmetic, void* |
| Function Calling | `references/20-function-calling.md` | ABI, stack frame, calling conventions |
| Compiler Optimization | `references/21-compiler-optimization.md` | Optimization flags, techniques |
| Linker & ELF | `references/22-linker-elf.md` | Linking, ELF format |
| Linked Lists | `references/23-linked-list-memory.md` | List operations, memory |
| External C Route Map | `references/c-tutorial-route-map.md` | Learning progression and topic routing |
| External C Essence | `references/c-tutorial-essence.md` | Distilled actionable rules for answers |

## Fusion Strategy (sysprog + external tutorial)

Use both sources together:
- Use sysprog references for deep implementation-level detail.
- Use external route map for pedagogical sequencing and issue triage.
- Start from topic classification (`practice`, `basics`, `expertise`), then jump to the strongest sysprog reference.

Recommended response order:
1. Classify the user's request into topic bucket(s).
2. Give a compact conceptual explanation.
3. Provide a minimal compilable C example.
4. Add a risk checklist (UB, lifetime, conversion, side effects).
5. Point to one route-map topic and one sysprog reference for follow-up.

## External Topic Router

Routing references:
- `references/c-tutorial-route-map.md`
- `references/c-tutorial-essence.md`

When users ask these, prioritize external mapping first:
- Beginner mistakes, debugging process, asking for help, coding style, naming
- Function/types/I-O/type conversion
- Declaration vs definition, scope/lifetime, dynamic allocation
- C standard differences, UB/unspecified behavior, lvalue/rvalue
- Array vs pointer, memory layout, struct details, side effects in subexpressions

## Task Routing Guide

### Memory & Pointer Issues
- **Pointer bugs**: `references/19-pointers.md`
- **Memory management**: `references/12-memory-management-alignment.md`
- **Linked lists**: `references/23-linked-list-memory.md`

### Compilation & Toolchain
- **Compiler warnings/errors**: `references/13-compiler-principles.md`, `references/21-compiler-optimization.md`
- **Linker issues**: `references/22-linker-elf.md`, `references/15-dynamic-linker.md`
- **Preprocessor macros**: `references/18-preprocessor.md`

### Code Safety & UB
- **Undefined behavior**: `references/08-undefined-behavior.md`
- **Safety checklist**: Cross-reference `08-undefined-behavior.md` and `19-pointers.md`

### Performance & Optimization
- **Bitwise operations**: `references/01-bitwise-operations.md`
- **Compiler optimizations**: `references/21-compiler-optimization.md`
- **Memory alignment**: `references/12-memory-management-alignment.md`

### Control Flow & Design
- **goto/switch patterns**: `references/09-goto-control-flow.md`
- **OOP patterns in C**: `references/14-oop-in-c.md`
- **Function calling**: `references/20-function-calling.md`

### I/O & Encoding
- **Stream I/O**: `references/07-stream-io.md`
- **Character encoding**: `references/11-character-encoding-data-structures.md`

## C Programming Techniques

### Safe goto Patterns (from `09-goto-control-flow.md`)

Use goto for centralized error handling:

```c
int process_data() {
    void *buffer = NULL;
    FILE *fp = NULL;
    int status = -1;

    buffer = malloc(BUF_SIZE);
    if (!buffer) goto cleanup;

    fp = fopen("data.txt", "r");
    if (!fp) goto cleanup;

    // ... process data ...
    status = 0;

cleanup:
    if (fp) fclose(fp);
    free(buffer);
    return status;
}
```

### Duff's Device (Loop Unrolling)

```c
void copy(char *to, char *from, int count) {
    int n = (count + 7) / 8;
    switch (count % 8) {
        case 0: do { *to++ = *from++;
        case 7:      *to++ = *from++;
        case 6:      *to++ = *from++;
        case 5:      *to++ = *from++;
        case 4:      *to++ = *from++;
        case 3:      *to++ = *from++;
        case 2:      *to++ = *from++;
        case 1:      *to++ = *from++;
                } while (--n > 0);
    }
}
```

### Multi-line Macro Safety

Always wrap multi-line macros in `do { ... } while (0)`:

```c
#define SAFE_FREE(ptr) do { \
    free(ptr); \
    (ptr) = NULL; \
} while (0)
```

### Container_of Macro (OOP in C)

```c
#define container_of(ptr, type, member) ({ \
    const typeof(((type *)0)->member) *__mptr = (ptr); \
    (type *)((char *)__mptr - offsetof(type, member)); \
})
```

## Output Style Guidelines

When answering C programming questions:

1. **Explain assumptions** - State what you're assuming about the platform (32/64-bit, endianness)
2. **Distinguish spec vs implementation** - Clarify what's guaranteed by C standard vs compiler-specific
3. **Provide minimal examples** - Show concise, compilable code snippets
4. **Include risk notes** - Warn about UB, aliasing, alignment, and overflow
5. **Reference sources** - Point to specific reference files for deep dives

## Common Pitfalls

### Undefined Behavior to Avoid
- Signed integer overflow
- Null pointer dereference
- Array bounds violation
- Strict aliasing violations
- Uninitialized variable use

### Safe Practices
- Use `size_t` for sizes and indices
- Check malloc return values
- Prefer `const` correctness
- Initialize all variables
- Use static analysis tools

## Scripts (Optional)

The `scripts/` directory may contain helper scripts:

- `find-pattern.sh` - Search for C idioms across the references
- `extract-examples.sh` - Extract code examples from reference files

To use scripts:
```bash
cd /home/ares/yyskills/output/modern-c-dev
./scripts/find-pattern.sh "Duff's Device"
```
