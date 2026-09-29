# AU101 · Week 10 — Mixing, Ducking and Priority

**Why this matters:** A combat scene can ask for fifty sounds in the same second, and the player can follow maybe three of them. Mixing is how you decide which three. If you leave that decision to chance, the sound the player needed (the reload click behind them, the boss wind-up) is the one that gets buried.

**You will be able to:**
- Compute the combined level of several sounds and explain why a busy scene runs out of headroom.
- Trace an HDR mix window through a scene and compute when each quiet sound drops out and when it returns.
- Design a sidechain duck (depth, attack, release) for dialogue over music and predict how it will sound.
- Rank sound requests under a voice limit using priority with a distance offset, and critique a priority table.

**Before class:** Collins, *Game Sound* (2008), chapters 1-3 (the course reading). As you reread, mark every place where a hardware limit on how many sounds could play at once shaped a design decision. Skim the Wwise Help pages "Understanding HDR" and "Defining playback priority" (links in Sources); you do not need Wwise installed.

**Prerequisites from earlier courses:** [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (decibels; this lecture uses `dB = 20 · log10(amplitude ratio)` and does not re-derive it). [CS101 week 14, polish pass](../../CS101-programming-for-games-i/lectures/w14-polish-pass-sound-particles-screen-shake.md) (`max_polyphony` and "at most N copies of this sound"). [GD101 week 12, feedback and clarity](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) (the rarer the event, the bigger the signal). From this course, [week 1](w01-what-sound-does-feedback-space-emotion.md) (the three jobs of game sound), [week 4](w04-layering-and-variation.md) (two layers add +3 dB or +6 dB), [week 5](w05-implementation-in-engine.md) (per-sound polyphony limits), [week 7](w07-spatial-audio-and-attenuation.md) (attenuation curves and max distance) and [week 8](w08-adaptive-music-vertical-layering.md) (music stems that get louder with intensity). [Week 6](w06-middleware-events-and-parameters.md) introduced buses and snapshots in middleware.

**Interactive:** [examples/w10-hdr-window.html](../examples/w10-hdr-window.html). Keep it open during section 2.

---

## 1. Why a busy scene runs out of room

### Levels add in power, not in decibels

Every digital output has a ceiling, 0 dBFS (decibels relative to full scale). A sample value above full scale is clipped, and clipping sounds like a harsh crackle. Everything you mix must fit under that ceiling.

Week 4 showed that two unrelated layers of equal level add +3 dB and two identical, aligned layers add +6 dB. A mix is the same problem with many more sounds. Unrelated sounds (a footstep and a gust of wind, say) add their *powers*, so for any number of them the combined level is:

```
L_total = 10 · log10( 10^(L_1/10) + 10^(L_2/10) + ... + 10^(L_n/10) )
```

- `L_i` is the level of sound `i` in dBFS.
- `L_total` is the level of the sum.

The rule to remember is that two equal sounds give +3 dB, and ten equal sounds give +10 dB. Run it:

```python
import math

def db_sum(levels):
    return 10 * math.log10(sum(10 ** (L / 10) for L in levels))

for n in (1, 2, 4, 10, 40):
    print(n, "sounds at -20 dBFS each ->", round(db_sum([-20] * n), 1), "dBFS")
```

```
1 sounds at -20 dBFS each -> -20.0 dBFS
2 sounds at -20 dBFS each -> -17.0 dBFS
4 sounds at -20 dBFS each -> -14.0 dBFS
10 sounds at -20 dBFS each -> -10.0 dBFS
40 sounds at -20 dBFS each -> -4.0 dBFS
```

A sound designed to sit comfortably at −20 dBFS on its own becomes a −4 dBFS wall when forty copies play. The formula also shows how a louder sound swamps a quieter one. A 0 dBFS sound plus a −10 dBFS sound sums to only +0.4 dBFS. The quieter one adds almost nothing to the total, and the ear has trouble picking it out. That is called **masking**.

### Why "turn everything down" fails

The naive fix is to lower every sound until the worst case fits. If your worst case is forty sounds, every sound drops by 16 dB. Now the quiet scene, one player walking through a forest, sits 16 dB lower than it should. The birds and the wind drift toward the noise of the player's room, the fridge, the fan on their laptop. You traded clarity in the loud scene for mush in the quiet one.

The real fix is to make decisions. At any moment the mix should know which sounds matter and let the others get quieter or stop. Games use three tools for this, and this lecture covers each one:

1. **An automatic window** that follows the loudest sound and drops whatever falls below it (HDR, section 2).
2. **Ducking**, where one category of sound pushes another down while it plays (section 3).
3. **Priority with a voice limit**, where the engine refuses to play the least important sounds at all (section 4).

A fourth tool, the static mix of buses and snapshots, you met in week 6 as middleware structure. Section 5 shows how the four fit together.

## 2. Worked example: the sliding window

### The hook

Battlefield: Bad Company (DICE, 2008) was the first game on DICE's Frostbite engine, and DICE promoted two headline features for it. One was destruction. The other was "HDR audio", a mixing system that lets louder sounds drown out softer ones. Players noticed the effect without knowing its name. When a tank shell lands next to you, the birdsong, the distant gunfire and your squad's footsteps vanish. A second later they fade back in. Nobody turned the birds down in the level. The mix did it on its own.

How does a mix decide, sixty times a second, what to drop? And how long should the world stay "deaf" after a blast?

### The model

HDR stands for high dynamic range. The idea comes from photography. The real world spans a much wider range of brightness (or loudness) than a screen (or speaker) can show, so a system maps the part that matters right now into the range the device has.

In HDR audio every sound gets a level on an in-game scale, `L_i` in dB. The reference point is arbitrary, so a shell blast can be +45 and a bird −15 without anything clipping. The system keeps a **window** of fixed width and slides it so its top sits on the loudest sound.

```
target(t) = max( T, loudest active L_i )

top(t) = target(t)                              if target(t) >= top(t − dt)    (instant attack)
top(t) = max( target(t), top(t − dt) − r · dt ) otherwise                      (limited release)

out_i = L_i − top(t)        in dBFS
sound i is audible when out_i >= −W, otherwise it is culled
```

- `L_i` is the in-game level of sound `i` (dB, arbitrary reference).
- `T` is the **threshold**, the lowest the window top may sit. It stops a quiet scene from being boosted to full scale.
- `top(t)` is the level mapped to 0 dBFS at time `t`.
- `W` is the **window width** in dB. Anything more than `W` below the top is culled.
- `r` is the **release rate** in dB per second, how fast the window slides back down once the loud sound stops.
- `out_i` is what the player actually hears for sound `i`, in dBFS.

Two things to notice. First, the relative levels inside the window never change. If the gunfire is 20 dB above the footsteps in the design, it is 20 dB above them in the output, whenever both are audible. Second, the attack is instant but the release is slow. A loud sound claims the top of the mix the moment it starts. When it ends, the window takes time to come back down, and that time is a design choice.

### Numbers you can check

Take a scene with four ongoing sounds and one blast. Settings: `T = 0`, `W = 48` dB, `r = 20` dB per second.

| Sound | In-game level `L_i` |
|---|---|
| Gunfire (another squad) | +20 |
| Footsteps (your squad) | 0 |
| Birds | −15 |
| Wind | −25 |
| Explosion, from `t = 0` to `t = 0.5` s | +45 |

Before the explosion the loudest sound is the gunfire, so `top = 20`. After the explosion ends at 0.5 s, the top falls at 20 dB per second: `top(t) = 45 − 20 · (t − 0.5)` until it reaches 20 again.

| Time | Top | Gunfire | Footsteps | Birds | Wind |
|---|---|---|---|---|---|
| before | 20 | 0 | −20 | −35 | −45 |
| 0.0 to 0.5 s (blast) | 45 | −25 | −45 | culled (−60) | culled (−70) |
| 1.0 s | 35 | −15 | −35 | culled (−50) | culled (−60) |
| 1.1 s | 33 | −13 | −33 | −48 (returns) | culled (−58) |
| 1.5 s | 25 | −5 | −25 | −40 | culled (−50) |
| 1.6 s | 23 | −3 | −23 | −38 | −48 (returns) |
| 1.75 s | 20 | 0 | −20 | −35 | −45 |

You can compute the "deaf time" for any sound directly. A sound at level `L` is audible again once `top ≤ L + W`. After a peak `P` ends, that takes

```
deaf time = (P − (L + W)) / r      (zero if the result is negative)
```

Birds: `(45 − 33) / 20 = 0.6` s after the blast ends. Wind: `(45 − 23) / 20 = 1.1` s. The footsteps never drop out, because `0 + 48 = 48` is above the peak.

### A visual you can move

Open the interactive. The left view shows the in-game levels as horizontal bars and the window as a shaded band. The right view shows what comes out, a meter per sound in dBFS. Press "Explosion" and watch the band jump up. The bars on the left do not move at all. The meters on the right drop, and the birds and wind go grey. Then drag the release slider from 20 to 5 dB per second and fire again. The birds now stay gone for 2.4 seconds and the wind for 4.4, which feels like shell shock. Drag it to 80 and the ambience snaps back in a fraction of a second, and with rapid fire it pumps. The background surges up between every shot.

### Cross-game recognition

**Wwise (Audiokinetic middleware; the Wwise Help documents HDR in releases from 2015.1 through 2021.1 and later).** Wwise lets you mark a bus as an HDR bus. Its help pages describe the same window: the loudest sound maps to 0 dBFS, the window has a fixed width, sounds below it become inaudible, and the bus behaves like a limiter with "infinitesimal attack" and a user-set release. It also has a threshold described as the lowest position of the window. That is our `T`, `W` and `r` with different labels. Games built on Wwise can switch this model on without writing it.

**Sidechain ducking (radio, and every engine's mixer).** Wwise's documentation introduces side-chaining with a radio DJ whose voice automatically pushes the music down. Unity's Audio Mixer calls the same thing ducking, one group lowering another while it plays. Rewrite it in our form and you get a window with only two sounds. The "key" (dialogue) plays, and the "target" (music) drops by a fixed amount. HDR generalises this: every sound is a key for every quieter sound. Section 3 builds the two-sound version properly.

**Overwatch (Blizzard, GDC 2016).** The sound team's talk describes the goal their director set, "Play by Sound", for a shooter with 12 players whose weapons and abilities are all distinct. That goal pushes against pure HDR. In a loudness-driven window the loudest thing wins, but in a competitive game the most *dangerous* thing must win, even when it is quiet. An enemy footstep behind you matters more than your own team's explosion. Keep that tension in mind for section 4, where importance becomes a number separate from loudness.

Three contexts, one idea. A mix is a window of limited size, and something has to decide where it sits.

### Eyes-open design judgment

- **Loud is not the same as important.** HDR uses loudness as its only measure of importance. For spectacle (a war game, an action set piece) that is often right. For information (footsteps in a shooter, a boss tell in a raid) it can be exactly wrong. Designers who use HDR usually tune in-game levels by importance rather than by physical loudness, so a boss wind-up gets a higher `L_i` than its real volume would suggest.
- **Release is a feel parameter.** Slow release sells impact and disorientation. Fast release keeps information flowing but can pump. Pick it on purpose and test it with the fastest-firing weapon in the game.
- **Your own sounds may need an exemption.** If the player's own rifle is the loudest thing in the scene, the window rides on it and the player hears less of the world whenever they fire. Some games route the player's own weapon outside the HDR bus or give it a lower in-game level than it "deserves".
- **The threshold protects quiet scenes.** Without `T`, a scene with only wind would push the wind to 0 dBFS. That is the photographic auto-exposure problem, and it sounds wrong.

### Check yourself (worked example)

1. With the same scene, change `W` to 36 dB. Which sounds are culled before the explosion even starts?
2. A designer wants the birds back 0.3 s after the blast ends. Which release rate does that need?
3. A second explosion at +40 starts at `t = 0.8` s. What is the top at 0.8 s, and why?

<details>
<summary>Answers</summary>

1. Top is 20, so anything below `20 − 36 = −16` is culled. The wind (−25) is culled and the birds (−15) are just audible at −35 dBFS.
2. The birds need `top ≤ 33`. From 45 that is a fall of 12 dB in 0.3 s, so `r = 40` dB per second.
3. At 0.8 s the released top is `45 − 20 × 0.3 = 39`. The new target is 40, which is above 39, so the attack is instant and the top jumps to 40.

</details>

## 3. Ducking: one category pushes another

HDR is automatic and global. Often you want something narrower. Dialogue must be understood, so music and ambience should dip while someone speaks. A low-health heartbeat should cut through the music. These are **sidechain ducks**: the level of one signal (the **key**) controls the gain of another (the **target**).

A game ducker has four settings:

- **Depth** `D`, how far the target drops, in dB. For music under dialogue, start somewhere around 6 to 10 dB and adjust by ear. That is enough to clear space without making the music vanish.
- **Attack time** `t_a`, how long the drop takes. Short, so the first word is not masked.
- **Release time** `t_r`, how long the target takes to come back once the key stops. Longer, so the music does not bounce back between sentences.
- **Threshold**, the key level that counts as "active". In a game you often skip the audio analysis and use the event itself: if a dialogue line is playing, the key is active.

The simplest model moves the target's gain in straight lines in dB:

```
key active:    gain ← max(−D, gain − (D / t_a) · dt)
key inactive:  gain ← min(0,  gain + (D / t_r) · dt)
```

With `D = 8` dB, `t_a = 0.1` s and `t_r = 1.0` s, the music reaches −8 dB 0.1 s after a line starts. When the line ends it climbs at 8 dB per second, so it is back to −4 dB after half a second and fully back after one second.

Real compressors curve these ramps (they are usually exponential), and a real sidechain compressor ducks in proportion to how far the key exceeds a threshold. For game mixing the straight-line version is enough to reason about, and it is what the lab asks you to implement.

Three decisions deserve more thought than they usually get.

1. **What ducks what.** Write it down as a table (key down the side, target across the top, depth in the cells). If dialogue ducks music and combat also ducks music, what happens when both fire? Most engines take the deeper of the two ducks, some add them. Know which yours does.
2. **Gaps between lines.** If two lines are 0.4 s apart and the release is 0.3 s, the music surges up between them. Make release longer than your typical gap, or keep the key active across a whole conversation.
3. **Whether the player notices.** A duck the player can hear as a volume change is too deep or too fast. A duck they never notice but that makes every line clear is the goal.

## 4. Priority: deciding what plays at all

HDR and ducking change levels. They still process every sound. But an engine can only mix so many **voices** (playing sound instances) at once, because each one costs CPU for decoding, resampling, filtering and spatialising. When requests exceed the limit, something must not play. Week 14 covers the CPU and memory cost of voices. This week is about choosing which ones survive.

### The priority number

Wwise gives every sound a priority from 1 (lowest) to 100 (highest). When a playback limit is reached, the lowest-priority instance is stopped or made virtual. A **virtual voice** is one the engine keeps track of (position, elapsed time) without mixing it, so it can come back if a slot frees up. Wwise also lets priority fall with distance: you set an offset, and the priority is reduced linearly from no offset at the source to the full offset at the attenuation's maximum distance.

```
p_eff = p − offset · min(d, d_max) / d_max
```

- `p` is the base priority, `offset` the amount removed at `d_max`, `d` the distance to the listener, `d_max` the maximum distance of the sound's attenuation (week 7).

Take `p = 60`, `offset = 20` and `d_max = 40` m. At 0 m the priority is 60, at 10 m it is 55, at 20 m it is 50, at 40 m or beyond it is 40.

### Ranking under a limit

Suppose three voices remain for combat sounds, and five requests arrive:

| Request | Base `p` | Distance | Started at | `p_eff` (offset 20, `d_max` 40) |
|---|---|---|---|---|
| Boss roar | 90 | 30 m | 0.0 s | 75 |
| Your spell | 80 | 0 m | 1.0 s | 80 |
| Ally A's spell | 60 | 10 m | 0.5 s | 55 |
| Ally B's spell | 60 | 10 m | 0.2 s | 55 |
| Ambience loop | 20 | 0 m | 0.0 s | 20 |

The top three are your spell (80), the boss roar (75) and one of the allies (55). The allies tie. Wwise lets you choose whether ties discard the oldest or the newest instance. Keep the oldest and Ally B plays. Keep the newest and Ally A plays. For a long sound, like a channelled spell, keeping the oldest avoids cutting it mid-way. For short, frequent sounds, keeping the newest means the player hears what just happened.

### Kill or go virtual

When a sound loses its slot, you choose its fate:

- **Kill it.** Right for short one-shots like footsteps. By the time a slot frees up, the moment has passed.
- **Send it to virtual.** Right for loops like a torch or a waterfall. The engine keeps its clock running, so it can come back from the elapsed time when it wins a slot again.
- **Keep playing silently.** Wwise documents this option for sounds that must stay sample-accurate, like a radio the player can turn back up.

CS101 week 14 gave you the crudest version of all this: `max_polyphony`, which steals from the oldest copy of the same sound. Priority generalises it across every sound in the game.

## 5. Putting the mix together

A shipped game combines all four tools in layers:

1. **Bus structure (static).** Master, then Music, Dialogue, SFX, UI, and SFX splits into Weapons, Foley and Ambience. Each bus has a base level set in the final mix. Week 6 built this in middleware.
2. **Snapshots (state-driven).** The pause menu lowers everything but UI. Underwater applies a low-pass filter to SFX. A snapshot is a stored set of bus levels and effects that the game switches to.
3. **Ducks (event-driven).** Dialogue ducks Music and Ambience by 8 dB. The low-health heartbeat ducks Music by 4 dB.
4. **HDR or loudness window (continuous).** Optional, usually on the SFX bus only.
5. **Priority and limits (per voice).** Per-sound limits (at most 4 copies of the footstep), per-bus limits, and a global limit.

Order matters. Priority decides what exists. The HDR window and ducks decide how loud the survivors are. Buses and snapshots set the frame around all of it.

Week 8's music is a good test of this structure. Its stems add up to about +6 dB at full intensity, exactly when combat effects are busiest. A duck from the SFX bus onto the music bus, or a snapshot for combat, is where you decide what gives way.

A useful habit when you debug a mix is to ask the three questions in that order. Is the sound playing at all (priority)? Is it being pushed down (ducks, HDR)? Is its bus too quiet (static mix)? Middleware profilers show all three. Guessing at the bus fader first wastes hours.

## In-class activity (25 minutes)

In groups of three, you are mixing a raid boss phase in a fantasy MMO. The boss has a 3-second wind-up tell before a wipe-level attack, the raid leader's voice chat is running, the music is at full intensity, and 20 players are casting.

1. Draw the bus tree (at least 8 buses).
2. Fill a duck table: which keys duck which targets, by how many dB, with what attack and release.
3. Write a priority table for six sounds: boss wind-up, player's own spell, ally spells, footsteps, boss music stem, ambience. Include the distance offset where it applies.
4. Decide whether you would put SFX on an HDR bus. If yes, give `T`, `W` and `r`, and say what in-game level the boss wind-up gets and why.

Expected output: one page with the tree, the two tables and a three-sentence HDR decision. Swap with another group and find the one situation where their wind-up tell would not be heard.

## Common misconceptions

- **"If it matters, make it louder."** Raising one sound raises the total and eats headroom, and in an HDR mix it pushes the window up so everything else drops. Make other things quieter, or give the important sound priority and a duck.
- **"Two sounds at −20 dB make −10 dB."** Uncorrelated sounds add in power: two give −17 dB. Only identical, time-aligned copies add in amplitude, giving −14 dB.
- **"HDR makes quiet sounds quieter."** It never changes their design level. It moves the window. Once the loud sound ends and the release runs, the quiet sounds come back at exactly their old output level.
- **"Priority is about volume."** Priority decides whether a voice gets a slot. A high-priority sound can still be quiet, and a loud sound can be culled if its priority is low.

## Check yourself

1. A town square has 12 fountain and crowd loops, each at −24 dBFS on its own. What is their combined level? How much would you need to lower each to keep the total at −18 dBFS?
2. An HDR bus has `T = 0`, `W = 40` and `r = 30` dB per second. A spell impact at +50 ends. How long until a campfire at −5 becomes audible again?
3. Dialogue ducks music by 10 dB with a 0.05 s attack and a 0.5 s release. Two lines are separated by a 0.25 s gap. How low does the music get and how high does it recover during the gap?
4. With `p = 70`, `offset = 30`, `d_max = 60` m, what is the effective priority at 15 m and at 90 m?
5. A designer says, "Our HDR mix is great, but players can't hear enemy footsteps in big fights." Explain why HDR causes this, and propose two fixes.

<details>
<summary>Answers</summary>

1. `−24 + 10 · log10(12) = −24 + 10.8 = −13.2` dBFS. To reach −18 you need each loop 4.8 dB lower, at about −28.8 dBFS.
2. The campfire needs `top ≤ −5 + 40 = 35`. From 50 that is 15 dB at 30 dB per second, so 0.5 s.
3. The attack rate is 200 dB per second, so the music reaches −10 dB in 0.05 s. The release rate is `10 / 0.5 = 20` dB per second, so in a 0.25 s gap it recovers 5 dB, to −5 dB, before the next line pushes it down again. The music audibly swells between lines. Lengthen the release or hold the key across the conversation.
4. At 15 m: `70 − 30 × 15/60 = 62.5`. At 90 m the offset is capped: `70 − 30 = 40`.
5. Footsteps have a low in-game level, so any explosion or spell pushes the window over them and they are culled for the whole fight. Fixes: raise the footsteps' in-game level above their physical loudness (tune by importance), route enemy footsteps to a bus outside HDR with a high priority, or duck the SFX bus a few dB when an enemy is within footstep range.

</details>

## Lab / assignment hook

[Lab 10, build the mix brain](../labs/lab10.md). You implement the power sum, the HDR window, a ducker and a priority allocator in standard-library Python, check them against this lecture's tables, then tune the release rate for a scene of your own. The allocator comes back in week 12, where forty players share one mix.

## Sources

- Audiokinetic, Wwise Help, "Understanding HDR" (Wwise 2021.1.4 documentation, Internet Archive snapshot of 17 October 2021; the page offers the same topic for versions 2015.1 to 2021.1). HDR maps the loudest sound to 0 dBFS, a fixed-width window, sounds below the window become inaudible, the window slides back gently after a loud sound ends.
- Audiokinetic, Wwise Help, "Using HDR" (Wwise 2021.1 documentation). The HDR bus as a limiter with "infinitesimal attack" and user-defined release; the threshold as the lowest window position.
- Audiokinetic, Wwise Help, "Defining playback priority" (Wwise 2024.1.5.8803 documentation, Internet Archive snapshot of 14 June 2025, checked 29 September 2026). Priority 1 (lowest) to 100 (highest); stop the newest or oldest instance on equal priority; offset interpolated linearly from none at the source to the full offset at the attenuation's max distance.
- Audiokinetic, Wwise Help, "Limiting object playback instances" and "Managing low-volume objects" (Wwise 2024.1 documentation). Kill, virtual voice and continue-to-play behaviours.
- Audiokinetic, Wwise Help, "Using side-chaining" (Wwise 2024.1.5.8803 documentation, Internet Archive snapshot of 14 June 2025, checked 29 September 2026). Side-chaining defined as monitoring one signal's level to control another, with the radio DJ whose voice ducks the music.
- Wikipedia, "High dynamic range", audio section, citing EA DICE's *Battlefield: Bad Company* Frostbite engine trailer (2007). HDR Audio in the Frostbite engine lets louder sounds drown out softer ones. Wikipedia, "Frostbite (game engine)": first released in 2008 for *Battlefield: Bad Company*.
- Unity Manual, "Audio Mixer" overview (Unity 6 documentation, accessed September 2026). Ducking described as one category of sound lowering another while it plays.
- Lawlor, S. & Neumann, T. (2016). "Overwatch: The Elusive Goal, Play by Sound". GDC 2016, GDC Vault session overview. The "Play by Sound" goal; 12 players with unique weapons and abilities.
- Collins, K. (2008). *Game Sound*. MIT Press.

## Interactive spec: examples/w10-hdr-window.html

**Purpose.** Make visible that an HDR mix never changes a sound's design level. It slides a window, and the release rate decides how long quiet sounds stay culled after a loud one.

**Layout.** Two linked views side by side (stacked on phones).

- *Left, "In the game world"*: a vertical dB axis from −40 to +60. One horizontal bar per sound at its in-game level `L_i`, labelled. A translucent band from `top − W` to `top` is the window, with a dashed line at `T`. Bars inside the band are coloured by category; bars below it are grey with a "culled" tag.
- *Right, "What the player hears"*: one vertical meter per sound, axis 0 to −60 dBFS, showing `out_i = L_i − top`, grey and empty when culled. Under the meters, a scrolling 4-second strip chart of `top(t)`.

**Sounds (defaults, editable levels via small number inputs).** Gunfire +20, Footsteps 0, Birds −15, Wind −25, Explosion +45 (plays for 0.5 s when triggered). Optional sixth sound "Enemy footstep" −5, off by default, toggled by a checkbox, to support check-yourself question 5.

**Controls.**
- Button "Explosion" (also key `E`). Triggers the +45 sound for 0.5 s.
- Button "Rapid fire" (key `R`). Triggers five +35 shots, 0.5 s on each, starting 0.6 s apart (so a 0.1 s gap between shots), to demonstrate pumping at high release rates.
- Slider release `r`: 5 to 80 dB/s, step 1, default 20.
- Slider window `W`: 24 to 72 dB, step 1, default 48.
- Slider threshold `T`: −20 to +20, step 1, default 0.
- Toggle "Hear it". Off by default. When on, each sound is a procedural Web Audio source whose gain is `10^(out_i/20)` (0 when culled): gunfire = bursts of filtered noise at 6 Hz, footsteps = short low noise clicks at 2 Hz, birds = sine chirps (2 to 4 kHz sweeps, random every 0.4 to 1.2 s), wind = low-passed pink-ish noise, explosion = a noise burst through a low-pass that falls from 2 kHz to 200 Hz with a 1.5 s decay. Master gain 0.25. No audio files.

**Exact rules.** Simulate at a fixed 50 Hz tick (`dt = 0.02`) regardless of frame rate, using the lecture's model: target = max(T, loudest active level); instant attack; release `top = max(target, top − r·dt)`; audible when `out_i ≥ −W`. An event with `t_on ≤ t ≤ t_off` counts as active (release starts at `t_off`). Report each "back after" time as the exact crossing inside the tick, found by interpolating the linear release, not as the first whole tick where the sound is audible. The two differ by up to one tick: with `r = 40` the wind crosses at 0.55 s, while plain tick counting would show 0.56 s.

**Readouts.** Current top (1 decimal), each `out_i` (1 decimal or "culled"), and after each explosion "Birds back after X.XX s, Wind back after Y.YY s", measured from the end of the blast.

**Test values (defaults).** Before explosion: top 20.0, outputs 0, −20, −35, −45. During: top 45.0, gunfire −25, footsteps −45, birds and wind culled. Birds back after 0.60 s, wind back after 1.10 s. With `r = 40`: 0.30 s and 0.55 s. With `W = 36` and no explosion, wind is culled and birds read −35.

**The one insight.** On first load, auto-trigger one explosion after 1 s so the first thing the student sees is the band jumping while the left-hand bars stay still.

**Accessibility.** All controls keyboard reachable with visible focus; meters have text values; `prefers-reduced-motion` replaces the strip chart animation with a static redraw every 250 ms; light and dark palettes from `templates/interactive-tokens.css`.
