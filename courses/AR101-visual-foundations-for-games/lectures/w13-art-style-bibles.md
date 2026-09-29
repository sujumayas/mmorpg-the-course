# AR101 · Week 13 — Art Style Bibles

**Why this matters:** A game's look is made by dozens of people over years, and in an MMO it may be extended by artists who join long after launch. A style bible is the document that lets a stranger make an asset that fits. If its rules can't be checked, every new artist adds a little drift, and after a few patches the world stops looking like one place.

**You will be able to:**
- Compute texel density for 2D and 3D assets and flag the ones that break a bible's target.
- Rewrite a vague style rule ("keep it painterly") as a checkable rule with a property, a target, a tolerance and a measurement method.
- Critique a published style guide (Team Fortress 2, Shovel Knight) by sorting its rules into hard, soft and exception.
- Design a one-page bible for a small MMO zone and run a stranger test on it.

**Before class:** Mitchell, Francke and Eng, "Illustrative Rendering in Team Fortress 2" (NPAR 2007), sections 1 to 4 (about three pages, skip the shader maths in section 5). David D'Angelo, "Breaking the NES for Shovel Knight" (Game Developer, 2014), the sections on resolution and color palette. Solarski, *Drawing Basics and Video Game Art* (2012), the material on art style and consistency that you find most useful for your style bible (use the table of contents).

**Prerequisites from earlier courses:** None outside AR101. This week pulls together the course so far. [Value (week 1)](w01-seeing-like-an-artist-value-before-color.md), [shape language (week 2)](w02-shape-language-circles-squares-triangles.md), [silhouettes (week 3)](w03-silhouette-readability.md), [color (week 4)](w04-color-theory-hue-saturation-value.md), [palettes (week 5)](w05-palettes-and-color-harmony.md) and [pixel art (week 6)](w06-pixel-art-fundamentals.md) each become a chapter of the bible.

**Interactive:** [examples/w13-texel-density.html](../examples/w13-texel-density.html). Keep it open during section 2.

---

## 1. What a style bible is for

A **style bible** (also called an art bible or style guide) is the written and illustrated reference that defines how a game looks. It answers the questions an artist asks before starting an asset. How big are heads relative to bodies? How dark can a shadow get? How many colors may a prop use? How sharp is a texture allowed to be?

Think about who reads it:

- **A new hire in week one.** They have talent but no memory of the hundred decisions the team made last year.
- **An outsourcing studio.** Large games send props, characters and environments to external vendors. The vendor sees the bible and a few reference files, never the meetings.
- **Community creators.** Some games accept player-made items. Those artists get only the public guidelines.
- **Your own team, three years later.** In a live MMO, the art team that ships the fifth expansion is partly different people from the team that shipped launch. The bible is how the world stays one world.

Each of these readers has one thing in common. They cannot ask you. So a bible is judged by one test. **Can someone who never talked to the team make an asset that fits, using only the bible?** This course calls that the *stranger test*, and you'll run it in the lab.

### The usual chapters

Most bibles have the same bones. You already have the material for most of them from earlier weeks.

1. **Pillars.** Three to five words that name the look, each paired with what it is *not*. "Chunky, not cute. Worn, not dirty. Warm, not orange." The "not" half does more work than the first half, because it rules things out.
2. **Shape language and proportions.** Which base shapes belong to which factions or roles (week 2), head-to-body ratios, how exaggerated hands and feet are.
3. **Silhouette rules.** The minimum readability test for characters and interactables (week 3).
4. **Value and color.** Value ranges for characters versus backgrounds (week 1), the palette and its ramps (weeks 4 and 5), and colors reserved for gameplay meaning.
5. **Lighting and rendering.** Light direction, shadow color, outline or no outline, rim lights.
6. **Materials and detail.** How much surface noise is allowed, how metal differs from wood, the scale of brush strokes or pixel clusters.
7. **Technical rules.** Texel density, texture sizes, polygon or sprite budgets, pixel scale. This is where art meets the pipeline, and it's the subject of next week.
8. **Examples.** Approved assets, rejected assets and the reason each was rejected.

This lecture spends most of its time on chapter 7 and on how to write rules for all the others. The reason is simple. Rules about numbers are the ones strangers can follow without guessing.

## 2. Worked example: texel density, the rule nobody sees until it breaks

