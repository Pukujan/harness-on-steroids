# Current

Updated: 2026-09-21
Plan status: **owner accepted / frozen operating direction**
Owner spec: spec/owner.v2.json

## Active experiment

Issue 22 - **Jev long-horizon matched A/B**

Purpose: test whether a validated Jev decision layer improves a shared,
context-fed coding harness over a matched no-Jev baseline across 60
Work-derived development turns and the available Pi/OpenCode/Grok Build arms.

## Current hypothesis

Jev should improve bounded action selection only when it receives the same
live repository/task context made available to the no-Jev baseline. The
previous one-shot hint pilot and context-poor v2 replay are historical smoke
evidence only.

## Baselines to preserve

- ChatGPT Work/Codex local transcript evidence = behavioral reference.
- Kilo Codex v0 = positive-control prompt baseline.
- Existing Kilo/OpenCode R1-R6, 22-thread replay, morph, and outcome notes = v0 historical/prototype evidence.

## Last verified v2 result — 2026-09-21

Implemented and tested the smallest reusable v2 loop:

- `DecisionContext` carries the owner ask, relevant conversation, beads,
  adapter observations, evidence, repository facts, changes, test results,
  constraints, phase, retries, and user-input status with deterministic
  32K-budget compaction.
- Jev receives nine typed Choice/Score/Noul questions through the OpenRouter
  Decisions API. The live schema was probed and corrected to the provider's
  `criteria` shape; native Noul and Score answers are parsed into booleans and
  legend labels.
- `JevDecisionLoop` validates phase-legal actions, rejects low-confidence,
  unknown, unavailable, or unavailable-bead decisions, executes one bounded
  adapter step, folds normalized observations back into context, and asks Jev
  again. Fake tests prove three-round context accumulation and no adapter call
  on fallback.
- OpenCode, Grok Build, and Pi each have normalized event/session extraction
  tests. Native session IDs are recorded only when emitted; the runner uses
  explicit context replay and does not invent continuation IDs.
- Fresh matched run: `reports/matched-replay-jev-v2-20260921.md`, run id
  `jev-v2-matched-20260921`, three development hashes across all three
  available adapters. It produced repeated decisions on one hash per adapter
  (two decisions each), while 6/9 Jev arms stopped on low confidence. Baseline
  arms timed out 7/9 times; none of the 18 arms reached a Work match. A single
  repetition does not establish variance.

All focused tests and ruff checks pass. Raw prompts, stderr, and adapter event
bodies remain in ignored `.controller-runs/` artifacts only.

## External Jev evidence update — 2026-09-21

Public Jev integrations confirm that Jev is decision-only. The host must
construct the live state and closed candidate set, then validate and execute
the selected option. See `research/jev-ecosystem-evidence.md` and
`research/jev-controller-v2-research.md` for the source-backed comparison.

The first v2 replay did not yet have that feeder: it supplied the owner ask,
one synthetic `task-main` bead, generic constraints, the intake action set,
and mostly empty conversation/repository/event/test context. It therefore
tested loop mechanics and fallback, not observation-derived coding decisions.

## Next action

**Exactly one next control-layer hypothesis:** add a bounded context-feeder
preflight before the first Jev call: deterministic repository facts plus a
coding-worker/adapter inspection that proposes real candidate beads and
acceptance criteria. Hold the Jev schema, confidence threshold, adapters, and
loop constant, then rerun the same frozen hashes. The earlier
`CLASSIFY_REQUEST` choice-set hypothesis is paused until the decision context
is populated, so the two interventions are not confounded.

## Long-horizon A/B contract

The executable contract is `research/jev-long-horizon-ab.md`. The next slice
must first add the shared deterministic context feeder and a 60-turn matched
runner. A and B must use the same Work-derived development turn fixtures,
fresh equivalent workspaces, feeder pack, timeout, and harness/model. B adds
only the Jev decision, typed validation, and bounded action hint. OpenCode and
Pi currently use `yolo-auto/qwen3.8-flash`; Grok Build uses `grok-4.7`; Jev is
the separate `typesafe/jev-1.13` OpenRouter call. The ChatGPT Work corpus
remains the behavioral reference and holdout remains sealed.

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
