# AU101 · Week 05 — Implementation in Engine: From Game Event to Speaker

**Why this matters:** A great sound played at the wrong moment is a bug. Between "the player pulled the trigger" and "air moved in the room" sit a game loop, an audio thread and a sound card, and each one moves your sound onto its own clock. This week you learn where those clocks are, how they bend timing you thought was fixed, and how to wire sounds to gameplay so they start, stop and repeat when they should.

**You will be able to:**
- Trace a sound from a gameplay event to the speaker and name each stage that adds delay.
- Compute the start times and intervals of a repeating sound triggered from a frame-based game loop, for both "reset" and "carry" cooldowns, at any frame rate.
- Design a trigger that keeps rhythmic sounds even by scheduling them on the audio clock, and state the latency it costs.
- Choose between frame-driven, distance-driven and animation-driven triggers for footsteps and loops, and debug the classic stuck-loop and retrigger bugs.

**Before class:** Chris Wilson, "A tale of two clocks" (web.dev, 2013), read to the end of the metronome timing diagrams (about 20 minutes). Godot Engine documentation, "Sync the gameplay with audio and music", the introduction and "Using the system clock to sync" (about 10 minutes). Unity 6.2 Scripting Reference, `AudioSource.PlayScheduled` and `AudioSettings.dspTime` (5 minutes).

**Prerequisites from earlier courses:** [CS101 week 3, the game loop](../../CS101-programming-for-games-i/lectures/w03-loops-and-the-game-loop.md) and [CS101 week 9, delta time and the accumulator](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md). The "carry" cooldown in section 2 is week 9's accumulator applied to a weapon. [CS101 week 7, engine intro](../../CS101-programming-for-games-i/lectures/w07-engine-intro-scenes-nodes-scripts.md) (callbacks and update order) and [CS101 week 11, game state machines](../../CS101-programming-for-games-i/lectures/w11-game-state-machines.md) (entering and leaving states, which is where loops start and stop). From this course, [week 4, layering and variation](w04-layering-and-variation.md) decides *what* plays; this week decides *when*.

**Interactive:** [examples/w05-trigger-timing.html](../examples/w05-trigger-timing.html). Keep it open, with headphones, during section 2.

---

## 1. The path from a game event to your ears

When your code says "play the gunshot", nothing happens right away. The request passes through several stages, and each has its own clock.

1. **The game loop.** Your gameplay code runs once per frame. At 60 frames per second a frame is 16.7 ms long. Anything that happens "between frames" is noticed at the next frame.
2. **The play call.** Your code asks a **player** to start a **clip**. Engines name these differently. Godot has `AudioStreamPlayer` nodes playing `AudioStream` resources. Unity has `AudioSource` components playing `AudioClip` assets. Middleware (next week) calls them event instances.
3. **The audio thread.** Sound is not computed one sample at a time as the game runs. A separate thread, the **mixer**, fills a **buffer** (a chunk of samples) with the sum of every playing sound, then hands the chunk to the operating system. The Godot documentation says it plainly: when you call `play()`, the sound starts when the audio thread processes the next chunk.
4. **Output.** The chunk waits in the operating system and the device before it reaches the speaker. Godot calls this the output latency and sets a preferred value of 15 ms by default (project setting `audio/driver/output_latency`, Godot 4).

A few more terms you'll need:

- A **voice** is one sound currently playing. Ten gunshots overlapping are ten voices.
- A **listener** is the "ears" in the scene, usually on the camera or the player. Week 7 covers how distance and direction to the listener change a sound.
- A **bus** is a named mixing channel ("SFX", "Music", "UI"). Sounds route into buses, and each bus has its own volume and effects. Week 10 builds a mix out of them.
- A **one-shot** plays once and ends by itself. A **loop** plays until something stops it. One-shots can be fire-and-forget. Loops always need a handle, some reference your code keeps so it can stop the sound later.

### The latency budget

