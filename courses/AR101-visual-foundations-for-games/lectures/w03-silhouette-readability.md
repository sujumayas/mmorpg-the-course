# AR101 · Week 03 — Silhouette Readability

**Why this matters:** In a fight, a player has a fraction of a second to decide whether the figure on the ridge is the healer to focus or the tank to ignore. They decide from the outline, often against the light, often at 40 pixels tall. If two of your classes share a silhouette, you have made a gameplay bug that no balance patch can fix.

**You will be able to:**
- Run the silhouette test on a roster of characters: black-fill each one and check whether every class is still identifiable.
- Compute the overlap (intersection over union) between two silhouettes and find the most confusable pair in a roster.
- Predict which details disappear when a sprite shrinks, and redesign a character so its identity survives at the smallest size players see it.
- Critique a character lineup by naming what carries each silhouette: proportion, extremities, negative space or pose.

**Before class:** Mitchell, Francke and Eng, "Illustrative Rendering in Team Fortress 2" (2007), section 3 and section 4.1 with its Figure 2 (the lineup of the nine classes, in color and in silhouette), about one page. Solarski, *Drawing Basics and Video Game Art* (2012), the material on silhouette and gesture (find it through the table of contents).

**Prerequisites from earlier courses:** None outside this course. This week uses [AR101 week 1, value before color](w01-seeing-like-an-artist-value-before-color.md) (a silhouette is the extreme value plan: one dark shape on a light ground) and [AR101 week 2, shape language](w02-shape-language-circles-squares-triangles.md) (a silhouette's big shapes carry the message). [GD101 week 12, feedback, juice, clarity and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) explains why fast identification matters in reaction-time terms, using the same Team Fortress 2 example.

**Interactive:** [`examples/w03-silhouette-lineup.html`](../examples/w03-silhouette-lineup.html). Keep it open during section 2.

---

## 1. What a silhouette is, and why it carries identity

A **silhouette** is the filled outline of a figure: every pixel that belongs to the character painted one flat color, everything else another. It is what you see of a person standing in a doorway with the light behind them. It keeps the outline, the proportions and the gaps between limbs and body. It throws away every interior detail: face, costume pattern, color, shading.

That sounds like a harsh test, and it is. It is also close to what a player sees in play:

- **At distance.** A character 300 meters away in an open world is a few dozen pixels tall. Interior detail blurs away. The outline remains.
- **In bad light.** Backlit against a sunset, in a dark dungeon, inside a smoke cloud, a character's interior goes dark and flat. The outline remains.
- **In the corner of the eye.** Peripheral vision sees shape and motion far better than it sees detail or color. A player watching their own health bar notices an enemy's outline at the edge of the screen.
- **In a crowd.** When 20 characters overlap in a raid, a player picks out individuals by the parts of their outline that stick out.

A character whose identity lives in its outline survives all four. A character whose identity lives in its color scheme or its face does not.

### The silhouette test

The test is simple enough to do in five minutes, and professional teams use it throughout concept work.

1. Line up every character that the player must tell apart, at the same scale, in a neutral standing pose.
2. Fill each one solid black on a white background.
3. Show the lineup to someone who knows the roster, briefly, and ask them to name each one. Or name them yourself, honestly, after looking away for a minute.
4. Any pair that gets confused is a design problem. Fix the outline, not the paint job.

This lecture adds a number to step 4 so you can find the weak pair before anyone else does, and so you can check a roster of 30 characters, which no one can eyeball reliably.

## 2. Worked example: the class lineup

### The hook

When Valve built Team Fortress 2 (2007), its nine classes had to be identifiable at a glance across varied distances and viewpoints, because the class of an enemy tells you how dangerous it is and how to fight it. In their paper on the game's art, the developers describe designing the nine classes to be very distinct from one another, with body proportions, weapons, footwear, hats and clothing folds all chosen to give each class a unique silhouette. They also describe how they checked it. During concept work they looked at the lineup in pure silhouette, with no interior detail at all, and used that view to validate the designs. The paper's Figure 2 prints the lineup twice, in color above and in black silhouette below, and every class is still recognizable in the black row.

Valve still applies the rule. The game's Workshop page, where players submit cosmetic items, says that the classes' distinctive silhouettes help players tell them apart in battle, and that Valve tends to avoid items that obscure or confuse those silhouettes. A good hat can be rejected for hiding the outline it sits on.

So "can you still tell them apart in black?" is a live design rule at a studio that sells player-made cosmetics. Can you run the same test on your own roster, with numbers?

### The model: overlap between two silhouettes

Represent each silhouette as a **mask**: a grid where each pixel is either filled (part of the character) or empty. Line the masks up so the characters stand on the same spot. Then compare two masks `a` and `b` by their **intersection over union**:

```
IoU(a, b) = |a ∩ b| / |a ∪ b|
```

- `|a ∩ b|` is the number of pixels filled in *both* masks.
- `|a ∪ b|` is the number of pixels filled in *either* mask.
- IoU = 1 means the two silhouettes are identical. IoU = 0 means they share no pixels at all.

IoU is also called the Jaccard index. Engineers use the same measure to score how well a detected box matches a real object in computer vision. For us, a high IoU means "these two outlines cover almost the same area, so a glance may confuse them".

Two practical rules come with the model.

**Alignment.** The masks must be lined up the way a player would compare them: standing on the same ground. In this course we anchor each mask at its feet. Find the lowest filled row, take the middle of the filled pixels in that row, and put that point at the origin. (Lab 03 shows what goes wrong when a staff or a cape also touches the ground.)

**Thresholds.** As a course convention, a pair with **IoU of 0.80 or more is too alike** and must be redesigned, and the target for a finished roster is **every pair at 0.75 or less** at every size the player sees. Like the value gap of week 1, these are working numbers for a first check, not results from a perception study. The final judge is a person looking at the lineup.

### Numbers you can check

Here is a small invented roster on a 12 × 20 pixel grid, built from rectangles so you can count pixels by hand. All four characters share the same body: a 4 × 4 head, a 6 × 5 torso and 4 × 6 legs, 70 pixels in all. Each class adds its own parts.

| Class | Added parts | Pixels |
|---|---|---|
| Knight | Tall shield, 3 × 7, held at the left side | 70 + 21 = 91 |
| Mage | Pointed hat (2 × 4 crown and a 6-pixel brim, overlapping by 2) and a staff 1 × 16 at the right, not touching the ground | 70 + 12 + 16 = 98 |
| Cleric | A hood, one 4-pixel row above the head | 70 + 4 = 74 |
| Rogue | A small dagger, 2 × 2, beside the torso | 70 + 4 = 74 |

Because every added part sits outside the shared body, the overlap of any two characters is at least the 70 body pixels. Work out the knight and the rogue. They share only the body, so `|a ∩ b| = 70`. The union is the body plus the shield plus the dagger, `70 + 21 + 4 = 95`. So `IoU = 70 / 95 = 0.737`.

The full table, with the original roster:

| Pair | Intersection | Union | IoU | Verdict |
|---|---|---|---|---|
| Cleric and rogue | 70 | 78 | 0.897 | Too alike |
| Cleric and mage | 74 | 98 | 0.755 | Borderline |
| Knight and cleric | 70 | 95 | 0.737 | OK |
| Knight and rogue | 70 | 95 | 0.737 | OK |
| Mage and rogue | 72 | 100 | 0.720 | OK |
| Knight and mage | 70 | 119 | 0.588 | Clearly distinct |

(The mage and the cleric overlap in 74 pixels, not 70, because the cleric's hood sits inside the mage's hat brim. The mage and rogue overlap in 72 because the staff and the dagger share two pixels.)

The cleric and the rogue fail. In color they may look nothing alike: a white-and-gold robe against dark green leather. In black they are the same standing figure with four extra pixels each.

### The scale test

Players rarely see a character at full art size. Shrink the roster to half size, as it might appear at a distance or on a minimap. The rule for shrinking is the usual one for pixel art: split the grid into 2 × 2 blocks, and a block becomes a filled pixel if at least half of its four pixels are filled. The 12 × 20 masks become 6 × 10.

| Pair | IoU at full size | IoU at half size |
|---|---|---|
| Cleric and rogue | 0.897 | **1.000** |
| Knight and cleric | 0.737 | 0.769 |
| Knight and rogue | 0.737 | 0.769 |
| Mage and rogue | 0.720 | 0.690 |
| Mage and cleric | 0.755 | 0.690 |
| Knight and mage | 0.588 | 0.571 |

At half size the cleric and the rogue are *identical*. The hood is one pixel tall and sits in the same 2 × 2 blocks as the top row of the head, blocks the head already fills, so it adds nothing. The dagger straddles four blocks. Two of them are already filled by the torso, and in the other two the dagger supplies only one pixel of four, below the half-full rule. Both identities were carried by details smaller than the block size, and both vanished. This is the most important lesson of the week. **A detail smaller than the shrink factor is not part of the silhouette at that size.**

### Fixing the roster

Fix the worst pair first, and fix it with a big shape, not a bigger detail.

**Fix 1: give the cleric a long robe.** Replace the cleric's legs (4 wide) with a robe 8 pixels wide over the same 6 rows. That adds 24 pixels, and the cleric becomes a wide bell shape, a circle-and-triangle silhouette that reads as calm and grounded (week 2). The cleric and rogue IoU drops from 0.897 to 70 / 102 = 0.686 at full size. At half size it is 0.769, still above the 0.75 target, because the rogue is now nothing but the base body at that size and its outline sits inside everyone else's.

**Fix 2: give the rogue a long knife held out sideways.** Replace the 2 × 2 dagger with a knife 4 pixels long and 2 tall, starting in the torso's right column and reaching out to the edge of the grid (it adds 6 pixels, because 2 of its 8 overlap the torso). Now the rogue has a horizontal line sticking out of its silhouette at chest height, a shape no one else has.

| Pair | Final roster, full size | Final roster, half size |
|---|---|---|
| Knight and rogue | 0.722 | 0.741 |
| Cleric and rogue | 0.673 | 0.741 |
| Mage and rogue | 0.706 | 0.724 |
| Knight and cleric | 0.615 | 0.677 |
| Cleric and mage | 0.607 | 0.571 |
| Knight and mage | 0.588 | 0.571 |

Every pair is now at or under 0.75 at both sizes. The worst pairs are the knight and the rogue and the cleric and the rogue, tied at 0.741 when small. The rogue is the next character to watch as the roster grows. In all, the final roster adds 83 pixels to the four shared bodies (shield 21, hat 12, staff 16, hood 4, robe 24, knife 6).

### A visual you can move

Open the interactive. It shows the four characters in color, each with interior detail, and they look different enough. Press **Black fill**. The cleric and the rogue collapse into near-twins, and the pair matrix beside them lights up 0.897 in the danger color. Switch **Size** to 1/2 and the matrix shows 1.000: they are pixel-for-pixel the same. Now toggle each character's parts on and off (robe, long knife, hood, shield, hat, staff) and watch the matrix and the "worst pair" line update. Try to find a roster where every pair stays under 0.75 at both sizes using *fewer* added pixels than the final roster above.

### Cross-game recognition

**Team Fortress 2 (Valve, 2007).** The hook is the model at production scale: nine classes, checked in black during concept, protected afterward by a rule that cosmetics must not obscure silhouettes. The paper names what carries each outline, and they map onto the parts in our roster: body proportions (our robe), weapons (our knife and staff), footwear and hats (our hood and hat). Where our model uses rectangles, Valve's artists used whole bodies, but the question each design answered is the same: which pixels does this class own that no other class does?

**The Staunton chess set (1849).** Chess pieces are a roster that must be told apart at a glance, across a board, by players of every eyesight. The Staunton pattern, registered in 1849 and marketed by Jaques of London, gave every piece a shared turned base and a distinct top: a horse's head for the knight, a mitre for the bishop, battlements for the rook, a coronet for the queen, a cross for the king, a plain ball for the pawn. A newspaper review of the time praised how every piece stood out distinctly even in complex positions. In our terms, the bases overlap heavily (high IoU from the shared body) and each piece owns a top shape. It also shows the model's blind spot, below: people weigh the top of a silhouette more than the base, and IoU weighs every pixel the same.

**"Who's That Pokémon?" (Pokémon anime, English dub from the first episode).** The show turned the silhouette test into a quiz. Before each commercial break it shows a creature as a solid silhouette and asks the audience to name it. The segment works because the creatures were designed with outlines that are distinct enough to guess from shape alone: ears, tails and body proportions that no other creature shares. Viewers practice exactly the skill this lecture measures.

Three contexts, one principle: every member of a roster must own some part of its outline that no other member has, big enough to survive at the size it is seen.

### Eyes-open design judgment

- **IoU weighs all pixels equally; people don't.** Players look at heads, weapons and the tips of the outline first, the way chess players read the tops of pieces. Two characters with IoU 0.70 can still be confused if the differing 30% is all at the feet. As a second check, run the test on the top third of each mask alone, or simply ask people.
- **Anchor choices change the answer.** Anchoring at the feet assumes characters stand on the ground. A flying or crouching class breaks the assumption. For those, compare at several offsets and take the highest overlap. That is the most confusable alignment, the one that matters.
- **Test more than one pose.** A silhouette is a single frame. Characters walk, attack and jump. A class whose identity is a raised weapon may lose it in the idle pose. Check the idle pose, the attack pose and the running pose.
- **In 3D, test more than one angle.** A shield that dominates the side view may disappear from the front. Render the black-fill test from the front, the side and three-quarters.
- **Small details are for close-ups.** The hood and dagger were fine as *secondary* identity (in the character select screen, in a cutscene), but they cannot carry *primary* identity. Decide which size is the smallest that matters for gameplay and test at that size.
- **Don't make everything distinct at any cost.** A roster where every silhouette shouts is noisy, and cosmetics and team colors must still fit. The goal is enough distinctness for the decision the player must make. Two support classes that the player responds to the same way can share a silhouette family; a healer and a sniper cannot.

## 3. What makes a silhouette distinct

When a pair fails the test, you have four levers. Use the biggest one that fits the character's story.

**Proportion.** The overall width, height and mass distribution. Tall and thin against short and wide is the strongest difference there is, because it changes every row of the mask. The robe fix was a proportion change: it turned a straight figure into a bell.

**Extremities.** Parts that stick out of the body: hats, hair, weapons, wings, tails, backpacks, shoulder armor. They own pixels no one else owns, and they sit where the eye looks, on the outer edge. The long knife and the mage's hat are extremities. Keep them at least as big as the shrink factor at the smallest size that matters.

**Negative space.** The gaps inside and around the silhouette: the gap between an arm and the torso, between the legs, between a shield and the body. The knight's silhouette has a one-pixel notch between the shield and the legs, and that gap makes the shield read as a separate object rather than a lump. Arms held away from the body read far better than arms at the sides. When you draw a character select pose, open up the negative space.

**Pose and gesture.** How the body is held: hunched, upright, wide stance, leaning forward. A rogue that crouches, a knight that stands square, a mage that leans on a staff. Pose is powerful in stills but changes with animation, so don't let it carry identity alone.

### Silhouettes at MMO scale

An MMO multiplies the problem. A roster of classes is crossed with playable body types and with thousands of gear pieces and cosmetics, and players meet each other in crowds. Three policies keep silhouettes readable:

- **Reserve the class-defining zone.** Decide which part of the outline identifies the class (a weapon type, a shoulder shape, a robe hem) and do not let cosmetic items cover or replace it. This is the Team Fortress 2 Workshop rule written as a spec.
- **Let cosmetics vary the interior, not the outline.** Recolors, patterns and trims change the inside of the mask and leave the test untouched.
- **Run the test on the worst case, not the default.** Put the biggest hat on the smallest body and the widest cape on the thinnest class, and run the lineup again. The confusable pair will usually appear there first.

## In-class activity (25 minutes)

Work in groups of three. Materials: grid paper (or the interactive's edit mode), a black marker, a phone camera, and a timer.

1. **(8 min)** Each person designs one character on a 12 × 20 grid for a four-class roster: tank, healer, ranged damage, melee damage. Everyone starts from the same base body (the one in section 2). Add at most 30 pixels.
2. **(5 min)** Fill your four characters black. Photograph the lineup. Show the photo to someone from another group for one second and ask them to name the roles. Record how many they get right.
3. **(7 min)** Count pixels and compute the IoU for your group's worst-looking pair by hand. Then check all six pairs in the interactive.
4. **(5 min)** Shrink to half size in the interactive. Which details vanished? Redesign one character so the worst pair is at or below 0.75 at both sizes, and write down the change.

Expected output: the lineup photo, the one-second recognition score, a six-row IoU table at two sizes, and a one-sentence description of the fix.

## Common misconceptions

- **"They look different in color, so they're fine."** Color and interior detail are the first things lost at distance, in bad light and in peripheral vision. The cleric and rogue looked different in color and were identical at half size.
- **"Add more detail to make a character more distinct."** Detail smaller than the shrink factor disappears. Distinctness at gameplay size comes from proportion and big extremities.
- **"IoU is the perceptual truth."** It is a quick, repeatable screen for a roster. It weighs all pixels equally and ignores which parts people look at. Confirm with a one-second recognition test.
- **"Silhouette is only for fighting games and shooters."** Any game where players must identify units, enemies, NPC roles or other players at a glance needs it, including MMOs, strategy games and mobile games with small sprites.

## Check yourself

1. Two silhouettes have 120 and 150 pixels, and they share 100 pixels when aligned. What is their IoU? Does the pair pass the course's 0.75 target?
2. In the original roster, what would the cleric and rogue IoU be if the rogue's dagger were removed entirely? What does that tell you about the cleric's hood?
3. A 2-pixel-wide spear is added to a character. Players see the character at quarter size (4 × 4 blocks). Will the spear survive the shrink? What width would guarantee it survives, whatever its alignment with the block grid?
4. A designer proposes making the rogue distinct by coloring it bright purple. Explain, using this lecture's model and week 1's, when that works and when it fails.

<details>
<summary>Answers</summary>

1. The union is `120 + 150 − 100 = 170`, so `IoU = 100 / 170 ≈ 0.588`. It passes.
2. The rogue would be the bare 70-pixel body, and the cleric is the body plus a 4-pixel hood. The overlap is 70 and the union is 74, so `IoU = 70/74 ≈ 0.946`. The hood alone makes almost no difference to the silhouette; it is a close-up detail, not an identity.
3. Not reliably. A 4 × 4 block is filled when at least 8 of its 16 pixels are. If both spear columns fall inside one block's columns, a stretch of spear that runs the block's full height fills exactly 8, and it survives. If the spear straddles a block boundary, each block gets one column, 4 of 16, and the spear vanishes. A width of 3 guarantees that at least 2 columns land in one block whatever the alignment, so 8 of 16, and it survives. In general the width must be at least the shrink factor minus 1. In practice, give yourself margin and make key shapes as wide as the shrink factor or wider.
4. The purple helps once the player is looking at the rogue in good light: it is a hue cue for identity. It does not help detection at a glance, in bad light, at a distance, for players who cannot distinguish that hue, or when team colors override it. It also does nothing if purple's value matches its surroundings (week 1). The silhouette is still identical at small size, so the underlying problem remains.

</details>

## Lab / assignment hook

[Lab 03, the silhouette test as a program](../labs/lab03.md). You will implement IoU, feet alignment, block downsampling and a worst-pair finder, run them on this lecture's roster, then design your own four-class roster as sprite files and redesign it until every pair is at or below 0.75 at full and half size. You will also run a one-second recognition test with real people and compare it with the numbers. This is one of the weekly studies (50% of the course grade), and the roster feeds your style bible (week 13).

## Sources

- Mitchell, J., Francke, M. and Eng, D. (2007). "Illustrative Rendering in Team Fortress 2." *Proceedings of NPAR 2007*, ACM. Section 4.1 and Figure 2: the nine classes designed to be visually distinct; body proportions, weapons and silhouette lines set by footwear, hats and clothing folds; silhouettes viewed with no interior detail to validate designs during concept.
- Valve, Team Fortress 2 Workshop page (teamfortress.com/workshop, retrieved September 2026). The classes' distinctive silhouettes help players tell them apart in battle; Valve tends to avoid items that obscure or confuse them.
- Wikipedia, "Staunton chess set". Introduced 1849, design registered by Nathaniel Cooke and first released by John Jaques of London; piece identities carried by the tops (horse head, mitre, battlements, coronet, crown with cross, ball); the *Illustrated London News* (1849) remark that every piece stands out distinctly.
- Bulbapedia, "Who's That Pokémon?" (Pokémon anime). A question segment that shows a Pokémon in silhouette for the audience to guess, used in the English dub from the first episode, dropped after season 6 and revived in the Black & White series.
- Jaccard, P. (1912). "The distribution of the flora in the alpine zone." *New Phytologist* 11(2), 37-50. The origin of the Jaccard index (intersection over union).
- Solarski, C. (2012). *Drawing Basics and Video Game Art*. Watson-Guptill. Course reading on silhouette and gesture.
- All roster values in section 2 were computed from the masks given there; the same masks ship as text files in Lab 03's starter.

## Interactive spec: examples/w03-silhouette-lineup.html

**The one insight.** Characters that look different in color can be the same silhouette, and shrinking makes it worse. The first screen shows the four characters in color with the matrix beside them; one press of **Black fill** reveals cleric and rogue at 0.897, and one more control (Size 1/2) shows 1.000.

**Characters (exact masks, 12 × 20 grid, x from 0 to 11 left to right, y from 0 to 19 top to bottom, rectangles inclusive).**
- Shared body: head x 4-7, y 5-8; torso x 3-8, y 9-13; legs x 4-7, y 14-19.
- Knight: shield x 0-2, y 9-15.
- Mage: hat crown x 5-6, y 1-4; brim x 3-8, y 4; staff x 10, y 3-18.
- Cleric: hood x 4-7, y 4. Optional robe (Fix 1): x 2-9, y 14-19.
- Rogue: dagger x 9-10, y 11-12. Optional long knife (Fix 2): x 8-11, y 10-11, which replaces the dagger.

Every part is a toggle. The defaults are the original roster (shield, hat, staff, hood, dagger on; robe and long knife off).

**Views.**
- **Lineup.** The four characters side by side, drawn pixel-perfect (nearest-neighbor scaling, integer zoom). In color mode each has invented interior detail painted only inside its own mask: knight steel gray armor with a lighter shield face; mage deep blue robe and ochre hat band; cleric white and gold; rogue dark green with a brown belt. Faces are two-pixel eyes. In **Black fill** mode each mask is solid ink on the paper color.
- **Pair matrix.** A 4 × 4 grid of IoU values to three decimals, with cells shaded by value (light below 0.75, amber 0.75 to 0.80, danger color at 0.80 or more) and a text label in each cell ("OK", "watch", "too alike").
- **Overlay.** Clicking or keyboard-selecting a matrix cell draws the two masks of that pair overlaid, aligned at the feet: shared pixels in ink, pixels only in the first in steel, only in the second in ochre, with the intersection and union counts printed.
- A line under the matrix: "Worst pair: cleric and rogue, IoU 0.897 (too alike)".

**Controls (native inputs, keyboard reachable, values printed).**
- Black fill: on or off.
- Size: 1 (12 × 20) or 1/2 (6 × 10). Shrinking uses 2 × 2 blocks from (0, 0); a block is filled when at least 2 of its 4 pixels are filled. Draw the shrunken masks at double zoom so they appear the same height.
- Part toggles for each character, as listed above.
- Thresholds: "too alike" (default 0.80) and "target" (default 0.75), each a slider 0.50 to 0.95.
- Presets: Original, Fix 1 (robe on), Fix 1 + 2 (robe and long knife on, dagger off).
- Pixel editor (for the in-class activity): an "Edit pixels" toggle, available at size 1, lets you click a lineup pixel (or Tab to a character, move with the arrow keys and press Space) to add or remove it; "Clear edits" resets. When every pair is under the target at both sizes, the status line reports the pixels added to the shared bodies and compares them with the final roster's 83.

**Computation.** Build each mask as a set of cells. Normalize: find the largest y with a filled cell; among cells in that row take `fx = floor((min x + max x) / 2)`; shift all cells by (−fx, −maxY). Shrinking happens before normalizing. IoU = |a ∩ b| / |a ∪ b|, with two empty masks counting as 1.

**Test values.**

| Preset, size | Pixels (knight, mage, cleric, rogue) | Worst pair | Other values |
|---|---|---|---|
| Original, 1 | 91, 98, 74, 74 | cleric-rogue 0.897 | cleric-mage 0.755, knight-cleric 0.737, knight-rogue 0.737, mage-rogue 0.720, knight-mage 0.588 |
| Original, 1/2 | 26, 29, 20, 20 | cleric-rogue 1.000 | knight-cleric 0.769, knight-rogue 0.769, cleric-mage 0.690, mage-rogue 0.690, knight-mage 0.571 |
| Fix 1, 1 | 91, 98, 98, 74 | knight-rogue 0.737 | mage-rogue 0.720, cleric-rogue 0.686, knight-cleric 0.615, cleric-mage 0.607, knight-mage 0.588 |
| Fix 1, 1/2 | 26, 29, 26, 20 | knight-rogue 0.769 and cleric-rogue 0.769 | mage-rogue 0.690, knight-cleric 0.677, cleric-mage 0.571, knight-mage 0.571 |
| Fix 1 + 2, 1 | 91, 98, 98, 76 | knight-rogue 0.722 | mage-rogue 0.706, cleric-rogue 0.673, knight-cleric 0.615, cleric-mage 0.607, knight-mage 0.588 |
| Fix 1 + 2, 1/2 | 26, 29, 26, 21 | knight-rogue 0.741 and cleric-rogue 0.741 | mage-rogue 0.724, knight-cleric 0.677, cleric-mage 0.571, knight-mage 0.571 |

**Accessibility and motion.** Matrix status is given as text in every cell, not only as shading. The overlay uses steel and ochre plus a legend, and a pattern (diagonal hatching) on one of the two exclusive regions so it works without color. No animation needed; any transition respects `prefers-reduced-motion`. Palette tokens from `templates/interactive-tokens.css`, light and dark. Character interior colors are data and do not change with the theme; in dark mode, Black fill uses the light ink color on the dark paper so the silhouettes stay visible.
