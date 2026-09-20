# Imitate gap (iteration 3 / v7)

Gold now: Work session **shapes**, not only tool totals. 85 `codex_work_desktop` sessions, calls only.

## v7 Work archetypes

| archetype | n | meaning |
| --- | --- | --- |
| exec_only | 33 | look burst, never write, never spawn |
| multi_agent | 27 | send_message(target) after look; spawn_agent in 2 |
| exec_wait | 16 | exec then wait(cell_id) |
| js | 4 | js cells mixed with exec |
| empty | 4 | no tool calls |
| patch | 1 | the rare shell↔apply_patch sandwich |

First call is never send_message (81/81). Median 15 tools before send. Median exec-run length 3.

## Modes updated

`.kilo/agent/codex.md` and `.opencode/agent/codex.md` now say: never Task as tool 1; default look-only; send/Task after the look burst; spawn is rare.

Scorer `src/score_session.py` now reports **R2 no-write** (Work write-rate 1/85).

## Kilo / OpenCode vs R2

See `reports/session-scores.md`.

| product | R1 look-first | R2 no-write | write-rate |
| --- | --- | --- | --- |
| Work gold | 81/81 not send-first | 84/85 | **0.01** |
| Kilo | 17/17 | **2/17** | **0.88** |
| OpenCode (not Study OS) | 23/24 | 11/24 | 0.54 |

Look-first is already strong. The remaining gap is **write-heaviness**.

## Still open

- Kilo has no JS notebook cell. Mapping is inspect tools + wait.
- Owner decides match. Do not switch to SWE-bench.
