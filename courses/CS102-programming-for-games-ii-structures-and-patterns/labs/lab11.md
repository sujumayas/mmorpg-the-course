# CS102 · Lab 11: Table-driven state machines

**Week:** 11 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** one of the weekly labs (labs are 40% of the course in total)

## Objective

Prove that a flag-based character can reach illegal states, replace it with a table-driven state machine that cannot, and finish the frame-stepped jump chain from [week 11](../lectures/w11-state-and-state-machines.md) so it reproduces the lecture's log and window tables. You leave with a small, tested `FSM` class that the week 12 lab and the pattern project reuse.

## Starter materials

- `lab11-starter.py`: Python 3.10+, standard library only. Run `python lab11-starter.py` for a printout and `python lab11-starter.py --test` for the self-checks. It contains:
  - `FSM`, a working table-driven machine: a dict from `(state, input)` to next state, plus optional hooks per `(from, to)` pair.
  - `FlagHeroine`, the four-boolean heroine from the lecture, with a landing input added.
  - `reachable(make, step, key, inputs, depth)`, a breadth-first search that tries every input sequence up to `depth` and returns the set of distinct states reached. It works on any design that has a `key()`.
  - `JumpChain`, the lecture's jump-chain model built on `FSM`. Guards in `_a_symbol` turn an A press into an input symbol such as `A_AFTER_SINGLE` or `A_FAST`, so the transitions stay in the data table `JUMP_TABLE`. Two rules are missing (marked `TODO step 5`): the speed guard on the double-jump landing, and the same-frame rerun of handlers.
  - Six self-checks, with a seventh added once `StateHeroine` exists. Four fail on the untouched starter.
- The landing length (4 frames), the countdown value (5, and 0 after a triple jump) and the speed threshold (above 20) come from the Super Mario 64 decompilation cited in the lecture. The airtimes, the heroine and every other number are invented for teaching.

## Steps

1. **Count the damage.** Run the starter. Record how many of the 16 flag combinations the flag heroine reaches within 6 inputs, and list the illegal ones. For two of them, write the shortest input sequence that reaches it (modify `reachable` to keep a parent pointer if you want the program to find it).
2. **Draw the table.** On paper or in markdown, write the heroine's full transition table (4 states × 4 inputs = 16 cells, each a next state or a dash).
3. **StateHeroine.** Implement `StateHeroine` using `FSM` and your table, with `handle(button)` and `key()`. Run the exhaustive search on it with depth 6 and then depth 10. Record the count of reachable states.
4. **Hooks.** Add hooks that print "jump sound" on `standing → jumping` and "thud" on `diving → standing`. Explain in one sentence why the thud belongs on the transition and not on entering `standing`.
5. **Finish the jump chain.** In `JumpChain`, add the speed guard so a press during `double_jump_land` becomes `A_SLOW` at speed 20 or less, and make `step` rerun `handle` in the same frame while it reports a change, capped at 4 passes. All seven self-checks must pass. Explain in two sentences why the rerun fixes both the clean-triple frame numbers and delay 4 in the window test. Then add tests for Check yourself question 2 (delays 2 and 7 at speed 25) and for the late-second case `run_chain([9, 3, 3], 25)` from the lecture.
6. **Data, not code.** Move `LAND_FRAMES`, `CHAIN_FRAMES`, `TRIPLE_SPEED` and `AIR_FRAMES` into one tuning dictionary that `JumpChain` takes as an argument, and add a made-up "easy mode" tuning with a longer window. Add a validation function that rejects a landing length of zero or less, a negative countdown value, and a jump in `AIR_FRAMES` with no entry in `LANDS_AS`. Show one rejected example, and show with a sweep that easy mode's window matches `L + C - 1`.
7. **Concurrency.** Give the heroine a second, independent `FSM` for her weapon (unarmed, sword, bow; inputs `EQUIP_SWORD`, `EQUIP_BOW`, `UNEQUIP`). Add one guard: the bow cannot be equipped while diving. Run `reachable` over the combined `(movement, weapon)` key and report how many pairs are reachable out of the 12 possible.

## Deliverable

Your completed `lab11.py`, passing `--test` with your added tests, plus a report (400 to 600 words) containing: the illegal flag states with their shortest sequences (step 1), the transition table (step 2), the reachable-state counts (steps 3 and 7), the hook explanation (step 4) and the rejected schedule example (step 6).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Flag analysis | Illegal states listed with shortest sequences, count correct | Count correct, sequences missing or long | Missing | 15% |
| StateHeroine and table | Table complete, FSM matches it, exhaustive search shows exactly 4 states at depths 6 and 10 | Works, table or depth-10 run missing | Illegal states still reachable | 25% |
| Jump chain | All seven checks plus the two added cases pass, rerun explained | Guard or rerun works, not both | Fewer than five checks pass | 25% |
| Data and validation | Tuning passed in, validation catches all three error kinds with a shown example, easy-mode window verified | Data moved, validation partial | Hard-coded still | 15% |
| Concurrency and hooks | Guard works, reachable pair count reported and explained, hook placement justified | One of the two done well | Neither | 20% |

<details>
<summary>Instructor check values</summary>

- Starter flag heroine: 8 of 16 combinations reachable within 6 inputs, 5 illegal: (air, jumping, diving), (air, jumping, ducking), (air, jumping, ducking, diving), (ground, diving), (ground, ducking, diving). Shortest to (air, jumping, ducking): DOWN_PRESS, B.
- StateHeroine: exactly 4 states at any depth.
- Starter jump chain without the rerun: every jump after the first starts one frame late (touchdown on 21, not 20), and a press on the landing's last frame is lost. Four checks fail: StateHeroine, clean triple, window, speed guard.
- Finished jump chain: `run_chain([3, 3], 25)` logs 0 grounded→jump, 20 jump→jump_land, 23 jump_land→double_jump, 47 double_jump→double_jump_land, 50 double_jump_land→triple_jump, 80 triple_jump→triple_jump_land, 84 triple_jump_land→grounded. Delays 1 to 8 double, 9 hops. Delays (2, 7) at speed 25: jump 0, double_jump 22, triple_jump 53. `run_chain([9, 3, 3], 25)`: jump 0, jump 29, double_jump 52, triple_jump 79.
- Easy mode with countdown `C`: window is `4 + C - 1` frames, so `C = 9` gives 12.
- Concurrency with the one guard: all 12 pairs are reachable. The guard blocks equipping the bow during a dive, but a heroine who equips the bow first can still jump and dive. Strong reports notice this and ask whether the designer meant to forbid the pair, which needs a second guard on the movement machine (no DOWN_PRESS dive while holding the bow).

</details>
