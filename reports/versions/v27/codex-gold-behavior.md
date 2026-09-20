# Codex gold behavior (full hashed corpus)

Generated: 2026-09-20T17:22:46Z

Local Codex/ChatGPT Work transcripts are gold. No message bodies.

- hashed files: **1521** / 1521
- lines: **355679**
- bad json lines: **0**
- sessions with decompose tools (spawn/plan/wait/list/followup): **30**
- sessions with exec/shell: **1195**
- sessions with apply_patch/file tools: **45**

## originator (one file once)

| originator | count |
| --- | --- |
| Codex Desktop | 1103 |
| codex_exec | 315 |
| codex_work_desktop | 87 |
| codex_vscode | 16 |

## collaboration_mode

| mode | count |
| --- | --- |
| default | 6836 |
| plan | 54 |

## models (turn_context)

| model | count |
| --- | --- |
| gpt-5.6-luna | 5144 |
| gpt-5.5 | 735 |
| gpt-5.6-terra | 565 |
| gpt-5.4-mini | 219 |
| gpt-5.6-sol | 114 |
| codex-auto-review | 66 |
| gpt-5.4 | 14 |
| grok-4-5 | 13 |
| gpt-5.6-sol-wm | 10 |
| gpt-5.5x-high | 3 |
| gpt-6-astra | 2 |
| gpt-4.1 | 1 |
| terra | 1 |
| gpt-5.1-codex-max | 1 |
| codex-mini | 1 |
| o3 | 1 |

## top-level JSONL type

| type | count |
| --- | --- |
| response_item | 170280 |
| event_msg | 156804 |
| token_usage_record | 17697 |
| turn_context | 6890 |
| world_state | 1858 |
| session_meta | 1532 |
| inter_agent_communication_metadata | 352 |
| compacted | 266 |

## tool names

| tool | count |
| --- | --- |
| exec | 30816 |
| shell_command | 8743 |
| wait | 3538 |
| apply_patch | 967 |
| wait_agent | 401 |
| js | 299 |
| send_message | 183 |
| update_plan | 137 |
| list_agents | 77 |
| _fetch_file | 63 |
| spawn_agent | 47 |
| request_user_input | 30 |
| request_permissions | 28 |
| followup_task | 27 |
| interrupt_agent | 25 |
| _create_file | 21 |
| run | 5 |
| view_image | 4 |
| create_thread | 3 |
| send_message_to_thread | 3 |
| multi_agent_v1 | 3 |
| _get_repo | 3 |
| _create_issue | 3 |
| _add_comment_to_issue | 3 |
| _update_file | 3 |
| read_thread_terminal | 2 |
| _fetch | 2 |
| _search_branches | 2 |
| _create_branch | 2 |
| _get_users_recent_prs_in_repo | 2 |
| list_mcp_resources | 1 |
| _search_installed_repositories_v2 | 1 |
| get_goal | 1 |
| _search_issues | 1 |
| list_available_plugins_to_install | 1 |
| _compare_commits | 1 |
| _create_pull_request | 1 |

## first tool in session

| first_tool | sessions |
| --- | --- |
| exec | 1128 |
| shell_command | 53 |
| update_plan | 9 |
| create_thread | 3 |
| _fetch | 1 |
| request_permissions | 1 |

## tool bigrams (top 40)

