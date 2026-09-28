# UX201 · Week 10 — HUD and Information Design

**Why this matters:** Every number on a HUD costs the player a look, and every look is time their eyes are off the fight. Teams argue about HUD layout by taste ("clean", "immersive", "cluttered"). This week gives you a way to price a look in milliseconds, so you can say which change to the HUD buys the most attention back and which is decoration.

**You will be able to:**
- Compute the angle between the point of action and a HUD element from screen size, viewing distance and position, for PC and TV setups.
- Estimate the time cost of one HUD check and the share of a fight a player spends looking away, and compare HUD designs by that share.
- Classify HUD elements with the Fagerholt and Lorentzon design space (non-diegetic, diegetic, spatial, meta) and predict the trade-off each placement brings.
- Build an information inventory for a HUD (what, how often, how urgent) and use it to decide what earns a place on screen and what should appear only when needed.

**Before class:** Celia Hodent, *The Gamer's Brain* (CRC Press, 2017), reread "Perception" (pp. 19-34) and "Attention" (pp. 51-58). Erik Fagerholt and Magnus Lorentzon, *Beyond the HUD: User Interfaces for Increased Player Immersion in FPS Games* (MSc thesis, Chalmers University of Technology, 2009), section 7 (the UI design space, about 6 pages, free online). Wikipedia, "Saccade" (the sections on timing and main sequence).

**Prerequisites from earlier courses:** [UX201 week 1, perception, attention and memory](w01-perception-attention-memory.md), for pop-out features and the fact that the fovea is small. [UX201 week 2, cognitive load and UI](w02-cognitive-load-and-ui.md), for split attention and the working-memory budget. [GD101 week 12, feedback, juice, clarity and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md), for telegraphs and the idea that feedback must be read in time. [MA101 week 10, angles, radians, sin and cos](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md), because this week turns centimetres on a screen into degrees of visual angle with an arctangent.

**Interactive:** [examples/w10-hud-glance-cost.html](../examples/w10-hud-glance-cost.html). Use it during section 2.

---

## 1. What a HUD is for

A **HUD** (heads-up display) is the information a game shows on top of, or inside, the play view while you play. The name comes from aircraft, where flight data is projected onto glass so the pilot can read it without looking down at the instruments. That origin already contains this week's whole argument. The point of a HUD is to shorten the trip between the thing you are watching and the thing you need to know.

A HUD answers four questions for each piece of information.

- **What** does the player need? Health, ammunition, cooldowns, the map, the objective.
- **When** do they need it? All the time, only in combat, only when it changes, only when they ask.
- **Where** should it sit? In a screen corner, next to the character, on the character, in the world.
- **How** is it encoded? A number, a bar, a colour, an icon, a sound, a vibration.

Most HUD arguments are about "where". Most HUD gains come from "when" and "how". The worked example shows why, with numbers.

Two facts from week 1 do most of the work. First, you see sharply only in a small central patch. The fovea covers about 5° of the visual field, and acuity falls to half the central value just 2° out and to one sixteenth by 30°. Second, peripheral vision is weak at detail and colour but good at motion. So a number in a screen corner cannot be read while you look at the boss. A large, pulsing red shape in the same corner can be noticed. Those are different jobs, and the HUD designer decides which one each element does.

## 2. Worked example: the price of a glance

### The hook

Dead Space (2008) shipped with no conventional HUD. Isaac Clarke's health is a glowing bar down the spine of his suit. Ammunition appears as a small hologram on the weapon when he raises it. Menus, the map and video calls are projected into the world as holograms, and the game keeps running while you use them.

It is the example most writing on game HUDs reaches for, including the thesis you read for today, and it is usually praised for immersion. But look at where the camera sits. Dead Space uses an over-the-shoulder third-person view, and Isaac's back is close to the centre of the screen, right next to the point you aim at. The health bar is on the character, but it is also inches from your crosshair. So is the "immersive" HUD better because it is fictional, or because it is close? And if it is closeness, how close is close enough? A health bar in the corner of a TV and one in the corner of a desk monitor are the same number of pixels from the centre. Are they the same distance for your eyes?

### The model

When you check a HUD element that sits away from where you are looking, your eyes do three things. They jump out to it, they rest on it long enough to read it, and they jump back. The jump is a **saccade**, a fast eye movement. The rest is a **fixation**. We price each part.

