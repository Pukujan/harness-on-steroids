# ChatGPT Work session shapes (`codex_work_desktop`)

Keys and counts only. No bodies. v7 interpretation.

Sessions: **87** (empty: **4**)
- send_message sessions: **25**
- spawn_agent sessions: **2**
- wait sessions: **31**
- apply_patch sessions: **1**
- first tool is not send_message: **83** / 83
- median tools/session: **23**
- median consecutive exec-run: **3**
- median tools before first send_message: **15**
- median tools before first wait: **10**
- median tools before first decompose: **12**
First-tool counts are **calls only** (`custom_tool_call` / `function_call`), not outputs.

## exclusive archetype

| archetype | sessions |
| --- | --- |
| exec_only | 35 |
| multi_agent | 27 |
| exec_wait | 16 |
| js | 4 |
| empty | 4 |
| patch | 1 |

Priority: patch > multi_agent > js > exec_wait > shell > exec_only.
multi_agent = send_message / spawn_agent / create_thread / followup / thread.

## first tool

| tool | sessions |
| --- | --- |
| exec | 81 |
| shell_command | 2 |

## first decompose tool

| tool | sessions |
| --- | --- |
| send_message | 23 |
| spawn_agent | 2 |
| multi_agent_v1 | 1 |
| list_agents | 1 |

## collapsed shapes (top 20)

| shape | sessions |
| --- | --- |
| exec | 35 |
| exec → wait → exec → wait → exec → wait → exec → wait | 9 |
| exec → wait → exec | 4 |
| exec → send_message → exec → send_message → exec → send_message → exec → send_message | 3 |
| exec → send_message → exec → send_message | 3 |
| exec → send_message → exec | 3 |
| exec → wait → exec → wait → exec → send_message | 2 |
| exec → js → exec → wait → exec → wait → exec → wait | 2 |
| exec → wait → exec → wait → exec → wait → exec | 2 |
| exec → js → exec → js → exec → js → exec → js | 2 |
| exec → wait → exec → wait → exec → wait → send_message → wait | 2 |
| exec → wait → exec → wait → exec | 2 |
| exec → send_message → exec → send_message → exec → wait → exec → wait | 2 |
| exec → wait → exec → wait → exec → wait → exec → send_message | 1 |
| exec → wait → send_message → exec → wait → exec | 1 |
| exec → js → exec | 1 |
| shell_command → multi_agent_v1 → shell_command → multi_agent_v1 → shell_command | 1 |
| shell_command → read_thread_terminal → shell_command → view_image → shell_command → apply_patch → shell_command → apply_patch | 1 |
| exec → send_message → exec → send_message → exec → send_message → exec → wait | 1 |
| exec → wait → exec → wait → send_message | 1 |

## `wait` input keysets

| keys | count |
| --- | --- |
| `cell_id,max_tokens,yield_time_ms` | 451 |
| `cell_id,max_tokens,terminate,yield_time_ms` | 5 |
| `cell_id,max_tokens,terminate` | 1 |

## `send_message` input keysets

| keys | count |
| --- | --- |
| `message,target` | 70 |

## `spawn_agent` input keysets

| keys | count |
| --- | --- |
| `fork_turns,message,task_name` | 3 |
| `fork_turns,message,model,reasoning_effort,task_name` | 2 |

## `wait_agent` input keysets

| keys | count |
| --- | --- |
| `timeout_ms` | 37 |

## `js` input keysets

| keys | count |
| --- | --- |
| `code,title` | 60 |
| `code` | 12 |
| `code,timeout_ms,title` | 9 |

## `shell_command` input keysets

| keys | count |
| --- | --- |
| `command,timeout_ms,workdir` | 24 |
| `command,workdir` | 15 |
| `command,timeout_ms` | 5 |

## `followup_task` input keysets

| keys | count |
| --- | --- |
| `message,target` | 1 |

## `exec` input keysets

| keys | count |
| --- | --- |
| `<non-json-or-empty>` | 7566 |

## `apply_patch` input keysets

| keys | count |
| --- | --- |
| `<non-json-or-empty>` | 2 |

## interpretation

Work default is an **exec burst**, then optional **wait(cell_id)**, then more exec.
Multi-piece work is **send_message(target, message)** after a look burst, not extra apply_patch.
spawn_agent is rare. apply_patch is almost absent.
