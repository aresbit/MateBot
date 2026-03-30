---
name: c-skill
description: Composite C skill that chains modern-c-makefile, spclib, and modern-c-dev.
version: 1
---

meta =
  name =
    modern-c-makefile =
    spclib =
    modern-c-dev =
  version =
    1 =
  license =
    MIT =
title =
  Modern C Makefile + spclib - sp.h Programming Guide + modern-c-dev =
skill =
  name =
    modern-c-makefile =
    spclib =
    modern-c-dev =
  description =
    
    Create, analyze, or improve Makefiles for modern C/C++ projects using best practices from the gnaro project template. Use when working with C/C++ projects that need clean, maintainable build systems for creating new Makefiles, improving existing ones, understanding modern patterns, or setting up comprehensive build workflows with testing and code quality tools.


    This skill should be used when the user asks to "write C code with sp.h", "use spclib", "sp.h API", "single-header C library",
    "modern C programming", "sp_str_t usage", "sp_alloc memory", "SP_LOG formatting", "dynamic array in C", "hash table in C",
    "cross-platform C code", or when working with the sp.h single-header C standard library replacement.


    Claude-optimized modern C skill from sysprog c-prog notes.
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

    Trigger this skill whenever the user mentions C programming, memory issues,
    pointer bugs, compiler warnings, undefined behavior, or low-level system programming. =
  entry =
    SKILL.md =
  refs =
     =
      references/best_practices.md =
      references/gnaro_makefile.md =
      reference/*.spcl =
      include/sp.h =
      references/00-index-c-prog.md =
      references/01-bitwise-operations.md =
      references/02-floating-point.md =
      references/03-c-programming-intro.md =
      references/04-c-deep-dive.md =
      references/05-c-runtime-library.md =
      references/06-c-standards.md =
      references/07-stream-io.md =
      references/08-undefined-behavior.md =
      references/09-goto-control-flow.md =
      references/10-server-framework.md =
      references/11-character-encoding-data-structures.md =
      references/12-memory-management-alignment.md =
      references/13-compiler-principles.md =
      references/14-oop-in-c.md =
      references/15-dynamic-linker.md =
      references/17-c-tips-and-tricks.md =
      references/18-preprocessor.md =
      references/19-pointers.md =
      references/20-function-calling.md =
      references/21-compiler-optimization.md =
      references/22-linker-elf.md =
      references/23-linked-list-memory.md =
  extras =
     =
      assets/basic_makefile.template =
      assets/cross_platform_guide.md =
      assets/project_structure_example.md =
      references/example/cli/palette.c =
      references/example/cli/prompt.c =
      references/example/freestanding/embed.c =
      references/example/freestanding/jit.c =
      references/example/msvc.c =
      references/index.md =
      assets/ =
      evals/ =
      scripts/ =
content =
  overview =
    
    This skill provides guidance and templates for creating clean, maintainable Makefiles for modern C/C++ projects, based on the best practices demonstrated in the [gnaro project](https://github.com/lucavallin/gnaro). It helps structure build systems that integrate compilation, testing, linting, formatting, and dependency management in a clear and organized way. =
  core_concepts =
    Understand these key Makefile concepts before implementing:
    concepts =
       =
        Variables: Centralize project settings like compiler flags, directories, and tool paths =
        Wildcards: Use patterns like `*.c` and `**/*.c` to automatically find source files =
        Automatic Variables: Leverage `$@` (target), `$<` (first dependency), `$*` (stem), `$(@D)` (target directory) =
        Phony Targets: Declare `.PHONY` targets for actions like `clean`, `format`, `lint` that don't produce files =
        Conditionals: Use `ifeq`/`else`/`endif` for debug/release builds or platform-specific configurations =
        Pattern Rules: Create generic rules for compiling `.c` to `.o` files =
  makefile_template =
    The complete gnaro Makefile template is available in [references/gnaro_makefile.md](references/gnaro_makefile.md). Key sections include:
    sections =
      project_structure_variables =
        Project Structure Variables
        code_block =
          debug ? =
            0 =
          NAME : =
            your-project =
          SRC_DIR : =
            src =
          BUILD_DIR : =
            build =
          INCLUDE_DIR : =
            include =
          LIB_DIR : =
            lib =
          TESTS_DIR : =
            tests =
          BIN_DIR : =
            bin =
      automatic_object_file_generation =
        Automatic Object File Generation
        code_block =
          OBJS : =
            $(patsubst %.c,%.o, $(wildcard $(SRC_DIR)/*.c) $(wildcard $(LIB_DIR)/**/*.c)) =
      compiler_and_tool_configuration =
        Compiler and Tool Configuration
        code_block =
          CC : =
            clang =
          LINTER : =
            clang-tidy =
          FORMATTER : =
            clang-format =
          CFLAGS : =
            -std =
              gnu17 -D _GNU_SOURCE -D __STDC_WANT_LIB_EXT1__ -Wall -Wextra -pedantic =
          LDFLAGS : =
            -lm =
      core_targets =
        Core Targets
        targets =
           =
            `$(NAME)`: Build executable with dependencies on format, lint, and object files =
            `$(OBJS)`: Pattern rule for compiling object files with directory creation =
            `test`: Compile and run CUnit tests =
            `lint`: Run static analysis with clang-tidy =
            `format`: Apply code formatting with clang-format =
            `check`: Run valgrind memory checks =
            `setup`: Install development dependencies (Debian/Ubuntu) =
            `clean`: Remove build artifacts =
            `bear`: Generate compile_commands.json for tooling =
  customization_guide =
    Adapting to Your Project
    steps =
       =
        Basic Configuration:
        Update `NAME` to your project name
        Adjust directory variables to match your project structure
        Modify `CFLAGS` for your C standard and feature requirements =
        Compiler and Tools:
        Change `CC`, `LINTER`, `FORMATTER` to match your installed versions
        For GCC projects: `CC : =
          gcc`
        Adjust tool paths for non-Debian systems =
        Cross-Platform Considerations:
        Replace apt-based `setup` target with appropriate package manager commands
        Use conditionals for platform-specific configurations:
        code_block =
          
          ifeq ($(OS),Windows_NT)
              # Windows-specific settings
          else ifeq ($(shell uname -s),Darwin)
              # macOS-specific settings  
          else
              # Linux-specific settings
          endif =
        Adding Features:
        Documentation: Add `docs` target for Doxygen or other documentation generators
        Packaging: Add `package` target for creating distributable archives
        Installation: Add `install` and `uninstall` targets for system installation =
    common_modifications =
      Multiple Executables:
      code_block =
        
        EXECUTABLES := app1 app2
        all: $(EXECUTABLES)

        app1: $(APP1_OBJS)
        	$(CC) $(CFLAGS) -o $(BIN_DIR)/$@ $^ $(LDFLAGS)

        app2: $(APP2_OBJS)
        	$(CC) $(CFLAGS) -o $(BIN_DIR)/$@ $^ $(LDFLAGS) =
      Header Dependency Generation:
      code_block =
        
        DEPFILES := $(OBJS:.o=.d)
        -include $(DEPFILES)

        %.d: %.c
        	@$(CC) $(CFLAGS) -MM -MP -MT $*.o -MF $@ $< =
      Verbose Mode:
      code_block =
        
        V ?= 0
        ifeq ($(V),1)
            Q :=
        else
            Q := @
        endif

        $(OBJS): dir
        	$(Q)mkdir -p $(BUILD_DIR)/$(@D)
        	$(Q)$(CC) $(CFLAGS) -o $(BUILD_DIR)/$@ -c $*.c =
  usage_examples =
    Example 1: Creating a New Makefile
    description =
      
      User: Create a Makefile for my C project "calculator" with source files in src/, headers in include/, tests in tests/
      Assistant: Creates Makefile based on template with customized variables =
    Example 2: Adding Testing to Existing Makefile
    description =
      
      User: Add CUnit testing support to my existing Makefile
      Assistant: Adds test target and updates dependencies =
    Example 3: Improving Build Performance
    description =
      
      User: My Makefile rebuilds everything when headers change
      Assistant: Adds automatic dependency generation with -MM flags =
    Example 4: Cross-Platform Support
    description =
      
      User: Make my Makefile work on both Linux and macOS
      Assistant: Adds OS detection and conditional tool paths =
  quick_reference =
    Essential Commands
    commands =
      code_block =
        
        make              # Build project (default target)
        make debug=1      # Build with debug symbols, no optimization
        make test         # Run tests
        make lint         # Run static analysis
        make format       # Format code
        make check        # Run memory checks
        make clean        # Clean build artifacts =
    Project Structure Convention
    structure =
      code_block =
        
        project/
        ├── Makefile
        ├── src/          # Source files (*.c)
        ├── include/      # Header files (*.h)
        ├── lib/          # Third-party libraries
        ├── tests/        # Test files
        ├── build/        # Object files (generated)
        └── bin/          # Executables (generated) =
    title =
      Quick Reference =
    setup =
      title =
        Setup =
      code =
        
        // In ONE C file only:
        #define SP_IMPLEMENTATION
        #include "sp.h" =
    types =
      title =
        Types =
      items =
         =
          s8/s16/s32/s64 - signed integers =
          u8/u16/u32/u64 - unsigned integers =
          f32/f64 - floats =
          c8 - char (UTF-8) =
          sp_str_t - {data, len} string (no null terminator) =
    string_operations =
      title =
        String Operations =
      code =
        sp_str_t s =
          sp_str_lit("hello");     // Compile-time literal =
        sp_str_t v =
          sp_str_view(cstr);       // View from C string =
        bool eq =
          sp_str_equal(a, b);         // Compare =
        bool empty =
          sp_str_empty(s);         // Check empty =
    dynamic_arrays =
      title =
        Dynamic Arrays =
      code =
        
        sp_dyn_array(int) arr = SP_NULLPTR;
        sp_dyn_array_push(arr, 42);
        sp_dyn_array_for(arr, i) { /* use arr[i] */ } =
    directory_iteration =
      title =
        Directory Iteration =
      simple =
        title =
          Simple directory traversal =
        code =
          
          sp_fs_for(dir, it) {
            SP_LOG("Entry: {}", SP_FMT_STR(it.entry.name));
          } =
      recursive =
        title =
          Recursive directory traversal =
        code =
          
          sp_fs_for_recursive(dir, it) {
            SP_LOG("Path: {}", SP_FMT_STR(it.entry.path));
          } =
    hash_tables =
      title =
        Hash Tables =
      code =
        sp_ht(sp_str_t, s32) map =
          SP_NULLPTR; =
        sp_ht_set_fns(map, sp_ht_hash_str, sp_ht_compare_str);
        sp_ht_insert(map, sp_str_lit("key"), 100);
        s32* val =
          sp_ht_getp(map, sp_str_lit("key")); =
    logging =
      title =
        Logging =
      code =
        
        SP_LOG("Value: {}", SP_FMT_S32(x));
        SP_LOG("{:fg green}Success{:reset}", SP_FMT_CSTR("")) =
  resources =
    This skill includes the following bundled resources:
    references =
      Reference documentation for Makefile best practices and templates:
      files =
         =
          [gnaro_makefile.md](references/gnaro_makefile.md): Complete Makefile from the gnaro project with detailed analysis and adaptation notes. Use this as the primary reference template. =
          [best_practices.md](references/best_practices.md): Comprehensive guide to modern C Makefile design patterns, advanced techniques, and common solutions. =
      when_to_load =
        
        Read these files when you need detailed analysis of Makefile patterns, adaptation guidance, or advanced techniques beyond what's covered in the main skill. =
    assets =
      Template files and guides for project setup:
      files =
         =
          [basic_makefile.template](assets/basic_makefile.template): Simplified Makefile template ready for customization. Replace `PROJECT_NAME` and adjust directories as needed. =
          [project_structure_example.md](assets/project_structure_example.md): Recommended project structure with variations for different project types (single-header libraries, applications with resources, multi-target projects). =
          [cross_platform_guide.md](assets/cross_platform_guide.md): Guide for adapting Makefiles to different operating systems (Linux, macOS, Windows) with platform detection, package manager integration, and cross-compilation support. =
      when_to_use =
        
        These files provide starting points and templates that can be copied and adapted for specific projects. They're particularly useful when creating new projects or porting existing ones to different platforms. =
    scripts =
      This skill doesn't include scripts since Makefile creation is primarily about configuration and structure rather than automated processing. However, consider creating custom scripts for:
      suggestions =
         =
          Project scaffolding (generating directory structure) =
          Dependency management =
          Build automation beyond Makefile capabilities =
  core_principles =
    title =
      Core Principles =
    text =
      
      **Always follow these rules when using sp.h:** =
    rules =
       =
        never_use =
          malloc/calloc/realloc =
          const char* =
          strcmp/strlen =
          printf =
          memset(&obj, 0, sizeof(obj)) =
          for(i =
            0; i<n; i++) on arrays =
        use_instead =
          sp_alloc() =
          sp_str_t (ptr+len string) =
          sp_str_equal() / sp_str_len() =
          SP_LOG() =
          SP_ZERO_INITIALIZE() =
          sp_dyn_array_for() / sp_carr_for() =
  module_namespaces =
    title =
      Module Namespaces =
    text =
      
      Search `references/index.md` for detailed API signatures: =
    table =
       =
        namespace =
          sp_str_* =
          sp_cstr_* =
          sp_dyn_array_* / sp_da =
          sp_ht_* =
          sp_alloc / sp_free =
          sp_io_* =
          sp_fs_* =
          sp_ps_* =
          sp_tm_* =
          sp_thread_* =
          sp_mutex_* =
          sp_env_* =
          sp_os_* =
          SP_LOG / SP_FMT_* =
        purpose =
          String operations =
          C string operations =
          Dynamic arrays =
          Hash tables =
          Memory allocation =
          File IO =
          Filesystem =
          Processes =
          Time =
          Threads =
          Mutexes =
          Environment =
          Platform =
          Logging =
        key_functions =
          sp_str_lit, sp_str_equal, sp_str_empty =
          sp_cstr_len, sp_cstr_equal =
          sp_dyn_array_push, sp_dyn_array_for =
          sp_ht_insert, sp_ht_getp, sp_ht_for =
          sp_alloc, sp_realloc, sp_free =
          sp_io_read_file, sp_io_write_file =
          sp_fs_exists, sp_fs_read, sp_fs_write, sp_fs_for, sp_fs_for_recursive =
          sp_ps_run, sp_ps_spawn =
          sp_tm_now_ns, sp_tm_sleep_ms =
          sp_thread_create, sp_thread_join =
          sp_mutex_init, sp_mutex_lock =
          sp_env_get, sp_env_set =
          sp_os_get_executable_ext =
          SP_LOG, SP_FMT_STR, SP_FMT_S32 =
  common_patterns =
    title =
      Common Patterns =
    zero_initialization =
      title =
        Zero Initialization =
      code =
        my_struct_t obj =
          SP_ZERO_INITIALIZE(); =
    error_handling =
      title =
        Error Handling =
      code =
        
        sp_try(expr);                    // Return if expr fails
        sp_try_goto(expr);               // goto sp_try_label if expr fails
        sp_try_as_goto(expr, label);     // goto label if expr fails
        sp_require(ptr != NULL);         // Return if condition false
        SP_ASSERT(condition);            // Assert
        SP_FATAL("msg {}", SP_FMT(...)); // Log and exit =
    switch_statements =
      title =
        Switch Statements =
      code =
        
        switch (val) {
          case A: { break; }
          case B: { break; }
          default: { SP_UNREACHABLE_CASE(); }
        } =
  reference_files =
    title =
      Reference Files =
    text =
      
      For complete API documentation with full function signatures: =
    items =
       =
        file =
          references/index.md =
        description =
          Comprehensive API reference with all function signatures, types, and macros =
  examples =
    title =
      Examples =
    text =
      
      Example code demonstrating sp.h usage: =
    table =
       =
        file =
          references/example/msvc.c =
          references/example/cli/palette.c =
          references/example/cli/prompt.c =
          references/example/freestanding/jit.c =
          references/example/freestanding/embed.c =
        description =
          MSVC compiler specific examples =
          Terminal color palette demo =
          Interactive CLI prompt example =
          Just-in-time compilation example =
          Embedded usage example =
  finding_apis =
    title =
      Finding APIs =
    text =
      
      When looking for a specific function: =
    steps =
       =
        Check the namespace table above =
        Search `references/index.md` for the pattern =
        All public APIs are prefixed with `SP_API` in the source =
resolve =
  merge =
    deep =
  conflict =
    right-bias =
  fixpoint =
    true =
  max_iter =
    64 =
purpose =
  
  This skill provides practical guidance for modern C language engineering tasks,
  sourced from the comprehensive "你所不知道的 C 語言" (Things You Don't Know About C)
  lecture series by sysprog. =
quick_reference_index =
  topic =
    name =
      Bitwise Operations =
      Floating Point =
      C Intro =
      C Deep Dive =
      CRT =
      C Standards =
      Stream I/O =
      Undefined Behavior =
      Control Flow =
      Server Framework =
      Encoding/DS =
      Memory Management =
      Compiler Principles =
      OOP in C =
      Dynamic Linker =
      Tips & Tricks =
      Preprocessor =
      Pointers =
      Function Calling =
      Compiler Optimization =
      Linker & ELF =
      Linked Lists =
    file =
      references/01-bitwise-operations.md =
      references/02-floating-point.md =
      references/03-c-programming-intro.md =
      references/04-c-deep-dive.md =
      references/05-c-runtime-library.md =
      references/06-c-standards.md =
      references/07-stream-io.md =
      references/08-undefined-behavior.md =
      references/09-goto-control-flow.md =
      references/10-server-framework.md =
      references/11-character-encoding-data-structures.md =
      references/12-memory-management-alignment.md =
      references/13-compiler-principles.md =
      references/14-oop-in-c.md =
      references/15-dynamic-linker.md =
      references/17-c-tips-and-tricks.md =
      references/18-preprocessor.md =
      references/19-pointers.md =
      references/20-function-calling.md =
      references/21-compiler-optimization.md =
      references/22-linker-elf.md =
      references/23-linked-list-memory.md =
    when_to_use =
      Bit manipulation, flags, masks =
      FP precision, IEEE 754, NaN/Inf =
      Language overview =
      Advanced concepts =
      Runtime library internals =
      C99/C11/C17 differences =
      EOF handling, buffering =
      UB detection and avoidance =
      goto, switch, coroutines =
      Network programming patterns =
      UTF-8, data structures =
      malloc, alignment, cache =
      Compiler internals =
      Object-oriented patterns =
      dlopen, dlsym, PLT/GOT =
      Idioms and techniques =
      Macros, conditional compilation =
      Pointer arithmetic, void* =
      ABI, stack frame, calling conventions =
      Optimization flags, techniques =
      Linking, ELF format =
      List operations, memory =
task_routing_guide =
  memory_and_pointer_issues =
    pointer_bugs =
      references/19-pointers.md =
    memory_management =
      references/12-memory-management-alignment.md =
    linked_lists =
      references/23-linked-list-memory.md =
  compilation_and_toolchain =
    compiler_warnings_errors =
       =
        references/13-compiler-principles.md =
        references/21-compiler-optimization.md =
    linker_issues =
       =
        references/22-linker-elf.md =
        references/15-dynamic-linker.md =
    preprocessor_macros =
      references/18-preprocessor.md =
  code_safety_and_ub =
    undefined_behavior =
      references/08-undefined-behavior.md =
    safety_checklist =
      Cross-reference 08-undefined-behavior.md and 19-pointers.md =
  performance_and_optimization =
    bitwise_operations =
      references/01-bitwise-operations.md =
    compiler_optimizations =
      references/21-compiler-optimization.md =
    memory_alignment =
      references/12-memory-management-alignment.md =
  control_flow_and_design =
    goto_switch_patterns =
      references/09-goto-control-flow.md =
    oop_patterns_in_c =
      references/14-oop-in-c.md =
    function_calling =
      references/20-function-calling.md =
  io_and_encoding =
    stream_io =
      references/07-stream-io.md =
    character_encoding =
      references/11-character-encoding-data-structures.md =
c_programming_techniques =
  safe_goto_patterns =
    description =
      Use goto for centralized error handling (from 09-goto-control-flow.md) =
    example =
      
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
      } =
  duffs_device =
    description =
      Loop Unrolling =
    example =
      
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
      } =
  multi_line_macro_safety =
    description =
      Always wrap multi-line macros in `do { ... } while (0)` =
    example =
      
      #define SAFE_FREE(ptr) do { \
          free(ptr); \
          (ptr) = NULL; \
      } while (0) =
  container_of_macro =
    description =
      OOP in C =
    example =
      
      #define container_of(ptr, type, member) ({ \
          const typeof(((type *)0)->member) *__mptr = (ptr); \
          (type *)((char *)__mptr - offsetof(type, member)); \
      }) =
output_style_guidelines =
  
  When answering C programming questions:
  1. Explain assumptions - State what you're assuming about the platform (32/64-bit, endianness)
  2. Distinguish spec vs implementation - Clarify what's guaranteed by C standard vs compiler-specific
  3. Provide minimal examples - Show concise, compilable code snippets
  4. Include risk notes - Warn about UB, aliasing, alignment, and overflow
  5. Reference sources - Point to specific reference files for deep dives =
common_pitfalls =
  undefined_behavior_to_avoid =
     =
      Signed integer overflow =
      Null pointer dereference =
      Array bounds violation =
      Strict aliasing violations =
      Uninitialized variable use =
  safe_practices =
     =
      Use `size_t` for sizes and indices =
      Check malloc return values =
      Prefer `const` correctness =
      Initialize all variables =
      Use static analysis tools =
scripts =
  description =
    The `scripts/` directory may contain helper scripts =
  scripts =
    find_pattern_sh =
      Search for C idioms across the references =
    extract_examples_sh =
      Extract code examples from reference files =
  usage_example =
    
    To use scripts:
    ```bash
    cd /home/ares/yyskills/output/modern-c-dev
    ./scripts/find-pattern.sh "Duff's Device"
    ``` =
