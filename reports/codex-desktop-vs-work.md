# Non-empty Codex Desktop vs Work (calls only)

v36. Do not average these originators.

| originator | files | with calls | apply_patch files | update_plan first |
| --- | --- | --- | --- | --- |
| codex_work_desktop | 87 | 83 | 1 | 0 |
| Codex Desktop | 1103 | 994 | 1 | 1 |

## `Codex Desktop` calls

| tool | count |
| --- | --- |
| exec | 22209 |
| wait | 3044 |
| shell_command | 2045 |
| wait_agent | 364 |
| js | 216 |
| apply_patch | 186 |
| send_message | 113 |
| list_agents | 68 |
| update_plan | 61 |
| _fetch_file | 52 |

### `Codex Desktop` first call

| tool | sessions |
| --- | --- |
| exec | 990 |
| shell_command | 1 |
| _fetch | 1 |
| update_plan | 1 |
| request_permissions | 1 |

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

Desktop is the bulk of the hashed corpus and still patches/plans more than Work.
Work gold stays exec/wait/send, almost no apply_patch. Do not imitate Desktop as Work.
