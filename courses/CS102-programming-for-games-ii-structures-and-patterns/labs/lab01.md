# CS102 · Lab 01: Gated stats

**Week:** 1 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** one of the weekly labs (labs are 40% of the course)

**Lecture:** [Week 01, classes, objects and encapsulation](../lectures/w01-classes-objects-encapsulation.md)

## Objective

Build two small classes whose invariants cannot be broken from outside: a stat stage that stays in −6 to +6 under any ability, and a fighter whose health stays in 0 to max. Then add a rule change of your own and show that it took one edit, not one per caller.

## Starter materials

All in [`lab01/`](lab01/):

- `stats.py`: the `StatStages` and `Fighter` classes with the constructors and properties written and every method body marked `TODO`.
- `test_stats.py`: 15 unit tests using Python's built-in `unittest`, including a randomized test that plays 2,000 random stage changes per ability and checks the invariant after each one.

You need Python 3.11 or later. No packages to install. From the `lab01` folder run:

```
python -m unittest -v
```

On the starter code, 13 tests fail with `NotImplementedError` and 2 pass (the ones that check `stage` and `hp` are read-only). That is expected.

## Steps

1. **Read before writing (10 min).** Read both classes and every test. For each class, write its invariant as one line in a comment at the top of the class. Write down, in your own words, the order of rules in `StatStages.change` that the tests expect.
2. **Multiplier (10 min).** Implement `StatStages.multiplier` as an exact `Fraction`. Run the tests; `test_table` should pass.
3. **The gate (20 min).** Implement `StatStages.change` and `reset`. Every change to `_stage` must happen inside `change` or `reset`. Run the tests; all `TestChange` tests should pass, including the randomized one.
4. **Fighter (20 min).** Implement `effective_attack`, `take_damage` and `heal`. Negative amounts are a programming error and must raise `ValueError`, not clamp. A downed fighter cannot be healed. Run the full suite until it is green.
5. **Attack your own class (10 min).** In a scratch file, try to put a `StatStages` outside −6 to +6 or a `Fighter` above `max_hp` without touching any name that starts with an underscore. Record every attempt and the result.
6. **A new rule, one edit (30 min).** Invent one new ability that changes how stages move. Examples: "Stubborn: drops are halved, rounding toward zero", "Overclock: the cap is ±8 for this Pokémon only", "Mirror: every change also applies half as much to defense". Implement it by editing only `StatStages` (and `Fighter.__init__` if the ability must reach a second stat). Add at least three tests for it, including one near a limit.
7. **Count the call sites (at home).** Write a file `moves.py` with at least five "move" functions that call `fighter.attack.change(...)` or `fighter.heal(...)`. Show with `git diff` or a before/after listing that step 6 changed none of them.

## Deliverable

A zip or repository link containing:

- `stats.py` with all methods implemented and your new ability.
- `test_stats.py` with the original 15 tests plus at least 3 of your own, all passing. Paste the final `python -m unittest -v` output into `RESULTS.txt`.
- `moves.py` from step 7.
- `NOTES.md`, at most 400 words: each invariant and the single method that enforces it; your attack attempts from step 5 and their results; which rule-order choice your ability forced you to make and why you chose it.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Correctness | All 15 provided tests pass; no test edited | 12-14 pass, or a provided test was changed with a stated reason | Fewer than 12 pass | 30% |
| Encapsulation | `_stage` and `_hp` change only inside their own class's methods; no public setters that skip rules | One method bypasses the gate | Callers write private fields directly | 20% |
| New ability | Implemented in one place; three or more tests, one at a limit; zero edits to `moves.py` | Works but touches callers, or tests miss the limit case | Missing or breaks the invariant | 25% |
| Attack log | Five or more concrete attempts, each with the observed result | Two to four attempts | None | 10% |
| Notes | Names each invariant, its gate, and a rule-order decision with a reason, in plain words | Invariants named, no rule-order reasoning | Missing or generic | 15% |
