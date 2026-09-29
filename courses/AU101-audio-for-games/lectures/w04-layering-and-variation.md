# AU101 · Week 04 — Layering and Variation: Beating the Machine-Gun Effect

**Why this matters:** A sound that plays the same way every time stops sounding like a thing in the world and starts sounding like a computer. Players can't always name the problem, but they hear it within a few repeats. This week you learn to measure repetition, to build one sound from parts so its variety multiplies, and to decide which sounds should not vary at all.

**You will be able to:**
- Compute the repeat chance of a sound setup from its variant counts, weights and pitch distribution.
- Design a layered sound (transient, body, tail) and predict how many distinct combinations it yields for a given number of files.
- Configure variation in an engine or middleware (file pools, no-repeat rules, pitch and volume ranges) and explain what each setting does to the repeat chance.
- Critique a sound set and decide which sounds need more variation and which must stay fixed because they carry information.

**Before class:** Reread section 4 of [CS101 week 14](../../CS101-programming-for-games-i/lectures/w14-polish-pass-sound-particles-screen-shake.md) (pitch in semitones and volume in decibels; about 10 minutes). Read the FMOD Studio User Manual (version 2.03), Instrument Reference, the "Playlist Selection Mode" entry for multi instruments, and the Modulator Reference, "Random Modulator" (about 15 minutes). Skim the Unity 6.2 Manual page "Audio Random Container reference".

**Prerequisites from earlier courses:** [CS101 week 14, polish pass](../../CS101-programming-for-games-i/lectures/w14-polish-pass-sound-particles-screen-shake.md) introduced `2^(s/12)` for semitones and `20 × log10` for decibels. This lecture assumes both. [CS101 week 13, randomness](../../CS101-programming-for-games-i/lectures/w13-randomness-spawning-and-procedural-variety.md) covered no-repeat rules and shuffle bags for Tetris pieces; you will meet the same rules applied to sound files. [MA102 week 2, independent events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md) has the multiplication rule that makes layering work. From this course, [AU101 week 3, synthesis for SFX](w03-synthesis-for-sfx.md) gives you the noise bursts and envelopes the interactive uses.

**Interactive:** [examples/w04-machine-gun.html](../examples/w04-machine-gun.html). Keep it open, with headphones, during section 2.

---

## 1. Why exact repeats sound wrong

Hit a table with your knuckle ten times. No two knocks are the same. Your hand lands a few millimetres to the side, a little harder, at a slightly different angle, and the table rings a little differently each time. Your ears have heard real-world repetition all your life, and it always carries small differences.

Now play one recorded knock ten times from a game engine. Every copy is identical to the last sample. The ear notices this quickly, especially when the sound repeats fast. Sound designers call the result the **machine-gun effect**: a rapid string of identical copies that sounds mechanical, like a stuck record, even when the source is a footstep or a sword swing.

The name is a little ironic. Real machine guns don't produce identical shots either. What sounds "machine-like" is the digital copy.

Two terms first:

- A **variant** is one of several recordings (or synthesized versions) of the same event. Six footstep recordings on stone are six variants.
- **Variation** is any change made at playback time to avoid identical copies. The common ones are choosing a different variant, shifting pitch, shifting volume, starting at a slightly different point in the file, and filtering.

There is a second reason to care about repetition, and it pulls the other way. A sound is also a **signal**. When players learn that a certain "ding" means "item picked up", they react to the sound before they read any text. If that ding changes too much, it stops being recognizable. So variation is a dial, not a switch. You will spend part of this lecture deciding where to set it for each sound.

## 2. Worked example: the machine-gun effect, measured

### The hook

In the original Doom (id Software, 1993), the chaingun fires one bullet every 4 game tics. Doom runs its game logic at 35 tics per second, so the chaingun fires 8.75 shots per second. Each shot calls the sound code with `sfx_pistol`. The chaingun has no gunshot of its own. It plays the pistol sample, fast.

