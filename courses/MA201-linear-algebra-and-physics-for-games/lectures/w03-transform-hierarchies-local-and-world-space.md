# MA201 · Week 03 — Transform Hierarchies: Local and World Space

**Why this matters:** A sword in a hand, a turret on a ship, a hat on a head and a camera on a boom are all positions described relative to something else. The engine turns those relative descriptions into world positions by multiplying matrices up a tree, and turns world positions back into "in front of me, a bit to the left" by inverting them. When a stretched parent makes its rotated child lean like a parallelogram, you need this week's model to know whether that is a bug, a feature, or an engine limitation.

**You will be able to:**
- Compose a node's world transform from the local transforms on its path to the root, using a basis matrix and an origin per node.
- Convert a world position or direction into any node's local space with the inverse transform, and read "ahead, behind, left, right" off the result.
- Compute the shear that a non-uniformly scaled parent puts on a rotated child, and predict how Unity, Unreal and Godot each display it.
- Decide where non-uniform scale is safe in a hierarchy and write a rule for your team.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed., 2011), chapter 3 (multiple coordinate spaces: world, object, upright and the transforms between them). Nystrom, *Game Programming Patterns* (2014), "Dirty Flag", the section on local and world transforms. Godot Engine documentation (4.x), tutorial "Matrices and transforms", from translation to the end.

**Prerequisites from earlier courses:** [CS102 week 7, scene graphs](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w07-trees-scene-graphs-and-skill-trees.md), where you composed world position and angle by recursion (the tank, turret and barrel). This week replaces "position plus angle" with a full matrix, which adds scale and shear. [MA201 week 2](w02-matrices-and-linear-transformations.md) (matrix columns, multiplication order, determinant, inverse). [MA201 week 1](w01-vectors-in-3d-and-the-cross-product.md) (building a frame from forward and up). [MA101 week 13](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md) (the dot product gives the angle between two vectors).

**Interactive:** [examples/w03-parent-scale-shear.html](../examples/w03-parent-scale-shear.html). Keep it open during section 3.

---

## 1. A transform is a matrix plus an offset

Last week's matrices kept the origin fixed. Real objects also move. So an object's placement in its parent's space needs two parts:

- a **basis** `B`, a 2×2 matrix in 2D or 3×3 in 3D, whose columns are where the object's own axes land in the parent's space. It holds rotation, scale and any shear.
- an **origin** `t`, a vector, which is where the object's own origin lands in the parent's space.

Together they are a **transform**, and it moves a point `p` given in the object's own coordinates into the parent's coordinates:

```
p_parent = B p + t
```

This is exactly how engines store transforms. Godot's `Transform2D` holds `x`, `y` and `origin`, and its `Transform3D` holds a `Basis` and an `origin`. Next week you will pack `B` and `t` into one bigger matrix. For now keep them apart, because it makes every step visible.

Engines usually let you edit a transform as three friendlier numbers, position, rotation and scale, often called **TRS**. From those the basis is built as rotation times scale, `B = R S`. With column vectors the matrix nearest the point acts first, so the object is scaled along its own axes and then rotated. Unreal documents this order for its `FTransform`: scale, then rotate, then translate. Build it the other way round, `S R`, and you are scaling along the parent's axes after rotating. Last week's section 4 showed those differ.

### Points and directions

A point has a location, so the offset applies. A **direction** (a velocity, a facing, an edge of a triangle) has no location, so it does not:

```
point:      p_parent = B p + t
direction:  v_parent = B v
```

Mixing these up is a classic bug. Move a character's forward vector with the point formula and it suddenly points at the character's position plus a unit step, which from far away is almost the same as pointing at the world origin. Unity splits the two into different methods for this reason. `TransformPoint` moves positions. `TransformDirection` rotates directions and, per its documentation, ignores both scale and position so the result keeps its length.

### Local and world space

A **space** (or coordinate frame) is a choice of origin and axes. Each node in a scene tree has its own **local space**. Its children's transforms are written in it. The root's space is **world space**.

A node's **local transform** takes points from the node's space into its parent's space. Its **world transform** takes points from the node's space all the way into world space. You met this split in CS102 week 7 as Godot's `position` and `global_position` and Unity's `localPosition` and `position`.

