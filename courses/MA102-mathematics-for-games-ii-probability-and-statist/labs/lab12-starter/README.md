# Lab 12 starter

- `playtest_w12.csv`: 40 testers of a fictional dungeon (`tester_id`, `experience`, `clear_minutes`, `deaths`, `minutes_idle`, `reached_boss`, `beat_boss`, `difficulty_rating`). `clear_minutes` runs from entering the dungeon to killing the boss or quitting. Synthetic data.
- `lab12_starter.py`: loads the CSV and gives you `inclusive_percentile(values, p)`, the week 12 rule, so your quartiles match the answer key. Standard library only; pandas and numpy work too.
- Spreadsheet users: open the CSV directly and use `PERCENTILE.INC`, which follows the same rule.
- `mulberry32.py` and `make_playtest.py`: instructor only. `python make_playtest.py` regenerates the CSV (seed 12). Change the seed or the planted rows for a new offering.
