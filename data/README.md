# Data

There's no real financial, personal or institutional data here.

- `study_config.json`: the grid, replicate count, seeds and figure plan, fixed
  before any results.
- `environment.json`: runtime and font versions used for validation.
- `reference/duel_benchmark.json`: exact game states from
  `scripts/export_reference.py`, used to check the browser game against Python.
- `generated/study.json`: every setting's estimates, paired differences, exact
  accuracies and equilibrium checks, with the config hash. Rebuilt by
  `scripts/run_study.py`.
- `generated/*.svg`: the article's figures, rebuilt by `scripts/make_figures.py`.

The JSON and SVG outputs are committed on purpose; PNG previews are ignored.
