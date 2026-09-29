# Lab 06 starter

Standard library only. Run from this folder with Python 3.10 or later.

1. `python battle.py --check` tests `work`, `speed` (MMO302 week 12's model), `stream_Bps` and a grid-based `count_pairs` against the week 6 lecture and a brute-force reference. It fails with `NotImplementedError` until you fill in the TODOs.
2. `python battle.py --run battle.csv` builds seeded battles of 250 to 4,000 pilots in six fleets, counts the pairs within a 5 km weapon range, and reports work per game-second, speed and per-client event streams. It takes about a second once `count_pairs` uses the grid.
3. `python lockstep.py --check` runs the same 300-unit skirmish as two separate processes with different `PYTHONHASHSEED` values and compares their per-tick checksums. It fails until you implement `first_divergence`, and then it fails again, because the simulation has a determinism bug for you to find and fix. The two seeds are fixed, so the failure is the same on every run. To run one machine by hand, set the seed yourself, for example `PYTHONHASHSEED=1 python lockstep.py --machine`.

Expected result once finished: `all checks passed` from both scripts. About 68% of pairs are in range at every size, and at 4,000 pilots the node sits at the 10% floor.
