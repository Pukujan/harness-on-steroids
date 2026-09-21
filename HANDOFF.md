# Handoff

**Owner wins:** `AGENTS.md` → `PLAN.md` → `ISSUES.md` → `CONTINUE.md`.

## 20h loop (now)

Until **2026-09-21T12:05:00Z** (then 48h deadline **2026-09-22T05:58:00Z**). 10-minute wakeup chain if paused. Do not SWE-bench. Do not wait.

## Current gold (do not average)

One-pager: `reports/codex-originator-dashboard.md`.

Primary: **ChatGPT Work** `codex_work_desktop` (**87** files / **83** with calls). Patch **1/83**, wait **31/83**, send **25**, spawn 2, `update_plan` **0**. First call exec 81 / shell 2. Never send first (83/83).

Do not imitate vscode (12/13 patch, 0 wait, 0 send) or nonempty `codex_exec` (31/105 patch, 11 plan). Desktop patch 1/994 — not the sandwich.

Hashed jsonl **1521**. Versions: `reports/versions/v7`–`v56`. Spec: `spec/codex-imitate-mode.md`. Modes: `.kilo/agent/codex.md`, `.opencode/agent/codex.md`. Scorer: `src/score_session.py`. Issue 12: process. Issue **13**: **22 long Work threads** (not 8 singles) + morphs; score vs Work execution. `/goal` in `spec/matched-task-goal.md`. Replay of 22 not complete.

Pytest owner-gate must stay green. Standing goal: `python -m src.goal_cli`. Do not shadow Kilo’s reserved `/goal`.

## Do not

Commit `data/` or bodies.

## Content-system preview — branch-local

- branch: `task/TASK-0015-content-system-preview`
- helper: `content-generation-modules` v0.1.2 at commit `cb8c18fa7789e4b651e1f963892bf056b0d3276d`
- review files: `docs/content-system-preview.md`, `docs/content-system-preview.html`
- generated assets: `docs/content-system-assets/hero.png`, `docs/content-system-assets/supporting-square.png`
- visual rule: narrative raster assets carry one short title and subtitle; SVGs and tiny helper graphics remain text-free
- validation: responsive desktop/tablet/mobile screenshots and PDF packet rendered locally; canonical README remains unchanged
- next action: inspect the preview PR before deciding whether any README or documentation promotion is warranted
