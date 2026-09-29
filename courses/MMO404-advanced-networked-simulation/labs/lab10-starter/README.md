# Lab 10 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root).

1. `python consistency.py --check` tests `conflict_p`, `forward_latency`, `count_conflicts`, the `DamageCounter` methods, the `VectorClock` methods, `happened_before` and `concurrent` against the week 10 lecture. It fails with `NotImplementedError` until you fill in the TODOs.
2. `python consistency.py --compare` prints, for claim rates 0.01 to 5 per second, the formula, the fixed-window simulation and the tick-aligned simulation side by side.
3. `python consistency.py --sweep conflicts.csv` writes the conflict share for claim rates from 0.01 to 10 per second, tick-aligned at 10 Hz, flushed, and tick-aligned at 30 Hz.

Expected once finished: `all checks passed`, and the three columns of `--compare` within half a percentage point of each other. Each command runs in a few seconds.