## 2. Composing down the tree

Suppose a parent has world transform `(Bp, tp)` and its child has local transform `(Bc, tc)`. A point `p` in the child's space goes first into the parent's space, then into the world:

```
p_world = Bp (Bc p + tc) + tp
        = (Bp Bc) p + (Bp tc + tp)
```

Read off the child's world transform:

```
B_world = Bp · Bc
t_world = Bp · tc + tp
```

The world basis is a product of matrices, parent on the left. The world origin is the child's offset carried through the parent's basis, then shifted by the parent's origin. In CS102 week 7 the second line was `world_pos(parent) + R(world_angle(parent)) · (x, y)`. It is the same formula, with the rotation `R` generalized to any basis `Bp`. The first line replaces "add the angles", which only works for pure rotations, with a matrix product that works for scale and shear too.

For a chain root → A → B → C, apply the rule repeatedly. C's world transform is `A · B · C`, the product of the local transforms from the root down. Engines compute this in one pre-order pass, handing each child its parent's result, and cache it until something above changes (the "dirty flag" from your reading).

Here is a complete 2D transform in Python. The `*` operator composes, `point` and `vector` apply, and `inverse` undoes (section 4).

```python
import math

class Xform:
    """A 2D affine transform: basis B (2x2, columns = where the axes land) plus origin t."""
    def __init__(self, B=((1.0, 0.0), (0.0, 1.0)), t=(0.0, 0.0)):
        self.B, self.t = B, t

    @staticmethod
    def trs(x, y, deg=0.0, sx=1.0, sy=1.0):
        c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        # B = R · S : scale first, then rotate
        return Xform(((c*sx, -s*sy), (s*sx, c*sy)), (x, y))

    def point(self, p):
        (a, b), (c, d) = self.B
        return (a*p[0] + b*p[1] + self.t[0], c*p[0] + d*p[1] + self.t[1])

    def vector(self, v):
        (a, b), (c, d) = self.B
        return (a*v[0] + b*v[1], c*v[0] + d*v[1])

    def __mul__(self, child):
        """parent * child = the child's transform expressed in the parent's space."""
        cols = [self.vector((child.B[0][j], child.B[1][j])) for j in (0, 1)]
        B = ((cols[0][0], cols[1][0]), (cols[0][1], cols[1][1]))
        return Xform(B, self.point(child.t))

    def inverse(self):
        (a, b), (c, d) = self.B
        k = a*d - b*c
        Bi = ((d/k, -b/k), (-c/k, a/k))
        inv = Xform(Bi, (0.0, 0.0))
        tx, ty = inv.vector(self.t)
        return Xform(Bi, (-tx, -ty))

ship  = Xform.trs(100, 50, deg=90, sx=2, sy=2)
crane = Xform.trs(3, 0, deg=30)
hook  = Xform.trs(4, 0)

crane_world = ship * crane
hook_world  = ship * crane * hook
print([round(v, 3) for v in crane_world.t])          # [100.0, 56.0]
print([round(v, 3) for v in hook_world.t])           # [96.0, 62.928]

player = (97.0, 66.0)
local = hook_world.inverse().point(player)
print([round(v, 3) for v in local])                  # [1.08, -1.201]
print([round(v, 3) for v in hook_world.point(local)])  # [97.0, 66.0]
```

`__mul__` computes the new basis by applying the parent's basis to each column of the child's basis, which is the matrix product from week 2. It computes the new origin with `point`, which is `Bp tc + tp`.

Check the crane by hand. The ship's basis is `2 R(90°) = [0 −2; 2 0]`. The crane's local origin is (3, 0). `Bp tc = (0·3 − 2·0, 2·3 + 0·0) = (0, 6)`, plus the ship's origin (100, 50), gives (100, 56). The ship is scaled 2×, so the crane's 3-unit offset became 6 world units. That is the one thing CS102's angle-only model could not do.

## 3. Worked example: the stretched parent that shears its child

### The hook

