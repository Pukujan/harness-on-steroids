# Iteration loop — harness behavior like Codex

Stop condition is **owner-accepted match**, not a single analysis pass.

```text
loop i = 1, 2, 3, ...
  1. Measure Codex gold (full hashed JSONL): task splits + tool chains
  2. Write / update spec/codex-imitate-mode.md from that measurement
  3. Encode spec into Kilo mode (current Kilo model)
  4. Encode the same spec into OpenCode mode (including free models, build mode)
  5. Differential check: Kilo mode vs OpenCode mode vs spec (same required states)
  6. Measure Kilo + OpenCode sessions with the same process metrics as Codex
  7. Gap report: where they still do not imitate Codex
  8. If owner says match → stop. Else patch modes and goto 3
```

Required inner states (both products, every iteration):

- Do not start coding first
- Decompose into tasks
- Research / identify (tools that look) before mutate
- Chain tools the way Codex does (from gold analysis, not from papers)
- Verify after mutate
- Model text is not truth; tool results and sources are

Forbidden loop exits: “we ran SWE-bench instead”; “transcripts cannot be gold”; deleting tests.
