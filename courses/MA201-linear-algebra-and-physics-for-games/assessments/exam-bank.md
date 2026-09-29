# MA201 exam bank

This bank holds 75 questions for the MA201 final exam. Students may study from it, and the problem sets point to it for practice. The final draws questions from it and changes the numbers, as set out in the [final exam brief](final-exam-brief.md).

Every question has two tags.

- **Weeks.** The lecture weeks the question uses. Cross-week questions list several.
- **Type.** `compute` asks you to run a model from the lectures on numbers you have not seen. `code` asks you to predict what a short Python snippet prints, find its bug, or write a small function. `explain` asks why a model behaves as it does, with numbers. `design` asks you to choose parameters or structures that meet a brief. `critique` asks you to judge someone else's plan and propose a fix.

Every number below was recomputed in Python 3.13 with the models exactly as the lectures state them, and every snippet was run with the course interpreter, `.venv/bin/python`, and prints what the answer says. Facts about shipped games and engines (Unreal's 0.71, Box2D's combine rule, Minecraft's per-tick drag and so on) come from the lecture named in the question, which cites the source and version. On the exam those facts are printed in the question. You never need to remember an engine's constants.

## Coverage

| Week | Topic | Questions |
|---|---|---|
| 1 | Vectors in 3D, cross product | 1 to 4, 12, 26 |
| 2 | Matrices and linear transformations | 5 to 8 |
| 3 | Transform hierarchies | 9 to 12 |
| 4 | Homogeneous coordinates and projection | 13 to 17 |
| 5 | Quaternions | 18 to 22 |
| 6 | Kinematics | 23 to 26, 74 |
| 7 | Numerical integration | 27 to 31, 74 |
| 8 | Forces, mass and drag | 32 to 37 |
| 9 | Collision detection | 38 to 42, 75 |
| 10 | Collision response and impulses | 43 to 48, 75 |
| 11 | Spatial partitioning | 49 to 52 |
| 12 | Raycasting | 53 to 57, 73 |
| 13 | Projectile motion and aiming | 58 to 65, 74 |
| 14 | Determinism and floating point | 66 to 72, 73 |

Type counts are 61 compute, 9 code, 2 explain, 2 design and 1 critique. So 70 of 75 questions (93%) ask you to run a model or read code rather than recall text, and the explain, design and critique questions also need new numbers.

---

## Week 1. Vectors in 3D and the cross product

1. **Week 1 · compute.** Compute `a × b` for `a = (3, −1, 2)` and `b = (1, 4, −2)`. Check the result with two dot products. A triangle has edges `a` and `b` from one corner. Give its area and its unit normal.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `a × b = (−6, 8, 13)`. Area 8.20. Unit normal `(−0.366, 0.488, 0.793)`.

    Components, each from the cycle x → y → z. x: `(−1)(−2) − 2·4 = 2 − 8 = −6`. y: `2·1 − 3·(−2) = 2 + 6 = 8`. z: `3·4 − (−1)·1 = 12 + 1 = 13`.

    Checks. `(−6, 8, 13) · (3, −1, 2) = −18 − 8 + 26 = 0`. `(−6, 8, 13) · (1, 4, −2) = −6 + 32 − 26 = 0`. Both zero, so the result is perpendicular to both inputs.

    Length `√(36 + 64 + 169) = √269 = 16.401`. That is the parallelogram's area, so the triangle's area is `16.401 / 2 = 8.20`. Divide the vector by 16.401 for the unit normal.

    </details>

2. **Week 1 · compute.** Use the week 1 ramp triangle in a Y-up world, `a = (0, 0, 0)`, `b = (0, 0, 1)`, `c = (1, rise, 0)`, so the run is 1. Classify ramps with rise 0.99, 1.02 and 1.03 under three presets: UE5 default (floor when `n̂ · û ≥ 0.71`), UE3 Pawn (floor when `n̂ · û ≥ 0.70`), and Godot 4.7 default (floor when the slope angle is at most `45° + 0.01 rad`). Give `n̂ · û` to 5 decimals and the slope angle to 3.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    | Rise : run | n̂ · û | Slope angle | UE5 | UE3 | Godot 4.7 |
    |---|---|---|---|---|---|
    | 0.99 : 1 | 0.71065 | 44.712° | floor | floor | floor |
    | 1.02 : 1 | 0.70007 | 45.567° | wall | floor | floor |
    | 1.03 : 1 | 0.69658 | 45.847° | wall | wall | wall |

    The week 1 table gives `n = (−rise, run, 0)`, so `n̂ · û = 1 / √(1 + rise²)`. For 0.99 that is `1 / √1.9801 = 0.71065`, just above 0.71. For 1.02 it is `1 / √2.0404 = 0.70007`, below 0.71 and above 0.70.

    Godot's limit is `45 + 0.573 = 45.573°`, which is `cos⁻¹(0.70000)`. The 1.02 ramp at 45.567° passes by 0.006°. That is the week 1 lesson in its sharpest form: a 2% change in rise moves a ramp across two engines' thresholds, so never author geometry this close to a limit.

    </details>

3. **Week 1 · compute.** Use `side = (f × d) · û`. (a) In Unreal Engine 5 (Z up, forward +X), a character faces `f = (1, 0, 0)` and the target offset is `d = (3, −4, 0)`. Compute `side` and say whether to turn left or right. (b) In Godot 4 (Y up, forward −Z, right-handed), `f = (0, 0, −1)` and `d = (2, 0, −5)`. Compute `side` and say which way to turn. Check (b) against where +X points in Godot.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `side = −4`, turn left. (b) `side = −2`, turn right.

    (a) `f × d = (0·0 − 0·(−4), 0·3 − 1·0, 1·(−4) − 0·3) = (0, 0, −4)`. With `û = (0, 0, 1)`, `side = −4`. The week 1 table says positive means right in Unreal, so negative means left. Check: Unreal's right is +Y, and the target has y = −4, so it is on the left.

    (b) `f × d = (0·(−5) − (−1)·0, (−1)·2 − 0·(−5), 0·0 − 0·2) = (0, −2, 0)`. With `û = (0, 1, 0)`, `side = −2`. In right-handed Godot positive means left, so negative means right. Check: Godot's right is +X and the target has x = 2, ahead and to the right.

    Same formula both times. Only the reading of the sign changed.

    </details>

4. **Week 1 · code.** Predict the four lines this prints, then explain each.

    ```python
    import math

    def cross(a, b):
        return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])

    def sub(a, b):
        return tuple(x - y for x, y in zip(a, b))

    def godot_class(a, b, c, up=(0.0, 1.0, 0.0)):
        n = cross(sub(b, a), sub(c, a))
        length = math.sqrt(sum(x * x for x in n))
        if length < 1e-9:
            return "no normal"
        cos_up = sum(x * u for x, u in zip(n, up)) / length
        angle = math.degrees(math.acos(max(-1.0, min(1.0, cos_up))))
        limit = 45 + math.degrees(0.01)
        if angle <= limit:
            return "floor"
        if 180 - angle <= limit:
            return "ceiling"
        return "wall"

    a, b, c = (0, 0, 0), (0, 0, 1), (2, 1.5, 0)
    print(godot_class(a, b, c))
    print(godot_class(a, c, b))
    print(godot_class(a, (1, 1, 0), (2, 2, 0)))
    print(godot_class((0, 0, 0), (0, 0, 1), (1, 1.02, 0)))
    ```

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** It prints `floor`, `ceiling`, `no normal`, `floor`.

    Line 1. `n = (0, 0, 1) × (2, 1.5, 0) = (−1.5, 2, 0)`, length 2.5, `cos_up = 0.8`, angle 36.87°. Floor.

    Line 2. Swapping `b` and `c` flips the cross product to `(1.5, −2, 0)`. The angle to up is 143.13°, so the angle to down is 36.87°, inside the limit. Godot's rule calls it a ceiling. This is the winding bug from week 1: same triangle, opposite order.

    Line 3. The three points lie on one line, so the cross product is the zero vector. The length guard returns "no normal" instead of dividing by zero.

    Line 4. The 1.02 : 1 ramp from question 2, at 45.567°, is inside Godot's 45.573° limit.

    </details>

## Week 2. Matrices and linear transformations

5. **Week 2 · compute.** A 2:1 isometric game uses tiles 48 pixels wide and 24 tall, with the week 2 layout (`y` down, tile (0, 0)'s top corner at the origin). (a) Write `M`, `det(M)` and `M⁻¹`. (b) Which tile contains the click (50, 40)? Check with the tile's four corners. (c) Where is the center of tile (3, 1) on screen?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `M = [24 −24; 12 12]`, `det = 576`, `M⁻¹ = [1/48 1/24; −1/48 1/24]`. (b) Tile (2, 0). (c) (48, 60).

    (a) The columns are the screen steps for one tile along `i` and `j`, `(w/2, h/2) = (24, 12)` and `(−24, 12)`. `det = 24·12 − (−24)·12 = 576 = w h / 2`. The week 2 inverse simplifies to `i = x/w + y/h`, `j = y/h − x/w`.

    (b) `i = 50/48 + 40/24 = 1.042 + 1.667 = 2.708`, `j = 1.667 − 1.042 = 0.625`. Floors give (2, 0). Corners of tile (2, 0): `M(2, 0) = (48, 24)`, `M(3, 0) = (72, 36)`, `M(2, 1) = (24, 36)`, `M(3, 1) = (48, 48)`. The point (50, 40) sits inside that diamond, a little right of its bottom corner.

    (c) `M(3.5, 1.5) = (24 × (3.5 − 1.5), 12 × (3.5 + 1.5)) = (48, 60)`.

    </details>

6. **Week 2 · compute.** `A = [0 −1; 1 0]` rotates by 90°. `B = [1 0; 0 3]` stretches y by 3. Compute `A B` and `B A`. Follow `x̂ = (1, 0)` through each and describe what each does to a health bar that lies along x.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `A B = [0 −3; 1 0]`, `B A = [0 −1; 3 0]`. `A B` sends `x̂` to (0, 1). `B A` sends it to (0, 3).

    `A B` applies `B` first. The stretch leaves `x̂` alone at (1, 0), then the rotation turns it to (0, 1). The bar turns upright at its original length. `B A` rotates first, to (0, 1), then the stretch along the screen's y triples it to (0, 3). The bar turns upright and gets three times longer.

    If a rotated health bar gets longer instead of staying the same length, the stretch was applied in screen space after the rotation, the week 2 order bug.

    </details>

7. **Week 2 · compute.** For each matrix give the determinant, the area scale factor, whether it mirrors, and whether it has an inverse: `P = [2 1; 4 2]`, `Q = [0 −2; 1 0]`, `R = [3 1; 1 −1]`. For the one that mirrors, what happens to a single-sided sprite quad drawn with back-face culling?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    | Matrix | det | Area × | Mirrors? | Invertible? |
    |---|---|---|---|---|
    | P | 0 | 0 | — | no |
    | Q | 2 | 2 | no | yes |
    | R | −4 | 4 | yes | yes |

    `det P = 2·2 − 1·4 = 0`. Its columns (2, 4) and (1, 2) are parallel, so the plane collapses onto a line. `det Q = 0·0 − (−2)·1 = 2`. `det R = 3·(−1) − 1·1 = −4`.

    `R` flips orientation, so it reverses each triangle's winding. A single-sided quad now faces away from the camera by the winding rule and back-face culling removes it. The sprite disappears unless the renderer flips its front-face rule when `det < 0`, as glTF does.

    </details>

8. **Week 2 · code.** Predict the output. Which line shows the bug the week 2 lecture warns about, and what does a player see?

    ```python
    import math

    def pick(x, y, w=64, h=32, rounder=math.floor):
        i = x / w + y / h
        j = y / h - x / w
        return rounder(i), rounder(j)

    for click in [(40, 30), (-40, 8), (10, -6)]:
        print(click, pick(*click), pick(*click, rounder=int))
    ```

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    ```
    (40, 30) (1, 0) (1, 0)
    (-40, 8) (-1, 0) (0, 0)
    (10, -6) (-1, -1) (0, 0)
    ```

    For (−40, 8), `i = −0.625 + 0.25 = −0.375` and `j = 0.25 + 0.625 = 0.875`. `floor(−0.375) = −1`, but `int(−0.375) = 0`, because `int` truncates toward zero. For (10, −6), both `i = −0.031` and `j = −0.344` are negative, and `int` turns both into 0.

    The second and third lines show the bug. Every click left of or above the map origin selects tile (0, 0) or a neighbour instead of the tile under the cursor. Players see clicks near one edge of the map land on the wrong tile.

    </details>

## Week 3. Transform hierarchies

9. **Week 3 · compute.** A guard stands at `(−3, 4)` facing 120° (local +x is forward, +y is its left). The player is at `(−5, 9)`. Find the player's position in the guard's local space without using an angle function, and say whether the player is ahead or behind and left or right.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Local `(5.33, −0.77)`. Ahead by 5.33 m and 0.77 m to the right.

    `d = p − t = (−2, 5)`. The guard's basis is `R(120°)`, a pure rotation, so its inverse is its transpose. The rows of `Rᵀ` are the forward vector `(cos 120°, sin 120°) = (−0.5, 0.866)` and the left vector `(−sin 120°, cos 120°) = (−0.866, −0.5)`.

    `x = forward · d = 1 + 4.330 = 5.330`. `y = left · d = 1.732 − 2.5 = −0.768`. Positive x is ahead. Negative y is the guard's right.

    </details>

10. **Week 3 · compute.** A parent has scale `(sx, sy) = (1, 2)`. Its child, a unit square, is rotated 60°. Compute the child's world edges (the columns of `W = S R(θ)`), their lengths, the corner angle and `det(W)`. Then give the corner angle at 45°. Does the corner open or close compared with the lecture's parent of scale (2, 1)?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Edges `(0.5, 1.732)` and `(−0.866, 1.0)`, lengths 1.803 and 1.323, corner angle 57.00°, `det = 2`. At 45° the corner is 53.13°. The corner closes, where the lecture's (2, 1) parent opened it to 123.00° and 126.87°.

    `edge_x = (1 · cos 60°, 2 · sin 60°) = (0.5, 1.732)`. `edge_y = (−1 · sin 60°, 2 · cos 60°) = (−0.866, 1.0)`. Dot product `−0.433 + 1.732 = 1.299`. `cos φ = 1.299 / (1.803 × 1.323) = 0.545`, so `φ = 57.00°`.

    The sign of `(sy² − sx²) sin θ cos θ = 3 × 0.433` is positive, so the edges lean together and the angle drops below 90°. The two answers are supplements of the lecture's (57.00 + 123.00 = 180, 53.13 + 126.87 = 180). Swapping which axis is stretched swaps which pair of corners is acute. `det = sx · sy = 2` at every angle, so the area never changes.

    </details>

11. **Week 3 · compute.** A ship has local transform `trs(10, 0, deg=90, sx=2, sy=2)` at the root. Its child `Mast` has `trs(1, 2)`. The mast's child `Lookout` has `trs(3, 0, deg=−90)`. (a) Give the mast's world origin and the lookout's world basis and origin. (b) Find the world point (4, 9) in the lookout's local space and check the round trip. (c) A second node has world basis `[3 0; 0 3]` and origin (2, 1). Compare the true local position of the world point (8, 7) with the result of the transpose-only inverse.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) Mast origin (6, 2). Lookout basis `[2 0; 0 2]`, origin (6, 8). (b) Local (−1, 0.5), and mapping it back gives (4, 9). (c) True local (2, 2). The transpose-only version gives (18, 18), nine times too far.

    (a) The ship's basis is `2 R(90°) = [0 −2; 2 0]`. The mast's origin in world space is `Bp tc + tp = (0·1 − 2·2, 2·1 + 0·2) + (10, 0) = (6, 2)`. Its basis is the ship's basis times the identity. The lookout's basis is `[0 −2; 2 0] · R(−90°) = [0 −2; 2 0] · [0 1; −1 0] = [2 0; 0 2]`. The rotations cancel and the ship's scale of 2 remains, so `det = 4`. Its origin is `[0 −2; 2 0] (3, 0) + (6, 2) = (0, 6) + (6, 2) = (6, 8)`.

    (b) `p_local = B⁻¹ (p − t) = [0.5 0; 0 0.5] (4 − 6, 9 − 8) = (−1, 0.5)`. Back: `2 × (−1, 0.5) + (6, 8) = (4, 9)`.

    (c) `B⁻¹ (p − t) = (6, 6) / 3 = (2, 2)`. The transpose of `3I` is `3I`, so the shortcut computes `3 × (6, 6) = (18, 18)`. The transpose inverts only rotations. This is Godot's `inverse()` called on a scaled node, where `affine_inverse()` is needed.

    </details>

12. **Weeks 1 and 3 · compute.** A ramp surface in a child's local space has unit normal `n = (−0.6, 0.8)` in a 2D y-up world (a 36.87° slope). Its parent stretches x by 3. (a) Carry the normal with `B n` and with the inverse transpose `(B⁻¹)ᵀ n`, normalize both, and give each slope angle. (b) Which is right, and what does a walkable test with threshold 0.71 on the y component say for each?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `B n` normalizes to `(−0.914, 0.406)`, a 66.04° slope. `(B⁻¹)ᵀ n` normalizes to `(−0.243, 0.970)`, a 14.04° slope. (b) The inverse transpose is right. The wrong normal fails the test (0.406 < 0.71, a wall). The right one passes (0.970, a floor).

    `B = [3 0; 0 1]`, so `B n = (−1.8, 0.8)`, length 1.970. `(B⁻¹)ᵀ = [1/3 0; 0 1]`, so `(B⁻¹)ᵀ n = (−0.2, 0.8)`, length 0.825.

    Check with geometry. The original slope rises 0.75 per unit of run (`tan 36.87° = 0.75`). Stretching x by 3 gives 0.25 per unit, which is `atan(0.25) = 14.04°`. The inverse-transpose normal matches that slope, and `B n` tilts the wrong way. A stretched ramp checked with `B n` becomes an unclimbable wall.

    </details>

## Week 4. Homogeneous coordinates and projection

13. **Week 4 · compute.** Using column vectors and the week 4 `rot_y`, build `M = translate(1, 5, 0) · rot_y(−90°)`. Apply it to the point `(0, 0, 2, 1)` and the direction `(0, 0, 2, 0)`. Then apply `rot_y(−90°) · translate(1, 5, 0)` to the same point.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Point `(−1, 5, 0, 1)`. Direction `(−2, 0, 0, 0)`. Wrong order `(−2, 5, 1, 1)`.

    `rot_y(−90°)` has `c = 0`, `s = −1`, so `x' = c x + s z = −z` and `z' = −s x + c z = x`. The point (0, 0, 2) turns to (−2, 0, 0), then the translation adds (1, 5, 0) to give (−1, 5, 0). The direction turns to (−2, 0, 0) and ignores the translation, because its `w = 0` multiplies the fourth column.

    In the other order the point moves first, to (1, 5, 2), then swings about the origin to `(−2, 5, 1)`. That is the "moved then orbited" bug.

    </details>

14. **Week 4 · compute.** (a) A game uses vertical FOV 60°. What horizontal angle does a 21:9 player see, and what Source-style setting (horizontal at 4:3) gives the same view? (b) Another game fixes a horizontal FOV of 100° on 16:9. What vertical FOV is that? If that vertical FOV were used Hor+ on a 4:3 monitor, what horizontal angle would the 4:3 player see?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 106.83° across. A Source setting of 75.18, so about 75. (b) Vertical 67.67°. A 4:3 player would see 83.58° across.

    (a) `θ_h = 2·atan(21/9 · tan 30°) = 2·atan(1.3472) = 106.83°`. The Source number is the horizontal angle a 4:3 screen would show, `2·atan(4/3 · tan 30°) = 2·atan(0.7698) = 75.18°`.

    (b) Invert the formula, `θ_v = 2·atan(tan(θ_h/2) / a) = 2·atan(1.1918 / 1.7778) = 67.67°`. Then `2·atan(4/3 · tan 33.84°) = 83.58°`.

    Note how close 75.18 is to Half-Life 2's default of 75. Source's default and a vertical 60° are almost the same view.

    </details>

15. **Week 4 · compute.** A camera has vertical FOV 50° on a 2560 × 1440 screen. (a) Where, in pixels, does the view-space point `(3, −1, −15)` land? (b) With vertical FOV 60° on a 1440-pixel-tall screen, how many pixels tall is a 1.8 m character 30 m away?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) Pixel (1588.8, 822.9). (b) 74.8 px.

    (a) `f = 1 / tan 25° = 2.1445`, `a = 2560/1440 = 1.7778`, depth `d = 15`. `x_ndc = (f/a) · 3 / 15 = 0.2413`, `y_ndc = f · (−1) / 15 = −0.1430`. Pixel `x = (0.2413 + 1)/2 × 2560 = 1588.8`. Pixel `y = (1 − (−0.1430))/2 × 1440 = 822.9`, below the center because the point is below the eye.

    (b) `f = 1 / tan 30° = 1.7321`. NDC height `1.8 / 30 × 1.7321 = 0.1039`. Half the screen's pixel height maps to one NDC unit, so `0.1039 × 720 = 74.8` px.

    </details>

