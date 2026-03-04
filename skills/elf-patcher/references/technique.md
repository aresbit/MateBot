# ELF Patching with C - Technical Reference

## Core Concept

This technique leverages GNU Linker (`ld`) features to patch binaries using C code instead of raw assembly:

1. **Symbol Address Definition** - Define symbols at specific memory addresses in linkerscript
2. **Section Placement** - Force sections to specific virtual addresses using location counter

## Linker Script Features

### Symbol Definition
```ld
/* Define a symbol at address 0x42069 */
my_puts = 0x42069;
```

Reference in C:
```c
extern void (*my_puts)(char *);
```

### Section Placement
```ld
SECTIONS {
    . = 0xdeadbeefcafebabe;  /* Set location counter */
    .patch ALIGN(1) : SUBALIGN(1) {  /* No alignment padding */
        KEEP(*(.patch))
    }
}
```

## GCC Attributes

### Section Attribute
```c
#define SECTION(x) __attribute__((section(x)))

SECTION(".patch")
int foo(void) { return 42; }
```

## Practical Example Structure

### Patch Code (binpatch.c)
```c
#define SECTION(x) __attribute__((section(x)))

SECTION(".patch.data.string1")
const char hello_binary_patching[] = "Hello, binary patching!";

SECTION(".patch.code.i_do_something")
void i_do_something() {
    puts(hello_binary_patching);
}
```

### Linker Script (binpatch.ld)
```ld
patch_at = 0x01139;      /* Target address in binary */
patch_size = 511;        /* Available space */
puts = 0x1030;           /* PLT entry address */

SECTIONS {
    . = patch_at;
    .patch ALIGN(1) : SUBALIGN(1) {
        KEEP(*(.patch.code.*))
        KEEP(*(.patch.data.*))
    }
    ASSERT(SIZEOF(.patch) <= patch_size, "patch is too big")
}
```

### Compilation & Application
```bash
# Compile patch
gcc -c binpatch.c -o binpatch.o -fno-pic -fno-pie -nostdlib

# Link with custom script
ld -T binpatch.ld binpatch.o -o patch.bin -nostdlib --oformat binary

# Apply to target
dd if=patch.bin of=target_binary bs=1 seek=$((0x1139)) conv=notrunc
```

## Important Considerations

### PIE Binaries
- Require compiler flags to emit `rel32` instead of absolute `call`/`jmp`
- Use `-fno-pic -fno-pie` for non-PIE code

### Size Constraints
- Linker script `ASSERT` validates patch fits in code cave
- Large patches may require direct assembly

### ABI Mismatches
- May need assembly stubs for calling convention adaptation
- Be careful with register preservation

## Platform Extensions

This technique can extend to:
- **Other languages**: Rust, Zig, Nim for patch generation
- **Cross-platform**: Platform-specific only in linker script
- **Other formats**: PE (Windows), Mach-O (macOS)
- **Dynamic resolution**: Embedded `dlsym` or `GetProcAddress` resolvers
