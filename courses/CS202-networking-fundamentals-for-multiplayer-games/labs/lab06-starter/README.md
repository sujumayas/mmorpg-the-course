# Lab 06 starter

Standard library only. Run with the course Python (`.venv/bin/python` at the repository root, or any Python 3.10+).

- `reliability.py`: 16-bit sequence comparison, an ack tracker with a 32-bit ack field, and a redundant-input simulator. `loss_pattern` (the week 2 bursty-loss model) is written. You write the rest.
- `python reliability.py --check` must print `all checks passed`.
- `python reliability.py --table` prints the lecture's section 2 table.
- `python reliability.py --sim --p 0.05 --q 0.5 --k 3` simulates one hour of 60 Hz inputs. With the default seed, independent 5% loss and three copies loses 23 inputs (formula 27), and bursty loss with `q = 0.5` loses 2,702 (formula 2,700).