Here is the surprise. The Doom source code that id released in 1997 contains a block commented "hacks to vary the sfx pitches". Before every sound starts, the code adds a random offset to the pitch, so no two pistol shots need to match. Chocolate Doom, a source port built to reproduce the DOS versions exactly, supports this "pitch-shifting from early versions of Doom" but turns it off by default for Doom, because later releases played every sound at its normal pitch. For Heretic (Raven Software, 1994), built on the same engine, Chocolate Doom turns it on by default.

So the same chaingun has shipped both ways, and players could compare. Which version repeats less, and by how much? To answer that you need a number for "how repetitive is this sound setup". This section builds that number.

### The model: repeat chance

Each time a sound plays, the game picks an **outcome**: which variant, at which pitch, at which volume. Suppose there are several possible outcomes, and outcome `i` has probability `p_i`. The chance that two plays in a row give the exact same outcome is:

```
R = p_1² + p_2² + ... + p_n²          (repeat chance)
```

- `R` is the **repeat chance**, the probability that the next play is an exact copy of the previous one.
- `p_i` is the probability of outcome `i`. The probabilities add up to 1.

Why squares? The two plays are independent, so the chance that both land on outcome `i` is `p_i × p_i`. Add that up over every outcome and you get `R`.

Two special cases do most of the work:

- **Uniform choice.** If all `n` outcomes are equally likely, every `p_i = 1/n`, and `R = n × (1/n)² = 1/n`. Six equally likely files give `R = 1/6`.
- **Independent parts multiply.** If a sound is built from parts that are chosen independently (a file and a pitch, or three layers), a repeat of the whole needs a repeat of every part at once, so `R_total = R_1 × R_2 × R_3`.

The cost side is just as simple. **Files add.** Three layers with four variants each need `4 + 4 + 4 = 12` files in memory, and they give `4 × 4 × 4 = 64` combinations. That asymmetry is the whole case for layering: variety multiplies while memory adds.

Over a burst of `N` plays there are `N − 1` neighbouring pairs, so:

```
expected exact repeats in a burst = (N − 1) × R
P(at least one exact repeat)      = 1 − (1 − R)^(N − 1)
```

One caution before the numbers. `R` counts *exact* copies. Two pitches a tiny fraction of a semitone apart may be different numbers but sound the same. The model gives a floor for how repetitive a setup sounds, not a ceiling, and the interactive lets you merge nearby pitches into groups to see how much that matters.

### Numbers you can check

Start with Doom. The code adds `16 − (random & 31)` to a normal pitch of 128. `random & 31` is a whole number from 0 to 31, so the offset runs from −15 to +16, 32 values, all equally likely. With one file and 32 pitches, `R = 1/32 ≈ 3.1%`.

How wide is that range in semitones? Chocolate Doom approximates the original sound library's pitch by changing the sample length by a factor of `2 − pitch/128`. At pitch 144 the length is 0.875 of normal, so playback runs `1 / 0.875 = 1.143` times faster, which is `12 × log2(1.143) ≈ +2.3` semitones. At pitch 113 the factor is 1.117, about −1.9 semitones. Doom's pistol wanders across roughly four semitones, in 32 steps.

Heretic uses a different rule: `(random & 7) − (random & 7)`. Two numbers from 0 to 7, subtracted. The result runs from −7 to +7, 15 values, but they are not equally likely. There are 8 ways to get 0 (both rolls equal) and only 1 way to get +7. That is a triangular distribution, the same shape you get from the difference of two dice. Squaring and adding the 15 probabilities gives `R = 344 / 4096 ≈ 8.4%`. Fewer outcomes, and the likely ones cluster in the middle, so the repeat chance is almost three times Doom's.

Now the full table for a 10-shot burst (9 neighbouring pairs):

| Setup | Outcomes | Repeat chance R | Expected repeats in 10 shots | P(at least one repeat) | Files in memory |
|---|---|---|---|---|---|
| One file, fixed pitch (Doom, later releases) | 1 | 100% | 9 | 100% | 1 |
| One file, Heretic pitch rule | 15, triangular | 8.4% | 0.76 | 55% | 1 |
| One file, Doom pitch rule | 32, uniform | 3.1% | 0.28 | 25% | 1 |
| Six files, uniform random | 6 | 16.7% | 1.5 | 81% | 6 |
| Six files, never the same twice in a row | 6 | 0% | 0 | 0% | 6 |
| Twelve files, uniform random | 12 | 8.3% | 0.75 | 54% | 12 |
| Three layers × four variants, uniform | 64 | 1.6% | 0.14 | 13% | 12 |

