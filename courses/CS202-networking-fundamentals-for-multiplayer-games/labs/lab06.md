# CS202 · Lab 06: Acks and copies

**Week:** 6 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Build the pieces of a reliability layer from the [week 6 lecture](../lectures/w06-reliability-over-udp.md). You write wraparound-safe sequence numbers, an ack header that confirms 33 packets, and a redundant-input scheme. Check the lecture's loss formulas against an hour of simulated packets, then choose the number of copies your own connection needs. You finish with a delivery-class table for a game of your own, backed by numbers.

## Starter materials

Folder [`lab06-starter/`](lab06-starter/README.md). Standard library Python only. Use the course interpreter (`.venv/bin/python` at the repository root) or any Python 3.10 or later.

- `reliability.py`: the 8-byte header format, the week 2 bursty loss generator (`loss_pattern`, written), report code and `--check`. You write `seq_greater_than`, `AckTracker.on_receive`, `AckTracker.ack_fields`, `acked_by`, `p_input_lost` and `simulate_redundancy`.
- Your Lab 02 log, or `sample_run.csv` from [Lab 02's starter](lab02-starter/README.md), for step 6.

## Steps

1. **Wraparound.** Implement `seq_greater_than`. Before running anything, predict by hand the results for (2, 65534), (65534, 2), (40000, 5000) and (32768, 0). Explain the last one in a sentence.
2. **Acks.** Implement `AckTracker` and `acked_by`. Reproduce the lecture's trace (received 65,533, 65,534, 0, 1, 3 gives `ack = 3` and `ack_bits = 0b110110`). Run `python reliability.py --check` until it prints `all checks passed`.
3. **Formulas.** Implement `p_input_lost` and `simulate_redundancy`. Run `python reliability.py --table` and confirm it matches the loss table in section 2 of the lecture (the program prints extra rows).
4. **Simulate an hour.** Run `--sim` for `p = 0.05` with `k` from 1 to 4, independent and with `q = 0.5`. Put the eight results next to the formula values in one table. With the default seed, `k = 3` must give 23 (independent) and 2,702 (bursty).
5. **Chance or bug?** Run the independent `k = 3` case with seeds 1 to 20. Report the mean and the smallest and largest counts. Is 23 against a formula of 27 a bug or chance? Use the spread you measured to argue it.
6. **Your connection.** From your Lab 02 log, measure the loss rate `p` and estimate `q` as (number of losses that follow a loss) divided by (number of losses). Find the smallest `k` that keeps lost inputs below 10 per hour at 60 inputs per second, by formula and by simulation with your `p` and `q`. Report the upload cost at that `k`.
7. **Spread the copies.** Add a function `simulate_spaced(lost, k, gap)` that sends input `i` in packets `i, i + gap, i + 2 gap, ...`. With `p = 0.05`, `q = 0.5` and `k = 3`, compare `gap = 1`, 2 and 3. Explain the result with the mean burst length `1/(1 − q)`, and state the extra delay each gap costs a rescued input at 60 Hz.
8. **Delivery classes.** For the game you used in Lab 04 or Lab 05, list at least eight message types. Give each a class (unreliable, sequenced, redundant with `k`, reliable ordered on a named channel), and for the reliable ones, the delay after one loss at your measured RTT.

## Deliverable

Your finished `reliability.py` with `simulate_spaced`, and one Markdown or PDF file with the step 1 predictions, the outputs and tables from steps 3 to 7, the argument in step 5, and the delivery-class table from step 8. Submit before next week's lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Sequence and acks | `--check` passes; predictions right, including the half-circle case explained | Passes, predictions or explanation missing | Fails the check | 20% |
| Formulas vs simulation | All eight cases tabled next to formulas; the step 5 argument uses the measured spread | Table complete, argument vague | Simulation not run or not compared | 20% |
| Your connection | `p` and `q` measured from a real log with the method shown; `k` found by formula and simulation; upload stated | `k` found one way only | Numbers assumed, not measured | 20% |
| Spaced copies | Function correct; three gaps compared; result explained with burst length and delay | Results given without explanation | Missing | 15% |
| Delivery classes | Every message classed with a reason; channels chosen to avoid head-of-line stalls; resend delays computed | Classes sensible, delays or channels missing | Everything reliable, or everything unreliable, without argument | 25% |
