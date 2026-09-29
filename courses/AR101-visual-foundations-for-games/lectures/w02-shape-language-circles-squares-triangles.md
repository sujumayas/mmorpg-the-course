# AR101 · Week 02 — Shape Language: Circles, Squares, Triangles

**Why this matters:** Players decide whether to hug, block or dodge something in the first fraction of a second, and they decide from its shape. If your friendly shopkeeper is all spikes or your deadliest trap is a soft blob, you have to spend tutorial text fixing a problem that the art created.

**You will be able to:**
- Compute a shape's circularity `C = 4πA/P²` and its sharpest corner angle, and place it on the circle, square, triangle map.
- Explain why circularity alone misclassifies some shapes, and fix the reading with a second number.
- Design a character or prop whose big, medium and small shapes all say the same thing.
- Critique a shipped game's enemies and hazards by naming the shape family each one uses and what it promises.

**Before class:** Solarski, *Drawing Basics and Video Game Art* (2012), the material on the circle, square and triangle as basic shapes of character design (find it through the table of contents). Mitchell, Francke and Eng, "Illustrative Rendering in Team Fortress 2" (2007), sections 4.1 and 4.2, about one page. Ramachandran and Hubbard, "Synaesthesia: a window into perception, thought and language" (2001), the section on the bouba/kiki demonstration, about two pages.

**Prerequisites from earlier courses:** None. This is a first-semester course. It builds on [AR101 week 1, value before color](w01-seeing-like-an-artist-value-before-color.md): value tells the player *that* something is there, shape tells them *what kind of thing* it is. Later, [GD201 week 5, affordances and signposting](../../GD201-level-and-world-design/lectures/w05-affordances-and-signposting.md) uses shape as one of its signposting channels.

**Interactive:** [`examples/w02-shape-reader.html`](../examples/w02-shape-reader.html). Keep it open during section 2.

---

## 1. Shapes speak before faces do

When you look at a character, you read the outline and the biggest masses before you read the face, the costume or the weapon. Artists exploit this with **shape language**: the habit of building a design from one dominant family of simple shapes so the whole design carries one message.

There are three families.

- **Circles and curves.** Soft, safe, friendly, young, harmless. A round shape has no edges to hurt you and no corners to catch on. Babies, pets, plush toys and most cute mascots are built from circles.
- **Squares and rectangles.** Stable, solid, dependable, heavy, stubborn. A square sits flat on its base and resists being pushed. Tanks, guardians, walls, fortresses and trustworthy workers are built from rectangles.
- **Triangles and points.** Dynamic, dangerous, fast, aggressive. A point can cut, and a triangle points in a direction. Villains, spikes, blades, arrowheads and speedy characters are built from triangles.

These readings are not arbitrary. The best-known evidence is the **bouba/kiki effect**. In 1929 the psychologist Wolfgang Köhler showed people a rounded blob and a jagged star-like shape and asked which one was called "maluma" and which "takete". Most people matched the soft word to the round shape. Ramachandran and Hubbard (2001) repeated the demonstration with "bouba" and "kiki" and reported that about 95% of people call the curvy shape bouba and the jagged one kiki. A 2022 study by Ćwiek and colleagues tested 917 people speaking 25 languages with 10 writing systems and found the match held above chance across cultures, although its strength varied by language. People link round shapes with soft qualities and sharp shapes with harsh ones, fast and without being taught.

That makes shape language a strong default. It does not make it a law. Associations are partly learned, and a designer can break them on purpose (section 2 closes on when). What you should never do is break them by accident.

### Three terms

- **Silhouette** is the filled outline of a thing, as if lit from behind. Week 3 is entirely about it.
- **Primary shape** is the largest mass of a design, the one that survives when the design shrinks to a thumbnail. It carries the main message.
- **Secondary and tertiary shapes** are the medium and small shapes: limbs, hats, weapons, ornaments. They can support the primary message or add a second note ("friendly, but armed").

## 2. Worked example: why you can stomp one and not the other

### The hook

