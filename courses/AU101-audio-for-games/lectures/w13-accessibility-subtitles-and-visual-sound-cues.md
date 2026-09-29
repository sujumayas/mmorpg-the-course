# AU101 · Week 13 — Accessibility: Subtitles and Visual Sound Cues

**Why this matters:** Some of your players cannot hear your game, and many more play with the sound low or off. Everything you built this term, from footsteps to music stingers, reaches them only if you turn it into something they can see or feel. A subtitle that vanishes before it can be read, or a footstep with no visual cue, is information you designed and then withheld.

**You will be able to:**
- Compute the reading rate a voice line forces on a subtitle, and the hold time needed to bring it under a reading limit.
- Decide for each line whether to hold, stack, condense or pace it, using the gap to the next line.
- Compute the direction marker or radial-indicator wedge for an off-screen sound from its position and the player's facing.
- Critique a game's captions and visual sound cues with the information test and the fairness test.

**Before class:** Xbox Accessibility Guideline 104, "Subtitles and captions" (Microsoft Learn, about 20 minutes). Netflix, "English (USA) Timed Text Style Guide", the sections on character limits and reading speed (10 minutes). Collins, *Game Sound*, chapter 1 again, the part on sound as information.

**Prerequisites from earlier courses:** [AU101 week 1, what sound does in games](w01-what-sound-does-feedback-space-emotion.md) (the three jobs of a sound and the cone of confusion; this lecture reuses both). [MA101 week 11, atan2 and turning toward a target](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w11-atan2-turning-toward-a-target.md) (the angle to a point and wrapping into (−180°, 180°]). [AU101 week 7, spatial audio](w07-spatial-audio-and-attenuation.md) and [week 10, mixing and priority](w10-mixing-ducking-and-priority.md) supply the direction and priority data this lecture reuses.

**Interactive:** [examples/w13-subtitle-reading-race.html](../examples/w13-subtitle-reading-race.html). Keep it open during section 2. Sound is optional; everything it shows is also drawn.

---

## 1. Who hears your game, and who doesn't

In week 1 you ran a mute test. You played with the sound off and wrote down the first moment you felt lost. For some players that is not a test. It is every session.

Three groups need what this lecture builds.

- **Players who are deaf or hard of hearing.** Some hear nothing. Many hear some frequencies and not others, or can't separate speech from a loud mix. Week 10's ducking helps the second group. Nothing in the mix helps the first.
- **Players in a situation that removes sound.** A baby asleep in the next room, a shared flat, a train, a stream with music over the top. Microsoft's guideline for subtitles lists players in noisy places and players avoiding disturbing others alongside deaf players.
- **Players who hear fine but read or process speech slowly.** Second-language speakers, younger players, players with dyslexia or a cognitive disability. They use subtitles even with sound on, and they are the ones a fast subtitle loses.

Two terms before we go on. **Subtitles** are text for speech. **Captions** are text for all important audio: speech, sound effects, music cues, and where a sound comes from. Microsoft's XAG 104 uses exactly this split, and so will we. A **visual sound cue** is any non-text picture of a sound, such as an arrow, a ring around the crosshair or a pulse on the minimap. A **haptic cue** is the same information sent through controller vibration.

You will meet the reading side of subtitles again in [UX201 week 11, accessibility guidelines](../../UX201-game-ux-and-player-psychology/lectures/w11-accessibility-guidelines.md), which covers contrast, text size and backplate opacity. This week stays with the audio side. When does a line of speech become text, how long does that text stay up, and which sounds deserve a picture?

## 2. Worked example: the subtitle that vanishes first

### The hook

You have seen this. A firefight, two characters shouting, and a subtitle flashes up and disappears while you are halfway through it. You didn't miss it because you read slowly. You missed it because the game showed the text for exactly as long as the actor took to say it, and the actor spoke faster than anyone reads.

Television solved this decades ago by editing subtitles. Netflix's English style guide caps reading speed at 20 characters per second for adult programmes and 17 for children's, with at most 42 characters per line and two lines per subtitle. Game subtitles often skip that step. The text is the recording script, word for word, and the timing is the audio file's length. Minecraft Java Edition shows the other side of the problem. Its 1.19.4 update (2023) added a Notification Time multiplier to the accessibility settings, and it changes how long closed captions stay on screen. That setting exists because one fixed display time was wrong for some players.

