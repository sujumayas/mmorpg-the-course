# PR401 · Week 05 — Prototype 2

**Why this matters:** Most first prototypes come back "unclear". Eight testers is enough to see what goes wrong and not enough to measure how often something goes right. Next week the greenlight panel will ask whether your load-bearing claim holds, and "it seemed promising" will not carry the vote. This week you work out how many testers a real answer costs, decide whether you can afford it, and build prototype 2 around what you can afford.

**You will be able to:**
- Tell a discovery question from a decision question, and use the right sample size rule for each.
- Compute the testers and observer hours needed to decide a rate against a threshold, with players tested in groups.
- Choose between a clean answer on one risk and partial answers on two, within a fixed budget, and justify the choice.
- Assemble a greenlight evidence table that states each load-bearing claim, its evidence level and its interval.

**Before class:** Reread [MA102 week 13, sampling and why n = 5 lies](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md), sections 2 and 4 (the Wilson interval and planning a sample size, 25 minutes). Reread [PR201 week 11](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md), the part on clustering and units (10 minutes). Bring your prototype 1 result reports, raw notes and time log.

**Interactive:** [Test size model](../examples/w05-test-size.html). Use it during section 2.

**Prerequisites from earlier courses:** [MA102 week 13](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) for the Wilson interval and `n = z² p(1 − p) / m²`, used here without re-deriving. [MA102 week 3](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) for the complement rule behind the discovery curve. [UX201 week 8](../../UX201-game-ux-and-player-psychology/lectures/w08-usability-testing-methods.md) for RITE and what five testers can and cannot show. Looking ahead, [MMO405 week 2](../../MMO405-research-methods-in-online-games/lectures/w02-quantitative-methods-overview.md) (next semester) covers units and nesting. From this course, [week 4](w04-prototype-1.md) for the risk sheet and the prototype brief.

---

## 1. What prototype 2 is for

Prototype 2 has three jobs, and a team with 45 hours can rarely do all three well.

1. **Settle what prototype 1 left unclear.** Usually the load-bearing claim with the highest exposure.
2. **Test the next risk in line.** For *Emberfall*, R2, the town storage load test.
3. **Produce evidence for the greenlight.** Numbers with intervals, not impressions.

Start by rerunning the week 4 picker with prototype 1's results. A refuted claim has changed the pitch, and its follow-up risks may outrank everything else. A supported claim frees budget. An unclear claim keeps most of its exposure, and the question becomes whether you can afford to make it clear.

Two changes to the prototype are allowed between 1 and 2. You can change the **test** (more testers, better measure) or the **design** (a new version of the loop). Try not to change both. If the rate moves after you changed both, you will not know which change moved it.

## 2. Worked example: how many testers settle the replay claim?

### The hook

In March 2000 Jakob Nielsen argued that usability tests need only about five users. His model, from a 1993 paper with Thomas Landauer, says that if a typical problem is met by 31% of users, five users find about 85% of the problems. The rule is widely quoted in game studios, often as "five testers is enough".

It is enough for what Nielsen asked: finding problems. It says nothing about measuring how often something happens. *Emberfall*'s prototype 1 ran the craft and trade loop with 8 players. Five of the eight met the kill criterion (at least two voluntary craft-and-sell cycles in session 2). The Wilson 95% interval for 5 out of 8 runs from 31% to 86%. The threshold was 50%. The interval sits on both sides of it. The team saw every major problem with the loop, and it still does not know whether the claim holds.

### The model

**Discovery** (Nielsen and Landauer). If a problem affects a share `λ` of players, the chance that at least one of `n` testers meets it is

```
P(seen) = 1 − (1 − λ)^n
```

**Decision** (MA102 week 13). To measure a rate `p` well enough that the 95% interval does not reach a threshold `t`, the interval's half-width must be smaller than the gap `|p − t|`:

```
n₀ = 1.96² × p(1 − p) / (p − t)²       testers, if each tester were independent
```

**Groups** (PR201 week 11). *Emberfall* players trade with each other, so testers in the same group are not independent. If one player sets a good price, the others' choices change. The **design effect** inflates the sample:

```
DE     = 1 + (k − 1) × ρ               k = group size, ρ = intra-group correlation
n      = n₀ × DE                        testers needed
groups = ⌈n / k⌉                        groups to recruit
hours  = groups × s × o                 observer hours
```

- `p` is the planning value, your best guess at the true rate. Prototype 1 gave 5 out of 8, so use `p = 0.65`.
- `t = 0.5` is the kill threshold committed in the week 4 brief.
- `ρ` measures how alike players in the same group behave. This guide uses `ρ = 0.2` as a planning assumption. You can estimate it from prototype 2's own data afterwards.
- `s` is the session hours each group needs to reach the measurement (two sessions of one hour, so `s = 2`), and `o` is observers per session.

