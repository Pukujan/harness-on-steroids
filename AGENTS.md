# harness-on-steroids — owner instructions

**The user owns this project. Agents do not.** If an older plan, PAM note, literature brief, or prior agent disagrees with this file or `PLAN.md`, **this file and PLAN.md win.** Do not “correct” the owner with SWE-bench, Harbor, mini-SWE-agent, or “don’t treat Codex as gold.”

Read in this order:

1. `AGENTS.md` (this file)
2. `PLAN.md`
3. `HANDOFF.md`
4. `.content-system/system-version.json` and the relevant `.content-system/` files before changing README, marketing, UX, image, or HTML content.

Do not treat `.kilo/plans/1789773436389-harness-on-steroids-campaign.md` as source of truth. It is leftover campaign text.

## What this project is

Local **ChatGPT Work / Codex desktop** transcripts are the **gold behavior**.

Analyze **all** of those transcripts. Learn how Codex **splits work into tasks** and **chains tool calls**. Write that down as a spec.

Then make **Kilo** (whatever model it is using now) and **OpenCode** (including free models, build mode) **imitate that same behavior**. Add a **mode** that is a copy of how Codex works. Both products should follow it.

Label corpus rows `source=codex_work`. This is local Codex/Work, not chatgpt.com Cloud.

## Gold

Codex/ChatGPT Work **behavior** is gold: task decomposition, tool-call chains, research-then-act, verification habits, sub-agents, plans, skills.

The transcript is enough data **for the process recipe**. There are already ~1.5k rollout files and a large sqlite index. **Do not invent a new exam. Do not re-test Codex on public benchmarks. Do not build a “Codex-style agent” from SWE-bench papers.**

Owner also wants **matched-task outcome**: the same local Work asks, replayed into Kilo/OpenCode (gitignored prompts), scored on observable results—not only tool names. That is PLAN step F, not SWE-bench.

## Do this

1. Parse **all** hashed local Codex JSONL (+ archived). Copy-hash first; never commit raw JSONL or message bodies.
2. Classify how Codex turns a user ask into **multiple tasks** and **tool sequences**. Write `reports/codex-gold-behavior.md` and a mode spec.
3. Implement that spec as a **Kilo agent/mode** and an **OpenCode agent/mode** (and/or skill) so they behave like Codex **with the models already in use**, including free OpenCode models in build mode.
4. Keep going until the spec is written from the full corpus and the modes exist.

## Do not

- Argue that transcripts cannot be gold
- Run SWE-bench, Terminal-Bench, Harbor, or mini-SWE-agent as the project
- Test Codex again on new tasks
- Build a separate Codex-clone product instead of teaching Kilo and OpenCode
- Scrape Brave or Chromium Codex web cache
- Commit message bodies, raw JSONL, sqlite, or session_diff
- Mix this with `hades-product` or `colorful-income`
- Create the old 26 GitHub-issue campaign as a substitute for this work

## Privacy

Copy then hash before parse. Git may contain specs, counts, redacted goldens, mode prompts. Not user chat text.

## Stop rewriting the goal

If you think SWE-bench is “better science,” **do not substitute it**. Do the analysis and the imitate-Codex modes. The owner already decided.

## Chat first, then no-stop

Before `/goal` and an explicit go-ahead, conversation is the job. Answer questions in detail. Clarify. **Seek go-ahead before starting a long-running task.** A status question is not a standing goal. ChatGPT Work looks, then talks. It does not start a no-stop loop from ordinary chat.

After `/goal` is set, the plan is frozen, and the owner says go, the no-stop loop applies: Owner ordered at least **48 hours** of autonomous progress (`CONTINUE.md`). Do not wait for approval. Do not stop yourself. CI owner-gate tests are mandatory; do not delete them.
