# AR101 · Week 08 — Sprite Animation: Frames and Timing

**Why this matters:** Two attacks can use the same six drawings and feel completely different, one a quick jab and the other a crushing blow. The difference is how long each drawing stays on screen. Beginners spend their time adding drawings. Experienced animators spend it moving time between the drawings they already have, which is faster and matters more. This week you learn to plan animation as a list of holds you can compute, read and hand to a programmer.

**You will be able to:**
- Compute an animation's length, its phase lengths and the drawing on screen at any tick from a list of holds.
- Convert holds between game ticks, milliseconds and engine settings (Aseprite durations, Godot frame durations).
- Design two timings for the same drawings that read as light and heavy, and justify each hold.
- Compute the cycle length of a walk from stride and speed so the feet don't slide.

**Before class:** Richard Williams, *The Animator's Survival Kit* (expanded edition, 2009), the material on timing and spacing (find it through the table of contents). Frank Thomas and Ollie Johnston, *The Illusion of Life* (1981), the chapter on the principles of animation, reading only "Anticipation", "Follow Through and Overlapping Action" and "Timing".

**Prerequisites from earlier courses:** AR101 has no prerequisite courses. From this course, [week 3 on silhouettes](w03-silhouette-readability.md) and [week 6 on pixel art](w06-pixel-art-fundamentals.md). Each drawing in an animation must read as a silhouette on its own. If you take them in parallel, [CS101 week 9, delta time](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) explains ticks and frame-rate independence, and [MA101 week 9, easing curves](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w09-easing-curves-for-animation-feel.md) is the maths of spacing. [GD101 week 12, feedback](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) turns the windup you draw this week into a reaction-time budget.

**Interactive:** [`examples/w08-timing-chart.html`](../examples/w08-timing-chart.html). Keep it open during section 2.

---

## 1. Drawings, frames and holds

Three words get mixed up in every animation conversation. Keep them apart.

- A **drawing** (animators also say a pose, or a cel) is one image of the character. A six-drawing attack has six images in the sprite sheet.
- A **frame** in the game sense is one update of the screen. Most games update 60 times per second, so one frame lasts 1/60 of a second, about 16.7 milliseconds. To avoid confusion with drawings, this lecture calls a game frame a **tick**.
- A **hold** is how many ticks a drawing stays on screen before the next one replaces it.

An animation, then, is a list of drawings and a list of holds. Nothing else. A sprite sheet with six drawings and the holds `[3, 3, 3, 3, 3, 3]` plays each drawing for 3 ticks, or 50 ms, and lasts 18 ticks, 0.3 seconds.

The number of drawings per second is not the game's frame rate. A game running at 60 ticks per second can show a sprite at 60 drawings per second (every drawing held 1 tick), 30 (held 2), 20 (held 3), 10 (held 6) or any uneven mix. Film animators have long had words for this. Film runs at 24 frames per second. A drawing held for one film frame is animated **on ones**, held for two is **on twos**, 12 drawings per second. In hand-drawn work, moving characters are often shot on twos, and animators switch to ones for quick movements that twos are too slow to convey. Pixel artists use the same idea with different numbers, and they very rarely animate on ones, because every drawing costs time to draw and clean up.

### Timing and spacing

Animation teachers, Williams among them, split the craft into two questions, and so will we.

**Timing** is how long each drawing is held. It is a list of numbers, the holds.

**Spacing** is how far things move between one drawing and the next. A sword that travels 2 pixels, then 6, then 14 between drawings accelerates. One that travels 14, 6, 2 slows down. Spacing is the drawing version of an easing curve, and MA101 week 9 gives you the functions behind it.

The two interact. You can make a motion faster by holding drawings for less time, or by spacing them farther apart. A swing drawn with wide spacing and held for 1 tick per drawing reads as a blur. The same spacing held for 6 ticks per drawing reads as a slideshow. This week focuses on timing, because it is the half you can change without redrawing anything.

## 2. Worked example: same drawings, different weight

### The hook

