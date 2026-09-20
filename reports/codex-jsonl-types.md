# Codex JSONL type/tool histograms

Generated: 2026-09-20T05:07:34Z

- hashed files scanned: **1518** / 1518
- lines parsed: **351780**
- bad json lines: **0**

## top-level `type`

| type | count |
| --- | --- |
| response_item | 168658 |
| event_msg | 155034 |
| token_usage_record | 17223 |
| turn_context | 6874 |
| world_state | 1848 |
| session_meta | 1529 |
| inter_agent_communication_metadata | 352 |
| compacted | 262 |

## unknown top-level types

| type | count |
| --- | --- |
| token_usage_record | 17223 |
| inter_agent_communication_metadata | 352 |

## nested `type` (payload walk, skip body keys)

| nested_type | count |
| --- | --- |
| item_completed | 86680 |
| input_text | 70198 |
| reasoning | 51091 |
| token_count | 50775 |
| Reasoning | 41349 |
| custom_tool_call_output | 32809 |
| custom_tool_call | 32782 |
| message | 29890 |
| AgentMessage | 18464 |
| function_call | 13797 |
| function_call_output | 13775 |
| disabled | 10575 |
| CommandExecution | 9660 |
| unknown | 9325 |
| task_started | 6779 |
| danger-full-access | 6531 |
| task_complete | 6316 |
| UserMessage | 6302 |
| McpToolCall | 5542 |
| string | 5541 |
| thread_settings_applied | 4044 |
| text_result | 3958 |
| FileChange | 3435 |
| update | 3329 |
| object | 3102 |
| function | 1894 |
| add | 1394 |
| User | 1219 |
| WebSearch | 621 |
| integer | 566 |
| … | 10 more |

## tool `name` (only when type looks like a tool call)

| tool_name | count |
| --- | --- |
| exec | 31831 |
| shell_command | 8743 |
| wait | 3559 |
| apply_patch | 967 |
| wait_agent | 444 |
| js | 335 |
| send_message | 192 |
| update_plan | 137 |
| list_agents | 87 |
| _fetch_file | 63 |
| spawn_agent | 56 |
| followup_task | 31 |
| request_user_input | 30 |
| interrupt_agent | 30 |
| request_permissions | 28 |
| _create_file | 21 |
| run | 5 |
| view_image | 4 |
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
| … | 5 more |
