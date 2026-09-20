# ChatGPT Work wait / exec-run insertion (`codex_work_desktop`)

Keys and counts only. No bodies. v9.

Sessions: **87** with wait: **31**
- exec-runs: **363** median length **3**
- after an exec-run: wait **218**, send_message **53**, apply_patch **0**, end **59**

## exec-run length buckets

| length | runs |
| --- | --- |
| 1 | 125 |
| 2 | 38 |
| 3 | 31 |
| 4 | 18 |
| 5 | 15 |
| 6-10 | 45 |
| 11-20 | 30 |
| 21-50 | 38 |
| 51+ | 23 |

## next tool after an exec-run

| next | count |
| --- | --- |
| wait | 218 |
| <end> | 59 |
| send_message | 53 |
| js | 23 |
| wait_agent | 5 |
| list_agents | 3 |
| spawn_agent | 2 |

## `wait` previous / next

| prev | count |
| --- | --- |
| wait | 235 |
| exec | 218 |
| send_message | 4 |

| next | count |
| --- | --- |
| wait | 235 |
| exec | 211 |
| send_message | 9 |
| <end> | 2 |

## `send_message` previous / next

| prev | count |
| --- | --- |
| exec | 53 |
| wait | 9 |
| wait_agent | 5 |
| send_message | 2 |
| list_agents | 1 |

| next | count |
| --- | --- |
| exec | 38 |
| <end> | 18 |
| wait_agent | 7 |
| wait | 4 |
| send_message | 2 |
| list_agents | 1 |

## interpretation

After a short exec burst, Work **waits or sends**, almost never patches.
wait is usually exec → wait → exec (or wait → wait). send_message sits between exec bursts.
Do not treat a long look-then-patch sandwich as Work gold.
