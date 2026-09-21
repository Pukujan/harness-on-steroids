"""Managed library facade. Import paths under src.* stay until issue 18 moves them."""

from src.goal_loop import GoalEngine
from src.owner_invariants import all_failures, load_spec
from src.score_session import score_seq

__all__ = ["GoalEngine", "all_failures", "load_spec", "score_seq"]
