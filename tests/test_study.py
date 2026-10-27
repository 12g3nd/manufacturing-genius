import math
import unittest

import numpy as np

from manufacturing_genius.duel import duel_payoff_matrix, zero_sum_equilibrium
from manufacturing_genius.study import exact_accuracy, select_winners, simulate_cell, state_strategies


class StudyTests(unittest.TestCase):
    def test_cached_states_match_original_solver_including_boundaries(self):
        for a in (0, .5, 1.5):
            gaps = np.unique(np.r_[np.linspace(-4, 4, 161), a*np.array([-2, -1, 0, 1, 2])])
            for rho in (-1, 0, .5, 1):
                p, q, v, audit = state_strategies(gaps, a, rho)
                for i, gap in enumerate(gaps):
                    eq = zero_sum_equilibrium(duel_payoff_matrix(float(gap), a, rho))
                    self.assertAlmostEqual(p[i], eq.row_risky_probability)
                    self.assertAlmostEqual(q[i], eq.column_risky_probability)
                    self.assertAlmostEqual(v[i], eq.value)
                self.assertLessEqual(max(x["max_deviation_gain"] for x in audit), 1e-12)

    def test_exact_integral_against_independent_midpoint_quadrature(self):
        # Independently integrate actual enumerated game values, not the closed formula.
        for delta in (.25, .75, 1.5):
            for a in (.5, 1.5, 3):
                for rho in (-1, 0, .5, 1):
                    exact = exact_accuracy(delta, a, rho)
                    bounds = sorted(set([-15, -2*a, -a, 0, a, 2*a, 15]))
                    totals = dict.fromkeys(exact, 0.)
                    for lo, hi in zip(bounds, bounds[1:]):
                        mid = (lo+hi)/2
                        m = duel_payoff_matrix(mid, a, rho)
                        vals = {"safe": m[0][0], "risky": m[1][1], "equilibrium": zero_sum_equilibrium(m).value}
                        # Midpoint quadrature of density, exact payoff on each segment.
                        x = np.linspace(lo, hi, 10001)
                        centers = (x[1:] + x[:-1])/2
                        mass = np.sum(np.exp(-(centers-2*delta)**2/4) / math.sqrt(4*math.pi)) * (hi-lo)/10000
                        for p in exact:
                            totals[p] += vals[p]*mass
                    for p in exact:
                        self.assertAlmostEqual(totals[p], exact[p], places=7)

    def test_safe_constraint_and_both_risky_sign_changes(self):
        differences = []
        for delta in (.25, .75, 1.5):
            for a in (0, .5, 1.5, 3):
                for rho in (0, .5, 1):
                    e = exact_accuracy(delta, a, rho)
                    self.assertLessEqual(e["equilibrium"], e["safe"]+1e-12)
                    differences.append(e["equilibrium"]-e["risky"])
        self.assertLess(min(differences), 0)
        self.assertGreater(max(differences), 0)

    def test_zero_risk_policies_agree_and_equal_ability_is_undefined(self):
        sim = simulate_cell(0, 0, 1, n=2000, seed=11)
        for p in ("safe", "risky"):
            np.testing.assert_array_equal(sim["winners"][p], sim["winners"]["equilibrium"])
        for metrics in sim["outcomes"].values():
            self.assertNotIn("accuracy", metrics)
            np.testing.assert_array_equal(metrics["selected_ability"], 0)
        self.assertTrue(all(x is None for x in exact_accuracy(0, 1, 0).values()))

    def test_zero_initial_noise_and_fair_ties(self):
        sim = simulate_cell(.75, 1.5, 0, n=10000, seed=27, sigma_0=0)
        np.testing.assert_array_equal(sim["outcomes"]["safe"]["accuracy"], 1)
        # Effective gap equals a here: this is a discrete, tie-bearing state.
        for policy, expected in exact_accuracy(.75, 1.5, 0, sigma_0=0).items():
            x = sim['outcomes'][policy]['accuracy']
            self.assertLessEqual(abs(x.mean()-expected), 5*x.std(ddof=1)/math.sqrt(len(x))+1e-12)
        ties = select_winners(np.zeros((10000, 2)), np.random.default_rng(17).random(10000))
        self.assertLess(abs(ties.mean()-.5), .02)
        self.assertEqual(select_winners(np.zeros((2, 2)), np.array([.1, .9])).tolist(), [0, 1])

    def test_label_swap_preserves_quality_and_complements_value(self):
        gap = np.array([-4., -1.5, -.2, 0, .2, 1.5, 4])
        for rho in (-1, 0, 1):
            v = state_strategies(gap, 1.5, rho)[2]
            swapped = state_strategies(-gap, 1.5, rho)[2]
            np.testing.assert_allclose(v, 1-swapped)
        scores = np.array([[2, 1], [0, 3], [1, 1.]])
        abilities = np.array([[.5, -.5], [-.5, .5], [.5, -.5]])
        t = np.array([.2, .9, .1])
        old = select_winners(scores, t)
        new = select_winners(scores[:, ::-1], 1-t)
        np.testing.assert_array_equal(abilities[np.arange(3), old], abilities[:, ::-1][np.arange(3), new])

    def test_fresh_evaluation_cannot_affect_selection_and_has_independent_noise(self):
        a = simulate_cell(.75, 1.5, 0, n=20000, seed=53)
        b = simulate_cell(.75, 1.5, 0, n=20000, seed=53, fresh_seed=999)
        self.assertLess(abs(a["fresh_first_noise_correlation"]), .025)
        for p in a["winners"]:
            np.testing.assert_array_equal(a["winners"][p], b["winners"][p])
            self.assertFalse(np.array_equal(a["outcomes"][p]["fresh"], b["outcomes"][p]["fresh"]))
            residual = a["outcomes"][p]["fresh_residual"]
            self.assertLess(abs(residual.mean()), 5*residual.std(ddof=1)/math.sqrt(len(residual)))
            metrics = a["outcomes"][p]
            self.assertAlmostEqual(metrics["selected_ability"].mean(), .75*(metrics["accuracy"].mean()-.5))

    def test_simulated_accuracy_matches_exact_with_stated_mc_error(self):
        for delta, a, rho in ((.75, 1.5, 0), (.25, 3, 1), (1.5, .5, .5)):
            sim = simulate_cell(delta, a, rho, n=20000, seed=104)
            for p, expected in exact_accuracy(delta, a, rho).items():
                x = sim["outcomes"][p]["accuracy"]
                self.assertLessEqual(abs(x.mean()-expected), 5*x.std(ddof=1)/math.sqrt(len(x))+1e-12)
