# MMO304 · Models assignment brief

**Weight:** 30% of the course grade.
**Work mode:** individual write-up. You may discuss methods with classmates, but every number and sentence you submit must come from your own sheet or code.
**Due:** before the next week's lecture, unless the lab says otherwise.

## What the Models assignment is

Each week from 1 to 10, and again in week 13, you build one model of an economy in a lab: a price in hours, a stock-and-flow simulator, a supply and demand fit, a crafting bill of materials. The Models assignment is those labs, plus two or three short questions per lab that check you can use the model on numbers you have not seen, without the tool doing the thinking.

Ten labs count toward this assignment. Each one is a **model set**.

| Week | Set | Lab | Added questions (bank numbers, issued with new numbers) |
|---|---|---|---|
| 1 | MS1 | [Lab 01: Pricing scarcity in hours](../labs/lab01.md) | 1, 2, 4 |
| 2 | MS2 | [Lab 02: Pricing the three kinds of value](../labs/lab02.md) | 5, 6, 8 |
| 3 | MS3 | [Lab 03: Build the faucet/sink simulator](../labs/lab03.md) | 10, 12, 13 |
| 4 | MS4 | [Lab 04: The real value of every gold number](../labs/lab04.md) | 15, 16, 19 |
| 5 | MS5 | [Lab 05: Sink targeting](../labs/lab05.md) | 20, 21, 23 |
| 6 | MS6 | [Lab 06: Estimating a market from auction data](../labs/lab06.md) | 24, 27, 28 |
| 7 | MS7 | [Lab 07: Crafting chain workbook](../labs/lab07.md) | 29, 30, 33 |
| 8-9 | MS8 | [Lab 08: Item lifecycle simulation](../labs/lab08.md), parts A to C in week 8 and part D (the money item) in week 9 | 34, 35, 39 |
| 10 | MS9 | [Lab 10: Search cost and market design](../labs/lab10.md) | 43, 44, 46 |
| 13 | MS10 | [Lab 13: Market reach and the upgrade drought](../labs/lab13.md) | 57, 58, 61 |

Lab 12 is the [telemetry lab](telemetry-lab-brief.md), graded on its own (20%). Lab 14 is a milestone of the [final economy spec](final-spec-brief.md). Week 11 has no lab. Its models return in the RMT section of the final spec.

The question numbers refer to the course [question bank](exam-bank.md). You receive each question with its numbers changed. The bank stays on the instructor side.

## Deliverables for each set

1. **The lab deliverable,** exactly as the lab specifies: sheet or script, plots, and the memo or note.
2. **Question answers,** one page at most, in a separate file or as the last page of the memo. For each question, name the model you used with every symbol defined once, show the substitution with units, give the result, and write one sentence that says what the number means for a designer.
3. **A reproducibility line.** For any simulated number, the seed and the command or sheet that produced it. For spreadsheets, confirm that every result cell is a formula.

## Milestones and feedback

| When | What happens |
|---|---|
| Each week, before lecture | Model set due on the course site. |
| Within one week of the deadline | Marked rubric returned, with the correct value for every added question. |
| After MS5 (week 6) | Mid-semester check. Any student averaging under 50 meets the instructor to review the week 3 to 5 money models before markets and crafting build on them. |
| Week 10 | MS9 returned. Your Lab 03 simulator, Lab 07 workbook and Lab 08 lifecycle sheet should be in shape to reuse in the final spec. |
| Week 14 | MS10 returned. The Lab 13 memo becomes the market section of your final spec, so fix anything the marker flags. |

## How a set is scored

Each model set is scored out of 100.

- **80 points** come from the lab's own rubric. Labs with percentage weights are scaled to 80. Lab 13 is marked out of 20 points and multiplied by 4.
- **20 points** come from the added questions, marked with the table below. With three questions, each is worth about 6.7 points.

Your Models grade is the average of your best 9 of the 10 sets. The dropped set covers one bad week. Missing sets count as 0 before the drop.

## Rubric

The lab portion uses the rubric printed in each lab. The first table marks each added question. The second sets the overall bands for a whole set.

**Added questions (per question, scaled to its share of the 20 points)**

| Criterion | Share | Full | Partial | Little | None |
|---|---|---|---|---|---|
| Model choice | 40% | 36-40%: the right lecture model, stated once with every symbol named | 20-35%: right model with one symbol misread (for example, `c + τv` written as `c × τv`, or daily and weekly rates mixed) | 5-19%: a related model that answers a different question (for example, total `M` where money per player was needed) | 0-4%: no model, or a guess |
| Substitution and arithmetic | 35% | 31-35%: every step shown, units kept, result correct to the lecture's rounding | 18-30%: one arithmetic slip that does not change the conclusion | 5-17%: slips that change the conclusion, or steps missing | 0-4%: number only, or wrong |
| Interpretation | 25% | 22-25%: one sentence that names the design consequence with a number ("newcomers lose 60% of their savings") | 12-21%: correct direction, no number | 3-11%: restates the result | 0-2%: missing |

**Overall bands for a model set (out of 100)**

| Band | Points | What it looks like |
|---|---|---|
| Excellent | 85-100 | Sheet or script reproduces every lecture test value and every check value the lab names. Every number traces to a formula or a seeded run. The memo argues from its own numbers and names who pays. Questions correct, each with a design sentence. |
| Good | 70-84 | Model correct on most checks, one quantity off or unexplained. Questions correct in method with one slip. Memo uses numbers but misses one trade-off. |
| Satisfactory | 55-69 | Model runs, but typed values or missing checks weaken it. One question uses the wrong model. Memo is partly opinion. |
| Weak | 40-54 | Several lecture tables not reproduced. Questions answered by number only. |
| Fail | 0-39 | Deliverable missing or not the week's model. |

## Rules

- **Late work** loses 10 points per day, up to three days. After three days the set scores 0 and counts toward the dropped set.
- **Spreadsheets** must be formula-driven. A typed value where a formula belongs costs the lab's model-correctness criterion.
- **Code** must run from a clean folder with the command in your README, using `.venv/bin/python` or plain Python 3 as the lab states.
- **Real-game numbers** in memos must come from a lecture's Sources, cited with the patch or era the lecture gives. If you use a number from elsewhere, cite it with its version and date.
