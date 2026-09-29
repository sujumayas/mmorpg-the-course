# AR101 · Week 14 — Pipeline: Export, Atlases, Import Settings

**Why this matters:** Your art is not finished when it looks right in your drawing program. It still has to be exported, packed and imported, and each of those steps can blur it, fringe it, bleed neighboring sprites into it or quadruple its memory cost. Artists who know the pipeline catch these problems before a programmer files them as bugs against your art.

**You will be able to:**
- Compute the GPU memory of a texture or atlas for uncompressed and block-compressed formats, with and without mipmaps.
- Derive the gutter an atlas needs to stay free of bleeding up to a given mip level, and predict when padding pushes an atlas into the next power-of-two size.
- Choose import settings (filter, mipmaps, compression, color space, pixels per unit) for pixel art, painted textures and UI, and justify each.
- Diagnose common pipeline artifacts (seams, halos, blur, mixels, banding) from a description of the symptom.

**Before class:** Unity 6 Manual, "Sprite Atlas properties reference" and "Introduction to mipmaps" (each a single page). NESdev Wiki, "PPU pattern tables," the introduction only. Microsoft Learn, "Texture Block Compression in Direct3D 11," the tables of formats and bytes per block.

**Prerequisites from earlier courses:** None outside AR101. You need [week 6 (pixel art, the pixel grid and mixels)](w06-pixel-art-fundamentals.md), [week 7 (tilesets)](w07-tilesets-and-seamless-tiling.md) and last week's texel density model from [week 13, art style bibles](w13-art-style-bibles.md). Programmers meet the same material from the engine side in CS201: [week 7, resource management and hot reload](../../CS201-game-engine-architecture/lectures/w07-resource-management-and-hot-reload.md) and [week 8, rendering pipeline overview](../../CS201-game-engine-architecture/lectures/w08-rendering-pipeline-overview.md).

**Interactive:** [examples/w14-atlas-bleed.html](../examples/w14-atlas-bleed.html). Keep it open during section 2.

---

## 1. From source file to screen

Every asset passes through the same five stages. The names change between engines, but the stages don't.

1. **Source.** The working file you paint in, with layers, guides and notes. A `.psd`, `.kra`, `.aseprite` or `.blend`. Nobody outside the art team ever loads it.
2. **Export.** A flattened image, usually PNG, written by your art program. Decisions made here include the size, the trim, the pivot point, and what color the transparent pixels hold.
3. **Pack.** A tool or the engine gathers many exported images into one large texture, an **atlas** (also called a sprite sheet), and records where each image landed.
4. **Import.** The engine converts the image into the format the graphics card (GPU) uses. It decides filtering, mipmaps, compression and scale. These choices are the **import settings**.
5. **Render.** The GPU samples the texture every frame, at whatever size and angle the camera shows it.

The important idea is that stages 2 to 5 can change what the player sees without anyone editing your art. A pixel character that is perfect in the source file can arrive on screen blurred (stage 4 filtering), with a dark fringe (stage 2 transparent pixels), with a stripe of its neighbor's color along one edge (stage 3 and 4 together), or at the wrong size relative to the tiles (stage 4 scale). This lecture walks the pipeline from the artist's side so you can control each of these.

## 2. Worked example: packing an atlas, where padding costs memory and saves you from bleeding

### The hook

For its first years, Minecraft stored almost every block texture in one image, `terrain.png`. It was a 256×256 pixel file cut into a grid of 16×16 squares, one square per block texture. To change a texture you edited that one image. In snapshot 13w02a (January 10, 2013), the development build that led to Java Edition 1.5, Mojang replaced it with one image file per block and item. Then the game stitches those files back into atlases every time it loads.

So Minecraft stopped *authoring* an atlas but kept *using* one. Why go to the trouble of stitching at runtime? And what goes wrong at the seams between squares that sit side by side in one texture?

The first question has an engine answer you'll study properly in CS201. A GPU draws fastest when many objects share one texture, because switching textures between batches of drawing costs time on every frame. An atlas lets hundreds of sprites or blocks draw as if they were one. The second question is an art answer, and it's this section's model.