In Guilty Gear Strive (Arc System Works, 2021), the character Sol Badguy has a standing punch and a standing heavy slash. The fan-maintained frame data on the Dustloop Wiki, read in September 2026, lists the punch at 5 frames of startup, 5 active frames and 9 frames of recovery. It lists the heavy slash at 11, 4 and 20. Dustloop counts startup up to and including the first frame that can hit. So the punch spends 4 ticks winding up, 5 able to hit and 9 recovering, 18 in all. The heavy slash spends 10, 4 and 20, 34 in all. Fighting games, as Dustloop's glossary notes, generally run at 60 frames per second, so these are ticks in our sense.

Look where the extra 16 ticks went. Almost none went into the part that hits. The heavy attack has fewer active ticks than the light one. The weight lives in the windup and the recovery. Players read "heavy" from how long the character gathers itself and how long it takes to come back. Those are animation holds, drawn by an artist.

### The model

Give the drawings indexes `i = 1 … n` and the holds `h_i`, each a whole number of ticks.

```
start_i  = h_1 + h_2 + … + h_(i−1)          (start_1 = 0)
T        = h_1 + h_2 + … + h_n              total length in ticks
seconds  = T / R                            R = tick rate, usually 60
drawing at tick t = the i with start_i ≤ t < start_i + h_i
```

- `h_i` is the hold of drawing `i`, in ticks.
- `start_i` is the tick on which drawing `i` first appears.
- `T` is the animation's total length. For a looping animation, use `t mod T` in the last line.
- `R` is the tick rate, the number of game updates per second.

Group the drawings into **phases** and sum the holds in each. For an attack the phases are **windup** (anticipation, the drawings before the hit), **active** (the drawings where the attack can connect) and **recovery** (follow-through and settle). The windup sum is the player's warning time. The recovery sum is how long the attacker is exposed afterwards.

### Numbers you can check

Take one set of six invented drawings for a sword swing. The drawings are *ready*, *coil*, *peak*, *strike*, *follow* and *settle*. The first three are windup, *strike* is active, and the last two are recovery. Three timings of the same six drawings:

| Timing | Holds (ticks) | Windup | Active | Recovery | Total ticks | Total ms |
|---|---|---|---|---|---|---|
| Even | 3, 3, 3, 3, 3, 3 | 9 | 3 | 6 | 18 | 300 |
| Light | 1, 1, 2, 5, 4, 5 | 4 | 5 | 9 | 18 | 300 |
| Heavy | 2, 4, 4, 4, 8, 12 | 10 | 4 | 20 | 34 | 566.7 |

The light timing copies the structure of Sol's punch (4, 5, 9) and the heavy one copies the heavy slash (10, 4, 20). Check two rows by hand. For the heavy timing, the windup is `2 + 4 + 4 = 10`, the active phase is 4, and the recovery is `8 + 12 = 20`. The total is 34 ticks, and `34 × 1000 / 60 = 566.7` ms.

Now look at the even row against the light row. They have the same length, 300 ms, and the same drawings. The even timing still feels wrong for a jab. It spends half its time (9 of 18 ticks) winding up, so the player sees a slow, telegraphed poke that then snaps back. The light timing spends 4 ticks winding up and lets the strike drawing sit for 5, so the eye catches the extended arm. The total didn't change. The distribution did.

Which drawing is on screen at tick 6? Under the light timing, the starts are 0, 1, 2, 4, 9, 13, and tick 6 falls in `4 ≤ 6 < 9`, so it's *strike*. Under the heavy timing, the starts are 0, 2, 6, 10, 14, 22, so tick 6 is the first tick of *peak*. At the same moment, one attack has already landed and the other is still raising the sword.

The code below computes the table and those two lookups. Run it with `.venv/bin/python`.

```python
TICKS_PER_SECOND = 60
DRAWINGS = ["ready", "coil", "peak", "strike", "follow", "settle"]
PHASE = ["windup", "windup", "windup", "active", "recovery", "recovery"]


def schedule(holds):
    starts, t = [], 0
    for h in holds:
        starts.append(t)
        t += h
    return starts, t


def drawing_at(holds, tick):
    starts, total = schedule(holds)
    tick %= total                                  # the animation loops
    for i in reversed(range(len(holds))):
        if tick >= starts[i]:
            return DRAWINGS[i]


def phases(holds):
    out = {"windup": 0, "active": 0, "recovery": 0}
    for h, p in zip(holds, PHASE):
        out[p] += h
    return out


for name, holds in [("even", [3, 3, 3, 3, 3, 3]),
                    ("light", [1, 1, 2, 5, 4, 5]),
                    ("heavy", [2, 4, 4, 4, 8, 12])]:
    starts, total = schedule(holds)
    ms = round(total * 1000 / TICKS_PER_SECOND, 1)
    print(f"{name:5} {total:2} ticks {ms:6} ms {phases(holds)}")

print(drawing_at([1, 1, 2, 5, 4, 5], 6), drawing_at([2, 4, 4, 4, 8, 12], 6))
```

