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

Pytest owner-gate must stay green. Standing goal: `python -m src.goal_cli`. Do not shadow Kilo’s reserved `/goal`.

## Do not

Commit `data/` or bodies.
