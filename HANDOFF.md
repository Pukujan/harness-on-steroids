# Handoff

**Owner wins:** `AGENTS.md` → `PLAN.md` → `ISSUES.md` → `CONTINUE.md`.

## 20h loop (now)

Until **2026-09-21T12:05:00Z** (then 48h deadline **2026-09-22T05:58:00Z**). 10-minute wakeup chain if paused. Do not SWE-bench. Do not wait.

## Current gold (do not average)

Primary: **ChatGPT Work** `codex_work_desktop` (85 sessions). First tool `exec` 76. `apply_patch` in **1** session. Multi-agent send/spawn **26**. After fail: shell 4, no patch.

VS Code Codex (16) is shell↔patch — **not** Work gold.

Kilo/OpenCode **imitate** Work via `.kilo/agent/codex.md` and `.opencode/agent/codex.md`. Scorer: `src/score_session.py`. Pattern: `spec/future-agent-pattern.md`.

Pytest owner-gate must stay green. Standing goal: `python -m src.goal_cli`. Do not shadow Kilo’s reserved `/goal`.

## Do not

Commit `data/` or bodies.
