# CS202 · Lab 05: 108 bits

**Week:** 5 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Build the serialization tools from the [week 5 lecture](../lectures/w05-serialization-and-bit-packing.md). You write bit counting, quantization, a bit writer and a bit reader that survives hostile input. Pack the lecture's player state into 14 bytes, then design and justify a packed state for an entity from your own game. You finish able to predict a packet's size before writing the code, and to show that your reader cannot be crashed by random bytes.

## Starter materials

Folder [`lab05-starter/`](lab05-starter/README.md). Standard library Python only. Use the course interpreter (`.venv/bin/python` at the repository root) or any Python 3.10 or later.

- `bitpack.py`: `FIELDS` (the lecture's player state), `SAMPLE` values, the naive `struct` layout, a fuzzer and a `--check` mode. You write `bits_for_count`, `steps`, `quantize`, `BitWriter.write`, `BitReader.read`, `pack_state` and `unpack_state`.
- Your Lab 03 `topology.py` for the bandwidth comparison in step 6.

## Steps

1. **Count bits.** Implement `bits_for_count` and `steps`. Before running anything, predict by hand the bits for x, z and yaw (wrapping and not wrapping). Then check your predictions.
2. **Quantize.** Implement `quantize` with clamping and wrapping. Write down one value where clamping changes the result and one where wrapping does.
3. **Bits in, bits out.** Implement `BitWriter.write` and `BitReader.read`. Reproduce the lecture's hand trace (5 in 3 bits, 1 in 1 bit, 300 in 9 bits gives `0xCD 0x12`). Run `python bitpack.py --check` until it prints `all checks passed`.
4. **Pack the player.** Implement `pack_state` and `unpack_state`. Run `python bitpack.py --demo`. It must report 108 bits in 14 bytes. For every field, confirm the round-trip error is no larger than half the precision.
5. **Fuzz.** Run `python bitpack.py --fuzz 10000`. Every packet must either decode or raise `ReadError`. If anything else is raised, fix the reader and record what the bug was. Then answer this. About 3% of random packets decode successfully. Why is that not a security problem by itself, and what does week 4 say the server must still do with a decoded state from a client?
6. **What it saves.** Using your Lab 03 functions, compute the dedicated server's upload for 8, 64 and 100 players at 20 Hz with `s = 44` and `s = 14`. Confirm the 64-player figures in the lecture (29,123 and 9,462 kbit/s).
7. **Your entity.** Pick one networked entity from a game you would like to build (a player in an open-world MMO, a vehicle, an RTS unit, a projectile). List 8 to 15 fields. For each, choose a range and precision, name who reads it (renderer, hit detection, UI, game rules) and say whether it wraps. Add the entity to `bitpack.py` as a second field list, pack a sample, and report bits, bytes and the naive size.
8. **Too coarse.** Choose one field of your entity and halve its bits. Describe in two sentences what a player would see, using the largest-error number.

## Deliverable

Your finished `bitpack.py` with your entity added, and one Markdown or PDF file with the predictions from step 1, the values from step 2, the outputs of steps 3 to 6, the fuzz answer, your entity's field table with justifications, and the step 8 description. Submit before next week's lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Bit tools | `--check` passes; writer rejects values that do not fit; hand predictions match | Passes, predictions missing or wrong | Fails the check | 25% |
| Round trip and fuzz | 108 bits in 14 bytes; every field's error within `p/2`; fuzz clean with any bug found described | Round trip works, fuzz run but bugs not explained | Fuzz crashes or not run | 20% |
| Bandwidth comparison | All six upload figures correct and the 64-player row matches the lecture | Minor arithmetic slips | Missing | 10% |
| Your entity | Every field has range, precision, reader and wrap decision with a reason; packed and measured in code | Table complete, justifications thin | Floats and 32-bit integers copied without thought | 30% |
| Too-coarse analysis | Uses the largest-error number and ties it to something a player sees | Plausible but not numeric | Missing | 15% |