In Super Mario Bros. (Nintendo, 1985), jumping on an enemy is the main verb. A Goomba, a squat brown mushroom-like walker with a rounded cap, dies when you land on it. From World 4-1 onward a cloud-riding enemy throws Spinies at you. A Spiny's shell is covered in spikes, and landing on it hurts Mario instead. You can only defeat it with a fireball or while invincible.

No text box explains this. Players work it out anyway, usually on sight, because the spikes tell them. Round top: safe to land on. Pointed top: don't.

Can we put a number on "round top" and "pointed top"? If we can, we can check our own designs before a playtest does.

### The model: two numbers per shape

**Circularity** measures how close a shape is to a circle:

```
C = 4π × A / P²
```

- `A` is the area of the shape.
- `P` is its perimeter, the length of its outline.
- `C = 1` for a perfect circle, and it is smaller for every other shape.

Why this formula? Of all shapes with a given perimeter, the circle encloses the most area. For a circle of radius `r`, `A = πr²` and `P = 2πr`, so `4πA/P² = 4π·πr² / 4π²r² = 1`. Any corner, flat side, spike or stretch wastes perimeter and pulls `C` down. `C` does not care about size: a big square and a small square have the same `C`.

**Sharpest corner** measures how pointed the shape gets:

```
θ = the smallest interior angle at any outward-pointing corner (degrees)
```

A circle has no corners, so we record θ = 180°. A square has four 90° corners. An equilateral triangle has 60° corners. A star's tips can be much sharper. Inward-pointing corners (the notches between a star's points) are ignored, because they can't poke anyone.

**The reading map** (a course heuristic, not a standard):

| Reading | Rule | Family |
|---|---|---|
| Sharp | θ ≤ 65° | Triangle: danger, speed, aggression |
| Square | 75° ≤ θ ≤ 105° | Square: stable, solid, dependable |
| Round | C ≥ 0.85 and θ ≥ 120° | Circle: soft, friendly, safe |
| In between | anything else | Check by eye; the message is mixed |

### Numbers you can check

For a regular polygon with `n` sides, circularity simplifies to `C = π / (n × tan(π/n))`, and each corner is `180 × (n − 2) / n` degrees. For a square with rounded corners (side `s`, corner radius `r`), `A = s² − (4 − π) r²` and `P = 4s − (8 − 2π) r`. You can verify every row below with a calculator.

| Shape | C | θ (sharpest) | Reading |
|---|---|---|---|
| Circle | 1.000 | none (180°) | Round |
| Regular octagon | 0.948 | 135° | Round |
| Square, corners rounded with r = 0.25 s | 0.933 | none (180°) | Round |
| Regular hexagon | 0.907 | 120° | Round |
| Regular pentagon | 0.865 | 108° | In between |
| Square | 0.785 | 90° | Square |
| Rectangle, 2 : 1 | 0.698 | 90° | Square |
| Equilateral triangle | 0.605 | 60° | Sharp |
| Rectangle, 3 : 1 | 0.589 | 90° | Square |
| Isosceles triangle, height 3 × base | 0.376 | 18.9° | Sharp |
| Five-point star, inner radius 0.5 | 0.419 | 52.5° | Sharp |
| Five-point star, inner radius 0.38 | 0.265 | 35.7° | Sharp |

Two checks by hand. For the square, `C = π / (4 × tan 45°) = π/4 ≈ 0.785`. For the equilateral triangle, `C = π / (3 × tan 60°) = π / (3 × 1.732) ≈ 0.605`.

Now the Goomba and the Spiny, drawn as simple invented stand-ins (not the originals). Model the walker as a dome: a half-disc of radius 1 on top of a base 2 wide and 0.4 tall, with its bottom corners rounded (radius 0.15). Its outline has no sharp corners, and `C` = 0.878. Model the spiked shell as the same dome with six triangular spikes spaced evenly along the arc, each tip 0.45 beyond the arc and each base spanning 18° of it. The spikes add a lot of perimeter and little area, so `C` falls to 0.365, and each tip is about 37°. One number says "much less round". The other says "sharp". The player's rule, "don't land on the sharp one", is exactly the θ test.

### The rectangle paradox, and why you need both numbers

