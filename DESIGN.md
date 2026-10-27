---
name: Manufacturing Genius
description: The last-round duel printed as a penny-press broadside, with the study following down the sheet.
colors:
  newsprint: "#dccfb1"
  newsprint-deep: "#cfc09d"
  relief-ink: "#1c1712"
  press-wash: "#4f4335"
  figure-wash: "#6e604d"
  figure-rule: "#b9a98a"
  alarm-red: "#9c2414"
typography:
  display:
    fontFamily: "Ultra, Rockwell Extra Bold, serif"
    fontSize: "calc(100cqw / 7.6)"
    fontWeight: 400
    lineHeight: 0.82
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "League Gothic, Arial Narrow, sans-serif"
    fontSize: "clamp(2.4rem, 5.4vw, 3.4rem)"
    fontWeight: 400
    lineHeight: 0.98
    letterSpacing: "0.005em"
  title:
    fontFamily: "League Gothic, Arial Narrow, sans-serif"
    fontSize: "clamp(1.75rem, 3.6vw, 2.15rem)"
    fontWeight: 400
    lineHeight: 1.02
    letterSpacing: "0.01em"
  numeral:
    fontFamily: "League Gothic, Arial Narrow, sans-serif"
    fontSize: "clamp(2.3rem, 9cqw, 3.6rem)"
    fontWeight: 400
    lineHeight: 1
    fontFeature: "tnum"
  score:
    fontFamily: "Ultra, Rockwell Extra Bold, serif"
    fontSize: "3.2rem"
    fontWeight: 400
    lineHeight: 1
    fontFeature: "tnum"
  body:
    fontFamily: "Old Standard, Georgia, serif"
    fontSize: "1.18rem"
    fontWeight: 400
    lineHeight: 1.6
    fontFeature: "lnum"
  label:
    fontFamily: "League Gothic, Arial Narrow, sans-serif"
    fontSize: "1.3rem"
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: "0.03em"
  note:
    fontFamily: "Old Standard, Georgia, serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  none: "0"
spacing:
  xs: "0.5rem"
  sm: "1rem"
  md: "1.5rem"
  lg: "2.25rem"
  xl: "3.25rem"
  section: "4.5rem"
components:
  button-inked:
    backgroundColor: "{colors.newsprint}"
    textColor: "{colors.relief-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.45rem 0.9rem"
    height: "52px"
  button-inked-hover:
    backgroundColor: "{colors.relief-ink}"
    textColor: "{colors.newsprint}"
  matrix-row:
    backgroundColor: "{colors.newsprint}"
    textColor: "{colors.relief-ink}"
    typography: "{typography.headline}"
    rounded: "{rounded.none}"
    padding: "0.3rem 0.8rem"
    height: "4.1rem"
  matrix-row-pressed:
    backgroundColor: "{colors.alarm-red}"
    textColor: "{colors.newsprint}"
  matrix-cell:
    textColor: "{colors.press-wash}"
    typography: "{typography.numeral}"
    rounded: "{rounded.none}"
    height: "4.1rem"
  matrix-cell-hit:
    backgroundColor: "{colors.relief-ink}"
    textColor: "{colors.newsprint}"
  select-field:
    backgroundColor: "{colors.newsprint}"
    textColor: "{colors.relief-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "0.55rem 0.7rem"
    height: "48px"
  disclosure-open:
    backgroundColor: "{colors.relief-ink}"
    textColor: "{colors.newsprint}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
  table-head:
    backgroundColor: "{colors.relief-ink}"
    textColor: "{colors.newsprint}"
    typography: "{typography.label}"
---

# Design System: Manufacturing Genius

## Overview

**Creative North Star: "The Day's Broadside"**