### Mipmaps and filtering in one paragraph each

When a texture appears on screen smaller than its real size, many texels fall inside one screen pixel. Sampling just one of them makes distant textures shimmer. The fix is a **mipmap chain**. The engine stores the texture at full size (level 0), then at half size (level 1), quarter size (level 2) and so on down to 1×1. Each level's texel is the average of a 2×2 block from the level above, so a level-`k` texel averages a `2^k × 2^k` block of the original. The GPU picks the level whose texels are about one screen pixel. The Unity manual puts the extra memory at 33%, because `1 + 1/4 + 1/16 + ...` approaches 4/3.

**Bilinear filtering** reads the four texels nearest the sample point and blends them. **Point filtering** (also called nearest) reads just one, which keeps pixel art crisp. **Trilinear** is bilinear plus a blend between two mip levels.

Both averaging steps reach *sideways*. In an atlas, sideways means into the neighboring sprite. That is **bleeding**, and it shows as a thin line of the wrong color along a sprite's edge, usually only when the camera zooms out.

### The model

One model with two parts, both about the atlas's budget.

**Memory.** For an atlas of width `W` and height `H`:

```
M = W × H × b × m
```

- `b` is bytes per texel. Uncompressed RGBA8 (8 bits each of red, green, blue and alpha) is 4. The block-compressed formats store 4×4 texel blocks at a fixed size. BC1 uses 8 bytes per block, so `b = 0.5`. BC7 uses 16 bytes per block, so `b = 1`.
- `m` is 1 without mipmaps and about 4/3 with them.

**Bleeding.** Give every sprite a **gutter** of `g` pixels on each side, filled by copying (extruding) the sprite's edge pixels outward. Start every sprite on a pixel coordinate that is a multiple of `2^L`. Then bilinear filtering cannot mix two sprites at any mip level up to

```
L = floor(log2(g))        for g ≥ 1
```

With `g = 0`, only point filtering at full size is safe.

Here is why, in one dimension. Put a sprite's left edge at position `a`, a multiple of `2^k`. At mip level `k`, one texel covers `2^k` original pixels. Sampling right at the sprite's edge, bilinear filtering reaches half a texel outward, into the level-`k` texel that covers pixels `a − 2^k` up to `a − 1`. That whole texel must be the sprite's own color. So the gutter must be at least `2^k` pixels. A 4-pixel gutter protects levels 0, 1 and 2. Level 3 needs 8.

### Numbers you can check

Pack 64 square sprites into a square power-of-two atlas (many platforms and tools prefer power-of-two sides, and square keeps the arithmetic simple). Each sprite gets a cell of `sprite + 2g` pixels on a grid. Memory is RGBA8 with no mipmaps.

| Sprite | Gutter g | Cell | Atlas | Memory | Sprite pixels fill | Safe to mip level |
|---|---|---|---|---|---|---|
| 32 | 0 | 32 | 256×256 | 256 KiB | 100% | none (point only) |
| 32 | 1 | 34 | 512×512 | 1,024 KiB | 25% | 0 |
| 32 | 2 | 36 | 512×512 | 1,024 KiB | 25% | 1 |
| 32 | 4 | 40 | 512×512 | 1,024 KiB | 25% | 2 |
| 32 | 8 | 48 | 512×512 | 1,024 KiB | 25% | 3 |
| 28 | 2 | 32 | 256×256 | 256 KiB | 77% | 1 |
| 24 | 4 | 32 | 256×256 | 256 KiB | 56% | 2 |

Check the second row by hand. A 34-pixel cell fits `floor(256 / 34) = 7` times across 256, so a 256 atlas holds 7 × 7 = 49 cells. That's short of 64, so the atlas doubles to 512×512, which holds 15 × 15. One pixel of gutter quadrupled the memory, and three quarters of the atlas is now empty.

