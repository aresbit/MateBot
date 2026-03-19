# External C Tutorial Essence

This file distills practical rules into a fast-response guide.

## Practice Essence

### 1) Debugging workflow first, code edits second

- Use two baseline methods:
  - print intermediate values to narrow fault range
  - use debugger for larger projects
- Start from IO and boundaries, then narrow to a few lines.
- Keep each debug step falsifiable: one inserted print, one hypothesis.
- For toy programs, output-based debugging is often faster than full debugger setup.

### 2) Build high-quality help requests

- Include:
  - minimal reproducible input
  - observed output vs expected output
  - compiler command and errors
  - what has already been tried
- Avoid screenshots of code and huge unfiltered code dumps.

### 3) Naming and habits are correctness tools

- Naming consistency reduces wrong-variable and wrong-index mistakes.
- Style should optimize readability and reviewability, not personal cleverness.

## Basics Essence

### 1) IO mental model: everything starts as characters

- Console input is line-buffered; Enter commits the line.
- `scanf` consumes from program input buffer, not directly from keyboard events.
- `%c` trap: leftover `'\n'` is a real character and may be consumed immediately.
- Input and output are logically independent; do not over-engineer IO staging for display order.

### 2) Type conversion: implicit conversion is frequent and risky

- Implicit conversion happens in assignment, expression evaluation, function args, and returns.
- Hidden risks:
  - precision loss
  - truncation
  - overflow (especially signed overflow => UB)
- Use explicit cast when intent must be visible, but split complex expressions for readability.

### 3) Declaration/definition, scope/lifetime, dynamic memory

- Distinguish declaration from definition to avoid linkage mistakes in C projects.
- Scope and lifetime are different dimensions; lifetime bugs can survive compilation.
- Dynamic memory rules:
  - pair allocation and free exactly once
  - never use memory after free
  - check allocation failure (`NULL`)
  - reject zero-size allocation as an API edge case unless explicitly handled

## Expertise Essence

### 1) Standards awareness should be explicit in answers

- Mention standard context when relevant (C89/C90, C99, C11, C18).
- Provide strict compile mode when diagnosing portability:
  - `-std=c89|c99|c11`
  - `-pedantic-errors`
- Clarify when compiler extensions may hide non-portable code.

### 2) UB / unspecified / implementation-defined: separate clearly

- UB: standard imposes no requirements; result not reliable.
- Unspecified: one of several valid outcomes, choice not fixed.
- Implementation-defined: implementation documents chosen behavior.
- Do not reason from one observed UB run to a general rule.

### 3) Side effects and sequence points

- Core high-risk rule:
  - between two sequence points, avoid modifying one object multiple times
  - avoid modifying and separately reading the same object in conflicting ways
- Avoid clever expressions like `i++ + i++` even if "it works" locally.

### 4) Memory/object model pitfalls

- Array name is not pointer (decay has contexts and limits).
- Memory layout includes alignment and padding; do not assume packed layout unless guaranteed.
- Struct advanced features (e.g. flexible array members, bit-fields) require careful ABI/layout assumptions.

## Response Recipe (When Using This File)

1. State the single most relevant rule from above.
2. Give one minimal compilable example.
3. Add one counterexample (what not to do).
4. End with one concrete validation command or test case.
