# UX201 · Lab 10: HUD glance audit

Assigned in week 10 ([lecture](../lectures/w10-hud-and-information-design.md)). Due at the start of week 11. Pairs allowed; each pair submits one report.

## Objective

Price the HUD of a shipped game in look-away time, check the model's glance counts against real play, and propose a redesign whose saving you can predict. The point is to find out which of the three levers (distance θ, checks per minute `f`, and whether the element can be read without a look) moves the result for your game, and by how much.

## Starter materials

Everything is in [`lab10-starter/`](lab10-starter/) and this file.

**1. `hud_glance.py`.** A dependency-free Python script (run it with `.venv/bin/python` or any Python 3). It reads a CSV of HUD elements and prints θ, time per check `T` and look-away share `E` for three screen setups (24-inch PC at 60 cm, 55-inch TV at 250 cm, 7-inch handheld at 35 cm). The model constants (`L = 200 ms`, `F = 250 ms`, `θ_f = 2.5°`, saccade `20 + 2.5θ` ms) sit at the top of the file. Edit `SETUPS` to add the screen you actually test on.

**2. `hud_elements.csv`.** An example input with five elements of an invented action game. Columns: `element`, `x_frac`, `y_frac` (element centre as a fraction of screen width and height from the top-left corner) and `checks_per_min`. Run the script on it first. The "health (corner)" row should give 23.8° and 27.0% on the PC setup, matching the lecture.

**3. Inventory template** (copy into your report).

| Element | Grid cell (non-diegetic, diegetic, spatial, meta) | x_frac | y_frac | Checks/min (estimated) | Checks/min (observed) | Urgency (H/M/L) | Resolution needed | Readable in periphery? |
|---|---|---|---|---|---|---|---|---|

**4. Glance-count sheet** (one per participant).

| Participant | Setup (screen, distance) | Segment (start and end time) | Element | Glances counted | Minutes of play | Glances per minute |
|---|---|---|---|---|---|---|

## Steps

1. **Pick a game and a tense segment.** Choose a shipped game with a combat or racing HUD, and one repeatable segment of 2-4 minutes (a boss, a match, a race). Write down the start and end state.
2. **Build the inventory.** Take a screenshot at 1920 × 1080 or larger. List every HUD element, place it in the Fagerholt and Lorentzon grid, and measure its centre as `x_frac`, `y_frac` in an image editor. Estimate checks per minute for each.
3. **Run the model.** Enter your elements in a CSV and run `hud_glance.py`. Add a setup that matches where you will test (measure the screen diagonal and the eye-to-screen distance with a tape).
4. **Observe real glances.** Record three participants playing the segment. Use a webcam above the screen pointed at the player's face, or a phone on a stand, synchronised with a screen capture. Count glances toward each of the top three elements (a clear eye movement toward the element and back). Compute observed checks per minute. If you have access to an eye tracker ([week 13](../lectures/w13-biometrics-and-eye-tracking.md)), use it and say so.
5. **Compare.** Put estimated and observed `f` side by side for the top three elements. Recompute `E` with observed `f`. Where they differ by more than a factor of two, explain why from the recording.
6. **Redesign.** Propose one change that attacks `f` (show on change, peripheral encoding, sound) and one that attacks θ (move or resize). Predict `E` for each with the script. Name what each change costs (resolution, clutter, occlusion, immersion, build time).
7. **Recommend.** Choose one change to ship and justify it in one paragraph.

## Deliverable

A PDF with a memo of at most two pages plus appendices.

- The segment, the setups tested and the inventory table.
- Script output for the current HUD and for both redesigns.
- The estimated versus observed `f` comparison, with the explanation of the largest gap.
- The recommendation, with its predicted saving in points of look-away share and its cost.
- Appendices: screenshots with element positions marked, glance-count sheets, your CSV files.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Inventory | Every element listed, grid cells justified, positions measured, urgency and resolution thought through | Most elements, some cells or positions guessed | Partial list, no positions | 20% |
| Model use | Setups measured, θ, `T`, `E` correct, constants stated | Correct for default setups only | Calculation errors or missing | 20% |
| Observation | Three participants, glance counts per element, clear method, gap explained with evidence | Fewer participants or loose counting, gap noted | No observation | 25% |
| Redesign | One `f` and one θ change, both predicted, costs named | Two changes, weak prediction or costs | One vague change | 25% |
| Writing | Numbers first, plain, within length | Readable, some padding | Hard to follow | 10% |
