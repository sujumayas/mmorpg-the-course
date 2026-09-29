# MA201 · Week 02 — Matrices and Linear Transformations

**Why this matters:** Rotating a sprite, stretching a health bar, mirroring a character, drawing an isometric map and working out which tile the mouse is on are all the same operation. A matrix is a small table of numbers that does that operation, and once you can read one you can build, combine and undo any of them. Every transform in every engine you will use is stored this way.

**You will be able to:**
- Read a 2×2 or 3×3 matrix as "where the axes land" and compute its effect on any vector by hand.
- Build the tile-to-screen matrix for an isometric map from the tile size, and invert it to turn a mouse click into a tile.
- Compose transforms by matrix multiplication, and predict when changing the order changes the result.
- Compute a determinant and use it to predict area change, mirroring, and whether a transform can be undone.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed., 2011), chapter 4 (introduction to matrices) and chapter 5 (matrices and linear transformations), the sections on rotation, scale, reflection and shearing. Godot Engine documentation (4.x), tutorial "Matrices and transforms", the first half, up to translation.

**Prerequisites from earlier courses:** [MA201 week 1](w01-vectors-in-3d-and-the-cross-product.md) (cross product, winding order). [MA101 week 10, angles, sin and cos](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) and [MA101 week 12, 2D vectors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w12-2d-vectors.md). [CS102 week 7, scene graphs](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w07-trees-scene-graphs-and-skill-trees.md), where you used the rotation formula `R(t) · (x, y)` without calling it a matrix.

**Interactive:** [examples/w02-isometric-basis.html](../examples/w02-isometric-basis.html). Keep it open during section 3.

---

## 1. Transformations that keep the grid straight

A **transformation** of the plane is a rule that moves every point to a new point. Rotating a sprite, scaling it, mirroring it and slanting it are all transformations. So is sliding it sideways.

A transformation is **linear** when it obeys two rules for all vectors `a`, `b` and numbers `k`:

```
T(a + b) = T(a) + T(b)
T(k a)   = k T(a)
```

In pictures, that means three things. The origin stays put, because `T(0) = T(0 · a) = 0 · T(a) = 0`. Straight lines stay straight. And evenly spaced grid lines stay parallel and evenly spaced, even if they tilt, stretch or lean.

Rotation about the origin, scaling, mirroring and shearing are linear. Sliding sideways is not, because it moves the origin. That is a real limitation, and week 4 removes it with a trick called homogeneous coordinates. For this week, everything is centered on the origin, and next week you will pair each matrix with a separate offset.

Why care about linearity? Because it means you only need to know where two vectors go. Every 2D vector is some amount of `x̂ = (1, 0)` plus some amount of `ŷ = (0, 1)`:

```
v = (vx, vy) = vx · x̂ + vy · ŷ
```

Apply a linear `T` and the two rules give

```
T(v) = vx · T(x̂) + vy · T(ŷ)
```

Know where `x̂` and `ŷ` land and you know where everything lands. Those two landing points are the whole transformation.

## 2. A matrix is where the axes land

Write the landing point of `x̂` as the first column and the landing point of `ŷ` as the second column. That table is the **matrix** of the transformation:

```
M = | a  b |      first column (a, c)  = where x̂ lands
    | c  d |      second column (b, d) = where ŷ lands

M v = vx · (a, c) + vy · (b, d) = (a vx + b vy,  c vx + d vy)
```

The last line is **matrix-vector multiplication**. The usual rule, "row times column", computes exactly the same numbers. Use whichever reading helps. The column reading tells you what a matrix *means*. The row reading is how you compute it quickly.

The vectors that the columns describe are called the **basis vectors** of the transformed space, and together they are its **basis**.

Here is a small gallery. Read each matrix by its columns before you read the description.

| Transformation | Matrix (rows) | x̂ lands at | ŷ lands at | What it does to a unit square |
|---|---|---|---|---|
| Identity | `[1 0; 0 1]` | (1, 0) | (0, 1) | nothing |
| Scale by 2 in x | `[2 0; 0 1]` | (2, 0) | (0, 1) | stretches it wide |
| Mirror in x | `[−1 0; 0 1]` | (−1, 0) | (0, 1) | flips it left to right |
| Rotate by t | `[cos t  −sin t; sin t  cos t]` | (cos t, sin t) | (−sin t, cos t) | turns it counter-clockwise |
| Shear | `[1 0.5; 0 1]` | (1, 0) | (0.5, 1) | leans it into a parallelogram |

