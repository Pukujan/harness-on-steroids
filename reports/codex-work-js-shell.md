# ChatGPT Work js vs shell vs exec (`codex_work_desktop`)

Keys and counts only. No bodies. v10.

Sessions with calls: **81** / 85
- with exec: **79**
- with js: **5** (also have exec: **5**)
- with shell_command: **2** (also apply_patch: **1**)

## call counts

| tool | count |
| --- | --- |
| exec | 7345 |
| wait | 457 |
| js | 81 |
| send_message | 70 |
| shell_command | 44 |
| wait_agent | 37 |
| list_agents | 9 |
| spawn_agent | 5 |
| multi_agent_v1 | 3 |
| view_image | 2 |
| apply_patch | 2 |
| interrupt_agent | 1 |

## `js` previous / next

| prev | count |
| --- | --- |
| js | 58 |
| exec | 23 |

| next | count |
| --- | --- |
| js | 58 |
| exec | 23 |

## `shell_command` previous / next

| prev | count |
| --- | --- |
| shell_command | 35 |
| <start> | 2 |
| multi_agent_v1 | 2 |
| view_image | 2 |
| apply_patch | 2 |
| read_thread_terminal | 1 |

| next | count |
| --- | --- |
| shell_command | 35 |
| multi_agent_v1 | 2 |
| <end> | 2 |
| view_image | 2 |
| apply_patch | 2 |
| read_thread_terminal | 1 |

## interpretation

Work inspect is **exec** (JS cells), not cwd shell. `js` is a rare sibling of exec.
`shell_command` is scarce; the only apply_patch session is in the shell slice.
Do not map Work gold to bash+edit. Map exec to Read/Grep/inspect; map js to a small script still after look.
