# Imitate gap (iteration 8 / v12)

v7–v11 stand. This slice: Work **task split is repeated send_message**, not spawn.

## Send topology

25/85 sessions send. Median **2** sends, first at index **15**. spawn_agent **2**, both **1**. send+apply_patch **0**.

After last send: end **18**, exec 5, wait_agent 2. Between sends: exec-only **26**, wait 11, wait_agent 6.

Spec “How Codex splits tasks” now follows Work, not the mixed-corpus spawn story.

## Still open

Kilo R2/R5 look-then-edit. OpenCode R6 todo-first. Owner decides match. Do not SWE-bench.
