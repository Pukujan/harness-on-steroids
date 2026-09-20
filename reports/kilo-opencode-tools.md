# Kilo / OpenCode tool names (counts only)

Generated: 2026-09-20T05:24:00Z from sqlite copies. No bodies.

Observe set used for proxies: read, glob, grep, webfetch, websearch, semantic_search, kilo_local_recall.  
Mutate set: edit, write, bash, patch.  
Plan-ish: open_plan, plan_exit, todowrite.

## Kilo (`kilo.db`)

18 sessions, 1480 messages, 7082 parts.

| tool | count |
| --- | --- |
| read | 826 |
| bash | 406 |
| edit | 322 |
| write | 263 |
| glob | 211 |
| grep | 206 |
| patch | 180 |
| webfetch | 128 |
| todowrite | 29 |
| kilo_local_recall | 21 |
| question | 20 |
| open_plan | 20 |
| task | 19 |
| plan_exit | 18 |
| skill | 14 |
| schedule_wakeup | 13 |
| semantic_search | 5 |
| suggest | 4 |
| agent_manager | 4 |
| background_process | 3 |

Loop proxies (17 sessions with tools, 16 with mutate):

- observe before first mutate: **15 / 16 (93.8%)**
- plan-ish before first mutate: **2 / 16 (12.5%)**
- median tool-seq to first mutate: **13**
- first tool: read 9, skill 3, kilo_local_recall 3, agent_manager 1, bash 1

**n=18. Do not treat as equal to Codex.**

## OpenCode (`opencode.db`)

153 sessions, 2631 messages, 10279 parts.

| tool | count |
| --- | --- |
| bash | 1295 |
| read | 551 |
| write | 341 |
| edit | 323 |
| webfetch | 97 |
| patch | 61 |
| todowrite | 55 |
| glob | 51 |
| grep | 43 |
| study-os-replay_get_problem_turn | 41 |
| websearch | 36 |
| study-os-replay_request_problem_expansion | 33 |
| task | 14 |
| question | 8 |
| skill | 3 |

Loop proxies (77 sessions with tools, 25 with mutate):

- observe before first mutate: **6 / 25 (24.0%)**
- plan-ish before first mutate: **5 / 25 (20.0%)**
- median tool-seq to first mutate: **1**
- first tools dominated by `study-os-replay_*` and `bash`

OpenCode local db is **not a clean coding-agent corpus**. Many sessions are Study OS replay, not harness-loop coding.
