# MMO307 · Lab 02: Power creep audit

**Week:** 2, vertical progression and power creep ([lecture](../lectures/w02-vertical-progression-and-power-creep.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the progression analysis (30%). Your creep budget is reused in week 5 (stat squish) and week 6 (catch-up).

## Objective

Measure power creep in two shipped games from their item-level histories, decide whether each is additive or multiplicative, and then write a creep budget for a four-expansion plan using the ratchet model.

## Starter materials

All in [`lab02-starter/`](lab02-starter/). Standard-library Python, run with `.venv/bin/python` or any Python 3.10+.

- [`itemlevels.csv`](lab02-starter/itemlevels.csv), the item-level data from the lecture. World of Warcraft ranges by expansion on each scale in use (native, after 8.0.1, after 9.0.1, after 12.0.0), from the Warcraft Wiki's "Stat squish" table, and Final Fantasy XIV maximum item levels per level cap from its official wiki's "Item Level" page. Columns `series, label, bottom, top, note`.
- [`creep.py`](lab02-starter/creep.py), a skeleton with a working `load_series` and nine functions to fill in: `increments`, `ratios`, `fit_additive`, `fit_multiplicative`, `creep_per_tier`, `creep_per_expansion`, `shelf_life`, `max_creep` and `largest_overlap`.
- [`test_creep.py`](lab02-starter/test_creep.py), tests from the lecture's numbers (increments 73 to 265 for WoW, 130 per expansion for FFXIV, `c = 5, 15, 25, 35` for `o = 0..3`, shelf lives 4.64 and 1.99, a budget of 23.22 levels per tier). Run `python test_creep.py`. On the starter, only the data-loading test passes.
- The [interactive](../examples/w02-power-creep.html) for spot checks.

## Steps

1. **Describe the data.** Implement `increments` and `ratios`. Print both for `wow_native`, `wow_sl_scale` and `ffxiv`.
2. **Fit two models.** Implement `fit_additive` (least squares on item level against expansion index) and `fit_multiplicative` (least squares on the log of item level). Report the slope, the growth ratio and the sum of squared errors for each series. Say which model fits each series better, and by how much.
3. **Ratchet.** Implement the four ratchet functions and `largest_overlap`. Run the tests until all pass.
4. **Chart.** Plot the WoW native series with both fitted curves, and the FFXIV series with both fitted curves (matplotlib or a spreadsheet). Label the axes and state the sums of squared errors in the legend.
5. **Infer a ladder.** Final Fantasy XIV's wiki gives three tiers of 40, 30 and 30 item levels per expansion plus about 30 between caps. Treat the 30-level steps as `c = o × s + u`. Propose two different `(o, s, u)` triples that give `c = 30` and explain what each would mean for players (which rung's gear the next tier replaces).
6. **Budget.** You are planning four expansions of three tiers, a four-rung ladder, `g = 0.8%` power per item level and `F = 1.8`. Your director wants a shelf life of at least three tiers. Find the largest `c`, then choose `s`, `u` and `o` to meet it. Report `C` per expansion, total creep over the plan and the plan's power multiplier `(1 + g)^(total creep)`.
7. **Stress test.** Your producer adds a fifth rung in expansion 3 and keeps "the new entry rung beats the old top rung." Compute the new `c`, the new shelf life and the plan multiplier. Propose the smallest change that restores a three-tier shelf life.

## Deliverable

Your completed `creep.py` with passing tests, the step 4 chart, and a memo of at most 600 words to your director. The memo covers the fit results for both games (step 2), your budget (step 6) and the stress test with your fix (step 7).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All tests pass; fits computed from scratch, not with a library call that hides the method | Tests pass with minor hard-coding | Tests fail | 25% |
| Data analysis | Correct fit for all three series, with SSE compared and a clear verdict per game | Fits correct, verdict unclear or missing one series | Fits wrong or missing | 25% |
| Ladder inference | Two valid triples with player-facing meaning explained | One valid triple, or meaning thin | Missing or arithmetic wrong | 15% |
| Budget and stress test | Largest `c` correct, plan numbers correct, fix is minimal and justified | Numbers correct, fix not minimal | Numbers wrong | 25% |
| Memo | Director could act on it; within length; numbers match code | Clear but misses a number | Hard to follow or over length | 10% |
