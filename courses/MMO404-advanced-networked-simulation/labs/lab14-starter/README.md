# Lab 14 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root).

1. `python teardown.py --check` tests `implied_pair_ns`, `implied_player_us`, `speedup_needed`, `nearest_reference`, `sensitivity` and `dominant_assumption` against the week 14 lecture. It fails with `NotImplementedError` until you fill in the TODOs.
2. `python teardown.py --cases` prints the lecture's table of implied pair costs with the nearest hardware reference.
3. `python teardown.py --sweep FWST-8 fwst8.csv` writes the bound as each assumption moves across its range. Add your group's case to `CASES` and sweep it too.

Expected once finished: `all checks passed`, and 233 ns for FWST-8 with "main-memory fetch" as its nearest reference.
