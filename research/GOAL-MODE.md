# /goal — Hermes and ChatGPT/Codex (what I missed earlier)

I previously only looked at Kilo/OpenCode slash files. **That was the wrong product.** `/goal` is a **loop engine**, not a saved prompt.

## ChatGPT / Codex

Hermes documents this as **Codex CLI 0.128.0 `/goal`** (Eric Traut, OpenAI). Idea: keep a standing objective across turns; **do not stop until it is achieved**.

Our local Codex JSONL already has a `get_goal` tool (1 call in 1518 files) — rare in this corpus, but the feature exists on the Codex side.

ChatGPT.com “Tasks” (scheduled reminders) is **not** the same thing. `/goal` is in-session auto-continue.

## Hermes Agent (Nous)

Official: [Persistent Goals](https://hermes-agent.nousresearch.com/docs/user-guide/features/goals)

```
/goal <text>          set standing goal, first turn starts now
/goal status|pause|resume|clear
/goal draft <text>    LLM drafts a completion contract then sets it
/subgoal <text>       extra acceptance criteria mid-loop
/goal gate add <cmd>  shell must exit 0 before “done”
/goal wait <pid>      park until a background process ends
```

After **every turn** a **judge model** returns `done | continue | blocked | wait`. If `continue`, Hermes injects a continuation into the **same session** (full context kept). Default budget **20 turns**, then pause. State lives in session DB → `/resume` still has the goal.

Also: **quality gates** (deterministic tests before the judge), **completion contract** (outcome / verify / constraints / boundaries / stop_when). Inspired by Codex; Hermes says implementation is independent.

Kanban `goal_mode=True` uses the **same engine** inside one worker card.

Hermes also has `/loop` (timed re-fire) and `/heartbeat` (idle re-prompt). Those are not `/goal`.

## What Kilo has today

| Piece | Kilo | Hermes/Codex `/goal` |
| --- | --- | --- |
| Slash file `/goal` we added | Re-injects PLAN.md once | Not the same |
| `schedule_wakeup` | New turn later | Same session, every turn |
| Judge | None | Aux model every turn |
| Shell gates | pytest in CI, not in-session | `/goal gate add` |
| Persistence | CONTINUE.md on disk | SessionDB `goal:<id>` |

**Kilo cannot import Hermes `/goal` by copying a markdown command.** It needs a product loop: after each assistant stop, run a judge, if not done send a synthetic user continue, until budget. Wakeups are the closest hook we have without changing Kilo itself.

## Import that would actually match

1. Keep `CONTINUE.md` as the standing goal text (owner plan).
2. Add **acceptance + gates** in that file (pytest owner-gate must pass; gold report covers all jsonl; both modes exist).
3. After each Kilo turn: if gates fail or ISSUES still open, **wakeup with `/goal` prompt** (poor man’s continue). That is not Hermes, but it is the portable part.
4. Real parity = Kilo/OpenCode implement judge+auto-continue. Out of this repo unless we patch those products.

Do not pretend `.kilo/command/goal.md` is Hermes `/goal`.
