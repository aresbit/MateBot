/* Binary Patch Linker Script Template
 *
 * Customize:
 * - patch_at: Address where patch should be placed
 * - patch_size: Maximum size available
 * - External symbols (puts, etc.) at their PLT/GOT addresses
 */

/* Configuration - MODIFY THESE */
patch_at = 0x1139;       /* Target address in binary */
patch_size = 511;        /* Available space in bytes */

/* External symbols - Set to actual addresses in target binary */
puts = 0x1030;           /* Example: PLT entry for puts */
/* scanf = 0x1040; */   /* Add more as needed */

SECTIONS {
    . = patch_at;

    .patch ALIGN(1) : SUBALIGN(1) {
        /* Code sections first */
        KEEP(*(.patch.code.*))
        KEEP(*(.patch.code))

        /* Data sections follow */
        KEEP(*(.patch.data.*))
        KEEP(*(.patch.data))

        /* BSS/uninitialized if needed */
        KEEP(*(.patch.bss.*))
    }

    /* Ensure patch fits in allocated space */
    ASSERT(SIZEOF(.patch) <= patch_size,
           "Patch size exceeds available space!")

    /* Optional: Warn if patch is large */
    ASSERT(SIZEOF(.patch) <= (patch_size * 0.9),
           "Warning: Patch using >90% of available space")
}
