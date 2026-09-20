# ChatGPT Work sessions with no tool calls

Counts only. No bodies. v24.

Work files: **87** empty of calls: **4**
- line counts: [14, 14, 24, 25]

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

Empty Work files are short (14–25 lines): user/assistant messages and task_started/complete, **no tool calls**.
Originator table **95** counts session_meta rows, not files; tool-call analysis uses **87** files.
Do not spawn or patch for these. They are not vscode sandwich.
