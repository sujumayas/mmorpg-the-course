# AU101 · Week 01 — What Sound Does in Games: Feedback, Space, Emotion

**Why this matters:** Sound is the only channel that reaches a player who is looking the wrong way. It confirms their actions, tells them where danger is, and sets how they feel about it. If you can name which of those jobs a sound is doing, you can design it, test it and defend it in a review instead of arguing about taste.

**You will be able to:**
- Classify any game sound by its job (feedback, space, emotion) and by whether it exists in the game world.
- Compute the interaural time difference for a sound at a given angle and explain why front and back sources get confused.
- Critique a game's audio with a structured sound audit and a mute test.
- Decide when a game needs more than stereo panning to place sounds around the player.

**Before class:** Collins, *Game Sound* (2008), chapters 1-3. Play 15 minutes of any game you like with the sound on, then 5 minutes with it muted, and write down the first moment you felt lost.

**Prerequisites from earlier courses:** [GD101 week 12, feedback, juice, clarity and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) (the three jobs of feedback: confirm, report, forecast). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (decibels and why volume sliders need them; this lecture uses that result and does not repeat it). [MA101 week 10, angles, radians, sin and cos](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) (radians and the sine of an angle). [CS101 week 14, polish pass](../../CS101-programming-for-games-i/lectures/w14-polish-pass-sound-particles-screen-shake.md) (playing a sound from code with pitch and volume variation).

**Interactive:** [examples/w01-cone-of-confusion.html](../examples/w01-cone-of-confusion.html). Use headphones. Keep it open during section 3.

---

## 1. What a sound is, in four numbers

A sound is a pressure wave. Something vibrates, pushes the air, and the push travels outward at about 343 metres per second in room-temperature air. When it reaches your ear, your eardrum moves in step with it. Everything you will do in this course is a way of shaping that wave or deciding when and where it starts.

Four numbers describe most of what you need this term.

- **Frequency** is how many times the wave repeats per second, measured in hertz (Hz). You met it in MA101 week 10 as the `f` in `sin(2πft)`. Low frequencies sound low: a large engine hum sits around 50 to 100 Hz. High frequencies sound high: the fizz on a cymbal is above 8,000 Hz (8 kHz). Healthy young ears hear roughly 20 Hz to 20 kHz, and the top end drops with age.
- **Amplitude** is how far the pressure swings. Audio tools measure amplitude ratios in **decibels (dB)**, a logarithmic unit. MA101 week 5 derived the conversion `dB = 20 · log10(amplitude ratio)`, so halving the amplitude is about −6 dB. Perceived loudness is a separate thing. A widely used rule of thumb says a sound must go up by about 10 dB to seem twice as loud.
- **Duration and envelope** describe how the sound starts, holds and fades. A gunshot reaches full level in a millisecond and is gone in half a second. A wind loop never starts or ends. Week 3 builds sounds from envelopes.
- **Position** is where the sound comes from relative to the listener. This one is the reason games have an audio programmer and films mostly do not. In a film the camera and the audience never move. In a game the listener turns every frame.

Hold on to position. Section 3 is about how the ear works it out and how easily it gets fooled.

## 2. The three jobs of game sound

Every sound in a game is doing at least one of three jobs. Naming the job tells you what a good version of that sound has to achieve.

### Feedback: "that happened"

GD101 week 12 split feedback into three kinds. Sound carries all three.

- **Confirm.** The player acted and the game accepted it. A button click, a footstep, the thunk of a reload finishing. Confirmation sounds must be fast (within a frame or two of the action) and consistent, because players learn them as part of the control.
- **Report.** Something changed in the game state. You took damage, an ally went down, a quest updated. Report sounds must be distinct from each other, because the player often cannot see the source.
- **Forecast.** Something is about to happen. A boss winds up, a grenade pin drops, footsteps approach. Forecast sounds are the most valuable sounds in a game, because they turn a surprise into a decision.

Left 4 Dead (Valve, 2008) and its sequel give every special infected enemy a short musical cue that the fan community calls its "bacteria" theme. Each enemy type has its own set of notes, so experienced players identify the threat before they see it. The same cue comes in two versions. On piano it means the enemy spawned nearby. On strings it means the enemy spawned further away. So a single musical sting forecasts what is coming and roughly how far away it is. In the November 2010 update, Valve turned these cues off in Left 4 Dead 2's Versus mode, where the infected are human players. A forecast that is fair against the game's AI director hands free information to one team when the enemy is a person.