Add the stages and you get the delay between an event and the sound. In the worst case at 60 fps, the event happens just after a frame starts, so it waits up to 16.7 ms to be noticed. Then the play call waits for the next mix chunk. At a chunk of 512 samples and 48,000 samples per second, a chunk lasts `512 / 48,000 = 10.7 ms`, so that wait is up to 10.7 ms. Then output latency adds its own amount, around 15 ms with Godot's default. That gives a worst case around 40 ms. That's fine for most sound effects. It is not fine when the *spacing* between sounds changes from one shot to the next, because the ear is much better at noticing an uneven rhythm than a constant delay. That's the subject of the worked example.

## 2. Worked example: the gun that changes speed with your monitor

### The hook

The original Doom (id Software, 1993) runs its whole game on a fixed clock: 35 tics per second (`TICRATE 35` in the released source). Every weapon animation is a list of frames, each lasting a whole number of tics. The chaingun's firing frames last 4 tics each, and each one fires a bullet and plays a sound. Four tics at 35 per second is `4 / 35 = 114.3 ms`, so the chaingun fires 8.75 times per second, 525 rounds per minute, and every gap between shots is exactly the same. There is nothing between tics for a shot to land on.

Modern games don't run on a fixed 35 Hz grid. They render at whatever the player's monitor and hardware allow: 30, 60, 144, 165, 240 frames per second. Suppose you design a rifle at 800 rounds per minute, one shot every 75 ms, and you trigger its sound from the game loop. Play it on a 60 Hz monitor and it fires at 720 rounds per minute. Play it at 144 Hz and it fires at 785. Or, with a different three-line implementation, it fires at the right average rate but with a limp: long, short, long, short.

Where does the time go? You can compute it.

### The model: sounds start on frame boundaries

Call the frame length `Δ` (delta, `1 / fps` seconds) and the weapon's intended period `T` (60 / rounds per minute). Gameplay code only runs at the start of a frame, so a shot that "should" fire at time `t` actually fires at the first frame boundary at or after `t`:

```
t_fired = ceil(t / Δ) × Δ
```

- `ceil` rounds up to the next whole number of frames.
- `t` is the moment the shot should happen.
- `t_fired` is when your code sees it and calls `play()`.

What `t` is depends on how you wrote the cooldown. There are two common ways.

**Reset cooldown.** When the gun fires, set the timer back to zero. `if time_since_shot >= T: fire(); time_since_shot = 0`. Any leftover time past `T` is thrown away. The gap between shots is always a whole number of frames, rounded up:

```
gap_reset = ceil(T / Δ) × Δ
```

**Carry cooldown.** When the gun fires, subtract `T` and keep the leftover: `time_since_shot -= T`. This is CS101 week 9's accumulator. Shot `k` should fire at `k × T`, so it fires at `ceil(k × T / Δ) × Δ`. The average rate is exactly right, but individual gaps jump between two frame counts.

There's a third way, which avoids the frame grid altogether. **Schedule on the audio clock.** The mixer has its own clock that counts samples, and most engines let you say "start this sound at audio time `x`" rather than "start it now". When the trigger is pulled at time `t_0`, you schedule shot `k` at:

```
t_audio = t_0 + L + k × T
```

where `L` is a small **lookahead**, a delay that gives the mixer time to prepare. Every gap is exactly `T`. The price is that every shot is `L` late.

### Numbers you can check

Take `T = 75 ms` (800 rounds per minute). At 60 fps, `Δ = 16.67 ms`, and `T / Δ = 4.5` frames.

- Reset: `ceil(4.5) = 5` frames, so every gap is `5 × 16.67 = 83.3 ms`. That's `60 / 0.0833 = 720` rounds per minute, 10% slow.
- Carry: shot 1 is due at 75 ms, which is 4.5 frames, so it fires at frame 5 (83.3 ms). Shot 2 is due at 150 ms, exactly frame 9 (150.0 ms). Shot 3 at 225 ms, frame 13.5, fires at frame 14 (233.3 ms). The gaps alternate 83.3, 66.7, 83.3, 66.7 ms.