It prints:

```
even  18 ticks  300.0 ms {'windup': 9, 'active': 3, 'recovery': 6}
light 18 ticks  300.0 ms {'windup': 4, 'active': 5, 'recovery': 9}
heavy 34 ticks  566.7 ms {'windup': 10, 'active': 4, 'recovery': 20}
strike peak
```

### The visual

Open [`examples/w08-timing-chart.html`](../examples/w08-timing-chart.html). The left view plays the six drawings of an invented figure made of simple shapes, with a sword drawn as a line. The right view is a **timing chart**, a strip of 60 ticks per second with one colored block per drawing, block width equal to its hold, and the three phases shaded underneath.

Load Even, then Light. The chart's total length doesn't move, but the blocks slide, and the figure's swing changes from a slow poke to a snap. Then load Heavy and switch on quarter speed. Watch the long hold on *settle*. That single block, 12 ticks, is where most of the weight comes from. Drag its slider down to 3 and the heavy swing turns into a light swing that happens to take too long to start.

### Cross-game recognition

The same list of holds appears in every tool and tradition, written in different units.

**Fighting games (Guilty Gear Strive, frame data as of September 2026).** Frame data tables are hold lists summed by phase: startup, active, recovery. They're printed for players because in these games the phase lengths decide who wins an exchange. Dustloop's entry for Sol's heavy slash also lists a 20-frame **hitstop** when it lands as a counter hit. Hitstop is a pause where both characters freeze when a hit lands. In our model, hitstop is an extra hold added to whatever drawing is on screen at the moment of impact, and it's another reason the heavy attack feels heavy.

**Film and hand-drawn animation (20th century to now).** Ones and twos are holds of 1 and 2 at a tick rate of 24. A traditional animator's timing chart, drawn as ticks along a line with the key drawings marked, is the paper version of the interactive's right-hand view.

**Aseprite (current .ase file format).** Aseprite stores a duration in milliseconds for each frame of an animation. A hold of `h` ticks at 60 ticks per second is `h × 1000 / 60` ms. Only holds that are multiples of 3 ticks give whole milliseconds, because 3 ticks is exactly 50 ms. A 1-tick hold is 16.67 ms, and the file can only store 16 or 17. If you plan in ticks and export in milliseconds, plan in multiples of 3 or accept a rounding drift of up to half a millisecond per drawing.

**Godot 4 (SpriteFrames, 4.x documentation).** Godot gives each animation a speed in frames per second and each drawing a relative duration, with the documented rule that a drawing's time on screen is its relative duration divided by the animation's speed times the playback speed. Set the speed to 60 and use your holds as relative durations, and the engine plays the list exactly as planned. Set the speed to 10 and the durations to 1, and every drawing lasts 100 ms, which is 6 ticks, the even-timing habit most beginners fall into.

Four places, one list of holds. When someone describes an animation as "8 frames at 12 fps" or "startup 11", rewrite it as holds in ticks. Then you can compare it with anything.

### Eyes-open design judgment

- **Windup is a design number.** The windup sum is the time a player has to see the attack coming. If you shorten it for snappier feel, you also shorten the opponent's reaction window. Agree the windup with the designer before you animate, and see GD101 week 12 for how that budget is set.
- **Recovery is where weight lives.** Long recovery reads as commitment and gives the opponent a punish window. For a player character, long recovery can also feel sluggish, because the player's input is ignored while it plays. Many action games let a new input cancel the end of recovery. Draw the settle so it looks fine if it's cut short.
- **Hold the key drawing, not every drawing.** The eye reads the drawing that stays longest. Give the longest holds to the drawings that carry the idea (the strike pose, the landing), and keep the in-betweens short.
- **Even timing is the beginner's default, and it's usually wrong.** Every drawing at 100 ms is what you get if you never touch the duration field. It gives equal weight to drawings that don't deserve it.
- **Ticks or seconds?** Holds in ticks assume the game ticks at a fixed rate. If the game runs its logic on variable delta time, your 5-tick active window becomes 83 ms on one machine and something else on another. CS101 week 9 shows the fixed-timestep fix. Tell the programmer which you designed for.

