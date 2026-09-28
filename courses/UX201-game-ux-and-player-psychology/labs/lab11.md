# UX201 · Lab 11: Accessibility audit of a shipped game

Assigned in week 11 ([lecture](../lectures/w11-accessibility-guidelines.md)). Due at the start of week 12. Pairs allowed; each pair submits one report.

## Objective

Audit one shipped game against twelve basic accessibility guidelines, measure contrast on its worst-case screens, and turn the failures into a ranked fix list a producer could schedule. The point is to practise the audit procedure from section 3 of the lecture (scope, audit, rank) and to measure rather than judge by eye.

## Starter materials

Everything is in [`lab11-starter/`](lab11-starter/) and this file.

**1. `contrast.py`.** A dependency-free Python script. It reads a CSV of colour measurements and prints relative luminance, the WCAG contrast ratio, pass or fail against the XAG 102 threshold (4.5:1 standard, 3:1 large), and the black-box opacity needed to pass (linear-light model from the lecture). Run it on the included `measurements.csv` first. The "white on snow" row should give 1.10:1 and a needed opacity of 0.80, matching the lecture.

**2. `measurements.csv`.** Example input. Columns: `screen`, `element`, `text_hex`, `background_hex`, `size` (`standard` or `large`).

**3. The twelve guidelines to audit.** Six from the Game Accessibility Guidelines (GAG) and six rules from the Xbox Accessibility Guidelines (XAG).

| # | Source | Guideline or rule |
|---|---|---|
| 1 | GAG | Allow controls to be remapped / reconfigured |
| 2 | GAG | Ensure no essential information is conveyed by a fixed colour alone |
| 3 | GAG | Use an easily readable default font size |
| 4 | GAG | Provide subtitles for all important speech |
| 5 | GAG | Provide a visual indication of who is currently speaking |
| 6 | GAG | Provide an option to adjust contrast |
| 7 | XAG 101 | Default text at least 26 px (console) or 18 px (PC) at 1080p, scalable to 200% |
| 8 | XAG 102 | Standard text and key elements at least 4.5:1 against the lowest-contrast background |
| 9 | XAG 103 | Critical audio cues also shown visually (or by haptics) |
| 10 | XAG 104 | Subtitles on by default, or selectable before any speech |
| 11 | XAG 104 | Subtitle lines at most about 40 characters, at most two lines |
| 12 | XAG 104 | Subtitle background available, with 0-100% opacity |

**4. Audit sheet** (copy into your report).

| # | In scope? | Result (pass, partial, fail) | Evidence (screenshot ID, measured value) | Players affected (permanent, temporary, situational) | Severity (blocks, hinders, annoys) | Fix and rough cost (S, M, L) |
|---|---|---|---|---|---|---|

## Steps

1. **Choose the game.** Any shipped game you can play for three hours during the week. Note the platform, version and the date you tested.
2. **Scope.** For each of the twelve items, decide whether the game has the feature it covers. Mark out-of-scope items and say why.
3. **Capture worst cases.** Play until you have screenshots of the menu, a dialogue scene with subtitles on, the brightest gameplay scene you can find, and the darkest. Capture at native resolution without scaling.
4. **Measure.** For at least eight text or HUD elements across those screenshots, pick the text colour and the background pixel with the least contrast directly behind the text (the lightest pixel for light text, the darkest for dark text). Add each to a CSV and run `contrast.py`. Measure text height in pixels as XAG 101 describes (top of the tallest ascender to the bottom of the lowest descender) for at least three text styles.
5. **Audit.** Fill in the audit sheet for all in-scope items, with evidence for each result.
6. **Colour check.** For one colour-coded element (team colours, rarity colours, map markers), compute the luminance contrast between the colours that must be told apart. If it is below 3:1, check whether a second channel (shape, icon, text) carries the same information.
7. **Rank.** Rank the failures by players affected × severity, then note cost. Pick the top three fixes.
8. **Reflect.** In one paragraph, name one thing the guidelines missed that a player with a disability might still hit in this game, and how you would find out ([week 8](../lectures/w08-usability-testing-methods.md) testing with players).

## Deliverable

A PDF with a memo of at most two pages plus appendices.

- The game, platform, version and test date.
- The completed audit sheet.
- The `contrast.py` output for your measurements, with the worst case highlighted and the needed subtitle box opacity for it.
- The top three fixes, each with who it helps, how you would verify it, and its rough cost.
- The reflection paragraph.
- Appendices: annotated screenshots, your CSV.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Scoping and audit | All twelve items scoped with reasons, results backed by evidence | Most items, some evidence missing | Results asserted without evidence | 25% |
| Measurement | At least eight contrast measurements on true worst-case backgrounds, text heights measured, script output correct | Fewer measurements or average backgrounds used | No measurements | 25% |
| Colour analysis | Luminance contrast computed, second channel checked, clear verdict | Computed without the channel check | Missing | 15% |
| Ranking and fixes | Ranking uses reach, severity and cost; fixes specific and verifiable | Reasonable ranking, vague fixes | Unranked list | 25% |
| Writing | Numbers first, plain, within length | Readable, some padding | Hard to follow | 10% |
