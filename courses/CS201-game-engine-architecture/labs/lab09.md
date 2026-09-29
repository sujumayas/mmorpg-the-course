# CS201 · Lab 09: An event-built input layer

**Week:** 9 ([lecture](../lectures/w09-input-and-event-systems.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs (one keyboard, swap every 20 minutes).
**Counts toward:** subsystem labs (50% of the course grade). Your final engine's input stage (week 4's stage 1) is a C++ port of this layer, and week 10's scripts receive actions from its action maps.

## Objective

Build the input layer from lecture sections 3 and 4: a per-frame summary derived from events, an action map with safe rebinding, and a context stack with press ownership, pop cleanup and focus-loss release. Replay a recorded 30-second session at several frame rates and show, with counts, that your layer reports every press at every rate while a sampling layer does not.

## Starter materials

All in [`lab09-starter/`](lab09-starter/). Python 3.10 or later, standard library only. Times are integer microseconds, so every comparison is exact.

- `input_layer.py`: the `Event` dataclass, `load_session`, a provided `sampled_presses` (the sampling design, for comparison), the `Context` class, and nine stubs marked `TODO A1` to `TODO C3` in `InputFrame`, `event_presses`, `ActionMap` and `Router`. Each docstring states exactly what the checker expects.
- `check_lab09.py`: ten checks. Run `python check_lab09.py` inside the folder. Every check prints `TODO` on the starter, then `PASS` or `FAIL` with a reason. The script exits with 0 only when all ten pass.
- `session.csv`: 30 seconds of recorded input, 3,976 events: key downs and ups for `w` (walking), `j` (jump), `k` (attack, mashed) and `e` (interact), and mouse motion at 125 Hz. Columns `time_us,kind,data`.

## Steps

### Part A: frames from events (45 min)

1. Implement `InputFrame.begin_frame` and `InputFrame.apply`, including `focus_lost`. Checks A1 to A4 must pass. A1 is the lecture's C++ example translated to Python.
2. Implement `event_presses`. Check A5 runs it on the session at 10, 30, 60 and 144 fps and requires the true count every time.
3. Write a short script `compare.py` that prints, for 10, 20, 30, 60, 144 and 240 fps, the presses per key reported by `sampled_presses` and by `event_presses`, and the percentage lost by sampling. Paste the table into your README.
4. The attack key `k` is mashed with taps of 4 to 40 ms. Use the lecture's `P(miss) = max(0, 1 − d/T)`, averaged over that range of `d`, to predict the fraction of `k` taps lost at 30 fps. Compare with your table. Show the calculation.
5. The walk key `w` is held for long stretches, yet sampling loses many of its presses at 30 fps. Open `session.csv`, find two consecutive `w` presses, and explain in two sentences what kind of gap the model's `d` must stand for here.

### Part B: action maps (25 min)

6. Implement `ActionMap.action_for` and `ActionMap.rebind`. Checks B1 and B2 must pass.
7. B2's rule is "the new binding wins and the old owner loses the key". Write two sentences in your README on what the options screen must show the player when `rebind` returns a non-`None` loser, and why silently leaving an action unbound is a bug report waiting to happen.

### Part C: routing (40 min)

8. Implement `Router.route`, `Router.pop` and `Router.focus_lost`. Checks C1 to C3 must pass.
9. Write a scenario test of your own, `test_camera.py`, for the lecture's in-class trace: gameplay binds `rmb` to `camera_drag` and `enter` to `open_chat`. The player holds `rmb`, opens chat with Enter, releases `rmb` while chat is open, and closes chat with Escape (pop). Assert that gameplay ends with nothing held. Then set the router to route ups to the top context instead (copy `route` and change one rule), run the same test, and record what gameplay believes.
10. In at most 150 words: the lecture's check-yourself question 4 asks about Shift held across a chat close. Decide whether your engine should re-send held keys to a context when it becomes the top again, and give one game situation where each choice is wrong.

### Part D (optional, +5 bonus): timestamps

11. Add `press_times(key)` to `InputFrame` that returns the true `time_us` of each press in the frame. Using the session, compute the mean difference between true press time and the frame time at which the press is processed, at 30 and 144 fps. Compare with the lecture's `T/2`.

## Deliverable

A zip of your `lab09-starter/` folder containing:

- `input_layer.py` with all ten checks passing, `compare.py` and `test_camera.py`.
- `README.md` (at most two pages): how to run everything, the step 3 table, the calculations and answers for steps 4, 5 and 7, the step 9 comparison, the step 10 paragraph, and Part D if attempted.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Frame summary and replay (A1-A5, step 3) | All pass; table covers six frame rates with loss percentages | Checks pass, table partial | Checks fail | 25 |
| Model against data (steps 4-5) | Averaged prediction computed and compared; re-press gap identified as the relevant `d` | Prediction made without averaging, or step 5 vague | Missing | 20 |
| Action maps (B1, B2, step 7) | Both pass; UI consequence named concretely | Checks pass, step 7 generic | Checks fail | 15 |
| Routing (C1-C3, step 9) | All pass; own scenario test passes and the top-context variant shows the stuck button | Checks pass, step 9 missing the variant | Checks fail | 25 |
| Design paragraph (step 10) | Makes a choice and gives a situation where each option fails | Choice without counterexamples | Missing | 15 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

True press counts in the session: `e` 33, `j` 22, `k` 28, `w` 30 (113 total). `sampled_presses` reports `k` 17, `w` 16, `e` 25, `j` 17 at 30 fps (75, 34% lost); 23, 18, 29, 20 at 60 fps (90, 20% lost); 27, 24, 33, 22 at 144 fps (106, 6% lost).

Step 4: for `d` uniform on 4 to 40 ms and `T = 33.3 ms`, the miss probability is `1 − d/T` for `d < 33.3` and 0 above. The average is `(1/36) × ∫ from 4 to 33.3 of (1 − d/33.3) dd ≈ 0.36`. Measured: 11 of 28 lost, 0.39. Close enough; accept any careful estimate.

Step 5: many consecutive `w` presses are separated by a release gap of only 5 ms. Sampling merges two presses when the key is up only between two samples, so the relevant `d` is the length of the *up* interval, not the down interval. Students who see this have understood that the model is about any state that lasts less than `T`.

Step 9 with top-context routing: chat receives the `rmb` up and eats it, gameplay still holds `camera_drag`, and the camera keeps turning after chat closes.

</details>
