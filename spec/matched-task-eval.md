# Matched-task eval (owner want)

Owner: tool-call histograms are **not** the result. Want Kilo and OpenCode to run **the same Work tasks** as **long threads** and be scored on **observable work** vs Work’s execution.

## Gold still

`codex_work_desktop`. Not vscode. Not SWE-bench. Not Harbor.

## Morph (not a JS file)

**Morph** = stretch the eval without leaving the main goal:

- **Vertical:** same Work jobs, deeper score (research, verification, outcome), multi-turn, not one-shot.
- **Horizontal:** more sessions + **adversarial paraphrases** of the ask (gitignored `data/replay/<hash>/morphs/`). Same job, warped wording; harness should still look, wait/send, verify.
- **Scope control:** still imitate Work in Kilo and OpenCode only. No new product. No SWE-bench.

Fuzz goal extents after `tests/test_metamorphic.py` stays green. Beware **task/test overfitting**.

## Sets

- Develop: 16 hashes (6–20 user turns) — `reports/work-long-holdout.md`
- Hidden holdout: 6 hashes (21+) — score last
- 8 singles: smoke only
- Owner-doc holdout + mutation tests: keep (`tests/test_hidden_holdout.py`, `tests/test_mutations.py`)

## Compare

Process R1–R6 (CI). Outcome vs that Work run. Morphs must not collapse scores. Document harness diffs so they reproduce on both products.

## Privacy

Never commit message bodies. Do not stand up SWE-bench as the project.

## Status

22 hashes listed. Holdout split listed. Full Kilo+OpenCode long replay **not complete**.
