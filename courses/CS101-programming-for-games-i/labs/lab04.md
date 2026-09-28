# CS101 · Lab 04: Refactoring the combat turn

**Week:** 4, functions and decomposition ([lecture](../lectures/w04-functions-and-decomposition.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the weekly exercises (40%). The functions you write here come back in lab 05, where the inventory feeds the potion count.

## Objective

Take a working but tangled text-adventure fight written as one long loop, split it into small pure functions, and make a set of boundary tests pass. Along the way, find the one boundary bug hiding in the original loop and explain it in two sentences.

## Starter materials

All in [`lab04-starter/`](lab04-starter/). Standard-library Python 3.10 or later, no packages.

- [`combat.py`](lab04-starter/combat.py) has three parts. Part A, `fight_tangled()`, is the original 50-line fight between you and a rat. It works, mostly. Part B has six empty functions (`attack_hits`, `damage`, `apply_damage`, `drink_potion`, `is_defeated`, `resolve_attack`), each with a docstring that says exactly what it must do. Part C, `play()`, is where you rebuild the fight from Part B.
- [`test_lab04.py`](lab04-starter/test_lab04.py) has seven tests, most of them at edges: a natural 20 against impossible defense, damage that would go below 1, a potion at full health, HP of exactly 0. Run it with `python test_lab04.py`. On the starter it reports `0/7 tests passed`.

The combat rules are the D&D-style rules from lecture section 2: roll a d20, a natural 20 always hits and doubles damage, a natural 1 always misses, otherwise you hit when `roll + bonus >= defense`. Damage is `attack − armor` with a floor of 1.

## Steps

1. **Play it.** Run `python combat.py` twice and win at least once. Then read `fight_tangled()` and, on paper, draw a box around each block that does one job. Label each box with a verb ("roll to hit", "clamp HP"). You should find at least six boxes.
2. **Write the pure functions.** Fill in Part B one function at a time. After each, run the tests. Do not use `print`, `input` or `random` inside Part B; `test_functions_are_pure` checks the first two.
3. **Find the bug.** `test_is_defeated_boundary` encodes the intended rule: a combatant at exactly 0 HP is out. Compare it with the line marked "look closely" in Part A. Run `fight_tangled(3)` and always attack. Write down what happens on turn 3 and why.
4. **Rebuild `play()`.** Rewrite the fight in Part C using only your Part B functions for rules. `play()` is the only place allowed to print, ask for input or roll dice. Delete the `return fight_tangled(seed)` line when your version works.
5. **Check equivalence.** With the same seed and the same choices, your `play()` and `fight_tangled()` should print the same rolls and damage, up to the turn where the bug changes the outcome. Run both with seed 3 and "always attack", and paste the two transcripts side by side in your notes.
6. **Extend (pick one).** (a) Add a "defend" action that adds 4 to your defense until your next turn. Write two tests for it first. (b) Give the rat a 25% chance to flee when below 5 HP. Pass the random number into a pure function `rat_flees(hp, roll)` so it stays testable, and write tests for `hp = 4, 5` and `roll` on each side of the threshold.

## Deliverable

Your edited `combat.py` with `python test_lab04.py` reporting `7/7 tests passed` (plus your extension's tests), and a note of at most 250 words covering: the bug from step 3 in two sentences, the transcripts from step 5, and one sentence on which function you'd expect to reuse in a different game and why.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 7/7 provided tests pass | 5-6 pass | 4 or fewer | 30% |
| Decomposition of `play()` | Rules live only in Part B; `play()` reads like a list of steps | Some rule logic still inline in `play()` | `play()` still calls `fight_tangled` or duplicates it | 25% |
| Bug explanation | Names the comparison, the HP value that exposes it and the visible effect (a 0 HP rat still bites) | Finds the line but explanation is vague | Not found | 15% |
| Extension with tests | Tests written first, cover both sides of each new comparison, pass | Works, tests thin | Missing or untested | 20% |
| Code quality | Clear names, docstrings kept, no globals for game state | Minor naming or duplication issues | Hard to follow | 10% |
