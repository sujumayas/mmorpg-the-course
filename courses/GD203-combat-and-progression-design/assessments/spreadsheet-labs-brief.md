# GD203 · Spreadsheet labs brief

**Weight:** 40% of the course grade.
**Covers:** the weekly spreadsheet labs in weeks 1 to 11, 13 and 14.
**Related briefs:** [simulation-brief.md](simulation-brief.md) (lab 12 counts there, not here) and [final-spec-brief.md](final-spec-brief.md) (labs 11 and 14 feed it directly).

## What this component is for

Every model in GD203 ends up as a spreadsheet. The labs are where you build those sheets one week at a time, so that by week 15 you own a working balance workbook for a small RPG. This component grades how well you build them. The questions it asks are practical. Does every number trace to one input? Do your check values match? Did you run the experiment the lab asked for and say what it showed?

## Which labs count

Thirteen labs count toward this component. Lab 12, the duel simulator, is part A of the simulation assessment and is graded there.

| Lab | Topic | Assigned | Due | Builds on | Can be dropped? |
|---|---|---|---|---|---|
| [01](../labs/lab01.md) | Stat sheet in a spreadsheet | Week 1 | Start of week 2 | — | Yes |
| [02](../labs/lab02.md) | Three damage formulas in one sheet | Week 2 | Start of week 3 | — | Yes |
| [03](../labs/lab03.md) | Effective HP and the defensive budget | Week 3 | Start of week 4 | Lab 02 | Yes |
| [04](../labs/lab04.md) | The breakpoint table | Week 4 | Start of week 5 | — | Yes |
| [05](../labs/lab05.md) | Burst, sustain and the crossover | Week 5 | Start of week 6 | Lab 04 | Yes |
| [06](../labs/lab06.md) | Crits, breakpoints and Monte Carlo | Week 6 | Start of week 7 | Lab 04 | Yes |
| [07](../labs/lab07.md) | XP curve and 40-hour pacing sheet | Week 7 | Start of week 8 | — | Yes |
| [08](../labs/lab08.md) | Power curves and scaling bands | Week 8 | Start of week 9 | Lab 07 | Yes |
| [09](../labs/lab09.md) | Item budget audit | Week 9 | Start of week 10 | — | Yes |
| [10](../labs/lab10.md) | Enemy roster from player units | Week 10 | Start of week 11 | — | Yes |
| [11](../labs/lab11.md) | The level-sweep balance sheet | Week 11 | Start of week 12 | Lab 10 | **No** |
| [13](../labs/lab13.md) | Difficulty ladder | Week 13 | Start of week 14 | Lab 04 or 10 (optional) | Yes |
| [14](../labs/lab14.md) | Progression audit | Week 14 | With the final spec, week 15 | — | **No** |

"Start of week N" means before the first class session of that week.

## How the grade is computed

1. Each lab is marked out of 100 with the rubric printed in that lab.
2. Labs 10, 11, 13 and 14 use four bands with percentage weights. Convert each criterion as `weight × band points / 4`, where Excellent is 4, Good 3, Needs work 2 and Missing 0 or 1. For example, a Good on a 25% criterion scores `25 × 3/4 = 18.75`.
3. Your two lowest lab scores are dropped, except labs 11 and 14. Those two are the spine of your final spec and always count.
4. The 11 remaining labs are averaged with equal weight. That average is worth 40% of the course grade, so each counted lab is worth about 3.6%.

A missing lab scores 0 and is a candidate for dropping like any other score.

## What to submit each week

- The spreadsheet file, or a view link that stays live until grades are released. Sheets that need a login to open are not marked.
- The memo or design note the lab asks for, as a PDF or inside the sheet on a tab named `Memo`. Word counts are targets. Anything within 20% either way is fine. Going far over usually means the memo restates the lab instead of making a decision.
- Any chart or drawing the lab names, embedded in the sheet or attached as an image.

Work alone on the sheet and the memo. You may discuss methods with classmates, and you should, but the cells and the words are yours.

## Rules that apply to every lab

These are the habits the lectures teach. Markers look for them in every lab, whatever that lab's rubric calls the criterion.

- **Inputs are separate.** Every constant lives on an `Inputs` tab (or the lab's named equivalent) with a label and a unit. No number other than 0 and 1 is typed into a formula elsewhere.
- **Check values match.** Each lab prints check values. Reproduce them before you run the experiments. If yours differ, say so in the memo and say which you trust and why. An honest mismatch loses fewer points than a silent one.
- **Charts show what the player feels.** Plot hits, seconds, shares of health, hours, ratios. Raw stats alone earn little.
- **Memos make decisions.** Each memo recommends something and backs each claim with a number from your sheet.

## Spot checks

Twice during the semester, in a lab session, a marker opens one of your submitted sheets with you for five minutes. They change one input and ask you to predict which way two outputs will move before the sheet recalculates. They may also ask one question in the style of the [exam bank](exam-bank.md), using a number from your sheet.

A spot check is not graded on its own. If you cannot explain how a number in your own sheet was produced, that lab is capped at 60 until you can. You may book a second attempt within a week.

## Late work and extensions

- You have two free 48-hour extensions for the semester. Tell the course team before the deadline. No reason needed.
- Beyond that, late work loses 10 points per 24 hours, up to 72 hours.
- After 72 hours the course team releases a reference sheet for labs that others build on (02, 04 and 07), so late submissions for those labs are not accepted after the release. Using a reference sheet as the starting point for the next lab costs nothing on that next lab.
- Lab 10 is the exception. Its [reference sheet](../labs/lab10-reference.md) comes out at the start of week 11, when lab 10 is due, so that everyone can start lab 11 on time. Lab 10 therefore cannot be submitted late or use a free extension.
- Lab 14 is due with the final spec and cannot use a free extension, because the final deadline is fixed.

## Rubric

Each lab's own rubric sets its criteria and weights, and it wins where the two differ. This common rubric is the band guide markers use to keep grades consistent across the 13 labs. The criteria map onto every lab's rubric rows.

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Sheet structure and traceability | 20 | 18-20: inputs isolated and named, no typed constants in formulas, tabs as the lab specifies | 14-17: one or two typed constants, labels mostly clear | 10-13: several typed constants, or inputs spread across tabs | 0-9: numbers typed into formulas throughout, or one tab doing everything |
| Correctness against check values | 30 | 27-30: every check value matches, edge cases handled (off-by-one, `ceil` guard, caps, `g = 1`) | 21-26: one error that propagates, otherwise correct | 15-20: several errors, or check values not attempted | 0-14: core tables wrong or missing |
| Experiments and analysis | 20 | 18-20: every experiment in the lab run, results tabulated, cause of each result stated | 14-17: all run, one explanation thin | 10-13: some experiments missing | 0-9: experiments skipped |
| Charts | 10 | 9-10: required charts present, labelled, on the right axes (log where growth is exponential), target bands drawn | 7-8: present, one missing a label or band | 5-6: some charts missing | 0-4: no charts |
| Memo or design note | 20 | 18-20: a clear decision, every claim backed by a number from the sheet, trade-off named | 14-17: decision with some unsupported claims | 10-13: decision stated with few numbers | 0-9: restates the lab, no decision |

Total: 100 points per lab.