Now vary the frame rate and the weapon:

| Weapon | Frame rate | Reset: gap | Reset: rounds per minute | Carry: gaps (ms) |
|---|---|---|---|---|
| 600 rpm (`T` = 100 ms) | 30 | 100.0 ms | 600 | all 100.0 |
| 600 rpm | 60 | 100.0 ms | 600 | all 100.0 |
| 600 rpm | 144 | 104.2 ms | 576 | 104.2, 97.2, 104.2, 97.2, 97.2 ... |
| 800 rpm (`T` = 75 ms) | 30 | 100.0 ms | 600 | 100.0, 66.7, 66.7, 66.7, 100.0 ... |
| 800 rpm | 60 | 83.3 ms | 720 | 83.3, 66.7, 83.3, 66.7 ... |
| 800 rpm | 144 | 76.4 ms | 785 | 76.4 (×4), 69.4, 76.4 ... |
| Any | Any, audio clock | exactly `T` | exact | all exactly `T` |

Three things stand out.

1. **Faster monitors can make a reset-cooldown gun slower.** The 600 rpm gun is perfect at 30 and 60 fps, because 100 ms is exactly 3 and 6 frames. At 144 fps, 100 ms is 14.4 frames, which rounds up to 15, and the gun loses 24 rounds per minute. The same thing happens at 165 fps (582 rpm). Players with expensive monitors get a weaker gun. That's a gameplay bug that shows up first as a sound problem, because the ear hears the tempo.
2. **Carry fixes the rate and moves the error into rhythm.** The average is right, but the gaps wobble by up to one frame. At 30 fps an 800 rpm gun alternates a 100 ms gap with three 66.7 ms gaps, a gallop you can hear.
3. **The audio clock fixes both**, as long as you accept a constant lookahead.

Doom had no such problem because its designers picked every weapon timing as a whole number of tics. On a fixed grid, the only rates you can choose are the ones the grid allows. That's a design constraint, and it's also a guarantee.

### Code you can run

```python
from fractions import Fraction
from math import ceil

def reset_times(rpm, fps, shots):
    """Cooldown restarts on the frame that fires, so leftover time is lost."""
    period, frame = Fraction(60, rpm), Fraction(1, fps)
    step = ceil(period / frame) * frame
    return [k * step for k in range(shots)]

def carry_times(rpm, fps, shots):
    """Cooldown keeps its leftover time: shot k fires on the first frame >= k * period."""
    period, frame = Fraction(60, rpm), Fraction(1, fps)
    return [ceil(k * period / frame) * frame for k in range(shots)]

def gaps_ms(times):
    return [round(float(b - a) * 1000, 1) for a, b in zip(times, times[1:])]

for fps in (60, 144):
    r = reset_times(800, fps, 7)
    print(f"{fps:>3} fps reset: {gaps_ms(r)}  -> {60 / float(r[1]):.0f} rpm")
    print(f"{fps:>3} fps carry: {gaps_ms(carry_times(800, fps, 7))}")
```

Output:

```
 60 fps reset: [83.3, 83.3, 83.3, 83.3, 83.3, 83.3]  -> 720 rpm
 60 fps carry: [83.3, 66.7, 83.3, 66.7, 83.3, 66.7]
144 fps reset: [76.4, 76.4, 76.4, 76.4, 76.4, 76.4]  -> 785 rpm
144 fps carry: [76.4, 76.4, 76.4, 76.4, 69.4, 76.4]
```

The code uses `Fraction` on purpose. With floats, shot 3 of a 600 rpm gun at 30 fps is due at `3 × 0.1 / (1/30)` frames, which Python computes as 9.000000000000002, so `ceil` returns 10 instead of 9 and invents a late shot. Exact fractions keep every frame count honest.

### A visual you can move

