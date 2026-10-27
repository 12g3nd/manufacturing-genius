"""Exact two-action contest; standard library only.

Action order is always (safe, risky). Matrix entries are A's expected prize
share: 1 for a win, 0 for a loss, and 1/2 for a tie. B receives 1 minus A's
share, so the constant-sum contest has the same strategies as a zero-sum game.
This module contains no model of latent talent and no empirical estimates.
"""

from dataclasses import dataclass
from math import fsum, isfinite
from numbers import Real
from typing import Sequence

PayoffMatrix = tuple[tuple[float, float], tuple[float, float]]
ShockDistribution = tuple[tuple[int, int, float], ...]


@dataclass(frozen=True)
class StrategyEvaluation:
    """Expected payoff and gains from the best unilateral deviations."""

    value: float
    row_deviation_gain: float
    column_deviation_gain: float
    exploitability: float
    max_deviation_gain: float


@dataclass(frozen=True)
class Equilibrium:
    """One verified equilibrium, which need not be unique in degenerate games.

    Probabilities refer to action index 1 (risky in the duel). Exploitability
    is the sum of the two best-response gains, also called the saddle gap.
    max_deviation_gain is the larger of those gains. All are in payoff units.
    """

    row_risky_probability: float
    column_risky_probability: float
    value: float
    row_deviation_gain: float
    column_deviation_gain: float
    exploitability: float
    max_deviation_gain: float


