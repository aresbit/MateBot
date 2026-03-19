# Course Map

This skill compresses MIT 6.851 into a design-oriented map rather than a lecture dump.

## Main Themes

- Time travel in data structures:
  Persistence, full persistence, confluent persistence, retroactivity, and non-oblivious retroactivity.
- Optimal search structures:
  Binary search trees, geometric viewpoints, splay trees, greedy trees, and dynamic optimality.
- Memory hierarchy:
  I/O models, external memory, red-blue pebble game, and cache-oblivious thinking.
- Research-style data structure design:
  Strong model assumptions, reduction-based design, lower bounds, and open problems.

## Theme Files

- `10-temporal-data-structures.md`: persistence and retroactivity
- `11-geometry-and-range-searching.md`: point location, range searching, and fractional cascading
- `12-dynamic-optimality-and-bsts.md`: BST access sequences and dynamic optimality
- `13-memory-hierarchy-and-cache-oblivious.md`: I/O models and cache-oblivious design
- `14-hashing-and-integer-structures.md`: hashing, predecessor, fusion trees, and lower bounds
- `15-tree-queries-and-strings.md`: RMQ, LCA, tries, suffix trees, and suffix arrays
- `16-succinct-structures.md`: succinct indexing and compressed representations
- `17-dynamic-graphs.md`: link-cut trees and dynamic connectivity

## How To Use The References

- Start with one theme file, not a raw lecture.
- Use the theme file to identify the right model, known tradeoffs, and neighboring techniques.
- Drop into `L01.md` to `L22.md` only when you need original detail, proof flavor, or a specific cited construction.
- When proposing a new structure, cross-check three things:
  model assumptions, lower-bound pressure, and whether the target tradeoff already appears in a theme family.

## Design Questions This Course Helps With

- Can this operation set support persistence or retroactivity cheaply?
- Is the bottleneck comparison complexity, word operations, or memory transfers?
- Does the problem become easier after geometric or temporal reinterpretation?
- Is there a decomposition that converts a hard dynamic problem into batched or offline pieces?
- What lower bound blocks the naive improvement I want?
