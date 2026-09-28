# CS102 · Lab 14: A test suite for the combat module

**Week:** 14 ([lecture](../lectures/w14-unit-testing-gameplay-rules.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** labs (40% of the course grade). The suite you write here runs against your final data-driven combat module, so tests that pass on correct code and fail on broken code earn marks twice.

## Objective

Find six planted bugs in six gameplay rules using example, property and injected-roll tests, fixing each one only after a test fails because of it. Then protect the lab 13 data with data tests and protect a whole fight with a replay test. Finally, measure why a sampling test would have missed one of the bugs.

## Starter materials

All in [`lab14-starter/`](lab14-starter/). Standard library only (`unittest`), Python 3.10 or later.

- `rules.py`: six pure rules (`damage_after_armor`, `is_crit`, `rage_bonus`, `xp_to_next`, `split_gold`, `regen`). Each docstring states the intent. Each function has exactly one bug.
- `fakes.py`: `ScriptedRng`, a stand-in for `random.Random` whose `random()` and `randint()` return values you script.
- `test_rules.py`: two example tests for `damage_after_armor` (both pass) and TODO markers for the rest.
- `fight.py`: a 30-second, 300-tick duel driven by a list of commands, with `simulate(commands, seed)`, `fingerprint(units)` and `record(path)`. `python fight.py` replays the saved fight and prints `MATCH` or the new fingerprint. Only `python fight.py --record` rewrites `replay_30s.json`, so do not use it while you experiment in step 8.
- `replay_30s.json`: a recorded fight (seed, 90 commands, expected fingerprint).
- Your lab 13 folder, for Part B. If your loader is not finished, use `../lab13-starter/` with the reference loader your instructor posts after the lab 13 deadline.

Run everything from inside the folder with `python -m unittest -v`.

## Steps

### Part A: find the six bugs (60 min)

For each rule, in any order:

1. Read only the docstring. Write one sentence of intent, as a property: what must be true for every input.
2. Turn it into a test method that sweeps a small domain with `self.subTest(...)`. Suggested domains: `raw` 1 to 100 and `armor` 0 to 100; `stacks` 0 to 30; `level` 1 to 60; `total` 0 to 300 and `players` 1 to 5; `hp` 1 to 100 with `max_hp` 100. For `is_crit`, inject rolls with `ScriptedRng` and test `chance` 0.0, 0.25 and 1.0 at and around their boundaries.
3. Run the suite. If your test fails, record the **smallest** failing input in a table in your README. If it passes, your property is too weak or aimed wrong. Write a second one before you look at the code.
4. Only now read the code, fix the bug, and rerun. The test that caught it stays in the suite as a regression test.

Add at least one example test per rule as well, named as a sentence (`test_level_one_needs_100_xp`).

### Part B: data tests (20 min)

5. In a new class `WeaponDataTests`, load your lab 13 `weapons.csv` once in `setUpClass`. Test that every weapon with an `upgrade` has strictly higher DPS than the weapon it upgrades from, one `subTest` per weapon.
6. Create `known_ids.txt` listing every weapon id currently in the file, one per line. Test that no known id has disappeared. Then rename `hand_axe` to `handaxe` in a copy of the file, point the test at the copy, and confirm it fails with a readable message. Put the id back.

### Part C: replay test (20 min)

7. Write `test_recorded_fight_is_unchanged`: load `replay_30s.json`, convert each command to a tuple, run `simulate` with the saved seed, and assert the fingerprint matches.
8. Change the damage floor in `fight.py` from `max(1, ...)` to `max(0, ...)`. Does the replay test fail? Explain in two sentences why or why not, using the fight's numbers. Then change `guard` to reduce a hit by a third instead of half and run again. Undo both changes.

### Part D: why sampling would not have found it (20 min)

9. Write a *sampling* test for `is_crit` at `chance = 0.25`: roll 1,000 times with `random.Random(seed)` and pass if the crit rate is within `3 × sqrt(0.25 × 0.75 / 1000)` of 0.25. Compute that tolerance by hand first and write it in your README.
10. Run your sampling test against the **original, buggy** `is_crit` with seeds 0 to 199. How many of the 200 runs fail? Then do the same against a deliberately broken version that returns `rng.random() < chance * 0.96`. How many fail now? Compare both with your injected-roll test from Part A in three sentences.

## Deliverable

A zip of your `lab14-starter/` folder with:

- `rules.py` with all six bugs fixed, `test_rules.py` with every test passing, and `known_ids.txt`.
- `README.md` (at most two pages): how to run the suite, the Part A table (rule, property sentence, smallest failing input, one-line fix), the Part C answers, and the Part D tolerance, both failure counts and your comparison.

Your instructor will also run your `test_rules.py` against six hidden broken versions of `rules.py`, each with one bug. Each hidden bug your suite catches is worth marks.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Six bugs found by tests (Part A) | Six properties, each fails before the fix, smallest inputs correct | Four or five found by tests, or smallest inputs missing | Three or fewer | 30 |
| Hidden-bug detection | Suite catches 5 or 6 hidden bugs | Catches 3 or 4 | Catches 2 or fewer | 15 |
| Data tests (Part B) | Both tests pass on good data and fail readably on the renamed copy | One test works | Missing | 15 |
| Replay test (Part C) | Test passes; both experiments explained with numbers from the fight | Test passes, explanations vague | Missing | 15 |
| Sampling vs injected (Part D) | Tolerance correct, both counts reported, comparison names flakiness and detection power | Counts reported without clear comparison | Missing | 15 |
| Test quality | Names read as sentences; arrange-act-assert; specific assertion methods | Mostly clear | Tests hard to read or use `assertTrue(a == b)` throughout | 10 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

Planted bugs and the smallest failing inputs a good property finds:

1. `damage_after_armor` returns 0 when `raw == armor`. Smallest: `raw=1, armor=1`.
2. `is_crit` uses `<=`, so `chance=0.0` crits on a roll of exactly `0.0`. Found only by injection. A sampling test essentially never sees it.
3. `rage_bonus` uses `stacks % 11`, so 11 stacks give no bonus. "Never drops" fails at 11 (and 22).
4. `xp_to_next` indexes `XP_TABLE[level]` instead of `level - 1`: level 1 returns 283 instead of 100, and level 59 raises `IndexError`.
5. `split_gold` drops the remainder. Smallest: `total=1, players=2` (sum 0).
6. `regen` adds without capping. Smallest with rate 5, dt 1: `hp=96`, returns 101.

Part C: with the recorded seed, the fight's final fingerprint is `bandit:-4:0;knight:50:0`. The `max(0, ...)` change only matters when a roll minus armor is 0 or less, which no roll in this fight produces (knight's minimum 6 vs armor 1, bandit's minimum 4 vs armor 3), so the replay still passes. That is the expected answer: a replay test only covers what the recorded fight exercises. The guard change alters the fingerprint.

Part D: tolerance is `3 × sqrt(0.1875 / 1000) ≈ 0.0411`. With seeds 0 to 199 the reference run gives 0 failures against the original `is_crit` (its bug lives only at a roll of exactly 0.0) and 0 failures against the 0.96 version (true rate 0.24), because a 1-point shift is a quarter of the 4.1-point tolerance. Both bugs are invisible to sampling at this size. The injected-roll boundary test catches the first in one call. The guard experiment changes the fingerprint to `bandit:-2:0;knight:52:0`.

</details>
