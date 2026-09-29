# AR101 · Week 07 — Tilesets and Seamless Tiling

**Why this matters:** Most 2D game worlds, and a lot of 3D ground, are built from a few small squares repeated thousands of times. If the squares don't join cleanly, the player sees a grid instead of a meadow. If you draw the wrong set of pieces, your level designer can't paint a path without you drawing new art every afternoon. This week you learn to draw tiles that repeat without seams, and to work out exactly which pieces a tileset needs before you draw any of them.

**You will be able to:**
- Compute the neighbour index of any tile in a map using the 4-bit edge rule and the 8-bit blob rule.
- Derive why an edge set needs 16 tiles, a corner set 16, and a full blob set 47, and compute the count for more terrains.
- Measure whether a tile will show a seam using the seam ratio, and fix a tile that fails.
- Choose between corner, edge and blob tilesets for a given game, and justify the art cost.

**Before class:** The Tiled manual, "Using Terrains" (Tiled 1.5 and later, current online edition). The GameMaker manual page on auto tiles. The Godot 4 documentation, "Using TileSets", section on terrains. Each is under ten minutes of reading. Skim, then come back to them after section 2.

**Prerequisites from earlier courses:** AR101 has no prerequisite courses. From this course, [week 6 on pixel art fundamentals](w06-pixel-art-fundamentals.md) sets the pixel grid, palette limits and clean lines you will use inside each tile. If you take CS101 in parallel, [CS101 week 5, arrays and lists](../../CS101-programming-for-games-i/lectures/w05-arrays-and-lists-inventories.md) shows how a grid is stored as a list of rows, which is how the code in this lecture reads a map.

**Interactive:** [`examples/w07-autotile.html`](../examples/w07-autotile.html). Keep it open during section 2.

---

## 1. Why games are made of tiles

A **tile** is a small square image, usually 8, 16 or 32 pixels on a side, drawn so that it can be placed on a grid next to other tiles. A **tileset** is the collection of tiles for one kind of place. A **tilemap** is the grid itself. Each cell of a tilemap holds a number, and the number says which tile from the tileset to draw there.

Tiles began as a memory trick, and the trick still explains how artists think about them. Take the Nintendo Entertainment System (NES, 1983 in Japan, 1985 in North America). Its background is a grid of 32 by 30 tiles, each 8 by 8 pixels, for a picture 256 pixels wide and 240 tall. The grid, called a nametable, takes 960 bytes, one byte per cell. The tile images live in a separate pattern table that holds 256 tiles of 16 bytes each, because each pixel has 2 bits (four possible colors).

Do the arithmetic. A unique 256 by 240 picture at 2 bits per pixel needs `256 × 240 × 2 / 8 = 15,360` bytes. The tile version needs 960 bytes for the grid plus 64 bytes of palette choices, and it reuses one shared set of 4,096 bytes of tile images (`256 × 16`) across every screen in that part of the game. The second screen of a level costs about 1 KB, not 15 KB.

The NES has one more rule that shaped its art. Its attribute table picks one of four background palettes for each 16 by 16 pixel area, which is a block of 2 by 2 tiles. You can't color a single 8 by 8 tile on its own. So NES artists usually built with 16 by 16 blocks of four tiles, often called **metatiles**, and designed maps in those blocks. When you see a staircase or a brick wall in an 8-bit game that seems to come in chunks of 16 pixels, that is why.

Modern hardware has memory to spare. Tiles survived for other reasons, and those reasons are what this lecture is about.

- **Speed of building.** A level designer paints a map with a brush that places tiles. A map of 200 by 200 cells is 40,000 decisions if each one is hand-painted art, and a few hundred brush strokes if it is tiles.
- **Consistency.** Every stone path in the game uses the same corner piece, so the world looks like one place.
- **Rules.** Because each cell is a number, the game can read the map. Walkable, water, wall. Collision and pathfinding come for free.

The cost is repetition. The player's eye is very good at finding a repeated pattern. Your job as the artist is to make the grid disappear. That has two parts. Each tile must join its copies without a visible seam, and the set of tiles must cover every way that terrains meet.

### Seamless tiles

