# /goal — long matched-task outcome (copy-paste)

Primary exam is **long Work threads**, not the 8 singles.

```
Outcome: Long-running matched-task eval. Primary set = 16 Work sessions with 6–20 user turns plus 6 with 21+ turns (reports/work-long-replay-set.md). Extract already in gitignored data/replay/. Replay each into Kilo Codex mode AND OpenCode Codex/build (current models) as multi-turn threads, not one-shot. After pytest metamorphic tests stay green, morph each ask (paraphrase in data/replay/<hash>/morphs/, never git) and replay morphs the same way. Score process R1–R6 AND observable outcome vs that Work session’s execution (research, verification, files/tests, asks addressed). Do not commit bodies. Do not print user.md. Do not SWE-bench.

Verification: pytest tests/test_metamorphic.py tests/test_matched_task_eval.py tests/test_extract_replay.py tests/test_work_replay_buckets.py tests/test_long_replay_set.py -q green. reports/work-long-replay-set.md lists 22 hashes. scores use hashes only in git; details in data/replay/scores.md.

Constraints: codex_work_desktop only. 8 singles are optional smoke, not the stop condition. Keep owner-gate. Privacy.

Boundaries: Not vscode. Not Harbor. Not a public Codex re-test. Do not stop after one short task.

Stop when: all 22 long threads have at least a Kilo process+outcome note and an OpenCode process+outcome note (hashes only in git); morphs attempted on a subset (≥3 hashes); owner can extend.
```
