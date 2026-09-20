# fail_mask for coding agents

v56. Kilo `code`, OpenCode `build`. Skip study-os. No bodies.

## kilo.db agent=code

| fail_mask | n |
| --- | --- |
| R2+R4+R5 | 5 |
| R2+R5 | 4 |
| R2+R3+R4+R5+R6 | 1 |
| R3+R6 | 1 |
| none | 1 |
| R2+R3+R5 | 1 |

## opencode.db agent=build

| fail_mask | n |
| --- | --- |
| R2+R3+R4+R5 | 6 |
| R3 | 3 |
| none | 3 |
| R2+R3+R4+R5+R6 | 3 |
| R3+R6 | 1 |
| R2+R3+R6 | 1 |
| R2+R3+R5 | 1 |
| R2+R4+R5 | 1 |

## interpretation

Coding copies still fail R2+R4+R5 (write + todowrite after look) and OpenCode R3 (bash-first).
