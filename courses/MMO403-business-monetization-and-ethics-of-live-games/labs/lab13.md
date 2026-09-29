# MMO403 · Lab 13: Phase budget and slip analysis

**Week:** 13, team and budget planning ([lecture](../lectures/w13-team-and-budget-planning.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the Models strand (40%). The budget you build here becomes the cost section of your final business plan, and lab 14 asks you to fund its first stage.

## Objective

Implement the week 13 burn model with staffing ramps, a contingency rule and the hire-or-slip comparison, check it against the lecture's numbers, then build a sourced budget for your own final-project MMO and stress it with three slip scenarios. By the end you should be able to say, with a number, how many months of slip your plan survives in each phase and what you will cut first when it doesn't.

## Starter materials

All in [`lab13-starter/`](lab13-starter/). Standard-library Python 3.10 or later.

- [`budget.py`](lab13-starter/budget.py), with a plan loader and eight empty functions: `phase_burn`, `burn_series` (with an optional ramp), `cash_out_month`, `slip`, `slip_cost`, `contingency_months`, `runway` and `crash_vs_slip`. Each docstring gives the exact rule.
- [`plan.csv`](lab13-starter/plan.csv), the lecture's three-phase plan (6 months at 12 people, 18 at 45, 6 at 60).
- [`test_budget.py`](lab13-starter/test_budget.py), eight tests built from the lecture: the $13,920,000 total, cash-out in months 33 and 32 for production and beta slips against $15 million, the slip costs of $510,000, $1,500,000 and $1,950,000, the ramped plan ($13,320,000), contingency months, the runway from check-yourself question 1, and the 148.5 head-month hiring example. Every test fails on the starter.
- The interactive [`examples/w13-burn-and-runway.html`](../examples/w13-burn-and-runway.html) for spot checks.

Run the tests from inside the folder with `python3 test_budget.py` (or `pytest`). From the repository root use `.venv/bin/python courses/MMO403-business-monetization-and-ethics-of-live-games/labs/lab13-starter/test_budget.py`. The script exits with status 0 only when all eight pass.

## Steps

### Part A: the model (45 min)

1. Implement `phase_burn`, `burn_series` without a ramp, `cash_out_month`, `slip` and `slip_cost`. Reproduce the lecture's slip table by hand for one row before you run the tests.
2. Implement the ramp in `burn_series`. With a three-month ramp, write down the headcount for months 1 to 9 on paper first (you should get 4, 8, 12, 12, 12, 12, 23, 34, 45).
3. Implement `contingency_months`, `runway` and `crash_vs_slip`. Run until all eight tests pass.

### Part B: what the ramp changes (20 min)

4. Recompute the slip table with a three-month ramp. A slip now adds months at the phase's full headcount. Explain in two sentences why the slip costs do not change at all while the total falls by $600,000, and what that says about where a ramp saves money.
5. Find the smallest cash amount (to the nearest $10,000) for which the ramped plan survives a three-month beta slip. Compare it with the flat plan's answer.

### Part C: your own budget (60 min)

6. Write a phase plan for your final-project MMO with at least four phases, including one live phase of at least 12 months after launch. Give each phase a headcount by role (at least design, engineering, art, QA, production, and community or support for the live phase).
7. Replace the lecture's `c` and `F` with sourced figures. For the loaded cost, start from a salary source for your region (a national statistics office, a published industry salary survey, or a studio's public accounts such as Cloud Imperium's) and state the multiplier you apply for taxes, benefits and equipment, with your reason. For `F`, list at least four fixed items with a cost and a source or a stated assumption for each.
8. Set the cash you intend to raise and a contingency percentage. Justify the percentage by listing the three least-tested risks in your plan.
9. Run three slip scenarios. (a) 3 months in pre-production. (b) 3 months in your largest phase. (c) A 4-month rework found in the second half of production. For each, give the extra cost, the cash-out month or the money left, and what you would do (spend contingency, cut, hire, or move the date). If you choose to hire, show `crash_vs_slip` with your own assumptions.
10. Write a cut list of at least five items in the order you would cut them, with the head-months each cut saves.
11. Optional, if you completed lab 01: use your `contribution` function to add revenue in the live phase and report the month in which cumulative contribution passes cumulative spend.

## Deliverable

- The completed `budget.py` with all eight tests passing.
- A PDF of at most 4 pages: the Part B answers, your plan table, the sources for `c` and `F`, the three scenarios in one table, the cut list, and a memo of at most 500 words to your studio lead recommending how much to raise and why.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation (Part A) | All eight tests pass; hand checks shown for steps 1 and 2 | Tests pass, hand checks missing | Tests fail | 25% |
| Ramp analysis (Part B) | Correct explanation and correct minimum cash | One of the two correct | Missing or wrong | 10% |
| Sourced costs (step 7) | `c` and every item of `F` sourced or explicitly assumed, with dates and a reasoned multiplier | Some items unsourced | Numbers without sources | 20% |
| Slip scenarios (step 9) | All three computed; each decision tied to its numbers; hiring case uses the model | Scenarios computed, decisions vague | Missing scenarios | 20% |
| Cut list and contingency | Ordered cuts with head-months saved; contingency tied to named risks | Cuts listed without sizes | Missing | 15% |
| Memo | Clear ask with runway and slip tolerance in months; no reliance on unplanned overtime | Ask present, reasoning thin | Missing | 10% |
