# Sources

The article keeps three things apart: published research, my own toy
derivations, and my own synthetic study. No paper supplies the duel's scores or
any simulated point in the figures.

## Hvide and Kristiansen (2003)

Hans K. Hvide and Eirik G. Kristiansen. "Risk Taking in Selection Contests."
*Games and Economic Behavior* 42(1), 172–179. DOI:
[10.1016/S0899-8256(02)00538-9](https://doi.org/10.1016/S0899-8256(02)00538-9).

- Metadata and the full abstract checked on the
  [University of Aberdeen research record](https://abdn.elsevierpure.com/en/publications/risk-taking-in-selection-contests/)
  and the [publisher's indexed page](https://www.sciencedirect.com/science/article/pii/S0899825602005389).
  (The university record lists the issue as 42; it's issue 1.)
- What the article uses it for: the paper studies risk choice, instead of
  effort, and how well contests select. I don't import its findings on
  restricting competition, and I don't claim to reproduce its proofs.
- I also read the 25-page Norges Bank working version (series 1999/2, title page
  dated February 7, 2000; [EconStor](https://hdl.handle.net/10419/209768)):
  introduction, model, information structure, selection propositions and
  conclusion. That version has private information about types and independent
  outputs, so my complete-information, correlated-shock study is a separate
  construction.
- I haven't read the full final journal text.

## Chen, Hughson and Stoughton (2025)

Joseph Chen, Eric Hughson and Neal Stoughton. "Strategic Mutual Fund
Tournaments." *Journal of Financial and Quantitative Analysis* 60(7), 3344–3379.
DOI: [10.1017/S0022109024000590](https://doi.org/10.1017/S0022109024000590).

- Metadata and the full abstract checked on the
  [Cambridge page](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/strategic-mutual-fund-tournaments/347C2C7FF149D3DE40538054FD545D91).
- What the article uses it for: their multi-period tournament analysis
  describes a leader cutting back on risk depending on the size of the lead. I
  don't claim my binary shared-shock equilibrium is their model.
- I also read the 61-page manuscript dated May 9, 2018
  ([SSRN 2023805](https://ssrn.com/abstract=2023805)): assumptions, the two- and
  multi-player lock-in sections, the conclusion and Table 1. Its continuous,
  initially independent normal risks differ from my binary example.
- The abstract mentions empirical support. I make no empirical claim, and I
  haven't read the full final journal text.

Both papers are context for the question, not validation of my numbers or
evidence that the toy model fits real institutions.

## Fonts and the masthead engraving

[Ultra](https://github.com/google/fonts/tree/main/apache/ultra) (Apache 2.0),
[League Gothic](https://github.com/google/fonts/tree/main/ofl/leaguegothic) and
[Old Standard TT](https://github.com/google/fonts/tree/main/ofl/oldstandardtt)
(both SIL OFL 1.1), from the official Google Fonts repository, bundled
unmodified in `assets/fonts/` with their licence texts. File hashes are in
`data/environment.json`.

The masthead engraving is "New York City: the fifth contest for the
long-distance pedestrian championship of the world, at the Madison Square
Garden. A spurt for the lead," *Frank Leslie's Illustrated Newspaper*,
4 October 1879, Library of Congress
[LCCN 99614124](https://lccn.loc.gov/99614124), public domain, via
[Wikimedia Commons](https://commons.wikimedia.org/wiki/File:New_York_City_-_the_fifth_contest_for_the_long-distance_pedestrian_championship_of_the_world,_at_the_Madison_Square_Garden_-_a_spurt_for_the_lead_LCCN99614124.jpg).
`assets/broadside/spurt-for-the-lead.jpg` is a crop of the runners with the
engraved line printed in black over a flat red field; the exact processing is
embedded in the file's JPEG comment.

The paper texture (`assets/broadside/newsprint.jpg`) is cut from
["Free dark vintage paper page texture for layers"](https://commons.wikimedia.org/wiki/File:Free_dark_vintage_paper_page_texture_for_layers_(2982207584).jpg)
by Pink Sherbet Photography, a photograph of a 120-year-old page, licensed
[CC BY 2.0](https://creativecommons.org/licenses/by/2.0/). I cropped it, flattened
the lighting, made it tile and tinted it; the steps are in the file's JPEG
comment. The worn wood-type mask (`assets/broadside/wood-wear.png`) is
generated in code and documented the same way.

## Study provenance

`data/study_config.json` was written before the first real run and is hashed
into `data/generated/study.json`. `docs/STUDY.md` records the
assumptions. The gap-game formulas and the both-safe inequality are my own
derivations, checked independently against the original enumerator. Every study
setting and paired comparison is saved, with nothing dropped based on results.