### Numbers you can check

**Discovery.** A problem that affects 31% of players: `1 − 0.69⁵ = 84%` chance of seeing it with 5 testers, 95% with 8. A problem that affects 10% of players: 41% with 5, 57% with 8. Prototype 1's 8 testers were a fine discovery sample for common problems.

**Decision.** `n₀ = 3.8416 × 0.65 × 0.35 / 0.15² = 38.8`, so 39 independent testers. Then groups:

| Group size `k` | `DE` | Testers `n` | Groups | Observer hours (`o = 1`) | Observer hours (`o = 2`) |
|---|---|---|---|---|---|
| 1 | 1.0 | 39 | 39 | 78 | 156 |
| 4 | 1.6 | 63 (64 recruited) | 16 | 32 | 64 |
| 8 | 2.4 | 94 (96 recruited) | 12 | 24 | 48 |

Check the `k = 4` row. `DE = 1 + 3 × 0.2 = 1.6`. `38.8 × 1.6 = 62.1`, rounded up to 63 testers. That is `⌈63 / 4⌉ = 16` groups. Each group needs 2 hours of observed play, so one observer spends 32 hours.

Three things jump out.

- The `k = 1` row is not an option. A trading economy with one player tests nothing, so the independent-sample number is only a reference.
- **Bigger groups need more testers but fewer hours.** At `k = 8` you recruit 96 people, a quarter of whom may never have heard of you, but you run only 12 groups. Recruiting and observing are different costs. Which one binds depends on your team.
- **Neither fits alongside R2.** Prototype 2's budget is 45.5 hours. R2's bot test costs 30. The cheapest clean R1 test costs 24 observer hours plus building, recruiting and analysis. The team cannot settle R1 and run R2 in the same week.

### The decision

The *Emberfall* team laid out three options.

1. **Clean R1, defer R2.** Run 12 groups of 8. R2 moves to technical design in week 7 with its exposure still open. Greenlight sees a clear answer on the biggest risk and an honest gap on the second.
2. **Half R1, full R2.** Run 6 groups of 8 (48 testers, 12 observer hours) and the bot test. The R1 interval will be about `±0.19` wide in effective terms, enough to catch a disaster (a true rate near 30%) but not to separate 0.55 from 0.65.
3. **Sequential R1.** Run 6 groups, look at the interval, and stop if it already clears 0.5 or is clearly below it. Run the other 6 only if needed. This saves hours on average, but the stop rule must be written in the brief before the first group plays. Otherwise it becomes "stop when we like the answer".

The team chose option 3, with R2 cut to a 15-hour, 20-bot version (week 4, check yourself question 2). Its brief says: "After 6 groups, stop if the Wilson interval computed with the design effect lies entirely above 0.5 or entirely below 0.5. Otherwise run 6 more." Looking twice slightly raises the chance of a false clear result. The team accepted that and wrote it down. [MMO308 week 6](../../MMO308-live-operations-analytics-and-experimentation/lectures/w06-ab-testing-statistics-and-pitfalls.md) explains why repeated looks at live A/B tests need stricter rules.

The lab 05 sheet computes the table and checks the brief for a stop rule.

### The same idea elsewhere

**MA102 week 13.** Its table said a margin of ±10 points needs about 97 testers at `p = 0.5`. The same formula gives *Emberfall*'s 39, because the gap to the threshold is 15 points and `p` is 0.65, not 0.5.

**UX201 week 8, RITE.** Rapid iterative testing fixes a problem as soon as it is seen and tests again with the next few users. That is a discovery process, and it works with small samples for exactly the reason Nielsen gave. It cannot tell you a rate. Use RITE on R5, the market UI, and a sized test on R1.

**PR201 week 11.** The playtest evidence table counted party outcomes with the party, not the player, as the unit. The design effect is the same correction written as a multiplier. When `ρ = 1`, everyone in a group behaves alike, `DE = k`, and each group counts as one tester.

### Eyes-open judgment

The planning formula sets the expected half-width equal to the gap. If the true rate really is 0.65, a test of that size gives a clear result only about half the time. For about an 80% chance, multiply `n₀` by roughly 2, which puts a clean R1 out of reach for most student teams. Say that at greenlight. "We sized the test to have even odds of a clear answer" is honest and shows you understand the evidence.

If the gap is small, no affordable test will settle it. A claim whose true rate is near its threshold cannot be the thing your whole pitch rests on. Change the design so the claim does not need to be close, or change the threshold to what the pitch actually needs, with week 1's model to back it.

And `ρ = 0.2` is a guess. Estimate it after the test. If it is higher, your effective sample was smaller than planned, and the interval must be widened to match.

