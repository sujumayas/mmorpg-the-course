# MMO302 · Lab 04: Zone handoff simulator

**Week:** 4 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Turn the [week 4 lecture](../lectures/w04-zone-servers-and-handoff.md)'s boundary-tax model into code, check the handoff formula against a random-walk simulation, and build the numbered handoff protocol so that no lost, duplicated or reordered message can leave a player with two owners. You finish with a zone layout for a given shard, with its handoff rate, ghost share and busiest zone stated as numbers.

## Starter materials

Folder [`lab04-starter/`](lab04-starter/README.md). Standard library Python only.

- `zone_sim.py`: stubs for `handoff_rate`, `ghost_fraction`, `busiest_zone`, `next_owner` (the hysteresis rule) and the two `ZoneServer` methods of the handoff protocol. Provided: `zone_of`, the random-walk `simulate`, the idle-crowd `idle_crowd`, a hand-driven `Network` that lets you lose and reorder messages, and a command line.
- `test_zone_sim.py`: the lecture's numbers, a simulation check, the ping-pong table and three protocol scenarios (normal, lost ACK, stale replay).

## Steps

1. **The formulas.** Implement `handoff_rate`, `ghost_fraction` and `busiest_zone`. Run `python zone_sim.py --table` and confirm it matches the lecture's two tables row for row.
2. **Hysteresis.** Implement `next_owner`. The owner keeps an entity while it stays inside the owner's square grown by `h/2` on every side. Explain in two sentences why growing the owner's square is the same as the lecture's "band of width `h`".
3. **Check the formula.** Run `python zone_sim.py --simulate 2` and `--simulate 4`. Record measured against predicted. Then change `simulate` so walkers bounce off the world edge instead of wrapping, and run again. Report the difference and explain it (hint: what does a wall do to the density near it, and to the direction of travel?).
4. **Ping-pong.** Run `python zone_sim.py --idle`, then add a loop over `checks_per_second` of 1 and 10. Reproduce the lecture's ping-pong table within 15%. Plot handoffs per second against `h` for both check rates.
5. **The protocol.** Implement `ZoneServer.start_handoff` and `ZoneServer.on_message`. Run `python test_zone_sim.py` until it prints `all lab 04 tests passed`.
6. **Break it on purpose.** Remove the stale-sequence check from `on_message` and show, with a sequence of `Network.deliver` calls, a state where two servers both `owns("p")`. Put the check back. Then write one new test of your own: a corner case where A offers the player to B and then, before any reply, the player's position says C. What should `start_handoff` do, and does your code do it?
7. **Extension (optional, counts toward "excellent").** Add `REVOKE(pid, seq)` so A can take a player back after a lost ACK, following the lecture's failure table. Show with a test that a REVOKE and a delayed ACK in either order still leave exactly one owner.
8. **Layout memo.** Use the in-class brief (8 km world, 4,000 players, 30% in a capital, a 400-player world boss, 900 players per server). Propose a layout, compute `H`, `G` and the busiest zone with your functions, pick a band `h`, and say where the world boss must not be allowed to spawn.

## Deliverable

Your finished `zone_sim.py` and tests, the measured-against-predicted numbers from step 3 (both edge rules), the ping-pong plot from step 4, the broken-protocol trace from step 6, and a layout memo of at most 500 words for step 8. One Markdown or PDF file plus the code.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model and hysteresis | Tables reproduced; `next_owner` passes; band equivalence explained | Tables right, explanation vague | Tests fail | 20% |
| Simulation analysis | Both edge rules run; wall effect explained with density and direction | Numbers reported without the explanation | Missing | 20% |
| Ping-pong | Table reproduced within 15% at both check rates; plot labelled | One check rate only | Missing | 15% |
| Protocol | All tests pass; broken trace shown; corner test written and passing; REVOKE extension done | Tests pass, broken trace or corner test missing | Tests fail | 25% |
| Layout memo | Every number from the functions; boss spawn rule justified with the city-border calculation | Numbers present, reasoning thin | Opinion without numbers | 20% |