Read the last two rows together. Same twelve files. Arranged as twelve whole sounds, they repeat in more than half of all bursts. Arranged as three layers of four, they repeat in about one burst in eight. Nothing changed but the arrangement.

Read rows 1 and 3 together. A single random pitch offset turns a guaranteed 9 repeats into about a quarter of a repeat per burst, with zero extra memory. That's why every engine you'll use ships pitch randomization, and why Doom's programmers bothered in 1993.

And row 5 shows that a memory rule can beat any pool size. "Never the same file twice in a row" sets the file-level repeat chance to zero. You'll see below that middleware ships exactly this rule.

### Code you can run

```python
from collections import Counter

def repeat_chance(weights):
    """Chance that two plays in a row give the same outcome."""
    total = sum(weights)
    return sum((w / total) ** 2 for w in weights)

doom = [1] * 32                        # 32 equally likely pitch offsets
heretic = Counter(a - b for a in range(8) for b in range(8))
layers = repeat_chance([1] * 4) ** 3   # 3 layers, 4 variants each

print(f"one file, fixed pitch: {repeat_chance([1]):.4f}")
print(f"Doom pitch offsets:    {repeat_chance(doom):.4f}")
print(f"Heretic pitch offsets: {repeat_chance(list(heretic.values())):.4f}")
print(f"six files, uniform:    {repeat_chance([1] * 6):.4f}")
print(f"3 layers x 4 variants: {layers:.4f}")
for name, r in [("fixed", 1.0), ("Doom", 1 / 32), ("layers", layers)]:
    print(f"{name:>6}: P(at least one repeat in 10 shots) = {1 - (1 - r) ** 9:.3f}")
```

Output:

```
one file, fixed pitch: 1.0000
Doom pitch offsets:    0.0312
Heretic pitch offsets: 0.0840
six files, uniform:    0.1667
3 layers x 4 variants: 0.0156
 fixed: P(at least one repeat in 10 shots) = 1.000
  Doom: P(at least one repeat in 10 shots) = 0.249
layers: P(at least one repeat in 10 shots) = 0.132
```

`repeat_chance` takes weights rather than probabilities because that's how tools store them. A Minecraft `sounds.json` entry with `weight: 2` counts as two entries, and the function divides by the total for you.

### A visual you can move

Open [`examples/w04-machine-gun.html`](../examples/w04-machine-gun.html). The top button fires a burst of 10 procedurally generated gunshots at Doom's chaingun rate, 8.75 per second. Below it, a strip of 10 tiles shows each shot as a coloured fingerprint: its layer variants and its pitch group. Identical shots get identical tiles, and exact repeats of the previous shot get a red outline.

Start in "Same sample × 10". Listen, then look: ten identical tiles, nine red outlines. Switch to "Doom pitch" and fire again. The tiles now differ, and the readout shows `R = 3.1%`. Now widen the "sounds the same within" slider to half a semitone. Neighbouring pitches merge, the number of outcomes drops from 32 to about 9, and `R` climbs to around 11%. The two views disagree on purpose. The tiles show what the computer did, and the grouped view shows what your ear probably gets. Finally switch to "3 layers × 4" with ±1 semitone of pitch and watch the long-run counter. Over 1,000 simulated bursts, the repeat count settles close to the model's prediction.

### Cross-game recognition

The formula hides in every tool. Your job is to find the `p_i` and the independent parts.

**Heretic (1994).** Already in the table. Its rule is the difference of two random numbers, so it produces a triangular pitch distribution. That favours pitches near normal, which keeps the weapon's identity steady while still avoiding exact copies. The price is a higher repeat chance than a uniform rule with the same number of outcomes. Heretic also uses an even narrower rule, `(random & 3) − (random & 3)`, for its ambient sounds (7 outcomes, `R = 44/256 ≈ 17%`).

