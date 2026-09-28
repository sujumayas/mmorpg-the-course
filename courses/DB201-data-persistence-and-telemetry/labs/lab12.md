# DB201 · Lab 12: KPIs in SQL

**Week:** 12 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** one of the SQL labs (SQL labs are 40% of the course)

**Lecture:** [Week 12, dashboards and KPIs](../lectures/w12-dashboards-and-kpis.md)

## Objective

Compute the core live-game KPIs in SQL from a session log, under explicit definitions, and see how much the definitions move the numbers. Then specify a dashboard in which every tile states what it means.

## Starter materials

All in [`lab12-starter/`](lab12-starter/):

- `gen_sessions.py`: writes `accounts.csv` (3,000 accounts owned by 2,859 people, with install day and UTC offset) and `sessions.csv` (45,123 sessions over 60 days, 1 March to 29 April 2026). Seed 1212.
- `kpis.py`: loads both files into `kpi.db`, runs every query in its `QUERIES` dictionary and writes each result to `out/<name>.csv`. The first query (`dau_utc`) is written as a pattern. Six are `None` and marked `TODO`.
- `check_lab12.py`: recomputes every KPI in plain Python (no SQL) and prints PASS, FAIL or TODO per query.

You need Python 3.10 or later. No packages to install. From the `lab12-starter` folder run:

```
python gen_sessions.py
python kpis.py
python check_lab12.py
```

On the starter code, `dau_utc` passes and the other six print TODO. The checker's last line gives the reference MAU and mean DAU for the last 30 days, so you can sanity-check your own.

## Steps

1. **Read the pattern (10 min).** Read `dau_utc`. Open `out/dau_utc.csv`. Why is there a row for 28 February when the data starts on 1 March? Write the answer in `RESULTS.md`.
2. **Three more DAUs (25 min).** Write `dau_5min` (sessions of 5 minutes or more), `dau_local` (player's local calendar day, using `utc_offset_hours`) and `dau_person` (count `person_id`). Each must pass.
3. **Compare (10 min).** For 1 April and 15 April, tabulate the four DAUs and the percentage difference of each from `dau_utc`. Which decision moves DAU most in this data? Is that true every day? Check a weekend day too.
4. **MAU and stickiness (20 min).** Write `mau_last30` and `stickiness_last30` for the 30 days ending 29 April. Then compute, in `RESULTS.md`, the sum of the 30 DAUs and explain in two sentences why it is not the MAU.
5. **Retention (25 min).** Write `retention` with one row per complete install cohort: install day, cohort size, D1 and D7 (exact-day, UTC). Then, in `RESULTS.md`, compute rolling D7 (active on day 7 or later) for the 1 March cohort with one extra query, and compare it with exact-day D7.
6. **Dashboard spec (at home).** Write `DASHBOARD.md`, a six-tile dashboard for a producer who meets every Monday. For each tile give: the question in the title, the definition footnote (threshold, day boundary, unit), the baseline it is compared with, the refresh schedule, and the query or table it reads. Sketch the layout (a hand drawing photographed is fine, or a plot of your CSVs in any tool).
7. **Optional, HyperLogLog (at home).** If you have Redis, `PFADD` each session's account into one key per UTC day, then `PFCOUNT` the 30 keys of the last window. Compare with your exact MAU and express the difference in standard errors (Redis documents 0.81%).

## Deliverable

A zip or repository link with:

- your `kpis.py`, with all seven queries passing `check_lab12.py`;
- the `out/` folder;
- `RESULTS.md` with steps 1, 3, 4 and 5;
- `DASHBOARD.md` with the six tiles and a layout sketch;
- a memo of at most 300 words recommending one DAU definition for the studio's weekly report, justified with your step 3 numbers, and saying what the report must footnote.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Queries | All seven pass; SQL readable, with comments naming the definition | Five or six pass | Four or fewer pass | 35% |
| Definitions analysis | Step 3 table with percentages, weekday and weekend compared, the dominant decision identified; 28 February explained | Table present, analysis thin | Missing or numbers inconsistent with the CSVs | 20% |
| Distinct counts and retention | Sum of DAU versus MAU explained correctly; rolling versus exact D7 computed and compared | One of the two done well | Missing or wrong | 15% |
| Dashboard spec | Six tiles, each with question, footnote, baseline, schedule and source table; layout sketch | Tiles present, some fields missing | Fewer than four tiles or no definitions | 20% |
| Memo | Clear choice backed by the student's numbers, with the footnote text | Choice made, justification generic | Missing | 10% |