First, turn screen position into **visual angle**, the angle at your eye between the point of action and the element:

```
θ = atan(d / D)
```

- `d` is the distance on the screen from the point of action (usually the screen centre or the crosshair) to the element, in centimetres.
- `D` is the viewing distance from eye to screen, in the same units.
- `θ` is in degrees.

Then price one check of that element:

```
T(θ) = F                              if θ ≤ θ_f
T(θ) = 2 × (L + s(θ)) + F             if θ > θ_f
s(θ) = 20 + 2.5 × θ                   (milliseconds)
```

- `F` is the fixation time needed to read the element. Reading research puts average fixations at 200-250 ms, so **we use `F = 250 ms`** for reading a number or a bar.
- `θ_f` is the radius you can read without moving your eyes. The fovea spans about 5°, so **we use `θ_f = 2.5°`**. Inside that radius, the check costs only the reading time.
- `L` is the **saccade latency**, the delay before a saccade starts. It is about 200 ms for an unexpected target, and shorter for practised moves to a known place. **We use `L = 200 ms`** and you will vary it.
- `s(θ)` is the saccade's own duration. Saccades last from about 20 to 200 ms depending on size. The line `20 + 2.5θ` is our teaching fit to the velocity figures on the Wikipedia "Saccade" page (a 10° saccade reaches about 300°/s, a 30° one about 500°/s). It gives 45 ms at 10° and 95 ms at 30°.
- The factor 2 is the trip out and the trip back.

Finally, if the player checks the element `f` times per minute, the share of time their eyes are off the action is the **look-away share**:

```
E = f × T(θ) / 60,000
```

Every value marked "we use" is a teaching assumption. The lab measures real ones.

### Numbers you can check

The setting is a boss fight in which the player checks their health **20 times per minute**, once every three seconds (a teaching assumption).

Two screens:

- **PC.** A 24-inch 16:9 monitor is 53.1 cm wide and 29.9 cm tall. At 60 cm from the eyes, put a health readout 3 cm in from the top-left corner. It sits `53.1 / 2 − 3 = 23.57` cm left of the centre and `29.9 / 2 − 3 = 11.94` cm above it, so `d = √(23.57² + 11.94²) = 26.4 cm`. So `θ = atan(26.4 / 60) = 23.8°`.
- **TV.** A 55-inch TV is 121.8 cm by 68.5 cm. Put the readout at the same relative position. It is now 60.5 cm from the centre, but the player sits 250 cm away, so `θ = atan(60.5 / 250) = 13.6°`.

The TV corner is closer to the eye than the monitor corner, by ten degrees, even though it is the same corner in the same layout. Now five designs:

| Design | Where and how | θ | T per check | Checks per min | Look-away share `E` |
|---|---|---|---|---|---|
| A | Number in corner, PC | 23.8° | 809 ms | 20 | 27.0% |
| B | Number in corner, TV | 13.6° | 758 ms | 20 | 25.3% |
| C | Bar near the character (Dead Space-like) | 5.0° | 715 ms | 20 | 23.8% |
| D | Bar hugging the crosshair | 2.0° | 250 ms | 20 | 8.3% |
| E | Corner bar with colour and pulse the periphery can read | 23.8° | 809 ms | 4 | 5.4% |

Check two rows by hand.

- **A:** `s = 20 + 2.5 × 23.8 = 79.5 ms`. `T = 2 × (200 + 79.5) + 250 = 809 ms`. `E = 20 × 0.809 / 60 = 0.270`.
- **E:** the bar sits in the same corner, but it changes colour and pulses as health falls. The player's periphery picks up the change, so they only look directly when something happens, say 4 times a minute. `E = 4 × 0.809 / 60 = 0.054`.

Three things stand out.

1. **Distance barely matters once you have to move your eyes.** Going from 23.8° to 5° (A to C) saves only 94 ms per check and 3 points of look-away share. Most of a glance is the latency and the reading, not the travel.
2. **Not moving your eyes at all is the big win.** D and C are 3° apart, but D is inside the reading radius. That 3° is worth 15 points of look-away share, five times more than the 19° between A and C.
3. **Checking less often is the other big win.** E keeps the worst position on the screen and still beats D, because an encoding the periphery can read turns 20 looks into 4.