**Minecraft (Java Edition 1.21.4).** Each sound event in `sounds.json` lists one or more files, and the game picks one at random each time the event fires. `block.stone.step` lists six files, `entity.generic.explode` lists four, and `entity.player.hurt` lists three. Each entry can carry an integer `weight` (default 1), and a weight of 2 is documented as the same as listing the file twice. In our model, the weights are the `p_i` before dividing by the total. Six equal stone steps give `R = 1/6`. If a resource pack gave one of them weight 6 and left the other five at 1, the repeat chance would jump to `(36 + 5) / 121 ≈ 34%`. Weights change repetition as well as frequency.

**FMOD Studio (2.03).** A multi instrument holds a playlist, and its "Playlist Selection Mode" has two random options. **Randomize** has no memory: past picks don't affect future ones, so a playlist of `n` equal items gives `R = 1/n`. **Shuffle** also picks at random, but as long as the playlist has at least three items and no play percentages, no item plays twice in a row. That rule sets the file-level repeat chance to 0. Pitch and volume variation come from a **random modulator**. On pitch, its range is centred on the current value. On a property measured in dB, the manual says the range runs from the current value *down* by the modulator's amount, so a 3 dB random modulator on volume gives levels between −3 dB and 0 dB, never louder. That keeps randomization from pushing a sound into clipping.

**Unity (Unity 6.2, Audio Random Container).** Unity's container has three playback modes. **Random** keeps every clip in the pool after it plays, and an "Avoid Repeating Last" setting lets you say how many other items must play before one can repeat. **Shuffle** removes clips from the pool as they play, so nothing repeats until every clip has played once. That's the Tetris 7-bag from CS101 week 13. Pitch randomization is set in **cents** (hundredths of a semitone), so ±100 cents is ±1 semitone.

Notice the naming clash. FMOD's "Shuffle" means "not twice in a row". Unity's "Shuffle" means "a bag". Both lower `R`, but they produce different streaks, and a sound designer moving between tools can get caught out. Always read what a mode does, not what it is called.

### Design judgment

Repeat chance is a tool for spotting problems, not a score to minimize. Before you add variants, decide these things on purpose.

- **How fast does the sound repeat?** Repetition is heard in bursts. A door that opens once a minute can have one file. A footstep at 2 per second, or an automatic weapon at 8 or more per second, needs a low `R`. Budget variation where the repeat rate is high.
- **Is the sound a signal?** Doom's pitch code exempts two sounds: `sfx_itemup` (item pickup) and `sfx_tink`. It also gives the chainsaw a narrower range (`8 − (random & 15)`, 16 values) than everything else. Whatever the programmers' reasons, the result fits a sensible rule. Confirmation and UI sounds (week 11) should be recognizable in a fraction of a second, so give them little or no variation.
- **How wide can the range go before identity breaks?** CS101 week 14 showed that ±4 semitones on a rapid gun starts to sound like a melody. Pitch shifting also changes length (a sample played faster is shorter), and large shifts make recordings sound small or huge. Keep pitch ranges narrow (about ±1 to ±2 semitones) and get the rest of your variety from files and layers.
- **Memory has a real price.** Twelve files cost twelve times one file. On a small platform, or for the hundreds of sounds in an MMO (week 12), the layering trick (multiply variety, add memory) is often the only way to afford variety at all.
- **Memory rules change streak shape.** "Not twice in a row" removes immediate repeats but allows A-B-A-B patterns. A bag removes all repeats within one cycle but makes the last item of each bag predictable. Pick the rule whose failure you mind least.

## 3. Layering: one sound from several parts

A **layer** is one part of a sound that plays at the same moment as the others. Most punchy game sounds are three layers or more, each doing a different job in time and frequency:

| Layer | Job | Typical length | Where its energy sits |
|---|---|---|---|
| Transient | The sharp start that tells you *when* | 5-30 ms | High frequencies, fast attack |
| Body | The weight, what the thing *is* | 50-300 ms | Low and mid frequencies |
| Tail | The space it happens in | 0.3-2 s | Reverb, echo, debris |

