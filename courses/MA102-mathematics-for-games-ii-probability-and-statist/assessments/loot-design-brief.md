# MA102 · Loot design brief

**Weight:** 20% of the course grade.
**Work:** individual.
**Runs:** week 9 to week 15. Final submission and presentation in week 15.
**Builds on:** [Lab 09](../labs/lab09.md) (your two-tier table), [Lab 10](../labs/lab10.md) (pity rules), [Lab 11](../labs/lab11.md) (simulation), [Lab 13](../labs/lab13.md) (reporting rates) and [Lab 14](../labs/lab14.md) (test plan).

## The task

You are the systems designer for a raid boss's loot. Design the full loot system, prove with exact math and simulation that it meets the producer's targets, control the worst-case waits on purpose, plan how you will measure it after launch, and explain it to players in plain words.

This project pulls the course together. A strong submission uses weighted tables (week 9), the complement rule and geometric waits (weeks 3 and 7), expected value and variance (weeks 4 and 5), bad-luck protection (week 10), Monte Carlo verification (week 11), sampling and confidence (week 13), and an A/B test plan (week 14).

## The producer's brief

> **The Ashen Sovereign.** A raid boss killed at most once per week per character. Loot is personal: each character gets their own rolls. The loot table is rolled **2 times per kill**. About 40,000 characters kill the boss every week.
>
> | Reward | Job | Target |
> |---|---|---|
> | Raid tokens | Income | 3 per kill, always, outside the weighted table |
> | Gold | Income | Expected 120 gold per kill from the table, within ±5 |
> | Tier armour piece | Progression | 95% of characters have at least one within 12 kills |
> | Raid weapon | Progression | 95% of characters have it within 30 kills, **and no character ever waits more than 40 kills** |
> | Mount | Trophy | Median character gets it around kill 150 (within ±10) |
>
> **Live event.** For four weeks each year, a Festival cloak drops with a per-kill chance of 10%, and expected gold per kill doubles. Armour and weapon chances are protected and must not move by more than 0.01 percentage points. The mount must stay inside its target.
>
> **Open question.** I have not decided whether the mount needs bad-luck protection. Tell me, with numbers, and tell me what it would cost.

Lab 09 covered the first five rows without the 40-kill cap. The cap, the mount decision, the verification, the economy numbers and the measurement plan are new.

## Deliverables

1. **Design document** (`loot-<name>.pdf`), at most 2,500 words plus tables and up to five figures. Required sections:
   1. *Targets to chances.* Each target converted to a per-kill and a per-roll chance, with the formula used.
   2. *The table.* Two tiers at least, all weights, every overall probability, and which entry absorbs future changes.
   3. *Bad-luck protection.* The rule for the weapon (and the mount, if you protect it), its parameters, its exact expected wait, median, 95th percentile and the share of characters who reach the cap.
   4. *Verification.* A Monte Carlo simulation of 10,000 or more characters that checks every target, each estimate with its 95% margin, plus the validation case you ran first.
   5. *Economy and feel.* Expected gold per kill and its standard deviation, weekly gold entering the economy for 40,000 characters, and the dry-player counts at 12, 30, 52 and 150 kills for each progression and trophy item.
   6. *Live event.* Before-and-after weights and probabilities, showing the protected items unchanged.
   7. *Measurement plan.* What a small playtest can tell you (discovery) and what needs telemetry (rates), with the sample size needed to confirm the weapon's per-kill rate to ±20% of itself. Then the A/B test plan from Lab 14 step 5 for one parameter of this system.
   8. *Player-facing text.* The odds page you would publish (at most 150 words), consistent with your computed numbers.
2. **Workbook or notebook** that regenerates every number in the document, with seeds.
3. **Presentation** in week 15: 5 minutes plus 3 minutes of questions. Show your table, one figure that shows the effect of your bad-luck protection, and your mount decision.

## Milestones

