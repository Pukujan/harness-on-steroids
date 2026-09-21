# /goal — long matched-task + morph (copy-paste)

Morph = stretch eval (paraphrase / extra turns), not a JS file. Holdout = 6 longest threads.

Reload if Kilo `/goal` 500s. Do **not** add `.kilo/command/goal.md`. Paste into **Set goal**, not `resume`.

```
Outcome: Imitate ChatGPT Work in Kilo and OpenCode. Long-running. Develop set = 16 Work threads (6–20 user turns). Hidden holdout = 6 threads (21+ user turns) scored last so we do not overfit. Extract is in gitignored data/replay/. Replay develop in Kilo Codex mode AND OpenCode (current models) as multi-turn threads. After tests/test_metamorphic.py tests/test_mutations.py tests/test_hidden_holdout.py stay green, add adversarial morphs of develop asks (paraphrase, gitignored) and replay those too. Score process R1–R6 AND outcome vs that Work execution (research, verification, ask addressed). Document harness changes so both products stay paired. Do not commit bodies. Do not print user.md. Do not SWE-bench. Do not start a new product.

Now: reports/replay-scores.md v65. Kilo cells on all 16+6. OpenCode develop 14/16; timeouts 633c140546c0 and 6eb8631b71ff. Morph *replays* with tools: at least 0d6ca4607eaf, 2bde00530ddd, 6e412585c223 (stop rule ≥3 met). Holdout OpenCode still pending. Gitignored .env has OpenRouter/OpenCode/Zen keys (subset from OneDrive configs/.env). OpenCode CLI already has Zen in auth.json. Default yolo-auto/qwen3.8-flash is NOT required.

Next: (1) one-turn streamed retries: python research/run_opencode_replay.py 633c140546c0 --max-turns 1 --model opencode/glm-5.3-flash then 6eb8631b71ff the same way. If Zen 403/empty, try --model openrouter/z-ai/glm-5.2:free (429 means key works, wait). (2) python research/score_replay_copies.py. (3) holdout OpenCode last, one hash one turn, do not edit Codex modes for holdout. (4) pytest green.

How: one hash, one user turn, --format json, flush to disk, 180s cap. Isolated oc-sandbox. --agent codex. Never bundle long OpenCode runs. Never print user.md. Never commit .env or data/.

Verification: pytest tests/test_metamorphic.py tests/test_mutations.py tests/test_hidden_holdout.py tests/test_long_replay_set.py tests/test_long_holdout.py tests/test_matched_task_eval.py tests/test_replay_scores.py -q green. reports/work-long-holdout.md has 16 develop + 6 holdout. Git scores are hashes only. Free model ids: reports/free-models.md.

Constraints: codex_work_desktop. 8 singles are smoke. Keep owner-gate. Privacy. Scope: Kilo+OpenCode imitate Work only. Clocks: 20h floor 2026-09-21T12:05Z; 48h 2026-09-22T05:58Z.

Boundaries: Not vscode. Not Harbor. Not public Codex re-test. Do not tune Codex mode text to holdout hashes. Do not stop after one short task. Do not shadow Kilo /goal with command/goal.md. Do not copy the whole OneDrive secrets dump.

Stop when: develop 16 have Kilo+OpenCode process+outcome notes; at least 3 develop hashes have a morph replay; holdout 6 scored once without further mode cherry-picks; owner can extend.
```
