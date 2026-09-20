# Codex gold behavior (full hashed corpus)

Generated: 2026-09-20T17:22:46Z

Local Codex/ChatGPT Work transcripts are gold. No message bodies.

- hashed files: **1521** / 1521
- lines: **355679**
- bad json lines: **0**
- sessions with decompose tools (spawn/plan/wait/list/followup): **30**
- sessions with exec/shell: **1195**
- sessions with apply_patch/file tools: **45**

## originator

| originator | count |
| --- | --- |
| Codex Desktop | 1106 |
| codex_exec | 315 |
| codex_work_desktop | 95 |
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

Primary gold is **ChatGPT Work** (`codex_work_desktop`, 95 files / 87 tool sessions). Work almost never `apply_patch` (1 session). The `shell_command → apply_patch` trigrams above are **codex_vscode** (n=16). See `reports/codex-by-originator.md`, `reports/codex-work-desktop-only.md`.

Work self-score on R1–R6: **81/83**. Snapshot of the 1518 generation: `reports/versions/v22/codex-gold-behavior-1518.md`.