A level designer needs a long bench. They take a square crate, set its scale to (2, 1), and it becomes a bench twice as long as it is deep. Then they put a small square sign on the bench as a child and turn the sign 30° so it faces the path. In a Unity scene the sign is no longer square. It leans into a parallelogram. Unity's manual warns about exactly this: a child rotated inside a non-uniformly scaled parent can appear skewed or "sheared", and a skewed box collider no longer matches the mesh it was meant to fit.

Build the same scene in Unreal and the sign stays a rectangle. Build it in Godot and it leans, like Unity. Same scene, same numbers, two different pictures. Which one is right? The matrices say both are doing something reasonable, and the difference is in what each engine's transform type is able to store.

### The model

Parent `P` has basis `S = [sx 0; 0 sy]`, a stretch along its own axes. Child `C` has basis `R(θ)`, a rotation, and is a unit square in its own space. By section 2, the child's world basis is

```
W = S · R(θ) = | sx cos θ   −sx sin θ |
               | sy sin θ    sy cos θ |
```

Its columns are where the sign's own edges go:

```
edge_x = (sx cos θ,  sy sin θ)
edge_y = (−sx sin θ, sy cos θ)
```

The sign stays square exactly when those two edges stay perpendicular. Test with the dot product from MA101 week 13:

```
edge_x · edge_y = −sx² sin θ cos θ + sy² sin θ cos θ = (sy² − sx²) sin θ cos θ
```

This is zero only when `sx = sy` (uniform scale), or when `sin θ cos θ = 0` (θ a multiple of 90°). Every other case produces **shear**, a basis whose axes are not perpendicular. The corner angle `φ` between the edges comes from `cos φ = (edge_x · edge_y) / (|edge_x| |edge_y|)`.

Meanwhile the area is untouched. `det(W) = det(S) · det(R) = sx sy · 1`. The sign's area is scaled by `sx sy`, whatever `θ` is. Week 2 said shear keeps area and changes angles. Here it is, appearing without anyone asking for it.

The other possible answer comes from composing scale and rotation *separately*: world rotation = parent rotation + child rotation, world scale = parent scale × child scale, component by component. That gives `W' = R(θ) · S`, the sign stretched along its *own* axes and then turned. `W'` has perpendicular edges for every `θ`. It is a rectangle, 2 by 1, turned 30°. It is also not what you get by multiplying the two matrices, because `S R ≠ R S`.

### Numbers you can check

Parent scale `(sx, sy) = (2, 1)`. Child rotation `θ` varies. The table gives the child's world edges (the columns of `W = S R(θ)`), their lengths, the corner angle, and the determinant.

| θ | edge_x | edge_y | \|edge_x\| | \|edge_y\| | Corner angle φ | det(W) |
|---|---|---|---|---|---|---|
| 0° | (2.000, 0.000) | (0.000, 1.000) | 2.000 | 1.000 | 90.00° | 2 |
| 15° | (1.932, 0.259) | (−0.518, 0.966) | 1.949 | 1.096 | 110.56° | 2 |
| 30° | (1.732, 0.500) | (−1.000, 0.866) | 1.803 | 1.323 | 123.00° | 2 |
| 45° | (1.414, 0.707) | (−1.414, 0.707) | 1.581 | 1.581 | 126.87° | 2 |
| 60° | (1.000, 0.866) | (−1.732, 0.500) | 1.323 | 1.803 | 123.00° | 2 |
| 90° | (0.000, 1.000) | (−2.000, 0.000) | 1.000 | 2.000 | 90.00° | 2 |

Check the 30° row by hand. `cos 30° = 0.866`, `sin 30° = 0.5`. `edge_x = (2 · 0.866, 1 · 0.5) = (1.732, 0.5)` and `edge_y = (−2 · 0.5, 1 · 0.866) = (−1, 0.866)`. Their dot product is `−1.732 + 0.433 = −1.299`. The lengths are 1.803 and 1.323. `cos φ = −1.299 / 2.385 = −0.545`, so `φ = 123.0°`. The sign's right-angled corner has opened to 123°, and the opposite corner has closed to 57°.

Three things stand out.

The lengths change with `θ`. At 30° the sign's own x-edge is 1.803 long, not 2. There is no single "world scale" that describes this object. That is why Unity calls its world-scale property `lossyScale` and documents that when a scaled parent has a rotated child, the scale "can not be represented correctly" as three numbers, only as a 3×3 matrix. The property returns a best guess.

