# AR101 · Week 11 — UI Visual Hierarchy

**Why this matters:** Every screen of UI makes a claim about what matters most, whether you planned it or not. The player's eye goes to the heaviest thing first, and if the heaviest thing is the wrong thing, no amount of good writing or clever icons will fix it. This week you learn to measure that claim and bend it to your intent.

**You will be able to:**
- Compute the visual weight of UI elements from their area and value contrast, and rank them.
- Count the inversions between the order you intend and the order the eye will follow.
- Design a four-tier label system in which each tier outweighs the one below by a clear step.
- Critique a shipped interface by separating what its colors name (category) from what its weights rank (importance).

**Before class:** Solarski, *Drawing Basics and Video Game Art* (2012), the material on value and on composition, focal points and contrast (find it through the table of contents). Brown, T. (2011), "More Meaningful Typography", *A List Apart*, the section on modular scales.

**Prerequisites from earlier courses:** None outside AR101. You need value as CIE L* and the value gap ΔV with its threshold of 20 from [AR101 week 1](w01-seeing-like-an-artist-value-before-color.md), the idea that hue and value are separate from AR101 week 4 ([color theory, hue, saturation, value](w04-color-theory-hue-saturation-value.md)), and the local contrast `C` and hierarchy ratio `H` from [AR101 week 9, composition and leading the eye](w09-composition-and-leading-the-eye.md). Later, [UX201 week 10, HUD and information design](../../UX201-game-ux-and-player-psychology/lectures/w10-hud-and-information-design.md) prices each glance at the HUD in time, and [UX201 week 1](../../UX201-game-ux-and-player-psychology/lectures/w01-perception-attention-memory.md) explains the pop-out effect that makes a heavy element win.

**Interactive:** [`examples/w11-squint-hierarchy.html`](../examples/w11-squint-hierarchy.html). Keep it open during section 2.

---

## 1. What hierarchy is

**Visual hierarchy** is the order in which a viewer's eye visits the parts of a layout. A good hierarchy matches the order of importance: the thing the player most needs is seen first, the next thing second, and the background detail last or never.

You already know the idea from painting. In week 9 you found a scene's focal point by its local value contrast and led the eye to it with lines and framing. A UI panel is a composition too, only it is small, crowded with text, and read under time pressure. An item tooltip might have eight lines. A raid frame has twenty health bars. A quest log has a title, objectives, a map pin and a reward list. In each case the artist decides, on purpose or by accident, what the eye hits first.

Hierarchy is built from a few channels.

- **Size.** Bigger elements take more of the visual field.
- **Value contrast.** An element far from its background in value stands out. Week 1 showed this is the strongest single channel.
- **Position.** In left-to-right languages, readers start at the top left. The top line of a panel is read before the bottom line.
- **Grouping.** Elements close together and aligned read as one unit (the Gestalt principle of proximity).
- **Hue and saturation.** A saturated color in a gray field pops (week 4, section 3). Hue is also the easiest channel to give a name ("green means uncommon").
- **Motion.** A pulse or shimmer draws the eye before anything static (week 10).

The last two are strong but tricky. Hue is great at saying what kind of thing something is. It is poor at saying how much of it there is, or how important it is. That difference is the subject of this week's worked example.

## 2. Worked example: the epic that whispers

### The hook

World of Warcraft colors item names by quality. From lowest to highest, the tiers players hunt for are Poor (gray), Common (white), Uncommon (green), Rare (blue), Epic (purple) and Legendary (orange). The game's own color codes, as documented by the Warcraft Wiki, are `#9d9d9d`, `#ffffff`, `#1eff00`, `#0070dd`, `#a335ee` and `#ff8000`. Players learn this code within hours. "Purple" is shorthand for a great item.

Now convert those six colors to value. The Epic purple, one of the most wanted rewards in the game, is darker than the Poor gray you sell to a vendor for pocket change. On a dark tooltip, the eye goes to the white and green names first and the purple one last. The game's color code ranks items one way. The eye ranks them almost the other way. You can put a number on how far apart they are.

### The model

Give each element on screen a **visual weight**:

```
W = A × ΔV

A  = area, in units of one line of body text   (text of the same length: A = s²)
s  = text size relative to body text           (body text: s = 1)
ΔV = |L*(element) − L*(what is behind it)|     (value contrast, 0 to 100)
```

An element that is twice as big with the same contrast has twice the weight. An element with twice the contrast at the same size also has twice the weight. For a label with a filled plate behind its text, add the parts: the plate's weight against the world, plus the text's weight against the plate.