That's the insight to carry away. **Padding is cheap per sprite and expensive at the power-of-two boundary.** The fix in the last two rows costs nothing in memory. Draw the sprites at 28 or 24 pixels and budget the gutter into the 32-pixel cell. The artist decides this before drawing, not after. That's why a pipeline rule belongs in the style bible.

The same table as a script (run it with `.venv/bin/python`):

```python
import math

def square_atlas(count, sprite, gutter):
    """Smallest square power-of-two atlas that holds `count` sprites on a grid."""
    cell = sprite + 2 * gutter
    side = 1
    while (side // cell) ** 2 < count:
        side *= 2
    return side

def safe_mip(gutter):
    return "none" if gutter == 0 else str(int(math.log2(gutter)))

for sprite, g in [(32, 0), (32, 1), (32, 2), (32, 4), (32, 8), (28, 2), (24, 4)]:
    side = square_atlas(64, sprite, g)
    kib = side * side * 4 // 1024
    fill = 64 * sprite * sprite / side ** 2
    print(f"{sprite}px + gutter {g}: {side}x{side}  {kib:4d} KiB  "
          f"fill {fill:4.0%}  safe mip {safe_mip(g)}")
```

It prints:

```
32px + gutter 0: 256x256   256 KiB  fill 100%  safe mip none
32px + gutter 1: 512x512  1024 KiB  fill  25%  safe mip 0
32px + gutter 2: 512x512  1024 KiB  fill  25%  safe mip 1
32px + gutter 4: 512x512  1024 KiB  fill  25%  safe mip 2
32px + gutter 8: 512x512  1024 KiB  fill  25%  safe mip 3
28px + gutter 2: 256x256   256 KiB  fill  77%  safe mip 1
24px + gutter 4: 256x256   256 KiB  fill  56%  safe mip 2
```

Now open [the interactive](../examples/w14-atlas-bleed.html). Set the gutter to 0 and drag the mip level slider from 0 to 2. Stone tiles drawn from the atlas grow a line of their neighbors' colors along their edges, and the line gets thicker at each level. Raise the gutter to 4 and the line disappears up to level 2, then comes back at 3. Watch the atlas size readout jump from 256 to 512 as soon as the gutter passes 0 with 32-pixel sprites. The left view shows the cost, the right view shows what it buys.

### Cross-game recognition

**Minecraft.** Back to the hook. `terrain.png` at 256×256 held a 16 × 16 grid of 16-pixel textures with no gutter, so 256 slots. By the memory model, stored as RGBA8 that's `256 × 256 × 4 = 262,144` bytes, 256 KiB. (That's this model's arithmetic, not a measurement of how the game stored it.) The current wiki documents atlases that support mipmapping, which is exactly when the gutter question starts to matter.

**The NES (1983 hardware).** The console's pattern tables are an atlas in hardware. Each table holds 256 tiles of 8×8 pixels, and each tile takes 16 bytes because every pixel has 2 bits (four color indices, one meaning transparent). Arrange the 256 tiles as a 16 × 16 grid and you have a 128×128 pixel image. Run the memory model with `b = 2/8 = 0.25` bytes per pixel. `128 × 128 × 0.25 = 4,096` bytes, exactly the 4 KiB address range of one table. Same formula, forty years apart. The NES never filtered or mipmapped, so it never needed a gutter.

**Stardew Valley (1.6 era).** Map art lives in tilesheets, PNG images cut into 16×16 tiles, and the modding docs say the tile size should always be 16. A tilesheet is an atlas authored by hand on a fixed grid. Because the game draws pixel art without mip-level blending, tiles can sit edge to edge.

**Unity (version 6).** The engine's Sprite Atlas asset has a padding setting with a default of 4 pixels between sprites, and an Alpha Dilation option that spreads a sprite's edge colors into the neighboring transparent pixels. Read through the model, 4 pixels shared by two neighbors gives each sprite about 2 pixels of its own, so the default is clean to about mip level 1, and only if sprites start on even coordinates. If those sprites will be seen further away, raise the padding. The model tells you which question to ask about any tool's default.

Four systems, one budget. Every atlas trades memory for gutter, and the power-of-two boundary decides when that trade suddenly gets expensive.

