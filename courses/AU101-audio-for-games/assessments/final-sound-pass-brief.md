# AU101 · Final sound pass brief

**Weight:** 40% of the course grade.
**Assigned:** week 10. **Milestone 1:** end of week 12. **Milestone 2:** end of week 14. **Final submission:** start of week 15, followed by a 15-minute crit in week 15.
**Work mode:** individual. A pair may share one slice only if each partner owns separate systems (for example one owns the mix and music integration, the other the SFX and accessibility), with a contribution statement. Each partner is marked on their own systems and answers crit questions alone.
**Lectures:** all fourteen, most directly [week 5, implementation](../lectures/w05-implementation-in-engine.md), [week 6, middleware](../lectures/w06-middleware-events-and-parameters.md), [week 7, attenuation](../lectures/w07-spatial-audio-and-attenuation.md), [week 10, mixing](../lectures/w10-mixing-ducking-and-priority.md), [week 12, many voices](../lectures/w12-audio-for-mmos-many-players-one-mix.md), [week 13, accessibility](../lectures/w13-accessibility-subtitles-and-visual-sound-cues.md) and [week 14, optimization](../lectures/w14-optimization-voices-memory-streaming.md).
**Labs that feed it:** [10](../labs/lab10.md) (the mix), [12](../labs/lab12.md) (the voice budget), [13](../labs/lab13.md) (the caption plan) and [14](../labs/lab14.md) (the budget sheet, a required appendix).

## What this component is for

The SFX pack and the adaptive music assignment each built one layer of sound. This assessment asks you to ship all of it in one game slice, at once, in its busiest moment, for players who hear well, players who hear some of it and players who hear none of it. It covers all three course outcomes and puts the most weight on the third: mix for clarity in dense scenes.

A slice that "sounds full" earns little. A slice where every gameplay-critical event reads in the busiest ten seconds, where you can say which sounds were dropped and why, where a muted player still gets the forecasts, and where the audio fits a stated memory and CPU budget, earns a lot.

## The slice

Use the slice from your [SFX pack](sfx-pack-brief.md) and [adaptive music](adaptive-music-brief.md), in Godot 4 or Unity 6, with FMOD Studio or Wwise if you used them before. The slice should play for 3 to 5 minutes and include:

- at least one **dense moment**: 10 or more sound sources active at once (enemies, projectiles, other characters, a crowd). If your slice has none, add a scripted stress scene with three times its normal enemy count;
- at least one **forecast** the player must act on (a wind-up, a warning, an approaching threat);
- at least one **UI flow** (a menu, inventory or shop);
- the **adaptive music** from your assignment, driven by real gameplay rather than a script.

## Audio sources and licences

