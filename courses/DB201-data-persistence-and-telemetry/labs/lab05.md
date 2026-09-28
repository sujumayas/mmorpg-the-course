# DB201 · Lab 05: Split saves, real crashes and commit cost

**Week:** 5 ([Transactions and ACID](../lectures/w05-transactions-and-acid.md))
**Time:** one 2-hour lab session plus up to 1.5 hours at home
**Work:** individually

## Objective

Confirm the split-save model by simulation and derive its closed form. Kill a real process halfway through a trade and see what autocommit and a transaction each leave on disk. Then measure what durability costs per commit and how batching changes it. By the end you should be able to write a persistence policy that says, for each game action, how it is saved and why.

## Starter materials

- Python 3.10 or later, standard library only. In this repository use `.venv/bin/python`.
- `labs/lab05-starter/acid_lab.py`, which contains:
  - `split_save_trial` and `split_save_rates(T, horizon)`: complete. A Monte Carlo of two characters saved on independent timers with a crash at a random time after a trade.
  - `split_save_formula(d_over_T)`: you write it (Part A).
  - `make_world` and `trade_worker(path, mode)`: complete. The worker runs in a child process, performs two of the four trade writes, and calls `os._exit(1)`.
  - `audit(path)`: you write it (Part B).
  - `commit_rate(path, n_trades, synchronous, batch)`: complete. It sets `PRAGMA fullfsync = ON`, which matters on macOS and is ignored elsewhere.
- Run `python acid_lab.py split`, `python acid_lab.py crash`, `python acid_lab.py commit`, or `python acid_lab.py` for all three.
- Reference output (Apple silicon, macOS, SQLite 3.53): split-save dupe and loss rates of 0.166 and 0.168 for crashes within 300 s at `T = 300`; about 3.9 ms per commit with `synchronous = FULL`.

## Steps

### Part A: the split save (35 minutes)

1. Run `python acid_lab.py split`. Record the dupe, loss and ok rates for each crash horizon.
2. Implement `split_save_formula` with `p = min(d/T, 1)`. Print it for `d/T = 0.1, 0.5, 0.9, 1.5` and check two values by hand.
3. The horizon of 300 s gives crashes uniform on `[0, T)`. Derive the average `P(dupe)` over that range by integrating your formula, and compare it with the simulation.
4. Explain why the horizon of 3,000 s gives much lower rates, in terms of the fraction of crashes that land after both characters have saved.
5. Modify `split_save_trial` so the giver is always saved at the moment of the trade (the lecture's "take before give" persistence). Rerun and report the new dupe and loss rates.

### Part B: a real crash (30 minutes)

6. Run `python acid_lab.py crash`. Record the gold and sword owner after restart for both modes.
7. Implement `audit(path)` so it returns total gold, the sword's owner, and a verdict of "consistent" or "HALF A TRADE". Rerun and paste the output.
8. Move the `os._exit(1)` line in `trade_worker` to each of the four possible positions (before the first write, after the first, after the second, and after the item move but before `COMMIT`). For each position and mode, record the verdict. Present a 4 × 2 table.
9. In one paragraph, explain why the transaction column is "consistent" in every row. Name the file SQLite uses to undo the partial transaction in WAL mode and in the default rollback-journal mode.

### Part C: what durability costs (25 minutes)

10. Run `python acid_lab.py commit`. Record trades per second and milliseconds per commit for each row.
11. Add a row with `batch = 1000` as the TODO asks. Explain why the milliseconds per commit stay roughly flat while trades per second grow.
12. Set `PRAGMA fullfsync` to OFF in `commit_rate` and rerun on macOS (skip this step on Linux or Windows and say so). Record the new time per commit and explain what it measures.
13. From your numbers, compute the largest number of players a server could support if every loot pickup (one per player every 2 s) were its own synchronous commit with no batching, and the batch size needed for 5,000 players.

### Part D: the policy (at home)

14. Write a half-page persistence policy for the lecture's eight game actions. For each, choose periodic save, asynchronous commit or synchronous transaction, justify it with a number from this lab or the lecture, and say which ACID property you are relaxing, if any.

## Deliverable

Your modified `acid_lab.py`, a results file with the tables from steps 1, 2, 5, 8, 10, 11 and 13, the paragraph from step 9, and the policy as a PDF.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Split-save model (25%) | Formula correct and checked by hand; average derived by integration and matched to simulation; step 5 rates explained | Formula and simulation agree, derivation sketchy | Formula wrong or unchecked | Not attempted |
| Crash experiment (25%) | `audit` correct; full 4 × 2 table; recovery mechanism named for both journal modes | Table complete, explanation thin | Only the default crash point tested | Missing |
| Commit cost (25%) | All rows measured, the flat per-commit time explained as one flush per batch, macOS `fullfsync` effect explained, step 13 computed | Measurements and step 13 present, explanation vague | Measurements only | Missing |
| Policy (25%) | Eight actions, each with a number and the relaxed property named; trades and money always synchronous | Policy sound, numbers missing for some actions | A trade or purchase left to periodic save | Missing |
