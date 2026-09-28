# CS101 · Lab 02: A cave with a way out

**Week:** 2 · **Time:** 2 hours in the lab · **Weight:** one of the weekly exercises (40% of the course across the semester)

**Lecture:** [Week 02, conditionals: room transitions and win/lose](../lectures/w02-conditionals-room-transitions-and-win-lose.md)

## Objective

Write the `if`/`elif`/`else` chains that move a player around a five-room cave, lock a door behind a key, and resolve a duel correctly in every case, including both players falling on the same frame and overkill. You will see an order bug happen, then fix it.

## Starter materials

- [`lab02-starter/cave.py`](lab02-starter/cave.py). A one-decision program with a map drawn in its header comment. It has two modes. `move` reads a room, whether you hold the key, and a command, and prints where you end up. `duel` reads two health values and prints the result. Two moves and a naive duel chain are already written.
- [`lab02-starter/check_lab02.py`](lab02-starter/check_lab02.py). A checker that runs 22 situations through your program. Do not edit it.

Run from inside `lab02-starter`:

```
python cave.py
python check_lab02.py
```

## Steps

1. **Draw the map as arrows (10 min).** On paper, draw each room as a box and each legal move as a labelled arrow. Count the arrows. That is how many movement branches you need, plus one for the locked door.
2. **Part A, movement (25 min).** Add a branch for every arrow. Make sure `Hall` and ` WEST ` (capitals, spaces) still work. The starter already cleans the input, so check that you see why.
3. **Part B, the locked vault (20 min).** First write the two vault branches in the *wrong* order, the general "north from the hall" branch above the "north from the hall with the key" branch. Run the checker and copy what it reports into your log. Then swap them and run again.
4. **Part C, the duel (25 min).** Write the truth table for `p1_out` and `p2_out` (four rows, plus two overkill rows). Fill in the intended result for each row. Then replace the naive chain so every row passes. Use `<=`.
5. **Run the checker (5 min)** until it prints `3/3 parts pass`.
6. **Stretch (optional).** Add a third mode, `race`, that reads two cars' positions and a finish line and prints `RESULT A wins`, `RESULT B wins`, `RESULT dead heat` or `RESULT racing`, using the lecture's check-yourself question 3 as the specification.

## Deliverable

Submit a zip with:
- Your edited `cave.py`.
- Your map drawing (photo is fine).
- A log (about 250 words) with: the checker output for the wrong-order vault from step 3 and one sentence explaining it; your duel truth table with intended results; and a short paragraph arguing for a tie policy other than sudden death for a game of your choice, naming the game.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker parts | 3/3 parts pass | 2 parts pass | 0-1 parts pass | 40% |
| Order bug evidence | Wrong-order output captured and explained by "first true branch wins" | Output captured, explanation vague | Step skipped | 15% |
| Truth table | All six rows with intended results that match the final code | Rows complete, one mismatch with code | Table missing or incomplete | 20% |
| Tie-policy argument | Names a game, a policy and a consequence for players | Policy named with little reasoning | Missing | 15% |
| Code readability | Branches grouped by room, named booleans for the duel | Correct but hard to scan | Deep nesting or dead branches | 10% |
