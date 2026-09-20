# Handoff

**Owner wins:** `AGENTS.md` → `PLAN.md` → `ISSUES.md` → `CONTINUE.md`.

## 20h loop (now)

Until **2026-09-21T12:05:00Z** (then 48h deadline **2026-09-22T05:58:00Z**). 10-minute wakeup chain if paused. Do not SWE-bench. Do not wait.

## Current gold (do not average)

Primary: **ChatGPT Work** `codex_work_desktop` (85 sessions). First tool `exec` 76. `apply_patch` in **1** session. Multi-agent send/spawn **26**. After fail: shell 4, no patch.

**v7 shapes** (`reports/codex-work-shapes.md`): exec_only 33, multi_agent 27, exec_wait 16, patch 1. First call never send. Median 15 tools before `send_message(target, message)`. spawn_agent in **2** sessions. Median exec burst 3.

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

Pytest owner-gate must stay green. Standing goal: `python -m src.goal_cli`. Do not shadow Kilo’s reserved `/goal`.

## Do not

Commit `data/` or bodies.
