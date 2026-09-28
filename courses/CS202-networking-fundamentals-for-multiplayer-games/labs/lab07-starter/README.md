# Lab 07 starter

Standard library only. Run with the course Python (`.venv/bin/python` at the repository root, or any Python 3.10+), from inside this folder.

- `snapcodec.py`: the week 7 entity format (five fields, 12 bytes), full snapshots, a decoder, the lecture's 64-entity arena, and a lossy network simulation. You write `encode_delta` and `apply_delta`.
- `python snapcodec.py --check` must print `all checks passed`. It tests the sizes from the lecture (906, 223 and 10 bytes), both round trips and the expected-delta formula.
- `python snapcodec.py --sim --loss 0.05 --seed 1` runs 30 seconds at 20 Hz with both baseline policies and prints bytes per snapshot, kbit/s and how often the client ends up wrong.
