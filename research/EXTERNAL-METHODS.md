# How the field actually turns coding-agent work into analysis and tests

Draft literature note. Not a freeze. Not an adapter. Not Milestone A.

I jumped to JSONL scripts before this. That was the wrong order.

## Three jobs people keep mixing up

| Job | What it is | What it is not |
| --- | --- | --- |
| **A. Outcome eval** | Hidden tests on a prepared repo. Did the patch resolve the issue? | Replaying a private ChatGPT chat |
| **B. Process / scaffold** | How the agent localizes, edits, and checks. ACI, tool mix, phases | “Read every transcript like a novel” |
| **C. Training / task synthesis** | Generate bugs + trajectories from **public** repos with execution envs | Distill your personal Codex JSONL into fine-tune data |

Our local Codex/Kilo/OpenCode logs are evidence for **B**. They are a bad, unsafe source for **A** and **C**.

## Outcome eval (how you “test them for tasks”)

**SWE-bench** (Jimenez et al., [arXiv:2310.06770](https://arxiv.org/abs/2310.06770)): GitHub issue + repo snapshot. Agent submits a patch. Grade with `FAIL_TO_PASS` tests the agent **does not see**, plus `PASS_TO_PASS` so it did not break unrelated code.

**SWE-bench Verified** ([OpenAI, 2024](https://openai.com/index/introducing-swe-bench-verified/)): human annotators threw out most of the original test set. About **68%** of sampled items were underspecified, had unfair tests, or other fatal issues. GPT-4o roughly **doubled** (16% → 33%) once impossible items were removed. Lesson they state in public: **invest in the eval itself**, or you will under/over-estimate the harness.

Also from that note: **scaffold variance is huge**. GPT-4 on Lite went from **2.7%** (early RAG) to **28.3%** (CodeR). Measuring Kilo vs OpenCode vs Codex **on the same public task set** matters more than cloning Codex chat style.

**Terminal-Bench** ([tbench.ai](https://www.tbench.ai/), Harbor): terminal/agent work, oracle solutions, `harbor run --agent … --env modal`. This is the actual overnight job for “test Kilo and OpenCode for tasks,” not parsing 1,518 private rollouts as if they were issues.

**τ-bench** (Yao et al., [arXiv:2406.12045](https://arxiv.org/abs/2406.12045)): tool + policy + user. Grade **database end-state**, not the transcript. `pass^k` for consistency across trials. GPT-4o was `<50%` and `pass^8 <25%` in retail. Reliability, not one lucky run.

**Do not** turn private Codex sessions into SWE-bench items. They have no hidden tests, often no repo snapshot, user text in the clear, and contamination risk. OpenAI already showed public GitHub issues were often unfair. Private chats are worse.

## Process analysis (what the JSONL is actually for)

**SWE-agent** (Yang et al., [arXiv:2405.15793](https://arxiv.org/abs/2405.15793)): the **agent-computer interface** (how it reads, edits, runs tests) changes behavior and scores. They ship a **trajectory browser**. Linear, inspectable traces are the analysis object.

**mini-SWE-agent** ([github.com/SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent)): 2025 result — **bash only**, no custom tools, linear history, `subprocess.run` per action, **>74% on SWE-bench Verified**. SWE-bench even has a **Bash Only** leaderboard so models are compared in the **same** mini-agent. That matches our local count: Codex `exec` (~32k) dwarfs `apply_patch` (~1k). “Rigor” in 2025 is often **a capable model + a shell + tests**, not a zoo of tools.

**Agentless** (Xia et al., [arXiv:2407.01489](https://arxiv.org/abs/2407.01489)): OpenAI used this as the coding showcase for GPT-4o / o1. Fixed pipeline, LLM does **not** pick the next tool:

1. **Localization** (files → functions → edit lines; IR + LLM)
2. **Repair** (small search/replace diffs, many samples)
3. **Patch validation** (reproduction tests + regression tests, majority vote)

They also measure **% correct location** at file/function/line, not only resolve rate. That is the process metric we should copy: did the agent look at the right place before editing?

This is the literature form of “research then mutate then verify.” It is **not** “count `plan` items in Codex.” Agentless barely uses autonomous planning. Our Codex sqlite already showed **plan is rare**; that does not mean Codex is sloppy. It may mean **localize/exec/test** is the real loop.

## Training data (if we ever want more tasks)

**SWE-smith** (Yang et al., [arXiv:2504.21798](https://arxiv.org/abs/2504.21798)): from a **public** Python repo, build an execution env, **synthesize** bugs that break tests, collect trajectories, train. 50k instances, 128 repos. They open-source procedure, tasks, trajectories, models.

That is how you scale tasks. **Not** by exporting ChatGPT Work JSONL.

## What our local traces are allowed to do

Allowed (process evidence, counts / hashes only in git):

- Tool mix: exec vs patch vs search vs tests
- Localization proxy: read/grep/web before first file write
- Validation proxy: test command after edit; error then search vs error then more mutate
- Scaffold comparison: Codex vs Kilo vs OpenCode **on the same metric definitions**
- Hypothesis generation for harness changes

Forbidden as “the eval”:

- User prompts as problem statements
- Replaying a personal session as a SWE-bench clone
- Fine-tuning on private trajectories
- Claiming Kilo equals ChatGPT because observe-prefix looked high on n=18

## Pipeline the literature actually supports

```text
private traces (Codex / Kilo / OpenCode)
        │  process metrics only
        ▼
hypotheses about the harness
        │
        ▼
public tasks with hidden tests
  SWE-bench Verified  +  Terminal-Bench (Harbor)  +  optional τ-bench
        │  same agent wrapper, several seeds (pass^k)
        ▼
change Kilo / OpenCode scaffold
        │
        ▼
re-run the public tasks
```

Overnight work that matches this (when we resume analysis):

1. Keep process metrics on hashed JSONL (exec read vs write, test-after-edit, error recovery). No bodies in git.
2. Do **not** extract private tasks.
3. Next campaign: wrap Kilo and OpenCode in Harbor / SWE-bench Verified (bash-only and native tools) and compare to mini-SWE-agent on the **same** instances.

## Sources

- Jimenez et al. SWE-bench. arXiv:2310.06770. https://www.swebench.com/
- OpenAI. SWE-bench Verified. 2024-08-13. https://openai.com/index/introducing-swe-bench-verified/
- Yang et al. SWE-agent. arXiv:2405.15793. https://swe-agent.com/
- Xia et al. Agentless. arXiv:2407.01489.
- Yang et al. SWE-smith. arXiv:2504.21798. https://swesmith.com/
- mini-SWE-agent. https://github.com/SWE-agent/mini-swe-agent
- Terminal-Bench / Harbor. https://www.tbench.ai/ https://github.com/harbor-framework/terminal-bench
- Yao et al. τ-bench. arXiv:2406.12045.
