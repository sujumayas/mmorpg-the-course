# MMO306 · Lab 02: Zone XP budget and hub layout

**Week:** 2 · **Time:** 2 hours in the lab plus about 2 hours at home · **Weight:** part of the encounter designs component (40%). The hub layout you produce here is the approach zone for your final dungeon.

**Lecture:** [Week 02, quest hubs and zone pacing](../lectures/w02-quest-hubs-and-zone-pacing.md). **Interactive:** [w02-zone-xp-budget.html](../examples/w02-zone-xp-budget.html), for checking hub coverage by eye.

## Objective

Implement the lecture's zone XP model: demand, quests needed, the share of each hub a player completes, skipping, and minutes per level. Then lay out the hubs for the zone in front of your final dungeon so that every player type you choose to support reaches the zone's climax, and show the numbers that prove it.

## Starter materials

- [`lab02-starter/zone.py`](lab02-starter/zone.py). Table loader and five functions to fill in: `zone_demand`, `quests_needed`, `hub_seen`, `hub_seen_skipping` and `level_minutes`.
- [`lab02-starter/xp_table.csv`](lab02-starter/xp_table.csv). XP to next level for levels 10 to 24 (invented, extends the lecture's table).
- [`lab02-starter/test_zone.py`](lab02-starter/test_zone.py). Tests taken from the lecture's table and check-yourself answers. Do not edit it.

Run from inside `lab02-starter`:

```
../../../../.venv/bin/python test_zone.py
../../../../.venv/bin/python zone.py
```

On the starter every test fails with `NotImplementedError`. When you are done, all five print `PASS`.

## Steps

1. **Part A, the budget (20 min).** Implement `zone_demand` and `quests_needed`. Reproduce the `n` column of the lecture's table (24.0, 20.0, 19.2, 12.0).
2. **Part B, hubs (15 min).** Implement `hub_seen`. Run `zone.py` and confirm it prints the lecture's hub columns.
3. **Part C, skipping (15 min).** Implement `hub_seen_skipping`. For the solo quester, find the skip share `s` at which the player walks through all 30 quests. Explain in one sentence why a zone with more skipping needs fewer quests per hub to reach the same place.
4. **Part D, clocks (15 min).** Implement `level_minutes`. Run the tests until all five pass. Draw one timeline for the lecture's zone with three rows: level-ups, hub arrivals and a climax quest you place. Mark where each of the four player types leaves.
5. **Part E, your zone (30 min).** Your final dungeon's entrance sits in a zone for levels 20 to 24. Choose `q`, `k`, a quest count `N` of at most 40, a hub split and the quest that holds the climax (the breadcrumb into the dungeon). Support at least three player types, defined by `k`, `o` and `s`. Every supported type must complete the climax quest. Record `X`, `n`, `c` and hub coverage for each type.
6. **Part F, a scaling variant (at home, 30 min).** Rewrite Part E under scaling within the range 20 to 24 (quests pay full XP until level 24, then the zone ends). Say what changes about which quests players reach and what you would cut or add.
7. **Design note (at home, 1 hour).** One page justifying your hub split with the numbers, naming the player type your zone serves worst and what it costs them.

## Deliverable

Submit a zip with:
- Your completed `zone.py`.
- The Part D timeline (image or spreadsheet).
- A table for Part E with one row per player type: `k`, `o`, `s`, `n`, `c`, share of each hub completed, and whether they reach the climax.
- The Part F comparison and the one-page design note.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Tests | All 5 pass | 3-4 pass | 0-2 pass | 20% |
| Timeline | Three clocks on one axis, leaving points for all four player types marked | Clocks drawn but leaving points missing | Missing | 15% |
| Zone design | At least three player types, every one reaches the climax, `c` stays between 1.0 and 1.6 for the typical type | Climax reached by most types, or `c` outside the range without justification | Climax missed by the typical type, or numbers missing | 35% |
| Scaling variant | Clear statement of what scaling changes in the model and one concrete cut or addition | Change described without numbers | Missing | 15% |
| Design note | Worst-served type named with its numbers and the cost stated | Justification without numbers | Missing | 15% |
