# Jev long-horizon matched A/B — 2026-09-22

> **Launch-blocked / not a baseline (do not reuse).** Every arm in this smoke
> recorded `fail_1` with **empty events** because the Pi adapter passed the full
> context-pack prompt as a command-line argument and Windows aborted it with
> `The command line is too long`. The harness never started, so the `0 tools /
> outcome no` cells measure a launch failure, not model behavior — the same
> class of contamination flagged for the pre-v66 traces. Fixed the same day: the
> adapter now delivers the prompt over stdin (Pi/OpenCode) and `--prompt-file`
> (Grok), pinned by `tests/test_jev_controller_module.py`. The seed-materialized
> workspace itself worked (this run validated `git archive` seeding). Re-run with
> a fresh `run_id` before drawing any A/B conclusion; do not compare new cells to
> these rows.

Hash-only comparison of a shared context-fed baseline (A) and a Jev-validated bounded-action arm (B). The six holdout hashes were not used.

## Frozen slice

- Development hashes: 0d6ca4607eaf
- Matched replay turns per arm/harness: 3
- Adapters requested: pi
- Per bounded invocation timeout: 10.0 seconds
- Jev timeout: 10.0 seconds
- Jev model: `typesafe/jev-1.13` via OpenRouter Decisions API
- OpenCode model: `yolo-auto/qwen3.8-flash`
- Pi model: `yolo-auto/qwen3.8-flash`
- Grok Build model: `grok-4.7`
- Grok Build configured max turns: `8`
- Gold/reference: local ChatGPT Work/Codex development evidence; R1-R6 are diagnostic.
- Raw prompts, event bodies, transcript bodies, and credentials remain ignored/local.

## Aggregate results

| Adapter | Mode | Tasks | Turns | Executed | Timeouts | Work-match | Outcomes | Mean tools/task | Jev decisions | Fallbacks |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|---:|
| pi | baseline | 1 | 3 | 3 | 0 | 0/1 | no=1 | 0 | 0 | 0 |
| pi | jev | 1 | 3 | 1 | 0 | 0/1 | no=1 | 0 | 3 | 2 |

## Per-task summaries

| Adapter | Hash | Mode | Turns | Executed | Statuses | Work-match | Outcome | Tools | Decisions | Fallbacks | R1-R6 fail mask |
|---|---|---|---:|---:|---|---:|---|---:|---:|---:|---|
| pi | `0d6ca4607eaf` | baseline | 3 | 3 | fail_1=3 | no | no | 0 | 0 | 0 | empty |
| pi | `0d6ca4607eaf` | jev | 3 | 1 | fail_1=1, not_executed=2 | no | no | 0 | 3 | 2 | empty |

## Interpretation boundary

This report uses a synthetic clean snapshot of this repository as the isolated execution workspace because the original Work worktrees are not part of the committed corpus. It therefore measures transfer of observable control behavior, not reproduction of every original file outcome. A/B cells are comparable only within the recorded harness, model, fixture, workspace, and turn budget.

Source run id: `jev-long-smoke-seed-20260922`