16. **Week 4 · compute.** A camera uses near `n = 0.2` m and far `F = 2000` m with the OpenGL-style matrix. (a) Compute `z_ndc` at depths 1 m and 50 m. (b) At what depth is `z_ndc = 0`, and what share of the depth range is used by depths up to 1 m? (c) A point's clip-space result is `(−6, 2, 9.5, 9)`. Is it inside the frustum? Give its NDC.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 0.6002 at 1 m, 0.9922 at 50 m. (b) About 0.4 m (0.39996). Depths up to 1 m use 80% of the range. (c) Outside, beyond the far plane. NDC `(−0.667, 0.222, 1.056)`.

    (a) `z_ndc(d) = (F + n)/(F − n) − 2Fn / ((F − n) d)`. `(F + n)/(F − n) = 1.0002`, `2Fn/(F − n) = 800/1999.8 = 0.40004`. At 1 m, `1.0002 − 0.4000 = 0.6002`. At 50 m, `1.0002 − 0.0080 = 0.9922`.

    (b) `d = 2Fn / (F + n) = 800 / 2000.2 = 0.39996`, about twice the near distance. The share up to 1 m is `(0.6002 + 1) / 2 = 80%`.

    (c) Inside needs `−w ≤ x, y, z ≤ w` with `w = 9`. `x = −6` and `y = 2` pass, but `z = 9.5 > 9` fails. Dividing by 9 gives `z_ndc = 1.056`, past the far plane at 1.

    </details>