Look at the 3 : 1 rectangle in the table. Its circularity, 0.589, is *lower* than the equilateral triangle's. If you used `C` alone, you would call a long flat platform more dangerous than a triangle. Nobody reads a brick as a threat.

The fix is the second number. The rectangle's sharpest corner is 90°, which puts it firmly in the square family. What makes a shape read as dangerous is not how far it is from a circle, it is whether it has a *point*. `C` separates round from not-round. θ separates square from sharp. You need both, which is why the map uses both.

### A visual you can move

Open the interactive. The left panel draws one shape; the right panel wears that same shape as the body of a small invented creature, with two eyes and feet. Start with the **sides** slider at 3 and the shape reads as a threat. Slide the **corner rounding** up and watch `C` climb and θ jump to "none" as the corners dissolve. The creature goes from hostile to harmless without its face changing. Now set sides to 4 and drag **stretch** out to 3 : 1. `C` falls below the triangle's value, but the creature still looks like a sturdy block, and the reading stays "square". Finally, add **spikes**. With spikes at depth 0.5, a round body reads as sharp at once, and the readout shows why: θ drops below 60°.

### Cross-game recognition

**Team Fortress 2 (Valve, 2007).** The paper on the game's art describes the two team bases in shape terms. The red team's base uses warm colors, natural materials and *angular* geometry. The blue team's uses cool colors, industrial materials and *orthogonal* forms. Both teams are built from blocks, so in our model both sit near the square family. The difference is θ: orthogonal means every corner is 90°, and angular means some corners are sharper than that. The same paper says the characters' clothing folds were drawn to echo the silhouette shapes, so the small shapes repeat the message of the big one.

**Celeste (Maddy Makes Games, 2018).** Spikes are drawn as rows of small triangles and kill the player on contact, unless the player is moving away from them in the direction they point. That is shape language turned into a rule. A triangle has a direction, and the game makes the direction mean something. Once a player learns one spike, every triangle in the game is a warning, and its orientation tells you which way is safe.

**The bouba/kiki demonstration (1929 onward).** Outside games entirely, the same two measures separate the two classic test figures. The bouba figure is a rounded blob with high `C` and no corners. The kiki figure is a star-like shape with low `C` and tips well under 60°. The experiment is the perceptual reason the Spiny works: the brain files the jagged outline under "harsh" before it has decided what the object is.

Three contexts (a platformer from 1985, a team shooter from 2007, a psychology demonstration from 1929) and one reading: round is safe, square is solid, pointed is dangerous, and the direction of a point matters.

### Eyes-open design judgment

- **Use the defaults for anything the player must learn fast.** Hazards, enemies, safe platforms and pickups should follow the map unless you have a reason. Each follow is one fewer thing to teach.
- **Break the map on purpose, and pay for it.** A cute round creature that turns out to be deadly is a classic surprise, and it can be a great moment. It costs the player's trust in your shapes for the rest of the game. If you subvert the map, do it once, make it memorable, and give the creature a second signal (a value or color change, a sound, a wind-up) so the player can recover.
- **Mix families deliberately.** A good tank design is a big rectangle (solid) with rounded corners (on your side). A good villain might be a rectangle (powerful) with triangular details (hostile). Pick the primary family for the main message and let secondary shapes add the second note. When primary and secondary disagree strongly, players get a mixed signal.
- **Watch the scale.** At 16 pixels, a 45° spike and a 90° corner may be the same two pixels. Corners and small spikes disappear first when a design shrinks, and round and square bodies become hard to tell apart. Carry the main message in the primary shape. Week 3 measures this, and week 6 deals with it pixel by pixel.
- **Culture and genre shape the reading.** The bouba/kiki match is strong but varies by language, and genre conventions add their own meanings (a star is a reward in many games even though its shape reads sharp). Test with your real audience, and check the map against your genre's habits.

## 3. Building a design from big, medium and small shapes

A reliable way to design a readable character, creature or prop is to work from the biggest shape down.

