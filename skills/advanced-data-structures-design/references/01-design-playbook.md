# Design Playbook

Use this checklist before proposing a data structure.

## 1. Choose The Right Model

Ask which model actually governs the target system:

- Pointer machine
- RAM or word-RAM
- Cell-probe
- BST model
- External-memory / I/O
- Cache-oblivious
- Persistent or retroactive timeline

Many bad designs fail because they optimize in the wrong model.

## 2. Pin Down The Operation Set

Write the exact interface:

- queries
- updates
- batch operations
- split / merge
- persistence or version branching
- retroactive insertion or deletion of operations

Then specify whether bounds must be worst-case, amortized, or expected.

## 3. Identify The Hard Axis

Usually one axis dominates:

- time vs space
- update vs query
- online vs offline
- locality vs flexibility
- comparison lower bound vs bit-trick opportunity
- dynamic maintenance vs rebuild

Design around the hard axis instead of polishing the easy one.

## 4. Look For A Representation Shift

Before inventing a new structure, test these shifts:

- turn time into a dimension
- turn updates into points or segments
- turn searches into geometric stabbing or range problems
- turn dynamic behavior into a decomposition over epochs
- turn cache cost into block movement

The course repeatedly uses representation changes to make hard problems tractable.

## 5. Pressure-Test The Tradeoff

For every proposal, answer:

- what is stored?
- what invariant is maintained?
- what operation pays for the work?
- where does amortization hide?
- what lower bound might contradict the target?
- what happens if the model changes slightly?

## 6. Prefer A Research-Grade Output Format

When presenting a candidate structure, use this order:

1. problem and model
2. target bounds
3. core idea
4. maintained invariant
5. operation costs
6. comparison to alternatives
7. known gap or open issue
