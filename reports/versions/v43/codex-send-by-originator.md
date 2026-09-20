# send_message / spawn_agent session rate by originator

Calls only. One originator per file. v43. Do not average.

| originator | files | with calls | send_message | spawn_agent |
| --- | --- | --- | --- | --- |
| codex_work_desktop | 87 | 83 | 25 | 2 |
| Codex Desktop | 1103 | 994 | 17 | 3 |
| codex_exec | 315 | 105 | 0 | 0 |
| codex_vscode | 16 | 13 | 0 | 0 |

## interpretation

Work splits with send_message, not vscode (0). spawn_agent is rare on Work.
Imitate send-after-look. Do not imitate vscode (no send, all patch).