Then check the hierarchy with two rules.

1. **Order rule.** List the elements from least to most important. An **inversion** is any pair where the less important element has the larger weight. Count them. Zero inversions means the eye's order matches yours. For `n` elements there are `n(n − 1)/2` pairs, so a random layout gets about half of them wrong.
2. **Step rule.** Each level should outweigh the level below it by a factor of at least 1.5. If two levels are closer than that, they tend to read as one level in a squint test. This is week 9's hierarchy ratio `H ≥ 1.5` applied down a whole ladder of levels instead of only between the focal point and its rival. Like week 9's threshold, it is a working rule for this course, not a law of perception. Use it as a starting point and check it with the squint test on real screens.

Why a product of area and contrast? It is the simplest formula that behaves like the squint test. Blur a layout and every element becomes a soft blob whose darkness or lightness against the background depends on its contrast, and whose size depends on its area. The biggest, most contrasting blobs are what survive the blur. Research saliency models, such as the one by Itti, Koch and Niebur (1998), combine contrast in intensity, color and orientation across several scales. Week 9's local contrast `C` kept one of those features, value, on a fixed grid. Our weight keeps value and adds area, because UI elements come in very different sizes, and size is the channel a UI artist changes most often.

### Numbers you can check

Put the six quality colors on a black background at the same text size. Then `A = 1` and ΔV is simply each color's L*, which you compute with the week 1 formula.

| Tier (least to most wanted) | Color | L* | Weight W on black |
|---|---|---|---|
| Poor | #9d9d9d | 64.7 | 64.7 |
| Common | #ffffff | 100.0 | 100.0 |
| Uncommon | #1eff00 | 87.9 | 87.9 |
| Rare | #0070dd | 48.0 | 48.0 |
| Epic | #a335ee | 47.6 | 47.6 |
| Legendary | #ff8000 | 67.1 | 67.1 |

Count inversions. Poor outweighs Rare and Epic (2). Common outweighs the four tiers above it (4). Uncommon outweighs Rare, Epic and Legendary (3). Rare outweighs Epic by a hair (1). That is **10 inversions out of 15 pairs**. A random order would average 7.5. By value, this ranking is worse than random. Rare and Epic also fail the step rule against each other by a mile. Their weight ratio is 1.01.

```python
def lightness(rgb):
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else y * 24389 / 27


def inversions(w):
    """Pairs listed in rising importance whose weights point the wrong way."""
    return sum(1 for i in range(len(w)) for j in range(i + 1, len(w)) if w[i] > w[j])


# World of Warcraft item quality colors, lowest tier first (Warcraft Wiki, "Quality")
quality = {"Poor": "9d9d9d", "Common": "ffffff", "Uncommon": "1eff00",
           "Rare": "0070dd", "Epic": "a335ee", "Legendary": "ff8000"}
weights = []
for name, hexcode in quality.items():
    rgb = tuple(int(hexcode[i:i + 2], 16) for i in (0, 2, 4))
    dl = lightness(rgb)              # on a black background, contrast equals L*
    weights.append(dl)
    print(f"{name:<10} L* = {dl:5.1f}")
print("inverted pairs:", inversions(weights), "of", len(weights) * (len(weights) - 1) // 2)
```

It prints the six L* values from the table and `inverted pairs: 10 of 15`.

Is World of Warcraft's tooltip broken, then? No, and this is the real lesson. The quality colors are a **categorical code**. They name the kind of item, the way a team jersey names a team. Veterans read "purple" as a word, not as a brightness. The game carries rank in other ways: the item name sits on the top line of the tooltip, and the most exciting drops come with extra ceremony such as special sounds or effects. The color is a label, and the weight is done elsewhere.

The trouble starts when a designer copies the colors and expects them to rank. Put the same four middle tiers on a mid-value ground, L* 35 (a stone floor, say, with loot labels floating over it), with no plates and no size changes.

