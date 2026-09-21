# Owner decisions and handoff

Status: **architecture reviewed; owner acceptance pending**. The review resolves the decision questions into recommended planning defaults so implementation does not need to guess. These defaults do not supersede `AGENTS.md` or `PLAN.md` until the owner explicitly accepts the reset.

## Resolved planning defaults

| Decision | Recommended resolution |
| --- | --- |
| 1. Priority order | Treat **safety/scope, authority, evidence integrity, and privacy as hard constraints**, not tradeable priorities. Within those constraints optimize lexicographically for: verified task outcome; research/evidence sufficiency; recovery/continuity; honest UX; useful delegation; latency/cost; stylistic similarity. |
| 2. Reference population | Primary normative evidence remains the full versioned `codex_work_desktop` population, including empty/no-call sessions for stop/UX behavior. Tool-process denominators distinguish sessions with calls. Other originators/clients (vscode, codex_exec, desktop variants) remain comparison/control strata unless separately approved; never average them into Work gold. Preserve model/client/time metadata and report coverage explicitly. |
| 3. Environment fidelity | Use a tiered fidelity record. Required for a comparable matched task: starting workspace/repo revision or reconstructable state, relevant files/artifacts, required tools, authority/permissions, and material external dependencies. Run mutations in isolated worktrees/sandboxes. If an essential dependency cannot be reconstructed, mark the run **non-comparable** or degraded rather than silently scoring it as a behavioral failure. |
| 4. Outcome identity | Freeze a per-task acceptance contract before replay: user intent/scope, required artifact or state change, relevant checks/tests, authority constraints, and forbidden side effects. Semantically equivalent implementations count. A Work run that was partial/blocked/failed stays labeled that way; its exact implementation is not retroactively the only correct outcome. |
| 5. Model matrix | Record exact provider/model/version for every run. Require (a) a cross-harness common model stratum where technically available to isolate harness effects and (b) each harness's realistic native/default model stratum. Add a constrained/free-model stress stratum where supported; do not fabricate parity when a model is unavailable on a harness. |
| 6. Enforcement budget | Runtime-enforce permission/authority boundaries, negotiated capability truth, event/result linkage, terminal async observation, and completion evidence wherever the host can enforce them. Material mutation verification is required for full conformance; if a host can only advise it, declare degraded conformance. Research sufficiency, decomposition choice, update timing, delegation choice, and prose style remain semantic/advisory until a reliable verifier exists. |
| 7. Variation tolerance | Accept different native tools, wording, number of steps, decomposition, and serialized-vs-delegated execution when dependencies, evidence, authority, verification, and outcome are equivalent. Disqualifying differences include unauthorized mutation/send, fabricated evidence, false completion, skipped required verification, ignored explicit correction/stop, capability misrepresentation, privacy leakage, or hidden unresolved required dependencies. |
| 8. Annotation authority | Maintain a versioned annotation handbook. Double-annotate a stratified sample plus all rare/high-risk classes; adjudicate disagreements with a third reviewer or designated research maintainer. Record both pre-adjudication disagreement and final labels. Do not harden a disputed behavior into a protocol invariant until agreement is demonstrably reliable; thresholds are frozen before adapter tuning. |
| 9. Privacy boundary | Confirm public Git contains only schemas, aggregate/structural evidence, approved hashes/aliases, redacted examples, tests, and derived reports. Raw JSONL/SQLite, transcript/prompt bodies, credentials, private account exports, user artifacts, raw paths/account IDs, and reversible content-derived identifiers stay local. Prefer keyed/HMAC-derived local IDs for newly derived sensitive identifiers. |
| 10. Repository reset policy | Preserve governance, issue/history logs, versioned reports, hashed-corpus methodology, owner-gate tests, replay evidence utilities, and current Kilo/OpenCode modes as historical/prototype artifacts. Freeze `spec/codex-imitate-mode.md` as v0 history. Build new protocol/evidence/verifier/adapter modules behind `src/hos/`; wrap before replacing. Delete or relocate old modules only after replacement tests and an audit mapping exist. |

## Review amendments that are now required by the planning package

1. **Hierarchical lifecycle:** represent run, task graph, and attempt phases separately so delegation, concurrency, waits, retries, and verification do not collapse into one linear state.
2. **Explicit capability negotiation:** persist a negotiated profile containing protocol/adapter/manifest versions, selected lowerings, enforced versus advisory invariants, degraded guarantees, and incompatibilities.
3. **Normative definitions:** define consequential action, material mutation, authority boundary, and verified scope independently of product-specific tool names.
4. **Version compatibility:** protocol, event schema, capability manifest, and adapter versions are recorded on every evaluated run; breaking changes require explicit version transitions.
5. **Comparable-outcome rules:** acceptance contracts and environment-fidelity rules are frozen before tuning; unreconstructable tasks are labeled non-comparable rather than converted into failures.
6. **Evaluation attribution:** compare reference Work, native harness, and adapter mode; match models across harnesses where possible and keep unmatched strata separate.
7. **Privacy-safe identifiers:** new derived identifiers must not create a reversible public fingerprint of private content.
8. **Governance switch:** if the owner accepts this reset, update `AGENTS.md`, `PLAN.md`, `ISSUES.md`, and owner invariants/tests in one dedicated governance change before implementation. Until that change, the old owner plan remains authoritative.

## Proposed next authorized slice after acceptance

Do **not** start with a prompt rewrite. Start with a read-only contract/evidence slice:

1. map current repo claims to the reviewed architecture and classify each as normative, diagnostic, historical, or unresolved;
2. inventory the upstream exporter schema and local Work corpus without copying bodies;
3. propose versioned event/context/index and negotiated-profile schemas;
4. run the missing UX/research/compaction measurements;
5. publish the annotation handbook plus an adjudicated sample/disagreement report;
6. return with protocol v1 draft, verifier fixtures, coverage report, and migration map for approval.

Only then should a `/goal` or long-running implementation loop be considered.

## Current handoff state

- Package branch: `planning/harness-agnostic-context`.
- Architecture review: completed in `11-owner-review.md`.
- Owner acceptance of the reset: **pending**.
- Existing implementation: preserved and untouched by this review.
- Existing issues 13–18: remain historical/open/in-progress as recorded until the governance switch.
- No adapter implementation, prompt rewrite, replay run, cleanup, or raw transcript/body export is authorized by this review.

## Completion definition for this review task

The review task is complete when these resolutions and amendments are committed and pushed. Issue 19 itself remains open until the owner explicitly accepts the reset and the governance source-of-truth files are updated.
