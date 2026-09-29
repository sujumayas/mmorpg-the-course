# Lab 12 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root).

1. `python ai_budget.py --check` tests `tier_rate`, `model_tier_counts`, `cost_ms_per_s`, `nearest_grid`, `thinks_per_tick` and `budgeted_tick` against the week 12 lecture. It fails with `NotImplementedError` until you fill in the TODOs.
2. `python ai_budget.py --measure` prints monsters per tier and AI cost for the lecture's four player layouts, then times `nearest_brute` against your `nearest_grid`.
3. `python ai_budget.py --sweep ai.csv` writes the model's tier counts and cost for 1 to 1,000 spread players.

Expected once finished: `all checks passed`, and the lecture's table reproduced exactly (939, 5,000 and 4,001 monsters per tier for 200 spread players). Each command runs in a few seconds.
