# AU101 · Lab 07: Attenuation curves, audible radius and panning

**Week:** 7 ([Spatial audio and attenuation](../lectures/w07-spatial-audio-and-attenuation.md))
**Time:** one 2-hour lab session plus about 1.5 hours at home
**Work:** individually for Parts A and C, in pairs for Part B

## Objective

Turn the lecture's attenuation and panning formulas into working code, use it to find where each curve becomes inaudible, and then use it as a design tool. By the end you will have a tested Python module and an attenuation table for a real sound list, with a reason behind every range.

## Starter materials

- Python 3.10 or later, standard library only. In this repository use `.venv/bin/python`.
- [`lab07-starter/spatial.py`](lab07-starter/spatial.py), which contains:
  - `to_db`, `inverse_gain` and `gain_for`: complete. Read them first; they show the style the tests expect.
  - `linear_gain`, `tapered_gain`, `audible_radius` and `pan_gains`: you write them. Each docstring gives the exact definition.
  - `SOUNDS`: a list of `(name, curve, ref, max_d)` rows that you replace in Part B.
  - `main()`: prints the curve table and, for each row of `SOUNDS`, the distances where it falls to −20 dB and −40 dB.
- [`lab07-starter/test_spatial.py`](lab07-starter/test_spatial.py): 13 unit tests. Do not edit it. On the starter, 11 of them fail.
- Run `python spatial.py` from the `lab07-starter` folder to print the report, and `python -m unittest test_spatial -v` to run the tests.

## Steps

### Part A: the curves (45 minutes)

1. Run the tests and note which fail. Read `inverse_gain` and check it against the Web Audio formula in lecture section 2.
2. By hand, compute the inverse gain and level at 2, 8 and 16 m with `ref = 1`. Compare with the lecture's table.
3. Implement `linear_gain`. Remember the clamp at both ends and that the result must never go below 0. The rolloff factor multiplies the fraction, as in the Web Audio model.
4. Implement `tapered_gain` as the smaller of the inverse gain and the squared linear gain. Run `python spatial.py` and find, from the table, the distance range where the tapered curve stops following the inverse curve. Then solve `1/d = ((32 − d)/31)²` numerically (a few lines in the Python shell are enough) to find the switch point to 0.1 m.
5. Implement `audible_radius` by bisection. The function you receive takes a distance and returns a gain. Return `math.inf` if the gain at `far` is still above the threshold. Explain in one sentence why bisection works here and would not work for a curve that rises again.

### Part B: an attenuation table (40 minutes, pairs)

6. You are the audio designers for a co-op arena game. The arena is 60 m across; the camera shows about 30 m. Replace `SOUNDS` with rows for these twelve sounds: player footsteps, enemy footsteps, enemy melee wind-up, enemy ranged charge-up, player gunshot, enemy gunshot, explosion, teammate revive call, health pickup hum (loop), capture point alarm (loop), crowd ambience (loop), wind (loop).
7. For each sound choose a curve, `ref` and `max_d`. Run `python spatial.py` and record the −20 dB and −40 dB radii.
8. Write one sentence per sound that ties its range to gameplay. At least three sentences must refer to a distance in the arena ("the wind-up must be readable at 12 m because the lunge reaches 10 m").
9. Identify two sounds that must use a curve with a guaranteed silence distance and one that should use the inverse curve with a cull distance instead. Say why.

### Part C: panning (25 minutes)

10. Implement `pan_gains`. The listener's `right` vector may have any length, so normalize it. A source sitting on the listener must return centred gains, not an error.
11. By hand, compute `p` and both gains for a listener at (0, 0) facing +y and a source at (−4, 3). Check your code against it.
12. The test `test_front_back_same` passes on purpose. Write two sentences on what it shows about stereo panning, and name one cue from lecture sections 3 or 4 that a game can add to separate front from back.

### Part D: at home

13. Change one sound in your table from a linear to a tapered curve, keeping `max_d`. Report how its −20 dB radius changes and whether the change helps or hurts the gameplay sentence you wrote for it.

## Deliverable

A zip containing your `spatial.py` (all 13 tests passing), a one-page PDF with the hand calculations from steps 2 and 11, the switch point from step 4 and the explanation from step 5, and the twelve-row attenuation table from Part B with its −20 dB and −40 dB radii and one gameplay sentence per row. Add the answers to steps 9, 12 and 13.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Code and tests (30%) | All 13 tests pass; functions clean and match the docstrings; bisection handles `inf` | All tests pass, some code duplicated or unclear | Some tests fail | Most tests fail |
| Hand calculations (15%) | Steps 2 and 11 correct and match the code; switch point found to 0.1 m | Minor arithmetic slip | Only one of the two calculations | Missing |
| Attenuation table (35%) | Twelve rows, radii from the code, each range tied to an arena distance or gameplay rule; step 9 choices justified | Table complete, some sentences generic | Fewer than ten rows or radii guessed | Missing |
| Reflection (20%) | Step 5, 12 and 13 answers use the model (numbers, not impressions) | Answers correct but thin | One answer missing or wrong | Missing |
