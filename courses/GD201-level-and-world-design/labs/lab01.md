# GD201 · Lab 01: Checkpoint placement and a one-verb lesson

**Week:** 1 · **Time:** 2 hours in the lab plus about 2 hours at home · **Weight:** part of the blockouts component (40% of the course). The paper level you design here is the starting layout for Lab 02's blockout.

**Lecture:** [Week 01, level design as teaching](../lectures/w01-level-design-as-teaching.md). **Interactive:** [w01-retry-cost.html](../examples/w01-retry-cost.html), for checking your numbers.

## Objective

Implement the lecture's retry model and segment model, use them to find the best checkpoint placement for a sample level, then design a five-beat paper level that teaches one verb. Measure the success chance of its challenges with three testers and place its checkpoints using your own code.

## Starter materials

- [`lab01-starter/retry.py`](lab01-starter/retry.py). The sample level (six challenges with `walk`, `t` and `p`) and five functions to fill in: `expected_time`, `penalty_ratio`, `segment_time`, `level_time` and `best_checkpoints`. The docstrings define each one.
- [`lab01-starter/check_lab01.py`](lab01-starter/check_lab01.py). A checker with 10 checks. Do not edit it.
- For the paper level: squared paper (or a printed 1 cm grid), coloured pens, a coin or token for the player, a timer (your phone) and a tally sheet.

Run from inside `lab01-starter` with the course Python:

```
python retry.py
python check_lab01.py
```

The starter runs and reports that the functions are not implemented. The checker prints `0/10 checks pass` until you fill them in.

## Steps

1. **Part A, one challenge (15 min).** Implement `expected_time` and `penalty_ratio`. Check them against the lecture's table (`t = 8`, `p = 0.2`, `r = 52` gives 248.0 s and 6.20).
2. **Part B, segments (20 min).** Implement `segment_time`. Reproduce the lecture's 154.0 s and 66.0 s. Then implement `level_time`, which splits the level at the checkpoints and adds the one-time walk to the first challenge of each segment.
3. **Part C, placement (15 min).** Implement `best_checkpoints` by brute force over every choice of extra checkpoints. Run the checker until it prints `10/10 checks pass`.
4. **Read the result (10 min).** For the sample level, record `level_time` for 1 to 6 checkpoints using `best_checkpoints`. Write two sentences on which challenge the best 3-checkpoint layout isolates and why the model picks it.
5. **Part D, the lesson plan (30 min).** Pick one verb (grapple, dash, wall-jump, push block, or your own). On paper, design five beats that introduce, practise, combine and test it, following the lesson matrix rules in section 3 of the lecture. Draw the level side-on or top-down on the grid. Mark every challenge and give it an estimated attempt time `t`.
6. **Part E, measure `p` (30 min, at home or in the lab).** Run the paper level with three testers who haven't seen it. Move their token by the rules you wrote. Use a coin flip, a die or a quick physical task (flicking a token into a box, for example) as the skill check for each challenge, and let testers practise so their success chance can rise. Don't coach them. For each challenge, tally attempts and clears, and compute `p̂ = clears / attempts`.
7. **Part F, place checkpoints (15 min).** Enter your level into `retry.py` as a new list, using your measured `p̂`. Find the best placement with 2 and with 3 checkpoints. Compare it with where you had put them by instinct.
8. **Stretch (optional).** Add a `stakes` flag to one challenge that forces a checkpoint far before it (a boss). Measure how much time it adds at your testers' `p̂` and at `p = 0.9`, and argue in one paragraph whether the tension is worth it.

## Deliverable

Submit a zip with:
- Your completed `retry.py` (including your level as a second list).
- A photo or scan of the paper level with beats, challenges and checkpoints marked.
- A one-page write-up with: the lesson matrix (verbs by beats, plus the `r` row); the tally table from step 6 with `p̂` for each challenge; the table from step 4; your instinctive and computed checkpoint placements side by side with `level_time` for each; and two to three sentences on what you changed and why.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker | 10/10 checks pass | 6-9 pass | 0-5 pass | 25% |
| Lesson matrix | One new verb per beat, every test preceded by practice, `r` row rises with mastery, rules broken only with a stated reason | Matrix complete but one rule broken without comment | Missing, or beats don't teach the verb | 25% |
| Measured `p̂` | Three testers, attempts and clears tallied per challenge, no coaching noted | Tallies present for most challenges | Values guessed rather than measured | 20% |
| Checkpoint analysis | Instinct vs computed placement compared with times, difference explained with the model | Comparison present, explanation vague | Missing | 20% |
| Code readability | Clear names, no copy-pasted blocks, level data separate from functions | Works but cluttered | Hard to follow | 10% |