| bigram | count |
| --- | --- |
| exec -> exec | 27240 |
| shell_command -> shell_command | 8031 |
| exec -> wait | 1970 |
| wait -> exec | 1950 |
| wait -> wait | 1561 |
| shell_command -> apply_patch | 517 |
| apply_patch -> shell_command | 512 |
| apply_patch -> apply_patch | 431 |
| wait_agent -> exec | 277 |
| exec -> wait_agent | 224 |
| js -> js | 214 |
| exec -> send_message | 126 |
| update_plan -> shell_command | 103 |
| shell_command -> update_plan | 99 |
| exec -> js | 83 |
| js -> exec | 82 |
| send_message -> exec | 71 |
| send_message -> wait_agent | 59 |
| _fetch_file -> _fetch_file | 58 |
| wait_agent -> list_agents | 49 |
| wait_agent -> wait_agent | 36 |
| spawn_agent -> wait_agent | 29 |
| list_agents -> wait_agent | 28 |
| list_agents -> exec | 27 |
| exec -> spawn_agent | 25 |
| wait_agent -> send_message | 25 |
| followup_task -> wait_agent | 25 |
| exec -> list_agents | 20 |
| request_user_input -> exec | 20 |
| shell_command -> request_permissions | 19 |
| exec -> request_user_input | 18 |
| _create_file -> _create_file | 18 |
| request_permissions -> shell_command | 15 |
| interrupt_agent -> followup_task | 15 |
| update_plan -> apply_patch | 14 |
| apply_patch -> update_plan | 12 |
| wait -> send_message | 12 |
| exec -> interrupt_agent | 12 |
| list_agents -> send_message | 10 |
| send_message -> send_message | 9 |

## tool trigrams (top 30)

| trigram | count |
| --- | --- |
| exec -> exec -> exec | 24664 |
| shell_command -> shell_command -> shell_command | 7426 |
| exec -> wait -> exec | 1416 |
| exec -> exec -> wait | 1296 |
| wait -> exec -> exec | 1268 |
| wait -> wait -> wait | 1017 |
| wait -> exec -> wait | 667 |
| exec -> wait -> wait | 543 |
| wait -> wait -> exec | 530 |
| shell_command -> shell_command -> apply_patch | 451 |
| apply_patch -> shell_command -> shell_command | 442 |
| shell_command -> apply_patch -> shell_command | 344 |
| apply_patch -> apply_patch -> apply_patch | 261 |
| wait_agent -> exec -> wait_agent | 180 |
| exec -> wait_agent -> exec | 176 |
| shell_command -> apply_patch -> apply_patch | 165 |
| apply_patch -> apply_patch -> shell_command | 163 |
| js -> js -> js | 162 |
| update_plan -> shell_command -> shell_command | 87 |
| shell_command -> shell_command -> update_plan | 84 |
| exec -> exec -> send_message | 83 |
| shell_command -> update_plan -> shell_command | 76 |
| js -> exec -> exec | 70 |
| exec -> exec -> js | 68 |
| apply_patch -> shell_command -> apply_patch | 60 |
| exec -> send_message -> exec | 59 |
| _fetch_file -> _fetch_file -> _fetch_file | 53 |
| exec -> js -> js | 52 |
| js -> js -> exec | 52 |
| send_message -> exec -> exec | 52 |

## How this feeds the imitate mode

Kilo and OpenCode must copy **these** chains (task split + tool order), not a public exam.

Elapsed s: 11

## Do not average originators

Primary gold is **ChatGPT Work** (`codex_work_desktop`, **87** files). Work almost never `apply_patch` (1 session). The `shell_command → apply_patch` trigrams above are **codex_vscode** (n=16). See `reports/codex-by-originator.md`, `reports/codex-work-desktop-only.md`.

Work self-score on R1–R6: **81/83**. Snapshot of the 1518 generation: `reports/versions/v22/codex-gold-behavior-1518.md`.

## Deep pass (exec bins, no command text)

Generated: 2026-09-20T17:24:07Z elapsed_s=17 files=1521 lines=355679

### exec/shell first-token bins