Open [`examples/w05-trigger-timing.html`](../examples/w05-trigger-timing.html). The top view is a timeline. Faint vertical lines are frame boundaries, dots above the axis are the intended shot times `k × T`, and markers below show when each shot actually plays under the chosen strategy. The bottom view plots each gap in milliseconds as a bar, with a dashed line at `T`. Press "Fire" to hear 16 shots.

Set 800 rpm and 60 fps and switch between the three strategies. On the timeline, reset markers drift further behind the dots with every shot. Carry markers stay close but hop between frames. Audio-clock markers sit at a constant offset `L` from every dot. The bar chart shows the same story as numbers: flat but too tall, zigzag, flat and exactly on the line. Then drag the frame rate from 30 to 240 and watch the reset line's rounds-per-minute readout jump around rather than settle. Turn on "mix chunks" to add the mixer's own grid (512 samples at 48 kHz). Carry gets rougher still, and the audio clock is unaffected, because it counts in samples.

### Cross-game recognition

**Doom (1993).** The fixed-grid solution. Every event is on a 1/35 s grid, and every weapon period is a whole number of tics (chaingun 4, so 8.75 shots per second). In our model `Δ = 1/35 s` and `T` is always a multiple of `Δ`, so `ceil(T / Δ) = T / Δ` exactly and the error is zero. Many modern engines offer a fixed-timestep gameplay update (CS101 week 9) that brings back part of this guarantee for game logic, but the sound still has to cross into the mixer's clock.

**Unity (Unity 6.2).** `AudioSettings.dspTime` is documented as the audio system's time, based on the number of samples actually processed, and far more precise than `Time.time`. `AudioSource.PlayScheduled(time)` plays a clip at an exact point on that timeline. The documentation calls it independent of the frame rate and recommends scheduling slightly in the future, about 100 to 200 ms. That's `t_audio = t_0 + L + k × T` with `L` of 100 to 200 ms. Unity's Audio Random Container also has a **Pulse** trigger mode that plays clips at a steady interval measured from the container's start, and the manual names an automatic rifle as a use for it. The engine does the carry-free scheduling for you.

**Web Audio API (browsers).** Chris Wilson's "A tale of two clocks" describes the same split. JavaScript timers (`setTimeout`) are imprecise and can be delayed by layout or garbage collection. The audio context's `currentTime` is exact. His metronome wakes up every 25 ms on the imprecise clock and schedules any notes due in the next 100 ms on the audio clock. In our terms, the game loop has become a 25 ms timer, and `L` is up to 100 ms. The article shows a timer callback arriving 50 ms late without a single missed beat, because the notes were already scheduled. This course's interactives use this method.

**Godot (Godot 4).** Godot's `play()` starts a sound at the next mix chunk rather than at an exact sample. The documentation's sync tutorial gives `AudioServer.get_time_to_next_mix()` and `AudioServer.get_output_latency()` so you can estimate when a sound will actually reach the speaker. That's the latency budget from section 1, measured instead of guessed. It's aimed at rhythm games, where the problem is the reverse of ours. The music is the clock, and the game has to line up with it.

Four environments, one principle. Game logic runs on a coarse, wobbly clock. Audio runs on a fine, steady one. Anything rhythmic should be timed on the steady clock.

### Design judgment

- **Don't delay the first shot.** Players feel input lag on the trigger pull far more than they notice a constant offset afterwards. A common pattern plays shot 0 immediately and schedules shots 1, 2, 3 ... on the audio clock relative to shot 0. The rhythm is exact and the trigger feels instant.
- **Keep gameplay and sound in agreement.** If the damage uses a reset cooldown at 720 rpm and the sound uses the audio clock at 800, the player hears more bullets than they deal. Fix the gameplay cooldown first (carry, or a fixed timestep), then schedule sound from the same shot times.
- **Lookahead is a trade-off.** A larger `L` survives worse hitches, as in Wilson's example, but anything that should interrupt the burst, such as releasing the trigger, takes effect up to `L` late. Shots already scheduled will still play. Keep `L` small for player weapons, or keep a handle so you can cancel scheduled shots.
- **Very fast repeats may want a loop.** Above roughly 15 to 20 shots per second, individual one-shots stack into dozens of voices. A designed loop for sustained fire, with a separate one-shot for the first shot and a "tail" one-shot on release, costs fewer voices and is immune to frame timing. The trade is less per-shot variation (week 4).
- **Test at more than one frame rate.** The 600 rpm row shows a bug that is invisible at 60 fps and obvious at 144. Put 30, 60 and 144 fps into your audio test plan.