The worst case is 45°, and it should look familiar. At 45° the edges are `(1.414, 0.707)` and `(−1.414, 0.707)`, which point the same way as Diablo's tile columns `(32, 16)` and `(−32, 16)` from last week. A square turned 45° and stretched 2:1 *is* the isometric diamond. Its corner angle is 126.87°, the same angle that shows up in the 2:1 dimetric projection.

The area never moves. `det(W) = 2` in every row. Shear is a redistribution of shape, not a change of size. That is why it is easy to miss in a playtest and easy to spot in a collider debug view.

### The visual

Open [examples/w03-parent-scale-shear.html](../examples/w03-parent-scale-shear.html). The left view shows the child's local space: a unit square with its two axes, and the rotation `θ`. The right view shows world space: the parent bench as a stretched rectangle and the child sign drawn with `W = S R(θ)`.

Drag the rotation slider. On the left, a square turns. On the right, the square turns and leans, its corners opening and closing. The readout shows the corner angle, and a small plot underneath traces `φ` against `θ`, peaking at 126.87° at 45°. The determinant readout never changes.

Now switch the composition mode from "matrix product (Unity, Godot)" to "separate rotation and scale (Unreal FTransform)". The right view redraws the sign as a 2 × 1 rectangle turned by `θ`. Leave the "ghost" toggle on and both shapes appear at once. They have the same area and the same center, and they disagree about every corner.

### Cross-game recognition

Three major engines, three answers to the same scene.

**Unity 6.** Each `Transform` stores local position, rotation and scale. Unity renders the child with the full matrix product down the hierarchy, so the child is drawn sheared. The manual warns that rotated children of non-uniformly scaled parents may appear skewed, that a skewed box collider does not match its mesh, and that such a child's scale is not updated automatically as it rotates. The scripting reference says `lossyScale` cannot represent the skew and is only an approximation.

**Unreal Engine 5 (5.3 source, read from a public mirror).** A scene component's world transform is its relative transform times its parent's world transform, computed with `FTransform`. An `FTransform` stores a translation, a rotation quaternion and a 3-number scale. When two are multiplied with positive scales, the source composes the rotations, multiplies the scale vectors component by component, and carries the translation through. A comment in that code notes that full matrix composition was removed for non-uniform scale. So an `FTransform` cannot hold shear at all, and the child comes out as the rotated rectangle `R(θ) S`, not `S R(θ)`. Its world position is still correct, because the translation is carried through the parent's scale properly. Only the child's shape differs from the matrix product.

**Godot 4.7.** `Node3D` stores its transform as a `Transform3D` whose `Basis` is a full 3×3 matrix. The class reference says a basis can represent rotation, scale and shear, and that a sheared basis makes a model look distorted. So Godot computes and stores the true product, like Unity, and shows the lean. Godot also gives you the tools to deal with it. `Transform3D.inverse()` is documented as correct only for orthonormal bases, and `affine_inverse()` handles non-uniform ones. `Node3D` has an option to orthonormalize its global transform, removing scale and shear from that node's world transform. Its 2D sibling `Transform2D` says the same about skew.

**Skeletal animation.** Character rigs are the same tree with bones as nodes. Animators who squash and stretch a parent bone non-uniformly will shear the child bones' meshes in a matrix-product engine. Exporters and runtimes deal with this in different ways, which is one reason "don't use non-uniform scale on bones" is common advice.

Rewritten in one form, every case is a question about `S R(θ)` versus `R(θ) S`. Which product does the engine compute, and can its transform type store the answer?

### Eyes-open design judgment

Neither behavior is wrong. Each is a trade-off, and your team should pick a rule on purpose.

