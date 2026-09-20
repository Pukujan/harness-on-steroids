# Codex-imitate mode spec

Source: `reports/codex-originator-dashboard.md`, `reports/codex-gold-behavior.md`, `reports/codex-work-shapes.md`. Hashed corpus **1521** files. Not SWE-bench papers.

Kilo and OpenCode both ship a selectable **codex** agent. Same states. Do not pin a model (current Kilo model / OpenCode free build mode).

**Primary gold slice is `codex_work_desktop` (ChatGPT Work),** 87 sessions (hashed corpus 1521). `apply_patch` in **1** session. Multi-agent send/spawn **26**. The shell↔patch sandwich is **VS Code** Codex (n=16) plus nonempty **`codex_exec` (31/105 patch)**. Codex Desktop patch is **1/994** nonempty files — do not treat Desktop as the sandwich. Do not let those minorities overwrite Work.

| originator | patch | wait | send | update_plan | cwd shell |
| --- | --- | --- | --- | --- | --- |
| Work | **1/83** | **31/83** | **25** | **0** | **2** |
| Desktop | **1/994** | 88/994 | 17 | 2 | 4 |
| `codex_exec` | **31/105** | 16/105 | 0 | 11 | **45** |
| vscode | **12/13** | **0/13** | **0** | 6 | **13** |

**v19 session shapes** (`reports/codex-work-shapes.md`, calls only): exclusive archetypes exec_only **35**, multi_agent **27**, exec_wait **16**, js **4**, empty **4**, patch **1**. First call is never `send_message` (83/83). Median **15** tools before first send, **3** consecutive execs per burst. Multi-piece is `send_message(target, message)` (25 sessions). `spawn_agent` is **2** sessions.

## What gold actually does

| Fact | Count |
| --- | --- |
| First tool `exec` | 1125 sessions |
| First tool `apply_patch` | **0** |
| `exec` calls | 30373 |
| of those, JS source prefix | **30044** |
| `shell_command` (command+workdir+timeout) | 8743 |
| `wait` with `cell_id` | ~3500 / 3538 |
| `apply_patch` | 967 |
| `js` tool (`code`,`title`) | 283 |
| `spawn_agent` (`task_name`,`fork_turns`,`message`) | 47 |
| `update_plan` (`plan`) | 137 full corpus; **Work 0** |
| Plan collaboration_mode vs default | 54 vs 6820 full corpus; **Work plan-mode sessions 0** |

Dominant chains: `exec → exec → exec` (26809 exec-exec pairs), `exec → wait → exec`, `shell_command → apply_patch → shell_command`, `spawn_agent → wait_agent`.

**Gold loop:** run a **code cell** (`exec` JS, or `js`), **wait on that cell**, repeat. Real filesystem shell is `shell_command` with workdir (Work: 2/87). Edits are rare. Multi-piece work: **repeated `send_message(target, message)`** after a look burst. `spawn_agent` is 2/87. Do not spawn for a one-file look.

## How Codex splits tasks (Work)

1. Most sessions never send or spawn. They stay on exec bursts (exec_only 35/87).
2. Multi-piece: `send_message` in **25/87**, median **2** sends, first send at median index **15**. `spawn_agent` in **2**. Both in **1**. send+apply_patch **0**.
3. Between consecutive sends: exec-only **26**, wait **11**, wait_agent **6**, adjacent **2**. Never patch.
4. After last send: **end 18**, exec 5, wait_agent 2. Often stop. `wait_agent` sessions **4**; `list_agents` **4**.

## Required states (both products)

1. **Look first.** Never Edit/Write as tool 1.
2. **Burst look.** Several observe calls (Read/Grep/Glob/inspect bash) like gold `exec → exec`.
3. **Wait on slow work.** After a long command or child: wait for the result (`wait`/`cell_id`, `wait_agent`). Do not pile more writes. After an exec/look burst, Work next tool is wait **218** / send **53** / end **57** / js **23** / apply_patch **0**. Wait-runs: 222, median 1, but **18/31** wait sessions cluster ≥2; after a wait-run next is exec **211**, never patch.
4. **If you write, look again.** Work apply_patch is 1/87. The `apply_patch → shell_command` sandwich is vscode (n=16), not Work default.
5. **Split only if multi-piece.** After a look burst, Task / send to a **named target**. Do not Todowrite — Work `update_plan` is **0**. One slice does not spawn. Never Task as tool 1. Never Todowrite as tool 1. `spawn_agent` is rare (2/87).
6. **After a failed command, look again.** Full corpus: `shell_command` 446 vs `apply_patch` 59. **Work-only:** 5 fails, next tool `shell_command` 4, **no patch**. Do not immediately write more.
7. **Do not plan-file first.** Work: `update_plan` **0**, `request_user_input` **0**, collaboration_mode=plan **0**. Mixed-corpus plan-mode also has zero `apply_patch` — still not Work default.
8. **Prose is not truth.** Tool output is.
9. **Same states in Kilo and OpenCode.**

## Mapping

| Codex gold | Kilo / OpenCode |
| --- | --- |
| exec JS cell + wait(cell_id) | Read/Grep/Glob then **wait for the tool**; do not spam. Work cwd shell is 2/87. |
| js (code,title) | rare (5/87); sits next to exec |
| shell_command + workdir | bash only when a real cwd command is required |
| apply_patch | edit / write |
| update_plan | **not Work** (0 calls). Do not Todowrite to imitate Work. |
| spawn_agent + task_name | task |
| wait_agent | wait for Task result |

## Forbidden

- Do not patch first
- Skip post-edit look
- Treat a public exam as gold
- Claim done without a tool result