1. **Choose the message.** One or two words: "gentle healer", "unmovable guard", "fast assassin".
2. **Choose the primary family.** Circle, square or triangle, from the map.
3. **Block the primary shape.** One large mass, roughly 60% of the design's area. Sketch at thumbnail size so you can't add detail yet.
4. **Add secondary shapes.** Two to four medium shapes (head, limbs, cloak, weapon), roughly 30% of the area, mostly in the same family.
5. **Add tertiary shapes.** Small details, roughly 10%. This is where you can put a contrasting note: a round face on a square guard, a small spike on a round pet that bites.
6. **Measure.** Trace the outer outline and compute `C` and θ (Lab 02's helper does it). Does the reading match your message?

The 60/30/10 split is a rule of thumb for variety, not a measurement from any game. Its purpose is to stop you from giving every shape the same size, which reads as monotonous, or from letting small details dominate, which reads as noise.

### Proportion and orientation

Two more properties change the reading without changing the family.

- **Base width.** A shape that is wider at the bottom (a pyramid, a trapezoid, a pear) reads as grounded and stable. A shape that is wider at the top (an inverted triangle, a big-shouldered torso on thin legs) reads as powerful but unstable, often aggressive. Heroic and villainous body types exploit this.
- **Direction.** A triangle that points forward reads as moving or attacking. A triangle that points up reads as rising, a mountain or a flame. A triangle that points down at the ground can read as a stake or a drill. Celeste's spikes use direction as a rule. Your designs can use it as a hint.

## 4. Shape and gameplay promises

Every shape makes a promise about the rules. A flat-topped rectangle promises you can stand on it. A round object promises it will roll or bounce. A pointed object promises it will hurt. When the collision box, the physics or the damage keeps that promise, players feel the game is fair. When it doesn't (a spike that doesn't hurt, a platform edge that is rounded in the art but square in the collision), players feel cheated, and they're right.

Two practical rules follow.

- **Match the art to the hitbox's shape family.** If the collision is a box, the visible object should read as a box. If it is a circle, round the art.
- **Keep shape vocabulary consistent across the game.** If triangles mean danger in world 1, they must mean danger in world 8. A shape vocabulary is a small language, and you are teaching it to the player one encounter at a time.

## In-class activity (25 minutes)

Work in groups of three. Materials: paper, a pen, a ruler or grid paper, and a phone calculator or the interactive.

1. **(10 min)** Each person draws three thumbnails of the same creature for a fantasy game: "a village guard dog". One must be circle-dominant, one square-dominant, one triangle-dominant. Keep the face and pose the same; change only the big shapes. Thumbnails 4 cm tall, no shading.
2. **(5 min)** Swap. Without being told the families, each reader labels every thumbnail with one word ("cuddly", "tough", "mean" or their own word).
3. **(5 min)** For each creature's body (the primary shape only), approximate the outline with a polygon of 6 to 10 points on grid paper, and compute or estimate `C` and θ. The interactive's polygon mode or Lab 02's helper can do the arithmetic.
4. **(5 min)** As a group, pick the one design where the reader's word and the model's reading disagreed the most, and explain why.

Expected output: nine thumbnails, the readers' labels, a table of `C` and θ per body, and two sentences on the most surprising disagreement.

## Common misconceptions

- **"Shape language means drawing every character from literal circles, squares and triangles."** The families describe the dominant character of the outline. A lion can be triangle-dominant without a single straight line.
- **"The less circular a shape is, the more threatening it looks."** A 3 : 1 rectangle is less circular than an equilateral triangle and reads as solid, not threatening. Danger comes from points, measured by θ, not from low `C`.
- **"Faces and colors carry character, so the outline doesn't matter much."** Faces and colors are read after the outline, and they vanish first at distance or small size. The outline is what the player reads during a fight.
- **"These associations are universal laws."** They are strong, cross-cultural tendencies with measurable variation, and players can learn new ones. Treat them as defaults you depart from on purpose.

## Check yourself

1. Compute `C` for a 4 : 1 rectangle. Where does it fall on the map, and why?
2. A square pickup with side 20 pixels has its corners rounded with radius 4. Compute `C`. What reading does it get?
3. A designer wants a "friendly" boss for a children's game but also needs it to feel powerful. Using the big, medium and small shape split, propose a design in three sentences and state the family of each level.
4. A five-point star has `C` = 0.419 and tips of 52.5°, so the map reads it as sharp. Yet stars are used as rewards in many games. Give two things other than outline that could make a star read as a reward, and say what that tells you about the limits of the map.

