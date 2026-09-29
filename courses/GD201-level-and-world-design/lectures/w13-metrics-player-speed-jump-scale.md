# GD201 · Week 13 — Metrics: player speed, jump, scale

**Why this matters:** Every ledge, gap, fence and doorway in your level is a question about the player's body: can it step up, jump across, squeeze through? If you answer those questions by eye, playtesters will find the ledge they can't reach and the wall they can hop over. If you answer them from a short list of measured numbers, you can check a whole level on paper before anyone plays it.

**You will be able to:**
- Compute a character's jump height and time to apex from engine constants, and the widest gap it can clear to a ledge at any height.
- Classify a height or gap as a step, a comfortable jump, a skill jump or a wall, using measured metrics and a stated margin.
- Convert metrics into body heights to compare the scale of different games and to size your own spaces.
- Build and run a metrics gym, and use it to correct a model against what the game really does.

**Before class:** The Level Design Book, "Metrics" and "Quake metrics" (book.leveldesignbook.com, the Blockout section). Totten, *An Architectural Approach to Level Design* (2nd ed., 2019), the chapter on scale and proportion. Reread MA101 week 3, section 2, on designing a jump from height and time.

**Prerequisites from earlier courses:** [MA101 week 3, polynomials and quadratic curves](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w03-polynomials-and-quadratic-curves.md) (the jump as a parabola, `g = 2h / t_h²`, and the landing window on a ledge). [GD201 week 2, blockout and greyboxing](w02-blockout-and-greyboxing.md) (scale figures, doorway rules and timing the critical path). [GD201 week 7, verticality and navigation](w07-verticality-and-navigation.md) (safe drop height and one-way edges, which this week's metrics let you find). Kinematics in full is [MA201 week 6](../../MA201-linear-algebra-and-physics-for-games/lectures/w06-kinematics-position-velocity-acceleration.md). Here you need only the formulas from MA101.

**Interactive:** [`examples/w13-jump-reach.html`](../examples/w13-jump-reach.html). Keep it open during section 2.

---

## 1. Two kinds of metric

In level design a **metric** is a measurement that sets the size of things in your level. The Level Design Book separates two kinds, and the distinction is worth keeping.

- **Player metrics** (sometimes called physics metrics) are facts about the character controller. Collision box size, eye height, walk and run speed, maximum step height, jump height, jump distance, safe drop height. You measure them in the engine. They are true or false.
- **Building metrics** are rules you choose for the spaces around the player. A regular corridor is 128 units wide. A low ceiling is 64. A door is 56 by 112. They describe the feel you want. They are good or bad, never true or false.

Building metrics sit on top of player metrics. The book's example minimums show this directly. In Quake, the collision box is 32 units wide and 56 tall, so the smallest hallway the player fits through is 33 units and the lowest ceiling is 57. Its recommended regular hallway is 128 units, four times the player's width. Week 2 gave you the same idea as a rule of thumb (doorways at least twice the scale figure's width). This week turns the rule of thumb into numbers you derive.

A few definitions for the rest of the lecture.

- The **collision box** (or hull, or capsule) is the invisible shape the engine moves around the level. It is not the character model and it is usually wider. When the box touches a ledge, the player is on the ledge, even if the model's feet are in the air.
- **Step height** is the tallest ledge the player walks onto without jumping.
- **Jump height** `h` is the highest the bottom of the collision box rises above the take-off floor.
- **Time to apex** `t_h` is how long the jump takes to reach that height.
- **Run speed** `v` is horizontal speed along the ground, in units per second.

Every engine has its own unit. Quake and Source use units that the community loosely calls inches. Minecraft uses blocks. Unity uses metres and Unreal centimetres. Don't convert between them. Work in the game's own unit, then convert to **body heights** (section 3) when you want to compare games.

## 2. Worked example: how far can the player jump?

### The hook

In Minecraft (Java Edition), a player jumps about 1.25 blocks. That is why you can hop onto a single block, which is one of the first things every player learns. Now look at a wooden fence. It is drawn one block tall, and it has a one-block hitbox for clicking. But its collision box is 1.5 blocks tall, so neither the player nor most mobs can jump over it. The fence is how you keep animals in a pen.

Nobody picked 1.5 because it looks nice. It is the jump height plus a margin. The fence's job ("stop anyone who doesn't have a jump boost") is defined by a player metric. That is the whole idea of this week. Every piece of geometry has a job, and the job is set by comparing its size with the player's metrics.

Height is the easy half. The harder question is horizontal. How wide a gap can the player jump, and how does that width change when the far ledge is higher or lower than the near one? Answer that and you can check every jump in a level before anyone plays it.

### The model

From MA101 week 3 you have a jump designed from its apex height `h` and time to apex `t_h`, with gravity `g = 2h / t_h²`. Most engines instead store a launch speed `v₀` and gravity `g`. Converting is one line each:

```
h   = v₀² / (2g)          apex height
t_h = v₀ / g              time to apex
```

MA101 week 3 solved one ledge with the quadratic formula. Here you solve it once for every ledge height. While in the air the player keeps moving forward at run speed `v`. The target ledge's top is `Δy` above the take-off floor (negative when it is lower). The player rises for `t_h` seconds, then falls from `h` down to `Δy`. The fall takes `sqrt(2(h − Δy) / g)`. Substitute `g = 2h / t_h²` and it simplifies to `t_h × sqrt(1 − Δy/h)`. So the horizontal distance covered before the box drops back to the ledge's height is:

```
reach R(Δy) = v × t_h × (1 + sqrt(1 − Δy / h))       valid for Δy ≤ h
widest gap   G(Δy) = R(Δy) + w
```

- `v` is run speed, `t_h` time to apex, `h` jump height. `v × t_h` is the distance covered while rising. Call it the **rise distance**.
- `Δy` is the height of the far ledge's top above the take-off floor.
- `w` is the width of the collision box. The player stays on the near edge until the back of the box leaves it, and lands once the front of the box reaches the far edge. So the box's width adds to the gap. This is why jumps feel more generous than the arc alone suggests.
- If `Δy > h`, the ledge is above the apex and no gap is clearable.

Read the bracket. At `Δy = 0` it is 2, so a flat gap is twice the rise distance. At `Δy = h` it is 1. A ledge at the apex height allows only the rise distance, half the flat reach. Below take-off, the bracket grows, but slowly, with a square root.

### Numbers you can check

Quake (1996) is a good first case because id Software released its source code. The player jump adds 270 units per second of upward speed, gravity defaults to 800 units/s², the maximum ground speed is 320 units/s, and the collision box is 32 × 32 × 56 units with a maximum step of 18. So:

```
h   = 270² / (2 × 800) = 72,900 / 1,600 = 45.56 units
t_h = 270 / 800        = 0.3375 s
rise distance v × t_h  = 320 × 0.3375   = 108 units
```

| Far ledge `Δy` | As a fraction of `h` | Bracket `1 + sqrt(1 − Δy/h)` | Reach `R` | Widest gap `G = R + 32` |
|---|---|---|---|---|
| −91.1 | −2 | 2.732 | 295.1 | 327.1 |
| −45.6 | −1 | 2.414 | 260.7 | 292.7 |
| 0 | 0 | 2.000 | 216.0 | 248.0 |
| 22.8 | 0.5 | 1.707 | 184.4 | 216.4 |
| 34.2 | 0.75 | 1.500 | 162.0 | 194.0 |
| 41.0 | 0.9 | 1.316 | 142.2 | 174.2 |
| 45.6 | 1 | 1.000 | 108.0 | 140.0 |
| 50.1 | 1.1 | — | — | unreachable |

Check the flat row by hand. Air time on the flat is `2 × 0.3375 = 0.675` s. At 320 units/s that is 216 units, plus the 32-unit box, 248.

Now compare with measurement. The Level Design Book's Quake metrics page gives the maximum running jump distance as 244 units and the maximum standing jump height as 43. The model says 248 and 45.6. It is within 2% on distance and 6% on height. The game steps its physics in frames and the player's box has to clear the ledge's top, not just touch it, so the real limits sit a little under the ideal parabola. That gap between model and game is the reason you still need a gym level (section 4). The model tells you the shape. The gym tells you the exact numbers.

Two rows deserve a second look.

- **The last tenth of the jump height is expensive.** Moving the far ledge from `0.9h` to `h`, only 4.6 units higher, cuts the widest gap from 174 to 140, a fifth of it. Near the apex the arc is almost flat, so a small rise in the ledge moves the landing point a long way back.
- **Dropping down buys less than you expect.** A ledge a full jump height below you extends the gap from 248 to 293, only 18% more. Each extra unit of drop is worth less than the one before, because the player is falling faster and faster.

You can reproduce the table with this code:

```python
from math import sqrt

def jump_from_engine(v0, g):
    """Apex height and time to apex from launch speed and gravity."""
    return v0 ** 2 / (2 * g), v0 / g

def max_gap(dy, h, t_h, v, w):
    """Widest gap (edge to edge) the player can clear to land dy above take-off."""
    if dy > h:
        return None                    # the ledge is above the apex
    return v * t_h * (1 + sqrt(1 - dy / h)) + w

h, t_h = jump_from_engine(270, 800)    # Quake: +270 u/s jump, gravity 800 u/s²
print(f"Quake: h = {h:.2f} u, t_h = {t_h:.4f} s")
for frac in (-2, -1, 0, 0.5, 0.75, 0.9, 1.0, 1.1):
    gap = max_gap(frac * h, h, t_h, v=320, w=32)
    print(f"dy = {frac:5.2f} h ({frac * h:6.1f} u): " +
          ("unreachable" if gap is None else f"max gap {gap:6.1f} u"))
```

```
Quake: h = 45.56 u, t_h = 0.3375 s
dy = -2.00 h ( -91.1 u): max gap  327.1 u
dy = -1.00 h ( -45.6 u): max gap  292.7 u
dy =  0.00 h (   0.0 u): max gap  248.0 u
dy =  0.50 h (  22.8 u): max gap  216.4 u
dy =  0.75 h (  34.2 u): max gap  194.0 u
dy =  0.90 h (  41.0 u): max gap  174.2 u
dy =  1.00 h (  45.6 u): max gap  140.0 u
dy =  1.10 h (  50.1 u): unreachable
```

### The visual

Open [`examples/w13-jump-reach.html`](../examples/w13-jump-reach.html). The left view is a side section: a take-off platform, a gap and a far ledge, with the player's box drawn at take-off and at landing and the arc between them. The right view plots the widest gap `G` against the far ledge's height `Δy` for the whole range. It is the **reach envelope**, and every jump in your level is a dot on this chart.

Drag the far ledge up. On the left, the arc lands short and the box falls into the gap. On the right, the dot crosses the envelope. Now drag it to just under the apex and watch how steeply the envelope drops in its last few units. Switch between the Quake and Half-Life 2 presets. The two envelopes have the same shape, because the bracket is the same, and differ only in scale. That is the point of the model. Every character's jump reach is the same curve, stretched by its rise distance and shifted by its box width.

### Cross-game recognition

**Half-Life 2 (2004, Source SDK 2013 code).** Valve's movement code defines the jump by its height. A constant sets the jump height to 21 units, and the launch speed is computed as `sqrt(2 × gravity × 21)`. With Half-Life 2's gravity of 600 the code uses 160 units/s, which the comment calls "approx. 21 units". This is the MA101 idea written into a shipped engine: pick the height, derive the speed. In our form, `h = 160² / 1,200 = 21.3` units and `t_h = 160 / 600 = 0.267` s. The box is 32 units wide and 72 tall, and the step height is 18, like Quake. Normal run speed is 190 and sprint is 320. So the flat gap is `190 × 0.267 × 2 + 32 = 133` units at a run and `203` at a sprint. Now compare step and jump. A jump rises only 3.3 units higher than a step, so a plain jump hardly opens any ledges that walking doesn't. The code has a second verb for that. Ducking in mid-air shrinks the box from 72 to 36 units and moves it up by the difference, which lifts the feet 36 units. By that arithmetic a crouch-jump reaches about `21.3 + 36 ≈ 57` units. In Half-Life 2 the real climbing metric is the crouch-jump, and a designer who sizes crates by the plain jump will block the player by accident.

**Minecraft (Java Edition, 1.21 era).** Minecraft shows the height bands most clearly. Its attributes give a step height of 0.6 blocks, so slabs (half a block) are walked onto. The jump climbs 1.2522 blocks, so one full block needs a jump. A fence collides at 1.5, so it is a wall. Each band's boundary is about 0.25 to 0.4 blocks above the metric below it, which leaves room for the player's imprecision. For distance, the wiki says a sprinting jump crosses up to four blocks of gap, against two without sprinting. And Minecraft is a warning about models. Its jump strength attribute is 0.42 blocks per tick and its gravity 0.08 blocks per tick². Put those into `v₀² / 2g` and you get 1.10 blocks, not the 1.25 the game achieves. The game steps its physics once per tick, with details the smooth formula leaves out, and the stepped result lands higher. The model's shape still holds. Its exact numbers must come from the gym.

**Real-world building codes.** The same logic governs the spaces you walk through every day. The Level Design Book lists the US convention for stairs, about 7 inches of rise per 11 of run, so each step fits a comfortable adult stride. A building code is a set of building metrics derived from human player metrics (leg length, stride, shoulder width), plus a margin. Your level's building metrics are the same thing for your character.

Three games and one building code, and one idea runs through all of them. Measure the body, derive the envelope, and give each piece of geometry a job by placing it deliberately inside or outside that envelope.

### Design judgment, eyes open

- **Design to measured limits, never to the model's.** Use the gym's numbers (244, 43 in Quake) as the edge of the envelope, not the formula's (248, 45.6). The formula is for understanding and for checking a level quickly.
- **Leave a margin, and write down its size.** The Level Design Book's Quake page tells mappers to build for shorter jumps than the maximum, because most players lack perfect timing. This course uses 80% of the widest gap and 90% of the jump height as the comfortable limit. That is a teaching convention, not an industry constant. Pick your own, state it on the metrics sheet, and apply it everywhere.
- **Use the band between comfortable and maximum on purpose.** A jump at 90% of the envelope is a skill test. Put those on optional routes and secrets, or after the lesson has been taught (week 1). A skill jump on the critical path is a checkpoint problem waiting to happen.
- **Blocking geometry needs a margin too.** If a wall is meant to stop the player, make it taller than the jump plus a margin, as Minecraft's fence does. Remember the extra verbs (crouch-jump, mantling, rocket jumps, bunnyhopping). The Level Design Book's advice for Quake is to let skilled players break optional parts of your map and keep tricks off the critical path.
- **Changing a metric late breaks every level.** Raise run speed by 10% and every gap in the game gets 10% easier. Lower the jump by 5 units and some ledges become walls. Lock player metrics early, and when they must change, rerun the audit (Lab 13 builds one).
- **Edge forgiveness is a design choice.** Some games add a short grace period after the player walks off a ledge during which a jump is still allowed. This widens `G` further. If your game has it, measure the gap in the gym with and without it, and design to the version without.

## 3. Scale: measure in bodies

A unit is not a size. Quake's 45.6-unit jump and Minecraft's 1.25-block jump can't be compared until you divide each by the height of the body doing the jumping. That gives the **body-height ratio**, the most useful way to compare the scale of two games.

| Game | Body height | Step (ratio) | Jump (ratio) | Run speed, bodies per second |
|---|---|---|---|---|
| Quake | 56 u | 18 (0.32) | 45.6 (0.81) | 320 / 56 = 5.7 |
| Half-Life 2 | 72 u | 18 (0.25) | 21.3 (0.30), crouch-jump about 57 (0.80) | run 2.6, sprint 4.4 |
| Minecraft (Java) | 1.8 blocks | 0.6 (0.33) | 1.25 (0.70) | walk 2.4, sprint 3.1 |

The run speeds use Minecraft's 4.317 blocks/s walk and 5.612 blocks/s sprint from the wiki, and Half-Life 2's 190 and 320 from its code.

A few patterns stand out.

- **Step height sits at a quarter to a third of the body in all three.** That is roughly knee height on a person, and a sensible default for your own controller.
- **The climbing verb reaches about three quarters of the body.** Quake's jump, Half-Life 2's crouch-jump and Minecraft's jump all land between 0.7 and 0.81. A player can climb onto something about waist to chest high. Anything above head height is a wall.
- **Speeds are far above human.** Quake's player covers almost six body heights a second. The Level Design Book notes that a Skyrim character runs (not sprints) at about 11.7 mph without tiring. Game spaces are built for these speeds, which is why a room at real-world scale feels small and a real-world distance feels endless.

That last point is why you size spaces by time, not by distance. A 30-second walk is the same experience in a game where you run at 5.7 bodies per second and in one where you walk at 2.4, even though the distances differ by more than a factor of two. Week 2 timed the critical path. Week 9 spaces points of interest in seconds. Both only work once you know the speed.

### Building metrics from player metrics

Once you have the body-height ratios, the week 2 rules become formulas you can apply to any character.

```
minimum corridor width   = 2 × box width        (week 2's rule)
comfortable corridor     = 4 × box width        (Quake's "regular" hallway: 128 = 4 × 32)
minimum ceiling          = box height + 1
comfortable ceiling      = about 2.3 × box height (Quake's "regular" ceiling: 128 ≈ 2.3 × 56)
walk-on ledge            ≤ step height
comfortable jump ledge   ≤ 0.9 × jump height    (this course's margin)
blocking wall            > jump height + margin, including every climbing verb
```

The multipliers are this course's reading of the Quake metrics page, not laws. Your camera changes them. A third-person camera sits behind and above the character and needs more room than a first-person camera at eye height, so corridors that feel fine in first person feel cramped in third. Measure your own in the gym.

## 4. The metrics sheet and the gym

Put your player metrics on one page, the **metrics sheet**, and share it with everyone who builds levels. It holds each metric, its measured value, the margin the team agreed and the date it was last checked. When a programmer changes the controller, the sheet changes the same day.

The numbers on the sheet come from a **gym** (the Level Design Book calls it a metrics zoo): a developer-only test map that exists to measure the character. A good gym has:

- **A step ramp:** a row of ledges rising in small increments (2 units in Quake, 0.1 m in Unity). Walk into each. The last one you step onto without jumping is your step height.
- **A jump wall:** the same idea, higher ledges. The last one you can jump onto is your jump height. Repeat with every climbing verb.
- **A gap ladder:** pairs of platforms with gaps widening in fixed steps, at several height differences (flat, half a jump up, a full jump down). The widest gap you clear ten times out of ten is the comfortable limit. The widest you clear at all is the maximum.
- **A drop tower** for the safe drop height from week 7.
- **Corridors and doorways** at 1, 1.5, 2, 3 and 4 box widths, and ceilings at several heights, to feel the building metrics with the real camera.
- **A timed run:** a straight track with marks every 10 units of distance and a timer, to measure run speed.

Label every piece in the gym with its size, using world-aligned grid textures so distances are readable at a glance. Then compare the gym with the model. If your gap ladder disagrees with `G(Δy)` by more than a few percent, something in the controller is not what you think: air control, acceleration, a speed cap in the air, a frame-rate dependency. Find out which before you build levels on it.

### Auditing a level

With the sheet and the formula, you can audit a blockout without playing it. List every jump on the critical path with its gap and height difference. Compute `G(Δy)` for each. Flag any jump above your comfortable margin, and any blocking wall below the jump height plus margin. Week 7's safe-drop check belongs on the same list. Lab 13 has you write this audit as a small script and run it on a level.

The audit doesn't replace playtesting. It catches the mistakes that playtesting would find slowly and at greater cost, so your testers spend their time on the questions only a player can answer.

## In-class activity (25 minutes)

Pairs, squared paper (1 square = 16 units) and a calculator.

1. **(5 min)** Use the Quake metrics (`h = 45.6`, `t_h = 0.3375`, `v = 320`, `w = 32`, step 18). Draw a side section of a short platforming route with five jumps, mixing flat gaps, jumps up and jumps down. Label every gap and height difference.
2. **(10 min)** Swap with another pair. Audit their route. For each jump compute `G(Δy)`, then classify it as comfortable (at most 80% of `G` and at most 90% of `h`), skill (between that and the maximum) or impossible.
3. **(5 min)** Add one blocking element to the route (a wall the player must not climb) and one secret jump that only a skilled player should make. Size both with the envelope.
4. **(5 min)** Return the sheets. Each pair explains one jump where the auditor's classification surprised them.

Expected output: the annotated section, the audit table with five rows, and the sizes of the wall and the secret jump with their reasoning.

## Common misconceptions

- **"A ledge at 90% of jump height is nearly as easy as a flat jump."** The widest gap falls fastest near the apex. At `0.9h` it is already 30% shorter than flat in Quake, and at `h` it is 44% shorter.
- **"Jumping down makes any gap possible."** The extra reach grows with the square root of the drop. A full jump height of drop adds less than a fifth to Quake's flat gap.
- **"The model's numbers are the game's numbers."** Frame stepping, box clearance, air control and acceleration all move the real limits. Measure them in a gym and use the model to understand the shape.
- **"Scale means matching the real world."** Game characters move several times faster than people and their spaces are built for that. Scale means proportion to the player's body and speed.

## Check yourself

1. In Half-Life 2 at normal run speed (190), what is the widest gap to a ledge 18 units higher than take-off? Would a sprinting player (320) clear a 150-unit gap to the same ledge?
2. In Quake, walking without the run key gives a forward speed of 200. You want a gap that walkers cannot clear on the flat but that runners clear comfortably (at most 80% of their widest gap). Which gap widths work?
3. A new game's controller has `h = 1.5` m, `t_h = 0.35` s, `v = 6` m/s and a box 0.6 m wide. What are the widest gaps on the flat and to a ledge 1.2 m high? Under this course's margins, is the ledge a comfortable jump?
4. Minecraft's fence collides at 1.5 blocks. Using the jump height, give its margin in blocks and as a percentage of the jump. Then name one thing players can do to get over it anyway, and say what that means for a designer who uses fences to block routes.

<details>
<summary>Answers</summary>

1. `h = 21.33`, `t_h = 0.2667`, rise distance `190 × 0.2667 = 50.67`. `sqrt(1 − 18/21.33) = sqrt(0.156) = 0.395`. `G = 50.67 × 1.395 + 32 = 102.7` units. Sprinting, the rise distance is 85.33 and `G = 85.33 × 1.395 + 32 = 151.1`, so 150 units is just clearable, with essentially no margin. It is a skill jump.
2. Walkers: rise distance `200 × 0.3375 = 67.5`, flat `G = 135 + 32 = 167`. Runners: flat `G = 248`, comfortable limit `0.8 × 248 = 198.4`. Any gap wider than 167 and at most about 198 works. Leave margin on both sides, around 180 to 190. (In practice, measure both limits in the gym first, since the real runner maximum is 244.)
3. Rise distance `6 × 0.35 = 2.1` m. Flat `G = 4.2 + 0.6 = 4.8` m. For 1.2 m, `1 − 1.2/1.5 = 0.2`, `sqrt(0.2) = 0.447`, `G = 2.1 × 1.447 + 0.6 = 3.64` m. The ledge is at `1.2 / 1.5 = 80%` of jump height, under the 90% limit, so it is comfortable for any gap up to `0.8 × 3.64 = 2.91` m.
4. `1.5 − 1.2522 = 0.25` blocks, about 20% of the jump. The wiki notes that a carpet placed on a fence lets players (but not mobs) jump onto it, and knockback can push a player over. A designer who needs a hard block must check every verb and item that changes the metric, not just the plain jump.

</details>

## Lab / assignment hook

[Lab 13, metrics gym and jump audit](../labs/lab13.md). You finish a small Python module that computes the reach envelope and audits a list of jumps, then build a metrics gym in your engine, measure your controller, correct the model against the measurements and audit your own blockout from Lab 02. The corrected metrics sheet is part of the final zone's design document.

## Sources

- The Level Design Book, "Metrics" (book.leveldesignbook.com, Blockout section, accessed September 2026). Player metrics versus building metrics; the metrics zoo test map; the list of core player metrics to measure; Skyrim world about 14 square miles and a running speed of about 11.7 mph; common player sizes by engine (Quake, Half-Life and Source 32 × 72); US stair convention of about 7 inches rise to 11 run; minimum hallway at least double the player width.
- The Level Design Book, "Quake metrics" (accessed September 2026). Collision hull 32 × 32 × 56; minimum hallway 33 and ceiling 57; maximum run speed 320 u/s; step 18; maximum running jump distance 244 and standing jump height 43; regular hallway 128 wide, regular ceiling 128; gravity 800; advice to build for shorter jumps and keep trick jumps off the critical path.
- id Software, Quake source code (released 1999, GitHub repository id-Software/Quake). `QW/client/pmove.c`: jump adds 270 to vertical speed, `STEPSIZE 18`, player box from (−16, −16, −24) to (16, 16, 32). `WinQuake/sv_phys.c`: `sv_gravity` 800. `WinQuake/sv_user.c`: `sv_maxspeed` 320. `WinQuake/cl_input.c`: `cl_forwardspeed` 200, doubled by the run key.
- Valve, Source SDK 2013 (GitHub repository ValveSoftware/source-sdk-2013), for Half-Life 2 (2004). `gamemovement.h`: `GAMEMOVEMENT_JUMP_HEIGHT 21`. `gamemovement.cpp`: launch speed `sqrt(2 × gravity × 21)`, 160 in Half-Life 2 at gravity 600; ducking in the air moves the origin up by the difference between standing and ducking hulls. `gamerules.cpp`: hull 32 × 32 × 72, ducking hull 36 tall, eye height 64. `movevars_shared.cpp`: `sv_gravity` 600 for Half-Life 2, `sv_stepsize` 18. `hl2_player.cpp`: walk 150, normal 190, sprint 320.
- Minecraft Wiki (Java Edition, 1.21 era, accessed September 2026). "Jumping": jump height 1.2522 blocks. "Fence": collision box 1.5 blocks tall, carpet and knockback exceptions. "Attribute": step height 0.6, jump strength 0.42 blocks per tick, gravity 0.08 blocks per tick². "Player": 1.8 × 0.6 blocks. "Walking": 4.317 blocks/s. "Sprinting": 5.612 m/s; sprint jumps cross up to four blocks against two without sprinting.
- Totten, C. W. (2019). *An Architectural Approach to Level Design* (2nd ed.). CRC Press.
- The reach formula `G(Δy)`, the 80% and 90% margins and the building-metric multipliers in section 3 are teaching models built for this lecture. The Quake and Half-Life 2 reach values are computed from engine constants, not measured in the games.

## Interactive spec: examples/w13-jump-reach.html

**Purpose.** Show that a character's jump reach is one curve, the reach envelope `G(Δy)`, and that every jump in a level is a point that sits inside or outside it.

**The one insight the visual must make obvious.** The widest clearable gap falls steeply as the far ledge approaches the apex height (half the flat reach at `Δy = h`), and grows only slowly for ledges below take-off. Different games have the same envelope shape, scaled by rise distance `v × t_h` and shifted by box width `w`.

**Layout.** Mobile (390px): side view on top, envelope chart below, controls, numbers panel. Desktop (1280px): side view and envelope side by side, controls and numbers below.

- **Side view, "The jump".** A take-off platform on the left ending at x = 0, a gap of width `gap`, a far ledge whose top is at height `Δy` (drawn below the take-off level when negative). Draw the collision box (width `w`, height = body height of the preset) at take-off with its back edge at x = 0, and the arc of the box's bottom-front corner from take-off. If the jump succeeds, draw the box resting on the far ledge with its front edge at x = gap. If it fails, draw the box's final position at the far ledge's height in the gap, in the "fail" colour. Dashed horizontal lines at the apex height `h` and at the step height. Grid in game units.
- **Envelope view, "Widest gap vs ledge height".** x axis `Δy` from `−2h` to `1.2h`, y axis gap from 0 to `G(−2h) × 1.1`. Solid curve `G(Δy)` for `Δy ≤ h`. Dashed curve `m × G(Δy)` for the margin. Vertical dashed lines at `Δy = step` and `Δy = 0.9h`. Region shading: comfortable (below the margin curve and `Δy ≤ 0.9h`), skill (between the curves or `0.9h < Δy ≤ h`), impossible (above `G` or `Δy > h`), with patterns as well as colour. The current jump is a large dot. Optional faint second curve for a comparison preset.

**Controls.** Preset select: "Quake, run" (`v0 = 270`, `g = 800`, `v = 320`, `w = 32`, body 56, step 18), "Quake, walk" (same, `v = 200`), "Half-Life 2, run" (`v0 = 160`, `g = 600`, `v = 190`, `w = 32`, body 72, step 18), "Half-Life 2, sprint" (`v = 320`), "Custom" (enables `h` slider 0.5 to 3 m step 0.05 default 1.5, `t_h` 0.2 to 0.6 s step 0.01 default 0.35, `v` 2 to 12 m/s step 0.1 default 6, `w` 0.2 to 1.2 m step 0.05 default 0.6, body 1.8 m, step 0.4 m). `gap` slider 0 to `1.2 × G(−2h)` (step 1 unit, or 0.05 m in Custom), default 200 in Quake units. `Δy` slider `−2h` to `1.2h` (step 0.5 unit, 0.05 m), default 0. Margin `m` slider 0.5 to 1.0, step 0.05, default 0.8. "Compare with" select (none or any preset) draws that preset's envelope faintly, in its own units scaled by `h` on x and by `G(0)` on y when "normalise" is ticked. Normalise checkbox: x becomes `Δy / h` and y becomes `G / G(0)`, so all presets collapse onto the same curve except for the effect of `w`. Reset.

**Formulas.**
```
h   = v0^2 / (2 g)          t_h = v0 / g         (presets)
g   = 2 h / t_h^2           v0  = 2 h / t_h      (Custom)
R(dy) = v * t_h * (1 + sqrt(1 - dy/h))           for dy <= h
G(dy) = R(dy) + w
arc of the box's bottom-front corner, from x = w at take-off:
  rise:  y(t) = v0 t - g t^2 / 2,   x(t) = w + v t
success if dy <= h and gap <= G(dy)
band: impossible if dy > h or gap > G(dy); skill if gap > m G(dy) or dy > 0.9 h; else comfortable
if dy <= step and gap == 0: label "walk"
```

**Numbers panel.** `h`, `t_h`, rise distance `v × t_h`, `G(0)`, `G(Δy)` for the current ledge, the current gap as a percentage of `G(Δy)`, the band, and a sentence from the data, for example "Quake, run: a ledge 41.0 u up allows at most 174.2 u of gap; your 150 u gap is 86% of that, a skill jump."

**Test values.**

| Setting | Expected |
|---|---|
| Quake run | `h = 45.5625`, `t_h = 0.3375`, rise 108.0, `G(0) = 248.0` |
| Quake run, `Δy = 22.78` (0.5h) | `G = 216.4` |
| Quake run, `Δy = 41.0` (0.9h) | `G = 174.2` |
| Quake run, `Δy = h` exactly (45.5625, the "h" shortcut button) | `G = 140.0`. Typing the rounded 45.56 gives 140.8, because the square root is steep near `h` |
| Quake run, `Δy = −h` (the "−h" button) | `G = 292.7` |
| Quake run, `Δy = −2h` (the "−2h" button, −91.1) | `G = 327.1` |
| Quake run, `Δy = 50` | impossible, "ledge above apex" |
| Quake walk | `G(0) = 167.0` |
| HL2 run | `h = 21.333`, `t_h = 0.2667`, `G(0) = 133.3`, `G(18) = 102.7` |
| HL2 sprint | `G(0) = 202.7`, `G(18) = 151.1` |
| Custom defaults | `G(0) = 4.80` m, `G(1.2) = 3.64` m |
| Quake run, gap 150, `Δy = 41.0`, `m = 0.8` | 86% of `G`, band "skill" |
| Normalise on, `w` ignored | all presets give `G/G(0) = 0.5` at `Δy/h = 1` (show `R/R(0)` when "exclude box width" is ticked) |

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Bands differ by pattern (solid, hatched, dotted) as well as colour. Native range inputs with numeric readouts and keyboard steps. Respect reduced motion (no animated arc, draw it at once). No game art, logos or screenshots. The player is a plain rectangle.
