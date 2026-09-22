# Analytical Machine v0

Status: implementation and full structural pass complete; ontology pilot
pending, 2026-09-22.

## Purpose

Build one small, repeatable, exportable analysis machine that can consume
future agent evidence without being tied to coding transcripts, Jev, a single
model, or a single harness.  The first consumers are two separate views over
the local corpus:

- Codex execution: inspection, tools, edits, execution output, delegation,
  waits, verification, continuity, and observable outcome.
- ChatGPT chat/research: user turns, response type, research activity,
  citations, provenance, answer shape, planning proportionality, and UX.

The lanes share a body-minimized evidence contract, but do not share a single
quality score or pretend that unlike events are equivalent.

## Non-goals for v0

- no raw transcript or prompt body in Git or exported derived artifacts;
- no automatic ontology mutation by a model;
- no graph database, OWL reasoner, Power BI project, or general orchestration
  framework before an analysis question requires it;
- no causal claims from event order alone;
- no treating deterministic output as proof that a metric is valid.

## Architecture

```text
raw local source
  -> source adapter
  -> CanonicalEvent (contract + provenance pointer + no body)
  -> lane analyzer
  -> deterministic summary/export
  -> optional graph projection and dashboard
```

The v0 implementation lives in `src/hos/analysis_machine/` and currently
supports JSONL adapters for the imported Codex envelope and the existing
ChatGPT provenance normalized views.  Normalization and lane aggregation are
streamable; the export can omit the large `events.jsonl` file for a summary-only
run.  The local export files are `manifest.json`, optional `events.jsonl`, and
`summary.json`.

Every export records:

- contract version;
- ontology version;
- analyzer version;
- event and episode counts;
- validation issue counts;
- unknown and parse-error coverage;
- the explicit policy that bodies are not written.

Stable event identity is based on a caller-supplied source identity plus a
stable source-record key or ordinal.  Codex session identity is carried from
session metadata to later records in the same file.  Citation/provenance rows
also include their structural field/pointer because one message can produce
multiple rows.  Filesystem order is never an ordering authority for summaries;
the CLI supplies sorted paths and source-local order.  The machine reports
duplicate IDs instead of silently dropping them.

The manifest and summary include a body-free event fingerprint, explicit
unknown/parse-error counts, validation counts, and the duplicate-tracking
coverage.  A bounded duplicate set is the default; a larger limit or an
external sort can be selected for a corpus where exact duplicate coverage is
required.

## Full local structural pass — 2026-09-22

The corrected summary-only run used 2,173 local JSONL sources and produced
556,241 canonical events across 1,499 episodes.  Codex contributed 419,893
events in 1,387 episodes; ChatGPT chat/research contributed 136,348 events in
112 episodes.  Exact duplicate tracking was enabled with a 600,000-ID cap:
zero duplicate IDs and zero validation issues were observed in this run.
28,565 events remained `unknown` coverage and zero parse errors were observed;
unknown events are not silently treated as known behavior. The aggregate is structural evidence for adapter
coverage and action-order relationships, not a quality, intent, causal, or private-
reasoning judgment.  The committed aggregate interpretation is
`reports/analysis-machine-full-corpus-20260922.md`; raw and derived event
bodies remain local and ignored.

## Living ontology policy

The ontology is versioned, append-friendly, and reviewable.  A candidate term
can be proposed by a model, a script, or a human, but it enters the accepted
ontology only after evidence review.

```text
proposed -> pilot -> accepted
             |          |
             +------> deprecated/replaced
```

Each proposal must retain its source event IDs, definition, positive examples,
counterexamples, lane, expected use, and review decision.  A new ontology
version must be rerun against a frozen pilot and a sealed holdout; old labels
remain readable through an explicit mapping.  A precise score with a changed
ontology is a new result, not a historical rewrite.

Provider routing is also part of the analysis provenance.  Sol may be used only
through the repository's CKFF worker route.  Luna may be used only through
native Codex/ChatGPT subagent spawning; Luna must never be sent through CKFF or
silently replaced by another provider.  Provider unavailability is recorded as
an unavailable arm, not hidden by fallback.

## Validation strategy

### Contract tests

- required IDs, lane, ordinal, kind, observation state;
- tool calls have tool identity;
- event IDs are unique within an export;
- malformed JSON becomes a bounded parse-error event;
- nested payloads and text bodies never appear in `CanonicalEvent` output;
- output includes contract, ontology, and analyzer versions.
- non-object JSONL records and invalid ordinals become explicit bounded
  `parse_error` events;