### Eyes-open design judgment

- **Pixel art usually wants no mipmaps, point filtering and a small gutter.** Pixel art drawn at integer scale is never shown smaller than its native size, so mipmaps buy nothing and blur edges. With point filtering and no mipmaps the model says `g = 0` is safe, though teams often keep 1 or 2 pixels to absorb rounding errors when the camera sits between pixels.
- **Painted and 3D textures need mipmaps, so they need gutters.** A painted prop sheet seen at many distances will bleed without a gutter. Decide the deepest mip level you care about (how far away the camera gets) and set `g = 2^L`.
- **Budget the gutter inside the grid.** If sprites live in 32-pixel cells, draw them at 28 or 24 and say so in the bible. Retrofitting a gutter onto finished 32-pixel art is what causes the 4× memory jump.
- **Separate atlases by how they're filtered.** Pixel sprites, painted props and UI want different import settings. One atlas has one set of settings. Mixing them forces a compromise that hurts everything in it.
- **Atlases are shared, so one bad sprite hurts many.** An oversized sprite can push an atlas into the next size and cost every sprite in it memory. Put size limits in the bible's technical chapter and check them at export.

## 3. Export, the part the artist controls

Most pipeline bugs that land on an artist's desk start at export. Five habits prevent most of them.

**Export at 1×.** Pixel art is exported at its native size, one art pixel per image pixel. Scaling happens in the engine through import settings or the camera, never in the file. An exported 4× copy looks fine until someone scales it by 0.75 to fit and every art pixel becomes a 3-pixel block, or until it sits next to a 1× tile and the two have different densities (week 13).

**Name files so a machine can sort them.** `hero_walk_03.png`, not `Hero Walk (final) 3.png`. Lowercase, no spaces, a fixed prefix per group, zero-padded frame numbers. Packers often sort alphabetically, and animation frames that sort `1, 10, 11, 2` play out of order.

**Decide trim and pivot deliberately.** Trimming removes empty transparent border so the atlas wastes less space. But the sprite's **pivot**, the point the engine uses as its position, often the feet, is measured from the image's corner. If you trim a walk cycle frame by frame, each frame's feet move relative to its corner and the character jitters. Either trim with a tool that records the offset, or keep every frame of an animation on the same canvas size.

