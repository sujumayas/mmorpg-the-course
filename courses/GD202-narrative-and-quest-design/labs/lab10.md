# GD202 · Lab 10: Lore budget

**Week:** 10, lore delivery without walls of text ([lecture](../lectures/w10-lore-delivery-without-walls-of-text.md)).
**Time:** 2 hours in lab, plus about 2 hours at home.
**Weight:** part of the dialogue exercises (40%).

## Objective

Implement the reading-decay model from the lecture as a small planner, fit the keep-reading chance `s` from playtest data, and use the planner to turn a 21-sentence lore dump into a delivery plan that gets at least 1.5 times as many sentences read while forcing every need-to-know fact on every player.

## Starter materials

All in [`lab10-starter/`](lab10-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`lore_budget.py`](lab10-starter/lore_budget.py) has six empty functions (`expected_read`, `completion`, `fit_s`, `plan_value`, `break_even_f`, `best_split`) and a provided `report` that prints a plan table once they work.
- [`test_lore_budget.py`](lab10-starter/test_lore_budget.py) holds the lecture's test values: `E(3) = 1.952` and `E(20) = 3.954` at `s = 0.8`, the four-note split at 6.45, the mixed plan at 10.08, break-even find chances of 0.37 and 0.25, and a best-split check where a low find chance makes the forced wall win.
- [`lore_dump.md`](lab10-starter/lore_dump.md) is an invented quest-giver speech of about 400 words in 21 sentences for a quest called "Light the Saltmere Lamp". It buries almost every fact the player needs in sentences 13 to 20.
- [`playtest_pages.csv`](lab10-starter/playtest_pages.csv) is invented telemetry from 50 testers reading a 6-page version of a similar text, one sentence per page. It gives how many testers reached each page.
- [`sample_plan.csv`](lab10-starter/sample_plan.csv) shows the plan format: one row per piece with its channel, sentence count, find chance and tier (`need`, `nice` or `fans`).
- The interactive [`examples/w10-lore-chunking.html`](../examples/w10-lore-chunking.html) for spot checks.

Run the tests from the repository root:

```
.venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab10-starter/test_lore_budget.py
```

On the starter every test reports `TODO` and the script exits with status 1. When all six pass it prints `All tests pass.` Then score a plan:

```
.venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab10-starter/lore_budget.py sample_plan.csv 0.8
```

The last argument is `s`.

## Steps

### Part A: the planner (40 min)

1. **Expected reading.** Implement `expected_read(n, s)` and `completion(n, s)`. Handle `n = 0` (a wordless piece, such as scorch marks) and `s = 1`. Check `E(3)` by hand first.
2. **Fit s.** Implement `fit_s`. Apply it to `playtest_pages.csv` using the last page. Then compute the page-to-page ratios (34/41, 28/34, and so on). Write two sentences on whether a constant `s` looks reasonable for this text.
3. **Plans.** Implement `plan_value`, `break_even_f` and `best_split`. Run the tests until all six pass.

### Part B: the lore dump (40 min)

4. **Tier it.** Number the 21 sentences of `lore_dump.md`. Mark each one need, nice or fans. The need tier is what a player must know to finish the quest: where the key is, who has to be spoken to and in what order, how to reach the stair, and the one physical danger.
5. **Measure the wall.** With your fitted `s`, compute `E(21)` and the share of players who reach each need-to-know sentence in its current position. Record the lowest.
6. **Redesign.** Write a delivery plan as a CSV in the sample format. Rules:
   - Every need-tier fact sits in a piece with find chance 1.0 (forced dialogue, a quest objective line, or an unmissable bark), and in the first two sentences of that piece.
   - Each other piece has a channel from lecture section 4 and a find chance of 0.3, 0.6 or 0.9, with a one-line reason tied to where it sits.
   - Rewrite every piece in your own words. You may cut facts. Keep a list of what you cut.
7. **Score it.** Run `lore_budget.py` on your plan with your fitted `s`. Your plan must reach at least `1.5 × E(21)` sentences read. If it doesn't, use `break_even_f` to find which pieces are dragging it down, and fix them.

### Part C: at home

8. **Stress test.** Rerun your plan with `s = 0.6` (a player in a hurry) and `s = 0.95` (a lore fan). Report both totals and the reach of your need-tier sentences. At which `s` does your plan's advantage over the wall shrink the most, and why?
9. **Write the pieces.** Write the final text of every piece, with its channel and where it sits in the level. Keep each piece to three sentences or fewer.

## Deliverable

`lore_budget.py` with all tests passing, your `plan.csv`, and a document of at most 600 words with:

- the tiered sentence list from step 4 and the reach table from step 5;
- the fitted `s` and your two sentences on the constant-`s` assumption;
- the `lore_budget.py` report for your plan, and the step 8 totals;
- the final text of every piece;
- a justification of at most 250 words covering what your plan loses compared with the wall (coherence, order, production cost) and why you accept it.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Planner correctness | All six tests pass; `s` fitted and the ratio check discussed | Five tests pass, or `s` fitted without the ratio check | Fewer than five pass | 25% |
| Tiering and measurement | Need tier covers every quest-critical fact and nothing else; reach table correct | One fact misplaced between tiers, or one reach value wrong | Tiers arbitrary or reach missing | 20% |
| Plan quality | At least 1.5 times the wall with need facts forced and first; find chances justified by placement | Target met but one find chance unjustified, or need facts forced but not first | Target missed or a need fact left to chance | 25% |
| Writing | Every piece leads with its payoff, three sentences or fewer, at most one new proper noun each, one consistent voice | Most pieces meet the rules | Pieces are cut-and-paste fragments of the dump | 20% |
| Judgment | Stress test explained with numbers; the losses of splitting named honestly | Stress test run, explanation thin | Missing | 10% |

<details>
<summary>Instructor check values</summary>

- `fit_s(15, 50, 6) = 0.818`. Page ratios run 0.83, 0.82, 0.82, 0.83, 0.79, so a constant `s` fits this data well.
- At `s = 0.818`, `E(21) ≈ 4.43`, so the target is about 6.65 sentences read. At `s = 0.8`, `E(21) ≈ 3.96`.
- Need facts: sentence 8 (where Ide lives), 13 (the key is needed), 14 (the chapel), 16 and 17 (the order: Ide's word, then the verse), 19 (causeway at low tide) and 20 (rotten steps). At `s = 0.818` the share reaching sentence 8 is about 20%, sentence 13 about 7%, and sentence 20 about 1.8%.
- `sample_plan.csv` at `s = 0.8`: 12 sentences, wall 3.73, plan 4.76 (1.28 times). It is below the 1.5 target on purpose.

</details>
