# GS101 · Lab 08: A constraint reading of a 3D game

Assigned in week 8 ([lecture](../lectures/w08-3d-and-the-genre-explosion.md)). Due at the start of week 10. This is a practice close reading, marked with feedback only, to prepare you for the first graded close reading (part of the 40% close-readings grade). Tutors return feedback within three working days, so you can use it before close reading 1 is due at the end of week 10.

## Objective

Write a 900-word close reading of one 3D game released between 1996 and 2002 that names a technical constraint with numbers, documents its traces in the game, and argues what the designers chose to do with it. The skill you are practising is the three-step constraint reading from lecture section 4: constraint, trace, choice.

## Starter materials

Everything below is included in this file.

**1. Eligible games.** Any 3D game first released between 1996 and 2002 on the PlayStation, Nintendo 64, Sega Saturn, Dreamcast, PlayStation 2 or PC. You may play it (original hardware, an official re-release or a legal emulator with a copy you own) or work from a recorded playthrough of at least 30 minutes. Name the version you used, because re-releases often change draw distance and frame rate.

**2. Trace log template (at least 12 entries).**

| # | Time in session or video (mm:ss) | Location in the game | What you see (fog, darkness, pop-in, camera turning away, corridor, loading pause, low-detail distant model) | What you think it hides or manages |
|---|---|---|---|---|
| 1 | | | | |

Describe what is on screen in words. Do not paste screenshots of the game into the deliverable; a written description with a timestamp is the evidence.

**3. Model sheet.** Use the week 8 interactive or this table.

| Variable | Your value | Why you chose it (one line) | Source or assumption |
|---|---|---|---|
| `R` (spec throughput) | | | |
| `e` (efficiency) | | | assumption |
| `f` (frame rate) | | | |
| `C` (fixed cost) | | | assumption |
| `ρ` (scene density) | | | assumption |
| `θ` (field of view) | | | |
| Result: `d` | | | model output |

Formulas: `P = R × e / f`, `P_world = P − C`, `d = √(2 × P_world / (ρ × θ_rad))`.

Known spec-sheet figures you may use, with the caveat from the lecture that they are manufacturer peak figures: PlayStation, 360,000 flat-shaded or 180,000 texture-mapped polygons per second. For other hardware, find a sourced figure yourself and cite it, or state that you are using an assumed value.

**4. Paragraph frame for the argument (optional).**

- Constraint: "On [hardware] at [frame rate], a [genre] game with [what is on screen] had roughly [number] polygons per frame for scenery under my assumptions, giving a draw distance near [d]."
- Trace: "The game shows this in [three specific traces with timestamps]."
- Choice: "The designers chose to [hide / dress up / make central] this limit, as shown by [evidence from the game or from what developers or reviewers said at the time]."
- Counter-reading: "One could argue instead that [alternative], but [reason]."

## Steps

1. Choose a game and a version. Check it with your lab instructor if it is outside the eligible range.
2. Play or watch for at least 30 minutes and fill the trace log.
3. Fill the model sheet. Mark every assumption as an assumption.
4. Find at least two contemporary sources (reviews, interviews or developer statements from within two years of release) about the game's visuals, camera or performance. Paraphrase; quote at most one short phrase per source.
5. Write the reading, following constraint, trace, choice, and ending with a counter-reading.
6. Swap drafts with a classmate. Each of you marks one sentence that claims more than the evidence supports. Revise.

## Deliverable

- The 900-word close reading (plus or minus 10%).
- The trace log and the model sheet as an appendix.
- A source list with version or era for every factual claim.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Constraint | Named with numbers, assumptions labelled, hardware and version stated | Named, but numbers vague or assumptions unlabelled | Asserted without numbers | 20% |
| Traces | Twelve or more logged traces, three used precisely in the essay with timestamps | Traces logged but used loosely | Few or no traces | 25% |
| Choice and argument | Clear claim about what the designers did with the limit, supported by the game and by contemporary sources, with a fair counter-reading | Claim present, evidence thin | "It was a hardware limit" with no reading of the choice | 35% |
| Sources and accuracy | Contemporary sources, dated, paraphrased, spec figures treated as spec figures | Some sources undated or overstated | Unsourced facts or invented quotes | 10% |
| Writing | Plain, precise, within length | Readable but padded | Hard to follow | 10% |