**Fill transparent pixels with color, not black.** In a PNG, a fully transparent pixel still stores red, green and blue values. Many programs store black. When bilinear filtering blends an edge pixel with its transparent neighbor, that black leaks into the edge and the sprite grows a dark halo. There are three fixes. Extrude or dilate edge colors into the transparent area (what Unity's Alpha Dilation automates). Use premultiplied alpha, a storage form where color is already multiplied by opacity, so transparent pixels contribute nothing. Or use point filtering. Know which one your project uses and write it in the bible.

**Export in the color space the engine expects.** Color textures are almost always authored in sRGB, the standard color space for displays. Data textures such as normal maps and masks are not colors and must be imported as linear. An sRGB flag on a normal map bends its values and the lighting goes subtly wrong. This is an import setting, but the artist has to label which files are data.

## 4. Import settings, as a table for your bible

Import settings live in the engine, but they decide how your art looks, so the art team should own them. Here is a starting table for the three kinds of asset in this course. The names follow Unity 6, and every major engine has the same knobs under similar names.

| Setting | Pixel-art sprites and tiles | Painted props and 3D textures | UI icons and panels |
|---|---|---|---|
| Filter mode | Point (no filter) | Bilinear or trilinear, plus anisotropic for floors seen at steep angles | Bilinear |
| Mipmaps | Off | On | Off if shown at native size |
| Compression | None, or lossless | Block compressed (BC7 for quality, BC1 for opaque and cheap) | None or BC7, check text edges |
| Color space | sRGB | sRGB for color, linear for normal and mask maps | sRGB |
| Pixels per unit | The tile size, the same for every sprite | Not used, texel density comes from UVs | Match the UI reference resolution |
| Atlas gutter | 0 to 2 | `2^L` for your deepest mip level | 2 to 4 with alpha dilation |

A few rows need explaining.

**Pixels per unit is texel density for 2D.** Unity's manual defines it as the number of sprite pixels that correspond to one unit of world space. That is `D` from last week's model with the world unit as the denominator. If the tiles import at 16 pixels per unit and one character imports at 32, the character renders at half size with pixels half as big as the tiles' pixels. That's a mixel, created by a single number in a settings panel. Make the value a hard rule in the bible.

**UI often doesn't need mipmaps.** The Unity manual notes that mipmaps give no benefit to a texture that is only shown at its full resolution, such as unscaled UI, while still costing a third more memory. Turn them off for HUD art drawn at native size. Keep them for UI that appears in the 3D world, like nameplates above players in an MMO, because those shrink with distance.

**Compression is lossy and blocky.** BC1 and BC7 work on 4×4 blocks and choose a small set of colors per block. On painted textures the loss is hard to see. On pixel art, where every pixel is a deliberate color from a small palette, the encoder may shift colors or blend them across a block edge. Pixel sprites are small, so leaving them uncompressed usually costs little. Check it with the memory model.

Price a full 2048×2048 atlas three ways to see what compression buys:

| Format | Bytes per texel | No mipmaps | With mipmaps (× about 4/3) |
|---|---|---|---|
| RGBA8 | 4 | 16 MiB | about 21.3 MiB |
| BC7 | 1 | 4 MiB | about 5.3 MiB |
| BC1 | 0.5 | 2 MiB | about 2.7 MiB |

Compare that with the 64-sprite pixel atlas from section 2, 256 KiB uncompressed. Pixel art almost never needs compression to fit. Large painted atlases almost always do.

## 5. A pipeline chapter for the style bible

Last week's bible had a technical chapter. This week gives you what goes in it. A good one answers each of these with a number or a named setting:

- Texel density target and tolerance, or pixels per unit for 2D (week 13).
- Maximum texture and sprite sizes per asset type.
- Atlas groups (which assets share an atlas) and each group's import settings from the table above.
- Gutter size and grid cell size, stated as "draw inside N pixels of a M-pixel cell."
- Transparent-pixel rule (dilate, premultiply or point-filter).
- File naming pattern, trim and pivot rules for animations.
- Which files are color (sRGB) and which are data (linear).

Each rule also needs a test, the same way last week's rules did. Most of these tests are automatic. A script can read every PNG in the export folder, check its size against the limit, check that transparent pixels aren't black at the edges, and check names against the pattern. That's the kind of script you'll start in the lab.

## In-class activity (25 minutes)

In pairs, diagnose five bug reports from an imaginary MMO team. For each, name the pipeline stage (export, pack, import or render), the cause, and the fix. Then write the bible rule that would have prevented it.

1. "When I zoom the camera out, a thin green line appears along the top of every stone path tile."
2. "The oak tree sprite has a dark outline that isn't in the source file. It's worst on the leaves."
3. "The new pixel-art hero looks soft and blurry compared to the tiles around her."
4. "The pet's pixels look half the size of every other creature's pixels."
5. "Our UI atlas went from 1 MiB to 4 MiB when we added one 40×40 icon."

Expected output is a five-row table (symptom, stage, cause, fix, bible rule). Swap tables with another pair and check each other's fixes against the section 2 model and the import settings table. The two bugs most pairs get wrong are 4 (it's an import setting, not the art) and 5 (it's a power-of-two jump, not the icon's own size).

## Common misconceptions

- **"Padding is a few pixels, so it costs a few pixels."** It costs a few pixels per sprite until the total crosses a power of two, and then the atlas doubles in each direction. In the section 2 table one pixel of gutter took 256 KiB to 1,024 KiB.
- **"Mipmaps make everything look better."** They prevent shimmer on textures shown smaller than native size. On pixel art and unscaled UI they blur edges and cost a third more memory for nothing.
- **"Transparent pixels are invisible, so their color doesn't matter."** Filtering blends them into visible edge pixels. Black transparent pixels make dark halos.
- **"Import settings are the programmer's job."** They decide sharpness, color and size on screen. If the art team doesn't own them, the look is set by whoever touched the panel last.

