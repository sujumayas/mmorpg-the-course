# AR101 · Exam bank: quiz, practice and crit questions

AR101 has no written exam. The course grade comes from the [weekly studies](weekly-studies-brief.md) (50%), the [style bible](style-bible-brief.md) (20%) and the [final piece](final-piece-brief.md) (30%). This bank does three other jobs.

- Practice. Work a week's questions before its lab. If you can answer them with the lecture closed, the lab's numbers will come quickly.
- Lab quizzes. From week 2 on, each lab opens with an ungraded 10-minute quiz of two or three questions from this bank. Usually one applies a lecture model to new numbers and one asks you to judge or fix a design.
- Crit questions. The style bible review and the week 15 crit of the final piece ask questions in this style, rewritten with the colors, masks, holds and file sizes from your own work.

Every question carries its week and one type.

- **compute**: apply a lecture model (L*, ΔV, circularity, IoU, HSV, ramps, run lengths, neighbour indices, seam ratio, holds, local contrast, headroom, visual weight, color-blind simulation, contrast ratio, texel density, atlas memory) to values you have not seen.
- **code**: say what a short Python snippet prints, and why.
- **analysis**: use a model to find a limit, a threshold or the cause of a result.
- **design**: choose values or shapes for a stated goal and justify them with a number.
- **critique**: find what is wrong with a proposal and say how to fix it.

All colors, masks, maps and assets are invented unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and version. Every snippet runs as shown with `.venv/bin/python`, and every number in the answers was recomputed in Python from the lectures' own models. Unless a question says otherwise, use the course defaults: L* from sRGB exactly as in [week 1](../lectures/w01-seeing-like-an-artist-value-before-color.md); a value gap ΔV under 10 merges, 20 reads, 40 reads at a glance; IoU of 0.80 or more is too alike and 0.75 is the target; a seam ratio of 1.5 passes; a hierarchy ratio or weight step of 1.5 is clear; 60 ticks per second; WCAG contrast of 3:1 for graphical objects. Write your own answer before you open the solution.

---

## Week 1 · Seeing like an artist: value before color

1. *Week 1 · compute.* A forest-floor tile is sRGB (110, 130, 90). Three figures can appear on it: an orange mushroom pickup (230, 120, 40), a blue slime enemy (60, 70, 140) and a pale bone key (250, 200, 150).
   (a) Compute the floor's relative luminance `Y` and its L*, then the L* of each figure.
   (b) Give each figure's ΔV against the floor and its verdict.
   (c) Which figure would you fix first, and would you move the figure or the floor?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Floor `Y = 0.2002`, L* 51.9. Orange 62.0, blue 32.3, pale 83.9. (b) Orange ΔV 10.2, blue 19.5, pale 32.0. The orange and the blue do not read reliably; the pale key reads but is not a split-second spot. (c) Fix the orange pickup, and move the figure.

(a) Linearize the floor: `110/255 = 0.431` gives 0.1559, `130/255 = 0.510` gives 0.2232, `90/255 = 0.353` gives 0.1022. `Y = 0.2126 × 0.1559 + 0.7152 × 0.2232 + 0.0722 × 0.1022 = 0.0331 + 0.1596 + 0.0074 = 0.2002`. That is above 0.0089, so `L* = 116 × 0.2002^(1/3) − 16 = 116 × 0.5850 − 16 = 51.9`. The figures follow the same way.

(b) `|62.0 − 51.9| = 10.2` sits just above the merge line, far below 20. `|32.3 − 51.9| = 19.5` misses 20 by half a point. `|83.9 − 51.9| = 32.0` reads.

(c) The orange is the most saturated color in the set and the one a player must find, yet in value it is almost the floor. Darkening the floor to help it would pull the floor toward the blue slime (a floor of L* 40 gives the orange 22 but leaves the slime at 7.7). Readability belongs to the pair, and here only the figure can move without breaking another pair. Lighten it toward a pale gold, as the lecture's gold potion does.
</details>

2. *Week 1 · compute.* An artist checks values with a "channel average" gray filter, `gray = (R + G + B) / 3`. A blue enemy (0, 0, 200) stands on bright grass (0, 200, 0).
   (a) What gray does the filter give each color, and what ΔV does it report?
   (b) What are the true L* values and ΔV?
   (c) Which way does the filter mislead the artist here, and which way did it mislead on the lecture's red potion?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Both become gray 67 (L* 28.4), so the filter reports ΔV 0, a merge. (b) Grass L* 70.4, enemy L* 24.2, ΔV 46.2, which reads at a glance. (c) Here the filter invents a problem. On the red potion it hid one.

(a) `(0 + 0 + 200) / 3 = (0 + 200 + 0) / 3 = 66.7`, rounded to 67 for both. Same gray, same L*.

(b) Green carries weight 0.7152 in `Y` and blue only 0.0722. `lin(200) = 0.578`, so the grass has `Y = 0.413` and the enemy `Y = 0.042`. That gives L* 70.4 and 24.2.

(c) The average treats the three channels as equal, and the eye does not. With the filter the artist would "fix" a pair that already separates by 46 points. On the lecture's dungeon, pure red (L* 53.2) averages to 85 (L* 36.1), 17 points too dark, which makes it look separated from the 53.6 floor when the true gap is 0.4. Use a luminance or L* grayscale.
</details>

3. *Week 1 · compute.* A 1-bit game fakes grays with dither patterns of white dots on black.
   (a) What L* does a pattern with one white dot in every three approximate from a distance?
   (b) What fraction of white dots approximates L* 50? Would you use one dot in five or one in six?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) L* 64.4. (b) 18.4% white. One in five (L* 51.8) is closer than one in six (47.8).

(a) One dot in three emits a third of the light, `Y = 0.333`. `L* = 116 × 0.333^(1/3) − 16 = 116 × 0.693 − 16 = 64.4`.

(b) Invert the L* curve. `Y = ((50 + 16) / 116)^3 = 0.569^3 = 0.184`. One in five is `Y = 0.2`, L* 51.8, off by 1.8. One in six is `Y = 0.167`, L* 47.8, off by 2.2. Because lightness follows a cube root of light, a middle gray needs far fewer than half the dots white. This is the lecture's Obra Dinn point: dither density is a value control, and it is not linear.
</details>

4. *Week 1 · analysis.* The band view posterizes L* into 4 bands, band `k = floor(L*/100 × 4)`. Two pairs from one level:
   - an enemy at L* 52 on a floor at L* 48;
   - a pickup at L* 74 on a second floor at L* 51.

   (a) Give each color's band and each pair's ΔV.
   (b) For each pair, say what the band view reports and what ΔV reports.
   (c) Why do they disagree, and which do you trust for a pass or fail?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Floor 48 is band 1, enemy 52 is band 2, ΔV 4. Floor 51 is band 2, pickup 74 is band 2, ΔV 23. (b) The band view shows the enemy separated and flags the pickup as merged. ΔV says the enemy merges and the pickup reads. (c) Band edges are arbitrary cuts. Trust ΔV for the verdict.

`floor(48/25) = 1`, `floor(52/25) = 2`, `floor(51/25) = 2`, `floor(74/25) = 2`. The enemy and its floor straddle the edge at 50, so the bands differ although the colors are 4 points apart. The pickup and its floor both sit inside the 50 to 75 band, 23 points apart. The band view is useful for seeing large value groups at a glance, the Game Boy test. ΔV measures the gap itself. When they disagree, fix what ΔV says (lighten or darken the enemy by at least 16 points), and if you want the band view to agree for the pickup, nudge it from 74 to 76 so it crosses into the top band.
</details>

## Week 2 · Shape language: circles, squares, triangles

5. *Week 2 · compute.* Use `C = π / (n × tan(π/n))` for regular polygons and `C = 4πA/P²` otherwise.
   (a) Compute `C` and the corner angle of a regular heptagon (7 sides). What does the reading map say?
   (b) Compute `C` for a 2.5 : 1 rectangle and give its reading.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `C = 0.932`, corners 128.6°, reading Round. (b) `C = 0.641`, θ = 90°, reading Square.

