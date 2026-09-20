# Same test for everyone (runbook, not executed)

Plain meaning: one worksheet, three students. Not “replay a Codex chat.”

## The worksheet

A public item with starting code and **hidden** checks. First coding worksheet: SWE-bench Verified (500 GitHub issues). First terminal worksheet: Terminal-Bench via Harbor.

This machine has `uv`. It does **not** have `harbor` or `mini` installed. Do not install or burn API quota until a human says iteration 0 exam may run.

## Three students (same item id)

| Student | How they sit the exam | Do not |
| --- | --- | --- |
| Codex-style baseline | mini-SWE-agent (bash only) on the item | Feed it a private ChatGPT transcript |
| Kilo | Kilo CLI in the same docker/workdir as the item | Different bug than the others |
| OpenCode | OpenCode CLI in that same workdir | Study-OS sessions as if they were the exam |

Score = hidden tests green. Optional extra: process ticks (read before write, test after edit). Process ticks are **not** “matched Codex tool names.”

## Commands we would run later (not now)

Harbor / Terminal-Bench:

```text
uv tool install "harbor[modal]"
uv run harbor run -d terminal-bench/terminal-bench@latest --agent oracle --n-concurrent 1 --env modal
```

Then the same dataset with `--agent` wrappers for Kilo and OpenCode once those wrappers exist.

SWE-bench Verified (mini-swe-agent batch) is documented at mini-swe-agent.com usage/swebench. Same instance list for every harness.

## Iteration 0

Do not run the exam overnight. Do not recopy JSONL. Do not patch Kilo.

Morning: human picks “tiny dry-run” (1–5 items) vs “full Verified.”
