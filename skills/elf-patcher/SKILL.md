---
name: elf-patcher
description: Patch ELF binaries using C code and linker script magic. Use when modifying Linux binaries by injecting compiled C code into code caves or specific addresses. Alternative to assembly patching for binary modification, reverse engineering payloads, or binary instrumentation tasks. Supports defining symbols at addresses, placing sections at offsets, and cross-platform patch generation.
---

# ELF Patcher with C

Patch ELF binaries using C code and GNU linker features instead of raw assembly.

## Quick Start

1. Copy templates from `assets/` directory
2. Customize `patch_at`, `patch_size`, and external symbols in linkerscript
3. Write patch logic in C using `SECTION(".patch.code.*")` attribute
4. Compile: `gcc -c binpatch.c -o binpatch.o -fno-pic -fno-pie -nostdlib`
5. Link: `ld -T binpatch.ld binpatch.o -o patch.bin -nostdlib --oformat binary`
6. Apply: `dd if=patch.bin of=target bs=1 seek=0xADDR conv=notrunc`

## Core Technique

This method leverages two GNU Linker features:

### 1. Symbol Definition
Define symbols at specific addresses in linkerscript:
```ld
my_puts = 0x42069;
```

Reference in C:
```c
extern void (*my_puts)(char *);
```

### 2. Section Placement
Force sections to specific virtual addresses:
```ld
SECTIONS {
    . = 0xdeadbeefcafebabe;  /* Location counter */
    .patch ALIGN(1) : SUBALIGN(1) {  /* No alignment */
        KEEP(*(.patch))
    }
}
```

## C Code Pattern

```c
#define SECTION(x) __attribute__((section(x)))

SECTION(".patch.data.message")
const char msg[] = "Hello from patch!";

SECTION(".patch.code.entry")
void patch_entry() {
    puts(msg);  /* 'puts' defined in linkerscript */
}
```

## Linker Script Pattern

```ld
patch_at = 0x01139;      /* Target address */
patch_size = 511;        /* Available bytes */
puts = 0x1030;           /* PLT entry */

SECTIONS {
    . = patch_at;
    .patch ALIGN(1) : SUBALIGN(1) {
        KEEP(*(.patch.code.*))
        KEEP(*(.patch.data.*))
    }
    ASSERT(SIZEOF(.patch) <= patch_size, "patch too big")
}
```

## Resources

### scripts/
- `apply_patch.py` - Python script to apply binary patch to target file

### references/
- `technique.md` - Detailed technical documentation and considerations

### assets/
- `binpatch.c` - Template for patch C code
- `binpatch.ld` - Template for linker script
- `Makefile` - Build automation template

## Important Considerations

- **PIE binaries**: Use `-fno-pic -fno-pie` flags for non-PIE code
- **Size limits**: `ASSERT` in linkerscript validates patch fits
- **ABI matching**: May need assembly stubs for calling conventions
- **External symbols**: Set to actual PLT/GOT addresses from target binary

## Extensions

This technique enables:
- Other languages (Rust, Zig, Nim) for patch generation
- Cross-platform patches (platform-specific only in linker script)
- PE/Mach-O compatibility
- Embedded dynamic symbol resolvers

Read `references/technique.md` for full technical details.
