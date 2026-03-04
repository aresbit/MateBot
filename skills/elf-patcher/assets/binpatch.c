/* Binary Patch Template
 *
 * Compile: gcc -c binpatch.c -o binpatch.o -fno-pic -fno-pie -nostdlib
 * Link:    ld -T binpatch.ld binpatch.o -o patch.bin -nostdlib --oformat binary
 */

#define SECTION(x) __attribute__((section(x)))

/* Declare external functions at their addresses (defined in linkerscript) */
extern int puts(const char *s);

/* Data section - strings and constants */
SECTION(".patch.data.message")
const char patch_message[] = "Hello from the patch!";

/* Code section - patch implementation */
SECTION(".patch.code.entry")
void patch_entry(void) {
    puts(patch_message);
    /* Add your patch logic here */
}

/* Additional data sections */
SECTION(".patch.data.buffer")
char patch_buffer[256];

/* Additional code sections */
SECTION(".patch.code.helper")
int helper_function(int x) {
    return x * 42;
}
