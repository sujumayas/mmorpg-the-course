# MMO302 · Lab 06: Movement validators

**Week:** 6 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Implement the three movement checks from the [week 6 lecture](../lectures/w06-simulation-authority-and-anti-cheat-by-design.md), reproduce both of its tables from your own code, and choose a lag tolerance that meets a target correction rate for honest players while bounding what a cheater gains. You finish with a validator you will reuse in the final world server.

## Starter materials

Folder [`lab06-starter/`](lab06-starter/README.md). Standard library Python only.

- `validators.py`: stubs for `PerPacket.check`, `SlidingWindow.check` and `TokenBucket.check`. Provided: a cheater trace, an honest one-hour trace with stalls, `max_sustained_factor`, `max_blink`, `corrected_stalls`, the lecture's correction formula and a command line.
- `test_validators.py`: the lecture's cheater table (3.5×, about 1.05×, 1.0×; blinks 2.45, 36.75 and 2.45 m), the rule that rejected moves change no state, and the honest-trace results.

## Steps

1. **Three checks.** Implement the three `check` methods from their docstrings. Take care that a rejected move changes nothing: no credit spent, no history added, and for the per-packet check the arrival time still updates. Run `python test_validators.py` until it prints `all lab 06 tests passed`.
2. **Reproduce the tables.** Run `python validators.py --cheat --stalls`. Paste the output. Explain why the per-packet check has zero corrections for honest players in every row, using the burst after a stall as the example. Every row has `s ≥ Δ`. Then run the per-packet check at `s = 0.05` and explain why it now corrects almost every stall.
3. **Wall check.** Add a `blocked(x0, y0, x1, y1)` function for a map with one wall segment, and a `Position` wrapper that feeds each validator both the distance and the path. Show a cheater who walks through the wall at legal speed and is accepted by the bare bucket, then rejected with the wall check.
4. **Choose a tolerance.** Your target is at most 15 corrected stalls per hour for honest players under the lecture's stall model. Find the smallest tolerance that meets it, first from the formula, then from the simulation. Report the bucket's blink at that tolerance.
5. **A different network.** Change `honest_trace` to stalls of 0.1 to 1.5 s at 3 per minute (a poor mobile connection). Repeat step 4. Discuss whether one tolerance should serve every player, or whether the server should adapt `s` per connection from measured jitter, and what a cheater could do with an adaptive `s`.
6. **Memo.** In at most 400 words, recommend the check shape and tolerance for a game with `v = 7` m/s and 10 updates a second, and say what the server does on a failure (correct, log, act), with the thresholds you would use for "act".

## Deliverable

Your finished `validators.py` with passing tests and the wall check, the output of step 2, the tolerance numbers from steps 4 and 5, and the memo. One Markdown or PDF file plus the code.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Validators | All tests pass; rejected moves change no state; code matches the docstrings | Tests pass with a state bug found in review | Tests fail | 30% |
| Tables and explanation | Both tables reproduced; per-packet zero-correction result explained with a burst | Tables without the explanation | Missing | 15% |
| Wall check | Walk-through-wall cheat shown accepted then rejected | Wall check written, demonstration missing | Missing | 15% |
| Tolerance choice | Formula and simulation agree; blink reported; the poor-network case analysed, including the adaptive-`s` risk | One network only | Missing | 25% |
| Memo | Check shape, tolerance and failure policy each backed by a number | Recommendation without thresholds | Opinion without numbers | 15% |