- **The matrix product is honest.** It is what "the child is attached to a stretched parent" means geometrically. A decal painted on a stretched wall should stretch with it. Unity and Godot give you that.
- **The TRS product is predictable.** Unreal's choice means every object's world transform is always a clean position, rotation and scale. Physics shapes stay boxes and spheres, `lossyScale`-style guesses are unnecessary, and inverting is cheap. The cost is that the child's shape no longer follows the true geometry.
- **Put non-uniform scale only on leaves.** The simplest team rule is "stretch only nodes with no children". A stretched mesh with no children cannot shear anyone. If a stretched crate needs things on it, make the crate mesh a child of an unscaled "Bench" node, and put the sign under that node, not under the mesh.
- **Colliders are the real risk.** A sheared render is a visual oddity. A sheared collider is a physics bug, because most physics engines only support boxes, spheres and capsules, which cannot shear. Unity warns about this directly. Treat any collider under a non-uniformly scaled parent as a code-review item.
- **Test at 45°.** The table shows the shear is worst at 45° and invisible at 0° and 90°. Content made on a grid often uses only multiples of 90°, so a hierarchy can look fine for months and break the first time someone rotates a child diagonally.

### Check yourself (worked example)

1. A parent has scale (3, 1). Its child is rotated 45°. Compute the child's world edges, their corner angle, and the determinant.
2. For what child rotations does a parent with scale (2, 1) produce no shear?
3. The same scene is built in Unreal. What is the world size and rotation of the child sign, and what is the area?

<details>
<summary>Answers</summary>

1. `edge_x = (3 · 0.707, 0.707) = (2.121, 0.707)`, `edge_y = (−2.121, 0.707)`. Dot product `−4.5 + 0.5 = −4.0`. Each length is `√5 = 2.236`, so `cos φ = −4 / 5 = −0.8`, `φ = 143.13°`. `det = 3 · 1 = 3`.
2. Multiples of 90°, where `sin θ cos θ = 0`. At those angles the child's edges line up with the parent's axes, so the stretch only scales them.
3. Unreal composes rotation and scale separately, so the sign has world scale (2, 1) along its own axes and world rotation 30°. It is a 2 × 1 rectangle turned 30°, with area 2, the same as the sheared version.

</details>

## 4. Going back: world space to local space

The hierarchy answers "where is my hand in the world?". Gameplay code more often asks the reverse. Where is the player relative to this guard? Did the arrow hit the front or the back of the shield? Is the ball left or right of the goalkeeper?

Each of these is a **world-to-local** conversion. It undoes the transform:

```
p_world = B p_local + t
p_local = B⁻¹ (p_world − t)
```

Subtract the origin first, then undo the basis. In the `Xform` class this is `inverse()`, which returns `(B⁻¹, −B⁻¹ t)`, and `inverse().point(p)` computes exactly the line above.

### A guard's point of view

A guard stands at `t = (10, 5)`, facing 30° (its local +x axis is forward, +y is its left). The player is at `p = (14, 9)`. The guard's basis is a pure rotation, `B = R(30°)`.

For a rotation, the inverse is the transpose. Week 2 showed that orthonormal matrices undo themselves this way. So

```
d = p − t = (4, 4)
p_local = R(30°)ᵀ d = ( 0.866·4 + 0.5·4,  −0.5·4 + 0.866·4 ) = (5.464, 1.464)
```

The player is 5.46 m ahead of the guard and 1.46 m to its left. No `atan2`, no angle wrapping. Once a point is in local space, "ahead" is the sign of `x` and "left" is the sign of `y`. The first row of `Rᵀ` is the guard's forward vector, so `p_local.x` is `forward · d`, the dot-product test from MA101 week 13. The second row is the guard's left vector, so `p_local.y` is the left-or-right test. World-to-local is those two tests run at once.

Unity exposes this as `InverseTransformPoint`, whose documentation notes the result is affected by scale, and `InverseTransformDirection`, which ignores scale and position. Godot exposes `Transform3D.inverse()` and `affine_inverse()`, and the difference matters. The fast `inverse()` is the transpose, correct only when the basis is a pure rotation. Call it on a scaled or sheared node and you get a wrong answer with no error. `affine_inverse()` does the full matrix inverse and works for any invertible basis.

### Through a hierarchy

For a node deep in a tree, first compose its world transform, then invert it. In the code above, the hook sits on a crane on a ship that is scaled 2×. The player at (97, 66) is at `(1.080, −1.201)` in the hook's space. Those are hook units, and the ship's scale of 2 makes each one 2 world meters. Mapping the local point back with `hook_world.point(local)` gives (97.0, 66.0) again, which is the round-trip check you should put in every test.

