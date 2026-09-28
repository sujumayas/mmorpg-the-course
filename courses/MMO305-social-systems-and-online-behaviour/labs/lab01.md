# MMO305 · Lab 01: Mapping bridging and bonding on a server

**Week:** 1 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the reading responses (20%)

## Objective

Measure the social structure of a small server, find the players it depends on, and change the membership rules so that no single departure can split it. You will use the E-I index, reach and brokers from [week 1](../lectures/w01-mmos-as-societies-social-capital.md), and you will see the week's main lesson in real data. The tie mix barely moves while the server's connectedness changes completely.

## Starter materials

All files are in [`lab01-starter/`](lab01-starter/).

- `players.csv`: 40 players in five guilds. Columns `player, guild`. Guild sizes are Ember 10, Frost 9, Gale 8, Hollow 7, Iron 6. Player IDs start with the guild's initial (E01 to E10, F01 to F09, and so on).
- `server-ties.csv`: 91 undirected ties observed over a month (invented data). Columns `a, guild_a, b, guild_b`. A tie means the two players grouped together at least three times, the week 3 acquaintance threshold.
- `netlib.py`: Python 3, standard library only. It loads both files and gives you `reach(players, edges, removed=())`, which returns the connected pairs, all pairs and average steps. You write `ei_index` and `find_brokers`. Running `python3 netlib.py` prints the server's reach.
- If you prefer a spreadsheet for steps 1 and 2, the CSV opens directly. Steps 3 onward need the script (or a network tool such as Gephi, if you already know one).

## Steps

1. **Count ties.** Count internal ties per guild and in total, and external ties. Compute each guild's internal density `L / (n(n − 1)/2)` and the server's E-I index.
2. **Reach.** Run `netlib.py`. Record reach and average steps. Then delete all external ties and compute reach again. Explain the difference in two sentences.
3. **Brokers.** Implement `find_brokers`. For each broker, record the reach among the remaining 39 players and say in one line what kind of player this would be in a real game (a trader, an officer who runs cross-guild raids, a friendly healer).
4. **Fragility budget.** Suppose each broker has a 10% chance of quitting in any month, independently. What is the chance that at least one quits in a given month? In a six-month season? (Use the complement rule from MA102 week 3.)
5. **Redesign by adding ties.** You may add at most **four** new external ties. Remove every broker while keeping the E-I index below −0.7. Report the fewest ties you needed, which pairs you tied, and the new E-I, reach and average steps.
6. **Redesign by rule.** Now instead of hand-placed ties, write one membership or content rule (for example, "each character may join one guild and one cross-guild league") and model its effect by adding the ties it would plausibly create in a month. Recompute everything. Compare it with step 5.

## Deliverable

Your completed `netlib.py` (or spreadsheet plus network tool files), a table of the numbers from steps 1 to 6, and a design memo of about 300 words to your lead designer. The memo must name the brokers, state the fragility risk from step 4, recommend the rule from step 6 or a better one, and name one cost of the rule to guild loyalty.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Tie counts and E-I | All counts, densities and E-I correct | One or two errors | Three or more errors | 15% |
| Reach analysis | Reach with and without external ties, clear explanation of why they differ | Numbers right, explanation vague | Missing or wrong | 15% |
| Brokers | All brokers found, reach after each removal correct, plausible in-game roles | Brokers found, reach missing | Brokers missed | 20% |
| Fragility | Correct complement-rule calculation for one month and six months | One period correct | Missing | 10% |
| Redesign by ties | No brokers, E-I below −0.7, minimal number of ties argued | No brokers but not minimal or not argued | Brokers remain | 20% |
| Rule and memo | Rule modelled with plausible ties, compared with step 5, cost to loyalty named, numbers cited | Rule stated, weakly modelled | Opinion without numbers | 20% |

<details>
<summary>Instructor check values</summary>

- Internal ties: Ember 27, Frost 19, Gale 15, Hollow 15, Iron 10, total `I = 86`. External `E = 5` (E10-F01, E10-G01, F09-H01, G08-H02, H07-I01). E-I `= (5 − 86) / 91 = −0.890`.
- Internal densities: Ember `27/45 = 0.60`, Frost `19/36 = 0.53`, Gale `15/28 = 0.54`, Hollow `15/21 = 0.71`, Iron `10/15 = 0.67`.
- Reach 780 of 780 (100%), average steps 4.03. Without external ties, every guild is still connected inside, so reach is the sum of within-guild pairs, `45 + 36 + 28 + 21 + 15 = 145` of 780 (18.6%). Common error: counting internal ties (86) instead of internal pairs.
- Brokers: E10 (reach after removal 471 of 741, 63.6%, Ember cut off), H07 (543 of 741, 73.3%, Iron cut off), I01 (571 of 741, 77.1%, the rest of Iron cut off). F09-H01 and G08-H02 form a cycle with E10's two ties, so F09, G08, H01, H02 are not brokers.
- Fragility with three brokers at 10% each: one month `1 − 0.9^3 = 27.1%`; six months `1 − 0.9^18 = 85.0%`.
- Minimum fix: **one** tie between a non-broker Ember member and a non-broker Iron member (for example E01-I02) removes all three brokers. E-I becomes `(6 − 86)/92 = −0.870`, reach stays 100%, average steps 3.63. Students who add four ties such as E01-H03, F02-I02, G02-I03 and E02-F03 get E-I −0.811, average steps 3.21, no brokers; full marks for correctness, lower for minimality unless argued.

</details>
