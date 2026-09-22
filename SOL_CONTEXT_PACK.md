# Sol Context Pack — `hermes-developer-bootstrap`

Architecture/planning packet. No credentials, no raw proxy keys, no user memory dumps, no chat transcript as authority.

## Product identity

Developer harness for long projects. Hermes should stop acting like a personal assistant that remembers the user, and start acting like a coding harness that treats context, attention, and project tasks as explicit state.

```text
project artifacts + state machine + provenance
                    ↓
       minimal task/context packet compiler
                    ↓
 lazy capabilities + model/provider routing + bounded delegation
                    ↓
 Hermes adapter (optional) or another agent harness
```

Rule:

> Compute and model context are disposable; verified project state is durable.

## Owner problems (test, do not assume)

| Symptom | Owner hypothesis | Test note |
|---|---|---|
| Token blow-up | Huge system prompt + eager tool schemas + skills/MCP | Measure anatomy before redesign |
| Context rot | Hermes compressor keeps too much, loses provenance | Compare default / off / conservative / checkpoint engine |
| Bad long-horizon recovery | Memory + compression as continuity | Disable memory; use checkpoint + new session |
| Hallucination without provenance | Free-form prose state | State machine + evidence receipts |
| Skills mostly unused | Catalog still costs tokens | No skills / index only / one skill |

Secondary ideas (separate experiments, not the first architecture freeze):

- Lazy MCP/tools via a gateway or Tool Search; core Hermes tools cannot all be deferred.
- Router/delegator profiles only if root+child+overhead < single-agent tokens.
- RTK (terminal output) and Caveman independently, then together.
- Skill-building for long tasks: skeptical; measure.

## Intended durable artifacts

| Artifact | Authority |
|---|---|
| `PROJECT.md` | mission, scope, invariants, non-goals |
| `ARCHITECTURE.md` | accepted design + reconsideration triggers |
| issues / `TASKS.md` | task graph, claims, lifecycle |
| `CHECKPOINT.json` | bounded machine-readable resume state |
| `HANDOFF.md` | short human next-session packet |
| evidence receipts | tests, commands, artifacts, model identity |

Transcript, USER.md, MEMORY.md, compressor summaries, and model confidence are **not** authority.

## State-machine intent (hypothesis)

```text
INTAKE → SCOPED → PLANNED → EXECUTING → VERIFYING → CHECKPOINTED
   ↑                  │            │              │             │
   └────── BLOCKED ───┴────────────┴──────────────┴──→ HANDED_OFF → CLOSED
```

A model may propose; validation decides whether state is durable.

Guards:

- `EXECUTING` needs scope, owner, expected evidence
- `VERIFYING` needs a declared check
- `CHECKPOINTED` needs bounded state + next action
- `HANDED_OFF` is fresh-session readable
- `CLOSED` needs acceptance evidence
- `BLOCKED` preserves the blocker; models do not invent workarounds as facts

## Capability model (hypothesis)

Initial context:

1. compact role contract
2. selected project/task/checkpoint packet
3. tiny core tools (files, terminal, todo, delegation)
4. compact capability index

Full schemas load on demand. Discovery must not silently expand context or hide a required tool.

Tool-output reduction is a view only: keep raw artifact ref, exit status, stderr, enough metadata to verify later.

## Hermes integration (hypothesis, not implemented here)

Use official plugin / context-engine / `pre_llm_call` seams if they exist. Keep the durable core **outside** Hermes.

Desired project profile:

- `memory.memory_enabled: false` and `memory.user_profile_enabled: false` (CLI `hermes memory off` is not enough)
- no automatic lossy compression
- checkpoint → new session + compact packet
- lazy tools/skills/MCP
- one profile switch restores stock Hermes

Official docs worth Sol reading (upstream, not local dirty trees):

- Providers / OpenAI-compatible proxy
- Toolsets and Tool Search
- Memory
- Skills / progressive disclosure
- Context-engine plugins and plugin hooks

Local installed Hermes (from sibling notes, re-verify): NousResearch/hermes-agent, package ~0.20.6, custom provider, stream on, WSL path `/usr/local/bin/hermes`. Local source was dirty vs upstream; do not treat it as clean `main`.

## Models / proxy constraints

Owner wants cheap/fast LiteLLM models through Hermes, streamed:

- `grok-4.6`
- `minimax-m3` (MiniMax M3 — not Kimi Max)
- `mimo-v2.5-pro`
- `kimi-k2.7-code` as a later strong option

Constraints:

- Streamed requests only
- Exact requested vs returned model identity
- Fallback ≠ success
- ~64K context needed for normal Hermes agent work
- Do not commit or rotate the local proxy key
- Do not add a database to paper over catalog errors
- OpenCode already works against the same local proxy; use that as a positive control

A sibling prototype reports streamed route-gate PASSes for the four aliases and a tiny lean vs baseline census. **Re-run before citing.** Payload census ≠ live Hermes turn loop.

## Evaluation bar (keep a change only if)

- total tokens decrease
- task failures and context-rot errors do not increase
- long-horizon recovery does not worsen
- no secret/state leak
- works from a fresh session
- reversible via profile switch

Do not start plugin publication until a real bottleneck is measured.

## Luna tickets Sol should emit (after the plan)

Each ticket: one artifact, one verify command, ≤600s, no architecture invention.

Example order (Sol may replace):

1. JSON schemas + transition validator, red/green tests
2. Provenance / artifact-reference validator
3. Deterministic context-packet compiler
4. Strict capability manifest/resolver
5. One reversible Hermes adapter seam (not live-home activation)
6. Fault-injection for missing/corrupt checkpoint
7. Hidden-holdout long-horizon runner that does not leak answers

## Questions Sol must answer

1. SDK-first with thin Hermes adapter, or Hermes-first bootstrap?
2. Files vs later optional DB for state?
3. How checkpoints avoid both context exhaustion and operator burden?
4. Which Hermes seams are enough vs upstream patches?
5. Public benchmark that cannot be gamed by shrinking prompts while harming correctness?

## Required Sol deliverable

Staged plan with component ownership, schema/API sketch, failure model, test matrix, rollback, private-then-public GitHub bootstrap, and a short Luna queue. Rejected alternatives listed. No claim that early token savings prove production viability.