A useful identity for trees is that the inverse of a product is the product of the inverses in reverse order:

```
(A · B · C)⁻¹ = C⁻¹ · B⁻¹ · A⁻¹
```

To go from world space down to C's space, undo A first, then B, then C. Think of taking off socks and shoes. The last thing on is the first thing off.

### Normals need special care

One more trap, which the sheared sign sets up. When a basis stretches unevenly, carrying a surface normal through it with `B n` gives a vector that is no longer perpendicular to the surface. Work it through on the bench. A 45° slope in the child has normal `(−0.707, 0.707)`. Stretch x by 2 and the slope becomes shallower, but `B n = (−1.414, 0.707)` leans *more* toward horizontal, the wrong way. The correct rule for normals is to use the **inverse transpose**, `(B⁻¹)ᵀ n`, then renormalize. For the stretch, `(B⁻¹)ᵀ = [0.5 0; 0 1]`, which gives `(−0.354, 0.707)`, a normal tilted toward vertical, as a shallower slope needs. Unreal's `FTransform` source contains a comment making the same point about transforming normals and planes under non-uniform scale. For rotations and uniform scale the inverse transpose points the same way as `B` itself, which is why the bug hides until someone stretches something. Your week 1 walkable test depends on normals, so a stretched ramp checked with `B n` gives the wrong verdict.

## 5. Cost and caching

A scene has thousands of nodes, and each world transform is a matrix product. Engines keep this cheap in three ways, and you should expect all three when you read an engine's source.

- **Cache world transforms.** Store each node's world transform and recompute it only when the node or an ancestor changes. That is the dirty flag from your reading, and it turns "walk to the root every time" into one pass over changed subtrees.
- **Prefer transposes to inverses.** For rotation-only nodes, `Bᵀ` costs nothing but a reordering of numbers. That is why engines treat "orthonormal" as a special, fast case, and why Godot names the general case `affine_inverse` separately.
- **Reparent carefully.** Moving a node to a new parent while keeping its local transform makes it jump in the world. To keep its world placement, set its new local transform to `(new_parent_world)⁻¹ · (old_world)`. Engines offer this as a "keep global transform" option. With a non-uniformly scaled new parent, that product may contain shear. In Unreal it cannot be stored exactly, so the object may change shape slightly on reparenting.

## In-class activity (25 minutes)

In groups of three, one person per engine: Unity, Unreal, Godot.

1. Build (on paper, or in the interactive) a hierarchy of three nodes: `Cart` with scale (1.5, 1) at the origin, a child `Crate` at local (1, 0.5) rotated 20°, and a grandchild `Lamp` at local (0, 0.5) rotated 25°.
2. Compute the `Lamp`'s world basis as a matrix product and its world origin. Then compute its corner angle.
3. Each person predicts what their engine will display for the lamp's shape and what its reported world scale would be. Unreal's person computes the separate-rotation-and-scale version.
4. A monster is at world position (3, 2). Compute its position in the `Lamp`'s local space with the full inverse, then again with the transpose-only inverse. How far apart are the two answers?
5. Write a two-line team rule for non-uniform scale that would have prevented the difference in step 4.

Expected output: the lamp's world matrix and origin, its corner angle, three engine predictions, two local positions of the monster, and the rule.

## Common misconceptions

- **"World rotation is the sum of the angles on the path."** Only when every node on the path has uniform scale. With a non-uniform parent, the child's world basis is not a rotation at all, so it has no single angle.
- **"Inverse and transpose are the same thing."** They agree only for rotation matrices. Using the transpose on a scaled or sheared transform gives a wrong local position without any error, which is why Godot documents `inverse()` as needing an orthonormal basis.
- **"Unreal is wrong because it does not shear."** It chose a transform type that cannot store shear, in return for cheap, clean transforms. The difference is a trade-off to design around, not a bug to report.
- **"Directions and points transform the same way."** Directions ignore the origin, and surface normals need the inverse transpose once scale is uneven.

## Check yourself