### Check this example

1. A 900 rpm weapon uses a reset cooldown. What rate does it fire at 60 fps and at 144 fps?
2. The same weapon uses a carry cooldown at 60 fps. List the first four gaps.

<details>
<summary>Answers</summary>

1. `T = 66.7 ms`. At 60 fps that's exactly 4 frames, so 900 rpm with no error. At 144 fps, `T / Δ = 9.6`, rounds up to 10 frames = 69.4 ms, so 864 rpm.
2. Since `T` is exactly 4 frames, every gap is 66.7 ms. Carry and reset agree whenever `T` is a whole number of frames.

</details>

## 3. Wiring sounds to gameplay

Timing is one half of implementation. The other half is making sure the right code asks for the right sound, once.

### Trigger on events, not on states

A **state** is something that stays true ("the player is running"). An **event** is a moment ("the player's foot touched the ground"). One-shots belong to events. A beginner's bug is to play a sound from the per-frame update whenever a state is true:

```
func _process(delta):
    if is_on_fire:
        $BurnSound.play()     # restarts the sound 60 times a second
```

Every frame, `play()` restarts the sound from the beginning, so you hear only the first few milliseconds, sixty times a second: a buzz. The fix is to act on the *change*. Start the loop when entering the state and stop it when leaving. That's CS101 week 11's `enter` and `exit` functions:

```
func enter_burning():
    $BurnSound.play()         # a looping stream

func exit_burning():
    $BurnSound.stop()
```

### The stuck loop

The mirror-image bug is a loop that never stops. The player dies while burning, the burning state is never exited because the whole character was freed, and the burn loop keeps playing forever at the spot where the player died, or it stops but a looping sound owned by a global audio manager doesn't. Two rules prevent most cases. First, a loop should be owned by the object whose state it describes, so it is freed with that object. Second, every path out of a state, including death, despawn and level change, must pass through the state's exit code.

### Footsteps: time, distance or animation?

Footsteps are the classic trigger design problem, and there are three common answers.

- **Timer.** Play a step every 0.5 s while moving. Simple, and wrong as soon as speed changes. A character sprinting at twice the speed still steps twice a second, and feet visibly slide out of sync with the sound.
- **Distance.** Play a step every time the character travels one stride length `s`. This is week 9's accumulator again, measuring metres instead of seconds: `walked += speed × delta; while walked >= s: step(); walked -= s`. At 3 m/s with a 0.75 m stride, that's 4 steps per second, and doubling the speed doubles the rate. It tracks speed without any animation data.
- **Animation event.** Mark the exact frame in the walk animation where each foot lands, and let the animation system call your step function there. Sound and picture match by construction, including stumbles and turns. This needs a marked-up animation for every gait, and blended animations can fire two events close together or skip one.

The distance method is a good default for prototypes and for top-down or distant cameras. Animation events are worth the extra work when the camera is close to the feet. Whatever you choose, the step function is the natural place to apply week 4's variation, and to pick the surface (stone, grass, wood). Next week, you'll hand that choice to middleware as a parameter.

## 4. Voices, limits and loading

### How many copies may play?

Every player node or source has a limit on how many sounds it can play at once. In Godot 4, `AudioStreamPlayer.max_polyphony` defaults to 1, and calling `play()` once the limit is reached cuts off the oldest sound. For a rapid gun, a limit of 1 means each new shot chops off the previous shot's tail. That removes overlap you might want. Raise it to 3 or 4 so tails can ring under the next shot. For a sound that should never stack, such as a low-health warning, a limit of 1 is correct.

