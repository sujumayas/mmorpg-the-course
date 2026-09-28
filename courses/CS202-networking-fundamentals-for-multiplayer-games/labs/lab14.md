# CS202 · Lab 14: Break it on purpose

**Week:** 14 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Build a seeded network conditioner, prove it matches the [week 14 lecture](../lectures/w14-testing-under-bad-networks-netem-clumsy.md) model, and use it in a test matrix to find, replay and fix bugs in a small interpolation client that passes every test on a perfect network. Then measure a real conditioner (netem, clumsy, or this lab's proxy) with Lab 02's ping and check that it does what its settings claim.

## Starter materials

Folder [`lab14-starter/`](lab14-starter/README.md). Standard library Python only.

- `conditioner.py`: a one-direction conditioner with netem-style uniform jitter, duplicates and a seeded Gilbert-Elliott dropper. You write `GilbertLoss.drop`, `burst_lengths`, `reorder_count` and `bursts_per_minute`. Running the file runs the checks.
- `toy_client.py`: a 30 Hz snapshot-interpolation client that draws one entity 120 ms in the past, with extrapolation when the buffer runs dry. It contains planted bugs.
- `run_matrix.py`: runs the client under each profile and seed, with three checks (no exception, the client's `server_tick` never goes backwards, no teleport or drift from the true position), and replays a single run with `--repro`.
- `profiles.json`: the five server-to-client profiles from the lecture's section 4 table.
- `udp_conditioner.py`: the same model as a live UDP proxy, for step 5.
- Lab 02's `echo_server.py`, `udp_ping.py` and `analyze.py` in [`lab02-starter/`](lab02-starter/README.md).

## Steps

1. **The model.** Implement the four TODOs in `conditioner.py` until `python conditioner.py` prints `all checks passed`. Before you run the formula check, compute by hand `bursts_per_minute(0.01, 0.5, 3, 30)` and the median wait it implies.
2. **Predict the matrix.** Before running anything else, fill in a table with one row per profile in `profiles.json`. For each, compute `λ` for bursts of at least 3 at 30 Hz and the chance of at least one in a 60-second run, and compute the chance that a consecutive pair of snapshots is reordered (lecture section 3). Predict which profiles will show failures.
3. **Run and replay.** Run `python run_matrix.py`. Compare the fail counts with your predictions. For each distinct failure message, replay one seed with `--repro` and write down the profile, seed, time and message. Now read `toy_client.py` and find the cause of each failure. Explain, with the section 3 formula, why one of the bugs can never appear in the `evening_wifi` profile at 30 Hz.
4. **Fix and prove it.** Fix each bug with the smallest change you can defend. After each fix, rerun the matrix with `--seeds 30` and show the table. Then add a profile of your own that would have caught the second bug at 20 Hz sending, and explain the settings.
5. **Measure a real conditioner.** Pick the tool for your OS. Run Lab 02's echo server and ping at 60 Hz for 60 seconds through it, analyze the log with Lab 02's `analyze.py`, and compare round-trip loss, minimum and median RTT, and reordered count with what the model predicts.
   - Linux: `sudo tc qdisc add dev lo root netem delay 20ms 15ms loss gemodel 2.63% 50% 100% 0%` (average 5%, mean burst 2), ping directly on port 40002, then `sudo tc qdisc del dev lo root`.
   - Windows: clumsy 0.3 with filter `udp and (udp.DstPort == 40002 or udp.SrcPort == 40002)`, Lag 20 ms and Drop 5%, both directions.
   - macOS or anything else: `python udp_conditioner.py --delay 20 --jitter 15 --loss 0.05 --burst 0.5` and ping on port 40004.
   Say which settings apply once and which apply twice on a round trip. If your measured numbers differ from the model by more than the MA102 week 13 margin, find out why.
6. **Size a real test.** Your team's nightly build gets 20 minutes of network testing. For the bug from step 3 that needed a burst, what `p` and `q` would give a 95% chance of catching it in that time at 30 Hz? Would you put that profile in the realism or the stress group?

## Deliverable

Your finished `conditioner.py` and fixed `toy_client.py`, your added profile, and a report (PDF or Markdown, at most four pages) with the hand calculations from step 1, the prediction table and the actual matrix from steps 2 and 3, the replay notes and bug explanations, the matrix after each fix, the step 5 comparison, and the step 6 answer. Submit before the final prototype review.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Conditioner | All checks pass; hand calculation agrees; burst and reorder functions follow the definitions | Passes with a function fitted to the test rather than the definition | Fails the checks | 20% |
| Prediction before running | Every profile's `λ`, detection chance and reorder chance computed before the run and compared honestly | Predictions for some profiles, or written after the run | No predictions | 20% |
| Bugs found and explained | Both bugs located, each tied to a network event with the lecture's formula, including why one cannot occur in `evening_wifi` | Both found, explanation thin | One or none found | 25% |
| Fixes and proof | Minimal fixes, 30-seed matrix clean after each, a new profile that catches the second bug at 20 Hz with justified settings | Fixed, matrix shown once | Fixes that hide the check instead of the bug | 15% |
| Real conditioner | Tool run and measured; one-way vs round-trip settings explained; differences checked against the margin | Measured but not compared with the model | No measurement | 15% |
| Writing | Plain, numbers with units, seeds and settings recorded for every claim | Mostly clear | Hard to follow | 5% |
