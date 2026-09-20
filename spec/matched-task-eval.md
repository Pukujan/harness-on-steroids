# Matched-task eval (owner want)

Owner: tool-call histograms are **not** the result. Want Kilo and OpenCode to run **the same Work tasks** as **long threads** and be scored on **observable work** and **Work’s own execution**, not only who called which tool.

## Gold still

Local ChatGPT Work transcripts (`codex_work_desktop`). Not vscode. Not SWE-bench. Not Harbor. Not re-testing Codex on a public bench.

## Primary set (not the 8 singles)

- **16** sessions with 6–20 user turns
- **6** sessions with 21+ user turns
- List: `reports/work-long-replay-set.md`
- 8 single-turn sessions are **smoke only**

## What to compare

For each hash:

1. **Process** — R1–R6 / work_match (keep; cheap CI).
2. **Research / verification** — look before change; look/run after change.
3. **Outcome vs that Work run** — did Kilo/OpenCode address the same asks (files, tests, checks), not “same bytes as Codex.”
4. **Metamorphic morphs** — paraphrase the ask (gitignored); same scores must not collapse; `tests/test_metamorphic.py` stays for docs/modes.

## Privacy

Never commit message bodies. Do not stand up SWE-bench as the project. Replay + morphs only under `data/replay/`. Git: hashes, counts, scores without quotes.

## Status

Extract exists locally for 82/87. Long-set list is in git. Full 22-thread Kilo+OpenCode replay **not complete**.