Now answer the hook. Dead Space's spine bar sits a few degrees from the crosshair, so on this model its gain over a corner readout is modest. What it also does is change "how": the bar is a large, coloured shape on the object you are already watching, so you can see "low" without reading anything. That is design E's trick more than design C's. The fiction is a bonus. The encoding does the work.

### A visual you can move

Open `examples/w10-hud-glance-cost.html`. The left view is a screen seen from the player's eye. Drag the health element anywhere on it. Two rings are drawn around the centre, the 2.5° reading radius and a 20° ring beyond which real players also turn their heads. Switch the display between PC (24 inches at 60 cm), TV (55 inches at 250 cm) and handheld (7 inches at 35 cm) and watch the rings change size on the same screen.

The right view plots the look-away share against θ for the current checks-per-minute. The line is a cliff followed by a gentle slope. Drag the element in from the corner and the dot slides down the gentle slope. Drag it inside the inner ring and it drops off the cliff. Then leave it in the corner and pull the checks-per-minute slider from 20 down to 4. The whole line sinks. The insight should be obvious in five seconds of play: where you put an element moves you along a slope, while whether the eye must move and how often it must go are the steep parts.

### Cross-game recognition

**World of Warcraft Edit Mode (patch 10.0.0, October 2022).** WoW's Edit Mode lets players rearrange the default HUD frames and share layouts. Before it, players used addons for the same thing. In our terms, Edit Mode hands the "where" decision to the player, who knows their own monitor and viewing distance. A raider who drags their own health frame and the boss's cast bar toward the centre is shrinking θ. A raider who uses Deadly Boss Mods (week 2) has a timer bar that grows and flashes as the mechanic approaches, which cuts `f`, because they no longer need to check.

**Contextual HUDs: Red Dead Redemption 2 and Horizon Zero Dawn.** Red Dead Redemption 2 shows only the minimap and the horse's stamina while you ride, and brings up ammunition and other combat information when a fight starts. Horizon Zero Dawn lets the player set each HUD element to always show, show only when relevant, or never show. Both are design E in a different form. The element appears when its state matters, so the player doesn't pay a look to learn that nothing has changed.

**Meta-perception: Killzone 2 and the heartbeat.** Fagerholt and Lorentzon describe Killzone 2 using blood on the screen to show low health, rather than a meter, and note that a heartbeat sound or a pulsing controller vibration can carry the same message. These are the purest form of E. The signal fills the periphery, or leaves vision entirely for sound and touch, so the look costs nothing. The price is resolution. You learn "badly hurt", not "34 HP".

In every case the move is the same. Write the element as `f × T(θ)` and ask which factor the design attacks. Moving it attacks θ, and gains little unless it crosses into the reading radius. Showing it on demand, or encoding it so the periphery can read it, attacks `f`, and gains a lot.

### Eyes-open design judgment

- **The model ignores the cost of leaving.** While your eyes are on the corner, you are not watching the boss. A telegraph that starts and ends inside that 800 ms is missed. The look-away share is roughly the chance that a brief event starts while you are looking away, and that is the number to put in front of a combat designer.
- **Close is not free.** An element that hugs the crosshair covers the thing you aim at, and it adds to the clutter you search through (week 1). Only the few elements checked most often, in the tensest moments, should earn a place inside the reading radius.
- **Peripheral encodings trade resolution for cost.** A red vignette tells you "danger" but not "how much". If the decision depends on the exact number (can I survive one more hit?), the player will look anyway. Give them both: a peripheral cue for "look now", and a readable number for when they do.
- **Head movement changes the price past about 20°.** Gaze shifts larger than about 20° usually bring a head turn, which is slower than the eye alone. Our model leaves this out, so it flatters large desk monitors and ultrawide screens. On those, corner elements cost more than the table says.
- **Screen and seat change the answer.** The same layout gives 24° on a desk and 14° on a couch. Test on the setups your players use, and let players move and scale elements, because you can't know every seat.
- **The numbers are placeholders.** `L`, `F` and the saccade line are averages from lab tasks. Practised players make faster, anticipatory glances. The ranking of designs is more robust than the milliseconds.

### Check yourself (worked example)

1. A player sits 45 cm from a 24-inch monitor (53.1 × 29.9 cm). A cooldown icon is 10 cm below the screen centre. Compute θ and the cost of one check.
2. On the TV setup, the player checks the minimap 12 times per minute. It is 55 cm from the centre. What is its look-away share? What if a contextual rule shows it only when an objective updates, 3 times a minute?
3. A designer moves the PC health readout from 23.8° to 12°. Another adds a pulsing low-health border and expects checks to fall from 20 to 10 per minute. Which change buys more? Show both.

