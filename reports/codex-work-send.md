# ChatGPT Work send_message task split (`codex_work_desktop`)

Counts only. No bodies. v12.

Sessions: **87**
- send_message: **25**
- spawn_agent: **2**
- both send and spawn: **1**
- list_agents: **4**
- wait_agent: **4**
- send and apply_patch: **0**
- median sends/session (among senders): **2**
- median index of first send: **15**

## sends per sending session

| sends | sessions |
| --- | --- |
| 1 | 11 |
| 2 | 6 |
| 3 | 2 |
| 4 | 1 |
| 5 | 2 |
| 6-10 | 2 |
| 11+ | 1 |

## after last send_message

| next | sessions |
| --- | --- |
| <end> | 18 |
| exec | 5 |
| wait_agent | 2 |

## between consecutive sends

| gap | count |
| --- | --- |
| exec-only | 26 |
| has-wait | 11 |
| has-wait_agent | 6 |
| <adjacent> | 2 |

## interpretation

Work splits multi-piece work with **repeated send_message**, not spawn_agent.
spawn_agent is 2 sessions. send+patch is 0. After the last send, look (exec) or stop.
Between sends, look (exec-only) or wait. Do not insert apply_patch.
