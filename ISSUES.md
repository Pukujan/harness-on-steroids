# Issue log (owner) — no skips, no exceptions

This file is the durable work log. Later agents read `AGENTS.md`, `PLAN.md`, then this. Closing an issue requires the **command** to pass in CI, not a prose claim.

**48-hour no-stop:** `CONTINUE.md`. Do not wait for the owner. Work issues in order.

**Document + push:** append `research/JOURNAL.md` after real work. Occasional push of specs/tests/reports/modes. Never push `data/` or transcripts.

Status: `open` | `in_progress` | `done`

## Gate issues (must stay green forever)

### 1. Owner spec (spec-driven)

- **Status:** done
- **Goal:** Machine spec of owner rules (Codex transcripts gold; analyze all; Kilo+OpenCode imitate; no SWE-bench substitute).
- **Files:** `spec/owner.v1.json`, `spec/owner.v1.md`, `spec/iteration-loop.md`
- **Command:** `pytest tests/test_properties.py -q`
- **Pass:** spec file validates; docs contain required claims
- **Parent:** none

### 2. Property tests

- **Status:** done
- **Goal:** Properties over `AGENTS.md` / `PLAN.md` / `HANDOFF.md` that fail if gold/imitate/no-exam rules are deleted.
- **Files:** `src/owner_invariants.py`, `tests/test_properties.py`
- **Command:** `pytest tests/test_properties.py -q`
- **Pass:** all properties green on current docs

### 3. Hidden holdout

- **Status:** done
- **Goal:** Extra sha256 needles not listed as plaintext in the spec. Rewording away the owner sentences fails CI.
- **Files:** `tests/holdout/holdout_sha256.json`, `tests/test_hidden_holdout.py`
- **Command:** `pytest tests/test_hidden_holdout.py -q`
- **Pass:** every holdout hash matches a substring of AGENTS.md or PLAN.md

### 4. Mutation tests

- **Status:** done
- **Goal:** If gold/imitate clauses are stripped or SWE-bench is installed as the goal, property+holdout tests **must fail**. If they still pass, the suite is weak.
- **Files:** `tests/test_mutations.py`
- **Command:** `pytest tests/test_mutations.py -q`
- **Pass:** each mutation is caught

### 5. Metamorphic tests

- **Status:** done
- **Goal:** Harmless transforms (whitespace, extra blank lines) still pass; Kilo-mode vs OpenCode-mode must stay equivalent once both exist.
- **Files:** `tests/test_metamorphic.py`
- **Command:** `pytest tests/test_metamorphic.py -q`
- **Pass:** all metamorphic relations hold

### 6. Differential validation

- **Status:** done
- **Goal:** Two independent checkers agree. AGENTS.md and PLAN.md do not contradict. Future Kilo vs OpenCode mode files must both satisfy the same behavior requirements.
- **Files:** `tests/test_differential.py`
- **Command:** `pytest tests/test_differential.py -q`
- **Pass:** checkers agree; no goal contradiction

### 7. CI/CD — no skip

- **Status:** done
- **Goal:** GitHub Actions runs properties, holdout, mutations, metamorphic, differential. No `continue-on-error`. Workflow cannot be a no-op.
- **Files:** `.github/workflows/owner-gate.yml`, `tests/test_ci_contract.py`, `pyproject.toml`
- **Command:** `pytest tests/test_ci_contract.py -q`
- **Pass:** workflow present, required jobs listed, local pytest green

## Delivery issues (the actual product)

### 8. Full Codex gold-behavior analysis

- **Status:** done
- **Goal:** Parse **all** hashed Codex JSONL. How Codex splits tasks and chains tools. No bodies in git.
- **Files:** `reports/codex-gold-behavior.md`
- **Command:** `pytest tests/test_imitate_modes.py tests/test_work_vs_vscode.py -q`
- **Notes:** hashed **1521**; Work **87** files; originator split in `reports/codex-by-originator.md`. 1518 snapshot in `reports/versions/v22/`.
- **Pass:** report exists; states file count 1521; task-split + tool-chain sections; Work not averaged with vscode
- **Parent:** 1

### 9. Imitate-Codex mode spec

- **Status:** done
- **Goal:** `spec/codex-imitate-mode.md` from issue 8, not from SWE-bench papers.
- **Files:** `spec/codex-imitate-mode.md`
- **Command:** `pytest tests/test_imitate_modes.py -q`
- **Pass:** spec lists required harness states (decompose, research, tool chain, verify) for both products
- **Parent:** 8

### 10. Kilo Codex-imitate mode

- **Status:** done
- **Goal:** Selectable Kilo agent/mode using whatever model Kilo is using now.
- **Files:** `.kilo/agent/codex.md` and global `~/.config/kilo/agent/codex.md`
- **Command:** `pytest tests/test_imitate_modes.py tests/test_work_shapes.py -q`
- **Pass:** mode exists and encodes spec 9
- **Parent:** 9

### 11. OpenCode Codex-imitate mode

- **Status:** done
- **Goal:** Same behavior in OpenCode build mode, including free models.
- **Files:** `.opencode/agent/codex.md` and global OpenCode agent
- **Command:** `pytest tests/test_imitate_modes.py tests/test_metamorphic.py -q`
- **Pass:** mode exists and is differentially equivalent to issue 10 on spec 9
- **Parent:** 9

### 12. Iteration loop until behavior matches

- **Status:** in_progress
- **Goal:** Repeat: measure Kilo+OpenCode sessions against Codex gold process → patch modes → measure again. Stop only when owner says the harness behavior matches.
- **Files:** `spec/iteration-loop.md`, `reports/imitate-gap.md`, `src/score_session.py`
- **Command:** `pytest tests/test_iteration_loop.py tests/test_score_session.py -q`
- **Notes:** work_match Work 81/83, Kilo **1/13** (skip plan). OpenCode 4/21. Live sqlite 18:24Z: Kilo `code` 14/`plan` 7; OpenCode `build` 96/`luna` 48/… — **neither product stores `agent=codex`** even though `/goal` sets `agent: codex`. Owner has not said match.
- **Pass:** loop documented; gap report after modes exist; owner-accepted match
- **Parent:** 10, 11

## Rules for agents

- Do not close 1–7 by deleting tests.
- Do not replace 8–12 with SWE-bench, Harbor, or a new Codex-clone product.
- Do not commit `data/` or message bodies.