(`[a b; c d]` means first row `a b`, second row `c d`.)

The rotation row is worth a second look. In CS102 week 7 you rotated a child's offset with `R(t) · (x, y) = (x cos t − y sin t, x sin t + y cos t)`. That formula *is* this matrix times `(x, y)`. The columns say why it works. The x-axis turns to angle `t`, which is `(cos t, sin t)` from MA101 week 10. The y-axis turns to angle `t + 90°`, which is `(−sin t, cos t)`.

In code, the column reading is two scaled vectors added:

```python
def mat_vec(M, v):
    (a, b), (c, d) = M
    return (a*v[0] + b*v[1], c*v[0] + d*v[1])

shear = ((1, 0.5), (0, 1))
print(mat_vec(shear, (2, 2)))    # (3.0, 2)
```

The point `(2, 2)` is 2 steps along the first column `(1, 0)` and 2 steps along the second column `(0.5, 1)`. That lands at `(2 + 1, 0 + 2) = (3, 2)`.

## 3. Worked example: Diablo's tiles and the mouse click

### The hook

Diablo (1996) draws its dungeons as a grid of diamond-shaped floor tiles seen from above at an angle. Many games of that decade did the same, and players call the look "isometric". Two facts about it surprise most people.

First, it is not isometric. DevilutionX, the community source port of Diablo built from a reconstruction of the original code, defines each floor tile as 64 pixels wide and 32 pixels tall. A diamond twice as wide as it is tall has edges that rise one pixel for every two across, an angle of `atan(1/2) = 26.57°`. A true isometric drawing needs 30°. The 2:1 ratio won because a line that steps two pixels across and one up is perfectly clean on a pixel grid, and a 30° line is not.

Second, working out which tile you clicked on is harder than it looks. The obvious code cuts the screen into 64×32 rectangles, one per tile, and picks the tile drawn in the middle of the rectangle you clicked. That picks the wrong tile for exactly half of all clicks, because each diamond fills only half of its rectangle. DevilutionX handles it in two steps. It finds the rectangle, then tests which corner triangle of the rectangle the click fell in and shifts to the neighbouring tile. The map editor Tiled solves the same problem in one line, by inverting a matrix.

### The model

Name the quantities:

- `(i, j)` is a tile coordinate. `i` counts tiles along one diagonal of the screen, `j` along the other.
- `(x, y)` is a screen position in pixels, with y pointing *down*, as it does on screens, in Tiled and in Godot's 2D.
- `w` and `h` are the tile's width and height in pixels. Diablo uses `w = 64`, `h = 32`.

Ask the section 2 question. Where does one step along `i` land on screen? Moving one tile along `i` goes half a tile right and half a tile down: `(w/2, h/2)`. One step along `j` goes half a tile left and half a tile down: `(−w/2, h/2)`. Those are the columns:

```
M = | w/2  −w/2 |          (x, y) = M (i, j) = ( (i − j) · w/2,  (i + j) · h/2 )
    | h/2   h/2 |
```

This puts the top corner of tile `(0, 0)` at the screen origin. A real renderer adds a fixed offset to center the map. That offset is not part of the matrix (section 1), so leave it out until week 4.

To go the other way, from a click to a tile, you need the **inverse matrix** `M⁻¹`, the matrix that undoes `M`. For any 2×2 matrix,

```
M = | a  b |       det(M) = a d − b c       M⁻¹ = 1/det(M) · |  d  −b |
    | c  d |                                                 | −c   a |
```

`det(M)` is the **determinant**, covered properly in section 5. For the tile matrix, `det(M) = (w/2)(h/2) − (−w/2)(h/2) = w h / 2`. Plug in and simplify:

```
M⁻¹ = |  1/w  1/h |          i = x/w + y/h
      | −1/w  1/h |          j = y/h − x/w
```

The tile you clicked is `(floor(i), floor(j))`. `floor` rounds down, so any point inside a diamond maps to that diamond's integer corner.