### Check yourself on the model

1. Holds are `[2, 2, 3, 6, 5, 6]` with the same phases as the swing. Give the windup, active and recovery sums, the total in ms, and the drawing on screen at tick 7.
2. A designer wants a heavy attack with at least 20 ticks of windup, using the same six drawings. The first three holds are now `[4, 8, ?]`. What is the smallest third hold that works?
3. An animation is described as "8 drawings at 12 fps" in a tool that runs the game at 60 ticks per second. What is each hold in ticks, and how long is the animation?

<details>
<summary>Answers</summary>

1. Windup `2 + 2 + 3 = 7`, active 6, recovery `5 + 6 = 11`, total 24 ticks, 400 ms. Starts are 0, 2, 4, 7, 13, 18, so tick 7 is the first tick of *strike*.
2. `4 + 8 + h ≥ 20`, so `h = 8`.
3. 12 drawings per second at 60 ticks per second means each is held `60 / 12 = 5` ticks. Eight drawings take 40 ticks, about 667 ms.

</details>

## 3. Loops and walk cycles

A **cycle** is an animation whose last drawing leads back into its first, so it can loop forever. Walks, runs, idles and flying wings are cycles. The model is unchanged, except you read the drawing at `t mod T`.

A walk cycle has one extra rule that ties the art to the game. The character moves across the ground at a speed set by the designer. The feet in the drawings move across the ground at a speed set by the artist. If the two disagree, the feet **slide**, skating over the ground like a moonwalk. To avoid it, the cycle's length must satisfy

```
T_seconds = d / v
```

- `d` is the distance the character's body travels over one full cycle, which for a walk is two steps (one stride with each foot), in pixels.
- `v` is the character's movement speed, in pixels per second.

**Example.** An 8-drawing walk where each step covers 24 pixels, so `d = 48` pixels per cycle. The designer sets the speed to 96 pixels per second. Then `T = 48 / 96 = 0.5` seconds, which is 30 ticks at 60 ticks per second. Eight drawings into 30 ticks don't divide evenly, since `30 / 8 = 3.75`. Use holds `[4, 4, 4, 3, 4, 4, 4, 3]`, which sum to 30 and put the short holds on the passing positions in the middle of each step, where the body is moving and the eye is least fussy.

If the designer later raises the speed to 120 pixels per second, the cycle must shrink to `48 / 120 = 0.4` seconds, 24 ticks, so every hold drops to 3. If the designer wants a range of speeds, most engines scale the playback speed of the cycle with the movement speed. In Godot's terms that's the playback speed in the documented formula. Either way, the numbers come from `d` and `v`, not from how the walk "feels" in the editor preview.

Idles are cycles too, but with no ground contact they can be as long as you like. A common trick is a long idle, 2 to 4 seconds, with one small breath or blink, so the loop point is hard to spot.

## 4. Smears, holds and hitstop

Three tools make fast actions readable at low drawing counts.

**Smear drawings.** When a sword moves a long way between two drawings, the eye may not connect them and the swing seems to teleport. A smear is one drawing, held for 1 or 2 ticks, that stretches the blade and arm along the whole path as a single shape. It's physically wrong and reads perfectly at game speed. In pixel art a smear is often a solid arc in the weapon's lightest color.

**Held key poses.** A drawing held long enough stops reading as motion and starts reading as a pose. Around 6 ticks (100 ms) and up, the eye has time to take in a silhouette. Put the long holds on the poses that must be read, like the peak of a windup that tells the player what's coming.

**Hitstop.** On impact, freeze the attacker and the target on their current drawings for a few ticks. The Dustloop entry for Sol's heavy slash gives 20 ticks of hitstop on a counter hit, a third of a second. Hitstop adds no drawings and costs nothing to draw. It lengthens the strike's hold only when the hit connects, which is why misses in these games feel lighter than hits. It belongs to the programmer and designer, but you should plan for it. The drawing on screen at impact is the one players will stare at during the freeze, so make it your clearest.

