# Lab 13 starter

- `drops.csv`: 3,000 simulated boss kills (`kill_id`, `player_id`, `dropped`), 150 players with 20 kills each. The drop rate is hidden.
- `intervals_template.py`: functions to fill in for steps 1 to 3 (Wald, Wilson, growing sample, coverage).
- `coverage_template.csv`: the 16-cell `coverage` grid for step 3. Fill in both columns. If you prefer a spreadsheet, open this file and add columns `n`, `k`, `p_hat`, `se`, `wald_low`, `wald_high`, `wilson_low`, `wilson_high` on a second sheet.
- `mulberry32.py`: the seeded generator the course interactives use. Use seed 13.
- `make_drops.py`: instructor only. Run `python make_drops.py <rate>` to regenerate `drops.csv` with a new hidden rate before each offering.
