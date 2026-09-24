# Checkpoint publisher

`tools/checkpoint.py` implements the local part of GitHub issue #7. It commits
only explicitly listed checkpoint paths on an issue branch, creates or reuses
one linked pull request, and asks GitHub to auto-merge after protected checks
pass. The publisher exits with `pending_ci_merge`; it does not wait for CI.
GitHub's branch protection remains the merge authority.

## Publish a checkpoint

Run from the task worktree after the issue acceptance criteria are frozen and
`checkpoints/CURRENT.md` records the verified result and next action:

```powershell
python tools/checkpoint.py publish --issue 7 --dry-run `
  --include .github/workflows/owner-gate.yml `
  --include checkpoints/CURRENT.md `
  --include HANDOFF.md `
  --include ISSUES.md `
  --include docs/checkpoint-publisher.md `
  --include src/hos/checkpoint_publisher.py `
  --include tests/test_checkpoint_publisher.py `
  --include tests/test_ci_contract.py `
  --include tools/checkpoint.py
```

Review the dry-run response, then repeat without `--dry-run`. Every dirty path
must exactly match the explicit `--include` list. The command rejects the base
branch, a stale issue branch, closed or underspecified issues, missing
checkpoint linkage, private/generated paths, raw prompt markers, credentials,
binary files, a pre-staged Git index, duplicate/ambiguous PRs, and failed
checks. It refuses rather than cleaning an unexpected file or staging an
unlisted path.

The resulting PR links to its issue and carries the checkpoint evidence. The
publisher enables the repository auto-merge capability if needed, opts that
eligible PR into squash auto-merge, then checks GitHub's state again. Its JSON
response is `pending_ci_merge` while checks or GitHub's merge queue are
pending, `checks_failed` when a check failed, and `merged` only when GitHub
confirms the merge. If the PR is already open and the issue branch has a new
verified checkpoint update, pass every changed path with `--include`; the
publisher commits and pushes that update to the same branch to retrigger CI.
The update must still include `checkpoints/CURRENT.md` and pass the same
private-artifact checks.

## Reconcile a merged worktree

Run the command from the canonical D: checkout after GitHub reports the PR as
merged:

```powershell
python tools/checkpoint.py reconcile --pr 123 `
  --worktree-path D:\claude\harnessonsteroids\worktrees\issue-7-checkpoint-automation
```

Reconciliation verifies the PR merge and issue link, requires the canonical
checkout to be clean and on `main`, fast-forwards it from `origin/main`, and
removes only a clean registered worktree under the approved D: worktree root
whose branch matches the merged PR. If the canonical checkout or task worktree
is dirty, it returns a blocked state and preserves both. Re-running after an
interrupted cleanup is safe; an already removed task worktree is treated as
complete only after the PR's merge commit is present in the canonical checkout.

GitHub state is the durable source for the PR, required checks, and merge.
Local cleanup state is reconstructed from the PR and registered Git worktrees,
so an interrupted local process can resume without a separate state database.

## Why the project uses GitHub Issues

HOS keeps the executable specification on the GitHub issue because it is
already connected to the task branch, PR, required checks, and merge state.
Use a sub-issue only for a separately verifiable deliverable with its own
acceptance criteria; keep implementation steps as a checklist in the parent.
`ISSUES.md` remains a historical map, not a second active backlog. GitHub
supports issue hierarchies, blocking relationships, and Projects for planning
when the work graph needs them. Jira adds value for cross-team, cross-project
planning and reporting; HOS does not currently need that extra system.

The asynchronous boundary is intentional: the agent publishes the PR and
queues auto-merge, while GitHub enforces the required checks and protected
branch rules. GitHub documents auto-merge as waiting for required checks and
reviews; the exact review policy remains project-specific.

- [GitHub Issues, sub-issues, and dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)
- [GitHub auto-merge](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request)
- [Jira timeline and dependency planning](https://www.atlassian.com/software/jira/guides/basic-roadmaps/overview)