A sword hit might be a metal "tick" for the transient, a thud from a punched cushion for the body, and a short ring for the tail. A gunshot might be a click, a low boom and an outdoor echo. None of those needs to come from a real sword or gun. Last week's synthesis tools can generate any of them.

Layering does two things for you. It lets you build a sound no single recording has, and it gives the variety multiplier from section 2. Because each layer is picked independently, three small pools produce many combinations.

### Adding layers changes loudness

When you stack layers, the result gets louder, and how much louder depends on how alike the layers are.

- Two **identical** layers, perfectly lined up, add their amplitudes. Twice the amplitude is `20 × log10(2) ≈ +6.0 dB`.
- Two **unrelated** layers of equal level (different recordings, noise from different seeds) add their *power*, not their amplitude. Twice the power is `10 × log10(2) ≈ +3.0 dB`.
- Two identical layers that are **out of step** can cancel. If one is flipped (its waveform inverted), or delayed by half a cycle of a strong low tone, the sum can be quieter than either layer alone. This is **phase cancellation**, and it's the classic layering bug: a big low "boom" layer that goes thin when you add a second boom.

Practical rules follow. Don't stack two recordings of the same event in the same frequency range. Give each layer its own band and job. And when pitch randomization is applied per layer, check the worst case: two low layers pitched in opposite directions can beat against each other audibly.

### Per-layer or whole-sound variation?

You can randomize each layer separately or randomize the finished sound as one. Per-layer randomization multiplies variety further. Whole-sound randomization keeps the layers in their designed relationship (the transient stays aligned with the body). A common split is to pick variants per layer and apply one pitch offset to the whole sound. In FMOD, that means multi instruments on each track and the random pitch modulator on the event. In Unity, one Audio Random Container per layer, each on its own source, played together.

## 4. Which axes to vary, and by how much

The repeat-chance model treats every axis the same way, so you can compare them directly. What differs is what each axis costs and how far you can push it.

| Axis | Adds outcomes by | Memory cost | Safe range (starting point) | Risk if pushed |
|---|---|---|---|---|
| File choice | Number of variants | One file each | 3-8 variants for frequent sounds | Memory, recording time |
| Pitch | Distinguishable steps in the range | None | ±1 to ±2 semitones | Melody effect, size change, length change |
| Volume | Distinguishable steps | None | 0 to −3 dB (downward only) | Reads as distance change, not variety |
| Start offset | Skip 0-20 ms of the file | None | A few ms, only on sustained sounds | Cuts off the transient |
| Filter | Cutoff steps | Small CPU | Mild low-pass range | Reads as distance or muffling |
| Layer variants | Multiplies with other layers | One file per variant | 2-4 per layer | Phase issues, mix density |

Volume deserves a warning. Our ears are less sensitive to small level changes than to small pitch changes, and a large random drop reads as "that shot came from further away". Keep volume variation small and downward, as FMOD's random modulator does for dB properties.

When is a sound varied *enough*? A practical test: play the busiest realistic sequence (a full magazine, a sprint across stone, a crowd of enemies attacking at once) and listen for any exact repeat you can pick out. If you hear one, first add a no-repeat rule, then widen pitch slightly, and only then record more variants. That order goes from cheapest to most expensive.

## In-class activity (25 minutes)

Work in pairs. You have a memory budget of **12 sound files** for a character's sword attack, which plays up to 3 times per second in combos.

1. Propose two designs that use at most 12 files. Design A uses whole-sound variants only. Design B uses layers (choose how many layers and how many variants each).
2. For each design, compute `R` with uniform picks, then with a no-repeat rule on each pool. Add a pitch range you'd accept and count its outcomes using half-semitone groups (a ±1 semitone range is 2 semitones wide, so it holds 4 half-semitone groups).
3. Compute the chance of at least one exact repeat in a 9-hit combo for each design.
4. Name one sound in the same game that should *not* vary, and say why in one sentence.