<details>
<summary>Answers</summary>

1. `A = 4`, `P = 10` (for sides 4 and 1), so `C = 4π × 4 / 100 ≈ 0.503`. Its sharpest corner is 90°, so it reads as square (a plank or a bar), even though `C` is lower than a triangle's 0.605.
2. `s = 20`, `r = 4`. `A = 400 − (4 − π) × 16 ≈ 400 − 13.73 = 386.27`. `P = 80 − (8 − 2π) × 4 ≈ 80 − 6.87 = 73.13`. `C = 4π × 386.27 / 73.13² ≈ 0.908`. No corners remain, so θ = 180° and the reading is round, comfortably over the 0.85 line. A softened square reads as friendly.
3. One good answer: the primary shape is a huge rounded rectangle for the body (square family, powerful and stable), the secondary shapes are round limbs and a round head (circle family, friendly), and the tertiary details are small rounded horns instead of pointed ones. The square body gives power, the circles make it safe.
4. Examples: a bright, high-value, saturated color that the game uses only for rewards; a gentle bobbing or spinning motion; a sparkle; a pleasant sound; consistent placement where rewards appear. The map describes the outline alone. Context, color, motion and convention can override it, and genre conventions (the star as a reward) are learned meanings layered on top of the shape.

</details>

## Lab / assignment hook

[Lab 02, the shape cast](../labs/lab02.md). A studio exercise: design three characters and three props, each built on one dominant shape family, run a blind-read test with five classmates, and measure each primary shape with the provided helper. This is one of the weekly studies (50% of the course grade).

## Sources

- Super Mario Wiki, "Spiny" and "Goomba" (Super Mario Bros., NES, 1985). Spinies first appear in World 4-1, thrown by Lakitu; stomping one hurts Mario; they are defeated with a Fire Flower's fireballs or a Starman. Goombas are defeated by jumping on them and resemble mushrooms.
- Mitchell, J., Francke, M. and Eng, D. (2007). "Illustrative Rendering in Team Fortress 2." *Proceedings of NPAR 2007*, ACM. Section 4.1: clothing folds designed to echo silhouette shapes. Section 4.2: red base with warm colors, natural materials and angular geometry; blue base with cool colors, industrial materials and orthogonal forms.
- Celeste Wiki (celeste.ink), "Spikes" (Celeste, 2018). Spikes kill Madeline on contact unless she is moving away from them in the direction they point.
- Wikipedia, "Bouba/kiki effect". Köhler (1929), takete and maluma; Ramachandran and Hubbard (2001), about 95% match; Ćwiek et al. (2022), 917 participants, 25 languages, 10 writing systems, above-chance consistency with variation by language.
- Ramachandran, V. S. and Hubbard, E. M. (2001). "Synaesthesia: a window into perception, thought and language." *Journal of Consciousness Studies* 8(12), 3-34.
- Ćwiek, A. et al. (2022). "The bouba/kiki effect is robust across cultures and writing systems." *Philosophical Transactions of the Royal Society B* 377(1841).
- Solarski, C. (2012). *Drawing Basics and Video Game Art*. Watson-Guptill. Course reading on the circle, square and triangle in character design.
- The circularity measure `4πA/P²` is the isoperimetric quotient, a standard shape descriptor in geometry and image analysis. The table's values were computed from its definition.

## Interactive spec: examples/w02-shape-reader.html

**The one insight.** Danger reads from points, not from "unroundness". The first screen must show a triangle creature reading "Sharp" and, one control away, a 3 : 1 bar whose `C` is lower than the triangle's but which reads "Square".

**Layout.** Two linked panels side by side on desktop, stacked on phones.