### Space: "it is over there, and this is the room"

Sound tells the player three spatial things that vision often cannot.

1. **Direction.** Where the source is, including behind you and above you.
2. **Distance.** How far away. Level drops with distance, high frequencies drop faster than low ones, and the ratio of direct sound to reflected sound shrinks. Week 7 turns these into attenuation curves.
3. **The space itself.** A footstep in a cathedral and a footstep in a wardrobe differ in their reflections, which we call **reverb**. Players read the size and material of a room from reverb without thinking about it.

Space is also why sound matters for fairness in competitive games. If a footstep from behind sounds like it came from in front, the player turns the wrong way and loses a fight they had the information to win. Section 3 is a worked example of exactly that failure.

### Emotion: "this is how you should feel about it"

Music, ambience and the character of each sound effect set mood and pacing. Left 4 Dead's Witch is the classic case. A cue plays while the survivors are near her, and it gets louder the closer they get. The music reports distance (space), forecasts a dangerous encounter (feedback) and builds dread (emotion), all at once. Most good game sounds do more than one job. The labels help you check that each job is covered, not sort sounds into boxes.

Emotion is also where silence lives. Removing music before a big moment makes the moment land harder. Week 8 and week 9 build music that reacts to game state.

### In the world or outside it

Film theory separates **diegetic** sound, which exists in the story world (a character's footsteps, a radio playing in a room), from **non-diegetic** sound, which only the audience hears (the score, a narrator). Games blur the line constantly. The Left 4 Dead cues are non-diegetic music that carries diegetic information. A health-low heartbeat is ambiguous on purpose.

Karen Collins, in the introduction to *Game Sound*, draws a line that matters more for implementation. The version below is this course's paraphrase, so check it against chapter 1 as you read. Some game audio is **interactive**: it responds directly to what the player does, like a jump sound. Some is **adaptive**: it responds to the game state, like combat music that starts when enemies notice you. **Dynamic audio** is her umbrella term for both. For you as a designer the question is simple. What triggers this sound, the player's input or the game's state? The answer decides who owns it in the code and how it gets tested.

## 3. Worked example: where is that footstep?

### The hook

Counter-Strike 2 is a game where players win rounds by listening. Its official release notes spend lines on exactly where sounds seem to come from. The 13 September 2023 notes list a "slight increase to stereo spread". The 29 June 2023 notes added a separate occlusion layer on the map Nuke to help with vertical sound positioning. The 6 February 2024 notes fixed some sounds that players perceived as coming from slightly behind them.

Why would a studio with Valve's resources still be fixing "is this in front or behind"? Because human ears are genuinely bad at telling front from back, and the reason is a single small formula.

### The model

Your two ears sit on opposite sides of your head. A sound from your right reaches your right ear first and your left ear a fraction of a millisecond later, because it has to travel around your head. That delay is the **interaural time difference (ITD)**. Your brain uses it as the main direction cue for low and mid frequencies.

A standard simple model treats the head as a sphere. It goes back to the psychologist Robert Woodworth in the 1930s:

```
ITD = (r / c) × (θ + sin θ)
```

- `r` is the head's radius. We use 0.0875 m, a common average.
- `c` is the speed of sound, 343 m/s.
- `θ` (theta) is the **lateral angle** in radians: how far the source is from straight ahead, measured toward the side, between 0 and π/2.
- `r / c` is about 0.255 milliseconds. It is the time sound takes to cross one head radius.

Here is the part that matters. Put a source at **azimuth** `a`, the angle around you, with 0° straight ahead, 90° hard right and 180° straight behind. The lateral angle is

```
θ = asin(sin a)
```

A source at 30° and a source at 150° have the same `sin a` (both 0.5), so they have the same lateral angle and the same ITD. So do 60° and 120°. For any source in front of you there is a mirror source behind you that produces exactly the same timing at your ears. In 3D the set of positions that share one ITD forms a cone around the line through your ears, and hearing researchers call it the **cone of confusion**.

### Numbers you can check

This script prints the table. Run it with `.venv/bin/python` from the repository root.

```python
import math

R, C = 0.0875, 343.0          # head radius in metres, speed of sound in m/s
RATE = 48000                  # samples per second in a typical game mix

for azimuth in [0, 30, 60, 90, 120, 150, 180]:
    theta = math.asin(math.sin(math.radians(azimuth)))
    itd_ms = R / C * (theta + math.sin(theta)) * 1000
    print(f"{azimuth:>3} deg  ITD {itd_ms:.3f} ms  = {itd_ms / 1000 * RATE:4.1f} samples")
```

It prints:

```
  0 deg  ITD 0.000 ms  =  0.0 samples
 30 deg  ITD 0.261 ms  = 12.5 samples
 60 deg  ITD 0.488 ms  = 23.4 samples
 90 deg  ITD 0.656 ms  = 31.5 samples
120 deg  ITD 0.488 ms  = 23.4 samples
150 deg  ITD 0.261 ms  = 12.5 samples
180 deg  ITD 0.000 ms  =  0.0 samples
```

| Azimuth (front) | Azimuth (behind, mirror) | Lateral angle | ITD | Samples at 48 kHz |
|---|---|---|---|---|
| 0° | 180° | 0° | 0.000 ms | 0 |
| 30° | 150° | 30° | 0.261 ms | 12.5 |
| 60° | 120° | 60° | 0.488 ms | 23.4 |
| 90° | 90° | 90° | 0.656 ms | 31.5 |

Check one row by hand. At 30°, `θ = 0.5236` rad and `sin θ = 0.5`. So `ITD = 0.2551 ms × 1.0236 = 0.261 ms`. Three things stand out.

1. The largest possible delay is about two thirds of a millisecond. Your brain resolves differences of a few hundredths of a millisecond, which is why direction works at all.
2. The whole left-right range fits in about 31 samples of a 48 kHz mix. A game that delays one ear by the wrong few samples moves the sound by tens of degrees.
3. Every row has a twin. Timing alone cannot separate the front column from the behind column.

### A visual you can move

Open [`examples/w01-cone-of-confusion.html`](../examples/w01-cone-of-confusion.html) with headphones on. The left view is a top-down head with a sound source you drag around a circle. The right view plots ITD against azimuth for the whole circle. Drag the source from 30° to 150°. The source on the left jumps from in front of the face to behind the head, and the dot on the right does not move vertically at all. Press "play click" at each position. With the "timing only" model, the two positions sound identical. Switch on "level difference" and they still sound identical, because the model's level difference also depends only on the lateral angle. Only the "head turn" button breaks the tie. It rotates the listener 20° and plays the click again. Now the front source and the back source move in opposite directions on the plot.

That last point is how you resolve the confusion in real life. You turn your head a little, and a source in front shifts one way while a source behind shifts the other. Hold the head still and the confusion returns.

### Cross-game recognition

**Counter-Strike 2 (2023-2024 release notes).** The patch lines quoted above are three different fixes for the same problem. "Stereo spread" widens the left-right difference so lateral angles are easier to tell apart. The Nuke occlusion layer adds a cue other than timing for up and down, because the cone of confusion also swallows elevation: a source straight above and a source straight ahead both have ITD zero. The "slightly behind the player" fix is a front-back error that players noticed and reported. In a first-person shooter the player turns the camera constantly, which is the game version of a head turn, so the confusion resolves quickly if the listener orientation follows the camera.

**Hellblade: Senua's Sacrifice (Ninja Theory, 2017).** The voices in Senua's head were recorded with **binaural** microphones, which sit in the ear canals of a model head. The recording keeps the timing and level differences, plus the filtering from the shape of the outer ear, the **pinna**. Those pinna cues are the main thing a real head uses to separate front from back, because the pinna shades sounds from behind more than sounds from the front. On headphones the voices appear to whisper from behind and beside the player. The game uses the same physics as the Counter-Strike problem, pointed at emotion instead of competition.

**The Web Audio API (current browsers, W3C specification).** The browser's `PannerNode` has two panning models. The default, `equalpower`, sets only the level in each channel. It cannot express front or back at all, since a source at 30° and one at 150° get the same left-right balance. The `HRTF` model convolves the sound with measured **head-related transfer functions**, filters recorded from real human ears that include pinna cues. Godot, Unity, FMOD and Wwise all offer the same choice under different names: cheap level panning, or HRTF-based spatialisation that costs more processing.

**Left 4 Dead (2008).** The piano-versus-strings cue is a designer's workaround for distance and direction that the ear cannot judge well. Instead of trusting spatial hearing, the game encodes "near" and "far" in the instrument. Reach for this when position is important and physics will not deliver it.

In all four, the question is the same. What does this sound need the player to know about position, and which cue delivers it: timing, level, pinna filtering, head movement, or an explicit symbolic code?

### Eyes-open design judgment

- **Stereo level panning is cheap and good enough for most side-view and top-down games.** When the camera never rotates, front and back rarely matter, so do not pay for HRTF.
- **First-person games get head turns for free.** Make the listener orientation follow the camera, not the character's body, or the player's instinctive turn will not disambiguate anything.
- **HRTF has costs.** It needs headphones (on speakers, sound from each speaker reaches both ears and scrambles the cues). Measured HRTFs come from other people's ears and can sound wrong to some players. It uses more CPU per voice, which matters in a crowded MMO scene (week 12 and week 14).
- **Competitive games must decide what information sound carries.** Valve decided the Left 4 Dead cues were fair against the AI and unfair against people. Treat every spatial cue as game information, and balance it like any other.
- **Never let direction live only in sound.** Some players are deaf or hard of hearing, and some play with the sound off. Week 13 covers visual sound indicators. For now, when a sound forecasts danger, ask what the visual twin is.

## 4. Listening like a designer: the sound audit

You will spend this course making sounds. Before that, you need a habit for hearing a game's audio as a system. The tool is a **sound audit**: a log of every sound event in a short stretch of play, with its job and trigger.

For each sound you hear, record:

1. **When** (timestamp) and **what** (a plain name like "enemy footstep, gravel").
2. **Source on screen?** Yes or no. Off-screen sounds are usually doing space or forecast work.
3. **Job.** Feedback, space or emotion. Pick the main one and note a second if it is strong.
4. **Feedback kind.** Confirm, report or forecast, if the job is feedback.
5. **Diegetic?** Does it exist in the game world?
6. **Trigger.** Player input (interactive) or game state (adaptive).
7. **Mute cost.** 1 to 3: how badly would a muted player miss this?

Twenty minutes of an audit teaches you three things about any game. First, the ratio of confirm to forecast sounds shows how much the game warns you before it hurts you. Second, the share of off-screen sources shows how much of the game's information lives only in audio. Third, the mute-cost-3 rows are the game's accessibility debt, which week 13 asks you to pay down.

### The mute test

The quickest audit is the one you did before class. Play with sound, then without. The moments you felt lost muted are the sounds carrying information vision does not. The moments that felt flat but still playable are the emotion layer. Good audio design usually shows up as a game that is much better with sound and still fully playable without it.

### How much to trust a single play session

An audit is a sample. One boss fight over-represents forecasts, and a menu session over-represents confirms. When you compare two games, audit comparable stretches: the first ten minutes of combat, say, or one full quest. The lab asks for at least 40 events so that a single odd moment cannot swing your percentages by more than a few points.

## In-class activity (25 minutes)

Work in groups of three. You need one laptop with a game or gameplay video that has original audio (no commentary), and one shared sheet.

1. **Five-minute blind listen (5 min).** One person watches the screen. The other two face away and write down each sound, where they think it came from (clock face: 12 is ahead, 6 is behind), and what they think happened.
2. **Compare (5 min).** The watcher reads out what actually happened. Mark every direction guess that was off by more than 90°. Count how many of those were front-back swaps (for example 2 o'clock heard as 4 o'clock).
3. **Job labels (10 min).** Together, label every sound from step 1 with job, feedback kind, trigger and mute cost.
4. **One redesign (5 min).** Pick the sound with the highest mute cost that the listeners got wrong. Write one sentence proposing a fix: a stronger cue, a symbolic code like Left 4 Dead's piano and strings, or a visual twin.

Expected output: the labelled list, the count of front-back swaps, and the one-sentence fix. Post them to the course board; we will tally front-back swaps across groups at the start of next class.

## Common misconceptions

- **"Sound is decoration; the game works without it."** Many games run fine muted, but competitive shooters, horror games and anything with off-screen threats lose real information. The audit's mute-cost column measures how much.
- **"If it's panned right, it sounds right."** Level panning places a sound on a left-right line. It cannot place it in front or behind. Front and back need pinna filtering (HRTF), head movement or a symbolic cue.
- **"Half the amplitude is half as loud."** Halving amplitude is −6 dB. Sounding half as loud takes roughly −10 dB. MA101 week 5 works through what this means for volume sliders.
- **"Music is the emotion layer and sound effects are the feedback layer."** Left 4 Dead's cues are music doing feedback and space work. A creaking floor is an effect doing emotion work. Label the job, not the file type.

## Check yourself

1. Using the model with `r = 0.0875` m and `c = 343` m/s, compute the ITD for a source at azimuth 45°. Which other azimuth produces the same ITD?
2. A game mixes at 44.1 kHz. How many samples of delay separate a source straight ahead from one at 90°?
3. A top-down strategy game places the listener at the camera, which never rotates. A designer wants to add HRTF. Give one argument for and one against, using this lecture's model.
4. Classify these four sounds by main job and, if feedback, by kind: (a) a rising whine before a boss's laser fires; (b) your character's footsteps echoing louder as you enter a cave; (c) a soft chime when an item goes into your bag; (d) a low drone that starts when you enter a haunted zone.
5. Left 4 Dead encodes "near" and "far" in piano versus strings. Suggest a comparable symbolic code for "above" versus "below" in a game with many floors, and say what problem it avoids.

<details>
<summary>Answers</summary>

1. `θ = 0.7854` rad and `sin θ = 0.7071`, so `ITD = 0.2551 × 1.4925 ≈ 0.381` ms. The mirror azimuth 135° gives the same value.
2. The 90° ITD is 0.656 ms. At 44,100 samples per second that is `0.000656 × 44100 ≈ 28.9` samples.
3. For: HRTF could add height and front-back cues that level panning cannot. Against: with a fixed camera, the map's "behind" is just the bottom of the screen and the player can see it. The cost (CPU per voice, headphone dependency, strangers' ears) buys little. Level panning plus distance attenuation is usually enough.
4. (a) Feedback, forecast. (b) Space, since the reverb change tells you the room changed; it also confirms movement. (c) Feedback, confirm. (d) Emotion, with a report component, since the zone change is also information.
5. One option: a short motif played higher in pitch for sources above and lower for sources below, or a different instrument family per floor. It avoids relying on elevation cues, which fall inside the cone of confusion and are weak without head movement or strong pinna filtering.

