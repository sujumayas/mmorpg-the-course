# MMO302 · Lab 14: Tick telemetry and a stall alert

**Assigned:** week 14 ([lecture](../lectures/w14-observability-logs-metrics-traces.md)). **Due:** start of week 15. **Feeds:** the week 15 load test, whose report must include the per-zone stall numbers this lab produces.

## Objective

Build the tick-time telemetry a zone server needs: a nearest-rank percentile, a mergeable bucket histogram with an exact over-budget count, the stall formulas, and a per-zone alert. Then run it over one hour of recorded ticks from 12 zones and find the zone players are complaining about, which the usual dashboard numbers do not show.

## Starter materials

The folder [`lab14-starter/`](lab14-starter/) contains:

- [`zones.py`](lab14-starter/zones.py), the data. `all_zones()` returns 72,000 tick times (one hour at 20 Hz) for each of 12 zones, generated deterministically so everyone gets the same numbers. Do not edit it, and do not read its generator to find the answer before step 5; treat it like a production data feed.
- [`tickmetrics.py`](lab14-starter/tickmetrics.py), your file. Every function raises `NotImplementedError`. Its `__main__` block prints a per-zone table once you are done.
- [`test_tickmetrics.py`](lab14-starter/test_tickmetrics.py), five tests. All five fail on the starter.

Run with the course Python:

```
cd labs/lab14-starter
../../../../.venv/bin/python test_tickmetrics.py   # PASS/FAIL per test (pytest also works)
../../../../.venv/bin/python tickmetrics.py        # per-zone table and alert, once implemented
```

## Steps

1. **Nearest-rank percentile (15 min).** Implement `nearest_rank(values, q)` as in lecture section 2. The test checks the lecture's 1,000-tick data set: p50 18, p95 24, p99 45, p99.9 140.
2. **The histogram (45 min).** Implement `observe`, `merge`, `count_over` and `quantile` for `TickHistogram`. Counts are per bucket, not cumulative, with an overflow bucket for values above 250 ms. `quantile` interpolates linearly inside the bucket holding rank `q × total`, starting the first bucket at 0. The tests check the lecture's section 3 numbers (busy p99 estimated at 50.0, quiet at about 14.9, merged fleet p99 about 23.8) and that merging ten histograms gives exactly the histogram of the combined data.
3. **Stall formulas (10 min).** Implement `stalls_per_minute(p, hz)` and `share_of_seconds_with_stall(p, hz)`.
4. **The alert (30 min).** Implement `stall_alert`: a zone fires if any rolling window of `window_min` minutes contains more than `max_per_min × window_min` ticks over budget. Use a running sum so the hour of data takes well under a second.
5. **Investigate (30 min).** Run `tickmetrics.py`. In your report, answer with numbers from its output:
   - Which zone has the highest mean tick time? Would a mean-based alert have paged someone about it, and should it have?
   - Which zone fires the stall alert? What are its mean, its histogram p99 and its p99.9? Explain, using the percentile rule `p_q ≤ B exactly when p ≤ 1 − q`, why p99 misses it.
   - Using the complement formula, estimate the share of seconds with a stall in the alerting zone. Then measure it directly (count 1-second blocks of 20 ticks with at least one stall). Explain the difference.
6. **Tune the alert (20 min).** Run `stall_alert` with `max_per_min` at 1, 2 and 4 and `window_min` at 1, 5 and 15. Record which zones fire in each of the nine cases. Pick one setting and defend it in three sentences: what a false page costs, what a missed stall costs.
7. **Write it up.**

## Deliverable

A zip or repository link containing:

- Your `tickmetrics.py`, with all five tests passing (paste the output in the report).
- `report.md`, 500 to 800 words, with: the per-zone table from step 5; the three step 5 answers; the 3 × 3 table from step 6 and your chosen setting with its defence; and one paragraph on which bucket edges you would add or move for a 30 Hz server, and why.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Tests | All five pass | Three or four pass | Two or fewer | 30% |
| Diagnosis | Correct zone found; p99 miss explained with the percentile rule and numbers | Correct zone, explanation vague | Wrong zone or none | 20% |
| Complement formula versus measurement | Both numbers given; difference explained by clustering (independence assumption broken) | Both numbers, no explanation | One or none | 15% |
| Alert tuning | 3 × 3 table complete; setting defended with costs of false and missed pages | Table complete, weak defence | Table missing | 20% |
| Bucket design for 30 Hz | Edge at the new 33.3 ms budget and a reason for each other change | Edge at budget only | Not done | 10% |
| Clarity | Numbers match reruns; concise | Minor gaps | Cannot be checked | 5% |
