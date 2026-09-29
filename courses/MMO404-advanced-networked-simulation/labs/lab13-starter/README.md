# Lab 13 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root).

1. `python cost_model.py --check` tests `cost_terms`, `shares`, `lever_saving`, `ceiling`, `spot_fill_limit` and `blended_price` against the week 13 lecture. It fails with `NotImplementedError` until you fill in the TODOs.
2. `python cost_model.py --levers` prints the lecture's lever table for the baseline.
3. `python cost_model.py --sweep cost.csv` writes capacity, the three cost terms and the compute share for tick rates from 5 to 128 Hz.

`zone_capacity` is given. It is week 1's capacity with the budget scaled to the tick rate. Expected once finished: `all checks passed`, and a lever table whose savings match the lecture (2.4%, 1.5%, 27.6%, 20.7%).
