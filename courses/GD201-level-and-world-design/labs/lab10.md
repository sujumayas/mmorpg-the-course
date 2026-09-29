# GD201 · Lab 10: Errand costs, shortcuts and gate slack

**Week:** 10 · **Time:** 2 hours in the lab plus about 2 hours at home · **Weight:** part of the blockouts component (40% of the course). The connection plan you produce here goes into your final greybox zone.

**Lecture:** [Week 10, hubs, spokes, and gating](../lectures/w10-hubs-spokes-and-gating.md). **Interactive:** [w10-hub-errands.html](../examples/w10-hub-errands.html), for checking unweighted cases.

## Objective

Implement the lecture's errand model on graphs whose links have real lengths, use it to choose the best shortcut for a chain-shaped zone, compute gate slack for a gated hub, and then apply all three to the connections of your own final-zone blockout.

## Starter materials

- [`lab10-starter/hubs.py`](lab10-starter/hubs.py). A sample zone (a river valley laid out as a chain of seven destinations from a town), five candidate shortcuts, a sample gated hub, and two given helpers: `build` (edge list to adjacency dict) and `shortest` (Dijkstra's algorithm, which is breadth-first search generalised to links of different lengths). You fill in four functions: `errand_cost`, `pairwise_cost`, `best_shortcut` and `gate_slack`. The docstrings define each one.
- [`lab10-starter/check_lab10.py`](lab10-starter/check_lab10.py). A checker with 10 checks. Do not edit it.
- Your blockout from earlier labs (engine project or paper plan) and a way to measure path lengths in it (the engine's ruler tool, or squares on the paper plan).

Run from inside `lab10-starter` with the course Python:

```
python hubs.py
python check_lab10.py
```

The starter runs and reports that the functions are not implemented. The checker prints `0/10 checks pass` until you fill them in.

## Steps

1. **Part A, the model (20 min).** Implement `errand_cost` using `shortest`. Check it against the lecture: a hub with eight spokes of 100 m gives 200 m, a chain of eight gives 900 m, and the chain plus a loop-back gives 500 m. Implement `pairwise_cost` and confirm the chain's 300 m.
2. **Part A, the sample zone (5 min).** Run `hubs.py`. Record `E` and the pairwise mean for the river valley. Convert `E` to seconds at 6 m/s.
3. **Part B, shortcuts (20 min).** Implement `best_shortcut`: add each candidate on its own, recompute `E`, keep the lowest. Print `E` for every candidate, not only the winner. The lecture said the best shortcut is usually the one that joins the far end to the hub. Is it here? Write two sentences explaining why or why not, using the distances from `shortest`.
4. **Part C, gate slack (15 min).** Implement `gate_slack`. Reproduce the lecture's table (2.00, 1.33, 1.20, 1.14, 1.25) and check-yourself question 3. Run the checker until it prints `10/10 checks pass`.
5. **Part C, fix the squeeze (10 min).** Change `SAMPLE_GATES` so that no gate has slack below 1.5 and the final door still needs at least 30 tokens. Record your thresholds and their slack.
6. **Part D, your zone (40 min).** Draw your final-zone blockout as a graph: one hub and at least six destinations. Measure each link's length in metres. Enter it as an edge list. Compute `E` and the pairwise mean.
7. **Part D, one shortcut (15 min).** List three shortcuts you could build (with lengths). Use `best_shortcut` to choose one. Then decide whether to build it, weighing the saving in `E` against what the shortcut costs you (a path players will skip, a view they will miss, a gate it bypasses).
8. **Part D, gates (15 min).** If your zone has count, key or level gates, list them with their thresholds and compute slack. If a key gate adds an errand (the key is far from its door), compute the extra metres.
9. **Stretch (optional).** Add a `return_home(edges, hub, uses_per_hour, errands_per_hour)` function that models a cooldown teleport home as in check-yourself question 4, and report the metres it saves per hour for your zone.

## Deliverable

Submit a zip with:
- Your completed `hubs.py`, including your zone's edge list and shortcut candidates.
- A one-page write-up with: the sample zone's `E` and pairwise mean; the table of `E` for every candidate shortcut and your two sentences from step 3; your new gate thresholds and slack from step 5; your zone's graph (a clear sketch with lengths), its `E` before and after your chosen shortcut, and your build-or-not decision in three to five sentences; your zone's gate slack table.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker | 10/10 checks pass | 6-9 pass | 0-5 pass | 25% |
| Shortcut analysis (sample) | All five candidates tabled; explanation uses the distances to say why the winner beats the far-end link | Table present, explanation vague | Missing or only the winner reported | 20% |
| Gate redesign | Every gate at slack ≥ 1.5, final door ≥ 30, thresholds justified | Constraint met without justification | Constraint not met | 15% |
| Own zone model | Graph matches the blockout, lengths measured, `E` and pairwise mean correct | Graph present, some lengths estimated | Missing or doesn't match the blockout | 25% |
| Design judgment | Build-or-not decision weighs the saving against a named cost | Decision stated with numbers only | No decision | 15% |