### Numbers you can check

Use Diablo's tile size, `w = 64` and `h = 32`, so `M = [32 −32; 16 16]` and `M⁻¹ = [1/64 1/32; −1/64 1/32]`.

Tile to screen (top corner of each tile):

| Tile (i, j) | x = 32(i − j) | y = 16(i + j) |
|---|---|---|
| (0, 0) | 0 | 0 |
| (1, 0) | 32 | 16 |
| (0, 1) | −32 | 16 |
| (1, 1) | 0 | 32 |
| (3, 2) | 32 | 80 |
| (2, 5) | −96 | 112 |

The center of a tile is its corner plus half a step along both axes, `M(i + 0.5, j + 0.5)`. For tile (0, 0) that is `(0, 16)`, which is `h/2` straight below the top corner, as it should be.

Screen to tile, compared with the obvious rectangle method. The rectangle method uses rectangles 64 wide and 32 tall, placed so that rectangle `(k, m)` has tile `(k + m, m − k)` drawn in its middle. It computes `k = floor((x + 32)/64)` and `m = floor(y/32)` and returns that middle tile.

| Click (x, y) | i = x/64 + y/32 | j = y/32 − x/64 | Correct tile | Rectangle method |
|---|---|---|---|---|
| (0, 8) | 0.250 | 0.250 | (0, 0) | (0, 0) |
| (0, 31) | 0.969 | 0.969 | (0, 0) | (0, 0) |
| (0, 33) | 1.031 | 1.031 | (1, 1) | (1, 1) |
| (40, 30) | 1.563 | 0.313 | (1, 0) | (1, −1) |
| (30, 10) | 0.781 | −0.156 | (0, −1) | (0, 0) |
| (−20, 50) | 1.250 | 1.875 | (1, 1) | (1, 1) |
| (100, 120) | 5.313 | 2.188 | (5, 2) | (5, 1) |

Check row (40, 30) by hand. `40/64 = 0.625` and `30/32 = 0.9375`, so `i = 1.5625` and `j = 0.3125`. Floors give tile (1, 0). Now confirm with the forward matrix. Tile (1, 0)'s corners are at `M(1,0) = (32, 16)`, `M(2,0) = (64, 32)`, `M(1,1) = (0, 32)` and `M(2,1) = (32, 48)`. The point (40, 30) sits inside that diamond.

The rectangle method is right near the middle of each rectangle and wrong in its four corners. Each corner triangle belongs to a neighbouring diamond. The four corners together are exactly half the rectangle's area, since a diamond's area is `w h / 2` (section 5 shows this is the determinant). Scan every pixel of a screen and the method is wrong for 50.0% of them. Rows (40, 30), (30, 10) and (100, 120) are corner clicks.

Row (30, 10) shows that the answer can be negative. That click is above and right of tile (0, 0), in tile (0, −1). Your map lookup must check bounds.

### The visual

Open [examples/w02-isometric-basis.html](../examples/w02-isometric-basis.html). The left view is "tile space", a plain square grid with `î` and `ĵ` arrows. The right view is "screen space", the same grid after `M`, drawn as diamonds, with the two columns of `M` shown as arrows from the origin.

Move the mouse over the screen view. The tile under the cursor lights up in both views, and a readout shows `(x, y)`, the unrounded `(i, j)` and the tile. Turn on "rectangle picking" and a dashed outline shows the rectangle method's answer. Sweep the cursor across one rectangle and watch the two answers agree in the middle and split in the corners. The "error map" toggle shades every pixel where they disagree. It covers half of every rectangle, so the readout, measured over the whole rectangles in view, always says 50.0%.

Now drag the arrow tips on the right. The whole grid follows, because the arrows *are* the matrix. Drag the `ĵ` arrow until it lies on top of `î`. The diamonds squash into a line, the determinant readout hits 0, and the picker reports "no inverse". Drag it past and the determinant turns negative, the diamond outlines change to the back-face colour from week 1, and the tile numbering runs the other way round.

### Cross-game recognition

