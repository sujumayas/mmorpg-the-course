# CS202 · Lab 02: Measure your own connection

**Week:** 2 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Build the measuring tool a netcode programmer reaches for first. You will run a game-style UDP ping through a proxy that injects delay, jitter and loss you control, write the analysis that turns the log into the numbers from the [week 2 lecture](../lectures/w02-latency-jitter-loss-measure-your-own.md), check that it recovers the settings you injected, and then point it at a real connection. You finish with a buffer recommendation for that connection.

## Starter materials

Folder [`lab02-starter/`](lab02-starter/README.md). Standard library Python only.

- `echo_server.py`: UDP echo on port 40002.
- `bad_net_proxy.py`: UDP proxy on port 40003 that adds `delay + U(0, jitter)` ms per datagram per direction, an extra spike with a set probability, and random loss. Seeded.
- `udp_ping.py`: sends 12-byte packets (sequence number and send time) at a fixed rate and writes `seq, send_ms, rtt_ms, arrival_order` to a CSV.
- `analyze.py`: loads a log and prints a report. You write the functions marked TODO. `python analyze.py --check` tests them on `sample_run.csv`.
- `sample_run.csv`: the 20 pings from the lecture's worked example, plus one lost packet.

## Steps

1. **Analysis first.** Implement `loss_rate`, `reordered`, `percentile`, `rfc3550_jitter`, `late_fraction` and `buffer_for` in `analyze.py`. Run `python analyze.py --check` until it prints `all checks passed`. Compute the median and the RFC 3550 jitter of the sample by hand for the first six packets, and show that your code agrees.
2. **A clean baseline.** Start `echo_server.py`. Run `udp_ping.py --port 40002 --seconds 30` (direct, no proxy). Analyze it. Record the minimum, median and P95 RTT. Explain in two sentences why localhost numbers are so small and what they measure.
3. **Recover what you injected.** Start the proxy with `--delay 20 --jitter 5 --spike-chance 0 --loss 0`. Ping through port 40003 for 30 seconds. Predict the minimum and median RTT before you look (both directions pass through the proxy), then compare.
4. **Loss, both ways.** Restart the proxy with `--loss 0.05`. Predict the ping loss rate with the lecture's round-trip formula, run 60 seconds, and compare. Is the difference within what you would expect from chance? Use the MA102 week 13 margin `1.96 × sqrt(p(1 − p) / n)`.
5. **Spikes and reordering.** Restart with `--spike-chance 0.05 --spike 80 --loss 0.01`. Run 60 seconds. Report reordered packets and explain why a spike of 80 ms at 20 Hz can reorder packets while a spike of 40 ms rarely does.
6. **Size the buffer.** For the run in step 5, report `B` for 10%, 5% and 1% late targets and the felt one-way latency for each. Plot the sorted extra delays with the three buffer lines (any plotting tool, or a spreadsheet).
7. **A real connection.** Run `echo_server.py --host 0.0.0.0` on one machine and ping it from another over the lab network, or over Wi-Fi from across the building, for at least 5 minutes at 20 Hz. Report every statistic from `analyze.py`, the longest loss burst, and a buffer recommendation for a third-person action game. Say whether you would trust a 1% target from this much data.

## Deliverable

Your finished `analyze.py` and a report (PDF or Markdown, at most three pages) with the hand check from step 1, predictions and results for steps 2 to 5 side by side, the plot from step 6, and the analysis and recommendation from step 7. Submit before next week's lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Analysis code | `--check` passes; functions are short and follow the lecture's definitions; hand check agrees | Passes with one function patched to fit the test rather than the definition | Fails the check | 25% |
| Predictions vs results | Every prediction written before the run, with the formula; differences explained with the margin | Predictions present but explanations thin | Results only, no predictions | 25% |
| Buffer sizing | Three `B` values, felt latency, plot with lines, a clear statement of the trade-off | Values present, plot or trade-off missing | Buffer chosen from the mean or SD | 20% |
| Real connection | Five or more minutes, all statistics, burst length, a recommendation that says how much data it rests on | Data collected but recommendation vague | No real measurement | 20% |
| Writing | Plain, numbers with units, one idea per paragraph | Mostly clear | Hard to follow | 10% |
