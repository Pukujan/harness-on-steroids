# ChatGPT Work wait clusters (`codex_work_desktop`)

Counts only. No bodies. v11.

Sessions: **85** with wait: **31** with wait-run length ≥2: **18**
- wait-runs: **222** median **1**
- wait_agent-runs: **19** median **1**

## wait-run length buckets

| length | runs |
| --- | --- |
| 1 | 111 |
| 2 | 25 |
| 3 | 73 |
| 4 | 5 |
| 5 | 3 |
| 6-10 | 4 |
| 11+ | 1 |

## wait_agent-run length buckets

| length | runs |
| --- | --- |
| 1 | 10 |
| 2 | 4 |
| 3 | 3 |
| 4 | 1 |
| 5 | 0 |
| 6-10 | 1 |
| 11+ | 0 |

## next after a wait-run

| next | count |
| --- | --- |
| exec | 211 |
| send_message | 9 |
| <end> | 2 |

## next after a wait_agent-run

| next | count |
| --- | --- |
| list_agents | 5 |
| exec | 5 |
| send_message | 5 |
| <end> | 2 |
| interrupt_agent | 1 |
| followup_task | 1 |

## interpretation

Work often **waits more than once** before looking again. After a wait-run, next is usually exec.
After wait_agent, next is list_agents / send_message / exec, not apply_patch.
Imitate: if you wait on a cell or child, you may wait again. Do not patch when the wait ends.
