# Non-empty vscode vs Work (calls only)

v39. Do not average these originators.

| originator | files | with calls | apply_patch files | first=shell |
| --- | --- | --- | --- | --- |
| codex_work_desktop | 87 | 83 | 1 | 2 |
| codex_vscode | 16 | 13 | **12** | **13** |

vscode nonempty: shell_command 5562, apply_patch 718. Every nonempty vscode session starts with shell_command. 12/13 patch.

Work: exec 81 first, apply_patch 1/83.

## interpretation

The shell↔patch sandwich is vscode (12/13 nonempty) plus nonempty `codex_exec` (31/105). Not Desktop (1/994). Not Work (1/83).
