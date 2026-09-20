# Codex exec/js/shell input shapes (keys only)

Files scanned: **1518**

- exec inputs with `command` key: **0**
- exec inputs with `code`/`source`: **0**
- js inputs with code-like key: **283**

## call counts (this pass)

| name | count |
| --- | --- |
| exec | 30373 |
| shell_command | 8743 |
| wait | 3538 |
| apply_patch | 967 |
| js | 283 |
| update_plan | 137 |
| spawn_agent | 47 |
| run | 5 |

## `apply_patch` input keysets

| keys | count |
| --- | --- |
| `<non-json-or-empty>` | 967 |

## `exec` input keysets

| keys | count |
| --- | --- |
| `<non-json-or-empty>` | 30373 |

## `js` input keysets

| keys | count |
| --- | --- |
| `code,title` | 229 |
| `code,timeout_ms,title` | 41 |
| `code` | 13 |

## `run` input keysets

| keys | count |
| --- | --- |
| `response_length,time` | 4 |
| `response_length,search_query` | 1 |

## `shell_command` input keysets

| keys | count |
| --- | --- |
| `command,timeout_ms,workdir` | 8586 |
| `command,justification,sandbox_permissions,timeout_ms,workdir` | 83 |
| `command,timeout_ms` | 30 |
| `command,login,timeout_ms,workdir` | 16 |
| `command,workdir` | 15 |
| `command,justification,prefix_rule,sandbox_permissions,timeout_ms,workdir` | 6 |
| `command` | 4 |
| `command,justification,sandbox_permissions` | 1 |
| `command,justification,sandbox_permissions,timeout_ms` | 1 |
| `command,login,timeout_ms` | 1 |

## `spawn_agent` input keysets

| keys | count |
| --- | --- |
| `fork_turns,message,model,reasoning_effort,task_name` | 42 |
| `fork_turns,message,task_name` | 5 |

## `update_plan` input keysets

| keys | count |
| --- | --- |
| `plan` | 106 |
| `explanation,plan` | 31 |

## `wait` input keysets

| keys | count |
| --- | --- |
| `cell_id,max_tokens,yield_time_ms` | 3500 |
| `cell_id,max_tokens,terminate` | 20 |
| `cell_id,max_tokens,terminate,yield_time_ms` | 18 |