**Tiled (map editor, version 1.12).** Tiled's isometric renderer converts tile to screen with `((x − y) · tileWidth/2 + originX, (x + y) · tileHeight/2)`, where `originX` centers the map. That is `M` plus an offset. Its screen-to-tile function subtracts the offset, then returns `(y/tileHeight + x/tileWidth, y/tileHeight − x/tileWidth)`. That is `M⁻¹`, term for term.

**DevilutionX (Diablo 1996 source port, version 1.5.5).** Tiles are `TILE_WIDTH 64` by `TILE_HEIGHT 32`. The mouse code first divides the screen position by 64 and 32 (the rectangle method), then compares the position inside the rectangle against the lines `py = px/2` and `py = 32 − px/2` to find which corner triangle the click is in, and shifts the tile. That is the inverse matrix worked out by hand for one specific `M`. The code is fast, and it gets the same answers, but you must rewrite it if the tile ratio ever changes. The matrix version works for any `w` and `h`.

**Godot 4.x, `Transform2D`.** Godot stores every 2D transform as three `Vector2` values named `x`, `y` and `origin`. Its class reference says `x` is column 0 of the matrix and `y` is column 1. By default `x` points right and `y` points *down*, the same screen convention as the table above. The reference also warns that rotating one axis on its own makes the transform "skewed". That is the shear row of the section 2 gallery. When you inspect a node's transform in Godot, you are reading where its axes land.

**True isometric.** For a true 30° projection, the columns are `(s cos 30°, s sin 30°)` and `(−s cos 30°, s sin 30°)`. The tile width-to-height ratio is `cos 30° / sin 30° = √3 ≈ 1.732`, so a 64-pixel-wide tile would be 36.95 pixels tall. The model is identical. Only two numbers in `M` change, and the picker keeps working without any new code.

Four places, one idea. A projection from tile space to screen space is a matrix whose columns are the screen steps for one tile along each axis, and picking is its inverse.

### Eyes-open design judgment

- **Pick the ratio for the art, not the math.** 2:1 gives clean pixel lines, which is why the pixel-art era settled on it. With smooth, anti-aliased 3D rendering you are free to use 30° or any angle your camera likes. Both work with the same picker.
- **Use the inverse, not a hand-tuned patch.** The DevilutionX approach is correct for 64×32, but it hides the model. If your artists might change the tile size, or you might add zoom, the inverse matrix handles it by construction.
- **Pick on the ground, then fix up for height.** The inverse finds the ground tile under the cursor. A tall wall or a character standing on tile `(3, 2)` is drawn higher on screen and overlaps tiles behind it. Players expect to click the thing they see, so real games test sprites first (front to back) and fall back to the ground pick. Decide this rule early. It shapes how you sort and store objects.
- **Floor, do not truncate.** `int(−0.156)` is 0 in most languages, while `floor(−0.156)` is −1. Truncating gives the wrong tile for every click left of or above the origin. Row (30, 10) in the table is that bug.

### Check yourself (worked example)

1. A game uses 32×16 tiles. Write `M` and `M⁻¹`. Which tile contains the screen point (20, 20)?
2. In Diablo's 64×32 layout, a monster stands on tile (4, 1). Where is the center of its tile on screen?
3. A game uses the rectangle method with no corner fix-up and 64×32 tiles. Players click uniformly at random. What fraction of clicks select the wrong tile, and does the answer change for 96×48 tiles?

<details>
<summary>Answers</summary>

1. `M = [16 −16; 8 8]`, `det = 256`, `M⁻¹ = [1/32 1/16; −1/32 1/16]`. `i = 20/32 + 20/16 = 1.875`, `j = 20/16 − 20/32 = 0.625`. Tile (1, 0).
2. `M(4.5, 1.5) = (32 · 3, 16 · 6) = (96, 96)`.
3. Half. The diamond drawn in each rectangle has area `w h / 2`, which is `det(M)`, so it fills half of the `w × h` rectangle. The other half is four corner triangles that belong to neighbours. The fraction is `(w h / 2) / (w h) = 1/2` for any tile size, so 96×48 is also wrong half the time.

</details>

## 4. Composing transforms: multiplication, and why order matters

Often you want several transformations in a row. Scale a sprite, then rotate it. Apply the isometric matrix, then a camera zoom. Doing `A` after `B` is itself a linear transformation, and its matrix is the **product** `A B`:

