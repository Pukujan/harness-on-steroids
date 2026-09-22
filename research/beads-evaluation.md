# Beads evaluation

Beads is a credible candidate for the durable task layer of this project. It is a distributed graph issue tracker for coding agents, backed by Dolt, with persistent issues, dependency edges, ready-work detection, atomic claiming, and explicit close/release flow. That gives long-horizon work a durable task graph instead of relying on a single prompt or a large markdown plan.

The useful boundary is:

- Beads stores durable work: parent tasks, child tasks, blockers, claims, notes, recovery context, and cross-agent coordination.
- A runtime state machine controls the current agent turn: what phase is active, which actions are allowed, what evidence is required before a transition, and which verification must run next.
- Prompt and context remain the behavior layer. Beads supplies durable state and the runtime machine supplies narrow enforcement where experiments show it helps.

Beads has a direct Codex integration. `bd setup codex` installs a skill, a managed `AGENTS.md` section, `.codex/config.toml` hook enablement, and lifecycle hooks. The hooks inject `bd prime` at session start and refresh the context after compaction. Its documented storage choices are embedded Dolt for the normal single-writer case and server-backed Dolt for concurrent writers; `--stealth` and `BEADS_DIR` support isolated or git-free use.

This repository should not run `bd init` automatically. It would modify the project guidance and Codex hook surface, which must be reconciled with the owner constitution first. The safe evaluation slice is a separate checkout or isolated `BEADS_DIR` using a small existing Work task: compare task recovery, blocker handling, and compaction recovery with the current checkpoint workflow, then keep, refine, or remove the integration based on observable results.

Sources:

- Beads repository and current README: <https://github.com/gastownhall/beads>
- Beads documentation: <https://beads.gascity.com/>
- Beads Codex integration: <https://beads.gascity.com/integrations/codex>