### The hook

Valve adds cosmetic items made by players to Team Fortress 2 through the Steam Workshop, and splits the store revenue with their creators. Valve's public Workshop FAQ gives outside artists a short list of technical guidelines. Hats should stay under 1,000 polygons and weapons under 6,500. Textures should not be larger than 512×512, and for hats 256×256 is usually enough. Then comes a rule that sounds odd at first. Keep the same texture density as the models around your item, with nothing higher resolution or lower resolution than what sits next to it.

Why would Valve turn away a *sharper* hat? More detail sounds like a better hat. The answer is that a hat is never seen alone. It sits on a head whose texture was painted at one density, next to a weapon painted at the same density. A hat four times sharper than the face under it looks pasted on, the way a photo cut-out looks in a painted scene. Sharpness is a style property, and the bible has to control it like color.

### The model

**Texel density** is how many texture pixels (texels) cover one unit of world size. For one direction across an asset:

```
D = T × f × r / S
```

- `D` is the texel density, in texels per meter (or per tile, in a 2D game).
- `T` is the texture's side length in texels, for example 512.
- `f` is the fraction of the texture's width that the asset's UV map uses for this face, between 0 and 1. A **UV map** is the flat layout that tells the engine which part of the texture lands on which part of the model.
- `r` is how many times the texture repeats across the face (1 if it doesn't tile).
- `S` is the world size of the face in meters (or tiles).

The bible sets a target `D*` and a tolerance. An asset passes when its ratio `D / D*` falls inside the tolerance band.

On screen, what the player sees is the size of one texel. If the camera shows `p` screen pixels per meter at some distance, each texel covers `p / D` screen pixels. Two assets at the same distance have texels whose sizes differ by the ratio of their densities. That ratio is what the eye catches. A face at twice the density looks twice as crisp as its neighbor, and the mismatch reads as "this came from a different game."

### Numbers you can check

Take an invented MMO zone, Saltmarsh Reach. Its bible sets `D* = 128` texels per meter with a tolerance of ±25%, so anything from 96 to 160 passes. Five assets arrive from three artists:

| Asset | World width S (m) | Texture T (px) | UV fraction f | Repeats r | D (px/m) | D / D* | Verdict |
|---|---|---|---|---|---|---|---|
| Stone wall | 4 | 512 | 1.00 | 1 | 128 | 1.00 | pass |
| Barrel | 1 | 256 | 0.50 | 1 | 128 | 1.00 | pass |
| Lantern | 0.25 | 256 | 0.50 | 1 | 512 | 4.00 | fail, 4× too sharp |
| Cliff face | 16 | 1024 | 1.00 | 1 | 64 | 0.50 | fail, 2× too blurry |
| Market tent | 6 | 1024 | 0.75 | 1 | 128 | 1.00 | pass |

Check the lantern by hand. Half of a 256-texel texture is 128 texels, spread across a quarter of a meter, so `128 / 0.25 = 512`. The artist gave a small prop a whole texture and used half of it. It looks lovely in the modeling program, where it fills the screen. In the game it sits on a table next to the barrel, and each of its texels is a quarter the size of the barrel's.

The same check as a script, which you can run with `.venv/bin/python`:

```python
TARGET, TOL = 128, 0.25          # px per meter, plus or minus 25%

assets = [  # name, world width S (m), texture side T (px), UV fraction f, repeats r
    ("stone wall",  4.0,  512, 1.00, 1),
    ("barrel",      1.0,  256, 0.50, 1),
    ("lantern",     0.25, 256, 0.50, 1),
    ("cliff face", 16.0, 1024, 1.00, 1),
    ("market tent", 6.0, 1024, 0.75, 1),
]

for name, S, T, f, r in assets:
    D = T * f * r / S
    ratio = D / TARGET
    ok = (1 - TOL) <= ratio <= (1 + TOL)
    print(f"{name:12} D = {D:6.1f} px/m  ratio {ratio:4.2f}  {'pass' if ok else 'FAIL'}")
```

It prints:

```
stone wall   D =  128.0 px/m  ratio 1.00  pass
barrel       D =  128.0 px/m  ratio 1.00  pass
lantern      D =  512.0 px/m  ratio 4.00  FAIL
cliff face   D =   64.0 px/m  ratio 0.50  FAIL
market tent  D =  128.0 px/m  ratio 1.00  pass
```

Five lines of code replace an argument between two artists about whether the lantern "looks a bit crisp." Keep a script like this next to the bible and run it on every submission.

The fixes use the same formula:

- **Lantern.** Move it onto a shared prop sheet with other small items so its UV island is 32 texels wide. Then `D = 32 / 0.25 = 128`. The texture budget freed up goes to other props.
- **Cliff face.** Keep the 1024 texture and tile it twice across the 16 meters. Then `D = 1024 × 2 / 16 = 128`. Tiling costs no extra memory, and it's why large terrain in most games repeats. The art problem then becomes hiding the repeat, which is [week 7's](w07-tilesets-and-seamless-tiling.md) subject.

