# AR101 · Style bible brief

**Weight:** 20% of the course grade.
**Assigned:** week 13. **Milestone 1:** start of week 14 ([lab 13](../labs/lab13.md), version 0.2). **Milestone 2:** start of week 15 ([lab 14](../labs/lab14.md), pipeline chapter). **Final submission:** end of week 15, version 1.0.
**Work mode:** individual. The stranger tests need a partner from another group, but the bible is yours.
**Lectures:** [week 13, art style bibles](../lectures/w13-art-style-bibles.md) and [week 14, pipeline](../lectures/w14-pipeline-export-atlases-import-settings.md), drawing on the models of weeks [1](../lectures/w01-seeing-like-an-artist-value-before-color.md), [2](../lectures/w02-shape-language-circles-squares-triangles.md), [3](../lectures/w03-silhouette-readability.md), [5](../lectures/w05-palettes-and-color-harmony.md), [6](../lectures/w06-pixel-art-fundamentals.md), [10](../lectures/w10-readability-in-chaos-vfx-and-telegraphing.md), [11](../lectures/w11-ui-visual-hierarchy.md) and [12](../lectures/w12-accessibility-color-blindness-and-contrast.md).
**Labs that feed it:** [01](../labs/lab01.md), [03](../labs/lab03.md), [05](../labs/lab05.md), [12](../labs/lab12.md), [13](../labs/lab13.md) and [14](../labs/lab14.md).

## What this component is for

A style bible lets someone who never talked to you make an asset that fits your game. The lecture calls that the stranger test, and it is how this component is judged. Your bible is for one zone of an invented MMO, the same zone as your [final piece](final-piece-brief.md). By week 15 it should read like a document a real team could hand to an outsourcing studio. Keep it short and checkable, with every rule saying what to measure, what number is allowed and how a reviewer checks it.

Most of the numbers already exist. Lab 01 gave you a value checker, lab 03 a silhouette matrix, lab 05 a zone palette, lab 12 a color-blind audit, lab 13 a density table and lab 14 an atlas report. The bible turns them into rules and decides which rules are hard.

## Your zone

Keep the zone you chose in lab 13 (Saltmarsh Reach, Cinder Terraces, The Lantern Archive, or your approved proposal). If you want to change zone after milestone 1, ask your tutor in week 14. A change means redoing the density table and the palette, so it rarely pays.

## What the bible contains

Version 1.0 is one PDF of at most 12 pages including images, plus the palette file and the scripts or reports that back its numbers. Use these chapters, in this order. Chapters may be short; none may be missing.

1. **Cover and changelog.** Zone name, version, date, and every change since 0.1 with the rule number it touches.
2. **Pillars.** Three to five pillars written as "X, not Y", each with one asset it would reject.
3. **Shape language and proportions.** Which shape family belongs to which faction or role (week 2), head-to-body proportions, the allowed range of the sharpest outward corner for friendly and hostile designs.
4. **Silhouette.** The character roster as a black-fill lineup at the smallest size players see it, the IoU matrix from your lab 03 tool at full and gameplay size, the pass rule, and the class-defining zone that cosmetics may not cover.
5. **Value and color.** Value bands in L* for background, characters and gameplay signals; the palette as swatches and a `.hex` file; the reserved gameplay color or colors with their minimum ΔV against every ground in the zone; the lab 01 pair table for the zone's critical pairs.
6. **Lighting and rendering.** Light direction, the shadow hue rule (week 5), outline or no outline and its minimum ΔV against the grounds.
7. **Effects and telegraphs.** The value band reserved for danger, the two-tone rule with its `t` and `α` and computed worst case, and the rule that tags every effect as signal or noise (week 10).
8. **Accessibility.** The lab 12 audit of every critical pair on at least two grounds in all four viewing modes, and the redundant shape or pattern code for every pair that relies on hue.
9. **UI hierarchy.** The number of levels, the weight step, and one worked label or tooltip showing zero inversions (week 11).
10. **Pixel and detail rules.** Allowed line slopes, orphan limits, the smallest detail that reads (week 6), texel density or pixels per unit with tolerance (week 13).
11. **Technical and pipeline.** Your lab 14 chapter, updated: import settings table per asset group, gutter and cell rule, transparent-pixel rule, naming pattern, color-space list, and a memory budget with the atlas sizes that meet it.
12. **Examples.** At least three approved and three rejected assets, each rejection naming the rule number it breaks.

### Rules

- At least 15 rules in the rule table from lab 13, covering at least seven of the chapters above.
- At least 8 rules with a numeric target. At least one each for value (ΔV), silhouette (IoU), density (`D` or pixels per unit), accessibility (ΔV in all four modes or 3:1 contrast) and pipeline (gutter or memory).
- Every rule has the four parts from the lecture (property, target, tolerance and scope, method), a hard or soft label, and a one-line reason.
- Gameplay rules (team and faction colors, silhouettes, telegraph colors, reserved hues) are hard unless you argue otherwise in writing.
- Every recorded exception gives the value it uses and the reason, the way Shovel Knight's team recorded its added colors.

