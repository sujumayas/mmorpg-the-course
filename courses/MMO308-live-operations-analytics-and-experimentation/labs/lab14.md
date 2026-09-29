# MMO308 · Lab 14: Sunset forecast and recommendation

**Week:** 14 ([lecture](../lectures/w14-sunsetting-content-and-servers.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** individual.
**Counts toward:** analytics labs (40% of the course grade). The recommendation memo is reused as the end-of-life section of your final live-ops plan.

## Objective

Fit a single-rate model and a core-plus-casual mixture to 18 months of noisy MAU, forecast when the game stops covering its maintenance cost under each one, find the announcement month a notice period forces, and put a dollar figure on each forecasting mistake. Then write the recommendation a studio lead would need.

## Starter materials

- [`lab14-starter.py`](lab14-starter.py): Python 3, standard library only. `make_history()` returns 18 months of MAU for a game whose true decline you do not know (about 3% noise). Stubs for the diagnostic, both models, both fits, the crossing, the announcement month and the error costs, plus eight tests that print PASS or FAIL. Run it first: all eight fail.
- The [sunset forecast interactive](../examples/w14-sunset-forecast.html) for checking curves by eye.
- Business assumptions for this lab: revenue per MAU `a = $4` a month, maintenance cost `C = $50,000` a month, notice six months.

Run with `.venv/bin/python courses/MMO308-live-operations-analytics-and-experimentation/labs/lab14-starter.py` from the repository root. The script exits with status 0 only when every test passes.

## Steps

### Part A: the diagnostic (15 min)

1. Implement `six_month_ratios` (test A1). Run it on `make_history()`. You get two ratios. Say in one sentence what they suggest.
2. Plot the 18 months on a linear axis and on a log axis. Describe the shape on each in one sentence.

### Part B: fit both models (40 min)

3. Implement `mixture` and `fit_single` (tests B1, B2). Fit the single rate to your history and report `M0`, the monthly rate and the half-life.
4. Implement `fit_mixture` (tests B3, B4). Report `w` and both half-lives.
5. Refit both models using only months 0 to 11, then months 0 to 17. Report how much each set of parameters moves. Which model is more stable as data arrives, and why is that not the same as being right?
6. Change the noise by calling `make_history(seed=s)` for five different seeds. For each, record the fitted `w`. Report the spread. This is your estimate of how far to trust a mixture fit on 18 months.

### Part C: forecasts and errors (35 min)

7. Implement `crossing`, `announce_month` and `error_costs` (tests C1 to C3).
8. Using your 18-month fits, compute both crossings at `C = $50,000`, both announcement months, and both error costs. Present them in one table.
9. Repeat step 8 with notice of 12 months. What changes and what does not?
10. The studio can cut maintenance to $40,000 by moving to a smaller team. Compute how many months that buys under each model.

### Part D: recommendation (30 min)

11. Write a one-page memo to the studio lead. It must give a recommended announcement month (or "not yet, revisit at month N"), the evidence (ratios, both fits, the seed spread from step 6), both error costs in dollars, what the players who remain would lose under each error, and the next data point that would change your mind. Include a sunset plan checklist with the five parts from lecture section 4 filled in for this game.

## Deliverable

- The completed `lab14-starter.py` with all eight tests passing.
- A PDF of at most 4 pages: Part A plots, the Part B parameters and stability results, the Part C tables, and the Part D memo.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Diagnostic (Part A) | Test A1 passes; both plots with a correct reading of each | Plots present, reading vague | Missing | 10 |
| Model fitting (Part B) | Tests B1 to B4 pass; stability and seed-spread results reported and interpreted | Fits correct, stability or spread missing | Tests fail | 30 |
| Forecasts and errors (Part C) | Tests C1 to C3 pass; tables for 6 and 12 months of notice; step 10 answered for both models | One table or step 10 missing | Tests fail | 25 |
| Recommendation (Part D) | Clear decision tied to evidence and uncertainty; both errors in dollars and in player terms; a named trigger to revisit; full five-part plan | Decision present, evidence or plan thin | Missing | 30 |
| Clarity | Every number has a unit and a source | Some numbers unexplained | Unreadable | 5 |
| **Total** | | | | **100** |
