# PR402 Lab 03: Demand forecast and hosting budget

**Week:** 3 (Production sprint 3). **Guide:** [week 3](../lectures/w03-production-sprint-3-feature-complete-and-server-budget.md). **Team lab**, submitted once per team.

## Objective

Forecast how many players will be connected at once at launch, size your zone server fleet from your load test, and build a hosting budget for weeks 4 to 15 that stays under your grant with a reserve. The checker tells you whether the fleet covers the launch peak and whether the budget fits.

## Starter materials

In [`labs/lab03-starter/`](lab03-starter/):

- `check_budget.py`. Standard library only. Run it with `.venv/bin/python check_budget.py demand.csv budget.csv`. It prints DAU, average, evening and launch CCU, zone servers needed, each budget line and the total against the grant less a 10% reserve, then `PASS` or `NOT READY`. It exits with code 1 when a rule fails.
- `demand.csv`. Emberfall's demand inputs, each with a source column. The launch fleet is set too small on purpose.
- `budget.csv`. Emberfall's naive plan from the guide, $743.50 against a $500 grant.

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter files. Fix the fleet size and change `budget.csv` to the guide's fixed plan. The total should be $448.30, under the $450 limit, and the checker should print `PASS`.
2. **Your demand.** Replace every value in `demand.csv` with your own, and write a source for each: a playtest, a sign-up count, a load-test run, or "course default". Use your real knee, not the maximum your bots reached.
3. **Your prices.** Look up your provider's current hourly prices for each machine type and its egress price. Save the price page as a PDF in the lab folder, with the date.
4. **Your lines.** Write one budget line per machine group per environment, with the hours per week it will run and the weeks. Compute egress from your forecast player-hours and measured bandwidth per player, and enter it as `fixed_dollars` with the calculation in `note`.
5. **Fit the grant.** Change schedules, not players, until the total fits under the grant less the reserve. Production may run all week from open beta. Nothing else may.
6. **Alerts and teardown.** Set provider budget alerts at 50% and 80% of the grant. Add "destroy bot fleet and test databases" to your load-test checklist.
7. **Weekly check.** From week 4, compare actual spend on the provider's billing page with the plan at each review. Write the difference in `spend-log.md`.

## Deliverable

In `production/week03/` in the team repository:

- `demand.csv` and `budget.csv` passing `check_budget.py`, with output saved as `check-output.txt`.
- The dated provider price page.
- A screenshot of the budget alerts.
- `spend-log.md`, started with the week 3 entry (zero or the dev costs so far).

**Checkable output:** the instructor reruns `check_budget.py` on your two files. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output file matches |
| Sourced demand | 4 | Every input has a real source; the knee comes from a load test with its latency threshold stated |
| Real prices | 3 | Dated price page matches the rates used |
| Complete lines | 3 | Every environment, peak servers, egress and load tests present; egress calculation shown |
| Schedules | 3 | Non-production environments scheduled; production schedule before open beta justified |
| Alerts and log | 3 | Alerts at 50% and 80% shown; teardown on the checklist; spend log started |