The page is a single sheet of nineteenth-century penny press. Mottled newsprint carries one black relief ink, worn wood type for the masthead and the scores, condensed gothic for heads and numerals, and a period news face for the text. The duel is the front-page event: a ruled box under the masthead holding the rule, the scores and a live 2x2 that the reader plays by pressing a row. The study then runs down the sheet in ruled sections and double-ruled evidence boxes, ending at the references and a colophon.

The sheet is dense and printed, not soft. Structure comes from rules (heavy-over-hairline pairs, double rules, column rules) and from ink: inverted ink blocks for headers, hard offset ink shadows under the things you can press. Colour is almost absent; one alarm red marks what the reader has chosen and floods the engraving. The style must never make the statistics look less serious, so every ornament is a print device that also does a job (separating, grouping, signalling a press).

This world replaced the earlier warm reading surface (Commissioner and Asap on ivory, clay accent, rounded controls). Nothing from that system carries over.

**Key Characteristics:**
- Mottled newsprint ground, one relief ink, one reserved red.
- Ultra wood type with a wear mask for the masthead and scores; League Gothic uppercase for every head, label and table numeral; Old Standard for reading.
- Thick-thin rule pairs open and close the sheet and every section head.
- Square corners everywhere; depth is a flat ink offset, never a blur.
- Pressable things look inked and physically press into the paper.

### Materials and provenance

Three rasters ship, each with embedded provenance:
- `assets/broadside/spurt-for-the-lead.jpg`: "A spurt for the lead", Frank Leslie's Illustrated Newspaper, 4 October 1879, public domain via the Library of Congress. The black relief line is multiplied over a flat alarm-red field and runs as a full-width band under the masthead, credited on a one-line ink strip at the lower right.
- `assets/broadside/newsprint.jpg`: photograph by Pink Sherbet Photography, CC BY 2.0, cropped, flattened and tiled at 720px as the page ground. Attribution sits in the colophon and `docs/SOURCES.md`; keep both if the texture stays.
- `assets/broadside/wood-wear.png`: a procedural wear mask applied to Ultra (masthead at 340px, scores at 260px) so the wood type prints unevenly.

Fonts are bundled in `assets/fonts`: Ultra (Apache 2.0), League Gothic and Old Standard TT (OFL). No font loads from a network.

### Review status

The finish review returned "ship" after three fix rounds and a final pass on the engraving band. That last verdict scored only the engraving item and confirmed the first-viewport fix still held; it was not a fresh review of the whole surface. The browser suite passes in Edge from 320px to 1920px. Firefox, Safari, touch hardware and screen readers have not been tested.

## Colors

Newsprint and one relief ink do almost all the work; a single alarm red is held back for the reader's own choice.

### Primary
- **Alarm Red** (alarm-red): the reader's score (105), the pressed matrix row, the better-row underline in the "Against this rival" column, the flat field under the masthead engraving, the focus ring, link hover and the range-slider accent. Nothing else.

### Neutral
- **Relief Ink** (relief-ink): all text, every rule and border, the offset shadows, inverted header blocks (game guide, rival column, table heads, open disclosures, credit strip), and every figure's primary series.
- **Newsprint** (newsprint): the page colour under the tiled paper photograph, and the face of every inked control. Inverted ink blocks use it as their text colour.
- **Newsprint Deep** (newsprint-deep): code blocks and the scrollbar track; a slightly darker sheet for verbatim material.
- **Press Wash** (press-wash): the numerals in matrix cells the reader has not chosen, so the chosen row reads in full ink beside them.
- **Figure Wash** (figure-wash): the third series in the matplotlib figures (filled triangles, dotted lines) and its swatch in the HTML figure keys.
- **Figure Rule** (figure-rule): gridlines inside the figures.
- Table cell borders and the mobile contents list use relief ink at 35% alpha (`rgba(28, 23, 18, .35)`) as a hairline.

### Named Rules

**The Reader's Red Rule.** Red marks the reader's own choice and nothing that the page chose for them: their score, their pressed row, the better row in the payoff column, focus, plus the engraving's colour field. Section heads, figures, the contents rail and the active contents entry stay in ink. If a new element wants red, it must be something the reader did.

