from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Sequence

import pytest
from src.hos.checkpoint_publisher import CheckpointError, CheckpointPublisher, SubprocessRunner

ISSUE = {
    "title": "Automate checkpoint publication",
    "body": "## Purpose\n\nScope\n\n## Acceptance criteria\n\nPass\n\n## Scope boundaries\n\nStop",
    "state": "OPEN",
    "url": "https://github.com/example/repo/issues/7",
}
PROTECTION = {
    "required_status_checks": {
        "strict": True,
        "contexts": ["lint", "typecheck", "tests", "windows-tests", "checkpoint-record"],
    },
    "enforce_admins": {"enabled": True},
}
PENDING_PR = {
    "number": 14,
    "title": "Checkpoint: issue #7",
    "url": "https://github.com/example/repo/pull/14",
    "state": "OPEN",
    "baseRefName": "main",
    "headRefName": "codex/issue-7-checkpoint-automation",
    "body": "Closes #7\n\n<!-- hos-issue-spec-sha256:"
    + hashlib.sha256(ISSUE["body"].strip().encode("utf-8")).hexdigest()
    + " -->",
    "isDraft": False,
    "mergedAt": None,
}


class FakeRunner:
    def __init__(self, root: Path, worktree_root: Path) -> None:
        self.root = root.resolve()
        self.worktree_root = worktree_root.resolve()
        self.calls: list[tuple[str, ...]] = []
        self.dirty = {"checkpoints/CURRENT.md", "src/example.py"}
        self.untracked: set[str] = set()
        self.staged: set[str] = set()
        self.branch = "codex/issue-7-checkpoint-automation"
        self.issue = ISSUE.copy()
        self.protection = PROTECTION.copy()
        self.prs: list[dict[str, object]] = []
        self.status_checks: list[dict[str, str]] = [
            {"name": name, "status": "IN_PROGRESS"}
            for name in ("lint", "typecheck", "tests", "windows-tests", "checkpoint-record")
        ]
        self.allow_auto_merge = True
        self.merge_immediately = False
        self.base_tip = "base-sha"
        self.common_ancestor = "base-sha"
        self.behind_count = "1"
        self.changed_since_base = {"checkpoints/CURRENT.md", "src/example.py"}
        self.canonical_dirty = ""
        self.task_dirty = ""
        self.pr_view: dict[str, object] = {
            "state": "OPEN",
            "mergedAt": None,
            "baseRefName": "main",
            "headRefName": self.branch,
            "body": "Closes #7",
            "mergeCommit": {"oid": "merge-sha"},
        }
        self.worktree_registered = True
        self.reconcile_mode = False
        self.removed: list[str] = []
        self.patch = "diff --git a/src/example.py b/src/example.py\n+value = 1\n"
        self.created_pr_body = ""

    def run(self, args: Sequence[str], cwd: Path | None = None) -> str:
        command = tuple(args)
        self.calls.append(command)
        if command[0] == "gh":
            return self._gh(command[1:])
        if command[0] == "git":
            index = command.index("-C")
            git_args = command[index + 2 :]
            git_cwd = Path(command[index + 1]).resolve()
            return self._git(git_args, git_cwd)
        raise AssertionError(f"Unexpected executable: {command[0]}")

    def _gh(self, args: Sequence[str]) -> str:
        if args[:3] == ("repo", "view", "--json"):
            return json.dumps({"nameWithOwner": "example/repo"})
        if args[:3] == ("issue", "view", "7"):
            return json.dumps(self.issue)
        if args[:2] == ("api", "repos/example/repo/branches/main/protection"):
            return json.dumps(self.protection)
        if args[:2] == ("api", "repos/example/repo"):
            if "PATCH" in args:
                self.allow_auto_merge = True
                return "{}"
            return json.dumps({"allow_auto_merge": self.allow_auto_merge})
        if args[:2] == ("pr", "list"):
            return json.dumps(self.prs)
        if args[:2] == ("pr", "view") and "statusCheckRollup" in args:
            return json.dumps({"statusCheckRollup": self.status_checks})
        if args[:2] == ("pr", "view") and "state,mergedAt" in args:
            return json.dumps(
                {"state": self.pr_view["state"], "mergedAt": self.pr_view["mergedAt"]}
            )
        if args[:2] == ("pr", "view"):
            self.reconcile_mode = True
            return json.dumps(self.pr_view)
        if args[:2] == ("pr", "create"):
            self.created_pr_body = args[args.index("--body") + 1]
            return "https://github.com/example/repo/pull/14"
        if args[:2] == ("pr", "edit"):
            body = args[args.index("--body") + 1]
            self.pr_view["body"] = body
            self.created_pr_body = body
            for pr in self.prs:
                if pr["number"] == int(args[2]):
                    pr["body"] = body
            return ""
        if args[:2] == ("pr", "merge"):
            if self.merge_immediately:
                self.pr_view["state"] = "MERGED"
                self.pr_view["mergedAt"] = "2026-09-24T00:00:00Z"
            return ""
        raise AssertionError(f"Unexpected GitHub command: {args}")

    def _git(self, args: Sequence[str], cwd: Path) -> str:
        if args == ("rev-parse", "--show-toplevel"):
            return str(self.root)
        if args == ("branch", "--show-current"):
            return "main" if self.reconcile_mode else self.branch
        if args == ("diff", "HEAD", "--name-only", "-z"):
            return "\0".join(sorted(self.dirty))
        if args == ("ls-files", "--others", "--exclude-standard", "-z"):
            return "\0".join(sorted(self.untracked))
        if args[:4] == ("diff", "--cached", "--name-only", "-z"):
            return "\0".join(sorted(self.staged))
        if args[:3] == ("diff", "--cached", "--binary"):
            return self.patch
        if args[0] == "diff" and "--check" in args:
            return ""
        if args and args[0] == "add":
            self.staged = set(args[2:])
            return ""
        if args and args[0] == "reset":
            self.staged.clear()
            return ""
        if args and args[0] == "commit":
            self.dirty.clear()
            self.staged.clear()
            return "commit-sha"
        if args == ("log", "-1", "--format=%B"):
            digest = hashlib.sha256(ISSUE["body"].strip().encode("utf-8")).hexdigest()
            return (
                "checkpoint: issue #7 - Automate checkpoint publication\n\n"
                f"Issue-Spec-SHA256: {digest}"
            )
        if args == ("fetch", "origin", "main"):
            return ""
        if args == ("rev-parse", "origin/main"):
            return self.base_tip
        if args == ("merge-base", "origin/main", "HEAD"):
            return self.common_ancestor
        if args == ("rev-list", "--count", "origin/main..HEAD"):
            return self.behind_count
        if args == ("diff", "--name-only", "origin/main...HEAD", "-z"):
            return "\0".join(sorted(self.changed_since_base))
        if args and args[0] == "push":
            return ""
        if args == ("status", "--porcelain", "--untracked-files=all"):
            if cwd == self.root and self.reconcile_mode:
                return self.canonical_dirty
            return self.task_dirty
        if args == ("rev-parse", "--path-format=absolute", "--git-common-dir"):
            return str(cwd / ".git")
        if args == ("worktree", "list", "--porcelain"):
            if not self.worktree_registered:
                return f"worktree {cwd}\nHEAD main-sha\nbranch refs/heads/main\n"
            target = self.worktree_root / "issue-7"
            return (
                f"worktree {cwd}\nHEAD main-sha\nbranch refs/heads/main\n\n"
                f"worktree {target}\nHEAD task-sha\nbranch refs/heads/{self.branch}\n"
            )
        if args == ("merge", "--ff-only", "origin/main"):
            return ""
        if args == ("merge-base", "merge-sha", "HEAD"):
            return "merge-sha"
        if args[:2] == ("worktree", "remove"):
            self.removed.append(args[2])
            return ""
        raise AssertionError(f"Unexpected Git command: {args} at {cwd}")


