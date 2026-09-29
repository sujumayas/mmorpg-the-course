# AU101 · Week 11 — UI Sound Design

**Why this matters:** UI sounds are the sounds players hear most often. An MMO player may click a vendor button two hundred times in an evening and hear the same "sold" chime every time. If those sounds are loud, long or vague, players turn the UI volume to zero, and you lose a channel that could have told them a purchase failed or a streak is building.

**You will be able to:**
- Compute the pitch, playback rate and duration of each step of a streak ladder, and choose its length, cap and reset rule.
- Design a UI sound family as a small language, with a written rule for what pitch direction, length and level mean.
- Estimate a sound's repetition exposure per session and set its length and level from it.
- Compute audio buffer latency and decide when a UI sound should fire in a networked action.

**Before class:** Collins, *Game Sound* (2008), chapters 1-3 (the course reading). Note any early arcade or console sound that worked as interface feedback rather than as part of the game world. Open any game's main menu and settings screen with your eyes closed and try to tell, by ear alone, which button you pressed and whether it worked.

**Prerequisites from earlier courses:** [GD101 week 12, feedback, juice, clarity and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) (confirm, report, forecast; one meaning per signal; rare events get the biggest signal). [CS101 week 14, polish pass](../../CS101-programming-for-games-i/lectures/w14-polish-pass-sound-particles-screen-shake.md) (pitch in semitones and `pitch_scale`, which changes pitch and length together). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (`2^(s/12)` is an exponential in `s`). From this course, [week 1](w01-what-sound-does-feedback-space-emotion.md) (sounds in the world and outside it), [week 3](w03-synthesis-for-sfx.md) (pitch contour carries meaning in sfxr's presets), [week 4](w04-layering-and-variation.md) (variation, which this week explains why UI sounds usually avoid) and [week 10](w10-mixing-ducking-and-priority.md) (ducking, priority).

**Interactive:** [examples/w11-streak-ladder.html](../examples/w11-streak-ladder.html). Keep it open during section 2.

---

## 1. What a UI sound is for

A **UI sound** is any sound attached to the interface rather than to the game world: menu hovers and clicks, inventory drags, notifications, quest-complete fanfares, the chime when a timer runs out. Week 1 called these non-diegetic sounds, because nobody in the game world hears them.

They do the same three feedback jobs GD101 week 12 named, in a very compressed form:

- **Confirm.** "Your press registered." Hover, click, toggle.
- **Report.** "Something changed." Item sold, mail arrived, level up, purchase failed.
- **Forecast.** "Something is coming." A queue pop, a cooldown about to finish, a timer entering its last ten seconds.

Two research traditions from human-computer interaction give you vocabulary for how a sound can carry that meaning.

**Auditory icons** (Gaver, 1986) use everyday sounds that resemble the event. A paper crumple for deleting a file, a coin clink for gold, a door creak for opening a bag. The player understands them on first hearing because they already know the real sound. They are hard to extend: what does "mail arrived" sound like in a fantasy world?

**Earcons** (Blattner, Sumikawa and Greenberg, 1989) are short abstract musical motifs: a few notes with a chosen pitch, rhythm and timbre. They mean nothing at first and have to be learned. In exchange they combine. Once "rising two notes" means "success", you can build "big success" with three rising notes and "success, but for someone else" with the same two notes on a softer timbre. Blattner and colleagues describe families of earcons that share a motif and vary one parameter at a time.

Most shipped games mix the two. The gold clink is an auditory icon. The quest-complete jingle is an earcon. The important thing is to decide which parameter carries which meaning and then never break the rule.

### A UI family is a small language

Write the rules down, just like a style guide for text. A typical family uses a few conventions:

- **Direction of pitch.** Rising means forward, open, gain, success. Falling means back, close, loss, cancel. Week 3 found the same rule built into sfxr's presets, where power-ups always slide up and hurt sounds always slide down.
- **Consonance.** A major third or perfect fifth reads as settled. A semitone clash or a tritone reads as wrong. Error sounds often use a small dissonant interval or a flat buzz.
- **Length and level scale with importance.** Hover is tiny. Level-up is big.
- **Timbre marks the category.** All inventory sounds share a wooden or cloth texture. All social notifications share a bell.

These are conventions, not laws of hearing. A rising siren means danger, not success. Your family only has to be consistent with itself and not fight what players already know from the genre.

## 2. Worked example: the streak ladder

### The hook

In Super Mario 64, each course hides eight red coins. Collect all eight and a star appears. Every version except the original 1996 Japanese release plays the red-coin sound one step higher for each coin collected, so by the seventh coin you can *hear* that you are nearly done. The original Japanese release did not. Every red coin played the same sound. The community's decompilation of the game shows both code paths side by side, one playing an identical sound for every coin and the other adding the coin count to the sound's pitch.

The coins, the counter and the star are unchanged. Only the sound changed, and it turned a count into a feeling of rising tension. How do you design a ladder like that, and where should it stop?

### The model

A **streak ladder** plays the `n`-th event of a streak at a pitch chosen from a scale:

```
s(n)   = scale[ min(n − 1, len(scale) − 1) ]      (cap mode)
       = scale[ (n − 1) mod len(scale) ]           (wrap mode)
f(n)   = f0 · 2^(s(n) / 12)
rate(n) = 2^(s(n) / 12)                             (if you resample a recorded sound)
dur(n)  = dur0 / rate(n)                            (resampling also shortens it)
n resets to 1 when the time since the previous event is longer than T_reset
```

- `n` is the position in the current streak, starting at 1.
- `scale` is a list of semitone offsets. A major scale is `[0, 2, 4, 5, 7, 9, 11, 12]`.
- `s(n)` is the offset in semitones for step `n`.
- `f0` is the frequency of the first step in hertz, `f(n)` the frequency of step `n`.
- `rate(n)` is the playback-rate multiplier if you pitch a recorded sample instead of synthesising it. CS101 week 14 showed that `pitch_scale` in Godot changes pitch and length together; `dur0` is the sample's original length.
- `T_reset` is the gap, in seconds, after which the streak starts over.

Twelve semitones double the frequency, which is one octave. That is the whole reason the formula uses `2^(s/12)`.

### Numbers you can check

With `f0 = 523.25` Hz (the note C5), a major scale and a 200 ms recorded chime:

```python
F0 = 523.25                        # C5, the first note of the ladder
MAJOR = [0, 2, 4, 5, 7, 9, 11, 12]  # semitones above F0

for n, s in enumerate(MAJOR, start=1):
    ratio = 2 ** (s / 12)
    print(f"step {n}: +{s:2d} st  ratio {ratio:.3f}  {F0 * ratio:7.2f} Hz  "
          f"200 ms sample lasts {200 / ratio:5.1f} ms")
```

```
step 1: + 0 st  ratio 1.000   523.25 Hz  200 ms sample lasts 200.0 ms
step 2: + 2 st  ratio 1.122   587.33 Hz  200 ms sample lasts 178.2 ms
step 3: + 4 st  ratio 1.260   659.25 Hz  200 ms sample lasts 158.7 ms
step 4: + 5 st  ratio 1.335   698.45 Hz  200 ms sample lasts 149.8 ms
step 5: + 7 st  ratio 1.498   783.99 Hz  200 ms sample lasts 133.5 ms
step 6: + 9 st  ratio 1.682   880.00 Hz  200 ms sample lasts 118.9 ms
step 7: +11 st  ratio 1.888   987.76 Hz  200 ms sample lasts 105.9 ms
step 8: +12 st  ratio 2.000  1046.50 Hz  200 ms sample lasts 100.0 ms
```

Three things in the table are design decisions in disguise.

1. **Eight steps span exactly one octave.** A major scale fits eight events (like eight red coins) perfectly, and step 8 lands on the same note name as step 1, one octave up. That sounds like arrival. A ladder of five steps might use `[0, 2, 4, 7, 12]` (a major pentatonic run to the octave) to get the same arrival.
2. **Resampling halves the length at the top.** If you pitch a recorded chime instead of synthesising it, step 8 lasts half as long as step 1. For a 200 ms chime that is fine. For a 40 ms click it becomes a 20 ms tick that may lose its body. Synthesised or pre-rendered steps avoid the problem.
3. **Step size is not constant in hertz.** From step 1 to 2 the pitch rises 64 Hz. From step 7 to 8 it rises 59 Hz, and from step 5 to 6 it rises 96 Hz. The ear hears semitones, not hertz. That is why the formula works in semitones and why a ladder that added a fixed 50 Hz per step would sound like it slowed down as it climbed.

Compare three settings for an 8-event streak:

| Mode | Semitones for steps 1-8 | Top frequency (from 523.25 Hz) | What it sounds like |
|---|---|---|---|
| Same | 0, 0, 0, 0, 0, 0, 0, 0 | 523.25 Hz | A counter with no direction (the 1996 Japanese red coins) |
| Chromatic | 0, 1, 2, 3, 4, 5, 6, 7 | 783.99 Hz | Rising but tense; only reaches a fifth |
| Major scale | 0, 2, 4, 5, 7, 9, 11, 12 | 1,046.50 Hz | Rising and resolving on the octave |

### A visual you can move

Open the interactive. Press the big button (or space) to collect. Each press plays the next step, lights a rung on a ladder drawn to scale in semitones, and shows its frequency, ratio and duration. The second view plots the same steps in hertz, so you can see the rungs spread out as they rise even though they sound evenly spaced. Switch between Same, Chromatic, Major and Pentatonic. Set the streak to 12 events and switch between Cap and Wrap to hear the difference between "stuck at the top" and "starting again". Then drag `T_reset` down to 0.3 s and try to keep a streak going.

### Cross-game recognition

**Peggle (PopCap, 2007).** Each shot bounces a ball through a field of pegs, and the peg-hit sound rises as the ball hits more of them. A 2009 interview with co-creator Sukhbir Sidhu lists that rising sound among the game's signature sounds. Sidhu also explained that one goal for the sound effects was to blend with the background music, so that randomly triggered effects could act as instruments in the soundtrack. In our model, `n` counts the pegs hit, the start of a new shot is the natural place to reset instead of a timer, and the scale is chosen to fit the music.

**Space Invaders (Taito, 1978).** The invaders' marching sound speeds up as you destroy them. The effect started as a hardware accident: the processor drew each frame faster when fewer aliens remained, so the aliens and their sound sped up together. Designer Tomohiro Nishikado kept it because it made the game more interesting. Here the ladder runs on **tempo** instead of pitch, and `n` counts down (invaders remaining) instead of up. It is the same idea: map progress toward the end onto a sound parameter that only moves one way, so the player feels the end approaching without reading a number.

**Super Mario 64 itself shows the "same" control condition.** The Japanese and international releases are the same game with and without a ladder. That is as close to an A/B test as you will find in a shipped product.

### Eyes-open design judgment

- **Decide the length before the scale.** Know the longest streak players can reach. If the answer is "unbounded" (a combo counter), choose cap or wrap deliberately. Cap is honest but the top step loses meaning once players sit on it. Wrap keeps moving but can sound like a reset the player did not earn. A third option is to cap the pitch and grow something else (add a harmony note, raise the level by 1 dB) for steps past the top.
- **Pick `f0` for the top, not the bottom.** Two octaves above 1 kHz gets shrill and fatiguing. Start low enough that the last step still sits comfortably.
- **Match the music, or step outside it on purpose.** A ladder in the key of the music (Peggle's approach) sounds like part of the score. A ladder that clashes stands out. Clashing is fine for warnings, and tiring for rewards.
- **Pair it with a visual.** The Super Mario 64 decompilation also spawns an on-screen number for each red coin before the last. A ladder alone fails players who are hard of hearing or playing muted. Week 13 covers this properly.
- **Resetting is feedback too.** When a streak breaks, the next event plays the bottom step. That drop is a "you lost it" message. Make sure `T_reset` matches the design rule players are told, or the sound will teach the wrong rule.

### Check yourself (worked example)

1. With `f0 = 440` Hz and a major scale, what frequency does step 5 play? Step 8?
2. A 150 ms recorded pickup is resampled for a ladder that climbs two octaves. How long is the top step?
3. A combo can reach 30 hits. Using a major-scale ladder in cap mode, from which hit onward does the pitch stop rising? What would you add to keep hits 9-30 feeling different?

<details>
<summary>Answers</summary>

1. Step 5 is +7 semitones: `440 × 2^(7/12) ≈ 659.26` Hz. Step 8 is +12: 880 Hz.
2. Two octaves is a rate of 4, so `150 / 4 = 37.5` ms.
3. From hit 8 onward every hit plays +12. Options: add a harmony note at hit 10 and another at 20; raise level by 1 dB per 5 hits up to a limit; switch to a brighter timbre; or change the rule so the ladder climbs every second hit.

</details>

## 3. The repetition budget

UI sounds repeat more than any other sound in the game. That changes how you design them.

Estimate the exposure for each UI event:

```
plays per session = events per minute × minutes per session
```

An MMO player clearing their bags at a vendor might sell 20 items a minute for 10 minutes: 200 "sold" sounds. Hovering over an action bar with a mouse can trigger hover sounds 60 or more times a minute. Across a 2-hour session that is 7,200 hovers. A level-up happens a handful of times per session.

The rule that follows is the one GD101 week 12 gave for visual feedback: **the more often an event happens, the smaller its signal.** A reasonable starting table for a family, which you will adjust by ear:

| Event | Typical rate | Length | Peak level | Character |
|---|---|---|---|---|
| Hover | many per minute | 20-40 ms | about −30 dBFS | Soft tick, little high-frequency content |
| Click / select | tens per minute | 40-80 ms | about −20 dBFS | Clear transient, one pitch |
| Confirm / cancel | a few per minute | 100-200 ms | about −14 dBFS | Two-note rise or fall |
| Error | rare | 150-300 ms | about −12 dBFS | Low, dissonant, distinct from cancel |
| Level up, quest complete | a few per session | 1-3 s | about −8 dBFS | Full earcon, may duck music (week 10) |

These levels are before the UI bus fader. They set the *relationships* inside the family, which is what the player learns.

### Why UI sounds usually skip variation

Week 4 taught you to vary pitch and volume so repeated sounds don't feel mechanical. UI is the exception. A UI sound is a symbol. The player should recognise "sold" instantly, and a random ±2 semitones would blur the difference between "sold" and "confirm". Keep UI sounds identical, and keep them *short and soft* so the repetition doesn't grate. The streak ladder is the exception that proves the rule: its pitch changes, but in a way that carries meaning, not at random.

## 4. Timing: when the sound fires

A UI sound has to land with the thing it confirms. Two delays stand between the press and the ear.

**Audio buffer latency.** The audio engine mixes in blocks called **buffers**. A sound triggered now cannot start before the next buffer goes out, and the driver often keeps more than one buffer queued.

```
buffer latency (ms) = 1000 × buffer size (samples) / sample rate (Hz)
```

```python
for buffer, rate in [(256, 48000), (512, 48000), (1024, 44100)]:
    one_buffer_ms = 1000 * buffer / rate
    print(f"{buffer:5d} samples at {rate} Hz: {one_buffer_ms:5.1f} ms per buffer, "
          f"{2 * one_buffer_ms:5.1f} ms with double buffering")
```

```
  256 samples at 48000 Hz:   5.3 ms per buffer,  10.7 ms with double buffering
  512 samples at 48000 Hz:  10.7 ms per buffer,  21.3 ms with double buffering
 1024 samples at 44100 Hz:  23.2 ms per buffer,  46.4 ms with double buffering
```

Compare with one frame at 60 frames per second, 16.7 ms. A 1,024-sample buffer queued twice puts the click almost three frames behind the button's visual press. Smaller buffers cost CPU (more mixing calls per second), so engines trade the two. Week 14 returns to that cost. For UI, the lesson is to test on the slowest target platform with its real buffer settings, because a click that feels crisp on your development machine can feel mushy on a console or phone.

**The trigger point.** The second delay is design, not hardware. Decide what each sound confirms:

- **Hover** fires when the pointer enters the element.
- **Click** fires on press, not release, so the confirmation is as early as possible.
- **Result** (confirm, error) fires when the result is known.

In a single-player game the result is known at once. In an MMO it often is not. When you buy from the auction house, the client sends a request and the server decides whether you got the item. That round trip can take 50 to 300 ms or more. If you play "purchase confirmed" on click and the server then says the item was already sold, you have lied to the player. The standard pattern is two sounds: a neutral click on press, then a confirm or error sound when the server answers. [CS202 week 2](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w02-latency-jitter-loss-measure-your-own.md) measures that round trip next year. Here you only need to know it exists and design for it.

## 5. Writing a family spec

A UI family spec is a table the whole team can read. One row per sound, with these columns:

- **Name and trigger.** "inv_drop: item dropped into a bag slot."
- **Meaning rule.** "Short woody knock; one pitch; no rise or fall because it is neutral."
- **Pitch.** Start and end frequency, or the ladder rule.
- **Length and peak.** In ms and dBFS.
- **Bus, ducks and priority.** Which bus it goes to, whether it ducks anything (week 10), and its priority. UI sounds usually get high priority, because a missing click feels like a broken button.
- **Frequency of use.** From the repetition budget.

Then test the family with a **blind identification** check. Play each sound to someone who has not seen the spec and ask what just happened. If "cancel" and "error" are confused more than occasionally, your meaning rules are not doing their job.

## In-class activity (25 minutes)

In pairs, design the UI family for an MMO auction house.

1. List every UI event in this flow: open the auction house, search, hover a listing, click buy, server confirms, server rejects (sold out), not enough gold, close. Add any we missed.
2. For each, fill the spec columns from section 5. Use the repetition budget to set length and level.
3. Decide the two-stage timing for "buy", including what plays if the server takes more than one second.
4. Add one streak ladder somewhere it helps (for example, a bulk sell where each item sold climbs). Give the scale, cap or wrap, and `T_reset`.

Expected output: a spec table of at least 9 rows, a one-sentence timing rule, and the ladder settings. Pair up with another team and run a blind identification test by humming or playing their sounds from the interactive's tone generator.

## Common misconceptions

- **"UI sounds should be exciting."** Most UI sounds should be nearly invisible. Save excitement for rare events, or players will mute the UI bus and lose the important sounds too.
- **"Rising pitch always means good."** It means "more" or "forward". A rising siren is a warning. Meaning comes from the family's rules and the genre, not from physics.
- **"A ladder can go up forever."** Each step multiplies frequency by at least `2^(1/12)`. Twenty-four steps of a chromatic ladder quadruple the frequency, and a 1 kHz start ends at 4 kHz, which is shrill. Cap it, wrap it or grow a different parameter.
- **"Play the success sound as soon as the button is pressed."** Only if success is already certain. In networked games, click on press and confirm on the server's answer.

## Check yourself

1. A menu click is a 60 ms recorded sample. Your ladder resamples it up 19 semitones at the top. How long is the top step, and is that a problem?
2. A crafting station plays a 1.2 s fanfare for every crafted item, and players craft about 8 items a minute for 20 minutes. How many seconds of fanfare do they hear per session? Propose a change.
3. Your console build uses 1,024-sample buffers at 48 kHz with two buffers queued. What is the audio latency? How many 60 fps frames is that?
4. Two sounds in a family are "cancel" (660 Hz falling to 440 Hz, 120 ms) and "error" (440 Hz falling to 415 Hz, 150 ms). In blind tests players confuse them. Using section 1's conventions, what would you change?
5. Why might a combo ladder in a rhythm game use `T_reset` tied to the beat rather than a fixed number of seconds?

<details>
<summary>Answers</summary>

1. `2^(19/12) ≈ 3.0`, so about 20 ms. A 20 ms click can lose its body and sound like a tick. Render the top steps separately, or synthesise them.
2. `8 × 20 = 160` plays, `160 × 1.2 = 192` s, over three minutes of fanfare. Use a short confirm for each item and keep the fanfare for the last item of a batch or a rare quality result.
3. `1000 × 1024 / 48000 = 21.3` ms per buffer, 42.7 ms with two queued, about 2.6 frames at 60 fps.
4. Both fall and both are consonant-ish. Make "error" lower and dissonant (a semitone clash or a buzz), give it a different timbre, and keep "cancel" as a clean falling interval. The difference should survive a noisy room.
5. Because the rule players follow is musical. A gap of one missed beat should break the streak whatever the song's tempo, so `T_reset` should scale with the beat length, which is 60 / BPM seconds.

</details>

## Lab / assignment hook

[Lab 11, render a UI family](../labs/lab11.md). You write a small standard-library Python synthesiser that renders sweeps and ladders to WAV files, check it against this lecture's table, then design, render and blind-test an eight-sound family for an interface of your choice. The family goes into your SFX pack (30%).

## Sources

- n64decomp, `sm64` decompilation project (GitHub), `src/game/behaviors/red_coin.inc.c`. The original Japanese version plays an identical sound for every red coin; all other versions add the number of coins collected to the red-coin sound so each plays higher; an orange number counter is spawned for each coin except the eighth. Super Mario 64, Japanese release 1996 and later versions.
- Mastrapa, G. (2009, June 10). "The Sounds of PopCap, Part 3: Peggle". *Crispy Gamer* (archived at the Internet Archive). Interview with Sukhbir Sidhu; rising sound as the ball hits pegs; the goal of blending effects with the music. Peggle, PopCap, 2007.
- Wikipedia, "Space Invaders". The aliens and their sound speed up as fewer remain, a result of the hardware rendering fewer aliens faster; Nishikado kept it as a feature. Taito, 1978.
- Blattner, M. M., Sumikawa, D. A. & Greenberg, R. M. (1989). "Earcons and Icons: Their Structure and Common Design Principles". *Human-Computer Interaction* 4(1), 11-44. doi:10.1207/s15327051hci0401_1.
- Gaver, W. W. (1986). "Auditory Icons: Using Sound in Computer Interfaces". *Human-Computer Interaction* 2(2), 167-177. doi:10.1207/s15327051hci0202_3.
- Collins, K. (2008). *Game Sound*. MIT Press.

## Interactive spec: examples/w11-streak-ladder.html

**Purpose.** Let students hear and see that a ladder that is even in semitones is uneven in hertz, and that the choice of scale, cap or wrap and reset time changes what a streak means.

**Layout.** Two linked views, side by side on desktop, stacked on phones.

- *Left, "What you hear" (semitones):* a vertical ladder with rungs drawn at equal spacing per semitone from 0 to 24. The scale's rungs are drawn solid; the current step glows. A step counter "n = 5" and a reset timer bar that drains over `T_reset`.
- *Right, "What the frequency does" (hertz):* the same steps plotted on a linear hertz axis from `f0` to `4·f0`, showing rungs spreading apart as they rise. A thin line connects played steps in order.
- Below: a big "Collect" button (also space bar and Enter) and a readout row.

**Controls.**
- Scale selector: Same `[0]`, Chromatic `[0..11, 12]` (13 steps), Major `[0,2,4,5,7,9,11,12]`, Pentatonic `[0,2,4,7,9,12]`, Custom (text field of comma-separated semitones, validated to integers 0-24).
- Mode: Cap / Wrap.
- `f0`: slider 220-880 Hz, default 523.25 (with snap buttons for 440 and 523.25).
- `T_reset`: slider 0.2-3.0 s, step 0.1, default 1.0.
- Source: "Synth" (default) or "Resample". In Synth mode each step is a 120 ms sine plus a quiet octave partial, 5 ms linear attack, exponential decay, peak −14 dBFS, rendered with Web Audio `OscillatorNode` at `f(n)`. In Resample mode, generate one 200 ms chime buffer procedurally at `f0` (the same recipe, rendered into an `AudioBuffer`) and play it with `playbackRate = 2^(s/12)`, so duration visibly shrinks.
- Button "Auto streak": plays 8 events 0.25 s apart, then one after a gap of `T_reset + 0.2` s to demonstrate the reset.

**Exact formulas.** `s(n)` as in the lecture (cap: `scale[min(n−1, len−1)]`; wrap: `scale[(n−1) mod len]`); `f(n) = f0 · 2^(s/12)`; `rate = 2^(s/12)`; `dur = dur0 / rate` in Resample mode, 120 ms in Synth mode. Streak resets when the gap since the last press is strictly greater than `T_reset`.

**Readouts next to the visual.** n, semitones, ratio (3 decimals), frequency (2 decimals, Hz), step size from the previous step in Hz and in semitones, duration (ms, 1 decimal).

**Test values.** `f0 = 523.25`, Major, Cap: steps 1-8 read 523.25, 587.33, 659.25, 698.45, 783.99, 880.00, 987.76, 1046.50 Hz; step 9 reads 1046.50 again. Wrap: step 9 reads 523.25. Resample at step 8: 100.0 ms. Chromatic step 8: 783.99 Hz. `f0 = 440`, Major step 5: 659.26 Hz.

**The one insight.** On load, show the Major ladder already played through 8 steps (static, no sound until the user interacts, because browsers block autoplay), with the hertz view making the uneven spacing obvious.

**Accessibility.** Every sound has a visible counterpart (glow and readout), keyboard control for all inputs with visible focus, `prefers-reduced-motion` disables the glow animation and timer-bar easing, light and dark palettes from `templates/interactive-tokens.css`. No audio files; everything generated with Web Audio.
