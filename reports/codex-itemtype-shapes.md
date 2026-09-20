# Codex item_type shapes (sqlite projection)

Not finished gold. Complements JSONL tool names.

- threads: **1403**
- with fileChange: **162**
- commandExecution/webSearch/imageView before first fileChange: **94**
- with plan/subagent/collab tools: **18**

## first item_type

| first | threads |
| --- | --- |
| userMessage | 1354 |
| reasoning | 43 |
| functionCallOutput | 6 |

## collapsed shapes (top 25)

| shape | threads |
| --- | --- |
| userMessage → reasoning → agentMessage → reasoning → mcpToolCall → reasoning → agentMessage | 559 |
| userMessage → agentMessage | 155 |
| userMessage | 122 |
| userMessage → reasoning → agentMessage → reasoning → mcpToolCall → reasoning → agentMessage → userMessage → reasoning → agentMessage | 91 |
| userMessage → reasoning → agentMessage → userMessage → reasoning → agentMessage → userMessage → reasoning → agentMessage → userMessage | 70 |
| reasoning → agentMessage → commandExecution → reasoning → commandExecution → reasoning → commandExecution → reasoning → commandExecution → reasoning | 34 |
| userMessage → reasoning → agentMessage → reasoning → mcpToolCall → reasoning → commandExecution → reasoning → commandExecution → reasoning | 34 |
| userMessage → reasoning → mcpToolCall → reasoning → agentMessage | 29 |
| userMessage → reasoning → agentMessage | 23 |
| userMessage → agentMessage → fileChange → agentMessage | 17 |
| userMessage → reasoning → agentMessage → reasoning → mcpToolCall → reasoning → agentMessage → userMessage → reasoning → mcpToolCall | 12 |
| userMessage → agentMessage → fileChange → agentMessage → fileChange → agentMessage | 10 |
| userMessage → reasoning → mcpToolCall → reasoning → agentMessage → userMessage → reasoning → mcpToolCall → reasoning → agentMessage | 10 |
| userMessage → agentMessage → userMessage → agentMessage → userMessage → agentMessage → userMessage → agentMessage → userMessage → agentMessage | 8 |
| reasoning → agentMessage → reasoning → commandExecution → reasoning → commandExecution → reasoning → commandExecution → reasoning → commandExecution | 8 |
| userMessage → reasoning → agentMessage → commandExecution → reasoning → commandExecution → reasoning → commandExecution → reasoning → commandExecution | 7 |
| userMessage → reasoning → agentMessage → commandExecution → reasoning → commandExecution → reasoning → agentMessage → commandExecution → reasoning | 7 |
| userMessage → reasoning → agentMessage → commandExecution → reasoning → commandExecution → reasoning → commandExecution → reasoning → agentMessage | 6 |
| userMessage → reasoning → agentMessage → reasoning → mcpToolCall → reasoning → agentMessage → commandExecution → reasoning → commandExecution | 5 |
| userMessage → agentMessage → webSearch → agentMessage → webSearch → agentMessage → fileChange → agentMessage → fileChange → agentMessage | 4 |
| userMessage → agentMessage → webSearch → agentMessage | 4 |
| userMessage → reasoning → agentMessage → reasoning → agentMessage → reasoning → agentMessage → reasoning → agentMessage → reasoning | 4 |
| userMessage → reasoning → mcpToolCall → reasoning → commandExecution → reasoning → commandExecution → reasoning → commandExecution → reasoning | 4 |
| userMessage → reasoning → agentMessage → userMessage → reasoning → agentMessage → userMessage → reasoning → agentMessage | 4 |
| userMessage → reasoning → agentMessage → reasoning → mcpToolCall | 4 |
