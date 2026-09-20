# Local corpus stats (counts only)

Generated: 2026-09-20T05:06:16Z

No message bodies, titles, previews, or paths with file contents.

## Codex Work / Desktop

Primary transcripts are local `rollout-*.jsonl`. ChatGPT.com Cloud is not this corpus.

Threads in `state_5` copy: **1569**

### Originator

| originator | count |
| --- | --- |
| (null) | 1561 |
| Codex Desktop | 5 |
| codex_work_desktop | 3 |

### thread_source

| thread_source | count |
| --- | --- |
| user | 1281 |
| subagent | 191 |
| (null) | 78 |
| agent_forked_thread | 6 |
| agent_created_thread | 6 |
| realtime_voice | 5 |
| chatgpt_handoff | 2 |

### model

| model | count |
| --- | --- |
| gpt-5.6-luna | 1143 |
| gpt-5.5 | 233 |
| gpt-5.6-terra | 92 |
| gpt-5.6-sol | 76 |
| gpt-5.4-mini | 8 |
| gpt-5.6-sol-wm | 3 |
| gpt-5.5x-high | 3 |
| gpt-5.4 | 2 |
| (null) | 2 |
| terra | 1 |
| o3 | 1 |
| grok-4-5 | 1 |
| gpt-5.1-codex-max | 1 |
| gpt-4.1 | 1 |
| codex-mini | 1 |
| codex-auto-review | 1 |

### archived

| archived | count |
| --- | --- |
| 0 | 1164 |
| 1 | 405 |

### item_type histogram

| item_type | count |
| --- | --- |
| reasoning | 29544 |
| agentMessage | 17639 |
| commandExecution | 12646 |
| userMessage | 6082 |
| mcpToolCall | 5393 |
| fileChange | 3030 |
| webSearch | 754 |
| collabAgentToolCall | 383 |
| contextCompaction | 230 |
| subAgentActivity | 199 |
| imageView | 35 |
| dynamicToolCall | 26 |
| plan | 16 |
| functionCallOutput | 11 |
| imageGeneration | 6 |

### loop proxies (item_type sequence, no bodies)

- threads with item rows: **1403**
- threads with fileChange: **162**
- threads with webSearch: **100**
- threads with plan: **8**
- webSearch/imageView before first fileChange: **48** (29.6%)
- plan before first fileChange: **3** (1.9%)
- median seq to first fileChange: **34**
- median seq to first commandExecution: **3**
- median seq to first webSearch: **11**

### first item_type

| first_item_type | threads |
| --- | --- |
| userMessage | 1354 |
| reasoning | 43 |
| functionCallOutput | 6 |

### first-10 item_type signatures (top 20)

| first10 | threads |
| --- | --- |
| userMessage|reasoning|agentMessage|reasoning|mcpToolCall|reasoning|agentMessage | 463 |
| userMessage | 121 |
| userMessage|agentMessage | 108 |
| userMessage|reasoning|agentMessage|reasoning|mcpToolCall|reasoning|reasoning|agentMessage | 84 |
| userMessage|reasoning|agentMessage|userMessage|reasoning|agentMessage|userMessage|reasoning|agentMessage|userMessage | 70 |
| userMessage|reasoning|agentMessage|reasoning|mcpToolCall|reasoning|agentMessage|userMessage|reasoning|agentMessage | 50 |
| userMessage|reasoning|agentMessage|reasoning|mcpToolCall|reasoning|reasoning|agentMessage|userMessage|reasoning | 35 |
| userMessage|reasoning|agentMessage|reasoning|mcpToolCall|reasoning|commandExecution|reasoning|commandExecution|reasoning | 27 |
| userMessage|reasoning|agentMessage | 22 |
| userMessage|reasoning|reasoning|mcpToolCall|reasoning|agentMessage | 21 |
| userMessage|agentMessage|agentMessage | 15 |
| userMessage|agentMessage|agentMessage|agentMessage | 12 |
| userMessage|agentMessage|agentMessage|agentMessage|agentMessage | 10 |
| reasoning|agentMessage|commandExecution|reasoning|commandExecution|reasoning|commandExecution|reasoning|commandExecution|reasoning | 10 |
| userMessage|agentMessage|agentMessage|agentMessage|agentMessage|agentMessage|agentMessage|agentMessage|agentMessage|agentMessage | 8 |
| userMessage|reasoning|reasoning|mcpToolCall|reasoning|agentMessage|userMessage|reasoning|mcpToolCall|reasoning | 8 |
| userMessage|reasoning|agentMessage|reasoning|mcpToolCall|reasoning|reasoning|reasoning|agentMessage | 8 |
| userMessage|reasoning|agentMessage|reasoning|mcpToolCall|reasoning|agentMessage|userMessage|reasoning|mcpToolCall | 7 |
| userMessage|reasoning|agentMessage|reasoning|mcpToolCall|reasoning|reasoning|reasoning|agentMessage|userMessage | 7 |
| userMessage|reasoning|agentMessage|commandExecution|reasoning|commandExecution|reasoning|commandExecution|reasoning|commandExecution | 6 |

## Kilo (this product CLI db)

### kilo.db

- sessions: **18**
- messages: **1480**
- parts: **7082**

part `json_extract(data,'$.type')`

| part_type | count |
| --- | --- |
| tool | 2532 |
| step-start | 1199 |
| reasoning | 1199 |
| step-finish | 1193 |
| text | 766 |
| patch | 180 |
| file | 12 |
| compaction | 1 |

message role/type extract

| role_or_type | count |
| --- | --- |
| assistant | 1208 |
| user | 272 |

## OpenCode

### opencode.db

- sessions: **153**
- messages: **2631**
- parts: **10279**

part `json_extract(data,'$.type')`

| part_type | count |
| --- | --- |
| tool | 2959 |
| step-start | 2144 |
| text | 2083 |
| step-finish | 2071 |
| reasoning | 944 |
| patch | 61 |
| compaction | 17 |

message role/type extract

| role_or_type | count |
| --- | --- |
| assistant | 2186 |
| user | 445 |

