# Work-gold process relations (measurable)

From `reports/codex-work-desktop-only.md` (87 ChatGPT Work sessions). Not VS Code.

| ID | Relation | Gold on Work |
| --- | --- | --- |
| R1 | First named tool is not apply_patch / edit / write | 0/87 patch-first; 81 first=`exec` |
| R2 | apply_patch is rare | 1/87 sessions |
| R3 | First look is exec/read, not cwd shell | Work first exec 79, shell **2**; exec→exec 6998 |
| R4 | Multi-piece uses send, not a plan list or extra patch | send 25/87; `update_plan` **0**; send+patch **0** |
| R5 | Wait after cells; do not patch at end of a look burst | 31/87 have `wait`; apply_patch after exec-run **0** |
| R6 | send/Task never first; look burst first | 81/81 first call ≠ send_message; median 15 tools before send |
| R2b | Most sessions never write | exec_only 35/87; apply_patch 1/87 |

A Kilo/OpenCode session **matches** if: first tool is observe (read/grep/glob/inspect bash/skill), zero write as tool 1, and if it writes it looks again after. It **fails** if first tool is edit/write/patch. **R2** (scorer `r2_no_write`): Work write-rate is 1/87; a session that never edits matches. **R5** (scorer `r5_no_write_after_look_run`): a look-run is not followed by edit/write/patch. **R3** (scorer `r3_read_first`): first tool is read/grep/glob/skill/recall, not bash. **R4** (scorer `r4_no_todowrite`): session has no todowrite (Work `update_plan` 0). **R6** (scorer `r6_decompose_not_first`): first tool is not task/todowrite/agent_manager.

**Work-match:** R1 ∧ R2 ∧ R3 ∧ R4 ∧ R5 ∧ R6 (`score_seq()["work_match"]`). Owner still decides stop. Do not score Study-OS OpenCode sessions as coding gold.
