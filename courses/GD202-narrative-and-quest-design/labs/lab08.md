# GD202 · Lab 08: Chain shapes

**Week:** 8, quest chains and zone storytelling ([lecture](../lectures/w08-quest-chains-and-zone-storytelling.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the quest chain assignment (60%). The zone graph you design here becomes the structure of your final quest chain.

## Objective

Write a tool that reads a zone's quest prerequisites and reports its trips `T`, width `W`, order control `C` and play time. Extend it to handle field handoffs. Then design the quest graph for your own zone and defend its shape with numbers.

## Starter materials

All in [`lab08-starter/`](lab08-starter/). Standard-library Python.

- [`quest_graph.py`](lab08-starter/quest_graph.py), a skeleton with a CSV loader, a working `ancestors` function and five TODO functions: `layers`, `trips`, `width`, `order_control` and `zone_minutes`. In the code, `work` is the lecture's `t_task` and `round_trip` is `t_travel`.
- [`zones.csv`](lab08-starter/zones.csv), the lecture's five nine-quest shapes (linear, strands, braided, flat, waves), one row per quest with its prerequisites separated by `;`.
- [`test_quest_graph.py`](lab08-starter/test_quest_graph.py), tests with the lecture's table: `T`, `W`, `C` and zone time for all five shapes, a small layering case, and checks that cycles and unknown prerequisites raise `ValueError`.
- The [interactive](../examples/w08-quest-chain-shapes.html) for spot checks.

Run the tests from inside the starter folder with `../../../../.venv/bin/python test_quest_graph.py`. They all fail on the starter. They all pass once your functions are correct.

## Steps

1. **Layers.** Implement `layers(zone)`. Check first that every prerequisite names a quest in the zone. Then repeatedly collect every unfinished quest whose prerequisites are all finished. If a round collects nothing while quests remain, raise `ValueError` (there is a cycle).
2. **Trips and width.** Implement `trips` and `width` from the layers.
3. **Order control.** Implement `order_control` using `ancestors`. Count a pair as fixed when either quest is an ancestor of the other.
4. **Zone time.** Implement `zone_minutes(zone, work, round_trip)`.
5. **Tests.** Run the test file until every test passes. Then run `quest_graph.py` and confirm the lecture table.
6. **Field handoffs.** Add a function `hub_trips(zone, field)` where `field` is a set of `(prerequisite, quest)` arrows whose follow-up is handed out in the field. A batching player who finishes a quest in the field and is handed its follow-up there does that follow-up in the same trip. Define it carefully in a docstring, write at least three tests of your own, and report `hub_trips` for the braided zone when all three arrows into the finale are field handoffs.
7. **Log cap.** Add `trips_with_cap(zone, m)`, where the player carries at most `m` quests per trip (lowest ids first). Test it on the flat zone with `m = 4` (answer: 3 trips).
8. **Your zone.** Draft the quest list for your final project's zone: 12 to 16 quests, with a spine of 3 to 5 bottleneck quests. Record it as a CSV in the same format. Your targets: `C ≥ 0.6`, `T ≤ 6`, `W ≤ 5`. Report all numbers and the zone time with `t_task = 3` and `t_travel = 4`.
9. **Stress test.** Remove the single arrow whose removal lowers `C` the most. Report which arrow it is, the new `C`, and what that tells you about which beat your zone depends on most.

## Deliverable

Your code with passing tests (including your own tests for steps 6 and 7), your zone CSV, and a report of at most 800 words: the lecture table reproduced, the handoff result, your zone's numbers with a drawing of its graph (hand-drawn photo is fine), and one paragraph per spine quest saying why it must be a bottleneck.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Core tool correctness | All provided tests pass; clear code | Tests pass, code hard to follow | Tests fail | 25% |
| Extensions (handoffs, cap) | Both defined precisely, with own tests that would catch a wrong answer | One extension complete, or tests too weak | Missing | 20% |
| Zone design | Meets all three targets; spine beats are real turns in the story | Misses one target, or spine is arbitrary | Misses two or more | 30% |
| Justification | Each bottleneck argued from what the player must already know | Arguments generic | Missing | 15% |
| Stress test | Arrow found and its story role explained | Arrow found, no reading of it | Missing | 10% |
