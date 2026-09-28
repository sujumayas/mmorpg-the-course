# CS102 · Lab 10: Build and instrument an event bus

**Week:** 10 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** one of the weekly labs (labs are 40% of the course in total)

## Objective

Turn a polling quest and achievement tracker into an event-driven one, fix the three bugs that event buses ship with, and measure the cost of both designs on the same 10-minute session. This lab applies the event bus, the cost model `F × N` against `E × L`, and the two classic bugs from [week 10](../lectures/w10-observer-and-events.md).

## Starter materials

- `lab10-starter.py`: Python 3.10+, standard library only. Run it from this folder with `python lab10-starter.py` for a report and `python lab10-starter.py --test` for the self-checks. It contains:
  - `make_session(seed)`, a scripted 10-minute session at 60 fps (36,000 frames). Each frame is a list of `(event_name, payload)` tuples: kills, loot, level-ups, enemy spawns and despawns, and a `player_moved` every frame. Same seed, same session.
  - `PollingTracker`, the "before" design. 150 objectives, each checked every frame.
  - `EventBus`, `Objective` and `Enemy`, the "after" design, with three planted bugs marked `TODO bug 1`, `TODO bug 2` and `TODO bug 3`.
  - Four self-checks. Two fail on the untouched starter.
- No real game's data is used. Enemy kinds and objectives are invented.

## Steps

1. **Baseline.** Run the report and the tests. Record the number of kills, the objectives completed by each design, the polling checks, the event callback calls and the `player_moved` listener count. Explain in two sentences why the listener count is so much larger than the number of enemies alive.
2. **Bug 1, no way to leave.** Make `subscribe` return an unsubscribe function. Rerun. The report now shows a mismatch between the two designs. Which objectives differ, and why did fixing bug 1 *expose* a different bug?
3. **Bug 2, modify while iterating.** Fix `emit` so a listener that unsubscribes during the loop cannot make the next listener miss the event. Rerun until the first three tests pass. In your write-up, trace by hand what happened to one missed objective, naming the list indices before and after the removal.
4. **Bug 3, the lapsed listener.** Make `Enemy` keep its unsubscribe handle and call it in `destroy()`. Rerun until all four tests pass. Record `player_moved` calls in the last minute before and after the fix, and compute the ratio.
5. **Split the cost.** Instrument the bus to count calls per event name. Report objective calls (`enemy_killed`, `item_looted`, `level_up`) separately from `player_moved`. Compare objective calls with the polling checks. Then compute `E × L` for `enemy_killed` from your numbers and check it against the measured calls.
6. **Keyed subscriptions.** Most `enemy_killed` listeners ignore most kills, because every kill objective filters by kind itself. Add an optional key to the bus, `subscribe("enemy_killed", cb, key="wolf")`, and an `emit` that calls only listeners with a matching key (or no key). Measure objective calls again.
7. **Typed events.** Replace the string names and keyword payloads with frozen dataclasses (`EnemyKilled(kind, killer)`, `ItemLooted(item)`, `LevelUp(level)`, `PlayerMoved(x, y)`), keyed by class. Keep all four tests passing.
8. **Event table.** Write a table with one row per event: name, payload fields, emitter, every listener, and whether each listener could safely be queued (S or Q, as in the in-class activity).

## Deliverable

Your modified `lab10.py` (copied from the starter), passing `--test`, and a short report (500 to 700 words) with: the numbers from steps 1, 4, 5 and 6 in one table, the hand trace from step 3, the event table from step 8, and one paragraph recommending when this game should poll and when it should use events, citing your measured numbers.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Bug fixes | All three fixed, all tests pass, each fix explained with its symptom | Tests pass, explanations thin | Tests fail | 25% |
| Hand trace of the missed event | Indices before and after removal, names the listener that was skipped | Trace correct but incomplete | Missing or wrong | 15% |
| Measurement | Per-event counts, lapsed-listener ratio, `E × L` checked against measurement | Counts given without the check | Numbers missing | 25% |
| Keyed subscriptions and typed events | Both work, call reduction measured | One works | Neither | 20% |
| Event table and recommendation | Complete table, S/Q justified, recommendation cites numbers | Table incomplete or recommendation without numbers | Missing | 15% |

<details>
<summary>Instructor check values (seed 2026)</summary>

- Session: 36,000 frames, 255 kills, 159 loot pickups, 6 level-ups, 1,176 spawns, 1,186 despawn events (some arrive when no enemy is alive). Polling: 52 objectives complete, 5,400,000 checks.
- Untouched starter: events 52 complete, 21,690,781 calls, 6 enemies alive, 1,176 `player_moved` listeners, 4,057,522 `player_moved` calls in the last minute. Tests 1 and 4 fail.
- After bug 1 only: 50 complete, mismatch on `kill_boar_65` and `kill_spider_55`. Tests 2, 3 and 4 fail.
- After bugs 1 and 2: 52 complete, 21,684,609 calls. Test 4 fails.
- After all three: 782,172 calls in total, 6 listeners, 34,204 `player_moved` calls in the last minute (ratio about 119 to 1). Objective calls alone: 31,733.
- Keyed subscriptions: objective calls fall from 31,733 to about 7,979 (roughly a quarter), since each kill now reaches only the still-active objectives for its kind.

</details>
