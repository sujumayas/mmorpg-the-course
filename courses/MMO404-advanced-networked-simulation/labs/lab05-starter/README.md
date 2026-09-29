# Lab 05 starter

Standard library only. Run from this folder with Python 3.10 or later.

1. `python lod.py --check` tests `smooth_interval`, `guess`, `needs_update` and the `Shaper` class against the week 5 lecture, including a dead-reckoning run on a circle. It fails with `NotImplementedError` until you fill in the TODOs.
2. `python lod.py --hub hub.csv` runs a seeded 300-entity hub for 60 seconds at 20 Hz under distance tiers and under error-driven updates (θ = 1°, 5-second heartbeat). A world boss spawns at t = 30 s. It prints quiet and panic bandwidth and angular error, and writes one row per second.
3. `python lod.py --hub hub_shaped.csv --shaped` sends both policies through a 96 kbit/s token bucket. `--budget 48` picks any rate in kbit/s.

Expected result once finished: `all checks passed`. Unshaped, tiers use 147.8 kbit/s in both halves and error-driven updates never exceed 1.00 degree of error.
