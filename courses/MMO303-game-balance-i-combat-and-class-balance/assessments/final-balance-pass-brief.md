# MMO303 · Final balance pass brief

**Weight:** 40% of the course grade.
**Week:** 15 (presentations and viva), with milestones in weeks 13 and 14.
**Work mode:** individual.
**Tools:** your [combat simulator](simulator-brief.md) (M3 version), your Lab 03 calculator and your Lab 10 equilibrium solver.

## The job

You are the balance designer for a fictional MMO about to ship four damage classes. The release candidate below fails in both PvE and PvP. Change as few numbers as you can so that the roster meets written targets, prove it with simulation evidence, and publish the changes as patch notes a player can read correctly.

This is the course in one task. Week 1 gives you the targets, weeks 2 and 3 the mitigation and time-to-kill math, weeks 9 and 10 the duel meta, weeks 12 and 13 the simulator and its error bars, and week 14 the notes.

## The release candidate

All classes act every 1.5 seconds starting at `t = 0`, so a 60-second fight has 40 actions. Crits deal 2× damage. `K = 100` for both armor and magic resistance (MR).

| Class | Base hit | Crit chance | Special rule | HP | Armor | MR | Damage type | Range |
|---|---|---|---|---|---|---|---|---|
| Duelist | 100 | 25% | none | 1,200 | 60 | 20 | physical | melee |
| Marksman | 110 | 10% | none | 1,000 | 30 | 30 | physical | ranged |
| Berserker | 95 | 15% | Frenzy | 1,400 | 70 | 10 | physical | melee |
| Ritualist | 70 | 20% | Rite | 900 | 20 | 60 | magic | ranged |

**Frenzy.** After each Berserker hit, roll crit first, then a 20% chance to trigger Frenzy if its internal cooldown is ready. Frenzy adds 30% damage to actions that start less than 6 seconds after the trigger, which is the next three actions. It cannot trigger again for 10 seconds after it triggers. The triggering hit does not benefit.

**Rite.** Each Ritualist Hit grants one charge. When the Ritualist has 4 charges at the start of an action, it casts Rite instead: 300 base damage, can crit, consumes all charges and grants none.

**Fight styles.**

- `S60`: single target, stationary, 60 s.
- `S300`: single target, stationary, 300 s.
- `M300`: single target, 300 s, with movement. Each melee action has a 15% chance to be lost (no damage, no crit roll, no proc, no charge). Ranged classes lose nothing.
- `Duel`: two classes attack each other from full health, acting at the same moments. Physical damage is multiplied by `100 / (100 + armor)`, magic by `100 / (100 + MR)`. The first to reach 0 HP loses. A double death in the same step is a draw worth half a win. No movement, no healing.

The instructor releases this roster as [`final-roster.yaml`](final-roster.yaml) in week 13. If anything in the file disagrees with this brief, the brief wins. Report it.

## Targets

These are the studio's targets. You may add your own in the targets document, but you may not weaken these.

| Property | Metric | Threshold |
|---|---|---|
| PvE viability | Mean DPS in `S60` and `S300`, relative to the four-class average in that style | every class within ±3%, and its 95% interval inside the band |
| PvE viability with movement | Mean DPS in `M300`, relative to the four-class average | every class within ±10% |
| PvP fairness | Duel win rate for each of the six pairs, at least 2,000 duels per pair | no class wins all three of its duels, and no class loses all three |
| PvP diversity | Equilibrium of the margin payoff matrix, margin `2w − 1` (weeks 9 and 10) | at least three classes in the support, each at 15% or more, and `N_eff` of the equilibrium mix at least 2.5 |
| Change budget | Count of numbers changed in the roster | at most 8, and no class's `S300` DPS moved by more than 15% from the release candidate |

A number counts as changed once however far you move it. Special-rule numbers (Frenzy's 20%, 30%, 6 s, 10 s, Rite's 300 and 4 charges) count like any other. You may not add new mechanics.

