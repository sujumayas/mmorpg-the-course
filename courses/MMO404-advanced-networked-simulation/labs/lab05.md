# MMO404 · Lab 05: Dead reckoning and shaping

**Week:** 5 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Build the two halves of the [week 5 lecture](../lectures/w05-bandwidth-shaping-and-lod-for-networking.md) and make them work together. You implement an error-driven (dead-reckoning) sender and check its interval against `√(2ε / a)`, then a token-bucket shaper whose queue keeps one update per entity and drains by priority. You run both on a seeded hub where a world boss spawns halfway through, find where the shaper makes things worse, and fix it.

## Starter materials

Folder [`lab05-starter/`](lab05-starter/README.md). Standard library Python only.

- `lod.py`: TODOs for `smooth_interval`, `guess`, `needs_update`, `Shaper.offer` and `Shaper.tick`. Given code builds the hub (`make_hub`, `behave`), runs it under either policy with or without the shaper (`run_hub`) and writes a CSV. `--check`, `--hub`, `--shaped` and `--budget` modes.

## Steps

1. **The sender.** Implement `smooth_interval`, `guess` and `needs_update`. Run `python lod.py --check` until only the shaper fails. The circle test compares your sender with the formula. Explain in two sentences why the formula holds only for small `ε / R`.
2. **The shaper.** Implement `Shaper.offer` (replace, do not append) and `Shaper.tick` (refill, then send by priority until the next update does not fit). Run `--check` until it prints `all checks passed`.
3. **Unshaped.** Run `python lod.py --hub hub.csv`. Plot kbit/s against time for both policies on one chart, and mean angular error on a second. Compare the quiet and panic numbers with the lecture's model (54.1 and 194.5 kbit/s for error-driven). The simulation gives different numbers. Name two behaviours in `behave` that explain the gap.
4. **Shaped, generous.** Run with `--shaped` (96 kbit/s). Tiers now show angular errors of tens or hundreds of degrees. Find out why. Look at which entities never get sent and what the client's guess does to them. Write the explanation in three sentences.
5. **Shaped, tight.** Run with `--budget 48`. Error-driven updates now break too, but only during the panic. Report the worst error and which band it comes from.
6. **Fix it.** Make two changes in your copy of `run_hub` and report the effect of each at 48 kbit/s. First, add the time since an entity's last update to its shaper priority, so waiting entities climb the queue (week 4's accumulator idea). Second, stop extrapolating a guess more than 1 second past its update (hold the last extrapolated position). Report mean and worst error in the panic, before and after each change.
7. **Your policy.** Write a one-page shaping policy for the hub. Give `ρ`, `σ`, the priority rule, the extrapolation limit, and the order in which you shed detail when the backlog grows. Support each choice with a number from steps 3 to 6.

## Deliverable

Your finished `lod.py`, the CSVs from steps 3 to 6, the two charts from step 3, and a report (PDF or Markdown, at most three pages) with the answers to steps 1 and 3 to 6 and the policy from step 7. Submit before the week 6 lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Sender | `--check` passes; small-angle limit of the formula explained | Passes, explanation missing | Fails | 15% |
| Shaper | Replace-not-append and priority drain correct; `--check` passes | Passes after patching a test value | Fails | 15% |
| Unshaped analysis | Both charts; gap with the lecture model explained by named behaviours | Charts present, gap unexplained | Missing | 15% |
| Starvation diagnosis | Steps 4 and 5 identify the starved entities and the unbounded extrapolation, with numbers | Symptom described, cause vague | Missing | 20% |
| Fix | Both changes implemented and measured separately, before and after | One change measured | Missing | 20% |
| Policy | Every parameter justified with a measured number; shedding order stated | Parameters given, some unjustified | Missing | 10% |
| Writing | Plain, units everywhere | Mostly clear | Hard to follow | 5% |