<details>
<summary>Answers</summary>

1. `θ = atan(10/45) = 12.5°`. `T = 2 × (200 + 20 + 31.3) + 250 = 752.5 ms`.
2. `θ = atan(55/250) = 12.4°`, `T = 2 × (200 + 20 + 31) + 250 = 752 ms`. `E = 12 × 0.752 / 60 = 15.0%`. With 3 checks a minute, `E = 3.8%`.
3. Moving it: `T(12°) = 2 × (200 + 50) + 250 = 750 ms`, `E = 20 × 0.75 / 60 = 25.0%`, a gain of 2 points over 27.0%. The border: `E = 10 × 0.809 / 60 = 13.5%`, a gain of 13.5 points. The border wins by a wide margin.

</details>

## 3. The HUD design space: fiction and space

Fagerholt and Lorentzon's 2009 thesis, written with EA DICE, gives the vocabulary most studios now use. They started from film theory, where **diegetic** means "part of the story world" (a radio playing in the scene) and **non-diegetic** means outside it (the soundtrack, the subtitles). Then they found the single axis too blunt. Is blood splattered on the camera part of the world? The character's face would be splattered, not their retinas.

So they split the question in two.

- **Is the element part of the fiction?** Does it exist in the game's story world?
- **Is the element in the 3D space?** Is it drawn in the scene's geometry, or as a flat overlay?

That gives four kinds of element.

| | In the 3D space | Flat overlay |
|---|---|---|
| **In the fiction** | Diegetic: Dead Space's spine bar, a wristwatch the character reads | Meta: an in-world phone shown as an overlay (their example is the phone in Grand Theft Auto IV) |
| **Outside the fiction** | Spatial (they call it geometric): outlines through walls, glowing path markers, floating names | Non-diegetic: the classic health bar and minimap in a corner |

Their analysis of shooters of the time found that most HUD information was non-diegetic. They also described **signifiers**, diegetic cues the player has to interpret, such as smoke from a weapon about to break.

Use the grid as a menu, not a ranking. Each cell has a typical price.

- **Non-diegetic** elements are cheap to build, easy to read, easy to make accessible (you can resize them, recolour them, add backplates, week 11) and easy to localise. They cost immersion if you think immersion is the goal, and they tend to end up in corners, at large θ.
- **Diegetic** elements fit the world and often sit near the action, because they live on the character or the weapon. They are hard to resize, hard to recolour for colour-blind players, and limited by what the fiction allows. A watch can't show a number that the world has no reason to know.
- **Spatial** elements put information where it is used, which kills split attention (week 2). They also add to scene clutter, raising `N` for every search (week 1), and they can occlude the scene.
- **Meta** elements carry information through effects on the view itself, such as blood, blur, desaturation or a heartbeat. They are the cheapest to read, often readable in the periphery, and the lowest in resolution.

The worked example tells you how to choose. Put the element where it gets the lowest `f × T(θ)` without losing the resolution the decision needs.

## 4. An information inventory

Before you draw a HUD, list what it must carry. The inventory is a table with one row per piece of information. For each row, note the following.

- **Frequency:** how often the player needs to check it in the tensest moment of play.
- **Urgency:** how bad it is to learn it one second late.
- **Resolution:** does the decision need the exact value, a band (low, medium, high), or just a yes/no?
- **Change rate:** how often it changes. Something that rarely changes should rarely need a look.

Here is an inventory for an invented action RPG boss fight.

| Information | Checks per min | Urgency | Resolution needed | Changes | Suggested treatment |
|---|---|---|---|---|---|
| Own health | 20 | High | Band, exact near death | Often | Bar near character, colour bands, low-health pulse |
| Boss cast | 10 | High | Which attack, how long | Often | Spatial telegraph on the boss, cast bar under boss |
| Potion count | 3 | Medium | Exact | Rarely | Corner, number, flashes when it drops |
| Gold | 0 | None | Exact | Rarely | Hide in combat |
| Quest objective | 0.2 | Low | Text | Rarely | Hide in combat, show on change |
| Minimap | 2 | Low in this fight | Map | Slowly | Shrink or hide in the arena |

