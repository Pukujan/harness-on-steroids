# /goal — long matched-task + morph (copy-paste)

Morph = stretch eval (paraphrase / extra turns), not a JS file. Holdout = 6 longest threads.

```
Outcome: Imitate ChatGPT Work in Kilo and OpenCode. Long-running. Develop set = 16 Work threads (6–20 user turns). Hidden holdout = 6 threads (21+ user turns) scored last so we do not overfit. Extract is in gitignored data/replay/. Replay develop in Kilo Codex mode AND OpenCode (current models) as multi-turn threads. After tests/test_metamorphic.py tests/test_mutations.py tests/test_hidden_holdout.py stay green, add adversarial morphs of develop asks (paraphrase, gitignored) and replay those too. Score process R1–R6 AND outcome vs that Work execution (research, verification, ask addressed). Document harness changes so both products stay paired. Do not commit bodies. Do not print user.md. Do not SWE-bench. Do not start a new product.

Verification: pytest tests/test_metamorphic.py tests/test_mutations.py tests/test_hidden_holdout.py tests/test_long_replay_set.py tests/test_long_holdout.py tests/test_matched_task_eval.py -q green. reports/work-long-holdout.md has 16 develop + 6 holdout. Git scores are hashes only.

Constraints: codex_work_desktop. 8 singles are smoke. Keep owner-gate. Privacy. Scope: Kilo+OpenCode imitate Work only.

Boundaries: Not vscode. Not Harbor. Not public Codex re-test. Do not tune Codex mode text to holdout hashes. Do not stop after one short task.

Stop when: develop 16 have Kilo+OpenCode process+outcome notes; at least 3 develop hashes have a morph replay; holdout 6 scored once without further mode cherry-picks; owner can extend.
```