Open [the interactive](../examples/w13-texel-density.html). Select the lantern and drag its texture size down. Its checker pattern shrinks toward the barrel's while its bar on the right moves into the green band. The two views tell the same story in two ways. The scene shows the clash, and the bar chart names the number.

### The 2D form

In a 2D game the "meter" is usually a tile, and the texel is a pixel of art. If tiles are 16 pixels wide, `D = 16` pixels per tile. The rule becomes stricter, because pixel art only looks right when every art pixel is the same size on screen. If the engine scales one sprite by a factor `k`, its density becomes `D / k`. A 16-pixel-per-tile character scaled by 1.5 "to read better" drops to about 10.7 pixels per tile, and its art pixels are 1.5 times the size of the tiles' pixels. Pixel artists call these mismatched pixels *mixels* (week 6). A pixel-art bible sets the tolerance to zero. Every sprite has `k = 1`, and anything that needs to be bigger is redrawn bigger.

### Cross-game recognition

**Minecraft (Java Edition).** A block is one meter on a side, and most block textures are 16×16 pixels. That makes the whole world `D = 16` pixels per meter. Resource packs can replace textures at 32×32, 64×64 and up, and the wiki notes that a pack may mix resolutions. Put a 32-pixel stone next to a 16-pixel dirt block and you have a 2× density clash, the same failure as the Saltmarsh cliff, in a game where you can count the pixels.

**Shovel Knight (Yacht Club Games, 2014).** The developers set a virtual resolution of 400×240, with background tiles of 16×16 like most NES games. At 1080p each art pixel is drawn 4.5 screen pixels wide, because 1080 / 240 = 4.5. Every sprite and tile obeys the same scale. Density is fixed at 16 pixels per tile for the whole game, and the art pixel is one size everywhere on screen.

**Stardew Valley (1.6 era).** The modding documentation says map tiles are 16×16 pixel squares and that the tile size should always be 16. That's a texel-density rule written for strangers, the modders, in exactly the TF2 spirit.

**Team Fortress 2.** Back to the hook, now in the model's form. Valve does not publish a number for `D*`. Its rule is relative. Match what's next to it, with texture size caps of 512 and 256 that stop the worst violations. That's a tolerance band defined by the neighbors rather than a fixed target.

Four games, one idea. Whether the unit is meters, tiles or "the hat's head," the bible fixes how many texels cover a unit of world, and anything off that number looks foreign.

### Eyes-open design judgment

Texel density is a rule you should set deliberately, and it has costs.

- **It's the cheapest consistency rule to check.** Two numbers from the file and one from the level give a pass or fail. Put it in every bible that has more than one artist.
- **Uniform is not always right.** Players look at some things from a hand's length and others from a hundred meters. Many 3D teams allow a higher density for first-person weapons, character faces and UI portraits, and a lower one for distant terrain. If you do that, write the exceptions as named tiers ("hero props 2× D*") so they are decisions, not accidents.
- **It fights memory.** A higher `D*` means larger textures for every asset. Next week you'll price that in kilobytes. The target should come from the camera distance and the memory budget together, not from how good a close-up screenshot looks.
- **Tolerance is a judgment.** ±25% is invisible to most players in a 3D game. In pixel art, even 1.5× is glaring. Choose the band from the style, and test it by putting a passing and a failing asset side by side.
- **The worst violations are the pretty ones.** The lantern was the best-looking asset in isolation. A bible review has to happen in the scene, next to neighbors, at game camera distance.

## 3. Writing rules strangers can follow