- **Left panel, "Shape".** The current outline, drawn large on a faint grid, filled with the ink color at 15% and stroked in ink. The sharpest outward corner is marked with a small arc and its angle in degrees. Below it, two gauges: `C` on a 0 to 1 bar with ticks at 0.605 (triangle), 0.785 (square) and 1 (circle); and θ on a 0 to 180° bar with the map's zones shaded (≤ 65 sharp, 75 to 105 square, ≥ 120 round).
- **Right panel, "As a creature".** The same outline used as the body of an invented creature: two simple circular eyes placed at 35% height, two small rounded feet under the base. The face never changes. A large label under it shows the reading: Sharp, Square, Round or In between.
- A small map plot below both panels: θ on the x-axis (0 to 180°), `C` on the y-axis (0 to 1), with the reading zones shaded and labeled, the current shape as a dot, and fixed reference dots for circle, square, equilateral triangle, 3 : 1 rectangle and the five-point star (inner 0.5).

**Controls (native inputs, keyboard reachable, values printed).**
- **Sides** `n`: 3 to 12, and a "circle" option at the end.
- **Corner rounding** `r`: 0 to 1, as a fraction of the largest possible fillet (at 1 every corner is a full arc and the shape is a circle for any n).
- **Stretch**: horizontal scale 1 to 4 (aspect ratio), applied to the polygon before rounding.
- **Spikes**: off, or a star with `n` points and inner radius ratio 0.3 to 0.9 (default 0.5 when switched on).
- **Polygon mode**: a text area where the student pastes `x,y` points (one per line), replacing the generated shape. Invalid input shows an inline error and keeps the last valid shape.
- **Presets**: Triangle (default), Square, Circle, 3 : 1 bar, Five-point star, Rounded square r = 0.25 s, "Walker vs spiked shell" (switches between the dome and the spiked dome defined in section 2: half-disc radius 1 over a 2 × 0.4 base with bottom corners rounded at 0.15; six spikes centered at arc angles 15°, 45°, ..., 165°, tips 0.45 beyond the arc, bases spanning ±9° of arc).

**Computation.** Build the outline as a polygon; approximate each rounded corner or circle with at least 16 segments per quarter turn. `A` by the shoelace formula, `P` as the sum of segment lengths, `C = 4πA/P²`. θ is the smallest interior angle at convex vertices of the unrounded polygon, ignoring reflex vertices (use the cross-product sign relative to the polygon's winding). Any vertex replaced by a fillet (r > 0) is not a corner; if no corners remain, θ = 180 and print "none". Reading: θ ≤ 65 is Sharp; 75 ≤ θ ≤ 105 is Square; `C` ≥ 0.85 and θ ≥ 120 is Round; otherwise In between.

**Test values (three decimals for C, one for θ).**

| Shape | C | θ | Reading |
|---|---|---|---|
| n = 3 | 0.605 | 60.0 | Sharp |
| n = 4 | 0.785 | 90.0 | Square |
| n = 5 | 0.865 | 108.0 | In between |
| n = 6 | 0.907 | 120.0 | Round |
| n = 8 | 0.948 | 135.0 | Round |
| n = 12 | 0.977 | 150.0 | Round |
| n = 4, stretch 2 | 0.698 | 90.0 | Square |
| n = 4, stretch 3 | 0.589 | 90.0 | Square |
| n = 4, rounding so r = 0.25 × side | 0.933 | none | Round |
| n = 4, r = 0.1 × side | 0.850 | none | Round |
| Star, 5 points, inner 0.5 | 0.419 | 52.5 | Sharp |
| Star, 5 points, inner 0.38 | 0.265 | 35.7 | Sharp |
| Star, 8 points, inner 0.7 | 0.535 | 74.3 | In between |
| Circle | 1.000 | none | Round |
| Walker dome | 0.878 | none | Round |
| Spiked shell | 0.365 | 37.4 | Sharp |

Values from polygon approximations of arcs may differ from the exact ones in the third decimal; the tolerance is ±0.003 for `C`.

**Accessibility and motion.** The reading is shown as a word, not only as a color. Shape changes are immediate; any easing between shapes is off under `prefers-reduced-motion`. Palette tokens from `templates/interactive-tokens.css`, light and dark. Use the danger color for the Sharp label, steel for Square, moss for Round, ink-soft for In between.
