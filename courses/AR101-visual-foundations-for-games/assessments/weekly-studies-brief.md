# AR101 · Weekly studies brief

**Weight:** 50% of the course grade.
**Assigned:** week 1. **Due:** each study at the start of the next week's studio. **Studies portfolio:** start of week 15.
**Work mode:** individual. Lab 12 is done in pairs; each partner hands in the shared tool and CSVs plus their own mockups and rationale.
**Lectures:** weeks 1 to 12, from [value before color](../lectures/w01-seeing-like-an-artist-value-before-color.md) to [color-blindness and contrast](../lectures/w12-accessibility-color-blindness-and-contrast.md).
**Labs that feed it:** [01](../labs/lab01.md) to [12](../labs/lab12.md).

## What this component is for

The first two course outcomes are practice outcomes. You apply value, color and shape to communicate gameplay, and you produce readable sprites and tiles at small sizes. You get there by making a small piece of art every week and proving with a number that it does its job. A study earns marks for the art and for the evidence together. A lovely sprite with no ΔV table earns less than a plain one whose outline is measured against every floor it will stand on.

The labs 13 and 14 outputs belong to the [style bible](style-bible-brief.md) and the [final piece](final-piece-brief.md), not to this component.

## What counts

The weekly studies are labs 01 to 12. Your **best 10 of 12** study scores count, at equal weight. The two dropped studies cover illness, a bad week or a study you started late. You do not need to apply for them.

| Study | Week | Topic | Automatic check you must reach | Reused in |
|---|---|---|---|---|
| [Lab 01](../labs/lab01.md) | 1 | The value checker | tests pass; every own pair ΔV ≥ 20 | Style bible (value chapter) |
| [Lab 02](../labs/lab02.md) | 2 | The shape cast | helper reruns to your table | Final piece (characters) |
| [Lab 03](../labs/lab03.md) | 3 | The silhouette test as a program | tests pass; every pair ≤ 0.75 at both sizes | Style bible (silhouette chapter), final piece |
| [Lab 04](../labs/lab04.md) | 4 | The palette swapper | `all tests pass` | Lab 05 |
| [Lab 05](../labs/lab05.md) | 5 | A zone palette | `all tests pass`; `zone.hex` checker `PASS` | Lab 06, style bible, final piece |
| [Lab 06](../labs/lab06.md) | 6 | A readable sprite | sprite checker `PASS` | Final piece |
| [Lab 07](../labs/lab07.md) | 7 | Autotiler and seamless tile | 8 of 8 tests; seam ratio ≤ 1.5 | Final piece (tileset) |
| [Lab 08](../labs/lab08.md) | 8 | One set of drawings, two weights | `ALL RULES PASS` | Final piece (animation) |
| [Lab 09](../labs/lab09.md) | 9 | Composing for the first look | three `PASS` reports at 8 by 5 | Final piece (composed screen) |
| [Lab 10](../labs/lab10.md) | 10 | The chaos plate test | probe ≥ 20 on all four plates | Final piece (telegraph) |
| [Lab 11](../labs/lab11.md) | 11 | The hierarchy audit | 6 of 6 tests; zero inversions on the redesign | Final piece (UI element) |
| [Lab 12](../labs/lab12.md) | 12 | The color-blind audit | 6 of 6 tests; every value pair ΔV ≥ 20 in four modes | Style bible (accessibility chapter) |

A study's mark and the later mark for the work that reuses it are separate. You earn the study mark for the study, and the bible or final piece mark for how well the work fits there.

Dropping a study removes its score, not its output. If you drop lab 03, 05 or 12, you still need a silhouette table, a zone palette and an accessibility audit for the style bible.

## How a study is scored

Every lab sheet has its own rubric. Labs 01 to 09 score each criterion on 0 to 4 with a weight in percent:

```
study score = sum over criteria of (points / 4) × weight
```

Labs 10 to 14 give each criterion full, half or no points out of a stated total of 100. Either way the study score is out of 100.

