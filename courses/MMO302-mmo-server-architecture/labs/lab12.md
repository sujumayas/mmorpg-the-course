# MMO302 · Lab 12: A time-dilation governor

**Week:** 12 ([lecture](../lectures/w12-single-shard-architectures-and-time-dilation.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** labs (40% of the course grade).

## Objective

Implement the lecture's load model for one overloaded node, replay a large battle through it with and without time dilation, and design a controller and floor policy you can defend with measured game time, backlog and command delay.

## Starter materials

All in [`lab12-starter/`](lab12-starter/). Python 3, standard library only.

- [`tidi.py`](lab12-starter/tidi.py) holds the lecture's constants (`A = 0.3` ms, `B = 1` µs, `C = 1`, floor 10%), a loader for the battle timeline, and three functions to write: `work`, `dilation` and `simulate`. The docstring of `simulate` gives the exact per-second update rules. Running the file prints "not run yet" until they work.
- [`battle.csv`](lab12-starter/battle.csv) is an invented 66-minute battle on one node. Pilots rise from 200 to a peak of 3,300 (minutes 35 to 44) and fall back to 300.
- [`test_tidi.py`](lab12-starter/test_tidi.py) has four `unittest` tests built from the lecture's tables. All fail on the starter. Run `python -m unittest test_tidi.py` inside the folder.

## Steps

### Part A: the model (30 min)

1. Implement `work` and `dilation`. The first test checks them against the lecture's table (1,000 pilots at 76.9%, 3,000 pilots at `W = 9.90`).
2. Implement `simulate` exactly as its docstring says. Run all four tests.
3. Run `python tidi.py`. Record, for both modes, the game-seconds that passed, the worst backlog, the worst command delay and the backlog at the end. With a correct model, dilation cuts the worst delay from about 17,665 s to about 123 s, and the battle covers about 1,685 game-seconds instead of 3,960.

### Part B: where the time went (30 min)

4. Change `simulate` to also return a per-second list of `(pilots, f, backlog, delay)`. Plot `f` and pilots against real time on one chart (two y axes), and delay for both modes on a second chart with a log scale.
5. Mark the seconds where the floor binds. Explain from the model why the backlog in dilation mode grows only in those seconds.
6. Compute how many game-minutes pass during the battle's 10 peak real minutes (35 to 44). State it as "players experienced N game-minutes of fighting in 10 real minutes."

### Part C: your governor (50 min)

7. Add a third mode, `"smooth"`, with the lecture's controller: `f ← f + α × (clamp(aim × C / work(n), FLOOR, 1) − f)`. Add `alpha` and `aim` arguments.
8. Sweep `α` in {1.0, 0.5, 0.2, 0.1} and `aim` in {1.0, 0.9, 0.8} on the battle timeline. Tabulate worst delay, end backlog and game-seconds covered.
9. Choose one pair and one floor (you may change `FLOOR`). Justify the choice in up to 200 words using three numbers from your table. Say what players lose with your choice, in their terms ("the fight took X% longer", "commands waited up to Y s").
10. **Past the floor.** Double the peak rows of `battle.csv` to 6,600 pilots. Rerun your governor. Write one paragraph proposing what the operator should do at that size, using a row of the lecture's section 5 table, and give one number from your run that supports it.

## Deliverable

- Your finished `tidi.py` passing all tests, with the Part B and Part C additions.
- A report of up to 3 pages (PDF): the Part A numbers, both Part B charts with the floor seconds marked, the Part C sweep table and justification, and the Part C step 10 paragraph.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Model and tests (Part A) | All four tests pass; both modes' numbers match the lab's reference within rounding | Tests pass, numbers not reported | Tests fail | 25 |
| Time accounting (Part B) | Both charts clear, floor seconds marked, backlog growth explained from `f × W − C`, peak game-minutes computed | Charts present, explanation vague | Missing | 25 |
| Governor design (Part C) | Full sweep, a defended choice using three numbers, player-facing cost stated | Sweep present, choice not argued with numbers | Missing | 30 |
| Past the floor | Proposal names a section 5 approach, supported by a number from the run | Proposal plausible, no supporting number | Missing | 10 |
| Code quality | Readable, parameters in one place, runs first time | Runs with minor fixes | Does not run | 10 |
| **Total** | | | | **100** |