So: how long does a subtitle need to stay up, and what do you do when the voice doesn't give it that long?

### The model

Four quantities describe one line of dialogue.

- `n` is the number of characters in the subtitle. Count every character the player's eye has to cross, including spaces and punctuation. This is the convention we use in this course and in the lab.
- `L` is the length of the voice clip, in seconds.
- `g` is the **gap**, the time from the end of this clip to the start of the next line.
- `R` is the **reading limit** in characters per second (CPS): the fastest rate you will ask a player to read. You choose it. Netflix's 17 and 20 are good reference points.

Add one policy number, `d_min`, the shortest time any subtitle stays up. A one-word line shown for a fifth of a second is a flicker, not text. This course uses `d_min = 1.0 s`.

The line needs to be on screen for

```
d = max(d_min, n / R)
```

If the subtitle disappears when the voice ends (we will call that **voice-locked**), it is up for `L` seconds and forces a reading rate of `n / L`. A reader who reads at exactly `R` has reached character `R × L` when it vanishes, so the fraction they never saw is

```
unread = max(0, 1 − R × L / n)
```

The fix is to **hold** the subtitle after the voice stops:

```
hold  h = max(0, d − L)
fits  if h ≤ g
```

If the hold is longer than the gap, the next line arrives while this one still needs time. Then you have four choices, and section 2 ends with them. One of them is to cut the text. The longest text that fits the time available is

```
n_max = floor(R × (L + g))
```

That is the whole model: one rate, one hold, one clash test.

### Numbers you can check

Here is a 17-second exchange from an invented stealth game. Three voices: Mara, Tomas and a radio. The clip lengths are what a voice actor might deliver under pressure.

First, the voice-locked version, where each subtitle lives exactly as long as its clip.

| # | Speaker | Line | n | L (s) | Forced rate n/L | Unread at R = 17 | Unread at R = 20 |
|---|---|---|---|---|---|---|---|
| 1 | Mara | Keep your head down. | 20 | 1.2 | 16.7 | 0% | 0% |
| 2 | Mara | Grenade! | 8 | 0.5 | 16.0 | 0% | 0% |
| 3 | Tomas | The bridge is out. We cross at the mill instead. | 48 | 2.2 | 21.8 | 22% | 8% |
| 4 | Mara | Cover me while I get this door open, and watch the roof! | 56 | 2.3 | 24.3 | 30% | 18% |
| 5 | Tomas | Go. | 3 | 0.3 | 10.0 | 0% | 0% |
| 6 | Radio | All units, the convoy leaves at dawn. Anyone not on it stays behind. | 68 | 3.6 | 18.9 | 10% | 0% |

Check line 4 by hand. At 17 CPS a reader gets through `17 × 2.3 = 39.1` characters in 2.3 seconds. The line has 56. They lose the last 17 characters, "d watch the roof!", so the whole warning "watch the roof!" goes unread, and that is the part that tells them where the danger is. Line 2 looks fine on rate, but 0.5 seconds is half of `d_min`. It will read as a flash.

Now the hold policy at `R = 17`, `d_min = 1.0`, with the gap to the next line:

| # | n | L (s) | Gap g (s) | Needed d (s) | Hold h (s) | h ≤ g? | n_max |
|---|---|---|---|---|---|---|---|
| 1 | 20 | 1.2 | 1.5 | 1.18 | 0.00 | yes | 45 |
| 2 | 8 | 0.5 | 0.3 | 1.00 | 0.50 | **no** | 13 |
| 3 | 48 | 2.2 | 0.4 | 2.82 | 0.62 | **no** | 44 |
| 4 | 56 | 2.3 | 2.0 | 3.29 | 0.99 | yes | 73 |
| 5 | 3 | 0.3 | 3.0 | 1.00 | 0.70 | yes | 56 |
| 6 | 68 | 3.6 | 0.5 | 4.00 | 0.40 | yes | 69 |

Holding fixes lines 4, 5 and 6. Line 4, the worst offender, only needed one more second, and it had two seconds of silence after it. Two lines still clash, for different reasons.

