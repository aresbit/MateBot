---
name: advanced-data-structures-design
description: High-entropy design skill for advanced data structures based on MIT 6.851. Use for inventing, comparing, or stress-testing data structures under strict asymptotic, model, persistence, cache, hashing, integer, string, graph, and lower-bound constraints.
---

# advanced-data-structures-design

## Purpose

Use this skill when the task is not just to implement a known data structure, but to design or evaluate one under strong theoretical constraints.

This skill is optimized for high-signal retrieval:

1. Start with `references/00-course-map.md`.
2. Read `references/01-design-playbook.md` before proposing a structure.
3. Use `references/02-problem-to-approach.md` to route from problem type to a theme file.
4. Read one of the thematic files `references/10-...md` to `references/17-...md`.
5. Only if needed, drill down into the raw lecture files `references/L01.md` to `references/L22.md`.

## What This Skill Is Good At

- Turning a problem statement into a data-structure design space
- Choosing the right computation model before designing
- Comparing update/query/space/preprocessing tradeoffs
- Reasoning about persistence, retroactivity, and time-travel variants
- Evaluating cache-aware and cache-oblivious designs
- Framing lower bounds and impossibility arguments
- Surfacing open problems and research-grade alternatives

## Working Style

When using this skill:

- State the model first: pointer machine, RAM, word-RAM, cell-probe, I/O, cache-oblivious, BST model, or dynamic graph setting.
- State the operation set next: query, update, partial rebuild, offline/online, batched, amortized, randomized, persistent, or retroactive.
- Separate known results from proposed synthesis.
- Prefer asymptotic tradeoff tables and invariants over long prose.
- Call out what the design is optimizing: worst-case, amortized, expected time, memory transfers, or space.

## Retrieval Notes

- `references/10-temporal-data-structures.md` is the entry for persistence and retroactivity.
- `references/12-dynamic-optimality-and-bsts.md` is the entry for BST access-sequence questions.
- `references/13-memory-hierarchy-and-cache-oblivious.md` is the entry for external-memory and cache-oblivious design.
- `references/14-hashing-and-integer-structures.md` is the entry for hashing, predecessor, and integer lower bounds.
- `references/17-dynamic-graphs.md` is the entry for connectivity and dynamic graph maintenance.
- Use `references/L01.md` to `references/L22.md` only when the theme file is too compressed for the task.
