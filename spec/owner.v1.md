# Owner spec v1 (spec-driven)

Normative machine copy: `spec/owner.v1.json`.

Agents may not skip this. CI is the gate. No exceptions.

## Claims

1. The user owns the project.
2. Local Codex / ChatGPT Work transcripts are **gold behavior**.
3. Work is: analyze **all** transcripts for task splits and tool chains; make **Kilo** and **OpenCode** (including free models, build mode) imitate that via a **mode**.
4. Do not invent a public exam. Do not re-test Codex. Do not replace this with SWE-bench / Harbor / mini-SWE-agent.
5. Iterate until harness behavior matches Codex gold (issue 12).

## Evidence

- Docs: `AGENTS.md`, `PLAN.md`, `HANDOFF.md`, `ISSUES.md`
- Tests: `tests/test_*.py`
- CI: `.github/workflows/owner-gate.yml`
