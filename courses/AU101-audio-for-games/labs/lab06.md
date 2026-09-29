# AU101 · Lab 06: An engine event and its contract

**Week:** 6, middleware events and parameters ([lecture](../lectures/w06-middleware-events-and-parameters.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** formative, feeds the adaptive music assignment (30%). The parameter, crossfade and seek techniques come back in that assignment.

## Objective

Build a parameter-driven engine sound in FMOD Studio from procedurally generated loops, and write the event contract that a programmer would code against. A validator checks that your contract keeps the total level flat across the RPM range and never stretches an audible loop more than 6 semitones. Then you make the FMOD event match the contract and prove it by ear.

This lab is mainly a studio brief. The code you run is small and provided. The checkable parts are the validator result and your recording.

## Starter materials

All in [`lab06-starter/`](lab06-starter/). Standard-library Python 3.10 or later. FMOD Studio 2.03 (download with a free FMOD account). Optional for step 9: your lab 05 scene in Unity 6 with the FMOD for Unity integration.

- [`make_loops.py`](lab06-starter/make_loops.py) writes procedural engine loops that repeat without a click. `python make_loops.py 1000 2000 4000` writes `engine_1000.wav`, `engine_2000.wav` and `engine_4000.wav`. Each loop is about 2 seconds, holds a whole number of engine cycles, and prints the exact RPM it represents.
- [`engine_contract.json`](lab06-starter/engine_contract.json) is the starter contract. It uses three loops an octave apart with linear crossfades and still has `TODO` fields.
- [`check_contract.py`](lab06-starter/check_contract.py) validates a contract. Run `python check_contract.py`. On the starter it fails four checks: `complete` (TODOs), `level` (−3.01 dB at 1,500 RPM), `stretch` (a loop pitched +11.07 semitones while still audible) and `seek` (no seek speeds). The docstring at the top explains each check.

## Steps

### Part 1: the contract (in lab)

1. **Run the validator on the starter** and copy its output into your notes. For the `level` failure, show by hand, using lecture section 2, why the linear curves give −3.01 dB at 1,500 RPM.
2. **Fill in the TODOs.** `stop_when` lists every gameplay moment that must stop and release the instance (think about week 5's stuck loop). `bank` names the bank. `owner` names who owns content and curves and who owns the RPM value. `set_by` says which script sets RPM and the formula it uses (the FMOD kart tutorial's `Lerp(minRPM, maxRPM, speed)` is a fine model).
3. **Fix the stretch.** The validator allows at most ±6 semitones on any loop with gain of at least 0.1. Choose new recorded RPMs so that neighbouring loops are close enough. Hint: 6 semitones is a factor of `2^(6/12) ≈ 1.414`. Generate the loops you need with `make_loops.py`.
4. **Fix the level.** Rewrite every gain curve so the total level stays within ±1.5 dB. Curves are straight lines between points, so you need several points per fade to approximate the equal-power shape `cos(t × 90°)` and `sin(t × 90°)`. Work out the smallest number of points per fade that passes, and note it.
5. **Choose seek speeds.** Add `seek_up_range_per_s` and `seek_down_range_per_s`. A full rise must take at most 1.0 s, and falling must be no faster than rising. Write one sentence on why.
6. **Pass.** Run `python check_contract.py` until it prints `contract OK`.

### Part 2: the event (at home)

7. **Build the event in FMOD Studio.** Create the event at the path in your contract. Add a continuous user parameter `RPM` with the contract's range. Add one audio track per loop, each holding a looping single instrument that spans the whole RPM sheet. On each track:
   - automate the instrument's pitch in semitones with `12 × log2(rpm / recorded_rpm)` (set points at every place your gain curve has a point, plus the ends),
   - automate the track volume with your gain curve. FMOD volume is in dB, so convert each point with `20 × log10(gain)`. A gain of 0 is −∞ dB (FMOD's minimum).
   - add a seek modulator to the RPM parameter with your ascending and descending speeds.
8. **Audition and record.** In FMOD Studio, drag the RPM parameter slowly from minimum to maximum and back, and then jump it from maximum to minimum. Record 60 seconds of the output with the parameter visible on screen. Listen for dips, bumps and loops that sound unnaturally squeezed or stretched.
9. **Optional: wire it into the game.** In your lab 05 Unity scene, replace the engine player with a `StudioEventEmitter` for your event and set RPM each frame from speed, as the FMOD for Unity kart tutorial does. Make sure the event instance stops on every `stop_when` case.

## Deliverable

1. Your final `engine_contract.json`, which must print `contract OK` with the provided `check_contract.py`, and the loop WAVs it refers to.
2. The FMOD Studio project folder (zipped), with the event at the contract's path.
3. The 60-second recording from step 8.
4. A note of at most 400 words with: the hand calculation from step 1, the loop spacing you chose in step 3 and why, the number of curve points from step 4, the seek sentence from step 5, and one thing you heard in step 8 that the validator cannot check.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Contract passes | `contract OK`; every field specific (real stop cases, real formula) | Passes but fields vague | Fails any check | 25% |
| Reasoning | Hand calculation correct; loop spacing and point count justified with the model | One part thin | Missing or wrong | 20% |
| FMOD event matches contract | Pitch and volume automation match the contract at every point; seek configured | Minor mismatches | Event does not follow the contract | 25% |
| Listening | Recording shows a flat, natural sweep; note names something audible the validator misses (loop seams, phasing, character change) | Recording fine, note generic | Audible dips or clicks, no note | 20% |
| Lifetime (optional step 9 or written plan) | Every stop case handled and demonstrated | Stop cases listed, some untested | Instance leaks | 10% |
