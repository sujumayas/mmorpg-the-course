# MMO309 Lab 03 starter: the lag-tolerant movement validator

Standard library Python 3.10 or later. From the repository root, use `.venv/bin/python`.

- `movement_validator.py`: the spike simulation, the jump generator, the session log generator and the reports are written. You write `rate_allowed`, `credit_allowed`, `min_setting`, `gravity_violations`, `violations`, `flag_stats` and `best_k`.

```
python movement_validator.py --check                       # 15 checks, all fail on the starter
python movement_validator.py --table                       # the lecture's section 2 table
python movement_validator.py --tune --L 250 --precision 0.9
```

The session log is generated from a fixed seed by `make_log()`, so everyone gets the same 10,000 players over 7 days. Do not change the seed or the generator.
