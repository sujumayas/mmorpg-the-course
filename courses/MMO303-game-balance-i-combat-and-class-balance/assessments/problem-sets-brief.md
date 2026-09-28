# MMO303 · Problem sets brief

**Weight:** 30% of the course grade.
**Work mode:** individual write-up. You may discuss methods with classmates, but every number and sentence you submit must come from your own sheet or code.
**Due:** before the next week's lecture, unless the lab says otherwise.

## What a problem set is

A problem set is one week's lab plus two or three short questions drawn from the course question bank. The lab is where you build a tool. The questions check that you can use the week's model on numbers you have not seen, without the tool doing the thinking.

Eleven labs count as problem sets. The other three labs belong to the larger assessments.

| Week | Problem set | Lab | Added questions (bank numbers, issued with new numbers) |
|---|---|---|---|
| 1 | PS1 | [Lab 01: Reading a balance dashboard](../labs/lab01.md) | 1, 2, 4 |
| 2 | PS2 | [Lab 02: Mitigation spreadsheet](../labs/lab02.md) | 5, 7, 9 |
| 3 | PS3 | [Lab 03: EHP / eDPS calculator and TTK matrix](../labs/lab03.md) | 10, 12, 14 |
| 4 | PS4 | [Lab 04: Mitigation stack audit](../labs/lab04.md) | 16, 17, 19 |
| 5 | PS5 | [Lab 05: Composition solver](../labs/lab05.md) | 21, 23 |
| 6 | PS6 | [Lab 06: Threat budget simulator](../labs/lab06.md) | 26, 29 |
| 7 | PS7 | [Lab 07: Healer mana budget](../labs/lab07.md) | 31, 32, 34 |
| 8 | PS8 | [Lab 08: Chain CC planner](../labs/lab08.md) | 35, 37, 38 |
| 9 | PS9 | [Lab 09: Patch the triangle](../labs/lab09.md) | 40, 41 |
| 10 | PS10 | [Lab 10: Solving a class meta](../labs/lab10.md) | 44, 46, 48 |
| 12 | PS11 | [Lab 12: Measuring stat weights](../labs/lab12.md) | 54, 56, 59 |

Lab 11 and Lab 13 are milestones of the [simulator project](simulator-brief.md). Lab 14 is a milestone of the [final balance pass](final-balance-pass-brief.md).

## Deliverables for each set

1. **The lab deliverable,** exactly as the lab specifies (sheet or code, memo or report, tests where asked).
2. **Question answers,** one page at most, in a separate file or the last page of the memo. For each question, show the model you used, the substitution with units, the result, and one sentence that says what the number means for a designer.
3. **A reproducibility line.** For any simulated number, the seed and command that produced it. For spreadsheets, confirm that every result cell is a formula.

## Milestones and feedback

| When | What happens |
|---|---|
| Each week, before lecture | Problem set due on the course site. |
| Within one week of the deadline | Marked rubric returned, with the correct values for every question. |
| After PS5 (week 6) | Mid-semester check. Any student averaging under 50 meets the instructor to review the week 2 to 5 models before threat and healing build on them. |
| Week 13 | Last problem set returned. Your Lab 03 calculator and Lab 05 solver should be in shape to reuse in the simulator and the final pass. |

## How a set is scored

Each problem set is scored out of 100.

- **80 points** come from the lab's own rubric, scaled from its weights or points to 80.
- **20 points** come from the added questions, marked with the table below. With three questions, each is worth about 6.7 points. With two, each is worth 10.

Your problem-set grade is the average of your best 10 of the 11 sets. The dropped set covers one bad week. Missing sets count as 0 before the drop.

## Rubric

The lab portion uses the rubric printed in each lab. The table below marks the added questions and sets the overall bands for a whole problem set.

**Added questions (per question, scaled to its share of the 20 points)**

| Criterion | Share | Full | Partial | Little | None |
|---|---|---|---|---|---|
| Model choice | 40% | 36-40%: the right lecture model, stated once with every symbol named | 20-35%: right model with one symbol misread (for example, shares instead of square roots, or points instead of relative percent) | 5-19%: a related model that answers a different question | 0-4%: no model, or a guess |
| Substitution and arithmetic | 35% | 31-35%: every step shown, units kept, result correct to the lecture's rounding | 18-30%: one arithmetic slip that does not change the conclusion | 5-17%: slips that change the conclusion, or steps missing | 0-4%: number only, or wrong |
| Interpretation | 25% | 22-25%: one sentence that names the design consequence with a number ("the Knight's share falls to 22%") | 12-21%: correct direction, no number | 3-11%: restates the result | 0-2%: missing |

**Overall bands for a problem set (out of 100)**

| Band | Points | What it looks like |
|---|---|---|
| Excellent | 85-100 | Tool reproduces every lecture test value. Every number traces to a formula or a seeded run. Memo argues from its own numbers. Questions correct with a design sentence each. |
| Good | 70-84 | Tool correct on most tests, one quantity off or unexplained. Questions correct in method with one slip. |
| Satisfactory | 55-69 | Tool runs but typed values or missing tests weaken it. One question uses the wrong model. Memo is partly opinion. |
| Weak | 40-54 | Several lecture test values not reproduced. Questions answered by number only. |
| Fail | 0-39 | Deliverable missing or not the week's model. |

## Rules

- **Late work** loses 10 points per day, up to three days. After three days the set scores 0 and counts toward the dropped set.
- **Spreadsheets** must be formula-driven. A typed value where a formula belongs costs the lab's structure criterion.
- **Code** must run from a clean checkout with the command in your README.
- **Real-game numbers** in memos must come from a lecture's Sources or be cited with the patch or era you used.