def _finite_real(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite real number, not {value!r}")
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite real number") from exc
    if not isfinite(result):
        raise ValueError(f"{name} must be a finite real number")
    return result


def _probability(value: Real, name: str) -> float:
    result = _finite_real(value, name)
    if not 0.0 <= result <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")
    return result


def _matrix(values: Sequence[Sequence[Real]]) -> PayoffMatrix:
    try:
        if len(values) != 2 or any(len(row) != 2 for row in values):
            raise ValueError("payoffs must be a 2 by 2 matrix")
        return (
            (_finite_real(values[0][0], "payoff"), _finite_real(values[0][1], "payoff")),
            (_finite_real(values[1][0], "payoff"), _finite_real(values[1][1], "payoff")),
        )
    except TypeError as exc:
        raise ValueError("payoffs must be a 2 by 2 matrix") from exc


def joint_shocks(correlation: Real = 1.0) -> ShockDistribution:
    """Return (A sign, B sign, probability) for two fair +/-1 shocks.

    Their Pearson correlation is exactly rho. At rho=1, risky positions move
    together; at rho=0 their shocks are independent; at rho=-1 they oppose.
    """
    rho = _finite_real(correlation, "correlation")
    if not -1.0 <= rho <= 1.0:
        raise ValueError("correlation must lie in [-1, 1]")
    same, opposite = (1.0 + rho) / 4.0, (1.0 - rho) / 4.0
    return ((1, 1, same), (1, -1, opposite), (-1, 1, opposite), (-1, -1, same))


def duel_payoff_matrix(
    initial_gap: Real = 5.0,
    shock_size: Real = 10.0,
    correlation: Real = 1.0,
) -> PayoffMatrix:
    """Enumerate the four shock outcomes for every action pair.

    initial_gap is A's starting score minus B's. Positive means A leads;
    negative means B leads. Safe adds zero; risky adds +/-shock_size. Both
    actions have zero expected increment. Absolute starting scores do not
    affect the contest, only their difference. Choices are simultaneous.
    """
    gap = _finite_real(initial_gap, "initial_gap")
    magnitude = _finite_real(shock_size, "shock_size")
    if magnitude < 0.0:
        raise ValueError("shock_size must be nonnegative")
    shocks = joint_shocks(correlation)
    rows = []
    for action_a in (0, 1):
        row = []
        for action_b in (0, 1):
            terms = []
            for sign_a, sign_b, probability in shocks:
                if probability == 0.0:
                    continue
                difference = gap + magnitude * (action_a * sign_a - action_b * sign_b)
                if not isfinite(difference):
                    raise ValueError("score difference overflowed; use smaller score units")
                prize_share = 1.0 if difference > 0 else 0.0 if difference < 0 else 0.5
                terms.append(probability * prize_share)
            row.append(fsum(terms))
        rows.append(tuple(row))
    return (rows[0], rows[1])


def evaluate_strategies(
    payoffs: Sequence[Sequence[Real]],
    row_risky_probability: Real,
    column_risky_probability: Real,
) -> StrategyEvaluation:
    """Evaluate independent mixed strategies and the best unilateral deviations.

    The row player maximizes the supplied payoff; the column player minimizes
    it. A mixed deviation cannot beat the best pure deviation in this game.
    """
    matrix = _matrix(payoffs)
    p = _probability(row_risky_probability, "row_risky_probability")
    q = _probability(column_risky_probability, "column_risky_probability")
    scale = max(1.0, *(abs(x) for row in matrix for x in row))
    a, b = (x / scale for x in matrix[0])
    c, d = (x / scale for x in matrix[1])
    row_values = (fsum(((1 - q) * a, q * b)), fsum(((1 - q) * c, q * d)))
    column_values = (fsum(((1 - p) * a, p * c)), fsum(((1 - p) * b, p * d)))
    value = fsum(((1 - p) * row_values[0], p * row_values[1]))
    row_gain = max(0.0, max(row_values) - value) * scale
    column_gain = max(0.0, value - min(column_values)) * scale
    return StrategyEvaluation(
        value=value * scale,
        row_deviation_gain=row_gain,
        column_deviation_gain=column_gain,
        exploitability=row_gain + column_gain,
        max_deviation_gain=max(row_gain, column_gain),
    )


def zero_sum_equilibrium(
    payoffs: Sequence[Sequence[Real]], *, tolerance: Real = 1e-12
) -> Equilibrium:
    """Find one equilibrium of a finite two-by-two zero-sum game.

    First check pure saddle points, then use indifference equations for an
    interior mixed equilibrium. Finally check both unilateral deviation gains.
    tolerance is relative to max(1, largest absolute payoff). This routine is
    specifically for a zero-sum/constant-sum game, not a general-sum game.
    """
    matrix = _matrix(payoffs)
    tol = _finite_real(tolerance, "tolerance")
    if tol <= 0.0 or tol > 1e-6:
        raise ValueError("tolerance must be positive and no larger than 1e-6")
    scale = max(1.0, *(abs(x) for row in matrix for x in row))
    normalized = tuple(tuple(x / scale for x in row) for row in matrix)
    chosen = None
    for row in (0, 1):
        for column in (0, 1):
            value = normalized[row][column]
            if (
                value >= max(normalized[0][column], normalized[1][column]) - tol
                and value <= min(normalized[row]) + tol
            ):
                chosen = (float(row), float(column))
                break
        if chosen is not None:
            break
    if chosen is None:
        a, b = normalized[0]
        c, d = normalized[1]
        denominator = fsum((a, -b, -c, d))
        if abs(denominator) <= tol:
            raise ArithmeticError("no stable mixed solution; inspect payoff scale")
        p, q = (a - b) / denominator, (a - c) / denominator
        if not -tol <= p <= 1.0 + tol or not -tol <= q <= 1.0 + tol:
            raise ArithmeticError("computed strategy is outside the probability simplex")
        chosen = (min(1.0, max(0.0, p)), min(1.0, max(0.0, q)))
    evaluation = evaluate_strategies(matrix, *chosen)
    if evaluation.max_deviation_gain > 4.0 * tol * scale:
        raise ArithmeticError("candidate failed the unilateral-deviation check")
    return Equilibrium(
        row_risky_probability=chosen[0],
        column_risky_probability=chosen[1],
        value=evaluation.value,
        row_deviation_gain=evaluation.row_deviation_gain,
        column_deviation_gain=evaluation.column_deviation_gain,
        exploitability=evaluation.exploitability,
        max_deviation_gain=evaluation.max_deviation_gain,
    )
