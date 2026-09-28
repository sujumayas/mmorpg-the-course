# CS202 · Lab 09: Prediction and reconciliation

**Weeks:** 8 and 9 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Implement the client side of the [week 8](../lectures/w08-client-side-prediction.md) and [week 9](../lectures/w09-server-reconciliation.md) lectures in a small simulator: prediction, naive snapping, reconciliation and smoothed corrections. Measure each against the lectures' models across round trips and loss rates, and see for yourself what a lost input does. You finish with a one-page tuning memo that sets a smoothing time and a snap threshold from your own measurements.

## Starter materials

Folder [`lab09-starter/`](lab09-starter/README.md). Standard library Python only. A spreadsheet or plotting tool of your choice for steps 5 and 6.

- `netsim.py`: the shared `step` (6 m/s, 60 Hz), an authoritative server with a scripted snare at 1.0 s, a network with one-way delay `RTT/2`, snapshot loss and optional input loss, a report and a `--check` mode. You write `Client.on_input`, `Client.on_snapshot` and `Client.displayed_offset`.

## Steps

Part A can be done after the week 8 lecture. Parts B and C need week 9.

**Part A: prediction**

1. **Dumb and predicted.** Implement `on_input`. In dumb mode it does nothing. Otherwise it appends `(seq, move)` to `self.pending` and advances `self.state` with `step`. Write a temporary `on_snapshot` that only sets `self.state` to the snapshot's state and returns the jump. Run `--mode dumb --no-snare` at round trips of 0, 50, 150 and 250 ms and record "first visible move". Check each against the week 8 model's best, average and worst cases.
2. **Naive snapping.** Run `--mode naive --no-snare --csv naive.csv` at 150 ms. From the CSV, list every backward jump and the time the character stops after the key is released. Explain in three sentences why the naive client ends up behaving like the dumb one.

**Part B: reconciliation**

3. **Reconcile.** Finish `on_snapshot`: drop acknowledged inputs in every mode, and in reconcile mode replay the rest from the server's state. Run `python netsim.py --check`. All lines except the smoothing line should pass.
4. **Smooth.** Implement `displayed_offset` and the smoothing lines of `on_snapshot` (see the TODO). Run `--check` until it prints `all checks passed`.
5. **Sweep.** For round trips 0, 50, 100, 150, 200, 250 and 300 ms, record the pending range and the snare correction in reconcile mode. Plot correction against round trip, fit a line, and compare its slope with the lecture's `Δv = 3` m/s.
6. **Loss.** At 150 ms, run snapshot loss 0, 5, 10 and 20% with seeds 1 to 5. Report the mean and largest snare correction per loss rate, and explain the increase with the lecture's model.

**Part C: what the lab hid from you**

7. **Lost inputs.** Run `--mode reconcile --no-snare --input-loss 0.05`. Count the corrections, give their size, and compare the server's final `x` with 12.0 m. Explain why each lost input produces exactly one correction. Then describe, in two sentences, the redundancy scheme you would add and what it costs in upload per second with 4-byte inputs at 60 Hz and the 28-byte header.
8. **Tuning memo.** Your game's worst movement surprise is a 12 m/s knockback lasting 0.25 s. Using your sweep, choose a smoothing time and a snap threshold for players with round trips up to 200 ms. One page, with the numbers that justify both choices and one case where your choice looks wrong.

## Deliverable

Your finished `netsim.py`, the tables from steps 1, 5, 6 and 7, the plot from step 5, the three-sentence explanation from step 2, and the one-page memo. Submit before the week 10 lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Implementation | `--check` passes; `on_snapshot` is short and follows the drop, accept, replay order | Passes with extra special cases or unclear code | Fails the check | 25% |
| Part A measurements | Dumb delays checked against best, average and worst; naive jumps listed; explanation correct | Numbers present, explanation thin | Missing | 15% |
| Sweep and loss | Plot with fitted slope close to 3 m/s and discussed; loss results over five seeds explained with the model | One of the two done well | Missing or unexplained | 25% |
| Lost inputs | Corrections counted and sized; one-correction-per-input explained; redundancy cost computed | Observed but not explained | Missing | 15% |
| Tuning memo | Both numbers follow from the measurements; a real failure case named | Numbers chosen with weak support | Opinion without numbers | 20% |
