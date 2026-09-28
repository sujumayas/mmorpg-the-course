# DB201 · Lab 11: A telemetry pipeline in SQLite

**Week:** 11 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** one of the SQL labs (SQL labs are 40% of the course)

**Lecture:** [Week 11, pipelines: collect, store, query](../lectures/w11-pipelines-collect-store-query.md)

## Objective

Build the load, rollup and query stages of a telemetry pipeline over a landing file that behaves like a real one: some batches arrive twice, some arrive after midnight. Make the load idempotent, build a daily rollup, measure the query-cost ladder from the lecture on your own machine, and quantify how incomplete a rollup is when it is built too early.

## Starter materials

All in [`lab11-starter/`](lab11-starter/):

- `make_events.py`: writes `events.ndjson`, 14 days of events for 400 players (seed 1111). About 2% of batches are duplicated (retries) and about 1% arrive after midnight UTC (late). Default output is 400,918 lines, about 135 MB. Do not commit it.
- `pipeline.py`: loads the file into `telemetry.db`, builds the rollup, runs and times the query "deaths in zone 7 on 2026-03-05" against raw events and against the rollup, and prints both query plans. Four `TODO`s.
- `check_lab11.py`: recomputes the expected answers from `events.ndjson` in plain Python and compares them with your database.

You need Python 3.10 or later. No packages to install. From the `lab11-starter` folder run:

```
python make_events.py
python pipeline.py
python check_lab11.py
```

On the starter code the load keeps every duplicate (400,918 rows), the rollup is empty, and the checker reports two FAILs. That is expected.

## Steps

1. **Measure the damage (10 min).** Run the three commands on the starter code. Record the raw answer for "deaths in zone 7 on 2026-03-05". Using the checker's expected row count, compute by what percentage the starter over-counts rows.
2. **Idempotent load, TODO 1 (15 min).** Make `event_id` a key and change the insert so a second copy is skipped. To prove idempotence, temporarily call `load(con)` a second time in `main()`, right after the first call, and confirm the row count does not change. Remove the extra call afterwards. The checker's first line should say PASS.
3. **Rollup, TODO 2 (20 min).** Write the SQL that fills `daily_zone_deaths(event_day, zone_id, deaths)`. Use `json_extract` to read the zone. Make it safe to run twice. The checker's second line should say PASS.
4. **The ladder, TODO 3 (20 min).** Add an index that lets the raw query skip most of the table. Record, for the full scan, the indexed query and the rollup: the query plan line, the time, and your estimate of rows touched. Put them in a table in `RESULTS.md` next to the lecture's L0 to L3.
5. **Your scan rate (10 min).** From the full-scan time and the row count, compute your machine's scan rate in rows per second. Use it to predict the full-scan time for 1,000 players. Then run `python make_events.py --players 1000` and `python pipeline.py` and compare the prediction with the measurement.
6. **Late events, TODO 4 (20 min).** Count events whose `received_at` day is after their `event_day`. Then answer: if the rollup for 2026-03-05 had been built at 00:05 on 2026-03-06, how many of that day's deaths would it have missed, and what percentage is that? At what time would it have been complete?
7. **Policy (at home).** The live team wants a "deaths per zone yesterday" tile that is correct by 09:00 UTC and never changes after that. Write the policy (when the rollup runs, which days it rebuilds) and add a `--rebuild-days N` option to `pipeline.py` that rebuilds only the last N days of the rollup, idempotently.

PostgreSQL notes are in the code comments marked `PG:`. If you have PostgreSQL, the optional extension is to load the same file into a table partitioned by day and show partition pruning with `EXPLAIN`.

## Deliverable

A zip or repository link with:

- your `pipeline.py`, passing `check_lab11.py`;
- `RESULTS.md` with the over-count percentage, the ladder table, your scan rate and prediction check, and the late-event numbers;
- a memo of at most 300 words: for the reference game in the lecture (40,000 DAU, 500 events per player per day, 90 days of raw data), recommend a storage layout and a rollup schedule for a 20-tile dashboard used by 10 people, using your measured scan rate. Name what your design cannot answer quickly.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Correctness | Checker passes; load is idempotent across repeated runs; rollup is safe to rerun | Checker passes but rerunning changes something | Checker fails | 30% |
| Measurement | Ladder table with plans, times and rows touched; scan rate computed; prediction compared with a real run | Table present, prediction missing or unchecked | Missing, or copied from the lecture | 25% |
| Late events | Correct late count, missed deaths and percentage, and the completion time, with the query shown | Numbers present, method unclear | Missing or wrong | 20% |
| Recommendation | Layout and schedule justified with the student's own scan rate; core load computed; limits named | Reasonable choice, thin numbers | No recommendation, or contradicts the measurements | 25% |
