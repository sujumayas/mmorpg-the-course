# CS203 · Lab 08: Utility scoring you can tune

**Week:** 8 ([Utility AI](../lectures/w08-utility-ai.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; swap designer briefs with a neighbor in Part B

## Objective

Build the small toolkit every utility system needs (response curves, scoring with a veto, selection with a commitment bonus), reproduce the lecture's switch points and 12-think trace, and then use the toolkit the way a designer would: turn a written brief ("drink at about a quarter health, fight on if the enemy is nearly dead, never fidget") into curves, and prove with numbers that the NPC does what the brief says.

## Starter materials

- Python 3.10 or later, no packages. In this repository, `.venv/bin/python`.
- [`labs/lab08-starter/utility.py`](lab08-starter/utility.py). It provides `clamp01`, the lecture's brute (`attack_desire`, `brute_scores`), the 12-think health trace `LECTURE_HP`, `replay()`, which re-decides every think and counts switches and finished potions, and `decision_map()`, which prints an ASCII map of which action wins for every pair of health values. You write `power`, `logistic`, `piecewise`, `score`, `choose` and `crossover`.
- [`labs/lab08-starter/test_utility.py`](lab08-starter/test_utility.py). Run `python test_utility.py` from inside the starter folder. It prints PASS, FAIL or TODO for nine tests and exits with status 1 until all pass. On the untouched starter all nine report TODO.
- The interactive [`examples/w08-utility-curves.html`](../examples/w08-utility-curves.html) for checking switch points by eye.

## Steps

### Part A: the toolkit (55 minutes)

1. Write `power(x, k)` and `logistic(x, mid, steep)`. Both clamp `x` to 0 to 1 first. Check by hand that `logistic(0.5)` is exactly 0.5 for any `steep`.
2. Write `piecewise(x, points)` with the lerp from MA101 week 8. The test uses a Sims-style hunger curve, `[(0, 0), (0.4, 0.1), (0.7, 0.3), (1, 1)]`. Work out `piecewise(0.55, ...)` by hand before you run it.
3. Write `score(considerations, combine)`. Considerations are functions, so that a zero can stop the evaluation before the expensive ones run. The test checks that it does. Support `"product"` and `"geomean"`.
4. Write `choose(scores, current, bonus)`. Multiply the current action's score by `1 + bonus`, and on an exact tie keep the current action.
5. Write `crossover(k, attack)`, the switch point `1 − attack^(1/k)`. Run the tests until all nine pass, then run `python utility.py` and copy its output into your report.

### Part B: tune a companion (50 minutes)

6. Your companion has three actions: Attack, Drink and Guard (raise a shield). Copy `brute_scores` into a new function `companion_scores(hp_percent, enemy_hp, enemies_near, potions)`, where `enemies_near` is 0 to 5. Guard should score high when several enemies are near and health is middling, and low otherwise. Use at least one logistic and one piecewise curve somewhere in the three actions.
7. The brief, from your designer: "With one enemy near and the enemy fresh, drink below about 25% health. With three or more enemies near, guard between 25% and 50% health. Never drink with no potions. Never switch more than 3 times in the lecture's 12-think trace." Tune your curves and a commitment bonus until the brief holds. For each sentence of the brief, print a number that proves it (a switch point, a map row, or a switch count).
8. Print `decision_map()`-style maps for your companion at `enemies_near` = 1 and 3. Mark where the brief's boundaries are and where your map puts them.
9. Swap briefs with a neighbor. Find one situation, a specific set of inputs, where their companion does something their brief did not ask for. Write it down with the scores.

### Part C: the design note (at home)

10. Write a note of at most 300 words to your designer. Report each switch point your companion ended with, and the one situation your neighbor found. Then argue whether that situation should be fixed with a curve change, a new consideration, or a rank (dual utility) as in lecture section 4, and say what each option would cost in other situations.

## Deliverable

Your completed `utility.py` with `test_utility.py` passing (paste its output), plus a PDF with the Part A output, your Part B curves (formulas and a plot or table of each), the proof numbers for every sentence of the brief, the two decision maps, your neighbor's finding, and the design note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Toolkit (30%) | All nine tests pass; the zero veto stops evaluation; code is short and clear | All pass, code hard to follow | Curves work but scoring or choice fails a test | Tests mostly fail |
| Meets the brief (30%) | Every sentence of the brief proved with a printed number; switch points within 2 percentage points of the brief | Brief met, proof for most sentences | Brief partly met | Missing |
| Curve choices (15%) | Each curve's shape explained as a behavior ("rises late because...") | Curves listed without reasons | Only linear curves | Missing |
| Peer finding (10%) | Concrete inputs, the scores that caused it, and why it breaks the brief | Situation described, no scores | Vague | Missing |
| Design note (15%) | Compares curve, consideration and rank fixes with their side effects, recommends one | Recommends a fix, no comparison | No numbers | Missing |
