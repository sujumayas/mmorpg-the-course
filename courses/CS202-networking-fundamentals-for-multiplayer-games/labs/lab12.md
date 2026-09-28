# CS202 · Lab 12: Lockstep timing and the desync hunt

**Week:** 12 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Model the timing of a deterministic lockstep game from the [week 12 lecture](../lectures/w12-deterministic-lockstep-rts.md), then find and fix real determinism bugs in a small two-player simulation using per-turn checksums. You finish with a lockstep configuration (turn length and `k`) for a given player population, and a short bug report for each desync you fixed.

## Starter materials

Folder [`lab12-starter/`](lab12-starter/README.md). Standard library Python only.

- `lockstep.py`, part A: stubs for `execution_delay`, `simulate_turns` and `Peer.checksum`, with `--timing` to print the effective turn length and average command delay for a range of latencies.
- `lockstep.py`, part B: a two-player simulation of 12 units with integer positions and health, tile reservation for move orders, a shared seeded random generator for hit rolls, and a fixed command script. `--sync` runs two peers and compares checksums every turn. The starter contains more than one determinism bug.

## Steps

1. **Part A functions.** Implement `execution_delay` and `simulate_turns` from the lecture's timing model, and `Peer.checksum` as a CRC-32 over the turn number and each unit's id, x, y and hp packed with `struct`. Run `python lockstep.py --check`. Every test except "two peers stay in sync" must pass.
2. **Reproduce Table 2.** Run `python lockstep.py --timing` and `--timing --jitter 60`. Confirm the fixed-latency rows against `T_eff = max(T, (T + L_max) / k)` by hand for the 250 ms and 400 ms rows.
3. **Choose `T` and `k`.** Your RTS has four players whose worst one-way latency is 180 ms on a normal evening and 320 ms at the 95th percentile, with 40 ms of jitter. Find the combination of `T` (between 100 and 250 ms) and `k` (2 to 4) with the lowest average command delay that never slows the game at the 95th percentile. Show the runs you used.
4. **Find the first desync.** Run `python lockstep.py --sync`. Record the first bad turn and the differing units. Write down, before changing anything, your hypothesis for the cause.
5. **Fix it.** Find the line that causes the divergence and fix it without changing the command script, the tile-reservation rule or the 75% hit chance. Explain why the bug produces different results on the two peers. Run `--sync` again.
6. **Repeat until clean.** There is more than one bug. For each, record the first bad turn, the differing field and the fix. You are done when `--check` prints `all checks passed` and `--sync --turns 2000` stays in sync.
7. **Break it on purpose.** Change health from integer tenths to a float and make damage `7.3`, applied through a helper that sums all hits a unit takes in one turn in the order the attackers are listed on that peer. Make the two peers list attackers in a different order. Does it desync? If not within 2,000 turns, explain why not with the lecture's floating-point section, and change the damage values until it does.
8. **Replay.** Save the command script and the starting seed to a JSON file, reload it in a fresh process, run 500 turns and confirm the final checksum matches. Explain why this is the same property that makes lockstep work.

## Deliverable

Your fixed `lockstep.py`, the tables from steps 2 and 3, a bug report for each desync (first bad turn, symptom, cause, fix, one sentence on how you would have prevented it), the step 7 experiment with its result, and the replay file and checksum from step 8. Submit before next week's lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Part A functions and timing | `--check` part A passes; Table 2 rows derived by hand; checksum packs explicit byte order | Passes, derivation thin | Fails | 20% |
| Configuration (step 3) | Search is systematic; chosen `T` and `k` meet the 95th percentile with the lowest delay, runs shown | Reasonable choice with partial evidence | Guessed | 15% |
| Desync fixes | All bugs fixed within the rules; `--sync --turns 2000` clean; each fix targets the cause, not the symptom | Some bugs fixed, or a fix that changes game rules | Still desyncs | 30% |
| Bug reports | Each report names the first bad turn, the field, the root cause in section 3's terms, and a prevention | Reports present but causes vague | Missing | 20% |
| Float experiment and replay | Step 7 shows or explains order dependence correctly; step 8 replay matches | One of the two | Neither | 15% |
