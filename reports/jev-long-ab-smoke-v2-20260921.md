# Jev long-horizon matched A/B — 2026-09-21

Hash-only comparison of a shared context-fed baseline (A) and a Jev-validated bounded-action arm (B). The six holdout hashes were not used.

## Frozen slice

- Development hashes: 0d6ca4607eaf
- Matched replay turns per arm/harness: 3
- Adapters requested: opencode, grok-build, pi
- Per bounded invocation timeout: 20.0 seconds
- Jev timeout: 20.0 seconds
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
| grok-build | baseline | 1 | 3 | 3 | 3 | 0/1 | no=1 | 0 | 0 | 0 |
| grok-build | jev | 1 | 3 | 1 | 1 | 0/1 | no=1 | 0 | 3 | 2 |
| opencode | baseline | 1 | 3 | 3 | 3 | 0/1 | no=1 | 0 | 0 | 0 |
| opencode | jev | 1 | 3 | 1 | 1 | 0/1 | no=1 | 0 | 3 | 2 |
| pi | baseline | 1 | 3 | 3 | 0 | 0/1 | no=1 | 0 | 0 | 0 |
| pi | jev | 1 | 3 | 1 | 0 | 0/1 | no=1 | 0 | 3 | 2 |

## Per-task summaries

| Adapter | Hash | Mode | Turns | Executed | Statuses | Work-match | Outcome | Tools | Decisions | Fallbacks | R1-R6 fail mask |
|---|---|---|---:|---:|---|---:|---|---:|---:|---:|---|
| opencode | `0d6ca4607eaf` | baseline | 3 | 3 | timeout=3 | no | no | 0 | 0 | 0 | empty |
| opencode | `0d6ca4607eaf` | jev | 3 | 1 | not_executed=2, timeout=1 | no | no | 0 | 3 | 2 | empty |
| grok-build | `0d6ca4607eaf` | baseline | 3 | 3 | timeout=3 | no | no | 0 | 0 | 0 | empty |
| grok-build | `0d6ca4607eaf` | jev | 3 | 1 | not_executed=2, timeout=1 | no | no | 0 | 3 | 2 | empty |
| pi | `0d6ca4607eaf` | baseline | 3 | 3 | fail_1=3 | no | no | 0 | 0 | 0 | empty |
| pi | `0d6ca4607eaf` | jev | 3 | 1 | fail_1=1, not_executed=2 | no | no | 0 | 3 | 2 | empty |

## Interpretation boundary

This report uses a synthetic clean snapshot of this repository as the isolated execution workspace because the original Work worktrees are not part of the committed corpus. It therefore measures transfer of observable control behavior, not reproduction of every original file outcome. A/B cells are comparable only within the recorded harness, model, fixture, workspace, and turn budget.

Source run id: `jev-long-smoke-v2-20260921`
