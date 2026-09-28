# Lab 10 starter

Standard library only. One file, `interp_lab.py`.

1. Finish the four functions marked TODO: `lerp`, `lerp_angle`, `InterpolationBuffer.sample` and `render_time`.
2. `python interp_lab.py --check` must print `all checks passed`. The tests use the snapshot table from the week 10 lecture (snapshots at 1000 and 1050 ms, 1100 lost, 1150 late).
3. `python interp_lab.py --sweep` prints one row per interpolation delay (0 to 200 ms) on a clean network. Add `--loss 0.05 --jitter 20` for a bad one, and `--seed N` to repeat with different random draws.

Columns: `interp` and `extrap` are the fractions of frames drawn each way, `mean err` and `max err` compare the drawn position with where the player really was at the render time, `pops` counts frames where the drawn player jumped more than twice a normal frame's movement, and `age` is how far in the past the player is drawn (`latency + delay`).