def test_subprocess_runner_reads_utf8_output() -> None:
    code = (
        "import sys; sys.stdout.reconfigure(encoding='utf-8'); "
        "print('curly quote: \\u2019 and caf\\u00e9')"
    )
    output = SubprocessRunner().run((sys.executable, "-c", code))
    assert output == "curly quote: \u2019 and caf\u00e9"


def test_subprocess_runner_fails_closed_on_invalid_utf8() -> None:
    with pytest.raises(CheckpointError, match="not valid UTF-8"):
        SubprocessRunner().run(
            (sys.executable, "-c", "import sys; sys.stdout.buffer.write(b'\\xff')")
        )


@pytest.fixture
def setup(tmp_path: Path) -> tuple[CheckpointPublisher, FakeRunner, Path, Path]:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "checkpoints").mkdir()
    (root / "src").mkdir()
    (root / "checkpoints" / "CURRENT.md").write_text(
        "# Current\n\nGitHub issue #7 is active.\n\n## Next action\n\nImplement the publisher.\n",
        encoding="utf-8",
    )
    (root / "src" / "example.py").write_text("value = 1\n", encoding="utf-8")
    worktree_root = tmp_path / "worktrees"
    worktree_root.mkdir()
    runner = FakeRunner(root, worktree_root)
    publisher = CheckpointPublisher(root, runner, worktree_root)
    return publisher, runner, root, worktree_root


