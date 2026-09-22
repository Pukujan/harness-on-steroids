# Sol Handoff — `hermes-developer-bootstrap`

Read this first. Then `SOL_CONTEXT_PACK.md`. Chat history is disposable.

## Role split

- **Sol (cloud):** architecture, research, review, durable plan. You own the plan.
- **Luna (local):** cheap bounded executor only, after the plan exists. Granular tickets, 600-second window, streamed provider calls.
- **Repo/docs/issues:** memory. Do not rely on Hermes personal memory or compressor summaries.

## What the owner wants

A community-shareable **developer-first** Hermes bootstrap/SDK, not a personal bot.

Canonical name: **`hermes-developer-bootstrap`**.

Hermes defaults that the owner wants bypassed, then measured:

1. Lossy context compression that rots long-horizon work.
2. Personal/user memory that is rarely useful and often harmful.
3. Eager tools, plugins, MCP, and skills that inflate every prompt.

Replacement hypothesis: project artifacts + explicit state machine + checkpoint/handoff packets + lazy capabilities. Continuity should look like git issues, `HANDOFF.md`, and fresh sessions — not MEMORY.md / USER.md / compressor prose.

Do **not** freeze that architecture yet. First distinguish where tokens actually go.

## Authority pattern to copy

Sibling repos (Finance Quant, Fossil Core, Financial Analysis Demo) treat the repository as the coordination layer:

- mandatory read order
- frozen invariants vs replaceable adapters
- bounded work packets
- evaluation claims from reproducible artifacts, not demos

Prefer: upstream pin → thin adapter → constrained extension → fork last.

## What is actually done vs claimed

This session did **not** install Hermes, did **not** mutate LiteLLM, did **not** rotate any key, and did **not** run a new model matrix.

Observed on disk:

| Item | Status |
|---|---|
| Local dir `D:\claude\hermes-developer-bootstrap` | missing |
| `SOL_HANDOFF.md` / `SOL_CONTEXT_PACK.md` in this worktree | this packet |
| Sibling experimental tree `D:\claude\hermes-lean-bootstrap` | exists; treat as **local prototype evidence**, not the product repo |
| Fossil Core coordination docs | pattern reference only; do not mix FOSSIL work into this product |

A later local prototype in `hermes-lean-bootstrap` already contains charter, streamed route-gate code, checkpoint types, an **uninstalled** no-loss context-engine stub, and dated evidence files. Those claims must be re-verified before they become architecture. Do not treat them as production proof.

## Interrupted / incomplete work (do not paper over)

Prior local turns were aborted repeatedly. Do not assume LiteLLM repair, Hermes profiles, RTK/Caveman, or plugin install finished.

Owner corrections that still stand:

- Model is **MiniMax M3**, not Kimi Max.
- Completions must be **streamed**.
- Local proxy key is local-only: **do not rotate, print, or commit it**.
- OpenCode already talks to the same proxy successfully; do not invent a “must add a DB” fix from a transient `No connected db` catalog error.
- Do not start a broad Hermes-core rewrite, LiteLLM campaign, or memory redesign as the first slice.

## First problem (Sol must keep this order)

Not “fix Hermes memory.” That is a large semantic problem.

First tractable slice: **capability-prompt tax** — how much context is consumed because tools/plugins/MCP/skills exist, not because the task needs them.

Tiny experimental loop:

1. Measure token anatomy on a few representative configs.
2. Change one boundary.
3. Measure again.

No SDD/TDD/giant backlog until that bottleneck is identified.

## What Sol should produce

A staged plan so Luna never invents architecture. Include:

1. SDK-vs-Hermes-adapter boundary (recommendation: **SDK first, thin Hermes adapter second**).
2. Durable schemas: project, task, checkpoint, handoff, evidence, provenance, capability contracts, legal transitions.
3. Minimal context-packet compiler + lazy capability gateway.
4. Reversible profile to disable Hermes personal memory and lossy compression without forking core.
5. Evaluation that can reject a change: tokens down, failures not up, long-horizon recovery not worse, no secret/state leak, fresh-session works.
6. Dependency-ordered Luna tickets: one artifact, one verify command, ≤600s each.

## Hard non-goals for Luna

- Fork or rewrite Hermes core
- Change live LiteLLM routing/credentials
- Activate an experimental context engine in the live Hermes home
- Install RTK/Caveman as a default
- Claim payload-census savings as live Hermes proof
- Treat gateway fallback as the requested model succeeding
