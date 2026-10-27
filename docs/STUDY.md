# The model and the study

Everything here is a toy construction or a synthetic simulation. Scores are
points, not returns, and nothing below describes how real managers, funds or
hiring panels behave.

## The duel

Two equally able players, A and B, with an observed starting gap (benchmark:
A leads 105 to 100). Each chooses at the same time: safe adds 0, risky adds
`+a` or `−a` with equal odds (benchmark `a = 10`). Both know the gap, the menu,
the shock law and the prize rule. The higher final score takes the prize; a tie
splits it. Players care only about their expected share of the prize: no risk
aversion, effort, costs or utility from the score itself.

The two risky signs `X_A, X_B` are ±1 with correlation `ρ`:

| X_A | X_B | Probability |
|---:|---:|---:|
| +1 | +1 | (1 + ρ)/4 |
| +1 | −1 | (1 − ρ)/4 |
| −1 | +1 | (1 − ρ)/4 |
| −1 | −1 | (1 + ρ)/4 |

The final gap is `D = gap + a(s_A X_A − s_B X_B)`, and A gets 1, ½ or 0 as `D`
is positive, zero or negative. B gets the rest, so the game is constant-sum and
the 2×2 solver in `src/manufacturing_genius/duel.py` applies. Every reported
equilibrium is checked by its unilateral-deviation gains.

Checked benchmarks, gap 5 and `a = 10`:

- `ρ = 1`: matrix [[1, ½], [½, 1]]. A wants to match and B wants to differ.
  Each goes risky ½ the time and A's value is ¾.
- `ρ = 0`: the both-risky entry becomes ¾. Each goes risky ⅔ of the time and
  A's value is ⅔.
- Equal scores give ½ everywhere, and a lead over `2a` is unassailable. Those
  degenerate games have several equilibria; the solver returns the first pure
  saddle in safe/risky row-major order and I make no uniqueness claim.

The duel's players are equally able, so it shows incentives. It can't say
anything about selecting ability.

## The selection study

One player has per-round ability `+δ/2`, the other `−δ/2`, with labels assigned
at random. Then:

- First round: `S_i = θ_i + σ₀ Z_i`, with independent standard normal `Z`.
- Last round: each player chooses `b_i ∈ {0, 1}`, and the final two-round score
  is `F_i = S_i + θ_i + a b_i X_i`, with the signs correlated as above and
  independent of the first round.
- Players know both abilities and both scores, a deliberately generous
  complete-information benchmark. The evaluator sees only `F` and picks the
  higher one, with a fair coin for ties.
- Each last round is the duel at effective gap `d = S_A − S_B + θ_A − θ_B`,
  solved exactly.

I compare that equilibrium with two fixed rules: **both safe** (no risk allowed)
and **both risky** (risk required). Neither fixed rule is an equilibrium.

After selection, both players take a fresh test, `H_i = θ_i + σ_H E_i`, with
new independent noise and no risk choice. `H` never feeds back into selection
or into any choice of figure or parameter. Since `F` covers two rounds and `H`
one, I compare `F/2` with `H`.

Outcomes:

| Outcome | Definition |
|---|---|
| Selection accuracy | P(the winner has the larger θ); undefined when δ = 0 |
| Selected ability | Mean θ of the winner |
| Overstatement | Mean `F/2 − θ` of the winner; a property of the estimator, not dishonesty |
| Fresh performance | Mean `H` of the winner |

These are linked rather than independent: `E[θ_selected] = δ(P(correct) − ½)`
and `E[H_selected] = E[θ_selected]`.

### What the setup already decides

For the better player the effective gap is `G ~ N(2δ, 2σ₀²)`. With `V(g)` the
equilibrium win probability and `V(−g) = 1 − V(g)`,

`A_eq − A_safe = −∫₀^∞ (1 − V(g)) (f(g) − f(−g)) dg ≤ 0`,

so strategic risk can't beat both-safe here. With `v = (2+ρ)/(3+ρ)` and `C` the
CDF of `G`, `A_safe = 1 − C(0)` and
`A_eq = 1 − C(a) + v(C(a) − C(0)) + (1−v)(C(0) − C(−a))`. Both-risky substitutes
`2a` for `a` and `(3+ρ)/4` for `v`. The comparison with both-risky can go either
way, and that's the interesting one.

## Choices fixed before any results

Recorded on 2026-10-25 in `data/study_config.json`, which is hashed into the
results:

- `σ₀ = σ_H = 1`. Grid: `δ ∈ {0, 0.25, 0.75, 1.5}`, `a ∈ {0, 0.5, 1.5, 3}`,
  `ρ ∈ {0, 0.5, 1}`: 48 settings, including equal-ability and zero-risk
  controls. `ρ = −1`, discrete boundaries and zero first-round noise are test
  cases.
- 10,000 independent contests per setting, which caps the binary Monte Carlo
  standard error at 0.5 percentage points. No adaptive increase.
- One master seed, with separate PCG64 streams for labels, first scores, risky
  shocks, action draws, tie breaks and the fresh test, and independent streams
  per setting. All three rules share the same draws within a contest, so policy
  differences are paired.
- Each last-round state maps to one of finitely many exact payoff matrices
  (by where `d` sits relative to −2a, −a, 0, a, 2a), so the solver is cached
  per state; every cached solution is re-checked.
- Wilson intervals for accuracy; sample SD/√n normal intervals for means and
  paired differences. All are pointwise Monte Carlo intervals: simulation error
  inside the model, not evidence the model is realistic.
- Every setting and both paired comparisons are saved and shown, including nulls
  and sign reversals. The fresh-test figure uses the slice δ = 0.75, a = 1.5,
  chosen in advance.

## Checks

`scripts/check.py` covers zero risk (all rules agree), zero first-round noise,
label swaps, the equal-ability null, fair ties, independence of the fresh draws,
deviation gains, the selected-ability identity, and simulated accuracy against
the exact formulas within Monte Carlo error. Results are in `docs/VALIDATION.md`.

## Not in this model

Risk here changes variance only: there's no effort, learning or investment with
a higher expected payoff, and the evaluator ranks raw scores instead of
inferring ability. Adding personal loss costs would make the game general-sum
and needs a different solver than the one in this repo.
