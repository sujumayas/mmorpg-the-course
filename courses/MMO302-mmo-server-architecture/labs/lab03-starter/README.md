# MMO302 lab 03 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root) or any Python 3.10 or later.

- `aoi.py`: seeded world generator (mulberry32, seed 302, identical to the week 3 interactive), brute-force radius sets, and the pacing test. You write `build_grid`, `candidates`, `grid_count`, `grid_radius_sets` and `Hysteresis.step`.
- `test_aoi.py`: checks your code on a four-player example, on the lecture's six worlds, against brute force, and on the hysteresis table. Run `python test_aoi.py` until it prints `all lab 03 tests passed` (it takes a few seconds, because it runs brute force twice).

Then:

```
python aoi.py --table
python aoi.py --boundary
python aoi.py --bench
```
