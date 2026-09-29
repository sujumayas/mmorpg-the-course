# MMO407 · Lab 11: Preservation plan for a closing world

**Assigned:** week 11 ([lecture](../lectures/w11-shutdowns-and-emulation-communities.md)). **Due:** start of week 12 class. **Feeds:** the case analyses (50%) and the sunset section of the week 13 launch plan.

## Objective

Turn the rebuild model into a decision about what your studio hands over when it closes a world. You will implement the rebuild clock with its kink, read `q` and `g` back out of a fan project's progress history, compare handover packages for a planned shutdown, and write the preservation section of a sunset plan in which every claim has a number.

## Starter materials

The folder [`lab11-starter/`](lab11-starter/) contains:

- [`rebuild.py`](lab11-starter/rebuild.py), your file. It has the lecture's section 2 values, a `slope` helper, `fit`, `load_history`, and three TODOs: `rebuild_hours` (with an optional cheaper rate for evidence-backed behaviours), the piecewise `completeness` curve, and `find_kink`.
- [`project_history.csv`](lab11-starter/project_history.csv), an invented fan project's yearly progress report, week and share of the game rebuilt.
- [`test_rebuild.py`](lab11-starter/test_rebuild.py), four tests. All four fail on the starter.

Standard library only. Run everything with the course Python from inside the starter folder:

```
cd labs/lab11-starter
../../../../.venv/bin/python -m unittest test_rebuild.py
../../../../.venv/bin/python rebuild.py
```

When the TODOs are done, the report prints the lecture's table (450, 585, 720, 990, 1,260 weeks), the completeness at five checkpoints for `q = 0.8`, and the history fit.

## Steps

1. **The clock (20 min).** Implement `rebuild_hours` (TODO 1). Note the docstring: a protocol document lowers the cost of evidence-backed behaviours only, and guessing still costs `g × w` at the original `w`. Check the lecture's 80% row and the in-class activity's option (b) by hand in your report.
2. **The curve (25 min).** Implement `completeness` (TODO 2). Print the curve every 52 weeks for `q` = 0.5, 0.8 and 1.0, and plot or tabulate it. Mark the kink on each.
3. **Read a history (30 min).** Implement `find_kink` (TODO 3) and run `fit` on the provided history. You should recover `q` and `g`. Then use the fitted values to answer: the project's lead says they will be "done in two more years." What does the model predict, assuming the team's hours stay the same? Show the calculation. (Hint: the slope before the kink gives `V / (B × w)`.)
4. **Noise (20 min).** Real progress reports are noisy. Copy the history, add or subtract up to 0.01 at random to each value after week 0 (fix a seed and print it), and refit five times. Report the spread of `q` and `g`. Which estimate is more fragile, and why?
5. **Compare packages (40 min).** Your studio closes an MMO in six months. Use `B = 2,000`, `w = 60`, `g = 4`, `w_s = 3`, 30 volunteers at 6 hours a week, and today's evidence `q = 0.55`. Compute `T` in years for: no action; (a) a capture window raising `q` to 0.85; (b) a protocol document with `w_evidence = 40`; (a)+(b); (c) binaries with a hosting licence; and the expected `T` of "try (c) with 50% licensor consent, fall back to (a)+(b)". Present one table.
6. **Write the plan (30 min).** Write the preservation section of the sunset plan, 300 to 400 words. It must answer MMO301 week 13's fifth question with this week's numbers, name the approvals each package needs (licensor, middleware vendors, privacy review under DB201 week 13), and give a date by which each approval must be requested so it lands before the servers close.

## Deliverable

A zip or repository link containing:

- Your `rebuild.py` with all tests passing (paste the test output in the report), and any script you used for steps 4 and 5.
- `report.md`, 800 to 1,100 words: the step 1 hand checks, the step 2 table, the step 3 fit and forecast, the step 4 spread, the step 5 table, and the step 6 plan.
- Every number reproducible from a command you list.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Tests | All four pass | Three pass | Two or fewer | 20% |
| Model use | Hand checks correct; kink marked on all three curves; forecast in step 3 derived from the fitted slope and `g` | Forecast given without derivation | Forecast missing or wrong | 20% |
| Noise analysis | Spread reported with seed; explains why `g` (a ratio of two small slopes) is more fragile than `q` | Spread reported, no explanation | Not done | 10% |
| Package comparison | All six rows correct, including the expected value with fallback | One or two rows wrong | Three or more wrong | 20% |
| Preservation plan | Numbers from step 5, every approval named with an owner and a request date, privacy handled explicitly | Numbers present, approvals vague | No numbers | 20% |
| Reproducibility and clarity | Commands listed; tables match reruns | Minor gaps | Cannot be rerun | 10% |