## Check yourself

1. An atlas is 1024×1024 RGBA8 with mipmaps. About how much GPU memory does it use? How much as BC7 with mipmaps?
2. Your painted prop atlas will be seen down to mip level 3. What gutter does each sprite need, and on what coordinates should sprites start?
3. You have 100 square icons of 30×30 pixels and add a 1-pixel gutter. What is the smallest square power-of-two atlas that holds them on a grid? What if the gutter is 2?
4. A tileset imports at 16 pixels per unit. A new chest sprite, drawn at the same pixel size as the tiles, imports at 32 pixels per unit. What does the player see, and what is the fix?
5. Using the NES numbers, how many bytes would one 8×8 tile take if each pixel had 4 bits (16 color indices) instead of 2?

<details>
<summary>Answers</summary>

1. `1024 × 1024 × 4 = 4 MiB`, times about 4/3 is about 5.3 MiB. As BC7, `b = 1`, so 1 MiB, about 1.3 MiB with mipmaps.
2. `g = 2^3 = 8` pixels of extruded edge on every side, and every sprite starts on a multiple of 8.
3. With `g = 1` the cell is 32. A 256 atlas holds 8 × 8 = 64, too few, so 512×512 (16 × 16 = 256 cells). With `g = 2` the cell is 34. A 256 atlas holds 7 × 7 = 49, still too few. A 512 atlas holds 15 × 15 = 225, enough, so still 512×512. Either way it's 512.
4. The chest renders at half the size it should, and its pixels are half the size of the tiles' pixels. The fix is to import it at 16 pixels per unit like everything else, and to make pixels per unit a hard rule in the bible.
5. `8 × 8 × 4 bits = 256 bits = 32 bytes`, twice the NES's 16.

</details>

## Lab / assignment hook

[Lab 14, build an atlas packer](../labs/lab14.md). You finish a small Python atlas packer and memory calculator, pack a set of 40 MMO interface sprites with different gutters, find the power-of-two cliff in real data, and write the pipeline chapter of your style bible from the results.

## Sources

- Minecraft Wiki, "terrain.png" and "Texture pack" (Java Edition history). `terrain.png` was a 256×256 atlas split into 16×16 squares; in snapshot 13w02a (January 10, 2013, leading to Java Edition 1.5) it was replaced by individual block and item images stitched into atlases at runtime.
- Minecraft Wiki, "Java Edition 13w02a" and "Resource pack" (current). One file per block or item, stitched at runtime; atlases that support mipmapping.
- NESdev Wiki, "PPU pattern tables." Each tile is 16 bytes in two bit planes; each pattern table holds 256 tiles, at $0000-$0FFF and $1000-$1FFF.
- Microsoft Learn, "Texture Block Compression in Direct3D 11." BC1 uses 8 bytes per 4×4 block; BC7 uses 16 bytes per 4×4 block.
- Unity Technologies, Unity 6 Manual, "Sprite Atlas properties reference." Padding default of 4 pixels between sprites; Alpha Dilation spreads edge colors into transparent pixels.
- Unity Technologies, Unity 6 Manual, "Introduction to mipmaps." Mipmaps add 33% to size and give no benefit to textures shown only at full resolution, such as unscaled UI.
- Unity Technologies, Unity 6 Manual, "Sprite (2D and UI) texture Import Settings." Pixels Per Unit definition; Point, Bilinear and Trilinear filter modes; mipmap generation.
- Stardew Valley Wiki, "Modding:Maps" (1.6 era). Tilesheets are PNG images divided into 16×16 tiles; tile size should always be 16.

## Interactive spec: examples/w14-atlas-bleed.html

**The one insight.** A gutter is what stops neighboring sprites bleeding into each other as the texture shrinks, and each extra mip level needs twice the gutter. But the gutter's real cost only shows at the power-of-two boundary, where one pixel can quadruple the atlas.

