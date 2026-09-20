# Originator dashboard (do not average)

v51. Rates among nonempty files. Sources: patch/wait/send/plan/shell/js-by-originator reports.

| originator | nonempty | patch | wait | send | spawn | update_plan | cwd shell | js |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Work | 83 | **1/83** | **31/83** | **25** | 2 | **0** | **2** | **5** |
| Desktop | 994 | 1/994 | 88/994 | 17 | 3 | 2 | 4 | 17 |
| `codex_exec` | 105 | **31/105** | 16/105 | 0 | 0 | 11 | **45** | 1 |
| vscode | 13 | **12/13** | **0/13** | **0** | 0 | 6 | **13** | 1 |

Imitate Work: look, wait, send; almost never patch; never update_plan; rare js next to exec. Do not imitate vscode (patch, no wait, no send, always cwd shell). Do not imitate nonempty exec (patch + plan-first + cwd shell).