</details>

## Lab / assignment hook

[Lab 01, sound audit](../labs/lab01.md). Audit 40 or more sound events from a game of your choice using the columns in section 4, validate your sheet with the provided checker, and write a 500-word memo on what the game's audio carries that its visuals do not. The audit feeds the SFX pack assignment, where you redesign the three highest-cost sounds.

## Sources

- Collins, K. (2008). *Game Sound: An Introduction to the History, Theory, and Practice of Video Game Music and Sound Design*. MIT Press. Chapters 1-3 (chapter 1 is the introduction, chapter 2 "Push Start Button", chapter 3 "Insert Quarter to Continue"); the interactive, adaptive and dynamic audio distinction is paraphrased from the introduction.
- Valve, Counter-Strike 2 release notes, 29 June 2023 (limited test: distance effects on positional sources, occlusion layer for vertical positioning on Nuke), 13 September 2023 ("slight increase to stereo spread"), 6 February 2024 (fix for player-centric sounds perceived as slightly behind the player). Steam news feed for app 730.
- Left 4 Dead Wiki, "Left 4 Dead Soundtrack" (Left 4 Dead, 2008, and Left 4 Dead 2, 2009). Special infected "bacteria" cues, piano for near spawns and strings for far spawns, Witch cue rising with proximity, cues disabled in Left 4 Dead 2 Versus by the 19 November 2010 update. Composer Mike Morasky.
- Wikipedia, "Left 4 Dead". Each special infected has a distinctive sound, silhouette and musical cue; the AI Director controls pacing.
- Wikipedia, "Hellblade: Senua's Sacrifice" (Ninja Theory, 2017). Voices recorded with binaural recording, informed by research on voice-hearing.
- MDN Web Docs, "PannerNode: panningModel property" (Web Audio API). `equalpower` default, `HRTF` using convolution with measured impulse responses.
- Woodworth, R. S. (1938). *Experimental Psychology*. Holt. Origin of the spherical-head ITD approximation `(r/c)(θ + sin θ)`.
- Nave, R. *HyperPhysics*, "Loudness" and "Rule of thumb for loudness" (Georgia State University). About 10 dB for a doubling of perceived loudness.

