# MA201 · Week 04 — Homogeneous Coordinates and Projection

**Why this matters:** Every frame, your engine turns a 3D world into a flat grid of pixels with two tricks. It adds a fourth coordinate so that moving things becomes a matrix multiply, and it divides by distance so that far things look small. When a player says "your FOV slider is wrong" or a wall flickers through another wall at 300 metres, one of those two tricks is the cause.

**You will be able to:**
- Build 4×4 matrices that translate, rotate and scale, and apply them to points (`w = 1`) and directions (`w = 0`) with the correct result for each.
- Compute where a 3D point lands on screen, in normalized device coordinates and in pixels, from a field of view, an aspect ratio and the perspective divide.
- Convert a field-of-view setting between vertical, horizontal and "horizontal at 4:3" conventions for any aspect ratio.
- Predict how depth precision is spread between the near and far planes, and choose near and far values that avoid z-fighting.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed., 2011), chapter 6, sections 6.4 (4×4 homogeneous matrices) and 6.5 (4×4 matrices and perspective projection). Skim chapter 10, section 10.2 on camera space and clip space. Re-read your MA201 week 2 notes on matrix multiplication.

**Prerequisites from earlier courses:** [MA101 week 10, angles, sin and cos](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) (radians and the unit circle, which gives you `tan`). [MA101 week 12, 2D vectors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w12-2d-vectors.md) (points versus displacements). [CS102 week 7, scene graphs](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w07-trees-scene-graphs-and-skill-trees.md) (local and world positions). [MA201 week 2, matrices and linear transformations](w02-matrices-and-linear-transformations.md). [MA201 week 3, transform hierarchies](w03-transform-hierarchies-local-and-world-space.md).

**Interactive:** [examples/w04-fov-frustum.html](../examples/w04-fov-frustum.html). Keep it open during section 3.

---

## 1. The one thing a 3×3 matrix cannot do

In week 2 you saw that a 3×3 matrix can rotate, scale and shear. Each of those is a **linear transformation**, a function `T` with `T(a + b) = T(a) + T(b)` and `T(k·a) = k·T(a)`. One consequence is easy to miss. Put the zero vector in and you always get the zero vector out, because `M · 0 = 0` for every matrix `M`.

That rules out the most common operation in a game. Moving an object 5 metres to the right sends the origin to `(5, 0, 0)`. No 3×3 matrix can do that. So a character's transform would have to be stored as "a matrix, plus a separate offset vector", and every operation on transforms would carry two parts around. Composing ten transforms in a scene graph would mean ten matrix products and a careful sum of rotated offsets.

The fix, used by every engine and graphics API you will meet, is to add one coordinate.

### Points and directions get a fourth number

Write every 3D quantity with four components, `(x, y, z, w)`:

- A **point** (a position, like a character's feet) has `w = 1`.
- A **direction** (a displacement, velocity, or surface normal) has `w = 0`.

This is **homogeneous coordinates**. The name comes from projective geometry, and you will see its full meaning in section 3. For now, `w` is a flag that says "does moving the object affect this?".

Now a 4×4 matrix can translate. With column vectors (the convention of this course, OpenGL, Godot and glTF), a translation by `t = (tx, ty, tz)` is

```
      | 1  0  0  tx |
T  =  | 0  1  0  ty |
      | 0  0  1  tz |
      | 0  0  0  1  |
```

Multiply it by a point `(x, y, z, 1)`. The top row gives `1·x + 0 + 0 + tx·1 = x + tx`. The fourth column is multiplied by `w`, and `w = 1`, so the offset is added. Multiply it by a direction `(x, y, z, 0)` and the fourth column is multiplied by zero. The direction comes out unchanged.

That is the behaviour you want. Moving a character does not change which way it is facing, and it does not change its velocity. A sword that is 1 metre long is still 1 metre long after the character walks across the map. The `w` flag makes the matrix do the right thing to each kind of quantity without an `if`.

It also explains a rule you met in MA101 week 12. Subtracting two points gives a direction: `(p, 1) − (q, 1) = (p − q, 0)`. Adding a direction to a point gives a point: `(p, 1) + (d, 0) = (p + d, 1)`. Adding two points gives `w = 2`, which is neither. That is the algebra telling you "the sum of two positions means nothing". The midpoint `½(p + q)` is fine, because it has `w = 1` again.

### The general affine matrix

Any combination of rotation, scale and translation fits in one 4×4 matrix of this shape:

```
      | a  b  c  tx |
M  =  | d  e  f  ty |      the 3×3 block A = [a b c; d e f; g h i] rotates and scales,
      | g  h  i  tz |      the column t moves,
      | 0  0  0  1  |      and the bottom row stays 0 0 0 1.
```

This is an **affine transformation**, a linear transformation followed by a translation. The matrices you compose in a scene graph (week 3) are all of this form. Because the bottom row is `0 0 0 1`, multiplying two of them gives another one of the same form. The whole chain from a finger bone to the world is one 4×4 matrix.

Order still matters, as it did in week 2. With column vectors the matrix nearest the vector acts first. `T · R · p` rotates `p` about the origin and then moves it. `R · T · p` moves it first and then swings it around the origin, which is usually a bug.

Here it is in code. The helpers in this lecture are plain Python lists so you can see every number. Engines use the same arithmetic.

```python
import math

def mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

def apply(M, v):
    return [sum(M[i][k] * v[k] for k in range(4)) for i in range(4)]

def translate(tx, ty, tz):
    return [[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]]

def rot_y(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]]

def show(v):
    return "(" + ", ".join(f"{x:.2f}" for x in v) + ")"

feet = [1, 0, 0, 1]      # a point
facing = [1, 0, 0, 0]    # a direction
M = mat_mul(translate(5, 0, 0), rot_y(90))   # rotate first, then move
print("point    ", show(apply(M, feet)))
print("direction", show(apply(M, facing)))
print("wrong order", show(apply(mat_mul(rot_y(90), translate(5, 0, 0)), feet)))
```

Output:

```
point     (5.00, 0.00, -1.00, 1.00)
direction (0.00, 0.00, -1.00, 0.00)
wrong order (0.00, 0.00, -6.00, 1.00)
```

The point `(1, 0, 0)` turned 90° about the y axis to `(0, 0, −1)` and then moved 5 along x. The direction turned but did not move. In the wrong order the point was moved to `(6, 0, 0)` first and then swung around the origin to `(0, 0, −6)`.

### Normals are the exception

Directions with `w = 0` are right for velocities and facing vectors. Surface normals need one more rule. If `M` scales non-uniformly (say, stretches x by 2), multiplying a normal by `M` tilts it off the surface. Normals must be transformed by the inverse transpose of the 3×3 block, `(A⁻¹)ᵀ`. For pure rotations `(A⁻¹)ᵀ = A`, which is why the bug only shows up on stretched meshes. You will not need this in the lab, but when lighting looks wrong only on a scaled object, this is the first thing to check.

## 2. From the world to the camera

Before anything can be projected, it has to be described from the camera's point of view. **View space** (also called camera space or eye space) is the frame where the camera sits at the origin. In the convention used by OpenGL, Godot and glTF, the camera looks down the negative z axis, x points right and y points up.

The camera is an object in the world like any other, with a world transform `C` (its position and rotation). The **view matrix** is its inverse, `V = C⁻¹`. If the camera stands at `(0, 2, 10)` and a tree is at `(0, 2, 0)`, then in view space the tree is at `(0, 0, −10)`, straight ahead and 10 metres away.

For a transform made only of rotation `R` and translation `t` (a **rigid transform**), the inverse is cheap, because the inverse of a rotation is its transpose:

```
C  = [ R   t ]        C⁻¹ = [ Rᵀ   −Rᵀ·t ]
     [ 0   1 ]              [ 0      1   ]
```

You do not have to invert a general 4×4 matrix every frame. Transpose the 3×3 block and rotate the negated position.

After this step every visible point has a negative z. Call `d = −z` the **depth** of the point, its distance in front of the camera measured along the view direction. Depth is what the rest of the lecture divides by.

## 3. Worked example: one FOV number, three different views

### The hook

Open the video settings of Half-Life 2 and a game made in Godot 4, and set both to a field of view of 75. Play both on the same 16:9 monitor. The Godot game shows a much wider slice of the world, about 108° from the left edge of the screen to the right. Half-Life 2 shows about 91°. Minecraft's default of 70 looks wider than Half-Life 2's 75.

Players notice this, and it is the source of endless forum threads asking "what FOV should I use?". The answer depends on which angle each game measures. The model below turns every convention into the same number.

### The model

A perspective camera is a **pinhole**. A point at view-space position `(x, y, −d)` projects onto a screen plane in front of the camera by similar triangles. Its height on screen is proportional to `y / d`. Twice as far away, half as tall. That division by depth is all that perspective is.

The **field of view** (FOV) sets how much of the world fits on screen. Let `θ_v` be the **vertical FOV**, the angle from the bottom edge of the view to the top edge. Then the top of the screen sits at slope `tan(θ_v / 2)`, and a point is on the top edge when `y / d = tan(θ_v / 2)`. Define the **focal factor**

```
f = 1 / tan(θ_v / 2)
```

and the screen is `a = width / height` times wider than it is tall (the **aspect ratio**). Then the projected position in **normalized device coordinates** (NDC), where both axes run from −1 at one edge of the screen to +1 at the other, is

```
x_ndc = (f / a) · x / d
y_ndc =  f      · y / d
```

The **horizontal FOV** `θ_h` follows from the same triangles. The right edge is at `x / d = a · tan(θ_v / 2)`, so

```
θ_h = 2 · atan( a · tan(θ_v / 2) )
```

That formula is the whole worked example. Three conventions are in common use, and each fixes a different thing:

- **Vertical FOV** (Unity's `Camera.fieldOfView`, Godot's default `KEEP_HEIGHT` mode, Minecraft, the glTF `yfov` property). The number you type is `θ_v`. Wider screens show more at the sides. This is called **Hor+** scaling.
- **Horizontal FOV** (Godot's `KEEP_WIDTH` mode). The number is `θ_h`. A wider screen shows less at the top and bottom.
- **Horizontal FOV at 4:3** (the Source engine). The number is the horizontal angle a 4:3 screen would show. Convert it to `θ_v` with `a = 4/3` once, and after that it behaves like a vertical FOV. The Source setting of 75 corresponds to a vertical FOV of 59.84°.

### Numbers you can check

Apply the formula to four settings on four screen shapes. Every entry is the horizontal angle, in degrees, from edge to edge.

| Setting | Convention | Vertical angle | 4:3 | 16:10 | 16:9 | 21:9 |
|---|---|---|---|---|---|---|
| Godot default, 75 | vertical | 75.00 | 91.31 | 101.67 | 107.51 | 121.63 |
| Minecraft default, 70 | vertical | 70.00 | 86.07 | 96.50 | 102.45 | 117.06 |
| Half-Life 2 default, 75 | horizontal at 4:3 | 59.84 | 75.00 | 85.28 | 91.31 | 106.65 |
| Source, 90 | horizontal at 4:3 | 73.74 | 90.00 | 100.39 | 106.26 | 120.51 |

Check one by hand. Godot at 16:9: `tan(37.5°) = 0.7673`, times `16/9 = 1.7778` gives `1.3641`, `atan(1.3641) = 53.75°`, doubled is `107.51°`. Godot's own class reference lists the same four values for its default.

Two cells match exactly. Half-Life 2's 75 on a 16:9 monitor is 91.31°, the same as Godot's 75 on a 4:3 monitor. That is not a coincidence. Source's rule is "a vertical FOV chosen so that a 4:3 screen shows the number you typed". Both rows have the same geometry, labelled differently.

The focal factor also tells you how big things look. A 1.8 m character standing 20 m away covers `1.8 / 20 = 0.09` of depth. In NDC that is `0.09 · f` tall, and on a 1080-pixel-high screen, where NDC height 2 spans 1,080 pixels, it is `0.09 · f · 540` pixels.

| Vertical FOV | f | Character height at 20 m on a 1080p screen |
|---|---|---|
| 75° (Godot default) | 1.3032 | 63.3 px |
| 70° (Minecraft default) | 1.4281 | 69.4 px |
| 59.84° (Source 75) | 1.7376 | 84.4 px |

A wider FOV makes every enemy smaller. A player who raises FOV to see more at the edges also gives up about a quarter of the pixel height of targets at the center. That trade is the real content of the "what FOV should I use" threads.

Here is the projection as code, with the 16:9 Godot default camera and a point 2 m right, 1 m up and 10 m ahead:

```python
import math

def ndc(x, y, d, vfov_deg, aspect):
    f = 1 / math.tan(math.radians(vfov_deg) / 2)
    return (f / aspect) * x / d, f * y / d

def to_pixels(xn, yn, width, height):
    return (xn + 1) / 2 * width, (1 - yn) / 2 * height   # pixel y grows downward

def hfov(vfov_deg, aspect):
    return math.degrees(2 * math.atan(aspect * math.tan(math.radians(vfov_deg) / 2)))

xn, yn = ndc(2, 1, 10, 75, 16 / 9)
px, py = to_pixels(xn, yn, 1920, 1080)
print(f"NDC ({xn:.4f}, {yn:.4f})  pixel ({px:.1f}, {py:.1f})")
print(f"Godot 75 at 16:9 -> {hfov(75, 16/9):.2f} deg across")
src_v = math.degrees(2 * math.atan(math.tan(math.radians(75) / 2) / (4 / 3)))
print(f"Source 75 -> vertical {src_v:.2f}, 16:9 across {hfov(src_v, 16/9):.2f}")
```

Output:

```
NDC (0.1466, 0.1303)  pixel (1100.7, 469.6)
Godot 75 at 16:9 -> 107.51 deg across
Source 75 -> vertical 59.84, 16:9 across 91.31
```

### The visual

Open [`examples/w04-fov-frustum.html`](../examples/w04-fov-frustum.html). The left panel is a top-down view of the camera's **frustum**, the wedge of space it can see, over a field of pillars. The right panel is what the camera draws. Pick a convention, type a number, and drag the aspect ratio from 4:3 to 21:9.

Watch what the same number does under each convention. With "vertical", widening the screen opens the wedge in the top view, and pillars appear at the edges of the right panel while the center pillar keeps its height in pixels. With "horizontal", the wedge stays fixed and the center pillar grows as the screen gets wider, because the vertical FOV is shrinking. The panel readout shows `θ_v`, `θ_h`, `f` and the center pillar's pixel height, so you can copy them into the table above.

### Cross-game recognition

**Source engine games (Half-Life 2 era onward).** Valve's documentation gives the conversion as `2 · atan(tan(fov / 2) · aspect / (4/3))`, the formula above with the 4:3 step folded in. The page gives Half-Life 2's default as 75 and says a 16:9 monitor shows about 91°. The page describes that 75 as a vertical FOV, yet its own formula treats it as a horizontal angle on a 4:3 frame. Trust the formula and the numbers, and state the convention explicitly in your own docs.

**Minecraft (Java Edition, current).** The Minecraft Wiki's options page says the FOV value is vertical, defaults to 70 ("Normal") and ranges from 30 to 110 ("Quake Pro"). Rewritten in the model's form it is a plain `θ_v`, so a 21:9 player at the default sees 117° across.

**Unity (Unity 6 scripting reference).** `Camera.fieldOfView` is documented as the vertical field of view in degrees, and the horizontal angle depends on the aspect ratio. Same form as Minecraft.

**glTF 2.0 (Khronos specification).** A glTF camera stores `yfov`, the vertical FOV in radians, and an optional `aspectRatio`. An artist's camera exported from Blender and loaded into any engine therefore arrives as `θ_v`. If your engine's camera is horizontal, you convert at import.

Four products, three labels, one formula. When you meet a new game's FOV setting, ask: *is the number `θ_v`, `θ_h`, or `θ_h` at some reference aspect?* Then convert everything to `θ_v` before you compare.

### Eyes-open design judgment

- **Choose vertical FOV (Hor+) for landscape games.** Godot's documentation recommends `KEEP_HEIGHT` for landscape projects so wider screens get a wider view. Ultrawide players see more at the sides and no one loses height. For a portrait phone game the argument flips, and fixing the horizontal angle keeps the play area readable.
- **Label the slider with its convention.** Show "vertical 70° (103° horizontal on your screen)". Players compare numbers between games. If you do not tell them which angle you mean, the comparison is wrong by up to 20°.
- **Wider is not free.** A wider FOV shrinks targets (the pixel table above), stretches the edges of the image, and costs performance because more objects are inside the frustum. Competitive players often choose it anyway. Clamp the range so the game still reads at both ends.
- **Hor+ can be an advantage in multiplayer.** A 21:9 player with vertical 70° sees 117° across while a 16:9 player sees 102°. Some competitive games cap the horizontal angle for fairness. Decide whether peripheral vision is a skill you want monitors to buy.

## 4. The perspective matrix and the divide

Section 3 did the projection by hand, with an explicit division by `d`. A GPU only multiplies 4×4 matrices by 4-vectors. So how does a matrix divide?

It doesn't. It puts the divisor into `w` and lets the hardware divide afterwards. The standard OpenGL-style perspective matrix, for near plane `n` and far plane `F` (distances in front of the camera), is

```
      | f/a   0        0                  0            |
P  =  |  0    f        0                  0            |
      |  0    0   (F + n)/(n − F)    2·F·n/(n − F)      |
      |  0    0       −1                  0            |
```

Multiply it by a view-space point `(x, y, −d, 1)`. The bottom row gives `w_clip = −(−d) = d`. The depth has been copied into `w`. The result, `(x_clip, y_clip, z_clip, w_clip)`, is in **clip space**. The GPU then performs the **perspective divide**, dividing every component by `w_clip`:

```
x_ndc = x_clip / w_clip = (f/a)·x / d
y_ndc = y_clip / w_clip =  f·y / d
z_ndc = z_clip / w_clip
```

The first two lines are exactly section 3's formulas. This is the second meaning of homogeneous coordinates. A 4-vector `(X, Y, Z, W)` with `W ≠ 0` stands for the 3D point `(X/W, Y/W, Z/W)`, so `(2, 4, 6, 2)` and `(1, 2, 3, 1)` are the same point. Directions with `W = 0` are "points at infinity", which is why a direction is unaffected by translation. In the affine matrices of section 1, `w` stayed 1 and the divide did nothing. The perspective matrix is the first one whose bottom row is not `0 0 0 1`, and it is the only one in the pipeline that needs the divide.

Clip space is also where the GPU throws away what you cannot see. A point is inside the frustum when `−w ≤ x, y, z ≤ w`. Testing before the divide avoids dividing by zero for points exactly at the camera.

```python
import math

def perspective(vfov_deg, aspect, near, far):
    f = 1 / math.tan(math.radians(vfov_deg) / 2)
    return [[f / aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (near - far), 2 * far * near / (near - far)],
            [0, 0, -1, 0]]

def apply(M, v):
    return [sum(M[i][k] * v[k] for k in range(4)) for i in range(4)]

P = perspective(75, 16 / 9, 0.05, 4000)
clip = apply(P, [2, 1, -10, 1])
ndc = [c / clip[3] for c in clip[:3]]
print("clip", [round(c, 4) for c in clip])
print("ndc ", [round(c, 4) for c in ndc])
```

Output:

```
clip [1.4661, 1.3032, 9.9002, 10]
ndc  [0.1466, 0.1303, 0.99]
```

The first two NDC values match the hand projection. The third is the depth value the GPU writes to the **depth buffer** (also called the z-buffer), which decides which surface is in front at each pixel.

### Where the depth precision goes

Look at `z_ndc` for that point, 10 metres away with a far plane at 4,000 metres. It is already 0.99. Almost the whole depth range has been used up in the first 10 metres. Write `z_ndc` as a function of depth:

```
z_ndc(d) = (F + n)/(F − n) − 2·F·n / ((F − n)·d)
```

It is a constant minus something proportional to `1/d`. You met this shape in MA101 week 6, a rational function with a horizontal asymptote. With the Godot defaults `n = 0.05` and `F = 4000`:

| Depth d (m) | z_ndc | Share of the [−1, 1] range used by depths up to d |
|---|---|---|
| 0.05 (near) | −1.0000 | 0% |
| 0.1 | 0.0000 | 50% |
| 1 | 0.9000 | 95% |
| 10 | 0.9900 | 99.5% |
| 100 | 0.9990 | 99.95% |
| 4,000 (far) | 1.0000 | 100% |

Half of all depth values are spent between 5 and 10 centimetres from the lens. Solving `z_ndc = 0` gives `d = 2Fn / (F + n) ≈ 2n`, so the halfway point is always about twice the near distance. The far plane barely matters.

A depth buffer stores `z_ndc` (remapped to [0, 1]) in a fixed number of bits, typically 24. When two surfaces 300 m away differ by less than one step of that buffer, the GPU cannot tell which is in front, and they flicker through each other. That is **z-fighting**. Godot's documentation for `Camera3D.near` warns that values lower than the default increase it. Doubling `n` roughly doubles the precision at every distance. Doubling `F` changes almost nothing. The rule of thumb follows: **push the near plane out as far as your game allows, and don't worry much about the far plane.**

Many modern engines go further and use **reversed-Z**, mapping the near plane to 1 and the far plane to 0 in a floating-point depth buffer. Floating-point numbers are densest near zero, so this spends the fine steps on distant surfaces, where the `1/d` curve had starved them. You do not need to implement it, but you should recognize the name when an engine setting mentions it.

## 5. Putting the pipeline together

One vertex of one character goes through this chain every frame:

```
clip = P · V · W · p_local
ndc  = clip.xyz / clip.w
pixel = ((x_ndc + 1)/2 · width, (1 − y_ndc)/2 · height)
```

- `W` is the object's world matrix, built from the scene graph of week 3 (affine, bottom row `0 0 0 1`).
- `V` is the inverse of the camera's world matrix (section 2).
- `P` is the perspective matrix (section 4), the only non-affine step.

Engines usually multiply `P · V · W` once per object on the CPU and send the product to the GPU. Every vertex then costs one matrix multiply. The divide and the pixel mapping are done by fixed hardware.

Two practical notes. First, **matrix storage order** is a separate question from the column-vector convention. glTF stores 4×4 matrices in column-major order, so the translation is in elements 12, 13 and 14 of the flat array. If you load a glTF node matrix and the object ends up at the origin with a strange shear, you probably read it row-major. Second, **handedness and the direction the camera looks** vary. Unity's world is left-handed and a camera's forward is +z. Its documentation notes that the view matrix (`worldToCameraMatrix`) still follows the OpenGL convention, with forward along −z. The formulas are the same with some signs flipped. Always check where the translation lives and which way the camera looks before you trust a matrix from another engine.

## In-class activity (25 minutes)

Work in pairs. You are designing the FOV slider for a third-person MMO that must look right on a 16:9 laptop, a 21:9 ultrawide and a 9:16 phone held upright.

1. Choose a convention (vertical, horizontal, or horizontal at a reference aspect). Justify it in two sentences, one of which names the phone case.
2. Pick a default and a range for the slider. For each end of the range and each of the three screens, compute `θ_h` and the pixel height of a 1.8 m character 20 m away on a 1080-pixel-tall screen. Use the interactive to check.
3. Write the label text the slider shows, including the converted angle.
4. Swap with another pair. Find one screen where their range makes targets too small (under 40 px at 20 m) or the view too narrow (under 80° across). Propose a fix.

Expected output: a one-paragraph convention choice, a 2 × 3 table of angles and pixel heights, the label text, and the weakness your partners found.

## Common misconceptions

- **"FOV 90 is FOV 90."** Only if both games measure the same angle. Source's 90 is a vertical angle of 73.74°. A vertical-convention game set to 90 is 16.3° wider in height and 15.0° wider across on 16:9 (121.28° against 106.26°). Convert to `θ_v` before comparing.
- **"Horizontal FOV scales linearly with aspect ratio."** It scales through `atan`. Doubling the aspect ratio does not double the angle, and no aspect ratio reaches 180°.
- **"Translations are linear transformations, so they fit in a 3×3 matrix."** A translation moves the origin, so it is not linear. It is affine, which is why the fourth coordinate exists.
- **"Z-fighting in the distance means the far plane is too far."** The far plane matters very little. The near plane controls precision everywhere. Push `n` out first.

## Check yourself

1. Apply `T = translate(3, 0, −2)` to the point `(1, 1, 1)` and to the direction `(1, 1, 1)`. Write both results with their `w`.
2. A game's FOV setting is vertical 90°. What horizontal angle does a 21:9 player see? What Source-style setting (horizontal at 4:3) gives the same view?
3. A camera has vertical FOV 60° on a 16:9, 1920 × 1080 screen. Where, in pixels, does the view-space point `(−3, 0, −12)` appear?
4. With `n = 0.1` and `F = 1000`, at what depth is `z_ndc = 0`? What happens to that depth if you change `n` to 0.5?
5. The clip-space result of a point is `(4, −2, 7.9, 8)`. Is the point inside the frustum? What are its NDC coordinates?

<details>
<summary>Answers</summary>

1. Point: `(4, 1, −1, 1)`. Direction: `(1, 1, 1, 0)`, unchanged.
2. `θ_h = 2·atan(21/9 · tan 45°) = 2·atan(2.3333) = 133.6°`. For Source, the equivalent 4:3 horizontal angle is `2·atan(4/3 · tan 45°) = 2·atan(1.3333) = 106.3°`, so a Source setting of about 106.
3. `f = 1/tan 30° = 1.7321`. `x_ndc = (1.7321 / 1.7778) · (−3) / 12 = −0.2436`, `y_ndc = 0`. Pixel `x = (1 − 0.2436)/2 · 1920 = 726.2`, `y = 540`.
4. `d = 2Fn / (F + n) = 200 / 1000.1 ≈ 0.19998`, about 0.2 m. With `n = 0.5`, `d = 1000 / 1000.5 ≈ 0.9995`, about 1 m. Half the range now covers five times as much depth near the camera, and every more distant surface gets finer steps.
5. Inside means `−8 ≤ 4, −2, 7.9 ≤ 8`. All three hold, so yes. NDC `(0.5, −0.25, 0.9875)`.

</details>

## Lab / assignment hook

[Lab 04, a software camera](../labs/lab04.md). You write the 4×4 helpers, the perspective matrix and a projector in Python, check them against this lecture's numbers, build a settings-screen FOV table that converts between the three conventions for five aspect ratios, and measure how depth precision changes with the near plane. Deliverable: your `camera.py` passing the tests, the FOV table, and a 300-word recommendation for your game's near and far planes and slider.

## Sources

- Valve Developer Community, "Field of View" (Internet Archive copy of 6 June 2026, re-checked 29 September 2026). Half-Life 2 default FOV 75; widescreen expands the horizontal view; 75 corresponds to about 91° on 16:9; scaled FOV formula `2·atan(tan(fov/2)·aspect/standardRatio)` with standard ratio 4:3; `ScaleFOVByWidthRatio` in `view.cpp`.
- Minecraft Wiki, "Options" (Java Edition, accessed September 2026). FOV default 70 ("Normal"), range 30 to 110 ("Quake Pro"), value measured as vertical vision.
- Unity Technologies, Scripting API, `Camera.fieldOfView` and `Camera.worldToCameraMatrix` (Unity 6 documentation, accessed September 2026). Vertical field of view in degrees, horizontal depending on aspect ratio; camera space follows the OpenGL convention with forward along −z, unlike Unity's +z forward.
- Godot Engine class reference, `Camera3D` (master branch, 4.8-dev, September 2026; the properties are unchanged across 4.x). `fov` default 75, applies to the axis not locked by `keep_aspect`; the listed horizontal equivalents 91.31°, 101.67°, 107.51° and 121.63°; `keep_aspect` default `KEEP_HEIGHT`, described as Hor+ and recommended for landscape; `near` default 0.05 with the z-fighting warning; `far` default 4000.
- Khronos Group, glTF 2.0 Specification (2.0.1, 2021). Camera `yfov` as vertical field of view in radians with optional `aspectRatio`; matrices stored column-major; perspective projection definitions.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development*, 2nd ed. CRC Press. Chapters 6 and 10.

## Interactive spec: examples/w04-fov-frustum.html

**Purpose.** Make it obvious that one FOV number means different views under different conventions, and that "vertical" (Hor+) keeps the center of the image fixed while "horizontal" makes it zoom as the aspect ratio changes.

**Layout.** Two linked panels side by side at 1280 px, stacked (top view above screen view) at 390 px.

- **Left panel, top-down view.** Camera at the bottom center, looking up the page. A field of 21 generic pillars (circles) placed at fixed world positions: one at `(0, −20)` directly ahead (the "target pillar", highlighted), 18 at every combination of x in {−24, −14, −7, 7, 14, 24} and depth in {10, 20, 35}, plus two at depth 60 with x = −10 and x = 10. Draw the horizontal frustum wedge with half-angle `θ_h / 2` from the camera, shaded. Pillars inside the wedge are filled, outside are outlined. Scale: 1 px = 0.1 m at 1280 width; fit to panel.
- **Right panel, screen view.** A rectangle with the chosen aspect ratio (height fixed at the panel height, width = height × a, letterboxed inside the panel if needed). Each pillar is 1.8 m tall and 0.6 m wide, standing on ground at `y = −1.6` relative to a camera eye height of 1.6. Draw each visible pillar as a rectangle from its projected bottom to top, using `x_ndc = (f/a)·x/d`, `y_ndc = f·y/d`, mapped to the rectangle. Draw far pillars first.

**Controls (all keyboard accessible).**
1. Convention radio group: "Vertical (Hor+)", "Horizontal", "Horizontal at 4:3 (Source)". Default Vertical.
2. FOV number slider 30 to 130, step 1, default 75, with a numeric input.
3. Aspect ratio select: 4:3, 16:10, 16:9, 21:9, 9:16. Default 16:9. Also a continuous slider for `a` from 0.5 to 2.6 (step 0.01) that stays in sync.
4. Preset buttons: "Godot default (vertical 75)", "Minecraft default (vertical 70)", "Half-Life 2 default (4:3 horizontal 75)", "Source 90".

**Conversions.** Let `N` be the slider value in radians.
- Vertical: `θ_v = N`.
- Horizontal: `θ_v = 2·atan(tan(N/2) / a)`.
- Horizontal at 4:3: `θ_v = 2·atan(tan(N/2) / (4/3))`.
Then `f = 1/tan(θ_v/2)`, `θ_h = 2·atan(a·tan(θ_v/2))`.

**Readouts (next to the screen view, monospaced, 2 decimals).** `θ_v`, `θ_h`, `f`, target pillar pixel height on a 1080-pixel-tall screen `= 1.8 / 20 · f · 540`, and the count of pillars visible.

**The one insight.** On first load (Vertical, 75, 16:9) the screen shows the target pillar at 63.3 px. Switching the aspect select from 16:9 to 21:9 in Vertical mode widens the wedge and adds pillars at the sides while the target stays 63.3 px. Doing the same in Horizontal mode keeps the wedge fixed and the target pillar grows. Put a small caption under the screen: "Target height: 63.3 px" updating live, so the change is visible without reading the table.

**Test values (must match to 2 decimals).**
- Vertical 75, 16:9: `θ_h` 107.51, `f` 1.30, target 63.34 px.
- Vertical 70, 16:9: `θ_h` 102.45, target 69.41 px.
- Horizontal at 4:3, 75, 16:9: `θ_v` 59.84, `θ_h` 91.31, target 84.45 px.
- Horizontal at 4:3, 90, 16:9: `θ_v` 73.74, `θ_h` 106.26.
- Vertical 75, 21:9: `θ_h` 121.63. Vertical 75, 4:3: `θ_h` 91.31.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, inline. Respect `prefers-reduced-motion` (no animated transitions, only redraws). Wedge and pillar colors must also differ in fill pattern (filled versus outlined) so color is not the only cue. No game art; pillars are plain shapes.