17. **Week 4 · compute.** A camera's world transform is `C = translate(0, 2, 10) · rot_y(90°)`. Build the view matrix `V = C⁻¹` with the rigid-inverse rule and give the view-space positions of two trees at `(−5, 2, 10)` and `(−5, 2, 13)`. Describe where each tree appears.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `(0, 0, −5)` and `(−3, 0, −5)`. The first is straight ahead, 5 m away. The second is 5 m ahead and 3 m to the left.

    The camera's forward is `rot_y(90°)` applied to (0, 0, −1), which is (−1, 0, 0). So the camera looks along world −x. The rigid inverse is `[Rᵀ, −Rᵀ t]`. Subtract the camera position, then apply `Rᵀ`. For the first tree `p − t = (−5, 0, 0)`, and `Rᵀ` turns world −x into view −z, giving (0, 0, −5).

    For the second, `p − t = (−5, 0, 3)`. `rot_y(90°)ᵀ` sends (x, y, z) to `(−z, y, x)`, which gives (−3, 0, −5). View x is negative, so the tree is left of center.

    </details>

## Week 5. Quaternions

18. **Week 5 · compute.** (a) Write the quaternion for 120° about `(0, 0, 1)` and use it to rotate `(1, 0, 0)`. (b) An engine prints `(w, x, y, z) = (0.5, 0.5, 0.5, 0.5)`. What rotation is it, and where does it send `(1, 0, 0)`?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `(0.5, 0, 0, 0.866)`. It sends (1, 0, 0) to `(−0.5, 0.866, 0)`. (b) 120° about `(1, 1, 1)/√3 = (0.577, 0.577, 0.577)`. It sends (1, 0, 0) to (0, 1, 0).

    (a) Half the angle is 60°. `w = cos 60° = 0.5` and the vector part is `sin 60° × (0, 0, 1)`. A 120° turn about z takes the x axis to `(cos 120°, sin 120°, 0)`.

    (b) `θ = 2·acos(0.5) = 120°`. Axis `(0.5, 0.5, 0.5) / sin 60° = (0.577, 0.577, 0.577)`. A 120° turn about the diagonal cycles the axes, x to y, y to z, z to x. Running the week 5 `rotate` gives (0, 1, 0).

    </details>

19. **Week 5 · compute.** A turret's keys are yaw −150° and yaw 160° about the up axis `(0, 1, 0)`. (a) Give both quaternions, their dot product and the true turn `φ`. (b) Which way does slerp go without the sign check, and how far? (c) Give the yaw at `t = 0.25, 0.5, 0.75` for the naive and checked slerp, wrapped to (−180°, 180°].

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `a = (0.2588, 0, −0.9659, 0)`, `b = (0.1736, 0, 0.9848, 0)`, `a · b = −0.9063`, `φ = 50°`. (b) The long way, 310°. (c) Naive: −72.5°, 5.0°, 82.5°. Checked: −162.5°, −175.0°, 172.5°.

    (a) `a = (cos(−75°), 0, sin(−75°), 0)` and `b = (cos 80°, 0, sin 80°, 0)`. `a · b = 0.0449 − 0.9513 = −0.9063`. `|a · b| = cos 25°`, so `φ = 50°`.

    (b) The dot product is negative, so the 4D angle is `acos(−0.9063) = 155°`, a 310° turn in 3D. Naive slerp sweeps from −150° up through 0° to 160°.

    (c) The naive yaw moves 77.5° per quarter. The checked version flips `b`, moves 12.5° per quarter the short way through 180° (−162.5, −175, then 172.5 on the other side of the wrap), and arrives at 160°.

    </details>

20. **Week 5 · compute.** (a) In Godot's YXZ order, a camera has yaw 20°, pitch 90°, roll 35°. Give a triple with yaw 0° and pitch 90° that gives the same orientation, and the shared quaternion. (b) A turret at yaw 10° must face yaw 100° and turns at most 60°/s on a 30 Hz tick. Using `t = min(1, ω·Δt / φ)`, give `t` and the yaw after one tick.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) Yaw 0°, pitch 90°, roll 15°. Quaternion `(0.7011, 0.7011, −0.0923, 0.0923)`. (b) `t = 0.0222`, yaw 12°.

    (a) At pitch 90° yaw and roll turn about the same line, so `(Y, R)` and `(Y + k, R + k)` give one orientation. With `k = −20`, `(20, 35)` becomes `(0, 15)`. Building `q_y(yaw) · q_x(pitch) · q_z(roll)` for both triples gives the same four numbers.

    (b) The remaining turn is `φ = 90°` (from the quaternions, `2·acos(|a · b|) = 2·acos(cos 45°)`). One tick allows `60 / 30 = 2°`, so `t = 2 / 90 = 0.0222`. Slerp turns at constant angular speed, so the yaw moves exactly 2°, to 12°.

    </details>

21. **Week 5 · code.** Predict what this prints and explain the middle value.

    ```python
    import math

    def yaw_quat(deg):
        h = math.radians(deg) / 2
        return (math.cos(h), 0.0, math.sin(h), 0.0)

    def slerp(a, b, t):
        d = sum(x * y for x, y in zip(a, b))
        omega = math.acos(max(-1.0, min(1.0, d)))
        s = math.sin(omega)
        return tuple((math.sin((1 - t) * omega) * x + math.sin(t * omega) * y) / s
                     for x, y in zip(a, b))

    def yaw_of(q):
        deg = math.degrees(2 * math.atan2(q[2], q[0]))
        return round((deg + 180) % 360 - 180, 1)

    a, b = yaw_quat(350), yaw_quat(10)
    print(round(sum(x * y for x, y in zip(a, b)), 4))
    print([yaw_of(slerp(a, b, t)) for t in (0.25, 0.5, 0.75)])
    ```

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    ```
    -0.9848
    [-95.0, -180.0, 95.0]
    ```

    Yaw 350° gives `a = (cos 175°, 0, sin 175°, 0) = (−0.9962, 0, 0.0872, 0)`. Yaw 10° gives `b = (0.9962, 0, 0.0872, 0)`. The dot product is `−0.9924 + 0.0076 = −0.9848`, negative. The orientations are only 20° apart, but this slerp has no sign check and travels the 340° arc. It starts at −10°, passes −95°, reaches the back of the room at ±180° at the halfway point (printed as −180.0 by the wrap), then 95°, then 10°.

    The fix is one line before `omega`: if `d < 0`, negate `b` and `d`. The checked midpoint is 0°.

    </details>

22. **Week 5 · compute.** For a 150° yaw turn from the identity, compare slerp and nlerp at `t = 0.25` and `t = 0.5`. At which `t` do they agree, and why?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** At `t = 0.25`, slerp gives 37.5° and nlerp 33.0°. At `t = 0.5` both give 75°.

    Slerp turns at constant speed, so it is at `0.25 × 150 = 37.5°`. Nlerp takes the straight chord between the two quaternions and normalizes. With `b = (cos 75°, 0, sin 75°, 0)`, the blend `0.75·(1, 0, 0, 0) + 0.25·b = (0.8147, 0, 0.2415, 0)` gives yaw `2·atan2(0.2415, 0.8147) = 33.0°`.

    At `t = 0.5` the chord's midpoint lies on the bisector of the two quaternions, so normalizing it gives exactly the halfway rotation. Nlerp lags early and catches up late. The gap grows with the size of the turn (the lecture's 120° turn gave 27.8° against 30°), which is why nlerp is fine for small per-frame turns.

    </details>

## Week 6. Kinematics

23. **Week 6 · compute.** A drone's logged positions at `t = 1.9`, `2.0` and `2.1` s are `(4.0, 10.0)`, `(4.6, 10.3)` and `(5.0, 10.8)` m. Estimate the velocity at `t = 2.0` with a central difference and with a forward difference, and the acceleration with a second difference.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Central `(5, 4)` m/s. Forward `(4, 5)` m/s. Acceleration `(−20, 20)` m/s².

    Central: `((5.0 − 4.0)/0.2, (10.8 − 10.0)/0.2) = (5, 4)`. Forward: `((5.0 − 4.6)/0.1, (10.8 − 10.3)/0.1) = (4, 5)`. Second difference: `((5.0 − 9.2 + 4.0)/0.01, (10.8 − 20.6 + 10.0)/0.01) = (−20, 20)`.

    The forward difference measures the average over the next 0.1 s. The drone is slowing in x and speeding up in y, so it disagrees with the central estimate in both components.

    </details>