For example, lab 06 with 4 on checker rules (20%), 3 on readability (25%), 4 on pixel craft (20%), 2 on light and color (20%) and 3 on the review sheet (15%) scores `20 + 18.75 + 20 + 10 + 11.25 = 80`.

Your tutor reruns every checker and test file on what you submitted. The number that counts is the one the tutor sees, not a pasted screenshot.

## Deliverables and milestones

| When | What |
|---|---|
| Each week, in the 2-hour studio | Work through the lab sheet with a tutor in the room. From week 2, the first 10 minutes are a short quiz drawn from the [exam bank](exam-bank.md) for the week just taught. The quiz is feedback only. |
| Start of the next week's studio | Submit the study as the lab sheet's deliverable asks, zipped, on the course page. Add a `SOURCES.md` (see below). |
| Weeks 4, 8 and 12 | Checkpoint. Your tutor returns your running mean and flags any study whose checker still fails, so you can fix it before the drop rule has to cover it. |
| Start of week 15 | Submit the studies portfolio described below. |

### The studies portfolio (week 15)

One PDF of at most 16 pages that shows the semester's studies as a body of work.

1. **Index page.** One row per study: title, the one image that best shows it, and the one number that proves it works (the smallest ΔV, the worst IoU, the seam ratio, `H`, the worst telegraph contrast, the inversion count).
2. **One page per study you are proud of,** at least six. The image at game scale and at 4× nearest-neighbour, its proving number, and two sentences on what you learned that you did not know before.
3. **Two revised studies.** Pick two studies where you now see a problem. Redo the weak part, rerun the checker, and show before and after side by side with both numbers. Revisions may come from dropped studies.
4. **Process record.** A short list, one line per study, of the iterations you kept (version numbers, what changed, why). Most of this already exists in your lab notes and reports.

## Original work and references

Every image you submit must be your own work. This is a gate. A study that breaks it is not marked until it is fixed, and work presented as yours when it is not is handled under the university's academic integrity policy.

- **Allowed.** Your own drawings, pixel art, paintings, renders and photographs. Shapes and palettes built from the lecture models. Palettes from Lospec or similar sites when a lab asks for them or the palette's page gives permission, credited by name and author.
- **Allowed as reference, with a record.** Screenshots of games you are analysing (labs 09 to 12 ask for some) and photographs or art you study for shape, value or color. List each one in `SOURCES.md` with its game or author, the version or date, and what you used it for. Reference images are for looking at. They may appear in a study only where the lab asks you to audit a shipped screen, labelled as the game's, never as your work.
- **Not allowed.** Tracing, painting over or copying the pixels of copyrighted art, including game sprites, characters, logos and screenshots. Existing game characters redrawn as your design. Output from image-generation tools in place of your drawing. Assets from packs or stores, unless the lab explicitly allows them and their licence permits submission for marking.

Ask before the deadline if you are unsure, not after.

## Late work

A study submitted up to 48 hours late is marked out of 80. After 48 hours it is marked for feedback only and counts as 0, which usually makes it one of your two drops. The studies portfolio is accepted up to 48 hours late with 10 points lost from its 20. Extensions for illness or other documented reasons follow the university policy and do not use up a drop.

## Rubric (component, out of 100)

| Criterion | Excellent | Adequate | Weak or missing | Points |
|---|---|---|---|---|
| Study scores | Mean of your best 10 study scores, scaled: `mean × 0.80`. A mean of 85 earns 68. | | | 80 |
| Two revised studies | Both revisions fix a real, named problem; before and after numbers from a rerun checker; the change is visible at game scale (9 to 10) | One strong revision, or two with thin evidence (5 to 8) | Cosmetic changes, no numbers, or missing (0 to 4) | 10 |
| Portfolio index and pages | Every study indexed with its image and proving number; the chosen pages show art at game scale and at 4×; the learning notes name a model or number (5 to 6) | Index complete, pages thin or numbers missing (3 to 4) | Index incomplete or pages missing (0 to 2) | 6 |
| Process record | Iterations listed for every study, each change tied to a number or a test result (4) | Iterations listed without reasons (2 to 3) | Missing (0 to 1) | 4 |
| **Total** | | | | **100** |
