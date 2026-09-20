# v12 — send_message task split

`codex-work-send.md`: Work multi-piece is repeated send_message (25 sessions, median 2 sends, first at index 15). spawn_agent is 2. send+apply_patch is 0. After last send, end 18 / exec 5. Between sends: exec-only 26.

Corrects mixed-corpus “spawn then wait_agent” as the Work split story.
