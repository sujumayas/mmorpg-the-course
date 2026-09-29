# MMO308 · Lab 02: Touches and play

**Week:** 2, KPIs ([lecture](../lectures/w02-kpis-dau-mau-stickiness-arpdau.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** one of the analytics labs (analytics labs are 40% of the course).

## Objective

A producer has received two lines: "MAU down 31% month on month" and "stickiness up 38% between day 69 and day 71". They want to know whether the game is shrinking and whether whatever happened on day 71 should be repeated. Build the KPI tree from the lecture, compute calendar and rolling MAU, stickiness, player-days and a regulars count from 90 days of activity for an invented MMO, and find out what really happened.

## Starter materials

All in [`lab02-starter/`](lab02-starter/). Standard-library Python 3.10 or later, no packages to install.

- [`gen_activity.py`](lab02-starter/gen_activity.py). Writes `activity.csv` (one row per active player per day, days 0 to 89) and `payments.csv` (one row per purchase). Seed 2026. Days 0-29 are month 1, 30-59 month 2, 60-89 month 3. The studio ran a free weekend on days 40 and 41. The generator is readable: you may look at how it makes players after you have done steps 1 to 4, not before.
- [`kpis.py`](lab02-starter/kpis.py). Loaders and a report are provided. Seven functions are marked `TODO`: `month_model` (the lecture's regulars-and-tourists model), `dau_series`, `window_mau`, `rolling_mau`, `regulars`, `kpi_tree` and `revenue_factors`. The module docstring fixes the conventions.
- [`test_kpis.py`](lab02-starter/test_kpis.py). Tests with the lecture's numbers (the update quarter: MAU 1,800,000, mean DAU 486,667, stickiness 0.270), a tiny hand-checkable log, the rolling-window echo, the revenue factors from Check yourself question 3, and identities that must hold on the generated data. On the starter every test prints `TODO` and the script exits with status 1.

From the `lab02-starter` folder:

```
python gen_activity.py
python test_kpis.py
python kpis.py
```

## Steps

1. **The model (15 min).** Implement `month_model`. Use it to reproduce the lecture's three-quarter table.
2. **Windows (30 min).** Implement `dau_series`, `window_mau`, `rolling_mau` and `regulars`. Check `TINY` in the test file by hand before you run the tests.
3. **The tree (20 min).** Implement `kpi_tree` and `revenue_factors`. Run the tests until all pass. Then run `kpis.py`.
4. **The loud story (20 min).** For each calendar month, tabulate MAU, mean DAU, stickiness, player-days and the regulars count on the month's last day. Compute month-over-month changes. Which KPIs agree with "MAU down 31%" and which do not? Estimate how many of month 2's MAU were free-weekend tourists, using only the KPIs (not the generator).
5. **The echo (15 min).** Plot daily DAU, 30-day rolling MAU and daily stickiness (mean DAU over the last 30 days divided by rolling MAU) for days 29 to 89. Mark days 40, 41, 70 and 71. Explain the stickiness jump in two sentences. On which day would a 7-day rolling WAU show the same kind of jump?
6. **Money (15 min).** Use `revenue_factors` for month 1 to 2 and month 2 to 3. Write each as a product. Did the free weekend's players pay? Compare the payer rate on days 40 and 41 with the rest of month 2.
7. **Report (at home).** Write the one-page KPI report the producer should have received.

## Deliverable

A zip or repository link with:

- your `kpis.py`, passing `test_kpis.py`;
- `RESULTS.md` with the step 4 table and tourist estimate, the step 5 chart and explanation, and the step 6 products and payer rates;
- a report of at most 400 words to the producer. It must answer both lines ("is the game shrinking?" and "should we repeat day 71?"), show MAU next to an engagement-weighted KPI, and propose the six tiles of a monthly KPI dashboard, each with its definition and the guardrail it is paired with.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All tests pass; conventions from the docstring followed; readable | Tests pass, code hard to follow | Tests fail | 30% |
| Touches versus play | Month table complete; MAU and engagement KPIs contrasted; tourist count estimated from KPIs with the method shown | Table complete, interpretation thin | Reads the MAU drop as players leaving | 25% |
| Echo | Chart marked correctly; jump explained as the event leaving the window; the 7-day equivalent day given | Echo explained, chart or 7-day answer missing | Not identified | 15% |
| Revenue factors | Both products correct; payer rate of the weekend compared with the rest of the month | Products correct, comparison missing | Missing or factors added instead of multiplied | 10% |
| Report | Both questions answered with numbers; six tiles with definitions and guardrails; within 400 words | Answers given, tiles incomplete | No clear answers | 20% |
