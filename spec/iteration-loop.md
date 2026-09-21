# Iteration loop - evidence-driven behavioral control

This is the normative fast loop for active development. The long-term goal is large; each iteration is deliberately small.

1. Choose one observed behavioral deviation and one hypothesis.
2. Freeze 3-5 representative existing task fixtures and acceptance criteria.
3. Run the current control on Pi + OpenCode + Grok Build in the same slice where technically possible. Record exact harness/model/provider/config.
4. Capture the complete observable trajectory: interaction, inspect/research, tools/results/waits/failures, mutations, verification/provenance, output, continuity, outcome.
5. Normalize only enough semantics to compare the harnesses and Work reference. Exact tool names and exact prose remain diagnostics.
6. Apply the smallest intervention: prompt/context first; capability/tool presentation next; checkpoint/continuation context next; narrow runtime guard only after repeated evidence earns it.
7. Rerun the same fixtures automatically.
8. Compare candidate vs previous control and reference evidence.
9. If behavior/outcome improves without material regression, keep it. If not, revert or revise.
10. Record the result, update CURRENT, then choose the next deviation.

## Required properties

- One main behavior hypothesis per normal slice.
- Pi + OpenCode + Grok Build are concurrent development surfaces, not sequential ports.
- Kilo Codex v0 remains a positive-control baseline/history.
- Tool order is diagnostic; complete observable behavior and outcome are the target.
- Same model across harnesses is useful but not required; exact model identity is always recorded.
- Repeated generations and morphs are used when they answer a robustness/variance question.
- Holdout boundaries stay sealed during tuning.
- No substantial architecture-only slice: produce a measured signal, evaluator capability, or observable result.
- Do not rescue a candidate by changing the acceptance contract after seeing its result.

## State-machine policy

A runtime state machine is **not required**.

Semantic labels such as inspect, research, execute, observe, verify, and terminal states may be derived for comparison. Promote a state/guard into runtime control only when repeated failures show prompt/context control is insufficient and a direct experiment demonstrates value.

## Stop / promotion

The fast loop stops for a hypothesis when it is kept, rejected, or blocked with evidence.

Promotion to a broader control version happens only after broader development tasks, relevant morphs/repeated runs, and the sealed holdout show no material regression in task outcome, verification, scope/safety, or truthful reporting.

Forbidden exits: replacing the project with a public benchmark; declaring success from tool-call similarity alone; building a general framework without measured need; deleting contradictory evidence.