- **Line 2 clashes because of `d_min`, not reading rate.** Eight characters take under half a second to read. The problem is the minimum display time. Cutting text can't help. `n_max = 13` is already more than 8.
- **Line 3 clashes on reading rate.** It needs 0.62 seconds of hold and has 0.4. Its `n_max` is 44, four characters short. "The bridge is out. We cross at the mill." has 40 characters, needs 2.35 seconds, holds 0.15 and fits.

This short program reproduces the second table. Change `R` to 20 and line 3 fits without edits.

```python
import math

R, D_MIN = 17, 1.0          # reading limit (CPS) and minimum display time (s)
script = [  # (text, voice length L, gap g to the next line), seconds
    ("Keep your head down.", 1.2, 1.5),
    ("Grenade!", 0.5, 0.3),
    ("The bridge is out. We cross at the mill instead.", 2.2, 0.4),
    ("Cover me while I get this door open, and watch the roof!", 2.3, 2.0),
    ("Go.", 0.3, 3.0),
    ("All units, the convoy leaves at dawn. Anyone not on it stays behind.", 3.6, 0.5),
]
for i, (text, L, g) in enumerate(script, 1):
    n = len(text)
    need = max(D_MIN, n / R)
    hold = max(0.0, need - L)
    fits = hold <= g + 1e-9
    n_max = math.floor(R * (L + g) + 1e-9)
    print(f"{i}  n={n:2d}  cps={n / L:4.1f}  need={need:4.2f}  hold={hold:4.2f}  "
          f"{'fits' if fits else 'CLASH'}  n_max={n_max}")
```

It prints:

```
1  n=20  cps=16.7  need=1.18  hold=0.00  fits  n_max=45
2  n= 8  cps=16.0  need=1.00  hold=0.50  CLASH  n_max=13
3  n=48  cps=21.8  need=2.82  hold=0.62  CLASH  n_max=44
4  n=56  cps=24.3  need=3.29  hold=0.99  fits  n_max=73
5  n= 3  cps=10.0  need=1.00  hold=0.70  fits  n_max=56
6  n=68  cps=18.9  need=4.00  hold=0.40  fits  n_max=69
```

### A visual you can move

Open [`examples/w13-subtitle-reading-race.html`](../examples/w13-subtitle-reading-race.html). The top view is the timeline. Voice clips are grey bars and subtitle events sit under them, with any hold drawn as a lighter extension. When a hold runs into the next line, the overlap turns red.

The bottom view is the reader. Press play and the exchange runs with a procedurally generated babble for each voice, a burst of short tones per syllable, so there is no recorded speech. Under the subtitle text, a highlight moves at `R` characters per second. That highlight is the reader. When a subtitle disappears, whatever the highlight had not reached drops into a "missed" list.

Start on the voice-locked policy at 17 CPS and watch line 4 leave with "and watch the roof!" still unread. Switch to the hold policy. Line 4 now stays up for its full 3.29 seconds and the highlight finishes it. Line 3 still turns red. Tick "condense line 3" and it clears. Then drag `R` to 12 and watch the red spread. A slower reader is not an edge case. It is a larger part of your audience than you think.

### Cross-game recognition

The same three numbers, `n`, `d` and `R`, sit under every subtitle and caption system you will meet. Each one below chooses a different number to control.

**Netflix (English timed text guide, current).** Controls `R` and `n` directly. 20 CPS for adults, 17 for children, 42 characters per line, two lines. The subtitler edits the text until `n / d ≤ R`, where `d` is set by the shot and the speech. That is our condense branch applied to every line, done by a person.

**Minecraft Java Edition (1.19.4 and later).** Controls `d` from the player's side. The Notification Time option is a multiplier, 1.0x by default, and it scales how long captions stay up. In our terms the player picks a longer `d` for themselves, which is the same as letting them lower `R`. It costs the designer nothing, because Minecraft's captions are a stacked list in the corner, not a single line that the next one must replace.

**The Outer Worlds (Obsidian, 2019).** Controls pace. Its "Minimal" conversation subtitle setting, which XAG 104 describes, shows only the NPC's last line while the player's dialogue choices are on screen. That text stays until the player picks a reply. `d` has no upper limit, so any `n` fits. This is the **player-paced** branch, and it works whenever the game can wait.