Expected output: a small table with both designs, their file counts, `R` values and burst repeat chances, plus your one-sentence exemption. Be ready to defend the number of layers you chose.

## Common misconceptions

- **"More files always means less repetition."** Twelve whole files repeat more than three layers of four. Arrangement matters as much as count. And a no-repeat rule on six files beats uniform random on twelve for immediate repeats.
- **"Random pitch is enough on its own."** It removes exact copies, but the ear groups nearby pitches, so 32 tiny steps behave more like 8 or 9 audible ones. Pitch helps most when combined with file variants.
- **"Shuffle means the same thing everywhere."** In FMOD it means "no item twice in a row". In Unity's Audio Random Container it means a bag that plays every clip before any repeats. Read the mode's description.
- **"Every sound should vary."** Signal sounds (pickups, UI confirmations, warnings) earn their value from being identical. Doom's own pitch code leaves the item pickup alone.

## Check yourself

1. A footstep event has 5 files with weights 3, 1, 1, 1, 1. What is its repeat chance? How does that compare with 5 equal weights?
2. A designer has 9 files for an impact. Option A is 9 whole variants. Option B is 3 layers of 3. Compute `R` for each with uniform picks, and the chance of at least one exact repeat in a burst of 6 impacts.
3. A gun uses one file and uniform pitch over 11 outcomes. The team adds a second, independent file pool of 4 variants, picked with a "never twice in a row" rule. What is `R` for the whole sound?
4. Heretic's ambient rule is `(random & 3) − (random & 3)`. List the outcomes with their counts out of 16, and verify `R = 44/256`.
5. You randomize volume by up to 6 dB, centred on normal (from −3 to +3 dB). Name two problems this can cause and a better setting.

<details>
<summary>Answers</summary>

1. Probabilities are 3/7 and four of 1/7. `R = (9 + 1 + 1 + 1 + 1) / 49 = 13/49 ≈ 26.5%`. With 5 equal weights, `R = 1/5 = 20%`. The heavy file makes repeats more likely.
2. A: `R = 1/9 ≈ 11.1%`, and with 5 pairs `1 − (8/9)^5 ≈ 44.5%`. B: `R = (1/3)^3 = 1/27 ≈ 3.7%`, and `1 − (26/27)^5 ≈ 17.2%`. Same files, less than half the repeat chance.
3. A repeat of the whole needs a repeat of the pitch *and* of the file. The file pool never repeats immediately, so its `R = 0`, and the product is 0. (Pitch-only repeats still happen 1 time in 11, but the file differs each time.)
4. Differences −3 to +3 with counts 1, 2, 3, 4, 3, 2, 1 out of 16. `R = (1 + 4 + 9 + 16 + 9 + 4 + 1) / 256 = 44/256 ≈ 17.2%`.
5. Shots up to +3 dB can clip or poke out of the mix, and large drops read as distance changes rather than variety. Use a small downward range (for example 0 to −2 dB), as FMOD's random modulator does for dB properties, and get variety from files and pitch instead.

</details>

## Lab / assignment hook

[Lab 04, the variation engine](../labs/lab04.md). You'll implement `repeat_chance`, a no-repeat picker and a burst planner in Python, render a "same sample × 10" burst and a layered burst to WAV files, and compare them by ear and by number. The layered sound you design in the lab's second part is the first entry in your **SFX pack** assignment (30% of the course grade).

## Sources

