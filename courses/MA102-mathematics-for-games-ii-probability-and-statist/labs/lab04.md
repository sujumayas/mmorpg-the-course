# MA102 · Lab 04: The expected-DPS spreadsheet

**Week:** 4 · **Time:** 2 hours in the lab plus up to 3 hours at home · **Weight:** part of the problem-set component

**Lecture:** [Week 04, Expected value: comparing weapons](../lectures/w04-expected-value-comparing-weapons.md)

## Objective

Build a spreadsheet that computes tooltip DPS and expected DPS for a set of weapons, find the break-even stat values where rankings flip, and write a balance recommendation for a producer. You will reuse this sheet in Lab 05.

## Starter materials

- A spreadsheet (Google Sheets, LibreOffice Calc or Excel). Python 3 is allowed if you also produce a table and a chart.
- The weapon list and character profiles below.

> **Weapon list: the Ashfall armory.** A new zone adds five two-handed and one-handed weapons. All numbers are item data.
>
> | Weapon | Min | Max | Speed (s) | Special |
> |---|---|---|---|---|
> | Iron Maul | 90 | 150 | 3.0 | none |
> | Keen Rapier | 30 | 42 | 1.0 | +25% crit chance |
> | Cinder Axe | 110 | 170 | 3.4 | crits deal ×2.5 instead of ×2 |
> | Twin Fangs | 12 | 18 | 0.6 | none |
> | Marksman Bow | 40 | 60 | 2.0 | never misses |
> | Gambler's Cleaver | 20 | 180 | 3.0 | +10% crit chance |
>
> **Character profiles** (all crits ×2 unless the weapon says otherwise):
> - *Fresh:* 10% miss chance, 5% base crit.
> - *Geared:* 3% miss chance, 20% base crit.
> - *Raid boss target:* 15% miss chance, 5% base crit (the boss dodges more).

## Steps

1. **Tooltip DPS.** For each weapon compute the average damage `(min + max) / 2` and tooltip DPS `average / speed`. Check: Iron Maul 40.00, Keen Rapier 36.00.
2. **Outcome table.** For the Fresh profile, build a miss / normal / crit table for each weapon with probability, damage and probability × damage, as in section 2 of the lecture. Confirm the probabilities in each table sum to 1. Check: Iron Maul expected damage per swing 113.4, expected DPS 37.80; Keen Rapier 42.12.
3. **Shortcut formula.** Add a column computing `(1 − q) × D × (1 + c(m − 1)) / s` directly. It must match step 2 for every weapon. If one does not, find the error before continuing.
4. **Three profiles.** Compute expected DPS for every weapon under all three profiles. Produce a table of rankings (1 to 6) per profile. Mark every weapon whose rank differs from its tooltip rank.
5. **Crit sweep chart.** Plot expected DPS against total crit chance from 0% to 60% for all six weapons on one chart, using the Fresh miss chance. Label each line.
6. **Break-even points.** Using algebra (show the equation) and then the chart, find (a) the total crit chance at which the Keen Rapier ties the Iron Maul, with the Maul held at the Fresh 5%, and (b) whether any shared crit chance from 0% to 100% lets the Iron Maul beat the Cinder Axe. Prove (b) with an inequality. Check (a): 16.7%.
7. **Recommendation.** The producer wants every weapon within 5% of the Iron Maul's expected DPS for the Geared profile. For each weapon outside that band, propose one numeric change (a damage range, a speed or a special) that brings it inside. Recompute to prove it.

## Deliverable

The spreadsheet with the tables from steps 1 to 4 and 7, the chart from step 5, the step-6 equations, and a 300-word memo to the producer. The memo names which weapons are misranked by the tooltip, for which profile, and why, in terms of the three multipliers (hit, average, crit).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Tooltip and expected DPS | All values correct under all three profiles; check values match | One weapon or profile wrong | Several wrong or check values fail | 30% |
| Outcome tables | Probabilities sum to 1, shortcut matches every table | Minor arithmetic slip, shortcut still present | Tables missing or probabilities do not sum to 1 | 15% |
| Chart and break-even | Chart labeled and correct; both break-even points solved algebraically and match the chart | One break-even point missing or only read from the chart | Missing | 20% |
| Balance changes | Every out-of-band weapon fixed with one change, recomputed and inside the band | Changes proposed, one not verified | No changes or changes not tested | 20% |
| Memo | Explains each misranking with the multiplier that causes it, names the profile | Lists misrankings without explaining them | Missing | 15% |
