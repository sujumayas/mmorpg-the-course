# Lab 11 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root).

1. `python physics_budget.py --check` tests the sleep rule (`update_sleep_time`, `island_should_sleep`, `t_move_for`), the budget model (`awake_little`, `awake_exact`, `cpu_ms_per_s`) and the seam functions (`islands`, `island_owner`) against the week 11 lecture, then runs a short live world. It fails with `NotImplementedError` until you fill in the TODOs.
2. `python physics_budget.py --measure` runs a 2,000-body world at kick rates 10, 50, 200 and 800 per second and prints Little's law, the exact form and the measured awake count.
3. `python physics_budget.py --sweep budget.csv` writes the awake count, CPU and share of the 200 ms/s budget for a 20,000-prop zone at kick rates from 10 to 1,000 per second.

Expected once finished: `all checks passed`, and measured counts within a few percent of the exact form. Each command runs in under ten seconds.
