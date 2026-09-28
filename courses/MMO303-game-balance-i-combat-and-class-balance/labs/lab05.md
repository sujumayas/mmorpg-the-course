# MMO303 · Lab 05: Composition solver

**Week:** 5, the holy trinity ([lecture](../lectures/w05-the-holy-trinity-tank-healer-dps.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the problem sets (30%). The solver is reused in the week 13 simulator project.

## Objective

Write a solver that enumerates every group composition of a given size, applies the damage, healing and spike checks from lecture section 2, and reports which compositions pass. Then use it to tune encounters so they produce the composition set you want.

## Starter materials

- `composition_solver.py` skeleton with a `Role` dataclass, an `Encounter` dataclass and an empty `check(group, encounter)` function. A spreadsheet version, `composition-solver.xlsx`, is provided for students who prefer it.
- `roles.csv` with the lecture's three roles (tank, healer, DPS) and their `p`, `q`, `m`, `HP`.
- `test_solver.py` with the lecture's test values: for the default encounter only (1,1,3) passes; with `B = 500, S = 3,500` both (1,1,3) and (0,1,4) pass; with `B = 1,500` nothing passes.
- The [interactive](../examples/w05-role-composition.html) for spot checks.

## Steps

1. **Enumerate.** Generate every `(t, h, d)` with `t + h + d = N`. Confirm the count is `(N + 1)(N + 2) / 2` (21 for `N = 5`).
2. **Target rule.** Implement the lecture rule: a tank if present, otherwise the non-tank with the highest HP, ties broken by mitigation.
3. **Checks.** Implement the three inequalities. Return which checks pass and the margin of each (value minus requirement).
4. **Tests.** Run `test_solver.py` until all tests pass.
5. **Tuning task A.** Find encounter numbers where exactly (1,1,3) and (1,2,2) pass for `N = 5`. Report the numbers and margins.
6. **Tuning task B.** Find encounter numbers where no composition with `t = 0` passes, but two compositions with `t = 1` do, for `N = 5`.
7. **Tuning task C.** For a 10-player raid, find numbers where the best composition uses 2 tanks and 3 healers. Explain which check forces the second tank (hint: add a second simultaneous target to the model, and describe how you did it).
8. **Slack.** For each tuned encounter, report the smallest margin among passing compositions as a percent of the requirement. Aim for at least 5% on every check, so near-miss groups can win with good play.

## Deliverable

The solver code (or sheet) with passing tests, and a report of at most 600 words with the three tuned encounters, their composition tables and a paragraph on the slack you chose.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Solver correctness | All provided tests pass; margins reported | Tests pass, margins missing | Tests fail | 30% |
| Tuning A and B | Both hit the target sets exactly, with margins shown | One target set off by one composition | Targets not met | 25% |
| Tuning C (raid) | Two-target extension implemented and explained | Extension ad hoc but produces the result | Missing | 20% |
| Slack analysis | Margins quantified, trade-off of tight vs loose checks discussed | Margins listed without discussion | Missing | 15% |
| Code or sheet quality | Readable, parameters not hard-coded | Works but hard to modify | Hard to follow | 10% |
