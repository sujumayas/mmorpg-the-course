# CS202 · Lab 13: Bandwidth budget

**Week:** 13 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Turn the [week 13 lecture](../lectures/w13-tick-rate-and-bandwidth-budgets.md) model into a tool you trust, then use it to write a real budget. You will implement the snapshot bandwidth formula, check it against the lecture's tables, replace the fixed interest cap with a radius-based count on a seeded world, and measure bytes per entity from an actual encoder instead of guessing. You finish with a one-page budget for a game you choose, with a tick rate, a snapshot rate and a per-client ceiling you can defend.

## Starter materials

Folder [`lab13-starter/`](lab13-starter/README.md). Standard library Python only.

- `budget.py`: the model from section 2 (`packets_per_snapshot`, `snapshot_bytes`, `client_Bps`, `server_Bps`), a seeded world generator `make_world`, a brute-force reference `brute_counts`, and TODOs for a grid-based `interest_counts` and `server_Bps_per_client`. `--check`, `--sweep` and `--world` modes.
- `encoder.py`: a full-precision entity packer (34 bytes) using `struct`, and TODOs for a quantized packer and its decoder (14 bytes).

## Steps

1. **The model.** Implement the four model functions in `budget.py`. Before running `--check`, compute `snapshot_bytes(64, 24)` and `server_Bps(64, 30, 24)` by hand and write them down. Then run `python budget.py --check` and fix anything it names except the two interest functions.
2. **Interest by grid.** Implement `interest_counts` with a uniform grid whose cells have side `radius`, checking only the 3 by 3 block around each player. `--check` compares it with `brute_counts` on 300 players. Then time both on 2,000 players with `time.perf_counter()` and report the ratio. Explain in two sentences why the grid wins, using the week's `O(n²)` argument and CS102 week 4.
3. **Per-client budgets.** Implement `server_Bps_per_client`. Run `python budget.py --world 500 --radius 60`, then again with `--cap 32`. Report the median and maximum `k`, the server upload in both runs and the worst client's download. Why does the cap save much less here than the lecture's "everyone hears everyone" comparison suggests? Why does it still matter for the worst client?
4. **The wall.** Run `python budget.py --sweep sweep.csv` and plot `server_mbit_nocap` and `server_mbit_cap` against `n` on linear axes and on log-log axes (any tool). On the log-log plot, measure both slopes between `n = 100` and `n = 1000` and say what exponent each shows. Mark where the no-cap curve crosses 1 Gbit/s.
5. **Real bytes.** Implement `encode_quantized` and `decode_quantized` in `encoder.py` until it prints `all checks passed`. Redo the 100-player lever table from the lecture with `b = 34` and `b = 14` instead of 40 and 16. Which lever saves more at 100 players, quantization or a cap of 32? Which wins at 500?
6. **Your budget.** Pick a game design (your PR201 project if you have one). Write a one-page budget: player count at peak density, tick rate and snapshot rate with the latency each adds, bytes per entity from step 5 or better, interest radius or cap, per-client ceiling, server upload at peak, and GB per match-hour. State what your server does when the ceiling is broken (section 4 of the lecture).

## Deliverable

Your finished `budget.py` and `encoder.py`, `sweep.csv`, the two plots, and a report (PDF or Markdown, at most three pages) with the hand calculations from step 1, the timing from step 2, the answers to steps 3 to 5, and the one-page budget from step 6. Submit before next week's lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model code | `--check` passes; functions follow the lecture's formulas; hand calculations agree | Passes after patching a value to fit the test | Fails the check | 20% |
| Interest management | Grid matches brute force exactly; timing ratio reported and explained with `O(n²)` vs `O(n)` | Correct but timing or explanation missing | Brute force only, or counts differ | 20% |
| Scaling analysis | Both plots, slopes measured near 2 and 1, wall marked, cap result from step 3 explained | Plots present, slopes or explanation thin | No plots | 20% |
| Encoder | 14-byte quantized packer passes; lever table redone and compared at 100 and 500 players | Packer passes, comparison missing | Packer fails | 15% |
| Budget | Every number present with units and a reason; latency cost of the chosen rate stated; overload policy chosen | Numbers present, some unjustified | Budget missing or copied from the lecture | 20% |
| Writing | Plain, one idea per paragraph, units everywhere | Mostly clear | Hard to follow | 5% |