A tile is **seamless** if a grid of copies of it shows no visible line where one copy ends and the next begins. The test artists use is the **offset test**. Shift the tile by half its width and half its height, wrapping pixels that fall off one side back onto the other. The old edges now meet in a cross through the middle of the tile, where you can see them. Most image editors have an offset or wrap view for exactly this.

You can put a number on it. Treat the tile as a grid of values, using CIE lightness L* from 0 to 100 as in [week 1](w01-seeing-like-an-artist-value-before-color.md). Look at every pair of neighbouring pixels inside the tile and take the mean absolute difference between them. Call it `d_in`. Then look at the pairs that meet across the wrap: the left column against the right column, and the top row against the bottom row. Take their mean absolute difference and call it `d_wrap`. The **seam ratio** is

```
seam ratio = d_wrap / d_in
```

- `d_in` is how much the texture changes from one pixel to the next in normal places.
- `d_wrap` is how much it changes across the joint between two copies.

A ratio near 1 means the joint looks like any other place in the texture, so the eye can't find it. A ratio well above 1 means the joint is a line. Our course uses 1.5 as the pass mark. That is a teaching threshold that works on small pixel tiles, not a published standard.

Two 4 by 4 tiles show the idea. The first is a diagonal pattern that steps by 10 between every pair of neighbours, including across the wrap:

```
40 50 60 50
50 60 50 40
60 50 40 50
50 40 50 60
```

Every one of the 24 interior pairs differs by 10, so `d_in = 10`. Each of the 8 wrap pairs also differs by 10, so `d_wrap = 10` and the ratio is 1.0. The second tile is a left-to-right gradient, four identical rows of `20 40 60 80`. Inside, the 12 horizontal pairs differ by 20 and the 12 vertical pairs by 0, so `d_in = 10`. Across the wrap, the 4 horizontal pairs differ by `80 − 20 = 60` and the 4 vertical pairs by 0, so `d_wrap = 30`. The seam ratio is 3.0. Tile the gradient and you get stripes with a hard dark-to-light jump every four pixels. That is a seam.

The fix is always the same. Whatever leaves one edge must come back in on the opposite edge. Paint across the offset cross until it vanishes, then offset back and check the original edges again.

### Seamless is not enough

A perfectly seamless tile still repeats. A 16 pixel grass tile on a 320 by 180 screen appears 20 times across and more than 11 times down. The player sees a wallpaper pattern, especially if the tile contains one bright flower. Three habits help.

- **Keep contrast low inside fill tiles.** A single high-contrast detail becomes a dot on a grid. Put details in separate decoration tiles and place those by hand.
- **Draw variants.** Two to four versions of the fill tile, with the same edges and different interiors. If the map picks among `v` variants at random, two neighbours match by chance only `1/v` of the time. [CS101 week 13](../../CS101-programming-for-games-i/lectures/w13-randomness-spawning-and-procedural-variety.md) covers seeded random choice, which keeps the map the same every time it loads.
- **Break the grid with larger pieces.** Rocks, trees and buildings that span several cells cover the rhythm.

## 2. Worked example: how many pieces does a path need?

### The hook

Open the auto tile page of the GameMaker manual and you'll find two template sizes, one with 16 tiles and one with 47. Open the Tiled manual and it says a complete corner set for two terrains needs 16 tiles, an edge set 16, and a set that matches corners and sides 256, though a "blob" set of 47 is enough in practice. Godot 4 offers three terrain modes with names that line up with those three sets.

47 is an odd number for three different tools to agree on. It isn't a convention someone picked. It falls out of one rule about which neighbours change the drawing. Once you see the rule you can plan any tileset before you draw it, and you'll know what a request like "add a third terrain" will cost you.

### The model

**Autotiling** means the editor picks each tile for you by looking at the cell's neighbours. You paint "path here" and the tool chooses the straight piece, the corner, the dead end or the crossing. To do that it turns the neighbourhood into a number, the **neighbour index**, and uses the number to look up a tile.

For the **edge rule**, look at the four cells that share a side with this one. Give each a bit value:

```
edge index = 1·N + 2·E + 4·S + 8·W
```

