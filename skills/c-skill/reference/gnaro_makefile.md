# Gnaro Project Makefile Reference

This is the complete Makefile from the [gnaro project](https://github.com/lucavallin/gnaro), which serves as a template for modern C project build systems.

## Complete Makefile

```makefile
# Project Settings
debug ?= 0
NAME := gnaro
SRC_DIR := src
BUILD_DIR := build
INCLUDE_DIR := include
LIB_DIR := lib
TESTS_DIR := tests
BIN_DIR := bin

# Generate paths for all object files
OBJS := $(patsubst %.c,%.o, $(wildcard $(SRC_DIR)/*.c) $(wildcard $(LIB_DIR)/**/*.c))

# Compiler settings
CC := clang-18
LINTER := clang-tidy-18
FORMATTER := clang-format-18

# Compiler and Linker flags Settings:
# 	-std=gnu17: Use the GNU17 standard
# 	-D _GNU_SOURCE: Use GNU extensions
# 	-D __STDC_WANT_LIB_EXT1__: Use C11 extensions
# 	-Wall: Enable all warnings
# 	-Wextra: Enable extra warnings
# 	-pedantic: Enable pedantic warnings
# 	-lm: Link to libm
CFLAGS := -std=gnu17 -D _GNU_SOURCE -D __STDC_WANT_LIB_EXT1__ -Wall -Wextra -pedantic
LDFLAGS := -lm

ifeq ($(debug), 1)
	CFLAGS := $(CFLAGS) -g -O0
else
	CFLAGS := $(CFLAGS) -Oz
endif

# Targets

# Build executable
$(NAME): format lint dir $(OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(BIN_DIR)/$@ $(patsubst %, build/%, $(OBJS))

# Build object files and third-party libraries
$(OBJS): dir
	@mkdir -p $(BUILD_DIR)/$(@D)
	@$(CC) $(CFLAGS) -o $(BUILD_DIR)/$@ -c $*.c

# Run CUnit tests
test: dir
	@$(CC) $(CFLAGS) -lcunit -o $(BIN_DIR)/$(NAME)_test $(TESTS_DIR)/*.c
	@$(BIN_DIR)/$(NAME)_test

# Run linter on source directories
lint:
	@$(LINTER) --config-file=.clang-tidy $(SRC_DIR)/* $(INCLUDE_DIR)/* $(TESTS_DIR)/* -- $(CFLAGS)

# Run formatter on source directories
format:
	@$(FORMATTER) -style=file -i $(SRC_DIR)/* $(INCLUDE_DIR)/* $(TESTS_DIR)/*

# Run valgrind memory checker on executable
check: $(NAME)
	@sudo valgrind -s --leak-check=full --show-leak-kinds=all $(BIN_DIR)/$< --help
	@sudo valgrind -s --leak-check=full --show-leak-kinds=all $(BIN_DIR)/$< --version
	@sudo valgrind -s --leak-check=full --show-leak-kinds=all $(BIN_DIR)/$< -v

# Setup dependencies for build and development
setup:
	# Update apt and upgrade packages
	@sudo apt update
	@sudo DEBIAN_FRONTEND=noninteractive apt upgrade -y

	# Install OS dependencies
	@sudo apt install -y bash libarchive-tools lsb-release wget software-properties-common gnupg

	# Install LLVM tools required for building the project
	@wget https://apt.llvm.org/llvm.sh
	@chmod +x llvm.sh
	@sudo ./llvm.sh 18
	@rm llvm.sh

	# Install Clang development tools
	@sudo apt install -y clang-tools-18 clang-format-18 clang-tidy-18 valgrind bear

	# Install CUnit testing framework
	@sudo apt install -y libcunit1 libcunit1-doc libcunit1-dev

	# Cleanup
	@sudo apt autoremove -y

# Setup build and bin directories
dir:
	@mkdir -p $(BUILD_DIR) $(BIN_DIR)

# Clean build and bin directories
clean:
	@rm -rf $(BUILD_DIR) $(BIN_DIR)

# Run bear to generate compile_commands.json
bear:
	bear --exclude $(LIB_DIR) make $(NAME)

.PHONY: lint format check setup dir clean bear
```

## Key Features and Design Patterns

### 1. Organized Variable Structure
- **Project settings**: Centralized configuration at the top
- **Directory variables**: Clear separation of source, build, test directories
- **Tool variables**: Explicit compiler and tool declarations

### 2. Automatic File Discovery
- Uses `wildcard` and `patsubst` to automatically find all `.c` files
- Supports nested directories with `**/*.c` pattern
- Eliminates manual file listing maintenance

### 3. Comprehensive Development Workflow
- **Build**: `make` or `make debug=1`
- **Testing**: `make test` with CUnit integration
- **Code quality**: `make lint` (clang-tidy) and `make format` (clang-format)
- **Memory checking**: `make check` with valgrind
- **Dependency setup**: `make setup` for development environment

### 4. Conditional Build Configurations
- Debug vs release builds controlled by `debug` variable
- Different optimization levels (-O0 vs -Oz)
- Easy to extend for other configurations (platform-specific, feature flags)

### 5. Clean Project Structure
- Generated files go to `build/` and `bin/` directories
- Source separation maintained in build output
- Easy cleanup with `make clean`

## Adaptation Notes

### For Different Compilers
```makefile
# For GCC
CC := gcc
LINTER := clang-tidy  # or use cppcheck, splint
FORMATTER := clang-format

# For different Clang versions
CC := clang
LINTER := clang-tidy
FORMATTER := clang-format
```

### For Cross-Platform Compatibility
The current `setup` target is Debian/Ubuntu specific. Consider:
- Platform detection with conditionals
- Alternative package managers (brew, yum, pacman)
- Containerized development environments

### For Different Test Frameworks
Replace CUnit with other frameworks:
```makefile
# For Check framework
test: dir
	@$(CC) $(CFLAGS) `pkg-config --cflags --libs check` -o $(BIN_DIR)/$(NAME)_test $(TESTS_DIR)/*.c
	@$(BIN_DIR)/$(NAME)_test

# For Google Test
LDFLAGS := -lm -lgtest -lgtest_main -lpthread
```

## Limitations and Considerations

1. **System Dependencies**: Setup target assumes Debian/Ubuntu with apt
2. **Tool Version Lock**: Specific to clang-18 toolchain
3. **Build Directory Assumption**: Assumes build directory mirrors source structure
4. **Header Dependencies**: Doesn't automatically track header file changes

Despite these limitations, this Makefile provides an excellent foundation that can be adapted to most C/C++ projects.