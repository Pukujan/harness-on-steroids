# Matched controller replay — 2026-09-21

This is a sanitized, hash-only report from the first-turn Work replay slice. It compares each hosted adapter with controller hints disabled and enabled. The runner records observable tool events and R1–R6/work-match outcomes; it does not copy prompts, message bodies, or CLI event bodies into this report.

## Frozen slice

- Work hashes: `0d6ca4607eaf`, `1a415bc257e5`, `28372e365066`
- Adapters: OpenCode + Qwen Flash, Grok Build + grok-4.7, Pi + Qwen Flash
- Modes: baseline and Jev hint
- Jev route: OpenRouter Decisions API only
- Per-arm timeout: 75 seconds
- Replay input: first stored user turn for each existing develop Work hash

## Aggregate results

| Adapter | Mode | n | ok / partial / timeout / fail | work-match | outcomes | mean tools | fail masks |
|---|---:|---:|---|---:|---|---:|---|
| opencode | baseline | 3 | 3 / 0 / 0 / 0 | 0/3 (0%) | no=3 | 0.0 | empty=3 |
| opencode | jev | 3 | 0 / 0 / 3 / 0 | 3/3 (100%) | partial=3 | 9.7 | none=3 |
| grok-build | baseline | 3 | 0 / 1 / 2 / 0 | 0/3 (0%) | no=3 | 0.0 | empty=3 |
| grok-build | jev | 3 | 0 / 2 / 1 / 0 | 0/3 (0%) | no=3 | 0.0 | empty=3 |
| pi | baseline | 3 | 2 / 0 / 0 / 1 | 0/3 (0%) | no=3 | 0.0 | empty=3 |
| pi | jev | 3 | 1 / 0 / 1 / 1 | 0/3 (0%) | no=2, partial=1 | 45.3 | R3=2, empty=1 |

## Per-task observations

| Adapter | Hash | Baseline status/tools | Jev status/tools | Jev action | Jev match |
|---|---|---:|---:|---|---:|
| opencode | `0d6ca4607eaf` | ok/0 | timeout/11 | INSPECT_TASK_STATE | yes |
| opencode | `1a415bc257e5` | ok/0 | timeout/5 | INSPECT_REPO | yes |
| opencode | `28372e365066` | ok/0 | timeout/13 | INSPECT_REPO | yes |
| grok-build | `0d6ca4607eaf` | timeout/0 | timeout/0 | INSPECT_TASK_STATE | no |
| grok-build | `1a415bc257e5` | timeout/0 | partial/0 | INSPECT_REPO | no |
| grok-build | `28372e365066` | partial/0 | partial/0 | INSPECT_REPO | no |
| pi | `0d6ca4607eaf` | ok/0 | ok/38 | INSPECT_TASK_STATE | no |
| pi | `1a415bc257e5` | fail_1/0 | fail_1/0 | INSPECT_TASK_STATE | no |
| pi | `28372e365066` | ok/0 | timeout/98 | INSPECT_REPO | no |

## Interpretation

On this three-task slice, the Jev hint increased observable tool activity for OpenCode and Pi. OpenCode reached a work-match on all three tasks before the timeout, while its baseline arm produced no parsed tool calls. Pi produced activity on two Jev tasks but also timed out on one and did not reach a work-match. Grok Build did not produce parsed tool calls within this slice, so the result is an adapter or timeout investigation signal rather than evidence about Grok quality.

These are pilot observations, not a controller verdict. The next useful step is to fix or confirm the Grok event adapter, then expand the same frozen manifest before changing prompts or adding state-machine enforcement.

## Source run IDs

- `replay-grok-3-20260921`
- `replay-opencode-3-20260921`
- `replay-pi-3-20260921`