Rows with high frequency and high urgency earn the centre of the screen and a peripheral encoding. Rows that change rarely should use "show on change" rather than a permanent slot. Rows with zero checks in combat should disappear in combat. That is the contextual HUD of Red Dead Redemption 2, derived from a table instead of a style choice.

Two rules come out of the table.

- **Budget the centre.** Only two or three elements fit inside the reading radius without covering the play. Spend them on the highest `f × urgency`.
- **Make every permanent element earn its place with `f`.** An element checked less than once a minute in combat costs clutter all the time and saves almost nothing when it is on screen.

## 5. Encoding: making the periphery do the work

Week 1 listed the features that guide attention without a search: colour, motion, orientation and size. Peripheral vision is weak at colour far out and weak at detail, but it detects motion well. That gives a short set of rules for the elements you want read without a look.

- **Use size and motion for "look now".** A bar that grows, a border that pulses, or an icon that bounces will be noticed from a corner. A digit changing from 41 to 34 will not.
- **Use colour for bands, with a second channel.** Green, amber and red bands are quick to learn, but colour alone fails for colour-blind players and weakens in the far periphery. Pair colour with shape, fill level or position (week 11 covers this in detail).
- **Use numbers only where the player will look.** Numbers need the fovea. Put them where the eye already goes, or accept the glance.
- **Keep positions fixed.** An element that always sits in the same place can be reached with a practised saccade, which shortens `L`. A HUD that rearranges itself makes every check a search.
- **Use sound and touch to leave vision entirely.** A heartbeat at low health, a rising tone for a charge, a controller pulse on a hit. These are free in look-away terms, and they help players who cannot rely on vision.

One caution about "clean" HUDs. Removing everything does not remove the player's need to know. It moves the knowledge into their head, which costs working memory (week 2), or into guesswork, which costs deaths. A minimal HUD is good design only when the information has somewhere else to live, such as the world, the character's animation, the sound, or the player's own well-practised count.

## In-class activity (25 minutes)

Groups of three. You need one screenshot of a shipped game's combat HUD (bring your own, or use a still from a gameplay video) and a ruler or an image editor that shows pixel positions.

1. **Inventory (8 min).** List every HUD element in the screenshot. For each one, place it in the Fagerholt and Lorentzon grid and estimate how often you would check it in a tense moment.
2. **Price it (10 min).** Pick the three most-checked elements. Measure their distance from the screen centre as a fraction of screen width and height. Compute θ for a 24-inch monitor at 60 cm and a 55-inch TV at 250 cm, then `T(θ)` and `E` for each.
3. **Fix one (7 min).** Propose one change that attacks `f`, and one that attacks θ. Compute both new values of `E`. Say which you would ship and what it costs (resolution, clutter, immersion, build time).

Expected output: an inventory table, three θ values per setup, two `E` values per element, and one recommendation with its cost.

## Common misconceptions

- **"Diegetic HUDs are better because they are immersive."** Placement and encoding decide cost, not fiction. A diegetic element far from the action costs as much as a corner bar. Dead Space's spine bar works because it sits near the crosshair and is readable as a shape.
- **"Moving an element closer always helps."** On this model, closer helps a little until the element is inside the reading radius, then it helps a lot. Moving from 24° to 12° buys about 2 points of look-away share.
- **"A minimal HUD is a lighter HUD."** Hiding information does not remove the need for it. It moves the cost into memory or into mistakes, unless another channel carries the information.
- **"Pixels are the unit of HUD layout."** The eye works in degrees. The same pixel offset is 24° at a desk and 14° on a couch. Lay out in fractions of the screen, then check in degrees for each target setup.

## Check yourself

1. A handheld with a 7-inch 16:9 screen (15.5 × 8.7 cm) is held 35 cm from the eyes. How far from the centre, in cm, can an element be and still sit inside the 2.5° reading radius? What fraction of the screen width is that?
2. A shooter shows ammunition as a number in the bottom-right corner (θ = 20° on the target PC setup). Players check it 6 times a minute in firefights. The team proposes a small ammo counter next to the crosshair at 1.5°. Compute `E` before and after. What does the new counter cost the player?
3. Classify each in the Fagerholt and Lorentzon grid: a floating name above an ally, a screen that turns grey as health falls, a map the character holds up in their hands, a quest log opened as a flat menu.
4. A mobile team says, "Our HUD is fine because nobody has complained." Using the inventory from section 4, describe a measurement that would test the claim.

