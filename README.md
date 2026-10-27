# MANUFACTURING GENIUS

A statistical feature about what a winning score actually tells you, with a
last-round game you can play and a reproducible simulation behind it.

**Read it:** [manufacturinggenius.jarabana.com](https://manufacturinggenius.jarabana.com)

When the prize goes to whoever finishes first, taking a gamble can be the smart
move even if it adds nothing to your expected score. I start with a two-player
duel small enough to solve exactly, then give the players real differences in
ability and check how often the better one wins, and how the winner looks when
you test them again. Everything is a toy model or a simulation; none of it is
real market data.

## Running it

Python 3.11+, [Quarto](https://quarto.org) and Node. On Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip install --no-deps -e .
powershell -ExecutionPolicy Bypass -File scripts/reproduce.ps1
```

That runs the checks, reruns the study (it reproduces `data/generated/study.json`
exactly), redraws the figures and renders `_output/index.html`, a single file
that works offline. On macOS/Linux, run the same steps from
`scripts/reproduce.ps1` with `.venv/bin/python` and `QUARTO_PYTHON` pointed at
it.

## What's where

| Path | |
|---|---|
| `index.qmd`, `manuscript/` | The article |
| `src/manufacturing_genius/` | Exact duel solver and the study simulation |
| `scripts/`, `tests/` | Study, figures and checks |
| `assets/` | The game, styling, fonts and masthead art |
| `data/` | Study config and saved results |
| `docs/STUDY.md` | The model and study design |
| `docs/SOURCES.md` | Papers, fonts and image credits |
| `docs/VALIDATION.md` | What was checked, and what wasn't |

## Licence

Code is MIT (see `LICENSE`). The article text is mine, all rights reserved.
Fonts and images keep their own licences, listed in `docs/SOURCES.md`.
