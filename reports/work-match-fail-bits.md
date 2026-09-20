# Work-match fail bits (v18)

Which R1–R6 bits kill `work_match`. No bodies.

Work self-score 79/81. Kilo 1/17. OpenCode 4/24.

## kilo.db

Dominant mask **R2+R4+R5** (10/17): look, then Todowrite, then edit.

| fail_mask | n |
| --- | --- |
| R2+R4+R5 | 10 |
| R2+R5 | 4 |
| R3+R6 | 1 |
| none | 1 |
| R2+R3+R5 | 1 |

## opencode.db

Bash-first (R3) is in almost every fail. Todowrite (R4) and write (R2) stack on top.

| fail_mask | n |
| --- | --- |
| R2+R3+R4+R5 | 6 |
| none | 4 |
| R3 | 3 |
| R2+R3+R4+R5+R6 | 3 |
| R3+R4+R6 | 3 |

Patch the copies toward: no Todowrite, no edit after a look burst, no bash as tool 1. Modes already say that. New sessions must use the updated Codex mode.
