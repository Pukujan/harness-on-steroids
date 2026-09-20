# wait session rate by originator

Calls only. One originator per file. v42. Do not average.

| originator | files | with calls | wait files | rate among nonempty |
| --- | --- | --- | --- | --- |
| codex_work_desktop | 87 | 83 | 31 | 31/83 |
| Codex Desktop | 1103 | 994 | 88 | 88/994 |
| codex_exec | 315 | 105 | 16 | 16/105 |
| codex_vscode | 16 | 13 | 0 | 0/13 |

## interpretation

Work and Desktop wait on cells. vscode almost never waits (shell↔patch instead).
Imitate Work wait-after-exec, not vscode.
