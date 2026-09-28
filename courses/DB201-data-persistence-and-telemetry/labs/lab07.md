# DB201 · Lab 07: Ranks at scale

**Week:** 7 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** one of the SQL labs (SQL labs are 40% of the course)

**Lecture:** [Week 07, NoSQL and key-value stores (Redis)](../lectures/w07-nosql-and-key-value-stores-redis.md)

## Objective

Measure what a rank lookup costs in SQL at different positions on a leaderboard, build the skip-list lookup Redis uses for `ZREVRANK`, and compare both with a periodically rebuilt rank table. Finish with a recommendation, backed by your own numbers, for a 2-million-player board.

## Starter materials

All in [`lab07-starter/`](lab07-starter/):

- `rank_lab.py`: builds an in-memory SQLite board with unique scores and an index on `score`; contains a skip list with spans whose insert is written for you; runs correctness checks against brute force; prints a timing table. You complete three functions marked `TODO`.

You need Python 3.10 or later. No packages to install. Run `python rank_lab.py --check` for the tests only, and `python rank_lab.py` for tests plus the timing table. Until you finish the TODOs, the script stops with "Not implemented yet".

No Redis server is needed. The skip list in the starter follows the same design as Redis sorted sets (a skip list whose lanes record spans, plus a hash table from member to score), written in Python so you can read and change it. If you have Redis installed, the optional step 7 compares it with the real thing.

## Steps

1. **Read the insert (15 min).** Read `SkipList.zadd`. On paper, draw a skip list with 6 members and 3 lanes and fill in every `span` value. Check: the spans along any one lane add up to the number of members.
2. **Part A, SQL rank (15 min).** Write `rank_sql` as one statement that counts players with a strictly higher score and adds one. Run `EXPLAIN QUERY PLAN` on it and paste the output into `RESULTS.md`. It should say `USING COVERING INDEX ix_players_score`.
3. **Part B, skip-list rank (30 min).** Write `SkipList.zrevrank`. Walk from the top lane down, moving forward while the next key is less than or equal to the target and adding spans. Count each forward move in `self.last_steps`. The check fails if a lookup takes more than `8 × log₂ N` steps, which catches a walk that only uses the bottom lane.
4. **Part C, snapshot (15 min).** Write `build_snapshot` with `RANK() OVER (ORDER BY score DESC)` into a `rank_snapshot` table keyed by player ID. Run `--check` until all three parts pass.
5. **Time it (20 min).** Run the full script at 200,000 players, then at 1,000,000 (`--players 1000000`). Copy both tables into `RESULTS.md`. Compute the mean `ns/entry` for ranks of 10,000 and above. That is your `c`.
6. **Fit and predict (at home).** Using your `c`, predict the SQL time at the median rank for 2,000,000 players and the CPU-seconds per second at 2,000 lookups per second spread evenly over the board. Plot SQL time against rank for your 1,000,000-player run on log-log axes, with the model line `(r − 1) × c` on top.
7. **Optional, real Redis (at home).** If you have `redis-server` and `pip install redis` in a virtual environment, load the same 1,000,000 scores with `ZADD` in pipelined batches of 10,000 and time `ZREVRANK` at the same ranks from Python. Report the round trip separately from the command time (`redis-cli --latency`).

## Deliverable

A zip or repository link with:

- `rank_lab.py` with your three functions, passing `--check`.
- `RESULTS.md` with the query plan, both timing tables, your value of `c`, the plot, and your predictions from step 6.
- A memo of at most 300 words: for a 2,000,000-player arena ladder where each player checks their rank after every match (peak 2,000 lookups a second), recommend live SQL, a snapshot every N minutes (pick N), or a Redis sorted set. Use your numbers. Name what the chosen option costs (staleness, memory, rebuild after a crash) and how you would handle it.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Correctness | All three parts pass `--check`; `zrevrank` uses spans on every lane and counts steps correctly | Passes, but step counting or `None` handling is off | One or more parts fail | 30% |
| Measurement | Both tables, query plan, `c` computed from ranks ≥ 10,000 with the method shown | Tables present, `c` computed loosely or from too few points | Missing or copied from the lecture | 25% |
| Model check | Log-log plot with the model line; predictions for 2M players with arithmetic shown and a sentence on where the model and data disagree | Plot or predictions, not both | Missing | 20% |
| Recommendation | Clear choice justified by the student's own numbers, with its costs named and a plan for each | Choice made, justification generic | No recommendation, or contradicts the measurements | 25% |
