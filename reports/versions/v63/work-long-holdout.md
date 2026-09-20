# Long-thread develop vs hidden holdout

v63. Hashes only. **Do not tune modes or spec anecdotes to holdout hashes.**

## Develop (n=16, the 6–20 band)

Use these to write morphs, iterate Codex mode, and report.

`0d6ca4607eaf` `1a415bc257e5` `1b09f49da9b9` `28372e365066` `2bde00530ddd` `633c140546c0` `6b1cd28c4803` `6e412585c223` `6eb8631b71ff` `74841f3cc419` `76b12d5e1a66` `8d42bc26b8ea` `a5842562d1c9` `b7e6393f4c14` `bd179678f540` `f37de8488162`

## Hidden holdout (n=6, the 21+ band)

Score last. Do not cherry-pick these while editing `.kilo/agent/codex.md` or `.opencode/agent/codex.md`.

`0aecd1eabdf2` `1442d08cf2d3` `3a749176fae1` `45ca341b6f6c` `555f9c94ba8e` `55fd1ef9b613`

If holdout process+outcome is much worse than develop, the harness overfit the mid band. Mutation tests (`tests/test_mutations.py`) and owner-doc holdout (`tests/test_hidden_holdout.py`) stay; this file is the **task** holdout.
