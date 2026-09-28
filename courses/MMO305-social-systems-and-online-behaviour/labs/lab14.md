# MMO305 · Lab 14: Positive-sum audit

**Week:** 14, [Designing for positive social play](../lectures/w14-designing-for-positive-social-play.md)
**Time:** one 2-hour lab session plus about 2 hours of writing
**Feeds:** the final social system design and research proposal (week 15, 50%)

## Objective

Model one social reward system from a shipped game, compute the stranger payoff `Δr`, the faucet multiplier and the free-rider limit, and propose a redesign whose costs you can put numbers on.

## Starter materials

1. **Spreadsheet skeleton.** Build it yourself from this description (any spreadsheet program).
   - Inputs in cells `B1:B7`: `S` (spawns per minute), `H` (health), `d` (damage per second per player), `t_s` (search seconds), `s` (scaling factor), `θ` (damage threshold as a fraction), and a tap cap `k` (maximum players who share credit, or a large number for no cap).
   - Column A, rows 10 to 29: `n` from 1 to 20.
   - Column B: `c = 60 / (H/d + t_s)` (same value on every row).
   - Column C, rule A: `=MIN(c, S/n)`.
   - Column D, rule B: `=MIN(S, 60 / (H/(n*d) + t_s))`.
   - Column E, rule C: `=MIN(S, 60 / (H*(1+s*(n-1))/(n*d) + t_s))`.
   - Columns F to H: `Δr` for each rule, the next row's value minus this row's.
   - Columns I to K: spot credits per minute, `MIN(n*c, S)` for rule A and `n × r(n)` for B and C.
   - Column L: a flag that is TRUE where `1/n < θ` (not every equal contributor qualifies).
2. **Check values.** With `S = 6`, `H = 1,000`, `d = 50`, `t_s = 10`, `s = 0.5`, your sheet must reproduce the lecture's table: at `n = 4`, 1.50 / 4.00 / 2.67; at `n = 6`, spot credits 6.00 / 27.00 / 16.62. Do not continue until it does.
3. **Source list.** The Warcraft Wiki "Tap" page and the Guild Wars 2 Wiki "Loot" and "Dynamic event" pages cited in the lecture, plus any official patch notes for your chosen game.

## Steps

1. **Pick a system** from a shipped game that is not one of the lecture's examples. Suitable choices include a public event system, a shared world boss, a gathering or fishing spot, a revive mechanic, a mentor or sprout programme, or a commendation system. Check with the instructor if unsure.
2. **Verify the rule.** From an official or well-maintained source, find how the game assigns credit when several players act on the same target or resource. Cite it with the game version or date. If you cannot verify a number, treat it as your assumption and label it so.
3. **Map it to the model.** Say which rule (A, B, C, a cap, or a mix) the system uses. Choose values for `S`, `H`, `d` and `t_s` and state that they are your assumptions.
4. **Compute** `r(n)`, `Δr(n)` and spot credits for `n = 1` to 20. Chart `r(n)` and mark where `Δr` changes sign.
5. **Judge the fit.** In 150 words, say what the system is for (create stories, build ties, move players through content, act as a currency faucet) and whether its sign of `Δr` serves that purpose.
6. **Redesign** with one or two changes (a cap, a threshold, a scaling factor, per-player instancing, a party-invite prompt). Recompute.
7. **Cost it.** For your redesign, give the change in faucet multiplier at `n = 6`, the change in fight length at `n = 6`, and the new free-rider limit `floor(1/θ)`. Name one social behaviour your change removes (for example, the invite etiquette that exclusive tagging creates).

## Deliverable

A spreadsheet plus a 1,000-word memo with: the verified rule and its citation, the before-and-after `r(n)` chart, the `Δr` sign table for `n = 1` to 6, the three cost numbers, and a closing paragraph stating the intended sign of `Δr` for this system in your final design proposal.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or weak (0) | Weight |
|---|---|---|---|---|
| Model correctness | Sheet reproduces the check values; formulas correct for all three rules and the cap | Minor formula errors that do not change the sign of `Δr` | Check values not reproduced | 25% |
| Verified rule | Credit rule sourced with version or date; assumptions clearly separated from facts | Source present but undated, or facts and assumptions mixed | No source | 15% |
| Judgment of fit | Names the system's purpose and argues from the sign of `Δr` | Purpose named but argument does not use `Δr` | Missing | 20% |
| Redesign and costs | Redesign changes `Δr` as intended; all three cost numbers correct; a lost behaviour named | Redesign sensible but costs incomplete | No redesign or no costs | 30% |
| Writing | Plain, precise, within length; chart labelled | Some vagueness or missing labels | Hard to follow | 10% |