- Codex session metadata is carried across records;
- repeated citation rows retain distinct structural identity;
- summary-only reruns cannot leave a stale `events.jsonl` artifact.

### Deterministic/golden tests

- the same normalized records produce byte-stable JSON output;
- input file order does not change summaries;
- duplicate records are reported, not silently merged;
- Codex and ChatGPT fixtures exercise both lanes and their lane-specific
  summaries;
- existing `score_seq` remains a differential diagnostic for its old mapped
  Codex/Kilo sequence, not an objective gold standard.

### Metamorphic relations

The relation applies only when its preconditions are true:

1. **Unknown-field relation:** adding unrecognized fields must not change
   normalized structural labels or aggregate counts.
2. **Partition relation:** splitting one source file into parts must produce
   the same result when source identity and source ordinals are preserved.
3. **Order relation:** permuting input files or records with distinct source
   ordinals must not change the result; arbitrary ordinal changes are not
   allowed because order is semantic evidence.
4. **Alias relation:** replacing equivalent tool aliases must preserve the
   coarse capability family while retaining the original tool name.
5. **Body-minimization relation:** changing body text must not change body-free
   structural metrics; content-length metrics, if later added, must be named
   as text-derived and tested separately.
6. **Lane isolation relation:** adding ChatGPT events cannot change Codex-only
   metrics, and adding Codex events cannot change ChatGPT-only metrics.
7. **Idempotence relation:** normalizing an already normalized fixture through
   an explicit adapter must not silently create a second semantic event.

Metamorphic tests do not prove that a metric is substantively correct.  They
catch brittle parsers, accidental file-order dependence, hidden body leakage,
and lane contamination.

### Mutation and differential tests

- remove a tool result and require result-rate/coverage to change;
- move a mutation before inspection and require the Codex inspection relation
  to fail;
- remove a citation event and require citation presence to change;
- corrupt an ordinal and require validation to report it;
- compare coarse Codex tool-family summaries with `score_seq` on the same
  synthetic sequence and document every intentional difference.

## Beads / dependency units

- **AM-01 Contract and versions — done:** body-free `CanonicalEvent`, stable
  IDs, validation issues, contract/ontology/analyzer versions.
- **AM-02 Source adapters — done for pilot:** Codex JSONL envelopes and
  ChatGPT normalized message/tool-event JSONL.
- **AM-03 Separate lane analyzers — done for pilot:** execution/research
  structural summaries with coverage and unknown counts.
- **AM-04 Validation gates — done for pilot:** contract tests, unknown-field
  relation, alias relation, order invariance, and body-minimization fixture.
- **AM-05 Full local pilot — done for the first slice:** one Codex session and
  one ChatGPT provenance conversation produced 5,525 events across three
  episodes. The export had zero parse errors, zero validation issues, and
  100% known-event coverage. A repeat run produced byte-identical hashes for
  `events.jsonl`, `summary.json`, and `manifest.json`. This is parser and
  contract evidence, not a claim about agent quality.
- **AM-05b Full corpus structural pass — done:** the two-lane local corpus
  produced 556,241 body-minimized events across 1,499 episodes. The corrected
  run used exact duplicate tracking and found zero duplicate IDs and zero
  validation issues, while retaining 28,565 unknown events and zero parse
  errors as explicit missingness. See the committed aggregate report.
- **AM-06 Ontology pilot — advisory pass complete:** a deterministic
  source-linked, body-minimized sample was independently reviewed by two native
  Luna passes, adjudicated, and checked on a sealed holdout. The codebook was
  clarified to separate action requests from observed evidence and research
  events from citation presence. No quality, UX, outcome, or planning label was
  promoted; native Luna annotations are advisory, not human gold.
- **AM-06b Owner/human adjudication — next:** create a larger lane-balanced
  sample, retain source event IDs in the ignored evidence plane, and adjudicate
  the structural labels against a concrete analysis question before promotion.
- **AM-07 Graph projection — deferred:** emit provenance edges only after a
  pilot query cannot be answered cleanly from event tables.
- **AM-08 Dashboard — deferred:** evaluate Power BI only after stable fact
  tables and useful repeated questions exist.

## Fast implementation order

1. Keep the pure module and fixtures green.
2. Add a bounded runner over one Codex slice and one ChatGPT slice.
3. Inspect only aggregate counts, parse/unknown coverage, and lane summaries.
4. Fix one adapter defect at a time; do not tune labels from the full corpus.
5. Freeze a pilot and holdout before ontology promotion.
6. Add graph/dashboard views only if the measured questions need them.

This sequence makes the analysis machinery useful immediately while keeping
future datasets, domains, and harnesses importable through the same contract.
