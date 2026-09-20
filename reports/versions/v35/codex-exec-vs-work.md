# Non-empty `codex_exec` vs Work (calls only)

v35. Do not average these originators.

| originator | files | with calls | apply_patch files |
| --- | --- | --- | --- |
| codex_work_desktop | 87 | 83 | 1 |
| codex_exec | 315 | 105 | 31 |

## `codex_exec` calls

| tool | count |
| --- | --- |
| shell_command | 1092 |
| exec | 1025 |
| apply_patch | 61 |
| wait | 37 |
| update_plan | 34 |
| _fetch_file | 11 |
| run | 5 |
| js | 1 |
| list_mcp_resources | 1 |
| _search_installed_repositories_v2 | 1 |

### `codex_exec` first call

| tool | sessions |
| --- | --- |
| exec | 60 |
| shell_command | 37 |
| update_plan | 8 |

## `codex_work_desktop` calls

| tool | count |
| --- | --- |
| exec | 7566 |
| wait | 457 |
| js | 81 |
| send_message | 70 |
| shell_command | 44 |
| wait_agent | 37 |
| list_agents | 9 |
| spawn_agent | 5 |
| multi_agent_v1 | 3 |
| view_image | 2 |

### `codex_work_desktop` first call

| tool | sessions |
| --- | --- |
| exec | 81 |
| shell_command | 2 |

## interpretation

Non-empty `codex_exec` patches more than Work. Work is exec/wait/send. Do not imitate exec-originator as Work.
