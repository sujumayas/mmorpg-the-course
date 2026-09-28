# MMO302 lab 01 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root) or any Python 3.10 or later.

- `crowd_cost.py`: the week 1 crowd cost model. You write `deliveries`, `layout`, `per_server`, `c_max` and `tick_ms`. The table printer, CSV sweep, timing probe and tick search are provided.
- `test_crowd_cost.py`: checks your functions against every number in the lecture's table. Run `python test_crowd_cost.py` until it prints `all lab 01 tests passed`.

Commands once the tests pass:

```
python crowd_cost.py --table
python crowd_cost.py --break-tick
python crowd_cost.py --measure
python crowd_cost.py --sweep sweep.csv
```
