# MMO309 Lab 01 starter: the threat ledger

Standard library Python 3.10 or later. From the repository root, use `.venv/bin/python`.

- `threat_ledger.py`: loading and reporting are written. You write `ale`, `rank`, `net_value` and `stable_top`.
- `threats.csv`: the week 1 lecture's eight threats, with low and high cost estimates added.
- `controls.csv`: the lecture's five controls.

```
python threat_ledger.py --check      # every check fails until you write the four functions
python threat_ledger.py --table      # rankings, ALE ranges, control net values
python threat_ledger.py --table --threats my_threats.csv --controls my_controls.csv
```

Your own CSV files must keep the same columns.
