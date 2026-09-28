# DB201 · Lab 08: The write-behind flusher

**Week:** 8 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** one of the SQL labs (SQL labs are 40% of the course)

**Lecture:** [Week 08, caching and write-behind](../lectures/w08-caching-and-write-behind.md)

## Objective

Finish a write-behind cache that coalesces changes, flushes them to SQLite in one transaction per batch and refuses stale writes. Then measure its write rate and its crash loss at several flush intervals, and check both against the lecture's model, `W = N × (1 − e^(−uT)) / T` and expected loss `T/2`.

## Starter materials

All in [`lab08-starter/`](lab08-starter/):

- `writebehind_lab.py`: the `char_state` table, a versioned upsert statement, a `WriteBehindCache` with `update` and `crash` written for you, a simulator that runs `N` players in simulated time with Poisson changes at rate `u`, correctness checks, and a results table. You complete `take_dirty` and `flush`.

You need Python 3.10 or later and nothing else. `python writebehind_lab.py --check` runs the tests. `python writebehind_lab.py` runs tests, the flush-interval table (2,000 players, `u = 2`, 30 simulated seconds) and a 200-crash loss test. Options `--players`, `--rate` and `--seconds` change the table's inputs.

Time is simulated, so the table takes seconds to produce, not minutes. The database writes are real.

## Steps

1. **Read the model and the upsert (10 min).** In `RESULTS.md`, explain in two sentences what the `WHERE excluded.version > char_state.version` clause prevents, and give one situation in a real MMO where it would fire.
2. **Part A, take_dirty (20 min).** Swap the dirty set for a new empty one before you build rows, and copy values into tuples. The checks include a change that arrives between `take_dirty` and the write. It must end up in the database on the next flush.
3. **Part A, flush (15 min).** One `with conn:` block, one `executemany`, count rows. Run `--check` until every line prints ok.
4. **Part B, the table (20 min).** Run the full script. Copy the table into `RESULTS.md`. Then run it again with `--players 5000 --rate 2 --seconds 20` and check the 1 s, 5 s and 30 s rows against the lecture's table (4,323, 1,000 and 167).
5. **Part C, crash loss (15 min).** The script crashes the cache 200 times at random moments with `T = 5` s. Record the mean and worst seconds lost. Change the crash test to `T = 30` (edit `run_table`) and record again. Do the means match `T/2`?
6. **Find the knee (at home).** For `u = 0.2` (experience gains) and `u = 5` (position), run the table at `T` values of `0.2/u`, `1/u`, `3/u` and `10/u`. For each `u`, report the percentage cut at `3/u`. Plot rows per second against `T` on log-log axes for both rates, with the model curves drawn in.
7. **Policy memo (at home).** Use the five data types and rates from the lecture's in-class activity. Pick a policy for each and compute the total write rate for a 3,000-player shard from the model, then confirm the two write-behind rows with the simulator.

## Deliverable

A zip or repository link with:

- `writebehind_lab.py` with your two methods, passing `--check`.
- `RESULTS.md` with the answer from step 1, the tables from steps 4 and 5, the knee results and plot from step 6.
- A policy memo of at most 400 words: one row per data type with its policy, `T` if write-behind, its write rate and the loss you accept; the shard total; and one paragraph on what your flusher must do on logout, zone transfer and before a trade.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Correct flusher | All checks pass; swap-before-build, snapshot tuples, one transaction per batch | Passes, but one of the three rules is met by accident rather than by design (explained wrongly in step 1) | Checks fail | 30% |
| Model check | Tables for both runs, measured rates within 10% of the model, crash means compared with `T/2` for two values of `T` | One run or one crash setting only | Missing, or numbers inconsistent with the script | 25% |
| Knee analysis | Both rates run at four intervals; cut at `3/u` reported; plot with model curves; one sentence on why the knee moves with `u` | Numbers present, plot or explanation missing | Missing | 20% |
| Policy memo | Every data type has a justified policy with numbers; trades and item creation are write-through; logout and zone-transfer flushes specified | Policies given, some without numbers or with a risky choice unexplained | Generic or missing | 25% |
