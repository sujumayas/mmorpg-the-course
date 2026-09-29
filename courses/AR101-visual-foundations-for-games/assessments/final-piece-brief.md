# AR101 · Final piece brief: a readable game screen

**Weight:** 30% of the course grade.
**Assigned:** week 9. **Milestone 1:** end of week 10. **Milestone 2:** end of week 12. **Milestone 3:** end of week 14. **Final submission and crit:** week 15.
**Work mode:** individual.
**Lectures:** all fourteen, with the heaviest use of [week 3, silhouettes](../lectures/w03-silhouette-readability.md), [week 7, tilesets](../lectures/w07-tilesets-and-seamless-tiling.md), [week 9, composition](../lectures/w09-composition-and-leading-the-eye.md), [week 10, telegraphs](../lectures/w10-readability-in-chaos-vfx-and-telegraphing.md), [week 12, accessibility](../lectures/w12-accessibility-color-blindness-and-contrast.md) and [week 14, pipeline](../lectures/w14-pipeline-export-atlases-import-settings.md).
**Labs that feed it:** [02](../labs/lab02.md), [03](../labs/lab03.md), [05](../labs/lab05.md), [06](../labs/lab06.md), [07](../labs/lab07.md), [08](../labs/lab08.md), [09](../labs/lab09.md), [10](../labs/lab10.md), [11](../labs/lab11.md), [12](../labs/lab12.md), [13](../labs/lab13.md) and [14](../labs/lab14.md).

## What this component is for

This is your portfolio piece for the course, and it tests all three outcomes at once. You make one screen of an invented MMO zone as a set of game-ready assets: tiles, characters, an animation, a boss telegraph and a piece of UI, composed into a single frame a player could read in one second. Then you prove, with the course's models, that it reads: in value, in silhouette, under a pile of effects, and for players with color vision deficiency.

The zone is the one in your [style bible](style-bible-brief.md). The bible sets the rules, and the piece is the first real test of them. A piece that looks good but breaks its own bible loses marks. So does a bible rule that the piece shows to be wrong and that you did not fix.

## Medium and format

Choose one, and use the same one as your lab 13 assets.

- **Pixel art** (recommended). Internal resolution 320 × 180 or 384 × 216, shown only at integer scale with nearest-neighbour filtering. Tiles 16 × 16. One art pixel size for every layer except UI text, and any exception recorded in the bible.
- **Flat vector or painted 2D.** A 1280 × 720 frame. Tiles or modular pieces of a fixed size, with a pixels-per-tile density rule in the bible and a tolerance you state.
- **Low-poly 3D,** by agreement with your tutor at milestone 1. The tileset becomes a modular kit of at least eight pieces that snap on a grid, and the density table replaces the seam ratio for textures that tile.

## What you make