## Interactive spec: examples/w01-cone-of-confusion.html

**Purpose.** Make the cone of confusion visible and audible. The one insight: a source in front and its mirror behind produce the same interaural time difference, and only a head turn (or pinna filtering) tells them apart.

**Layout.** Two linked views side by side on desktop, stacked on mobile (source view on top).

- **Left, "Top-down head".** A circle for the head (radius about 30% of the panel) with a nose tick at 0° (up) and ear marks at 90° and 270°. A draggable source dot on a larger ring (radius about 85%). A faint ghost dot at the mirror position `180° − a` (drawn in `--ink-soft`, dashed outline). Label both with their azimuth.
- **Right, "ITD vs azimuth".** x axis azimuth 0° to 360°, y axis ITD from −0.7 ms to +0.7 ms (positive means the right ear leads). Plot the curve `ITD(a)` for the whole circle in `--steel`. Mark the current source as a solid dot and the mirror as a hollow dot. They sit at the same height. Draw a horizontal dashed line through both.

**Model (exact).**

```
R = 0.0875, C = 343
lateral(a) = asin(sin(a))            // a in radians, azimuth 0 = front, +90° = right
ITD(a) = (R / C) * (lateral(a) + sin(lateral(a)))   // seconds, signed: positive = right ear first
ILD_dB(a) = 6 * sin(a)               // simple level difference used by "level difference" mode, right minus left
```

