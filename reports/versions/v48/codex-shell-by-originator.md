# shell_command session rate by originator

Calls only. One originator per file. v48. Do not average.

| originator | files | with calls | shell_command files | shell first |
| --- | --- | --- | --- | --- |
| codex_work_desktop | 87 | 83 | 2 | 2 |
| Codex Desktop | 1103 | 994 | 4 | 1 |
| codex_exec | 315 | 105 | 45 | 37 |
| codex_vscode | 16 | 13 | 13 | 13 |

## interpretation

Work almost never cwd-shells. vscode always starts with shell. Do not bash as tool 1.
