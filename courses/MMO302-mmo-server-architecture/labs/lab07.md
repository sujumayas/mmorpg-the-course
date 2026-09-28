# MMO302 · Lab 07: Persistence strategies under crash

**Week:** 7 ([lecture](../lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** labs (40% of the course grade). Your event log is reused in lab 08's audit and in the final world server.

## Objective

Implement two of the lecture's persistence strategies, write-behind with dirty tracking and an event log with group commit and snapshots. Crash them on purpose and check that the commits, bytes, lost changes and replayed events you measure match the section 2 formulas. Then explain every place where they do not.

## Starter materials

- [`lab07-starter/persistence.py`](lab07-starter/persistence.py) is Python 3, standard library only. It provides a `Database` that counts commits and bytes, an `apply` function for events, the `WriteBehindStore` and `EventLog` classes with five `TODO` stubs, and a `run` function that simulates a shard in 10 ms steps (200 players by default, 0.5 changes per player per second, each change on one of three fields). Time is in integer milliseconds throughout, so you never compare floats.
- [`lab07-starter/test_persistence.py`](lab07-starter/test_persistence.py) has six tests. All six fail on the starter and pass on a correct solution. Run them with `python -m unittest test_persistence.py` from inside `lab07-starter/`.
- Running `python persistence.py` prints "not run yet" until the stubs are filled in. After that it prints commits per second, kB per second and changes per second for both strategies and one crash for each.
- The lecture's section 2 formulas and the `examples/w07-persistence-strategies.html` interactive once it is built.

## Steps

### Part A: write-behind (40 min)

1. Implement `WriteBehindStore.add` (TODO 1). Update the in-memory value, mark the field dirty for that player, count the change, and record the time of the oldest unflushed change.
2. Implement `flush` (TODO 2). Write one `db.commit` per dirty player containing only that player's dirty rows, sized `rows × ROW_BYTES`, then clear the dirty marks and the counters.
3. Implement `crash` (TODO 3). Memory is gone, so rebuild it from `db.rows` and return how many changes never reached the database.
4. Run the three write-behind tests. Then run `run("write-behind")` for `flush_ms` of 1,000, 5,000, 10,000 and 30,000. Record commits per second and kB per second in a table next to the lecture's predictions `N / F` and `(N / F) × min(c × F, h) × s` with `h = 3`.

### Part B: event log (40 min)

5. Implement `EventLog.tick` (TODO 4). At each group-commit boundary, commit all pending events as one `db.commit` and move them to `durable`. Skip empty commits. At each snapshot boundary, build the state of every durable event and store it with the count it covers.
6. Implement `crash_and_recover` (TODO 5). Pending events are lost. Copy the snapshot and replay only the durable events after it. Return the state, the number replayed and the number lost.
7. Run all six tests.
8. Crash the event log at 30, 60, 90 and 119 seconds with `snapshot_ms = 60_000`. Record events replayed and compare them with `N × c × (t mod K)`.

### Part C: explain the gaps (30 min)

9. Your measured event-log commits per second will be well below the lecture's `1 / g = 100`. Explain why, and show that `(1 / g) × (1 − e^(−λg))` predicts your number, where `λ` is the shard's events per second and `λg` is the expected number of events per 10 ms window. (Hint: a window with no events commits nothing.)
10. Your measured write-behind kB per second will be below the prediction with `h = 3`. The number of changes a player makes in one window is random, with mean `c × F`, and each change picks one of 3 fields. Show that a given field is left untouched with probability close to `e^(−c × F / 3)`, compute the expected number of distinct fields per flush, and use it to correct the prediction. Your corrected value should land within 5% of the measurement.
11. Add a slow-database mode to `run` in which every flush is delayed by an extra 15 seconds. Measure `oldest_dirty_age` just before each flush. Write two sentences on why the real loss window is not `F`.

## Deliverable

- Your completed `persistence.py` passing all six tests, plus any code you added for Part C.
- A report of up to 2 pages with these contents:
  - The Part A table (four flush intervals, measured against predicted).
  - The Part B table (four crash times, measured against predicted).
  - The two corrected predictions from Part C, steps 9 and 10, with their arithmetic.
  - The slow-database result.
  - A 300-word persistence policy for the lecture's in-class survival MMO. Name the strategy and parameters for each kind of state and justify them with your own measurements.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Write-behind implementation | All three write-behind tests pass; coalescing and crash loss correct | Tests pass with a hard-coded shortcut, or crash loss off by one flush | Tests fail | 20 |
| Event log implementation | All three event-log tests pass; recovery uses snapshot plus tail, not full replay | Recovery correct but replays the whole log | Tests fail | 20 |
| Measured against predicted | Both tables complete, gaps under 10% or explained | Tables complete, gaps unexplained | Missing | 20 |
| Explaining the gaps (Part C) | Both corrected formulas derived and matching within 5%; slow-database result explained | One of the two correct | Missing | 20 |
| Policy memo | Per-state strategy with parameters, backed by the pair's own numbers, names one weakness | Policy plausible but not tied to measurements | Missing | 15 |
| Code quality | Readable, runs first time, parameters in one place | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
