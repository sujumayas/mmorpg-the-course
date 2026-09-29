# MMO404 · Lab 10: Conflicts and convergence

**Week:** 10 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Turn the [week 10 lecture](../lectures/w10-consistency-models.md) into tools you can use on a real design. You implement the conflict model for guessed cross-server claims and check it against two simulations, one of them tick-aligned. Then you build the two structures that let servers agree without forwarding every write, a replicated damage counter and a vector clock, and test them against messages that arrive late, twice and out of order. You finish with a consistency plan for a world boss fought across a seam.

## Starter materials

Folder [`lab10-starter/`](lab10-starter/README.md). Standard library Python only. Run with `.venv/bin/python` from the repository root or any Python 3.10+.

- `consistency.py`: constants `T = 0.1` and `D = 0.001`, a Poisson claim generator, a fixed-window simulation and a tick-aligned simulation (both given), and TODOs for `conflict_p`, `forward_latency`, `count_conflicts`, the `DamageCounter` methods `hit`, `merge` and `hp`, the `VectorClock` methods `event` and `receive`, and the functions `happened_before` and `concurrent`. It has `--check`, `--compare` and `--sweep` modes.

## Steps

1. **By hand first.** Before writing code, compute `P(conflict)` for `λ = 0.5` per second at 10 Hz with `d = 1 ms`, tick-aligned and flushed, and the forward policy's average and worst added latency. Keep the numbers for your report.
2. **The model.** Implement `conflict_p` and `forward_latency`. Then implement `count_conflicts` with two pointers that walk both sorted lists once. Run `python consistency.py --check`. It stops at the damage counter until step 4.
3. **Is the model honest?** Run `--compare`. Read `simulate_ticked` and write down, in two sentences, how its timing differs from the fixed window in the lecture. Then change `phase_b` in `simulate_ticked` to 0.0 (both servers tick together) and to 0.099, and rerun. Report the tick-aligned column for all three phases. One phase is clearly worse than the formula. Work out the average visibility window for that phase from the three waits (to leave, on the wire, to be applied), put it into `conflict_p`, and show that it explains the result. What does this tell you about starting two servers' ticks at the same moment?
4. **The counter.** Implement `DamageCounter.hit`, `merge` and `hp`. The check sends 500 snapshots from three servers in a shuffled order with 50 duplicates and requires all three to agree. Then break it on purpose: replace `max` in `merge` with `+`, run the check, and record what fails and why. Restore it.
5. **Thresholds.** Write a short script that runs two `DamageCounter`s on a 10,000 health boss, each dealing 400 damage per tick and merging the other's snapshot one tick late. Print the tick at which each server first sees health at or below zero, and the true tick of death. In three sentences, explain what would go wrong if each server ran its own death and loot logic, and how an owner fixes it.
6. **Vector clocks.** Implement `VectorClock.event`, `VectorClock.receive`, `happened_before` and `concurrent` until `--check` prints `all checks passed`. Then replay the zone-chat example from section 4 of the lecture with three vector clocks and show that server C can detect that the reply arrived before the question it depends on.
7. **Your plan.** A world boss with 3,000,000 health spawns on a seam between two 10 Hz servers with a 1 ms link. Fifty players fight it from each side at 600 damage per second each. When it dies, a loot chest appears that about 40 players click in the first two seconds. Write a one-page plan that names a policy (forward, guess, merge or eventual) for damage, death, the loot chest and the combat log. For each, give the number that justifies it: the staleness of the health bar in health points and percent, the conflict share if the chest were guessed, the forward latency and how you hide it.

## Deliverable

Your finished `consistency.py`, `conflicts.csv` from `--sweep` with a chart of its three series against `λ` on a log axis, the threshold script from step 5, and a report (PDF or Markdown, at most three pages) with the hand calculations from step 1, the phase results from step 3, the broken-merge finding from step 4, the explanation from step 5, the replay from step 6 and the plan from step 7. Submit before the week 11 lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model and conflict counting | `--check` passes; `count_conflicts` is a single pass; hand numbers match the code | Passes with a nested loop over all pairs | Fails the check | 20% |
| Model validation | Three phases reported; the in-step case explained with a window of 1.5 T and a sound recommendation about tick phase | Numbers reported, explanation vague | Step skipped | 15% |
| Convergent counter | Passes; the `+` merge failure is explained with duplicated snapshots | Passes, explanation thin | Fails the check | 15% |
| Thresholds | Script prints both servers' death ticks and the truth; double-loot risk and owner fix explained | Script runs, explanation incomplete | Missing | 15% |
| Vector clocks | Passes; chat replay shows detection of the out-of-order reply | Passes, replay missing | Fails the check | 10% |
| Consistency plan | Every policy justified with a computed number and units; forward latency hidden by a named animation or delay | Policies chosen, some numbers missing | Plan missing or copied from the lecture | 20% |
| Writing | Plain, one idea per paragraph, units everywhere | Mostly clear | Hard to follow | 5% |