**Controls.**
- Drag the source (mouse, touch). Keyboard: focus the source and use Left/Right arrows for ±5°, Shift+arrow for ±15°. Also a range input 0-359 mirroring it.
- Radio group "cue model": `timing only`, `timing + level difference`.
- Button "play click": synthesise a 5 ms noise burst (white noise, linear decay) and play it through a `ChannelMergerNode` with the far ear delayed by `|ITD|` via a `DelayNode` per channel. In level mode, apply `±ILD_dB/2` to each channel. No `PannerNode`; the point is to hear only the model.
- Button "play mirror": the same click at `180° − a`.
- Button "head turn +20°": plays the click at `a` (before the turn) and then at `a − 20°` (after the turn; listener rotated right means the source's relative azimuth decreases), and animates both the source dot and the mirror dot on the right plot along the curve. Show text: "front source ITD went from X to Y; mirror went from X to Z". They move in opposite directions.
- Toggle for head radius 0.07-0.10 m (small slider), default 0.0875.

**Readouts (exact numbers next to the visual).** Azimuth, mirror azimuth, lateral angle, ITD in ms (3 decimals), ITD in samples at 48 kHz (1 decimal), ILD in dB (1 decimal).

**Test values (must match).**
- a = 30°: ITD 0.261 ms, 12.5 samples. Mirror 150°: same.
- a = 60°: 0.488 ms, 23.4 samples. Mirror 120°: same.
- a = 90°: 0.656 ms, 31.5 samples. Mirror is itself.
- a = 270°: −0.656 ms.
- Head turn from a = 30°: front source goes to 10° (ITD 0.089 ms); mirror 150° goes to 130° (ITD 0.418 ms).

**First screen.** Source at 30°, mirror at 150°, both dots on the plot at the same height with the dashed line visible, caption: "Same delay, opposite sides of your head."

**Accessibility and rules.** Audio only starts after a user gesture. All buttons keyboard reachable. Respect `prefers-reduced-motion` (no animation for the head turn, just jump). Use the shared tokens in `templates/interactive-tokens.css`. No external audio files. Show a short "headphones recommended" note under the buttons.
