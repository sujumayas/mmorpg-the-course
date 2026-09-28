# MA101 · Lab grading key (labs 13 and 14)

Reference answers for the generated starter data in `labs/starter/`, computed by the course reviewer against reference solutions. Regenerating the data changes these values.

## Lab 13: Guard vision

| Check | Reference value |
|---|---|
| First-seen time, sentry_a | 10.3 s |
| First-seen time, sentry_b | 7.8 s |
| First-seen time, patrol_c | 16.4 s |
| First-seen time, tower_d | 1.8 s |
| 30° cone with graded focus | meter never fills (max 0.63) |
| 45° cone with graded focus | spots at 11.9 s |

## Lab 14: Range queries

| Check | Reference value |
|---|---|
| Mobs in safe / random / despawn zones | 576 / 1,530 / 2,894 |
| Mobs kept by the bounding-box prefilter | 163 |
| Wrong answers from int32 overflow | 1,070, starting at 463.5 blocks |
| Chase state changes, two radii (hysteresis) | 3 |
| Chase state changes, one radius | 9 |
