# AU101 · Adaptive music brief

**Weight:** 30% of the course grade.
**Assigned:** week 7. **Milestone:** end of week 8. **Final submission:** end of week 10.
**Work mode:** individual.
**Lectures:** [week 6, parameters, crossfades and seek](../lectures/w06-middleware-events-and-parameters.md), [week 8, vertical layering](../lectures/w08-adaptive-music-vertical-layering.md) and [week 9, horizontal re-sequencing and stingers](../lectures/w09-horizontal-re-sequencing-and-stingers.md). Week 10's [ducking](../lectures/w10-mixing-ducking-and-priority.md) helps with the loudness decision.
**Labs that feed it:** [06](../labs/lab06.md) (parameters and seek speeds), [08](../labs/lab08.md) (the layered half) and [09](../labs/lab09.md) (the horizontal half).

## What this component is for

This assessment covers the second course outcome: build adaptive music with layers and transitions. You score one encounter from the game slice you chose for the [SFX pack](sfx-pack-brief.md), so that the music follows what happens: it thickens as the fight grows, moves to a new section when the situation changes, marks key events with stingers, and never lands a switch in the middle of a beat.

This is not a composition course. Most of the marks go to the adaptive system: the intensity mapping, the stem thresholds and fade rates, the transition matrix, the waits it produces, and how well all of it fits the encounter. Composition and mix quality carry 10 of the 100 points, so a simple, well-built score beats an ambitious one that drifts out of time.

## The encounter

Pick one encounter in your slice that lasts 2 to 4 minutes and has at least four musical situations. A few examples follow.

- **A dungeon room.** Explore, enemies alerted, combat, a mini-boss phase, victory, and death.
- **A stealth section.** Sneaking, suspicious guard, full alert, search, and escape.
- **A town under attack.** Calm town, warning bells, siege wave, lull between waves, and the last wave.

Write it as a timeline of game events with times, the way lab 09's `DEMO` and `RAID` lists are written. This scripted playthrough is what you record and what the markers use to check your waits.

## Music sources and licences

The music must be yours or properly licensed, and you must say which parts are which in `LICENSES.md`.

- **Your own composition** at any skill level, played, programmed or recorded by you. Short loops are fine.
- **Procedural stems** from your lab 08 renderer, changed to your own patterns, tempo and key.
- **Your own arrangement of a public-domain melody.** The melody must be out of copyright (for example a folk tune or a composition whose composer died long ago), and the arrangement and recording must be yours. Existing recordings of it are not.
- **Third-party stems** under CC0, or CC-BY with credit, that allow changes. They may make up at most half of your stems, and you must write the transitions, bridges and stingers yourself.

Do not use commercial music, game soundtracks, stems ripped from games, or loops from packs whose licence does not let you submit the source files for marking. Audio from a generator tool counts as third-party and needs the same record. Undeclared third-party material is handled under the academic integrity policy.

## What you build

### Vertical layering (week 8, lab 08)

