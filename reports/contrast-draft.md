# Contrast draft (Codex Work vs Kilo vs OpenCode)

Generated: 2026-09-20T05:24:00Z from hashed copies. Counts only. Not a claim that Kilo equals ChatGPT.

## Scale (not comparable without this table)

| Corpus | Sessions / threads | Messages or items | What “mutate” means here |
| --- | --- | --- | --- |
| Codex Work JSONL | 1518 hashed files, 351780 lines | sqlite 1403 threads with items | `fileChange` (strict) vs `commandExecution` / `exec` (mixed) |
| OpenCode | 153 sessions | 2631 msgs / 10279 parts | bash/write/edit/patch |
| Kilo (this product) | 18 sessions | 1480 msgs / 7082 parts | bash/write/edit/patch |

Kilo sessions are **dense** (~393 parts/session) vs OpenCode (~67) vs Codex (~54 items/thread). Kilo **n is too small** for product claims.

## Codex Work (the ChatGPT-adjacent local corpus)

- Cloud is not here. `chatgpt_handoff` = 2 threads.
- Models: luna 1143, gpt-5.5 233, terra 92, sol 76.
- JSONL top-level types include unknown-to-plan keys: `token_usage_record` (17223), `inter_agent_communication_metadata` (352). Counted, did not crash.
- Tool names: **exec 31831**, shell_command 8743, wait 3559, apply_patch 967, update_plan 137. Exec dwarfs patch.

Loop proxies from `item_type` (no bodies):

- threads with fileChange: **162 / 1403**
- threads with webSearch: **100 / 1403**
- threads with plan item: **8 / 1403**
- webSearch/imageView before first fileChange: **48 / 162 (29.6%)**
- plan before first fileChange: **3 / 162 (1.9%)**
- median seq to first **commandExecution: 3**
- median seq to first fileChange: 34
- median seq to first webSearch: 11

Dominant early signature: `userMessage → reasoning → agentMessage → mcpToolCall`, not search-then-plan-then-edit.

**Takeaway:** Codex rigor on this disk is not “always webSearch + plan.” It is early MCP/exec, lots of reasoning, rare explicit `plan` items, and search in a minority of mutating threads. `commandExecution`/`exec` is the real mutate-or-observe blob and still needs hashed-arg rules.

## Kilo vs OpenCode (same tool vocabulary)

| Proxy | Kilo | OpenCode |
| --- | --- | --- |
| observe before first mutate | 15/16 (93.8%) | 6/25 (24.0%) |
| plan-ish before first mutate | 2/16 (12.5%) | 5/25 (20.0%) |
| median tool-seq to mutate | 13 | 1 |
| first tool | mostly `read` | study-os-replay / `bash` |
| web-like observe | webfetch 128 | webfetch 97 + websearch 36 |

OpenCode’s db is mixed with **Study OS replay** tools. Do not ship OpenCode-only as “coding agent vs ChatGPT.”

Kilo’s high observe-prefix is real in this tiny sample and **does not** prove Kilo matches Codex. Codex’s cheap search-before-fileChange rate is 30% under a stricter mutate definition.

## Classification v0 (keep)

| Source | Observe | Plan | Mutate | Skill |
| --- | --- | --- | --- | --- |
| Codex sqlite | webSearch, imageView | plan, update_plan | fileChange; exec mixed | mcp/dynamic/collab |
| Codex JSONL | (tool names later) | update_plan | exec, apply_patch, shell_command | spawn_agent, mcp |
| Kilo/OpenCode parts | read/glob/grep/webfetch/websearch | open_plan, todowrite | bash/edit/write/patch | skill, task |

## Still open

- Split Codex `exec` into read vs write without bodies (hash argv shape / cwd-free flags only).
- Filter OpenCode to coding sessions (drop study-os-replay) before any product claim.
- Grow Kilo n or label it “illustrative.”
- events.v1 adapter still **not earned**; sqlite + JSONL histograms already answer the first question.

## Out of this campaign

No harness patches. No Milestone A issues. No Cloud scrape.
