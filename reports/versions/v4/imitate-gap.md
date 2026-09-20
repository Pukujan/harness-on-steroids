# Imitate gap (iteration 2)

Gold now: `exec` is **JS cells** (30044/30373), then `wait(cell_id)`, not Get-Content. Real shell is `shell_command`+workdir. Edits sit between shells. Spawn is rare and named (`task_name`).

## Modes updated

`.kilo/agent/codex.md` and `.opencode/agent/codex.md` now say wait-on-slow-work and cell/wait_agent, not “bash is the whole gold.”

## Error recovery (new)

Gold after fail: **look 446 / patch 59**. Modes now say look-again after failure.

## First tool (sqlite copies, this machine)

- **Kilo** 17 tool sessions: first is `read` 9, skill 3, recall 3, bash 1. **Zero** edit/write first.
- **OpenCode** 77: Study OS tools dominate; bash 10 first; 1 non-bash write-first.

Kilo already look-first in this tiny sample. Gap is wait-on-cell, sandwich after edit, error-then-look — not “stop writing first.” OpenCode is not a clean coding corpus.

## Originator split (do not average away Work)

| originator | n | first tool | writes |
| --- | --- | --- | --- |
| Codex Desktop | 1105 | exec | some apply_patch (186) |
| codex_exec | 315 | exec/shell | apply_patch 61 |
| **codex_work_desktop** | **93** | **exec** | **apply_patch not in top tools** |
| codex_vscode | 16 | shell_command | apply_patch 718 (sandwich) |

Imitate **Work**, not VS Code. Modes updated.

## Still open

- Kilo has no JS notebook cell. Mapping is inspect tools + wait.
- Owner decides match. Do not switch to SWE-bench.
