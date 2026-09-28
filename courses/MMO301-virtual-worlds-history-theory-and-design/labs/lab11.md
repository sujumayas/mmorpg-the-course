# MMO301 · Lab 11: The laws review

Assigned in week 11 ([lecture](../lectures/w11-kosters-laws-of-online-world-design.md)). Due at the start of week 13. Marked with the rubric below; it feeds the risks chapter of your world design bible.

## Objective

Run a full Koster's Laws review on a feature brief, put numbers on the population laws with `1 − e^(−qH)` and `1 − (1 − f)^n`, count the system interactions the feature creates, and propose isolation rules that remove the worst cases without removing the feature. The skill you are practising is turning an aphorism into a design requirement.

## Starter materials

Everything below is included in this file. The game, "Ashfall Reach," and all numbers are invented.

**1. Feature brief: "Beast bonding" (proposed for Ashfall Reach's first major update).**

> Any player can bond with a wild creature after defeating it, including elite creatures and dungeon bosses. Bonded beasts follow the player everywhere, including cities, dungeons and player housing. A bonded beast keeps every ability it had in the wild, including area-of-effect attacks, debuffs and summons. Players can dismiss a beast to a personal stable at any time and resummon it anywhere. Beasts can be traded to other players. A player may own up to 5 bonded beasts.

**2. Existing systems in Ashfall Reach (30).** Movement and mounts; melee combat; spell combat; area-of-effect damage; debuffs; buffs; healing; crowd control; summons; threat; death and resurrection; loot; trading; auction house; mail; crafting; gathering; player housing; guild halls; guilds; parties; raids; instanced dungeons; open-world PvP flagging; safe zones (cities); NPC guards; quests; world events; chat; reputation.

**3. Population figures.**

| Population | Players | Hours each |
|---|---|---|
| Internal QA | 35 | 150 |
| Public test server | 3,000 | 12 |
| Update day (live) | 120,000 | 3 |
| Update week (live) | 120,000 | 18 |

Peak concurrency on update day: 40,000. Assume a troublemaker share `f` between 0.5% and 2%.

**4. Review template (one row per family, from lecture section 5).**

| Family | Question | Your worst plausible case | Numbers | Isolation rule or accepted risk |
|---|---|---|---|---|
| Loophole | | | | |
| Troublemakers | | | | |
| Interactions | | | | |
| Expectations | | | | |
| Communication | | | | |
| Persistence | | | | |

## Steps

1. Read the brief and list at least five ways the feature could be abused or could break the world. For each, name the law (from Koster's page, not only the lecture) that predicts it.
2. Pick your three worst cases. For each, give `q` as a range (a low and a high estimate per player-hour) with one sentence of reasoning.
3. For each worst case, compute P(found) for all four populations at both ends of the range, and the expected wait at peak concurrency. Present one table per case.
4. Identify the single most dangerous group context (a raid, a city, a housing district). Compute P(at least one troublemaker) for its group size at `f = 0.5%`, 1% and 2%.
5. Count the new pairs the feature creates with the 30 existing systems. List the ten pairs you think are riskiest, and for each say whether an isolation rule can remove it.
6. Fill the review template.
7. Write the isolation plan.

## Deliverable

- The completed review template.
- The three exposure tables and the troublemaker table.
- A 500-word isolation plan for the Ashfall Reach design lead: which rules you would add (for example, "beasts are reset to stable when entering a safe zone"), which risks you accept and why, what telemetry would detect the remaining cases on update day, and what you would roll back if a case is found.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Laws applied | Five or more failure modes, each tied to a correctly paraphrased named law | Three or four, or some laws misapplied | Laws named without connection to the feature | 20% |
| Exposure numbers | `q` ranges reasoned, all probabilities and waits correct, both ends of range shown | Minor errors, or ranges unjustified | Wrong model or missing tables | 25% |
| Interactions | Pair count correct, risky pairs specific to the brief, isolation judged pair by pair | Count right, pairs generic | Not attempted | 20% |
| Isolation plan | Rules that remove worst cases while keeping the feature; accepted risks stated with reasons; telemetry and rollback plan specific | Sensible rules, thin on telemetry or rollback | Proposes cutting the feature without analysis | 35% |

Instructor check values: QA `H = 5,250`; public test `H = 36,000`; update day `H = 360,000`; update week `H = 2,160,000`. At `q = 1e-5`: 5.1%, 30.2%, 97.3%, more than 99.99%; wait at peak 2.5 hours. New pairs from one feature added to 30 systems: 30.
