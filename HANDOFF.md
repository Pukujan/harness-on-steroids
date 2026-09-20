# Handoff

**Owner wins:** `AGENTS.md` → `PLAN.md` → `ISSUES.md` → `CONTINUE.md`.

## 20h loop (now)

Until **2026-09-21T12:05:00Z** (then 48h deadline **2026-09-22T05:58:00Z**). 10-minute wakeup chain if paused. Do not SWE-bench. Do not wait.

## Current gold (do not average)

Primary: **ChatGPT Work** `codex_work_desktop` (**87** sessions). `apply_patch` in **1**. Multi-agent send/spawn **26**. After fail: shell 4, no patch. Hashed jsonl **1521**.

**v19 shapes:** exec_only **35**, multi_agent 27, exec_wait 16, patch 1. First call never send (83/83). Median 15 before send. spawn 2. Median exec burst 3.

**v20:** refreshed kilo.db. Sessions 20, work_match **1/20**. Mode patches did not lift the score; scored sessions are not the Codex agent.

**v21:** originator table on 1521 files. Work 95 metas / 87 tool sessions. vscode patch 718 unchanged.

**v22:** `codex-gold-behavior.md` regenerated on 1521. Do not average originators. 1518 snapshot in `reports/versions/v22/`.

**v23:** deep pass on 1521: js_cell **29231**, write-first-exec 1. Work still primary.

**v24:** 4/87 Work files have no tool calls (short threads). Originator 95 is session_meta rows.

**v25:** 95 = 79 files ×1 meta + 8 ×2. Modes: if nothing to look up, stop.

**v26:** originator table is one file once. Work **87**, Desktop 1103, vscode 16.

**v27:** `codex-gold-behavior.md` originator counts match files (Work 87), not session_meta rows.

**v28:** ISSUES 8–11 done. 12 open until owner says match (Kilo work_match 1/20).

**v29:** Kilo `/goal` selects the Codex agent (`agent: codex`), same as OpenCode.

**v30:** scorer skips plan-agent sessions. Kilo work_match 1/13. sqlite has `code`/`build`, not `codex` yet.

**v31:** originator first-tool is calls only. Work exec 81, shell 2.

**v32:** mixed-corpus first-tool calls only: exec 1131. create_thread-as-first was an output.

VS Code Codex (16) is shell↔patch — **not** Work gold.

Kilo/OpenCode **imitate** Work via `.kilo/agent/codex.md` and `.opencode/agent/codex.md`. Scorer: `src/score_session.py` (R1 look-first, **R2 no-write**, **R6 decompose-not-first**). Pattern: `spec/future-agent-pattern.md`.

**v8 gap:** Kilo write-rate 0.88 vs Work 0.01. OpenCode R6 16/24 (todowrite/task first). Never Todowrite as tool 1.

**v9:** After exec-run, Work wait 218 / send 53 / apply_patch **0**. Scorer R5. Kilo R5 **2/17**. After look burst, do not Edit next.

**v10:** Work cwd `shell_command` in **2/85**; js in 5 (next to exec). Prefer Read/Grep/Glob. Synced global Kilo/OpenCode `agent/codex.md` off the project files (they still had the vscode sandwich).

**v11:** wait-runs 222, 18/31 wait sessions cluster ≥2; after wait-run exec 211, never patch. You may wait more than once.

**v12:** send_message 25/85, median 2 sends, first at 15. spawn 2. send+patch 0. After last send, end 18. Between sends, look or wait.

**v13:** Work `update_plan` **0**, plan-mode **0**. Do not Todowrite. Full-corpus plan 137 is not Work.

**v14:** Scorer R4 no-todowrite. Kilo **7/17** (10 todowrite sessions). OpenCode 11/24. Todowrite no longer counts as multi_piece.

**v15:** R3 read-first not bash. Kilo 15/17. OpenCode **5/24** (bash-first 10). Do not bash as tool 1.

**v16:** work_match = R1∧R2∧R3∧R4∧R5∧R6. Kilo **1/17**, OpenCode **4/24**. Owner decides stop.

**v17:** Work self-score **79/81 (0.98)**. Scorer is the right exam. Copies should move toward 0.98.

**v18:** fail_mask. Kilo dominant **R2+R4+R5** (10/17). OpenCode **R3** (bash-first) stacked with todo/write.

Pytest owner-gate must stay green. Standing goal: `python -m src.goal_cli`. Do not shadow Kilo’s reserved `/goal`.

## Do not

Commit `data/` or bodies.