1. **A composed gameplay screen.** One frame containing the player character, at least two other characters or creatures, a pickup, an exit or objective, a HUD element, and a boss telegraph in its windup. Deliver it twice: a calm frame (no effects) and a chaos frame (at least 8 overlapping additive effects around the telegraph, made with lab 10's plate method or your own).
2. **A tileset.** A seamless fill tile, plus a complete 16-tile edge set, 16-tile corner set or 47-tile blob set for the zone's main ground transition, with a test map that uses every index.
3. **A character roster.** At least three characters or creatures that the player must tell apart, drawn to the bible's proportions and shape rules. At least one of them appears in the composed screen at gameplay size.
4. **One animation.** Either a six-to-eight-drawing action with a timing sheet (lab 08 format), or a walk or run cycle whose length satisfies `T = d / v` for a movement speed you state.
5. **One UI element.** A loot label set, an item tooltip or a unit frame, with its importance list and weight table.
6. **An export package.** Every sprite and tile exported at 1×, packed with your lab 14 packer into one or more atlases, with the atlas PNG, the placement file, the import settings table and the memory figure.
7. **A case study page.** One page, 300 to 500 words, for your portfolio. What the screen is, the three decisions you are proudest of, each with its number, and one thing you would change.

You may start from lab work. Say in the case study which assets began in which lab and what you changed. At least half of the assets in the composed screen must be made after milestone 1.

## Readability targets

These are the course's working thresholds. Your bible may set stricter ones. It may not set looser ones without a recorded exception and reason.

| Check | Target | Tool |
|---|---|---|
| Critical pairs (player, enemies, pickup, exit, telegraph against their grounds) | ΔV ≥ 20; pickup and enemies ≥ 30 | [lab 01](../labs/lab01.md) checker |
| First look in the calm frame | Focal cell on the objective you name, `H ≥ 1.5` at 8 by 5 | [lab 09](../labs/lab09.md) `focal_map.py` |
| Roster silhouettes | Every pair IoU ≤ 0.75 at full size and at the size in the screen | [lab 03](../labs/lab03.md) tool |
| Tileset | Seam ratio ≤ 1.5; no visible grid in a 5 by 5 repeat at play scale | [lab 07](../labs/lab07.md) `seam_check.py` |
| Telegraph | Contrast ≥ 20 in the calm and chaos frames; two-tone worst case stated | [lab 10](../labs/lab10.md) probe |
| Accessibility | Every critical pair ΔV ≥ 20 in typical, protan, deutan and tritan views, or a listed shape or pattern difference | [lab 12](../labs/lab12.md) audit |
| UI | Zero inversions; every step ≥ 1.5, or one weak step justified | [lab 11](../labs/lab11.md) tool |
| Pixel art | Integer scale only; sprite checker passes on every sprite | [lab 06](../labs/lab06.md) checker |
| Pipeline | Atlas side and memory within the bible's budget; gutter matches the deepest mip level you use | [lab 14](../labs/lab14.md) packer |

## Original work and references

Everything in the piece is your own work. This is a gate. A piece that breaks it is not marked until the problem is fixed, and work presented as yours when it is not is handled under the university's academic integrity policy.

- **Allowed.** Your own drawings, pixel art, paintings and models. Palettes from Lospec or similar sites if credited. Fonts under an open licence (for example the SIL Open Font License) for UI text, credited.
- **Allowed as reference, with a record.** Games, photographs and art you study for shape, value, color or composition, listed in `SOURCES.md` with the game or author, version or date, and what you took from it. A reference board is welcome in the case study if every image in it is credited and none is presented as yours.
- **Not allowed.** Tracing, painting over or copying the pixels of copyrighted art. Existing game characters, logos or locations, redrawn or not. Output from image-generation tools in place of your drawing. Assets from packs or stores.

The full rules are in the [weekly studies brief](weekly-studies-brief.md#original-work-and-references). Ask before a milestone if you are unsure.

## Milestones

| When | What you submit | Points |
|---|---|---|
| End of week 10 | **Proposal.** Zone name and three pillars. A one-paragraph screen brief (who the player is, what threatens them, what they must find). Three greyscale three-value thumbnails of the screen with the focal target in different places, each run through `focal_map.py`, and your pick. Medium choice (and 3D agreement if needed). | 3 |
| End of week 12 | **Block-in.** The screen at internal resolution in flat values, with every element placed and the calm-frame focal report passing. The zone palette (lab 05) applied. The roster as black-fill silhouettes with the IoU matrix. The fill tile with its seam ratio. | 3 |
| End of week 14 | **Near-final.** The full-color screen, the tileset, the roster and the animation, packed once with the lab 14 packer. A list of every readability target with its current number and pass or fail. | 2 |
| Week 15 | **Final submission and crit.** Everything below, and a 5-minute presentation followed by 3 minutes of questions. | 92 |

Tutors give written feedback on every milestone within a week. The milestone points are for a complete, on-time submission. The feedback is where the value is.

## Deliverables

- `screen_calm.png` and `screen_chaos.png` at internal resolution, plus 4× nearest-neighbour copies (pixel art) or the 1280 × 720 frames, and grayscale and four-up color-blind versions of the calm frame.
- `tileset.png` in index order, `fill.png`, `test_map.png` and the map as a 0/1 text grid.
- `roster.png` in color and in black fill, at full and gameplay size.
- The animation as a GIF at 4× and a sprite sheet, with its timing CSV.
- The UI element as a mockup and its blurred version, with its CSV.
- `export/`: atlas PNGs, placement files, the import settings table and the memory figure.
- `reports/`: the output of every tool in the targets table, rerunnable from the files you submit.
- `case_study.pdf`, one page.
- `SOURCES.md`.

## The crit

Week 15 runs as a crit. You have 5 minutes to show the calm frame, then the chaos frame, then the one decision you are proudest of. The panel (a tutor and two classmates) then asks 3 minutes of questions in the style of the [exam bank](exam-bank.md), using your numbers. Expect questions like "your pickup's ΔV is 22 on the moss, what happens on the sand?", "what is the worst-case contrast of your telegraph?", or "which pair in your roster would merge first if we halve the size?". Answer with the model, not with taste.

## Late work

Milestones submitted up to 48 hours late earn half their points. The final submission cannot be late without documented illness or emergency, because the crits run in week 15. With permission, work submitted up to 48 hours late is marked normally but presented in a make-up crit.

## Rubric (out of 100)

| Criterion | Excellent | Adequate | Weak or missing | Points |
|---|---|---|---|---|
| Milestones | All three complete and on time (8) | One late or incomplete (4 to 6) | Two or more missing (0 to 3) | 8 |
| Composed screen: readability | Calm frame's focal cell is the named objective with `H ≥ 1.5`; every critical pair meets its ΔV target; the screen reads in grayscale at 1× (18 to 20) | Focal point correct but `H` borderline, or one critical pair short (10 to 17) | Wrong focal point or several pairs merge (0 to 9) | 20 |
| Characters and silhouettes | Three or more characters in one roster; every pair ≤ 0.75 at both sizes; shapes follow the bible's language; readable at gameplay size (11 to 12) | All pairs below 0.80, one above 0.75, or shape language inconsistent (6 to 10) | A pair at 0.80 or more, or fewer than three characters (0 to 5) | 12 |
| Tileset | Complete set for the chosen rule, consistent border and light; fill passes the seam ratio with no visible grid; test map uses every index (11 to 12) | One or two pieces inconsistent, or the grid shows at play scale (6 to 10) | Pieces missing or seams visible (0 to 5) | 12 |
| Animation | Timing sheet sums correctly; holds placed on the key drawings for the stated weight, or `T = d / v` met to the tick; every drawing reads as a silhouette (9 to 10) | Timing correct but even or arbitrary, or one drawing muddy (5 to 8) | No timing sheet, or feet slide (0 to 4) | 10 |
| Telegraph and accessibility | Two-tone telegraph reads at 20 or more in both frames; stated worst case matches the model; every critical pair passes in all four views or has a listed shape difference (9 to 10) | Passes in one frame or fails one view with a correct diagnosis (5 to 8) | Relies on hue alone or is lost in the chaos frame (0 to 4) | 10 |
| UI element | Zero inversions, steps ≥ 1.5 or justified, category code kept, reads in the blur (6) | One inversion or weak step unjustified (3 to 5) | Hierarchy inverted (0 to 2) | 6 |
| Fit to the style bible | Every asset follows version 0.3's rules; any exception recorded with its reason; a reviewer could check this from the bible alone (9 to 10) | One or two silent violations (5 to 8) | The piece ignores the bible (0 to 4) | 10 |
| Pipeline and export | Every file at 1×, named to the bible's pattern; atlas within budget; gutter tied to a mip level; import settings match the asset type (5) | One area wrong, for example a non-integer scale or an oversized atlas (2 to 4) | No export package (0 to 1) | 5 |
| Case study and crit | Case study names three decisions with their numbers and one honest change; crit answers use the models and your own numbers (6 to 7) | Clear but generic, or crit answers rely on taste (3 to 5) | Missing, or cannot explain the work (0 to 2) | 7 |
| **Total** | | | | **100** |
