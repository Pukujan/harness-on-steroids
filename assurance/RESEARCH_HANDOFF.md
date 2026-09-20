# Research handoff — harness-loop measurement

Not a freeze. Not Milestone A. Not authorization to patch Kilo or OpenCode.

## Problem

Coding agents here (Kilo, OpenCode, others) feel less reliable than ChatGPT/Codex Work: weaker research before edits, weaker provenance, weaker verifiability, weaker “the code can be checked.” The question is what that difference actually looks like in local transcripts, before anyone changes a harness.

## Intended outcome (now)

Measure local Codex/Work desktop rollouts against local OpenCode and Kilo sessions. Counts, type histograms, observe/plan/mutate proxies. No message bodies in git.

## Intended outcome (later, out of this campaign)

Use that contrast to change Kilo/OpenCode (and similar) so they research, cite, plan, and verify more like Codex. That is a **different campaign**, after a reviewed contrast exists.

## Assumptions treated as input

- ChatGPT.com Cloud chats are **not** on this disk as transcripts.
- The local “ChatGPT-like” corpus is **Codex Desktop / ChatGPT Work** JSONL under `%USERPROFILE%\.codex\`.
- `source=codex_work` is the correct label. Do not call it Cloud.
- Copy then hash before parse. Git gets stats, schemas, redacted goldens, pack metadata only.

## Evidence already on this PC (2026-09-20)

| Corpus | What it is | Scale (counts only) |
| --- | --- | --- |
| Codex live rollouts | `~\.codex\sessions\**\rollout-*.jsonl` | 1113 files, ~1.06 GB |
| Codex archived | `~\.codex\archived_sessions\**\rollout-*.jsonl` | 405 files, ~362 MB |
| Codex thread index | `thread_history_1.sqlite` | ~490 MB; 75,980 items; 6,350 turns |
| Codex sidebar | `state_5.sqlite` | 1,569 threads |
| OpenCode | `~\.local\share\opencode\opencode.db` | 153 sessions, 2,631 messages, 10,279 parts |
| Kilo (this product) | `~\.local\share\kilo\kilo.db` | 18 sessions, 1,462 messages, 6,969 parts |
| Kilo `session_diff` | JSON sidecars | 18 files — **not** the transcript |
| Kilo Code VS Code | `kilocode.kilo-code` | empty |
| ChatGPT Cloud ZIP | `data/incoming/` | absent |
| Chromium / Brave | Store/web cache | out of corpus |

Codex `thread_source`: mostly `user` (1281), plus subagents (191). `chatgpt_handoff` = 2. Models: mostly `gpt-5.6-luna` (1143), then `gpt-5.5` / terra / sol.

Codex `item_type` already classifies the loop: reasoning, agentMessage, commandExecution, userMessage, mcpToolCall, fileChange, webSearch, plan, etc.

JSONL record types seen: `session_meta`, `event_msg`, `response_item`, `turn_context`, `compacted`, `world_state`. Originators on sampled files: `codex_work_desktop` and `Codex Desktop`.

## Alternatives already considered

- Scrape Brave / Chromium `%APPDATA%\Codex\web\` as if it were ChatGPT Cloud — **rejected**.
- Unofficial chatgpt.com API — **rejected**.
- Treat Kilo `session_diff` as the Kilo corpus — **wrong**; `kilo.db` is the session store.
- Ship a 26-issue GitHub catalog before reuse/scope — **blocked by PAM**.
- Patch Kilo/OpenCode now to “be like ChatGPT” — **blocked until contrast**.
- Hermes / hades gateway schema as the event model — **do not reuse that schema**; reuse only the counts-only privacy pattern.

## Unresolved

- How much of `commandExecution` is read vs write (needs hashed-arg rules, not bodies in git).
- Whether Cloud ZIP will ever appear in `data/incoming/`.
- Whether 18 Kilo sessions are enough contrast, or we only report “Kilo n is small.”
- Human review of reuse disposition (required before `build_new` of adapters/issue catalog).

## Known reusable systems

See `assurance/BUILD_VS_REUSE.md`.

## Rejected approaches

Brave scrape; Cloud-as-local; harness patches this campaign; committing JSONL/sqlite; counting PAM as a product alternative.
