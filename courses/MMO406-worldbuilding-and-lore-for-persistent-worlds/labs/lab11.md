# MMO406 · Lab 11: The continuity checker

**Week:** 11, retcons and continuity ([lecture](../lectures/w11-retcons-and-continuity.md), [interactive](../examples/w11-retcon-blast-radius.html)).
**Time:** 2 hours in lab, plus about 3 hours at home.
**Weight:** part of the exercises (40%). The graph and tier table you build here become the "canon and continuity" chapter of your world bible.

## Objective

Implement the week 11 blast-radius model, a validator for dependency errors, and tier-based conflict resolution. Run them on a *Thornmere* canon file with planted problems. Then build the dependency graph for your own world, and write a retcon memo that prices one real change three ways before you choose.

## Starter materials

All in [`lab11-starter/`](lab11-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`continuity.py`](lab11-starter/continuity.py) has the model in its docstring and five empty functions: `descendants`, `blast`, `validate`, `resolve` and `contradiction_chance`. It also has a `report` function and a command line. As shipped it prints a TODO and exits with status 1.
- [`thornmere_canon.json`](lab11-starter/thornmere_canon.json) holds the twelve facts of the lecture table plus four more: a printed comic (C1), an in-world song (X1) and two legends (L1, L2). Every fact has a tier and the values it asserts. The file has exactly three planted dependency problems and four value conflicts.
- [`test_continuity.py`](lab11-starter/test_continuity.py) holds seven tests. They check the lecture's blast table on the twelve lecture facts, the full file (including a cycle, which your search must survive), the planted problems, tier resolution and the contradiction formula.

### The canon file format

```json
{
  "tiers": ["core", "game", "tie-in", "flavor"],
  "facts": [
    {"id": "F3", "text": "The Tidewardens were founded in 941 to rebuild the dikes",
     "depends_on": ["F1"], "cost": 1, "frozen": false, "tier": "core",
     "asserts": {"tidewardens_founded": 941}}
  ]
}
```

`tiers` lists tiers from highest to lowest. `asserts` holds the checkable values a fact states, so two facts contradict when they assert different values for the same key.

Run the tests and the report from the repository root:

```
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab11-starter/test_continuity.py
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab11-starter/continuity.py courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab11-starter/thornmere_canon.json
```

On the starter all seven tests report `TODO` and the script exits with status 1.

## Steps

1. **Search (20 min).** Implement `descendants`. Build a map from each id to the ids that depend on it, then walk it with a stack or queue and a `seen` set. Ignore dependencies on ids that do not exist. The `seen` set is what makes the search terminate on a cycle. In a cycle a fact becomes its own descendant, so `L1`'s descendants are `{L1, L2}`.
2. **Blast (15 min).** Implement `blast`: radius is the number of descendants, cost sums the non-frozen facts in the review set (the fact plus its descendants), frozen lists the frozen facts in the review set, sorted. The first three tests pass when steps 1 and 2 are right.
3. **Validate (15 min).** Implement `validate`. Report one `UNKNOWN_DEP` per missing id and one `CYCLE` per fact that is its own descendant. Return the list sorted.
4. **Resolve (30 min).** Implement `resolve` using the rule in the docstring and the tier table from lecture section 4. Then implement `contradiction_chance` (one line). Run the tests until all seven pass.
5. **Read the report (15 min).** Run the report on `thornmere_canon.json`. For each planted problem and each conflict, write one line: what it is and what a continuity lead should do. Then answer: F2's radius is 8 in the full file but 6 in the lecture. Which two facts account for the difference, and which of them makes F2 frozen-reaching?
6. **Your graph (60 min, at home).** Write a canon file for your own world with at least 25 facts: at least 8 core facts, 10 game-tier pieces of content (quests, dungeons, items, zones, factions) with realistic costs, 2 frozen tie-ins, and 3 flavor facts. Every fact asserts at least one key where that makes sense. Run `validate` until it is clean. Report the three facts with the largest cost `W` and the three with the largest radius. Are they the same three?
7. **Your retcon memo (45 min, at home).** Pick a change a future expansion might want (a character who should have lived, a date that blocks a flashback, a faction that should have had a secret). Price it as substitutive, subtractive and additive: review set, cost, frozen nodes touched and contradictions left. Recommend one and justify the choice in terms of blast radius and frozen media. Add the new node to your file if you choose the additive version, and rerun the checker.

## Deliverable

A zip or repository link containing:

- `continuity.py` with all seven tests passing (paste the test output into the report).
- Your canon file.
- `lab11.md`, 700 to 1,100 words, with: the Thornmere report and your one-line action for each problem and conflict (step 5); the top-three tables for your own graph and one paragraph on why radius and cost disagree or agree (step 6); your tier table; and the retcon memo with a three-row comparison table (step 7).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Checker correctness | All seven tests pass; search survives cycles; output sorted as specified | Five or six pass | Four or fewer | 25% |
| Reading the Thornmere report | Every problem and conflict has a sensible action; F2 difference explained (X1 and C1, with C1 reaching a frozen comic) | Most problems handled, explanation partial | Report pasted without reading | 15% |
| Own canon graph | 25+ facts across all tiers, clean validation, realistic costs, top-three analysis insightful | Meets counts, costs arbitrary or analysis thin | Under counts or failing validation | 25% |
| Tier table | Tiers defined with what each includes and who can override it; frozen media placed deliberately | Tiers listed without rules | Missing | 10% |
| Retcon memo | Three options priced with the model; recommendation follows from the numbers and frozen nodes; new node added and checked | Options priced, recommendation weakly argued | One option only, or no numbers | 25% |

<details>
<summary>Instructor check values</summary>

- Lecture graph (twelve facts): F1 11 / 73.5 / [N1]; F2 6 / 58.5 / []; F3 6 / 45.5 / [N1]; F4 2 / 31.5; D1 1 / 45; Y1 1 / 11; Q1 1 / 8 / [N1]; I1 0 / 0.5.
- Full file: F1 radius 13, cost 74.0, frozen [C1, N1]; F2 radius 8, cost 59.0, frozen [C1]; D1 radius 2, cost 45, frozen [C1]; L1 and L2 radius 2, cost 4.
- Planted problems: T1 depends on F7, which does not exist; L1 and L2 depend on each other.
- Conflicts: X1 (flavor) says the Drowning began in 910, overridden by F1 (core, 912); N1 (tie-in) dates the Tidewardens to 939, overridden by F3 (core, 941); C1 (tie-in) floods the Archive in 912, overridden by D1 (game, 915); I1 and R1 (both game) disagree on the signet's metal, unresolved. Q1 agrees with F4 on 941, which is not a conflict.
- Good actions: fix T1's reference or add the missing fact; break the legend cycle by making one legend the root (or accept it as an in-world paradox and mark both flavor, but still remove the dependency loop in the graph); keep the frozen N1 and C1 as logged contradictions, or add flavor-tier text that squares them; fix I1 or R1, choosing the cheaper one (I1, 0.5 days, versus R1, 30 days).
- Common student bugs: counting the fact itself in the radius (fails on the lecture values); adding frozen costs; marking agreeing lower-tier facts as overridden; infinite loop on L1 when `seen` is checked after pushing instead of before.

</details>
