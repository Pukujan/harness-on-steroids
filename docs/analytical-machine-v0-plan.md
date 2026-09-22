# Analytical Machine v0

Status: active implementation slice, 2026-09-22.

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
ChatGPT provenance `messages.jsonl` / `tool-events.jsonl` views.  Its export is
three local files: `manifest.json`, `events.jsonl`, and `summary.json`.

Every export records:

- contract version;
- ontology version;
- analyzer version;
- event and episode counts;
- validation issue counts;
- unknown and parse-error coverage;
- the explicit policy that bodies are not written.

Stable event identity is based on a caller-supplied source identity plus a
source record key.  Filesystem order is never an ordering authority.  The
machine sorts by episode, source ordinal, and event ID and reports duplicates
instead of silently dropping them.

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

## Validation strategy

### Contract tests

- required IDs, lane, ordinal, kind, observation state;
- tool calls have tool identity;
- event IDs are unique within an export;
- malformed JSON becomes a bounded parse-error event;
- nested payloads and text bodies never appear in `CanonicalEvent` output;
- output includes contract, ontology, and analyzer versions.

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
- **AM-06 Ontology pilot — next:** annotate a small double-reviewed sample and
  promote only categories that improve an observable analysis question.
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