24. **Week 6 · compute.** A server logs player positions 30 times per second, each with error up to 0.1 m. (a) What is the worst-case error of a forward-difference speed and of a second-difference acceleration? (b) An anti-cheat rule flags anyone above 8 m/s. Honest players can sprint at 7.5 m/s. What tolerance does the per-sample check need, and what would you do instead?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 6 m/s and 360 m/s². (b) A per-sample check would need a limit of about 13.5 m/s to avoid false flags, which catches almost nothing. Measure distance over a longer window instead.

    (a) `2e/h = 2 × 0.1 × 30 = 6` m/s. `4e/h² = 4 × 0.1 × 900 = 360` m/s², about 37 times Earth's gravity, so acceleration from raw positions is noise.

    (b) An honest sprinter can read `7.5 + 6 = 13.5` m/s for one sample. Over one second (30 samples) the endpoint error is still at most 0.2 m, so the speed error is 0.2 m/s and a limit of 8 m/s works. Longer windows trade detection delay for accuracy.

    </details>

25. **Week 6 · compute.** A platformer has jump velocity 500 px/s and gravity 1,200 px/s². (a) Give the baseline air time and apex. (b) On an elevator descending at 200 px/s, give the world apex, the apex above the elevator floor and the air time until landing on it under `ADD_VELOCITY` and under `ADD_UPWARD_VELOCITY`. (c) Under `DO_NOTHING` on a platform sliding at 180 px/s, where does the player land relative to the take-off spot? (d) A mine cart brakes at 150 px/s² during the jump, with full velocity inheritance. Where does the player land relative to the cart?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 0.833 s, 104.2 px. (b) `ADD_VELOCITY`: world apex 37.5 px, relative apex 104.2 px, air 0.833 s. `ADD_UPWARD_VELOCITY`: world apex 104.2 px, relative apex 204.2 px, air 1.167 s. (c) 150 px behind. (d) 52.1 px ahead of the take-off spot.

    (a) `T = 2 × 500 / 1200 = 0.833` s, `h = 500² / 2400 = 104.2` px.

    (b) Full inheritance launches at `500 − 200 = 300` px/s in the world (apex `300² / 2400 = 37.5`) and 500 relative to the floor. Dropping the downward part launches at 500 in the world and `500 + 200 = 700` relative, apex `700² / 2400 = 204.2`, air `2 × 700 / 1200 = 1.167` s.

    (c) `180 × 0.833 = 150` px, the platform slides out from under the player.

    (d) In the cart's frame the player drifts by `−½ a_p T²`. With `a_p = −150`, that is `+½ × 150 × 0.833² = 52.1` px forward. A braking cart throws the rider forward, as a real one does.

    </details>

26. **Weeks 1 and 6 · compute.** A turntable spins with `ω = (0, 1.5, 0)` rad/s. Players stand at `r = (2, 0, 0)` and `r = (0, 0, 2)` m from the center. Give each one's velocity with `v = ω × r`, their speed and their centripetal acceleration. In which direction does each leave if they jump?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** At (2, 0, 0), `v = (0, 0, −3)` m/s. At (0, 0, 2), `v = (3, 0, 0)` m/s. Both have speed 3 m/s and centripetal acceleration 4.5 m/s² toward the center. Each leaves along its velocity, the tangent, not outward.

    `(0, 1.5, 0) × (2, 0, 0) = (1.5·0 − 0·0, 0·2 − 0·0, 0·0 − 1.5·2) = (0, 0, −3)`. `(0, 1.5, 0) × (0, 0, 2) = (1.5·2 − 0, 0 − 0, 0 − 0) = (3, 0, 0)`. Speed `ω r = 3`. Acceleration `ω² r = 2.25 × 2 = 4.5`, or `v² / r = 9 / 2`.

    Each velocity is perpendicular to its radius. A player who expects to be thrown straight out is wrong by 90°.

    </details>

## Week 7. Numerical integration

27. **Week 7 · compute.** A body is at `x = (2, 0)` with `v = (0, 0.8)` under the orbit's gravity `a(x) = −x / |x|³` (GM = 1). With `dt = 0.2`, take one step of explicit Euler, semi-implicit Euler and velocity Verlet. Give each new state, `|x|` and the energy `E = ½|v|² − 1/|x|`. The starting energy is −0.18.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    | Rule | x_new | v_new | \|x_new\| | E |
    |---|---|---|---|---|
    | Explicit Euler | (2.000, 0.160) | (−0.050, 0.800) | 2.00639 | −0.17716 |
    | Semi-implicit | (1.990, 0.160) | (−0.050, 0.800) | 1.99642 | −0.17965 |
    | Velocity Verlet | (1.995, 0.160) | (−0.04988, 0.79800) | 2.00141 | −0.18000 |

    `a(x) = −(2, 0) / 8 = (−0.25, 0)`. Explicit Euler moves with the old velocity, `(2, 0) + 0.2·(0, 0.8) = (2, 0.16)`, then sets `v = (−0.05, 0.8)`. Semi-implicit updates the velocity first and moves with it, `x = (2 − 0.01, 0.16)`. Verlet adds `½ a dt² = (−0.005, 0)` to the explicit position, then averages the old acceleration with the new one at (1.995, 0.16), which is `(−0.2489, −0.0200)`.

    Explicit Euler lands outside the start radius and gains 0.0028 of energy in one step. Semi-implicit lands inside. Verlet keeps the energy to five decimals.

    </details>

28. **Week 7 · compute.** A bobbing pickup uses explicit Euler on a spring with `ω = 8` rad/s at 50 Hz. By what factor has its amplitude grown after 2 seconds? What would you change?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 3.54 times. Switch to semi-implicit Euler, which keeps the amplitude bounded at this step.

    `ω·dt = 8/50 = 0.16`, so each step multiplies `A²` by `1 + 0.0256`. Two seconds is 100 steps, so the amplitude grows by `1.0256^50 = 3.54`. A 10 cm bob is 35 cm after two seconds.

    Halving the step would only slow the growth. The rule is the problem. At `ω·dt = 0.16` semi-implicit Euler is far from its limit of 2.

    </details>

29. **Week 7 · compute.** Cloth runs semi-implicit Euler at 90 Hz. (a) What is the largest stable `k / m`? (b) A rope segment has `k = 50,000` N/m and `m = 1.5` kg. Is it stable? (c) How many sub-steps per tick keep `ω·dt ≤ 1.5`? (d) How far does a semi-implicit spring overshoot at `ω·dt = 1.5`?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 32,400. (b) No, `ω·dt = 2.03`. (c) 2 sub-steps. (d) Its peak is 1.51 times the true amplitude.

    (a) `ω·dt < 2` gives `ω < 180` rad/s, so `k / m < 180² = 32,400`.

    (b) `ω = √(50,000 / 1.5) = √33,333 = 182.6` rad/s, and `182.6 / 90 = 2.03`, just past the limit.

    (c) `dt ≤ 1.5 / 182.6 = 0.00822` s. One tick is 0.0111 s, so it needs `0.0111 / 0.00822 = 1.35`, rounded up to 2 sub-steps.

    (d) `1 / √(1 − (1.5/2)²) = 1 / √0.4375 = 1.51`. Stable but 51% too far, which is why the lab's margin is not a luxury.

    </details>

30. **Week 7 · code.** This code measures a jump with `v0 = 10` and `g = 20` (exact apex 2.5). Predict the four numbers, name the integrator each call uses, and give the size of the error in terms of `v0` and `dt`.

    ```python
    def jump(fps, v0=10.0, g=20.0, swap=False):
        dt = 1 / fps
        y, v, apex = 0.0, v0, 0.0
        while True:
            if swap:
                v -= g * dt
                y += v * dt
            else:
                y += v * dt
                v -= g * dt
            apex = max(apex, y)
            if y < 0:
                return round(apex, 4)

    print(jump(30), jump(30, swap=True), jump(120), jump(120, swap=True))
    ```

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** It prints `2.6667 2.3333 2.5417 2.4583`. `swap=False` is explicit Euler and overshoots. `swap=True` is semi-implicit Euler and undershoots. Each is off by `v0·dt/2`, which is 0.1667 at 30 fps and 0.0417 at 120 fps.

    Under constant gravity both rules are stable, and their errors are equal and opposite. Quadrupling the frame rate divides the error by 4, a first-order method. Velocity Verlet would print 2.5 at the apex sample at every frame rate, because its position update is the exact kinematics formula.

    </details>

31. **Week 7 · explain.** Explain with the step in question 27 (velocity perpendicular to the radius, as at every point of a circular orbit) why explicit Euler gains energy on every such step, while semi-implicit Euler's energy error changes sign. Then explain why a smaller step does not fix explicit Euler.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Explicit Euler moves along the tangent at the start of the step, and a tangent always points outside the circle. In question 27 it landed at radius 2.00639, further out than 2, and further out means more energy. Every step errs in the same direction, so the errors add up.

    Semi-implicit Euler bends the velocity toward the center first, so it landed inside, at 1.99642. On the next step the body is closer, gravity is stronger, and the error swings back. The energy wobbles in a band instead of climbing.

    For the spring the lecture showed the exact factor, `A²` grows by `1 + ω²·dt²` per step. A smaller step makes the factor closer to 1, but over a fixed time the growth is about `e^(ω²·dt·t/2)`, which still grows without bound. The step size slows the drift. Only the rule change stops it.

    </details>

## Week 8. Forces, mass and drag

32. **Week 8 · compute.** An entity at 20 ticks per second applies gravity `g = 0.05` blocks per tick², then drag `d = 0.97`. Find the terminal velocity in blocks per tick and blocks per second, and the ticks and seconds to reach 90% of it from rest.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 1.617 blocks per tick, 32.33 blocks per second. 76 ticks, 3.8 s.

    With acceleration before drag, `v* = g·d / (1 − d) = 0.05 × 0.97 / 0.03 = 1.617`, times 20 is 32.33 blocks/s. The gap to terminal speed shrinks by `d` per tick, so 90% needs `0.97^n = 0.1`, `n = ln 0.1 / ln 0.97 = 75.6`, rounded up to 76 ticks.

    </details>

