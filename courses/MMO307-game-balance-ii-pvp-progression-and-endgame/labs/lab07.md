# MMO307 · Lab 07: Split register

**Week:** 7, PvP balance vs PvE balance ([lecture](../lectures/w07-pvp-vs-pve-split-tuning.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** formative. Your split register is reused in the final season design (40%).

## Objective

Implement the week 7 model, prove to yourself that shared numbers cannot meet both targets for this roster, and find the fewest and coarsest splits that put six classes inside the PvE band and the PvP band at once.

## Starter materials

- [`lab07-starter/split_tuning.py`](lab07-starter/split_tuning.py), standard-library Python. It holds the constants (`H = 30,000`, `C = 60`, PvE target 1,100 ±3%, TTK band 15 to 22 s) and a six-class roster, all invented. The functions `pve_dps`, `pvp_ttk`, `clone`, `burst_multiplier`, `sustain_multiplier` and `audit` are empty.
- [`lab07-starter/test_split_tuning.py`](lab07-starter/test_split_tuning.py) with the lecture's values: the three-class table, the one-shot case, `p = 0.8` giving 15.4 s, `q = 1.2` giving 21.4 s, `h = 4.35` giving 152.1 s, the clone at 20 and 22 s, and the audit results. All tests fail on the starter. Run from the starter folder with `../../../../.venv/bin/python test_split_tuning.py`, or with pytest.
- The [split-tuning interactive](../examples/w07-split-tuning.html) for checking single classes by eye.

| Class | `s` | `B` |
|---|---|---|
| Duelist | 900 | 12,000 |
| Ravager | 700 | 24,000 |
| Channeler | 1,050 | 3,000 |
| Assassin | 600 | 30,000 |
| Warden | 1,000 | 6,000 |
| Stormcaller | 820 | 16,800 |

## Steps

1. **Model.** Implement `pve_dps` and `pvp_ttk` exactly as the lecture writes them, including the `max(0, ...)` for one-shots.
2. **Clone.** Implement `clone(D, T)`. Print the clone shape for every whole-second TTK from 15 to 22 and add it to your memo as a small table.
3. **Inverses.** Implement `burst_multiplier` and `sustain_multiplier`. Check each by feeding its result back into `pvp_ttk`.
4. **Audit.** Implement `audit`. Run it on the unsplit roster and list which classes fail which band.
5. **Shared-numbers attempt.** Before any split, try to fix the roster with shared numbers only. For each failing class, report the clone shape nearest its current `(s, B)` and how far its burst would have to move, as a percentage. This is your evidence for or against splitting.
6. **Split solver.** Write `solve(roster)` that returns a split plan: for each class, either no split, a `p`, or a `q`, rounded to 0.05, so that `audit` returns no problems. Prefer, in order, no split, then a global `h` alone, then per-class `q`, then per-class `p`. Explain in a comment why this order matches the lecture's "coarsest grain first" rule, or argue for a different order.
7. **Global lever.** Separately, find the `h` in steps of 0.05 that minimizes the slowest-to-fastest TTK ratio across all six classes with no per-class splits. Report the ratio and the mean TTK. Say whether that pace is acceptable for an arena game where matches should last under three minutes.
8. **Split register.** Write the final plan as a table with one row per split: class, field, multiplier, mode, reason, date added, audit date.

## Deliverable

The completed `split_tuning.py` with all tests passing and your `solve` function, the split register, and a memo of at most 300 words to the PvE and PvP leads. The memo must state how many splits you need, why shared numbers could not do it (cite the clone table), and one risk each split creates for players.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model and tests | All provided tests pass; functions match the lecture's formulas | One function wrong or tests edited | Tests fail | 25% |
| Shared-numbers evidence | Clone table and distance-to-clone for each failing class, correctly computed | Clone table only | Missing or wrong | 20% |
| Split solver | Every class inside both bands with the fewest splits; order of preference justified | Valid plan, more splits than needed or no justification | Plan leaves classes out of band | 25% |
| Global lever analysis | Best `h`, ratio and mean TTK reported and judged against a pace limit | Numbers without judgment | Missing | 10% |
| Register and memo | Register complete; memo plain, numeric, names one player-facing risk per split, within limit | Some rows or risks missing | Hard to act on | 20% |
