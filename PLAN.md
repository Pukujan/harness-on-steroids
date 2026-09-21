# Plan (owner) — Codex transcripts are gold; Kilo and OpenCode imitate them

Owner: Pujan. Agents execute this. They do not replace it.

## Goal

1. **Analyze every local Codex / ChatGPT Work transcript** (sessions + archived rollouts).
2. **Write down** how Codex classifies work into multiple **tasks** and **tool-call chains**.
3. Make **Kilo** and **OpenCode** behave that way: a dedicated **mode** (and skills/routing as needed) that copies Codex, using **current Kilo models** and **any OpenCode model including free ones in build mode**.

No public coding exam. No “Codex-style mini agent.” No re-testing Codex. The transcripts are the dataset.

## Gold standard

Codex behavior in the local JSONL is the reference:

- How a request is split into tasks / sub-agents / plans
- Order of tools (read/search vs exec vs patch vs wait vs spawn)
- When it researches vs when it edits vs when it checks
- Multi-tool and multi-task structure

Kilo and OpenCode should follow **that**, not a paper benchmark.

## Corpus (already on this PC)

- `%USERPROFILE%\.codex\sessions\**\rollout-*.jsonl`
- `%USERPROFILE%\.codex\archived_sessions\**\rollout-*.jsonl`
- Indexes: `thread_history_1.sqlite`, `state_5.sqlite` (metadata / item_type; no bodies in git)
- Hashed copies: `data/raw/` (gitignored). Copy-hash is **done** (~1518 files). Do not recopy unless files changed.
- Not corpus: Brave, Chromium cache, chatgpt.com Cloud ZIP (absent)

## Steps

### A — Full transcript analysis (now)

Stream **all** hashed JSONL. No message bodies in git.

Produce:

- `reports/codex-gold-behavior.md` — task split, tool-chain patterns, sub-agent/plan/exec mix, sequence shapes
- Supporting count tables under `reports/` as needed

Must cover **all** files, not a 40-file sample.

### B — Durable spec

`spec/codex-imitate-mode.md` — state machine / routing a coding agent must follow to imitate Codex (decompose, research, tool mix, verify). Written from **A**, not from SWE-bench papers.

### C — Kilo mode

Add a selectable Kilo **agent/mode** (`.kilo/agent/` and/or global `~/.config/kilo/`) plus skill if needed, named so a human can pick “behave like Codex.” Works with whatever model Kilo is using.

### D — OpenCode mode

Same behavior for OpenCode build mode, including free models. Agent/instruction/skill in OpenCode’s config layout.

### E — Stop (process layer)

Modes exist, spec exists, analysis of the full corpus exists. Process scorer (R1–R6) stays. Then the owner says what is next.

### F — Matched-task outcome (owner)

Tool-call histograms are **not** the final result. Replay **the same local Work asks** into Kilo and OpenCode Codex mode (current models). Score **observable work**: research, verification, files/tests, whether the ask was addressed. Process scores stay as a layer.

Prompts live only under gitignored `data/replay/`. Never commit bodies. Not SWE-bench. Not a public exam. Not re-testing Codex on Harbor.

Spec: `spec/matched-task-eval.md`. Index: `reports/work-session-index.md`. Long set: `reports/work-long-replay-set.md`. Holdout: `reports/work-long-holdout.md`. Morph = stretch eval (paraphrase / multi-turn), not a JS file. Replay **not complete**.

### G — Work research, planning, provenance (not only tools)

Tool-call histograms are not how Work researches or plans. Work treats **tool output as memory**. It waits on cells, then writes a short brief to a named child. It does not keep an 832k chat as the plan. **Do not treat the chat as the project.**

Counts only. No message bodies in git. Produce reports, then recode into `spec/codex-imitate-mode.md` and both Codex modes:

- Assistant-turn shape (speak before first tool / after last; length bands)
- `send_message` brief structure (the plan is that message; `update_plan` is 0)
- User-turn classes (question / go / correction)
- `compacted` events (listed in the corpus, never opened)

**Synthesize late:** child brief, user answer, or git checkpoint — not a plan file, not a running novel.

Research gates (Work-like, testable):

- **Valid:** claim tied to a tool result, or **not observed**
- **Enough:** the target of the next action was actually read; stop if nothing to look up
- **Action reliable:** no send/write until that; look/test after write
- **Provenance:** path / command / hash when the answer needs the repo; JOURNAL is not fact

Do not build a summarizer first. Lost in the Middle / RULER / LLMLingua / MemGPT are warnings, not the exam. Spec: `spec/work-research-gates.md`. **Not complete.**

### H — Durable evidence (this repo)

Scratchpad = git checkpoint, not in-window compression. Non-destructive PCM-shaped files (`checkpoints/CURRENT.md`, one active task) if they do not overwrite `AGENTS.md` / `PLAN.md` / `HANDOFF.md`. Owner gold stays. New sessions read CURRENT, not this chat.

### I — Portable Codex pack

After G is in the spec: harness-neutral loop + Kilo/OpenCode adapters. Pi/Hermes later. Not a new Codex-clone product.

## Explicitly out

- SWE-bench / SWE-bench Verified / Terminal-Bench / Harbor as the project
- mini-SWE-agent / “Codex-style agent” as a new product
- Using Codex to sit a new exam
- Treating literature as a veto of this plan
- 26 GitHub issues from the old campaign as a stall
- A summarizer / compressor as the project or as session memory

## Quality gates (no exception)

Property tests, hidden holdout, mutation tests, metamorphic tests, differential tests, iteration-loop tests, and CI (`.github/workflows/owner-gate.yml`). Agents may not skip or delete them. New code follows `spec/repo-modules.md`. Ruff/mypy on `src/` (issue 18).

## 48-hour no-stop

See `CONTINUE.md`. After `/goal` and owner go, keep executing this plan until the owner stops you or the deadline and deliverables exist. Ordinary chat still answers first.

## Privacy still

No raw JSONL, sqlite, or chat bodies in git.
