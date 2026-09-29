# MMO406 · Lab 10: The foreshadowing plan

**Week:** 10, expansion planning ([lecture](../lectures/w10-expansion-planning.md), [interactive](../examples/w10-foreshadow-horizon.html)).
**Time:** 2 hours in lab, plus about 3 hours at home.
**Weight:** part of the exercises (40%). The briefs you write here become the "expansions" chapter of your world bible.

## Objective

Implement the week 10 foreshadowing model and an auditor that reads a plan of hooks and says which ones are planted too early or too late. Fix a sample plan for *Thornmere*, then write a three-expansion arc and three expansion briefs for your own world, with every hook's lead time defended by a number.

## Starter materials

All in [`lab10-starter/`](lab10-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`foreshadow.py`](lab10-starter/foreshadow.py) has the model in its docstring and four empty functions: `expected_value`, `best_horizon`, `best_whole` and `audit`. It also has a `report` function and a command line. As shipped it prints a TODO and exits with status 1.
- [`thornmere_plan.json`](lab10-starter/thornmere_plan.json) is a plan for the lecture's invented world: launch plus four expansions, seven hooks, a team plan-change rate `ρ = 0.2`, `v = 1`, and the three hook types from the lecture (vague `D = 0.5`, named `D = 2`, announced `D = 4`). Exactly four hooks are badly timed.
- [`test_foreshadow.py`](lab10-starter/test_foreshadow.py) holds seven tests with values from the lecture: the table in section 2, the continuous and whole-number optima (including ties, which go to the lower `d`), the statuses of the seven Thornmere hooks, and input validation.

### The plan file format

```json
{
  "rho": 0.2,
  "v": 1.0,
  "D": {"vague": 0.5, "named": 2.0, "announced": 4.0},
  "hooks": [
    {"id": "H1", "text": "Lights seen under the drowned lowlands",
     "type": "vague", "planted": 0, "payoff": 3}
  ]
}
```

`planted` and `payoff` are expansion numbers, with 0 for launch. The lead time is `d = payoff − planted`. A hook's status is "too early" if `d > d* + 1`, "too late" if `d < d* − 1`, and "ok" otherwise.

Run the tests and the report from the repository root:

```
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab10-starter/test_foreshadow.py
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab10-starter/foreshadow.py courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab10-starter/thornmere_plan.json
```

On the starter all seven tests report `TODO` and the script exits with status 1.

## Steps

1. **Model (20 min).** Implement `expected_value` and `best_horizon`. The first two tests pass when they are right. Check one value by hand against the lecture table.
2. **Whole-number optimum (15 min).** Implement `best_whole`. Loop `d` from 0 to `d_max` and keep the best, replacing it only when a later value is higher by more than `TIE`. That rule gives the lowest `d` on ties, which the tests check with two exact ties from the lecture.
3. **Auditor (30 min).** Implement `audit`. Validate the inputs first, then compute one row per hook and return the rows sorted by id. Do not modify the plan you were given. Run the tests until all seven pass.
4. **Fix Thornmere (30 min).** Run the report on `thornmere_plan.json`. For each of the four badly timed hooks, choose one repair and save the result as `thornmere_plan_v2.json`. A repair can move the planting expansion, move the payoff, or change the hook's type (for example, turning a named villain into a vague rumor until one cycle before the payoff). Record each repair in a table: hook, problem, repair, `d` and `E(d)` before and after. The v2 plan must report every hook as "ok" with no negative `E`, and the announced trilogy must either become "ok" or stop being an announcement.
5. **Estimate your team's `ρ` (15 min).** Use a real record if you have one: your studio project's sprint plans, a roadmap from PR201 or PR301, or last term's group project. Count the items planned one cycle ahead and how many changed. If you have no record, use `ρ = 0.25` and say so. Report the count and your `ρ`.
6. **Your arc (45 min, at home).** Write a plan file for your own world: launch plus three expansions, with at least eight hooks, at least one of each type. Every hook needs a one-sentence text. Run the auditor with your `ρ` until every hook is "ok". Then change `ρ` by 0.1 in the unfavourable direction and run it again. Note which hooks change status. Those are the ones your plan is most exposed on.
7. **Your briefs (60 min, at home).** Write one expansion brief per expansion, using the table in lecture section 5. Every brief must name its stakes rung, list its lead-in hooks with their `d` and `d*` from the auditor, and give an escape hatch for each named hook. At least one expansion must step down or change the kind of stakes, with a sentence on why.

## Deliverable

A zip or repository link containing:

- `foreshadow.py` with all seven tests passing (paste the test output into the report).
- `thornmere_plan_v2.json` and your own plan file.
- `lab10.md`, 800 to 1,200 words, with: the Thornmere repair table and its report before and after; your `ρ` estimate with its evidence; your plan's report at your `ρ` and at `ρ + 0.1`, with one paragraph on the exposed hooks; and the three expansion briefs.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model and auditor | All seven tests pass; code validates input and leaves the plan unmodified | Five or six pass | Four or fewer | 25% |
| Thornmere repairs | All four fixed, v2 all "ok", each repair justified in terms of `d`, `D` or `ρ` | Fixed, but repairs unexplained or one hook still off | Fewer than three fixed | 15% |
| `ρ` estimate | Evidence counted from a real record, or the default stated honestly; sensitivity run and exposed hooks discussed | Estimate given with thin evidence | No estimate or no sensitivity run | 15% |
| Arc design | Eight or more hooks across all three types; vague hooks planted early and specific ones late; every hook "ok" | Meets counts, a few hooks only "ok" by accident | Under eight hooks or failing the auditor | 20% |
| Expansion briefs | All fields filled; stakes plan deliberate with a step-down or change of kind; an escape hatch for every named hook | Briefs complete but stakes or escape hatches generic | Briefs missing fields | 25% |

<details>
<summary>Instructor check values</summary>

- `expected_value(2, 1, 2, 0.2)` is 0.56; `expected_value(8, 1, 2, 0.1)` is 2.3047; `best_horizon(1, 2, 0.2)` is 2.4814; `best_horizon(1, 4, 0.3)` is 0.
- `best_whole(1, 2, 0.2)` is `(2, 0.56)` (tie with `d = 3`). `best_whole(1, 0, 0.25)` is `(3, 1.265625)` (tie with `d = 4`). `best_whole(1, 4, 0.2)` is `(0, 0.0)` (tie with `d = 1`).
- Thornmere report on a correct solution:

```
H1   vague       3   3.98    1.29  ok
H2   named       4   2.48    0.46  too early
H3   announced   3   0.48   -0.42  too early  (negative)
H4   named       0   2.48    0.00  too late
H5   vague       3   3.98    1.29  ok
H6   named       2   2.48    0.56  ok
H7   vague       1   3.98    0.70  too late
```

- "ok" ranges at `ρ = 0.2`, `v = 1`: vague hooks `d` = 3 or 4; named hooks `d` = 2 or 3; announced hooks `d` = 0 or 1.
- Typical good repairs: H2 planted in expansion 1 or 2 instead of launch (or kept at launch but made vague, with `d = 4`); H3 turned into a vague in-game prophecy with `d = 3`, or announced only in expansion 2 or 3; H4 seeded in expansion 0 or 1 as a named exile; H7 paid off in expansion 3 or 4. A student who keeps H7's payoff in expansion 1 and makes it "named" still gets "too late" (`d = 1` is below 1.48), which is a useful discovery to discuss.
- Common student bug: computing `d` as `planted − payoff`, which the validation test catches, or returning rows in file order instead of sorted by id.

</details>
