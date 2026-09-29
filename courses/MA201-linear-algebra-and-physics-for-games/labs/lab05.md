# MA201 · Lab 05: A quaternion toolkit

**Week:** 5, quaternions for rotation ([lecture](../lectures/w05-quaternions-for-rotation.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the problem sets (40%).

## Objective

Write the dozen quaternion functions a gameplay programmer actually uses, check each one against a number from the lecture, and then act as the engineer on call for an animation bug. A turret animation exported from a content tool swings round the wrong way once in its 20-second loop. You will find the frame, explain the cause from the exporter's rule, and fix it two ways.

## Starter materials

All in [`lab05-starter/`](lab05-starter/). Python 3.10 or later, standard library only.

- [`quat.py`](lab05-starter/quat.py). Quaternions are `(w, x, y, z)` tuples. `dot`, `conj`, `yaw_of` and `load_keys` are given. You write:
  - Part A: `from_axis_angle`, `to_axis_angle`, `normalize`, `mul`, `rotate`, `from_euler_yxz` (Godot's default order), `turn_between`.
  - Part B: `slerp` with a `shortest` switch, and `nlerp`.
  - Part C: `long_way_segments` and `max_yaw_step`, which replays keyframes at 60 fps.
- [`turret_keys.csv`](lab05-starter/turret_keys.csv): 41 keyframes, one every 0.5 s, with columns `time, yaw_deg_unwrapped, qw, qx, qy, qz`. The yaw column is what the animator keyed. The quaternion columns are what the exporter wrote.
- [`make_keys.py`](lab05-starter/make_keys.py): the script that produced the file. Read it only in step 6.
- [`test_lab05.py`](lab05-starter/test_lab05.py): eleven tests. Run `python test_lab05.py` inside the folder. On the starter it reports `0/11 tests passed`.
- The week 5 interactive, [`examples/w05-slerp-long-way.html`](../examples/w05-slerp-long-way.html).

## Steps

1. **Predict.** By hand, write the quaternion for 90° about y, and for 60° about x. Compute `turn_between` for yaw 170° and yaw −170°. Keep the numbers to compare with your code.
2. **Part A.** Implement the functions in order. `to_axis_angle` must survive the identity quaternion. Make the first six tests pass. `test_gimbal_lock` checks section 1's table: two different Euler triples, one orientation.
3. **Order experiment.** Using `from_euler_yxz`, build the orientation (yaw 40°, pitch 30°, roll 0°). Then build `mul(pitch, yaw)` (the other order) from the same two single-axis quaternions. Report where each sends the forward vector `(0, 0, −1)`, and the `turn_between` the two results. One sentence: what would a player see if an engine used the wrong order?
4. **Part B.** Implement `slerp` and `nlerp`. Reproduce the lecture's turret table (naive and checked, at `t` = 0, 0.25, 0.5, 0.75, 1). Then, for a 120° turn, tabulate the yaw from slerp and nlerp at `t` = 0.1 to 0.9 in steps of 0.1 and report the largest difference.
5. **Part C, find the bug.** Implement `long_way_segments` and `max_yaw_step`. Run them on `turret_keys.csv`. Report which segment spins, at what time, its naive yaw sweep in degrees, and `max_yaw_step` with and without the sign check. A checked replay should never move more than 2° per frame on this file.
6. **Explain the cause.** Open `make_keys.py`. The exporter makes `w ≥ 0` on every key. Explain in three or four sentences why that rule produces a negative dot product exactly when the keyed yaw crosses 180° (or 540°, or −180°). Use the half-angle fact: which yaw values have `cos(yaw/2) < 0`?
7. **Fix it twice.** Fix A, in the player: use the checked slerp. Fix B, in the exporter: before writing each key, flip its sign if its dot product with the previous written key is negative. Implement Fix B as a function `make_continuous(keys)`, run `long_way_segments` on the result, and show it is empty. One paragraph: which fix belongs where, and why a glTF-compliant importer makes Fix A automatic but Fix B still worth doing.

## Deliverable

Your `quat.py` with `python test_lab05.py` reporting `11/11 tests passed` and `make_continuous` added, plus a bug report of at most one page for the animation team:

- Step 1 predictions next to your code's values.
- The step 3 result and sentence.
- The step 4 slerp and nlerp table and the largest difference.
- The step 5 findings (segment, time, sweep, both `max_yaw_step` values).
- The step 6 explanation and the step 7 paragraph.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 11/11 | 8-10 | 7 or fewer | 30% |
| Order and interpolation (steps 3 and 4) | Correct vectors, correct turn, tables complete, largest nlerp difference reported with the `t` it occurs at | Numbers mostly right, explanation thin | Missing | 20% |
| Bug found (step 5) | Correct segment, time and sweep, both frame-step numbers | Segment found, numbers incomplete | Not found | 20% |
| Cause explained (step 6) | Names the half angle, identifies the yaws where `w` changes sign, and connects the forced flip to the double cover | Right idea, no link to the half angle | Wrong or missing | 15% |
| Fixes (step 7) | Both fixes work, `make_continuous` output has no long segments, paragraph places each fix and cites the glTF rule | One fix works | Missing | 15% |