**Layout.** Two linked views, side by side on desktop, stacked on mobile.

- **Left, "The atlas."** A square atlas drawn to scale (fit to panel) holding 64 invented sprites, each a flat colored shape on transparent background (circle, square, triangle, diamond in 8 distinct palette colors, repeating). Each sprite's gutter is drawn in a lighter tint of its own color (extruded), and empty atlas area is a neutral checkerboard. Readouts under it: atlas side, memory in KiB for the selected format, fill percentage, safe mip level.
- **Right, "In the game."** A strip of 6 ground tiles drawn from one atlas sprite (a solid "stone" gray square whose atlas neighbors above and below are bright green and whose neighbors to the left and right are bright magenta). The strip is rendered at the chosen mip level by software: build the mip chain from the atlas image with a 2×2 box filter, then sample each output pixel with bilinear filtering at that level. Show it magnified. For every level-k texel of the tile, take a 4×4 grid of evenly spaced sample points (at offsets 1/8, 3/8, 5/8, 7/8 of the texel) and bilinearly sample each, then draw each sample as a block. This magnified sampling is what lets edge samples reach half a texel outward, as in the lecture's derivation. Bleeding shows as green or magenta along tile edges.

**Controls.**

- Sprite size (select: 24, 28, 32; default 32).
- Gutter `g` per side (slider 0 to 8, integer; default 0).
- Align sprites to `2^L` toggle (default on). When off, the stone starts where the packed grid puts it (one cell plus `g`) with no rounding, and the model's level is no longer a guarantee. With the sprite sizes offered here (24, 28, 32) the unaligned stone happens to bleed at the model's level or later, never earlier (for example `g = 1` stays clean at level 1). The page says so in a note, and presents the aligned case as the guarantee.
- Mip level (slider 0 to 4; default 0).
- Filter (radio: point, bilinear; default bilinear). Point with mip level 0 must show no bleeding at `g = 0`.
- Format for the memory readout (radio: RGBA8, BC7, BC1) and a mipmaps checkbox.

**Formulas.** Cell `= sprite + 2g`. Atlas side is the smallest power of two `s` with `floor(s / cell)^2 ≥ 64`. Memory `= s² × b × m` with `b` = 4, 1, 0.5 and `m` = 1 or the exact mip-chain sum (for block formats count whole 4×4 blocks per level, minimum one block). Fill `= 64 × sprite² / s²`. Safe mip `L = floor(log2 g)` for `g ≥ 1`, "none (point only)" for `g = 0`.

**Test values (must match the lecture table).**

| Sprite | g | Atlas | RGBA8, no mips | Fill | Safe mip |
|---|---|---|---|---|---|
| 32 | 0 | 256 | 256 KiB | 100% | none |
| 32 | 1 | 512 | 1,024 KiB | 25% | 0 |
| 32 | 2 | 512 | 1,024 KiB | 25% | 1 |
| 32 | 4 | 512 | 1,024 KiB | 25% | 2 |
| 32 | 8 | 512 | 1,024 KiB | 25% | 3 |
| 28 | 2 | 256 | 256 KiB | 77% | 1 |
| 24 | 4 | 256 | 256 KiB | 56% | 2 |

Extra checks. 256 atlas RGBA8 with mipmaps shows 341.3 KiB. The right view with `g = 4`, aligned, bilinear shows no green or magenta at mip levels 0, 1 and 2, and shows it at level 3. With `g = 0`, bilinear shows faint bleeding at level 0 already, in the outermost samples of the edge texels. With `g = 1`, level 0 is clean and level 1 bleeds.

**First screen.** Sprite 32, `g = 0`, mip level 1, bilinear, so the green line is visible immediately and the atlas readout says 256 KiB.

**Constraints.** Self-contained HTML, palette tokens from `templates/interactive-tokens.css` inline, invented shapes only, keyboard operable, `prefers-reduced-motion` respected, light and dark themes, no horizontal overflow at 390 px. Keep the software renderer small (the strip is at most 6 × 32 source pixels wide) so it updates instantly on slider input.
