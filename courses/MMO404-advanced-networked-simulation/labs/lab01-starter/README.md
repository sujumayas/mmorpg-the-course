# Lab 01 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root).

1. `python zone_capacity.py --check` tests `aoi_fraction`, `pair_fraction`, `tick_ms`, `capacity` and `count_pairs` against the week 1 lecture. It fails with `NotImplementedError` until you fill in the TODOs.
2. `python zone_capacity.py --measure` builds seeded 1,000-player zones with hot-spot shares 0, 0.1, 0.25, 0.5 and 1, counts the real interacting pairs and compares them with the model.
3. `python zone_capacity.py --sweep capacity.csv` writes the capacity for hot-spot shares 0.00 to 1.00, on today's CPU and on one twice as fast.

Expected once finished: `all checks passed`, and measured/model ratios between 0.93 and 1.00.
