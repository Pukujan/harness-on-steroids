# Handoff

**Owner wins:** `AGENTS.md` → `PLAN.md` → `ISSUES.md` → `CONTINUE.md`.

## 20h loop (now)

**20h floor elapsed** 2026-09-21T12:05Z (`reports/20h-floor-gaps.md`). Not complete. Keep 48h until **2026-09-22T05:58:00Z**. Restore 10-minute wakeups if paused. Do not SWE-bench. Do not wait.

That no-stop is after `/goal` + go-ahead. Ordinary chat answers first and seeks go-ahead.

## /goal paste

`spec/matched-task-goal.md` (updated v65 next-queue). Kilo reserved `/goal`: paste into Set goal after reload. Do **not** add `.kilo/command/goal.md`. CLI: `python -m src.goal_cli status`.

## Queued in PLAN (not started)

G–I: Work research/planning/provenance counts, git checkpoints, portable pack. Spec: `spec/work-research-gates.md`. Issues 14–17.
Research note: `research/work-ux-gaps.md`. Module map: `spec/repo-modules.md`. Combined `/goal` (not started): `spec/combined-slices-goal.md`. Issue 18: lint/types/layout.

## Next slice (issue 13 stop-when notes present)

`reports/replay-scores.md` has develop 16 Kilo+OpenCode cells, holdout 6 OpenCode one-turn cells, morph ≥3. Morph *replays with tools*: `0d6ca4607eaf`, `2bde00530ddd`, `6e412585c223`. No Codex mode edits for holdout. Full original-cwd multi-turn still not done. Issues 14–18 remain queued. Do not start `spec/combined-slices-goal.md` unless the owner pastes it.

Owner can extend: extra `-c` turns, original worktrees, holdout morphs. Do not treat one-turn sandbox scores as full Work outcome match.

Gitignored `.env` has OpenRouter/Zen keys; do not commit it.

## Current gold (do not average)

One-pager: `reports/codex-originator-dashboard.md`.

Primary: **ChatGPT Work** `codex_work_desktop` (**87** files / **83** with calls). Patch **1/83**, wait **31/83**, send **25**, spawn 2, `update_plan` **0**. First call exec 81 / shell 2. Never send first (83/83).

Do not imitate vscode (12/13 patch, 0 wait, 0 send) or nonempty `codex_exec` (31/105 patch, 11 plan). Desktop patch 1/994 — not the sandwich.

Hashed jsonl **1521**. Spec: `spec/codex-imitate-mode.md`. Modes: `.kilo/agent/codex.md`, `.opencode/agent/codex.md`. Issue 12 process; issue 13 matched-task **not complete**.

Pytest owner-gate must stay green.

## Do not

Commit `data/` or bodies. Print `user.md`. Bundle long OpenCode runs in one tool call.

## Content-system preview

- helper: `content-generation-modules` v0.1.2 at commit `cb8c18fa7789e4b651e1f963892bf056b0d3276d`
- review files: `docs/content-system-preview.md`, `docs/content-system-preview.html`
- generated assets: `docs/content-system-assets/hero.png`, `docs/content-system-assets/supporting-square.png`
- visual rule: narrative raster assets carry one short title and subtitle; SVGs and tiny helper graphics remain text-free
- merged via PR #1. Read `.content-system/` before changing README, marketing, UX, image, or HTML content.
