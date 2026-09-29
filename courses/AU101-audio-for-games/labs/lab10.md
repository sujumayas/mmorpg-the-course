# AU101 · Lab 10: Build the mix brain

**Week:** 10 ([lecture](../lectures/w10-mixing-ducking-and-priority.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** individual.
**Counts toward:** the final sound pass (40%). The allocator is reused in lab 12.

## Objective

Implement the four mixing rules from the week 10 lecture as small functions (power sum, HDR window, sidechain duck, priority allocation), prove them against the lecture's numbers, and then use them to make and defend one mix decision: the release rate for a scene you design.

## Starter materials

All in [`lab10-starter/`](lab10-starter/). Python 3, standard library only.

- [`mixer.py`](lab10-starter/mixer.py): function stubs with the exact rules in their docstrings (`db_sum`, `hdr_target`, `hdr_step`, `hdr_output`, `duck_step`, `effective_priority`, `allocate`, `run_scene`) and the lecture's scene as `SCENE`. Running it prints "Not written yet" until `run_scene` works, then prints the scene timeline every 0.25 s.
- [`test_mixer.py`](lab10-starter/test_mixer.py): six tests built from the lecture. They check the power-sum table (−17.0, −10.0, −4.0 dBFS), the instant attack and limited release, the edge of the window (a sound exactly `W` below the top is audible), the scene timeline (birds back at 1.1 s, wind at 1.75 s at the latest), the duck ramp (−8 dB after 0.1 s, −4 dB after 0.5 s of release) and the allocator (tie broken by oldest or newest). All six fail on the starter.
- The [HDR window interactive](../examples/w10-hdr-window.html) for spot checks.

Run the tests with `python3 test_mixer.py` from inside the folder. It prints PASS or FAIL per test and exits with status 1 while anything fails.

## Steps

### Part A: the functions (50 min)

1. Implement `db_sum`, then `hdr_target`, `hdr_step` and `hdr_output`. Run the tests after each one.
2. Implement `duck_step`. The gain is in dB, 0 means no duck, and it must never overshoot `−depth` or 0.
3. Implement `effective_priority` and `allocate`. Sort by effective priority, highest first, and break ties by `start_time` according to `keep`.
4. Implement `run_scene` with integer ticks (`t = i * dt`) so float drift cannot move an event by one tick. Run `python3 mixer.py` and compare the printout with the lecture's table.

### Part B: your own scene (40 min)

5. Design a 10-second scene for a game of your choice with at least six sounds, two of which are loud and short (a blast, a spell impact, a door slam). Write it as an `events` list. Give each sound an in-game level chosen by **importance**, and justify any level that differs from how physically loud the sound would be.
6. Run it at release rates of 10, 20, 40 and 80 dB per second. For each, record the deaf time of your two quietest sounds after each loud event, and whether any sound drops out and returns more than twice in one second (pumping).
7. Pick a release rate. Add one sentence on how it serves the feel you want.

### Part C: ducks and priority (30 min)

8. Add a dialogue line from 2.0 to 4.5 s and a second from 4.8 to 7.0 s. Duck music by 8 dB with a 0.1 s attack. Find the shortest release time for which the music never recovers more than 2 dB in the gap between lines.
9. Write a priority table for eight sounds in your scene with base priorities and one distance offset rule. Run `allocate` with a limit of 4 at two moments of your scene and list which sounds survive.

## Deliverable

- Your completed `mixer.py`, with all six tests passing, plus a `my_scene.py` that imports it and prints your Part B and C results.
- A two-page PDF: the scene table with levels and justifications, the Part B release comparison table, your chosen release rate with a reason, the Part C release time with the calculation, and the priority table with the two allocation results. End with a 100-word note on one thing HDR got wrong in your scene and how you fixed it.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Functions (Part A) | All six tests pass; code readable; integer ticks used | Four or five tests pass | Three or fewer pass | 30 |
| Scene design | Six or more sounds with importance-based levels, each deviation justified | Levels given without justification | Missing | 15 |
| Release study | Four rates compared with deaf times and pumping noted; choice tied to feel | Table present, choice not justified | Missing | 20 |
| Duck release | Correct shortest release with the arithmetic shown | Plausible value without working | Missing | 15 |
| Priority table | Eight sounds, offset rule, two allocations explained | Table without allocations | Missing | 10 |
| HDR note | Names a specific failure and a fix from the lecture's options | Generic note | Missing | 10 |
| **Total** | | | | **100** |
