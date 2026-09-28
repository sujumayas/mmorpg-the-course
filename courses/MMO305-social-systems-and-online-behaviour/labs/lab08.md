# MMO305 · Lab 08: Plague and reservoir

**Week:** 8 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the reading responses and field observation work

## Objective

Build the reservoir SIS model from [week 8](../lectures/w08-griefing-typology-and-design-responses.md) in a spreadsheet, reproduce the lecture's tables, then plan the response to a new contagion mechanic with a limited budget. You will find out which lever, contact or reservoir, is binding in your scenario.

The model, one row per minute:

```
I(t+1) = I(t) + β × (N − I(t)) × (I(t) + C) / N − γ × I(t)
R0 = β / γ
steady state: a = β(N − C) − γN,  I* = [a + sqrt(a² + 4β²NC)] / (2β)
```

## Starter materials

- A blank spreadsheet (Google Sheets, Excel or LibreOffice Calc), or Python.
- **Sheet layout to build.** A parameter block in cells B1:B6 with labels in A1:A6: `N`, `beta`, `gamma`, `C`, `I0`, `steps`. A table starting in row 10 with columns `minute` (0 to 120), `I`, `new_infections`, `exits`. Row 10 holds minute 0 with `I = I0`. Each later row applies the update rule to the row above and clamps `I` to the range 0 to `N`.
- **Reproduction targets** (from the lecture, `N = 1,000`, `γ = 0.5`, `I0 = 10`): `β = 0.4, C = 20` gives `I(1) = 16.88`, `I(10) ≈ 50.0` and `I* = 60.5`. `β = 1.0, C = 0` gives `I(10) ≈ 311.2` and `I* = 500`.
- **The new scenario.** Your game's next raid has a boss curse, "Hexbloom", that can leave the raid on summoned companions, like Corrupted Blood. Before launch your team estimates, for a busy capital city:
  - `N = 1,500` players present, `γ = 0.4` per minute.
  - Contact `β = 0.9` in the crowded market district.
  - Reservoir `C = 30`, made of 12 infectious town NPCs, 10 companion carriers and 8 players expected to carry it on purpose.
- **Budget.** You have 10 fix points. Options and their effects:

  | Fix | Cost (points) | Effect |
  |---|---|---|
  | NPCs immune to the curse | 3 | removes 12 from `C` |
  | Companions cleanse on dismiss | 3 | removes 10 from `C` |
  | Report-and-remove for deliberate carriers | 4 | removes 6 of the 8 griefers from `C` (recall 75%) |
  | Curse cannot be cast within city limits (spreads out the market) | 4 | `β` falls by 0.3 |
  | In-town warning and "flee" portal | 2 | `β` falls by 0.15 |
  | Shorter curse duration | 3 | `γ` rises by 0.2 |
  | Free cure vendor at the city gate | 2 | `γ` rises by 0.1 |

## Steps

1. **Build and reproduce.** Build the sheet and reproduce both reproduction targets to one decimal place. Add a cell that computes `I*` with the quadratic, and check it against minute 120 of your table.
2. **Baseline.** Run the Hexbloom scenario with no fixes. Record `R0`, `I*` and the minute when `I` first exceeds 500.
3. **Single levers.** For each fix alone, record the new `R0` and `I*`. Rank the fixes by `I*` reduction per point spent.
4. **Your plan.** Choose a set of fixes costing at most 10 points. Record `R0`, `I*` and the time course. Plot your plan against the baseline on one chart.
5. **Which lever was binding?** Explain, using the steady-state map from the lecture, whether your plan works mainly by pushing `R0` below 1 or by shrinking `C`, and why the other lever alone would have failed.
6. **Griefer stress test.** Suppose the griefer estimate was wrong and 25 players carry the curse on purpose, not 8. Rerun your plan. Does it still hold? What would you change?

## Deliverable

The sheet, the comparison chart, and a memo of about 300 words to your raid team. The memo must list your chosen fixes and their cost, give `R0` and `I*` before and after, name the binding lever, and report the result of the griefer stress test.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model and reproduction | Both targets matched to one decimal; quadratic `I*` agrees with minute 120 | Targets matched, `I*` cell missing | Targets not matched | 25% |
| Single-lever ranking | Every fix evaluated, ranking by reduction per point correct | Most fixes evaluated | Missing | 20% |
| Plan within budget | Plan at most 10 points, numbers correct, chart clear | Plan valid, chart unclear | Over budget or numbers wrong | 20% |
| Binding lever | Correct regime identified with reference to `R0 = 1` and the reservoir | Regime named without the reasoning | Missing or wrong | 20% |
| Stress test and memo | Stress test run and its lesson stated in a clear memo of about 300 words | Stress test run but not interpreted | Missing | 15% |

<details>
<summary>Instructor check values</summary>

- Baseline: `R0 = 0.9 / 0.4 = 2.25`, `a = 0.9 × 1,470 − 0.4 × 1,500 = 723`, `I* ≈ 856` (about 57% of the city infected). `I` first passes 500 at minute 7.
- Removing all 30 of `C` alone (costs more than the budget anyway) still leaves `I* = 1,500 × (1 − 1/2.25) ≈ 833`. The reservoir is not binding at baseline; contact is.
- A plan that reaches `R0 < 1` must bring `β/γ` under 1. Example: city-limits rule (4) plus warning portal (2) gives `β = 0.45`; cure vendor (2) gives `γ = 0.5`, so `R0 = 0.9`. That spends 8 points and leaves 2, not enough for any reservoir fix. With `C = 30`, `I* ≈ 135`: the plague is contained but endemic, because the reservoir is now binding.
- Alternative: city-limits (4) plus shorter duration (3) plus NPC immunity (3): `β = 0.6`, `γ = 0.6`, `R0 = 1.0`, `C = 18`. `I* ≈ 156`. Students who find plans in the 130-200 range with a clear account of the regime should earn full marks.
- Stress test: with 25 deliberate carriers instead of 8, `C` rises by 17. For the first plan above, `C = 47` and `I* ≈ 179`, a third higher. Plans that bought report-and-remove are less sensitive to this error.

</details>