- `N`, `E`, `S`, `W` are 1 if the neighbour to the north, east, south or west is the same terrain, and 0 if not.
- Each neighbour doubles the value of the one before, so every combination gives a different sum from 0 to 15.

Four neighbours with two states each give `2^4 = 16` combinations, so an edge set has 16 tiles. Index 0 is an isolated blob. Index 15 is a cell surrounded on all four sides. Index 5 (`N + S`) is a vertical straight piece.

For the **blob rule**, look at all eight neighbours and number them clockwise from north:

```
blob index = 1·N + 2·NE + 4·E + 8·SE + 16·S + 32·SW + 64·W + 128·NW
```

Eight neighbours give `2^8 = 256` combinations. But most of those draw the same picture, because of one fact.

**A corner neighbour only matters when both edges beside it are filled.** Picture a path cell with a path to the east and nothing to the north. Whether the north-east cell holds path or grass makes no difference to this tile, because this tile's north edge is already a grass border. The corner shows up only when north and east are both path. Then you have to decide whether the inside corner is filled (a solid area) or notched (two paths meeting at a corner of grass).

So before looking up a tile, clear every corner bit whose two neighbouring edges aren't both set. Count what is left by grouping the 16 edge patterns by how many "live" corners each one has:

| Edge pattern | How many patterns | Live corners | Tiles |
|---|---|---|---|
| No edges | 1 | 0 | 1 |
| One edge | 4 | 0 | 4 |
| Two opposite edges (a straight) | 2 | 0 | 2 |
| Two adjacent edges (an elbow) | 4 | 1 | 4 × 2 = 8 |
| Three edges (a T) | 4 | 2 | 4 × 4 = 16 |
| Four edges | 1 | 4 | 1 × 16 = 16 |
| **Total** | 16 | | **47** |

An elbow has one live corner, which can be filled or empty, so each elbow comes in two versions. A T has two live corners and four versions. A cell surrounded on four sides has four live corners and 16 versions. Add them and you get 47.

The **corner rule** is the third model, and the one Tiled calls a corner set. Instead of asking which neighbours are filled, it stores terrain at the four corners of each cell. A tile is then described by four corner values, each grass or path, so there are `2^4 = 16` tiles. Painting happens on the grid of corners, which sits half a cell offset from the tile grid. Artists often call this a **dual grid**. Corner sets make soft, rounded transitions between large areas. They can't draw a path one tile wide, because a path narrower than a tile has no corners of its own.

### Numbers you can check

Here is a small map of a plaza with a path leaving south. 1 is path, 0 is grass. Each path cell shows `edge index / blob index`.

```
map                 edge / blob
0 0 0 0 0            .      .      .      .     .
0 1 1 1 0            .    6/28   14/124 12/112  .
0 1 1 1 0            .    3/7    15/215  9/193  .
0 0 1 0 0            .      .     5/17    .     .
0 0 1 0 0            .      .     1/1     .     .
```

Check three of them by hand.

- **Top-left plaza cell** (row 1, column 1). East and south are path, north and west are grass. Edge index `2 + 4 = 6`. For the blob index, E is 4, S is 16, and the south-east corner is path with both of its edges (E and S) filled, so it counts: 8. Total 28.
- **Plaza centre** (row 2, column 2). All four edges are path, so the edge index is 15. In the blob rule, N, NE, E, S, W and NW are path, but SE and SW are grass because the path narrows below. That gives `1 + 2 + 4 + 16 + 64 + 128 = 215`. The tile shows a solid plaza with two small grass notches at its lower corners.
- **Bottom of the path** (row 4, column 2). Only north is path. Edge index 1, blob index 1. A dead end.

Now compare the plaza centre in the two rules. The edge rule says 15, "surrounded", and draws a plain fill tile. It can't see that the lower corners are grass, so the path's inside corners come out square and wrong. The blob rule sees them. That is the whole reason blob sets exist: an edge set can't draw inside corners.

The code below computes both indices and confirms the count of 47 by pushing all 256 raw patterns through the corner rule. Run it with `.venv/bin/python`.