Global limits and **voice stealing**, deciding which sound to drop when the whole game runs out of voices, belong to week 10 (priority) and week 14 (optimization). For now, the rule is local. Decide per sound how many copies may overlap, and set it on purpose.

### Load it or stream it?

A short sound effect is usually **loaded**. The whole file is decoded into memory before it's needed, so it can start instantly and play many copies. Long files (music, long ambience) are usually **streamed**, read from disk a piece at a time while playing, which saves memory but takes time to start and costs file access per copy.

Minecraft's resource packs make this choice visible. Each sound entry in `sounds.json` can set `stream: true`, which the Minecraft Wiki recommends for sounds longer than a few seconds and notes is used for music and records. The same page documents the cost. A streamed sound allows only 4 instances of that sound at once, while non-streamed sounds allow many more. There's also a `preload` flag that loads a sound when the pack loads rather than on first play, which avoids a hitch the first time an important sound fires. Those are the same three knobs every engine gives you: stream or not, how many copies, and when to load.

## In-class activity (25 minutes)

In groups of three, you are the audio programmer on a top-down shooter. The designer's weapon sheet lists a pistol at 300 rpm, an SMG at 900 rpm and a minigun at 1,500 rpm. The game uses a reset cooldown and runs uncapped.

1. For each weapon, compute the actual rate at 60, 144 and 240 fps under the reset cooldown. Mark any weapon whose rate changes by more than 2% between frame rates.
2. Rewrite the trigger for the minigun using the audio clock. Choose a lookahead `L`, and write pseudocode for trigger pressed, each frame while held, and trigger released. Say what happens to shots already scheduled when the trigger is released.
3. Decide whether the minigun should use one-shots or a loop. Justify it with a voice count. How many shots overlap if each shot's tail lasts 0.6 s?

Expected output: a 9-cell table of rates, the pseudocode, and a two-sentence recommendation with the voice count.

## Common misconceptions

- **"If I call `play()` now, the sound plays now."** It plays at the next frame boundary your code runs on, then at the next mix chunk, then after output latency. Only the audio clock gives exact timing.
- **"A higher frame rate always makes timing better."** Only if the period divides evenly into frames. The 600 rpm reset gun is exact at 60 fps and 4% slow at 144.
- **"The carry cooldown solves it."** It fixes the average rate, which matters for gameplay balance. It doesn't fix the rhythm, which is what players hear.
- **"Scheduling ahead adds lag to everything."** Only if you schedule the first event too. Play the first shot now and schedule the rest from it.

## Check yourself

1. A 1,200 rpm weapon runs a reset cooldown at 144 fps. What is its actual rate? Would a carry cooldown have the right average rate?
2. Your mixer uses chunks of 1,024 samples at 48,000 Hz. What is the largest extra delay the chunk grid adds to a `play()` call? What does that do to the gaps of a carry-cooldown gun that already wobbles by one 16.7 ms frame?
3. A character's stride is 0.8 m. Using the distance method, how many steps per second do you hear at 2 m/s and at 5 m/s? What would a 0.5 s timer give at both speeds?
4. With Unity's `PlayScheduled`, you set `L = 150 ms` and schedule a full 30-round magazine at 600 rpm when the trigger is pressed. The player releases the trigger after 0.5 s. How many shots have *played*, and how many more will play if you do nothing? What should the code do instead?

<details>
<summary>Answers</summary>

