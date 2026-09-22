"""Deterministic repository context feeding for Jev and matched baselines.

The feeder has no model or tool authority. It collects bounded, privacy-safe
facts from an isolated workspace and updates a ``DecisionContext`` that may be
given to either a plain harness or Jev. Keeping this component shared is what
makes the long-horizon A/B comparison an intervention on Jev rather than an
uncontrolled comparison of context quality.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from .core import ControllerAction, ControllerPhase, DecisionBead, DecisionContext

_PATH_RE = re.compile(
    r"(?<![\w.-])(?:[\w.-]+[\\/])*[\w.-]+\.(?:py|pyi|ts|tsx|js|jsx|json|md|toml|yaml|yml|txt)"
)
_INSTRUCTION_NAMES = {
    "AGENTS.md",
    "PLAN.md",
    "README.md",
    "pyproject.toml",
    "package.json",
    "CONTRIBUTING.md",
}
_SKIP_PARTS = {
    ".git",
    ".controller-runs",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "node_modules",
    "data",
    ".kilo",
    ".opencode",
}

_FEEDER_ACTIONS: dict[ControllerPhase, tuple[ControllerAction, ...]] = {
    ControllerPhase.INTAKE: (
        ControllerAction.INSPECT_REPO,
        ControllerAction.INSPECT_TASK_STATE,
        ControllerAction.READ_DOCS,
        ControllerAction.SEARCH_LOCAL,
        ControllerAction.BUILD_CONTEXT_PACK,
        ControllerAction.ASK_USER,
        ControllerAction.ESCALATE,
    ),
    ControllerPhase.OBSERVE: (
        ControllerAction.INSPECT_REPO,
        ControllerAction.INSPECT_TASK_STATE,
        ControllerAction.READ_SOURCE,
        ControllerAction.READ_DOCS,
        ControllerAction.SEARCH_LOCAL,
        ControllerAction.DECOMPOSE,
        ControllerAction.BUILD_CONTEXT_PACK,
        ControllerAction.ASK_USER,
        ControllerAction.ESCALATE,
    ),
    ControllerPhase.UNDERSTAND: (
        ControllerAction.READ_SOURCE,
        ControllerAction.READ_DOCS,
        ControllerAction.SEARCH_LOCAL,
        ControllerAction.DECOMPOSE,
        ControllerAction.CREATE_BEAD,
        ControllerAction.BUILD_CONTEXT_PACK,
        ControllerAction.ASK_USER,
        ControllerAction.ESCALATE,
    ),
    ControllerPhase.PLAN: (
        ControllerAction.CREATE_BEAD,
        ControllerAction.UPDATE_BEAD,
        ControllerAction.DECOMPOSE,
        ControllerAction.APPLY_PATCH,
        ControllerAction.WRITE_FILE,
        ControllerAction.ASK_USER,
        ControllerAction.ESCALATE,
    ),
    ControllerPhase.EXECUTE: (
        ControllerAction.APPLY_PATCH,
        ControllerAction.WRITE_FILE,
        ControllerAction.CHECK_STATUS,
        ControllerAction.RUN_TARGETED_TESTS,
        ControllerAction.CHECK_GIT_DIFF,
        ControllerAction.ASK_USER,
        ControllerAction.ESCALATE,
    ),
    ControllerPhase.VERIFY: (
        ControllerAction.RUN_TARGETED_TESTS,
        ControllerAction.RUN_BROAD_TESTS,
        ControllerAction.RUN_CONTRACT_CHECK,
        ControllerAction.CHECK_GIT_DIFF,
        ControllerAction.CHECK_STATUS,
        ControllerAction.REVIEW_RESULT,
        ControllerAction.FINALIZE,
        ControllerAction.ASK_USER,
        ControllerAction.ESCALATE,
    ),
    ControllerPhase.RECOVER: (
        ControllerAction.INSPECT_REPO,
        ControllerAction.INSPECT_TASK_STATE,
        ControllerAction.CHECK_STATUS,
        ControllerAction.RETRY_TRANSIENT_FAILURE,
        ControllerAction.RECOVER_AFTER_FAILURE,
        ControllerAction.ASK_USER,
        ControllerAction.ESCALATE,
    ),
    ControllerPhase.DELEGATE: (
        ControllerAction.DELEGATE_TO_SOL,
        ControllerAction.DELEGATE_TO_SPECIALIST,
        ControllerAction.WAIT_FOR_WORK,
        ControllerAction.RESUME_WORK,
        ControllerAction.CHECK_STATUS,
        ControllerAction.ASK_USER,
        ControllerAction.ESCALATE,
    ),
    ControllerPhase.COMMUNICATE: (
        ControllerAction.UPDATE_USER,
        ControllerAction.FINALIZE,
        ControllerAction.ASK_USER,
        ControllerAction.ESCALATE,
    ),
    ControllerPhase.COMPLETE: (ControllerAction.FINALIZE, ControllerAction.UPDATE_USER),
}


@dataclass(frozen=True)
class FeederSnapshot:
    """The bounded facts collected at one context boundary."""

    facts: tuple[str, ...]
    changed_paths: tuple[str, ...]
    relevant_paths: tuple[str, ...]
    candidate_beads: tuple[DecisionBead, ...]
    digest: str
    git_available: bool


def _unique(values: Iterable[str]) -> tuple[str, ...]:
    result: list[str] = []
    for value in values:
        cleaned = str(value).strip()
        if cleaned and cleaned not in result:
            result.append(cleaned)
    return tuple(result)


def _run_text(command: Sequence[str], workdir: Path, timeout: float) -> tuple[str, bool]:
    try:
        completed = subprocess.run(
            list(command),
            cwd=workdir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "", False
    return completed.stdout.strip(), completed.returncode == 0


def _safe_relative(path: Path, root: Path) -> str | None:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return None
    if any(part in _SKIP_PARTS for part in relative.parts):
        return None
    return relative.as_posix()


def _workspace_files(workdir: Path, limit: int = 400) -> tuple[str, ...]:
    paths: list[str] = []
    if not workdir.is_dir():
        return ()
    for path in sorted(workdir.rglob("*")):
        if not path.is_file():
            continue
        relative = _safe_relative(path, workdir)
        if relative is not None:
            paths.append(relative)
        if len(paths) >= limit:
            break
    return tuple(paths)


def _changed_paths(status: str) -> tuple[str, ...]:
    paths: list[str] = []
    for line in status.splitlines():
        value = line.strip()
        if not value:
            continue
        if len(value) > 3 and value[2] == " ":
            value = value[3:]
        elif len(value) > 2:
            value = value[2:]
        paths.append(value.replace("\\", "/"))
    return _unique(paths)


def _candidate_beads(relevant_paths: Sequence[str]) -> tuple[DecisionBead, ...]:
    detail = ", ".join(relevant_paths[:6]) or "the isolated repository workspace"
    return (
        DecisionBead(
            "inspect-context",
            f"Inspect the owner request and relevant workspace files ({detail}).",
            acceptance_criteria=("relevant facts and files are identified",),
        ),
        DecisionBead(
            "plan-change",
            "Decompose the request into one bounded implementation or research step.",
            dependencies=("inspect-context",),
            acceptance_criteria=("the next bounded change has an acceptance check",),
        ),
        DecisionBead(
            "execute-change",
            "Apply the approved bounded change in the isolated workspace.",
            dependencies=("plan-change",),
            acceptance_criteria=("the requested change is observable in the workspace",),
        ),
        DecisionBead(
            "verify-result",
            "Run the smallest relevant verification and review the resulting state.",
            dependencies=("execute-change",),
            acceptance_criteria=("verification evidence is recorded",),
        ),
    )


def _safe_excerpt(path: Path, root: Path) -> str | None:
    relative = _safe_relative(path, root)
    if relative is None or path.stat().st_size > 8_000:
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    lines: list[str] = []
    for line in text.splitlines():
        value = re.sub(
            r"(?:api[_-]?key|token|secret|password)\s*[:=].*",
            "[redacted]",
            line,
            flags=re.I,
        )
        value = value.strip()
        if value:
            lines.append(value[:240])
        if len(lines) >= 3:
            break
    if not lines:
        return None
    return f"excerpt:{relative}:" + " | ".join(lines)


class RepositoryContextFeeder:
    """Collect and fold current workspace facts into a decision context."""

    def __init__(self, *, command_timeout: float = 3.0, max_facts: int = 80) -> None:
        self.command_timeout = command_timeout
        self.max_facts = max_facts

    def collect(self, workdir: Path, user_turn: str = "") -> FeederSnapshot:
        files = _workspace_files(workdir)
        instruction_files = tuple(
            path for path in files if Path(path).name in _INSTRUCTION_NAMES
        )
        explicit_paths = [match.replace("\\", "/") for match in _PATH_RE.findall(user_turn)]
        relevant_paths = _unique(path for path in explicit_paths if path in files)
        if not relevant_paths:
            relevant_paths = instruction_files[:8] or files[:8]

        status, status_ok = _run_text(
            ("git", "status", "--short", "--untracked-files=all"), workdir, self.command_timeout
        )
        branch, branch_ok = _run_text(
            ("git", "branch", "--show-current"), workdir, self.command_timeout
        )
        diff_paths, diff_ok = _run_text(
            ("git", "diff", "--name-only"), workdir, self.command_timeout
        )
        changed_paths = _unique((*_changed_paths(status), *diff_paths.splitlines()))
        facts = [
            f"workspace_files:{len(files)}",
            f"instruction_files:{','.join(instruction_files[:8]) or 'none'}",
            f"relevant_paths:{','.join(relevant_paths[:8]) or 'none'}",
            f"git_available:{status_ok and branch_ok}",
            f"git_branch:{branch or 'unavailable'}",
            f"git_status:{'clean' if status_ok and not status else 'changed_or_unavailable'}",
            f"changed_paths_count:{len(changed_paths)}",
            f"git_diff_available:{diff_ok}",
        ]
        for path in relevant_paths[:8]:
            facts.append(f"relevant_file:{path}")
            excerpt = _safe_excerpt(workdir / path, workdir)
            if excerpt:
                facts.append(excerpt)
        digest = hashlib.sha256(
            "\n".join((*facts, *changed_paths)).encode("utf-8", errors="replace")
        ).hexdigest()[:16]
        facts.append(f"context_pack_digest:{digest}")
        return FeederSnapshot(
            facts=_unique(facts)[: self.max_facts],
            changed_paths=changed_paths,
            relevant_paths=relevant_paths,
            candidate_beads=_candidate_beads(relevant_paths),
            digest=digest,
            git_available=status_ok and branch_ok,
        )

    def update(
        self,
        context: DecisionContext,
        workdir: Path,
        *,
        user_turn: str | None = None,
        prior_turns: Sequence[str] = (),
        turn_index: int | None = None,
    ) -> FeederSnapshot:
        if user_turn:
            context.add_conversation(user_turn)
        for turn in prior_turns:
            if turn and turn not in context.relevant_conversation:
                context.add_conversation(turn)
        if turn_index is not None:
            context.turn_index = turn_index
        if context.phase in {ControllerPhase.COMPLETE, ControllerPhase.COMMUNICATE}:
            context.set_phase(ControllerPhase.INTAKE)
        snapshot = self.collect(workdir, context.current_user_turn)
        context.repo_facts = _unique((*context.repo_facts, *snapshot.facts))[-self.max_facts :]
        context.changed_paths = _unique((*context.changed_paths, *snapshot.changed_paths))
        if not context.candidate_beads:
            context.candidate_beads = snapshot.candidate_beads
            context.open_beads = snapshot.candidate_beads
        context.allowed_actions = tuple(
            action.value for action in _FEEDER_ACTIONS[context.phase]
        )
        context.add_evidence(f"context_pack:{snapshot.digest}")
        return snapshot


__all__ = ["FeederSnapshot", "RepositoryContextFeeder"]
