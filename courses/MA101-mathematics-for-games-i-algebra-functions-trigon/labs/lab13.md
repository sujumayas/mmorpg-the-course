# MA101 · Lab 13: Guard vision

Assigned in week 13 ([lecture](../lectures/w13-dot-product-facing-and-vision-cones.md)). Due at the start of week 14. Counts toward the problem-set grade.

## Objective

Implement a guard's vision with the dot product, with no angle functions in the runtime test. You will build the cone test, the left/right turn test and a graded detection meter, run them against a recorded player path, and find a planted bug from its symptoms alone.

By the end you will have a small, tested vision module you can reuse in CS203's perception week.

## Starter materials

- [`starter/lab13_starter.py`](starter/lab13_starter.py). Python 3, no libraries beyond the standard `math` and `csv` modules. It imports your `Vec2` from `lab12_starter.py` (keep both in one folder) and falls back to a reference `Vec2` if yours is unfinished. It has CSV loaders, a self-check against the lecture's nine positions, and four empty functions:
  - `dot(a, b)` returns the dot product.
  - `in_cone(guard_pos, guard_fwd, half_angle_deg, sight_range, player_pos)` returns `True` or `False`.
  - `side(guard_fwd, guard_pos, player_pos)` returns `"left"`, `"right"` or `"ahead/behind"`.
  - `focus(guard_pos, guard_fwd, half_angle_deg, player_pos)` returns a number from 0 to 1.
- [`starter/guards.csv`](starter/guards.csv): four guards with columns `name, x, y, facing_deg, half_angle_deg, range`. Guard `sentry_a` is at (0, 0), facing 0°, half-angle 30°, range 20, which matches the lecture's table.
- [`starter/path.csv`](starter/path.csv): a recorded player path of 200 samples, columns `t, x, y`, taken 0.1 s apart.
- [`starter/buggy_guard.py`](starter/buggy_guard.py): a teammate's guard implementation that players report as "sees me from the side when I'm far away." Do not read it until step 5.
- Spreadsheet route: import `guards.csv` and `path.csv` into any spreadsheet. The dot product of vectors in columns A:B and C:D is `=A2*C2+B2*D2`.
- The week 13 interactive, [`examples/w13-vision-cone.html`](../examples/w13-vision-cone.html), to check individual positions.

## Steps

1. **Dot product and cone test.** Implement `dot` and `in_cone`. Compute the threshold `c = cos(radians(half_angle_deg))` once per call, then test `dot(f̂, d̂) ≥ c` and `|d| ≤ range`. Do not call `acos` or `atan2` inside `in_cone`. Run it for `sentry_a` against the nine positions in the lecture's table and confirm all nine answers match.
2. **Squared form.** Write `in_cone_fast`, which uses `f̂ · d ≥ 0` and `(f̂ · d)² ≥ c² × (d · d)` with no square root or division. Loop over every integer point in a 60 × 60 square around `sentry_a` and confirm `in_cone` and `in_cone_fast` agree on every one. Report the number of points seen.
3. **Left or right.** Implement `side` with the perpendicular dot product `l̂ · d`, where `l̂ = (−f.y, f.x)`. For each guard, report the side of the player at `t = 5.0 s` in `path.csv`.
4. **Replay the path.** For each guard, run `in_cone` over the whole path. Report the first time each guard sees the player, or "never." Plot (or chart in the spreadsheet) the dot product `f̂ · d̂` over time for `sentry_a`, with a horizontal line at `c`.
5. **Find the bug.** Run `buggy_guard.py` on the same path and grid as step 2. Compare its seen/not-seen map with yours. Describe the shape of the region it reports as seen. Then open the file, find the bug and fix it in one line. Explain in two sentences why the symptom only appears when the player is far away.
6. **Graded detection.** Implement `focus` as `clamp((f̂ · d̂ − c) / (1 − c), 0, 1)`. Add a detection meter that rises by `focus × 0.8` per second while the player is in range and in the cone and drains by 0.3 per second otherwise. Replay the path for `sentry_a` and report the time the meter first reaches 1.0, or its maximum if it never does.
7. **Tune.** Choose a new half-angle for `sentry_a` so that the player on this path is spotted between 8 and 12 seconds. Report the half-angle, `c`, and the spotted time.

## Deliverable

Submit your completed `lab13_starter.py` (or spreadsheet) and a PDF memo of at most 350 words, addressed to a level designer. The memo must contain:

- The step 2 count and a one-line statement that the fast and slow tests agree.
- The step 4 table of first-seen times for all four guards and the dot-product plot.
- Your bug description and the one-line fix from step 5.
- Your tuned half-angle from step 7, and one sentence on how a player would read that guard's cone in game.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Cone test correctness | Matches all nine lecture positions; no angle functions at runtime; fast form agrees on every grid point | Minor errors, or uses `acos` at runtime | Wrong answers or does not run | 25% |
| Side and path replay | Correct sides and first-seen times for all guards, clear plot with threshold line | One guard wrong or plot unclear | Missing or mostly wrong | 20% |
| Bug diagnosis | Correct region shape (half-plane), correct fix, explanation names the missing normalization and the role of distance | Fix correct but explanation weak | Bug not found | 20% |
| Graded detection and tuning | Meter implemented as specified, tuned angle hits the target window, numbers reported | Meter works but tuning misses the window | Missing | 25% |
| Memo clarity | Under 350 words, numbers first, a designer could act on it | Understandable but padded or missing a number | Hard to follow | 10% |
