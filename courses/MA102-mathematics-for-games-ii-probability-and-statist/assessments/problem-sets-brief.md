# MA102 · Problem sets brief

**Weight:** 35% of the course grade.
**Work:** individual unless a lab says otherwise (lab 14 is done in pairs).
**Made of:** 13 weekly labs. Lab 11 is not part of this component; it is the separate Monte Carlo lab (see [monte-carlo-lab-brief.md](monte-carlo-lab-brief.md)).

## What the problem sets are for

Each week's lecture gives you one model. The lab makes you use it on numbers you have not seen, check it against a simulation or a hand count, and write a short recommendation someone else could act on. The problem sets are where you practise that full loop every week, so that by the loot design project and the final you do it without thinking.

## The labs

| Lab | Week | Topic | Due | Work |
|---|---|---|---|---|
| [Lab 01](../labs/lab01.md) | 1 | Sample spaces in a spreadsheet | start of week 2 | individual |
| [Lab 02](../labs/lab02.md) | 2 | Streak detective | start of week 3 | individual |
| [Lab 03](../labs/lab03.md) | 3 | The drop-rate calculator | start of week 4 | individual |
| [Lab 04](../labs/lab04.md) | 4 | The expected-DPS spreadsheet | start of week 5 | individual |
| [Lab 05](../labs/lab05.md) | 5 | Swing and overkill | start of week 6 | individual |
| [Lab 06](../labs/lab06.md) | 6 | Crit simulator versus the binomial | start of week 7 | individual |
| [Lab 07](../labs/lab07.md) | 7 | Dry streaks at scale | start of week 8 | individual |
| [Lab 08](../labs/lab08.md) | 8 | Dice by design | start of week 9 | individual |
| [Lab 09](../labs/lab09.md) | 9 | Loot table from targets | start of week 10 | individual |
| [Lab 10](../labs/lab10.md) | 10 | Design a bad-luck protection rule | start of week 11 | individual |
| [Lab 12](../labs/lab12.md) | 12 | Summarizing a playtest | start of week 13 | individual |
| [Lab 13](../labs/lab13.md) | 13 | How many kills until you trust a drop rate? | start of week 14 | individual |
| [Lab 14](../labs/lab14.md) | 14 | Analyze an A/B test, and design one | start of week 15 | pairs |

## Deliverables

Each lab file lists its own deliverable. Every submission, whatever the lab, must also meet these four standards.

1. **Reproducible.** Every number in your write-up can be regenerated from the file you submit. Simulations use the seed the lab names. A grader who runs your notebook or recalculates your sheet gets your numbers.
2. **Checked.** Wherever the lab gives check values (for example Lab 04's Iron Maul 37.80 or Lab 07's 69 / 100 / 299 / 459), your submission shows them matching, or says why not.
3. **Stated with context.** Probabilities say what event they belong to. Estimates carry n and, from week 11 on, a margin of error. Percentiles name the rule used.
4. **Written for a designer.** The memo or report is short, puts numbers first, and ends with a recommendation. The word limit in each lab is a hard cap.

## Milestones

The problem sets have no single due date. The rhythm is weekly.

- **In the lab session:** start the lab with a teaching assistant present. Most labs' first two steps (the check values) should be done before you leave.
- **Midweek:** post any blocking question on the course forum by Thursday. Answers go to everyone.
- **Start of the next week:** submit. The table above gives each date.
- **Week 8 checkpoint:** you receive a running total for labs 01 to 07 with written feedback on the most common error in your work so far.
- **Week 15:** the final component grade is published with the exam results.

## How labs are scored

Each lab has its own rubric with weighted criteria. Convert each criterion level to a share of that criterion's weight, then add.

| Lab rubric level | Share of the criterion's weight |
|---|---|
| Excellent (4) | 100% |
| Adequate, high end (3) | 75% |
| Adequate, low end (2) | 50% |
| Missing or wrong, partial (1) | 25% |
| Missing or wrong (0) | 0% |
| Labs 13 and 14: full / half / 0 points | 100% / 50% / 0% |

Labs 13 and 14 are marked out of 20 points; multiply by 5 to get a score out of 100.

**Component grade.** Your lowest lab score is dropped. The component grade is the mean of the best 12 lab scores, which is worth 35 of the course's 100 points.

## Rubric bands

The table below describes what each band of a lab score looks like, whatever the lab. Graders use it to settle borderline criterion levels.

| Band (points out of 100) | What the work shows |
|---|---|
| 90 to 100 | Every check value matches. The model is applied to the brief's new numbers without error. Simulations are seeded and agree with the exact values within their stated noise. The memo gives a recommendation a designer could act on today, with the trade-off named. |
| 75 to 89 | The model is right and applied correctly, with one or two arithmetic or rounding slips that do not change the recommendation. Checks are present. The memo is clear but a number or a trade-off is missing. |
| 60 to 74 | The main computation is right, but a part is missing (often the simulation check or the design step), or one modelling error changes a secondary result. The memo restates numbers without turning them into a recommendation. |
| 40 to 59 | A model is applied where it does not fit (for example the binomial for a fight with no fixed number of attacks), or several check values fail and the write-up does not notice. Some useful work remains. |
| 0 to 39 | Missing, not reproducible, or mostly wrong. Numbers cannot be traced to the submitted file. |

## Deductions and rules

- **Late work** loses 10 points per day, up to three days. After three days it scores 0. Each student has one 72-hour extension to use on any lab, no reason needed. Tell the instructor before the deadline.
- **Unreproducible numbers.** A number that the grader cannot regenerate from your file scores as missing, even if it is correct.
- **Over the word limit.** Graders stop reading at the limit.
- **Collaboration.** You may discuss methods. You may not share files, code or written answers, except with your partner in lab 14. Name anyone you discussed a lab with at the top of your submission.

## How the problem sets connect to the rest of the course

- Labs 02, 06, 07 and 10 build the simulation code you reuse in the [Monte Carlo lab](monte-carlo-lab-brief.md).
- Lab 09's table and Lab 14's test plan are the starting points of the [loot design project](loot-design-brief.md).
- Most compute questions in the [exam bank](exam-bank.md) use the same models as a lab, with new numbers. Working the labs carefully is the best exam preparation.
