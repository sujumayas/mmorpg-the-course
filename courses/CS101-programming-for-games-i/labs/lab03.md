# CS101 · Lab 03: Loop it

**Week:** 3 · **Time:** 2 hours in the lab plus up to 1 hour at home · **Weight:** one of the weekly exercises (40% of the course across the semester). Mini-game 1 (the Ledge Run platformer, labs 07 to 09) reuses this lab's read, change, check order for its win and loss checks.

**Lecture:** [Week 03, loops: the game loop concept](../lectures/w03-loops-and-the-game-loop.md)

## Objective

Turn a one-turn cave into a playable turn loop with a key, a vault, a move limit and a win check. Then write a frame loop that reproduces the Space Invaders speed table by counting frames, and compare what you measure with the lecture's `F / N` model.

## Starter materials

- [`lab03-starter/loop_cave.py`](lab03-starter/loop_cave.py). The Lab 02 map as one turn of a game with state (`room`, `has_key`, `moves`, `playing`). It plays one command and stops.
- [`lab03-starter/invaders.py`](lab03-starter/invaders.py). A frame loop with the update step missing and a safety counter that stops it after 100,000 frames.
- [`lab03-starter/check_lab03.py`](lab03-starter/check_lab03.py). A checker with 8 cave scripts and 8 invader configurations. Do not edit it.

Run from inside `lab03-starter`:

```
python loop_cave.py
python invaders.py
python check_lab03.py
```

## Steps

1. **Part A, the loop (20 min).** Wrap the whole turn in `while playing:`. Indent it by four spaces. Play it by hand: `north`, `south`, `quit`.
2. **Part B, key and vault (20 min).** Add `take key` in the armory and the locked vault. Reuse your Lab 02 branch order.
3. **Part C, win and lose (15 min).** Add the outcome checks. Read the rule in the header about the fifteenth move and decide which check goes first. Write the reason in one sentence in your log.
4. **Trace (10 min).** Before running, trace the commands `north`, `east`, `take key`, `west`, `north` in a table with columns for iteration, command, room, `has_key`, `moves` and printed line.
5. **Part D, the frame loop (25 min).** Fill in the update step in `invaders.py`. Do not use the formula. Run it for 55, 28, 11 and 1 aliens at 60 fps with 1 alien per frame, and copy the results into a table next to the lecture's table.
6. **Two per frame (15 min).** Run 55, 11 and 1 aliens with 2 aliens per frame. The model predicts `N / 2` frames per step. Compare with what you measured and explain any difference.
7. **Run the checker** until it prints `4/4 parts pass`.
8. **Stretch (optional).** Add a `lamp_oil` that drops by 7 each move and ends the game at `lamp_oil <= 0`. Which rule ends the game first, the move limit or the oil?

## Deliverable

Submit a zip with:
- Your edited `loop_cave.py` and `invaders.py`.
- A log (about 300 words) with: your trace table from step 4; the one-sentence reason for your check order; your Part D table (measured frames, seconds and speed for 55, 28, 11 and 1 aliens) beside the lecture's model values; the two-per-frame comparison and its explanation.
- One paragraph: the cave's move limit counts moves, not seconds. Would the invaders' speed-up still work if the arcade ran at 30 frames per second? Use the model to answer.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker parts | 4/4 parts pass | 2-3 parts pass | 0-1 parts pass | 35% |
| Trace table | Every iteration correct, including `moves` and printed line | One or two cells wrong | Missing | 15% |
| Measured vs model | All four rows measured and compared; two-per-frame difference explained by whole frames | Rows present, explanation vague | Formula used instead of measuring, or rows missing | 25% |
| 30 fps paragraph | Uses `d × F / N` with numbers and states what changes and what does not | Correct conclusion without numbers | Missing or wrong | 15% |
| Code readability | Loop controlled by the flag, one read-change-check turn, no leftover safety hacks without reason | Works but cluttered | Hard to follow | 10% |