- id Software, DOOM source code, `linuxdoom-1.10/s_sound.c` (released 1997, GitHub `id-Software/DOOM`). The "hacks to vary the sfx pitches" block: offset `16 − (M_Random() & 31)` on a normal pitch of 128 for most sounds, `8 − (M_Random() & 15)` for the chainsaw sounds, none for `sfx_itemup` and `sfx_tink`. Also `doomdef.h` (`TICRATE 35`), `info.c` (chaingun firing states of 4 tics each) and `p_pspr.c` (`A_FireCGun` starts `sfx_pistol`).
- Chocolate Doom, source and release notes (GitHub `chocolate-doom/chocolate-doom`, master branch, 2026). `src/doom/s_sound.c` (pitch-shifting off by default for Doom), `src/heretic/s_sound.c` (Heretic rules `(M_Random() & 7) − (M_Random() & 7)` and `(M_Random() & 3) − (M_Random() & 3)`, on by default), `src/i_sdlsound.c` (the length approximation `1 + (1 − pitch/128)`, described as based on measurements of the original), `NEWS.md` ("pitch-shifting from early versions of Doom, Heretic, and Hexen").
- Minecraft Wiki, "sounds.json" (Java Edition). One listed sound chosen at random per event; `weight` integer, default 1, weight 2 equal to listing twice. Event file lists from the Java Edition 1.21.4 asset `sounds.json` (as mirrored in GitHub `InventivetalentDev/minecraft-assets`, branch 1.21.4): six files for `block.stone.step`, four for `entity.generic.explode`, three for `entity.player.hurt`.
- Firelight Technologies, FMOD Studio User Manual 2.03 (2.03.14, May 2026), Instrument Reference, "Playlist Selection Mode" (Shuffle, Randomize, sequential modes; the three-item, no-play-percentage condition), and Modulator Reference, "Random Modulator" (downward range on dB properties, centred range otherwise, pitch range up to 48 semitones).
- Unity Technologies, Unity 6.2 Manual, "Audio Random Container reference". Sequential, Shuffle and Random modes; "Avoid Repeating Last"; pitch randomization in cents; the Pulse trigger mode.
- Collins, K. (2008). *Game Sound: An Introduction to the History, Theory, and Practice of Video Game Music and Sound Design*. MIT Press. Course reading, chapters 1-3.

## Interactive spec: examples/w04-machine-gun.html

**The one insight:** the same twelve files repeat far less when arranged as layers than as whole sounds, and a no-repeat rule removes immediate repeats outright. A second insight sits in the grouping slider: the computer's count of distinct outcomes overstates what the ear hears, because nearby pitches merge.

**Layout.** Two linked views plus a control panel. Mobile: stacked (burst strip, then stats, then controls). From 900 px: burst strip and stats on the left (60%), controls on the right.

- **Top view, "Burst":** a row of 10 tiles, one per shot in the most recent burst, animated left to right in time with playback (static when `prefers-reduced-motion` is set). Each tile shows the shot's fingerprint: one small coloured bar per layer, the bar's colour picked by variant index from a fixed 4-colour palette, and a small pitch label in semitones to one decimal (for example `+1.2`). Tiles whose fingerprint exactly matches the previous tile get a red outline (the damage red token) and the label "repeat". When the grouping slider is above 0, a second, dotted outline marks tiles that match the previous tile *within the grouping* but not exactly.
- **Bottom view, "Long run":** a bar chart with two bars per mode: predicted expected repeats per 10-shot burst `9 × R` and measured average over simulated bursts. A "Simulate 1,000 bursts" button runs silently and fills the measured bar. Exact numbers print above each bar to 2 decimals.

**Sound generation (Web Audio API, all procedural, no audio files).** One `AudioContext`, created on the first user gesture. A gunshot is up to three layers, each an `AudioBufferSourceNode` playing a pre-rendered buffer, summed into a `GainNode` then a `DynamicsCompressorNode` (threshold −6 dB) to prevent clipping, then the destination.

- Transient layer, 4 variants: white noise, 20 ms, exponential decay (time constant 4 ms), through a high-pass at 2,000 Hz. Variants differ by noise seed (seeded PRNG, mulberry32 with seeds 11, 12, 13, 14) and high-pass cutoff (2,000, 2,400, 2,800, 3,200 Hz).
- Body layer, 4 variants: a sine sweep from `f0` to 50 Hz over 120 ms with exponential amplitude decay (time constant 40 ms), `f0` = 140, 160, 180, 200 Hz, plus low-passed noise (cutoff 800 Hz) at −12 dB relative, seeds 21 to 24.
- Tail layer, 4 variants: noise, 600 ms, decay time constant 150 ms, band-pass centred at 500, 600, 700, 800 Hz, Q 0.7, seeds 31 to 34, at −10 dB relative.
- Pre-render all 12 buffers once with `OfflineAudioContext` at 44.1 kHz. Pitch shift a shot by setting `playbackRate = 2^(s/12)` on every layer's source. Volume offset by a gain of `10^(g/20)`.
- Shots are scheduled on the audio clock (`start(ctx.currentTime + 0.05 + k × interval)`), never with `setTimeout`, so timing is exact. Interval default `4/35` s (Doom chaingun, 8.75 shots per second).

