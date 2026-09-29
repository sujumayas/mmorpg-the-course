# AU101 · SFX pack brief

**Weight:** 30% of the course grade.
**Assigned:** week 1. **Milestone 1:** end of week 4. **Milestone 2:** end of week 7. **Final submission:** end of week 12.
**Work mode:** individual.
**Lectures:** [week 1, the three jobs of sound](../lectures/w01-what-sound-does-feedback-space-emotion.md), [week 2, recording and foley](../lectures/w02-recording-and-foley-basics.md), [week 3, synthesis](../lectures/w03-synthesis-for-sfx.md), [week 4, layering and variation](../lectures/w04-layering-and-variation.md), [week 5, implementation](../lectures/w05-implementation-in-engine.md), [week 7, attenuation](../lectures/w07-spatial-audio-and-attenuation.md) and [week 11, UI sound](../lectures/w11-ui-sound-design.md).
**Labs that feed it:** [01](../labs/lab01.md), [02](../labs/lab02.md), [03](../labs/lab03.md), [04](../labs/lab04.md), [05](../labs/lab05.md), [07](../labs/lab07.md) and [11](../labs/lab11.md).

## What this component is for

This assessment covers the first course outcome: design and implement SFX that communicate game state. Most of the pack is lab work you have already started, finished to one standard and wired into a game. A sound that "sounds cool" earns little on its own. A sound that does a job you can name, varies where repetition would hurt and stays fixed where it is a signal, sits at a level you planned, and plays at the right moment in an engine earns a lot.

## Your game slice

Pick one small game slice now and keep it for the whole course. The same slice carries into the [adaptive music](adaptive-music-brief.md) assignment and the [final sound pass](final-sound-pass-brief.md). Good choices:

- your own game from another course, such as the [CS101 final arcade game](../../CS101-programming-for-games-i/assessments/final-arcade-game-brief.md);
- the sample slice the instructor provides in week 1 (a small top-down dungeon room with a player, two enemy types, a door, a pickup and an inventory screen);
- an open-source game whose licence lets you change its audio and share the result for marking. Name the licence in your slice description.

Write a slice description of about 150 words: genre, camera, what the player does, what threatens them, which screens have UI, and where the listener sits.

## Audio sources and licences

Every sound in the pack must be yours or properly licensed. This is a gate. A pack with undeclared third-party audio is not marked until the record is complete, and material presented as your own work when it is not is handled under the academic integrity policy.

- **Allowed without limit:** sounds you recorded yourself, and sounds you synthesised yourself (your lab 03 and lab 11 code, sfxr-style tools, a synthesiser plugin).
- **Allowed with a record:** third-party recordings under CC0, or under CC-BY with credit, used as **layers** that you edited, layered or processed. At most a quarter of the pack's files may contain third-party material, and none may be a whole third-party sound submitted unchanged. Audio from a generator tool counts as third-party material: check the tool's terms give you the rights, and record it the same way.
- **Not allowed:** audio ripped from games, films, streams or music; sample packs or commercial libraries whose licence does not let you submit the source files for marking; anything with no clear licence. Ask before the deadline if you are unsure, not after.
- **People.** If someone else performs foley or voice for you, get their written agreement to use the recording in coursework and keep it with your submission.

Keep `LICENSES.md` from week 1 on, with one row per third-party file: your file name, source, author, URL, licence, and what you changed. Write "none" if the pack has no third-party material.

## What you build

The pack is at least 20 sound events for your slice. An **event** is one thing the game can ask for, and it may play one of several files.

1. **Footsteps (from lab 02).** The player on two surfaces, at least 4 variants each, from your own recordings. Give each set a pick rule and pitch and volume ranges, and compute `R` and the chance of an exact repeat over 8 steps.
2. **One layered hero action (from lab 04 Part 2).** The most frequent action in your slice (an attack, a shot, a spell, a pickaxe strike), built from three layers with one job each (transient, body, tail) and 3 or 4 variants per layer. State `R` and the burst repeat chance for the longest realistic burst.
3. **Six synthesised sounds (from lab 03).** Six events of your slice, each written as its six numbers. Every pitch contour must match the meaning of its event, or break the rule on purpose with the reason written down.
4. **Three information sounds (from lab 01).** Redesign the three mute-cost-3 sounds you picked in your audit. Either design them as replacements for the audited game or carry the same job into your slice. For each, state the job, what was wrong with the original, and the visual twin a muted player would get.
5. **A UI family (from lab 11).** Eight UI sounds with written meaning rules, lengths and peaks set from a repetition budget, and one streak ladder with its scale, cap or wrap choice and `T_reset`.
6. **Two loops.** One stereo ambience bed, and one gameplay loop tied to a state (burning, charging, an engine, a shield). Both loop without a click.

### Technical specification

| Rule | Value |
|---|---|
| Format | WAV, 48,000 Hz, 16- or 24-bit PCM. Keep higher-rate source recordings in your archive, not in the pack. |
| Channels | Mono for every point source the engine positions. Stereo only for the ambience bed and for UI sounds where you justify it. |
| Peaks | At most −1 dBFS; no clipping (three or more consecutive samples at 0.999 of full scale, as in lab 02). |
| Relative levels | UI peaks follow your week 11 repetition budget. Every other event has a planned peak in the sheet, and the file matches it within 1 dB. |
| Names | `CatID_description_initials_NN.wav`, as in lab 02. |
| 3D events | A curve, `r` and `R` from your lab 07 table, with one sentence tying the range to a gameplay distance. |
| Loops | Loop points at zero crossings or with a short crossfade; no click when looped ten times. |

### Implementation

The pack must play in a small scene in Godot 4 or Unity 6, with or without FMOD Studio. Reuse your lab 05 scene.

