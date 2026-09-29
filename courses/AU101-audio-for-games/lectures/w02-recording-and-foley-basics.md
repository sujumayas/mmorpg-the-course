# AU101 · Week 02 — Recording and Foley Basics

**Why this matters:** Most game sounds start as a recording of something ordinary: a boot on gravel, celery snapped near a microphone, a door hinge slowed down until it groans like a dungeon gate. A bad recording limits every sound you build on it, and no plugin can put back what the microphone never captured. This week you learn how to capture sound that survives the editing and pitch changes games put it through.

**You will be able to:**
- Compute the highest frequency, dynamic range and file size of a recording from its sample rate and bit depth.
- Predict how much high-frequency content survives when a recording is pitched down, and choose a recording sample rate to match.
- Set microphone distance and input gain for a clean take, using the inverse-square rule and a headroom target in dBFS.
- Plan and run a small foley session with consistent file names and room tone.

**Before class:** Collins, *Game Sound* (2008), chapter 2. As you read, list every limit on memory, sample rate or channels the text mentions, and keep the list for section 3. Skim the Universal Category System overview page (universalcategorysystem.com) so you know what a CatID is. Bring headphones and a phone that can record.

**Prerequisites from earlier courses:** [AU101 week 1](w01-what-sound-does-feedback-space-emotion.md) (frequency, amplitude, the three jobs of sound). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (decibels as `20 · log10` of an amplitude ratio). [MA101 week 10, sin and cos](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) (a wave as `sin(2πft)`). [CS101 week 9, delta time and fixed timesteps](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (a simulation that only looks at the world at fixed moments).

**Interactive:** [examples/w02-sample-rate-and-pitch.html](../examples/w02-sample-rate-and-pitch.html). Keep it open during section 3.

---

## 1. From air to numbers

A microphone is a **transducer**. It turns air pressure into voltage. An **audio interface** (or the chip inside your phone) turns that voltage into numbers. It measures the voltage many thousands of times per second and stores each measurement as an integer. Two settings define that conversion.

- **Sample rate** (`fs`) is how many measurements per second, in hertz. Common rates are 44,100 Hz (the CD rate), 48,000 Hz (the usual rate for video and games) and 96,000 or 192,000 Hz for recording that will be heavily processed.
- **Bit depth** (`N`) is how many bits each measurement gets. 16-bit gives 65,536 possible levels. 24-bit gives about 16.8 million.

A recording's level is measured in **dBFS**, decibels relative to **full scale**. 0 dBFS is the largest number the format can store. Everything real is below it, so levels are negative: −6 dBFS is half of full-scale amplitude, −20 dBFS a tenth. If the input goes above full scale, the converter stores the maximum value for every sample that should have been bigger. That flat-topped wave is **clipping**. It sounds like crackle or harsh distortion, and it is permanent.

### Microphones in one page

You will meet two main types.

- **Dynamic** microphones move a coil in a magnet. They are rugged, handle very loud sources (a slammed door, a gunshot at a range) and pick up less room sound. They are less sensitive to quiet detail.
- **Condenser** microphones measure a thin charged membrane. They need power (usually "phantom power" from the interface), capture quiet detail and high frequencies well, and hear the room more. Most foley is recorded with condensers.

Each microphone also has a **polar pattern**, how sensitive it is from each direction.

- **Omnidirectional** hears all around equally. Good for ambience, bad in a noisy room.
- **Cardioid** (heart-shaped) hears the front and rejects the back. The default for foley and voice.
- **Shotgun** (supercardioid or hypercardioid with a long tube) is narrow at the front. Used outdoors and for aiming at one source among many.
- **Binaural** is a pair of microphones inside the ears of a model head. Week 1 showed how Hellblade used it to put voices behind the player. It only works for headphone playback of the recording as it is. Games that position sounds in 3D at runtime usually record in mono and let the engine do the placement.

That last point matters for everything you record this term. **Most game sound effects are recorded and exported in mono.** The engine pans, attenuates and spatialises them at runtime (week 7). A stereo recording of a footstep bakes in one position, which is wrong the moment the player turns.

## 2. Distance, gain and headroom

### The inverse-square rule

Sound from a small source spreads over a sphere. Double the distance and the same energy covers four times the area, so the level drops by about 6 dB. In general, moving the microphone from distance `d1` to distance `d2` changes the direct sound level by

```
change in dB = 20 × log10(d1 / d2)
```

Moving from 60 cm to 15 cm is a factor of 4, so +12 dB. The room's background noise (fridge hum, traffic, ventilation) does not care where your microphone is, so it stays the same. Your **signal-to-noise ratio** improves by the full 12 dB. That is why foley artists work close, often 15 to 40 cm from the prop. It is the cheapest noise reduction there is.

Close has limits. Directional microphones boost bass when very close, an effect called **proximity effect**. It can make a footstep boom unnaturally. Bursts of air from a mouth or a swung object hit the diaphragm as **plosives**, loud low thumps. And at very close range, small movements of the prop change the level a lot, because 5 cm is a big fraction of 10 cm. A consistent distance between takes matters more than the exact number.

### Room sound

Every room adds reflections. A tiled bathroom adds bright, long ones, and a bedroom full of clothes adds very few. For foley you want very little room, because you will add the right space later with reverb (week 7), and you cannot subtract the wrong one. Practical fixes, in order of cost: get closer, hang duvets or blankets around the recording spot, record in a wardrobe full of clothes, rent a treated booth.

### Gain staging and headroom

**Gain** is the amplification before the converter. Set it too low and the sound sits near the noise floor. Set it too high and peaks clip. The margin between your loudest peak and 0 dBFS is **headroom**.

With 24-bit recording, headroom is almost free. The format's theoretical range is about 144 dB (section 3), far more than any real room or microphone delivers, so a take that peaks at −12 dBFS still sits well above the converter's own noise. A good default for foley is **peaks between −12 and −6 dBFS**. Performers always hit harder on the real take than in the soundcheck, and that margin absorbs it.

Clipping cannot be fixed afterward. Tools that "declip" guess at the missing tops of the wave and often fail on sharp transients like impacts. If a take clips, record it again.

## 3. Worked example: why record at 96 kHz for a game that plays at 48 kHz?

### The hook

The original Doom (id Software, 1993) stored its sound effects as 8-bit samples played at 11,025 Hz. You can read both numbers in the Linux source release. The mixer defines `SAMPLERATE` as 11025 and reads each effect's raw data as unsigned 8-bit values. The shotgun and the imp's screech sound crunchy and dull next to a modern recording, and players still recognise them decades later.

Now jump forward. Sound designers today routinely record props at 96 or 192 kHz, even though the game's mixer runs at 44.1 or 48 kHz and nobody can hear above about 20 kHz. That looks like waste: four times the storage for sound nobody hears. The model below shows why it is not, and why Doom's numbers are closer to your future than you think.

### The model

Three formulas, each with every symbol named.

**1. The Nyquist limit.** A signal sampled at `fs` samples per second can only represent frequencies below half the rate:

```
f_nyquist = fs / 2
```

Before sampling, a filter removes content above `f_nyquist`. If it did not, that content would fold back as false lower tones, called **aliasing**.

**2. Bit depth and dynamic range.** Each extra bit doubles the number of levels, which is about 6.02 dB:

```
dynamic range ≈ 6.02 × N dB
```

**3. Storage.** Uncompressed audio costs

```
bytes per second = fs × (N / 8) × channels
```

Now the part that matters for games. Games constantly play sounds at a different pitch from the recording. Godot's `AudioStreamPlayer.pitch_scale` is documented as a multiplier of the stream's sample rate, where 0.5 halves the pitch. Halving the pitch halves *every* frequency in the sound, including the top of its range. If the highest frequency in the recording is `f_top`, then after playing at pitch factor `p`:

```
f_top_after = p × f_top
f_top       = min(fs / 2, f_mic, f_source)
```

- `p` is the pitch factor (1 is unchanged, 0.5 is one octave down, 0.25 two octaves down).
- `f_mic` is the highest frequency your microphone captures. Check its spec sheet. Many are specified to 20 kHz; some specialist models go much higher.
- `f_source` is the highest frequency the prop actually makes. Keys, glass, metal scrapes and cloth have strong content above 20 kHz. A bass drum has almost none.

The recording's sample rate is one of three limits. Pitching down pulls whatever top you captured down into the audible range, and everything above it stays empty.

### Numbers you can check

First the formats, one minute of mono audio:

| Format | Nyquist | Dynamic range | Bytes per second | One minute (MB) |
|---|---|---|---|---|
| Doom (1993), 11,025 Hz, 8-bit | 5,512.5 Hz | 48 dB | 11,025 | 0.66 |
| CD, 44,100 Hz, 16-bit | 22,050 Hz | 96 dB | 88,200 | 5.29 |
| 48,000 Hz, 24-bit | 24,000 Hz | 144 dB | 144,000 | 8.64 |
| 96,000 Hz, 24-bit | 48,000 Hz | 144 dB | 288,000 | 17.28 |
| 192,000 Hz, 24-bit | 96,000 Hz | 144 dB | 576,000 | 34.56 |

Check one row by hand. 48,000 × 3 bytes = 144,000 bytes per second. Times 60 is 8,640,000 bytes, or 8.64 MB.

Now the pitch problem. Take a jangling key ring with content up to 60 kHz, recorded with a microphone that captures up to 40 kHz. You want a heavy, slow "dungeon keys" version at half and quarter pitch.

```python
def top_after_pitch(fs, f_mic, f_source, pitch):
    """Highest frequency left in a recording after playing it at `pitch`."""
    return pitch * min(fs / 2, f_mic, f_source)

F_MIC, F_KEYS = 40_000, 60_000
for fs in (48_000, 96_000, 192_000):
    tops = [top_after_pitch(fs, F_MIC, F_KEYS, p) for p in (1.0, 0.5, 0.25)]
    print(f"{fs:>7} Hz: " + "  ".join(f"{t / 1000:5.1f} kHz" for t in tops))
```

It prints:

```
  48000 Hz:  24.0 kHz   12.0 kHz    6.0 kHz
  96000 Hz:  40.0 kHz   20.0 kHz   10.0 kHz
 192000 Hz:  40.0 kHz   20.0 kHz   10.0 kHz
```

| Recorded at | Pitch 1.0 | Pitch 0.5 (one octave down) | Pitch 0.25 (two octaves down) |
|---|---|---|---|
| 48 kHz | 24 kHz (fills the audible range) | 12 kHz (top 8 kHz of hearing empty) | 6 kHz (close to Doom's 5.5 kHz) |
| 96 kHz | 40 kHz | 20 kHz (full audible range) | 10 kHz |
| 192 kHz | 40 kHz (microphone-limited) | 20 kHz | 10 kHz |

Three readings.

1. At normal pitch all three recordings sound the same to a human. The extra content above 20 kHz is inaudible.
2. One octave down, the 48 kHz recording loses the top 8 kHz of hearing. The keys sound muffled, as if heard through a wall. The 96 kHz recording still fills the whole range.
3. Two octaves down, the 48 kHz recording has about the bandwidth of a 1993 Doom sample. And 192 kHz buys nothing over 96 kHz here, because the microphone stops at 40 kHz. The chain is only as wide as its narrowest link.

### A visual you can move

Open [`examples/w02-sample-rate-and-pitch.html`](../examples/w02-sample-rate-and-pitch.html). The page synthesises a key-jingle sound with energy up to 60 kHz and "records" it at the sample rate you pick. The left view shows the spectrum of the recording, frequency against level, with a shaded band from 0 to 20 kHz marking what humans hear. The right view shows the spectrum after your pitch change. Set the rate to 48 kHz and drag pitch from 1.0 to 0.25. On the left, nothing changes. On the right, the top edge of the sound slides down through the audible band and leaves an empty region above it. Switch to 96 kHz and drag again. The empty region only appears below pitch 0.5. Press play to hear both versions side by side. A bit-depth selector adds quantisation noise so you can hear 8-bit Doom-style grain against 24-bit silence.

### Cross-game recognition

**Doom (1993).** 11,025 Hz and 8 bits were a memory and CPU budget. The Linux source mixes eight channels of those samples into a 16-bit stereo buffer. The low rate caps every effect at 5.5 kHz, and the 8-bit depth leaves audible hiss under quiet tails. The designers made the sounds loud, short and punchy, which hides both limits. Your two-octaves-down recording lands in the same place by a different route.

**Godot 4.7 (current engine documentation).** The project setting `audio/driver/mix_rate` defaults to 44,100 Hz, and `pitch_scale` multiplies the sample rate. A pitch scale of 0.5 on a 48 kHz file plays it one octave lower and twice as long, with the top frequency halved exactly as the model says. Unity, FMOD and Wwise all expose the same kind of multiplier under different names. The pitch variation you coded in CS101 week 14 (±2 semitones, a factor from 0.89 to 1.12) barely moves the top edge. Creature designs that drop a sound by one or two octaves move it a lot.

**VALORANT (Riot Games, 128-tick servers since launch in 2020).** The same sampling idea applies to game state. Riot's tech blog explains that the servers run at 128 ticks per second, so each tick has 7.8125 ms to process. The server looks at the world 128 times a second, just as a converter looks at a voltage 48,000 times a second. Anything that happens and un-happens between two ticks is invisible to it, the game-state version of content above Nyquist. CS101 week 9's fixed timestep is the same structure in your own game loop, and MMO302 week 5 compares tick rates across genres.

In all three, ask one question: *what is the fastest change this system can represent, and what happens to anything faster?*

### Eyes-open design judgment

- **Record at 96 kHz when you plan to pitch down, slow down or stretch.** Creature voices, magic whooshes, giant footsteps and slow-motion effects all qualify. The extra content becomes audible detail after the shift.
- **Record at 48 kHz when the sound will play at roughly its natural pitch.** UI clicks, dialogue and most footsteps gain nothing from higher rates, and the files are half the size.
- **Match the microphone to the rate.** A 192 kHz recording through a microphone that stops at 20 kHz is a 192 kHz file full of nothing. Spend on the microphone before the sample rate.
- **Ship at the game's rate, not the recording's.** Export the final edited sound at 48 kHz (or whatever your engine mixes at), then let the engine compress it. The high-rate recording is a source file, like a layered image file for art. Keep it in your source archive, not in the build.
- **Pitching down is not the only way to get weight.** Layering a low-frequency element under a normal-pitch recording (week 4) or synthesising a sub-bass thump (week 3) often sounds better than an extreme pitch shift, and costs nothing in recording.

## 4. Foley: performing sound to picture

**Foley** is sound performed and recorded to match on-screen action: footsteps, cloth rustle, handling of objects. The practice is named after Jack Foley, who developed live, in-sync effects performance for Hollywood films starting in the late 1920s. Film foley artists watch the picture and perform along with it. Game foley is usually performed as a library of variations, because the game decides at runtime which step or rustle to play.

### The three foley families

1. **Footsteps.** One set per surface and shoe type: concrete, gravel, wood, metal grate, grass, snow, water. Each set needs walk, run, jog-stop, scuff and land variants, and enough takes of each that the game can avoid repeats (week 4's topic).
2. **Cloth and gear.** The rustle of clothing and equipment as a character moves. Often a few long takes of movement, later cut into short pieces and layered under footsteps.
3. **Props.** Handling sounds: picking up, putting down, opening, dropping. Most interface and inventory sounds are prop foley in disguise. A backpack's zip becomes "open inventory".

### Foley is a performance

Good foley is a performance. Match the weight and speed of the character. A heavy knight's step is slow heel then slap of the whole sole, a thief's is a light roll from toe. Record more takes than you think you need (at least five per action, usually ten). Vary the performance slightly between takes, because variety you record is cheaper than variety you fake in software.

Substitution is half the craft. Snapping celery or a bundle of dry pasta sounds more like breaking bones on a microphone than the real thing would. A leather wallet flexed near the microphone makes armour creak. Cornstarch in a leather pouch, squeezed, is a classic snow-footstep trick. Try things, record them, and judge by ear on headphones, never by what the prop is.

### Session discipline

A recording you cannot find is a recording you do not have. Every session should produce:

- **A slate** at the start of each file: say what the take is ("gravel, boots, walk, take three"). It costs two seconds and saves hours.
- **Room tone:** 30 seconds of the empty room with everyone still. You will use it to measure the noise floor and to fill gaps in edits without audible dropouts.
- **Consistent file names.** The Universal Category System (UCS, version 8.2.1, January 2024) is a public-domain category list used by sound libraries. Each category has a short CatID, for example `WOODHndl` for wood handling, that begins the file name. This course uses a simplified version: `CatID_description_initials_NN.wav`, for example `FOOTGrvl_boot-walk_AB_03.wav`.
- **A log** with take numbers and a one-word judgement ("good", "clip", "car passed").

## In-class activity (25 minutes)

Groups of three, one phone recording app per group (most can record uncompressed WAV; if not, use the highest quality setting and note the format). One set of keys, one book, one sheet of paper.

1. **Distance ladder (10 min).** Record the same key jingle at 15 cm, 30 cm and 60 cm, three takes each, same shake. Then record 10 seconds of room tone.
2. **Measure (10 min).** In Audacity (free), select each take and use Analyze > Contrast or read the peak level. Fill a table: distance, peak dBFS, room tone level, difference.
3. **Compare to the model (5 min).** The inverse-square rule predicts +6 dB for each halving of distance. How close did you get? Name one reason for the gap (the room, the prop moving, the phone's automatic gain).

Expected output: a 9-row table and a one-sentence explanation of the gap. Phone apps often apply automatic gain control, which flattens the difference. Spotting that is a good result, not a failure.

## Common misconceptions

- **"Higher sample rate always sounds better."** At normal playback pitch, content above 20 kHz is inaudible. Higher rates pay off only when the sound will be pitched down or slowed, and only if the microphone and source have content up there.
- **"24-bit is louder than 16-bit."** Bit depth sets the floor (how quiet the quietest detail can be), not the ceiling. Both formats peak at the same 0 dBFS.
- **"Record as hot as possible."** That advice dates from 16-bit and tape. With 24-bit, peaks at −12 to −6 dBFS lose nothing audible and protect you from clipping.
- **"Stereo is richer, so record effects in stereo."** A stereo footstep has its position baked in. The engine positions mono sounds in 3D at runtime. Record ambiences in stereo, point sources in mono.

## Check yourself

1. A sound recorded at 44.1 kHz is played at `pitch_scale` 0.6. Assuming the microphone and source both reach past Nyquist, what is the highest frequency left? How much of the 0 to 20 kHz audible band is empty?
2. Your microphone captures up to 20 kHz. Is there any benefit in recording at 96 kHz instead of 48 kHz for a creature voice you will pitch down an octave? Use the model.
3. You record a door creak at 40 cm and it peaks at −24 dBFS. Where should you move the microphone to bring the peak to about −12 dBFS without touching gain? What else changes when you do?
4. A game ships 600 unique one-second mono sound effects. How many megabytes is that uncompressed at 48 kHz, 16-bit? At 96 kHz, 24-bit? Which one should ship?

<details>
<summary>Answers</summary>

1. `f_top = 44,100 / 2 = 22,050` Hz. After pitch 0.6 it is `0.6 × 22,050 = 13,230` Hz. The band from about 13.2 kHz to 20 kHz, roughly 6.8 kHz of it, is empty.
2. No. `f_top = min(fs/2, f_mic, f_source) = 20` kHz at either rate, so after pitch 0.5 the top is 10 kHz in both cases. The microphone is the limit; the higher rate only costs storage.
3. You need +12 dB, which is a distance factor of 4 (`20 × log10(4) ≈ 12`), so move to 10 cm. The room noise stays put, so the signal-to-noise ratio also improves by 12 dB. But at 10 cm expect more proximity effect (bass boost) and more sensitivity to small movements of the door.
4. 48 kHz, 16-bit: `48,000 × 2 = 96,000` bytes per second, times 600 = 57.6 MB. 96 kHz, 24-bit: `288,000 × 600` = 172.8 MB. Ship the 48 kHz version (compressed further by the engine) and keep the 96 kHz originals in the source archive.

</details>

## Lab / assignment hook

[Lab 02, foley session and level check](../labs/lab02.md). Implement three level-measuring functions in Python, then record a 12-file foley set (footsteps on two surfaces, cloth, three props, room tone) to a fixed specification and prove it meets the spec with the provided checker. The files become source material for the SFX pack.

## Sources

- id Software, DOOM source code release (Linux version 1.10, 1997 release of the 1993 game), `linuxdoom-1.10/i_sound.c`: `SAMPLERATE 11025`, eight mixing channels, effects read as unsigned 8-bit data, 16-bit stereo mix buffer. https://github.com/id-Software/DOOM
- Godot Engine documentation (Godot 4.7), `AudioStreamPlayer.pitch_scale` (multiplier of the stream's sample rate; 0.5 halves the pitch) and `ProjectSettings.audio/driver/mix_rate` (default 44,100 Hz).
- Riot Games Technology blog, "VALORANT's 128-Tick Servers" (31 August 2020, date checked on technology.riotgames.com 29 September 2026). 128 ticks per second; 7.8125 ms per frame of server work.
- Universal Category System, universalcategorysystem.com. Public-domain category list for sound effects, version 8.2.1 (January 2024), CatID example `WOODHndl`.
- Wikipedia, "Jack Foley (sound effects artist)". Developed live, synchronised sound-effect performance for film; the trade is named after him.
- Wikipedia, "Hellblade: Senua's Sacrifice". Voices recorded binaurally (see week 1).
- Collins, K. (2008). *Game Sound*. MIT Press. Chapter 2 (course reading).

## Interactive spec: examples/w02-sample-rate-and-pitch.html

**Purpose.** Show that pitching a recording down drags its top frequency into the audible band, so the recording's sample rate (and microphone) decide how bright the pitched sound can be. The one insight: at pitch 1.0 a 48 kHz and a 96 kHz recording look and sound identical in the audible band; at pitch 0.5 only the 96 kHz one still fills it.

**Layout.** Two linked spectrum views side by side (stacked on mobile), controls below, readouts beside each view.

- **Left, "Recording".** x axis frequency 0 to 100 kHz on a linear scale, y axis level in dB (−90 to 0). Shade 0-20 kHz in `--paper-2` and label it "audible". Draw the recording's spectrum envelope in `--steel`. Draw a vertical line at `f_top = min(fs/2, f_mic, f_source)` labelled with its value.
- **Right, "After pitch".** Same axes, but x axis 0 to 24 kHz (the game's 48 kHz mix). Draw the pitched spectrum (each frequency multiplied by `p`) in `--ochre`, and shade the empty region from `p × f_top` to 20 kHz in a hatched `--blood` at low opacity, labelled "empty: X kHz".

**Model (exact).**

```
f_top = min(fs / 2, f_mic, f_source)
f_top_after = p × f_top
empty_kHz = max(0, 20 − f_top_after / 1000)
bytes_per_min_mono = fs × (N / 8) × 60
dynamic_range_dB = 6.02 × N
```

The synthetic source spectrum for drawing: level `L(f) = −6 − 18 × (f / 60 kHz)` dB for `f ≤ f_source`, and −90 dB above. Cut at `f_top`.

**Controls.**
- Sample rate: segmented control 11,025 / 22,050 / 44,100 / 48,000 / 96,000 / 192,000 Hz. Default 48,000.
- Bit depth: 8 / 16 / 24. Default 24.
- Microphone limit `f_mic`: slider 16-100 kHz, step 1 kHz. Default 40 kHz.
- Source content `f_source`: preset buttons "keys (60 kHz)", "door creak (30 kHz)", "kick drum (8 kHz)". Default keys.
- Pitch `p`: slider 0.25-1.0, step 0.01, with tick marks at 0.25, 0.5, 1.0. Default 1.0.
- Buttons "play original" and "play pitched".

**Audio (procedural, no files).** Build a key-jingle with an `OfflineAudioContext` at 192,000 Hz if the browser supports it (fall back to the highest supported rate and show a note): 40 sine partials with random frequencies between 2 kHz and `f_source`, each with a random start in the first 300 ms and an exponential decay of 80-250 ms, amplitude falling with frequency to match `L(f)`. Low-pass the result at `f_top` with a steep `BiquadFilterNode` chain (4 lowpass stages). Quantise to `N` bits (`round(x × 2^(N−1)) / 2^(N−1)`) with no dither so 8-bit grain is audible. Play pitched versions with `AudioBufferSourceNode.playbackRate = p` through the page's normal context. Fix the random seed so every student hears the same jingle.

**Readouts (exact).** Nyquist in Hz, `f_top`, `f_top_after` (kHz, 1 decimal), empty band in kHz, dynamic range in dB (1 decimal), bytes per minute mono and MB per minute (2 decimals).

**Test values (must match).**
- 48,000 Hz, keys, mic 40 kHz, p 1.0: `f_top` 24.0 kHz, after 24.0, empty 0.0.
- 48,000 Hz, p 0.5: after 12.0 kHz, empty 8.0 kHz.
- 48,000 Hz, p 0.25: after 6.0 kHz, empty 14.0 kHz.
- 96,000 Hz, p 0.5: `f_top` 40.0, after 20.0, empty 0.0.
- 192,000 Hz, p 0.25: after 10.0 kHz (microphone-limited).
- 11,025 Hz, 8-bit: Nyquist 5,512.5 Hz, dynamic range 48.2 dB, 661,500 bytes per minute (0.66 MB).
- 48,000 Hz, 24-bit: 8,640,000 bytes per minute (8.64 MB), 144.5 dB.

**First screen.** 48 kHz, keys, p = 0.5, so the empty hatched band (8.0 kHz) is visible immediately, with a one-line caption: "One octave down, the top of a 48 kHz recording falls to 12 kHz."

**Rules.** Audio starts only on a user gesture. Keyboard-accessible controls with visible focus. Respect `prefers-reduced-motion` and `prefers-color-scheme`. Shared tokens from `templates/interactive-tokens.css`. No external audio.