33. **Week 8 · compute.** A drag factor of 0.9 per tick at 20 Hz must be ported to a 60 Hz loop. (a) Give the coefficient `c` in 1/s and the time constant. (b) Give the per-step factor at 60 Hz. (c) Gravity was 0.05 blocks per tick². What should each 60 Hz step add to the velocity, in blocks per second?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `c = 2.107` per second, `τ = 0.475` s. (b) 0.96549. (c) 0.333 blocks/s per step.

    (a) `c = −ln(0.9) / 0.05 = 2.107`, `τ = 1 / c = 0.475` s.

    (b) `e^(−c/60) = 0.9^(1/3) = 0.96549`.

    (c) 0.05 blocks per tick² is `0.05 × 20² = 20` blocks/s². Each 1/60 s step adds `20 / 60 = 0.333` blocks/s. Copying 0.05 unchanged into a 60 Hz loop would triple gravity per second of play.

    </details>

34. **Week 8 · compute.** A 3 kg drone has velocity `(4, −2)` m/s. This step it receives a thrust of `(6, 0)` N and a linear drag force `−1.5 v` N, plus gravity 9.81 m/s² down. With the week 8 accumulator and semi-implicit Euler at `dt = 0.1`, give the total force, the acceleration, the new velocity and the position change. What are its terminal velocities in x and y?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Force `(0, 3)` N. Acceleration `(0, −8.81)` m/s². New velocity `(4, −2.881)` m/s. Position change `(0.4, −0.288)` m. Terminal x velocity 4 m/s, terminal y velocity 19.62 m/s downward.

    Drag is `−1.5 × (4, −2) = (−6, 3)`. Adding the thrust gives `(0, 3)`. Divide by the mass and add gravity as an acceleration: `(0, 1 − 9.81)`. Then `v += a·dt` and `x += v·dt` with the new velocity.

    In x, thrust balances drag when `1.5 v = 6`, `v = 4`, so the drone is already at its terminal speed there. In y, drag balances weight when `1.5 v = 3 × 9.81`, `v = 19.62` m/s. With drag as a force, the heavier the drone the faster it falls.

    </details>

35. **Week 8 · compute.** A swamp uses a damping coefficient `c = 45` per second. Give the per-step factor for the exact, Padé and linear forms at 60 Hz and at 30 Hz. Which are safe at each rate, and what does the player see with the unsafe one?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    | Rate | c·h | Exact e^(−ch) | Padé 1/(1 + ch) | Linear 1 − ch |
    |---|---|---|---|---|
    | 60 Hz | 0.75 | 0.4724 | 0.5714 | 0.2500 |
    | 30 Hz | 1.50 | 0.2231 | 0.4000 | −0.5000 |

    At 60 Hz all three slow the body. At 30 Hz the linear form reverses the velocity every step and halves it, so a crate in the swamp jitters back and forth while it stops. Exact and Padé are safe at both rates. Past `c·h = 2` (below 22.5 Hz here) the linear form would grow the jitter until the crate flies off.

    </details>

36. **Week 8 · compute.** Quake's ground friction (from the week 8 lecture) lowers speed by `frametime × 4 × max(speed, 100)` each frame. Ignoring frame rounding, how long does a player moving at 150 units/s take to stop after releasing the keys, and how far do they slide?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 0.351 s and 25 units.

    Above 100 units/s the rule is linear drag at rate 4, `v = 150 e^(−4t)`, reaching 100 after `ln(1.5)/4 = 0.101` s. It covers `(150 − 100) / 4 = 12.5` units. Below 100 the deceleration is constant, `4 × 100 = 400` units/s², so it takes `100/400 = 0.25` s and covers `100² / 800 = 12.5` units. Totals: 0.351 s and 25 units.

    </details>

37. **Week 8 · code.** Predict the two lines this prints. Which pair of numbers matches the thrown-projectile order change in Minecraft Java Edition 1.21.2, and what general rule do both lines show?

    ```python
    def terminal(g, d, order, ticks=3000):
        v = 0.0
        for _ in range(ticks):
            if order == "drag first":
                v *= d
                v -= g
            else:
                v -= g
                v *= d
        return round(-v * 20, 2)

    print(terminal(0.03, 0.99, "drag first"), terminal(0.03, 0.99, "drag last"))
    print(terminal(0.06, 0.95, "drag first"), terminal(0.06, 0.95, "drag last"))
    ```

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    ```
    60.0 59.4
    24.0 22.8
    ```

    The first line is the snowball: `g/(1 − d) = 3.00` blocks per tick before 1.21.2 and `g·d/(1 − d) = 2.97` after, 60.0 and 59.4 blocks/s. The second line uses the same rule with other numbers, `0.06/0.05 = 1.2` and `1.2 × 0.95 = 1.14` blocks per tick.

    Moving the drag after gravity multiplies the terminal speed by `d`. Three thousand ticks is enough for both to reach the fixed point to two decimals.

    </details>

## Week 9. Collision detection

38. **Week 9 · compute.** (a) Sphere A at `(2, −1, 0)` with radius 1.2 and sphere B at `(3, 1, 2)` with radius 2. Do they overlap? Give the normal from A to B and the depth. (b) AABB A has center (0, 0, 0) and half-extents (2, 1, 1). AABB B has center (3.2, 0.5, −0.4) and half-extents (1.5, 1, 1). Give the overlap on each axis and the MTV.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) Yes. Normal `(0.333, 0.667, 0.667)`, depth 0.2. (b) Overlaps 0.3, 1.5 and 1.6. MTV normal (1, 0, 0), depth 0.3.

    (a) `d = (1, 2, 2)`, `|d|² = 9 < 3.2² = 10.24`. `|d| = 3`, depth `3.2 − 3 = 0.2`, normal `d/3`.

    (b) x: `3.5 − 3.2 = 0.3`. y: `2 − 0.5 = 1.5`. z: `2 − 0.4 = 1.6`. All positive, so they overlap. The smallest is x, and `c_B,x − c_A,x > 0`, so the normal is +x.

    </details>

39. **Week 9 · compute.** Box A is axis-aligned at the origin with half-extents (1.5, 1). Box B has half-extents (1, 0.5), is rotated 60° (`u_B = (0.5, 0.866)`, `v_B = (−0.866, 0.5)`), and is centered at (2.2, 1.6). Fill the SAT table (axis, `|d · n|`, `r_A`, `r_B`, overlap) for all four axes and give the result.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    | Axis n | \|d · n\| | r_A | r_B | Overlap |
    |---|---|---|---|---|
    | (1, 0) | 2.2000 | 1.5000 | 0.9330 | +0.2330 |
    | (0, 1) | 1.6000 | 1.0000 | 1.1160 | +0.5160 |
    | (0.5, 0.866) | 2.4856 | 1.6160 | 1.0000 | +0.1304 |
    | (−0.866, 0.5) | 1.1053 | 1.7990 | 0.5000 | +1.1938 |

    Collision. MTV normal (0.5, 0.866), depth 0.1304.

    Radii use `r = h_u |u · n| + h_v |v · n|`. For B on (1, 0), `1 × 0.5 + 0.5 × 0.866 = 0.933`. For A on B's u axis, `1.5 × 0.5 + 1 × 0.866 = 1.616`. Every overlap is positive, so no axis separates them. The smallest overlap is on B's u axis, and `d · n = 2.4856 > 0`, so the normal already points from A to B.

    </details>

40. **Week 9 · compute.** Move B in question 39 to (2.4, 1.7). (a) What does an AABB test on B's bounding box say? (b) What does SAT say? (c) What does the difference mean for a player standing next to this crate?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) Hit, with 0.033 of overlap on x. (b) No collision. B's u axis (0.5, 0.866) separates them by 0.0562. (c) The AABB test would block the player at a visible gap of about 6 cm.

    (a) B's AABB half-extents are its radii on the world axes, 0.933 and 1.116. On x, `1.5 + 0.933 − 2.4 = 0.033 > 0`. On y, `1 + 1.116 − 1.7 = 0.416 > 0`. Both overlap.

    (b) On B's u axis, `|d · n| = 2.4 × 0.5 + 1.7 × 0.866 = 2.6722` against `1.616 + 1.0 = 2.616`, a gap of 0.0562. One gap is enough.

    (c) The AABB is only a broad-phase filter. Using it as the verdict produces false hits whenever a box is rotated.

    </details>

41. **Week 9 · compute.** How many SAT axes are needed for (a) a regular hexagon against a rectangle in 2D, and (b) a box against a hexagonal prism in 3D? A hexagonal prism has two cap faces and six side faces, three pairs of parallel sides, six vertical edges and twelve cap edges.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 5 distinct axes (at most 10 if you do not merge parallel normals). (b) 19.

    (a) A regular hexagon's six edge normals come in three parallel pairs, so it contributes 3 directions. The rectangle contributes 2. The general bound `m + k = 6 + 4 = 10` counts each parallel pair twice.

    (b) Face directions: 3 for the box, and 4 for the prism (1 for both caps plus 3 side directions). Edge directions: 3 for the box, and 4 for the prism (3 cap edge directions plus the vertical). Cross products `3 × 4 = 12`. Total `3 + 4 + 12 = 19`, minus any cross product that comes out zero length because two edges are parallel (the box's vertical edges and the prism's vertical edges, if both shapes stand upright).

    </details>

42. **Week 9 · compute.** A plank with half-extents (3, 0.5) is rotated 20°. Give the half-extents of its AABB and the ratio of the AABB's area to the plank's.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Half-extents (2.990, 1.496). The AABB is 2.98 times the plank's area.

    On x: `3 cos 20° + 0.5 sin 20° = 2.819 + 0.171 = 2.990`. On y: `3 sin 20° + 0.5 cos 20° = 1.026 + 0.470 = 1.496`. Area ratio `(4 × 2.990 × 1.496) / (4 × 3 × 0.5) = 17.89 / 6 = 2.98`. Long thin shapes suffer most, because the long half-extent projects onto the short axis.

    </details>

## Week 10. Collision response and impulses

43. **Week 10 · compute.** A 3 kg cart at +4 m/s meets a 1 kg cart at −2 m/s head on, with the normal +x from the heavy cart to the light one and `e = 0.6`. Compute `j`, both final velocities, momentum before and after, and the kinetic energy lost with the reduced-mass formula. Check the energy with the final speeds.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `j = 7.2` N·s. Velocities 1.6 m/s and 5.2 m/s. Momentum 10 before and after. 8.64 J lost, 33.2% of 26 J.

    `v_n = −2 − 4 = −6`. Inverse masses sum to `1/3 + 1 = 4/3`. `j = 1.6 × 6 / (4/3) = 7.2`. `v_A' = 4 − 7.2/3 = 1.6`. `v_B' = −2 + 7.2 = 5.2`. The separation speed is 3.6, which is `0.6 × 6`, as restitution requires.

    `μ = 1 / (4/3) = 0.75` kg. Loss `½ × 0.75 × (1 − 0.36) × 36 = 8.64` J. Check: before `½·3·16 + ½·1·4 = 26` J, after `½·3·2.56 + ½·1·27.04 = 3.84 + 13.52 = 17.36` J. Difference 8.64 J.

    </details>

