"""Standing /goal loop: Codex CLI + Hermes semantics. No LLM required for the core."""

from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal

Verdict = Literal["done", "continue", "blocked", "wait"]
Status = Literal["active", "paused", "done", "blocked"]

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE = ROOT / "data" / "goal-state.json"
DONE_MARKERS = ("<<goal_loop_complete>>",)
BLOCKED_MARKERS = ("blocked:", "need user input", "unachievable")


@dataclass
class Contract:
    outcome: str = ""
    verification: str = ""
    constraints: str = ""
    boundaries: str = ""
    stop_when: str = ""


@dataclass
class GoalState:
    text: str = ""
    status: Status = "paused"
    turns: int = 0
    max_turns: int = 20
    subgoals: list[str] = field(default_factory=list)
    gates: list[str] = field(default_factory=list)
    contract: dict = field(default_factory=dict)
    last_verdict: str = ""
    last_reason: str = ""

    def active(self) -> bool:
        return self.status == "active" and bool(self.text)


def load_state(path: Path | None = None) -> GoalState:
    p = path or DEFAULT_STATE
    if not p.is_file():
        return GoalState()
    raw = json.loads(p.read_text(encoding="utf-8"))
    return GoalState(**{k: raw[k] for k in GoalState.__dataclass_fields__ if k in raw})


def save_state(state: GoalState, path: Path | None = None) -> None:
    p = path or DEFAULT_STATE
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(asdict(state), indent=2), encoding="utf-8")


def run_gates(gates: list[str], cwd: Path | None = None) -> list[dict]:
    results = []
    for cmd in gates:
        try:
            proc = subprocess.run(
                cmd,
                shell=True,
                cwd=str(cwd or ROOT),
                capture_output=True,
                text=True,
                timeout=60,
            )
            tail = ((proc.stdout or "") + (proc.stderr or ""))[-3000:]
            results.append(
                {"cmd": cmd, "ok": proc.returncode == 0, "code": proc.returncode, "tail": tail}
            )
        except Exception as exc:
            results.append({"cmd": cmd, "ok": False, "code": -1, "tail": type(exc).__name__})
    return results


def rule_judge(
    state: GoalState, last_response: str, gate_results: list[dict]
) -> tuple[Verdict, str]:
    """Conservative rule judge (Hermes: done only with evidence)."""
    if any(not g["ok"] for g in gate_results):
        failed = next(g for g in gate_results if not g["ok"])
        return "continue", f"gate failed: {failed['cmd']}"
    text = (last_response or "").lower()
    if any(m in text for m in BLOCKED_MARKERS):
        return "blocked", "agent reported blocked"
    if state.gates and all(g["ok"] for g in gate_results) and gate_results:
        if any(m in text for m in DONE_MARKERS):
            return "done", "gates passed and explicit completion marker"
        return "continue", "gates passed but response did not confirm done"
    if any(m in text for m in DONE_MARKERS) and not state.gates:
        return "done", "explicit completion marker"
    if any(m in text for m in BLOCKED_MARKERS):
        return "blocked", "blocked marker"
    return "continue", "goal not evidenced as complete"


def gate_first_judge(
    state: GoalState, last_response: str, gate_results: list[dict]
) -> tuple[Verdict, str]:
    """Differential twin: gates dominate; never done if a gate is red."""
    if any(not g["ok"] for g in gate_results):
        return "continue", "red gate"
    return rule_judge(state, last_response, gate_results)


class GoalEngine:
    def __init__(self, path: Path | None = None, judge=rule_judge):
        self.path = path or DEFAULT_STATE
        self.judge = judge
        self.state = load_state(self.path)

    def persist(self) -> None:
        save_state(self.state, self.path)

    def set_goal(self, text: str, max_turns: int = 20, contract: dict | None = None) -> GoalState:
        self.state = GoalState(
            text=text.strip(),
            status="active",
            turns=0,
            max_turns=max_turns,
            contract=contract or {},
        )
        self.persist()
        return self.state

    def add_subgoal(self, text: str) -> GoalState:
        if not self.state.text:
            raise ValueError("no active goal")
        self.state.subgoals.append(text.strip())
        self.persist()
        return self.state

    def add_gate(self, cmd: str) -> GoalState:
        if not self.state.text:
            raise ValueError("no active goal")
        self.state.gates.append(cmd)
        self.persist()
        return self.state

    def pause(self) -> GoalState:
        if self.state.status == "active":
            self.state.status = "paused"
            self.persist()
        return self.state

    def resume(self) -> GoalState:
        if self.state.text:
            self.state.status = "active"
            self.state.turns = 0
            self.persist()
        return self.state

    def clear(self) -> GoalState:
        self.state = GoalState()
        self.persist()
        return self.state

    def tick(self, last_response: str, cwd: Path | None = None) -> dict:
        if self.state.status != "active" or not self.state.text:
            return {
                "verdict": "blocked",
                "reason": "no active goal",
                "continue": False,
                "state": asdict(self.state),
            }
        gates = run_gates(self.state.gates, cwd=cwd)
        try:
            verdict, reason = self.judge(self.state, last_response, gates)
        except Exception:
            verdict, reason = "continue", "judge error fail-open"
        if verdict == "done" and any(not g["ok"] for g in gates):
            verdict, reason = "continue", "cannot be done with red gate"
        self.state.last_verdict = verdict
        self.state.last_reason = reason
        if verdict == "done":
            self.state.status = "done"
        elif verdict == "blocked":
            self.state.status = "blocked"
        else:
            self.state.turns += 1
            if self.state.turns >= self.state.max_turns:
                self.state.status = "paused"
                reason = f"budget {self.state.max_turns} exhausted"
                verdict = "continue"
                self.state.last_reason = reason
        self.persist()
        cont = self.state.status == "active" and verdict == "continue"
        prompt = None
        if cont:
            prompt = (
                f"[Continuing toward your standing goal] {self.state.text}\n"
                f"Reason: {reason}\n"
                f"Turns {self.state.turns}/{self.state.max_turns}."
            )
        return {
            "verdict": verdict,
            "reason": reason,
            "continue": cont,
            "prompt": prompt,
            "gates": gates,
            "state": asdict(self.state),
        }


def continuation_prompt(state: GoalState, reason: str) -> str:
    return f"[Continuing toward your standing goal] {state.text}\nReason: {reason}"