Texel density is easy because it's already a number. Most of a bible is about things that feel harder to measure, like mood, detail and color. The skill this section teaches is turning those into rules someone else can check.

### The anatomy of a checkable rule

A checkable rule has four parts:

| Part | Question it answers | Example |
|---|---|---|
| Property | What do I measure? | Value (lightness) of a character's darkest large area |
| Target | What number or range is allowed? | Not below 15% |
| Tolerance and scope | Where, and how strict? | All playable characters, in-game lighting, areas bigger than the palm |
| Method | How do I measure it? | Screenshot at default camera, convert to grayscale, eyedropper the largest dark area |

And one optional part that bibles leave out too often. **Why.** "Because full black reads as a hole in the scene and hides the silhouette at night." A rule with a reason gets followed in spirit when the letter doesn't cover a case.

Compare three versions of the same rule:

1. "Keep it painterly." Two artists will disagree about what this allows.
2. "Avoid fine surface detail." Better. It names the property but not a limit.
3. "No texture detail smaller than 4 texels at `D*`. No photo-sourced texture without an overpaint pass. Test by viewing the asset at game distance and checking that every visible mark is a deliberate brush stroke." Now two reviewers agree.

The last version is longer, and that's fine. Bibles get read slowly by people who want to get it right.

### Reading Team Fortress 2 as a bible

Valve's 2007 paper on Team Fortress 2 is one of the few detailed art-direction documents a studio has published. It reads like a bible with the reasons left in. Here is what it says, paraphrased, and how each rule sorts.

- **Source of the look.** The style draws on early-to-mid 20th century commercial illustrators J. C. Leyendecker, Dean Cornwell and Norman Rockwell. That's a pillar, not a rule. It tells an artist where to look for reference.
- **Shading shifts from warm to cool, and shadows go cool rather than black.** Checkable. Sample a shadow and a lit area and compare hues.
- **Saturation rises near the terminator, the line where light turns to shadow, which is often reddened.** Checkable, with a method.
- **The nine classes have distinct silhouettes, and the team validated this during concept by viewing them in pure silhouette.** A silhouette test rule, exactly week 3's method.
- **Interior details such as clothing folds echo the silhouette shapes.** Shape language (week 2), checkable by overlaying fold lines on the outline.
- **High-frequency detail is left out where possible, and silhouettes are picked out with rim highlights rather than dark outlines.** Two rendering rules.
- **The red team's buildings use warm colors, natural materials and angular forms. The blue team's use cool colors, industrial materials and orthogonal forms.** A faction contrast rule written as three paired properties. You could hand this to a stranger.
- **Colors sit near realism but with more saturation and value contrast, with muted colors dominant and small areas of saturation.** A palette rule that names a ratio without giving a number. A stricter bible would say what fraction of an image may be highly saturated.

Now look at the Workshop FAQ, which is the version written for strangers. Valve describes the target as an idealized 1950s to 60s Americana look, neither hyper-realistic nor overly cartoony. It asks for flat colors near the base game's color family, avoiding pure black, pure white and fully saturated colors, with a subtle vertical gradient and a subtle ambient-occlusion layer on top. It also says items that obscure class silhouettes tend to be rejected. And then it says something every bible should say. Apart from the no-go areas, such as obscenity and copyright, these are guidelines rather than hard rules, and an item that breaks one may still be picked.

That gives you three categories:

