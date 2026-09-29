# AR101 · Lab 13: A one-page style bible and a stranger test

**Assigned:** week 13 ([lecture](../lectures/w13-art-style-bibles.md)). **Due:** start of week 14 class. **Feeds:** the style bible assessment (20% of the course grade). This lab is your first draft of it.

## Objective

Write a short style bible for one zone of an invented MMO, prove its technical rules with numbers, make three assets that pass it, and find out whether it works by giving it to a stranger. By the end you should be able to point at every rule in your bible and say how a reviewer checks it.

This is a studio exercise, not a coding lab. You may work in pixel art, flat vector shapes, low-poly 3D or painted 2D. Pick the medium you'll use for your final portfolio piece.

## Starter materials

- **Zone brief (choose one, or propose your own to the instructor by Wednesday).**
  - *Saltmarsh Reach.* A fishing town on stilts over tidal flats. Two factions share it, the Tidewardens (keepers of the sea wall) and the Reedfolk (smugglers in the marsh).
  - *Cinder Terraces.* A mining settlement cut into a cooling lava slope. Friendly miners, hostile ash elementals.
  - *The Lantern Archive.* An underground library lit only by carried lights. Scholars and the things that eat books.
- **Rule table template.** Copy this into your document and fill one row per rule.

  | # | Chapter | Property | Target | Tolerance and scope | Method | Hard or soft | Why |
  |---|---|---|---|---|---|---|---|
  | 1 | Technical | Texel density | 128 px/m (or 16 px per tile) | ±25% (or 0 for pixel art), all props | `D = T × f × r / S` from the file | Hard | Mixed densities look pasted in |

- **Density table template.**

  | Asset | S (m or tiles) | T (px) | f | r (or scale k) | D | D / D* | Pass? |
  |---|---|---|---|---|---|---|---|

- **Audit sheet template** for the stranger test. One row per rule, columns "pass", "fail", "rule unclear", and a notes column.
- The week 13 lecture's density script (section 2), which you may adapt to check your table. It runs with `.venv/bin/python`.

Use only your own art or art you make from basic shapes. No game screenshots, characters or logos in the bible. You may name games in text as references.

## Steps

1. **Pillars (20 min).** Write three to five pillars for your zone, each as "X, not Y." Test each pair by naming one asset it would reject.
2. **Rules (60 min).** Write at least eight rules in the rule table, covering at least five chapters from the lecture (pillars, shape, silhouette, value and color, lighting, materials, technical). At least four rules must have a numeric target. At least one must be texel density. At least one must reserve a color for gameplay meaning, for example "only enemy spell areas use this red."
3. **Density table (30 min).** Plan six assets for the zone with their world sizes and texture or sprite sizes. Compute `D` for each. At least one planned asset must fail on your first draft. Fix it using `T`, `f`, `r` or (for pixel art) redrawing, and show the before and after rows.
4. **Make three assets (2 to 3 hours).** Build three of the six. At least one must be a character or creature, and at least one must be a prop. Put all three in a single lineup image at game scale on a neutral background, plus one grayscale copy of the lineup and one silhouette copy (all fills black).
5. **Stranger test (45 min in week 14 studio time, or arranged with a classmate).** Swap bibles with someone from another group. Give them the bible only. They make one asset from one of your planned rows in 45 minutes, in any medium. Then you audit their asset rule by rule on the audit sheet before you look at it in your lineup.
6. **Revise (30 min).** For every "rule unclear," rewrite the rule. For every asset that passed all rules but looks wrong in the lineup, find the property that differs and add a rule. Record each change in a short changelog at the end of the bible (version 0.1 to 0.2).

## Deliverable

One PDF or Markdown file (plus image files) containing:

- The bible, version 0.2, no longer than four pages including images. Pillars, the rule table, and at least one approved and one rejected example image, each with a one-line reason.
- The density table with before and after rows for the failing asset.
- The lineup image, its grayscale copy and its silhouette copy.
- The completed audit sheet from the stranger test and a photo or export of the stranger's asset.
- The changelog from 0.1 to 0.2 (at least three entries).

A reviewer must be able to check the deliverable without asking you anything. Every numeric rule has a method, every density row can be recomputed from its columns, and every changelog entry points to a rule number.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Checkable rules | Eight or more rules, all with property, target, scope and method; at least four numeric; hard or soft labelled with a reason | Eight rules, some missing a method or target | Mostly mood words with no targets | 25% |
| Texel density | Table correct to one decimal; a failing asset fixed with the formula and shown before and after | Table present with an arithmetic error, or no fix shown | No density rule or table | 15% |
| Assets and lineup | Three assets that pass every rule; lineup, grayscale and silhouette versions show consistent scale, value and readable shapes | Three assets with one clear rule violation the student did not catch | Fewer than three assets or no lineup | 25% |
| Stranger test | Audit completed before viewing in lineup; findings specific; each linked to a rule number | Test done, findings vague | Not done | 20% |
| Revision | Three or more changelog entries that fix real defects found in the test | Changelog present, entries cosmetic | No revision | 15% |