```python
EDGE = [(-1, 0, 1), (0, 1, 2), (1, 0, 4), (0, -1, 8)]                  # N E S W
BLOB = [(-1, 0, 1), (-1, 1, 2), (0, 1, 4), (1, 1, 8),
        (1, 0, 16), (1, -1, 32), (0, -1, 64), (-1, -1, 128)]         # N NE E SE S SW W NW
CORNERS = [(2, 1, 4), (8, 4, 16), (32, 16, 64), (128, 64, 1)]        # corner bit, its two edges


def filled(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == 1


def edge_index(grid, r, c):
    return sum(bit for dr, dc, bit in EDGE if filled(grid, r + dr, c + dc))


def corner_rule(m):
    for corner, a, b in CORNERS:
        if m & corner and not (m & a and m & b):
            m -= corner
    return m


def blob_index(grid, r, c):
    return corner_rule(sum(bit for dr, dc, bit in BLOB if filled(grid, r + dr, c + dc)))


plaza = [[0, 0, 0, 0, 0],
         [0, 1, 1, 1, 0],
         [0, 1, 1, 1, 0],
         [0, 0, 1, 0, 0],
         [0, 0, 1, 0, 0]]
print(edge_index(plaza, 1, 1), blob_index(plaza, 1, 1))
print(edge_index(plaza, 2, 2), blob_index(plaza, 2, 2))
print(len({corner_rule(raw) for raw in range(256)}), "blob tiles")
```

It prints `6 28`, then `15 215`, then `47 blob tiles`.

### The visual