1. `T = 50 ms`, `Δ = 6.94 ms`, `T / Δ = 7.2`, rounds up to 8 frames = 55.6 ms, so 1,080 rpm, 10% slow. A carry cooldown fires shot `k` at the first frame after `k × 50 ms`, so the average rate is exactly 1,200. Only the gaps wobble, between 7 and 8 frames.
2. `1,024 / 48,000 = 21.3 ms`. That's longer than a frame at 60 fps, so the chunk grid can dominate. Gaps can now vary by up to one frame plus one chunk, about 38 ms, around a 75 ms period. Scheduling on the audio clock removes both.
3. Distance: `2 / 0.8 = 2.5` steps per second and `5 / 0.8 = 6.25`. The timer gives 2 per second at both speeds, so at 5 m/s the feet would land three times for every step you hear.
4. Shots are at `0.15 + 0.1k` s. By 0.5 s, shots at 0.15, 0.25, 0.35 and 0.45 s have played, 4 shots, and 26 more will play. Schedule only a short window ahead (for example the next 2 shots), refill it each frame while the trigger is held, and stop any source already scheduled beyond the release time.

</details>

## Lab / assignment hook

[Lab 05, trigger timing](../labs/lab05.md). You'll implement the three trigger strategies and the mix-chunk grid in Python, render each to a click-track WAV, and measure the gaps. Then you'll wire one looping and one repeating sound into a small engine scene (Godot 4 or Unity) and test it at two frame rates.

## Sources

- id Software, DOOM source code (`linuxdoom-1.10`, released 1997, GitHub `id-Software/DOOM`). `doomdef.h`: `TICRATE 35`. `info.c`: chaingun firing states `S_CHAIN1` and `S_CHAIN2` of 4 tics each, both calling `A_FireCGun`. `p_pspr.c`: `A_FireCGun` starts `sfx_pistol`.
- Chocolate Doom, `src/m_config.c` (master branch, 2026). The comment on `snd_maxslicetime_ms` describes one sound slice per tic "with the 35fps timer".
- Godot Engine documentation (Godot 4), "Sync the gameplay with audio and music" (godot-docs repository, `tutorials/audio/sync_with_audio.rst`). Audio mixed in chunks; `play()` starts at the next chunk; `AudioServer.get_time_to_next_mix()` and `get_output_latency()`.
- Godot Engine class reference (Godot 4, master branch 4.8 development, September 2026), `ProjectSettings` (`audio/driver/output_latency`, default 15 ms; `audio/driver/mix_rate`, default 44,100 Hz) and `AudioStreamPlayer` (`max_polyphony`, default 1, cuts off the oldest sound).
- Unity Technologies, Unity 6.2 Scripting Reference, `AudioSource.PlayScheduled` (absolute time on the `dspTime` timeline, independent of frame rate, schedule about 100-200 ms ahead) and `AudioSettings.dspTime` (based on samples processed, more precise than `Time.time`).
- Unity Technologies, Unity 6.2 Manual, "Audio Random Container reference". Pulse trigger mode with intervals from the container's start, suggested for an automatic rifle.
- Wilson, C. (2013). "A tale of two clocks". web.dev (originally HTML5 Rocks). JavaScript timers versus the audio clock; 25 ms timer, 100 ms lookahead; a 50 ms late callback without a missed beat.
- Minecraft Wiki, "sounds.json" (Java Edition). `stream` recommended for sounds longer than a few seconds; streamed sounds limited to 4 instances; `preload` flag.

## Interactive spec: examples/w05-trigger-timing.html

**The one insight:** a repeating sound triggered from the game loop inherits the frame grid. A reset cooldown gets the rate wrong, a carry cooldown gets the rhythm wrong, and scheduling on the audio clock gets both right at the cost of a constant lookahead.

**Layout.** Two linked views and a control panel. Mobile: stacked (timeline, gap chart, controls, readouts). From 900 px: views on the left (65%), controls and readouts on the right.

- **Top view, "Timeline":** the first 600 ms after the trigger, horizontal axis in ms with ticks every 50 ms. Faint vertical lines at every frame boundary `n × Δ`. Optional second grid (toggle "Mix chunks") drawn as short ticks at every `m × B / sr`. Hollow circles above the axis at intended times `k × T`. Filled markers below the axis at actual play times for the selected strategy. A thin connector from each circle to its marker shows the error; label the error in ms on hover or focus.
- **Bottom view, "Gaps":** one bar per gap between consecutive shots (first 15 gaps), height in ms, with a dashed horizontal line at `T` labelled "intended". Bars within 0.5 ms of `T` use the value (ochre) token; others use the damage (red) token.

