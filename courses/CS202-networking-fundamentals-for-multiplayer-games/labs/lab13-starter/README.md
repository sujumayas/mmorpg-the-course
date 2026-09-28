# Lab 13 starter

Standard library only. Run from this folder.

1. `python budget.py --check` tests `packets_per_snapshot`, `snapshot_bytes`, `client_Bps`, `server_Bps`, `interest_counts` and `server_Bps_per_client` against the numbers in the week 13 lecture. It fails with `NotImplementedError` until you fill in the TODOs.
2. `python budget.py --sweep sweep.csv` writes client and server bandwidth for `n = 2` to `1000`, with and without a cap of 32.
3. `python budget.py --world 500 --radius 60 [--cap 32]` scatters 500 players (seeded, bunched around five hot spots) and reports the interest counts and the resulting server upload.
4. `python encoder.py` packs 1,000 random entities at full precision and quantized, and reports bytes per entity and the worst round-trip error. Fill in `encode_quantized` and `decode_quantized` first.

Expected results once finished: `all checks passed` from both scripts, 34 bytes full precision, 14 bytes quantized.
