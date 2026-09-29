# AU101 — Audio for Games

Year 1, semester 2 · 3 credits · Prerequisites: none

Sound as feedback and atmosphere: SFX design, adaptive music and implementation with middleware.

## Learning outcomes

- Design and implement SFX that communicate game state
- Build adaptive music with layers and transitions
- Mix for clarity in dense scenes

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | What sound does in games: feedback, space, emotion | [lecture](lectures/w01-what-sound-does-feedback-space-emotion.md) | [cone-of-confusion](examples/w01-cone-of-confusion.html) |
| 2 | Recording and foley basics | [lecture](lectures/w02-recording-and-foley-basics.md) | [sample-rate-and-pitch](examples/w02-sample-rate-and-pitch.html) |
| 3 | Synthesis for SFX | [lecture](lectures/w03-synthesis-for-sfx.md) | [pitch-contour-synth](examples/w03-pitch-contour-synth.html) |
| 4 | Layering and variation (avoid machine-gun effect) | [lecture](lectures/w04-layering-and-variation.md) | [machine-gun](examples/w04-machine-gun.html) |
| 5 | Implementation in engine | [lecture](lectures/w05-implementation-in-engine.md) | [trigger-timing](examples/w05-trigger-timing.html) |
| 6 | Middleware: FMOD/Wwise events and parameters | [lecture](lectures/w06-middleware-events-and-parameters.md) | [engine-rpm](examples/w06-engine-rpm.html) |
| 7 | Spatial audio and attenuation | [lecture](lectures/w07-spatial-audio-and-attenuation.md) | [attenuation-curves](examples/w07-attenuation-curves.html) |
| 8 | Adaptive music: vertical layering | [lecture](lectures/w08-adaptive-music-vertical-layering.md) | [layer-mixer](examples/w08-layer-mixer.html) |
| 9 | Horizontal re-sequencing and stingers | [lecture](lectures/w09-horizontal-re-sequencing-and-stingers.md) | [sync-points](examples/w09-sync-points.html) |
| 10 | Mixing, ducking, priority | [lecture](lectures/w10-mixing-ducking-and-priority.md) | [hdr-window](examples/w10-hdr-window.html) |
| 11 | UI sound design | [lecture](lectures/w11-ui-sound-design.md) | [streak-ladder](examples/w11-streak-ladder.html) |
| 12 | Audio for MMOs: many players, one mix | [lecture](lectures/w12-audio-for-mmos-many-players-one-mix.md) | [raid-voice-budget](examples/w12-raid-voice-budget.html) |
| 13 | Accessibility: subtitles and visual sound cues | [lecture](lectures/w13-accessibility-subtitles-and-visual-sound-cues.md) | [subtitle-reading-race](examples/w13-subtitle-reading-race.html) |
| 14 | Optimization: voices, memory, streaming | [lecture](lectures/w14-optimization-voices-memory-streaming.md) | [audio-budget](examples/w14-audio-budget.html) |
| 15 | Final: sound pass on a game slice | [assessments](#assessment-materials) | — |

## Signature worked examples

- The machine-gun effect: same sample x10 vs randomized pitch/volume variants (interactive player)
- Vertical layering: combat intensity slider mixes stems in real time

## Labs

- [AU101 · Lab 01: Sound audit](labs/lab01.md)
- [AU101 · Lab 02: Foley session and level check](labs/lab02.md)
- [AU101 · Lab 03: A tiny sound-effect synthesiser](labs/lab03.md)
- [AU101 · Lab 04: The variation engine](labs/lab04.md)
- [AU101 · Lab 05: Trigger timing](labs/lab05.md)
- [AU101 · Lab 06: An engine event and its contract](labs/lab06.md)
- [AU101 · Lab 07: Attenuation curves, audible radius and panning](labs/lab07.md)
- [AU101 · Lab 08: A layered score from an intensity curve](labs/lab08.md)
- [AU101 · Lab 09: A quantized music director](labs/lab09.md)
- [AU101 · Lab 10: Build the mix brain](labs/lab10.md)
- [AU101 · Lab 11: Render a UI family](labs/lab11.md)
- [AU101 · Lab 12: The raid voice budget](labs/lab12.md)
- [AU101 · Lab 13: Subtitle timing and directional cues](labs/lab13.md)
- [AU101 · Lab 14: An audio budget you can defend](labs/lab14.md)

## Assessment materials

- [AU101 · Exam bank: quiz, practice and crit questions](assessments/exam-bank.md)
- [AU101 · Adaptive music brief](assessments/adaptive-music-brief.md)
- [AU101 · Final sound pass brief](assessments/final-sound-pass-brief.md)
- [AU101 · SFX pack brief](assessments/sfx-pack-brief.md)

## Readings

- Collins — Game Sound, ch. 1-3

## Assessment

SFX pack (30%), adaptive music (30%), final sound pass (40%)