### Check yourself

1. Prototype 1 had come back 7 out of 8 instead of 5 out of 8. With `p = 0.85` and `t = 0.5`, how many independent testers does `n₀` give? With groups of 8 and `ρ = 0.2`, how many groups?
2. The team plays groups of 6. What are `DE`, `n`, groups and observer hours with one observer and `s = 2`?

<details><summary>Answers</summary>

1. `n₀ = 3.8416 × 0.85 × 0.15 / 0.35² = 4.0`, so about 4 testers. With `DE = 2.4`, `n = 9.6`, rounded up to 10, which is 2 groups of 8. A result far from the threshold is cheap to confirm. The formula is rough at such small `n`, so run at least 2 groups anyway.
2. `DE = 1 + 5 × 0.2 = 2.0`. `n = 38.8 × 2.0 = 77.7`, so 78 testers. `⌈78 / 6⌉ = 13` groups. Observer hours `13 × 2 × 1 = 26`.

</details>

## 3. Iterating the prototype

If prototype 1 refuted the claim or showed a design problem, prototype 2 is a new version of the design. Change the smallest thing that addresses what you saw, and keep the test the same, so the two results compare.

Record each change in the brief as "we changed X because we saw Y in prototype 1", with a pointer to the raw notes. At greenlight, a panel trusts a team that can show a result, a change, and a second result much more than a team with one good-looking session.

Keep prototype code in `prototypes/`. The week 4 rule holds. Second-version prototype code is still throwaway, and it is the version most likely to leak into production because it now looks nearly finished.

## 4. The greenlight evidence table

Week 6 is the greenlight review. MMO403 week 14 described what a panel is buying: the chance the game succeeds, and evidence that the team knows where it could fail. Bring one table:

| Claim | Load-bearing | Evidence level | Result | Interval or measure | Remaining exposure (h) |
|---|---|---|---|---|---|

- Every load-bearing claim appears, including the ones you did not test, with their exposure unchanged.
- Rates come with an interval and `n`, and grouped tests state `k` and the `ρ` used.
- The exposure column sums to the burn-down total from the lab 04 checker, rerun with prototype results.

This table is the core of the pitch assessment. A strong pitch with a weak table will not be greenlit. A modest pitch with an honest table usually will, with conditions.

## Studio session plan

This is a build week. The session plans and sizes prototype 2, then starts it.

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:25 | Prototype 1 readouts. Each team reports each item in two minutes: claim, criterion, result, one surprise | Shared results board |
| 0:25 to 0:50 | Re-pick. Teams update `risks.csv` with prototype 1 results and rerun the lab 04 checker | Prototype 2 candidates |
| 0:50 to 1:25 | Sizing. Teams size the test for their top decision question with the lab 05 sheet and the interactive, for two or three group sizes | Sizing table |
| 1:25 to 1:35 | Break | |
| 1:35 to 2:05 | The trade-off. Each team writes its options (clean, split, sequential) and chooses. Another team reads the stop rule and tries to find a result it does not cover | Prototype 2 brief with stop rule |
| 2:05 to 2:40 | Recruitment. Classes pool testers: each team offers its members as testers for two other teams' prototypes, and books group slots | Tester calendar |
| 2:40 to 3:00 | Evidence table draft. Teams fill the greenlight table with what they know today | Draft table |

## Deliverables

Due before the week 6 greenlight session, in `preproduction/week05/` in your team repository.

- **Updated risk sheet** and lab 04 checker output with prototype 1 results.
- **Sizing sheet** (`sizing.csv`) and the lab 05 checker output.
- **Prototype 2 brief** with the options considered, the choice, and the stop rule if sequential, committed before the first group plays.
- **Prototype 2 build** in `prototypes/p2/` with a README, and **result reports** with raw notes.
- **Greenlight evidence table** as described in section 4.
- **Time log** for prototype 2, and one line comparing prototype 1's actual hours against `c`.

See [lab 05](../labs/lab05.md).

## Common failure modes

- **Five testers for a rate.** The team reports "4 of 5 liked it" as a decision. Fix: say whether each question is discovery or decision, and size decisions with the formula.
- **Players as the unit when groups are.** Ninety-six testers in 12 groups are treated as 96 independent results. Fix: apply the design effect, or report per group.
- **The moving stop.** The team peeks after every group and stops when the answer looks good. Fix: one pre-written look, in the committed brief.
- **Everything changed at once.** The loop, the UI and the tester pool all changed between prototypes. Fix: change the design or the test, not both.
- **Untested claims left off the table.** The evidence table shows only what went well. Fix: every load-bearing claim appears, with its remaining exposure.

## Review checklist

The instructor checks prototype 2 and the evidence table when:

