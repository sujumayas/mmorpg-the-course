# MMO402 · Lab 06: Triage the queue

**Week:** 6 ([lecture](../lectures/w06-moderation-at-scale.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** case analyses (30% of the course grade).

## Objective

Given one day of scored player reports with ground-truth labels, choose an automatic-action threshold `h` and a review threshold `l` that catch as many violations as possible within a fixed review budget and a cap on wrong automatic actions. Then write the one-page moderation policy that the numbers support.

## Starter materials

**Data:** [`lab06-reports.csv`](lab06-reports.csv), 2,000 rows, one per report. The data is synthetic, generated for this lab with a fixed seed, and does not come from any game. The columns are:

| Column | Meaning |
|---|---|
| `report_id` | R0001 to R2000 |
| `score` | Classifier score from 0 to 1 (three decimals). Higher means more likely a violation |
| `category` | `spam`, `cheating`, `harassment`, `hate` or `offensive_name`, as chosen by the reporter |
| `violating` | Ground truth: 1 if the report is a real violation, 0 if not. Your policy may not use this column; it is for scoring only |
| `handle_minutes` | Average human handling time for the category: 0.5 for spam and offensive names, 2.0 for harassment and hate, 3.0 for cheating |

**Constraints for the main task.**

- Review budget: 2 moderators × 6 productive hours = **720 minutes** of handling time per day.
- At most **5 wrong automatic actions** per day (non-violations with `score ≥ h`).
- Tiers as in the lecture: `score ≥ h` is auto-actioned, `l ≤ score < h` is reviewed (and, as in the lecture, reviewers decide correctly), `score < l` is dismissed.

**Tools.** A spreadsheet or Python 3 with the standard library (`csv`). `matplotlib` is optional for the charts. Use thresholds on a grid of 0.05 (0.00, 0.05, ..., 1.00), plus `h = 1.01` to mean "no automatic tier".

## Steps

### Part A: one threshold (30 min)

1. Load the data. Count reports and violations. Check that you get 2,000 reports and 214 violations (10.7%).
2. For a single threshold `t` from 0.00 to 1.00 in steps of 0.05, compute flagged reports (`score ≥ t`), true positives, false positives, **precision** (true positives / flagged) and **recall** (true positives / 214).
3. Plot precision and recall against `t` on one chart. Mark the `t` where they cross.

### Part B: two thresholds under constraints (45 min)

4. For every pair with `l ≤ h` on the grid, compute auto-actioned count, wrong automatic actions, review count, review minutes (sum of `handle_minutes` in the review tier), dismissed violations (misses) and total violations caught (auto plus review).
5. Keep only the pairs that meet both constraints. Among those, find the pair that catches the most violations. Break ties by fewer review minutes.
6. Report your chosen `(h, l)` and its full row.

### Part C: stress it (25 min)

7. **Surge.** Double every report (treat each row as two). Keep 720 minutes. What is the best feasible pair now, and how many violations does the surge push into the dismiss tier?
8. **Category rules.** Cheating reports take 3 minutes each. Try a rule that never auto-actions cheating (the penalty is a ban, so a human must decide) while keeping the rest of your policy. Does it still fit the budget? What do you give up?
9. **Audit the dismiss tier.** With your chosen `(h, l)`, list the dismissed violations by category. Which category would a weekly 1% random audit of dismissed reports be most likely to catch, and how many dismissed reports would that audit read per day?

## Deliverable

A PDF named `lab06-<surname1>-<surname2>.pdf` with:

1. The precision/recall chart and the crossing threshold (Part A).
2. Your chosen `(h, l)` with its row and the constraint check (Part B).
3. Answers to steps 7 to 9 with numbers (Part C).
4. A one-page moderation policy for this game that states the thresholds, the penalty for automatic actions (and why it is reversible), how cheating is handled, the surge plan, and the audit plan. Each claim in it must cite a number from Parts A to C.

Also submit your spreadsheet or script.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Part A: precision and recall | Correct at every grid point; chart labelled; crossing marked | Minor arithmetic slips; chart unlabelled | Wrong definitions or missing | 20% |
| Part B: constrained search | Correct feasible optimum with full row and constraint check | Feasible pair found but not optimal, or row incomplete | Infeasible pair or missing | 25% |
| Part C: surge, category rule, audit | All three answered with numbers and a sentence of interpretation each | Two of three | One or none | 20% |
| Moderation policy | Every rule tied to a number; penalty ladder reversible where automatic; audit plan concrete | Rules stated with weak links to numbers | Opinion without numbers | 25% |
| Reproducibility | Script or sheet runs and reproduces the reported numbers | Runs with manual fixes | Missing | 10% |

<details>
<summary>Instructor check values</summary>

- 2,000 reports, 214 violations.
- Single threshold: `t = 0.30` flags 790 (195 true, 595 false), precision 24.7%, recall 91.1%. `t = 0.50` flags 290 (150 true), precision 51.7%, recall 70.1%. `t = 0.70` flags 103 (90 true), precision 87.4%, recall 42.1%. `t = 0.80` flags 51 (50 true), precision 98.0%, recall 23.4%. `t = 0.90` flags 14 (all true), recall 6.5%.
- Part B optimum on the 0.05 grid: `h = 0.80`, `l = 0.40`. Auto-actions 51 (1 wrong), review 434 reports taking 669.0 minutes, dismissed 1,515 with 33 violations missed, 181 caught (recall 84.6%). The pair `h = 0.85`, `l = 0.40` also catches 181 with 0 wrong but uses 699.0 minutes, so it loses the tie-break.
- For comparison: `h = 0.80`, `l = 0.30` catches 195 but needs 1,150.5 minutes (infeasible). `h = 0.70`, `l = 0.40` catches 181 but has 13 wrong automatic actions (infeasible). Reviewing everything needs 3,135.5 minutes.
- At the optimum, the 33 missed violations are 19 spam, 7 harassment, 4 hate, 2 cheating and 1 offensive name. Review minutes by category: cheating 249.0, harassment 218.0, hate 108.0, spam 75.5, offensive names 18.5.
- Surge (every row doubled, so review minutes and wrong automatic actions both double): the optimum is `h = 0.80`, `l = 0.55`, with 2 wrong automatic actions, 551.0 review minutes and 270 of 428 violations caught (63.1%). Misses rise from 66 (33 doubled) to 158, so the surge pushes 92 more violations into the dismiss tier. Note that `l = 0.50` is infeasible here and the next grid point up is the binding choice.

</details>
