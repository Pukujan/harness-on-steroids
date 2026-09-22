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

**Blocking defect found and fixed first (2026-09-22, `reports/versions/v66/README.md`).**
The replay runners passed the raw first user turn to the harness. In these Work
transcripts that turn is the prepended `<recommended_plugins>` / `<environment_context>`
block, and for **11 of the 22** develop+holdout hashes it contains no ask at all, so a
baseline on those hashes measures behaviour on a **task-free prompt**. Any hint/control
arm that adds a directive would appear to help only because it supplied the sole
instruction — this is exactly what the pre-fix Pi/OpenCode/Grok controller rows show
(baseline 0 tool calls vs a hint arm up to 306). Do **not** reuse pre-v66 traces as a
baseline, and do not compare new cells to them.

Fix is in: `research/replay_lib.py` (`strip_context_blocks` / `first_ask` / `ask_turns`),
both runners now send the real ask and record `ask_present` / `ask_shifted`, plus gate
`tests/test_replay_prompt_hygiene.py`. The `reports/replay-scores.md` OpenCode column is
flagged contaminated for those 11 hashes (rows kept because `tests/test_replay_scores.py`
pins them).

Before selecting the 3-5 tasks: move the old `data/replay/<hash>/opencode.ndjson` aside
per hash (the runner **appends**, so re-running in place mixes old and new evidence and
silently corrupts the pinned cells), then take fresh traces on the real ask.

Then proceed as planned: select 3-5 representative tasks from the existing **development** replay set, not holdout. Freeze their acceptance/environment notes, then run the current configuration through:

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
