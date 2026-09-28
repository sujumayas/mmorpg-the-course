# Lab 04 starter

Standard library only. Run with the course Python (`.venv/bin/python` at the repository root, or any Python 3.10+).

- `movement_check.py`: the week 4 model. Policy A is a server speed check with a percentage tolerance. Policy B is a per-tick command budget. `arrivals` and the report code are written. You write `min_tolerance`, `speed_check`, `tick_budget` and `min_budget`.
- `python movement_check.py --check` must print `all checks passed`.
- `python movement_check.py --table` then prints the table in section 2 of the lecture (20 ms of jitter needs a 66.7% tolerance or a budget of 5).
- `python movement_check.py --jitter 20 --budget 4 --cheat 2` runs one scenario under both policies.
