# Imitate gap (iteration 11 / v15)

v14 R4 stands. This slice: **R3 read-first**, not bash-first. Work first tool is exec 79 / shell 2.

## R3 live copies

| product | R1 | R3 read-first | bash-first |
| --- | --- | --- | --- |
| Work gold | 81/81 not patch | exec 79, shell 2 | shell 2 |
| Kilo | 17/17 | **15/17** | 1 |
| OpenCode | 23/24 | **5/24** | **10** |

OpenCode often starts with bash. Work almost never starts with cwd shell. Modes: do not bash as tool 1.

## Still open

Kilo R2/R4/R5. OpenCode R3/R4/R6. Owner decides match. Do not SWE-bench.
