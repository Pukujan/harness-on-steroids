# Matched-task eval (owner want)

Owner: tool-call histograms are **not** the result. Want Kilo and OpenCode to run **the same Work tasks** and be scored on **observable work**, not only who called which tool.

## Gold still

Local ChatGPT Work transcripts (`codex_work_desktop`). Not vscode. Not SWE-bench. Not a new public exam. Not re-testing Codex on Harbor.

## What to compare (when replay exists)

For a Work session (hashed id only in git):

1. **Process** — existing R1–R6 / work_match (keep).
2. **Research** — did it look before changing anything (already R1/R3).
3. **Verification** — did it look/run after a change (R5 sandwich).
4. **Outcome** — files changed, tests run, whether the ask was addressed. Outcome needs a local replay; bodies stay in `data/raw/` (gitignored).

## Privacy

- Never commit message bodies, raw JSONL, or sqlite.
- Replay prompts, if used, live only under gitignored `data/replay/`.
- Git may hold: session hash, turn counts, tool names, scores.

## Not this

- Do not paste Work user text into git or into this spec.
- Do not stand up SWE-bench as the project.
- Do not claim outcome match until replay exists.

## Status

Index: `reports/work-session-index.md`. Extract: `python research/extract_replay.py` → `data/replay/` (gitignored). Goal prompt: `spec/matched-task-goal.md`. Replay into Kilo/OpenCode **not run** until you `/goal` that prompt.