- Gameplay triggers every event it can. Add a test panel (a key per event) for the rest.
- Footsteps use the distance method or animation events, not a timer (week 5).
- The hero action keeps its rhythm at 60 and 144 fps. State which trigger strategy you used.
- Variation runs as the sheet says: the same pools, pick rules and ranges.
- The gameplay loop starts when its state is entered and stops on every exit, including the object being freed and a scene change.
- 3D events use the attenuation settings from the sheet. Say where the listener sits and why.
- Polyphony is set per event on purpose: how many copies may overlap, and what happens to the oldest.

## Deliverables

- `pack/`: every WAV file in the pack, named to the specification.
- `sfx_sheet.csv` with one row per event and these columns: `event`, `files`, `job`, `feedback_kind`, `trigger`, `variants`, `pick_rule`, `pitch_range_st`, `volume_range_db`, `R`, `planned_peak_dbfs`, `measured_peak_dbfs`, `length_ms`, `curve`, `ref_m`, `max_m`, `bus`, `max_polyphony`. Measure peaks with your lab 02 `peak_dbfs`.
- The engine project, zipped, with a `README.md` that says how to open it and run the scene.
- A screen capture of 2 to 3 minutes, with audio, showing every event at least once: a burst of the hero action, footsteps on both surfaces, both loops starting and stopping (including one abnormal exit), the UI family and one streak with a reset. Put the event name on screen as it plays (the debug overlay or a caption is fine).
- `DESIGN.md`, 1,200 to 1,800 words, with these sections: the slice and its sound jobs; variation decisions, including which events do not vary and why, with `R` and burst figures; the three redesigns, before and after; the UI meaning rules and your lab 11 blind-test results; the attenuation choices; and one thing you would change with another week.
- `LICENSES.md`, as above.

## Milestone 1: sources and first designs (end of week 4, 10 points)

Submit the slice description, your event list with the job of each event, the lab 02 recording folder with its checker printout, the six lab 03 sounds with their parameter table, and the lab 04 layered sound with its variation table. Feedback comes back within a week and focuses on whether each event has a clear job and whether your source recordings are clean enough to build on.

## Milestone 2: in the engine (end of week 7, 10 points)

A 5-minute demo in the lab session. The scene runs, footsteps play on both surfaces from the distance or animation trigger, the hero action fires at 60 and 144 fps without drift, and the gameplay loop survives all three exits. Bring your lab 07 attenuation table for every 3D event in the pack and the measured peaks of every file so far.

## Rubric

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| Milestone 1 | 9 to 10: every event has a named job; recordings pass the checker; synth and layered drafts with tables | 6 to 8: one part thin | 2 to 5: event list or recordings missing | 0 to 1 | 10 |
| Milestone 2 | 9 to 10: all four demo checks pass; attenuation table and peaks complete | 6 to 8: one check fails | 2 to 5: scene runs, most checks fail | 0 to 1 | 10 |
| Communicates game state | 14 to 15: every event does its stated job; forecasts arrive early enough to act on; the three redesigns fix a named problem and each has a visual twin | 10 to 13: one or two events vague | 5 to 9: jobs stated but sounds do not deliver them | 0 to 4 | 15 |
| Craft | 14 to 15: clean recordings with consistent distance; synth contours match meaning; layers have separate bands and jobs, no phase holes; loops seamless | 10 to 13: minor noise, a weak layer or a small click | 5 to 9: audible noise, clipping or muddy layers | 0 to 4 | 15 |
| Variation and repetition | 11 to 12: pools, rules and ranges chosen from `R` and burst figures; signal sounds kept fixed on purpose; no exact repeat audible in the capture | 8 to 10: correct numbers, thin reasons | 4 to 7: variation present but untested, or on a signal sound | 0 to 3 | 12 |
| Levels and specification | 7 to 8: every file within 1 dB of its planned peak; format, channels and names to spec | 5 to 6: two or three files off | 2 to 4: many files off spec | 0 to 1 | 8 |
| Implementation | 11 to 12: triggers correct at both frame rates; loops exit cleanly in every case; attenuation and polyphony match the sheet | 8 to 10: one behaviour wrong | 4 to 7: several events hard-wired or stuck | 0 to 3 | 12 |
| UI family | 9 to 10: meaning rules followed by all eight sounds; lengths and peaks from the repetition budget; ladder choices justified; blind test shows the fix worked | 6 to 8: one rule broken or the retest missing | 3 to 5: sounds present, rules or budget missing | 0 to 2 | 10 |
| Sheet and design note | 7 to 8: sheet complete and matches the files; every decision in `DESIGN.md` has a number or a mechanism behind it | 5 to 6: gaps in the sheet or generic reasons | 2 to 4: sheet or note largely missing | 0 to 1 | 8 |
| **Total** | | | | | **100** |

The SFX pack mark is the total out of 100, multiplied by 0.30.

## Rules and advice

- **Your labs are the parts.** Labs 01 to 04, 07 and 11 each produce a piece of this pack. The new work is making the pieces sound like one game and play in one scene.
- **Name the job first.** Before you design any event, write its job and feedback kind in the sheet. If you cannot, the sound probably does not need to exist.
- **Measure, then listen, then measure again.** Peaks come from your code, repeat chances from the model, and the final call from your ears on headphones.
- **Late submission.** Up to 48 hours late, the final is marked out of 64 instead of 80. Milestones cannot be late, but a missed milestone can be shown at the next lab session for half marks.
- **Integrity.** Every file must be traceable to your own recording or synthesis, or to a row in `LICENSES.md`. Keep your session folders and synth parameter files until grades are released; markers may ask for them.
