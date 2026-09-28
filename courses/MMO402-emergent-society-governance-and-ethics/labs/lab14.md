# MMO402 · Lab 14: Debate case file

**Assigned:** week 14 ([lecture](../lectures/w14-debates.md)), first session. **Due:** at the start of your debate, in the week 14 second session. **Time:** 2 hours in lab plus about 3 hours of team preparation. **Feeds:** the debate (20%). The case file is submitted with your team's debate mark.

## Objective

Prepare both sides of your team's assigned motion from week 14, section 5, using the crux method. Find the weight and the score at which the decision flips, place both sides on a decision map, and prepare arguments that go to the crux instead of around it. Sides are assigned 48 hours before the debate, so the case file must work for either side.

## Starter materials

- [`lab14-starter.py`](lab14-starter.py). A standard-library Python script. It loads a criteria table, prints each option's weighted value and the gap `D`, and computes the crux weight of every criterion with `crux_weight()`. When one weight changes, the other weights keep their proportions. One function is left as a TODO, `crux_score()`.
- [`lab14-criteria.csv`](lab14-criteria.csv). A worked sample with the header `criterion,weight,restrict,free` and three rows based on the lecture's RuneScape example: `harm_prevented` (weight 0.5; restrict 8, free 4), `freedom_and_fun` (0.4; 3, 9) and `enforcement_cost` (0.1; 6, 4, where cheaper scores higher). Copy it and replace the rows with your own motion's criteria. Weights must add to 1, and higher scores must always be better.
- The interactive `examples/w14-crux-map.html` once built, for placing debaters on a two-criterion map.
- Your lab 13 memo, and the lecture of the week your motion draws on.

Check your setup before you start. `python3 lab14-starter.py lab14-criteria.csv` must print `restrict: 5.800   free: 6.000   gap D = -0.200` and crux weights 0.5238 for `harm_prevented`, 0.3793 for `freedom_and_fun` and 0.1818 for `enforcement_cost`.

## Steps

1. **Crux score (20 min).** Implement `crux_score()`. It returns the change `x` to the first option's score on one criterion that makes `D = 0` with all weights fixed. Since only that criterion's term changes, `x = −D / w_j`. Check it on the sample file.
2. **Your criteria (30 min, as a team).** Write the two options for your motion (the motion passes, the motion fails). Choose three or four criteria. Name any constraints (legal duties, protection of minors) separately, because constraints are not traded off. Agree on weights and scores as a team and record where you disagreed.
3. **Find the crux (15 min).** Run the script. Report the gap, each criterion's crux weight and crux score. Identify the one criterion whose crux lies closest to your chosen weight or score. That is where the debate will be fought.
4. **Map both sides (20 min).** Pick the two criteria that matter most and draw a decision map, by hand or with the interactive. Place your team's view and your best guess at the opposing view. Label the gap between them "fact," "value" or "both."
5. **Arguments (at home).** Write three Toulmin arguments, at least one for each side, with all six parts. At least one must attack or defend the warrant closest to the crux.
6. **Steelman and evidence (at home).** Write a steelman of each side of at most 100 words. Build an evidence log of at least six items, each with its source, the axis it answers (fact or value), and its typical flaw from lecture section 4.

## Deliverable

A case file of at most six pages, in Markdown or PDF, with:

- The criteria table, with constraints listed separately, and the script's output.
- The decision map with both sides placed and the gap labelled.
- Three Toulmin arguments laid out as tables.
- Two steelmen, one for each side.
- The evidence log.
- One paragraph, "Our crux," stating in plain words the single question on which the motion turns.
- Your completed `lab14-starter.py` and your criteria CSV.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing (0) | Weight |
|---|---|---|---|---|
| Crux analysis | `crux_score()` correct; crux weights and scores reported; the closest crux identified and stated in plain words | Crux computed but not interpreted, or code incorrect | No crux | 25% |
| Criteria and constraints | Criteria cover both sides fairly; constraints separated; team disagreements recorded | Criteria favour one side or constraints mixed in | Missing | 15% |
| Decision map | Both sides placed; gap labelled correctly as fact, value or both, with a reason | Map drawn, gap unlabelled or mislabelled | Missing | 15% |
| Toulmin arguments | Three complete arguments; at least one engages the warrant at the crux | Arguments missing parts or avoid the crux | Fewer than two | 20% |
| Steelmen | Each would be accepted by the other side as fair | One side weaker than the other | Missing | 10% |
| Evidence log | Six or more sourced items, each labelled by axis with its flaw named | Fewer items or unlabelled | Missing | 15% |

<details>
<summary>Instructor check values</summary>

- Sample file: `U(restrict) = 5.8`, `U(free) = 6.0`, `D = −0.2`.
- Crux weights: `harm_prevented` 0.5238, `freedom_and_fun` 0.3793, `enforcement_cost` 0.1818.
- `crux_score()` for restrict: `harm_prevented` +0.400 (to 8.4), `freedom_and_fun` +0.500 (to 3.5), `enforcement_cost` +2.000 (to 8.0). The harm criterion has the nearest crux in score terms, which matches the lecture's reading that the 2007 debate turned on how much harm the trade limit prevented.

</details>
