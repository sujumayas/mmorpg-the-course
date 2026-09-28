# MMO301 · Lab 14: World concept and density budget

**Assigned:** week 14 ([lecture](../lectures/w14-designing-a-world-concept.md)). **Due:** start of week 15, with the world bible. **Feeds:** chapter 1 of the world design bible (40%).

## Objective

Write the one-page concept for your final world, with a sentence, pillars and seven numbered commitments, and back the density commitment with a spreadsheet that sizes the field area and plans map copies across a day. Then test the concept against a peer's critique and revise it.

## Starter materials

**1. Concept template.** Copy this into your document and fill every line. Do not add sections.

```
# <World name>
Sentence: <one sentence a stranger understands>
Pillars (3-5, each one a designer could argue against):
- ...
Commitments:
1. Who it is for: <motivations served first, second, tolerated; cite week 8 or 9 model>
2. Normal evening: <core loop with minutes>
3. What lasts: <what persists, decays (rate), resets (period)>
4. Density: P_peak = , h = , r = m, E_target = at <hour>, E_max = , A = km², copies at peak =
5. Economy: <main faucet, main sinks, market structure>
6. Conduct: <PvP rules, grief limits, operator promises>
7. Ending: <sunset trigger with a number, notice period, final content, what players keep, preservation>
```

**2. Density budget spreadsheet.** Build it in any spreadsheet tool with these cells and columns.

- Input cells: `P_peak`, `h`, `r` (m), `E_target`, reference hour for sizing, `E_max`.
- Derived cells: view area `= PI() * r^2`, field area `A = (1 - h) * P_peak * share(ref hour) * PI() * r^2 / E_target` in m² and km², side length `= SQRT(A)`.
- Hourly table, 24 rows (hours 0-23), columns: `hour`, `share` (your own daily curve; start from the lecture's eight values and interpolate linearly), `P = P_peak * share`, `field = (1 - h) * P`, `E1 = field * PI() * r^2 / A`, `copies = CEILING(E1 / E_max)`, `E_copy = E1 / copies`.
- A chart of `E1` and `E_copy` over the day, with horizontal lines at 1 and `E_max`.

**Check your sheet** with the lecture's world before you use your own numbers. With `P_peak = 3,000`, `h = 0.4`, `r = 150`, `E_target = 4` sized at 21:00, you must get `A = 31.81 km²`, `E1 = 1.00` at 03:00 and `2.40` at 12:00. Sized at 03:00 instead, `A = 7.95 km²` and with `E_max = 6` you must get 3 copies at 21:00 with `E_copy = 5.33`.

**3. The interactive** [`examples/w14-density-budget.html`](../examples/w14-density-budget.html), for exploring before you commit numbers to the sheet.

## Steps

1. **Draft (45 min).** Fill the template. Every commitment needs at least one number or checkable rule.
2. **Density budget (45 min).** Build and check the spreadsheet, then enter your world's values. Choose your own daily curve and justify it in two sentences (who plays, which time zones). Decide whether you size for peak, for trough or for a middle hour, and whether you use copies.
3. **Consistency pass (20 min).** Make sure the density commitment matches the rest. A world with a single global market has a high `h`. A world for explorers needs a low `E` somewhere. A group-content loop needs enough players in view at the trough.
4. **Peer critique (30 min, in the week 14 lab session).** Swap with an assigned partner. Apply the five tests from lecture section 4 (number, night shift, motivation, persistence, sunset) to their concept. Write one to three sentences per test, naming what breaks.
5. **Revision (30 min).** Revise your concept in response. Keep a change log of what you changed and which critique caused it. You may reject a critique if you explain why in one sentence.

## Deliverable

A single file with: the final one-page concept, the density spreadsheet (as a file plus a screenshot of the hourly chart), the peer critique you received, and the change log. The one-page concept must fit on one A4 page at 11-point text.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing (0) | Weight |
|---|---|---|---|---|
| Sentence and pillars | Clear sentence; every pillar is arguable and used later to settle a design choice | Pillars present but some are unarguable ("fun combat") | Missing or pure fiction | 15% |
| Seven commitments | All seven answered with numbers or checkable rules, consistent with each other | All present but some vague or inconsistent | Two or more missing | 25% |
| Density budget | Sheet passes the check values; own curve justified; sizing and copies choices explained with numbers | Sheet correct but choices unexplained | Sheet wrong or missing | 25% |
| Use of course models | Commitments explicitly use weeks 8-13 models (player types, persistence, shard density, sunset) | Models mentioned but not applied | No link to course models | 15% |
| Critique and revision | Specific critique given to the partner; change log shows real revisions or reasoned rejections | Generic critique or cosmetic revisions | No critique or no revision | 20% |
