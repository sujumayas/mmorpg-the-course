# MMO308 · Lab 04: Funnels and churn from an event log

**Week:** 4 ([Funnels and churn](../lectures/w04-funnels-and-churn.md))
**Time:** 2 hours in lab plus up to 2 hours at home
**Counts toward:** analytics labs (40% of the course grade)
**Work:** in pairs; submit one folder per pair

## Objective

You will compute the same story funnel three ways from one log and see how far apart the answers are. Then you will label churn with several inactivity windows and measure, against what players actually did afterwards, how often each window is wrong for each kind of player.

## Starter materials

All in [`lab04-starter/`](lab04-starter/README.md). Python 3.10 or later, standard library only.

- `gen_log.py` writes three files from seed 404. `players.csv` has 6,000 players with `install_day` (0 to 119, a quarter of them in launch week) and `cadence` (`daily`, `regular` or `occasional`). `sessions.csv` has one row per player per day played. `chapters.csv` has one row per story chapter completed (1 to 8) with its day. The log runs to day 179. You analyse on day 119. Days 120 to 179 are the future, used only to check churn labels.
- `funnel.py` loads the files and holds five functions to write: `step_conversions`, `snapshot_funnel`, `cohort_funnel`, `churned` and `false_churn_share`. Each docstring states the exact definition. `main()` prints a table from whatever you have finished.
- `check_lab04.py` prints PASS, FAIL or TODO per function and exits non-zero until all pass.

```
python gen_log.py
python funnel.py
python check_lab04.py
```

On the starter, every function prints TODO.

## Steps

1. **Step conversion (10 min).** Write `step_conversions`. Check it by hand on `[200, 150, 75, 60]`.
2. **The snapshot (20 min).** Write `snapshot_funnel`, the open, unboxed funnel a dashboard would show on day 119. Record the shares and step conversions in `RESULTS.md`. Which chapter looks weakest?
3. **Cohort funnels (30 min).** Write `cohort_funnel` (closed and time-boxed, as defined in the docstring). Run it with 30-day and 60-day boxes. Put the three funnels in one table. Explain in three sentences why the 30-day box shows falling step conversions for chapters 5 to 8 while the 60-day box does not, using the `q / (q + h)` model from the lecture.
4. **Is chapter 3 really weak? (15 min).** In all three funnels, compare chapter 3's step conversion with the average of chapters 4 to 8. Is chapter 3 an artifact of when you measured, or a real problem? Then split the 60-day cohort funnel by `cadence` (add a small helper; the checker does not test it). Which segment's funnel is least mature at 60 days, and why?
5. **Churn labels (20 min).** Write `churned` and `false_churn_share`. Fill in a table of false-churn share for W = 3, 7, 14 and 30, for each cadence and for all players. Compare the shape with the lecture's formula table. They will not match exactly. Name one difference between the lab's generator and the lecture's model that explains it.
6. **Recommendation memo (at home).** One page to a live-ops producer. Recommend (a) which funnel definition the story dashboard should use, with its box length, and (b) a churn window for each cadence segment, each with its measured false-churn share and the detection delay it implies. State one decision the team could make wrongly with the current default of a snapshot funnel and a single 7-day window.

## Deliverable

One folder named `lab04-<name1>-<name2>` containing your `funnel.py` (passing `check_lab04.py`), `RESULTS.md` with the tables and answers to steps 2 to 5, and `memo.pdf` from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All six checks PASS | Four or five PASS | Three or fewer | 5 |
| Funnel comparison (steps 2 and 3) | Three funnels tabulated; the 30-day decline explained with pace racing hazard, in numbers | Table correct, explanation vague | Missing | 4 |
| Chapter 3 and segments (step 4) | Chapter 3 shown weak in every definition; least mature segment identified with a reason from cadence | One of the two parts done | Missing | 3 |
| Churn table (step 5) | Complete table, one specific model difference named | Table complete, no explanation | Missing or wrong | 3 |
| Memo (step 6) | Definitions justified by the lab's numbers; windows per segment with false-churn share and delay; a concrete wrong decision named | Recommendations without numbers | Missing | 5 |
