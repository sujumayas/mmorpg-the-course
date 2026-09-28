# MMO302 · Lab 02: Layer assignment

**Week:** 2 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

The [week 2 lecture](../lectures/w02-shards-realms-zones-instances-layers.md) computed layers for a crowd split evenly and at random. Real players arrive one at a time and many belong to guilds. In this lab you write two placement policies, measure what each does to contention and to guild cohesion, and turn the results into a layering policy you could hand to a server team.

## Starter materials

Folder [`lab02-starter/`](lab02-starter/README.md). Standard library Python only.

- `layers.py`: `mulberry32` (the same generator as the week 3 interactive), `make_population` (3,000 players, 60% in guilds of 5 to 25, shuffled arrival order), the lecture's contention model `quest_time`, and a report. Stubs for `assign_random`, `assign_guild` and `cohesion`.
- `test_layers.py`: checks your functions against the reference results.

## Steps

1. **Cohesion first.** Implement `cohesion(layer_of, guild_of)`, the share of same-guild pairs on the same layer. Solo players (guild `None`) do not count. Work the tiny example in the test by hand before you code.
2. **Random placement.** Implement `assign_random` exactly as its docstring says, including the rule for picking among open layers, so your result matches the test.
3. **Guild placement.** Implement `assign_guild`. Run the tests until they pass, then run `python layers.py`. Paste the output. Explain in two sentences why random cohesion comes out near 5% at 20 layers, using the lecture's `1 / L`.
4. **Squeeze the cap.** Rerun with `--cap 150` (no spare room at all) and `--cap 160`. Record the largest layer, cohesion and average quest time for both policies. Find the smallest cap at which guild placement keeps cohesion at 100%.
5. **Fewer layers.** Rerun with `--layers 10 --cap 330`. Compare average quest time and meetable players with the 20-layer run and with the lecture's table. Say which lecture column the simulation reproduces and which it cannot (hint: the lecture's model has no guilds).
6. **Retirement.** Write a function `retire(layer_of, keep)` that moves every player on layers `keep` and above onto the least-loaded remaining layer, keeping guilds together when they fit. Apply it to the 20-layer guild placement with `keep = 5` (day 5 in the lecture's table). Report how many players moved, the new largest layer, and the new cohesion. Each moved player is someone who sees the world reset around them. Say whether you would do this move during peak hours.
7. **Policy.** Write a one-page layering policy for the in-class launch scenario. State the placement rule, the cap, when layers are created, when they are retired, and what happens to a player mid-fight when their layer retires. Back every choice with a number from steps 3 to 6.

## Deliverable

Your finished `layers.py` (including `retire`), the outputs of steps 3 to 6 in a table, and the policy from step 7, in one Markdown or PDF file plus the code.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Placement code | All tests pass; policies follow the docstrings exactly | Tests pass but tie-breaking or cap handling hard-coded | Tests fail | 25% |
| Experiments | Steps 4 and 5 complete with the smallest safe cap found and the lecture comparison explained | Runs complete but the comparison is thin | Fewer than two experiments | 20% |
| Retirement | `retire` works, keeps guilds together where possible, moved count and cohesion reported | Works but splits guilds needlessly or omits counts | Missing | 20% |
| Policy | Every rule backed by a number; mid-fight retirement handled; player-facing cost named | Rules present, some unbacked | Opinion without numbers | 25% |
| Clarity | Tables labelled, units stated, explanations use the lecture's terms | Mostly clear | Hard to follow | 10% |
