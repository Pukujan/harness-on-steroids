---
description: Standing /goal loop (Codex/Hermes). Set, tick, gates. Does not stop until done or budget.
agent: codex
---

This is the harness-on-steroids goal engine, not a one-shot prompt.

CLI (from repo root):

- `python -m src.goal_cli set "OBJECTIVE"`
- `python -m src.goal_cli gate "pytest tests/test_goal_loop.py -q"`
- After each of your turns: write a short result, then `python -m src.goal_cli tick --response "..." `
- Exit code 10 = continue (do the printed prompt). 0 = stop (done/paused/blocked).
- `python -m src.goal_cli status|pause|resume|clear`

Rules: look first (codex mode). Gates run before “done”. Do not claim done if a gate is red. Budget 20 then pause.

If the user typed `/goal ...` with text, treat that text as `set`. Then work one slice, tick, and if continue keep going in this turn until tick says stop or you hit a real block.