<details>
<summary>Answers</summary>

1. `d = 35 × tan(2.5°) = 1.53 cm`. That is `1.53 / 15.5 ≈ 10%` of the screen width either side of the centre. On a small screen held close, the reading radius covers a much bigger share of the screen than on a TV.
2. Before: `T(20°) = 2 × (200 + 70) + 250 = 790 ms`, `E = 6 × 0.79 / 60 = 7.9%`. After: `T = 250 ms`, `E = 2.5%`. The cost is clutter and occlusion right where the player aims, and one more element in every visual search near the crosshair.
3. Floating name: spatial (in the 3D space, not in the fiction). Grey screen: meta, and outside the fiction on a strict reading. Fagerholt and Lorentzon call this kind "meta-perception". Map in hands: diegetic. Flat quest log: non-diegetic, unless the fiction says it is the character's journal, in which case it is meta. Note that the grey screen and the held map sit in different cells, yet both avoid a corner readout.
4. Record play sessions, count glances at each element (from eye-tracking if you have it, week 13, or from a think-aloud and video), and compute `f` and `E` per element. Then check for deaths or errors that happened during a look away. "No complaints" measures what players notice about the HUD, not what the HUD costs them.

</details>

## Lab hook

[Lab 10, HUD glance audit](../labs/lab10.md). You pick a shipped game, build its HUD inventory, measure element positions from screenshots, compute θ and look-away share for two screen setups, count real glances from recorded play, and propose a redesign with a predicted saving. Deliverable: the inventory, the calculation sheet and a two-page memo.

## Sources

- Wikipedia, "Dead Space (2008 video game)" (accessed September 2026). Released October 2008 (PS3 and Xbox 360 on 13 October in North America; PC on 20 October). Health and energy shown on the back of the suit; ammunition count appears when a weapon is raised; menus, map, inventory and video calls are holographic, in-world displays; time does not pause while browsing menus.
- Wikipedia, "HUD (video games)" (accessed September 2026). Dead Space's health along the spine is visible thanks to the third-person view; Red Dead Redemption 2 shows the minimap and horse stamina while riding and adds combat information in fights; Horizon Zero Dawn lets players set each element to always, when relevant, or never.
- Fagerholt, E. & Lorentzon, M. (2009). *Beyond the HUD: User Interfaces for Increased Player Immersion in FPS Games*. MSc thesis, Chalmers University of Technology, Göteborg (examiner Staffan Björk; tutor at EA DICE). Section 7: the diegesis and spatiality design space, its revision into fiction and spatiality, and the categories non-diegetic, meta-perception, meta-representation, geometric, diegetic and signifier; examples from Killzone 2, Mirror's Edge, Grand Theft Auto IV, Far Cry 2, Dead Space and Call of Juarez. http://publications.lib.chalmers.se/records/fulltext/111921.pdf
- Wikipedia, "Saccade" (accessed September 2026). Saccades last about 20-200 ms depending on amplitude; about 200 ms to initiate for unexpected stimuli; main-sequence examples of 300°/s at 10° and 500°/s at 30°; gaze shifts larger than about 20° are accompanied by a head movement.
- Wikipedia, "Eye movement in reading" (accessed September 2026). Average fixation 200-250 ms, range 100 to over 500 ms.
- Wikipedia, "Peripheral vision" (accessed September 2026). Fovea corresponds to about 5° of the visual field; acuity halves by 2° and falls to one sixteenth at 30°; peripheral vision is good at motion and weak at detail, colour and shape.
- Warcraft Wiki, "Edit Mode" (warcraft.wiki.gg, accessed September 2026). Added in patch 10.0.0, 25 October 2022; lets players rearrange the HUD from the default layout and share layouts.
- Warcraft Wiki, "Deadly Boss Mods" (warcraft.wiki.gg, accessed September 2026), as cited in UX201 week 2.
- Hodent, C. (2017). *The Gamer's Brain*. CRC Press. Chapters "Perception" and "Attention."
- The glance-cost model, the saccade fit `20 + 2.5θ` ms, `L = 200 ms`, `F = 250 ms`, `θ_f = 2.5°`, the 20 checks per minute and the boss-fight inventory are teaching assumptions, not measurements of any shipped game.

