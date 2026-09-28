# CS202 · Lab 11: Rewind hit detection

**Week:** 11 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Implement the server side of lag compensation from the [week 11 lecture](../lectures/w11-lag-compensation-rewind-hit-detection.md). You build a per-player history, a rewound ray test and a capped rewind time. Then measure both sides of the trade, the shooter's hit rate and the victim's time behind cover, and write a rewind policy for a real player population.

## Starter materials

Folder [`lab11-starter/`](lab11-starter/README.md). Standard library Python only.

- `rewind.py`: stubs for `History.position_at`, `ray_hits_circle` and `rewind_time`, plus a finished harness. The server ticks at 60 Hz and records the target each tick. `--accuracy` fires 200 shots at a strafing target (6 m/s, reversing every 700 ms), each aimed at exactly what the shooter's screen showed. `--cover` has a victim run behind a wall and a shooter fire on the last visible frame, then reports how long the victim's own screen showed them hidden before the kill arrived.

## Steps

1. **Implement the three functions.** `position_at` lerps between the two records around `t_ms` and clamps outside the buffer. `ray_hits_circle` uses the dot product and squared distances, with no square root in the comparison. `rewind_time` subtracts `min(RTT + D, cap)`. A hit is `perpendicular² ≤ radius²`, as in the lecture. Use `≤`, not `<`: at RTT 150 with a 200 ms cap the residual lead is exactly 0.30 m, the radius, and the shot grazes. Run `python rewind.py --check` until it prints `all checks passed`.
2. **Reproduce Tables 1 and 2.** Run `python rewind.py --accuracy --cover`. Confirm the with-rewind column is 100% at every RTT and the cover windows match `RTT_s + D + RTT_v` within 1 ms. Explain the 10% of hits that land without rewind.
3. **Interpolation matters.** Repeat step 2 with `--interp 0` and with `--interp 50`. At what RTT does a center shot without rewind start missing? Relate the answer to the hitbox radius and `v × (RTT + D)`.
4. **The cap.** Run `--cover` with caps of 150, 200, 300 and 1000 ms. For each cap, give the largest shooter RTT that still gets the kill and the worst victim window. Then add a `--accuracy` column for a shooter who aims at the displayed center under each cap, and report where hit rate collapses.
5. **Don't trust the client's clock.** Add a `claimed_view_ms` argument to `server_hit`, as if the client reported the tick it was rendering. Accept it only if it is within 200 ms of the server's own estimate `arrival − (RTT + D)` and not older than the cap; otherwise use the estimate. Write two tests: an honest claim that is used, and a "backtrack" claim 600 ms old that is rejected.
6. **Cost.** Time 10,000 calls of `server_hit` with 32 players in the history (loop the rewind over all 31 other players). Report microseconds per shot. Then add a broad phase that skips any player whose recorded x range over the rewind window is more than 1 m from the ray, and report the new time.
7. **Policy.** Your game's players in one region have round trips spread evenly between 20 and 120 ms, and in a second region between 120 and 220 ms. `D = 50` ms. Recommend `R_max` per region or one global value. For the 10th, 50th and 90th percentile player in each region, give the shooter's residual lead and the worst victim window they can cause.

## Deliverable

Your finished `rewind.py` with the step 5 tests and the step 6 broad phase, the output tables from steps 2 to 4 and 6, and a one-page policy for step 7. Submit before next week's lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Core functions | `--check` passes; ray test uses dot product and squared distances; history clamps correctly | Passes with a workaround or unclear code | Fails the check | 25% |
| Measurements (steps 2-4) | All runs reported, results explained with `v × (RTT + D)` and `W = RTT_s + D + RTT_v`, cap trade stated in numbers | Runs reported, explanations partial | Missing runs | 20% |
| Client claim check (step 5) | Both tests pass; tolerance and cap both enforced; explains the backtrack cheat | One test, or only one bound | Missing | 15% |
| Cost and broad phase (step 6) | Timing before and after, broad phase correct and measured speed-up explained | Timing only | Missing | 15% |
| Policy (step 7) | Cap chosen from the percentiles; residual lead and victim window given per percentile and region; who pays stated plainly | Choice sensible, numbers thin | Opinion without numbers | 25% |
