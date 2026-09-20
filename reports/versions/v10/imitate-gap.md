# Imitate gap (iteration 6 / v10)

v7–v9 stand. This slice: Work inspect is **exec**, not cwd shell. Global Kilo/OpenCode modes were stale (VS Code sandwich) and are now synced to the project Work modes.

## Work js vs shell

| | sessions | calls |
| --- | --- | --- |
| exec | 79/81 | 7345 |
| js | 5/81 (all also exec) | 81 |
| shell_command | **2/81** | 44 |
| shell + apply_patch | 1 | 2 |

js sits next to exec (js→js 58, exec→js 23). shell sits next to shell, and the patch session is in that slice.

Do not map Work gold to bash+edit.

## Copies

Kilo still fails R2/R5 (look then edit). OpenCode fails R6 (todo/task first) and R5. Modes now prefer Read/Grep/Glob; cwd shell is 2/85.

Global `~/.config/kilo/agent/codex.md` and `~/.config/opencode/agent/codex.md` copied from the project files this run (`research/sync_global_modes.py`).

## Still open

- Kilo has no JS notebook cell. Mapping is Read/Grep/Glob + wait.
- Owner decides match. Do not switch to SWE-bench.