```
(A B) v = A (B v)
```

Read it right to left. `B` acts first, then `A`. That right-to-left reading trips up everyone at first.

To compute `A B`, apply `A` to each column of `B`. Column 1 of `A B` is `A` times column 1 of `B`, and the same for column 2. The column reading explains why. `B` sends `x̂` to its first column, then `A` moves that point, so the product's first column is `A` applied to `B`'s first column.

```python
def mat_mul(A, B):
    (a, b), (c, d) = A
    (e, f), (g, h) = B
    return ((a*e + b*g, a*f + b*h),
            (c*e + d*g, c*f + d*h))

rot90   = ((0, -1), (1, 0))
stretch = ((2, 0), (0, 1))
print(mat_mul(rot90, stretch))   # ((0, -1), (2, 0))
print(mat_mul(stretch, rot90))   # ((0, -2), (1, 0))
```

The two products differ. Follow `x̂ = (1, 0)` through each:

| Order | Step 1 | Step 2 | x̂ ends at |
|---|---|---|---|
| `rot90 · stretch` (stretch first) | stretch: (2, 0) | rotate: (0, 2) | (0, 2) |
| `stretch · rot90` (rotate first) | rotate: (0, 1) | stretch: (0, 1) | (0, 1) |

Stretch-then-rotate gives a sprite that is long in the direction it now faces. Rotate-then-stretch stretches along the *screen's* x-axis, whatever the sprite faces. If a rotated health bar gets longer instead of wider, you composed in the wrong order.

Matrix multiplication is **associative**, `(A B) C = A (B C)`, so you may combine a long chain in any grouping. It is **not commutative**. `A B` and `B A` are usually different. The exceptions are special: two rotations about the same point commute, and two scales along the same axes commute. A rotation and a non-uniform scale almost never do.

This is the reason engines fix an order for the parts of a transform. Epic's API reference for `FTransform` states that positions are transformed in the order scale, then rotate, then translate. Next week you will stack these per-node matrices up a whole scene tree, and the order question becomes the central one.

## 5. The determinant: area, mirrors and undo

The determinant `det(M) = a d − b c` looked like a formula for the inverse. It has a picture of its own.

**It is the area scale factor.** A linear transform sends the unit square (area 1) to the parallelogram spanned by its two columns. That parallelogram's area is `|det(M)|`. So every shape's area is multiplied by `|det(M)|`. For the Diablo matrix, `det = 32 · 16 − (−32) · 16 = 1024`. The unit tile square becomes a diamond of 1,024 pixels. Check it with the diamond formula, half the width times the height: `64 · 32 / 2 = 1024`.

You met the same number last week. In 3D the cross product's length is the area of the parallelogram of two vectors. In 2D, `det` is the z-component of the cross product of the two columns, `(a, c, 0) × (b, d, 0) = (0, 0, ad − bc)`.

**Its sign says whether the transform mirrors.** A positive determinant keeps orientation: turning from `x̂` to `ŷ` is still counter-clockwise after the transform. A negative determinant flips it. `[−1 0; 0 1]` has determinant −1. So does any matrix that mirrors, however it is rotated or scaled. Rotations always have determinant +1.

This is exactly the week 1 inside-out statue. A mirroring transform reverses the winding order of every triangle. The glTF 2.0 specification writes the rule in these terms: if the determinant of a node's world transform is negative, front faces use clockwise winding instead of counter-clockwise. A renderer that ignores the sign draws mirrored meshes inside out.

**Zero means you cannot undo it.** If `det(M) = 0`, the columns are parallel and the whole plane is squashed onto a line (or a point). Many points land on the same spot, so no inverse can say where each came from. The inverse formula divides by `det(M)`, and the division fails. Code that inverts matrices must check for this, with a tolerance, because floating point rarely gives exactly 0.

| Matrix | det | Area × | Mirrors? | Invertible? |
|---|---|---|---|---|
| Identity | 1 | 1 | no | yes |
| Diablo tile `[32 −32; 16 16]` | 1024 | 1024 | no | yes |
| Rotate 30° | 1 | 1 | no | yes |
| Mirror in x `[−1 0; 0 1]` | −1 | 1 | yes | yes |
| Shear `[1 0.5; 0 1]` | 1 | 1 | no | yes |
| Collapse `[2 4; 1 2]` | 0 | 0 | — | no |

