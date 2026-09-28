# MMO302 lab 02 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root) or any Python 3.10 or later.

- `layers.py`: a deterministic population of 3,000 players (1,800 of them in 116 guilds) arriving at a zone. You write `assign_random`, `assign_guild` and `cohesion`. The population generator, the contention model and the report are provided.
- `test_layers.py`: run `python test_layers.py` until it prints `all lab 02 tests passed`.

Then compare policies with `python layers.py` (20 layers, cap 180) and try other settings with `--layers` and `--cap`.
