# MMO303 · Lab 07: Healer mana budget

**Week:** 7, healing throughput and mana economy ([lecture](../lectures/w07-healing-throughput-and-mana-economy.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the problem sets (30%).

## Objective

Build a spreadsheet that turns a healer's mana pool, regeneration and spell list into an efficient frontier and a sustainable-HPS curve over fight length. Use it to find a hidden enrage timer and to tune a kit so every spell earns its place.

## Starter materials

- The template in [`lab07-starter/`](lab07-starter/): one CSV per tab. Import each as a sheet in any spreadsheet tool.
  - [`Spells.csv`](lab07-starter/Spells.csv): `spell, heal, mana_cost, cast_time_s, HPS, MPS, HPM, time_to_oom_s, overheal, effective_HPS, frontier_status`. The Tidecaller inputs and step 6 overheal factors are filled in; the rest is yours.
  - [`Frontier.csv`](lab07-starter/Frontier.csv): `segment, from_spell, to_spell, MPS_from, MPS_to, HPS_from, HPS_to, marginal_HPM`, starting at the origin.
  - [`Curve.csv`](lab07-starter/Curve.csv): `T_s, budget_MPS, region, sustainable_HPS, enrage_check_750`, with `T_s` filled from 10 to 600 in steps of 10.
  - [`Encounter.csv`](lab07-starter/Encounter.csv): `parameter, value, unit, note`, holding the pool, regeneration, boss DTPS and fight length, plus the Mend and Surge check values.
- The lecture's Mend and Surge healer for checking: `M = 10,000`, `r = 20`, Mend 2,000 / 250 / 2.5 s, Surge 1,500 / 375 / 1.5 s.
- The "Tidecaller" healer kit to analyse:

| Spell | Heal | Mana cost | Cast time |
|---|---|---|---|
| Brook | 2,400 | 300 | 3.0 s |
| Torrent | 1,800 | 450 | 1.5 s |
| Spray | 1,200 | 300 | 1.5 s |

- Tidecaller pool `M = 12,000`, regeneration `r = 25` mana per second.
- Encounter: a boss that deals 750 DTPS to the tank after mitigation for 5 minutes.
- The [mana budget interactive](../examples/w07-mana-budget.html) from the lecture, for checking your curve.

## Steps

1. **Spell rates.** On `Spells`, compute HPS, MPS and HPM for each spell, and time to OOM when cast alone (`M / (MPS − r)`).
2. **Frontier.** On `Frontier`, sort spells by MPS and build the upper convex hull starting at the origin. List each frontier segment with its marginal HPM. Mark any spell below the frontier as "never cast".
3. **Curve.** On `Curve`, compute `B(T) = M / T + r` and sustainable HPS for T from 10 to 600 seconds in 10-second steps, by interpolating along the frontier. Chart it.
4. **Check against the lecture.** Switch the inputs to Mend and Surge. Your sheet must give 915.6 HPS at 60 s, 604.4 at 180 s, and region boundaries at 43.5 s and 125 s.
5. **Encounter.** Switch back to Tidecaller. Find the fight length at which sustainable HPS drops below 750. Does the healer survive the full 5 minutes?
6. **Overheal.** Add an overheal factor per spell (Brook 30%, Torrent 15%, Spray 10%). Recompute the frontier and the enrage time. Does any spell change status?
7. **Tune.** Change at most two numbers in the kit so that every spell is on the frontier and each is the best choice somewhere between 60 and 360 seconds, while the healer keeps up with 750 DTPS for 5 minutes with 20% overheal on every spell.

## Deliverable

The completed sheet and a memo of at most 400 words to the class designer. It must state the original enrage time, which spells were dead and why (in marginal HPM), your two changes, and the new frontier.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | Reproduces all four lecture test values; frontier built from the hull, not by hand | One test value off | Test values not reproduced | 25% |
| Tidecaller analysis | Rates, frontier, dead spell and enrage time all correct | Minor slip in one quantity | Frontier or enrage time wrong | 25% |
| Overheal step | Recomputed and the change in status explained | Recomputed, not interpreted | Missing | 15% |
| Tuning | Two changes meet every constraint, shown with numbers | Most constraints met | Constraints not checked | 25% |
| Memo writing | Plain, numeric, within the word limit | Some vague claims | Hard to act on | 10% |