- **Hard rules.** Break one and the asset is rejected, no discussion. In TF2 these are legal and technical (copyright, the texture cap) and gameplay-critical (don't hide the class silhouette).
- **Soft rules.** The default. Break one and you need a reason that a reviewer accepts.
- **Recorded exceptions.** A soft rule broken on purpose, written down with the reason so the next artist knows it was deliberate.

Your bible should label each rule with its category. Gameplay rules (team colors, silhouettes, telegraph colors) are almost always hard. Taste rules are soft.

### Shovel Knight, a bible built from a constraint with its exceptions written down

Shovel Knight's art team started from a ready-made rulebook, the NES hardware. The NES could output 54 colors, a fixed tile grid and a small screen. The team then decided which constraints to keep and which to break, and they wrote the breaks down publicly.

They kept the 16×16 tile size and the vertical resolution of 240 lines. They broke the 256-pixel width to fill a 16:9 screen, giving 400×240. They kept the NES palette because it gives the game a distinctive look, but found it had no useful yellow and too few dark shades. So they added a handful of colors, and they named at least one of them by hex value, a dark purple (#22123B) used in one stage and then reused elsewhere as a bridge between colors.

That's the pattern of a well-run bible. Start from a clear rule set. Break it only where the rule costs you something you need. Record every break, with the value and the reason, so the exception doesn't quietly become "anything goes."

### Tools that make rules checkable

A few habits turn soft rules into things you can test in minutes:

- **Grayscale checks.** Convert a screenshot to grayscale to test value rules (week 1).
- **Silhouette fills.** Fill every character with black against a light background (week 3).
- **Palette locks.** Keep the approved palette as a swatch file. Pixel artists can lock the palette so off-palette colors are impossible (week 5).
- **Lineups.** Keep a "canon lineup" image with every approved character or prop at the same scale. Every new asset gets dropped into the lineup before review. Most drift is invisible alone and obvious in a lineup.
- **Density checkers.** Most 3D tools can overlay a checker texture at the target density. Every asset should show squares the same size as its neighbors'. The interactive uses exactly this view.

## 4. Bibles in a live game

A single-player game ships and its bible can retire. An MMO's bible has to live as long as the game. Three practices keep it useful.

**Version it like code.** Give the bible a version number and a changelog. When a rule changes, say which assets it affects and whether old assets will be updated or left alone. "Shadow floor raised from 10% to 15% value in v2.3. Launch zones not repainted, all new zones must comply." Without this, reviewers argue over which rule applies.

**Let it evolve on purpose.** Valve's FAQ admits the art style has evolved over the years. That's normal. What you want to avoid is evolution by accident, where each expansion drifts a little and nobody decided it. Schedule a review of the bible with each major content release. Compare a screenshot from launch and one from the current build side by side, and decide whether each difference was intended.

**Separate the world bible from the zone bible.** A zone may have its own palette and mood, a desert zone with warmer light, a haunted zone with a colder palette. The world-level rules (texel density, silhouette tests, gameplay colors, UI) stay fixed across all zones. The zone-level rules sit on top. This two-level structure is how a big world gets variety without losing identity. Gameplay colors are the most important thing to hold fixed. If red means "enemy spell area" in one zone, it cannot mean "decoration" in the next.

## 5. Running a stranger test

You can't know if a bible works by rereading it, because you already know what you meant. Test it the way you'd test a game, with someone who wasn't there.

1. **Pick a brief.** "A market-stall prop for Saltmarsh Reach" or "a hat for the Tinker class."
2. **Hand over the bible and nothing else.** No conversation, no pointing at your sketches.
3. **Let them make it.** Time-box it to the size of the asset.
4. **Audit it against the rules.** Go rule by rule and mark pass, fail or "rule unclear." Do this before you look at it in the lineup, so the gut reaction doesn't override the checklist.
5. **Then look at it in the lineup.** Does it fit? If it passes every rule but still looks wrong, your bible is missing a rule. Find the property that differs and write the rule.
6. **Revise the bible, not the asset.** The artist did what the document said. Every "rule unclear" and every "passes but looks wrong" is a defect in the bible.

The output of a stranger test is a list of bible defects. Two or three rounds usually shrink that list to nothing important.

## In-class activity (25 minutes)

In groups of three, write the technical and color chapters of a bible for a small invented MMO zone, then attack another group's.

1. **Write (10 min).** Pick a zone concept and write six rules. At least one must be texel density with a target and tolerance, at least two must be value or color rules with numbers, and each rule must be labelled hard or soft. Use the four-part anatomy.
2. **Swap (5 min).** Give your six rules to another group.
3. **Attack (10 min).** For each rule you received, describe an asset that obeys it to the letter and still clearly doesn't fit the zone. Write that asset down in one sentence. For the density rule, give its `T`, `f`, `r` and `S`.

Expected output is six rules, plus the list of loopholes the other group found. The rules with the fewest loopholes are the ones that name a property and a method.

## Common misconceptions

- **"More texture resolution is always better."** Only if its neighbors get it too. A single asset at 4× density looks pasted in. Density is a consistency rule first and a quality setting second.
- **"A style bible is a mood board."** A mood board shows the feeling. A bible has to let a stranger reproduce it, which needs rules with targets and methods. Keep the mood board as the first page, not the whole document.
- **"If the rules are strict, the art will be boring."** Strict technical and gameplay rules usually free artists, because they stop arguing about what's allowed. Variety comes from the soft rules and from zone-level bibles.
- **"Guidelines that allow exceptions are useless."** Exceptions are fine if they're recorded with a reason. Shovel Knight's extra colors are exceptions, written down with hex values.

## Check yourself

1. A bible targets `D* = 256` px/m with ±25% tolerance. An artist maps a 2-meter door so it uses 60% of the width of a 1024 texture, with no tiling. Does it pass? If not, what texture size (keeping `f = 0.6`) would put it closest to the target?
2. A floor is 12 meters wide. The bible's density is 128 px/m. You have a 512 texture that tiles. How many repeats do you need across the floor?
3. A pixel-art game uses 16-pixel tiles. A designer asks for the boss sprite, drawn at 16 px per tile, to be scaled up by 2 to look bigger. What happens to its density, and what should the bible say instead?
4. Rewrite "shadows shouldn't be too dark" as a checkable rule with all four parts.
5. In a Minecraft resource pack, the stone texture is 64×64 and the dirt texture is 16×16. At the same distance, how many times wider is a dirt texel than a stone texel on screen?

<details>
<summary>Answers</summary>

1. `D = 1024 × 0.6 / 2 = 307.2` px/m. The ratio is 1.2, inside ±25%, so it passes. A 512 texture would give `512 × 0.6 / 2 = 153.6`, ratio 0.6, which fails, so 1024 is already the closest size. If the lead wants it exact, reduce `f` to 0.5, which gives exactly 256.
2. `128 = 512 × r / 12`, so `r = 3`. Three repeats across the floor.
3. Density drops from 16 to 8 pixels per tile, so each boss art pixel is twice as wide as a tile pixel on screen. The bible should require `k = 1` for all sprites and say that anything that must be bigger is redrawn at the larger size in native pixels.
4. One good answer. Property is the value (lightness) of the darkest area larger than a fingertip on screen. Target is not below 15%. Scope is all characters and props under default in-game lighting. Method is a grayscale screenshot at default camera, sampled with an eyedropper. Why is that darker areas read as holes and hide silhouettes at night.
5. Both blocks are one meter. Stone is 64 px/m, dirt is 16 px/m. Texel size on screen is `p / D`, so a dirt texel is 64/16 = 4 times wider.

</details>

## Lab / assignment hook

[Lab 13, the one-page style bible and stranger test](../labs/lab13.md). You write a bible for an invented MMO zone with at least eight rules, compute a density table for six assets, make three assets that pass, and run a stranger test with a partner. This lab is the first draft of the style bible assessment (20% of the course grade).

## Sources

- Valve, "Team Fortress 2 Workshop" FAQ, teamfortress.com/workshop (page as retrieved 29 September 2026). Hat and weapon polygon guidelines (under 1,000 and 6,500), texture cap 512×512 and 256×256 usually enough for hats, the rule to keep texture density matched to neighboring models, the 1950s to 60s Americana description, flat colors avoiding pure black, pure white and full saturation, the vertical gradient and ambient-occlusion layer, rejection for obscured silhouettes, and the statement that most items are judged by guidelines rather than hard rules.
- Mitchell, J., Francke, M. and Eng, D. (2007). "Illustrative Rendering in Team Fortress 2." *Proceedings of NPAR 2007*, Valve. The Leyendecker, Cornwell and Rockwell influence, warm-to-cool shading, reddened terminator, distinct silhouettes validated in concept, folds echoing silhouettes, rim highlights instead of outlines, red and blue base properties, increased saturation and value contrast with muted colors dominant.
- D'Angelo, D. (2014). "Breaking the NES for Shovel Knight." Game Developer (formerly Gamasutra), 25 June 2014. Virtual resolution 400×240, each art pixel 4.5 screen pixels at 1080p, 16×16 background tiles, NES output of 54 colors, the added dark purple #22123B. https://www.gamedeveloper.com/design/breaking-the-nes-for-shovel-knight
- Minecraft Wiki, "Block" (current Java Edition). Blocks occupy one cubic meter; most block textures are 16×16 pixels.
- Minecraft Wiki, "Texture pack" (history through Java Edition 1.5). Default textures 16×16; higher resolutions called HD; resolutions can be mixed within one pack.
- Stardew Valley Wiki, "Modding:Maps" (game version 1.6 era). Tiles are 16×16 pixel squares; tile size should always be 16.
- Solarski, C. (2012). *Drawing Basics and Video Game Art*. Watson-Guptill.

## Interactive spec: examples/w13-texel-density.html

**The one insight.** An asset can look fine alone and still clash in the scene, and texel density names the clash with one number. The picture on the left shows the clash, the bar chart on the right shows the number, and they move together.

**Layout.** Two linked views side by side on desktop, stacked on mobile (scene on top).

- **Left, "In the scene."** A flat front-on scene at a fixed camera, drawn with plain shapes. Five invented assets from the lecture table stand on a ground line at their relative world widths: stone wall (4 m), barrel (1 m), lantern (0.25 m, sitting on top of the barrel), cliff face (16 m, drawn as a backdrop band, cropped to the view), market tent (6 m). Each asset's shape is filled with a two-tone checker pattern where one checker square equals 8 texels. So the on-screen square width is `8 × p / D` where `p` is screen pixels per meter (fixed so the 16 m view fits the panel width). The asset colors are muted and distinct (use palette tokens), so the checker size is what changes, not the hue. Render with nearest-neighbour so checkers stay crisp.
- **Right, "Density vs the bible."** A horizontal bar per asset showing `D` on a log2 axis from 16 to 1024 px/m, with a vertical line at `D*` and a shaded band from `D*(1 − tol)` to `D*(1 + tol)`. Bars inside the band use the "ok" token, outside use the "warn" token. Next to each bar print `D` to one decimal and the ratio `D/D*` to two decimals, plus "pass" or "FAIL".

**Controls.**

- Asset selector (radio group or tabs, keyboard accessible), default "lantern".
- For the selected asset: texture size `T` (select: 64, 128, 256, 512, 1024, 2048), UV fraction `f` (slider 0.05 to 1.00, step 0.05), repeats `r` (stepper 1 to 8), world width `S` (read-only, shown).
- Bible target `D*` (select: 64, 128, 256, 512; default 128) and tolerance (slider 0% to 50%, step 5%, default 25%).
- "2D mode" toggle. Relabels units to px per tile, sets `D* = 16`, tolerance 0 and replaces the five assets with a 1-tile grass block, a 1-tile crate, a 2-tile hero sprite with a scale factor `k` slider (0.5 to 3, step 0.25) instead of `T/f/r`. Density is `16 / k`. In 2D mode one checker square is 2 art pixels instead of 8 texels, so a 16-pixel tile shows 8 squares across and the view is 10 tiles wide. When `k ≠ 1` the hero's checker squares visibly differ from the tiles'.
- "Reset to lecture table" button.

**Formulas.** `D = T × f × r / S`. Pass when `(1 − tol) ≤ D/D* ≤ (1 + tol)` (inclusive). Checker square on screen `= 8 × p / D`.

**Test values (default state must match the lecture table exactly).**

| Asset | S | T | f | r | D | D/D* at D*=128 | Verdict at ±25% |
|---|---|---|---|---|---|---|---|
| Stone wall | 4 | 512 | 1.00 | 1 | 128.0 | 1.00 | pass |
| Barrel | 1 | 256 | 0.50 | 1 | 128.0 | 1.00 | pass |
| Lantern | 0.25 | 256 | 0.50 | 1 | 512.0 | 4.00 | FAIL |
| Cliff face | 16 | 1024 | 1.00 | 1 | 64.0 | 0.50 | FAIL |
| Market tent | 6 | 1024 | 0.75 | 1 | 128.0 | 1.00 | pass |

Fix checks. Lantern with `T = 64`, `f = 0.50` gives `D = 128.0`, pass. Cliff with `r = 2` gives `D = 128.0`, pass. In 2D mode, hero `k = 1.5` gives `D = 10.7`, ratio 0.67, FAIL.

**First screen.** Default state with the lantern selected and FAIL visible, so the student sees the tiny-checker lantern on the big-checker barrel before touching anything.

**Constraints.** Self-contained HTML, palette tokens from `templates/interactive-tokens.css` inline, no game art, keyboard operable, `prefers-reduced-motion` respected (no animated transitions when set), light and dark themes, no horizontal overflow at 390 px.
