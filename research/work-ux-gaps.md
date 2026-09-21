# Work UX / research / provenance gaps (durable)

Counts and structure only. No message bodies. Not SWE-bench. **Measurement not run** except tool-loop gold already in `reports/`.

## Encoded (tool loop)

Look burst, wait on `cell_id`, `send_message` after median 15 tools, `update_plan` 0, patch 1/87, chat-first vs no-stop in `AGENTS.md` / modes. Process R1–R6. Output-style briefing is a Kilo overlay, not a Work sentence measurement.

## Not encoded (still missing reports)

| Gap | What to count | Issue |
| --- | --- | --- |
| Talk vs tools | Speak before first tool / after last; length bands; heading-like vs plain | 14 |
| Child briefs | `send_message` length, target, look/verify/stop flags | 14 |
| User-turn class | question / go / correction | 14 |
| `compacted` | 262–266 events listed, never opened; Work vs vscode | 14 |
| Provenance in answers | path/command/hash or **not observed** | 15 |
| Research gates | valid / enough / action reliable / synthesize late | 15 |
| Same-thread wait vs wakeup | Work waits in-session; we use CONTINUE wakeups | 14, 15 |
| Outcome | PLAN F / issue 13 | 13 |
| Checkpoints | CURRENT + one task; README/STATUS drift | 16 |
| Export pack | spec + mapping + tests + adapters | 17 |
| Foundation | modules, ruff, mypy | 18 |

## Work research / planning (from counts)

Research = exec burst + wait + look again. Planning = doing, then a named `send_message` if multi-piece. Long-run = same thread + `cell_id`, not a 10-minute wakeup. Provenance in Work is tool output; we only slogan’d “prose is not truth.”

Do not treat the chat as the project. Synthesize late: child brief, user answer, or git checkpoint.

## Context / compression

Do not build a summarizer first. Measure `compacted` first. Lost in the Middle / RULER / LLMLingua / MemGPT are warnings, not the exam. Scratchpad = git checkpoint (issue 16).

## PCM vs imitate pack

PCM stores project state. The imitate pack stores how to act. Both required. PCM init must not overwrite `AGENTS.md` / `PLAN.md` / `HANDOFF.md`.

## Replay hygiene (issue 13)

Isolated `oc-sandbox`. No `--auto` on original Work cwds. No extra-turn on test-pinned hashes. No `user.md` in git or stdout.
