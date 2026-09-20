# Local corpus inventory (pre-copy, counts only)

Generated 2026-09-20 from live paths. Overnight runner will copy-hash then rewrite richer reports under `reports/local-corpus.md`.

## Codex / ChatGPT Work desktop

Not chatgpt.com Cloud.

| Item | Count |
| --- | --- |
| live `rollout-*.jsonl` | 1113 (~1.06 GB) |
| archived `rollout-*.jsonl` | 405 (~362 MB) |
| `session_index.jsonl` lines | 165 (incomplete vs glob) |
| `state_5.sqlite` threads | 1569 (1164 live / 405 archived) |
| `thread_history_1.sqlite` items | 75980 |
| turns | 6350 |
| spawn edges | 183 |

### thread_source

| source | count |
| --- | --- |
| user | 1281 |
| subagent | 191 |
| (null) | 78 |
| agent_forked_thread | 6 |
| agent_created_thread | 6 |
| realtime_voice | 5 |
| chatgpt_handoff | 2 |

### models (threads)

| model | count |
| --- | --- |
| gpt-5.6-luna | 1143 |
| gpt-5.5 | 233 |
| gpt-5.6-terra | 92 |
| gpt-5.6-sol | 76 |
| gpt-5.4-mini | 8 |
| other | 17 |

### item_type (already a classifier)

| item_type | count |
| --- | --- |
| reasoning | 29540 |
| agentMessage | 17637 |
| commandExecution | 12644 |
| userMessage | 6082 |
| mcpToolCall | 5393 |
| fileChange | 3029 |
| webSearch | 754 |
| collabAgentToolCall | 383 |
| contextCompaction | 230 |
| subAgentActivity | 199 |
| imageView | 35 |
| dynamicToolCall | 26 |
| plan | 16 |
| functionCallOutput | 11 |
| imageGeneration | 6 |

JSONL types sampled: `session_meta`, `event_msg`, `response_item`, `turn_context`, `compacted`, `world_state`.

## OpenCode

`opencode.db`: 153 sessions, 2631 messages, 10279 parts, 40364 events, 17 projects.

Models mixed: gpt-5.5, minimax, grok-4.6, mimo, deepseek, qwen, gemini, luna/terra via LiteLLM.

## Kilo (this product)

`kilo.db`: 18 sessions, 1462 messages, 6969 parts. Almost all `grok-4.6`.

`storage/session_diff`: 18 JSON files — sidecars, not the transcript.

## Not a corpus

| Path | Why |
| --- | --- |
| `kilocode.kilo-code` VS Code globalStorage | empty |
| ChatGPT.com | not on disk |
| `OpenAI.Codex` Store package LocalState | not treated as transcripts |
| Brave / Chromium web cache | forbidden |