**Xbox Accessibility Guideline 104 (page dated May 2022).** Controls layout. It asks for lines of no more than 40 characters and no more than two lines on screen, and says long lines are harder to read when dialogue is fast. That is a limit on `n` per row that sits beside the limit on `n / d`.

Four products, four knobs, one inequality: `n / d ≤ R`.

### Eyes-open design judgment

When a line clashes, you have four fixes. Each has a cost.

- **Hold.** Free when the gap exists. It fails in exactly the scenes that need it most, fast back-and-forth dialogue, because those have no gaps.
- **Stack.** Show the old line as the top row and the new one below, each with its speaker's name. Line 2, "Grenade!", should stack, since it fails on `d_min` and no edit helps. Stacking uses up the two-row limit, so you can't stack onto a line that already needs two rows.
- **Condense.** Edit the subtitle so it says less than the voice. The Game Accessibility Guidelines include this as its own item: subtitles cut down to a words-per-minute rate suited to the audience. It works every time. It also means the text and the audio disagree, which annoys hearing players who read along. It also has to be redone for every language, because a German line is often longer than the English one it translates. Budget for it in localization, not in the last week.
- **Pace.** Wait for the player. This is correct for conversations and menus and impossible for a firefight.

Decide the reading limit before recording, not after. If your writers know that combat barks will be shown at 17 CPS, they write "Cover me. Watch the roof!" instead of the 56-character version. It is cheaper to change a script than to re-edit 4,000 subtitle files.

Put subtitles on by default, or ask about them before the first line of speech plays. XAG 104 points to Gears 5, which starts its first launch with subtitles and captions on and then shows its accessibility menu. The Game Accessibility Guidelines say the same.

And test with real readers. The model gives you a floor, not a guarantee. A 17 CPS line in a 12-point font on a television across the room is still unreadable.

## 3. Visual sound cues: giving sounds a direction

### Which sounds get a caption?

Not every sound needs one. Captioning every footstep, leaf and gun click fills the screen with noise, and the important caption gets lost in it. Use the **information test**, which follows XAG 104. A sound gets a caption or a visual cue if it carries information the player needs *and* that information is not already on screen.

Run it on three sounds.