**The Ink-Only Figures Rule.** Figure series are told apart by ink value (ink or figure wash), marker fill (solid, open, wash) and line style (heavy solid, dashed, dotted), never by hue. The established mapping: equilibrium is ink, filled circle, heavy solid line (2.2); both-safe is ink, open square, dashed (1.3); both-risky is figure wash, filled triangle, dotted (1.6). Figures render on a transparent ground so the newsprint shows through.

## Typography

**Display Font:** Ultra (with Rockwell Extra Bold, serif)
**Heads and Numerals:** League Gothic (with Arial Narrow, sans-serif)
**Body Font:** Old Standard TT, declared as "Old Standard" (with Georgia, serif)
**Code:** ui-monospace, Cascadia Mono, Consolas

**Character:** Fat-face wood type shouts the title and the scores; a tall condensed gothic sets every head, label and number in uppercase with slight tracking; a Victorian news serif carries the reading, set italic for notes, captions and guide copy.

### Hierarchy
- **Display** (Ultra 400, sized to the column with container units, 0.82 line-height): the masthead only. MANUFACTURING at `100cqw / 10.95`, GENIUS at `100cqw / 7.6`, centred, uppercase, never wrapping, wear-masked.
- **Score** (Ultra 400, 3.2rem, tabular figures): the two scores in the duel's scoreboard, also wear-masked.
- **Headline** (League Gothic 400, clamp(2.4rem, 5.4vw, 3.4rem), 0.98): section heads (h2), uppercase, sitting under a heavy-over-hairline rule pair. Appendix and references headings use the same treatment.
- **Title** (League Gothic 400, clamp(1.75rem, 3.6vw, 2.15rem), 1.02): subsection heads (h3), uppercase, under a 1.5px rule. h4 is League Gothic 1.45rem.
- **Numeral** (League Gothic 400, clamp(2.3rem, 9cqw, 3.6rem), tabular): payoff matrix cells. Row buttons use League Gothic at clamp(2rem, 6cqw, 2.4rem).
- **Body** (Old Standard 400, 1.18rem, 1.6, lining figures): reading text, capped at 36em per paragraph. Drops to 1.1rem under 600px. The opening sets in two ruled columns with a four-line Ultra drop cap on the first paragraph.
- **Label** (League Gothic 400, 1.15–1.6rem, 0.03–0.08em tracking, uppercase): buttons, disclosure summaries, control labels, table heads, the folio, contents rail entries, verdict lines.
- **Note** (Old Standard italic, 0.9–1rem): figure captions, measurements, game notes, guide copy, matrix sub-labels, contents subsections.

### Named Rules

**The Three Faces Rule.** Ultra is for the masthead, the scores and the opening drop cap only; League Gothic for heads, labels and numerals; Old Standard for everything read. Do not set reading text in League Gothic or a head in Old Standard.

**The Honest Minus Rule.** Old Standard draws U+2212 as a long dash, so its font faces exclude that code point through unicode-range and minus signs fall back to the next serif. Keep the exclusion on any new Old Standard face.

## Layout

The sheet lives inside Quarto's article column with the contents rail to its right on wide screens. The masthead sits in the body column, not full-bleed: a heavy-over-hairline rule (5px and 1.5px with a 4px gap), the two-line Ultra title, a full-width engraving band 150–170px tall, then a byline folio between 1.5px rules with SVG stars as separators. At 1440x900 the masthead, folio and the top of the front-page box (guide, scores, matrix head and rows) are all above the fold.

The front page is a ruled grid: game guide (ink block) and scoreboard side by side at 1.45fr to 1fr, then the full-width matrix, the play area, and the author's invitation in two ruled columns under a double rule. Under 760px it collapses to one column in that order; the opening columns, the rules columns and every two-up control grid go single-column; the folio stacks and drops its stars. Under 600px padding steps down to the small space and the front page's shadow shrinks to the standard press shadow.

