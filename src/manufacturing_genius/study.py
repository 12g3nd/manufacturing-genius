"""Design 1.0: persistent ability, exact state games and paired simulations.

All observations are synthetic score points. Selection never reads fresh data.
"""
from dataclasses import asdict
from math import erf, sqrt

import numpy as np

from .duel import duel_payoff_matrix, zero_sum_equilibrium

POLICIES = ("equilibrium", "safe", "risky")
STREAMS = {"labels": 1, "first_round": 2, "potential_risk": 3,
           "actions": 4, "ties": 5, "fresh_evaluation": 6}


def exact_accuracy(delta, risk_size, correlation, sigma_0=1.0):
    """Integrate the piecewise win probabilities over the effective normal gap."""
    if delta == 0:
        return {p: None for p in POLICIES}
    if delta < 0 or risk_size < 0 or sigma_0 < 0 or not -1 <= correlation <= 1:
        raise ValueError("invalid study parameters")
    if sigma_0 == 0:
        m = duel_payoff_matrix(2 * delta, risk_size, correlation)
        return {"equilibrium": zero_sum_equilibrium(m).value,
                "safe": m[0][0], "risky": m[1][1]}
    def cdf(x):
        return (1 + erf((x - 2 * delta) / (2 * sigma_0))) / 2
    safe = 1 - cdf(0)
    def integrated(threshold, v):
        return (1 - cdf(threshold) + v * (cdf(threshold) - cdf(0))
                + (1 - v) * (cdf(0) - cdf(-threshold)))
    return {"safe": safe,
            "equilibrium": integrated(risk_size, (2 + correlation) / (3 + correlation)),
            "risky": integrated(2 * risk_size, (3 + correlation) / 4)}


def state_strategies(gaps, risk_size, correlation):
    """Solve every distinct encountered payoff matrix, including exact ties.

    The four-outcome payoff matrix is constant between five thresholds. Cache
    those finite states, using the original enumerator and original solver.
    """
    gaps = np.asarray(gaps, dtype=float)
    if risk_size < 0 or not np.isfinite(gaps).all():
        raise ValueError("invalid state")
    if risk_size == 0:
        ids = np.sign(gaps).astype(int) + 1
        representatives = [-1, 0, 1]
    else:
        thresholds = risk_size * np.array([-2, -1, 0, 1, 2])
        ids = (np.searchsorted(thresholds, gaps, side="left")
               + np.searchsorted(thresholds, gaps, side="right"))
        representatives = risk_size * np.array([-3, -2, -1.5, -1, -.5, 0, .5, 1, 1.5, 2, 3])
    p, q, value = (np.empty_like(gaps) for _ in range(3))
    audit = []
    for state in np.unique(ids):
        gap = float(representatives[state])
        matrix = duel_payoff_matrix(gap, risk_size, correlation)
        eq = zero_sum_equilibrium(matrix)
        mask = ids == state
        p[mask], q[mask], value[mask] = eq.row_risky_probability, eq.column_risky_probability, eq.value
        audit.append({"representative_gap": gap, "matrix": matrix, **asdict(eq)})
    return p, q, value, audit


def select_winners(final_scores, tie_uniform):
    """An actual selected person (0=A, 1=B); exact score ties use fair draws."""
    d = final_scores[:, 0] - final_scores[:, 1]
    return np.where(d > 0, 0, np.where(d < 0, 1, (tie_uniform >= .5).astype(int)))


def simulate_cell(delta, risk_size, correlation, *, n, seed, scenario=0,
                  sigma_0=1.0, sigma_H=1.0, fresh_seed=None):
    """Common random numbers across policies, independent streams by role/cell.

    fresh_seed is a test hook: changing it must never change selected winners.
    """
    def rng(role):
        master = fresh_seed if role == "fresh_evaluation" and fresh_seed is not None else seed
        return np.random.Generator(np.random.PCG64(np.random.SeedSequence([master, scenario, STREAMS[role]])))
    sign = np.where(rng("labels").random(n) < .5, 1, -1)
    theta = np.column_stack((sign, -sign)) * delta / 2
    initial_noise = rng("first_round").standard_normal((n, 2))
    first = theta + sigma_0 * initial_noise
    gaps = first[:, 0] - first[:, 1] + theta[:, 0] - theta[:, 1]
    p, q, value, audit = state_strategies(gaps, risk_size, correlation)
    risk_draws = rng("potential_risk").random((n, 2))
    xa = np.where(risk_draws[:, 0] < .5, 1, -1)
    xb = xa * np.where(risk_draws[:, 1] < (1 + correlation) / 2, 1, -1)
    potential = np.column_stack((xa, xb))
    action_uniforms = rng("actions").random((n, 2))
    strategic_actions = action_uniforms < np.column_stack((p, q))
    tie_uniform = rng("ties").random(n)
    # Separate independent draw, never supplied to select_winners/state_strategies.
    fresh_noise = rng("fresh_evaluation").standard_normal((n, 2))
    fresh = theta + sigma_H * fresh_noise
    outcomes, winners = {}, {}
    rows = np.arange(n)
    for policy, actions in (("equilibrium", strategic_actions), ("safe", 0), ("risky", 1)):
        final = first + theta + risk_size * actions * potential
        chosen = select_winners(final, tie_uniform)
        ability = theta[rows, chosen]
        reported = final[rows, chosen] / 2
        heldout = fresh[rows, chosen]
        winners[policy] = chosen
        outcomes[policy] = {"selected_ability": ability, "reported_score": reported,
                            "overstatement": reported - ability, "fresh": heldout,
                            "fresh_residual": heldout - ability}
        if delta > 0:
            outcomes[policy]["accuracy"] = (ability > 0).astype(float)
    return {"outcomes": outcomes, "winners": winners, "audit": audit,
            "fresh_first_noise_correlation": float(np.corrcoef(initial_noise.ravel(), fresh_noise.ravel())[0, 1]),
            "state_value": value}


def summarize(values, *, binary=False):
    values = np.asarray(values, dtype=float)
    n = len(values)
    mean = float(values.mean())
    se = float(values.std(ddof=1) / sqrt(n))
    low, high = mean - 1.96 * se, mean + 1.96 * se
    if binary:
        z2 = 1.96**2
        center = (mean + z2 / (2 * n)) / (1 + z2 / n)
        radius = 1.96 * sqrt(mean * (1 - mean) / n + z2 / (4 * n*n)) / (1 + z2 / n)
        low, high = center - radius, center + radius
    return {"mean": mean, "mc_se": se, "low": low, "high": high}
