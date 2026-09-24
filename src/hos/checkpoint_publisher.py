"""Issue-backed checkpoint publication and local merge reconciliation.

The publisher deliberately delegates GitHub policy enforcement to GitHub's
protected-branch checks and auto-merge. It never pushes to the base branch and
never removes a dirty or unmerged worktree.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Any, Protocol, Sequence

REQUIRED_CHECKS = ("lint", "typecheck", "tests", "windows-tests", "checkpoint-record")
DEFAULT_BASE_BRANCH = "main"
DEFAULT_WORKTREE_ROOT = Path(r"D:\claude\harnessonsteroids\worktrees")
BINARY_PATCH_HEADER = "GIT " + "binary patch"

_FORBIDDEN_PARTS = {
    ".controller-runs",
    ".harness-cache",
    ".git",
    ".sol",
    ".tools",
    ".venv",
    "auth.json",
    "data",
    "node_modules",
}
_FORBIDDEN_SUFFIXES = {
    ".db",
    ".env",
    ".jsonl",
    ".ndjson",
    ".key",
    ".pem",
    ".sqlite",
    ".sqlite3",
}
_SECRET_PATTERNS = (
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{24,}\b"),
    re.compile(r"\bxai-[A-Za-z0-9_-]{24,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~-]{24,}\b", re.IGNORECASE),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\", re.IGNORECASE),
)
_PROMPT_MARKERS = tuple(
    "<" + tag
    for tag in (
        "recommended_plugins>",
        "environment_context>",
        "user>",
        "assistant>",
        "tool_call>",
        "tool_result>",
    )
)


class CheckpointError(RuntimeError):
    """A fail-closed checkpoint validation or GitHub operation error."""


class CommandRunner(Protocol):
    def run(self, args: Sequence[str], cwd: Path | None = None) -> str: ...


class SubprocessRunner:
    """Run commands without echoing their output, which may contain private data."""

    def run(self, args: Sequence[str], cwd: Path | None = None) -> str:
        try:
            result = subprocess.run(
                list(args),
                cwd=cwd,
                text=True,
                encoding="utf-8",
                errors="surrogateescape",
                capture_output=True,
                check=False,
            )
        except OSError as exc:
            raise CheckpointError(f"Could not start {args[0]}.") from exc
        if result.stdout is None or result.stderr is None:
            raise CheckpointError("The command output could not be decoded safely.")
        try:
            result.stdout.encode("utf-8", errors="strict")
            result.stderr.encode("utf-8", errors="strict")
        except UnicodeEncodeError as exc:
            raise CheckpointError("The command output was not valid UTF-8.") from exc
        if result.returncode:
            # Tool stderr can contain prompt fragments or credential-bearing URLs.
            raise CheckpointError(f"{Path(args[0]).name} failed (exit {result.returncode}).")
        return result.stdout.strip()


@dataclass(frozen=True)
class PublishResult:
    state: str
    issue: int
    branch: str
    pull_request: int | None = None
    url: str | None = None
    dry_run: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "issue": self.issue,
            "branch": self.branch,
            "pull_request": self.pull_request,
            "url": self.url,
            "dry_run": self.dry_run,
        }


@dataclass(frozen=True)
class ReconcileResult:
    state: str
    pull_request: int
    canonical_checkout: str
    worktree: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "pull_request": self.pull_request,
            "canonical_checkout": self.canonical_checkout,
            "worktree": self.worktree,
        }


class CheckpointPublisher:
    def __init__(
        self,
        root: Path,
        runner: CommandRunner | None = None,
        worktree_root: Path = DEFAULT_WORKTREE_ROOT,
    ) -> None:
        self.root = root.resolve()
        self.runner = runner or SubprocessRunner()
        self.enforce_d_drive = worktree_root == DEFAULT_WORKTREE_ROOT
        self.worktree_root = worktree_root.resolve()

    def _git(self, *args: str, cwd: Path | None = None) -> str:
        command = ("git", "-C", str(cwd or self.root), *args)
        return self.runner.run(command)

    def _gh(self, *args: str) -> str:
        return self.runner.run(("gh", *args), cwd=self.root)

    def _gh_json(self, *args: str) -> Any:
        output = self._gh(*args)
        try:
            return json.loads(output)
        except json.JSONDecodeError as exc:
            raise CheckpointError("GitHub CLI returned invalid JSON.") from exc

    def _repo_slug(self) -> str:
        value = self._gh_json("repo", "view", "--json", "nameWithOwner")
        slug = value.get("nameWithOwner", "")
        if not isinstance(slug, str) or not re.fullmatch(r"[^/\s]+/[^/\s]+", slug):
            raise CheckpointError("Could not identify the GitHub repository.")
        return slug

    def _issue(self, number: int) -> dict[str, Any]:
        issue = self._gh_json("issue", "view", str(number), "--json", "title,body,state,url")
        body = issue.get("body")
        if not isinstance(body, str):
            raise CheckpointError("The linked issue has no readable acceptance criteria.")
        required_sections = ("## Purpose", "## Acceptance criteria", "## Scope boundaries")
        if any(section.casefold() not in body.casefold() for section in required_sections):
            raise CheckpointError("The linked issue needs frozen scope and acceptance criteria.")
        return issue

    @staticmethod
    def _issue_spec_digest(issue: dict[str, Any]) -> str:
        body = issue.get("body")
        if not isinstance(body, str):
            raise CheckpointError("The linked issue has no readable acceptance criteria.")
        return hashlib.sha256(body.strip().encode("utf-8")).hexdigest()

    def _protection(self, slug: str, base: str) -> dict[str, Any]:
        value = self._gh_json("api", f"repos/{slug}/branches/{base}/protection")
        checks = value.get("required_status_checks") or {}
        contexts = set(checks.get("contexts") or [])
        required = set(REQUIRED_CHECKS)
        if checks.get("strict") is not True or not required.issubset(contexts):
            raise CheckpointError("The base branch is missing required strict CI checks.")
        if value.get("enforce_admins", {}).get("enabled") is not True:
            raise CheckpointError("The base branch must retain its no-bypass protection.")
        return value

    @staticmethod
    def _safe_path(raw: str) -> str:
        path = Path(raw)
        windows_path = PureWindowsPath(raw)
        if (
            path.is_absolute()
            or windows_path.is_absolute()
            or re.match(r"^[A-Za-z]:", raw)
            or not raw
        ):
            raise CheckpointError("Checkpoint paths must be relative paths inside the repository.")
        normalized = raw.replace("\\", "/")
        if ".." in Path(normalized).parts:
            raise CheckpointError("Checkpoint paths must be relative paths inside the repository.")
        while normalized.startswith("./"):
            normalized = normalized[2:]
        parts = {part.casefold() for part in Path(normalized).parts}
        if parts & _FORBIDDEN_PARTS or Path(normalized).suffix.casefold() in _FORBIDDEN_SUFFIXES:
            raise CheckpointError(
                "A selected path points to private data or a generated dependency."
            )
        if Path(normalized).name.casefold().startswith(".env"):
            raise CheckpointError("Environment files cannot be published.")
        return normalized

    def _dirty_paths(self) -> set[str]:
        tracked = self._git("diff", "HEAD", "--name-only", "-z").split("\0")
        untracked = self._git("ls-files", "--others", "--exclude-standard", "-z").split("\0")
        return {item.replace("\\", "/") for item in (*tracked, *untracked) if item}

    def _check_current_checkpoint(self, issue: int) -> None:
        path = self.root / "checkpoints" / "CURRENT.md"
        if not path.is_file():
            raise CheckpointError("The checkpoint file is missing.")
        body = path.read_text(encoding="utf-8")
        issue_pattern = re.compile(rf"\b(?:GitHub\s+)?issue\s+#{issue}\b", re.IGNORECASE)
        if not issue_pattern.search(body):
            raise CheckpointError("CURRENT.md must name the real GitHub issue.")
        if not re.search(r"^##\s+Next action\s*$", body, re.IGNORECASE | re.MULTILINE):
            raise CheckpointError("CURRENT.md must contain an exact Next action section.")

    def _scan_selected_changes(self, paths: Sequence[str]) -> None:
        patch = self._git("diff", "--cached", "--binary", "--", *paths)
        if len(patch.encode("utf-8")) > 8_000_000:
            raise CheckpointError("The staged checkpoint is too large for safe publication.")
        if BINARY_PATCH_HEADER in patch or re.search(
            r"^Binary files .* differ$", patch, re.MULTILINE
        ):
            raise CheckpointError("Binary artifacts are not accepted in checkpoint commits.")
        for pattern in _SECRET_PATTERNS:
            if pattern.search(patch):
                raise CheckpointError(
                    "The staged checkpoint contains a credential or private path."
                )
        if any(marker.casefold() in patch.casefold() for marker in _PROMPT_MARKERS):
            raise CheckpointError("Raw prompt or transcript material is not publishable.")

    def _stage_checkpoint(
        self, issue_number: int, issue: dict[str, Any], spec_digest: str, selected: list[str]
    ) -> None:
        if self._git("diff", "--cached", "--name-only", "-z"):
            raise CheckpointError("The Git staging area must be clean before publication.")
        try:
            self._git("add", "--", *selected)
        except CheckpointError:
            self._git("reset", "--", *selected)
            raise
        staged = {
            item.replace("\\", "/")
            for item in self._git("diff", "--cached", "--name-only", "-z").split("\0")
            if item
        }
        if staged != set(selected):
            self._git("reset", "--", *selected)
            raise CheckpointError("The staged paths differ from the explicit checkpoint path list.")
        try:
            self._scan_selected_changes(selected)
            self._git("diff", "--cached", "--check")
        except CheckpointError:
            self._git("reset", "--", *selected)
            raise
        self._git(
            "commit",
            "-m",
            f"checkpoint: issue #{issue_number} - {issue['title']}",
            "-m",
            f"Issue-Spec-SHA256: {spec_digest}",
        )

    def _open_prs(self, branch: str) -> list[dict[str, Any]]:
        value = self._gh_json(
            "pr",
            "list",
            "--head",
            branch,
            "--state",
            "all",
            "--json",
            "number,title,url,state,baseRefName,headRefName,body,isDraft,mergedAt",
        )
        if not isinstance(value, list):
            raise CheckpointError("GitHub CLI returned an invalid pull request list.")
        return value

    def _ensure_auto_merge_available(self, slug: str) -> None:
        repo = self._gh_json("api", f"repos/{slug}")
        if repo.get("allow_auto_merge") is True:
            return
        self._gh("api", f"repos/{slug}", "--method", "PATCH", "-F", "allow_auto_merge=true")

    def _check_results(self, number: int) -> str:
        pr = self._gh_json("pr", "view", str(number), "--json", "statusCheckRollup")
        checks = pr.get("statusCheckRollup") or []
        failures = {
            "FAILURE",
            "ERROR",
            "CANCELLED",
            "TIMED_OUT",
            "ACTION_REQUIRED",
            "STARTUP_FAILURE",
            "NEUTRAL",
            "STALE",
        }
        required = set(REQUIRED_CHECKS)
        named = {
            (item.get("name") or item.get("context") or ""): item
            for item in checks
            if (item.get("name") or item.get("context")) in required
        }
        for check in named.values():
            conclusion = (check.get("conclusion") or check.get("state") or "").upper()
            if conclusion in failures:
                return "checks_failed"
        if not required.issubset(named):
            return "checks_pending"
        for item in named.values():
            state = (item.get("conclusion") or item.get("state") or "").upper()
            status = (item.get("status") or "").upper()
            if status != "COMPLETED" and state not in {"SUCCESS", "FAILURE", "ERROR"}:
                return "checks_pending"
            if state not in {"SUCCESS", "SKIPPED"}:
                return "checks_pending"
        return "checks_passed"

    def _merged(self, number: int) -> bool:
        pr = self._gh_json("pr", "view", str(number), "--json", "state,mergedAt")
        return pr.get("state") == "MERGED" and bool(pr.get("mergedAt"))

    def _set_pr_state(self, number: int, body: str, state: str) -> str:
        original = body
        marker = f"<!-- hos-checkpoint-state:{state} -->"
        visible = f"**Checkpoint state:** `{state}`"
        if re.search(r"(?m)^<!-- hos-checkpoint-state:[a-z_]+ -->$", body):
            body = re.sub(r"(?m)^<!-- hos-checkpoint-state:[a-z_]+ -->$", marker, body)
            body = re.sub(r"(?m)^\*\*Checkpoint state:\*\* `[^`]*`$", visible, body)
        else:
            body = f"{body.rstrip()}\n\n{visible}\n{marker}\n"
        if body != original:
            self._gh("pr", "edit", str(number), "--body", body)
        return body

    def publish(
        self,
        issue_number: int,
        include_paths: Sequence[str] = (),
        dry_run: bool = False,
        base_branch: str = DEFAULT_BASE_BRANCH,
    ) -> PublishResult:
        if Path(self._git("rev-parse", "--show-toplevel")).resolve() != self.root:
            raise CheckpointError("Run the publisher from the task repository root.")
        branch = self._git("branch", "--show-current")
        issue_branch = re.compile(rf"(?:^|[-/])issue-{issue_number}(?:[-/]|$)", re.IGNORECASE)
        if branch in {"", base_branch} or not issue_branch.search(branch):
            raise CheckpointError("Publish only from a task branch named for the linked issue.")

        issue = self._issue(issue_number)
        spec_digest = self._issue_spec_digest(issue)
        slug = self._repo_slug()
        self._protection(slug, base_branch)
        self._check_current_checkpoint(issue_number)

        if not dry_run:
            self._git("fetch", "origin", base_branch)
            base_tip = self._git("rev-parse", f"origin/{base_branch}")
            common_ancestor = self._git("merge-base", f"origin/{base_branch}", "HEAD")
            if common_ancestor != base_tip:
                raise CheckpointError(
                    "The issue branch is stale; update it from the protected base first."
                )

        prs = self._open_prs(branch)
        if len(prs) > 1:
            raise CheckpointError("More than one pull request exists for this task branch.")
        if prs:
            pr = prs[0]
            if pr.get("baseRefName") != base_branch or pr.get("headRefName") != branch:
                raise CheckpointError("The existing pull request targets an unexpected branch.")
            if not re.search(
                rf"\b(?:closes|fixes|resolves)\s+#{issue_number}\b",
                pr.get("body") or "",
                re.IGNORECASE,
            ):
                raise CheckpointError("The existing pull request is not linked to this issue.")
            digest_marker = f"<!-- hos-issue-spec-sha256:{spec_digest} -->"
            if digest_marker not in (pr.get("body") or ""):
                raise CheckpointError("The issue scope changed after this PR was created.")
            if pr.get("state") == "MERGED":
                self._set_pr_state(int(pr["number"]), str(pr.get("body") or ""), "merged")
                return PublishResult("merged", issue_number, branch, pr["number"], pr["url"])
            if issue.get("state") != "OPEN":
                raise CheckpointError(
                    "The linked GitHub issue must remain open until its PR merges."
                )
            if pr.get("state") != "OPEN" or pr.get("isDraft") is True:
                raise CheckpointError("The existing pull request is closed or draft.")
            dirty = self._dirty_paths()
            selected = sorted({self._safe_path(path) for path in include_paths})
            if dirty:
                if not selected:
                    raise CheckpointError("List every checkpoint path explicitly with --include.")
                if dirty != set(selected):
                    raise CheckpointError(
                        "Dirty paths must exactly match the explicit checkpoint path list."
                    )
                if "checkpoints/CURRENT.md" not in selected:
                    raise CheckpointError(
                        "Every checkpoint update must update checkpoints/CURRENT.md."
                    )
                if dry_run:
                    self._git("diff", "--check", "--", *selected)
                    return PublishResult(
                        "would_update_pr", issue_number, branch, pr["number"], pr["url"], True
                    )
                self._stage_checkpoint(issue_number, issue, spec_digest, selected)
                self._git("push", "--set-upstream", "origin", branch)
                prs = self._open_prs(branch)
                if len(prs) != 1:
                    raise CheckpointError("The updated task branch has an ambiguous pull request.")
                pr = prs[0]
                if (
                    pr.get("state") != "OPEN"
                    or pr.get("baseRefName") != base_branch
                    or pr.get("headRefName") != branch
                    or not re.search(
                        rf"\b(?:closes|fixes|resolves)\s+#{issue_number}\b",
                        pr.get("body") or "",
                        re.IGNORECASE,
                    )
                    or f"<!-- hos-issue-spec-sha256:{spec_digest} -->" not in (pr.get("body") or "")
                ):
                    raise CheckpointError(
                        "The updated pull request no longer matches the issue scope."
                    )
            elif selected:
                raise CheckpointError(
                    "The explicit checkpoint path list has no corresponding changes."
                )
            check_state = self._check_results(int(pr["number"]))
            if check_state == "checks_failed":
                self._set_pr_state(int(pr["number"]), str(pr.get("body") or ""), "checks_failed")
                return PublishResult("checks_failed", issue_number, branch, pr["number"], pr["url"])
            if dry_run:
                return PublishResult(
                    "would_enable_auto_merge", issue_number, branch, pr["number"], pr["url"], True
                )
            self._ensure_auto_merge_available(slug)
            self._set_pr_state(int(pr["number"]), str(pr.get("body") or ""), "pending_ci_merge")
            self._gh("pr", "merge", str(pr["number"]), "--auto", "--squash")
            state = "merged" if self._merged(int(pr["number"])) else "pending_ci_merge"
            if state == "merged":
                self._set_pr_state(int(pr["number"]), str(pr.get("body") or ""), state)
            return PublishResult(state, issue_number, branch, pr["number"], pr["url"])

        if issue.get("state") != "OPEN":
            raise CheckpointError("The linked GitHub issue must be open before publication.")

        selected = sorted({self._safe_path(path) for path in include_paths})
        dirty = self._dirty_paths()
        if dirty:
            if not selected:
                raise CheckpointError("List every checkpoint path explicitly with --include.")
            if dirty != set(selected):
                raise CheckpointError(
                    "Dirty paths must exactly match the explicit checkpoint path list."
                )
            if "checkpoints/CURRENT.md" not in selected:
                raise CheckpointError("Every checkpoint commit must update checkpoints/CURRENT.md.")
            if dry_run:
                self._git("diff", "--check", "--", *selected)
                return PublishResult("would_publish", issue_number, branch, dry_run=True)
            self._stage_checkpoint(issue_number, issue, spec_digest, selected)
        else:
            if selected:
                raise CheckpointError(
                    "The explicit checkpoint path list has no corresponding changes."
                )
            message = self._git("log", "-1", "--format=%B")
            if not re.search(
                rf"^checkpoint: issue #{issue_number}\b", message, re.IGNORECASE | re.MULTILINE
            ):
                raise CheckpointError(
                    "No publisher-created checkpoint commit is available to resume."
                )
            if f"Issue-Spec-SHA256: {spec_digest}" not in message:
                raise CheckpointError(
                    "The issue scope changed after this checkpoint commit was created."
                )

        # The issue branch must contain at least one checkpoint commit beyond the base.
        ahead = self._git("rev-list", "--count", f"origin/{base_branch}..HEAD")
        if not ahead.isdigit() or int(ahead) < 1:
            raise CheckpointError("The issue branch has no checkpoint commit.")
        changed_since_base = {
            item
            for item in self._git(
                "diff", "--name-only", f"origin/{base_branch}...HEAD", "-z"
            ).split("\0")
            if item
        }
        if "checkpoints/CURRENT.md" not in changed_since_base:
            raise CheckpointError(
                "The branch must contain a checkpoint update relative to the base."
            )

        if dry_run:
            return PublishResult("would_publish", issue_number, branch, dry_run=True)
        self._git("push", "--set-upstream", "origin", branch)
        current_prs = self._open_prs(branch)
        if not current_prs:
            body = (
                f"Closes #{issue_number}\n\n"
                f"<!-- hos-issue-spec-sha256:{spec_digest} -->\n\n"
                "**Checkpoint state:** `pending_ci_merge`\n"
                "<!-- hos-checkpoint-state:pending_ci_merge -->\n\n"
                "## Checkpoint evidence\n\n"
                "See `checkpoints/CURRENT.md` for the verified result and exact next action.\n\n"
                "## Verification\n\n"
                "The required repository checks must pass before GitHub auto-merges "
                "this checkpoint.\n"
            )
            pr_body = body
            created = self._gh(
                "pr",
                "create",
                "--base",
                base_branch,
                "--head",
                branch,
                "--title",
                f"Checkpoint: issue #{issue_number} — {issue['title']}",
                "--body",
                body,
            )
            url_match = re.search(r"https://github\.com/[^\s]+/pull/(\d+)", created)
            if not url_match:
                raise CheckpointError("GitHub created a pull request but returned no usable URL.")
            pr_number = int(url_match.group(1))
            pr_url = url_match.group(0)
        else:
            if len(current_prs) != 1:
                raise CheckpointError("The task branch has an ambiguous pull request state.")
            concurrent_pr = current_prs[0]
            if (
                concurrent_pr.get("state") != "OPEN"
                or concurrent_pr.get("baseRefName") != base_branch
                or concurrent_pr.get("headRefName") != branch
                or f"<!-- hos-issue-spec-sha256:{spec_digest} -->"
                not in str(concurrent_pr.get("body") or "")
            ):
                raise CheckpointError("A concurrent pull request has a conflicting scope or state.")
            pr_number = int(concurrent_pr["number"])
            pr_url = str(concurrent_pr["url"])
            pr_body = str(concurrent_pr.get("body") or "")

        check_state = self._check_results(pr_number)
        if check_state == "checks_failed":
            self._set_pr_state(pr_number, pr_body, "checks_failed")
            return PublishResult("checks_failed", issue_number, branch, pr_number, pr_url)
        self._ensure_auto_merge_available(slug)
        self._set_pr_state(pr_number, pr_body, "pending_ci_merge")
        self._gh("pr", "merge", str(pr_number), "--auto", "--squash")
        state = "merged" if self._merged(pr_number) else "pending_ci_merge"
        if state == "merged":
            self._set_pr_state(pr_number, pr_body, state)
        return PublishResult(state, issue_number, branch, pr_number, pr_url)

    def reconcile(
        self,
        pull_request: int,
        worktree_path: Path,
        base_branch: str = DEFAULT_BASE_BRANCH,
    ) -> ReconcileResult:
        pr = self._gh_json(
            "pr",
            "view",
            str(pull_request),
            "--json",
            "state,mergedAt,baseRefName,headRefName,body,mergeCommit",
        )
        if pr.get("state") != "MERGED" or not pr.get("mergedAt"):
            raise CheckpointError("Local closeout is allowed only after GitHub confirms the merge.")
        if pr.get("baseRefName") != base_branch:
            raise CheckpointError("The merged pull request targeted an unexpected base branch.")
        issue_match = re.search(
            r"(?:closes|fixes|resolves)\s+#(\d+)", pr.get("body") or "", re.IGNORECASE
        )
        if not issue_match:
            raise CheckpointError("The merged pull request is not linked to a GitHub issue.")

        common_dir = Path(self._git("rev-parse", "--path-format=absolute", "--git-common-dir"))
        canonical = common_dir.parent.resolve()
        requested = worktree_path.resolve()
        root = self.worktree_root
        if requested == canonical or root not in requested.parents:
            raise CheckpointError(
                "The requested cleanup path is outside the approved D: worktree root."
            )
        if self.enforce_d_drive and requested.drive.casefold() != "d:":
            raise CheckpointError("HOS temporary worktrees must reside on D:.")

        canonical_dirty = self._git("status", "--porcelain", "--untracked-files=all", cwd=canonical)
        if canonical_dirty:
            self._set_pr_state(
                pull_request, str(pr.get("body") or ""), "merged_cleanup_blocked_dirty_canonical"
            )
            return ReconcileResult(
                "merged_cleanup_blocked_dirty_canonical",
                pull_request,
                str(canonical),
                str(requested),
            )

        current_branch = self._git("branch", "--show-current", cwd=canonical)
        if current_branch != base_branch:
            raise CheckpointError("The canonical checkout is not on the protected base branch.")

        worktrees = self._git("worktree", "list", "--porcelain", cwd=canonical)
        registered = _parse_worktrees(worktrees)
        entry = next((row for row in registered if Path(row["path"]).resolve() == requested), None)
        branch_name = str(pr.get("headRefName") or "")
        matching_branch = [
            row
            for row in registered
            if row.get("branch", "").removeprefix("refs/heads/") == branch_name
        ]
        if requested.exists():
            if entry is None:
                raise CheckpointError("The requested path is not a registered repository worktree.")
            if entry.get("branch", "").removeprefix("refs/heads/") != branch_name:
                raise CheckpointError(
                    "The requested worktree does not belong to the merged pull request branch."
                )
            if self._git("status", "--porcelain", "--untracked-files=all", cwd=requested):
                self._set_pr_state(
                    pull_request,
                    str(pr.get("body") or ""),
                    "merged_cleanup_blocked_dirty_worktree",
                )
                return ReconcileResult(
                    "merged_cleanup_blocked_dirty_worktree",
                    pull_request,
                    str(canonical),
                    str(requested),
                )
        elif entry is not None:
            self._set_pr_state(
                pull_request,
                str(pr.get("body") or ""),
                "merged_cleanup_blocked_stale_registration",
            )
            return ReconcileResult(
                "merged_cleanup_blocked_stale_registration",
                pull_request,
                str(canonical),
                str(requested),
            )
        elif matching_branch:
            raise CheckpointError("The merged branch is registered at a different worktree path.")

        self._git("fetch", "origin", base_branch, cwd=canonical)
        self._git("merge", "--ff-only", f"origin/{base_branch}", cwd=canonical)
        merge_commit = (pr.get("mergeCommit") or {}).get("oid")
        if not isinstance(merge_commit, str) or not merge_commit:
            raise CheckpointError(
                "GitHub did not provide the merge commit needed for reconciliation."
            )
        if self._git("merge-base", merge_commit, "HEAD", cwd=canonical) != merge_commit:
            raise CheckpointError("The confirmed merge is not present in the canonical checkout.")

        if not requested.exists():
            self._set_pr_state(pull_request, str(pr.get("body") or ""), "complete")
            return ReconcileResult("complete", pull_request, str(canonical), str(requested))
        self._set_pr_state(pull_request, str(pr.get("body") or ""), "merged_cleanup_pending")
        self._git("worktree", "remove", str(requested), cwd=canonical)
        self._set_pr_state(pull_request, str(pr.get("body") or ""), "complete")
        return ReconcileResult("complete", pull_request, str(canonical), str(requested))


def _parse_worktrees(value: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for block in value.strip().split("\n\n"):
        row: dict[str, str] = {}
        for line in block.splitlines():
            key, _, item = line.partition(" ")
            row["path" if key == "worktree" else key] = item
        if row:
            rows.append(row)
    return rows


def find_repository_root(start: Path) -> Path:
    runner = SubprocessRunner()
    result = runner.run(("git", "-C", str(start.resolve()), "rev-parse", "--show-toplevel"))
    return Path(result).resolve()


__all__ = [
    "CheckpointError",
    "CheckpointPublisher",
    "DEFAULT_BASE_BRANCH",
    "DEFAULT_WORKTREE_ROOT",
    "PublishResult",
    "REQUIRED_CHECKS",
    "ReconcileResult",
    "find_repository_root",
]
