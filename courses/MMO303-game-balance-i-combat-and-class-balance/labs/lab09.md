# MMO303 · Lab 09: Patch the triangle

**Week:** 9, intransitivity and counters ([lecture](../lectures/w09-intransitivity-and-counters.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the problem sets (30%).

## Objective

Simulate how a player population responds to balance patches in a counter-based game. Predict week-1 win rates and the long-run stable mix by hand, then check both with a replicator-dynamics simulation, first for three classes and then for five.

## Starter materials

- [`lab09-starter/counter_sim.py`](lab09-starter/counter_sim.py), standard-library Python with `margins_from_winrates`, `expected_margins`, `stable_mix3`, `step` and `run` stubs, and [`test_counter_sim.py`](lab09-starter/test_counter_sim.py) with the Knight-buff checks from step 2. If you prefer a spreadsheet, put the margin matrix on one tab and one row per week on another, and check it against the same values.
- The three-class arena from the lecture: Knight, Mage, Ranger, starting at 60% on every favorable link.
- Three proposed patches:
  - Patch 1: Knight over Ranger becomes 70%.
  - Patch 2: Ranger over Mage becomes 52%.
  - Patch 3: Mage over Knight becomes 66% and Knight over Ranger becomes 66%.
- A five-class extension (Knight, Ranger, Cleric, Mage, Rogue) as a 5 × 5 win-rate matrix in [`lab09-starter/five-class.csv`](lab09-starter/five-class.csv). Each class beats the next two in that order at 60% and loses to the two before it at 40%. The triangle's links are kept: Knight beats Ranger, Ranger beats Mage, Mage beats Knight.
- The [counter triangle interactive](../examples/w09-counter-triangle.html), for checking three-class results.

## Steps

1. **Margins.** Convert win rates to margins `2w − 1` and fill the antisymmetric margin matrix.
2. **Check against the lecture.** With the Knight buff (70/60/60), your stable-mix formula must give 25 / 50 / 25, week-1 win rates of 53.3%, 50.0% and 46.7%, and one simulation step with `η = 1` from one third each must give 35.6%, 33.3%, 31.1%.
3. **Predict by hand.** For each patch, write down the stable mix and the week-1 win rates before running anything.
4. **Simulate.** Run 30 weeks for each patch from the old stable mix with `η = 1`. Plot shares over time. Report the range each class's share covers during the run.
5. **Friction.** Add loyalty: each week only 30% of players are willing to switch (`η = 0.3`), and 5% of the population re-rolls at random. Rerun Patch 1. Does the population settle, and where?
6. **Five classes.** Solve the stable mix of the five-class matrix (by the indifference equations or by long simulation with friction). Then buff one link to 70% and report which class gains the most share. Explain it with the counter graph.
7. **Advise.** The community asks for "more Knights" in the three-class game. Propose the smallest single-link change that raises the Knight's stable share to 40%, and give the week-1 win rates players will see.

## Deliverable

The sheet or script with passing tests, the plots, and a memo of at most 400 words to the live team. It must compare your hand predictions with the simulation for all three patches, describe the friction result, and give your "more Knights" patch with its week-1 win rates and a warning about how the dashboard will look in week 1.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | Reproduces all lecture test values; margin matrix antisymmetric | One test value off | Test values not reproduced | 20% |
| Predictions vs simulation | Hand predictions written first and all match or differences explained | Predictions partly match, unexplained gaps | Predictions missing or written after the fact | 25% |
| Friction and five-class analysis | Both done, results explained with the counter graph | Done with thin explanation | Missing | 25% |
| "More Knights" patch | Smallest single change found, 40% verified, week-1 rates given | Change works but is not minimal | Wrong link changed | 20% |
| Memo writing | Plain, numeric, within the word limit | Some vague claims | Hard to act on | 10% |