The shear row says something useful. Shearing tilts shapes, but it keeps their area exactly. Next week you will see a shear appear in a scene tree where nobody asked for one, with its area untouched and its angles wrong.

```python
def det(M):
    (a, b), (c, d) = M
    return a*d - b*c

def inverse(M, eps=1e-12):
    (a, b), (c, d) = M
    k = det(M)
    if abs(k) < eps:
        return None
    return ((d/k, -b/k), (-c/k, a/k))

tile = ((32, -32), (16, 16))
print(det(tile))                        # 1024
print(inverse(tile))                    # ((0.015625, 0.03125), (-0.015625, 0.03125))
print(inverse(((2, 4), (1, 2))))        # None
```

`0.015625 = 1/64` and `0.03125 = 1/32`, the inverse from section 3.

## 6. Up to 3D: three columns

Everything above carries to 3D with a third column. A 3×3 matrix's columns are where `x̂`, `ŷ` and `ẑ` land:

```
M = | Xx  Yx  Zx |      M v = vx · X + vy · Y + vz · Z
    | Xy  Yy  Zy |
    | Xz  Yz  Zz |
```

Godot's `Basis` type is exactly this, and its reference says each of its axes `x`, `y` and `z` is a column of the matrix. The frame you built with two cross products at the end of week 1 (right, up, forward) drops straight into a matrix. Put `right` in the first column, `up` in the second and the backward direction in the third (Godot's forward is −Z). That matrix rotates anything from the character's local frame into the world.

The 3D determinant is the **volume** scale factor, and it equals `X · (Y × Z)`, a dot product of one column with the cross product of the other two. Its sign again says whether the transform mirrors.

One special case matters a lot. When the three columns are unit length and mutually perpendicular, the matrix is a pure rotation (possibly with a mirror). Such a matrix is called **orthonormal**, and its inverse is its **transpose**, the same table flipped over its diagonal. No division, no determinant. Engines use this constantly, and so will you next week when you convert world positions back into a character's local frame.

## In-class activity (25 minutes)

In pairs, with the interactive and paper.

1. Your artist delivers an "isometric" tile set with tiles 96 pixels wide and 48 tall. Write `M` and `M⁻¹`. Pick three points on screen, one inside a tile, one near an edge, one left of the origin, and find each tile by hand. Check with the interactive's custom tile size.
2. The camera must support a 2× zoom. Write the zoom matrix `Z` and the combined tile-to-screen matrix. Does the order `Z M` or `M Z` matter here? Explain using section 4.
3. The art director wants to try true 30° isometric with the same tile width. Compute the new `h`, the new determinant, and the new tile area in pixels.
4. Write the determinant of each of your matrices and say, before computing anything, which one would draw sprites mirrored if applied to them.

Expected output: three matrices with inverses, three picked tiles, and a two-sentence answer to question 2.

## Common misconceptions

