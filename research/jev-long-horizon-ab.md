# Jev long-horizon matched A/B experiment

Updated: 2026-09-21

Status: executable experiment contract; implementation and run pending.

## Question

Does a bounded Jev decision layer improve observable, Work-aligned coding-agent
behavior and task outcomes over the same harness, model, repository context,
and task turns without Jev?

The reference remains the local ChatGPT Work/Codex corpus. The 16 development
threads and six hidden holdout threads in
[`reports/work-long-holdout.md`](../reports/work-long-holdout.md) remain the
fixture boundary. The Work-derived taxonomy and R1-R6 scores are diagnostic
gold signals, not an exact tool-order requirement. The richer comparison must
also retain inspection, verification, provenance, continuity, outcome, and
truthful reporting signals.

## Main hypothesis

Adding Jev will improve action selection only when both arms receive the same
live context feeder and the Jev arm chooses from a closed set of legal,
observation-derived candidates. Jev must not be credited for context that only
its arm receives.

This is one intervention: add the Jev decision/validation step. The feeder,
prompt budget, harness, model, task turn, workspace snapshot, timeout, and
adapter configuration stay matched between A and B.

## Arms

### A — matched no-Jev baseline

For each selected Work user turn, the harness receives:

- the current owner-visible ask;
- the same deterministic repository/context-feeder pack used by B;
- the same accumulated observable history and current workspace;
- no Jev answer, action hint, or controller fallback.

The harness remains responsible for deciding and executing its own next tool
action.

### B — matched Jev controller

The harness receives the same inputs as A. Before the bounded invocation,
Jev receives the privacy-safe `DecisionContext` containing the owner ask,
relevant prior turns, repository facts, changed paths, normalized prior events,
test evidence, open/candidate beads, phase, constraints, and the legal action
set. The host validates Jev's typed answer and adds only the selected bounded
action to the harness prompt. The harness remains responsible for tools and
side effects; Jev has no file-system or tool authority.

After the invocation, the feeder observes workspace status and normalized
events, updates the context, and the next user turn is presented. A low-
confidence or invalid Jev answer is recorded as a fallback and does not run an
unapproved action.

## Scale and fixtures

Run **60 matched replay user turns** across the existing **16 development
hashes**, with no holdout use or tuning. Allocate at least three turns to every
development hash, then continue in the frozen report order until the total is
60. Preserve task boundaries and accumulated state within each hash; do not
pretend 60 independent one-shot tasks are a long run.

The six hidden holdout hashes remain sealed until the development A/B report,
one hypothesis decision, and any control revision are complete. If a second
repetition is affordable, repeat the same 60 development turns with a fresh
run id; do not replace the first repetition.

## Model and harness matrix

Record exact values from the ignored `.env` at run time without committing
credentials:

| Harness | Current configured execution model | Jev |
|---|---|---|
| OpenCode | `OPENCODE_MODEL=yolo-auto/qwen3.8-flash` | `typesafe/jev-1.13` via OpenRouter |
| Pi | `PI_MODEL=yolo-auto/qwen3.8-flash` | `typesafe/jev-1.13` via OpenRouter |
| Grok Build | `GROK_BUILD_MODEL=grok-4.7` | `typesafe/jev-1.13` via OpenRouter |

Qwen Flash is therefore the current bigger execution model for the OpenCode
and Pi arms, through Yolo Auto. It is not Jev: Jev is the separate controller
call. The report must state the exact configured model strings rather than
calling any arm model-agnostic.

## Context feeder contract

The feeder is shared by A and B and may use deterministic local inspection:

- current workspace git status, branch, top-level tree, instruction files,
  changed paths, and test/command results;
- current and recent owner turns, with harness boilerplate removed;
- normalized adapter event kinds, statuses, tool names, failures, and session
  metadata, never raw event bodies;
- bounded file names and safe excerpts when the workspace actually contains
  relevant files;
- candidate beads with descriptions and acceptance criteria derived from the
  current task state, not an unrestricted action catalog.

The first context pack must be auditable by hash and field counts. It must not
commit prompt bodies, raw transcript bodies, credentials, or private files.

## Measurements

For every arm, harness, hash, and replay turn, retain hash-only or aggregate
records for:

- status, timeout, return code, duration, and bounded invocation count;
- Jev decision, confidence, validation/fallback reason, and decision latency
  for B only;
- normalized tool/action sequence, waits, failures, retries, delegation, and
  continuation/session observations;
- R1-R6 fail masks as cheap diagnostic signals;
- Work-match/process alignment where the scorer can compute it;
- inspection/research, verification/provenance, output honesty, continuity,
  changed paths, tests, and observable task outcome;
- per-task and per-harness A-minus-B comparisons, plus repeated-run variance
  when a second repetition exists.

No claim of Jev benefit is valid if the arms differ in fixture, model,
workspace, context pack, timeout, or turn budget. A result with unavailable
or non-comparable harnesses must say so explicitly.

## Success and stop rules

The experiment succeeds as an evidence slice if it produces 60 matched turns
per arm for each available harness, or an explicit count and reason for every
unavailable/non-comparable cell, with a hash-only report and frozen fixture
manifest.

Jev is retained only if B improves a predeclared outcome or observable
behavior measure without harming verification, safety, scope, honest output,
or continuity. If the result is null or worse, preserve it and choose exactly
one next control-layer hypothesis. Do not tune the evaluator or expose
holdout results to rescue a disappointing result.

## Current execution checklist

1. Add the shared deterministic context feeder and tests.
2. Add a long-horizon runner that consumes up to 60 Work-derived user turns
   while preserving per-hash context and fresh A/B workspaces.
3. Run a small smoke cell on one development hash per available harness.
4. Run the frozen 60-turn development A/B matrix for OpenCode, Pi, and Grok
   Build where available.
5. Write the hash-only report, update `checkpoints/CURRENT.md`, and only then
   consider the sealed holdout.

## Execution result — 2026-09-22

The checklist is complete for the development slice. OpenCode, Grok Build, and
Pi each produced a clean 60-turn A/B result over all 16 development hashes;
the six holdout hashes remained sealed. The combined hash-only report is
`reports/jev-long-ab-20260922.md`, with one detailed report per harness.

The current Jev policy is not promoted. Work-match was OpenCode 8/16 baseline
versus 4/16 Jev, Grok Build 0/16 versus 0/16, and Pi 0/16 versus 0/16. Jev's
0.55 confidence gate caused 47, 47, and 48 fallbacks and only 13, 13, and 12
executed Jev turns. This is the measured under-execution failure to address;
it is not evidence that Jev can inspect files or act without the host feeder.

The harness liveness boundary is now a 20-minute inactivity timeout reset by
stdout/stderr progress, with a two-hour absolute safety cap. Timeout reasons
are retained as `inactivity` or `max_runtime`; see
`docs/harness-timeout-policy.md`.

The one follow-up hypothesis is to keep the feeder, choices, models, fixtures,
and timeouts fixed while making low-confidence Jev output advisory and still
executing the baseline-equivalent feeder prompt. A fresh matched 60-turn slice
is required before changing the candidate taxonomy or exposing holdout hashes.
