# Validation

What I actually checked on the current build, and what I didn't. Validated on
Windows 11 with Python 3.13.13, Quarto 1.9.38 and Node 24.15.0
(`data/environment.json` has the full versions).

## The maths and the study

| Check | Result |
|---|---|
| `python scripts/check.py` | 23 tests pass: the exact duel, ties at one and two shocks, unassailable leads, zero risk, label swaps, the cached study states against the original solver, the exact both-safe integral against independent quadrature, and simulated accuracy against exact values within the stated Monte Carlo error |
| `python scripts/export_reference.py` + `node scripts/check_browser_math.cjs` | 1,386 browser states, 15,251 numerical assertions: the JavaScript game matches the Python reference for every slider combination and boundary |
| `python scripts/run_study.py` | Reproduces `data/generated/study.json` byte for byte. Largest unilateral-deviation gain over all solved states: 5.6e-17 |
| Hand check | Shared shock (ρ = 1): matrix [[1, ½], [½, 1]], each player risky 50%, A's value 75%. Independent (ρ = 0): both-risky entry 75%, each player risky ⅔, A's value ⅔. General ρ: A's value (2+ρ)/(3+ρ), both-risky (3+ρ)/4, matching the derivation in the article |
| Selection identity | E[θ_selected] = δ[P(correct) − ½] holds for the saved sample means; fresh performance tracks selected ability (0.207 vs 0.210 in the worked example) |

The both-safe result is a consequence of the setup, and the article says so.
The comparison with both-risky changes sign between independent and shared
shocks (+6.58 and −5.70 percentage points exact at δ = 0.75, a = 1.5).

## The rendered page

`quarto render index.qmd` produces one self-contained `_output/index.html` with
fonts, the masthead engraving, the paper texture, scripts and figures embedded.

`npm run check:article` (Playwright 1.62.1, headless Edge 156) passes. It opens
the local file with all network requests blocked and checks:

- the three guided rival rules played by pressing the matrix rows, keyboard
  activation and focus order, exact best responses, and 27 boundary settings in
  free play;
- both reversal panels and all 48 study settings against the saved results and
  intervals, including the equal-ability and zero-risk controls;
- layouts at 320, 375, 390, 414, 768, 1280, 1440 and 1920 px with no page or
  figure overflow, and 200% text size at 320, 390 and 1280 px;
- the no-JavaScript fallback (exact payoff table and charts still readable);
- the bundled fonts load, contents links open collapsed evidence, and no page
  errors or external requests occur.

Sampled text contrast is 11.5:1 or better for every text role the suite
measures (ink on the newsprint ground). Paper on the alarm-red pressed button is
6.1:1, and alarm red on newsprint is 5.1:1, by calculation.

## Design review

The broadside design went through Impeccable's independent finish review: three
fix rounds, then a final pass on the masthead engraving, ending in a **ship**
verdict. That last pass re-checked only the open items; it wasn't a fresh review
of the whole page. At 1440×900 the masthead, engraving, scores and the whole 2×2
fit on the first screen.

All three images in `assets/broadside/` carry their origin or generation steps
in the file itself (`embed-prompt.mjs --scan`: 0 missing). Sources and licences
are in `docs/SOURCES.md`.

## Not tested

Firefox and Safari on this build, a physical touch device, real browser zoom
(only root text resizing was emulated) and a screen reader. The full final
journal texts of the two cited papers weren't read; see `docs/SOURCES.md`.