| Tier | Text L* | ΔV against ground 35 | W |
|---|---|---|---|
| Junk (gray #9d9d9d) | 64.7 | 29.7 | 29.7 |
| Common (white) | 100.0 | 65.0 | 65.0 |
| Rare (blue #0070dd) | 48.0 | 13.0 | 13.0 |
| Epic (purple #a335ee) | 47.6 | 12.6 | 12.6 |

Five of six pairs are inverted, and the two best tiers now fall below the week 1 gap of 20. On a stone floor the epic label is close to invisible in value. A new player's eye skips it and goes to the white junk.

### Designing a hierarchy that ranks

Keep the hue code, because players have learned it, and add weight channels that rise with rank. Here is a label system for an invented MMO, still on the L* 35 ground.

| Tier | Design | Parts (A × ΔV) | W | Step from tier below |
|---|---|---|---|---|
| Junk | Text s = 0.9, gray L* 55, no plate | 0.81 × 20 | 16.2 | — |
| Common | Text s = 1.0, white L* 100, no plate | 1.0 × 65 | 65.0 | 4.0× |
| Rare | Dark plate L* 10, area 2.0; text s = 1.1, white | 2.0 × 25 + 1.21 × 90 | 158.9 | 2.4× |
| Epic | Light plate L* 90, area 2.6; text s = 1.25, dark L* 10 | 2.6 × 55 + 1.5625 × 80 | 268.0 | 1.7× |

Zero inversions, and every step clears 1.5. Look at how the weight was earned. Junk is shrunk and dimmed, so it recedes. Rare gets a dark plate, which adds area and lifts its white text to 90 points of contrast. Epic flips to dark text on a light plate, which is the heaviest thing on the ground because it is the only large light area. The blue and purple hues can still tint the plates and borders, so the category code survives.

The epic step (1.7×) is the smallest. That is common in real systems. The top of a hierarchy runs out of room because the plate cannot get lighter than white or larger than the space allows. Designers then add a channel outside the label, such as a beam of light, a sound or a minimap marker, which is exactly what the next section shows.

### A visual you can move

Open [`examples/w11-squint-hierarchy.html`](../examples/w11-squint-hierarchy.html). The top view shows four loot labels floating over a stone floor, drawn crisp on the left and blurred on the right (a squint test). The bottom view is a bar chart of each tier's weight, sorted in the intended order, with inverted pairs linked by red arcs and weak steps marked.

Load the "Hue only" preset. On the crisp side the four labels look distinct, because your eye reads the colors. On the blurred side the white common-tier label is the only one you can find easily, and the rare and epic labels are nearly gone. The chart shows five red arcs. Now load "Weighted". The blurred side shows four blobs growing in the right order, and the arcs disappear. Drag the epic plate's value down from 90 toward 35 and watch the epic blob fade into the floor at the moment its bar drops below rare.

### Cross-game recognition

**Path of Exile, item filters (current game).** Path of Exile lets players write text filters that restyle every loot label on the ground. The official documentation lists the tools: font size from 1 to 45, text, border and background colors each with an alpha value, one of 16 alert sounds, minimap icons in three sizes with a choice of colors and shapes, and a colored light beam. Read those through the model. Font size raises `A`. Background color with alpha adds a plate and its contrast. Border adds a thin high-contrast ring. The beam, sound and minimap icon are channels outside the label, used when the label alone has run out of weight. Players share filters that sort thousands of item types into tiers with these channels. It is a whole community building the weighted hierarchy of the previous table because the default one did not rank finely enough for them.

**Diablo II (original release and Lord of Destruction).** Blizzard's official item guide from the era gives item names distinct colors by type: blue for magic items, yellow for rare items, green for set items and gold for unique items. As in World of Warcraft, the colors are categories that players learn. Yellow is one of the lightest hues a screen can show (week 4), so on the dark item labels a rare item's name has a lot of value contrast whatever its actual worth. Check yourself question 3 asks you to judge that from the model.

**A newspaper front page.** Outside games, the front page is a hierarchy built almost entirely from size and position. The lead headline is the largest type on the page, at the top. Secondary headlines step down in size, and body text is smallest. Color is rare. It works because every step in size is large, often well above the 1.5 area ratio of our step rule. It is the same model with `ΔV` held constant and `A` doing all the work.

**Modular type scales.** Typographers often pick sizes from a **modular scale**, a sequence where each size is the previous one times a fixed ratio (Tim Brown's 2011 article uses the golden ratio, 1.618, as its main example). A ratio of 1.25 in size gives `1.25² = 1.5625` in area, so each step on a 1.25 scale clears our 1.5 step rule from size alone. A ratio of 1.1 gives only 1.21, and you would need contrast or a plate to make up the rest.

Four contexts, one model. Hierarchy comes from weight, weight comes from area times value contrast, and hue is best spent naming things.

### Eyes-open design judgment

- **Separate naming from ranking.** Use hue for categories (item type, faction, damage school) and weight (size, value, plates) for importance. When one channel must do both, the ranking usually loses.
- **Learned codes are real, but slow.** Veterans read the World of Warcraft colors instantly. New players do not, and they form their first impressions of loot from what their eyes do. If your onboarding matters, make the weight agree with the code.
- **The top of a hierarchy runs out of room.** Plates cannot get lighter than white, and labels cannot grow forever. Plan the top tier's extra channel (sound, beam, motion, a separate panel) before you need it.
- **Too many levels flatten everything.** Each extra level needs a 1.5× step. Four levels need a weight range of at least `1.5³ ≈ 3.4×` between top and bottom. Seven levels need more than 11×. Most panels read best with three or four levels. Merge the rest.
- **The model ignores meaning.** A small red "!" can outrank a large headline because players have learned to fear it. Weight predicts where the eye lands before reading starts. Test with players for everything after that.

### Check yourself (worked example)

1. A tooltip shows an item name at `s = 1.3` in white (L* 100) and a stat line at `s = 1.0` in gray L* 70, both on a background of L* 15. Compute both weights and the step. Does the name clear the 1.5 rule?
2. You must keep a single text size for all four loot tiers. The ground is L* 35. Can value alone give four tiers with 1.5× steps? Try text values 55, 65, 80 and 100.
3. Diablo II shows rare names in yellow and unique names in gold. If yellow has L* about 90 and gold about 70, both on a label background of L* 10, which reads as more important by the model, and is that the order the game intends?

<details>
<summary>Answers</summary>

1. Name: `1.3² × 85 = 1.69 × 85 = 143.7`. Stats: `1.0 × 55 = 55`. Step `143.7 / 55 = 2.6`, so yes.
2. Weights are `ΔV` = 20, 30, 45 and 65. Steps are 1.5, 1.5 and 1.44. The last step just misses, and the first tier sits exactly at the week 1 gap of 20. Value alone nearly works but leaves no room for error. Add size or a plate at the top.
3. Rare weight is 80, unique is 60. The model says rare outranks unique, although uniques are the rarer and usually the more wanted items. The game relies on players learning the gold color, just as World of Warcraft relies on learned purple.

</details>

## 3. Building hierarchy in a panel

The worked example ranked labels. Most UI is a panel of many parts, and the same model applies with a few extra habits.

### Start from an importance list

Before you draw anything, write the panel's content as a list, most important first. For an item tooltip: name, whether you can use it, the stat that changed compared to your current item, the other stats, the flavor text, the sell price. Assign each a level from 1 (must see first) to 3 or 4 (read only if interested). If more than one or two items are at level 1, the panel is trying to say too much at once. Push something down or move it to another panel.

### Spend weight top-down

Give the level 1 element the most weight and the best position. Give level 2 about a 1.5× to 2× step less, and so on. You now have a weight budget, and every decoration spends from it. A bright ornamental border around the whole tooltip has a large area and high contrast, so it may outweigh the name. Borders, frames and background art should sit near the ground's value unless they carry meaning.

### Use grouping to reduce levels

Proximity lets the eye treat several items as one. Five stat lines with tight spacing and a shared left edge read as one block at level 2. The same five lines spread out with uneven gaps read as five separate things competing for level 2. Whitespace between groups is free. It does not add weight, but it tells the eye where one unit ends.

### Contrast changes when the background does

In week 10 you saw that a signal's contrast depends on what is behind it. HUD elements float over the game world, which changes from snowfield to cave. A white label has ΔV 90 in a cave and ΔV 5 on snow. Plates (a semi-opaque dark backing) fix this. They give the text a stable local background, which makes its contrast predictable. The cost is area and occlusion of the world. Many games offer a slider for plate opacity for exactly this reason.

### Size must survive the screen

A text size that reads well on your monitor may be too small on a television across the room or on a phone. The absolute size limit belongs to UX201, where [week 11, accessibility guidelines](../../UX201-game-ux-and-player-psychology/lectures/w11-accessibility-guidelines.md) treats text size as a viewing angle. For hierarchy, notice that the smallest level sets the floor. If body text is already at the minimum readable size, the hierarchy can only grow upward, and the top levels get large quickly.

### The squint test, done properly

1. Take a screenshot at the target resolution.
2. Blur it (a Gaussian blur of about 1% of the screen width works) or step back until you cannot read the text.
3. Write down the order in which blobs catch your eye.
4. Compare it with your importance list. Every disagreement is an inversion you can see.

The lab gives you a script that blurs screenshots and computes weights, so you can do both steps with numbers.

## In-class activity (25 minutes)

Pairs. Each pair picks one UI panel from a game they play (an item tooltip, a quest tracker, a party frame or a vendor window) and takes a screenshot. Cite the game and version.

1. Write the panel's importance list from the player's point of view (5 to 8 items), levels 1 to 4. (5 min)
2. Estimate each element's size relative to body text and its value contrast with its background (use the week 1 gray card or a color picker and the L* formula). Compute weights. (8 min)
3. Count inversions and weak steps. (4 min)
4. Blur the screenshot on a laptop and compare the blob order with your computed order. Note one place where the model and your eye disagree, and why. (5 min)
5. Sketch one change that removes the worst inversion. (3 min)

Expected output: the importance list, a weight table, the inversion count, one model-versus-eye disagreement, and a thumbnail fix.

## Common misconceptions

- **"Bright colors make things important."** Saturated colors pop in a gray field, but a saturated blue or purple can have low value and low weight. Check the value, not the vividness.
- **"If players learn the color code, hierarchy doesn't matter."** Learned codes name categories. They do not stop the eye from landing first on the heaviest element, and new players have not learned the code yet.
- **"More levels means more information."** Past three or four levels, the steps shrink below what the eye can separate, and the panel reads as flat. Group and merge instead.
- **"A border makes an element stand out."** A thin border adds little area. A thick, high-contrast frame around everything adds weight to the frame, not to its contents.

## Check yourself

1. An action bar has 12 ability icons of equal size. One ability is the team's emergency heal. Name two ways to give it a 1.5× weight step over the others without making it larger, and compute one of them if each icon has ΔV 40.
2. A quest tracker shows the quest title (s = 1.2, ΔV 60), three objectives (s = 1.0, ΔV 50 each, grouped) and a timer (s = 1.0, ΔV 80). The intended order, least to most important, is objectives, title, timer. Count inversions and check the steps.
3. Your epic label from section 2 runs out of weight on a snowfield of L* 92. Recompute its weight there, and propose a fix that does not change the text or plate values.
4. A designer uses a modular scale with ratio 1.2 for four text levels and the same contrast for all. Which steps fail the 1.5 rule, and what is the smallest ratio that passes by size alone?

<details>
<summary>Answers</summary>

1. Raise its contrast or add a plate or ring. With a light ring that lifts it to ΔV 60, the weight becomes `1 × 60 = 60` against 40 for the others, a 1.5× step. Motion (a slow pulse when a teammate is low) is another channel, but save it for when the heal matters.
2. Weights are objectives 50, title `1.44 × 60 = 86.4`, timer 80. The timer should be heaviest but title outweighs it: 1 inversion. Steps are 86.4 / 50 = 1.73 for the title over the objectives and 0.93 for the timer over the title. Fix the timer, for example with a larger size or a plate.
3. Plate: `2.6 × |90 − 92| = 5.2`. Text on plate is unchanged, `1.5625 × 80 = 125`. Total 130.2, which is now below rare if rare keeps its dark plate there (`2.0 × 82 + 1.21 × 90 ≈ 272.9`). Fix with a channel that does not depend on the ground: a dark outer border around the light plate (two-tone, as in week 10), a beam, or a sound.
4. Area steps are `1.2² = 1.44` for every step, so all three fail. The smallest size ratio that passes is `√1.5 ≈ 1.225`.

</details>

## Lab hook

[Lab 11, the hierarchy audit](../labs/lab11.md). You finish a small Python tool that computes weights, inversions and weak steps from a CSV, run it on a shipped UI panel and on your own redesign, and check both with the provided blur script. The deliverable is the before and after mockups, their blurred versions, the tool's reports and a short design note.

## Sources

- Warcraft Wiki, "Quality" (World of Warcraft, current retail). Tier names and hex color codes: Poor #9d9d9d, Common #ffffff, Uncommon #1eff00, Rare #0070dd, Epic #a335ee, Legendary #ff8000. https://warcraft.wiki.gg/wiki/Quality
- Grinding Gear Games, "Item Filter Information" (Path of Exile, current game). `SetFontSize` range 1-45; text, border and background colors with alpha; `PlayAlertSound` ids 1-16; `MinimapIcon` sizes 0-2 with colors and shapes; `PlayEffect` beams. https://www.pathofexile.com/item-filter/about
- Blizzard Entertainment, Diablo II: Lord of Destruction item guide (classic.battle.net, original era). Magic items named in blue, rare in yellow, set in green, unique in gold. http://classic.battle.net/diablo2exp/items/
- Brown, T. (2011, May 3). "More Meaningful Typography." *A List Apart*, issue 327. Modular scales, golden ratio example.
- Itti, L., Koch, C. & Niebur, E. (1998). "A Model of Saliency-Based Visual Attention for Rapid Scene Analysis." *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 20(11), 1254-1259.
- Solarski, C. (2012). *Drawing Basics and Video Game Art*. Watson-Guptill.
- CIE L* formula and the value gap of 20: AR101 week 1. Hue and value as separate properties: AR101 week 4.

## Interactive spec: examples/w11-squint-hierarchy.html

**The one insight:** the eye ranks elements by weight (area times value contrast), not by the meaning of their hue. A hue-coded set of labels that looks distinct when crisp collapses to one visible label when blurred, and a weighted set keeps its order.

**Layout.** Two panels. Mobile: stacked. Desktop (≥ 960px): the label scene on top across the full width, split into "Crisp" and "Squint" halves; the weight chart below.

1. **Label scene.** A flat floor filled with gray at `L*_ground` (convert L* to sRGB gray as in the week 10 spec). Four loot labels in a row: Junk, Common, Rare, Epic, each an invented short item name (for example "Cracked Mug", "Iron Buckle", "Tidewarden Ring", "Crown of Nine Bells"). Each label = optional rectangular plate (fill value and area slider) + text (size and value) + optional 2px border in the tier hue. The "Squint" half renders the same scene with a CSS `filter: blur(Npx)` where N = 1% of the panel width (at least 4px), plus a toggle "Grayscale".
2. **Weight chart.** Horizontal axis: tiers in intended order, least to most important. Vertical bars: weight `W = plate_area × |L*_plate − L*_ground| + s² × |L*_text − L*_behind|`, where `L*_behind` is the plate value if a plate is shown, else the ground value. Draw a red arc between every inverted pair. Label each bar with W and each gap with the step ratio; mark ratios below 1.5 with a warning color and the text "weak step".

**Readout (copyable).** A table: tier, s, text L*, plate L*, plate area, W, step from the tier below. Summary line: "Inversions: k of 6. Weak steps: m of 3."

**Controls.**
- Presets: "Hue only" (default on load), "Weighted", "WoW colors on black".
- Per tier (collapsible on mobile): text size s (0.8-1.6, step 0.05), text L* (0-100), plate on/off, plate L* (0-100), plate area (1.0-3.0, step 0.1), tier hue (color picker, cosmetic only: it tints the text or border but the model uses the L* sliders; when the user picks a hue, keep the chosen L*).
- Ground L* (0-100, default 35). Blur amount. Grayscale toggle. Reset.

**Preset values and expected results.**
- "Hue only": ground 35, no plates, s = 1 for all, text colors #9d9d9d, #ffffff, #0070dd, #a335ee (text L* 64.7, 100.0, 48.0, 47.6). Weights 29.7, 65.0, 13.0, 12.6. Inversions 5 of 6.
- "Weighted": ground 35. Junk s 0.9, text L* 55, no plate (W 16.2). Common s 1.0, text L* 100, no plate (W 65.0). Rare plate L* 10 area 2.0, text s 1.1 L* 100 (W 158.9). Epic plate L* 90 area 2.6, text s 1.25 L* 10 (W 268.0). Steps 4.01, 2.44, 1.69. Inversions 0, weak steps 0.
- "WoW colors on black": six tiers Poor, Common, Uncommon, Rare, Epic, Legendary with the hex codes from the lecture, ground 0, no plates, s = 1. Weights 64.7, 100.0, 87.9, 48.0, 47.6, 67.1. Inversions 10 of 15. (The chart grows to six bars for this preset.)
- In "Weighted", setting ground to 92 gives Junk W 30.0, Common W 8.0, Rare W 272.9 and Epic W 130.2: two inversions (Junk over Common, Rare over Epic).

**First screen.** "Hue only" preset: crisp side shows four colored labels, squint side shows one clear white blob and three faint ones, chart shows five red arcs, caption "Four colors. One label your eye can find."

**Accessibility and style.** Shared palette tokens, both color schemes (the scene itself keeps its own gray values). Inversion arcs are also dashed and listed in text. All controls keyboard operable with visible focus. Respect reduced motion (no animated transitions of bars). No game art, logos or real item names.