**Controls.**
- Rounds per minute: slider 120 to 1,500, step 10, default 800. Also a number input.
- Frame rate: select 30, 60, 90, 120, 144, 165, 240; default 60.
- Strategy (radio): "Reset cooldown", "Carry cooldown", "Audio clock". Default "Reset cooldown".
- Lookahead `L`: slider 0 to 200 ms, step 5, default 50 (only used by "Audio clock").
- Toggle "Mix chunks": when on, reset and carry times are further rounded up to the next chunk boundary. Chunk size select 256, 512, 1,024 samples at a sample rate of 48,000 Hz; default 512.
- Button "Fire 16 shots" (key F): plays the shots through Web Audio at the computed times relative to `ctx.currentTime + 0.1` (the audio clock is used for playback in all three strategies so the page itself does not add jitter; the strategy only decides the *times*). Sound: a 25 ms click made of a 2 kHz sine burst with a 5 ms exponential decay plus a little noise, generated in an `AudioBuffer`. Button "Compare" plays reset, then carry, then audio clock, 1 s apart.

**Formulas** (use exact rational arithmetic or integer microseconds to avoid float rounding; e.g. compute in units of `1 / (fps × rpm)` minutes or round `t × fps` to 9 decimals before `ceil`).
- `T = 60 / rpm` s, `Δ = 1 / fps` s.
- Reset: `t_k = k × ceil(T / Δ) × Δ`.
- Carry: `t_k = ceil(k × T / Δ) × Δ`.
- Audio clock: `t_k = L + k × T` (trigger at `t_0 = 0`; show markers offset by `L`).
- Mix chunks (reset and carry only): `t_k' = ceil(t_k / C) × C`, `C = chunk / 48000` s.
- Actual rate for reset: `60 / (ceil(T / Δ) × Δ)` rpm.

**Readouts (live text).** `T` in ms (1 decimal), `Δ` in ms (2 decimals), `T / Δ` (2 decimals), actual average rate in rpm (integer, over the 16 shots), smallest and largest gap in ms (1 decimal), largest timing error versus intended in ms, and for "Audio clock" the added latency `L`.

**Test values.**
- 800 rpm, 60 fps, reset: all gaps 83.3 ms, rate 720 rpm.
- 800 rpm, 60 fps, carry: gaps 83.3, 66.7, 83.3, 66.7 ...; 16 shots span 68 frames (1.1333 s), so the average over those 15 gaps is 794 rpm; it tends to 800 over long bursts.
- 800 rpm, 144 fps, reset: gaps 76.4 ms, 785 rpm. Carry: 76.4, 76.4, 76.4, 76.4, 69.4, 76.4 ...
- 600 rpm, 60 fps, reset: 100.0 ms, 600 rpm. 600 rpm, 144 fps, reset: 104.2 ms, 576 rpm. 600 rpm, 165 fps, reset: 582 rpm.
- 800 rpm, 30 fps, carry: 100.0, 66.7, 66.7, 66.7, 100.0 ...
- Any rpm and fps, audio clock: every gap equals `T` to 0.1 ms; first marker at `L`.
- 800 rpm, 60 fps, carry with 512-sample chunks: gaps 85.3, 74.7, 74.7, 74.7, 74.7, 74.7, 74.7, 74.7, 85.3, 64.0, 85.3, 64.0 ...; smallest 64.0, largest 85.3 ms. Reset with 512-sample chunks: mostly 85.3 ms with an occasional 74.7 ms.

**Accessibility.** Keyboard reachable controls with visible focus; the gap chart has a text table fallback (a collapsible "Show numbers" listing each shot's intended time, actual time and gap). No sound until the user presses a button; volume slider default 60% and mute toggle. When `prefers-reduced-motion` is set, markers appear without animation. Respect `prefers-color-scheme`. No game art; plain shapes only.
