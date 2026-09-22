# Jev controller v2 matched replay — 2026-09-21

This hash-only report compares one baseline invocation with a repeated Jev decision loop over the same existing development Work hashes.

## Frozen slice

- Work hashes: 0d6ca4607eaf, 1a415bc257e5, 28372e365066
- Adapters: opencode, grok-build, pi
- Per bounded invocation timeout: 15.0 seconds
- Jev model: `typesafe/jev-1.13` via OpenRouter Decisions API
- Adapter models: OpenCode `yolo-auto/qwen3.8-flash`, Grok Build `grok-4.7`, Pi `yolo-auto/qwen3.8-flash`
- Loop context mode: explicit accumulated context; no session identifier was invented or reused

## Aggregate results

| Adapter | Mode | n | statuses | timeouts | work-match | outcomes | mean tools | mean Jev decisions | variance |
|---|---|---:|---|---:|---:|---|---:|---:|---|
| grok-build | baseline | 3 | timeout=3 | 3 | 0/3 | no=3 | 0 | 0 | not available (single repetition) |
| grok-build | jev-loop | 3 | fallback=2, timeout=1 | 1 | 0/3 | no=3 | 0 | 1.3 | not available (single repetition) |
| opencode | baseline | 3 | timeout=3 | 3 | 0/3 | no=3 | 0.3 | 0 | not available (single repetition) |
| opencode | jev-loop | 3 | fallback=2, timeout=1 | 1 | 0/3 | no=3 | 0.3 | 1.3 | not available (single repetition) |
| pi | baseline | 3 | fail_1=1, ok=1, timeout=1 | 1 | 0/3 | no=3 | 3.3 | 0 | not available (single repetition) |
| pi | jev-loop | 3 | fallback=2, timeout=1 | 1 | 0/3 | no=2, partial=1 | 6.7 | 1.3 | not available (single repetition) |

## Per-task observations

| Adapter | Hash | Mode | status | decisions | tools | work-match | outcome | actions | sessions observed |
|---|---|---|---|---:|---:|---:|---|---|---:|
| opencode | `0d6ca4607eaf` | baseline | timeout | 0 | 0 | no | no | disabled | 1 |
| opencode | `0d6ca4607eaf` | jev-loop | fallback | 1 | 0 | no | no | ESCALATE | 0 |
| opencode | `1a415bc257e5` | baseline | timeout | 0 | 0 | no | no | disabled | 1 |
| opencode | `1a415bc257e5` | jev-loop | fallback | 1 | 0 | no | no | ESCALATE | 0 |
| opencode | `28372e365066` | baseline | timeout | 0 | 1 | no | no | disabled | 1 |
| opencode | `28372e365066` | jev-loop | timeout | 2 | 1 | no | no | CLASSIFY_REQUEST, ESCALATE | 1 |
| grok-build | `0d6ca4607eaf` | baseline | timeout | 0 | 0 | no | no | disabled | 0 |
| grok-build | `0d6ca4607eaf` | jev-loop | fallback | 1 | 0 | no | no | ESCALATE | 0 |
| grok-build | `1a415bc257e5` | baseline | timeout | 0 | 0 | no | no | disabled | 0 |
| grok-build | `1a415bc257e5` | jev-loop | fallback | 1 | 0 | no | no | ESCALATE | 0 |
| grok-build | `28372e365066` | baseline | timeout | 0 | 0 | no | no | disabled | 0 |
| grok-build | `28372e365066` | jev-loop | timeout | 2 | 0 | no | no | CLASSIFY_REQUEST, ESCALATE | 0 |
| pi | `0d6ca4607eaf` | baseline | timeout | 0 | 0 | no | no | disabled | 0 |
| pi | `0d6ca4607eaf` | jev-loop | fallback | 1 | 0 | no | no | ESCALATE | 0 |
| pi | `1a415bc257e5` | baseline | fail_1 | 0 | 0 | no | no | disabled | 0 |
| pi | `1a415bc257e5` | jev-loop | fallback | 1 | 0 | no | no | ESCALATE | 0 |
| pi | `28372e365066` | baseline | ok | 0 | 10 | no | no | disabled | 0 |
| pi | `28372e365066` | jev-loop | timeout | 2 | 20 | no | partial | CLASSIFY_REQUEST, ESCALATE | 0 |

## Interpretation boundary

The recurring deviations are: 7/9 baseline arms timed out, 6/9 Jev arms
stopped before adapter execution for low selected-action confidence, and none
of the 18 arms reached a Work match. The three loop arms that did execute a
bounded step made two decisions each, but each ended in a timeout and no
Work-match evidence under the 15-second invocation bound. OpenCode emitted a
native session identifier; Grok Build and Pi did not emit one in these files.

This is the smallest v2 implementation slice. A single repetition does not
support a repeated-run variance claim; the report records that limitation
instead of treating task-to-task differences as variance evidence. Native
session identifiers are recorded only when emitted by an adapter. The loop
therefore uses explicit context replay, which is the documented fallback for
adapters whose continuation semantics are not yet proven.

Source run id: `jev-v2-matched-20260921`
