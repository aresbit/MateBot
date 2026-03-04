# Binary Patch Makefile Template

# Configuration
TARGET_PATCH = patch.bin
PATCH_ADDR = 0x1139

# Tools
CC = gcc
LD = ld
CFLAGS = -c -fno-pic -fno-pie -nostdlib -Wall
LDFLAGS = -nostdlib --oformat binary

# Source files
SRC = binpatch.c
OBJ = $(SRC:.c=.o)
SCRIPT = binpatch.ld

.PHONY: all clean apply

all: $(TARGET_PATCH)

$(OBJ): $(SRC)
	$(CC) $(CFLAGS) $< -o $@

$(TARGET_PATCH): $(OBJ) $(SCRIPT)
	$(LD) -T $(SCRIPT) $< -o $@ $(LDFLAGS)
	@echo "Patch size: $$(stat -f%z $@ 2>/dev/null || stat -c%s $@) bytes"

# Apply patch to target binary (customize TARGET_BIN)
apply: $(TARGET_PATCH)
	@test -n "$(TARGET_BIN)" || (echo "Usage: make apply TARGET_BIN=<binary>" && exit 1)
	dd if=$(TARGET_PATCH) of=$(TARGET_BIN) bs=1 seek=$$(($(PATCH_ADDR))) conv=notrunc
	@echo "Patch applied to $(TARGET_BIN)"

clean:
	rm -f $(OBJ) $(TARGET_PATCH)

# Analyze patch contents
analyze: $(TARGET_PATCH)
	@objdump -b binary -m i386:x86-64 -D $(TARGET_PATCH)