44. **Week 10 · compute.** A 0.2 kg ball lands on a static floor at `v = (2, −5)` m/s. The normal from the floor to the ball is (0, 1), `e = 0.5`. (a) Give `j` and the new vertical velocity. (b) Give the new horizontal velocity with `μ = 0.3` and with `μ = 0.1`.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `j = 1.5` N·s, new vertical velocity +2.5 m/s. (b) With `μ = 0.3` the ball grips and its horizontal velocity becomes 0. With `μ = 0.1` it keeps 1.25 m/s.

    (a) `v_n = −5`. The floor has inverse mass 0, so `j = 1.5 × 5 / 5 = 1.5`. The ball gains `1.5 / 0.2 = 7.5` m/s upward.

    (b) Stopping the 2 m/s slide needs `0.2 × 2 = 0.4` N·s. With `μ = 0.3` the limit is `0.3 × 1.5 = 0.45`, which is enough. With `μ = 0.1` the limit is 0.15, so the ball loses `0.15 / 0.2 = 0.75` m/s and keeps 1.25.

    </details>

45. **Week 10 · compute.** A ball with bounce 0.8 is dropped from 2 m onto mud with bounce 0.1. Using the week 10 combine rules, what `e` does Box2D v2.4.1 use, Unity with the default Average, Unity with Multiply, and Godot's built-in 3D solver? Give the first bounce height for each (use `e² h`). Does Unity's default bounce threshold of 2 stop the first bounce?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    | Engine and rule | e | First bounce height |
    |---|---|---|
    | Box2D, max | 0.80 | 1.28 m |
    | Unity, Average | 0.45 | 0.405 m |
    | Unity, Multiply | 0.08 | 0.013 m |
    | Godot, sum clamped | 0.90 | 1.62 m |

    The impact speed is `√(2 × 9.81 × 2) = 6.26` m/s, above 2, so the first bounce happens in Unity. Under Godot's sum the mud makes the ball bouncier than on a dead floor, which a designer must know before tuning mud.

    </details>

46. **Week 10 · compute.** Using the week 10 `drop()` model, a ball is dropped from 1.5 m with `e = 0.7`. Give the number of bounces, the last bounce height and the time to rest for thresholds 0.0001 m/s, 1 m/s and 2 m/s, and the exact limit `t₀ (1 + e)/(1 − e)`.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    | Threshold | Bounces | Last bounce | Time to rest |
    |---|---|---|---|
    | 0.0001 m/s | 31 | about 0 m | 3.13 s |
    | 1 m/s | 5 | 0.042 m | 2.70 s |
    | 2 m/s | 3 | 0.176 m | 2.25 s |

    Exact limit `√(2 × 1.5 / 9.81) × 1.7 / 0.3 = 0.553 × 5.667 = 3.13` s.

    The first impact is at `√(2 × 9.81 × 1.5) = 5.42` m/s. Bounce `k` happens while `5.42 × 0.7^(k−1)` is at least the threshold. For 1 m/s, `0.7^(k−1) ≥ 0.184`, so `k − 1 ≤ 4.74` and there are 5 bounces. For 2 m/s, `k − 1 ≤ 2.80`, so 3 bounces. The heights run 0.735, 0.360, 0.176, 0.086, 0.042 m, each `e² = 0.49` of the one before.

    </details>

47. **Week 10 · code.** Two 1 kg crates spawned overlapping by 2 cm are already moving apart. Predict both lines. What line is missing, and what does the player see without it?

    ```python
    def resolve(inv_a, v_a, inv_b, v_b, e):
        v_n = v_b - v_a                  # normal points from A to B, along +x
        j = -(1 + e) * v_n / (inv_a + inv_b)
        return round(v_a - j * inv_a, 3), round(v_b + j * inv_b, 3)

    print(resolve(1.0, -0.5, 1.0, 0.5, 0.8))
    print(resolve(1.0, 2.0, 1.0, 0.0, 0.8))
    ```

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    ```
    (0.4, -0.4)
    (0.2, 1.8)
    ```

    The second line is a correct head-on collision. The first is the bug. The crates separate at `v_n = +1`, yet the code computes `j = −1.8 × 1 / 2 = −0.9` and turns them around so they approach at 0.8 m/s. The next step finds them overlapping and approaching, bounces them apart, and so on, so the crates stick together and buzz.

    The missing line is `if v_n >= 0: return v_a, v_b` before computing `j`.

    </details>

48. **Week 10 · compute.** A box spawns 8 cm into the floor. The solver removes `0.2 × (depth − 0.005)` of overlap per step, as Box2D v2.4.1 does. How many 60 Hz steps until the overlap is within 1 mm of the slop? Why is this better than adding separating velocity?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 20 steps, one third of a second.

    The excess over slop starts at 0.075 m and shrinks by 0.8 per step. It drops below 0.001 m when `0.8^n < 0.0133`, `n > 19.35`, so 20 steps, leaving 0.86 mm.

    The correction moves positions and never writes velocity. Separating velocity would outlive the overlap and launch the box, the "explode apart on spawn" bug.

    </details>

## Week 11. Spatial partitioning

49. **Week 11 · compute.** Players query `r = 6` m at a density of 0.05 per m². Find `s*` and `W(s*)`. How much worse is a cell of 12 m?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `s* = 6.21` m and `W = 25.2`. At 12 m, `W = 32.8`, 30% worse.

    `s* = (2r/ρ)^(1/3) = (12 / 0.05)^(1/3) = 240^(1/3) = 6.21`. `W = (12 + 6.21)² × (1/6.21² + 0.05) = 331.8 × 0.0759 = 25.2`. At 12 m, `24² × (1/144 + 0.05) = 576 × 0.0569 = 32.8`. Doubling the cell size cost only 30%, the cube root's forgiveness.

    </details>

50. **Week 11 · compute.** An arena holds 1,200 players in an 80 m square who query `r = 3` m. The surrounding plains hold monsters at 0.0008 per m² who query `r = 40` m. (a) Find `s*` for each and their ratio. (b) With one grid of 8 m, how many times its own best does each group pay? (c) Recommend a structure.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) Arena 3.17 m, plains 46.4 m, ratio 14.6. (b) Arena 1.65 times, plains 6.3 times. (c) Two grids (3 m and 45 m) or a quadtree.

    (a) Arena `ρ = 1200 / 6400 = 0.1875`, `s* = (6 / 0.1875)^(1/3) = 32^(1/3) = 3.17`. Plains `s* = (80 / 0.0008)^(1/3) = 100,000^(1/3) = 46.4`.

    (b) Arena: `W(3.17) = 24.1`, `W(8) = 39.8`. Plains: `W(46.4) = 20.2`, `W(8) = 127.2`.

    (c) The ratio 14.6 is above the lecture's rule of thumb of 2, so no single grid is close to ideal for both. Exactly two query types differ, so two grids each at its own optimum is the simplest win. A quadtree also works without knowing where the arena is, at the price of its descent cost.

    </details>

51. **Week 11 · compute.** A quadtree with capacity 4 covers a 512 m square root. About how wide are the leaves in a region of density 0.25 per m², and at what depth are they?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** About 4 m wide, at depth 7.

    Leaves split until each holds about `k` entities, so a leaf's area is about `k / ρ = 4 / 0.25 = 16` m², 4 m across. Each level halves the width, and `512 / 2^7 = 4`, so depth 7.

    </details>

52. **Week 11 · design.** A bullet-hell arena is 200 m × 120 m with 5,000 bullets that each move several metres per frame. Four players each query radius 0.5 m against the bullets every frame. Choose a structure, a cell size and an update strategy, and justify them with numbers.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** A hashed grid rebuilt every frame, with cells of about 1.7 m.

    Density `ρ = 5000 / 24,000 = 0.208` per m². `s* = (1 / 0.208)^(1/3) = 1.69` m, where `W = 4.0` per query. The four queries cost about 16 units a frame. The update cost dominates. Rebuilding is 5,000 dictionary inserts with no bookkeeping, and bullets that move several metres per frame would change cells almost every frame anyway, so "update on cell change" saves nothing. A quadtree rebuild costs 5,000 inserts times its depth. The model's numbers favour the grid clearly. A different answer earns full marks if it counts update cost against query cost with numbers.

    </details>

## Week 12. Raycasting

53. **Week 12 · compute.** A ray starts at (1.2, 0.5) in a unit grid at 30° (`d = (0.866, 0.5)`). Give `t_delta_x`, `t_delta_y`, the first `t_max_x` and `t_max_y`, and the first five cells the grid walk enters with the `t` of each.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `t_delta = (1.1547, 2.0)`. First `t_max = (0.9238, 1.0)`.

    | Step | t | Enter cell |
    |---|---|---|
    | 1 | 0.9238 | (2, 0) |
    | 2 | 1.0000 | (2, 1) |
    | 3 | 2.0785 | (3, 1) |
    | 4 | 3.0000 | (3, 2) |
    | 5 | 3.2332 | (4, 2) |

    The first vertical line is x = 2, `0.8 / 0.866 = 0.9238` away. The first horizontal line is y = 1, `0.5 / 0.5 = 1.0` away. Cross whichever is smaller and add that axis's `t_delta` to it: x at 0.924, then y at 1.0, then x at 2.079, then y at 3.0, then x at 3.233.

    </details>

54. **Week 12 · compute.** A ray starts at (0, 1, 0) with unit direction (0.6, 0, 0.8). (a) Find the first hit with a sphere of radius 1 centered at (6, 1.5, 8), and the hit point. (b) Does it hit if the center moves to (6, 2.2, 8)?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `t = 9.134`, hit point (5.480, 1.0, 7.307). (b) No, the discriminant is −0.44.

    (a) `m = o − c = (−6, −0.5, −8)`. `b = m · d = −3.6 − 6.4 = −10`. `k = 36 + 0.25 + 64 − 1 = 99.25`. `disc = 100 − 99.25 = 0.75`. `t = 10 − √0.75 = 9.134`. The point is `o + t d`.

    (b) The center is now 1.2 from the ray's line, more than the radius. `k = 36 + 1.44 + 64 − 1 = 100.44`, `disc = 100 − 100.44 < 0`.

    </details>

