"""Mathematical checks for the introductory game, not claims about talent."""

import math
import random
import unittest

from manufacturing_genius.duel import (
    duel_payoff_matrix,
    evaluate_strategies,
    joint_shocks,
    zero_sum_equilibrium,
)


class DuelTests(unittest.TestCase):
    def assertMatrixClose(self, actual, expected):
        for actual_row, expected_row in zip(actual, expected):
            for x, y in zip(actual_row, expected_row):
                self.assertAlmostEqual(x, y)

    def test_shared_shock_benchmark_and_equilibrium(self):
        matrix = duel_payoff_matrix()
        self.assertEqual(matrix, ((1.0, 0.5), (0.5, 1.0)))
        result = zero_sum_equilibrium(matrix)
        self.assertAlmostEqual(result.row_risky_probability, 0.5)
        self.assertAlmostEqual(result.column_risky_probability, 0.5)
        self.assertAlmostEqual(result.value, 0.75)
        self.assertLessEqual(result.exploitability, 1e-12)

    def test_independent_shocks_change_strategies_and_value(self):
        matrix = duel_payoff_matrix(correlation=0)
        self.assertEqual(matrix, ((1.0, 0.5), (0.5, 0.75)))
        result = zero_sum_equilibrium(matrix)
        self.assertAlmostEqual(result.row_risky_probability, 2 / 3)
        self.assertAlmostEqual(result.column_risky_probability, 2 / 3)
        self.assertAlmostEqual(result.value, 2 / 3)

    def test_anticorrelation_boundary(self):
        matrix = duel_payoff_matrix(correlation=-1)
        self.assertEqual(matrix, ((1.0, 0.5), (0.5, 0.5)))
        result = zero_sum_equilibrium(matrix)
        self.assertAlmostEqual(result.value, 0.5)
        self.assertLessEqual(result.exploitability, 1e-12)

    def test_equal_initial_scores_have_half_prize_share(self):
        for rho in (-1.0, -0.4, 0.0, 0.6, 1.0):
            self.assertMatrixClose(
                duel_payoff_matrix(initial_gap=0, correlation=rho),
                ((0.5, 0.5), (0.5, 0.5)),
            )

    def test_ties_at_one_shock_are_split_fairly(self):
        self.assertEqual(
            duel_payoff_matrix(initial_gap=10, shock_size=10, correlation=1),
            ((1.0, 0.75), (0.75, 1.0)),
        )

    def test_ties_at_two_shocks(self):
        self.assertEqual(
            duel_payoff_matrix(initial_gap=20, shock_size=10, correlation=0),
            ((1.0, 1.0), (1.0, 0.875)),
        )

    def test_unassailable_lead_and_zero_risk(self):
        for rho in (-1, 0, 1):
            for gap, expected in ((21, 1.0), (-21, 0.0)):
                matrix = duel_payoff_matrix(initial_gap=gap, correlation=rho)
                self.assertEqual(matrix, ((expected, expected), (expected, expected)))
                self.assertAlmostEqual(zero_sum_equilibrium(matrix).value, expected)
        self.assertEqual(duel_payoff_matrix(shock_size=0), ((1.0, 1.0), (1.0, 1.0)))

    def test_player_swap_complements_transposed_matrix(self):
        for gap in (-25, -20, -10, -5, 0, 5, 10, 20, 25):
            for rho in (-1, -0.25, 0, 0.75, 1):
                original = duel_payoff_matrix(initial_gap=gap, correlation=rho)
                reversed_game = duel_payoff_matrix(initial_gap=-gap, correlation=rho)
                self.assertMatrixClose(
                    reversed_game,
                    tuple(tuple(1 - original[j][i] for j in (0, 1)) for i in (0, 1)),
                )

    def test_score_unit_invariance(self):
        original = duel_payoff_matrix(initial_gap=5, shock_size=10, correlation=0.3)
        self.assertEqual(original, duel_payoff_matrix(500, 1000, 0.3))

    def test_joint_distribution_has_fair_marginals_and_requested_correlation(self):
        for rho in (-1, -0.7, 0, 0.3, 1):
            shocks = joint_shocks(rho)
            self.assertAlmostEqual(sum(prob for _, _, prob in shocks), 1)
            self.assertAlmostEqual(sum(a * prob for a, _, prob in shocks), 0)
            self.assertAlmostEqual(sum(b * prob for _, b, prob in shocks), 0)
            self.assertAlmostEqual(sum(a * b * prob for a, b, prob in shocks), rho)

    def test_best_response_diagnostics_expose_a_non_equilibrium(self):
        result = evaluate_strategies(duel_payoff_matrix(), 0, 0)
        self.assertEqual(result.value, 1)
        self.assertEqual(result.row_deviation_gain, 0)
        self.assertEqual(result.column_deviation_gain, 0.5)
        self.assertEqual(result.exploitability, 0.5)

    def test_general_solver_on_hand_computed_games(self):
        # A strict pure saddle, then asymmetric matching pennies.
        pure = zero_sum_equilibrium(((3, 1), (2, 0)))
        self.assertEqual((pure.row_risky_probability, pure.column_risky_probability), (0, 1))
        self.assertEqual(pure.value, 1)
        mixed = zero_sum_equilibrium(((2, -1), (-3, 4)))
        self.assertAlmostEqual(mixed.row_risky_probability, 0.3)
        self.assertAlmostEqual(mixed.column_risky_probability, 0.5)
        self.assertAlmostEqual(mixed.value, 0.5)

    def test_equilibria_allow_no_profitable_unilateral_deviation(self):
        # Reproducible integer games cover saddle points, degeneracies and mixtures.
        rng = random.Random(20261025)
        for _ in range(200):
            matrix = tuple(tuple(rng.randint(-9, 9) for _ in (0, 1)) for _ in (0, 1))
            eq = zero_sum_equilibrium(matrix)
            for deviation in (0.0, 0.25, 0.5, 0.75, 1.0):
                row_value = evaluate_strategies(matrix, deviation, eq.column_risky_probability).value
                column_value = evaluate_strategies(matrix, eq.row_risky_probability, deviation).value
                self.assertLessEqual(row_value, eq.value + 1e-10)
                self.assertGreaterEqual(column_value, eq.value - 1e-10)

    def test_positive_affine_payoff_transformation_preserves_strategies(self):
        original = ((2, -1), (-3, 4))
        transformed = tuple(tuple(7 * x - 20 for x in row) for row in original)
        first, second = zero_sum_equilibrium(original), zero_sum_equilibrium(transformed)
        self.assertAlmostEqual(first.row_risky_probability, second.row_risky_probability)
        self.assertAlmostEqual(first.column_risky_probability, second.column_risky_probability)
        self.assertAlmostEqual(second.value, 7 * first.value - 20)

    def test_invalid_parameters_and_matrices(self):
        for invalid in (math.nan, math.inf, -math.inf, True, "5", None):
            with self.assertRaises(ValueError):
                duel_payoff_matrix(initial_gap=invalid)
        for invalid in (-1, math.nan, True):
            with self.assertRaises(ValueError):
                duel_payoff_matrix(shock_size=invalid)
        for invalid in (-1.01, 1.01, math.inf, False):
            with self.assertRaises(ValueError):
                joint_shocks(invalid)
        for invalid in ((), ((1, 2),), ((1, 2, 3), (4, 5, 6)), ((1, math.nan), (3, 4)), None):
            with self.assertRaises(ValueError):
                zero_sum_equilibrium(invalid)
        for invalid in (-0.1, 1.1, math.nan, True):
            with self.assertRaises(ValueError):
                evaluate_strategies(((1, 0), (0, 1)), invalid, 0.5)
        for invalid in (0, -1, 0.1, math.nan):
            with self.assertRaises(ValueError):
                zero_sum_equilibrium(((1, 0), (0, 1)), tolerance=invalid)


if __name__ == "__main__":
    unittest.main()
