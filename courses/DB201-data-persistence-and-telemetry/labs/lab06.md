# DB201 · Lab 06: Reproduce the dupe, then make it impossible

**Week:** 6 ([Race conditions and the duplication bug](../lectures/w06-race-conditions-and-the-duplication-bug.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; pair up for step 12

## Objective

Reproduce the trade dupe on a real database, deterministically and then with real threads. Count how many of the 20 interleavings duplicate the sword, and check the timing model against a stress test. Then implement three fixes that make the dupe impossible in every interleaving. This lab is the core of the final inventory service, so the fixed handlers you write here are the ones you will build on.

## Starter materials

- Python 3.10 or later, standard library only. In this repository use `.venv/bin/python`.
- `labs/lab06-starter/dupe_lab.py`, which contains:
  - `make_world`, `connect`, `load`, `save`, `copies_in_blobs`, `copies_in_rows`: complete. A world with a giver who owns sword 5001 and two receivers, stored both as JSON inventories (blob model, with a `version` column) and as an `items` table (row model).
  - `naive_trade(con, receiver)`: complete. The lecture's `R G T` handler, written as a generator that yields after each database step.
  - `run_interleaving(handler, order, path, counter)`: complete. A deterministic scheduler. `order` is a string such as `"112122"`. A handler that yields `WAIT` (it could not get a lock) gives its turn to the other trade.
  - `all_orders()` and `table()`: complete. Run all 20 interleavings and count dupes.
  - `stress(handler, counter, attempts)`: complete. Real threads, each trade delayed uniformly in `[0, 3 ms]`, 0.5 ms of simulated work between steps.
  - `conditional_trade`, `locked_trade`, `versioned_trade`: you write them (Part B).
- Run `python dupe_lab.py` (all handlers, then a 300-attempt stress test), `python dupe_lab.py --order 121212` to trace one interleaving, or `python dupe_lab.py --stress 2000`.
- Reference output (lecturer's machine): naive handler dupes in 18 of 20 interleavings; stress-test dupe rate between 60% and 68% across runs. The three fixes, correctly written, show 0 of 20 and 0.0%.

## Steps

### Part A: reproduce it (35 minutes)

1. Run `python dupe_lab.py` without changes. Record the naive handler's table and its stress-test dupe rate.
2. Trace `112122`, `121212` and `211221` with `--order`. For each, copy the printed states into a table and mark the step where a trade's copy of the giver's inventory becomes stale.
3. Change `naive_trade` so it takes before it gives (`R T G`) and rerun the table. Report the count and explain it with the lecture's dupe condition. Restore the original order afterwards.
4. The stress test uses `J = 3 ms`. Estimate the race window `w` from your measured dupe rate by solving `P = 1 − (1 − w/J)²`. Then change `work_ms` to 0.1 and to 1.0, predict the new dupe rate from your `w` model, and measure it. Report predicted against measured.

### Part B: three fixes (50 minutes)

5. **B1, conditional update (row model).** Implement `conditional_trade` with one `UPDATE items ... WHERE item_id = ? AND owner_id = ?` and a `rowcount` check. It must yield exactly once.
6. **B2, lock (blob model).** Implement `locked_trade`: `BEGIN IMMEDIATE`, then the three naive steps, then `COMMIT`. If `BEGIN IMMEDIATE` raises `sqlite3.OperationalError`, yield `WAIT` and try again in a loop. In a comment, write the PostgreSQL version using `SELECT ... FOR UPDATE`.
7. **B3, version check (blob model).** Implement `versioned_trade`. Read the items and the version, take with `UPDATE ... WHERE character_id = ? AND version = ?`, return `"conflict"` on zero rows, and only then give.
8. Run `python dupe_lab.py`. All three fixes must show 0 of 20 and a 0.0% stress-test rate. Paste the outcome columns (`trade1=`, `trade2=`) for `121122` under each fix and explain why they differ between fixes.
9. Run `python dupe_lab.py --stress 2000` and record the rates. A fix that shows even one dupe in 2,000 attempts is wrong. Find the bug.

### Part C: deadlock and ordering (20 minutes)

10. Add a second world item, 250 gold on character 2, and write `swap_trade(con, a, b)` for a two-way trade (sword from 1 to 2, gold from 2 to 1) that locks the two characters in the order given. Using two connections and `BEGIN IMMEDIATE` is not enough to show a deadlock in SQLite, because it has one database lock. Explain why in two sentences.
11. Write the PostgreSQL version of `swap_trade` as SQL (no need to run it) that locks both characters with one `SELECT ... ORDER BY character_id FOR UPDATE`. Explain why it cannot deadlock against another `swap_trade` in the opposite direction.

### Part D: the incident note (at home)

12. With a partner, write a one-page incident note for this report from a live game: "Mailing an item to an alt and logging out quickly sometimes leaves a copy in the sender's bags." Classify the root cause with the lecture's three-row table (race, split save, trusting the client), give the evidence that would confirm it (which queries you would run on which tables), propose the fix and the kill switch, and state whether you would roll back and why.

## Deliverable

Your modified `dupe_lab.py`, a results file with the tables from steps 1 to 4, 8 and 9, your answers to steps 10 and 11, and the incident note as a PDF.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Reproduction and traces (20%) | Three traces with the stale step marked; the `R T G` count explained by the dupe condition | Traces correct, explanation thin | One trace, or stale step not identified | Not attempted |
| Timing model (15%) | `w` estimated from data; predictions made before measuring for two `work_ms` values; errors discussed | Predictions present, made after measuring | Measurements without a model | Missing |
| Fixes (35%) | All three fixes pass 20 of 20 and 2,000 stress attempts; `121122` outcomes explained; PostgreSQL comment for B2 correct | Two fixes pass, or all pass with thin explanation | One fix passes | None pass |
| Deadlock (10%) | SQLite limitation explained; PostgreSQL SQL correct with ordered locking and a clear argument | SQL correct, argument vague | Ordering missing | Missing |
| Incident note (20%) | Root cause classified with evidence queries, fix, kill switch, and a reasoned rollback decision | Classification and fix sound, evidence thin | Fix proposed without classification | Missing |