- **"A matrix is a grid of unrelated numbers."** Each column is a vector, where one axis lands. Read the columns and you can sketch the transform without computing anything.
- **"`A B` means do `A` first."** With column vectors, `A B v` applies `B` first. Engines and libraries document their convention (Unreal's `FTransform` multiplication, for example, reads the other way round). Check before you compose.
- **"Picking a tile is division by the tile size."** That works only for rectangular tiles aligned with the screen. For diamonds it is the inverse matrix. Rectangle division without a corner fix-up is wrong for half of all clicks.
- **"A negative determinant is a bug."** It means a mirror, which is often intentional (flipping a sprite to face left). The bug is forgetting that a mirror also flips winding order.

## Check yourself

1. Without multiplying, describe what `[0 1; 1 0]` does to the unit square. What is its determinant, and what does the sign tell you?
2. Compute `[1 2; 0 1] · [3; 4]`, first by rows, then as a sum of scaled columns.
3. `A` rotates by 90° and `B` scales by 3 in both directions. Do `A B` and `B A` differ? Explain from the pictures, then confirm by multiplying.
4. A tile matrix has determinant 0. What does the map look like on screen, and what does the mouse picker return?
5. A sprite is transformed by `[−2 0; 0 2]`. By what factor does its area change, and will a renderer that culls back faces still draw it with the default winding rule?

<details>
<summary>Answers</summary>

1. `x̂` lands at (0, 1) and `ŷ` lands at (1, 0). It swaps the axes, which mirrors the square across the line y = x. `det = 0 · 0 − 1 · 1 = −1`. The negative sign says it is a mirror.
2. By rows: `(1·3 + 2·4, 0·3 + 1·4) = (11, 4)`. By columns: `3 · (1, 0) + 4 · (2, 1) = (3 + 8, 0 + 4) = (11, 4)`.
3. They are equal. A uniform scale looks the same in every direction, so rotating before or after makes no difference. `A = [0 −1; 1 0]`, `B = [3 0; 0 3]`, and both products are `[0 −3; 3 0]`.
4. The two tile axes are parallel, so every tile is drawn on a single line and has zero area. There is no inverse, so the picker cannot recover a tile. A correct picker returns "none" rather than dividing by zero.
5. `det = −4`, so area is multiplied by 4 and the sprite is mirrored. Its winding flips, so with a single-sided quad and back-face culling it disappears. 2D engines usually draw sprites double-sided or handle the flip for you. In 3D you have to handle it yourself.

</details>

## Lab / assignment hook

[Lab 02, the isometric picker](../labs/lab02.md). Implement 2×2 matrix operations (multiply, determinant, inverse), build the tile-to-screen and screen-to-tile functions for any tile size, and measure how often rectangle picking is wrong over a full screen of clicks. Then add zoom and a mirrored map and check the picker still works. Deliverable: the completed Python file passing the tests, and a short report with your error-rate measurements.

## Sources

- DevilutionX (community source port of Diablo, 1996, from a reconstruction of the original code), release 1.5.5, `Source/levels/dun_tile.hpp` (`TILE_WIDTH 64`, `TILE_HEIGHT 32`) and `Source/cursor.cpp` (`ConvertToTileGrid` divides by tile width and height; `ShiftToDiamondGridAlignment` corrects with the lines `py < px/2` and `py >= TILE_HEIGHT − px/2`). https://github.com/diasurgical/devilutionX, accessed September 2026.
- Tiled Map Editor, release 1.12.2, `src/libtiled/isometricrenderer.cpp` (`tileToScreenCoords` and `screenToTileCoords`). https://github.com/mapeditor/tiled, accessed September 2026.
- Wikipedia, "Isometric video game graphics" (accessed September 2026). Game "isometric" art usually uses a 2:1 pixel pattern at about 26.565°, a form of dimetric projection, because 30° lines do not form a clean pixel pattern. The article carries original-research tags, so this lecture checks the 64×32 figure against DevilutionX's source instead of relying on it.
- Godot Engine documentation, class references `Transform2D` and `Basis` (4.7, accessed September 2026). `x` and `y` (and `z` for `Basis`) are the matrix columns; in 2D `y` points down on the identity transform; rotating one axis on its own produces skew or shear.
- Unreal Engine 5.3.2 source, `Core/Public/Math/TransformNonVectorized.h`. Read from a public third-party mirror of the source on GitHub, since Epic's repository requires an account; accessed September 2026. Positions are transformed in the order scale, rotate, translate; `A * B` applies `A` first. The same two rules appear in Epic's API reference, "FTransform" (Unreal Engine 4.27 documentation, Internet Archive copy of 19 July 2024).
- Khronos, glTF 2.0 Specification. The sign of the node's global transform determinant decides whether front faces are counterclockwise or clockwise.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development*, 2nd ed. CRC Press.
- The 96×48 tile set, the zoom factor and the collapse matrix are invented for teaching.

## Interactive spec: examples/w02-isometric-basis.html

**The one insight:** the tile-to-screen map is a matrix whose two columns are the screen steps for one tile along each axis. Picking a tile is the inverse matrix, and rectangle picking without a corner fix-up is visibly wrong in every rectangle corner, half the screen. Dragging a column arrow reshapes the whole grid, and the determinant readout shows area, mirroring and "no inverse" as the arrows move.

**Layout.** Two linked views side by side at 1280 px, stacked at 390 px (screen view on top, since that is where the mouse interaction happens).

- **Left, "Tile space":** a square grid of tiles `i, j ∈ [−2, 8]`, one unit per cell, `i` to the right and `j` downward, with arrows `î = (1, 0)` and `ĵ = (0, 1)` from the origin. Label cell (0, 0).
- **Right, "Screen space":** the same tiles drawn as parallelograms using `M`, y pointing down, origin placed at a fixed pixel so that tiles 0 to 7 in both axes fit. Draw the two columns of `M` as draggable arrows from the origin: `col0 = (w/2, h/2)` and `col1 = (−w/2, h/2)` at defaults. Tile outlines use the accent colour when `det(M) > 0` and the back-face hatch colour when `det(M) < 0`.
- **Readouts (copyable text):** `M` as a 2×2 table, `det(M)`, `M⁻¹` as a 2×2 table (or "no inverse" when `|det| < 1e-9`), the cursor's `(x, y)` relative to the origin, unrounded `(i, j)` to 3 decimals, the correct tile `(floor(i), floor(j))`, and when rectangle mode is on, the rectangle tile plus "agree" or "disagree".

**Controls (keyboard accessible, labelled):**

1. Tile width `w`: slider 16 to 128, step 2, default 64.
2. Tile height `h`: slider 8 to 96, step 2, default 32. A "true isometric" button sets `h = w / √3` (rounded to 2 decimals).
3. Drag handles on the tips of `col0` and `col1` (arrow keys move the focused handle by 1 pixel, shift+arrow by 8). Dragging overrides `w` and `h`; a "reset to tile size" button restores `M` from the sliders.
4. "Rectangle picking" toggle (only meaningful while the columns are the slider defaults `(w/2, h/2)` and `(−w/2, h/2)`; disable it with a note after the handles are dragged): `k = floor((x + w/2)/w)`, `m = floor(y/h)`, rectangle tile `(k + m, m − k)`. Draw the rectangle `x ∈ [k·w − w/2, k·w + w/2)`, `y ∈ [m·h, m·h + h)` as a dashed outline and highlight its tile, alongside the correct diamond highlight.
5. "Error map" toggle: shades every pixel of the screen view where rectangle and correct picks disagree, and shows the disagreeing fraction as a percentage (expected 50.0% for any tile size). Measure the fraction over the whole rectangles that intersect the view, not over the clipped view, because a view edge that cuts rectangles off can hold more corner than middle and read slightly off 50%.
6. Keyboard picking: when the screen view has focus, the arrow keys move a crosshair 1 pixel per press (shift for 8) so keyboard users can pick tiles.

**Formulas.** `(x, y) = (col0.x · i + col1.x · j, col0.y · i + col1.y · j)`. `det = col0.x · col1.y − col1.x · col0.y`. `M⁻¹ = (1/det) · [col1.y  −col1.x; −col0.y  col0.x]`. Pick: `(i, j) = M⁻¹ (x, y)`, tile `(floor(i), floor(j))`. Highlight the picked tile in both views.

**Test values (defaults w = 64, h = 32).** `det = 1024`. `M⁻¹ = [0.015625 0.03125; −0.015625 0.03125]`. Tile (3, 2) top corner at (32, 80); tile (2, 5) at (−96, 112). Picks (correct, then rectangle): (0, 8) → (0, 0), (0, 0); (0, 31) → (0, 0), (0, 0); (0, 33) → (1, 1), (1, 1); (40, 30) → (1, 0) with unrounded (1.563, 0.313), rectangle (1, −1); (30, 10) → (0, −1), rectangle (0, 0); (−20, 50) → (1, 1), (1, 1); (100, 120) → (5, 2), rectangle (5, 1). True-isometric button with w = 64 sets h = 36.95.

**First screen.** Defaults, rectangle picking on, crosshair placed at (40, 30) so the two highlights already disagree and the readout says "disagree". Caption: "Diablo's 64×32 tiles. The dashed box is where the obvious code thinks you clicked."

**Accessibility and motion.** No animation required. Colours from the shared palette; the correct and rectangle highlights must differ in outline style (solid vs dashed), not only colour.