def test_dry_run_validates_checkpoint_without_side_effects(setup) -> None:
    publisher, runner, _, _ = setup
    result = publisher.publish(
        7,
        ["checkpoints/CURRENT.md", "src/example.py"],
        dry_run=True,
    )
    assert result.state == "would_publish"
    assert result.dry_run is True
    commands = [call[3:] for call in runner.calls if call[0] == "git"]
    assert not any(command and command[0] in {"add", "commit", "push"} for command in commands)
    assert not any(
        call[:2] in {("gh", "pr"), ("gh", "api")} and "PATCH" in call for call in runner.calls
    )


def test_unrelated_dirty_path_refuses_publication(setup) -> None:
    publisher, runner, _, _ = setup
    runner.dirty.add("README.md")
    with pytest.raises(CheckpointError, match="exactly match"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"], dry_run=True)


@pytest.mark.parametrize(
    "path",
    [
        "data/private.json",
        ".controller-runs/run/events.ndjson",
        ".env",
        ".envrc",
        ".env.production",
        ".harness-cache/opencode/config.json",
        "node_modules/pkg/index.js",
        ".git/config",
        "traces/session.ndjson",
        "../outside.txt",
        "D:/private.txt",
    ],
)
def test_private_and_outside_paths_are_rejected(setup, path: str) -> None:
    publisher, _, _, _ = setup
    with pytest.raises(CheckpointError):
        publisher._safe_path(path)


def test_issue_without_frozen_acceptance_sections_is_rejected(setup) -> None:
    publisher, runner, _, _ = setup
    runner.issue["body"] = "Only a sentence."
    with pytest.raises(CheckpointError, match="frozen scope"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"], dry_run=True)


def test_missing_issue_fails_closed(setup) -> None:
    publisher, runner, _, _ = setup
    runner.issue = {}
    with pytest.raises(CheckpointError, match="no readable acceptance criteria"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"], dry_run=True)


def test_base_branch_is_never_publishable(setup) -> None:
    publisher, runner, _, _ = setup
    runner.branch = "main"
    with pytest.raises(CheckpointError, match="task branch"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"], dry_run=True)


def test_branch_for_another_issue_cannot_be_published(setup) -> None:
    publisher, runner, _, _ = setup
    runner.branch = "codex/issue-70-something"
    with pytest.raises(CheckpointError, match="task branch"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"], dry_run=True)


def test_private_content_is_unstaged_and_not_committed(setup) -> None:
    publisher, runner, _, _ = setup
    secret = "ghp_" + "123456789012345678901234567890"
    runner.patch = f"diff --git a/src/example.py b/src/example.py\n+token = '{secret}'\n"
    with pytest.raises(CheckpointError, match="credential or private path"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"])
    assert runner.staged == set()
    commands = [call[3:] for call in runner.calls if call[0] == "git"]
    assert not any(command and command[0] in {"commit", "push"} for command in commands)


def test_binary_patch_guard_does_not_match_its_split_text_representation(setup) -> None:
    publisher, runner, _, _ = setup
    runner.patch = (
        'diff --git a/src/example.py b/src/example.py\n+binary_header = "GIT " + "binary patch"\n'
    )
    publisher._scan_selected_changes(["src/example.py"])


def test_raw_prompt_markers_are_rejected(setup) -> None:
    publisher, runner, _, _ = setup
    marker = "<" + "environment_context>"
    runner.patch = f"diff --git a/src/example.py b/src/example.py\n+prompt = {marker!r}\n"
    with pytest.raises(CheckpointError, match="Raw prompt or transcript"):
        publisher._scan_selected_changes(["src/example.py"])


def test_pre_staged_changes_are_preserved_and_publication_stops(setup) -> None:
    publisher, runner, _, _ = setup
    runner.staged = {"src/example.py"}
    with pytest.raises(CheckpointError, match="staging area must be clean"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"])
    assert runner.staged == {"src/example.py"}
    assert not any(
        call[3:] and call[3] in {"add", "reset", "commit", "push"}
        for call in runner.calls
        if call[0] == "git"
    )


@pytest.mark.parametrize(
    ("prefix", "suffix"),
    [
        ("xai-", "12345678901234567890123456789012"),
        ("AIza", "12345678901234567890123456789012345"),
        ("AKIA", "1234567890ABCDEF"),
    ],
)
def test_common_provider_credentials_are_rejected(setup, prefix: str, suffix: str) -> None:
    publisher, runner, _, _ = setup
    secret = prefix + suffix
    runner.patch = f"diff --git a/src/example.py b/src/example.py\n+token = '{secret}'\n"
    with pytest.raises(CheckpointError, match="credential or private path"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"])
    assert runner.staged == set()


def test_branch_protection_requires_every_check_and_no_bypass(setup) -> None:
    publisher, runner, _, _ = setup
    runner.protection["required_status_checks"] = {"strict": False, "contexts": ["lint"]}
    with pytest.raises(CheckpointError, match="required strict CI checks"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"], dry_run=True)


def test_existing_pr_rejects_changed_issue_spec(setup) -> None:
    publisher, runner, _, _ = setup
    runner.dirty.clear()
    runner.prs = [dict(PENDING_PR, body="Closes #7")]
    with pytest.raises(CheckpointError, match="scope changed"):
        publisher.publish(7)


def test_missing_checkpoint_or_issue_reference_is_rejected(setup) -> None:
    publisher, _, root, _ = setup
    (root / "checkpoints" / "CURRENT.md").write_text(
        "# Current\n\n## Next action\n\nContinue.\n", encoding="utf-8"
    )
    with pytest.raises(CheckpointError, match="real GitHub issue"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"], dry_run=True)


def test_stale_base_refuses_before_staging_or_committing(setup) -> None:
    publisher, runner, _, _ = setup
    runner.common_ancestor = "old-base-sha"
    with pytest.raises(CheckpointError, match="stale"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"])
    commands = [call[3:] for call in runner.calls if call[0] == "git"]
    assert not any(command and command[0] in {"add", "commit", "push"} for command in commands)


def test_open_pr_returns_pending_ci_merge_and_does_not_wait(setup) -> None:
    publisher, runner, _, _ = setup
    runner.dirty.clear()
    runner.prs = [PENDING_PR]
    result = publisher.publish(7)
    assert result.state == "pending_ci_merge"
    assert result.pull_request == 14
    assert any(call[:3] == ("gh", "pr", "merge") for call in runner.calls)


def test_open_pr_can_be_updated_from_explicit_checkpoint_paths(setup) -> None:
    publisher, runner, _, _ = setup
    runner.prs = [dict(PENDING_PR)]
    result = publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"])
    assert result.state == "pending_ci_merge"
    git_commands = [call[3:] for call in runner.calls if call[0] == "git"]
    assert any(command and command[0] == "commit" for command in git_commands)
    assert any(command and command[0] == "push" for command in git_commands)
    assert any(call[:3] == ("gh", "pr", "merge") for call in runner.calls)


def test_open_pr_update_dry_run_does_not_stage_or_push(setup) -> None:
    publisher, runner, _, _ = setup
    runner.prs = [dict(PENDING_PR)]
    result = publisher.publish(
        7,
        ["checkpoints/CURRENT.md", "src/example.py"],
        dry_run=True,
    )
    assert result.state == "would_update_pr"
    assert result.dry_run is True
    git_commands = [call[3:] for call in runner.calls if call[0] == "git"]
    assert not any(command and command[0] in {"add", "commit", "push"} for command in git_commands)


def test_open_pr_update_refuses_unlisted_or_private_changes(setup) -> None:
    publisher, runner, _, _ = setup
    runner.prs = [dict(PENDING_PR)]
    runner.dirty.add("README.md")
    with pytest.raises(CheckpointError, match="exactly match"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"])


def test_failed_required_check_does_not_enable_auto_merge_or_mark_complete(setup) -> None:
    publisher, runner, _, _ = setup
    runner.dirty.clear()
    runner.prs = [PENDING_PR]
    runner.status_checks = [{"name": "lint", "status": "COMPLETED", "conclusion": "FAILURE"}]
    result = publisher.publish(7)
    assert result.state == "checks_failed"
    assert not any(call[:3] == ("gh", "pr", "merge") for call in runner.calls)
    assert not any(call[:2] == ("gh", "api") and "PATCH" in call for call in runner.calls)
    assert "hos-checkpoint-state:checks_failed" in str(runner.prs[0]["body"])


def test_required_checks_must_all_be_present_and_successful(setup) -> None:
    publisher, runner, _, _ = setup
    runner.status_checks = [
        {"name": name, "status": "COMPLETED", "conclusion": "SUCCESS"}
        for name in ("lint", "typecheck", "tests", "windows-tests", "checkpoint-record")
    ]
    assert publisher._check_results(14) == "checks_passed"
    runner.status_checks.pop()
    assert publisher._check_results(14) == "checks_pending"


def test_auto_merge_is_enabled_once_for_an_eligible_pr(setup) -> None:
    publisher, runner, _, _ = setup
    runner.dirty.clear()
    runner.prs = [PENDING_PR]
    runner.allow_auto_merge = False
    result = publisher.publish(7)
    assert result.state == "pending_ci_merge"
    assert runner.allow_auto_merge is True
    assert any(call[:2] == ("gh", "api") and "PATCH" in call for call in runner.calls)


def test_merged_existing_pr_is_idempotently_reported(setup) -> None:
    publisher, runner, _, _ = setup
    merged = dict(PENDING_PR, state="MERGED", mergedAt="2026-09-24T00:00:00Z")
    runner.prs = [merged]
    result = publisher.publish(7)
    assert result.state == "merged"
    assert not any(call[:3] == ("gh", "pr", "merge") for call in runner.calls)


def test_merged_pr_remains_idempotent_after_github_closes_linked_issue(setup) -> None:
    publisher, runner, _, _ = setup
    runner.issue["state"] = "CLOSED"
    runner.prs = [dict(PENDING_PR, state="MERGED", mergedAt="2026-09-24T00:00:00Z")]
    assert publisher.publish(7).state == "merged"


def test_closed_issue_without_merged_pr_cannot_publish(setup) -> None:
    publisher, runner, _, _ = setup
    runner.issue["state"] = "CLOSED"
    with pytest.raises(CheckpointError, match="must be open"):
        publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"], dry_run=True)


def test_new_checkpoint_is_committed_published_and_queued_asynchronously(setup) -> None:
    publisher, runner, _, _ = setup
    result = publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"])
    assert result.state == "pending_ci_merge"
    assert result.url == "https://github.com/example/repo/pull/14"
    assert any(call[:2] == ("git", "-C") and "commit" in call for call in runner.calls)
    assert any(call[:2] == ("git", "-C") and "push" in call for call in runner.calls)
    assert any(call[:2] == ("gh", "pr") and "create" in call for call in runner.calls)
    assert "hos-issue-spec-sha256:" in runner.created_pr_body
    assert "hos-checkpoint-state:pending_ci_merge" in runner.created_pr_body


def test_publish_confirms_immediate_merge_instead_of_reporting_pending(setup) -> None:
    publisher, runner, _, _ = setup
    runner.merge_immediately = True
    result = publisher.publish(7, ["checkpoints/CURRENT.md", "src/example.py"])
    assert result.state == "merged"


def test_reconcile_refuses_before_github_confirms_merge(setup) -> None:
    publisher, runner, _, worktree_root = setup
    runner.pr_view = dict(runner.pr_view, state="OPEN", mergedAt=None)
    with pytest.raises(CheckpointError, match="only after GitHub confirms"):
        publisher.reconcile(14, worktree_root / "issue-7")
    assert not runner.removed


def test_reconcile_preserves_dirty_canonical_checkout(setup) -> None:
    publisher, runner, _, worktree_root = setup
    runner.pr_view["state"] = "MERGED"
    runner.pr_view["mergedAt"] = "2026-09-24T00:00:00Z"
    runner.canonical_dirty = " M HANDOFF.md"
    result = publisher.reconcile(14, worktree_root / "issue-7")
    assert result.state == "merged_cleanup_blocked_dirty_canonical"
    assert not runner.removed


def test_reconcile_preserves_dirty_task_worktree(setup) -> None:
    publisher, runner, _, worktree_root = setup
    runner.pr_view["state"] = "MERGED"
    runner.pr_view["mergedAt"] = "2026-09-24T00:00:00Z"
    target = worktree_root / "issue-7"
    target.mkdir()
    runner.task_dirty = "?? notes.txt"
    result = publisher.reconcile(14, target)
    assert result.state == "merged_cleanup_blocked_dirty_worktree"
    assert not runner.removed
    assert not any(call[3:] == ("merge", "--ff-only", "origin/main") for call in runner.calls)


def test_reconcile_updates_canonical_and_removes_only_registered_clean_worktree(setup) -> None:
    publisher, runner, _, worktree_root = setup
    runner.pr_view["state"] = "MERGED"
    runner.pr_view["mergedAt"] = "2026-09-24T00:00:00Z"
    target = worktree_root / "issue-7"
    target.mkdir()
    result = publisher.reconcile(14, target)
    assert result.state == "complete"
    assert runner.removed == [str(target.resolve())]


def test_reconcile_is_idempotent_after_worktree_was_already_removed(setup) -> None:
    publisher, runner, _, worktree_root = setup
    runner.pr_view["state"] = "MERGED"
    runner.pr_view["mergedAt"] = "2026-09-24T00:00:00Z"
    target = worktree_root / "issue-7"
    runner.worktree_registered = False
    result = publisher.reconcile(14, target)
    assert result.state == "complete"
    assert not runner.removed


def test_reconcile_reports_interrupted_removal_with_stale_registration(setup) -> None:
    publisher, runner, _, worktree_root = setup
    runner.pr_view["state"] = "MERGED"
    runner.pr_view["mergedAt"] = "2026-09-24T00:00:00Z"
    target = worktree_root / "issue-7"
    runner.worktree_registered = True
    result = publisher.reconcile(14, target)
    assert result.state == "merged_cleanup_blocked_stale_registration"
    assert not runner.removed


def test_reconcile_rejects_wrong_worktree_path_before_advancing_canonical(setup) -> None:
    publisher, runner, _, worktree_root = setup
    runner.pr_view["state"] = "MERGED"
    runner.pr_view["mergedAt"] = "2026-09-24T00:00:00Z"
    wrong_path = worktree_root / "different-worktree"
    with pytest.raises(CheckpointError, match="different worktree path"):
        publisher.reconcile(14, wrong_path)
    assert not any(call[3:] == ("merge", "--ff-only", "origin/main") for call in runner.calls)


def test_reconcile_rejects_unregistered_existing_path_before_advancing_canonical(setup) -> None:
    publisher, runner, _, worktree_root = setup
    runner.pr_view["state"] = "MERGED"
    runner.pr_view["mergedAt"] = "2026-09-24T00:00:00Z"
    runner.worktree_registered = False
    target = worktree_root / "unregistered"
    target.mkdir()
    with pytest.raises(CheckpointError, match="not a registered repository worktree"):
        publisher.reconcile(14, target)
    assert not any(call[3:] == ("merge", "--ff-only", "origin/main") for call in runner.calls)


def test_reconcile_rejects_path_outside_approved_worktree_root(setup, tmp_path: Path) -> None:
    publisher, runner, _, _ = setup
    runner.pr_view["state"] = "MERGED"
    runner.pr_view["mergedAt"] = "2026-09-24T00:00:00Z"
    with pytest.raises(CheckpointError, match="outside the approved"):
        publisher.reconcile(14, tmp_path / "elsewhere")
