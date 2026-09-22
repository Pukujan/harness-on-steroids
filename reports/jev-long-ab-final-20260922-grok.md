# Jev long-horizon matched A/B — 2026-09-22

Hash-only comparison of a shared context-fed baseline (A) and a Jev-validated bounded-action arm (B). The six holdout hashes were not used.

## Frozen slice

- Development hashes: 0d6ca4607eaf, 1a415bc257e5, 1b09f49da9b9, 28372e365066, 2bde00530ddd, 633c140546c0, 6b1cd28c4803, 6e412585c223, 6eb8631b71ff, 74841f3cc419, 76b12d5e1a66, 8d42bc26b8ea, a5842562d1c9, b7e6393f4c14, bd179678f540, f37de8488162
- Matched replay turns per arm/harness: 60
- Adapters requested: grok-build
- Per bounded invocation timeout: 60.0 seconds
- Jev timeout: 30.0 seconds
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
| grok-build | baseline | 16 | 60 | 60 | 58 | 0/16 | no=16 | 0 | 0 | 0 |
| grok-build | jev | 16 | 60 | 13 | 12 | 0/16 | no=16 | 0 | 60 | 47 |

## Per-task summaries

| Adapter | Hash | Mode | Turns | Executed | Statuses | Work-match | Outcome | Tools | Decisions | Fallbacks | R1-R6 fail mask |
|---|---|---|---:|---:|---|---:|---|---:|---:|---:|---|
| grok-build | `0d6ca4607eaf` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| grok-build | `0d6ca4607eaf` | jev | 4 | 1 | not_executed=3, timeout=1 | no | no | 0 | 4 | 3 | empty |
| grok-build | `1a415bc257e5` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| grok-build | `1a415bc257e5` | jev | 4 | 0 | not_executed=4 | no | no | 0 | 4 | 4 | empty |
| grok-build | `1b09f49da9b9` | baseline | 4 | 4 | ok=1, timeout=3 | no | no | 0 | 0 | 0 | empty |
| grok-build | `1b09f49da9b9` | jev | 4 | 0 | not_executed=4 | no | no | 0 | 4 | 4 | empty |
| grok-build | `28372e365066` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| grok-build | `28372e365066` | jev | 4 | 2 | not_executed=2, timeout=2 | no | no | 0 | 4 | 2 | empty |
| grok-build | `2bde00530ddd` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| grok-build | `2bde00530ddd` | jev | 4 | 1 | not_executed=3, timeout=1 | no | no | 0 | 4 | 3 | empty |
| grok-build | `633c140546c0` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| grok-build | `633c140546c0` | jev | 4 | 0 | not_executed=4 | no | no | 0 | 4 | 4 | empty |
| grok-build | `6b1cd28c4803` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| grok-build | `6b1cd28c4803` | jev | 4 | 1 | not_executed=3, timeout=1 | no | no | 0 | 4 | 3 | empty |
| grok-build | `6e412585c223` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| grok-build | `6e412585c223` | jev | 4 | 1 | not_executed=3, timeout=1 | no | no | 0 | 4 | 3 | empty |
| grok-build | `6eb8631b71ff` | baseline | 4 | 4 | ok=1, timeout=3 | no | no | 0 | 0 | 0 | empty |
| grok-build | `6eb8631b71ff` | jev | 4 | 0 | not_executed=4 | no | no | 0 | 4 | 4 | empty |
| grok-build | `74841f3cc419` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| grok-build | `74841f3cc419` | jev | 4 | 1 | not_executed=3, timeout=1 | no | no | 0 | 4 | 3 | empty |
| grok-build | `76b12d5e1a66` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| grok-build | `76b12d5e1a66` | jev | 4 | 1 | not_executed=3, timeout=1 | no | no | 0 | 4 | 3 | empty |
| grok-build | `8d42bc26b8ea` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| grok-build | `8d42bc26b8ea` | jev | 4 | 1 | not_executed=3, timeout=1 | no | no | 0 | 4 | 3 | empty |
| grok-build | `a5842562d1c9` | baseline | 3 | 3 | timeout=3 | no | no | 0 | 0 | 0 | empty |
| grok-build | `a5842562d1c9` | jev | 3 | 0 | not_executed=3 | no | no | 0 | 3 | 3 | empty |
| grok-build | `b7e6393f4c14` | baseline | 3 | 3 | timeout=3 | no | no | 0 | 0 | 0 | empty |
| grok-build | `b7e6393f4c14` | jev | 3 | 2 | not_executed=1, partial=1, timeout=1 | no | no | 0 | 3 | 1 | empty |
| grok-build | `bd179678f540` | baseline | 3 | 3 | timeout=3 | no | no | 0 | 0 | 0 | empty |
| grok-build | `bd179678f540` | jev | 3 | 1 | not_executed=2, timeout=1 | no | no | 0 | 3 | 2 | empty |
| grok-build | `f37de8488162` | baseline | 3 | 3 | timeout=3 | no | no | 0 | 0 | 0 | empty |
| grok-build | `f37de8488162` | jev | 3 | 1 | not_executed=2, timeout=1 | no | no | 0 | 3 | 2 | empty |

## Interpretation boundary

This report uses a synthetic clean snapshot of this repository as the isolated execution workspace because the original Work worktrees are not part of the committed corpus. It therefore measures transfer of observable control behavior, not reproduction of every original file outcome. A/B cells are comparable only within the recorded harness, model, fixture, workspace, and turn budget.

Source run id: `jev-long-ab-final-20260922-grok`
