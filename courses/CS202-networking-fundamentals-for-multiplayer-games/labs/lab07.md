# CS202 · Lab 07: A snapshot codec

**Week:** 7 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Build the delta encoder and decoder from the [week 7 lecture](../lectures/w07-snapshots-and-delta-compression.md), reproduce its size tables, and show with a seeded simulation why a delta must be encoded against the last *acknowledged* snapshot. Then shrink the format with quantization and a full-snapshot fallback, and measure what each change buys. You finish with a codec you can defend in bytes per second and in correctness under loss.

## Starter materials

Folder [`lab07-starter/`](lab07-starter/README.md). Standard library Python only.

- `snapcodec.py`: the entity format (`x`, `y` as 32-bit floats, `yaw` 16 bits, `hp` and `anim` 8 bits each), `encode_full`, `decode`, the arena generator, the network simulation and a `--check` mode. You write `encode_delta` and `apply_delta`.
- Your [Lab 05](lab05.md) quantization functions, for step 5.

## Steps

1. **Predict first.** Before writing code, compute by hand the full snapshot for 64 entities and the delta for 16 moving players plus one changed prop. Write both numbers down.
2. **Implement the codec.** Write `encode_delta` and `apply_delta` following their docstrings. Unchanged entities are not written. Changed fields carry absolute values. Run `python snapcodec.py --check` until it prints `all checks passed`.
3. **Baseline policies.** Run `python snapcodec.py --sim` with `--loss 0`, `0.01`, `0.05` and `0.2`, seed 1. Put the results in a table like the lecture's and confirm they match. Then run seeds 2 to 6 at 5% loss and report the mean and range of "client wrong" for each policy.
4. **Find the stale entities.** Add a few lines to `simulate` that, for the "sent" policy, record which entity ids are wrong at the end of the run. Show that they are props, not players, and explain why in two sentences using the word "absolute".
5. **Quantize.** Write `encode_delta_q` and `apply_delta_q`, a second format where `x` and `y` are 16-bit unsigned integers covering 0 to 256 m (about 4 mm per step; players in the simulation reach x = 165 m). Round-trip every entity and report the largest position error. Measure the delta for 16 moving players plus one prop, and the mean bytes per snapshot from the simulation. Compare with the lecture's estimate in section 3.
6. **Fall back to full.** Make the encoder compute both a delta and a full snapshot and send the smaller one. Write a test in which all 64 entities change every field (the lecture's 970-byte case) and show that the encoder sends 906 bytes.
7. **Budget.** Using your numbers, compute a 16-player server's upload at 20 Hz for full snapshots, the week 7 delta and your quantized delta, including 28 bytes of header per packet. Express each in Mbit/s.

## Deliverable

Your `snapcodec.py` with the two TODOs, the quantized format, the fallback and its test. The tables from steps 3, 5 and 7, the stale-entity list from step 4 and its explanation, and a half-page note recommending a baseline policy and a format for a 16-player arena game, with the numbers that support it. Submit before the week 8 lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Codec | `--check` passes; code follows the format exactly; hand predictions from step 1 match | Passes with unclear code, or predictions missing | Fails the check | 25% |
| Baseline experiment | Table matches the lecture; five extra seeds with mean and range; correct conclusion | One seed only, or conclusion vague | Missing or wrong | 20% |
| Stale-entity analysis | Wrong entities listed and identified as rarely changing props; mechanism explained with absolute values | List present, explanation thin | Missing | 15% |
| Quantization and fallback | Both work with tests; position error reported and within one step; savings measured | One of the two, or untested | Missing | 20% |
| Budget and recommendation | Three upload figures correct; recommendation follows from them and names the trade-off | Figures present, reasoning thin | Opinion without numbers | 20% |
