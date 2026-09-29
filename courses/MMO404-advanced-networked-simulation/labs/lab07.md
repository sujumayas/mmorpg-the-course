# MMO404 · Lab 07: A dilation controller

**Week:** 7 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Build the time dilation controller from the [week 7 lecture](../lectures/w07-time-dilation-revisited.md), reproduce its tables exactly, and tune it on a noisy, seeded battle to meet a target for backlog and speed jitter. Then compute clock domains for a small seamless map and plan node reinforcements for a fight across several systems. You finish with a dilation and node plan for one of the lecture's scene cards, backed by your own runs.

## Starter materials

Folder [`lab07-starter/`](lab07-starter/README.md). Standard library Python only.

- `tidi_control.py`: the node constants from MMO302 week 12 (`A`, `B`, `C`, `FLOOR`), the `mulberry32` generator shared with the interactive, the 180-second battle, and printers for the lecture's tables (`--table`, `--battle`) and a CSV sweep (`--grid`). Stubs for `work`, `target_speed`, `next_speed`, `run`, `domain_speeds` and `node_speed`.
- `test_tidi_control.py`: the lecture's numbers as tests.

## Steps

1. **The node.** Implement `work(n)`. Check by hand that 500 pilots fit at full speed and 2,000 do not.
2. **The controller.** Implement `target_speed` and `next_speed` following their docstrings. Before you code, compute the target for backlog `q = 3.6`, `m = 4.6`, aim 0.9, `τ = 5` by hand and say why it is clamped.
3. **The loop.** Implement `run`. Keep the order of operations exactly as the docstring gives it, including one generator draw per second even with no noise, or your numbers will not match the interactive. Run `python test_tidi_control.py` until the section 2 and 3 checks pass. Then run `python tidi_control.py --table` and `--battle` and paste both outputs.
4. **The ceiling.** Write a function `floor_capacity(aim, floor)` that returns the largest pilot count the node can hold at the floor without the backlog growing. Check it gives about 2,854 at aim 0.9. Run a battle whose second wave is 50 pilots above your answer and one 50 below, noise 0, and show the backlog in the last minute of each wave.
5. **Tune.** Your target is peak backlog under 3 s, mean backlog under 0.2 s and jitter under 0.07 on the default battle with noise 0.3 and seed 7. Run `--grid grid.csv`, add any settings you want to try (you may change `τ`, `α_down` and the floor as well), and find the setting that meets the target with the most game-seconds. Then check it on seeds 1 to 10 and report how many seeds still meet the target.
6. **Domains.** Implement `domain_speeds`. The tests cover the lecture's examples. Then take the 3 × 3 grid of servers below, where each number is the speed that server can afford alone, and every server links to its horizontal and vertical neighbours. Compute delivered game-seconds per real second as one domain. Then find the smallest set of links whose removal raises delivered game-seconds above 6, prove no smaller set works, and say what those gates would be in a real world (a canyon, a portal, a zone line). Say what the players on the slow server lose.

   ```
   1.0  1.0  0.9
   1.0  0.3  1.0
   0.8  1.0  1.0
   ```

7. **Nodes.** Implement `node_speed` and run the tests until they all pass. Reproduce the three plans in section 4 of the lecture. Then take the lecture's three-system card (1,200, 800 and 400 pilots, one gate between each pair, quiet systems with a total load of 0.2 on the ordinary node). You may book one dedicated node with `C = 2`. Find the booking that maximizes the slowest system's speed, then move 400 pilots from the largest system to the smallest and report every speed again.
8. **Policy.** Pick one scene card from the lecture's in-class activity. In one page, give your controller settings with numbers from step 5, the largest fight your node holds from step 4, your node booking with its speeds before and after the crowd moves, and what players see when the fight grows past your ceiling.

## Deliverable

Your finished `tidi_control.py` (including `floor_capacity`), the outputs of step 3, the two runs of step 4, your tuning table with the chosen setting and its seed check from step 5, the domain answer from step 6, the node plans from step 7, and the policy from step 8, in one Markdown or PDF file plus the code.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Controller code | All tests pass; order of operations and generator use match the docstring | Tests pass for section 2 but the noisy battle is off | Tests fail | 25% |
| Ceiling | `floor_capacity` exact; the two runs show bounded and growing backlog on either side | Capacity correct, runs missing or unexplained | Missing or wrong | 15% |
| Tuning | Target met with a justified setting; seed check reported; the trade-off in game-seconds stated | Target met on seed 7 only, or trade-off not stated | Target not met | 25% |
| Domains and nodes | Single-domain value correct; the four links around the slow server found, minimality argued, and each turned into a world feature; node booking justified with speeds before and after the crowd moves | Correct values, weak argument or unexplained booking | Missing | 15% |
| Policy | Every setting and the node booking backed by a number from your runs; player experience past the ceiling named | Settings present, some unbacked | Opinion without numbers | 20% |