| When | Milestone | What you submit | Points |
|---|---|---|---|
| End of week 10 | M1, table draft | One page. Lab 09 table revised for this brief: per-kill and per-roll chances, weights, gold value, and a check that each lab 09 target is met | 3 |
| End of week 12 | M2, protection and first simulation | One page plus notebook. Your weapon cap rule with exact statistics, a validated simulation of the weapon wait, and your first view on the mount | 4 |
| End of week 14 | M3, measurement plan and peer review | Your test plan (Lab 14 step 5) and a full draft. You review one classmate's draft with the checklist the instructor provides | 3 |
| Week 15 | Final | Document, notebook, presentation | 90 |

Milestones are marked for completion and effort. Their main value is the written feedback you get on each one.

## Rubric

100 points: 10 from the milestones and 90 from the final submission.

| Criterion | Points | Excellent | Good | Adequate | Weak |
|---|---|---|---|---|---|
| Targets and table | 20 | **18 to 20.** Every target converted correctly, including the two-roll adjustment. Weights are integers and rounded in the direction that keeps each promise. Every probability recomputes. Absorbing entry named | **14 to 17.** All targets met, one conversion or rounding slip that does not break a target | **10 to 13.** Most targets met, or the two-roll adjustment ignored | **0 to 9.** Several targets missed or numbers do not recompute |
| Bad-luck protection | 20 | **18 to 20.** The 40-kill cap is met by a stated rule. Expected wait, median, 95th percentile and share reaching the cap computed exactly and matched by simulation. Mount decision argued from dry-player counts, with its cost in rarity and stored state | **14 to 17.** Rule correct and analysed, mount decision present but thinly argued | **10 to 13.** Rule meets the cap but its statistics are incomplete or only simulated | **0 to 9.** Cap not met, or rule stated without analysis |
| Verification | 15 | **14 to 15.** Validation case run first and covered. Every target checked by simulation with a 95% margin. Differences between exact and simulated values explained | **11 to 13.** Simulation checks all targets, margins on most | **7 to 10.** Simulation runs, margins missing or no validation | **0 to 6.** No working simulation |
| Economy, feel and live event | 10 | **9 to 10.** Gold mean and SD per kill, weekly injection, dry-player counts at all four checkpoints. Event applied with protected items unchanged to 0.01 points and the mount in range | **7 to 8.** One of these parts incomplete | **5 to 6.** Event moves a protected item slightly, or economy numbers missing | **0 to 4.** Missing |
| Measurement plan | 10 | **9 to 10.** Discovery versus rate measurement clearly separated. Sample size for the weapon rate correct. Test plan complete (hypothesis, metric, baseline, minimum effect, α, power, n, duration, unit of randomization, one online-game threat with a mitigation) | **7 to 8.** Plan complete, one sizing error | **5 to 6.** Plan present but unsized or generic | **0 to 4.** Missing |
| Judgment and player communication | 10 | **9 to 10.** Each major choice names what it gives up. Odds page is honest, matches the numbers and tells players about the cap | **7 to 8.** Trade-offs named for most choices, odds page mostly consistent | **5 to 6.** Choices listed without trade-offs, or the odds page contradicts a computed number | **0 to 4.** Missing |
| Presentation | 5 | **5.** On time, one clear figure, answers questions with numbers | **4.** Clear, slightly over time or one vague answer | **3.** Hard to follow in places | **0 to 2.** Missing or unprepared |
| Milestones | 10 | M1 3, M2 4, M3 3, awarded for complete, on-time work with a real attempt at every part | | | |

## Reference numbers for self-checking

These follow from the brief and the lecture formulas. They are not a full answer.

- Weapon without protection: 95% within 30 kills needs a per-kill chance of `1 − 0.05^(1/30) ≈ 9.5%`. At that rate `0.905^40 ≈ 1.8%` of characters would still be dry after 40 kills, about 740 characters. That is why the cap needs a rule, not a luckier rate.
- Mount: a median of 150 kills means about `1 − 0.5^(1/150) ≈ 0.46%` per kill. Without protection, about 30% of weekly characters would still be dry after 260 kills (five years). Your mount decision should start from that number.

## Rules

- **Late work** loses 10 points per day on the final submission, up to three days. Presentations are not rescheduled except for documented illness.
- **Reuse.** You are expected to reuse your own lab 09, 10, 11 and 14 work. Say where.
- **Collaboration.** Discuss ideas freely. The document, workbook and presentation are your own. Peer review comments at M3 are allowed and encouraged; name your reviewer.
