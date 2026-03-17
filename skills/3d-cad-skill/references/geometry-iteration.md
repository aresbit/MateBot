# Geometry Iteration

Use this reference when building or debugging a 3D model through repeated render-inspect-revise cycles.

## Loop

1. Produce a minimal renderable model.
2. Generate evidence: render, screenshot, projection, section cut, or explicit dimensions.
3. Compare the evidence against the brief.
4. State the specific defect.
5. Apply the smallest plausible fix.
6. Repeat until the remaining uncertainty is minor and explicit.

## What To Inspect

### Global form

- Overall proportions
- Symmetry and centering
- Orientation of major features
- Whether the silhouette matches the intended object

### Functional geometry

- Hole diameter and placement
- Wall thickness
- Slot widths and insertion paths
- Clearances for lids, fasteners, or mating parts
- Contact surfaces and support points

### Fabrication risk

- Thin or fragile members
- Unsupported bridges and overhangs
- Internal voids that cannot be cleaned or printed
- Sharp internal corners where a radius is likely needed

## How To Diagnose Problems

- If the whole part looks wrong, inspect coordinate system choices and base dimensions first.
- If one feature drifts, inspect local transforms and subtraction volumes.
- If symmetry is off, replace duplicated magic numbers with mirrored parameters.
- If exported meshes fail, simplify booleans and check for coplanar or zero-thickness geometry.
- If the part is hard to revise, refactor repeated dimensions into named parameters before continuing.

## Modeling Style

- Use named parameters for every critical dimension.
- Group related operations into small modules or functions.
- Keep boolean operands readable and spatially local.
- Comment only where spatial intent is not obvious from the code.
- Prefer deterministic geometry over clever compact code.

## OpenSCAD Notes

- Start from primitives and boolean composition.
- Keep `difference()`, `union()`, and `intersection()` blocks visually clean.
- Avoid burying key dimensions inside nested transforms.
- When debugging, isolate one body or subtraction volume at a time.

## build123d Notes

- Separate sketch definition from 3D feature creation.
- Name workplanes and construction geometry clearly.
- Treat fillets and chamfers as late-stage operations.
- Use helper functions when a feature repeats with stable intent.

## Response Pattern

When reporting progress to the user, keep it concrete:

- What changed
- What evidence you used to verify it
- What remains uncertain

Do not claim a fit-critical model is correct unless it has been verified by render evidence, explicit dimension checks, or user-provided measurements.
