# Jev controller pilot

> **INVALID AS A COMPARISON — read before quoting any cell below.** Every run in
> this file (and `pilot-hosted1-20260921`, `pilot-pi1-20260921`,
> `replay-{pi,grok,opencode}-3-20260921`) sent the harness a prompt that, for most
> pool tasks, contained **no task at all**. The runner passed `user_turns()[0]`,
> which in these Work transcripts is the prepended `<recommended_plugins>` /
> `<environment_context>` block. For **11 of the 22** develop+holdout hashes that
> first turn holds nothing else, so the baseline arm received boilerplate only
> while the Jev arm additionally received the controller directive — the only
> actionable text in the prompt. The observed effect (baseline 0 tool calls, Jev
> up to 306) therefore measures **"was there an instruction?"**, not routing
> quality, and cannot be read as Jev raising tool activity or causing timeouts.
> The extraction path is fixed in `research/replay_lib.py` (`strip_context_blocks`,
> `first_ask`, `ask_turns`) and both runners now record `ask_present` /
> `ask_shifted` per row. Nothing in this file may be used as a controller result
> until the set is re-run with real asks; do not compare new cells to these.

This is a small, hash-only pilot of the separate Jev controller layer against
existing Work replay tasks. Each task was run once in baseline mode and once
with one initial Jev routing hint. The controller did not receive tools or
filesystem authority. Raw prompts and CLI event bodies remain ignored under
`.controller-runs/`.

## OpenCode pilot

Run: `pilot-opencode2-20260921` · two develop hashes · 90-second cap · free
OpenRouter execution model.

| hash | baseline | Jev | baseline tools | Jev tools | work match | outcome |
| --- | --- | --- | ---: | ---: | --- | --- |
| `0d6ca4607eaf` | ok | ok | 7 | 33 | true / true | partial / partial |
| `1a415bc257e5` | ok | timeout | 3 | 28 | true / true | partial / partial |

The controller chose `INSPECT_TASK_STATE` for both rows, with confidence
0.32–0.34. In this tiny sample it increased observed tool activity and caused
one timeout; it did not change the Work-match or outcome labels. This is a
measurement of a first hint, not evidence that Jev improves the full task.

## Grok Build pilot

Run: `pilot-grok2-20260921` · one develop hash · 90-second cap.

| hash | baseline | Jev | baseline tools | Jev tools | work match | outcome |
| --- | --- | --- | ---: | ---: | --- | --- |
| `0d6ca4607eaf` | partial / empty | partial / empty | 0 | 0 | false / false | no / no |

Jev chose `INSPECT_REPO` with confidence 0.34. The adapter and provider both
need a larger matched run before any controller conclusion is drawn.

## Hosted model and Pi pilot

The hosted arms use Qwen Flash through the existing YOLO Auto OpenCode
provider and Grok Build’s authenticated xAI CLI. Pi was installed separately
and then pointed at the same Qwen endpoint through a project-local provider
file. These are one-task smoke measurements on `0d6ca4607eaf`, each with a
90-second cap.

| adapter / model | mode | status | tools | work match | fail mask | outcome |
| --- | --- | --- | ---: | --- | --- | --- |
| OpenCode / Qwen Flash | baseline | ok | 4 | false | R3 | partial |
| OpenCode / Qwen Flash | Jev | timeout | 13 | true | none | partial |
| Grok Build / grok-4.7 | baseline | partial | 0 | false | empty | no |
| Grok Build / grok-4.7 | Jev | partial | 0 | false | empty | no |
| Pi 0.87 / Qwen Flash | baseline | ok | 0 | false | empty | no |
| Pi 0.87 / Qwen Flash | Jev | timeout | 53 | false | R3 | partial |

The Qwen OpenCode rows are from `pilot-hosted1-20260921`; the Pi rows are from
`pilot-pi1-20260921` after installation. The result shows that the adapters
and routes are live, while model/task compatibility and timeout behavior still
need a fixed larger pool. It does not justify promoting the Jev hint to an
enforcing state guard.

## First valid comparison (post-fix)

Run `replay-fix-20260922` · OpenCode / Qwen Flash · 150-second cap · real owner ask
in both arms (`ask_present` true for every row). `0d6ca4607eaf` is a task whose raw
first turn was boilerplate only (`ask_shifted` true); `1a415bc257e5` already carried
its ask in turn 1 and acts as the control.

| hash | ask_shifted | baseline status / tools | Jev action | Jev status / tools | work match |
| --- | --- | --- | --- | --- | --- |
| `0d6ca4607eaf` | yes | ok / 6 | INSPECT_REPO | timeout / 6 | false / false |
| `1a415bc257e5` | no | ok / 0 | INSPECT_TASK_STATE | timeout / 14 | false / true |

Baseline now performs real tool work (6 calls) where the same arm previously logged
zero, which is the signature of the fixed prompt rather than a controller effect.
With two tasks this is still a smoke test: both Jev rows hit the cap, one raised tool
count and one did not, and no work-match gain is established. Treat only these two
rows as comparable; everything above the banner is not.

## Decision for the next slice

Keep the controller as a bounded routing layer and run a larger matched set
with the same task hashes, fixed adapter settings, and per-step state updates.
Compare work match, R1–R6 cells, outcome label, tool count, timeout rate, and
whether the chosen action was appropriate. Do not promote Jev to a runtime
state machine guard from this pilot alone.