The rules from the [SFX pack brief](sfx-pack-brief.md#audio-sources-and-licences) apply to every new sound, and the rules from the [adaptive music brief](adaptive-music-brief.md#music-sources-and-licences) apply to the music. All audio must be your own or properly licensed (CC0, or CC-BY with credit), and every third-party file needs a row in `LICENSES.md`. If you use an open-source game as the slice, its original audio does not count toward your marks, and any original sound you keep must be listed with its licence. Voice lines must be recorded by you or by people who agreed in writing; do not use synthetic copies of real people's voices.

## What you build

### 1. The sound pass

Every player action, threat, pickup, door, UI event and state change in the slice has a sound or a deliberate silence, listed in an event table in the week 6 contract format: event path or name, one-shot or persistent, parameters with ranges, bank or load group, owner, and every way a persistent event stops. Reuse the pack; add what the slice still needs.

### 2. The mix (week 10, lab 10)

- A **bus tree** of at least eight buses (for example Master, Music, Dialogue, SFX, Weapons, Foley, Ambience, UI) with base levels.
- **Snapshots** for at least pause or menu, and one gameplay state (low health, underwater, a boss phase).
- A **duck table**: key, target, depth, attack and release. Include music under dialogue or voice, and check the release against the gaps between your lines.
- A **priority table** with base priorities, a distance offset rule, per-event instance limits, what happens to a sound that loses its slot (kill or virtual), and the global voice limit.
- A written decision on **HDR**: use it on the SFX bus or not. If yes, give `T`, `W` and `r`, and the in-game level of each forecast sound chosen by importance.
- **Headroom**: the master peaks at or below −1 dBFS in the busiest moment, with no clipping.

### 3. Many voices (week 12, lab 12)

For the dense moment, compute the average demand with Little's law, state your voice budget, and design relevance tiers with reservations and spill-down (you, the main threat, allies, everyone else). If the slice can have 20 or more agents, add a crowd bed or an audio LOD for the "others" tier. Then measure: run the dense moment and record the peak real voice count and which tier lost sounds.

### 4. Spatial decisions (week 7)

An attenuation table for every 3D category, the listener placement (camera, character or split) with the reason, and one occlusion or distance-filter cue.

### 5. Accessibility (week 13, lab 13)

- **Subtitles** for every voice line, checked with your lab 13 checker at `R = 17` and `d_min = 1.0 s`, with every clash fixed by a named strategy. If the slice has no speech, write one short radio or companion exchange of at least six lines and subtitle it.
- **Captions** with keys for every sound that passes the information test, including music that carries game state.
- **Visual sound cues** (markers or a radial indicator) for at least the forecasts, with the direction computed from bearing and facing, and a paragraph on the fairness test.
- A **mute run**: play the slice's hardest part with sound off and cues on, and report what you missed.

### 6. The budget (week 14, lab 14)

The budget sheet from lab 14 Part C for your slice, with a stated target platform, memory and CPU budgets, a load type and codec per group, the checker output, and the profiler comparison from the busiest 30 seconds. This appendix is required; a submission without it is capped at half marks for the budget criterion.

## Deliverables

- The project, zipped, with a `README.md` that says how to open it, run the slice, turn on the debug view (voice count, current music state and intensity, active snapshots) and jump to the dense moment. It must run from a clean copy on the lab machines.
- **Two captures.** A 3 to 5 minute playthrough with sound, captions on and the debug view visible, and a 60 to 90 second capture of the hardest part with sound muted and visual cues on.
- A **before and after**: 30 seconds of the dense moment with the SFX pack dropped in and no mix work (all buses at 0 dB, no ducks, no priorities), and the same 30 seconds after the pass.
- `SOUND_PASS.md`, 2,000 to 3,000 words, with these sections: the slice and what its sound must communicate; the event table; the mix (bus tree, snapshots, ducks, priorities, the HDR decision, and what the before and after capture shows); many voices (demand, tiers, measured peak and losses); spatial decisions; accessibility (subtitle report, caption plan, cues, fairness, the mute run); and the three decisions you are least sure of, with what you would test next.
- Appendices: the lab 14 budget CSV and checker output; the lab 13 checker output on your script; `LICENSES.md`.
- Pairs only: `CONTRIBUTIONS.md`, one paragraph each, naming the systems and files each partner owns.

## Milestone 1: the plan (end of week 12, 10 points)

Two pages, before most of the integration exists. The slice's event table (it may be incomplete), the bus tree, a first duck table and priority table, the Little's-law demand for the dense moment with your voice budget, and a first budget sheet from lab 14 with the target platform. Feedback comes back within a week and focuses on whether the plan protects the forecasts in the dense moment.

## Milestone 2: the rough pass (end of week 14, 10 points)

A 5-minute demo in the lab session. The slice runs with the pack and the music integrated, the bus tree and at least one duck and one snapshot work, the debug view shows the voice count and music state, and you can jump to the dense moment. Bring the peak voice count you measured there and one sound you found missing in it.

## The crit (week 15, 15 minutes)

You run your submission from a clean copy on a lab machine while two examiners watch and listen on headphones.

1. **Play (4 min).** Play the slice's opening and its dense moment with the debug view on.
2. **Break it (3 min).** An examiner picks a sound and asks you to show where it lives: its event, bus, ducks, priority and budget group. Then they mute a bus or change a duck depth and you explain what changed.
3. **Mute run (3 min).** The examiner plays the hardest part muted with your cues on.
4. **Questions (5 min).** Three questions in the style of the [exam bank](exam-bank.md), rewritten with the numbers from your own sheet, mix and budget. At least one is a compute question.

## Rubric

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| Milestone 1: the plan | 9 to 10: event table, bus tree, ducks, priorities, demand and budget draft present and consistent | 6 to 8: one part thin | 2 to 5: several parts missing | 0 to 1 | 10 |
| Milestone 2: the rough pass | 9 to 10: all demo checks pass; measured peak voices and a missing sound reported | 6 to 8: one check fails | 2 to 5: slice runs, integration largely missing | 0 to 1 | 10 |
| Clarity in the dense moment | 14 to 15: every forecast and critical report reads in the busiest 10 s; the before and after shows a named improvement; nothing important is masked or dropped | 10 to 13: one critical sound weak | 5 to 9: the dense moment is a wall of sound | 0 to 4 | 15 |
| Mix structure | 14 to 15: bus tree, snapshots, ducks and priorities work as documented; duck release fits the line gaps; HDR decision argued; master peaks at or below −1 dBFS | 10 to 13: one element missing or undocumented | 5 to 9: mix mostly static, or clipping | 0 to 4 | 15 |
| Many voices | 7 to 8: demand computed, tiers with reservations and spill-down, measured peak compared with the model, losses fall on the right tier | 5 to 6: tiers present, no measurement | 2 to 4: voice limit only | 0 to 1 | 8 |
| Music integration | 7 to 8: music driven by real gameplay; switches on sync points; stingers fit; music ducks or trims under the dense moment as decided | 5 to 6: one behaviour off | 2 to 4: music plays but does not follow the game | 0 to 1 | 8 |
| Spatial | 5 to 6: attenuation per category tied to gameplay distances; listener placement justified; one occlusion or filter cue | 3 to 4: defaults with reasons | 1 to 2: defaults, no reasons | 0 | 6 |
| Accessibility | 9 to 10: subtitles pass the checker; captions and cues cover every sound that passes the information test; fairness argued; the mute run found and fixed a gap | 6 to 8: one part thin | 3 to 5: subtitles only | 0 to 2 | 10 |
| Budget and performance | 7 to 8: budget sheet fits a stated platform; load types and codecs chosen per group with reasons; profiler figures compared with the sheet and the sheet updated | 5 to 6: fits, no measurement | 2 to 4: sheet incomplete | 0 to 1 | 8 |
| Crit | 9 to 10: runs from a clean copy; every sound traced to its event, bus and budget group; answers use your own numbers | 6 to 8: one step needs help | 3 to 5: two steps fail, or answers vague | 0 to 2 | 10 |
| **Total** | | | | | **100** |

The final sound pass mark is the total out of 100, multiplied by 0.40.

## Rules and advice

- **Protect the forecasts first.** Decide in week 10 which three sounds must never be lost in the dense moment, and design the priority table, the ducks and the tiers around them.
- **Debug view from day one.** A voice counter, the music state and the active snapshots on screen will find most mix bugs faster than listening alone.
- **Before and after is evidence.** Record the "before" capture as soon as the pack is in, before you touch the mix.
- **Budget early.** Fill the lab 14 sheet at milestone 1 with estimates, then replace each estimate with a measurement.
- **Late submission.** Up to 48 hours late, the final is marked out of 64 instead of 80, and the crit is rescheduled if the timetable allows. Milestones cannot be late, but a missed milestone can be shown at the next lab session for half marks.
- **Integrity.** Every sound, stem and line must trace to your own work or to a row in `LICENSES.md`. In the crit you must be able to explain every event, bus and number you submit.
