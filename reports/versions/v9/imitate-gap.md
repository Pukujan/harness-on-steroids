# Imitate gap (iteration 5 / v9)

v7 shapes and v8 R6 stand. This slice: **after an exec-run, Work never patches**.

## Work wait insertion

361 exec-runs, median length 3. Next tool: wait **218**, end 57, send_message **53**, js 23, apply_patch **0**.

wait clusters: wait→wait 235, exec→wait 218, wait→exec 211.

## R5 vs copies

| product | R1 | R2 | R5 no-write-after-look-run | R6 |
| --- | --- | --- | --- | --- |
| Work gold | 81/81 | 84/85 | exec-run→patch **0** | 81/81 |
| Kilo | 17/17 | 2/17 | **2/17** | 16/17 |
| OpenCode (not Study OS) | 23/24 | 11/24 | **12/24** | 16/24 |

Kilo looks, then **edits**. Work looks, then **waits or sends**. Modes now: after a look burst, wait or Task/send or stop — do not Edit as the next tool.

## Still open

- Kilo has no JS notebook cell. Mapping is inspect tools + wait.
- Owner decides match. Do not switch to SWE-bench.