- A treasure chest opening in front of the player. The player can see it open. No caption.
- A door opening behind the player in a stealth level. The player needs to know, and nothing on screen shows it. Caption it, with a direction.
- The music shifting to combat intensity (week 8's vertical layering). This one is easy to miss. The music is telling a hearing player that an enemy has noticed them. Gears 5 captions it, and XAG 104 uses it as an example. Music that carries game state is information. Caption it.

Week 1 gave every sound three possible jobs: feedback, space and emotion. The information test catches mostly the first two. Emotion is harder. A caption such as "[tense music]" helps with it, and a haptic pulse can too, but you should decide it on purpose rather than skip it.

### The model: bearing, marker, wedge

A caption for an off-screen sound needs a direction. Put the player at the origin with `+y` as map north and `+x` as east. Use **compass headings** for angles: 0° is north, 90° is east, and angles grow clockwise. The player faces heading `φ`. A sound source sits at offset `(dx, dy)` from the player.

```
bearing   b   = atan2(dx, dy)            (compass heading of the source)
relative  rel = wrap(b − φ)              (in (−180°, 180°], positive = to the right)
```

Notice the arguments. MA101 week 11 wrote `atan2(dy, dx)` for angles measured counterclockwise from east. Swapping the arguments gives the same direction measured clockwise from north. Pick one convention per project and write it down.

Two ways to show `rel` are common.

**Direction markers** follow Minecraft Java Edition's closed captions: `<` if the sound is off screen to the left, `>` if to the right, nothing if it is on screen. With a horizontal field of view `F`, the sound is on screen when `|rel| ≤ F / 2`. We add a fourth marker, `v`, for sounds behind the player, `|rel| ≥ 135°`. Week 1 showed why. Stereo panning can't tell front from back (the cone of confusion), so a sound straight behind the player is the one a hearing player is most likely to misplace too.

**Radial indicators** follow Fortnite's sound visualizer, a ring of wedges around the crosshair. With `k` wedges and wedge 0 straight ahead:

```
wedge = round(rel / (360° / k)) mod k
```

### Numbers you can check

The player stands at the origin with a 90° field of view. Four sources:

| Source | Offset (dx, dy) | Bearing b | Facing north: rel | Marker | Wedge (k=8) | Facing east: rel | Marker | Wedge |
|---|---|---|---|---|---|---|---|---|
| Wolf | (3, 4) | 36.87° | 36.87° | none | 1 | −53.13° | `<` | 7 |
| Footsteps | (−5, 1) | −78.69° | −78.69° | `<` | 6 | −168.69° | `v` | 4 |
| Door | (4, −5) | 141.34° | 141.34° | `v` | 3 | 51.34° | `>` | 1 |
| Chest | (6, 2) | 71.57° | 71.57° | `>` | 2 | −18.43° | none | 0 |

Check the wolf when facing east: `36.87 − 90 = −53.13`. That is past the 45° edge of the screen on the left, so the marker is `<`. For the wedge, `−53.13 / 45 = −1.18`, which rounds to −1, and `−1 mod 8 = 7`, the front-left wedge. Check the footsteps facing east: `−78.69 − 90 = −168.69`, well past 135°, so `v`.

### Cross-game recognition

**Minecraft Java Edition.** Captions (called subtitles until 1.21.9) arrived in 1.9, in development snapshot 15w43b in 2015. Each nearby sound gets a line in a box at the bottom right, with `<` or `>` when its source is off screen, and the text fades as the sound fades. That is our marker model with no `v`, plus a fade that carries loudness.

**Fortnite (Epic Games, update v5.00, July 2018).** The sound visualizer, built first for the mobile version, became available on all platforms. On PC and console, turning it on also muted sound effects. Epic's patch notes gave no reason, but the effect is clear. A player could not have both the visualizer and full audio, so the visualizer could not be used as a way to get more information than the audio gave. The current settings list it as "Visualize Sound Effects", described as a radial indicator for some sounds.

**The Last of Us Part II (Naughty Dog, 2020).** Can I Play That's deaf accessibility review describes visual markers for enemy positions in stealth and combat, a directional indicator when the player is about to be spotted, markers that show where incoming fire comes from, and controller vibration near dangerous ledges. The game won Innovation in Accessibility at The Game Awards 2020. Each of those features is a bearing turned into a picture or a vibration.

**Far Cry New Dawn (Ubisoft, 2019).** XAG 104 shows it captioning an explosion with an arrow toward its source. Same bearing, drawn in the world.

### Design judgment: the fairness test

A visual cue can show more than the audio does. A ring that marks every footstep within 40 metres with a crisp wedge is more precise than the blurry direction most players get from stereo headphones. In a competitive game that turns an accessibility option into something every serious player switches on. Epic's 2018 choice to mute effects while the visualizer was on is one answer, and it has a cost. Players with partial hearing who want both lose one.

Two other answers are worth knowing. You can **match the precision**: show only the wedge, with no distance, and only for sounds a hearing player could pick out. Or you can **match the priority**: use the same voice-priority rules as week 10, so the visual shows the few sounds that won the mix, not every sound playing. Both keep the cue honest.

Whatever you pick, apply the **fairness test**. With the cue on and sound off, does a player learn about as much as a player with sound on and no cue? Not much less, and not much more.

## 4. Building it: what the audio system has to know

None of this works if the audio system can't answer questions. At minimum, every sound event needs three pieces of data your week 6 middleware setup can carry.

- **A caption key.** A short, lowercase description in brackets, following Netflix's style for sound labels. "[door opens]", "[footsteps approach]". Localized like any other string. Most sounds have none. Leave the key blank on purpose, so an empty key means "we decided" rather than "we forgot."
- **A category** the player can switch on or off separately: dialogue, background chatter, gameplay sounds, music. XAG 104 asks for independent toggles, and The Outer Worlds splits conversation, bark and cinematic subtitles.
- **A position and a priority**, which you already have from weeks 7 and 10.

Subtitles need their own data. For each line, store the text, the speaker, the clip length and the reading rate it was checked at. Run the section 2 check in your build pipeline, as the lab does. Then a writer who adds a 90-character bark at the last minute gets a failed build, not a bug report after launch.

A note on speaker names. XAG 104 asks for the speaker's name each time the speaker changes. Names count toward `n`. "Tomas: Go." is 10 characters, not 3. At `d_min = 1.0` that makes no difference, but a stack of named barks can overflow two rows fast.

## In-class activity (25 minutes)

Groups of three. You need a laptop with the interactive and a 60-second clip of combat or tense dialogue from any shipped game with its sound on. Record it yourself or pick a public video, but do not share or redistribute it.

1. **Transcribe (8 min).** Write every spoken line with its start time and clip length, to 0.1 s. Use the video's timestamps.
2. **Time it (7 min).** Compute `n`, forced rate `n/L`, hold and clash at `R = 17` for each line. Mark the three worst lines.
3. **Audit the sounds (5 min).** List every non-speech sound you hear. Apply the information test. For the ones that pass, write a caption key and a marker (`<`, `>`, `v` or none) for the moment it plays.
4. **Compare (5 min).** Turn the game's subtitles on (from the video, or from memory if you own it). Did it hold, stack, condense or pace the three worst lines? Did it caption the sounds you picked?

Expected output: one table of lines with rates and verdicts, one list of captioned sounds with markers, and two sentences on what the shipped game did differently.

## Common misconceptions

- **"Subtitles just need to match the audio."** Matching the audio word for word, and in time, is what makes them unreadable in fast scenes. A subtitle needs `d ≥ n / R`, and the voice doesn't guarantee that.
- **"Splitting a long line into two subtitles fixes the speed."** It fixes the row limit, not the reading rate. Two halves of a 56-character line shown across the same 2.3 seconds still ask for 24 characters per second.
- **"Caption everything to be safe."** A screen full of captions buries the one that matters. Caption what passes the information test.
- **"Visual cues are only for deaf players."** They are also for players in loud rooms, players with the sound off, and players who can't place sounds front to back. That is why their fairness has to be designed.

## Check yourself

1. A bark "Flank left, flank left, they're coming round the tower!" (55 characters) has a 2.0 s clip and a 0.6 s gap to the next line. At `R = 17` and `d_min = 1.0`, what hold does it need, and does it fit? What is `n_max`?
2. The same bark shown voice-locked. What fraction does a 17 CPS reader miss? Which words are they?
3. A team says "our subtitles are fine, the average forced rate across the script is 15 CPS." Why is the average the wrong number? What would you compute instead?
4. The player faces heading 200°. A sound is at offset (−2, −2). What are its bearing, relative angle and marker with a 90° field of view? Which of 8 wedges lights up?
5. You are designing a PvP shooter. A tester says the radial indicator gives her a better idea where footsteps are than her headphones do. Name two changes that would bring the cue in line with the fairness test.

<details>
<summary>Answers</summary>

1. `d = max(1.0, 55/17) = 3.24 s`. Hold `= 3.24 − 2.0 = 1.24 s`, more than the 0.6 s gap, so it clashes. `n_max = floor(17 × 2.6) = 44`. You need to cut 11 characters, for example "Flank left! They're coming round the tower!" (43).
2. `1 − 17 × 2.0 / 55 = 1 − 34/55 = 0.38`, so 38%. The reader reaches character 34 and misses the last 21 characters, most of "coming round the tower!". The location, the useful part, is what gets lost.
3. The average hides the outliers, and the player only fails on the outliers. A script of mostly slow lines with a few 25 CPS barks has a fine average. Compute the rate or clash for every line and report the worst ones, or the count of lines over `R`.
4. Bearing `atan2(−2, −2) = −135°`. Relative `wrap(−135 − 200) = wrap(−335) = 25°`. That is inside ±45°, so it is on screen and gets no marker. Wedge `round(25/45) = round(0.56) = 1`.
5. Any two of these. Show direction only as a wedge, with no distance, and make the wedges wide. Only show sounds that won the week 10 priority mix, not every sound in range. Add the same delay and fade a hearing player gets from a distant sound. Or follow Fortnite's 2018 choice and mute effects while the visualizer is on, and state what that costs players with partial hearing.

</details>

## Lab / assignment hook

[Lab 13, subtitle timing and directional cues](../labs/lab13.md). You write the reading-rate checker and the direction-marker function from this lecture in Python, run them on a 12-line script, fix every clashing line with a named strategy, and write a caption plan for the sounds in your own final-project slice. The checker is the kind of build step you will use in the week 15 sound pass.

## Sources

- Microsoft Learn, Xbox Accessibility Guideline 104, "Subtitles and captions" (page dated 9 May 2022, accessed September 2026). Subtitles versus captions; speaker names on speaker change; lines of no more than 40 characters and no more than two lines; long lines harder to read when dialogue is fast; independent toggles; examples from Gears 5 (subtitles on at first launch, a caption for music intensifying), Minecraft Java Edition (directional arrows on captions), Far Cry New Dawn (explosion caption with an arrow), The Outer Worlds (conversation, bark and cinematic subtitle settings with a Minimal mode), Forza Horizon 4 and 5.
- Netflix Partner Help Center, "English (USA) Timed Text Style Guide" (accessed September 2026). 42 characters per line, two lines, reading speed up to 20 characters per second for adult programmes and 17 for children's, bracketed lowercase sound-effect labels used only when not visually identifiable.
- Minecraft Wiki, "Closed captions" (accessed September 2026). Subtitles added in Java Edition 1.9 (snapshot 15w43b, 2015); `<` and `>` for off-screen sounds; fading with the sound; Notification Display Time option in 1.19.4 changes how long they are displayed; renamed to Closed Captions in 1.21.9; Bedrock Edition captions from 26.x.
- Minecraft Wiki, "Options" (accessed September 2026). Notification Time accessibility option, default 1.0x, added in 1.19.4 (23w03a, renamed in 23w06a).
- Fortnite Wiki, "Update v5.00" (released 12 July 2018). The mobile sound visualizer made available on all platforms, with audible sound effects muted while it is on, except on mobile. Fortnite Wiki, "Settings" (current, v33-era menus): "Visualize Sound Effects" as a radial indicator for some sounds.
- Moscoso, C. (18 June 2020), "The Last of Us Part II accessibility review", *Can I Play That?* Visual enemy markers, spotted-direction indicator, incoming-fire markers, haptic ledge warnings, subtitle speaker colours and background opacity.
- Wikipedia, "The Last of Us Part II". Winner of Innovation in Accessibility at The Game Awards 2020.
- Game Accessibility Guidelines (gameaccessibilityguidelines.com), "Ensure that subtitles/captions are cut down to and presented at an appropriate words-per-minute for the target age group" and "Provide captions or visuals for significant background sounds" (accessed September 2026).
- Collins, K. (2008). *Game Sound*. MIT Press. Chapter 1.

## Interactive spec: examples/w13-subtitle-reading-race.html

**Purpose.** Show that a subtitle timed to its voice clip can leave the reader behind, and that the hold time `h = max(0, max(d_min, n/R) − L)` fixes most lines but clashes with the next line when the gap is short.

**The one insight the visual must make obvious.** On first load (voice-locked, R = 17) line 4's reading highlight is frozen at character 39 of 56 when the subtitle disappears, with "and watch the roof!" shown in the missed list (the list starts at the beginning of the word the reader was in, since half a word is not read; the unread percentage still counts characters). Switching to "Hold" makes the same line stay 0.99 s longer and finish, while line 3's timeline bar shows a red overlap of 0.22 s.

**Layout.** Two linked views stacked on phones (390px), side by side at 1024px and wider.

- **Top, "Timeline".** Horizontal axis 0 to 18 s with ticks every second. Row 1: voice clips as grey bars labelled with the speaker's initial. Row 2: subtitle events as accent-coloured bars from start to start + max(L, displayed time). The hold part is drawn lighter. Where an event overlaps the next event's start, the overlapping part is red with a hatch pattern and a label "clash 0.22 s". A playhead line moves during playback. Tapping a bar selects that line in the table.
- **Bottom, "Reader".** A generic dark scene rectangle (flat gradient, no art) with a subtitle box at the bottom: speaker name in bold, then the text, wrapped at 42 characters. A highlight (underline plus background tint) advances through the text at R characters per second of playback time, starting when the subtitle appears. When the subtitle disappears, the characters the highlight had not reached are appended to a "Missed" list below the scene as `#4 Mara: "and watch the roof!"`. In stack mode, show up to two events as two rows, older on top.
- **Table under both views.** One row per line: #, speaker, n, L, forced rate n/L, needed d, hold h, gap g, verdict (fits / clash), unread % under the current policy. The selected row is highlighted. Values must match the lecture's tables exactly at the default settings.

**Data (fixed).** Start times and clip lengths in seconds:

| # | Speaker | Text | start | L |
|---|---|---|---|---|
| 1 | Mara | Keep your head down. | 0.0 | 1.2 |
| 2 | Mara | Grenade! | 2.7 | 0.5 |
| 3 | Tomas | The bridge is out. We cross at the mill instead. | 3.5 | 2.2 |
| 4 | Mara | Cover me while I get this door open, and watch the roof! | 6.1 | 2.3 |
| 5 | Tomas | Go. | 10.4 | 0.3 |
| 6 | Radio | All units, the convoy leaves at dawn. Anyone not on it stays behind. | 13.7 | 3.6 |

Gap g = next start − (start + L). Line 6's gap is 0.5 (the scene ends at 17.8 s).

**Controls.**
- Reading limit R: slider 8 to 25 CPS, step 1, default 17. Keyboard arrows move it.
- Policy: radio group "Voice-locked" (display time = L), "Hold" (display time = max(d_min, n/R), cut off when the next line starts), "Hold + stack" (as Hold, but a line that clashes stays on as the top row while the next appears below, up to two rows total). Default Voice-locked.
- d_min: slider 0.5 to 2.0 s, step 0.1, default 1.0.
- Checkbox "Condense line 3": replaces its text with "The bridge is out. We cross at the mill." (40 characters).
- Play / Pause, Restart, and speed 0.5x / 1x. Space toggles play.
- Sound on/off toggle, default on, starting the AudioContext only on the first user gesture.

**Formulas.** n = text length including spaces and punctuation. need = max(d_min, n / R). hold = max(0, need − L). clash if hold > g + 1e-9, clash amount = hold − g. unread (voice-locked) = max(0, 1 − R·L/n). Under Hold, the displayed time is min(need, L + g), and unread = max(0, 1 − R·min(need, L+g)/n). Under Hold + stack the displayed time is need.

**Procedural voice (Web Audio).** No recorded audio. For each line, estimate syllables as the count of vowel groups (`/[aeiouy]+/gi`), minimum 1. Spread that many syllable blips evenly across L. Each blip: a sawtooth oscillator at the speaker's pitch (Mara 220 Hz, Tomas 140 Hz, Radio 180 Hz) with ±3% random pitch per blip, through a bandpass filter whose centre is picked at random from 500, 700, 900 or 1200 Hz (Q = 4), with a gain envelope of 10 ms attack, 40 ms hold, 50 ms release, peak gain 0.15. Radio adds a highpass at 400 Hz and a lowpass at 3,000 Hz. Respect a master mute. Under prefers-reduced-motion, the highlight still advances but the playhead jumps in 0.5 s steps instead of animating.

**Test values (defaults R = 17, d_min = 1.0).**
- Voice-locked: unread % for lines 1 to 6 = 0, 0, 22, 30, 0, 10. Line 4's highlight stops at character 39.
- Hold: holds = 0.00, 0.50, 0.62, 0.99, 0.70, 0.40. Clashes on lines 2 (0.20 s) and 3 (0.22 s). Unread under Hold: line 3 = 1 − 17 × 2.6 / 48 = 8%; line 2 = 0.
- Condense line 3 on: n = 40, need 2.35, hold 0.15, fits.
- R = 20, Hold: line 3 hold 0.20, fits; line 2 still clashes by 0.20 s.
- R = 12, Voice-locked: line 4 unread = 1 − 27.6/56 = 51%.

**Accessibility of the example itself.** All controls are native inputs with labels. The missed list is an `aria-live="polite"` region. Colour is never the only signal: clashes use hatch plus a text label.
