# PR101 · Lab 09: Your cone and your post-mortem

**Week:** 9 ([Jam post-mortem](../lectures/w09-jam-post-mortem.md))
**Time:** one 2-hour lab session plus about 3 hours at home
**Work:** individually for Part A, in jam teams for Parts B and C

## Objective

Turn a jam log into the two views of the cone of uncertainty from lecture section 2, test your code against the lecture's numbers, then run it on your team's log and the class's pooled log. Use the results to write your team's jam post-mortem: a data section, went right and went wrong with evidence, and three changes that can be checked in the final project.

## Starter materials

- Python 3.10 or later, standard library only. In this repository use `.venv/bin/python`.
- [`lab09-starter/cone.py`](lab09-starter/cone.py), which contains:
  - `load_log` and `task_histories`: complete.
  - `checkpoint_ratios(history)`: you write it. Returns `(x, total_ratio, remaining_ratio)` for each usable open row of a finished task.
  - `zero_claims(rows)`: you write it. Counts open rows that claim 0 hours remaining.
  - `band(values)`: you write it. Returns p10, p50 and p90 with the inclusive rule from MA102 week 12.
  - `cone_table(rows, edges)`: you write it. Pools the ratios and summarises each `x` bin.
  - `initial_bias(rows)`: you write it. Median of actual ÷ first estimate over finished tasks.
  - `main`: complete. Prints the table. On the starter it prints the log size and a note that functions are still TODO.
  - `write_lab06_csv`: complete. `python cone.py <log> --lab06 <out.csv>` converts your jam log to lab 06's one-row-per-task format, so week 6's module can compute your plan ratio and skew penalty from the same data.
- [`lab09-starter/test_cone.py`](lab09-starter/test_cone.py): 8 unit tests. Do not edit it. All 8 fail on the starter.
- [`lab09-starter/jam_log_sample.csv`](lab09-starter/jam_log_sample.csv): the invented 8-team sample from the lecture (52 tasks, 184 rows).
- Your team's `jam_log.csv` from lab 08, and the class's pooled log (the lecturer posts it after the in-class activity).
- The interactive [`examples/w09-cone-of-uncertainty.html`](../examples/w09-cone-of-uncertainty.html).

From the `lab09-starter` folder:

```
python cone.py
python -m unittest test_cone -v
python cone.py ../../<your repo>/jam_log.csv
```

## Steps

### Part A: the code (50 minutes, individual)

1. Run the tests and note which fail.
2. Implement `checkpoint_ratios`. Use the formulas from lecture section 2. Return `[]` for any task whose last row isn't `done`. Skip open rows with `remaining_est == 0`.
3. By hand, compute the four rows for task T01 in lab 08's template log. Confirm they match the lecture's table and `test_spawner_ratios`.
4. Implement `zero_claims`, `band`, `cone_table` and `initial_bias`. In `cone_table`, a bin with fewer than two points gets `None` for both bands.
5. Run `python cone.py`. Your printout must match the lecture's pooled table: bias 1.50, 6 zero claims, and the four bins with the same n, percentiles and spreads.
6. In two or three sentences, explain why the first bin has the same p50 (1.50) in both views, and why that stops being true in later bins.

### Part B: your data (40 minutes, team)

7. Run `check_log.py` from lab 08 on your team's log, then run `cone.py` on it. Paste the printout into your notes.
8. Paste your log into the interactive. Screenshot both views.
9. List every cut task with its first estimate, its spent hours when cut, and the lower bound on its ratio. Recompute your median with the cut tasks included at their lower bounds.
10. Convert your log with `--lab06` and run your lab 06 module on it. Record your median and plan ratio `R`. On the sample log they are 1.50 and 1.69 (222.5 / 132). Compare yours with week 6's invented cohort (median 1.00; plan ratio 1.48 with no size rule, 1.06 with the split rule) and compute the buffer `b = 1 − 1/R` your final project should hold back.
11. Run `cone.py` on the class's pooled log. Compare its first-bin and last-bin spreads, in both views, with the sample's and with Little's factor of 3 to 4. Is your class's remaining view a pipe or a cone?

### Part C: the post-mortem (at home, team)

12. Hold the 90-minute meeting from lecture section 3. Use the data from Part B on screen.
13. Write the post-mortem, at most 1,500 words, with these sections:
    - **What we made.** One paragraph and the link to the `v0.1.0` build.
    - **The numbers.** Your cone table (both views), median ratio with and without cut tasks, plan ratio and the buffer it implies, zero-claims count, planned versus shipped must and should cards, freeze hour and post-freeze changes.
    - **What went right.** Three to five items, each pointing to evidence (a log row, a commit, a board image).
    - **What went wrong.** Three to five items, blameless, each with evidence.
    - **Three changes.** Each with an owner and a check you can apply in week 13.
14. Each team member reads the draft and signs off in the repository (a commit that adds their name to a `signoff.txt`).

## Deliverable

A zip with your completed `cone.py` (all 8 tests pass; printout on the sample matches the lecture), a PDF with the answers to steps 3, 6, 9, 10 and 11 and the screenshots from step 8, and your team's post-mortem PDF with the sign-off commit hash.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Code and tests (25%) | All 8 tests pass; sample printout matches the lecture; step 6 explanation uses the weighted-average argument | All tests pass; explanation vague | Some tests fail | Most tests fail |
| Analysis of own data (25%) | Both views read correctly; cut tasks included as lower bounds; class comparison states pipe or cone with numbers | Analysis correct, cut tasks or class comparison thin | Numbers reported without interpretation | Missing |
| Post-mortem evidence (25%) | Every went right and went wrong item points to evidence; blameless throughout | Most items have evidence | Items are opinions; some name people | Missing |
| Three changes (25%) | Each change follows from the data, has an owner and a check that can be applied in week 13 | Changes have owners but weak checks | Changes are vague ("communicate better") | Missing |