The matrix sizes from its own container (container queries), not the viewport: four tracks (row label, two rival columns, the "Against this rival" net column) with 10px gaps, tightening to 6px gaps and smaller numerals under 34rem. It scrolls horizontally rather than squeezing below its minimum width.

Spacing follows the scale in the frontmatter: sections open with 4.5rem above, subsections 3.25rem, boxes pad at 1.5rem (1rem on phones), and grids gap at 1.5rem. Wide figures and the results table sit in horizontal scrollers with a minimum width; on phones a one-line italic hint above the grid figure says it scrolls.

## Elevation & Depth

Depth is printed, not lit. Things that can be pressed, and the front-page box, carry a hard ink offset with no blur; pressing moves the element 3px down and right while the shadow collapses to 2px, so the control seats into the paper. Everything else is flat and separated by rules.

### Shadow Vocabulary
- **Front-page offset** (`box-shadow: 12px 12px 0 #1c1712`): the duel's front-page box only; drops to the press shadow under 600px.
- **Press** (`box-shadow: 8px 8px 0 var(--mg-ink)`): the masthead engraving band.
- **Press small** (`box-shadow: 5px 5px 0 var(--mg-ink)`): inked controls at rest (reading shortcuts, guide buttons, disclosure summaries, matrix rows; 4px on narrow matrices).
- **Pressed** (`box-shadow: 2px 2px 0 var(--mg-ink)` with `translate(3px, 3px)`): the active state of every inked control and the resting state of the pressed matrix row.

### Named Rules

**The Press-Not-Lift Rule.** Shadows are flat ink offsets down and to the right, and only on pressable controls, the engraving band and the front-page box. Interaction moves an element into the paper, never up off it. Secondary text buttons (skip, restart) drop the shadow and use a 1.5px border so the primary action stays the one that looks inked.

## Shapes

Every corner is square (border-radius 0 on controls, selects, code blocks and boxes). Form comes from rule weight: 3px solid ink for controls, the front-page box, the engraving band and section dividers inside the duel; 5px double for evidence boxes, the references box, the double rule above the duel's rules and controls, and the "Against this rival" column; 1.5px for hairlines, column rules and subsection heads. The sheet opens with a 5px rule over a 1.5px rule and the colophon closes with the inverse (1.5px over 5px).

One-sided rules are print column rules, not card accents: the 5px double rule on the left of the "Against this rival" column and of the random-play dispatch. The design-hook's side-tab check is accepted as ignored for `assets/report.css` only (recorded in `.impeccable/config.json`, which describes it as the rule between the engraving plate and the red flood inside the ruled band). Keep the suppression scoped to that file; one-sided borders anywhere else still get flagged.

### Named Rules

**The Rule Weight Rule.** Three weights only: 1.5px hairline, 3px solid, 5px (solid in rule pairs, double around boxes). Grouping is said with a rule, never with a tinted card or a radius.

## Components

### Inked Buttons
Tactile and blunt: a block of paper outlined in ink that presses down when used.
- **Shape:** square, 3px ink border.
- **Primary:** newsprint face, ink text in League Gothic uppercase (1.45rem in the guide, 1.6rem in the reading shortcuts with an SVG pointing-hand mark), minimum 52px tall (60px for shortcuts), press-small shadow.
- **Hover (hover-capable devices only):** inverts to an ink face with newsprint text.
- **Active:** moves 3px down and right, shadow collapses to the pressed offset. Transitions run 0.12s on `cubic-bezier(.2, .8, .2, 1)` and switch off under reduced motion.
- **Focus:** 3px alarm-red outline at 3px offset, page-wide.
- **Secondary text button:** same face and type, 1.5px border, no shadow.
- **Disabled:** 55% opacity, not-allowed cursor.

