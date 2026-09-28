# MMO303 · Lab 08: Chain CC planner

**Week:** 8, crowd control and diminishing returns ([lecture](../lectures/w08-crowd-control-and-diminishing-returns.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the problem sets (30%).

## Objective

Build a tool that applies a diminishing-returns rule to a list of crowd control abilities, finds the chain that gives the most control on one target in a 60-second window, and compares three DR rules for a small arena game.

## Starter materials

- `cc-planner-template.xlsx` or `cc_planner.py` (starter Python with an empty `simulate(chain, rule)` function and a test file). Choose one.
- A 2v2 arena team with these abilities. All are invented for this lab.

| Ability | Owner | Category | Base duration | Cooldown |
|---|---|---|---|---|
| Shield Bash | Warden | stun | 5 s | 30 s |
| Hamstring Net | Warden | root | 6 s | 20 s |
| Hex | Oracle | incapacitate | 8 s | 45 s |
| Thunderclap | Oracle | stun | 3 s | 20 s |
| Hush | Oracle | silence | 4 s | 25 s |

- Three DR rules to compare:
  - Rule A: `m = (1, 0.5, 0.25, 0)`, `R = 18` s (the WoW era from the lecture).
  - Rule B: `m = (1, 0.5, 0)`, `R = 16` s.
  - Rule C: no DR at all, cooldowns only.
- The target: 24,000 EHP, heals itself for 700 HPS when not stunned or incapacitated. The 2v2 team deals 1,800 DPS combined.
- The [CC diminishing returns interactive](../examples/w08-cc-diminishing-returns.html), for checking single-category chains.

## Steps

1. **DR engine.** Implement the lecture's rule: process applications in time order, reset the step to 1 when a cast lands more than `R` seconds after the previous effect in that category ended, and multiply base duration by `m_k`.
2. **Check against the lecture.** Three chained 6 s stuns under Rule A must give 10.5 s. The 6, 4, 3 chain must give 8.75 s longest first and 6.5 s shortest first.
3. **Best chain.** For each rule, find the schedule that maximizes seconds the target spends stunned or incapacitated in the first 60 seconds, respecting cooldowns. A greedy search is fine if you justify it; brute force over orders is better.
4. **Uptime.** Report control uptime for each rule and the per-category breakdown.
5. **Time-to-kill.** Using the lecture's section 4 model, compute the target's TTK under each rule's best chain. Flag any rule where the target dies without acting.
6. **Silence check.** Hush does not stop self-healing in this model. Change the model so silence also stops healing and redo step 5 for Rule A only. Say whether Hush should share a category with anything.
7. **Recommend.** Pick a rule, or propose your own, that keeps this team's TTK above 15 seconds while leaving each ability useful.

## Deliverable

The tool (sheet or script with passing tests) and a memo of at most 300 words to the PvP lead. It must give the best chain and uptime under each rule, the TTK comparison, and your recommended rule with its uptime ceiling for a 5-second stun.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| DR engine | Reproduces all lecture test values; reset window counted from effect end | One rule detail wrong | Test values not reproduced | 25% |
| Chain search | Best chain found and shown optimal for each rule | Plausible chains, optimality not argued | Cooldowns ignored or chains invalid | 25% |
| TTK and silence analysis | Correct TTK per rule, silence variant interpreted | Computed, thin interpretation | Missing | 20% |
| Recommendation | Rule meets the 15 s target, ceiling stated, trade-off named | Rule chosen, partial numbers | No clear recommendation | 20% |
| Memo writing | Plain, numeric, within the word limit | Some vague claims | Hard to act on | 10% |
