"""Checked mathematical starting point for Manufacturing Genius."""

from .duel import (
    Equilibrium,
    StrategyEvaluation,
    duel_payoff_matrix,
    evaluate_strategies,
    joint_shocks,
    zero_sum_equilibrium,
)

__all__ = [
    "Equilibrium",
    "StrategyEvaluation",
    "duel_payoff_matrix",
    "evaluate_strategies",
    "joint_shocks",
    "zero_sum_equilibrium",
]
