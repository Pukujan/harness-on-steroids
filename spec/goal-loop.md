# /goal loop spec (implemented)

Engine: `src/goal_loop.py`. CLI: `python -m src.goal_cli`. Tests: `tests/test_goal_loop.py`.

Semantics from Codex CLI 0.128.0 and Hermes Persistent Goals. Kilo has no native judge; this process is the loop.

## Prove it works

```
python -m pytest tests/test_goal_loop.py -q
```

Includes a live fake agent that writes four files until a shell gate passes.

## Wire

`/goal` command in `.kilo/command/goal.md` tells the agent to `set` then `tick` after each slice.