| bin | count |
| --- | --- |
| js_cell | 29231 |
| look | 5168 |
| check | 2062 |
| other:@' | 250 |
| redacted | 230 |
| git_other | 224 |
| other:text(await | 150 |
| other:if | 130 |
| other:docker | 109 |
| write | 94 |
| script | 90 |
| other:get-ciminstance | 72 |
| other:hermes | 69 |
| other:python.exe | 68 |
| other:gh | 61 |
| other:$path | 55 |
| other:start-sleep | 53 |
| other:railway | 42 |
| other:get-command | 41 |
| other:ssh | 41 |
| other:cmd | 41 |
| other:get-process | 40 |
| other:$i=1; | 30 |
| other:try | 29 |
| other:$paths | 25 |
| other:cortex | 25 |
| other:npm.cmd | 25 |
| other:$root | 24 |
| other:text(all_tools.filter(x | 22 |
| other:curl.exe | 22 |
| other:get-date | 21 |
| other:where.exe | 21 |
| other:get-filehash | 20 |
| other:tailscale | 18 |
| other:$lines | 18 |
| other:foreach | 17 |
| other:bash | 17 |
| other:hades-backup'; | 17 |
| other:$files | 14 |
| other:opencode | 14 |

### first exec bin in a session

| first_bin | sessions |
| --- | --- |
| js_cell | 1128 |
| look | 54 |
| check | 4 |
| other:config.yaml'; | 1 |
| other:i.test(x.name+" | 1 |
| other:$erroractionpreference | 1 |
| git_other | 1 |
| other:get-command | 1 |
| other:text(await | 1 |
| other:$erroractionpreference='stop'; | 1 |
| write | 1 |
| other:get-location; | 1 |

- sessions with exec bins: **1195**
- look before first write (among those with a write bin): **40**
- write as first exec bin: **1**
- median exec-steps to first write bin: **21**
- sessions with decompose tools: **67**

### first decompose tool

| tool | sessions |
| --- | --- |
| send_message | 39 |
| update_plan | 19 |
| spawn_agent | 5 |
| create_thread | 3 |
| list_agents | 1 |

### collapsed look/write/check shapes (top 25)

| shape | sessions |
| --- | --- |
| js_cell | 957 |
| js_cell|check|js_cell|check|js_cell|check|js_cell|check | 42 |
| js_cell|check|js_cell | 22 |
| js_cell|check|js_cell|check|js_cell | 20 |
| look | 11 |
| js_cell|redacted|js_cell | 9 |
| js_cell|check|js_cell|check|js_cell|check|js_cell | 8 |
| js_cell|redacted|js_cell|check|js_cell|check|js_cell|check | 6 |
| js_cell|other:text(all_tools.filter(x|js_cell | 6 |
| js_cell|check | 5 |
| js_cell|check|js_cell|check | 4 |
| js_cell|check|js_cell|check|js_cell|check | 3 |
| js_cell|check|js_cell|other:function|js_cell|other:function|js_cell|check | 2 |
| js_cell|redacted|js_cell|redacted|js_cell|redacted|js_cell|redacted | 2 |
| js_cell|redacted|js_cell|redacted|js_cell | 2 |
| js_cell|other:for|js_cell|check|js_cell|check|js_cell | 2 |
| js_cell|redacted|js_cell|check|js_cell|check|js_cell | 2 |
| js_cell|other:text(all_tools.filter(x|js_cell|other:text(all_tools.filter(x|js_cell | 2 |
| look|git_other|check|look|write|look|write|look | 1 |
| other:config.yaml';|other:hermes';|other:config.yaml';|write|other:config.yaml';|other:hermes|other:$files|other:hermes'; | 1 |
| look|other:if|look|other:if|look|other:if|look|other:$paths | 1 |
| js_cell|other:for|js_cell | 1 |
| js_cell|write|check|js_cell | 1 |
| js_cell|redacted|js_cell|redacted|js_cell|redacted|js_cell|other:text(all_tools.filter(x | 1 |
| look|other:hermes|look|other:docker|other:hermes|redacted|look | 1 |

Mixed-corpus `exec` is still mostly **js_cell** (29231). Write-as-first-exec-bin is **1**. Do not treat this mixed binning as Work gold; Work cwd shell is 2/87. Work task-split and wait reports are under `reports/codex-work-*.md`.