55. **Week 12 · compute.** A ray from (1, 1, 0) with direction (0.8, 0.6, 0) meets the box from (4, 2, −1) to (7, 5, 1). Give each slab interval, the entry and exit `t`, and the entry point.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** x slab 3.75 to 7.5. y slab 1.667 to 6.667. z no limit. Entry 3.75, exit 6.667. Entry point (4, 3.25, 0).

    x: `(4 − 1)/0.8 = 3.75`, `(7 − 1)/0.8 = 7.5`. y: `(2 − 1)/0.6 = 1.667`, `(5 − 1)/0.6 = 6.667`. z: `d_z = 0` and the origin's z = 0 lies inside [−1, 1]. Entry is the largest entry, 3.75. Exit is the smallest exit, 6.667. Entry comes first, so it hits at `(1 + 3.75 × 0.8, 1 + 3.75 × 0.6, 0) = (4, 3.25, 0)`.

    </details>

56. **Week 12 · compute.** A raycast renderer draws column height `300 / dist`. A wall is square to the view, 5 units ahead. How tall is the center column, and the column for a ray 25° off the view direction, with and without the perpendicular correction? What percent short is the uncorrected edge?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Center 60. At 25° off axis, 54.4 without the correction and 60 with it. The uncorrected column is 9.4% short.

    The ray at 25° travels `5 / cos 25° = 5.517` to the wall. `300 / 5.517 = 54.4`. The perpendicular distance is `5.517 × cos 25° = 5`, which gives 60 like the center.

    </details>

57. **Week 12 · code.** Using the week 12 `dda_cells` and `sampled_cells` functions (quarter-cell sampling), predict what this prints. What does the missing cell mean for a line-of-sight check?

    ```python
    import math

    def dda_cells(ax, ay, bx, by):
        dx, dy = bx - ax, by - ay
        cx, cy, end = int(ax), int(ay), (int(bx), int(by))
        sx, sy = (1 if dx > 0 else -1), (1 if dy > 0 else -1)
        tdx = abs(1 / dx) if dx else math.inf
        tdy = abs(1 / dy) if dy else math.inf
        tmx = ((cx + (dx > 0)) - ax) / dx if dx else math.inf
        tmy = ((cy + (dy > 0)) - ay) / dy if dy else math.inf
        cells = [(cx, cy)]
        while (cx, cy) != end:
            if tmx < tmy:
                cx, tmx = cx + sx, tmx + tdx
            else:
                cy, tmy = cy + sy, tmy + tdy
            cells.append((cx, cy))
        return cells

    def sampled_cells(ax, ay, bx, by, per_cell=4):
        n = max(1, math.ceil(per_cell * max(abs(bx - ax), abs(by - ay))))
        return list(dict.fromkeys((int(ax + (bx - ax) * i / n), int(ay + (by - ay) * i / n))
                                  for i in range(n + 1)))

    walk = dda_cells(0.2, 0.8, 5.3, 2.4)
    samp = sampled_cells(0.2, 0.8, 5.3, 2.4)
    print(walk)
    print([c for c in walk if c not in samp])
    ```

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    ```
    [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (4, 2), (5, 2)]
    [(4, 1)]
    ```

    The segment clips the corner of cell (4, 1) between two samples, which are about 0.26 units apart along it. A pillar in (4, 1) would not block the sampled check, so a player could see through its corner. The grid walk visits every cell the segment crosses and would block the view.

    </details>

## Week 13. Projectile motion and aiming

58. **Week 13 · compute.** A turret fires bolts at 20 m/s at a runner 40 m away moving straight across at 8 m/s. Give the flight time, the aim point and the lead angle.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 2.182 s, aim point (40, 17.46), lead 23.58°.

    `D · u = 0`, so `b = 0` and `t = |D| / √(s² − |u|²) = 40 / √336 = 2.182`. The runner moves `8 × 2.182 = 17.46` m. `atan(17.46 / 40) = 23.58°`.

    </details>

59. **Week 13 · compute.** A target 30 m away along +x moves at `u = (−6, 6)` m/s, toward the shooter and across. The shot flies at 15 m/s. Give `a`, `b`, `c`, the discriminant, both roots, the flight time, the aim point and the lead angle.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `a = −153`, `b = −360`, `c = 900`, discriminant 680,400, roots −3.872 and 1.519. Flight time 1.519 s, aim point (20.89, 9.11), lead 23.58°.

    `a = 72 − 225 = −153`. `b = 2 × (30 × −6) = −360`, negative because the target closes. `c = 900`. `disc = 129,600 + 550,800 = 680,400`, root 824.9. Roots `(360 ∓ 824.9) / (−306)`. The shot is faster than the target, so exactly one root is positive. The aim point is `(30 − 6 × 1.519, 6 × 1.519)`.

    </details>

60. **Week 13 · explain.** Questions 58 and 59 have the same lead angle, 23.58°, with different distances, speeds and headings. Show why, and state the rule.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** The sine of the lead angle equals the target's speed across the line of fire divided by the shot speed, `sin(lead) = u⊥ / s`. Both questions have `u⊥ / s = 0.4`.

    Take the triangle formed by the shooter, the target's start and the intercept point. The side from the shooter to the intercept has length `s t`, and the side along the target's path has length `|u| t`. By the law of sines, `sin(lead) / (|u| t) = sin(β) / (s t)`, where `β` is the angle at the target's start between its path and the line back to the shooter. `|u| sin β` is `u⊥`, the target's speed across the line of fire. So `sin(lead) = u⊥ t / (s t) = u⊥ / s`, and the flight time cancels.

    Question 58: `8 / 20 = 0.4`. Question 59: the across component is 6 m/s, and `6 / 15 = 0.4`. `asin(0.4) = 23.58°`. Motion along the line of fire changes the flight time, not the lead angle. That is why an archer's lead depends only on how fast the target crosses its view.

    </details>

61. **Week 13 · compute.** A slow spell flies at 10 m/s. A monster starts 50 m away along +x. (a) With `u = (−12, 9)` m/s, can the spell hit, and when? Give the aim point. (b) With `u = (−9, 12)`, same speed, what changes?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) Yes. The earliest root is 3.056 s, aim point (13.32, 27.51). (b) No intercept.

    (a) `a = 225 − 100 = 125`, `b = 2 × (50 × −12) = −1200`, `c = 2500`. `disc = 1,440,000 − 1,250,000 = 190,000`, root 435.9. Both roots, 3.056 and 6.544, are positive because the shot is slower than a closing target. The first is the hit. Check: the aim point's distance is 30.56 m, which is `10 × 3.056`.

    (b) `b = 2 × (50 × −9) = −900`. `disc = 810,000 − 1,250,000 < 0`. The monster closes more slowly and crosses faster, so the spell's growing reach circle never touches it. The AI needs a fallback.

    </details>

62. **Week 13 · compute.** An archer shoots at 30 m/s under `g = 9.81` at a target 50 m away horizontally and 5 m below. Give the low and high arc angles and flight times. What is the maximum range on flat ground?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Low arc 10.29° (1.69 s). High arc 74.00° (6.05 s). Maximum flat range 91.7 m.

    `s² = 900`, `s⁴ = 810,000`. The root's argument is `810,000 − 9.81 × (9.81 × 2500 + 2 × (−5) × 900) = 810,000 − 152,300 = 657,700`, root 811.0. `tan θ = (900 ∓ 811.0) / 490.5`, giving 0.1815 and 3.488. Flight time `50 / (30 cos θ)`. Maximum range `s² / g = 91.7` m.

    </details>

63. **Week 13 · compute.** A wizard's bolt flies at 25 m/s after a 0.3 s cast. The target is 15 m away along +x, moving across at 5 m/s, and has a hit radius of 0.6 m. (a) Give `D'`, the flight time after release and the total time from the start of the cast. (b) With a 0.25 s reaction time, what is the dodge budget, and is the bolt dodgeable at this range? (c) Is there any range at which it is not?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `D' = (15, 1.5)`, flight 0.628 s, total 0.928 s. (b) 3.39 m, far more than 0.6 m, so dodgeable. (c) No. Even at 1 m the budget is 0.69 m.

    (a) During the cast the target moves `5 × 0.3 = 1.5` m. `a = 25 − 625 = −600`, `b = 2 × 1.5 × 5 = 15`, `c = 227.25`. `disc = 225 + 545,400 = 545,625`, root 738.7. The positive root is `(−15 − 738.7) / (−1200) = 0.628`.

    (b) `|u| (τ + t − t_react) = 5 × (0.3 + 0.628 − 0.25) = 3.39` m.

    (c) The cast delay already exceeds the reaction time, so the budget is at least `5 × 0.05 = 0.25` m plus the flight. At 1 m the flight is 0.087 s and the budget is 0.69 m. A designer who wants point-blank hits to land must shorten the cast below the reaction time or grow the hit radius.

    </details>

64. **Week 13 · compute.** A shooter uses the fixed-point iteration `t_next = |D + u t| / s` with `D = (20, 0)`, `u = (0, 6)` and `s = 12`, starting from `t = 0`. Give the first four iterates and how far the target is from each aim point on arrival. Compare with the exact root.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    | Guess | Assumed t | Actual t to that point | Miss on arrival |
    |---|---|---|---|
    | 0 | 0 | 1.6667 | 10.0 m |
    | 1 | 1.6667 | 1.8634 | 1.18 m |
    | 2 | 1.8634 | 1.9094 | 0.28 m |
    | 3 | 1.9094 | 1.9207 | 0.07 m |

    Exact root `20 / √(144 − 36) = 1.9245` s.

    The miss is `6 × (actual − assumed)`. Each step cuts it by about a factor of 4 here, slower than the TF2 example's factor of 8, because the target is half as fast as the shot instead of about a third. The closer the speeds, the slower the iteration, and the quadratic has no such limit.

    </details>

