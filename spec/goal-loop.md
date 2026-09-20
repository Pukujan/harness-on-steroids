# /goal loop spec (implemented)

Engine: `src/goal_loop.py`. CLI: `python -m src.goal_cli`. Tests: `tests/test_goal_loop.py`.

Semantics from Codex CLI 0.128.0 and Hermes Persistent Goals. The Python engine is for tests and CLI ticks. It is **not** Kilo's slash command.

## Prove it works

```
python -m pytest tests/test_goal_loop.py -q
```

Includes a live fake agent that writes four files until a shell gate passes.

## Wire

Kilo already ships a **reserved** `/goal` (pause / resume / clear). Do **not** add `.kilo/command/goal.md` or a global `command/goal.md` — that shadows the product command and can 500. Use Kilo's `/goal` in chat. Use `python -m src.goal_cli` only for the local test engine.
