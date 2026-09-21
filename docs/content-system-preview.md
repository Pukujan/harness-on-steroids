# Harness on steroids — content-system preview

> Review artifact for `TASK-0015`. This is a proposed story and visual direction; it does not replace `README.md`.

## Start here

A coding agent can be clever and still be hard to trust. **The failure often lives in the loop around the model**: it edits before looking, guesses while a tool is still running, splits work too early, or stops without checking what changed.

![Coding agents need a loop](content-system-assets/hero.png)

## The problem with the agent

The same model behaves differently depending on the wrapper around it. A rushed wrapper turns a capable model into a brittle collaborator; a careful wrapper gives it time to **inspect, wait, divide the work, act, and verify**. That difference is easy to feel in a real repository and surprisingly easy to hide behind a polished final answer.

## What this repository is

Harness on steroids is a research project about that surrounding behavior. It treats **local ChatGPT Work / Codex desktop transcripts as the reference process**, analyzes the full copy-hashed corpus, and writes the useful patterns into a mode that Kilo and OpenCode can follow.

This is not a new “Codex clone.” It is a durable attempt to answer a narrower question: *what did the reliable workflow actually do, and can another wrapper reproduce those habits with the models it already uses?*

## How it tackles the gap

1. **Look before changing anything.** Read the project contract and inspect the smallest useful surface first.
2. **Wait instead of guessing.** Treat slow tools as state that needs observation, not as an invitation to invent progress.
3. **Split after reconnaissance.** Send named work only after the shape of the problem is visible.
4. **Verify the result.** A good-sounding response is not evidence; files, tests, and observed outputs are.

![The reliable loop](content-system-assets/supporting-square.png)

## The technical shape

The corpus is **copied and hashed before parsing**; raw JSONL, SQLite, and message bodies stay out of Git. Reports separate ChatGPT Work from other Codex surfaces so the reference behavior is not diluted. The written mode spec then has paired implementations in `.kilo/agent/codex.md` and `.opencode/agent/codex.md`, with process checks in `src/score_session.py`.

The project also keeps a harder question open: **process similarity is not outcome reliability**. Matched long Work tasks, morphs, holdouts, mutation tests, and differential checks are part of the plan because “used the right tools” is not enough.

## What it deliberately does not claim

It does not turn a transcript into universal truth, run SWE-bench as a substitute for the owner's corpus, or claim that a mode is finished because a short demo looks good. **The recipe is written; outcome replay is still in progress.**

## Review questions

- Can a first-time reader explain the inspect–act–verify idea after twenty seconds?
- Does the story distinguish the reference process from the unfinished outcome evaluation?
- Are the claims tied to `AGENTS.md`, `PLAN.md`, `HANDOFF.md`, specs, reports, or tests?
- Does the image title orient the reader without covering the people or robot?

## Contract used

This preview pins `content-generation-modules@0.1.2` at `cb8c18f`. Canonical repository files remain unchanged until review.
