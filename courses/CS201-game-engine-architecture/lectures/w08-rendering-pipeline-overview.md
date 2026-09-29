# CS201 · Week 08 — Rendering Pipeline Overview

**Why this matters:** Your engine does not draw anything. It writes a list of instructions and hands it to a driver, and the GPU does the drawing. How you build and order that list decides whether a scene of two thousand objects costs 4 ms of CPU time or 24 ms, and whether glass and smoke look right or pop in front of each other. This week you learn what happens between "here is my scene" and "here are pixels", and which part of it you control.

**You will be able to:**
- Trace one triangle through the stages of the rendering pipeline and say which stages run on the CPU, which on the GPU, and which are programmable.
- Compute the number of state changes for a draw list in random and sorted order, and the CPU submit time that follows.
- Design a 64-bit sort key that groups opaque draws by material, orders translucent draws back to front, and puts the UI last.
- Predict the fragment shading cost of an overdraw-heavy scene for front-to-back, random and back-to-front order.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed.), chapter 11, sections 11.1 "Foundations of Depth-Buffered Triangle Rasterization" and 11.2 "The Rendering Pipeline". Godot Engine documentation (4.x), "GPU optimization", the sections "Draw calls, state changes, and APIs" and "Reuse shaders and materials". Unity 6 Scripting API, the page for `Rendering.RenderQueue`.