**Controls.**
- Mode (radio, keyboard selectable): "Same sample × 10" (body variant 0 only, no pitch, no volume change); "Doom pitch" (body variant 0 only, pitch offset from Doom's rule mapped to semitones with `s = 12 × log2(1 / (2 − (128 + k)/128))`, `k` uniform integer in −15..16); "Heretic pitch" (as Doom but `k = a − b`, `a, b` uniform in 0..7); "12 whole variants" (12 precomputed full shots, each one transient + body + tail combination fixed: shot `j` uses transient `j mod 4`, body `floor(j/3) mod 4`, tail `(j + 1) mod 4`, uniform pick among the 12); "3 layers × 4" (each layer picked uniformly and independently).
- Toggle "No repeat": when on, each pool never picks the same index twice in a row (reroll until different). For "12 whole variants" it applies to the 12 pool.
- Pitch range: slider 0 to ±3 semitones, step 0.25, default ±1, active for the two layer/variant modes; pitch drawn uniform from a continuous range, then shown to one decimal.
- "Sounds the same within": slider 0 to 1 semitone, step 0.05, default 0. Pitches are grouped into bins of this width (bin index `floor(s / width)`); 0 means exact comparison.
- Rate: slider 2 to 15 shots per second, default 8.75.
- Buttons: "Fire burst" (key F), "Simulate 1,000 bursts" (key S).

**Readouts (live text next to the stats view).** Number of outcomes `n`, repeat chance `R` as a percentage to 1 decimal, expected repeats per burst `9R` to 2 decimals, `P(at least one repeat) = 1 − (1 − R)^9` as a percentage, files in memory. For continuous pitch with grouping width `w` and range `±P`, count pitch groups as `ceil(2P / w)` and treat them as uniform; with `w = 0`, show "pitch: continuous, exact repeats ≈ 0" and use only the file part for `R`.

**Formulas.**
- `R = Σ p_i²`; independent parts multiply; with the no-repeat toggle a pool contributes `R = 0` to immediate repeats.
- Files in memory: "Same sample" and Doom/Heretic modes 1; "12 whole variants" 12; "3 layers × 4" 12.

**Test values.**
- Same sample × 10: n = 1, R = 100.0%, expected 9.00, P = 100%.
- Doom pitch, grouping 0: n = 32, R = 3.1%, expected 0.28, P = 24.9%.
- Heretic pitch, grouping 0: n = 15, R = 8.4%, expected 0.76, P = 54.6%.
- 12 whole variants, pitch ±0, no repeat off: R = 8.3%, expected 0.75, P = 54.3%.
- 3 layers × 4, pitch ±0, no repeat off: n = 64, R = 1.6%, expected 0.14, P = 13.2%.
- Either variant mode with no repeat on: R = 0.0%, expected 0.00.
- Doom pitch with grouping 0.5 semitone: the 32 pitch values span about −1.92 to +2.31 semitones and fall into 9 groups; R rises to roughly 11% (exact value depends on bin edges; compute it from the actual group counts, and show it).
- Simulating 1,000 bursts in "3 layers × 4" (no pitch) gives a measured average within about 0.03 of 0.14.

**Accessibility.** All controls reachable by keyboard with visible focus. A text summary under the burst strip updates after each burst ("10 shots, 0 exact repeats, 2 within 0.5 semitone"). No sound plays until the user presses a button; a visible volume slider (default 70%) and a mute toggle. Respect `prefers-color-scheme` and `prefers-reduced-motion`. No game art or logos; tiles and bars are plain shapes.
