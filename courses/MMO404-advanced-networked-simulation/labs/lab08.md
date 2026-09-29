# MMO404 · Lab 08: Lookahead on the border

**Week:** 8 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Implement the conservative two-server model from the [week 8 lecture](../lectures/w08-distributed-simulation-research.md), reproduce its tables, and measure how much lookahead a border needs for a given message delay. Then work out the lookahead a real ability list allows and write the border rule that protects it.

## Starter materials

Folder [`lab08-starter/`](lab08-starter/README.md). Standard library Python only.

- `lookahead.py`: the `mulberry32` generator shared with the interactive, `random_ticks` (seed 404, 30 to 70 ms), the lecture's ability table and printers (`--pattern`, `--random`, `--smallest`, `--abilities`). Stubs for `finish_times`, `effective_tick`, `stalls`, `smallest_lookahead` and `border_lookahead`.
- `test_lookahead.py`: the lecture's numbers as tests.

## Steps

1. **By hand first.** Fill in the lecture's four-row table for `L = 1`, `δ = 20` (A: 40, 60, 40, 60 ms; B: 60, 40, 60, 40 ms) on paper. Check your finish times against the lecture's printed output.
2. **The model.** Implement `finish_times` and `effective_tick`. Run the tests until the pattern checks pass, then run `python lookahead.py --pattern` and `--random` and paste both outputs.
3. **Stalls.** Implement `stalls`. Explain in two sentences why, in the out-of-phase pattern at `L = 1`, A stalls 1,000 ms over 100 ticks and B only 980 ms.
4. **How much lookahead.** Implement `smallest_lookahead` and run `--smallest`. Plot smallest `L` against delay. Put the lecture's estimate `L ≥ (X̄ + δ) / X̄` on the same plot and explain where the measured values sit above it and why (hint: jitter).
5. **Unequal servers.** Make B 20% slower on average (multiply B's ticks by 1.2) and rerun steps 2 and 4. Report the effective tick at `L = 1, 2, 4` with 20 ms delay. Explain why no lookahead brings the pair below B's own pace, and what that means for a mesh where one server holds the fight.
6. **Abilities.** Implement `border_lookahead` and run `--abilities`. Then take the ability list your group used in the in-class activity. Enter each ability's minimum cause-to-effect delay, compute the border's lookahead, and apply your group's change. Use your step 4 table to say what delay your border can now tolerate within 5%.
7. **Border rule.** Write a one-page border rule for your class. State the lookahead the rule guarantees, list each ability with its delay, say what happens to an ability that would break the rule (redesign, confine to one server, or accept the cost), and say how interrupts and cancellations are handled.

## Deliverable

Your finished `lookahead.py`, the outputs of steps 2 and 6, the stall explanation from step 3, the plot from step 4, the unequal-server results from step 5, and the border rule from step 7, in one Markdown or PDF file plus the code.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model code | All tests pass; hand table matches; stalls explained tick by tick | Tests pass, explanation vague | Tests fail | 25% |
| Lookahead measurement | Plot of smallest `L` against delay with the estimate overlaid; the gap explained by jitter | Plot present, gap unexplained | Missing | 20% |
| Unequal servers | Numbers at three lookaheads; the bottleneck argument stated and tied to meshing | Numbers only | Missing | 15% |
| Ability analysis | Every ability's delay justified; border lookahead and tolerated delay computed | Delays given without reasons | Missing or wrong | 15% |
| Border rule | Guarantee stated; every ability placed; interrupts handled; cost in feel named | Rule present, interrupts or cost missing | Opinion without numbers | 25% |
