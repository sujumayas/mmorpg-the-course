# DB201 · Lab 09: A migration under load

**Week:** 9 · **Time:** 2 hours in the lab plus up to 3 hours at home · **Weight:** one of the SQL labs (SQL labs are 40% of the course)

**Lecture:** [Week 09, schema migrations in a live game](../lectures/w09-schema-migrations-in-a-live-game.md)

## Objective

Run the durability migration from the lecture on a 1,000,000-row item table while a game thread keeps writing to it. Compare the one-statement backfill with batched backfills, check the measured stalls against `b / r`, fit `r` and `o` from your own runs, and turn the numbers into a migration plan for a 60-million-row production table.

## Starter materials

All in [`lab09-starter/`](lab09-starter/):

- `migration_lab.py`: builds `item_def` (500 types, each with a maximum durability) and `item_instance` in a temporary SQLite file, runs the expand step (`ADD COLUMN durability`), starts a `GameWriter` thread that updates 200 random items a second and records how long each write waits, runs a backfill, and prints a results table. The one-statement backfill is written for you. You complete `backfill_batched` and `fit_rate_and_overhead`.

You need Python 3.10 or later and nothing else. `python migration_lab.py --check` runs the tests on a 5,000-row table. `python migration_lab.py` runs the tests and then the experiment on 1,000,000 rows, which takes about half a minute. `--rows` and `--duty` change the inputs.

Two differences from PostgreSQL matter here, and the starter's docstring repeats them. SQLite allows one writer at a time for the whole database, so every game write waits while a batch runs. PostgreSQL makes only writes to rows the batch has touched wait. And SQLite runs inside your process with no network, so it updates rows much faster than the 20,000 rows a second the lecture assumed for a production PostgreSQL server, and its per-batch overhead is far smaller. The shape of the results carries over. The absolute numbers do not.

## Steps

1. **Predict first (10 min).** Read `backfill_one_statement` and `GameWriter.run`. Before running anything, write in `RESULTS.md` what you expect the game's worst wait to be during the one-statement backfill, and why.
2. **Part A, batched backfill (40 min).** Write `backfill_batched`. Each batch is one `BEGIN IMMEDIATE ... COMMIT` containing the ranged `UPDATE ... FROM item_def` and the progress upsert. Resume from `backfill_progress`. Sleep to keep the duty cycle. The checks test batch count, correct values, that rows already written by new code are left alone, that a finished job does nothing when run again, and that a duty cycle of 0.5 roughly doubles the elapsed time.
3. **Part C, the fit (15 min).** Write `fit_rate_and_overhead` as a least-squares line through `(b, mean batch time)`. The check uses synthetic data with `r = 100,000` and `o = 2 ms`.
4. **Run the experiment (15 min).** Run the full script at the default duty of 0.5. Copy the table into `RESULTS.md`. For each batched row, compute `b / r` from your fitted `r` and put it next to the measured max wait.
5. **Explain the floor (at home).** At small batch sizes the max wait stops falling at a few milliseconds. Find out why. Hint: time a single game write with no backfill running. Then read the comment in `GameWriter.__init__` and explain in three sentences why the starter polls the lock itself instead of using SQLite's built-in busy timeout. Try the built-in timeout (`connect(path)` with the default) and report what happens to the max wait at `b = 100`.
6. **Vary the duty cycle (at home).** Rerun with `--duty 0.25` and `--duty 1.0`. Check that the max wait barely changes while the total time moves as `1/d`, as the lecture's model predicts.
7. **Plan for production (at home).** Using the lecture's PostgreSQL numbers (`N = 60,000,000`, `r = 20,000`, `o = 5 ms`), a stall budget of one 50 ms server tick and a deadline of six hours, choose `b` and `d`, compute the total time, and write the full expand, migrate, enforce and contract sequence with the SQL for each step.

## Deliverable

A zip or repository link with:

- `migration_lab.py` with your two functions, passing `--check`.
- `RESULTS.md` with your prediction from step 1, the tables from steps 4 and 6 with `b / r` beside each measured max wait, your fitted `r` and `o`, and the explanation from step 5.
- A migration plan of at most 500 words for the 60-million-row table: `b`, `d` and total time with arithmetic; the SQL for each step; which server version ships at each step; how the job resumes after a crash; what you monitor while it runs and the number at which you would lower `d`.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Correct backfill | All checks pass; one transaction per batch including progress; range by primary key; idempotent filter; duty-cycle sleep | Passes, but progress is written outside the batch transaction or the range is found with `LIMIT` | Checks fail | 30% |
| Measurement and model | Tables at three duty cycles; `b / r` beside each max wait; fitted `r` and `o`; a sentence on where the model and the data disagree | One duty cycle, or no comparison with `b / r` | Missing or inconsistent with the script | 25% |
| Explanation of the floor | Identifies the game write's own commit time as the floor and explains how a polling busy handler with long sleeps inflates waits, with the measured effect | One of the two explained | Missing or wrong | 15% |
| Production plan | `b` from the stall budget and `d` from the deadline, with arithmetic; complete expand, backfill, enforce, contract sequence with SQL; resume and monitoring covered | Correct numbers, sequence or monitoring incomplete | Plan would stall trades or break old code during the deploy | 30% |
