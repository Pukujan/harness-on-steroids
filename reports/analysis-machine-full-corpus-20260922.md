# Analytical machine full-corpus structural report

Date: 2026-09-22  
Status: descriptive structural evidence; not an agent-quality evaluation  
Machine: `analysis-machine/0.1.0`  
Contract: `analysis-event/0.1.0`  
Ontology: `analysis-ontology/0.1.0`  
Codebook: `analysis-codebook/0.1.0`

## Scope and method

The reusable analysis machine processed the local imported Codex and ChatGPT
provenance JSONL through separate lane adapters and a shared, body-minimized
`CanonicalEvent` contract. The run used 2,173 JSONL source files and wrote a
summary-only local export; raw transcript bodies and normalized event bodies
were not committed. The ignored local run directory is
`data/derived/analysis-machine/full-summary-20260922-v5/`.

The run used a 600,000-ID exact duplicate-tracking limit, larger than the
556,241-event input, so the duplicate result is complete for this run. The
streaming input order was the CLI's deterministic sorted-path/source-local
order. The export fingerprint is recorded in the ignored manifest and summary.

## Aggregate coverage

| Measure | Result |
| --- | ---: |
| Source JSONL files | 2,173 |
| Canonical events | 556,241 |
| Episodes | 1,499 |
| Codex events / episodes | 419,893 / 1,387 |
| ChatGPT events / episodes | 136,348 / 112 |
| Known-event rate | 94.8646% |
| Unknown events | 28,565 |
| Parse-error events | 0 |
| Validation issues | 0 |
| Duplicate IDs | 0 |
| Duplicate checks skipped | 0 |

“Known-event rate” means the event kind was recognized by the current adapter;
it does not mean the event body or outcome was understood. The 28,565 unknown
events break down as token-usage records 25,809, world-state records 2,014,
inter-agent metadata 352, attachment records 72, and 318 records with an
unknown subtype. They are recognized source shapes that still lack a promoted
canonical kind, not necessarily malformed input.

## Codex execution lane

| Structural measure | Result | Denominator / interpretation |
| --- | ---: | --- |
| Tool calls | 53,183 | observed Codex tool-call events |
| Tool results | 53,190 | observed result events; one call can yield multiple results |
| Tool results per call | 1.00013 | result-event count divided by call-event count |
| First tool family | execute 1,051; other 10 | normalized first-tool family by episode |
| Episodes with a mutation-family event | 45 | episode-level structural relation |
| Mutation episodes with prior inspection-family event | 3 / 45 | qualifying normalized events only |
| Mutation episodes with later verification-family event | 0 / 45 | qualifying normalized events only |
| Delegation-family events | 285 | observed normalized tool-family events |
| Compaction events | 318 | observed lifecycle/compaction events |

These are adapter-defined event relationships. They do not prove that a task
was unsafe, that verification truly should have happened, or that no
verification existed outside the recognized event vocabulary.

## ChatGPT chat/research lane

| Structural measure | Result | Denominator / interpretation |
| --- | ---: | --- |
| User messages | 2,430 | normalized user message events |
| Assistant messages | 7,144 | normalized assistant message events |
| Chat episodes | 112 | all normalized ChatGPT episode IDs |
| Episodes with assistant messages | 96 | subset used only as a descriptive companion count |
| Citation events | 30,084 | normalized citation rows |
| Episodes with citation events | 100 / 112 | presence, not citation correctness |
| Citation-presence rate | 89.2857% | 100 divided by 112 |
| Tool calls / results | 27,534 / 38,751 | normalized chat tool events |
| Code events | 34,584 | source adapter content-type classification |
| Execution-output events | 2,163 | source adapter content-type classification |
| Research events | 0 | unavailable/not observed in this adapter view; not “no research” |

The scoped known-message/tool rate was 105,943 / 136,348 = 77.7004%.
Artifact, provenance-edge, node, rendered-turn, lifecycle, and unknown kinds
are intentionally outside that scoped numerator. It must not be read as an
overall evidence-quality score.

## What this run establishes

- The adapters can process the imported corpus in a bounded streaming pass.
- Lane totals, episode totals, versions, missingness, event fingerprints, and
  exact duplicate coverage are now visible in the export.
- The current structural vocabulary can support descriptive counts and narrow
  event-order relations.
- The machine is repeatable infrastructure for a later annotation study.

## What this run does not establish

It does not establish agent quality, task success, intent, private reasoning,
planning proportionality, UX quality, citation correctness, claim support,
research absence, causality, or a Codex-versus-ChatGPT ranking. A zero in an
event relation means “no qualifying event observed under this adapter and
codebook,” not proof of absence.

The next evidence step is a small source-linked, body-minimized, independently
double-reviewed ontology pilot. Proposed labels remain non-authoritative until
that pilot has positive examples, counterexamples, disagreement reporting, and
an adjudicated migration decision.
