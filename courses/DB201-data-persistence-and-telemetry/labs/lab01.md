# DB201 · Lab 01: Save intervals and a crash-proof save

**Week:** 1 ([Why persistence is hard in games](../lectures/w01-why-persistence-is-hard-in-games.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually

## Objective

Turn the periodic-save model from lecture into numbers you computed yourself, confirm the `T / 2` average loss by simulation, price a hybrid save policy, and write a save routine that leaves a valid file on disk no matter where a crash lands.

## Starter materials

- Python 3.10 or later, standard library only. In this repository use `.venv/bin/python`.
- `labs/lab01-starter/save_sim.py`, which contains:
  - `model(n_players, interval_s, state_bytes)`: complete. Returns `W`, `B`, average and worst loss, and player-hours lost per crash.
  - `simulate_loss(interval_s)`: you write it (Part A).
  - `hybrid_writes_per_s(n_players, interval_s, events_per_player_hour)`: you write it (Part A).
  - `write_with_crash(f, text, crash_after)`: complete. Writes in 64-character chunks and raises `SimulatedCrash` after `crash_after` characters, with the partial data flushed.
  - `naive_save`: complete, overwrites the file in place.
  - `atomic_save`: you write it (Part B).
  - `crash_test(save_fn)`: saves version 1, then crashes while saving version 2 at 41 evenly spaced points, and counts how often the file left behind is neither version.
- Run `python save_sim.py --check` for the tests only, `python save_sim.py` for the tests plus the model table.

## Steps

### Part A: the model (35 minutes)

1. Run `python save_sim.py` before changing anything. Copy the model table (T = 1, 10, 60, 300, 840 s) into your report and check two rows by hand against the lecture's formulas.
2. Implement `simulate_loss`. For each simulated crash, the time since the player's last save is uniform on `[0, T)`. Return the mean. The check expects about 150 s for `T = 300`.
3. Extend your report with a simulated column for all five `T` values and compare it with `T / 2`.
4. Implement `hybrid_writes_per_s` as periodic writes plus event writes. The check expects 26.667 for `N = 4,000`, `T = 300`, `e = 12`.

### Part B: the crash-proof save (35 minutes)

5. Look at the `naive_save` line of the check output. Explain in two sentences why every one of the 41 crash points leaves a corrupt file, including the crash at character 0.
6. Implement `atomic_save`: write the full text to a temporary file in the same directory using `write_with_crash`, flush, `os.fsync`, then `os.replace` the temporary file over the real one. The check must report `0/41`.
7. Remove the `flush` and `os.fsync` lines and run the check again. It still passes. Explain why: what kind of crash does `write_with_crash` imitate, and what kind of crash would the missing `fsync` expose? Put the lines back.

### Part C: the policy (at home)

8. Use the in-class MMO from lecture (6,000 players, 40 kB state, `e = 14.5` valuable events per player-hour, 2 kB per event write). Add rows to the model table for your chosen `T` and compute the hybrid writes and bytes per second.
9. Write at most 250 words recommending a save policy for that game. Include the value of `T`, the list of valuable events, the average loss of cheap state in seconds, and one risk the hybrid creates (for example, a character restored with a new item but without the XP that earned it).

## Deliverable

Your completed `save_sim.py`, and a report (Markdown, text or notebook) with the tables from steps 1, 3 and 8, the answers to steps 5 and 7, and the policy memo.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Model and simulation (25%) | Table complete, two rows hand-checked, simulation within 2% of `T/2` for all five `T` | Table complete, one hand check | Table partly filled or simulation off | Missing |
| Hybrid computation (15%) | Function correct; step 8 rows correct for writes and bytes | Writes correct, bytes missing | Arithmetic errors | Missing |
| Atomic save (30%) | `0/41` corrupt; explanation of naive failure names truncation; step 7 distinguishes a process crash from a power loss | `0/41`, explanations thin | Passes only after changing the test | Does not pass |
| Policy memo (25%) | Justified `T`, event list, cheap-state loss in seconds, a concrete risk of the hybrid | Policy clear, one element missing | Policy without numbers | Missing |
| Code quality (5%) | No changes to the test harness; readable names | Minor issues | Harness edited | Missing |