- [ ] Each prototype question is labelled discovery or decision.
- [ ] Decision questions are sized with `n₀`, a stated `ρ` and the design effect, and `check_sizing.py` prints `PASS`.
- [ ] The prototype 2 brief lists the options and the choice, and any stop rule was committed before the first group.
- [ ] Changes between prototypes are one kind at a time, each traced to a prototype 1 observation.
- [ ] Results report `n`, `k`, the interval and the verdict against the threshold.
- [ ] The evidence table includes every load-bearing claim, and its exposure column matches the rerun burn-down.
- [ ] Time logs for both prototypes are complete.

## Sources

- Nielsen, J. (18 March 2000). "Why You Only Need to Test with 5 Users." Nielsen Norman Group. The share of problems found by `n` users, `1 − (1 − L)^n`, with a typical `L` of 31%, giving about 85% for five users.
- Nielsen, J., and Landauer, T. K. (1993). "A mathematical model of the finding of usability problems." *Proceedings of ACM INTERCHI '93*, Amsterdam, 206 to 213.
- MA102 week 13 and PR201 week 11 in this repository for the Wilson interval, sample-size planning and clustered units.
- Kish, L. (1965). *Survey Sampling*. Wiley. The design effect for cluster samples, `1 + (m − 1)ρ`.
- *Emberfall*, its prototype results, the planning value `ρ = 0.2` and the session lengths are invented for teaching.

## Interactive spec

**File:** `examples/w05-test-size.html`

**The one insight the visual must make obvious:** the tester count that finds most problems (discovery) is far smaller than the count that decides a rate against a threshold, and grouping players trades testers for hours.

**Top view: two questions, one axis.** x axis testers `n` from 1 to 120 (linear). Left y axis: probability of seeing a problem `1 − (1 − λ)^n`, drawn as a rising curve for the chosen `λ`. Right y axis: the Wilson 95% interval for the planning rate `p` at effective sample `n / DE`, drawn as a shaded band around a horizontal line at `p`, with a dashed horizontal line at the threshold `t`. Mark with a vertical line the first `n` where the band no longer touches `t` (the decision `n`), and with another the `n` where the discovery curve passes 85%. Label both with their values.

**Bottom view: group size trade-off.** Bars for `k` = 2, 4, 6, 8, 10: bar height is observer hours `⌈n / k⌉ × s × o`, and a dot above each bar shows testers recruited `⌈n / k⌉ × k`, on a second axis. Highlight the bar for the selected `k`. Draw the remaining prototype budget (`B` minus other work) as a horizontal line.

**Controls.**
- Planning rate `p`: slider 0.05 to 0.95, step 0.01, default 0.65.
- Threshold `t`: slider 0.05 to 0.95, step 0.01, default 0.50.
- Problem share `λ`: slider 0.01 to 0.6, step 0.01, default 0.31.
- Group size `k`: slider 1 to 10, default 8.
- Correlation `ρ`: slider 0 to 1, step 0.05, default 0.2.
- Session hours `s`: 0.5 to 4, step 0.5, default 2. Observers `o`: 1 or 2, default 1.
- Budget `B`: 20 to 80, default 45.5; other work already committed: 0 to 60, default 15 (the small R2 test).

**Formulas.** `n₀ = 1.96² p(1 − p) / (p − t)²` (show "no finite n" when `p = t`). `DE = 1 + (k − 1)ρ`. `n = ⌈n₀ × DE⌉`. Wilson interval at effective size `m = n / DE`: centre `(p + z²/2m) / (1 + z²/m)`, half-width `z × √(p(1 − p)/m + z²/4m²) / (1 + z²/m)`, `z = 1.96`. Note that the band-exclusion `n` from the Wilson interval will differ slightly from `n₀`; show both.

**Readout.** `n₀`, `DE`, `n`, groups, testers recruited, observer hours, budget left, discovery `n` for 85%.

**Test values (defaults must reproduce these).** `n₀ = 38.8`. At `k = 4`: `DE = 1.6`, `n = 63`, 16 groups, 64 recruited, 32 observer hours. At `k = 8`: `DE = 2.4`, `n = 94`, 12 groups, 96 recruited, 24 observer hours. At `k = 6`: `DE = 2.0`, `n = 78`, 13 groups, 26 hours. Discovery at `λ = 0.31`: 84.4% at `n = 5`, 94.9% at `n = 8`; the 85% line is crossed at `n = 6` (5.1 continuous). Wilson interval for 5 of 8: 0.306 to 0.863. Setting `p = 0.85` gives `n₀ = 4.0`.

**Accessibility.** All values in the readout are live text. Sliders have visible labels and keyboard steps. Colour is never the only cue: the decision and discovery markers are also labelled in text. Respect `prefers-reduced-motion`.