Hint, not a requirement. Among physical attackers of equal DPS, the duel winner is the one with more physical EHP, so the three physical classes are ordered transitively. Only the damage-type difference can create a cycle. Work out which cycle you want on paper before you touch the simulator.

## Deliverables

Submit one repository or zip with these files.

1. **`targets.md`** (at most one page). The five targets above in the week 1 format (property, metric, population, threshold, minimum sample), any targets you add, and a rule for which target wins when two conflict.
2. **`evidence/`**. Every simulated table as CSV, with seed, command and simulator version in the file header.
   - Baseline: `S60`, `S300` and `M300` matrices and the duel matrix for the release candidate.
   - Final: the same four tables after your changes.
   - The payoff matrix, dominance check and equilibrium solution for baseline and final, with the payoff proof (every supported class earns the game value).
   - A common-random-numbers comparison for each changed class, giving the change in `S300` DPS with its 95% interval.
3. **`changes.md`**. One row per changed number: old value, new value, the reason, the prediction you wrote before simulating (a `δ_total` from damage shares, or a TTK or EHP calculation for duels), and the simulated result. Predictions written after the fact score zero on that criterion, so commit them first and keep the history.
4. **`patch-notes.md`**. One entry per changed class following the week 14 checklist (target, old ⇒ new, context, intended effect with simulated total and interval, what did not change). Flag any hits-to-kill breakpoint against the 900 to 1,400 HP range of the roster.
5. **`report.md`** (1,500 to 2,500 words). Diagnosis of the release candidate with numbers, the plan, what worked and what did not, and three risks the simulator cannot see (player skill, sticky class choice, group play, or others). End with one paragraph on what you would watch in live telemetry during the first two weeks.
6. **Slides** for a 10-minute presentation.

## Milestones

| Week | Milestone | Share of this 40% |
|---|---|---|
| 13 | M1: `targets.md` draft and the baseline evidence tables, submitted at the end of week 13. Feedback within three days. | 5% |
| 14 | M2: [Lab 14](../labs/lab14.md), patch notes from simulation evidence, scored with its rubric. This is practice on the Lab 13 roster and the model for the final notes. | 15% |
| 15 | M3: full submission, due 48 hours before the presentation session. | 60% |
| 15 | M4: 10-minute presentation and 10-minute viva. | 20% |

## Presentation and viva

The presentation shows the baseline problems, your changes, the final evidence and your patch notes. Keep numbers on screen with their intervals.

In the viva, an examiner changes one number in your final roster and asks you to predict the effect on one target by hand before running the simulator. Questions come from the question bank, weeks 3, 9, 10, 13 and 14, with new numbers. You will also be asked to defend one change against the alternative you rejected.

## Rubric for M3 and M4

M3 is scored out of 100, M4 out of 100. The marker picks the band that fits best within each criterion.

**M3: submission**

| Criterion | Points | Excellent | Good | Weak | Missing |
|---|---|---|---|---|---|
| Targets met | 25 | 22-25: every target met with intervals shown, within the change budget | 15-21: all targets met but one only at the point estimate, or budget met with no slack | 6-14: one target missed with a clear argument why it cannot be met together with another | 0-5: several targets missed, or budget exceeded |
| Evidence quality | 20 | 18-20: every table seeded and reproducible, CRN used for each change, equilibrium proof included | 12-17: reproducible, one table missing an interval or seed | 5-11: tables present but several cannot be reproduced | 0-4: point estimates only |
| Prediction before simulation | 15 | 13-15: every change predicted first, predictions within about 1 point of simulation or the gap explained by state, procs or breakpoints | 8-12: most changes predicted, gaps partly explained | 3-7: predictions thin or clearly written after the fact | 0-2: none |
| Diagnosis and design reasoning | 15 | 13-15: baseline problems named with numbers and mechanisms, changes target the mechanism (EHP, damage type, proc) rather than flat damage everywhere | 8-12: diagnosis correct, some changes blunt | 3-7: diagnosis partly unsupported | 0-2: missing |
| Patch notes | 15 | 13-15: all five checklist parts on every entry, units unambiguous, breakpoints flagged, audience named | 8-12: one part missing on some entries, or one ambiguous percent | 3-7: numbers only | 0-2: missing |
| Report and risks | 10 | 9-10: three concrete risks the simulator cannot see, telemetry plan with named metrics | 6-8: risks generic or telemetry plan vague | 2-5: short or unfocused | 0-1: missing |
| **Total** | **100** | | | | |