(a) `π/7 = 25.71°`, `tan 25.71° = 0.4816`, `7 × 0.4816 = 3.371`, `π / 3.371 = 0.932`. Each corner is `180 × 5 / 7 = 128.6°`. Round needs `C ≥ 0.85` and `θ ≥ 120°`, and both hold.

(b) Sides 2.5 and 1: `A = 2.5`, `P = 7`, `C = 4π × 2.5 / 49 = 0.641`. That is only a little above the equilateral triangle's 0.605, but the corner is 90°, inside the 75° to 105° square band. It reads as a plank, not a threat.
</details>

6. *Week 2 · analysis.* A square pickup has its corners rounded with radius `r`. Use `A = s² − (4 − π) r²` and `P = 4s − (8 − 2π) r` with `s = 1`.
   (a) Compute `C` for `r = 0.05` and `r = 0.1`, and give each reading.
   (b) The pickup is a 16-pixel sprite. What is the smallest whole-pixel corner radius that reads as round under the map?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `r = 0.05`: `C = 0.819`, In between. `r = 0.1`: `C = 0.850`, Round, just. (b) 2 pixels.

(a) At `r = 0.05`, `A = 1 − 0.858 × 0.0025 = 0.9979` and `P = 4 − 1.717 × 0.05 = 3.914`, so `C = 4π × 0.9979 / 15.32 = 0.819`. No corners remain, so θ = 180°, but Round also needs `C ≥ 0.85`, and it misses. At `r = 0.1`, `A = 0.9914`, `P = 3.828`, `C = 0.850`.

(b) The threshold is `r ≥ 0.1 s`, and `0.1 × 16 = 1.6` pixels. A 1-pixel corner cut is only about 6% of the side and reads as a square with nicked corners. Round up to 2 pixels. This is week 2 meeting week 6: at small sizes, shape messages come in whole pixels.
</details>

7. *Week 2 · critique.* A level designer ranks hazards in a spreadsheet by circularity, lowest first, and flags the lowest as "most threatening". The list puts a 5 : 1 wooden plank at the top, ahead of a triangular spike. Compute the plank's `C`, say what went wrong, and rewrite the spreadsheet rule.

<details>
<summary>Answer and worked solution</summary>

**Answer.** The plank has `C = 0.436`, lower than the triangle's 0.605, and it still reads as solid. The rule measures "not round", while danger comes from points. Flag danger with the sharpest corner, `θ ≤ 65°`, and use `C` only to separate round from not round.

Sides 5 and 1: `A = 5`, `P = 12`, `C = 4π × 5 / 144 = 0.436`. This is the lecture's rectangle paradox, stretched further. Stretching lowers `C` without adding a single point. A better sheet has two columns: θ decides Sharp (≤ 65°) or Square (75° to 105°), and `C ≥ 0.85` with θ ≥ 120° decides Round. The plank lands in Square, the spike in Sharp.
</details>

8. *Week 2 · design.* A village blacksmith NPC must read as strong and trustworthy. Late in the story the same character is corrupted and becomes a boss. You may change only shapes, not the face or the height. Give the primary, secondary and tertiary family of both versions, name the one measurement you would check on each outline, and add the second signal the lecture asks for when you break a player's expectations.

<details>
<summary>Answer and worked solution</summary>

**Answer.** One good answer follows. The trusted smith has a big rounded rectangle for a body (square family, stable and on your side), round forearms and head (circle), and small rounded details such as a round apron buckle. Check that the outline's sharpest corner stays at or above 75°. The corrupted smith keeps the rectangle body so players recognize him, flips the base so the shoulders are wider than the feet (powerful, unstable), and adds triangular extremities: shoulder spikes, a pointed hood, a jagged hammer head. Check that the sharpest outward corner falls to 65° or less. Because the player learned to trust this silhouette, add a second channel for the change: a value shift (darker body, light rim), a sound and a wind-up pose.

A strong answer also says which shapes are the same between versions (the body block) so the player sees one character changed, not a new enemy.
</details>

## Week 3 · Silhouette readability

9. *Week 3 · compute.* Two aligned silhouettes have 110 and 96 filled pixels and share 84.
   (a) What is their IoU? Does the pair meet the 0.75 target?
   (b) The artist adds a 10-pixel hat to the first one only, outside the second mask. New IoU?
   (c) Instead, the same 10-pixel hat is added to both, in the same place. New IoU? What does the comparison teach?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 0.689, which passes. (b) 0.636. (c) 0.712. Parts one character owns lower IoU; parts two characters share raise it.

(a) Union `= 110 + 96 − 84 = 122`. `IoU = 84 / 122 = 0.689`.

(b) The hat joins the union only: `84 / 132 = 0.636`.

(c) The hat joins both intersection and union: `94 / (120 + 106 − 94) = 94 / 132 = 0.712`. Shared cosmetics make a roster more alike. That is why the lecture's MMO policy reserves a class-defining zone that cosmetics may not cover.
</details>

10. *Week 3 · compute.* Use the lecture's roster masks. The cleric gets the robe from Fix 1 (98 pixels). The rogue loses its dagger entirely, leaving the bare 70-pixel body.
   (a) What are the intersection, union and IoU at full size?
   (b) The lecture's table gives cleric and rogue at half size after Fix 1 as 0.769. Why does removing the dagger not change that number?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Intersection 70, union 98, IoU 0.714. (b) At half size the dagger had already vanished, so the rogue was the bare body either way.

(a) The robe spans columns 2 to 9 over the leg rows, which covers the legs at columns 4 to 7. So the bare body sits inside the robed cleric. Intersection 70, union 98, `70 / 98 = 0.714`. It passes at full size.

(b) Section 2 showed the dagger straddles four 2 × 2 blocks and supplies too little to any empty block to reach the half-full rule. At half size the rogue is 20 pixels, the base body, with or without the dagger. A detail smaller than the shrink factor is not part of the silhouette at that size, so the pair still fails the 0.75 target when small.
</details>

11. *Week 3 · analysis.* The mage's staff is 1 pixel wide at column 10 and runs from row 3 to row 18.
   (a) At half size (2 × 2 blocks from (0, 0), filled when at least 2 of 4 pixels are filled), how many pixels does the staff keep?
   (b) At quarter size (4 × 4 blocks, filled at 8 of 16), what is left of it?
   (c) At quarter size, how does the whole mage compare with the bare 70-pixel body?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 7 pixels. (b) Nothing. (c) They are identical, 4 pixels each.

(a) Column 10 falls in block column 5 (columns 10 and 11). A block row covers two pixel rows. Rows 4 and 5, 6 and 7, and so on up to 16 and 17 each give the block 2 of 4 pixels, which survives: 7 blocks. The end blocks (rows 2 and 3, rows 18 and 19) hold only one staff pixel each and drop.

(b) A 4 × 4 block holding one staff column gets at most 4 of 16 pixels, half of what it needs.

