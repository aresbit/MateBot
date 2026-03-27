## Experiment 0 - baseline

**Score:** 6/7 (85.7%)
**Change:** none
**Reasoning:** establish baseline before mutation.
**Result:** missing efficiency-mode guidance.
**Failing outputs:** no explicit 30-minute emergency path.

## Experiment 1 - keep

**Score:** 7/7 (100.0%)
**Change:** added `高效模式（30分钟）` with strict limits: max 3 commands, top 3 blockers, 10-minute validation.
**Reasoning:** users often need emergency recovery speed; explicit budget improves execution efficiency.
**Result:** fixed the only failing eval (`efficiency_mode`).
**Failing outputs:** none.

## Experiment 2 - discard

**Score:** 7/7 (100.0%)
**Change:** tried adding terminology glossary.
**Reasoning:** expected to reduce ambiguity.
**Result:** no measurable gain on binary evals; extra content adds noise.
**Failing outputs:** none.
