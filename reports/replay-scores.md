# Replay scores (hashes only)

v65. Work process from JSONL. OpenCode cells from gitignored ndjson copies. Kilo cells kept. No bodies.

## develop (16)

| hash12 | work_match | fail_mask | kilo | opencode | morph |
| --- | --- | --- | --- | --- | --- |
| 0d6ca4607eaf | yes | none | yes/none/partial | no/R2+R4+R5/partial | yes |
| 1a415bc257e5 | yes | none | yes/none/partial | yes/none/partial | yes |
| 1b09f49da9b9 | no | R3 | yes/none/yes | no/R3/partial | yes |
| 28372e365066 | yes | none | yes/none/partial | no/R3/no | yes |
| 2bde00530ddd | yes | none | yes/none/partial | no/R4/partial | yes |
| 633c140546c0 | yes | none | yes/none/partial | yes/none/partial | yes |
| 6b1cd28c4803 | yes | none | yes/none/yes | no/R2+R5/partial | yes |
| 6e412585c223 | yes | none | yes/none/yes | yes/none/partial | yes |
| 6eb8631b71ff | yes | none | no/R2+R5/partial | yes/none/partial | yes |
| 74841f3cc419 | yes | none | yes/none/partial | yes/none/partial | yes |
| 76b12d5e1a66 | yes | none | yes/none/yes | no/R4/partial | yes |
| 8d42bc26b8ea | yes | none | yes/none/no | no/R2+R5/partial | yes |
| a5842562d1c9 | yes | none | yes/none/partial | no/R2+R5/partial | yes |
| b7e6393f4c14 | yes | none | yes/none/yes | no/R2+R5/partial | yes |
| bd179678f540 | yes | none | yes/none/partial | yes/none/partial | yes |
| f37de8488162 | yes | none | yes/none/partial | no/R3/partial | yes |

## holdout (6)

| hash12 | work_match | fail_mask | kilo | opencode | morph |
| --- | --- | --- | --- | --- | --- |
| 0aecd1eabdf2 | yes | none | no/R2+R5/yes | no/R2+R3+R5/partial | pending |
| 1442d08cf2d3 | yes | none | yes/none/yes | no/R2+R4+R5/partial | pending |
| 3a749176fae1 | yes | none | yes/none/yes | yes/none/partial | pending |
| 45ca341b6f6c | yes | none | yes/none/partial | no/R2+R5/partial | pending |
| 555f9c94ba8e | yes | none | yes/none/partial | no/R2+R3+R5/partial | pending |
| 55fd1ef9b613 | yes | none | yes/none/yes | no/R4/partial | pending |

Kilo and OpenCode live replay of these threads is **not done**.

## OpenCode cells that are prompt-contaminated (v66)

The OpenCode column above was produced by a runner that sent the raw first user
turn. For the hashes below that turn was the `<recommended_plugins>` /
`<environment_context>` preamble only, so **the OpenCode cell was earned with no
owner ask in the prompt** (extra `-c` turns may have added a real ask later in the
thread, which is why some cells still look healthy). Those cells describe how the
harness behaves on a task-free prompt, not how it imitates Work on that ask.

Affected (11 of 22): `0d6ca4607eaf`, `28372e365066`, `2bde00530ddd`, `6e412585c223`,
`8d42bc26b8ea`, `b7e6393f4c14`, `bd179678f540`, `f37de8488162`, `1442d08cf2d3`,
`555f9c94ba8e`, `55fd1ef9b613`.

Rows are left as-is because `tests/test_replay_scores.py` pins them as a CI contract
and gate tests are not deleted to hide a defect. The Work and Kilo columns are
unaffected (Work is scored from its own JSONL; Kilo cells come from sqlite copies).
Re-run these 11 OpenCode replays with the fixed runner before quoting the column as
issue 13 evidence.
