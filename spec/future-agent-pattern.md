# Portable pattern for future coding agents (from ChatGPT Work gold)

Copy these relations, not Codex tool names.

1. **Do not write first.** Work: 0/85 patch-first; 76 first=`exec`.
2. **Burst look** (`exec → exec`).
3. **Wait on slow cells/tools** (31/85 have `wait`). After an exec-run, wait or send, never patch (apply_patch after exec-run **0**).
4. **Split multi-piece with named workers** (`send_message(target, message)` after a look burst; `spawn_agent` in 2/85), not extra patches (`apply_patch` in 1/85). Never send/Task first. Default session is look-only (exec_only 33/85).
5. **After failure, look again** (full-corpus: shell 446 vs patch 59).
6. **Prose is not truth.** Tool output is.

Kilo/OpenCode map: Read/Grep/Glob → look (Work cwd shell is 2/85; do not treat bash as exec). Edit/Write → patch; Task → send/spawn; wait for Task → wait_agent. js is rare (5/85) next to exec.

Score with `src/score_session.py`. Owner docs win on conflict (`spec/prompt-stack.md`).
