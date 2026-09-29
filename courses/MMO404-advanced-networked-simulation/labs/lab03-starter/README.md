# Lab 03 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root).

1. `python partition.py --check` tests `crowd_split_us`, `kd_headcount` and `kd_by_load` against the week 3 lecture. It fails with `NotImplementedError` until you fill in the TODOs.
2. `python partition.py --compare` partitions the seeded 3,000-player world across 16 servers three ways and prints the busiest server's load, the mean load and the cross-server pairs.
3. `python partition.py --crowd 300` prints the per-server and total load when one 300-player crowd is split across 1 to 32 servers.

Expected once finished: `all checks passed`; the static grid's busiest server at 68.0 ms and `kd_headcount` at 64.7 ms with 28.7% of pairs cut; `kd_by_load` under 50 ms.