## In-class activity (25 minutes)

Work in pairs. Each pair gets a printed strip of six drawings for an invented creature's bite (open, wider, lunge, snap, shake, close) and a timing-chart worksheet with 40 tick boxes.

1. Decide which drawings are windup, active and recovery. Write it down.
2. Design a light timing with a total of 18 to 24 ticks. Color the tick boxes, one color per drawing.
3. Design a heavy timing using the same drawings, with a windup at least twice as long as the light one's.
4. Enter both into the interactive's custom mode and watch them at full and quarter speed. Adjust once each.
5. Swap worksheets with another pair. Without being told which is which, they label each timing "light" or "heavy" and write one sentence on which hold gave it away.

Expected output: two filled timing charts with phase sums, and the other pair's labels and sentence. If they mislabel yours, find the hold that misled them.

## Common misconceptions

- **"More drawings make smoother, better animation."** More drawings make denser animation. Twelve evenly held drawings can feel worse than six well-timed ones. Fix the holds before you add drawings.
- **"Frames per second means how fast the game runs."** Keep the game's tick rate apart from the animation's drawing rate. A 60 tick-per-second game usually shows sprites at 8 to 15 drawings per second.
- **"Heavy attacks need a longer active phase."** In the Guilty Gear data above, the heavy slash is active for fewer ticks than the punch. Heaviness comes from windup, recovery and hitstop.
- **"The walk looks right in the editor, so it's right."** The editor doesn't move the character. Only the `T = d / v` check, or a test in the game, catches sliding feet.

## Check yourself

1. An idle loop has holds `[30, 6, 6, 30, 6, 6]`. How long is it in seconds, and at what tick does the second 30-tick hold begin?
2. You export a hold of 5 ticks to Aseprite. What duration in ms will you type, and what rounding error does it introduce?
3. A run cycle of 6 drawings covers 60 pixels per cycle, and the character runs at 180 pixels per second. How many ticks is the cycle, and what holds would you use?
4. A designer asks you to cut an enemy's heavy attack from 34 ticks to 24 "without making it easier". Which phase would you cut, and why?
5. In Godot, an animation runs at a speed of 12 fps and one drawing has a relative duration of 2.0. How long is that drawing on screen at normal playback, in ms and in ticks?

<details>
<summary>Answers</summary>

1. `30 + 6 + 6 + 30 + 6 + 6 = 84` ticks, 1.4 seconds. The fourth drawing starts at `30 + 6 + 6 = 42`.
2. `5 × 1000 / 60 = 83.33` ms. You type 83, which is 0.33 ms short, so over a long animation the drift adds up. Holds that are multiples of 3 avoid it.
3. `T = 60 / 180 = 1/3` second, 20 ticks. Six drawings into 20 ticks is 3.33 each, so use holds like `[4, 3, 3, 4, 3, 3]`, with the longer holds on the contact poses.
4. Cut recovery, not windup. The windup is the player's warning, so shortening it makes the attack harder to react to, which is a difficulty change. Recovery from 20 to 10 ticks keeps the warning and shortens the punish window, which the designer should hear as a trade-off.
5. `2.0 / (12 × 1) = 0.1667` s, which is 166.7 ms, or 10 ticks.

</details>

## Lab / assignment hook

[Lab 08, one set of drawings, two weights](../labs/lab08.md). You animate a six-to-eight drawing attack for an invented character, deliver it in two timings with a timing CSV for each, and run the provided checker. Deliverable: two GIFs, two CSVs that pass the checker, and a 200-word note on where the time went.

## Sources