### Payoff Matrix (signature)
The front-page event. Column heads are League Gothic uppercase with an italic sub-label ("every time", "never") over a 3px rule; the rival column the current rule plays inverts to an ink block; the "Against this rival" head sits over a 5px double rule.
- **Row buttons** are inked buttons in League Gothic at headline scale with an Old Standard note under the label. Pressed (`aria-pressed="true"`), the row fills alarm red with a red border and newsprint text and stays seated at the pressed offset.
- **Cells** are 1.5px-ruled boxes with League Gothic tabular numerals. Unchosen rows read in press wash; the chosen row's cells take a 3px border and full ink; the drawn outcome inverts to an ink block.
- **"Against this rival" column** is set off by a 5px double rule on its left; the better row's figure turns alarm red with a 4px underline.

### Scoreboard
Two scores in worn Ultra over League Gothic labels; the reader's score is alarm red, the rival's ink. An italic line below states the position ("You lead.").

### Game Guide
An ink block with newsprint text: League Gothic title, a tracked uppercase progress line ("Rule 1 of 3", which states the reader's place in the three guided rules), italic guide copy.

### Boxed Evidence
Figure panels, the static benchmark and the references sit inside a 5px double ink border with 1.5rem padding. Two-up comparisons divide with a 1.5px column rule and stack with a top rule under 900px. Verdict lines are League Gothic uppercase over a 1.5px rule; captions are Old Standard italic, left-aligned, under a rule.

### Disclosures
Summaries are inked buttons with the label at left and an italic "Show" / "Hide" at right. Open, the summary inverts to an ink block.

### Inputs
- **Select:** square, 3px ink border, newsprint face, Old Standard 1.05rem, 48px tall.
- **Range:** native slider with the alarm-red accent, 44px tall hit area; its value prints beside the League Gothic label in Old Standard tabular figures.

### Tables
Ink header rows with newsprint League Gothic uppercase text; transparent body cells with 35%-ink hairlines and tabular figures. The full results ledger scrolls inside a container ruled 3px top and bottom, with a sticky header.

### Navigation
The contents rail is headed "In this sheet" in League Gothic under a 3px rule. Top-level entries are League Gothic uppercase; subsections Old Standard italic. The active entry is bold with a 3px ink underline, never red. Under 992px an in-page contents list replaces the rail, with 44px rows divided by hairlines.

### Masthead and Colophon
The masthead is described in Layout. The colophon is centred italic Old Standard under the closing rule pair and names the faces, the engraving source and the paper photograph's licence.

## Do's and Don'ts

### Do:
- **Do** keep alarm red for what the reader chose (score, pressed row, better row), the focus ring and the engraving's colour field.
- **Do** separate figure series by ink value, marker fill and line style, using the equilibrium / both-safe / both-risky mapping above.
- **Do** group with rules at 1.5px, 3px or 5px (double around boxes) and keep every corner square.
- **Do** give pressable controls a 3px ink border and a hard ink offset that collapses by 3px when pressed.
- **Do** set heads, labels and numerals in League Gothic uppercase, reading text in Old Standard, and reserve Ultra for the masthead, scores and the opening drop cap.
- **Do** keep tabular figures on scores, matrix cells, tables and measurements.
- **Do** carry provenance in any new shipping raster and credit it in the colophon and `docs/SOURCES.md`.

### Don't:
- **Don't** round corners, add blurred or lifted shadows, or use tinted cards to group content.
- **Don't** use red in figures, the contents rail, section heads or any decoration the reader did not trigger.
- **Don't** add grid or graph-paper backgrounds, rubber stamps or stamp-style badges.
- **Don't** add small tracked uppercase labels above headings; heads stand on their rules.
- **Don't** reintroduce the retired warm reading surface (Commissioner, Asap, ivory ground, clay accent, rounded controls).
- **Don't** set Old Standard faces without the U+2212 exclusion.
