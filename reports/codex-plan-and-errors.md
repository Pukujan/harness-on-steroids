# Codex plan-mode vs default, and after failed exec

Files: **1518**

- failed tool outputs (nonzero Exit code prefix): **1058**
- spawn_agent calls: **47** (with model field: **0**)

## first tool by collaboration_mode (approx, last mode on file)

### first tool, mode=default

| name | count |
| --- | --- |
| exec | 1123 |
| shell_command | 53 |
| update_plan | 9 |
| create_thread | 3 |
| _fetch | 1 |
| request_permissions | 1 |

### first tool, mode=plan

| name | count |
| --- | --- |
| exec | 2 |

## tools by last collaboration_mode

### tools, mode=default

| name | count |
| --- | --- |
| exec | 30150 |
| shell_command | 8679 |
| wait | 3466 |
| apply_patch | 967 |
| wait_agent | 401 |
| js | 283 |
| send_message | 183 |
| update_plan | 137 |
| list_agents | 77 |
| _fetch_file | 63 |
| spawn_agent | 47 |
| request_permissions | 28 |

### tools, mode=plan

| name | count |
| --- | --- |
| exec | 223 |
| wait | 72 |
| shell_command | 64 |
| request_user_input | 29 |

## next tool after nonzero exit

| name | count |
| --- | --- |
| shell_command | 446 |
| apply_patch | 59 |
| update_plan | 10 |
| run | 4 |
| request_permissions | 4 |
| js | 1 |
| list_mcp_resources | 1 |
| _search_installed_repositories_v2 | 1 |
| _fetch_file | 1 |
| exec | 1 |
| view_image | 1 |
| _get_users_recent_prs_in_repo | 1 |

## spawn_agent fork_turns (values only)

| name | count |
| --- | --- |
