# MMO406 · Lab 01: The tension ledger

**Week:** 1, setting as system ([lecture](../lectures/w01-setting-as-system.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** exercises (40% of the course, shared across the exercise labs). The ledger you write here is a required appendix of the final world bible (60%).

## Objective

Turn the week 1 model into a tool, then use it on your own setting. You will code the stock-and-flow ledger and an audit that reads a bible's tensions from JSON and flags entries that are not real tensions or not tied to a system. Then you will write the first tension list for your world bible and revise it until it supplies at least eight full expansions at a consumption rate you justify.

## Starter materials

All in [`lab01-starter/`](lab01-starter/). Standard-library Python, run with the program's `.venv/bin/python`.

- [`ledger.py`](lab01-starter/ledger.py), with a finished loader, `audit` and `report`, and five empty functions: `refill`, `launch_stock`, `simulate`, `full_expansions` and `problems`.
- [`coastal.json`](lab01-starter/coastal.json), the Salt Coast bible from the lecture's section 3 (10 plot tensions, 2 structural tensions, `c = 3`).
- [`broken.json`](lab01-starter/broken.json), a four-entry draft with two faults for the audit to catch.
- [`test_ledger.py`](lab01-starter/test_ledger.py), tests built from the lecture: the section 2 table (`N` = 4, 5, 10, unlimited), the check-yourself answers (7, 10 and 11 expansions), the stock sequence 12, 10, 8, 6, 4, 2, agreement between your simulation and your closed form for 750 input combinations, the Salt Coast audit (`P0 = 10`, `R = 1.5`, `N = 5`) and the two faults in the broken draft. The tests fail on the starter and pass once your functions are correct.
- The [interactive](../examples/w01-tension-ledger.html), for spot checks.

Run the tests from inside the starter folder:

```
cd courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab01-starter
../../../../.venv/bin/python test_ledger.py
```

## Steps

1. **Refill and stock (15 min).** Implement `refill` and `launch_stock`. Use `fractions.Fraction` for `g` so that 0.5 + 1 is exactly 3/2. A plot tension with an empty `wants` or `blocked_by` does not count toward `P0`.
2. **Simulate (15 min).** Implement `simulate` with the lecture's rule. A short expansion consumes nothing and still receives the refill.
3. **Closed form (15 min).** Implement `full_expansions`. Use integer floor division on fractions, not `math.floor` on floats. `test_simulate_agrees_with_closed_form` is your proof that the formula and the simulation agree.
4. **Audit (15 min).** Implement `problems`. Run `ledger.py broken.json` and read the report. In one sentence each, say how you would fix the two faults.
5. **Your first ledger (at home).** Write `mybible.json` for the world you will develop all term. At least 10 tensions, at least 2 of them structural, every structural tension tied to a named game system from your MMO301 world concept. Write `who`, `wants` and `blocked_by` as short phrases, not paragraphs.
6. **Justify `c` (at home).** Pick a shipped MMO expansion you know. Count the story arcs that close in it (main arc plus zone arcs). Use that count, scaled to your team's size, as your `c`. Cite the expansion and its year.
7. **Revise to eight (at home).** If your bible supplies fewer than 8 full expansions, revise it. You may not simply add plot tensions. Every revision must change `R` (a new structural tension, a higher `g` justified by a system, or a plot tension rewritten as structural). Keep every version and its report.
8. **Explain the mechanics (at home).** Add a short table in the style of the lecture's section 5: at least four mechanics from your game, each marked explain or tolerate, with the world rule and its obligations for the explained ones.

## Deliverable

- Your completed `ledger.py` with all six tests passing.
- The broken-draft report and your two one-sentence fixes.
- `mybible.json`, every revision, and a report of at most 700 words: the `c` you chose and why, the report output for each version, what you changed and why the change raised `R`, and the explain-or-tolerate table.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Correctness | All six tests pass; exact fractions used | Five pass, or floats cause an edge failure | Fewer than five pass | 25% |
| Ledger quality | Every entry has a clear want and block; plot and structural classified correctly with a reason | Most entries clear; one or two misclassified | Entries are lore paragraphs, not tensions | 20% |
| Structural tensions | Each tied to a named system, with a `g` justified by how that system changes the world | Tied to systems, `g` asserted without reason | Not tied to systems | 20% |
| Revision to eight | Final version reaches `N ≥ 8` by raising `R`; every version reported | Reaches 8 but partly by padding `P0` | Does not reach 8 or versions missing | 20% |
| Mechanics table | Four or more mechanics; obligations named and at least one turned into a tension | Table complete, obligations thin | Missing | 15% |
