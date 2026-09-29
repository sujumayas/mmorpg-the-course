# MMO404 · Lab 02: Seams and handoff

**Week:** 2 · **Time:** 2 hours in lab plus about 4 hours at home · **Weight:** part of the labs (40%)

## Objective

Build the two halves of a seamless border from the [week 2 lecture](../lectures/w02-seamless-worlds-and-boundary-handoff.md). In part A you implement a handoff protocol that never has two owners and never loses, doubles or reorders an input, even when messages between servers are slow. In part B you implement the seam cost model, reproduce the lecture's table, and choose a band width for a different player population. The protocol you write here is the core of the course's final demo, the seamless two-server handoff.

## Starter materials

Folder [`lab02-starter/`](lab02-starter/README.md). Standard library Python only. Run with `.venv/bin/python` from the repository root or any Python 3.10+.

- `handoff.py`: two servers, a gateway and a delayed link are given, with a test harness that walks a dithering player across the border. You implement `wants_handoff` and the three `Server` handlers `on_input`, `end_of_tick` and `on_message`. The helper `_apply_in_order` is given.
- `seam.py`: the lecture's traveller and dweller simulation is given. You implement `update_owner`, `ghost_count` and `seam_cost_ms_per_s`.

## Steps

1. **Read the harness.** Before writing code, read `run` in `handoff.py` and write down, for a link delay of 2 ticks, the tick at which B receives `transfer` and the tick at which A receives `ack` if A starts a handoff at the end of tick 3. Check your answer later with `--trace`.
2. **Hysteresis.** Implement `wants_handoff(x, side, w)`. The owner on side A hands over when `x > w/2`; the owner on side B when `x < −w/2`.
3. **The protocol.** Implement `on_input`, `end_of_tick` and `on_message` following the docstrings and section 3 of the lecture. Run `python handoff.py --check` until it prints `all checks passed`. The tests run 30 walks (link delays of 1, 2 and 3 ticks, bands of 0 and 4 m, five seeds).
4. **Break it on purpose.** Make two deliberate bugs, one at a time, and record which assertion catches each: (a) in `end_of_tick`, stay `authoritative` after sending `transfer`; (b) in `on_message`, on `ack`, drop the buffer instead of forwarding it. Restore the correct code afterwards. In two sentences each, describe what a player would see in a real game.
5. **Seam cost.** Implement the three functions in `seam.py` and run `python seam.py --check`. Then run `python seam.py --sweep seam.csv` and plot handoff CPU, ghost CPU and total seam cost against `w`. Mark the minimum.
6. **A different crowd.** Change the dweller spread from 4 m to 10 m (the `4.0` in `handoffs_per_s`) and repeat the sweep. Report the new best `w` and the cost at it. One seed is noisy, most of all at small `w` (the lecture's section 2 shows `H(0)` ranging from 6.2 to 10.9 across seeds), so average `handoffs_per_s` over seeds 1 to 8 before you choose. Explain in three sentences why the minimum moved and why doubling `ρ` would not move it.
7. **Time-to-trigger.** Add a second rule to `update_owner`: a player must stay past the band edge for `k` consecutive ticks before the handoff happens (you will need per-player state). Sweep `k = 1, 2, 3, 5` at `w = 5`. Does time-to-trigger replace band width, or add to it? Answer with numbers.

## Deliverable

Your finished `handoff.py` and `seam.py`, `seam.csv` and the plot for both spreads, and a report (PDF or Markdown, at most four pages) with the answer to step 1, the bug descriptions from step 4, the results and explanations from steps 6 and 7, and one paragraph recommending a band width and time-to-trigger for a market-town border. Submit before the week 3 lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Handoff protocol | `--check` passes; code follows the four roles; no special cases for the tests | Passes with a workaround that would fail under a longer delay | Fails the check | 30% |
| Failure analysis | Both bugs caught and named; player-visible effect described correctly (duplicated movement or snap-back, lost actions) | Bugs caught, effects vague | Step skipped | 15% |
| Seam model | `seam.py --check` passes; plot shows both terms and the minimum | Passes, plot incomplete | Fails the check | 20% |
| Movement analysis | New minimum reported; explanation uses dithering scale and the proportional scaling of `H` and `G` with `ρ` | Minimum reported, explanation thin | Missing | 15% |
| Time-to-trigger | Implemented, swept, and compared with band width in numbers | Implemented without a clear comparison | Missing | 15% |
| Writing | Plain, one idea per paragraph, units everywhere | Mostly clear | Hard to follow | 5% |