1. A parent has world transform `B = [0 −1; 1 0]` (rotate 90°), `t = (5, 2)`. Its child has local origin (3, 1) and identity basis. Where is the child's origin in the world?
2. With the same parent, which local point lands on the world point (5, 6)?
3. A node's world basis is `[2 0; 0 2]` and origin (1, 1). Would Godot's `inverse()` give the right world-to-local result? What about `affine_inverse()`?
4. A child is rotated 30° under a parent scaled (1, 3). Without the full table, is the corner angle larger or smaller than 90°? Use the sign of `(sy² − sx²) sin θ cos θ`.
5. A hierarchy is root → A → B. You have the inverse world transforms of A and of B's local transform. Write B's world-to-local transform in terms of them.

<details>
<summary>Answers</summary>

1. `B tc = (0·3 − 1·1, 1·3 + 0·1) = (−1, 3)`, plus (5, 2) gives (4, 5).
2. `p_world − t = (0, 4)`. `B⁻¹ = Bᵀ = [0 1; −1 0]`. `Bᵀ (0, 4) = (4, 0)`. So the local point (4, 0).
3. No. The basis is a uniform scale of 2, not orthonormal. The transpose is `[2 0; 0 2]`, not its inverse `[0.5 0; 0 0.5]`, so distances come out 4 times too large. `affine_inverse()` computes the true inverse and is correct.
4. `sy² − sx² = 9 − 1 = 8 > 0` and `sin 30° cos 30° > 0`, so the dot product of the edges is positive. That means the angle between them is less than 90°. The corner closes, to 40.89°.
5. B's world transform is `A_world · B_local`, so its inverse is `B_local⁻¹ · A_world⁻¹`. Undo A first (apply `A_world⁻¹` to the point), then `B_local⁻¹`.

</details>

## Lab / assignment hook

[Lab 03, local and world space](../labs/lab03.md). Complete the `Xform` class (compose, point, vector, inverse, normal transform), build a four-level hierarchy from a data file, and answer gameplay questions in local space (ahead, behind, left, right). Then measure the shear every node picks up from its ancestors and flag the ones that break your team's rule. Deliverable: the completed Python file passing the tests, and a short audit table of the flagged nodes with a proposed fix for each.

## Sources

