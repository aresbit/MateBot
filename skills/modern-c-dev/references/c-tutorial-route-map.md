# External C Tutorial Route Map

Use this file as a routing layer. First pick the closest topic, then pair it
with one or more deep-dive sysprog references from this skill.

## Practice

1. Introduction
- Use when: user asks for learning path or course entry point.
- Pair with: `03-c-programming-intro.md`, `06-c-standards.md`

2. Summary Of Common Mistakes For Beginners
- Use when: repeated beginner bugs, confusion about basic semantics.
- Pair with: `08-undefined-behavior.md`, `19-pointers.md`, `07-stream-io.md`

3. Summary Of Basic Debugging Skills
- Use when: locating bugs, isolating root causes, reproducing failures.
- Pair with: `13-compiler-principles.md`, `21-compiler-optimization.md`

4. The Right Way To Ask Others For Help
- Use when: issue templates, repro reports, collaboration.
- Pair with: `17-c-tips-and-tricks.md`

5. Convention Of Naming Identifier
- Use when: API naming, variable naming, consistency.
- Pair with: `17-c-tips-and-tricks.md`

## Basics

6. Function
- Use when: function signatures, parameters, call behavior, contracts.
- Pair with: `20-function-calling.md`

7. Types
- Use when: integer/floating type choice, signedness, aliasing concerns.
- Pair with: `02-floating-point.md`, `06-c-standards.md`, `08-undefined-behavior.md`

8. Input And Output
- Use when: stdin/stdout/stderr, EOF, buffering, `scanf`/`fgets` usage.
- Pair with: `07-stream-io.md`, `05-c-runtime-library.md`

9. Type Conversion
- Use when: implicit cast bugs, truncation, promotion rules.
- Pair with: `06-c-standards.md`, `08-undefined-behavior.md`, `02-floating-point.md`

10. Declaration And Definition
- Use when: `extern`, multiple definition, header/source boundaries.
- Pair with: `22-linker-elf.md`, `13-compiler-principles.md`

11. Scope And Lifetime
- Use when: storage duration, visibility, dangling references.
- Pair with: `12-memory-management-alignment.md`, `19-pointers.md`

12. Dynamic Memory Allocation
- Use when: malloc/free strategy, leaks, ownership.
- Pair with: `12-memory-management-alignment.md`, `23-linked-list-memory.md`

## Expertise

13. Overview Of C Standards
- Use when: C89/C99/C11/C17/C23 compatibility questions.
- Pair with: `06-c-standards.md`

14. Undefined Behaviour And Unspecified Behaviour
- Use when: nondeterministic behavior, compiler-dependent output.
- Pair with: `08-undefined-behavior.md`, `21-compiler-optimization.md`

15. Lvalue And Rvalue
- Use when: assignment legality, temporary objects, expression categories.
- Pair with: `04-c-deep-dive.md`, `06-c-standards.md`

16. Array Name Is Not A Pointer
- Use when: array decay confusion, `sizeof` surprises, function parameters.
- Pair with: `19-pointers.md`, `04-c-deep-dive.md`

17. Memory Layout And Rules
- Use when: alignment, padding, memory segments, object representation.
- Pair with: `12-memory-management-alignment.md`, `22-linker-elf.md`

18. More About The Structure Type
- Use when: struct packing, nesting, layout assumptions.
- Pair with: `12-memory-management-alignment.md`, `14-oop-in-c.md`

19. Do Not Abuse Side Effects In Subexpressions
- Use when: order-of-evaluation bugs, sequence-point issues.
- Pair with: `08-undefined-behavior.md`, `09-goto-control-flow.md`

## Fast Triage Heuristics

- If the user is blocked in debugging workflow, start from Practice first.
- If bug symptom involves syntax/type/API behavior, start from Basics.
- If symptom is "sometimes works, sometimes fails", prioritize Expertise and UB checks.
