# Codex Gold Behavior Mode Specification

## Overview

This mode replicates the Codex/ChatGPT Work gold behavior identified in `codex-gold-behavior.md`. It defines how Kilo and OpenCode agents should decompose user queries into tasks, execute them in parallel where possible, and deliver verified results.

## Core Architecture

### 1. Task Decomposition (Planner Role)

- **Input**: Raw user message
- **Process**: Parse into structured components (intent, entities, constraints)
- **Output**: Ordered list of sub-tasks with assigned responsibilities
- **Pattern**: Input → Context → Reason → Act → Verify → Respond

### 2. Parallel Execution Strategy

| Phase | Parallelizable? | Tools Used | Notes |
|-------|-----------------|------------|--------|
| Document retrieval | ✅ | `item_completed`, `web_search` | Can run concurrently when multiple sources needed |
| Code execution | ✅ | `exec`, `shell_command` | Batch multiple computations |
| Reasoning | ✅ | `reasoning` | Can process multiple sub-questions in parallel |
| External lookup | ✅ | `web_search` | Fetch additional context |
| Final response | ❌ | `send_message` | Single output per task sequence |

### 3. State Management

Each task maintains a `Plan` object with:
- `task_id`: Unique identifier
- `status`: started → active → completed → failed
- `steps`: Array of executed sub-tasks
- `results`: Collected outputs from each step
- `verification`: Pass/fail flag for each step

### 4. Workflow Steps

1. **Parse & Decompose** (`codex` subagent)
   - Extract intent, entities, constraints
   - Generate task sequence

2. **Execute Independent Work** (parallel)
   - `item_completed` (document loading)
   - `web_search` (external lookup)
   - `exec` / `shell_command` (computations)

3. **Reason & Validate** (`codex` subagent)
   - Perform logical deduction
   - Cross-check results

4. **Verify** (`update_plan`)
   - Confirm all prerequisites met
   - Ensure no missing dependencies

5. **Respond** (`send_message`)
   - Compose final answer
   - Attach supporting evidence

## Mode Configuration

### Primary Agents

| Agent | Role | Model | Responsibilities |
|-------|------|-------|------------------|
| Planner | Task decomposition | `litellm/gpt-5.6-sol` | Break down queries, assign sub-tasks |
| Researcher | Data gathering | `litellm/gpt-5.6-terra` | Execute `exec`/`shell_command`, fetch web data |
| Analyst | Reasoning & validation | `litellm/gpt-5.6-sol` | Perform logical inference, verify results |
| Communicator | Response generation | `litellm/gpt-5.6-sol` | Format and send final answers |

### Sub-Agent Types

- **`codex`**: Handles task decomposition and planning
- **`explore`**: Optional - for rapid document discovery
- **`general`**: Fallback for complex reasoning
- **`luna`**: Alternative planning seat (mid-tier)
- **`sol`**: Same-transport critique (cross-vendor validation)

## Implementation Guidelines

### Task Definition Template

Each task should follow this structure:
```json
{
  "id": "task_123",
  "type": "decompose",
  "steps": [
    {
      "name": "load_document",
      "tool": "item_completed",
      "params": {...}
    },
    {
      "name": "run_code",
      "tool": "exec",
      "params": {...}
    }
  ],
  "dependencies": ["input_parsed"]
}
```

### Parallelism Rules

- **Never start more than N concurrent `exec`/`shell_command` calls** (N=3-5 based on provider timeout)
- **Group independent `item_completed` calls** together
- **Sequence dependent steps** (e.g., reasoning after data collection)
- **Use `wait`** to ensure async operations complete before proceeding

### Verification Protocol

1. After each major step, call `update_plan` with `"status": "verified"`
2. Before `send_message`, ensure all prerequisite steps are marked `completed`
3. Log intermediate results for auditability

## Example Usage Flow

```
User: "Find the average price of items in this CSV and compare with online prices"

1. Planner → Decompose into:
   - Step 1: Load CSV (item_completed)
   - Step 2: Calculate average (exec)
   - Step 3: Search web for comparable prices (web_search)
   - Step 4: Compare and summarize (reasoning)

2. Parallel execution:
   - item_completed (CSV loading) ──┐
   - exec (average calculation) ───┼─→ All start together
   - web_search (price comparison) ─┘

3. Sequential reasoning:
   - reasoning (compare results)

4. Verification:
   - update_plan (all steps verified)

5. Response:
   - send_message (final answer with computed average and price comparison)
```

## Monitoring & Observability

- Track task duration and success rates
- Log tool call counts per agent type
- Alert on `failed` task states
- Periodic review of `inter_agent_communication_metadata` for coordination efficiency

## Compliance Notes

- Follow the seat map: use `litellm/gpt-5.6-sol` for primary work (top tier)
- Respect provider timeouts (600s max per task)
- Do not use Anthropic models (not in the LiteLLM catalog)
- All tool calls must be within the same transport (no cross-vendor mixing for core work)
