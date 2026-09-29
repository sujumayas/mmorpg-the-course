# AU101 · Lab 05: Trigger timing

**Week:** 5, implementation in engine ([lecture](../lectures/w05-implementation-in-engine.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home for Part 2.
**Weight:** formative, feeds the SFX pack (30%). Part 2's scene is reused in lab 06, where the same triggers call middleware events instead of engine players.

## Objective

Compute, hear and fix the frame-grid timing problem from lecture section 2. Then wire a repeating one-shot and a loop into an engine scene, test it at two frame rates, and show that the scheduled version keeps time.

## Starter materials

All in [`lab05-starter/`](lab05-starter/). Standard-library Python 3.10 or later for Part 1. Godot 4 (standard build) or Unity 6 for Part 2.

- [`timing.py`](lab05-starter/timing.py) has four parts. Part A holds the three trigger strategies (`reset_times`, `carry_times`, `audio_clock_times`) and `snap_to_chunks`, which models a mixer that starts sounds only at chunk boundaries. Part B holds three measuring functions (`gaps_ms`, `average_rpm`, `worst_error_ms`). Part C holds `distance_steps`, the footstep accumulator from lecture section 3. Part D is provided and renders click tracks to WAV.
- [`test_lab05.py`](lab05-starter/test_lab05.py) has seven tests. Run `python test_lab05.py`. On the starter it reports `0/7 tests passed`.

Every time in `timing.py` is a `fractions.Fraction` of a second. One test checks the float trap from the lecture (shot 3 of a 600 rpm gun at 30 fps), and a float version of `carry_times` fails it.

## Steps

### Part 1: the model (in lab)

1. **Strategies.** Implement Part A. Use `math.ceil` on Fractions, which returns an exact integer. Run the tests after each function.
2. **Measuring.** Implement Part B. `average_rpm` divides the number of gaps by the span from first to last shot. The carry cooldown over 16 shots at 60 fps gives 794 rpm, not 800. Write one sentence in your notes explaining why the short-burst average is below the long-run rate.
3. **Footsteps.** Implement Part C. The test also checks that a character who stops walking stops stepping.
4. **Listen.** Run `python timing.py`. It renders 24 shots of an 800 rpm weapon three ways at 30 fps: `reset_30fps.wav`, `carry_30fps.wav` and `audio_clock.wav`. Listen on headphones. Describe each in one sentence, and say which one you'd accept in a shipped game.
5. **Fill the table.** Using your functions, fill in the table below for 800 rpm (16 shots). For "chunks", apply `snap_to_chunks` with 512 samples after the strategy.

| Frame rate | Reset rpm | Reset + chunks: min / max gap | Carry rpm | Carry + chunks: min / max gap | Audio clock: min / max gap |
|---|---|---|---|---|---|
| 30 | | | | | |
| 60 | | | | | |
| 144 | | | | | |

### Part 2: in the engine (at home)

6. **Build the scene.** In Godot 4 or Unity 6, make a scene with a "weapon" that fires while a key is held, at 800 rpm, playing a short click or one of your week 4 sounds. Implement the reset cooldown first, exactly as in the lecture.
7. **Test at two frame rates.** Cap the frame rate at 60 and then at 144. In Godot set `Engine.max_fps` and turn V-Sync off in the project settings. In Unity set `QualitySettings.vSyncCount = 0` and `Application.targetFrameRate`. Hold the key for 3 seconds, count the shots (print a counter), and compute the rate. Compare with your table.
8. **Fix it.** Change the gameplay cooldown to carry. Then schedule the sounds on the audio clock. In Unity use `AudioSource.PlayScheduled` with `AudioSettings.dspTime`, playing the first shot at once and scheduling the rest from it, and keep a list of scheduled sources so you can stop them on release. In Godot 4, `play()` starts at the next mix chunk, so the practical fix is to render the burst's rhythm into a looping stream, or to drive a stream that you fill yourself with `AudioStreamGenerator`. Pick one and explain the choice in two sentences.
9. **A loop with a clean exit.** Add a looping "burning" sound that starts when a state is entered and stops when it is left. Test three exits: leaving normally, the object being freed while burning, and a scene change. None of them may leave the loop playing.

## Deliverable

1. Your `timing.py` with `python test_lab05.py` reporting `7/7 tests passed`, and the three WAV files.
2. The completed table from step 5.
3. A 60 to 90 second screen capture with audio from Part 2 showing: the reset version at 60 and 144 fps with the shot counter, the fixed version at both rates, and the three loop exits.
4. A note of at most 350 words covering steps 2, 4, 7 and 8.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 7/7 | 5-6 | 4 or fewer | 25% |
| Table and explanation | All 15 cells correct; the 794 rpm effect explained with the model | Minor errors, explanation present | Many errors or missing | 20% |
| Engine rate test | Measured rates within one shot of the model at both frame rates, and the discrepancy explained | Measured at one rate only, or unexplained differences | No measurement | 20% |
| Fix quality | First shot immediate, rest exact, release stops scheduled shots, choice justified | Rhythm fixed but release or first shot wrong | Not fixed | 20% |
| Loop exits | All three exits silent | Two of three | Loop sticks in common cases | 15% |
