# ChatGPT Work sessions with no tool calls

Counts only. No bodies. v25.

Work files: **87** empty of calls: **4**
- line counts: [14, 14, 24, 25]
- session_meta rows: **95** (files with 1 meta: **79**; with 2: **8**)

## top-level types (empty files)

| type | count |
| --- | --- |
| event_msg | 35 |
| response_item | 25 |
| turn_context | 7 |
| world_state | 6 |
| session_meta | 4 |

## payload.type (empty files)

| type | count |
| --- | --- |
| message | 21 |
| item_completed | 14 |
| task_started | 7 |
| task_complete | 7 |
| reasoning | 4 |
| token_count | 4 |
| thread_settings_applied | 3 |

## interpretation

Empty Work files are short (14–25 lines): messages and task_started/complete, **no tool calls**.
Originator **95** is session_meta rows (79 files ×1 + 8 files ×2). Tool-call analysis uses **87** files.
If there is nothing to look up, stop. Do not spawn or patch.
