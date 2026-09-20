# Work-gold process relations (measurable)

From `reports/codex-work-desktop-only.md` (85 ChatGPT Work sessions). Not VS Code.

| ID | Relation | Gold on Work |
| --- | --- | --- |
| R1 | First named tool is not apply_patch / edit / write | 0/85 patch-first; 76/81 first=`exec` |
| R2 | apply_patch is rare | 1/85 sessions |
| R3 | Observe bursts exist | exec→exec 6998 |
| R4 | Multi-piece uses send/spawn, not extra patch | 26/85 send or spawn |
| R5 | Wait after cells | 31/85 have `wait` |
| R6 | send/Task never first; look burst first | 81/81 first call ≠ send_message; median 15 tools before send |
| R2b | Most sessions never write | exec_only 33/85; apply_patch 1/85 |

A Kilo/OpenCode session **matches** if: first tool is observe (read/grep/glob/inspect bash/skill), zero write as tool 1, and if it writes it looks again after. It **fails** if first tool is edit/write/patch. **R2** (scorer `r2_no_write`): Work write-rate is 1/85; a session that never edits matches.

Do not score Study-OS OpenCode sessions as coding gold.
