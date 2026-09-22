# Current

Updated: 2026-09-21
Plan status: **owner accepted / frozen operating direction**
Owner spec: spec/owner.v2.json

## Active experiment

Issue 21 - **Jev persistent decision controller**

Purpose: implement the smallest context-aware Jev controller and measure it
against the preserved v1 hint pilot and existing Work behavior evidence.

## Current hypothesis

Jev should classify and select the next bounded bead/action from the full
relevant task context, then receive the resulting adapter events and decide
again. The previous one-shot hint pilot is only v1 smoke evidence.

## Baselines to preserve

- ChatGPT Work/Codex local transcript evidence = behavioral reference.
- Kilo Codex v0 = positive-control prompt baseline.
- Existing Kilo/OpenCode R1-R6, 22-thread replay, morph, and outcome notes = v0 historical/prototype evidence.

## Next action

**Current next action:** implement and test `spec/jev-controller-v2.md` as a
small reusable decision loop. Add the durable research/spec/issue record first,
then run one fake-adapter loop, one OpenCode smoke task, and one matched
baseline-versus-Jev slice across the available adapters.

**Historical baseline note:** a blocking defect was found and fixed first
(2026-09-22, `reports/versions/v66/README.md`).
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

The v1 pilot is already recorded in `reports/matched-replay-20260921.md`.
Before a new matched run, move old per-run artifacts aside or use a fresh
`run_id`; do not append fresh traces to an old evidence directory.

Then proceed as planned: select 3-5 representative tasks from the existing **development** replay set, not holdout. Freeze their acceptance/environment notes, then run the current configuration through:

1. Pi
2. OpenCode
3. Grok Build

in the same slice where technically possible.

Record exact model/provider/harness/control version and capture all observable interaction, tool/result, wait/failure, verification/provenance, output, continuity, and outcome signals that each harness exposes.

The next v2 slice is now explicitly authorized by the owner. Keep the old
baseline for comparison and change only the Jev decision-loop behavior in the
first implementation run.

Historical v1 baseline: **Baseline multi-harness Work behavior replay**.
Historical v1 baseline contract: **Do not change prompts/control before this baseline.**
The old slice also stated: **Do not build a general state machine or protocol framework in this slice.** Those sentences remain here as the
preserved v1 baseline boundary; Issue 21 is the separately authorized v2
experiment.

## Stop condition for this slice

Return with:
- comparable traces or explicit non-comparable reasons for all three harnesses;
- a compact automatic/structural comparison against Work reference evidence;
- the largest recurring behavioral deviations;
- exactly one smallest next control-layer hypothesis.

Do not build a general protocol framework in this slice. The v2 loop may use a
narrow runtime phase/transition gate because the owner explicitly approved
this controller experiment; expand it only if the measured replay requires it.

## Continuity rule

After real work, update this file to the measured result and exact next action. Do not use chat history as the project checkpoint.