- Unity documentation, Unity 6.6 (accessed September 2026). Manual "Transform component" (non-uniform scaling; a child rotated inside a non-uniformly scaled parent may appear skewed or sheared; a skewed Box Collider does not match the rendered mesh; the child's scale is not updated automatically as it rotates). Scripting reference `Transform.lossyScale` (with a scaled parent and a rotated child the scale is skewed and cannot be represented as a 3-component vector, only a 3×3 matrix; the value is approximate). `Transform.InverseTransformPoint` (world to local, affected by scale) and `Transform.InverseTransformDirection` (not affected by scale or position).
- Unreal Engine 5.3.2 source, as mirrored publicly on GitHub (accessed September 2026). `Core/Public/Math/TransformNonVectorized.h`: `FTransform` is scale, rotation (quaternion) and translation; positions are transformed scale, rotate, translate; `Multiply` composes rotation, multiplies `Scale3D` component-wise and carries translation, with a comment that matrix composition for non-uniform scale is not supported; a comment on transforming normals under non-uniform scale with the adjoint of the inverse. `Engine/Private/Components/SceneComponent.cpp`: `CalcNewComponentToWorld_GeneralCase` returns `NewRelativeTransform * ParentToWorld`. The storage (scale, quaternion rotation, translation) and the scale, rotate, translate order also appear in Epic's API reference, "FTransform" (Unreal Engine 4.27 documentation, Internet Archive copy of 19 July 2024).
- Godot Engine documentation, class references `Transform2D`, `Transform3D`, `Basis` and `Node3D` (4.7, accessed September 2026). Basis columns; a basis can represent rotation, scale and shear; `inverse()` requires an orthonormal basis and `affine_inverse()` handles non-uniform ones; `Node3D` can orthonormalize its global transform.
- Nystrom, R. (2014). *Game Programming Patterns*, "Dirty Flag" (gameprogrammingpatterns.com).
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development*, 2nd ed. CRC Press.
- The bench, sign, ship, crane, guard and cart scenes are invented for teaching.

## Interactive spec: examples/w03-parent-scale-shear.html

**The one insight:** a rotated child under a non-uniformly scaled parent gets world basis `S R(θ)`, which shears: its corner angle swings away from 90° (worst at 45°) while its area stays fixed. An engine that composes rotation and scale separately (Unreal's `FTransform`) draws `R(θ) S` instead, a clean rectangle of the same area. Seeing both shapes overlaid is the point.

**Layout.** Two linked views side by side at 1280 px, stacked at 390 px (world view on top), plus a small plot below the world view.

- **Left, "Child local space":** a unit square centred on the origin with its local x and y axes as arrows, rotated by `θ`. Grid every 0.5 units, range −1.5 to 1.5.
- **Right, "World space":** the parent drawn as a rectangle of size `2sx × 2sy` (its local unit square scaled, centred at the world origin, light fill). The child square drawn with world basis `W` (centred at the origin, accent fill), with its two world edge vectors (`W`'s columns) drawn as arrows. Mark the corner angle at one corner with an arc and label it. Range −4 to 4 in both axes, y up, grid every 1 unit.
- **Plot, "Corner angle vs child rotation":** x-axis `θ` from 0° to 180°, y-axis `φ` from 0° to 180°, a curve for the current `(sx, sy)`, a dashed line at 90°, and a marker at the current `θ`.

**Readouts (copyable text):** `W` as a 2×2 table (3 decimals), `edge_x`, `edge_y`, their lengths, `edge_x · edge_y`, corner angle `φ` (2 decimals), `det(W)` (3 decimals), and in the separate-composition mode the same values for `W' = R(θ) S`. Add a line "Unity-style lossyScale guess: (|edge_x|, |edge_y|)" to show that the lengths change with `θ`.

**Controls (keyboard accessible, labelled):**

1. Child rotation `θ`: slider 0° to 180°, step 1°, default 30°.
2. Parent scale `sx`: slider 0.25 to 4, step 0.05, default 2.
3. Parent scale `sy`: slider 0.25 to 4, step 0.05, default 1.
4. Composition mode, radio buttons: "Matrix product S·R (Unity, Godot)" (default) and "Separate rotation and scale R·S (Unreal FTransform)".
5. "Ghost" toggle (default on): draw the other mode's shape as a dashed outline so both are visible.
6. Preset buttons: θ = 0°, 15°, 30°, 45°, 60°, 90°.

**Formulas.** `R(θ) = [cos θ, −sin θ; sin θ, cos θ]`, `S = [sx, 0; 0, sy]`. Matrix mode `W = S R(θ)`; separate mode `W' = R(θ) S`. Corner angle `φ = acos((c0 · c1) / (|c0| |c1|))` where `c0, c1` are the columns. `det = sx · sy` in both modes.

**Test values (sx = 2, sy = 1, matrix mode):** θ = 0 → edges (2, 0), (0, 1), φ = 90.00°. θ = 15 → (1.932, 0.259), (−0.518, 0.966), φ = 110.56°. θ = 30 → (1.732, 0.500), (−1.000, 0.866), lengths 1.803 and 1.323, dot −1.299, φ = 123.00°. θ = 45 → (1.414, 0.707), (−1.414, 0.707), φ = 126.87°. θ = 60 → φ = 123.00°. θ = 90 → (0, 1), (−2, 0), φ = 90.00°. `det = 2.000` throughout. Separate mode at θ = 30: `W' = [1.732, −0.5; 1.0, 0.866]`, φ = 90.00°, det 2.000. With sx = 3, sy = 1, θ = 45: φ = 143.13°, det 3.

**First screen.** Defaults (θ = 30°, scale (2, 1), matrix mode, ghost on), so the leaning sign and the dashed Unreal rectangle are both visible and the angle readout says 123.00°. Caption: "Stretch the parent, turn the child. The area never changes. The corners do."

**Accessibility and motion.** Sliders respond to arrow keys; no animation required. Under `prefers-reduced-motion`, no transitions on mode switch. The two shapes differ by fill versus dashed outline, not by colour alone.