## Interactive spec: examples/w10-hud-glance-cost.html

**Purpose.** Show that the cost of a HUD check is dominated by whether the eye must move and how often, while the distance moved matters much less.

**The one insight the visual must make obvious.** Dragging the element from the corner toward the centre slides the cost down a gentle slope until it crosses the reading ring, where it drops off a cliff. Lowering checks per minute sinks the whole curve. Both effects are larger than any move that stays outside the ring.

**Layout.** Two linked views side by side at 1280px, stacked at 390px (screen view first). Controls below. A numbers panel under the controls.

- **Left, "What the eye sees".** A 16:9 rectangle for the chosen display. A crosshair at the centre. Two concentric circles centred on it: the reading radius (`θ_f`, default 2.5°) and the head-turn ring (20°), both converted to on-screen radius with `r = D × tan(θ)` scaled to the rectangle. If a ring is larger than the screen, clip it and label it "beyond screen edge". One draggable HUD element (a small generic bar, no game art). Show its θ next to it.
- **Right, "Share of the fight spent looking away".** x axis θ from 0° to 35°. y axis look-away share `E` from 0% to 40%. Plot `E(θ)` for the current `f`, as a line with the step at `θ_f`. Draw a dot at the element's current θ. Draw a faint second line for the design-E comparison (same θ curve at `f_peripheral`) when the "peripheral encoding" toggle is on. Shade θ > 20° lightly with a note "head turn not modelled; real cost higher".

**Controls.**

- Display: segmented PC (24 in, 60 cm), TV (55 in, 250 cm), Handheld (7 in, 35 cm), Custom. Custom exposes diagonal (5-100 in) and viewing distance (20-400 cm). All screens 16:9.
- Checks per minute `f`: slider 1-40, default 20.
- Peripheral encoding: toggle. When on, a second slider "checks per minute with peripheral cue" 1-40, default 4, and the dot follows that line.
- Saccade latency `L`: slider 50-300 ms, step 10, default 200.
- Reading fixation `F`: slider 100-500 ms, step 10, default 250.
- Reading radius `θ_f`: slider 1-5°, step 0.5, default 2.5.
- Preset positions buttons: "Corner (A)", "Near character 5° (C)", "At crosshair 2° (D)". Keyboard users can move the element with arrow keys (1% of screen width per press, 5% with Shift).
- Reset.

**Formulas.**

- Screen width `W = diag × 2.54 × 16/√337`, height `H = diag × 2.54 × 9/√337` (cm).
- Element offset from centre `(x, y)` in cm; `d = √(x² + y²)`; `θ = atan(d / D)` in degrees.
- `s(θ) = 20 + 2.5θ` ms. `T = F` if `θ ≤ θ_f`, else `T = 2(L + s(θ)) + F`.
- `E = f × T / 60000`.

**Numbers panel.** θ, T (ms), E (%) for the current element, plus a mini-table of the five designs from the lecture recomputed with current slider values.

**Test values** (defaults `L = 200`, `F = 250`, `θ_f = 2.5`, `f = 20`).

| Case | θ | T (ms) | E |
|---|---|---|---|
| PC, element at (−23.57, +11.94) cm, the exact 3 cm inset | 23.76° | 808.8 | 27.0% |
| TV, element at (−54.00, +27.37) cm, same fraction of the screen | 13.61° | 758.1 | 25.3% |
| θ = 5° | 5 | 715.0 | 23.8% |
| θ = 2° | 2 | 250 | 8.3% |
| PC corner, `f = 4` | 23.76° | 808.8 | 5.4% |
| θ = 3° | 3 | 705 | 23.5% |
| PC corner with `L = 100` | 23.76° | 608.8 | 20.3% |

- Handheld 7 in at 35 cm: reading radius on screen `35 × tan 2.5° = 1.53 cm`.
- Use the unrounded inset coordinates. Rounding them to (−23.6, +12.0) gives `d = 26.48` cm and θ = 23.81°, not 23.76°. The lecture's table rounds θ to 23.8° either way, and `T` changes by less than 0.3 ms.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. The two rings differ by dash pattern as well as colour. Values printed as text next to every visual. All controls keyboard operable with visible focus. Respect `prefers-reduced-motion` (no animated transitions when set). No game art, logos or screenshots; the HUD element is a plain bar labelled "health".