(c) The hat and the staff are both thinner than the block, so both vanish, and the quarter-size mage is the same 4-pixel shape as the bare body. At that size every class that relies on thin extras becomes the same class. To keep the staff, make it at least 3 pixels wide (the lecture's rule of shrink factor minus 1) or give the mage a proportion change instead.
</details>

12. *Week 3 · critique.* Two classes in your roster score IoU 0.70, under the target, yet playtesters confuse them in 40% of one-second glances. Every pixel that differs between them sits in the boots and the bottom of a cape. Explain the result and propose one extra check and one design fix.

<details>
<summary>Answer and worked solution</summary>

**Answer.** IoU weighs every pixel equally, and people do not. Players read heads, weapons and the top of the outline first, the way chess players read the tops of the pieces, so a 30% difference at the feet may never be looked at. Run IoU on the top third of each mask as a second check (lab 03's stretch). Fix the pair by moving identity to where the eye goes: a hat, a shoulder shape or a weapon held high, at least as wide as the shrink factor at the smallest size players see.
</details>

## Week 4 · Color theory: hue, saturation, value

13. *Week 4 · compute.* Convert (200, 120, 40) to HSV by hand. Then compute its L* and say how far it sits below the gray at the same HSV V.

<details>
<summary>Answer and worked solution</summary>

**Answer.** H 30°, S 80%, V 78.4%. L* 57.9, which is 22.7 below the ceiling gray (200, 200, 200) at L* 80.6.

`r = 0.784`, `g = 0.471`, `b = 0.157`. `hi = 0.784` (red), `lo = 0.157`, `C = 0.627`. `V = 78.4%`, `S = 0.627 / 0.784 = 80%`. Red leads, so `H = 60 × ((g − b)/C mod 6) = 60 × (0.314 / 0.627) = 60 × 0.5 = 30°`. The ceiling rule says every color at V 78.4% sits at or under the gray (200, 200, 200). This orange sits 22.7 under it.
</details>

14. *Week 4 · compute.* Convert `H = 200°, S = 60%, V = 80%` to RGB by hand with the lecture's sector rule. Give the hex code and L*.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (82, 163, 204), `52A3CC`, L* 63.6.

`C = 0.8 × 0.6 = 0.48`. `H/60 = 3.333`, `3.333 mod 2 = 1.333`, `|1.333 − 1| = 0.333`, so `X = 0.48 × 0.667 = 0.32`. 200° is in the 180° to 240° sector, `(0, X, C) = (0, 0.32, 0.48)`. `m = 0.8 − 0.48 = 0.32`, giving `(0.32, 0.64, 0.80)`. Times 255: `(81.6, 163.2, 204)`, rounded `(82, 163, 204)`.
</details>

15. *Week 4 · analysis.* Team colors are pure red and pure blue at S = V = 100%, and the lecture's ceiling table puts them 20.9 apart in L*. The art lead wants both teams to read at the same value.
   (a) Keeping red at S = 100%, what HSV V brings it down to blue's L* of 32.3?
   (b) Why can't you meet in the middle by making the blue lighter at S = 100%?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) About V = 62%, which gives (158, 0, 0) at L* 32.4. (b) Blue at S = V = 100% is already as light as a fully saturated blue can be.

(a) L* rises with V at fixed H and S, so bisect V. V = 61.8% rounds to (158, 0, 0), L* 32.4. The red becomes a deep maroon.

(b) By the ceiling rule, V = 100% is the top of the V slider, and a saturated blue sits 67.7 under the white ceiling there. The only way to lighten it is to lower S, which pales it. So the choice is a dark red and a saturated blue, or a light red and a pale blue. The lecture's Team Fortress 2 example makes the same point. A naive red and blue swap would make one team read darker on the same map.
</details>

16. *Week 4 · design.* Two factions use a green `H 120°, S 70%, V 80%` and a purple `H 280°, S 70%, V 80%`. Compute both L* values. Then give two ways to put them at the same value, with numbers, and say which one you would pick for faction banners seen across a dark field.

<details>
<summary>Answer and worked solution</summary>

**Answer.** Green (61, 204, 61) is L* 72.6, purple (156, 61, 204) is L* 45.3, a gap of 27.3. Fix 1: lighten the purple. Even at V = 100% it only reaches (196, 77, 255), L* 56.4, so keep V at 100% and lower S to about 40.7%, giving (220, 151, 255) at L* 72.6, a pale lilac. Fix 2: darken the green to V ≈ 48.5%, giving (37, 124, 37) at L* 45.6.

On a dark field the banners need to separate from the ground, so the light pair (Fix 1) wins: both banners at L* 72.6 sit far above a dark ground and still differ in hue for identity. The cost is a purple that is no longer saturated. The ceiling rule decides that trade, because a light, saturated purple does not exist.
</details>

17. *Week 4 · critique.* A UI artist shows a locked ability by desaturating its blue icon (0, 0, 255) from S = 100% to S = 0%, keeping V = 100%. Compute L* at S = 100%, 50% and 0%. What went wrong, and what should "locked" do instead?

<details>
<summary>Answer and worked solution</summary>

**Answer.** L* goes 32.3, then 59.2 at (128, 128, 255), then 100 at white. The locked icon becomes the brightest thing on the bar. "Locked" should lower value as well, for example a mid-dark gray near L* 32 such as (76, 76, 76), or a dimmed icon with a lock symbol.

By the ceiling rule, lowering S moves a color toward the gray at its own V, and at V = 100% that gray is white. Desaturation is not darkening. The fix keeps the lock readable as "inactive" by removing hue and adding no weight, and a shape (the lock glyph) carries the meaning for players who cannot see the hue change.
</details>

## Week 5 · Palettes and color harmony

18. *Week 5 · compute.* Use `lerp_hue(a, b, t) = a + d × t` with `d = ((b − a + 180) mod 360) − 180`, taken mod 360.
   (a) Compute `lerp_hue(330, 60, 0.25)` and `lerp_hue(60, 330, 0.25)`.
   (b) Compute `lerp_hue(100, 280, 0.5)` and `lerp_hue(280, 100, 0.5)`. What is special about this pair, and what should a palette tool do about it?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 352.5° and 37.5°. (b) 10° and 190°. The ends are exactly opposite, so both ways round are equally short, and the formula's tie rule sends the two calls to opposite sides of the wheel.

(a) `d = ((60 − 330 + 180) mod 360) − 180 = (−90 mod 360) − 180 = 270 − 180 = 90`, so `330 + 22.5 = 352.5`. The other way, `d = (450 mod 360) − 180 = −90`, so `60 − 22.5 = 37.5`. Both travel through red at 0°.

(b) `d = (360 mod 360) − 180 = −180` for the first, giving `100 − 90 = 10°` (through red). For the second, `d = (0 mod 360) − 180 = −180`, giving `280 − 90 = 190°` (through cyan). A ramp between complements has no short way. The tool should ask which way to go, or the artist should move one end a few degrees so the shorter path is the one they want.
</details>

19. *Week 5 · compute.* A zone's base hue is 250° (blue-violet).
   (a) List the hues for the analogous, complementary, split-complementary, triadic and tetradic schemes.
   (b) The zone is analogous around 250°. Which scheme hue would you reserve for loot, and what does week 4's ceiling rule say about its value?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Analogous 220°, 250°, 280°. Complementary 250°, 70°. Split-complementary 250°, 40°, 100°. Triadic 250°, 10°, 130°. Tetradic 250°, 340°, 70°, 160°. (b) The complement, 70° (a yellow-green), is the strongest hue contrast with the zone, and it sits close to its ceiling, so it can be both saturated and light.

(a) All angles mod 360: `250 + 180 = 430 → 70`, `250 + 150 = 400 → 40`, `250 + 210 = 460 → 100`, `250 + 120 = 370 → 10`, and so on.

(b) Hues near yellow lose little L* at full saturation (yellow is 2.9 below the ceiling). A light, saturated loot color stands out on the zone's blues in hue and can also be placed far above them in value. Check it against the zone's large light areas with week 1's ΔV before you commit, and never use it for decoration.
</details>

20. *Week 5 · compute.* A lava ramp has five steps: `H_shadow = 350°`, `H_light = 50°`, `S_mid = 80%`, `S_end = 50%`, `V` from 25% to 95%.
   (a) Compute H, S and V for the middle step (t = 0.5), then its RGB and hex by hand.
   (b) The five steps have L* 16.8, 27.1, 40.2, 63.7 and 88.2. Which neighbour gap is weakest, and what would you change?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) H 20°, S 80%, V 60%, RGB (153, 71, 31), hex `99471F`, L* 40.2. (b) The two darkest steps are only 10.3 apart, right at the merge line. Lower `V_dark` or use `even_ramp` to spread the dark end.

(a) `d = ((50 − 350 + 180) mod 360) − 180 = 240 − 180 = 60`, so `H = 350 + 30 = 380 mod 360 = 20°`. `|2t − 1| = 0`, so `S = S_mid = 80%`. `V = 25 + 70 × 0.5 = 60%`. Then `C = 0.48`, `H/60 = 0.333`, `X = 0.48 × (1 − |0.333 − 1|) = 0.16`, sector 0° to 60° gives `(C, X, 0)`, `m = 0.12`, so `(0.60, 0.28, 0.12) × 255 = (153, 71, 31)`.

(b) The gaps are 10.3, 13.1, 23.5 and 24.5. The dark end crowds because the shadow hue (350°, a red) sits far under its ceiling and the ends also have lower saturation. A 5-step ramp spanning 71 points of L* could have even steps of about 18. Solve V per step for L* targets of 16.8, 34.6, 52.5, 70.4, 88.2, lowering S only where the ceiling forces it.
</details>

21. *Week 5 · critique.* A student builds an "ice" ramp with `H_shadow = 200°` and `H_light = 250°` (the light end moves toward blue), `S_mid = 75%`, `S_end = 40%`, `V` 20% to 95%, four steps. The steps come out at L* 17.1, 29.7, 37.5 and 65.2. Swapping the two ends (shadow 250°, light 200°) gives 13.0, 23.7, 46.1 and 81.0. Critique the first ramp with numbers and explain the difference with week 4's ceiling rule.

<details>
<summary>Answer and worked solution</summary>

**Answer.** The first ramp's middle gap is 7.8, under 10, so two shading bands merge, and its total range is only 48.1. The swapped ramp has gaps of 10.7, 22.4 and 34.9 and a range of 68.0. Moving the light end toward blue fights the ceiling. Blue sits furthest under it, so the lighter steps lose the L* their V should give them.

The shift direction also contradicts the lecture's default (light goes warm, shadow goes cool). An ice zone can justify cool light, but then keep the shift small in the light steps, or raise S less there, and recheck the grayscale strip. Value steps come first; the hue shift must not undo them.
</details>

## Week 6 · Pixel art fundamentals

22. *Week 6 · compute.* Give the runs, the period and the angle of three lines: 14 × 6, 16 × 6 and 18 × 6. Which would you allow on a building edge?

<details>
<summary>Answer and worked solution</summary>

**Answer.** 14 × 6: runs 2, 2, 3, 2, 2, 3, period 3, 23.20°. 16 × 6: runs 2, 3, 3, 2, 3, 3, period 3, 20.56°. 18 × 6: runs 3, 3, 3, 3, 3, 3, period 1, 18.43°. Only 18 × 6 is clean, the 3 : 1 slope.

For 14 × 6, `w/h = 2.333`. The floors of `2.333k` for `k = 0 … 6` are 0, 2, 4, 7, 9, 11, 14, so the runs are 2, 2, 3, 2, 2, 3. `gcd(14, 6) = 2` gives `p = 6 / 2 = 3`: a wobbly line (it is a 7 : 3 line drawn twice). For 16 × 6 the floors of `2.667k` are 0, 2, 5, 8, 10, 13, 16, `gcd = 2`, `p = 3`. For 18 × 6, `w/h = 3` exactly, so every run is 3. A building edge is long and the eye follows it, so use the clean line.
</details>

23. *Week 6 · code.* What does this print? Explain the last line in terms of the run formula.

```python
from math import atan2, degrees, floor, gcd

def runs(w, h):
    return [(k + 1) * w // h - k * w // h for k in range(h)]

def period(w, h):
    return h // gcd(w, h)

for w, h in [(6, 4), (16, 4), (13, 4)]:
    print(w, h, runs(w, h), period(w, h), f"{degrees(atan2(h, w)):.2f}")

def pixel_widths(scale, n):
    return [floor((i + 1) * scale) - floor(i * scale) for i in range(n)]

print(pixel_widths(1366 / 320, 8))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
6 4 [1, 2, 1, 2] 2 33.69
16 4 [4, 4, 4, 4] 1 14.04
13 4 [3, 3, 3, 4] 4 17.10
[4, 4, 4, 5, 4, 4, 4, 5]
```

6 × 4 is a 3 : 2 line, steady with alternating runs. 16 × 4 is the clean 4 : 1 line. 13 × 4 is wobbly: `gcd(13, 4) = 1`, so the pattern never repeats inside the line. The last line is the run formula with `scale = 4.269` in place of `w/h`. A 320-pixel game on a 1366-pixel-wide screen draws its art pixels 4 or 5 screen pixels wide, so one column in four is 25% wider. That is a mixel pattern across the whole screen.
</details>

24. *Week 6 · compute.* A pixel game renders internally at 320 × 180.
   (a) What scale does a 2560 × 1440 monitor give? Is it safe?
   (b) What scale does a 1366 × 768 laptop give? What should the game do, and how big is the border?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 8 in both directions, an integer, so safe. (b) 4.27 in both directions, not an integer. Scale by 4 to 1280 × 720 and letterbox: 86 pixels of border across (43 each side) and 48 down (24 top and bottom).

`2560 / 320 = 8`, `1440 / 180 = 8`. `1366 / 320 = 4.269`, `768 / 180 = 4.267`. The largest whole number that fits is 4, giving `320 × 4 = 1280` and `180 × 4 = 720`. `1366 − 1280 = 86` and `768 − 720 = 48`. The alternative of stretching to fill gives art pixels of 4 and 5 screen pixels, as question 23 shows.
</details>

25. *Week 6 · analysis.* Two hand-drawn lines are each 10 pixels wide and 4 tall. Line A has runs 2, 2, 4, 2. Line B has runs 3, 3, 2, 2. Is either one a correct pixel line? What should each be?

<details>
<summary>Answer and worked solution</summary>

**Answer.** Neither. Both should be 2, 3, 2, 3.

The model allows only runs of `floor(w/h) = 2` or one more, 3, spread evenly. Line A has a run of 4, two more than the shortest run, which the formula never produces, so it is a jaggy. Line B uses only legal lengths but bunches the long runs at the start, so the line bends partway along. The correct pattern from `floor(2.5k)` for `k = 0 … 4` is 0, 2, 5, 7, 10, giving 2, 3, 2, 3 with period 2, a steady line at 21.80°.
</details>

## Week 7 · Tilesets and seamless tiling

26. *Week 7 · compute.* A map (1 is path, 0 is grass, rows and columns from 0):

```
0 0 0 0 0 0
0 1 1 1 1 0
0 1 1 0 1 0
0 1 0 0 1 0
0 0 0 0 0 0
```

Give the edge index `1·N + 2·E + 4·S + 8·W`, the raw blob value and the blob index after the corner rule for cells (1, 2), (1, 3) and (2, 2).

<details>
<summary>Answer and worked solution</summary>

**Answer.** (1, 2): edge 14, raw 116, blob 116. (1, 3): edge 10, raw 108, blob 68. (2, 2): edge 9, raw 227, blob 193.

(1, 2): E, S and W are path, so `2 + 4 + 8 = 14`. Raw blob: E 4, S 16, SW 32, W 64 = 116. The only corner, SW, has both S and W filled, so it stays.

(1, 3): E and W are path, `2 + 8 = 10`. Raw: E 4, SE 8, SW 32, W 64 = 108. SE needs E and S, and S is grass, so clear 8. SW needs S and W, so clear 32. Blob 68, a horizontal straight. The diagonal path cells below do not change this tile.

(2, 2): N and W are path, `1 + 8 = 9`. Raw: N 1, NE 2, SW 32, W 64, NW 128 = 227. NE needs N and E (E is grass), clear it. SW needs S and W (S is grass), clear it. NW has N and W, keep it. `1 + 64 + 128 = 193`, an elbow with a filled inside corner.
</details>

27. *Week 7 · compute.* A 4 × 4 tile has these L* values:

```
30 40 50 40
40 50 60 50
50 60 70 60
60 70 80 70
```

Compute `d_in`, `d_wrap` and the seam ratio. Does it pass? Where is the seam, and how would you fix it?

<details>
<summary>Answer and worked solution</summary>

**Answer.** `d_in = 10`, `d_wrap = 20`, ratio 2.0, which fails the 1.5 mark. The seam runs horizontally, where the bottom row (60 to 80) meets the next copy's top row (30 to 50).

Inside, every horizontal neighbour pair differs by 10 (12 pairs) and every vertical pair by 10 (12 pairs), so `d_in = 10`. Across the wrap, the right column against the left differs by 10 in all 4 rows, and the bottom row against the top differs by 30 in all 4 columns. `d_wrap = (4 × 10 + 4 × 30) / 8 = 20`. The rows already go up and come back down, so the horizontal wrap is fine. The tile brightens by 30 from top to bottom and never returns, a vertical gradient. Make the bottom rows fall back toward the top row's values, then run the offset test again.
</details>

28. *Week 7 · compute.*
   (a) A corner set where each corner can be one of 5 terrains: how many tiles unlayered, and how many if you layer 16-tile corner sets with the bottom terrain as a plain fill?
   (b) Of the 47 blob tiles, how many have exactly two edges filled? Explain the count.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `5^4 = 625` unlayered. Layered, `4 × 16 + 1 = 65`. (b) 10: the 2 straights and 8 elbow versions.

(b) Two filled edges are either opposite (N and S, or E and W, 2 patterns) or adjacent (4 patterns). A straight has no live corner, so 1 tile each. An elbow has one live corner between its two edges, filled or empty, so 2 tiles each. `2 + 4 × 2 = 10`. The corner rule is what makes the elbows double: a corner matters only between two filled edges.
</details>

29. *Week 7 · design.* Choose the edge, corner or blob rule for each feature and give one reason: (a) a top-down castle wall one tile thick with inside corners; (b) the shore where large lava pools meet rock; (c) a wooden fence.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Blob, 47 tiles. Only the blob rule draws a one-tile-wide line and correct inside corners. (b) Corner set, 16 tiles. It gives soft, rounded transitions between large areas and the pools never need a one-tile-wide feature. (c) Edge set, 16 tiles. A fence is a line, and the edge rule draws lines, turns, T junctions and crossings with no inside corners to worry about.

A strong answer adds the cost. The blob set is almost three times the drawing, and a top-down wall lit from one side usually cannot be mirrored to save work.
</details>

## Week 8 · Sprite animation: frames and timing

30. *Week 8 · code.* What does this print? Name the phase the player sees at tick 20.

```python
DRAWINGS = ["crouch", "rise", "peak", "slam", "shake", "lift", "settle"]
PHASE = ["windup", "windup", "windup", "active", "recovery", "recovery", "recovery"]
HOLDS = [3, 6, 9, 3, 3, 6, 12]

starts, t = [], 0
for h in HOLDS:
    starts.append(t)
    t += h

def drawing_at(tick):
    tick %= t
    for i in reversed(range(len(HOLDS))):
        if tick >= starts[i]:
            return DRAWINGS[i]

sums = {}
for h, p in zip(HOLDS, PHASE):
    sums[p] = sums.get(p, 0) + h
print(t, round(t * 1000 / 60, 1), sums)
print(drawing_at(20), drawing_at(29), drawing_at(45))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
42 700.0 {'windup': 18, 'active': 3, 'recovery': 21}
slam lift rise
```

The starts are 0, 3, 9, 18, 21, 24, 30. Tick 20 falls in `18 ≤ 20 < 21`, *slam*, the active phase. Tick 29 falls in `24 ≤ 29 < 30`, *lift*. Tick 45 wraps: `45 mod 42 = 3`, the first tick of *rise*. The windup of 18 ticks (300 ms) is the player's warning; the 21-tick recovery is the punish window.
</details>

31. *Week 8 · compute.* An 8-drawing walk covers two steps of 32 pixels each per cycle.
   (a) The character moves at 128 pixels per second. How many ticks is the cycle, and what holds would you use?
   (b) The designer changes the speed to 100 pixels per second. What goes wrong, and what are your two options?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `T = 64 / 128 = 0.5` s, 30 ticks. Holds `[4, 4, 4, 3, 4, 4, 4, 3]`. (b) `T = 0.64` s is 38.4 ticks, not a whole number. Round to 38 ticks and the feet imply 101.1 px/s, a 1% slide, or ask for a speed the cycle divides into, or scale playback speed with movement speed.

(a) `d = 2 × 32 = 64`. `30 / 8 = 3.75`, so six holds of 4 and two of 3, with the short holds on the passing positions as in the lecture.

(b) `64 / 100 = 0.64` s and `0.64 × 60 = 38.4`. At 38 ticks the cycle is 0.633 s, so the feet move at `64 / 0.633 = 101.1` px/s against a body at 100. At 39 ticks it is 98.5 px/s. A 1% slide is small on a short walk and visible on a long, straight one. The clean fix comes from `T = d / v`: speeds of 96, 120 or 128 px/s give whole-tick cycles of 40, 32 and 30 ticks.
</details>

32. *Week 8 · compute.*
   (a) You export holds `[1, 1, 1, 4, 4]` ticks to a tool that stores whole milliseconds. What do you type for each drawing, and how far does the total drift from the planned length?
   (b) In Godot 4, an animation's speed is 15 fps and the relative durations are `[1, 1, 2, 4, 1, 3]`. Give each drawing's time in ticks and the total in ms. What changes at a playback speed of 1.5?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 17, 17, 17, 67, 67 ms, total 185 ms against a planned 183.3 ms, 1.7 ms long. (b) Holds of 4, 4, 8, 16, 4 and 12 ticks, 48 ticks, 800 ms. At playback speed 1.5 the total is 32 ticks, 533.3 ms.

(a) One tick is 16.67 ms and four ticks are 66.67 ms. Each rounds up, so the error adds instead of cancelling. Holds that are multiples of 3 ticks avoid it.

(b) Godot's rule is relative duration divided by (speed × playback speed). At 15 fps one unit is `1/15` s, 66.7 ms, exactly 4 ticks. `4 × (1 + 1 + 2 + 4 + 1 + 3) = 48` ticks, `48 × 1000 / 60 = 800` ms. At playback speed 1.5 each unit is `1 / 22.5` s, so the total is `12 / 22.5 = 0.533` s, 32 ticks.
</details>

33. *Week 8 · critique.* An animator turns the lecture's light swing (holds `[1, 1, 2, 5, 4, 5]`) into a heavy swing by holding the *strike* drawing for 14 ticks instead of 5, leaving every other hold alone. Give the new phase sums and total, say why it will not read as heavy, and propose a heavy timing that keeps the total under 40 ticks. Use the lecture's Guilty Gear Strive data in your reasoning.

<details>
<summary>Answer and worked solution</summary>

**Answer.** New sums: windup 4, active 14, recovery 9, total 27 ticks (450 ms). It reads as a jab that freezes, not a heavy blow. The lecture's frame data for Sol Badguy (Dustloop, September 2026) gives the standing heavy slash fewer active frames than the standing punch (4 against 5) and puts the extra time into startup and recovery. Weight lives in the windup and recovery, plus hitstop on impact.

One heavy timing: `[2, 4, 6, 4, 8, 12]`, windup 12, active 4, recovery 20, total 36 ticks (600 ms). The windup triples, the active phase stays within 2 ticks of the light one (lab 08's rule 6), and the long *settle* hold carries the weight. Hitstop can add a freeze on the strike drawing only when the hit lands.
</details>

## Week 9 · Composition and leading the eye

34. *Week 9 · compute.* A cave thumbnail, 5 columns by 4 rows (row 0 at the top), has a glowing crystal (90) at row 1, column 2 and a wall lantern (75) at row 2, column 4:

```
30 30 30 30 30
30 30 90 30 30
30 30 30 30 75
15 15 15 15 15
```

Compute the local contrast `C` of the crystal and the lantern by hand, then `H`. Which reading does the scene get?

<details>
<summary>Answer and worked solution</summary>

**Answer.** Crystal `C = 60`, lantern `C = 51`, `H = 1.18`, two competing focal points.

The crystal's eight neighbours are all 30, so `C = |90 − 30| = 60`. The lantern sits on the right edge, so it has five neighbours: (1, 3) 30, (1, 4) 30, (2, 3) 30, (3, 3) 15, (3, 4) 15. Mean `120 / 5 = 24`, so `C = |75 − 24| = 51`. The lantern does not touch the crystal (they are two columns apart), so it is the rival. `H = 60 / 51 = 1.18`, under 1.5. The lantern sits next to the darkest band of the frame, which is why it scores almost as high as the brighter crystal.
</details>

35. *Week 9 · code.* The lecture's `contrast_map` and `focal` functions are unchanged. What do these lines print?

```python
cave = [[30, 30, 30, 30, 30],
        [30, 30, 90, 30, 30],
        [30, 30, 30, 30, 75],
        [15, 15, 15, 15, 15]]
print(focal(cave))
cave[2][4] = 45
print(focal(cave))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
((1, 2), 60, (2, 4), 51, 1.18)
((1, 2), 60, (2, 4), 21, 2.86)
```

The first line is question 34. With the lantern at 45 its neighbour mean is still 24, so `C = 21`, and `H = 60 / 21 = 2.86`. This is scene D from the lecture in a new room. Keep the lantern, lower its value, and it becomes a supporting accent.
</details>

36. *Week 9 · analysis.* In the cave of question 34, what is the brightest lantern value that still gives the crystal `H ≥ 1.5`? Could brightening the crystal alone fix the scene instead?

<details>
<summary>Answer and worked solution</summary>

**Answer.** 64. Brightening the crystal alone cannot fix it.

The rival must have `C ≤ 60 / 1.5 = 40`, so `|V − 24| ≤ 40`, which means `V ≤ 64`. At 64, `H = 60 / 40 = 1.5` exactly, and at 65 it drops to 1.46. Changing the lantern does not touch the crystal's neighbourhood (they are two columns apart), and no other cell climbs above 40. The crystal can reach at most `C = |100 − 30| = 70`, and `70 / 51 = 1.37`, still competing. As in the lecture's scene C, you win hierarchy by quieting the rival, not by shouting louder.
</details>

37. *Week 9 · critique.* To "frame" the crystal, an artist paints the whole top row of the cave in question 34 a bright 85, leaving the lantern at 75. Predict the crystal's new `C` and what happens to the focal point. Would a dark top row of 10 have worked better?

<details>
<summary>Answer and worked solution</summary>

**Answer.** The crystal drops to `C = 39.4` and the lantern (51) becomes the focal point, with `H = 51 / 39.4 = 1.30` in the wrong direction. A dark top row lifts the crystal to 67.5 and keeps it focal, but `H` is still only about 1.3, so the lantern must still come down.

With the bright row, the crystal's neighbours are three cells of 85 and five of 30, mean `405 / 8 = 50.6`, so `C = |90 − 50.6| = 39.4`. The frame raised the neighbour mean and ate the crystal's contrast. With a dark row of 10, the mean is `180 / 8 = 22.5` and `C = 67.5`. Framing works when the frame contrasts with the target, as the lecture's dark archway does. A frame of the same value as the target hides it.
</details>

## Week 10 · Readability in chaos: VFX and telegraphing

38. *Week 10 · compute.* A floor has value 40. Each overlapping player effect adds 8 points. The telegraph has an additive fill of `t = 30` and a black rim at `α = 0.6`.
   (a) At how many overlapping effects does the fill alone fail the 20 threshold?
   (b) What is the rim's contrast with no effects, and does it pass?
   (c) What is the two-tone worst case?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 6 effects. (b) 24, a pass. (c) 30.

(a) The fill fails when the headroom `100 − B` is under 20, so when `B > 80`. `B = 40 + 8N`: at `N = 5`, `B = 80` and the headroom is exactly 20, a pass. At `N = 6`, `B = 88` and the fill contrast is 12.

(b) `α × B = 0.6 × 40 = 24`.

(c) `min(t, 100α / (1 + α)) = min(30, 60 / 1.6) = min(30, 37.5) = 30`. The fill sets the worst case here, so the pair never drops below 30 at any background.
</details>

39. *Week 10 · design.* Your telegraph fill adds `t = 45`. What is the lowest rim opacity `α` that guarantees a two-tone worst case of at least 35? What would you change if you needed 50?

<details>
<summary>Answer and worked solution</summary>

**Answer.** `α ≥ 0.54`. A worst case of 50 needs both `t ≥ 50` and `α ≥ 1`, so raise the fill to at least 50 and use a fully opaque rim.

`100α / (1 + α) ≥ 35` gives `100α ≥ 35 + 35α`, `65α ≥ 35`, `α ≥ 0.538`. For 50, the rim term needs `100α / (1 + α) ≥ 50`, so `α ≥ 1`, the most a rim can give, and the fill term needs `t ≥ 50`. At that point the design is at the limit of the model. A thicker rim or a second dark band inside the fill buys margin that the formula does not show.
</details>

40. *Week 10 · analysis.* Instead of an additive fill, an artist draws the telegraph as a white disk at 50% alpha ("over" blending). Using the lecture's definition of alpha blending, write its contrast against a background of value `B`, and compute it for `B` = 30, 70 and 100. Which part of the lecture's model does it behave like?

<details>
<summary>Answer and worked solution</summary>

**Answer.** Contrast `= 0.5 × (100 − B)`: 35 at `B = 30`, 15 at `B = 70` (fails), 0 at `B = 100`. It behaves like the additive fill, limited by headroom, only worse, because it loses half its contrast at every background.

A 50% white over `B` leaves `0.5 × B + 0.5 × 100`, which is `0.5 × (100 − B)` above the background. Any light-only signal, whatever its blend mode, shrinks as the background brightens and dies at white. The lecture's fix still applies: add a dark part, so one half of the signal always has contrast.
</details>

41. *Week 10 · critique.* A night-zone boss uses a rim-only telegraph (black, `α = 0.9`) because "rims survive glow". The cave floor is value 12. Compute the rim's contrast with no effects and with 8 effects of 10 points each. What does the result say about the proposal, and what is the fix?

<details>
<summary>Answer and worked solution</summary>

**Answer.** With no effects the rim gives `0.9 × 12 = 10.8`, a fail. With 8 effects, `B = 92` and the rim gives 82.8. The rim-only design fails exactly when the fight is quiet. Add a light fill. With `t = 40`, the fill gives `min(40, 88) = 40` on the empty floor, and the pair covers both cases.

This is the lecture's point that the two styles fail in opposite conditions. The high-visibility vest in the lecture carries both fluorescent fabric and reflective bands for the same reason.
</details>

## Week 11 · UI visual hierarchy

42. *Week 11 · compute.* An item tooltip sits on a dark panel of L* 12. From least to most important: sell price (s 0.8, L* 75), flavor text (s 0.9, L* 45), other stats (s 0.9, L* 70), "can equip" line (s 1.0, L* 60), the changed stat (s 1.0, L* 80), item name (s 1.4, L* 95). Use `W = s² × ΔV`.
   (a) Compute the six weights.
   (b) Count inversions and list the weak steps (ratio under 1.5).

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 40.3, 26.7, 47.0, 48.0, 68.0, 162.7. (b) 1 inversion (sell price over flavor). Weak steps: flavor over price 0.66, "can equip" over stats 1.02, changed stat over "can equip" 1.42.

(a) Price `0.64 × 63 = 40.32`. Flavor `0.81 × 33 = 26.73`. Stats `0.81 × 58 = 46.98`. Equip `1 × 48 = 48`. Changed stat `1 × 68 = 68`. Name `1.96 × 83 = 162.68`.

(b) Only the price outweighs something above it. The steps are 0.66, 1.76, 1.02, 1.42 and 2.39. The middle of the tooltip is flat. Stats, "can equip" and the changed stat read as one level in a squint. Dim the price, and push the changed stat up with a plate or size so it clears 1.5 over "can equip".
</details>

43. *Week 11 · critique.* The same tooltip gets an ornate border of area 6 (in body-text lines) at L* 40 on the L* 12 panel. The designer calls it "decoration, lowest importance". Compute its weight and the new inversion count, and say what the lecture recommends.

<details>
<summary>Answer and worked solution</summary>

**Answer.** Weight `6 × 28 = 168`, heavier than the item name (162.7). As the least important element it now outweighs all six others, so the inversions rise from 1 to 7.

Borders, frames and background art spend the weight budget. The lecture's rule is to keep them near the ground's value unless they carry meaning. Pulling the border to L* 18 gives `6 × 6 = 36`, below everything except the flavor text, and removes 5 of the new inversions.
</details>

44. *Week 11 · compute.* Put the six World of Warcraft quality colors from the lecture (Warcraft Wiki, current retail) as text of equal size on a stone ground of L* 60. Their L* values are Poor 64.7, Common 100.0, Uncommon 87.9, Rare 48.0, Epic 47.6, Legendary 67.1. Compute each weight and count the inversions. Which tier is almost invisible?

<details>
<summary>Answer and worked solution</summary>

**Answer.** Weights 4.7, 40.0, 27.9, 12.0, 12.4, 7.1. Inversions 9 of 15. Poor is almost invisible (ΔV 4.7), and Legendary, the top tier, has the second-lowest weight.

Common outweighs the four tiers above it (4), Uncommon outweighs Rare, Epic and Legendary (3), Rare outweighs Legendary (1) and Epic outweighs Legendary (1). On black the lecture counted 10. The code works as a category label for players who have learned it, and a mid-value ground makes it worse as a ranking. Rare, Epic and Legendary all fall under week 1's gap of 20.
</details>

45. *Week 11 · compute.* A designer picks text sizes from a modular scale with ratio 1.3 and keeps the same contrast for all levels.
   (a) What is the area step between levels? Does it pass the step rule?
   (b) With four levels, what is the weight ratio between top and bottom?
   (c) What is the smallest scale ratio that passes the step rule by size alone?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `1.3² = 1.69`, which passes 1.5. (b) `1.69³ = 4.83`. (c) `√1.5 = 1.225`.

For text of the same length, `A = s²`, so every size step is squared. Four levels at a 1.5 step need at least `1.5³ = 3.4` between top and bottom; the 1.3 scale gives 4.83, room to spare. A 1.2 scale gives 1.44 per step and fails every step, as the lecture's check yourself shows.
</details>

## Week 12 · Accessibility: color-blindness and contrast

46. *Week 12 · compute.* Use about 1 in 12 men and 1 in 200 women with color vision deficiency.
   (a) What is the chance that a party of 15 men includes at least one affected player?
   (b) A group of 20 men and 20 women?
   (c) A 40-player raid of 30 men and 10 women?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 72.9%. (b) 84.1%. (c) 93.0%.

(a) `1 − (11/12)^15 = 1 − 0.271 = 0.729`.

(b) `1 − (11/12)^20 × (199/200)^20 = 1 − 0.1755 × 0.9046 = 0.841`.

(c) `1 − (11/12)^30 × (199/200)^10 = 1 − 0.0735 × 0.9511 = 0.930`. In almost every raid, someone sees your red and green differently.
</details>

47. *Week 12 · compute.* A pale sand floor has relative luminance `Y = 0.30`.
   (a) What is the largest `Y` a dark rim can have and still reach 3:1 against it? What L* is that?
   (b) What `Y` would a lighter fill need for 3:1? What does that tell you about light telegraphs on this floor?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `Y ≤ 0.0667`, L* 31.0, while the floor is L* 61.7, a ΔV of 30.6. (b) `Y ≥ 1.0`, pure white and nothing else. On a floor this light only a dark part can pass 3:1.

(a) `(0.30 + 0.05) / (Y + 0.05) ≥ 3` gives `Y + 0.05 ≤ 0.1167`, `Y ≤ 0.0667`. `L* = 116 × 0.0667^(1/3) − 16 = 31.0`.

(b) `(Y + 0.05) / 0.35 ≥ 3` gives `Y ≥ 1.0`. A fill can still pass the course's ΔV 20 (anything above L* 81.7 does), but not the web standard. This is the week 10 headroom problem again, measured in contrast ratio.
</details>

48. *Week 12 · compute.* A green has linear RGB (0.05, 0.45, 0.06). Multiply it by the lecture's protanopia matrix (Machado, Oliveira and Fernandes, 2009, severity 1.0) and round each result to three decimals. Which channel changed most?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (0.469, 0.366, 0.041). Red rose the most, from 0.05 to 0.469.

Row 1: `0.152286 × 0.05 + 1.052583 × 0.45 − 0.204868 × 0.06 = 0.0076 + 0.4737 − 0.0123 = 0.469`. Row 2: `0.114503 × 0.05 + 0.786281 × 0.45 + 0.099216 × 0.06 = 0.0057 + 0.3538 + 0.0060 = 0.366`. Row 3: `−0.003882 × 0.05 − 0.048116 × 0.45 + 1.051998 × 0.06 = −0.0002 − 0.0217 + 0.0631 = 0.041`. The green signal spreads into red, so the color turns yellowish: the red-green difference that told it apart from a red is mostly gone.
</details>

49. *Week 12 · analysis.* A team game proposes orange (240, 140, 20) against blue (40, 90, 220). Simulated with the lecture's code, the pair's ΔV is 24.9 for typical vision, 14.7 for protanopia, 28.2 for deuteranopia and 18.6 for tritanopia, and its ΔE never falls below 87.7. A red (230, 60, 50) against a green (60, 160, 70) gives ΔV 6.4, 17.9, 0.1 and 4.9, with ΔE 16.7 for deuteranopia. Which pair would you ship as team colors, and what else must the design do?

<details>
<summary>Answer and worked solution</summary>

**Answer.** Ship orange against blue. It stays far apart in total color difference for every viewer because it runs along the blue-yellow axis that red-green viewers keep. It is not a value-safe pair, though. Protan and tritan viewers see less than 20 of value between the teams. So use it for identity only, and give detection to value and shape.

The red-green pair fails on every count for deuteranopes, ΔV 0.1 and ΔE 16.7, which the lecture's scale calls two shades of one color. For the orange and blue pair, add a shape cue (a different nameplate frame or icon per team) and make sure each team color separates from the floors it appears on, measured per viewer. This is the lecture's Splatoon lesson. The Color Lock pairs work because they separate on the axis every viewer keeps.
</details>

50. *Week 12 · critique.* A producer says: "We'll add a full-screen colorblind filter in the options menu, so the art team doesn't need to change the raid telegraphs." Give two problems with this plan and the order of fixes the lecture recommends.

<details>
<summary>Answer and worked solution</summary>

**Answer.** First, a mode only helps players who find it, and in a 20-man group about 82% of groups contain an affected player, so the default must already work. Second, the Game Accessibility Guidelines warn that full-screen filters shift every color, can make the rest of the art look wrong for the players they are meant to help, and still may not separate the colors that matter.

The order is to design value and shape first so critical pairs pass ΔV ≥ 20 in all four simulations (the two-tone telegraph and redundant shape coding), then offer a palette swap for the few gameplay colors, as Overwatch does with its enemy and friendly UI colors, and use a full-screen filter last if at all.
</details>

## Week 13 · Art style bibles

51. *Week 13 · compute.* A bible targets `D* = 128` px/m with ±25% tolerance. Compute `D = T × f × r / S`, the ratio and the verdict for four assets, then fix every failure.

| Asset | S (m) | T (px) | f | r |
|---|---|---|---|---|
| Shop sign | 1.5 | 512 | 0.25 | 1 |
| Pier planks | 10 | 512 | 1.00 | 3 |
| Crate | 0.8 | 256 | 0.50 | 1 |
| Statue | 3 | 2048 | 0.50 | 1 |

<details>
<summary>Answer and worked solution</summary>

**Answer.** Sign 85.3, ratio 0.67, fail (too blurry). Planks 153.6, ratio 1.20, pass. Crate 160.0, ratio 1.25, pass on the edge. Statue 341.3, ratio 2.67, fail (too sharp).

The band is 96 to 160, inclusive. Sign: `512 × 0.25 / 1.5 = 85.3`. Fix with a larger UV island, `f = 128 × 1.5 / 512 = 0.375` (192 texels), which gives exactly 128. Statue: `2048 × 0.5 / 3 = 341.3`. Drop to a 1024 texture and `f = 0.375`, `1024 × 0.375 / 3 = 128`, which also frees memory. The crate passes only because the tolerance is inclusive. A reviewer should flag it as the next one to drift.
</details>

52. *Week 13 · compute.* A courtyard floor is 24 m across and tiles a texture. The bible's density is 128 px/m.
   (a) How many repeats does a 1024 texture need? A 512?
   (b) The floor is changed to 20 m with the 1024 texture. Repeats must be whole. Which counts pass at ±25%?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 3 repeats of 1024, 6 of 512. (b) 2 repeats give 102.4 (ratio 0.80, pass) and 3 give 153.6 (ratio 1.20, pass).

(a) `r = D* × S / T = 128 × 24 / 1024 = 3` and `128 × 24 / 512 = 6`. Both give exactly 128; the 512 version uses a quarter of the memory and shows its repeat twice as often, which week 7's variants and decoration must then hide.

(b) `1024 × 2 / 20 = 102.4` and `1024 × 3 / 20 = 153.6`. Both pass; 2.5 repeats would hit 128 but a seamless tile must repeat a whole number of times across a face that ends at a wall. Pick the one closer to the neighbouring assets.
</details>

53. *Week 13 · analysis.* A 2D game's tiles import at 32 pixels per tile. A pet sprite drawn at the same pixel size imports at 16 pixels per tile. What does the player see, what is its density ratio, and what rule belongs in the bible?

<details>
<summary>Answer and worked solution</summary>

**Answer.** The pet renders at twice the intended size, and each of its art pixels is twice as wide as a tile pixel, which is a mixel. Its density is 16 against a target of 32, ratio 0.5, the same as scaling it by `k = 2`. The bible rule is hard, with zero tolerance for pixel art: every sprite and tile imports at the same pixels per unit, and anything that must be larger is redrawn larger.

This is the week 13 2D form (`D / k`) meeting week 14's pixels-per-unit setting. A single number in an import panel produces the same failure as a scaled sprite.
</details>

54. *Week 13 · design.* Rewrite the rule "Keep the marsh zone gloomy but readable" as a checkable rule with a property, a target, a tolerance and scope, a method, a hard or soft label and a reason.

<details>
<summary>Answer and worked solution</summary>

**Answer.** One good answer. Property: the L* of large background areas (walls, water, sky) and of gameplay figures. Target: backgrounds between L* 20 and 45; every enemy, pickup and interactable at least ΔV 20 from the ground behind it, and at least 30 for enemies. Tolerance and scope: all marsh maps, default camera, in-game lighting, areas larger than two tiles for the background rule. Method: grayscale screenshot at default camera, sample with an eyedropper or run the lab 01 checker on the listed pairs. Hard or soft: the background band is soft (a lit shrine may break it with a recorded exception); the figure gap is hard. Why: a dark background sets the mood, and a guaranteed gap keeps gameplay visible in it.

A strong answer splits "gloomy" (a soft mood rule) from "readable" (a hard gameplay rule), since the lecture sorts gameplay rules as almost always hard.
</details>

## Week 14 · Pipeline: export, atlases, import settings

55. *Week 14 · compute.* A 1024 × 512 texture of painted props.
   (a) Give its memory as RGBA8 and as BC1, with and without mipmaps (use 4/3 for mipmaps).
   (b) The zone's texture budget is 12 MiB. How many 2048 × 2048 BC7 atlases with mipmaps fit? How many RGBA8 atlases without mipmaps?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) RGBA8 2 MiB, about 2.67 MiB with mipmaps. BC1 256 KiB, about 341.3 KiB with mipmaps. (b) Two BC7 atlases (10.67 MiB). No RGBA8 atlas, since one is 16 MiB.

(a) `1024 × 512 = 524,288` texels. `× 4 = 2,097,152` bytes, 2 MiB. `× 0.5 = 262,144` bytes, 256 KiB. Mipmaps add about a third.

(b) `2048² × 1 × 4/3 = 5.33 MiB` per BC7 atlas; two fit in 12, three do not. `2048² × 4 = 16 MiB` alone breaks the budget.
</details>

56. *Week 14 · code.* What does this print? Which line shows a power-of-two cliff, and what did it buy?

```python
import math

def square_atlas(count, sprite, gutter):
    cell = sprite + 2 * gutter
    side = 1
    while (side // cell) ** 2 < count:
        side *= 2
    return side

def safe_mip(gutter):
    return "none" if gutter == 0 else str(int(math.log2(gutter)))

for count, sprite, g in [(64, 60, 2), (64, 60, 3), (64, 56, 4), (100, 30, 1)]:
    side = square_atlas(count, sprite, g)
    kib = side * side * 4 // 1024
    print(f"{count} x {sprite}px, gutter {g}: {side}x{side} {kib} KiB, safe mip {safe_mip(g)}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
64 x 60px, gutter 2: 512x512 1024 KiB, safe mip 1
64 x 60px, gutter 3: 1024x1024 4096 KiB, safe mip 1
64 x 56px, gutter 4: 512x512 1024 KiB, safe mip 2
100 x 30px, gutter 1: 512x512 1024 KiB, safe mip 0
```

The second line is the cliff. A cell of 66 fits `512 // 66 = 7` times across, 49 cells, short of 64, so the atlas doubles to 1024 and the memory quadruples. It bought nothing, since `floor(log2 3) = 1`, the same safe level as a gutter of 2. The third line is the fix from the lecture: draw at 56 inside a 64-pixel cell, which gives a real extra mip level at the old size.
</details>

57. *Week 14 · analysis.* (a) Give the safe mip level for gutters of 3, 5, 6 and 8 pixels, and the coordinate multiple each sprite must start on. (b) Why does a 3-pixel gutter protect no more than a 2-pixel one?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 3 gives level 1 (start on multiples of 2), 5 gives level 2 (multiples of 4), 6 gives level 2 (multiples of 4), 8 gives level 3 (multiples of 8). (b) Protection comes in powers of two.

At mip level `k` one texel covers `2^k` original pixels, and bilinear filtering at the sprite's edge reaches into the whole level-`k` texel outside it. That texel must be the sprite's own extruded color, so the gutter must be at least `2^k`. A 3-pixel gutter covers level 1 (2 pixels) but not level 2 (4 pixels). The third pixel costs space and adds no level. Choose gutters of 1, 2, 4 or 8.
</details>

58. *Week 14 · analysis.* Name the pipeline stage (export, pack, import or render), the cause and the fix for each report:
   (a) "Every leaf on the oak sprite has a thin dark fringe that isn't in the source file."
   (b) "The pixel-art player looks soft next to the crisp tiles."
   (c) "The walk cycle jitters up and down by a pixel since we started trimming sprites."
   (d) "Normal-mapped rocks look lit from the wrong angle, but only in the game."

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Export, with the halo appearing at import or render. The transparent pixels store black, and bilinear filtering blends it into the edges. Dilate edge colors into the transparent area, use premultiplied alpha, or use point filtering. (b) Import. The sprite uses bilinear filtering or mipmaps. Set point filtering and turn mipmaps off for pixel art. (c) Export or pack. Trimming each frame moves the pivot relative to the image corner. Trim with a tool that records offsets, or keep every frame of an animation on the same canvas. (d) Import. The normal map is flagged sRGB. Import data textures as linear, and label which files are data at export.

A strong answer adds the bible rule for each, as the lecture's in-class activity asks.
</details>

59. *Week 14 · design.* A pixel-art game shows its sprites only at integer scale and never smaller than native size. A teammate proposes 8-pixel gutters "to be safe" on the character atlas. Using the lecture's model and import settings table, give the settings you would choose, the gutter, and one reason a team might still keep a small gutter.

<details>
<summary>Answer and worked solution</summary>

**Answer.** Point filtering, mipmaps off, no lossy compression, sRGB, the same pixels per unit as the tiles. With point filtering and no mipmaps the model says a gutter of 0 is safe, so 8 pixels buys nothing and can push the atlas over a power-of-two boundary. Many teams still keep 1 or 2 pixels to absorb rounding when the camera sits between pixels.

The 8-pixel gutter protects mip level 3, which this game never uses. On the lecture's 64 sprites of 32 pixels, any gutter above 0 doubles the atlas side and quadruples its memory, from 256 KiB to 1,024 KiB.
</details>
