# MMO407 · Lab 08: Battle escalation model

**Week:** 8 ([lecture](../lectures/w08-eve-large-scale-events.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** the launch plan (50% of the course grade). Your event plan becomes the "player-scheduled peaks" section of your final launch plan.

## Objective

Implement the lecture's escalation loop (reinforcements on the real clock, fight progress on the game clock), reproduce its numbers, measure which levers shorten a dilated fight, fit the model to a published battle timeline, and write an event plan for a player-scheduled siege.

## Starter materials

- [`lab08-starter/battle_loop.py`](lab08-starter/battle_loop.py), Python 3, standard library only. It provides MMO302's `work` and `speed` with the invented constants, and three stubs:
  - `battle` (TODO 1), the minute-by-minute loop. It returns a dictionary with the real length, final headcount, pilot-hours, game-minutes done, minutes at the floor and whether the fight was decided.
  - `fit_rate` (TODO 2), a least-squares arrival rate from `(minute, pilots)` observations.
  - `objective_for_length` (TODO 3), the smallest objective `G` that makes a fight last a target length.
- [`lab08-starter/test_battle_loop.py`](lab08-starter/test_battle_loop.py) has six tests. All fail on the starter and pass on a correct solution. Run them from inside `lab08-starter/` with `python -m unittest test_battle_loop.py`.
- `python battle_loop.py` prints four of the lecture's lines once TODO 1 is done.
- The interactive `examples/w08-battle-escalation.html`, once it is built.

## Steps

### Part A: the loop (35 min)

1. Implement `battle` (TODO 1) and run the tests. `test_defaults` must give 419 minutes, 6,000 pilots, 31,442 pilot-hours and 318 minutes at the floor.
2. Record `n(t)` and `game(t)` every minute for the lecture battle and for the undilated fight, and plot them on two stacked charts with a shared time axis. Mark the minute the speed first reaches the floor.
3. Check the lecture's two-phase estimate. Compute by hand the minute the floor is reached and the game-minutes done by then, estimate the total, and compare with the model. Explain any gap in one sentence.

### Part B: which levers matter (40 min)

4. Sweep `r` from 0 to 40 in steps of 2 and `G` from 10 to 120 in steps of 10. Show the real length as a heat map or table. Mark the cells where the fight lasts longer than 12 hours.
5. For the lecture battle, compute the length after each of these changes, one at a time: `r` halved, `G` halved, `C` doubled, pool halved, floor raised to 0.2. Rank them. For the top two, explain in two sentences each why they beat their proportional effect.
6. Define the loop's **stretch** as the dilated length divided by the undilated length. Plot the stretch against `r` for `G = 30, 60, 90`. Describe the shape, and name the value of `r` above which the stretch grows fastest for `G = 60`.

### Part C: fit a real timeline (30 min)

7. Implement `fit_rate` and `objective_for_length` (TODOs 2 and 3) and run all tests.
8. CCP's FWST-8 report gives more than 4,000 pilots at 16:52 and more than 6,000 at 17:36, with a peak of 6,557 at 18:16. Take 16:34 as minute 0. Fit `r` from the first two points. Then run `battle` with `n0 = 4,000`, your fitted `r`, `pool = 6,557` and `G = 60`, using the lecture's constants. Report `T`.
9. The real structure took 11 hours 44 minutes (704 minutes) of shooting. Use `objective_for_length` to find the `G` that reproduces 704 minutes with the same inputs. Write a short paragraph on what this fit can and cannot tell you. The constants are invented, the arrivals slowed after 17:36, and a structure's hit points are not a game-time objective in the simple sense. Which of your conclusions from Part B survive those caveats?

### Part D: the event plan (15 min)

10. Your MMO has monthly castle sieges on one server with this lecture's dilation model. Expect 1,500 players at the start, 25 per minute arriving, and a pool of 5,000. Choose `G`, one travel-friction rule (a value of `r`) and one real-time brake so that 90% of sieges end within three hours. Model at least three scenarios (a quiet siege, the expected one, and a war-deciding one with twice the arrivals and pool) and report each one's length, peak and whether it was decided.

## Deliverable

- `battle_loop.py` passing all six tests, plus your code for steps 2 to 10.
- The plots from steps 2, 4 and 6.
- A one-page event plan for step 10: the objective size, the travel rule, the brake and who it favours, the three scenario results, what the operator watches during the siege, and the one number you would ask players for in advance.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Loop (steps 1 to 3) | Tests pass; plots show the two curves pulling apart; two-phase check done and gap explained | Tests pass; check or explanation missing | Tests fail | 25 |
| Levers (steps 4 to 6) | Full sweep; levers ranked with numbers; nonlinearity explained; stretch plot described | Sweep and ranking without explanation | Missing | 25 |
| Fit (steps 7 to 9) | Tests pass; `r` and `G` fitted; caveats stated and tied to Part B conclusions | Fit done, caveats generic | Missing | 20 |
| Event plan (step 10) | Three scenarios modelled; brake and its winner named; operator watch-list concrete | Plan given for one scenario | Missing | 25 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
