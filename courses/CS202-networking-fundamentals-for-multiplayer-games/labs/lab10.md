# CS202 · Lab 10: The interpolation buffer

**Week:** 10 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Build the client-side buffer from the [week 10 lecture](../lectures/w10-entity-interpolation.md), prove it reproduces the lecture's Table 2, then measure what each interpolation delay `D` costs and buys under a bad network. You finish with a recommended `D` for a game of your choosing, backed by pop counts and the distance-behind cost in meters.

## Starter materials

Folder [`lab10-starter/`](lab10-starter/README.md). Standard library Python only.

- `interp_lab.py`: stubs for `lerp`, `lerp_angle`, `InterpolationBuffer.sample` and `render_time`, plus a finished harness. The harness streams 20 Hz snapshots of a player strafing at 6 m/s (reversing every 700 ms) through a simulated network with latency, jitter and loss, draws 60 frames per second, and reports the fraction of frames interpolated and extrapolated, the mean and maximum position error, the number of visible pops and the age of what is drawn.

Run it with `.venv/bin/python interp_lab.py` from the repository root's virtual environment, or any Python 3.10 or newer.

## Steps

1. **Implement the four functions.** Follow the docstrings. `sample` must return `(x, mode)` with mode `"interp"`, `"extrap"` or `"hold"`, and must cap extrapolation at `max_extrap_ms`. Run `python interp_lab.py --check` until it prints `all checks passed`.
2. **Reproduce the lecture by hand.** Pick two rows of the lecture's Table 2 (one extrapolated, one interpolated) and show the arithmetic for `t_r`, `alpha` and `x`. Confirm the `--check` output agrees.
3. **Clean network sweep.** Run `python interp_lab.py --sweep`. Explain in two sentences why `D = 50` is already perfect here and why `D = 0` and `D = 25` pop.
4. **Bad network sweep.** Run `python interp_lab.py --sweep --loss 0.05 --jitter 20` with seeds 10, 11 and 12. Put the three runs in one table. For each `D`, report the average and the worst pop count across seeds.
5. **Burst loss.** Change the harness so losses come in bursts, using week 2's model. After a lost snapshot, the next is lost with probability `q = 0.5`, otherwise with probability `p`. Choose `p` so the average loss is still about 5%. Repeat step 4. Which `D` do you need now, and does it match the lecture's `D = kΔ + J` rule?
6. **Angles.** Add a heading to the strafing player (90° while moving right, 270° while moving left, turning through 0° over 100 ms at each reversal). Interpolate it with `lerp_angle` and with a plain `lerp`. Report the largest frame-to-frame change in heading for each, and explain the difference.
7. **Recommend.** Choose a game (a shooter, a brawler, an MMO with 100 players in view, or your own). State its snapshot rate and a realistic loss pattern, then recommend `D`. Give the pop rate you expect, how far behind the server a player at 6 m/s will be drawn (`v × (L + D)`), and one change to the game that would let you lower `D`.

## Deliverable

Your finished `interp_lab.py` (with the burst-loss and heading changes), the tables from steps 3 to 6, the two hand-checked rows from step 2, and a one-page recommendation. Submit before next week's lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Buffer implementation | `--check` passes; `sample` handles interp, capped extrap and hold cleanly and matches the lecture's code | Passes with special cases or unclear code | Fails the check | 25% |
| Hand verification | Two rows of Table 2 derived step by step, matching the tool | One row, or arithmetic without explanation | Missing | 10% |
| Sweeps (steps 3-4) | Three seeds, averages and worst cases, correct explanation of why `D = 50` suffices on a clean network | One seed, or explanation vague | Missing | 20% |
| Burst loss and angles (steps 5-6) | Burst model correct, `D` chosen from data and related to `kΔ + J`; heading jump measured both ways and explained with the shortest-arc rule | One of the two done well | Neither | 20% |
| Recommendation | `D` follows from measured pops and the distance-behind cost; one concrete lever to lower `D` (send rate, loss handling) with its price | Sensible choice, numbers thin | Opinion without numbers | 25% |