### Second stranger test

Run the stranger test from lab 13 a second time on version 0.3 (version 0.2 plus your pipeline chapter), in the week 15 studio. Use a different stranger from round 1 and a different asset row. Audit their asset rule by rule on the audit sheet before you view it in the lineup, then revise. The changelog from 0.3 to 1.0 must have at least three entries, each pointing to a finding.

## Original work and references

The bible's images are your own work: your assets, your lineups, your diagrams, your charts. Name games in text as references (as the lectures do with Team Fortress 2 or Shovel Knight), but do not put game screenshots, characters or logos in the bible. Palettes from Lospec or similar sites may seed your zone palette if credited by name and author. Tracing or painting over copyrighted art, and image-generation output in place of your own drawing, are not allowed. List every outside source in a `SOURCES.md` next to the PDF. The full rules are in the [weekly studies brief](weekly-studies-brief.md#original-work-and-references).

## Deliverables

- `bible_v1.0.pdf`, at most 12 pages.
- `zone.hex`, the palette the bible defines, passing the lab 05 checker.
- `evidence/`: the reports your numbers come from (lab 01 pair report, lab 03 matrix, lab 12 audit before and after, density table script output, lab 14 atlas report), each named after the chapter it supports.
- `stranger_test_2/`: the stranger's asset, your completed audit sheet and the lineup with their asset in it.
- `SOURCES.md`.

## Milestones

| When | What | Points |
|---|---|---|
| Start of week 14 | Milestone 1: lab 13 deliverable (version 0.2, density table, three assets, first stranger test, changelog 0.1 to 0.2). Marked with lab 13's rubric for feedback; the points here are for a complete, on-time submission. | 5 |
| Start of week 15 | Milestone 2: lab 14 deliverable, including the pipeline chapter. Marked with lab 14's rubric for feedback; the points here are for a complete, on-time submission. | 5 |
| Week 15 studio | Second stranger test on version 0.3. | in the rubric below |
| End of week 15 | Version 1.0 and all deliverables. | 90 |

Your final piece is judged against version 0.3, the bible as it stood when you built the piece. Changes you make to the bible after the week 15 crit are welcome and belong in the changelog, but they do not change how the piece is marked.

## Late work

Milestones submitted up to 48 hours late earn half their points; after that they earn none but still get feedback. Version 1.0 submitted up to 48 hours late loses 10 points. After 48 hours it is marked for feedback only and scores 0. Extensions for illness or other documented reasons follow the university policy.

## Rubric (out of 100)

| Criterion | Excellent | Adequate | Weak or missing | Points |
|---|---|---|---|---|
| Milestones | Both milestones complete and on time (10) | One milestone late or incomplete (5) | Neither submitted (0) | 10 |
| Pillars and scope | Three to five "X, not Y" pillars, each with a rejected asset; zone and asset types clearly scoped (7 to 8) | Pillars present, some without a rejection or too vague to rule anything out (4 to 6) | Mood words only (0 to 3) | 8 |
| Checkable rules | 15 or more rules; every rule has property, target, scope, method, hard or soft label and reason; at least 8 numeric, covering the five required areas (17 to 20) | 15 rules with some parts missing, or fewer numeric rules than required (9 to 16) | Fewer than 10 rules, or mostly unmeasurable (0 to 8) | 20 |
| Evidence for readability rules | Value, silhouette and accessibility chapters each backed by a report in `evidence/` that a reviewer can rerun; critical pairs pass on at least two grounds in all four modes; exceptions shape-coded and listed (17 to 20) | Reports present with gaps, or one chapter asserted without numbers (9 to 16) | Numbers missing or not reproducible (0 to 8) | 20 |
| Technical and pipeline chapter | Density table recomputes from its columns; import settings per asset group; gutter and cell rule tied to a safe mip level; memory budget met with named atlas sizes; naming, transparency and color-space rules each with a test (13 to 15) | Chapter present, one area missing or untested (7 to 12) | Missing or copied from the lecture without adaptation (0 to 6) | 15 |
| Examples | Three or more approved and three or more rejected assets, each rejection naming its rule number, shown in a lineup at game scale (8 to 10) | Examples present, reasons vague (4 to 7) | Fewer than two each (0 to 3) | 10 |
| Second stranger test and revision | Different stranger and asset row; audit done before the lineup; three or more changelog entries fixing real defects found (10 to 12) | Test done, findings or fixes thin (5 to 9) | Not done (0 to 4) | 12 |
| Clarity and layout | A reader finds any rule by number in under a minute; at most 12 pages; images labelled; no rule contradicts another (5) | Findable with effort, or over length (2 to 4) | Hard to navigate (0 to 1) | 5 |
| **Total** | | | | **100** |
