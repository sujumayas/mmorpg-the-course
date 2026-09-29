# AU101 · Lab 02: Foley session and level check

**Week:** 2, recording and foley basics ([lecture](../lectures/w02-recording-and-foley-basics.md)).
**Time:** 2 hours in lab (code and session plan), a 90-minute recording session in the booth or at home, and up to 1 hour of editing.
**Weight:** formative, feeds the SFX pack (30%). These recordings are your source material for weeks 3 and 4.

## Objective

Write the three level measurements a recording engineer checks after every take, then record a small foley set to a fixed specification and prove it meets the spec with a checker that uses your code.

## Starter materials

All in [`lab02-starter/`](lab02-starter/). Standard-library Python, no installs.

- [`levels.py`](lab02-starter/levels.py) with a working `read_wav` (16-bit and 24-bit PCM), `amplitude_to_dbfs` and `clipped_runs`, and three functions for you to write: `peak_dbfs`, `rms_dbfs` and `noise_floor_dbfs`.
- [`test_levels.py`](lab02-starter/test_levels.py). All 11 tests fail on the starter. They check, among other things, that a sine of amplitude 0.5 peaks at −6.02 dBFS, that a full-scale sine has an RMS of −3.01 dBFS, and that the noise floor of 100 ms at 0.1 followed by 100 ms at 0.001 is −60 dBFS.
- [`check_foley.py`](lab02-starter/check_foley.py), the session checker. It imports your `levels.py` and checks every WAV in a folder against the spec below.
- Recording kit: a booth condenser microphone and interface, or your phone in an uncompressed WAV mode plus Audacity (free) to convert to 48 kHz, 24-bit.

Run the tests from the repository root:

```
.venv/bin/python -m unittest discover courses/AU101-audio-for-games/labs/lab02-starter
```

## The session spec

| Rule | Value |
|---|---|
| Format | WAV, 48,000 Hz, 24-bit PCM |
| Channels | mono for effects; room tone may be mono or stereo |
| Peak level (effects) | between −20 and −1 dBFS; aim for −12 to −6 |
| Clipping | none (3 or more consecutive samples at 0.999 of full scale fails) |
| Room tone | one file, at least 20 seconds, CatID `AMBRoom` |
| Signal-to-noise | every effect's peak at least 40 dB above the room tone floor |
| Names | `CatID_description_initials_NN.wav`, e.g. `FOOTGrvl_boot-walk_AB_03.wav` |
| Count | at least 11 effect files plus the room tone |

CatIDs follow the Universal Category System pattern: four capital letters for the category, then two to five letters for the subcategory. Use `FOOT` for footsteps, `CLTH` for cloth, and pick sensible ones for props (for example `WOODHndl`, `METLImpt`). Descriptions are lowercase with hyphens.

## Steps

1. **Code.** Implement `peak_dbfs`, `rms_dbfs` and `noise_floor_dbfs` until all tests pass.
2. **Plan.** Write a shot list of 11 or more effects: two footstep surfaces with at least three takes each, one cloth movement, and three props. For each, note the microphone distance you will use and the character or object it is for.
3. **Soundcheck.** Record one take per prop at your planned distance. Adjust gain (or distance) until peaks land between −12 and −6 dBFS. Write the settings down.
4. **Record.** Record at least five takes per action. Slate each file verbally. Record 30 seconds of room tone with everyone still, before you pack up.
5. **Edit.** Trim each chosen take to the sound plus a short tail. Remove the slate. Do not normalise or compress yet; the checker is measuring your recording, not your processing. Export to the spec.
6. **Check.** Run `check_foley.py` on your folder. Fix anything that fails by re-recording or re-exporting, not by bending the rules.
7. **Distance experiment.** Record one prop at two distances, one double the other, with the same gain. Measure both peaks with your `peak_dbfs` and compare the difference with the 6 dB the inverse-square rule predicts.

```
.venv/bin/python courses/AU101-audio-for-games/labs/lab02-starter/check_foley.py my_session/
```

## Deliverable

1. Your `levels.py` with all tests passing.
2. The folder of 12 or more WAV files, passing the checker, plus the checker's printout.
3. A one-page session report: shot list with distances and gain settings, the room tone floor, the distance experiment (both peaks, the measured difference, and one reason it differs from 6 dB), and the two takes you are proudest of and why.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Level functions | All 11 tests pass; code is short and readable | Tests pass with awkward code | Tests fail | 20% |
| Spec compliance | Checker passes with no manual edits to the checker | One or two files fail with a stated reason | Many failures | 25% |
| Recording quality | Clean takes, consistent distance, no audible room or handling noise | Minor noise or level jumps between takes | Noisy, clipped or inconsistent | 25% |
| Distance experiment | Both peaks measured, gap from 6 dB explained with a physical reason | Measured without explanation | Missing | 15% |
| Session report | Shot list, settings and choices clear enough to repeat the session | Partial | Missing | 15% |