**M4: presentation and viva**

| Criterion | Points | Excellent | Good | Weak | Missing |
|---|---|---|---|---|---|
| Presentation clarity | 30 | 26-30: fits 10 minutes, every claim has a number and interval on screen | 18-25: clear, a few unsupported claims or slight overrun | 8-17: hard to follow or mostly text | 0-7: not given |
| Hand prediction in the viva | 40 | 35-40: correct model, prediction within the simulator's interval | 24-34: correct model, arithmetic slip | 10-23: needs prompting to choose the model | 0-9: cannot predict |
| Defending a change | 30 | 26-30: names the rejected alternative and why, with numbers | 18-25: defends the change, alternative vague | 8-17: restates the change | 0-7: cannot defend |
| **Total** | **100** | | | | |

## Rules

- Your simulator must be your M3 simulator, with any bug fixes listed in the report. If you use the instructor's reference core, say so.
- Every number in the notes and report must trace to a file in `evidence/`.
- Late M3 submissions lose 10% per day and cannot be presented at the showcase; you present in a make-up slot instead.

<details>
<summary>Instructor check values for the release candidate</summary>

Computed with an independent reference simulator following the rules above, 20,000 fights per cell. Student values should agree within their intervals.

- `S300` mean DPS: Duelist 83.3, Marksman 80.7, Berserker 78.8, Ritualist 92.8. Average 83.9. Relative: −0.7%, −3.8%, −6.1%, +10.6%. `S60` means are the same to one decimal, with wider single-fight spread.
- `M300` mean DPS: Duelist 70.9, Marksman 80.7, Berserker 66.6, Ritualist 92.8. Average 77.7. Relative: −8.8%, +3.8%, −14.3%, +19.4%.
- Duel win rates (row beats column): Duelist over Marksman about 1.00, Berserker over Duelist about 0.88, Duelist over Ritualist about 0.93, Berserker over Marksman about 1.00, Marksman over Ritualist about 0.86, Berserker over Ritualist about 0.89.
- The Berserker wins all three duels and the Ritualist loses all three. The equilibrium is pure Berserker. The Ritualist is the strongest PvE class and the weakest PvP class, which is the tension students must resolve.
- Duels are close to deterministic because each lasts only about 10 to 35 actions and crits are the only randomness, so small changes flip matchups from near 0 to near 1. Students who aim for 50/50 matchups everywhere will struggle. A cycle through the Ritualist is the intended route. One verified solution uses seven changes. Base hits Marksman 110 ⇒ 113.6, Berserker 95 ⇒ 100.3 and Ritualist 70 ⇒ 56.1 bring every class within 0.6% in `S300` and within 9% in `M300`. Then Ritualist armor 20 ⇒ 110, Duelist MR 20 ⇒ 60, Duelist armor 60 ⇒ 85 and Marksman MR 30 ⇒ 95 give duel win rates of about Duelist over Marksman 1.00, Berserker over Duelist 0.66, Duelist over Ritualist 0.70, Berserker over Marksman 1.00, Marksman over Ritualist 0.69 and Ritualist over Berserker 0.80 (3,000 duels per pair). The equilibrium is Duelist 45%, Berserker 30%, Ritualist 24%, Marksman 0%, with `N_eff` 2.8. A first attempt with smaller EHP margins (Ritualist armor 75) left the Berserker beating the Ritualist 68% of the time, because the Rite burst and Frenzy make close matchups noisy. Students should expect to iterate.

</details>