- Dustloop Wiki, "GGST/Sol Badguy/Data" (Guilty Gear Strive, page revision of 20 September 2026). Standing P startup 5, active 5, recovery 9; standing H startup 11, active 4, recovery 20, with a note of 20 frames of hitstop on a counter hit (verified September 2026). https://www.dustloop.com/w/GGST/Sol_Badguy/Data
- Dustloop Wiki, character pages and "Glossary" (read September 2026). Startup counts up to and including the first active frame; most fighting games run at 60 frames per second.
- Aseprite, "ASE file format specification" (aseprite repository, main branch, read September 2026). Per-frame duration stored in milliseconds; the old header speed field is deprecated. https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md
- Godot Engine documentation, "SpriteFrames" class reference (Godot 4 stable docs, read September 2026). Animation speed in frames per second, relative frame duration defaulting to 1.0, and the formula for a frame's absolute duration. https://docs.godotengine.org/en/stable/classes/class_spriteframes.html
- Williams, R. (2009). *The Animator's Survival Kit* (expanded ed.; first published 2001). Faber and Faber. Course reading on timing and spacing.
- Wikipedia, "Traditional animation", section "Shooting on twos" (retrieved September 2026). Film runs at 24 frames per second; moving characters are often shot on twos, and quick movements revert to ones because twos are too slow to convey them.
- Thomas, F. & Johnston, O. (1981). *The Illusion of Life: Disney Animation*. Abbeville Press. The principles of anticipation, follow-through and timing.
- The three swing timings, the walk-cycle numbers and the idle example are invented for this lecture.

## Interactive spec: examples/w08-timing-chart.html

**Purpose.** Show that the same six drawings read as light or heavy depending only on how the holds are distributed, and let students read the drawing on screen at any tick.

**Layout.** Two linked views, side by side on desktop, stacked on mobile.

- **Left: stage.** An invented figure built from simple shapes (circle head, rounded-rectangle body, two line-segment arms, a sword as a thick line with a small crossguard). Six poses, defined as joint angles: ready (sword angle 200°), coil (160°), peak (110°), strike (10°), follow (−40°), settle (220°), measured counter-clockwise from pointing right. The sword and arm snap between poses with no interpolation, because the lesson is holds, not tweening. The drawing currently shown is named under the figure, for example "strike (drawing 4 of 6), tick 6".
- **Right: timing chart.** A horizontal strip with one tick per unit width and a ruler every 6 ticks (100 ms). Each drawing is a block whose width is its hold, colored per drawing with its name inside if it fits. Beneath the strip, three phase bands (windup, active, recovery) with their sums in ticks and ms. A playhead line moves across the strip in sync with the stage. Clicking or pressing Left/Right on the strip scrubs the playhead one tick at a time and pauses.
- **Numbers panel.** Total ticks, total ms (one decimal), windup, active and recovery sums, and a table of start ticks per drawing.

**Controls.** Preset buttons Even `[3,3,3,3,3,3]`, Light `[1,1,2,5,4,5]`, Heavy `[2,4,4,4,8,12]`. Six hold sliders (0-24 ticks each, integer steps; a hold of 0 skips that drawing). Play/Pause (Space), Loop toggle, speed selector 1×, ½×, ¼×. A "hitstop on strike" slider (0-20 ticks) that adds a hold to drawing 4 only when a "Hit lands" checkbox is on, drawn as a hatched extension of the strike block. A "compare" toggle that shows a second chart underneath with another preset, both playheads locked to the same tick.

**Formulas.** `start_i = Σ_{j<i} h_j`, `T = Σ h_i`, ms `= T × 1000 / 60`, drawing at tick `t` is the `i` with `start_i ≤ t mod T < start_i + h_i`. Playback advances one tick per 1/60 s at 1× using an accumulator on `requestAnimationFrame` time, so the tick count is correct on 120 Hz screens.

**Test values.** Even: total 18 ticks, 300.0 ms, phases 9/3/6. Light: 18, 300.0, 4/5/9, starts 0,1,2,4,9,13, tick 6 shows strike. Heavy: 34, 566.7, 10/4/20, starts 0,2,6,10,14,22, tick 6 shows peak. Heavy with hitstop 20 and "Hit lands": 54 ticks, 900.0 ms, active phase 24.

**Insight to make obvious.** With compare on and Even over Light, both strips are the same length but the strike block sits at tick 9 in one and tick 4 in the other. The student sees the attack land at different moments from identical drawings.

**Accessibility and style.** Tokens from `templates/interactive-tokens.css`, inline. Drawing colors must also carry the drawing number as text. Under `prefers-reduced-motion`, start paused and advance only on scrub or on a Step button. Keyboard access for every slider and button.