Open [`examples/w07-autotile.html`](../examples/w07-autotile.html). The left view is a map you paint with a click or the keyboard. The right view is the tileset, with every tile the map is using lit up and a counter such as "using 8 of 47" (the count for the lecture's plaza map). Switch between the edge, blob and corner rules.

Try this. Paint a 3 by 3 block, then add a single path cell touching one of its corners diagonally. In the blob rule the block's corner tile doesn't change, because the diagonal neighbour touches an edge pair that isn't filled. Now fill one of the two cells between them. The corner tile changes at once. You've watched the corner rule decide which of the 256 patterns matter. Then switch to the edge rule and paint a plus sign. The centre shows a plain fill with square inside corners, the flaw you found by hand above.

### Cross-game recognition

Every major 2D tile tool uses one of these three rules. Learn to recognize them under different names.

**Tiled (1.5 and later).** Tiled calls them a Corner Set, an Edge Set and a Mixed Set. Its manual gives 16 tiles for a complete two-terrain corner set, 16 for an edge set and 256 for a complete mixed set, and says the 47-tile blob set works with the mixed type. In our terms, "mixed" is the blob rule before the corner rule removes the redundant patterns. The 256 is `2^8`, and the 47 is what survives.

**GameMaker (current manual).** The auto tile editor offers a 47-tile template and a 16-tile template. The manual suggests the 47-tile version for side-on platformers and for top-down walls that need many connections, and the 16-tile version for top-down landscapes, since it makes nicer transitions. Rewritten in our terms, the 47 template is the blob rule, which can draw thin walls and inside corners. The 16 template gives the soft area transitions a corner set is good at.

**Godot 4 (4.x documentation).** A terrain set has one of three modes: Match Corners and Sides, Match Corners, or Match Sides. Each tile carries **peering bits**, one per neighbour direction, that say which terrain must sit there for the tile to be chosen. "Match Sides" is the edge rule with four peering bits. "Match Corners" is the corner rule. "Match Corners and Sides" is the blob rule with eight bits. Godot doesn't force you to draw all 47, but a map will show a gap wherever it needs a tile you didn't draw.

**The NES (1980s).** No autotiling here, but the same question in reverse. The 2 by 2 palette areas pushed artists to design in 16 pixel metatiles, and a metatile is a small tile made of tiles. The designer's question was still "which combinations do I need, given the memory I have?" The 256-tile limit made that question sharp.

Three tools, three names, one rule. When you meet a new engine's tile system, ask one question. Does a tile depend on the four sides, the four corners, or all eight neighbours? The answer tells you whether you're drawing 16 pieces or 47.

### Eyes-open design judgment

No rule is correct. Each one trades art time against what the map can express.

- **Blob sets cost three times the drawing.** 47 tiles is almost three times 16. Many of the 47 are mirrors or rotations of each other, so a tool that can flip tiles saves work. Top-down games with lighting from one side usually can't flip, because a mirrored tile puts the shadow on the wrong side.
- **Corner sets look softer and forbid thin features.** A corner set can't draw a path one tile wide. If your game needs narrow walls, fences or one-lane paths, you need the edge rule or the blob rule.
- **Edge sets are for lines, not areas.** Fences, pipes, roads and platforms are lines. The edge rule draws them in 16 pieces. Used for large areas, it gives square inside corners.
- **More terrains grow fast.** A corner set where each corner can be one of `n` terrains needs `n^4` tiles. Two terrains need 16. Three need 81. Four need 256. Artists avoid that with **layering**. Draw each terrain as its own 16-tile corner set with a transparent outside, and stack the layers (water under sand under grass). Three terrains then need `3 × 16 = 48` tiles, or `2 × 16 + 1 = 33` if the bottom layer is a plain fill. The cost is a draw order you have to respect. Grass can overlap sand, but sand can never overlap grass.
- **Decide the tile size with the camera.** A 16 pixel tile at 4× scale is 64 screen pixels. A 32 pixel tile at 2× is the same size on screen with four times the pixels to draw. Pick the one your team can afford to draw 47 times, and check it against week 6's rule for how much detail reads at that size.

### Check yourself on the model

1. A cell has path to the north, east and west, and grass to the south. The north-east cell is path and the north-west cell is grass. What are its edge index and blob index?
2. How many different blob tiles have exactly three edges filled? Explain the count without looking at the table.
3. A game needs grass, dirt, sand and water, and any corner can hold any of the four. How many tiles does an unlayered corner set need? How many does a layered one need if water is a plain fill at the bottom?

<details>
<summary>Answers</summary>

1. Edge index `1 + 2 + 8 = 11`. Raw blob bits are N 1, NE 2, E 4, W 64, NW 0 (grass). NE has both N and E set, so it stays. Blob index `1 + 2 + 4 + 64 = 71`.
2. There are four ways to pick three edges (leave out N, E, S or W). Each T shape has two live corners, the two that sit between filled edges, and each can be filled or empty. `4 × 2^2 = 16`.
3. Unlayered, `4^4 = 256`. Layered, three terrains need a 16-tile corner set each and water is one fill tile, so `3 × 16 + 1 = 49`.

</details>

## 3. Designing a tileset sheet

With the count settled, plan the sheet before you draw.

**Start from the fill.** Draw the tile at index 15 (edge rule) or 255 (blob rule) first, and make it pass the offset test and the seam ratio. Every other tile borrows its interior. If the fill changes later, all 47 change.

**Draw one border, then derive.** Draw a single straight border (for example index 5 or 10 in the edge rule) and an outer corner. Most other pieces are cuts and joins of these two. Keep the border's width and highlight identical on every piece, or the eye will catch the tile that is one pixel thicker.

**Lay the sheet out by index.** Put tile `k` at position `k` on the sheet, left to right and top to bottom. That way anyone can read off which tile is missing by comparing the map's index with the sheet. GameMaker, Tiled and Godot each have their own template layouts. Use the tool's template when you target that tool, and keep an index-ordered master copy for yourself.

**Keep light consistent.** If light comes from the top left, every border piece has its highlight on the top and left and its shadow on the bottom and right. This is why you can't rotate a lit border piece to make the other three. A rotated tile puts light on the wrong side, and in a map the error repeats hundreds of times.

**Check at play scale.** Tiles are drawn zoomed in and played zoomed out. Before you call a set done, paint a test map with every index in it, view it at the game's real scale, and squint. The seam you couldn't see at 800% zoom is often obvious at 100%, and the reverse is also true.

## In-class activity (25 minutes)

Work in pairs with the paper tile kit (a sheet of 16 printed edge tiles and 47 blob tiles for a stone path, cut into squares, and a 6 by 6 grid).

1. One partner draws a path shape on the grid in pencil, with at least one plaza, one T junction and one dead end.
2. The other partner computes the edge index of every path cell and places the matching edge tile. Photograph the result.
3. Swap roles. Compute blob indices for the same map and place blob tiles. Photograph again.
4. Circle every cell where the two photographs differ. For each circled cell, write which corner neighbour caused the difference.
5. Count how many distinct tiles each version used.

Expected output: two photographs, a list of the circled cells with their reasons, and the two counts. The lecture's plaza map uses only 8 of the 47 blob tiles, and your maps will likely use a minority too. Raise that in discussion. A single level rarely needs every tile, but you can't know in advance which ones a designer's next map will need.

## Common misconceptions

- **"A blob tileset needs 256 tiles."** 256 is the number of raw neighbour patterns. After the corner rule, 47 of them draw differently.
- **"If the edges match, the tile is seamless."** Matching edge pixels is necessary but not sufficient. A tile can join its copies perfectly and still show a grid because of one bright detail or a lighting gradient. Test the seam ratio and look at a 5 by 5 repeat at play scale.
- **"Corner sets and edge sets are the same because both have 16 tiles."** They answer different questions. An edge set can draw a one-tile-wide path. A corner set can't, but it gives rounded area transitions.
- **"I can rotate one border tile to make the others."** Only if the tile has no directional light. Most game tiles do.

## Check yourself

1. A 16 by 16 tile has `d_in = 6` and `d_wrap = 15`. Does it pass the course's seam threshold? What would you look for first to fix it?
2. On the NES, a screen of background is 32 by 30 tiles. How many bytes does the tile grid take, and how many bytes would the same screen take as a unique picture at 2 bits per pixel? What is the ratio?
3. In the edge rule, which indices are straight pieces, and which are dead ends?
4. A designer wants roads (thin lines) that cross grass areas with soft shores against water. Which tile rule would you use for each, and why?
5. A map picks among 3 variants of a fill tile at random. On a row of 20 fill tiles, how many neighbouring pairs would you expect to be identical?

<details>
<summary>Answers</summary>

1. `15 / 6 = 2.5`, above 1.5, so it fails. Look for a light-to-dark gradient across the tile first, since a gradient always breaks at the wrap. Then look for detail that stops at one edge and doesn't come back on the other.
2. `32 × 30 = 960` bytes of grid. `256 × 240 × 2 / 8 = 15,360` bytes for a unique picture. The ratio is 16 to 1, before counting the shared 4,096 bytes of tile images that every screen reuses.
3. Straights have two opposite edges, `N + S = 5` and `E + W = 10`. Dead ends have one edge, indices 1, 2, 4 and 8.
4. Roads with the edge rule, because only the edge rule (or blob) can draw a line one tile wide, and roads don't need filled inside corners. Shores with a corner set, because it gives rounded transitions between large areas.
5. There are 19 neighbouring pairs, and each matches with probability `1/3`, so about 6.3 pairs.

</details>

## Lab / assignment hook

[Lab 07, autotiler and seamless tile](../labs/lab07.md). You write the edge and blob index functions against provided tests, measure the seam ratio of your own fill tile with a provided script, and draw a 16-tile edge set for a path. Deliverable: passing tests, the tile sheet PNG, and a 250-word note on which tiles your test map never used.

## Sources

- NESdev Wiki, "PPU nametables", "PPU pattern tables" and "PPU attribute tables" (NES hardware, 1983-1985 release era). 32 by 30 grid of 8 by 8 tiles, 960 bytes plus a 64-byte attribute table per nametable; two pattern tables of 256 tiles at 16 bytes and 2 bits per pixel; one palette choice per 16 by 16 pixel area. https://www.nesdev.org/wiki/PPU_nametables
- Tiled documentation, "Using Terrains" (Tiled 1.5 and later, stable edition read September 2026). Corner, Edge and Mixed sets; 16, 16 and 256 tiles for complete two-terrain sets; the 47-tile blob set with the mixed type. https://doc.mapeditor.org/en/stable/manual/terrain/
- GameMaker Manual, "Auto Tiles" (monthly release manual, read September 2026). 47-tile and 16-tile templates and the suggested uses of each. https://manual.gamemaker.io/monthly/en/The_Asset_Editors/Tile_Set_Editors/Auto_Tiles.htm
- Godot Engine documentation, "Using TileSets" (Godot 4.7 stable docs). Terrain modes Match Corners and Sides, Match Corners, Match Sides; peering bits. https://docs.godotengine.org/en/stable/tutorials/2d/using_tilesets.html
- Solarski, C. (2012). *Drawing Basics and Video Game Art*. Watson-Guptill. Course reading for value and form inside tiles.
- The seam ratio and its 1.5 threshold are this course's teaching model, not a published metric.

## Interactive spec: examples/w07-autotile.html

**Purpose.** Show that 256 neighbour patterns collapse to 47 tiles because a corner only matters between two filled edges, and that the edge rule can't draw inside corners.

**Layout.** Two linked views side by side on desktop, stacked on mobile (map on top).

- **Left: map.** A 10 by 8 grid of cells (grass or path). Click or tap toggles a cell. Keyboard: arrow keys move a visible focus ring, Space or Enter toggles. Each path cell is drawn procedurally with shapes (no bitmaps): a light stone fill, darker grass around, and a 2 px border drawn on each side whose neighbour is grass. In blob mode, draw a small grass notch (a quarter circle of radius 25% of the cell) at each inside corner where the two edges are path and the diagonal is grass. In edge mode, never draw notches. In corner mode, use a dual grid. The painted cells become corner samples, and the displayed tiles sit on a second grid offset by half a cell, so each displayed tile covers the meeting point of four painted cells and takes those four as its corner values. Draw the tile with rounded path areas at its path corners, so neighbouring tiles join into soft blobs.
- A toggle "show indices" prints the index in each path cell (edge mode 0-15, blob mode the 0-255 value after the corner rule, corner mode 0-15 using NW=1, NE=2, SE=4, SW=8).
- **Right: tileset.** A grid of every tile in the current rule (16 or 47), each drawn with the same procedural renderer, in ascending index order, labelled with its index. Tiles used by the map are highlighted with the accent color and a count badge. Above it, a counter: "Using U of 47 tiles" (or "of 16").
- **Below the tileset:** a line of text for the hovered or focused cell, for example "Cell (2,2): raw 8-neighbour pattern 247 → after corner rule 215". This is where the student sees raw patterns collapse.

**Controls.** Segmented control for the rule: Edge (16), Blob (47), Corner (16). Buttons: Clear, Presets ("Plaza and path", "Plus sign", "Diagonal touch", "Random 40%" with a fixed seed of 7). A "show indices" checkbox.

**Formulas.** Edge index `1·N + 2·E + 4·S + 8·W`. Raw blob `1·N + 2·NE + 4·E + 8·SE + 16·S + 32·SW + 64·W + 128·NW`. Corner rule: clear bit 2 unless bits 1 and 4 are set; clear 8 unless 4 and 16; clear 32 unless 16 and 64; clear 128 unless 64 and 1. Cells outside the map count as grass. The 47 blob values, sorted, must be generated by applying the corner rule to 0-255 and taking the distinct results.

**Test values.** The "Plaza and path" preset places the lecture's 5 by 5 map in the top-left of the grid. Required readings: cell (1,1) edge 6 / blob 28; (1,2) 14/124; (1,3) 12/112; (2,1) 3/7; (2,2) 15/215; (2,3) 9/193; (3,2) 5/17; (4,2) 1/1. Tiles used in blob mode for that preset: 8 of 47. The "Plus sign" preset (centre plus its 4 edge neighbours only): centre edge 15, blob 85. A lone cell: edge 0, blob 0. A full 3 by 3 block: centre blob 255; top-left corner cell blob 28.

**Insight to make obvious.** In the "Diagonal touch" preset (a 3 by 3 block with one extra cell touching its bottom-right corner diagonally), the status line shows the raw pattern of the block's corner cell changing while the reduced index and drawn tile stay the same. Toggle one of the two cells between them and the tile changes.

**Accessibility and style.** Use `templates/interactive-tokens.css` tokens inline. Path versus grass must differ in lightness, not hue alone. Honour `prefers-reduced-motion` (no tile animation) and `prefers-color-scheme`.
