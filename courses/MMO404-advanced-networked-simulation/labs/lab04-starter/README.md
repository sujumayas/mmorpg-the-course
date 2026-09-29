# Lab 04 starter

Standard library only. Run from this folder with Python 3.10 or later.

1. `python priority.py --check` tests `falloff`, `priority`, `priority_speed`, `fair_rates` and `Accumulator.pick` against the numbers in the week 4 lecture. It fails with `NotImplementedError` until you fill in the TODOs.
2. `python priority.py --scene scene.csv` runs a seeded 400-entity scene for 1,000 ticks at 20 Hz with a budget of 20 updates per tick, once per falloff (inverse, square, flat). It prints and saves each class's mean update interval and mean angular error.
3. `python priority.py --scene scene_speed.csv --speed` does the same with the speed term from lecture section 3.

Expected result once finished: `all checks passed`. With the inverse falloff and no speed term, the three player classes (party, enemies, far players) show angular errors within about 0.3 degrees of each other.