**Prerequisites from earlier courses:** [AR101 week 14, pipeline, atlases and import settings](../../AR101-visual-foundations-for-games/lectures/w14-pipeline-export-atlases-import-settings.md) (textures, mipmaps and atlases from the artist's side; this week explains why atlases also save CPU time). [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) (sorting cost). MA201, running alongside this course, covers the vertex transforms mentioned in section 1 in [week 2, matrices](../../MA201-linear-algebra-and-physics-for-games/lectures/w02-matrices-and-linear-transformations.md) and [week 4, projection](../../MA201-linear-algebra-and-physics-for-games/lectures/w04-homogeneous-coordinates-and-projection.md); you do not need them yet. From this course, [week 4, the frame](w04-the-frame-update-render-present.md) (render preparation on the CPU, GPU time, frames in flight) and [week 7, resource management](w07-resource-management-and-hot-reload.md) (materials and textures arrive as handles).

**Interactive:** [w08-draw-order.html](../examples/w08-draw-order.html). Keep it open during section 2.

---

## 1. From scene to pixels in two halves

Week 4 split the frame into CPU work and GPU work, and named one CPU stage "render preparation". This week opens that box and the GPU box behind it.

### Vocabulary first

- A **mesh** is a list of vertices (points with position, normal, texture coordinates) and a list of triangles that connect them.
- A **shader** is a small program that runs on the GPU. A **vertex shader** runs once per vertex. A **fragment shader** (Direct3D calls it a pixel shader) runs once per candidate pixel a triangle covers.
- A **material** is a shader plus the inputs it needs: textures, colors, numbers. Two objects share a material if they use the same shader with the same inputs.
- **Render state** (or pipeline state) is everything the GPU must be configured with before it can draw: which shader, which textures, which blend mode, whether to test and write depth.
- A **draw call** is one command to the GPU: "draw these triangles from this mesh with the current state". Changing render state between draw calls is a **state change**.

### The CPU half: application stage

The CPU half runs in your engine. It is often called the **application stage**.

1. **Visibility.** Decide which objects could be on screen. The cheapest version tests each object's bounding box against the camera's view volume (frustum culling). Everything that fails is skipped entirely.
2. **Build the render queue.** For each visible object, emit one entry per mesh part: which mesh, which material, which transform, which pass (opaque, translucent, UI).
3. **Sort the queue.** Put the entries in an order that is correct (translucent after opaque, back to front) and cheap (few state changes). Section 3 builds the sort key.
4. **Submit.** Walk the sorted queue. For each entry, change whatever state differs from the previous entry, then issue the draw call. The graphics API (Vulkan, Direct3D 12, Metal, OpenGL) and the driver translate this into a **command buffer** the GPU reads.

Steps 1 to 3 are ordinary engine code. Step 4 crosses into the driver, and that crossing has a price per call. Godot's documentation says it plainly: nearly every OpenGL command needs validation to check the GPU is in the right state, so the goal is to send as few instructions as possible and group similar objects to avoid state changes.

### The GPU half

The GPU works through the command buffer in stages. Follow one triangle.

| Stage | What happens to the triangle | Programmable? |
|---|---|---|
| Input assembly | Three vertex indices are read and the three vertices fetched from the mesh's buffer. | No, configured |
| Vertex shader | Each vertex is transformed from the model's space to the screen (MA201 covers the matrices). | Yes |
| Clipping and primitive assembly | Parts outside the view are cut away; the triangle is set up for rasterizing. | No |
| Rasterization | The triangle is turned into **fragments**: one per pixel center it covers, with values interpolated from the three vertices. | No, configured |
| Early depth test | If the depth buffer already holds something nearer at this pixel, the fragment is thrown away before shading. | No, configured |
| Fragment shader | Each surviving fragment computes a color: sample textures, apply lighting. | Yes |
| Output merge | Depth test (if not done early), blending with what is already there, write to the frame buffer. | No, configured |

The **depth buffer** (z-buffer) stores, for every pixel, the depth of the nearest surface drawn so far. It is what lets you draw opaque objects in any order and still get the right picture: a far wall drawn after a near crate fails the depth test at the crate's pixels. The correctness is free. The cost is not, as section 4 shows.

Two stages are programmable, and those are the ones your artists' shaders live in. The rest are fixed hardware you configure through render state. That split is why state changes exist at all: every configurable stage has settings, and changing them between draws means the GPU (and the driver on the CPU) must reconfigure.

### Where the time goes

Rendering can be slow in two different places, and the fix depends on which.

- **CPU-bound on submission.** Too many draw calls or state changes. The GPU sits idle waiting for commands. Fix: fewer, better-ordered draws.
- **GPU-bound.** Too many vertices, too many fragments, or fragment shaders that are too expensive. Fix: less geometry, less overdraw, cheaper shaders, lower resolution.

A quick test tells them apart. Halve the render resolution. If the frame gets much faster, you were paying per fragment on the GPU. If it barely moves, look at the CPU side. Week 13 turns this into a proper profiling method.

## 2. Worked example: why Hitman GO's pieces share materials

### The hook

Hitman GO (Square Enix Montreal, 2014) turned a stealth series into a mobile board game. Its characters look like painted plastic figures standing on a diorama. That look was partly an engine decision. The artists skipped detailed textures and used color swatches, so most characters shared materials, and the team noted that this let them use many colors without paying for many draw calls. On a 2014 phone, a stylistic choice was also a CPU budget choice.

Why would sharing a material matter that much? Because what costs CPU time is not the number of objects. It is the number of times the renderer has to change state between them.

### The model

Give each draw a material. Walk the draw list in order and count a **switch** each time a draw's material differs from the one before. The CPU submit time is

```
t_submit = N × c_draw + W × c_switch
```

- `N` is the number of draw calls.
- `W` is the number of material switches.
- `c_draw` is the CPU cost of issuing one draw with no state change.
- `c_switch` is the extra cost of changing material (binding a shader, textures and constants).

Now suppose `N` draws are spread evenly over `M` materials. In a **random order**, any two neighbors differ with probability very close to `1 − 1/M`. The exact expected count over a random shuffle works out to

```
W_random = N × (1 − 1/M)
```

In **sorted order**, all draws with the same material sit together, so there is one switch at each boundary:

```
W_sorted = M − 1
```

The first grows with the number of objects. The second depends only on the number of materials. That is the whole argument for sorting, and the whole argument for Hitman GO's swatches, which push `M` toward 1.

### Numbers you can check

Take `N = 2,000` draws over `M = 40` materials. Assume `c_draw = 2 µs` and `c_switch = 10 µs`. These costs are assumptions for the exercise; real values depend on the API, the driver and what the switch changes, and you will measure your own in the lab.

```python
import random

def switches(materials_in_order):
    return sum(a != b for a, b in zip(materials_in_order, materials_in_order[1:]))

def submit_ms(draws, n_switches, draw_us=2.0, switch_us=10.0):
    return (draws * draw_us + n_switches * switch_us) / 1000

N, M = 2000, 40
draws = [i % M for i in range(N)]           # 50 draws for each of 40 materials
random.seed(7)
trials = []
for _ in range(200):
    random.shuffle(draws)
    trials.append(switches(draws))
print("formula N(1 - 1/M):", N * (1 - 1 / M))
print("simulated average: ", sum(trials) / len(trials))
print("sorted:            ", switches(sorted(draws)))
print("submit ms, shuffled vs sorted:", submit_ms(N, 1950), submit_ms(N, M - 1))
```

```
formula N(1 - 1/M): 1950.0
simulated average:  1950.925
sorted:             39
submit ms, shuffled vs sorted: 23.5 4.39
```

The simulation agrees with the formula to within one switch. Now vary the scene.

| Scene | `N` | `M` | Order | Switches `W` | Submit time |
|---|---|---|---|---|---|
| City block, shuffled | 2,000 | 40 | random | 1,950 | 23.5 ms |
| City block, sorted | 2,000 | 40 | by material | 39 | 4.39 ms |
| Same, 25% translucent (500 draws, 10 materials) | 2,000 | 30 + 10 | by key (section 3) | 29 + 1 + 450 = 480 | 8.8 ms |
| Translucent materials atlased down to 2 | 2,000 | 30 + 2 | by key | 29 + 1 + 250 = 280 | 6.8 ms |
| Hitman GO style, one shared material | 2,000 | 1 | any | 0 | 4.0 ms |

Check row 3 by hand. The 1,500 opaque draws over 30 materials sort into 29 switches. One more switch happens when the queue moves from opaque to translucent. The 500 translucent draws must go back to front (section 3 explains why), so their materials land in effectively random order: `500 × (1 − 1/10) = 450`. Total 480, and `2,000 × 2 + 480 × 10 = 8,800 µs`.

At 60 Hz the whole frame has 16.7 ms. The shuffled city spends 23.5 ms just talking to the driver, so it cannot hit 60 fps whatever the GPU does. Sorting alone buys back 19 ms.

### A visual you can move

Open the interactive. The top view is a strip of 2,000 thin bars, one per draw, colored by material, in submission order. The bottom view is the submit-time bar split into "draws" and "switches", with the switch count printed. Press **Shuffle** and the strip becomes noise while the switch segment dwarfs the draw segment. Press **Sort by material** and the strip becomes 40 clean bands and the switch segment almost vanishes. Now raise the translucent share. The right end of the strip turns back into noise, because correctness forces an order that ignores materials, and the switch segment grows back. The insight the picture must make obvious: **submit time follows the number of color changes in the strip, not the number of bars.**

### Cross-game recognition

- **Unity (Unity 6).** Every material has a render queue number from 0 to 5,000. The named queues are Background 1000, Geometry 2000, AlphaTest 2450, Transparent 3000 and Overlay 4000. Objects in queues up to 2500 are sorted as opaque, normally front to back. Objects above 2500 are sorted back to front. That queue number is the top field of a sort key, exactly like the pass bits in section 3.
- **Godot 4.** The documentation lists reusing materials as its first rendering priority, then reusing shaders, and suggests atlases to reduce texture changes when materials cannot be shared. Translucent objects are drawn after opaque ones and sorted back to front by each node's position. In the model, "reuse materials" lowers `M`.
- **Texture atlases (AR101 week 14).** Packing many sprites into one texture lets them share one material, so a 2D scene's `M` drops from the number of sprites to the number of atlases. Godot's 2D renderer goes further and batches similar items into a single draw call, which lowers `N` too.
- **Unity batching (Unity 6 manual).** Static batching combines static meshes that share a material into shared buffers of up to 64,000 vertices. Dynamic batching combines small moving meshes on the CPU and only accepts meshes under 300 vertices (900 vertex attributes). Both lower `N` for draws that already share a material, which is why sharing comes first.
- **Low-overhead APIs.** AMD pitched Mantle, the forerunner of Vulkan, with a claim of up to nine times more draw calls per second than comparable APIs, by cutting CPU validation overhead. In the model that lowers `c_draw` and `c_switch`. The shape `N × c_draw + W × c_switch` stays the same.

Every one of these is either lowering `M` (share materials, atlas), lowering `N` (batch), lowering the costs (new APIs), or ordering the list so `W` approaches `M − 1` (sort).

### Eyes-open design judgment

- **Sorting costs time too.** Sorting 2,000 64-bit keys is `O(N log N)`, around 22,000 comparisons, well under a millisecond. It wins by a wide margin here. For a queue of 50 draws it may not be worth doing at all.
- **Material count is an art-direction decision.** Hitman GO chose a look that made `M` small. A realistic city with a unique material per building cannot. Agree on a material budget per scene with the art team the same way you agree on a triangle budget.
- **Batching fights culling.** Godot's documentation warns that joined objects cannot be culled one by one: a whole off-screen city joined to one visible blade of grass is drawn in full. Lowering `N` can raise GPU work.
- **Translucency is expensive twice.** It forces back-to-front order, which breaks material grouping (row 3), and it defeats the early depth test (section 4). Keep translucent materials few and small on screen.

### Check yourself (worked example)

1. A dungeon has 600 draws over 12 materials in random order. How many switches do you expect, and how many after sorting? With `c_draw = 2 µs` and `c_switch = 10 µs`, what is the saving?
2. An artist proposes giving each of 200 unique props its own material "for flexibility". The props are about 400 of the scene's 1,200 draws, and the other 800 draws use 20 materials. Sorted, how many switches does the scene have before and after the proposal if the props previously shared 4 materials?
3. Why does `W_random` barely change when `M` goes from 40 to 400, but `W_sorted` changes a lot?

<details>
<summary>Answers</summary>

1. `600 × (1 − 1/12) = 550` switches random, 11 sorted. Saving `539 × 10 µs = 5.39 ms`.
2. Before: `20 + 4 = 24` materials, 23 switches. After: `20 + 200 = 220` materials, 219 switches. That is 196 more switches, about 2 ms at 10 µs each, for one art decision.
3. `1 − 1/40 = 0.975` and `1 − 1/400 = 0.9975`, so in random order almost every neighbor already differs. Sorted, `W = M − 1` goes from 39 to 399, ten times more.

</details>

## 3. Building the sort key

Sorting by one field is easy. A real renderer needs several rules at once:

- All opaque draws before all translucent draws, and the UI last.
- Opaque draws grouped by material, and within one material, near before far.
- Translucent draws strictly far before near, whatever their material.

Instead of writing a comparison function with a chain of `if`s, pack the rules into one 64-bit integer per draw and sort the integers. The most important rule goes in the highest bits, because integer comparison looks at high bits first. The layout below is this course's own; engines use many variants of the same idea, and Unity's render queue number from section 2 is the top field of one.

```cpp
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <vector>

enum Pass : std::uint64_t { Opaque = 0, Translucent = 1, UI = 2 };

// bits 62-63: pass | bits 0-61: fields that depend on the pass
std::uint64_t make_key(Pass pass, std::uint16_t material, std::uint32_t depth24) {
    std::uint64_t key = std::uint64_t(pass) << 62;
    depth24 &= 0xFFFFFF;                                   // 24-bit depth, 0 = near
    if (pass == Translucent)                               // far first, then material
        key |= std::uint64_t(0xFFFFFF - depth24) << 16 | material;
    else                                                   // material first, near first
        key |= std::uint64_t(material) << 24 | depth24;
    return key;
}

struct Draw { const char* name; std::uint64_t key; };

int main() {
    std::vector<Draw> q = {
        {"glass A (mat 3, depth 100)", make_key(Translucent, 3, 100)},
        {"rock 1  (mat 7, depth 900)", make_key(Opaque, 7, 900)},
        {"health bar (mat 1)",         make_key(UI, 1, 0)},
        {"tree    (mat 2, depth 500)", make_key(Opaque, 2, 500)},
        {"rock 2  (mat 7, depth 200)", make_key(Opaque, 7, 200)},
        {"smoke   (mat 5, depth 800)", make_key(Translucent, 5, 800)},
    };
    std::sort(q.begin(), q.end(), [](const Draw& a, const Draw& b) { return a.key < b.key; });
    for (const Draw& d : q) std::printf("%016llx  %s\n", (unsigned long long)d.key, d.name);
}
```

Compiled with `clang++ -std=c++17`, it prints:

```
00000000020001f4  tree    (mat 2, depth 500)
00000000070000c8  rock 2  (mat 7, depth 200)
0000000007000384  rock 1  (mat 7, depth 900)
400000fffcdf0005  smoke   (mat 5, depth 800)
400000ffff9b0003  glass A (mat 3, depth 100)
8000000001000000  health bar (mat 1)
```

Read the hex. The first digit is the pass: `0` opaque, `4` translucent (binary `01` in the top two bits), `8` UI (`10`). Within opaque, the material id sits above the depth, so both rocks are together and the nearer one (depth 200) comes first. Within translucent, the depth is **inverted** (`0xFFFFFF − depth`), so the far smoke sorts before the near glass even though the smoke's material id is higher.

Three design decisions hide in that layout.

- **Field widths are budgets.** 16 bits of material allows 65,536 materials. 24 bits of depth gives about 16.7 million depth steps. If your game has more materials than the field holds, two materials alias and the sort silently groups the wrong draws.
- **Depth is quantized.** You convert the view-space distance into 24 bits. Two objects closer together than one step tie, and then the next field decides.
- **The material id should be a small dense number.** Week 7's resource handles give you one: the slot index of the material's handle. A pointer would work as a sort key but spreads draws by memory address, which is meaningless.

Why must translucent draws go far to near? Blending combines a fragment's color with whatever is already in the frame buffer. Smoke drawn over glass mixes smoke onto glass-over-scene. Glass drawn first and smoke second, when the smoke is really behind the glass, puts the smoke on top. Unlike opaque drawing, where the depth buffer fixes the order for you, blending needs the right order from you. That is why Godot sorts translucent objects back to front and why Unity treats every queue above 2500 as back to front. Both sort by object position, not per triangle, so two large overlapping translucent objects can still sort wrongly. Godot's documentation says so and offers per-material priorities and per-node sorting offsets as the fix.

## 4. Overdraw and why opaque goes front to back

Section 2 counted CPU time. Order also changes GPU time, through the early depth test.

**Overdraw** is shading the same pixel more than once in a frame. **Depth complexity** `d` is the number of opaque surfaces stacked behind one pixel. A forest viewed through its trees might have `d = 4` at many pixels.

With the early depth test on, a fragment is shaded only if it is nearer than anything drawn at that pixel so far. So the number of fragments shaded at a pixel is the number of times a new nearest surface arrives:

- **Front to back:** the first surface is the nearest, and everything after fails. 1 shaded fragment.
- **Back to front:** every surface is nearer than the last. `d` shaded fragments.
- **Random order:** the expected number of "new nearest" events in a random sequence of `d` values is the harmonic number `H_d = 1 + 1/2 + … + 1/d`.

```python
import random

def shaded_per_pixel(depth_complexity, order, trials=20000, seed=1):
    """Average fragments shaded per pixel when an early depth test is on."""
    rng = random.Random(seed)
    total = 0
    for _ in range(trials):
        depths = list(range(depth_complexity))      # 0 is nearest
        if order == "front_to_back":
            depths.sort()
        elif order == "back_to_front":
            depths.sort(reverse=True)
        else:
            rng.shuffle(depths)
        nearest = float("inf")
        for d in depths:
            if d < nearest:                         # passes the depth test
                total += 1
                nearest = d
    return total / trials

for order in ("front_to_back", "random", "back_to_front"):
    print(order, [round(shaded_per_pixel(d, order), 2) for d in (1, 2, 4, 8)])
print("harmonic", [round(sum(1 / k for k in range(1, d + 1)), 2) for d in (1, 2, 4, 8)])
```

```
front_to_back [1.0, 1.0, 1.0, 1.0]
random [1.0, 1.5, 2.08, 2.72]
back_to_front [1.0, 2.0, 4.0, 8.0]
harmonic [1.0, 1.5, 2.08, 2.72]
```

At 1920 × 1080 (about 2.07 million pixels) with `d = 4` everywhere, front to back shades 2.07 million fragments, random order about 4.3 million, and back to front 8.3 million. If the fragment shader is the GPU's bottleneck, that is up to a factor of four in GPU time from order alone.

This is why section 3's key puts depth inside the opaque pass, after material. You get material grouping for the CPU and rough front-to-back order within each material for the GPU. Some engines go further and draw a **depth prepass**: render all opaque geometry once with a trivial shader that writes only depth, then draw again with full shading and an "equal" depth test, so every pixel is shaded exactly once. It trades extra vertex work and draw calls for zero overdraw. Whether it pays depends on which side is the bottleneck, and that is a measurement, not a rule.

Mobile GPUs change the picture again. Godot's documentation notes that many mobile GPUs use tile-based rendering: they split the screen into tiles and sort each tile's triangles by depth themselves to cut overdraw, at the cost of slower vertex processing. On those GPUs, your front-to-back sort matters less and your vertex count matters more.

## In-class activity (25 minutes)

In groups of three, design the render queue for an MMO town square at peak hours.

The scene has 180 player characters (each 3 draws: body, armor, weapon), 60 buildings (each 2 draws), 400 props, 250 particle effects (translucent), and 40 UI elements. Player armor comes in 90 distinct materials. Buildings and props share 35 materials. Particles use 12 materials. UI uses one atlas.

1. Count `N`. Compute `W` for a shuffled queue using the whole-scene `M`, and for a queue sorted by your key. State your assumptions. (10 min)
2. Design the bit layout of your 64-bit key: which fields, which widths, which order. Check that 90 armor materials fit. (8 min)
3. Pick one change that would lower submit time the most: an atlas for armor, merging particle materials, or batching props. Estimate the new `W` or `N` with the model and argue for it. (7 min)

Expected output: a key diagram with bit ranges, two switch counts, and a one-paragraph recommendation with its number.

## Common misconceptions

- **"Draw calls are expensive, so count objects."** Count state changes too. A thousand draws with one material cost far less than a thousand draws alternating between two.
- **"The depth buffer means order doesn't matter."** It means order doesn't matter for *correct opaque pixels*. It matters for GPU cost (overdraw) and it matters for correctness of translucent pixels.
- **"Sorting translucent objects by distance always works."** Engines sort by object position. Large or intersecting translucent objects can still sort wrongly, and no single sort order fixes two objects that pass through each other.
- **"Batching everything is always faster."** Batched objects are culled together, so you may draw more triangles. Batching lowers CPU submit cost and can raise GPU cost.

## Check yourself

1. Name the two programmable stages of the pipeline and say how many times each runs for a mesh of 1,000 vertices covering 50,000 pixels with no overdraw.
2. In the section 3 key, a translucent draw has depth 0 (nearest possible) and material 9. Write its key in hex.
3. A scene has 1,200 opaque draws over 24 materials and 300 translucent draws over 6 materials. Estimate the switches when sorted with the section 3 key, and the submit time with `c_draw = 2 µs`, `c_switch = 10 µs`.
4. A pixel has depth complexity 3. What is the expected number of fragments shaded in random order? Which order would you pick for the opaque pass if the game is GPU-bound on fragment shading, and why might you still not draw strictly front to back?
5. Halving the render resolution changes a frame from 22 ms to 21 ms. Is the renderer CPU-bound or GPU-bound on fragments, and which technique from this lecture would you try first?

<details>
<summary>Answers</summary>

1. Vertex shader: 1,000 times (once per vertex; with an index buffer, shared vertices may even be cached). Fragment shader: 50,000 times (once per covered pixel, since there is no overdraw).
2. Pass bits `01` give `0x4000000000000000`. Inverted depth `0xFFFFFF − 0 = 0xFFFFFF`, shifted left 16 gives `0x000000FFFFFF0000`. Material 9 in the low bits. Key `0x400000FFFFFF0009`.
3. Opaque sorted: 23. Transition: 1. Translucent in back-to-front order, effectively random in material: `300 × (1 − 1/6) = 250`. Total 274. Time `1,500 × 2 + 274 × 10 = 5,740 µs ≈ 5.7 ms`.
4. `H_3 = 1 + 0.5 + 0.333 = 1.83`. Front to back within the opaque pass. You might still group by material first, because a strict depth order across materials would bring back the material switches from section 2. The key trades a little overdraw for far fewer switches.
5. Mostly not fragment-bound, since fewer pixels barely helped. Look at CPU submission first: count draws and switches, and sort or share materials.

</details>

## Lab / assignment hook

[Lab 08, a sorted render queue](../labs/lab08.md). You implement the sort key and a switch counter in C++, run them on a recorded 1,800-draw scene, and measure the switch count and a simulated submit time for three orderings. You then change the key layout to cut the translucent switches and defend the trade-off in a short memo.

## Sources

- Wikipedia, "Hitman Go" (retrieved September 2026), section on development, citing Gamasutra's 2014 coverage of Square Enix Montreal. Color swatches instead of detailed textures, so most characters shared materials and the team avoided many draw calls.
- Unity Technologies, Unity 6 Scripting API, `Rendering.RenderQueue`. Queue values 1000, 2450, 2500, 3000, 4000; range 0 to 5,000; queues up to 2500 sorted by opaque sort mode, above 2500 back to front. Geometry is the standard opaque queue (2000).
- Unity Technologies, Unity 6 Manual, "Introduction to batching meshes" (DrawCallBatching). Static batching buffers up to 64,000 vertices; dynamic batching limited to meshes under 300 vertices or 900 vertex attributes.
- Godot Engine documentation (4.x, master branch, retrieved September 2026), "GPU optimization" (validation cost of API commands, 2D batching, 3D batching and culling, reuse materials then shaders, atlases, tile-based rendering on mobile) and "3D rendering limitations", section "Transparency sorting" (back to front by node position; render priority and sorting offset).
- Wikipedia, "Mantle (API)" (checked 29 September 2026), citing AMD's GPU14 Tech Day livestream (September 2013, archived 27 September 2013). AMD's claim of up to nine times more draw calls per second than comparable APIs by reducing CPU overhead.
- Gregory, J. (2018). *Game Engine Architecture*, 3rd ed. CRC Press. Chapter 11, sections 11.1 and 11.2.

## Interactive spec: examples/w08-draw-order.html

**Purpose.** Show that CPU submit time follows the number of material changes in the draw list, that sorting collapses them to `M − 1`, and that translucency forces some of them back.

**Layout.** Two stacked views on all screen sizes, sharing the width.

- **View A, "Draw list".** A horizontal strip of `N` thin vertical bars in submission order, each colored by its material (use a fixed palette of 40 distinguishable hues generated from the shared tokens, cycling lightness for materials above the palette size). Opaque draws on the left, translucent on the right when sorted by key. Translucent bars get a diagonal hatch overlay so the pass is visible without color. Above the strip, a thin marker row with a tick at every switch (where the bar color changes). Below the strip, the text "N draws, W switches, M materials".
- **View B, "CPU submit time".** One horizontal bar, scale 0 to 30 ms, split into "draws" = `N × c_draw` and "switches" = `W × c_switch`, each segment labelled with its milliseconds. A vertical line at 16.67 ms labelled "60 Hz frame". A second, smaller bar underneath: "overdraw at d = 4" showing shaded fragments per pixel for the current opaque order (1.00 front to back, 2.08 random, 4.00 back to front).

**Controls.**
- Order buttons: **Shuffle**, **Sort by material**, **Sort by key** (opaque by material then near-to-far, translucent far-to-near with materials effectively random, UI last).
- Sliders: `N` 100 to 4,000 (step 100, default 2,000); opaque materials `M_o` 1 to 200 (default 40, the lecture's city block; the translucent test rows set it to 30); translucent share 0% to 50% (step 5%, default 0% in the first screen); translucent materials `M_t` 1 to 40 (default 10); `c_draw` 0.5 to 10 µs (default 2); `c_switch` 0 to 50 µs (default 10).
- Checkbox "one shared material (Hitman GO style)" which sets `M_o = 1` and `M_t = 1` and disables those sliders.
- Opaque depth order for view B's second bar: front to back / random / back to front, set automatically by the order button (sort by key gives front to back within material; shuffle gives random; a manual override select is allowed).

**Model.** Draw `i` gets a material and a depth drawn from a seeded PRNG (mulberry32 with seed 7, so the same slider values always give the same strip). Opaque draws use materials `0..M_o−1` evenly; translucent draws use `M_t` separate materials evenly. Count `W` directly from the displayed order: the number of adjacent pairs whose material differs. Show the formula value next to the counted value: `N(1 − 1/M)` for shuffle with `M = M_o + M_t`, and `(M_o − 1) + 1 + N_t(1 − 1/M_t)` for sort by key (omit the `+ 1` if there are no translucent draws).

**Test values.**
- `N = 2,000`, `M_o = 40`, translucent 0%, Shuffle: counted `W` within ±40 of 1,950; formula 1,950; time ≈ 23.5 ms. Sort by material: `W = 39`, 4.39 ms.
- `N = 2,000`, `M_o = 30`, translucent 25% (`N_t = 500`), `M_t = 10`, Sort by key: formula `29 + 1 + 450 = 480`, counted within ±25; time ≈ 8.8 ms.
- Same with `M_t = 2`: formula 280, ≈ 6.8 ms.
- Shared material checkbox on, any order: `W = 0` if translucent share is 0%, 4.0 ms at `N = 2,000`.

**The one insight.** On first load the strip is shuffled noise and the switches segment crosses the 60 Hz line. One press of "Sort by material" turns the strip into clean bands and the switch segment nearly disappears, while the number of bars is unchanged.

**Accessibility.** Buttons and sliders are native controls with labels and visible focus. The counted `W` and the time are in an `aria-live="polite"` region. Material colors are never the only cue: switches are also marked by ticks, and translucent draws by hatching. With `prefers-reduced-motion`, reorder instantly instead of animating bars to their new positions.