65. **Week 13 · code.** Write `lead_aim(D, u, s, delay=0.0)` for a straight shot. It returns `(t_flight, aim_point)` or `None`, handles a cast delay, a target as fast as the shot, a negative discriminant and no positive root. Test it on question 63, on question 61(b), and on a target 20 m away approaching head on at the shot's own speed of 10 m/s.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** One correct version, which prints `0.6281 (15.0, 4.64)`, then `None`, then `(1.0, (10.0, 0.0))`:

    ```python
    import math

    def lead_aim(D, u, s, delay=0.0):
        """Aim point for a straight shot at speed s that leaves after `delay` seconds.
        D and u are 2D tuples relative to the shooter. Returns (t_flight, aim) or None."""
        dx, dy = D[0] + u[0] * delay, D[1] + u[1] * delay      # where the target is at release
        a = u[0] ** 2 + u[1] ** 2 - s * s
        b = 2 * (dx * u[0] + dy * u[1])
        c = dx * dx + dy * dy
        if abs(a) < 1e-9:
            t = -c / b if b < 0 else None
        else:
            disc = b * b - 4 * a * c
            if disc < 0:
                return None
            r = math.sqrt(disc)
            t = next((x for x in sorted(((-b - r) / (2 * a), (-b + r) / (2 * a))) if x > 0), None)
        if t is None:
            return None
        return t, (dx + u[0] * t, dy + u[1] * t)

    t, aim = lead_aim((15.0, 0.0), (0.0, 5.0), 25.0, delay=0.3)
    print(round(t, 4), tuple(round(x, 3) for x in aim))
    print(lead_aim((50.0, 0.0), (-9.0, 12.0), 10.0))
    print(lead_aim((20.0, 0.0), (-10.0, 0.0), 10.0))
    ```

    Marking: the tolerance on `a`, the sign test on `b` in the linear case, the discriminant check, and choosing the smallest positive root each carry marks. The head-on case has `a = 0` and `t = −400 / (2 × 20 × −10) = 1.0` s, meeting at 10 m.

    </details>

## Week 14. Determinism and floating point

66. **Week 14 · compute.** Give the float32 gap at 3,000 m, 40,000 m and 1,500 km, in millimetres.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 0.244 mm, 3.91 mm and 125 mm.

    3,000 lies in [2,048, 4,096), so the gap is `2^(11 − 23) = 2⁻¹²` m. 40,000 lies in [32,768, 65,536), gap `2⁻⁸` m. 1,500,000 lies in [1,048,576, 2,097,152), gap `2⁻³ = 0.125` m.

    </details>

67. **Week 14 · compute.** A creeping enemy moves at 0.8 m/s on a 30 Hz tick in float32. (a) What speed does it actually move at 150 km from the origin? (b) At what distance does it freeze?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 0.9375 m/s, 17% fast. (b) From 524,288 m.

    (a) The step is `0.8 / 30 = 0.02667` m. At 150 km the gap is `2^(17 − 23) = 0.015625` m. `0.02667 / 0.015625 = 1.71` rounds to 2 gaps, 0.03125 m per tick, which is `0.03125 × 30 = 0.9375` m/s.

    (b) It freezes once the gap exceeds twice the step, 0.0533 m. The first such gap is `2⁻⁴ = 0.0625`, which starts at `2¹⁹ = 524,288` m.

    </details>

68. **Week 14 · compute.** A server keeps `time_since_start` in float32 and adds `dt` each tick. After how many hours does the clock stop at 30 Hz, and at 60 Hz? What should it do instead?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 291 hours at 30 Hz, 145.6 hours at 60 Hz. Count ticks in a 64-bit integer and compute time as `tick × dt` in double when needed.

    At 30 Hz `dt = 0.0333`, and the clock stops when the gap exceeds 0.0667. The first such gap is `2⁻³ = 0.125` s, from `2²⁰ = 1,048,576` s. At 60 Hz the gap must exceed 0.0333, first at `2⁻⁴ = 0.0625` from `2¹⁹ = 524,288` s. The clock runs at the wrong rate long before it stops.

    </details>

69. **Week 14 · compute.** A game stores positions as int32 millimetres and moves a runner at 2.5 m/s on a 144 Hz tick by adding a rounded whole number of millimetres. What speed does the runner have, and does it depend on distance? What is the range limit? How would you remove the speed error?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 2.448 m/s, 2.1% slow, at every distance. The range limit is 2³¹ mm, about 2,147 km. Carry the remainder from tick to tick, or use a smaller unit.

    The step is `2500 / 144 = 17.36` mm, which rounds to 17 mm, and `17 × 144 = 2448` mm per second. Carrying the 0.36 mm remainder into the next tick makes the long-run speed exact.

    </details>

70. **Week 14 · code.** Predict the three lines this prints.

    ```python
    import struct

    def f32(x):
        return struct.unpack("<f", struct.pack("<f", x))[0]

    print(f32(2**24 + 1), f32(2**24 + 3))
    print(f32(10_000.0 + 0.001), f32(10_000.0 + 0.0004))
    t = f32(40 * 3600.0)
    for _ in range(20):
        t = f32(t + f32(1 / 20))
    print(round(t - 40 * 3600.0, 4))
    ```

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.**

    ```
    16777216.0 16777220.0
    10000.0009765625 10000.0
    0.9375
    ```

    At `2²⁴` the gap is 2. `2²⁴ + 1` is a tie and rounds to the even neighbour, `2²⁴`. `2²⁴ + 3` is also a tie between 16,777,218 and 16,777,220 and rounds to the one with the even significand, 16,777,220.

    At 10,000 the gap is `2⁻¹⁰ = 0.000977`. Adding 0.001 is just over one gap and moves one step. Adding 0.0004 is less than half a gap and is lost.

    At 40 hours (144,000 s) the gap is `2⁻⁶ = 0.015625` s. Each 0.05 s tick is 3.2 gaps, which rounds to 3, so 20 ticks (one real second) advance the clock by `20 × 3 × 0.015625 = 0.9375` s.

    </details>

71. **Week 14 · critique.** A teammate proposes a lockstep checksum that compares peers' positions rounded to 6 decimal places and resynchronizes only when they differ. Using the week 14 arena numbers, say what goes wrong and what the checksum should hash instead.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** The check passes while the simulations have already split, and it fires only once the divergence is visible.

    In the week 14 arena, a one-bit difference entered the velocity at tick 1,402 (11.7 s). It first reached the positions at tick 2,012 (16.8 s), in the last bits only, and stayed in them from 20.5 s. Positions rounded to 6 decimals first disagree at tick 4,581 (38.2 s), and the difference was 1.4 units at 60 s. The rounded-position check stays silent for 26.5 seconds after the cause, and rounding can also hide a difference that sits just across a rounding boundary on one peer. By the time it fires, the two games are far apart and the replay has no record of where they split.

    Hash the exact bits of every value the next tick reads, velocities included, every tick. The first differing tick then points at the cause. A tolerance cannot work, because chaos grows any difference.

    </details>

72. **Week 14 · design.** Your sandbox world is a 20 km square centered on the origin, simulated in float32 at 60 Hz. The slowest mover is a lift at 0.3 m/s. Sessions last up to 12 hours with a float32 clock. Rate positions and the clock as safe (at least 20 gaps per step), visible (2 to 20) or broken (under 2), and propose representations.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Positions are visible (5.1 gaps per step at the edge). The clock is visible (4.3 gaps per tick at 12 hours, running 6.25% slow). Use an integer tick counter for time. For positions, use a floating origin or local frames for slow movers, or float64 on the server.

    The edge coordinate is 10,000 m, where the gap is `2⁻¹⁰ = 0.977` mm. The lift moves `0.3 / 60 = 5` mm per tick, which is 5.1 gaps. At 12 hours, 43,200 s, the gap is `2⁻⁸ = 0.0039` s. One tick of 0.01667 s is 4.27 gaps, which rounds to 4, so the clock advances 0.015625 s per tick and runs 6.25% slow. The costs to state: a floating origin needs every absolute position shifted in the same frame, and doubles double the memory of every position.

    </details>

## Cross-week questions

73. **Weeks 12 and 14 · compute.** A ricochet laser restarts each ray `ε = 0.001` m along the surface normal to avoid hitting the same wall. The level is built in float32 metres. Is that safe at x = 10,000 m? What about `ε = 0.0004`? Recommend a rule for `ε`.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** At 10,000 m, 0.001 m is barely one gap (0.000977 m), so the offset survives by one step and rounding in the hit point can undo it. 0.0004 m is lost completely, `f32(10000 + 0.0004) = 10000`, and the laser hits its own wall at `t ≈ 0`. Choose `ε` as several gaps at the largest coordinate the level uses, or cast in a local frame near the origin.

    The gap in [8,192, 16,384) is `2⁻¹⁰` m. `f32(10000 + 0.001) = 10000.0009765625`, one gap. A rule such as `ε ≥ 8 × gap32(max coordinate)` gives 7.8 mm at 10 km, which is still invisible to a player.

    </details>

74. **Weeks 6, 7 and 13 · compute.** An archer's arrow flies for 2.0 s. The game steps it with semi-implicit Euler at 30 Hz under `g = 9.81`, but the aim solver assumes the exact parabola. How far below the aim point does the arrow arrive? What two fixes does the week 13 lecture offer?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 0.327 m low. Aim with the same integrator the game flies with, or fly the arrow on the exact formula from its launch time.

    Semi-implicit Euler's drop after `n` steps is `½ g dt² n(n + 1)`, which is the exact `½ g t²` plus `½ g t dt`. That extra is `0.5 × 9.81 × 2.0 / 30 = 0.327` m. Stepping 60 ticks in Python gives a drop of 19.947 m against the exact 19.620 m. At 60 Hz the error halves. A third of a metre is enough to miss a head.

    </details>

75. **Weeks 9 and 10 · compute.** A static box A and a 1 kg crate B are in contact with the question 39 MTV normal, `n = (0.5, 0.866)`. B moves at `(−1, −1)` m/s and `e = 0`. (a) Give `v_n`, `j` and B's new velocity. (b) A bug flips the normal to `(−0.5, −0.866)`. What does the resolver do now?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `v_n = −1.366`, `j = 1.366` N·s, new velocity `(−0.317, 0.183)`. (b) It sees `v_n = +1.366`, decides the bodies are separating, and applies no impulse. The crate keeps sinking into the box.

    (a) `v_n = (−1, −1) · (0.5, 0.866) = −1.366`. With A static, `j = 1 × 1.366 / 1`. `v' = (−1, −1) + 1.366 × (0.5, 0.866)`. The new normal speed is 0, as `e = 0` requires, and the crate slides along the face.

    (b) The sign of `v_n` flips with the normal, so the approach test fails. This is the week 9 warning in numbers. Always check `d · n > 0` when building the contact.

    </details>
