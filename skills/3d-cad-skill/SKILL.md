---
name: 3d-cad-skill
description: Create and iterate parametric 3D CAD models for Claude using an inspectable feedback loop. Use when the task involves OpenSCAD, build123d, STL/STEP/3MF output, fixture/enclosure/adapter design, or debugging shape accuracy from renders or screenshots.
---

# 3D CAD Skill

Use this skill for parametric 3D modeling tasks where geometry must be correct, manufacturable, and easy to revise.

## When To Use It

Trigger this skill when the user asks for any of the following:

- A 3D printable or CAD-ready part
- OpenSCAD or build123d model generation
- Edits to an existing parametric model
- Shape debugging from screenshots, renders, or exported meshes
- Precise dimensions, fit checks, tolerances, wall thicknesses, or hole placement

## Core Rule

Do not trust mental visualization of 3D geometry. Write code, render or export a view, inspect the result, then revise.

If the environment supports screenshots or image inspection, use them after every meaningful geometry change. If not, inspect through deterministic evidence such as orthographic projections, section cuts, bounding-box checks, and explicit dimension calculations.

## Workflow

1. Capture the design brief.
2. Choose the modeling representation.
3. Build the smallest correct parametric skeleton.
4. Render and inspect.
5. Fix one geometric issue at a time.
6. Deliver the model with clear parameters and assumptions.

## 1. Capture The Design Brief

Before modeling, extract:

- Target output: `stl`, `step`, `3mf`, source code only, or all of them
- Modeling stack: prefer the user's requested tool; otherwise default to the simplest proven option
- Critical dimensions and units
- Mating parts, clearances, print orientation, and strength constraints
- Whether the goal is appearance, fit, mechanism, or manufacturability

If requirements are incomplete, make explicit assumptions and keep the first version simple.

## 2. Choose The Modeling Representation

- Use OpenSCAD for straightforward constructive solid geometry, parameterized print parts, jigs, spacers, brackets, trays, and enclosures.
- Use build123d when the part benefits from sketch-extrude workflows, fillet/chamfer-heavy operations, or more structured Python logic.
- Prefer simple primitives and boolean composition before introducing advanced operations.

## 3. Build The Smallest Correct Parametric Skeleton

Start with a coarse model that proves overall proportions and alignment:

- Define top-level parameters first.
- Separate base body, cutouts, mounts, and cosmetic details.
- Keep transforms and coordinate frames obvious.
- Delay fillets, chamfers, text embossing, and decorative features until the base geometry is correct.

Structure code so a later pass can adjust one concern without rewriting the whole model.

## 4. Render And Inspect

After each meaningful change, inspect the result deliberately:

- Check silhouette and proportions from multiple angles.
- Check critical dimensions numerically.
- Check whether holes, cutouts, and mating faces are centered and aligned.
- Check printability: unsupported spans, wall thickness, trapped voids, and impossible overhangs.
- Check whether the model matches the user's stated intent, not just whether the code runs.

Read [`references/geometry-iteration.md`](/home/ares/.claude/skills/3d-cad-skill/references/geometry-iteration.md) when the task needs a stricter inspection loop or when you are debugging repeated geometry mistakes.

## 5. Fix One Geometric Issue At A Time

When something looks wrong:

- Name the defect precisely.
- Identify the smallest parameter or operation likely causing it.
- Change one thing.
- Re-render and compare against the previous result.

Avoid broad rewrites unless the part architecture is clearly wrong.

## 6. Deliverables

Default deliverables:

- The source model
- A short list of exposed parameters
- Assumptions and unresolved risks
- Export instructions if the environment cannot generate meshes directly

When useful, also provide:

- Recommended print orientation
- Suggested tolerance ranges
- Notes on likely failure points or reinforcement options

## Quality Bar

The final result should be:

- Parametric rather than hard-coded
- Easy to inspect and revise
- Dimensionally explicit
- Realistic for the intended fabrication method
- Honest about assumptions and unverified fit
