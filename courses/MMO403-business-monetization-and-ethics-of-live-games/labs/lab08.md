# MMO403 · Lab 08: A dark-pattern review

**Week:** 8, dark patterns ([lecture](../lectures/w08-dark-patterns.md)).
**Time:** 2 hours in the lab, plus up to 3 hours to finish the review.
**Work mode:** pairs for the code, individual review.
**Counts toward:** ethics analysis (20% of the course grade), one of its five lab pieces with labs 03, 04, 06 and 07 (see the [ethics analysis brief](../assessments/ethics-analysis-brief.md)).

## Objective

Implement the friction-for-sale model and the asymmetric-friction calculation, reproduce the lecture's numbers, find out which assumptions move the LTV-optimal wait, and then write a dark-pattern review of one real game in the six-step format of section 4.

## Starter materials

All in [`lab08-starter/`](lab08-starter/). Standard-library Python.

- [`friction.py`](lab08-starter/friction.py): the lecture's default parameters and stubs for `pay`, `retention`, `arpu`, `lifetime`, `ltv`, `best_wait`, `lifetime_lost`, `completion`, `asymmetry` and `accidental`. A `sweep` helper is provided and works once the stubs do.
- [`test_friction.py`](lab08-starter/test_friction.py): five tests built from the lecture's table, its optimum and sensitivity results, and the section 3 numbers. All five fail on the starter. Run them from the repository root:

```
.venv/bin/python courses/MMO403-business-monetization-and-ethics-of-live-games/labs/lab08-starter/test_friction.py
```

- The interactive `examples/w08-friction-for-sale.html`, for checking single settings by hand.

## Steps

1. **The model.** Implement the five model functions. Confirm the `w = 2` row by hand before you trust the code.
2. **The optimum.** Implement `best_wait` on an integer grid (the docstring explains why) and `lifetime_lost`. You should get 3.46 hours, $11.02 and 37.6%.
3. **Asymmetry.** Implement `completion`, `asymmetry` and `accidental`. Run the tests until all five pass.
4. **Sensitivity.** Use `sweep` on each of `d`, `A0`, `s` and `m` across a range you can defend (at least five values each). Make one table per parameter with the best wait, peak LTV and lifetime at the peak. Write one sentence per parameter on the direction the best wait moves and why, using the optimum rule `ARPU'/ARPU = c'/c`.
5. **A policy test.** Suppose your studio adopts a rule: "no wall may cut modelled lifetime by more than 15% against no wall". Find the longest `w` that meets it under the defaults, and the LTV there. How much LTV does the rule cost relative to the peak?
6. **A real game.** Pick one live game with a store or a timed progression system you can document from public material (store pages, patch notes, wiki pages, your own notes). Write the six-step review from section 4 of the lecture. For step 3, you won't have the studio's data: state your assumptions and use the model only to reason about direction, not to claim real numbers.

## Deliverable

Your completed `friction.py` with all tests passing; the sensitivity tables and the policy-test result (one page); and an individual review of at most 700 words. The review must place the feature in the taxonomy, state the wall or the asymmetry, report both views, apply the disclosure test, check the audience including the PEGI June 2026 criteria, and end with a signed decision: ship as is, ship with named changes, or do not ship. Describe screens in words. Do not paste game art or screenshots.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All five tests pass; grid search uses integer indices; readable | Tests pass with minor style issues | Tests fail | 25% |
| Sensitivity and policy test | Four sweeps, each direction explained with the optimum rule; policy cost computed | Sweeps done, explanations thin | Missing or wrong | 25% |
| Review quality | All six steps; taxonomy placement justified; both views; disclosure test applied honestly | Steps present, some shallow | Opinion without the method | 30% |
| Balance and evidence | Separates pacing from friction for sale; sources for every factual claim about the game | Mostly sourced, some one-sidedness | Unsourced or one-sided | 20% |
