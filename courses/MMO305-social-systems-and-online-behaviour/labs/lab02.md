# MMO305 · Lab 02: Three networks from one census

**Week:** 2 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** practice for the field observation (30%); submitted with the reading responses (20%)

## Objective

Turn a guild's census log into the three networks from [week 2](../lectures/w02-playing-alone-together.md) (co-presence, co-location and co-activity), measure how far apart they are, find the guild's real play group, and propose features that each target one layer. This is the same analysis you will run on your own census in the field observation.

## Starter materials

- [`lab02-starter/census.csv`](lab02-starter/census.csv): an invented census of a 20-member guild (M01 to M20) over one evening, 16 snapshots every 15 minutes from 18:00 to 21:45. One row per online member per snapshot, 150 rows. Columns `member, time, zone, grouped` (`y` or `n`). A member with no row at a time was offline. Zones are City, Marsh, Ridge, Fen, Crypt and Keep. Crypt and Keep are dungeons.
- A spreadsheet (pivot tables are enough for steps 1, 2 and 5) or Python 3 with the standard library. Pair counting in steps 3 and 4 is easier in Python. Group rows by `time`, then loop over pairs of members with `itertools.combinations`.

**Tie rules for this lab** (stricter than the lecture's "at least one snapshot", closer to the paper's time weighting):

| Layer | Tie between two members if... |
|---|---|
| Co-presence | both online in at least 1 common snapshot |
| Co-location | same zone, not City, in at least 2 common snapshots |
| Co-activity | both grouped, same zone, in at least 2 common snapshots |

## Steps

1. **Roster view.** Plot online members per snapshot as a bar chart. Report the peak, and the time of the peak. This is what a guild leader sees.
2. **Grouped share.** Compute online member-snapshots, grouped member-snapshots, and the grouped share. Compare with the week 2 census finding for mid-level characters.
3. **Three densities.** With `n = 20`, `P = 190`. Build all three networks under the tie rules and compute the three densities. Put them in a table beside the Ducheneaut et al. means for guilds of 16 to 30 members (co-presence 0.27, co-location 0.08). Explain in three sentences why your co-presence density is much higher than theirs (hint: what time span does each census cover?).
4. **Main core and isolates.** Find the main core of the co-location network (the largest `k` with a non-empty k-core, and its members). List the members with no co-location tie at all.
5. **Alone together.** Count member-snapshots where a member is in a non-City zone, not grouped, with at least one other online guildmate in the same zone. Name the three members with the most.
6. **Sensitivity.** Recompute co-location density with a threshold of 1 snapshot instead of 2. How much does it change? What does this tell you about reporting densities without stating the tie rule?
7. **Two features, two layers.** Propose one feature that raises co-location among the solo questers (M08 to M14) and one that turns some of that co-location into co-activity. For each, say which cells of the census would change if it worked and estimate the new density.

## Deliverable

A table of all numbers from steps 1 to 6, the roster chart, a drawing (hand or tool) of the co-location network with the main core marked, and a memo of about 300 words to the guild's officers. The memo must say who the guild's real play group is, which members are at risk of drifting away and why, and recommend the two features from step 7.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Roster and grouped share | Chart labelled, peak and grouped share correct, compared with the paper | Numbers right, no comparison | Missing or wrong | 15% |
| Three densities | All three correct under the stated rules, comparison with Table 1 explained by time span | One density wrong or explanation missing | Two or more wrong | 25% |
| Core, isolates, alone together | Main core, isolates and alone-together counts correct | One of the three wrong | Two or more wrong | 20% |
| Sensitivity | Both thresholds computed, clear point about stating tie rules | Computed, no point made | Missing | 10% |
| Features and memo | Each feature aimed at one layer, census changes named, density estimates given, at-risk members named with reasons | Features plausible but not tied to layers or numbers | Opinion without numbers | 30% |

<details>
<summary>Instructor check values</summary>

- Online per snapshot, 18:00 to 21:45: 3, 4, 6, 9, 15, 16, 15, 14, 14, 14, 10, 9, 10, 5, 4, 2. Peak 16 at 19:15.
- Online member-snapshots 150, grouped 43, grouped share 28.7%. (Core five grouped in the Keep for 7 snapshots each, 35; M06 and M07 grouped in the Crypt for 4 each, 8.)
- Co-presence 159 of 190, density 0.837. Co-location (2+ snapshots) 15 of 190, 0.079: the 10 pairs among M01-M05 plus M06-M07, M08-M18, M09-M10, M10-M13, M13-M14. Co-activity (2+ snapshots) 11 of 190, 0.058: the 10 core pairs plus M06-M07.
- Why co-presence is higher than the paper's 0.27: this census covers one evening at peak time, while the paper's networks cover weeks of play across all hours. Over a month, many pairs keep different schedules and never overlap. Within one peak evening, most members who log in at all overlap with most others. Co-location is close to the paper's value because it depends on shared activity, not on shared schedules.
- Main core: k = 4, {M01, M02, M03, M04, M05}, 25% of the guild. Co-location isolates (7): M11, M12, M15, M16, M17, M19, M20. M15 and M16 are City idlers, present all evening and never co-located.
- Alone-together member-snapshots: 45. Highest are M10 (6), then M06, M13 and M14 (5 each).
- Sensitivity: co-location with a 1-snapshot threshold is 37 of 190, 0.195, about 2.5 times the 2-snapshot value.

</details>
