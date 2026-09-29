# MMO403 · Models brief

**Weight:** 40% of the course grade.
**Work mode:** as each lab states (individual or pairs). The two added questions in every set are always answered individually.
**Due:** before the lecture of the week after each lab, unless the lab says otherwise.

## What the models strand is

Most weeks of MMO403 end with a model you can run: contribution by business model, an LTV curve, a cheapest-cover solver, a battle pass finish line, a Lorenz curve, a price test, a token's revenue, a store's take, a burn plan, a stage gate. The models strand is those labs, plus two short questions per lab that check you can use the model on numbers you have not seen, without the code doing the thinking.

Ten labs count toward it. Each one is a **model set**.

| Week | Set | Lab | What counts | Added questions (bank numbers, issued with new numbers) |
|---|---|---|---|---|
| 1 | MS1 | [Lab 01: Business model race](../labs/lab01.md) | Whole lab | 1, 2 |
| 2 | MS2 | [Lab 02: LTV curve and payback](../labs/lab02.md) | Whole lab | 5, 7 |
| 3 | MS3 | [Lab 03: Premium currency store audit](../labs/lab03.md) | Solver, real-store audit, redesign, presentation | 9, 11 |
| 5 | MS4 | [Lab 05: Tune a battle pass](../labs/lab05.md) | Whole lab | 18, 19 |
| 9 | MS5 | [Lab 09: The spending curve of a live game](../labs/lab09.md) | Whole lab | 37, 39 |
| 10 | MS6 | [Lab 10: Reading a three-arm price test](../labs/lab10.md) | Whole lab | 42, 43 |
| 11 | MS7 | [Lab 11: A token for a subscription MMO](../labs/lab11.md) | Whole lab | 46, 47 |
| 12 | MS8 | [Lab 12: The revenue waterfall](../labs/lab12.md) | Whole lab | 51, 52 |
| 13 | MS9 | [Lab 13: Phase budget and slip analysis](../labs/lab13.md) | Parts A and B | 55, 57 |
| 14 | MS10 | [Lab 14: Stage-gate funding plan and pitch](../labs/lab14.md) | Parts A and B | 59, 60 |

The question numbers refer to the course [exam bank](exam-bank.md). You receive each question with its numbers changed, so working the bank version is good practice and does not give you the answer.

Some lab work counts elsewhere, so nothing is marked twice.

- Lab 03's written check against the CPC principles goes to the [ethics analysis](ethics-analysis-brief.md), as do labs 04, 06, 07 and 08 in full.
- Lab 13 Part C and lab 14 Parts C and D are milestones of the [business plan](business-plan-brief.md).

## Deliverables for each set

1. **The lab deliverable,** exactly as the lab specifies: code with passing tests or checker, results file and the memo or note.
2. **Answers to the two added questions,** one page at most, as a separate file or the last page of the lab submission. For each question, name the model with every symbol defined once, show the substitution with units, give the result, and write one sentence on what the number means for a designer or a producer.
3. **A reproducibility line.** For any simulated number, the seed and the command that produced it. For any real-world price or fee, its source and the date you read it.

## Milestones and feedback

| When | What happens |
|---|---|
| Each lab week, before the next lecture | Model set due. |
| Within one week of the deadline | Marked rubric returned, with the correct value for both added questions. |
| After MS3 (week 4) | Early check. Any student averaging under 50 meets the instructor to review the week 1 to 3 models, since the business plan builds on all three. |
| After MS5 (week 10) | Your lab 01, 02 and 09 code should be in shape to reuse in the business plan's revenue model. Fix anything the marker flagged. |
| Week 14 | MS9 returned. Its model feeds the business plan's cost section, so correct it before week 15. |

## How a set is scored

Each set is scored out of 100.

| Component | Points |
|---|---|
| Lab deliverable, marked with the lab's own rubric and scaled to 80 | 80 |
| Added question A | 10 |
| Added question B | 10 |
| **Total** | **100** |

Scaling rules for the lab part:

- Labs whose rubric is in percentage weights are scaled directly: 85% on the lab rubric is 68 of 80.
- Labs whose rubric is in points out of 20 (labs 05, 10, 11, 12) are multiplied by 4.
- Where only part of a lab counts, only those rubric rows are marked and rescaled to 80. For lab 03 that is solver, real-store audit, redesign and presentation (80% of its rubric). For lab 13 it is implementation and ramp analysis (35%). For lab 14 it is implementation and sensitivity (30%).

Your models grade is the average of your best 9 of the 10 sets. The dropped set covers one bad week. A missing set counts as 0 before the drop.

## Rubric for each added question (10 points)

| Criterion | Full | Partial | None | Points |
|---|---|---|---|---|
| Model | Names the lecture model and defines every symbol it uses | Model named, some symbols undefined | Wrong model or none | 2 |
| Working | Substitution shown with units; a reader can follow each step | Steps skipped but recoverable | Result only | 3 |
| Result | Correct to the precision the lecture uses (tolerance 1% or one unit in the last digit shown) | Right method, arithmetic slip | Wrong or missing | 3 |
| Meaning | One sentence that says what the number implies for a decision, with the number in it | Generic sentence | Missing | 2 |
| **Total** | | | | **10** |

## Rules that apply to every set

- **Code must run.** Tests or checkers run with `.venv/bin/python` from the repository root, or with `python3` inside the starter folder, as each lab says. Code that does not run earns no marks for the implementation row, whatever it would have printed.
- **Integer money and tolerances.** Use integer cents or an explicit tolerance for money and probability comparisons, as the lab starters do.
- **Real prices carry dates.** Store prices, fees and platform terms change. A real number without a source and a read date is marked as an assumption.
- **Invented numbers are labelled.** The labs use invented parameters on purpose. Say so when you reuse one, and never present one as a studio's data.
- **Your own work.** You may discuss methods with classmates. Every number and sentence you submit must come from your own code or sheet. Pairs submit one lab deliverable and two sets of added-question answers.