- At least one music state is built from **at least four stems**, one of them the bed, all sharing one tempo, one key and one loop length (or lengths that divide it evenly), cut to the same sample.
- One **intensity** value from 0 to 1 drives the stems through clamped ramps with thresholds `a_i` and width `w`.
- Intensity comes from game values through a formula you write down (in the style of the lecture's `0.2 · enemies + 0.4 · (1 − health)`), smoothed with separate up and down rates.
- A written **loudness decision**: the level growth from bed to full intensity in dB, and whether you keep it, trim the stems, or duck the music under effects.
- At least one stem is **replaced** rather than added (for example a calm melody giving way to a combat melody), with the crossfade curve chosen for the material (equal-power for different recordings, linear for identical aligned ones).

### Horizontal re-sequencing and stingers (week 9, lab 09)

- At least **four music states**, switched by a director that follows the three rules from the lecture: a request sets a pending switch at the next sync point, a newer request replaces it, and a request for the current state cancels it.
- A **transition matrix** with an explicit sync unit for every transition the encounter can produce, and a bridge segment on at least one of them.
- At least **two stingers**, each quantized to the beat, with a cooldown. At least one is pitched, with a harmony plan: unpitched, one variant per chord, or common tones checked by ear.

### Implementation

Build it in one of these:

- **FMOD Studio 2.03** (recommended): a parameter for intensity with automation curves on each stem and a seek modulator, transition markers or regions with quantization for the states, and stingers as quantized instruments. You may drive it from your SFX pack scene or from FMOD Studio's own parameter controls.
- **Wwise**, with the equivalent RTPC, states and music transitions.
- **Your lab 08 and lab 09 code**, extended to render the whole scripted encounter to one WAV file, with the director's log and the smoothed intensity written to CSV every 0.1 s.

Whichever you choose, the recording must show the intensity value and the current state while the music plays.

## Deliverables

- The project (FMOD or Wwise project folder, or your Python code), zipped, with a `README.md` that says how to reproduce the recording.
- `stems/`: every stem, segment, bridge and stinger as WAV, 48 kHz.
- `encounter.csv`: the scripted game events with times.
- A recording of 2 to 4 minutes of the scripted encounter with the intensity value and state on screen (a screen capture), or the rendered WAV plus a plot of intensity and state against time (code route).
- The director's log, or the middleware profiler capture, for the recorded run.
- `MUSIC_DESIGN.md`, 1,500 to 2,000 words, with these sections:
  1. **The encounter** in three sentences, and what the music must tell the player.
  2. **The intensity mapping**: the formula, three typical situations with their `x`, and a check that it matches the pacing you want. Say where it fails, as the lecture's low-health example does.
  3. **The stems**: a table with each stem, threshold, width and frequency range; the levels at three intensities; the smoothing rates with the rise and fall times they give; and the loudness decision with its dB figure.
  4. **Every reachable mix**: list the stem combinations the mapping can produce and confirm you listened to each.
  5. **The transition matrix** as a table, with a wait table (average and worst case for each unit at your tempo) and one sentence per transition on why its unit suits the event.
  6. **Stingers**: when each fires, its quantization and cooldown, and its harmony plan.
  7. **The log against the design**: for each state event in `encounter.csv`, the request time, the switch time and the wait. Point out any wait longer than the event deserves and say what you did about it.
  8. **What you would change** with another week.
- `LICENSES.md`.

## Milestone: the layered half (end of week 8, 15 points)

Submit your stems for the layered state (at least four), the intensity formula, the thresholds, width and rates, and a 60-second render or recording with the intensity driven through its whole range and back. Include a table of stem gains and the level at four intensities, computed with your lab 08 functions. Feedback comes back within a week and focuses on whether the stems stay in time and whether the rise and fall times suit the encounter.

## Rubric

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| Milestone | 13 to 15: four or more stems in time; mapping, thresholds and rates stated; gain table computed and correct | 9 to 12: one element missing or a stem drifts | 4 to 8: stems or numbers largely missing | 0 to 3 | 15 |
| Vertical layering | 18 to 20: stems share one clock and never restart; entries are heard one at a time; every reachable mix sounds finished; loudness decision argued with a dB figure; the replaced stem uses the right crossfade curve | 13 to 17: one of those weak | 7 to 12: layering works but drifts, clicks or piles up | 0 to 6 | 20 |
| Intensity mapping and smoothing | 9 to 10: formula from named game values; asymmetric rates justified with rise and fall times; failure case found and handled | 6 to 8: mapping works, reasons generic | 3 to 5: intensity scripted by hand, no mapping | 0 to 2 | 10 |
| Horizontal transitions | 18 to 20: four or more states; every reachable transition has an explicit unit; waits tabled and matched by the log; replace and cancel rules visible in the log; one bridge that fits | 13 to 17: one transition left to a default or one wait too long | 7 to 12: switches land off the beat or states flicker | 0 to 6 | 20 |
| Stingers | 9 to 10: two or more, beat-quantized, with cooldowns; the pitched one fits the harmony under it | 6 to 8: one weak or clashing | 3 to 5: stingers present but unquantized | 0 to 2 | 10 |
| Implementation and recording | 9 to 10: reproducible from the README; intensity and state visible throughout; the recording matches `encounter.csv` | 6 to 8: minor gaps | 3 to 5: recording does not show the system working | 0 to 2 | 10 |
| Composition and mix | 9 to 10: bed complete on its own; stems in separate frequency ranges; identity in the early stems; peaks below full scale at full intensity | 6 to 8: one stem muddy or the bed thin | 3 to 5: clashes or clipping at full intensity | 0 to 2 | 10 |
| Design document | 5: every section present, every choice backed by a number from the lecture models | 3 to 4: one section thin | 1 to 2: several sections missing | 0 | 5 |
| **Total** | | | | | **100** |

The adaptive music mark is the total out of 100, multiplied by 0.30.

## Rules and advice

- **Labs 08 and 09 are the halves.** Lab 08 gives you the layered state and its numbers; lab 09 gives you the director and the matrix. The new work is joining them in one encounter and recording it.
- **Write the matrix before the music.** Decide the states, the units and the stingers on paper, then compose segments that end where the switches will land.
- **One clock.** Most failures in layered music are stems of slightly different lengths. Cut every stem to the same sample count and check it in code.
- **Test the worst case.** Fire the most urgent event just after a sync point and listen to how long the player waits. If it is too long, add a stinger or shorten the unit.
- **Late submission.** Up to 48 hours late, the final is marked out of 68 instead of 85. The milestone cannot be late, but a missed milestone can be shown at the next lab session for half marks.
- **Integrity.** Keep your project history and source files until grades are released. In the week 15 crit you may be asked to open the project and change a threshold or a sync unit live.
