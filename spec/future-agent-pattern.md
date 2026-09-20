# Portable pattern for future coding agents (from ChatGPT Work gold)

Copy these relations, not Codex tool names.

1. **Do not write first.** Work: 0/87 patch-first; 81 first=`exec` (calls).
2. **Burst look** (`exec → exec`).
3. **Wait on slow cells/tools** (31/87 have `wait`). After an exec-run, wait or send, never patch (apply_patch after exec-run **0**).
4. **Split multi-piece with named workers** (`send_message` in 25/87, median 2 sends, first at index 15; `spawn_agent` in 2/87). Between sends, look or wait; send+patch **0**. Never send/Task first. **Do not Todowrite** — Work `update_plan` is 0. Default session is look-only (exec_only 35/87).
5. **After failure, look again** (full-corpus: shell 446 vs patch 59).
6. **Prose is not truth.** Tool output is.

Kilo/OpenCode map: Read/Grep/Glob → look (Work cwd shell is 2/87; do not treat bash as exec). Edit/Write → patch; Task → send/spawn; wait for Task → wait_agent. js is rare (5/87) next to exec.

Score with `src/score_session.py`. Owner docs win on conflict (`spec/prompt-stack.md`).
