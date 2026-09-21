# Current

Updated: 2026-09-21
Plan status: **owner accepted / frozen operating direction**
Owner spec: spec/owner.v2.json

## Active experiment

GitHub issue #2 - **Baseline multi-harness Work behavior replay**

Purpose: establish the first baseline under the new plan before changing the control layer.

## Current hypothesis

No new control hypothesis yet. First measure the baseline across Pi, OpenCode, and Grok Build on the same small set of existing long Work-derived development tasks.

## Baselines to preserve

- ChatGPT Work/Codex local transcript evidence = behavioral reference.
- Kilo Codex v0 = positive-control prompt baseline.
- Existing Kilo/OpenCode R1-R6, 22-thread replay, morph, and outcome notes = v0 historical/prototype evidence.

## Next action

Select 3-5 representative tasks from the existing **development** replay set, not holdout. Freeze their acceptance/environment notes, then run the current configuration through:

1. Pi
2. OpenCode
3. Grok Build

in the same slice where technically possible.

Record exact model/provider/harness/control version and capture all observable interaction, tool/result, wait/failure, verification/provenance, output, continuity, and outcome signals that each harness exposes.

**Do not change prompts/control before this baseline.**

## Stop condition for this slice

Return with:
- comparable traces or explicit non-comparable reasons for all three harnesses;
- a compact automatic/structural comparison against Work reference evidence;
- the largest recurring behavioral deviations;
- exactly one smallest next control-layer hypothesis.

Do not build a general state machine or protocol framework in this slice.

## Continuity rule

After real work, update this file to the measured result and exact next action. Do not use chat history as the project checkpoint.
