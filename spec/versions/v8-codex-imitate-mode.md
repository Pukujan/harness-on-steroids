# Codex-imitate mode spec

Source: `reports/codex-gold-behavior.md`, `reports/codex-exec-shape.md`, `reports/codex-exec-prefix.md`, `reports/codex-itemtype-shapes.md`. Full hashed corpus (1518 files). Not SWE-bench papers.

Kilo and OpenCode both ship a selectable **codex** agent. Same states. Do not pin a model (current Kilo model / OpenCode free build mode).

**Primary gold slice is `codex_work_desktop` (ChatGPT Work),** 85 sessions with tools: first tool `exec` 76, `apply_patch` in **1** session (2 calls), multi-agent send/spawn in **26**. Chains: `exec → exec` (6998), `exec → wait`, `exec → send_message`. VS Code Codex (n=16) is the shell↔patch sandwich; do not let that minority overwrite Work.

**v7 session shapes** (`reports/codex-work-shapes.md`, calls only): exclusive archetypes exec_only **33**, multi_agent **27**, exec_wait **16**, js **4**, empty **4**, patch **1**. First call is never `send_message` (81/81). Median **15** tools before first send, **3** consecutive execs per burst. Multi-piece is `send_message(target, message)` (70 calls / 25 sessions). `spawn_agent` is **2** sessions.

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
| `update_plan` (`plan`) | 137 |
| Plan collaboration_mode vs default | 54 vs 6820 |

Dominant chains: `exec → exec → exec` (26809 exec-exec pairs), `exec → wait → exec`, `shell_command → apply_patch → shell_command`, `spawn_agent → wait_agent`.

**Gold loop:** run a **code cell** (`exec` JS, or `js`), **wait on that cell**, repeat. Real filesystem shell is `shell_command` with workdir. Edits are `apply_patch` **between** shells. Multi-piece work: `update_plan` then `spawn_agent` then `wait_agent` / `send_message`. Do not spawn for a one-file look.

## How Codex splits tasks

1. Most sessions never spawn. They stay on exec/shell bursts.
2. When they do: `exec → spawn_agent` (task_name + message + optional model) → `wait_agent`.
3. Parallel workers: `send_message`, `list_agents`, `followup_task`, `interrupt_agent`.
4. Plan text is `update_plan.plan`, often next to `shell_command`, not a separate Plan-mode session.

## Required states (both products)

1. **Look first.** Never Edit/Write as tool 1.
2. **Burst look.** Several observe calls (Read/Grep/Glob/inspect bash) like gold `exec → exec`.
3. **Wait on slow work.** After a long command or child: wait for the result (`wait`/`cell_id`, `wait_agent`). Do not pile more writes.
4. **Sandwich edits.** After every write, look again (`apply_patch → shell_command`).
5. **Split only if multi-piece.** After a look burst, Todowrite / Task / send to a **named target**. One slice does not spawn. Never Task as tool 1. Never Todowrite as tool 1. `spawn_agent` is rare (2/85).
6. **After a failed command, look again.** Full corpus: `shell_command` 446 vs `apply_patch` 59. **Work-only:** 5 fails, next tool `shell_command` 4, **no patch**. Do not immediately write more.
7. **Plan-like turns do not patch.** Plan-mode tool mix is exec/wait/shell/`request_user_input` — **zero** `apply_patch` in that slice.
8. **Prose is not truth.** Tool output is.
9. **Same states in Kilo and OpenCode.**

## Mapping

| Codex gold | Kilo / OpenCode |
| --- | --- |
| exec JS cell + wait(cell_id) | bash/read/grep then **wait for the tool**; do not spam |
| shell_command + workdir | bash (inspect or test) |
| apply_patch | edit / write |
| update_plan | todowrite |
| spawn_agent + task_name | task |
| wait_agent | wait for Task result |
| js (code,title) | bash or a small script; still look first |

## Forbidden

- Do not patch first
- Skip post-edit look
- Treat a public exam as gold
- Claim done without a tool result
