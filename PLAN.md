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

### E — Stop

Modes exist, spec exists, analysis of the full corpus exists. Then the owner says what is next.

## Explicitly out

- SWE-bench / SWE-bench Verified / Terminal-Bench / Harbor as the project
- mini-SWE-agent / “Codex-style agent” as a new product
- Using Codex to sit a new exam
- Treating literature as a veto of this plan
- 26 GitHub issues from the old campaign as a stall

## Quality gates (no exception)

Property tests, hidden holdout, mutation tests, metamorphic tests, differential tests, iteration-loop tests, and CI (`.github/workflows/owner-gate.yml`). Agents may not skip or delete them.

## 48-hour no-stop

See `CONTINUE.md`. Keep executing this plan until the owner stops you or the deadline and deliverables exist.

## Privacy still

No raw JSONL, sqlite, or chat bodies in git.
