# Jev long-horizon matched A/B — 2026-09-22

Hash-only comparison of a shared context-fed baseline (A) and a Jev-validated bounded-action arm (B). The six holdout hashes were not used.

## Frozen slice

- Development hashes: 0d6ca4607eaf, 1a415bc257e5, 1b09f49da9b9, 28372e365066, 2bde00530ddd, 633c140546c0, 6b1cd28c4803, 6e412585c223, 6eb8631b71ff, 74841f3cc419, 76b12d5e1a66, 8d42bc26b8ea, a5842562d1c9, b7e6393f4c14, bd179678f540, f37de8488162
- Matched replay turns per arm/harness: 60
- Adapters requested: opencode
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
| opencode | baseline | 16 | 60 | 60 | 57 | 8/16 | no=5, partial=11 | 8.3 | 0 | 0 |
| opencode | jev | 16 | 60 | 13 | 12 | 4/16 | no=9, partial=7 | 3.6 | 60 | 47 |

## Per-task summaries

| Adapter | Hash | Mode | Turns | Executed | Statuses | Work-match | Outcome | Tools | Decisions | Fallbacks | R1-R6 fail mask |
|---|---|---|---:|---:|---|---:|---|---:|---:|---:|---|
| opencode | `0d6ca4607eaf` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| opencode | `0d6ca4607eaf` | jev | 4 | 1 | not_executed=3, timeout=1 | no | no | 0 | 4 | 3 | empty |
| opencode | `1a415bc257e5` | baseline | 4 | 4 | timeout=4 | no | no | 1 | 0 | 0 | R3 |
| opencode | `1a415bc257e5` | jev | 4 | 0 | not_executed=4 | no | no | 0 | 4 | 4 | empty |
| opencode | `1b09f49da9b9` | baseline | 4 | 4 | ok=3, timeout=1 | yes | partial | 3 | 0 | 0 | none |
| opencode | `1b09f49da9b9` | jev | 4 | 0 | not_executed=4 | no | no | 0 | 4 | 4 | empty |
| opencode | `28372e365066` | baseline | 4 | 4 | timeout=4 | yes | partial | 9 | 0 | 0 | none |
| opencode | `28372e365066` | jev | 4 | 1 | not_executed=3, timeout=1 | no | partial | 2 | 4 | 3 | R3 |
| opencode | `2bde00530ddd` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| opencode | `2bde00530ddd` | jev | 4 | 1 | not_executed=3, timeout=1 | no | no | 0 | 4 | 3 | empty |
| opencode | `633c140546c0` | baseline | 4 | 4 | timeout=4 | no | partial | 6 | 0 | 0 | R3 |
| opencode | `633c140546c0` | jev | 4 | 0 | not_executed=4 | no | no | 0 | 4 | 4 | empty |
| opencode | `6b1cd28c4803` | baseline | 4 | 4 | timeout=4 | yes | partial | 3 | 0 | 0 | none |
| opencode | `6b1cd28c4803` | jev | 4 | 1 | not_executed=3, timeout=1 | no | no | 0 | 4 | 3 | empty |
| opencode | `6e412585c223` | baseline | 4 | 4 | timeout=4 | yes | partial | 4 | 0 | 0 | none |
| opencode | `6e412585c223` | jev | 4 | 1 | not_executed=3, timeout=1 | yes | partial | 5 | 4 | 3 | none |
| opencode | `6eb8631b71ff` | baseline | 4 | 4 | timeout=4 | no | partial | 12 | 0 | 0 | R3 |
| opencode | `6eb8631b71ff` | jev | 4 | 0 | not_executed=4 | no | no | 0 | 4 | 4 | empty |
| opencode | `74841f3cc419` | baseline | 4 | 4 | timeout=4 | no | no | 0 | 0 | 0 | empty |
| opencode | `74841f3cc419` | jev | 4 | 1 | not_executed=3, timeout=1 | no | no | 0 | 4 | 3 | empty |
| opencode | `76b12d5e1a66` | baseline | 4 | 4 | timeout=4 | yes | partial | 18 | 0 | 0 | none |
| opencode | `76b12d5e1a66` | jev | 4 | 1 | not_executed=3, timeout=1 | no | partial | 11 | 4 | 3 | R3 |
| opencode | `8d42bc26b8ea` | baseline | 4 | 4 | timeout=4 | no | partial | 24 | 0 | 0 | R3 |
| opencode | `8d42bc26b8ea` | jev | 4 | 2 | not_executed=2, ok=1, timeout=1 | no | partial | 10 | 4 | 2 | R3 |
| opencode | `a5842562d1c9` | baseline | 3 | 3 | timeout=3 | yes | partial | 20 | 0 | 0 | none |
| opencode | `a5842562d1c9` | jev | 3 | 0 | not_executed=3 | no | no | 0 | 3 | 3 | empty |
| opencode | `b7e6393f4c14` | baseline | 3 | 3 | timeout=3 | yes | partial | 15 | 0 | 0 | none |
| opencode | `b7e6393f4c14` | jev | 3 | 2 | not_executed=1, timeout=2 | yes | partial | 14 | 3 | 1 | none |
| opencode | `bd179678f540` | baseline | 3 | 3 | timeout=3 | no | no | 3 | 0 | 0 | R3 |
| opencode | `bd179678f540` | jev | 3 | 1 | not_executed=2, timeout=1 | yes | partial | 8 | 3 | 2 | none |
| opencode | `f37de8488162` | baseline | 3 | 3 | timeout=3 | yes | partial | 15 | 0 | 0 | none |
| opencode | `f37de8488162` | jev | 3 | 1 | not_executed=2, timeout=1 | yes | partial | 8 | 3 | 2 | none |

## Interpretation boundary

This report uses a synthetic clean snapshot of this repository as the isolated execution workspace because the original Work worktrees are not part of the committed corpus. It therefore measures transfer of observable control behavior, not reproduction of every original file outcome. A/B cells are comparable only within the recorded harness, model, fixture, workspace, and turn budget.

Source run id: `jev-long-ab-final-20260922-opencode`
