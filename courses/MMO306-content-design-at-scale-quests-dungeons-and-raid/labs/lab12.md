# MMO306 · Lab 12: A content validator

**Week:** 12 ([lecture](../lectures/w12-content-tooling-and-pipelines.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** final dungeon (60%). Your final dungeon's content files must pass the validator you write here, extended with the rules from Part B.

## Objective

Write a validator for a small zone's quest, NPC, item, loot and text data, prove it catches a seeded set of defects without false alarms, extend it with rules of your own, and use the defect funnel to argue what your rules are worth in hours.

## Starter materials

All in [`lab12-starter/`](lab12-starter/). Standard-library Python 3, run with `.venv/bin/python` from the repository root or any Python 3.9+.

- [`validate_content.py`](lab12-starter/validate_content.py), with `load` written and `validate` to write. The docstring lists the nine error codes the tests expect and the exact rule for each.
- [`funnel.py`](lab12-starter/funnel.py), with the lecture's teaching values and two functions to write, `run_pipeline` and `insert_after`.
- [`content/zone_clean.json`](lab12-starter/content/zone_clean.json), a five-quest zone in three languages with no defects.
- [`content/zone_seeded.json`](lab12-starter/content/zone_seeded.json), the same zone with 14 seeded defects of 9 kinds. Don't read the diff before you write the validator. Treat it as a test.
- [`test_lab12.py`](lab12-starter/test_lab12.py), nine tests: the clean zone gives no errors, the seeded zone gives exactly the expected `(code, id)` pairs, loot chances allow float error, long chains aren't cycles, a self-requirement is, and the funnel reproduces the lecture's 853.0 and 415.8 hours. All fail on the starter.
- The [interactive](../examples/w12-defect-funnel.html) for checking Part C.

## Steps

### Part A: the validator (50 min)

1. Implement reference checks first (`REF_NPC`, `REF_ITEM`, `REF_STRING`, `REF_QUEST`) and run `python validate_content.py content/zone_seeded.json`.
2. Add `DUP_ID`, `XP_BUDGET` and `LEVEL_ORDER`.
3. Add `CYCLE` with a depth-first search over prerequisites. Every quest on a cycle gets one error. GD202 week 14 covers state search if you want a refresher.
4. Add `LOOT_SUM` with a tolerance for float error.
5. Run the tests until the six validator tests pass. Then time the validator on a zone scaled to 5,000 quests (write a generator that copies the clean zone with new IDs). It must run in under one second, so it can run on every save.

### Part B: your own rules (30 min)

6. Add three rules your final dungeon needs, each with a new code. Candidates include: every boss has an enrage timer shorter than the instance reset; no quest item is sellable; every string fits its UI box at 130% of its English length; reward items are at or below the quest's level. For each rule, add one test with a small in-memory content file that breaks it and one that doesn't.
7. Split your codes into errors (block the build) and warnings (weekly review). Justify each choice in one line.

### Part C: what the rules are worth (40 min)

8. Implement `run_pipeline` and `insert_after`. Run all tests.
9. Estimate, for your own final dungeon, the defects per class per 1,000 items and a catch rate for your validator per class. Write each estimate with one sentence of reasoning.
10. Run the funnel with and without your validator. Report found, hours and escaped per stage, and the share of live cost that interaction defects account for after your validator.
11. Name the next stage you would invest in and show, with the funnel, how many hours it saves.

## Deliverable

- The completed `validate_content.py` and `funnel.py` with all tests passing, your three new rules with their tests, and the 5,000-quest timing script.
- A report of at most 2 pages: the rules table (code, error or warning, reason), the Part C estimates and funnel tables, and your investment recommendation with its hours saved.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Validator correctness (Part A) | All six validator tests pass; no false alarms on the clean zone; 5,000 quests in under 1 s | Tests pass but slow, or one rule has a false alarm | Seeded test fails | 35 |
| Own rules (Part B) | Three useful rules with passing and failing tests; error/warning split justified | Rules present, tests or justification thin | Missing | 25 |
| Funnel analysis (Part C) | Funnel tests pass; estimates reasoned; recommendation backed by hours | Numbers present, reasoning thin | Missing | 25 |
| Code quality | Readable, each rule a small function, messages say what to fix | Works, hard to extend | Does not run | 15 |
| **Total** | | | | **100** |
