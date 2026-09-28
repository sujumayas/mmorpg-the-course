# MMO305 · Exam bank: quiz, practice and viva questions

MMO305 has no written exam. The grade comes from the reading responses (20%, [reading-responses-brief.md](reading-responses-brief.md)), the field observation (30%, [field-observation-brief.md](field-observation-brief.md)) and the final social system design and research proposal (50%, [final-design-proposal-brief.md](final-design-proposal-brief.md)). This bank does three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go faster.
- **Weekly quizzes.** Most weeks open with a 10-minute ungraded quiz of two or three questions from this bank, usually one compute question and one explain or critique question.
- **Viva.** The 12-minute viva after your final design presentation in week 15 draws questions in the style of this bank. Examiners rewrite them with the numbers from your own design, so knowing these answers by heart will not help. Knowing the models will.

Every question is tagged with the week or weeks it draws on and a type.

- **compute**: apply a lecture model to numbers you have not seen before.
- **explain**: say why a model behaves the way it does, with a number as evidence.
- **design**: choose values or rules that meet a stated goal, and show that they meet it.
- **critique**: find what is wrong with a proposal or a claim, and say how to fix it.

A question tagged **new case** asks you to apply a lecture model to numbers or a situation the lecture did not work through. 52 of the 65 questions carry that tag. By type there are 34 compute, 7 explain, 10 design and 14 critique questions.

All numbers are invented for teaching unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and version, and no question relies on a game fact the lectures do not state. Every numeric answer was recomputed in Python. Where rounding matters, the solution says how it was rounded. Write your own answer before you open the solution.

---

## Week 1: MMOs as societies, social capital

Lecture: [w01-mmos-as-societies-social-capital.md](../lectures/w01-mmos-as-societies-social-capital.md).

1. *Week 1 · compute · new case.* A small server has three guilds, A, B and C, of 7 players each. Everyone in a guild knows everyone else in it. (a) How many internal ties are there, how many pairs of players, and what is the reach with no external ties? (b) Player A7 befriends B1 and C1. Give the E-I index and the reach. (c) A7 quits. What share of the remaining pairs can still reach each other? (d) Instead of A7's two ties, the designer's cross-guild event produces three ties A7-B1, B7-C1 and C7-A1. Give the E-I index and say whether any broker remains.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 63 internal ties, 210 pairs, reach 30.0%. (b) E-I −0.938, reach 100%. (c) 57 of 190 pairs, 30.0%. (d) E-I −0.909, no brokers.

(a) Each guild has `7 × 6 / 2 = 21` ties, so `I = 63`. The server has `21 × 20 / 2 = 210` pairs. With no external ties only pairs inside a guild connect, so reach is `63 / 210 = 30.0%`.

(b) `E-I = (2 − 63) / (2 + 63) = −61 / 65 = −0.938`. A7 connects all three guilds, so every pair can reach every other. Reach is 100%.

(c) Without A7 there are 20 players and `20 × 19 / 2 = 190` pairs. Guild A has 6 members left, 15 pairs. B and C have 21 each. Connected pairs `= 15 + 21 + 21 = 57`, and `57 / 190 = 30.0%`. The server lost 1 player in 21 and all of its connection.

(d) `E-I = (3 − 63) / 66 = −0.909`. The three ties form a cycle through the three guilds, so every guild has two routes to every other. Removing any single player leaves the rest connected. One extra tie bought the resilience, the same lesson as the lecture's "every pair of guilds linked once" row.
</details>

2. *Week 1 · explain · new case.* A server has four guilds of 5 players, fully connected inside, so `I = 40`. Compare two changes. In change X, player A5 also joins guild B as a second guild and gains a tie to all five B members. In change Y, A5 simply befriends B1. Compute the E-I index and the reach after each. Then explain why the two changes move the E-I index so differently but give the same reach.

<details>
<summary>Answer and worked solution</summary>

**Answer:** X gives E-I −0.778, Y gives −0.951. Both give reach 65 of 190, 34.2%.

There are 20 players and 190 pairs. X adds 5 external ties, so `E-I = (5 − 40) / 45 = −0.778`. Y adds 1, so `E-I = (1 − 40) / 41 = −0.951`.

In both cases guilds A and B become one connected block of 10 players, `10 × 9 / 2 = 45` pairs, while C and D stay closed with 10 pairs each. Reach is `45 + 10 + 10 = 65` of 190, 34.2%.

Reach needs only one crossing point between two clusters. The first tie between A and B connects all `5 × 5 = 25` cross pairs. The next four ties connect nobody new. They shorten paths and add backup, which is why multiple membership reads as a big change on the E-I index and a small one on reach. The E-I index measures the mix of ties. Reach measures structure.
</details>

3. *Week 1 · critique.* A producer announces a "big social update": two more guild ranks, a larger guild bank and a guild hall with crafting stations only members can use. The press release says it will "bring the whole server together." Critique the claim using the week 1 model, and propose one feature that would do what the press release says.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Every listed feature adds or deepens internal ties, so it makes the E-I index more negative and adds nothing to reach. It may strengthen guilds. It does not connect the server.

Sort each feature into the two columns from section 4, "creates internal ties" and "creates external ties." Ranks, a bank and a members-only hall all go in the first column. None creates a tie between guilds, so reach is unchanged. The members-only stations may even remove a reason to meet outsiders, such as asking another guild's crafter for help.

A feature that would bring the server together creates external ties, ideally redundant ones so no broker holds the server together. Examples from the lecture's levers are an open public event where anyone nearby can join and everyone is rewarded, a cross-guild chat group players can join alongside their guild (as FFXIV linkshells allow), or a formal alliance layer. The measure to report would be reach and the broker count, not the number of guild features.
</details>

## Week 2: Playing alone together

Lecture: [w02-playing-alone-together.md](../lectures/w02-playing-alone-together.md).

4. *Week 2 · compute · new case.* Here is an invented census of a six-member guild, one snapshot every 15 minutes. A blank cell means offline and an asterisk means grouped. City does not count for co-location.

| Member | 20:00 | 20:15 | 20:30 | 20:45 |
|---|---|---|---|---|
| Ada | Bog | Bog* | Bog* | City |
| Ben | | Bog* | Bog* | Bog |
| Cy | City | City | Hill | Hill |
| Dee | Hill | | | |
| Eve | | | Hill | Hill |
| Flo | City | City | City | |

Using the lecture's "at least one snapshot" rule, compute (a) the three densities, (b) the grouped share of online time, (c) the main core of the co-location network, and (d) the number of member-snapshots spent alone together.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Co-presence 0.867, co-location 0.133, co-activity 0.067. (b) 23.5%. (c) The 1-core {Ada, Ben, Cy, Eve}, 4 of 6. (d) 4.

(a) `P = 6 × 5 / 2 = 15`. Dee is online only at 20:00. Ben is online only from 20:15 and Eve only from 20:30, so Dee-Ben and Dee-Eve never overlap. Every other pair overlaps at least once, so co-presence `L = 13` and `D = 13 / 15 = 0.867`.

Co-location needs the same non-City zone at the same time. Ada and Ben share the Bog at 20:15 and 20:30. Cy and Eve share the Hill at 20:30 and 20:45. Cy and Dee both visit the Hill, but never at the same time. So `L = 2` and `D = 2 / 15 = 0.133`.

Co-activity needs both grouped in the same zone. Only Ada and Ben qualify, so `L = 1` and `D = 1 / 15 = 0.067`.

(b) Online member-snapshots are `4 + 3 + 4 + 1 + 2 + 3 = 17`. Grouped ones are Ada twice and Ben twice, 4. The grouped share is `4 / 17 = 23.5%`.

(c) In the co-location network Ada, Ben, Cy and Eve each have one tie, and Dee and Flo have none. No member has two ties, so the main core is the 1-core of those four.

(d) Cy and Eve share the Hill at two snapshots without grouping, 4 member-snapshots. Ben alone in the Bog at 20:45 does not count, because no guildmate is there.
</details>

5. *Week 2 · compute · new case.* A 30-member guild has the census means for guilds of 6 or more from the lecture, co-presence density 0.27 and co-location density 0.09. (a) About how many co-presence and co-location ties does the guild have in total? (b) How many co-location ties does the average member have? (c) The guild leader says, "Everyone plays with everyone here." Which number would you show the leader, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 117 co-presence and 39 co-location ties. (b) About 2.6. (c) The co-location figure.

(a) `P = 30 × 29 / 2 = 435`. Co-presence `0.27 × 435 = 117.45`, about 117. Co-location `0.09 × 435 = 39.15`, about 39.

(b) Each member has `D × (n − 1) = 0.09 × 29 = 2.61` co-location ties on average, out of 29 guildmates. The co-presence equivalent is `0.27 × 29 = 7.83`.

(c) "Everyone plays with everyone" is a claim about co-activity, the strongest layer. Even co-location, the weaker layer above it, links each member to fewer than 3 of 29 guildmates. The roster and guild chat show co-presence, which is why the leader's impression is so far off.
</details>

6. *Week 2 · critique.* A live-ops team adds a daily reward to anyone who spends 30 minutes online at the same time as at least three guildmates, and reports it as a success because "guildmates online together" rose 40%. Critique the feature and the metric, using the three layers and the Star Wars Galaxies case.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Both the reward and the metric sit on co-presence, the weakest layer. The feature buys logins, not play together, and the metric cannot tell the difference.

The reward requires only being online together, so players can meet it while soloing in different zones or idling in a city. It raises co-presence density and leaves co-location and co-activity where they were. The metric "guildmates online together" measures the same layer, so the dashboard reports success by construction.

Star Wars Galaxies shows the next step up. Its entertainer buff paid combat players to stand in the same cantina, which raised co-location, yet co-activity stayed low. If even a co-location reward does not produce joint play, a co-presence reward is further away still. The fix is to reward something done together (a group activity completed, a shared event) and to instrument co-location and co-activity density alongside co-presence.
</details>

7. *Week 2 · explain · new case.* Suppose every guild member, whatever the guild's size, sustains about 4 co-activity ties. Compute co-activity density for guilds of 10, 50 and 200 members, and explain what the numbers imply for how you judge a large guild's health.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0.444, 0.082 and 0.020.

Each member has about 4 ties out of `n − 1` possible, so `D ≈ 4 / (n − 1)`. That gives `4 / 9 = 0.444`, `4 / 49 = 0.082` and `4 / 199 = 0.020`.

Density falls with size even though every member behaves the same way. Low density in a large guild is expected and says nothing on its own about failure. The lecture's test is whether the main core is large enough to run the guild's content, so judge a big guild by its core, not by its density.
</details>

## Week 3: Forced vs voluntary grouping

Lecture: [w03-forced-vs-voluntary-grouping.md](../lectures/w03-forced-vs-voluntary-grouping.md).

8. *Week 3 · compute · new case.* A dungeon queue draws 5-player groups (`m = 4`) from a pool of `N = 300`. A player runs `r = 25` dungeons this month. Compute `p`, the expected distinct people met, the repeat encounters, the expected acquaintances with `k = 3`, and the chance that a given partner shows up again in the next 25 runs. Then use the approximation `r ≈ k(N − 1)/m` to estimate how many runs it takes to meet a given player 3 times on average.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `p = 0.0134`, `D ≈ 85.5`, repeats ≈ 14.5, acquaintances ≈ 1.3, reappear chance ≈ 28.6%, about 224 runs.

`p = 4 / 299 = 0.01338`. The chance of missing a given player for 25 runs is `(1 − 0.01338)^25 ≈ 0.714`, so `D = 299 × 0.286 ≈ 85.5`. The month has `4 × 25 = 100` partner slots, so `100 − 85.5 = 14.5` went to repeats.

Acquaintances are `A = 299 × P(X ≥ 3)` with `X ~ Binomial(25, 0.01338)`. `P(X ≥ 3) ≈ 0.0044`, so `A ≈ 1.3`.

Reappearance within the next 25 runs is `1 − 0.714 = 28.6%`.

The approximation gives `3 × 299 / 4 ≈ 224` runs, about nine months of this player's pace.
</details>

9. *Week 3 · compute · new case.* Soloing pays 120 experience per minute. A group pays 200 per minute once it is running. (a) What is the largest share of the session that forming a group can take before soloing wins? (b) Formation actually takes 30% of the session. What group rate would make grouping break even? (c) Name one lever that acts on each of (a) and (b).

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 40%. (b) About 171 per minute, so the current 200 already clears it. (c) Matchmaking or teleports shrink `w`, group bonuses raise `R_g`.

(a) Group if `200 × (1 − w) > 120`, so `1 − w > 0.6` and `w < 0.4`.

(b) With `w = 0.3`, grouping wins if `R_g × 0.7 > 120`, so `R_g > 171.4`. At 200 grouping wins, but by a margin of only `200 × 0.7 − 120 = 20` per minute.

(c) A group finder, fast travel to the dungeon or NPC fill-ins lower `w`. A group bonus or group-only rewards raise `R_g`. Neither says anything about whether the group produces ties, which needs the re-encounter model.
</details>

10. *Week 3 · compute · new case.* A game's pickup content has prisoner's dilemma payoffs `T = 7`, `R = 5`, `P = 2`, `S = 0`. (a) Compute both of Axelrod's thresholds for `w` from the lecture. (b) Using the week 3 pool-size table (20 runs ahead), which pools clear the bar? (c) What does this imply for the design of the queue?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.4 and 0.4. (b) Only the pool of 60. (c) Larger pools need enforcement or reputation.

(a) First condition `w ≥ (T − R) / (T − P) = 2 / 5 = 0.4`. Second condition `w ≥ (T − R) / (R − S) = 2 / 5 = 0.4`. With these payoffs the two tests agree.

(b) The table's reappearance chances are 75% (N = 60), 33% (200), 8% (1,000), 2% (5,000) and 0.4% (20,000). Only `N = 60` clears 0.4.

(c) In any pool larger than a few hundred, cooperation cannot sustain itself through repeat meetings alone. The queue needs rules that replace reputation (deserter penalties, vote kicks) or a reputation system that makes the shadow of the future longer (week 6).
</details>

11. *Week 3 · design · new case.* You are designing a weekly 8-player raid (`m = 7`). A typical player runs it twice a week, so `r = 8` a month. The social team wants the average player to gain at least 2 acquaintances (met 3 or more times) a month from the raid finder alone. What is the largest pool `N` that meets the target? What would you add if the queue must draw from a larger pool to keep waits short?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `N = 84`. For larger pools, add a re-meet tool such as "keep this raid together next week."

Compute `A = (N − 1) × P(X ≥ 3)` with `X ~ Binomial(8, 7 / (N − 1))`.

| `N` | `p` | Acquaintances `A` |
|---|---|---|
| 60 | 0.119 | 3.49 |
| 80 | 0.089 | 2.19 |
| 84 | 0.084 | 2.02 |
| 85 | 0.083 | 1.98 |
| 100 | 0.071 | 1.50 |

The largest pool that meets the target is 84. A pool that small will often fail to fill 8 slots with the right roles, which is the speed side of the trade-off. The lecture's funnel pattern keeps a big pool for introductions and adds a requeue or priority-matching option that turns a random pairing into a repeat. That breaks the binomial's randomness, so acquaintances no longer depend mainly on `N` (lab 03 measures this).
</details>

12. *Week 3 · critique.* A director says: "Our new MMO will require groups for all levelling content. The queue will be cross-server so nobody waits. Forced grouping builds community." Critique the plan using the week 3 model.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Forced grouping builds ties only in small pools. A cross-server queue makes the pool so large that repeat meetings almost vanish, so the plan pays the costs of forced grouping and gets none of the social benefit.

A cross-server pool puts `N` in the thousands. In the lecture's table, at `N = 5,000` a player meets about 79 distinct people in 20 runs, makes essentially zero acquaintances, and has about a 2% chance of seeing a given partner again. Forcing every levelling session through that queue gives players constant strangers.

Two more costs follow. With the shadow of the future near zero, desertion and loot grabbing carry no social cost, so the team will need deserter penalties and vote kicks, which create griefing routes of their own (week 8). And forcing groups removes `R_s` as an option, so players with 20 minutes or odd schedules have nothing to do.

A better plan is tiered content. Keep levelling soloable or open (GW2-style events), put tie-building content in small or pre-made pools with a group bonus, and add a requeue or friend prompt after good runs.
</details>

## Week 4: Guilds, formation, lifecycle, leadership

Lecture: [w04-guilds-formation-lifecycle-leadership.md](../lectures/w04-guilds-formation-lifecycle-leadership.md).

13. *Week 4 · compute · new case.* A guild's main activity needs `M = 15`. It recruits `R = 1.5` members a week, loses `c_low = 4%` a week above the threshold and `c_high = 18%` below it. (a) Find both steady states and say which are valid. (b) A walkout drops the guild to 12. Where is it after 1, 2, 3 and 4 weeks with normal recruiting? (c) What steady weekly recruitment would rescue a guild just below 15? (d) How many recruits in a single week would lift it from 12 to 15 or more?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 37.5 and 8.3, both valid. (b) 11.34, 10.80, 10.36, 9.99. (c) More than 2.7 a week. (d) 6 recruits.

(a) `N_high = 1.5 / 0.04 = 37.5`, which is at least 15, so it is valid. `N_low = 1.5 / 0.18 = 8.33`, which is below 15, so it is valid too. The guild is bistable.

(b) Below 15 each week uses `c_high`. Week 1 is `12 + 1.5 − 0.18 × 12 = 11.34`. Then `11.34 + 1.5 − 2.04 = 10.80`, then 10.36, then 9.99. It is sliding toward 8.3.

(c) `R > c_high × M = 0.18 × 15 = 2.7` per week.

(d) Solve `12 + R − 0.18 × 12 ≥ 15`, so `R ≥ 5.16`. In whole players that is 6, which lands the guild at 15.84. From there low churn takes over and it keeps growing (16.71, 17.54, 18.34 over the next three weeks).
</details>

14. *Week 4 · design · new case.* A guild has `R = 2`, `c_low = 5%`, `c_high = 25%` and a fixed raid size that makes `M = 25`. The designer wants guilds like this one to have no dying equilibrium at all. (a) Give its steady states. (b) What `M` would remove the dying state if `R` and the churn rates stay the same? (c) What recruitment rate would remove it at `M = 25`? (d) Which of the two is the more realistic design lever, and what shipped change does it resemble?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 40 and 8, both valid. (b) `M ≤ 8`. (c) `R ≥ 6.25` a week. (d) Lowering `M`, as flexible raid sizes did.

(a) `N_high = 2 / 0.05 = 40` (valid) and `N_low = 2 / 0.25 = 8` (valid, below 25).

(b) The dying state exists only while `N_low = R / c_high` is below `M`. It disappears when `M ≤ 8`.

(c) At `M = 25` it disappears when `R / c_high ≥ 25`, so `R ≥ 0.25 × 25 = 6.25` recruits a week, more than three times the guild's current rate.

(d) Designers control `M` directly and control `R` only weakly, through tools like a guild finder. Flexible raid sizes (WoW patch 5.4 and 6.0.2, 10 to 30 players on Normal and Heroic) lowered the effective `M` to 10 for most guilds. The cost is encounter tuning, since a fight that scales from 10 to 30 is harder to balance than one fixed size.
</details>

15. *Week 4 · explain · new case.* A game raises its guild cap from 100 to 500 and advertises "bigger, healthier communities." Using the coordination-cost formula, compute the number of pairs at 25, 100 and 500 members, and explain what the cap change does and does not do.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 300, 4,950 and 124,750 pairs.

`pairs = n(n − 1)/2`. At 25 that is 300, at 100 it is 4,950, at 500 it is 124,750. Going from 100 to 500 members multiplies the members by 5 and the pairs by about 25.

The cap is a database and power limit. It lets a guild hold more names. It does not let anyone hold more relationships. Past a few dozen members a guild has to split into subgroups (raid teams, officer councils, social circles) or become a crowd of strangers sharing a tag. The lecture's point is that the social limit comes from the players, so "healthier" does not follow from "bigger."
</details>

16. *Week 4 · critique.* Two designers argue about inactive-leader succession. One wants officers to claim leadership after 7 days of leader inactivity. The other wants 180 days. WoW's shipped rule moved from 30 to 90 days. Using the week 4 model, name the risk each proposal creates and say what you would add to make a short window safer.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Seven days invites takeovers during ordinary absences. 180 days leaves a leaderless guild long enough to cross its threshold.

A leader's absence lowers `R` (nobody recruits) and raises `c` (nobody resolves disputes). In the lecture's model a guild near `M` can go from growing to collapsing within a few weeks of that, so a 180-day wait means the guild the officers finally inherit may already be below `M` and on the dying branch.

A 7-day window protects against that, but an officer can seize a guild while the leader is on a week's holiday. That is a storming-stage event, and a walkout it triggers can itself push `N` below `M`.

Ways to make a short window safer include notifying the leader and giving them a veto period, requiring a vote among senior ranks, or letting the leader name a designated successor in advance. Each keeps the fast response without making absence a vulnerability.
</details>

## Week 5: Raiding as organization, DKP

Lecture: [w05-raiding-as-organization-dkp.md](../lectures/w05-raiding-as-organization-dkp.md).

17. *Week 5 · compute · new case.* A 10-player raid team has members who each attend 80% of nights, independently. (a) What is the chance of fielding 10 from a roster of 10, 12 and 14? (b) What is the smallest roster that fields 10 on at least 90% of nights? (c) How many bench players is that?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 10.7%, 55.8%, 87.0%. (b) 15. (c) 5.

`P(at least 10) = Σ_{x=10}^{R} C(R, x) 0.8^x 0.2^{R−x}`.

| Roster `R` | P(field 10) |
|---|---|
| 10 | 10.7% |
| 11 | 32.2% |
| 12 | 55.8% |
| 13 | 74.7% |
| 14 | 87.0% |
| 15 | 93.9% |

The first roster at or above 90% is 15, which carries 5 players beyond the raid size. At 80% attendance the bench is half the size of the raid, and every one of those players needs a reason to keep signing up.
</details>

18. *Week 5 · compute · new case.* Three raiders A, B and C split one item a night at price `P = 30`, ties to roster order. Run earned-spent DKP with `e = 15` and zero-sum DKP side by side for six nights. After night 6, C leaves and newcomer D takes the last roster slot with a balance of 0. (a) What is `ρ` for each system? (b) On which night does D win a first item under each? (c) Check both against the first-item formula.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 1.5 and 1. (b) Night 11 under earned-spent, night 9 under zero-sum. (c) The formula gives 5 and 3 nights of attendance, which match.

(a) Earned-spent `ρ = 3 × 15 / 30 = 1.5`. Zero-sum pays `30 / 3 = 10` a night, so `ρ = 1`.

(b) Balances after each night's item is paid:

| Night | ES winner | A | B | C or D | ZS winner | A | B | C or D |
|---|---|---|---|---|---|---|---|---|
| 1 | A | −15 | 15 | 15 | A | −20 | 10 | 10 |
| 2 | B | 0 | 0 | 30 | B | −10 | −10 | 20 |
| 3 | C | 15 | 15 | 15 | C | 0 | 0 | 0 |
| 6 | C | 30 | 30 | 30 | C | 0 | 0 | 0 |
| 7 (D joins) | A | 15 | 45 | 15 | A | −20 | 10 | 10 |
| 8 | B | 30 | 30 | 30 | B | −10 | −10 | 20 |
| 9 | A | 15 | 45 | 45 | D | 0 | 0 | 0 |
| 10 | B | 30 | 30 | 60 | | | | |
| 11 | D | 45 | 45 | 45 | | | | |

Under earned-spent, on night 9 D ties A and B at 45 before paying and loses on roster order. On night 11 D finally leads.

(c) `first-item wait ≈ n/k + T(ρ − 1)(n − 1)/n`. Earned-spent: `3 + 6 × 0.5 × 2/3 = 3 + 2 = 5` nights of attendance, nights 7 to 11. Zero-sum: `3 + 0 = 3`, nights 7 to 9.
</details>

19. *Week 5 · compute · new case.* A 25-player raid runs earned-spent DKP with `e = 12` a night, 4 items a night and a fixed price of 60. (a) Compute `ρ` and the points the raid gains per night in total. (b) A recruit replaces a veteran after 40 nights. Estimate the wait for a first item. (c) What does the wait become if the same recruit joins after 80 nights?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `ρ = 1.25`, and the raid's total rises 60 points a night. (b) About 16 nights. (c) About 25 nights.

(a) `ρ = 25 × 12 / (4 × 60) = 300 / 240 = 1.25`. Created 300, spent 240, net 60 a night.

(b) `25/4 + 40 × 0.25 × 24/25 = 6.25 + 9.6 = 15.85`, about 16 nights.

(c) `6.25 + 80 × 0.25 × 0.96 = 6.25 + 19.2 = 25.45`, about 25 nights. The wait grows with the age of the guild, which is the opposite of what a guild that needs recruits wants.
</details>

20. *Week 5 · design · new case.* A 10-player raid drops 2 items a night and pays `e = 10` a night. The officers want a recruit who joins after 60 nights to wait no more than 8 nights for a first item. What is the highest `ρ` they can allow, and what fixed price does that require?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `ρ ≤ 1.056`, so a price of at least 48.

The rotation alone takes `n/k = 5` nights, so the inflation term may add at most 3. `60 × (ρ − 1) × 9/10 ≤ 3` gives `ρ − 1 ≤ 0.0556`, so `ρ ≤ 1.056`.

`ρ = 10 × 10 / (2P) = 50 / P`. So `50 / P ≤ 1.056` gives `P ≥ 47.4`. A price of 48 gives `ρ = 1.042` and a wait of `5 + 60 × 0.042 × 0.9 ≈ 7.3` nights.

Zero-sum (`P = 50` at this earning rate, `ρ = 1`) would give 5 nights and stay at 5 however old the guild gets.
</details>

21. *Week 5 · critique.* A 20-player raid uses earned-spent DKP with `e = 10`, 4 items a night at `P = 50`. The officers decide the 6 bench players should also earn the full 10 a night, "to be fair." Critique the change with numbers, and propose a version that keeps the bench coming back without the side effect.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Paying the bench raises `ρ` from 1.00 to 1.30. That turns a balanced system into an inflating one, and a recruit who joins after 30 nights waits about 14 nights instead of 5.

Without bench pay, `ρ = 20 × 10 / (4 × 50) = 1.00`. With bench pay, 26 players earn and the same 4 items drain, so `ρ = 26 × 10 / 200 = 1.30`. Points are added without items to spend them on.

The recruit's wait with `ρ = 1.3` after `T = 30` nights is `20/4 + 30 × 0.3 × 19/20 = 5 + 8.55 = 13.55`. At `ρ = 1` it is 5.

Not paying the bench is worse, since bench players leave and the roster falls below what the binomial table says the raid needs. Fixes that keep both include paying the bench a fraction and raising the price so `ρ` stays at 1 (for example, bench at 50% gives `230 / (4P) = 1` at `P = 57.5`), adding a decay to all balances, or capping balances so the gap a recruit faces is bounded.
</details>

## Week 6: Trust and reputation systems

Lecture: [w06-trust-and-reputation-systems.md](../lectures/w06-trust-and-reputation-systems.md).

22. *Week 6 · compute · new case.* A reputation system uses `score = (r + 1)/(r + s + 2)` with forgetting factor `λ = 0.85`. Give its memory in matches, the half-life of one match, and the highest score an always-good player can approach.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Memory 6.7 matches, half-life 4.3 matches, ceiling 0.885.

Memory `= 1 / (1 − 0.85) = 6.67`. Half-life `= ln 0.5 / ln 0.85 = 4.27`. An always-good player settles at `r = 6.67`, `s = 0`, so the ceiling is `7.67 / 8.67 = 0.885`.

With under seven matches of memory, one bad evening is a large share of the record. This setting would catch turncoats fast and punish honest bad luck hard.
</details>

23. *Week 6 · compute · new case.* With `λ = 0.9` and the neutral prior, a player has `r = 5`, `s = 2`. They now play good, bad, good. Give the score before and after each match.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0.667, then 0.699, 0.622, 0.658.

Start: `6 / 9 = 0.667`.

Good: `r = 0.9 × 5 + 1 = 5.5`, `s = 0.9 × 2 = 1.8`. Score `6.5 / 9.3 = 0.699`.

Bad: `r = 0.9 × 5.5 = 4.95`, `s = 0.9 × 1.8 + 1 = 2.62`. Score `5.95 / 9.57 = 0.622`.

Good: `r = 0.9 × 4.95 + 1 = 5.455`, `s = 0.9 × 2.62 = 2.358`. Score `6.455 / 9.813 = 0.658`.

Decay applies before the new rating is added. Forgetting to decay first is the most common error.
</details>

24. *Week 6 · compute · new case.* A free-to-play game uses `score = (r + a)/(r + s + a + b)` with `λ = 0.9`, `a = 1`, `b = 2`. (a) What does a brand-new account score? (b) Where does an always-bad player settle? (c) By what factor does an always-bad player raise their score by making a new account? (d) Compare with the neutral prior `a = b = 1`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.333. (b) 0.077. (c) About 4.3 times. (d) With the neutral prior the gain is about 6 times.

(a) `a / (a + b) = 1/3 = 0.333`.

(b) Always bad means `r = 0` and `s = 1 / (1 − 0.9) = 10` at the steady state. Score `1 / (10 + 3) = 0.077`.

(c) `0.333 / 0.077 = 4.33`.

(d) With `a = b = 1` the newcomer scores 0.5 and the always-bad player `1/12 = 0.083`, a gain of 6 times (the lecture's figure). The harsher prior cuts the payoff of whitewashing, and every honest newcomer pays for it by starting at 0.333. That is Friedman and Resnick's dues-paying convention built into the formula.
</details>

25. *Week 6 · design · new case.* A matchmaker designer wants a match's weight to halve after 20 matches, with the neutral prior. (a) What `λ` does that require? (b) What are the memory and the ceiling? (c) Starting from the ceiling, how many bad matches in a row drop a perfect player below 0.5? Compare with `λ = 0.9`. (d) Which kind of harm is this setting built to catch?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `λ = 0.966`. (b) Memory 29.4, ceiling 0.968. (c) 21, against 7 at `λ = 0.9`. (d) Steady, noisy low-level misbehaviour rather than sudden switches.

(a) `λ = 0.5^(1/20) = 0.9659`.

(b) Memory `1 / (1 − 0.9659) = 29.4`. Ceiling `30.4 / 31.4 = 0.968`.

(c) Each bad match multiplies `r` by `λ` and adds 1 to `s`. Iterating from `r = 29.4`, `s = 0`, the score first drops below 0.5 after the 21st bad match (0.484). With `λ = 0.9` it takes 7 (0.482).

(d) A long half-life averages out noise, so honest players on a bad streak are protected. It also gives a turncoat about 20 matches of cover. Choose it if the harm you care about is steady toxicity that ratings measure noisily, and pair it with a separate fast report route for sudden, serious offences.
</details>

26. *Week 6 · critique.* A game shows each player's lifetime "kudos" count on their nameplate, labelled "Trust." Kudos can only be given, never taken away, and friends in a premade group can kudos each other every match. Name three problems in model terms and one fix for each.

<details>
<summary>Answer and worked solution</summary>

**Answer:** No `s`, `λ = 1`, and open collusion. Add negative ratings, add forgetting, and restrict who may rate.

No `s`. Kudos only accumulate, so the count cannot show bad behaviour. A scammer with 800 kudos still reads as trustworthy. Fix: pair it with a separate reporting system, or add a negative rating that feeds `s`.

`λ = 1`. The count is a lifetime total, so it measures time played and role as much as conduct, and it gives a turncoat a shield. Fix: decay old kudos, or show a recent-window level instead of a lifetime number.

Collusion. Friends in a premade can mint kudos for each other. FFXIV's commendation rule allows ratings only between players matched from outside a premade party for this reason. Fix: that rule, a per-pair time limit, or a cap per match.

The label is also a problem. A positive-only count is not a trust score, so the lecture's advice is not to present it as one.
</details>

## Week 7: Status, prestige and conspicuous display

Lecture: [w07-status-prestige-and-conspicuous-display.md](../lectures/w07-status-prestige-and-conspicuous-display.md).

27. *Week 7 · compute · new case.* A "speed clear" title is earned by `e = 50%` of skilled players, who are `s = 8%` of the population, and by `u = 1%` of unskilled players through strong groups. (a) Compute ownership, rarity in bits, precision and lift with no boosting market. (b) Repeat with a boosting market at `b = 4%`. (c) At what `b` does precision reach 50%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `f = 4.92%`, 4.35 bits, precision 81.3%, lift 10.2. (b) `f = 8.6%`, 3.54 bits, precision 46.5%, lift 5.8. (c) `b ≈ 3.35%`.

(a) Skilled owners `0.08 × 0.5 = 0.04`. Unskilled owners `0.92 × 0.01 = 0.0092`. `f = 0.0492`, rarity `log2(1/0.0492) = 4.35` bits, precision `0.04 / 0.0492 = 81.3%`, lift `0.813 / 0.08 = 10.2`.

(b) Unskilled owners `0.92 × 0.05 = 0.046`. `f = 0.086`, rarity 3.54 bits, precision `0.04 / 0.086 = 46.5%`, lift 5.8.

(c) Precision is 50% when unskilled owners equal skilled owners, `0.92 × (0.01 + b) = 0.04`, so `b = 0.04 / 0.92 − 0.01 = 0.0335`.

The title lost less than one bit of rarity and more than a third of its precision. A player glancing at it still sees a rare title.
</details>

28. *Week 7 · design · new case.* Using the lecture's badge (`s = 5%`, `e = 60%`, `u = 0.5%`), the design goal is precision of at least 70%. What is the largest carry rate `b` you can tolerate? Name one rule that could hold `b` there, and one group of players it upsets.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `b ≤ 0.85%`.

Skilled owners are `0.05 × 0.6 = 0.03`. Precision `0.03 / (0.03 + 0.95(u + b)) ≥ 0.7` requires `0.95(u + b) ≤ 0.03 × 0.3 / 0.7 = 0.01286`, so `u + b ≤ 0.01353` and `b ≤ 0.00853`.

The lecture's options include awarding the badge only to players who meet a performance bar in the run, making it untradeable and tied to the character that did the deed (the Infernal cape pattern), or showing on inspection how a run was completed. A performance bar upsets carry sellers and buyers, and also weaker players in strong guilds who used to earn it through `u`.
</details>

29. *Week 7 · explain · new case.* Take the speed-clear title from question 27 with the boosting market (`b = 4%`). The game lets players hide titles. Skilled owners show it 90% of the time and unskilled owners 40% of the time. What is the precision among titles players can see? Explain the mechanism and the side effect.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 66.2%, up from 46.5%.

Shown skilled owners `0.04 × 0.9 = 0.036`. Shown unskilled owners `0.046 × 0.4 = 0.0184`. Precision among visible titles `0.036 / 0.0544 = 66.2%`.

Showing acts as a second filter that removes more unskilled owners than skilled ones, so the displayed set is more skilled than the set of all owners. The side effect is that an empty title slot now carries a faint negative signal. About 37% of owners hide it (`1 − 0.0544 / 0.086`), and some of them are skilled players who simply prefer privacy.
</details>

30. *Week 7 · compute · new case.* A mount drops at 0.2% for anyone who kills a boss. A designer proposes cutting the rate to 0.1% "to make it more prestigious." What happens to its rarity and to its precision as a skill signal? What does the mount actually signal?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Rarity rises from 8.97 to 9.97 bits. Precision stays at the base rate `s`, lift 1.

`log2(1/0.002) = 8.97` bits and `log2(1/0.001) = 9.97`. Halving the rate adds exactly one bit.

The drop rate is the same for skilled and unskilled players, so `e = u` and `P(skilled | owns) = s`, lift 1, before and after. The mount is a luck and persistence signal (players who farmed the boss for months). It becomes rarer, not more meaningful about skill.
</details>

31. *Week 7 · critique.* A group-finder team proposes a filter that lets group leaders require a named achievement before a player can apply. Trace the gatekeeping loop this could start, and propose two changes that damp it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The filter automates step 1 of the loop. Damp it by keeping `b` low for credential items and by offering an entry route that does not show credentials.

The loop from section 4 runs like this. Leaders require the achievement because it predicts success. Players without it cannot get in, so its practical value rises. Demand for carries rises, which raises `b`. Precision falls, leaders see holders fail and demand a stricter credential, and the loop turns again with a higher bar. Newer players are pushed out every cycle even though the content has not changed.

Damping options from the lecture are making the credential expire with the tier (as Cutting Edge does), protecting `b` for any item the filter can use (untradeable, performance bar), keeping an automated finder that does not show achievements or matches by measured performance, and giving pushed-out players a separate status track.
</details>

## Week 8: Griefing, typology and design responses

Lecture: [w08-griefing-typology-and-design-responses.md](../lectures/w08-griefing-typology-and-design-responses.md).

32. *Week 8 · compute · new case.* A city has `N = 2,000` players, exit rate `γ = 0.4` per minute, contact `β = 0.3`, and a reservoir of `C = 10` permanent carriers. (a) What is `R0`? (b) Estimate `I*` with the amplifier approximation. (c) Compute `I*` exactly with the quadratic.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.75. (b) 30. (c) 28.4.

(a) `R0 = 0.3 / 0.4 = 0.75`.

(b) `I* ≈ C × R0 / (1 − R0) = 10 × 0.75 / 0.25 = 30`.

(c) `a = 0.3 × 1,990 − 0.4 × 2,000 = 597 − 800 = −203`. `a² + 4β²NC = 41,209 + 4 × 0.09 × 2,000 × 10 = 41,209 + 7,200 = 48,409`, whose square root is 220.0. `I* = (−203 + 220.0) / 0.6 = 28.4`.

The approximation is close here because `R0` is well below 1 and `I*` is small next to `N`.
</details>

33. *Week 8 · compute · new case.* In the city from question 32, 20 players are infected at minute 0. Compute `I(1)`. Is the city above or below its steady state, and which way will it move?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `I(1) = 20.91`. Below the steady state of 28.4, so it rises.

New infections `= 0.3 × 1,980 × (20 + 10) / 2,000 = 8.91`. Exits `= 0.4 × 20 = 8`. `I(1) = 20 + 8.91 − 8 = 20.91`.

Inflow exceeds outflow by 0.91, so the count climbs toward 28.4. The reservoir keeps the plague alive even though `R0 < 1`.
</details>

34. *Week 8 · explain · new case.* A city of `N = 1,000` has `γ = 0.5` and crowded contact `β = 0.8`. Compute `I*` for four cases: (a) `C = 0`, (b) `C = 15`, (c) contact halved to `β = 0.4` with `C = 15`, (d) halved contact and `C = 0`. Then explain which lever is binding at each contact level.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 375. (b) 397.7. (c) 47.9. (d) 0.

(a) `R0 = 1.6`, so `I* = 1,000 × (1 − 1/1.6) = 375`.

(b) Quadratic with `a = 0.8 × 985 − 500 = 288`: `I* = (288 + √(288² + 4 × 0.64 × 1,000 × 15)) / 1.6 = (288 + 348.3) / 1.6 = 397.7`.

(c) `R0 = 0.8`. `a = 0.4 × 985 − 500 = −106`, `I* = (−106 + √(11,236 + 9,600)) / 0.8 = (−106 + 144.3) / 0.8 = 47.9`. The approximation `15 × 0.8 / 0.2 = 60` is in range and high.

(d) `R0 < 1` with no reservoir, so the outbreak dies out.

At `β = 0.8` the plague sustains itself, so removing all 15 carriers only moves `I*` from 398 to 375. Contact is binding. At `β = 0.4` contact is under the threshold, and the 15 carriers alone hold 48 players sick. The reservoir is binding. The two levers work only together, the lecture's reading of Corrupted Blood.
</details>

35. *Week 8 · critique · new case.* Classify each incident with Foo and Koivisto's four types, say whether it is reaction-driven or gain-driven, and pick the response family from section 3 that fits best. (a) A player sells a "guaranteed rare-drop location" for gold and the location is invented. (b) A max-level player stands on a quest giver so low-level players cannot click it, and dances when they complain. (c) A max-level player repeatedly kills the same low-level player at their respawn point. (d) A player harvests every herb node along a questing route while others are fighting nearby, never grouping.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Scamming, gain-driven. (b) Harassment, reaction-driven. (c) Power imposition, reaction-driven. (d) Greed play, gain-driven.

(a) Remove the payoff or the route. A reputation mark raises the cost, and a trade that holds payment until the service is delivered removes the route. A mute button does nothing, because the scammer wants the gold, not a reaction.

(b) Remove the route (no player collision at quest givers) or the audience (let victims hide the griefer). Punishment alone may feed the reaction the griefer wants.

(c) Consent or respawn-location changes remove the payoff and the route. A level-gap PvP rule is the classic fix.

(d) Remove the payoff. Per-player nodes, as in Guild Wars 2 gathering from week 14, make the second player cost you nothing.

A designer who answers (b) with loot changes or (a) with a mute button is solving the wrong problem.
</details>

## Week 9: Toxicity, research and interventions

Lecture: [w09-toxicity-research-and-interventions.md](../lectures/w09-toxicity-research-and-interventions.md).

36. *Week 9 · compute · new case.* A 3v3 arena game (`n = 6`) has `p = 3%` persistent offenders with `r_h = 0.35` and occasional offenders with `r_o = 0.025`. Compute `q`, the share of incidents from each group, and the share of toxic matches.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `q = 0.03475`, occasional 69.8%, persistent 30.2%, toxic matches 19.1%.

`q = 0.97 × 0.025 + 0.03 × 0.35 = 0.02425 + 0.0105 = 0.03475`. Occasional share `0.02425 / 0.03475 = 69.8%`. Persistent share `0.0105 / 0.03475 = 30.2%`. Toxic matches `1 − (1 − 0.03475)^6 = 1 − 0.809 = 19.1%`.

Each persistent player commits 14 times the incidents of an ordinary one, and the persistent group still causes under a third of the total.
</details>

37. *Week 9 · compute · new case.* For the game in question 36, compute `q` after, the share of incidents removed and the toxic-match share for (a) catching 60% of persistent offenders, (b) perfect detection, (c) a situational change that lowers everyone's rate by 15%, and (d) (a) and (c) together.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Intervention | `q` after | Removed | Toxic matches |
|---|---|---|---|
| None | 0.03475 | 0% | 19.1% |
| (a) `k = 0.6` | 0.02845 | 18.1% | 15.9% |
| (b) `k = 1` | 0.02425 | 30.2% | 13.7% |
| (c) `x = 0.15` | 0.02954 | 15.0% | 16.5% |
| (d) both | 0.02418 | 30.4% | 13.7% |

(a) `0.02425 + 0.0105 × 0.4 = 0.02845`. (b) `0.02425`, the ceiling on punishment. (c) `0.85 × 0.03475 = 0.02954`. (d) `0.85 × 0.02845 = 0.02418`.

Here the persistent share (30%) is larger than in the lecture's example (25%), so 60% recall beats a 15% situational change. The combination still matches perfect detection, because the two act on different parts of `q`.
</details>

38. *Week 9 · compute · new case.* A detection system catches 80% of persistent offenders and wrongly flags 0.2% of everyone else. The game has 20,000 players, 3% of them persistent. (a) How many correct and wrong punishments per cycle, and what is the precision? (b) What false-positive rate would give 95% precision?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 480 correct, 38.8 wrong, precision 92.5%. (b) At most about 0.13%.

(a) Correct `0.8 × 0.03 × 20,000 = 480`. Wrong `0.002 × 0.97 × 20,000 = 38.8`. Precision `480 / 518.8 = 92.5%`.

(b) For 95% precision the wrong count must be at most `480 / 19 = 25.3`. That needs `fpr ≤ 25.3 / 19,400 = 0.13%`.

The innocent group is 32 times larger than the guilty one, so a fraction of a percent of false positives becomes dozens of wrongly punished players.
</details>

39. *Week 9 · critique.* A studio's plan says: "Toxicity is caused by a toxic 2%. We will ban them and cut toxic matches by 80%." Critique the plan with the lecture's example numbers, and say what evidence the studio should collect before choosing.

<details>
<summary>Answer and worked solution</summary>

**Answer:** In the lecture's example the persistent 2% cause 25.4% of incidents, so even perfect detection removes about a quarter of incidents and toxic matches fall from 33.1% to 25.8%, not by 80%.

With `p = 2%`, `r_h = 0.5`, `r_o = 0.03`, `q = 0.0394`, of which `0.01 / 0.0394 = 25.4%` is persistent. Catching all of them gives `q = 0.0294` and `1 − 0.9706^10 = 25.8%` toxic matches. And a real detector is not perfect. At `k = 0.7` with a 0.5% false-positive rate it punishes 49 innocent players for every 140 guilty ones.

The evidence to collect first is the split: count incidents per player in the studio's own data and see how concentrated they are. If `p × r_h` is most of `q`, bans will work. If not, as Riot reported for League, situational design (surrender rules, role selection, matchmaking that avoids stomps) has to carry most of the reduction, tested with an A/B experiment.
</details>

## Week 10: Communication design, chat, emotes, pings

Lecture: [w10-communication-design-chat-emotes-pings.md](../lectures/w10-communication-design-chat-emotes-pings.md).

40. *Week 10 · compute · new case.* A city channel has `L = 800` listeners. 8% of them post, each at 0.6 messages a minute. Readers manage `R = 15` messages a minute and the window shows `W = 12` lines. Compute `M`, the on-screen lifetime `T`, coverage, audience per message and the saturation point `L*`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `M = 38.4` a minute, `T = 18.75 s`, coverage 39.1%, audience 312.5, `L* = 312.5`.

`M = 0.08 × 800 × 0.6 = 38.4`. `T = 60 × 12 / 38.4 = 18.75` seconds. `c = 15 / 38.4 = 39.1%`. `A = 800 × 0.391 = 312.5`. `L* = 15 / (0.08 × 0.6) = 312.5`.

The channel is saturated, and the audience per message equals `L*` exactly, as the model predicts. Doubling the city's population would halve `T` and leave `A` at 312.5.
</details>

41. *Week 10 · compute · new case.* Use the keystroke-level model (`M = 1.35 s`, `K = 0.28 s`, `P = 1.1 s`) to price a typed "stack on me" (11 characters, plus a key to open chat and one to send) against a one-key ping on a target already in view and a ping on the minimap. By what factor is the in-view ping faster?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Typed 4.99 s, in-view ping 1.63 s, minimap ping 2.73 s. The in-view ping is about 3.1 times faster.

Typed `= 1.35 + 13 × 0.28 = 1.35 + 3.64 = 4.99` s. In-view ping `= 1.35 + 0.28 = 1.63` s. Minimap ping adds pointing, `1.35 + 1.1 + 0.28 = 2.73` s. Ratio `4.99 / 1.63 = 3.06`.

The gap is far smaller than the lecture's 35-character callout (11.71 s), which is why short typed macros survive in games with pings. Pings win most on long, specific messages and on reading in the play space.
</details>

42. *Week 10 · compute · new case.* Take the lecture's 1,000-listener channel (`s = 0.1`, `r = 0.5`, `R = 20`, `W = 10`). Twenty of the 100 posters start reposting at 3 messages a minute while the other 80 stay at 0.5. Compute the channel rate, coverage, line lifetime, and reader-views per minute for a spammer and for a polite poster. Compare the polite poster with the no-spam case.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `M = 100`, coverage 20%, lifetime 6 s, spammer 600 views a minute, polite poster 100, down from 200.

`M = 20 × 3 + 80 × 0.5 = 60 + 40 = 100`. `c = 20 / 100 = 20%`, so each message reaches `1,000 × 0.2 = 200` readers. `T = 600 / 100 = 6` seconds.

A spammer gets `3 × 200 = 600` reader-views a minute. A polite poster gets `0.5 × 200 = 100`. Before the spam, a polite poster had `0.5 × 400 = 200`. The spammers took half of every polite poster's attention and got six times as much each.
</details>

43. *Week 10 · design · new case.* A server's trade channel has `L = 1,200`, `s = 0.1`, `r = 0.5`, `R = 20`. The design goal is that a reader who follows one channel sees at least 60% of its messages. Into how many topic channels, followed evenly, should you split it? What does the split do for a seller's audience per message, and what else would you add?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 2 channels. Readers see 66.7% of their channel, but a seller's audience per message stays at 400.

Coverage `c = R / (s × L_channel × r) ≥ 0.6` needs `L_channel ≤ 20 / (0.6 × 0.05) = 666.7`. Split 2 gives 600 listeners each, `M = 30`, coverage `20 / 30 = 66.7%`.

Each channel is still saturated (`L* = 400`), so audience per message is `600 × 0.667 = 400`, the same as before the split. Readers win, posters do not (lab 10 finds the same). The larger lever is removing the need to post. An auction house or a group finder turns broadcasts into searches and lowers `s` in the channel toward zero.
</details>

44. *Week 10 · critique.* A producer proposes merging every city's trade channel into one server-wide channel "so every seller reaches the whole market." Critique the proposal with the model and give a better route to the same goal.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Past saturation `L` cancels. A bigger channel does not give any seller a bigger audience per message. It only shortens each line's lifetime and strengthens the spam incentive.

Audience per message is `min(L, R / (s × r))`. Once the merged channel passes `L* = R / (s × r)`, every message reaches the same `R / (s × r)` readers whatever `L` is. Merging raises `M`, shortens `T`, and pays posters who repost more often, which drives `r` up and coverage down for everyone.

WoW's own Trade design already made this trade: it links all capitals on a realm, because one market is easier to search, and in patch 9.2.7 it split services off into a second channel. The better route to "every seller reaches the whole market" is a searchable listing tool (an auction house or a services board), which replaces broadcast with search. If a merged channel is kept, pair it with a per-poster rate cap.
</details>

## Week 11: Newcomers and mentoring systems

Lecture: [w11-newcomers-and-mentoring-systems.md](../lectures/w11-newcomers-and-mentoring-systems.md).

45. *Week 11 · compute · new case.* A game's newcomers have solo churn `a = 0.12`, tied churn `b = 0.03` and connection rate `p = 0.03`. Compute `R₁` and `R₂` by hand, the share who ever attach, and the expected length of the connection clock.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `R₁ = 0.88`, `R₂ = 0.777`, ever attach 20%, clock 6.7 days.

`U₁ = 1 × 0.85 = 0.85`, `A₁ = 0.03`, `R₁ = 0.88`.

`U₂ = 0.85 × 0.85 = 0.7225`. `A₂ = 0.03 × 0.97 + 0.85 × 0.03 = 0.0291 + 0.0255 = 0.0546`. `R₂ = 0.7771`.

Ever attach `p / (a + p) = 0.03 / 0.15 = 20%`. Clock `1 / (a + p) = 6.7` days.
</details>

46. *Week 11 · explain · new case.* For the game in question 45, compare two changes. A tutorial cuts `a` to 0.09. A mentor channel raises `p` to 0.05. Compute retention at days 7, 30 and 60 for each, and the attached share of day-30 survivors. Explain why this result differs from the lecture's table, and what it means for how you evaluate the two.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Design | Day 7 | Day 30 | Day 60 | Attached share at day 30 |
|---|---|---|---|---|
| Baseline | 44.2% | 10.6% | 4.0% | 93% |
| Tutorial, `a = 0.09` | 54.2% | 14.8% | 5.4% | 85% |
| Mentoring, `p = 0.05` | 46.3% | 14.6% | 5.7% | 97% |

Iterate the update rule, or use the closed form `R[t] = qᵗ + p((1 − b)ᵗ − qᵗ)/(a + p − b)`.

The tutorial wins at day 7 and still narrowly at day 30. The mentoring curve crosses it on day 33 and leads at day 60. In the lecture the crossing came around day 20. Two things moved it. The mentoring change here is smaller (`p` rises by 0.02, not 0.04), and tied churn is higher (`b = 0.03`), so the attached group drains faster and the payoff of attachment takes longer to show.

The general point holds. The two changes act on different parts of the curve, and which one "wins" depends on the horizon. Report retention at several horizons and the attached share, or measure `p` directly, and choose the horizon before running the test.
</details>

47. *Week 11 · compute.* FFXIV's Novice Network holds 100 mentors and 412 new adventurers per instance. (a) A busy evening brings 3,000 new adventurers online. How many instances are needed, and how many mentors fill every mentor slot? (b) Only 300 mentors are online. What is the ratio of new adventurers to mentors, compared with a full instance?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 8 instances and 800 mentors. (b) 10 per mentor, against about 4.1.

(a) `3,000 / 412 = 7.28`, so 8 instances. Filling every slot takes `8 × 100 = 800` mentors.

(b) `3,000 / 300 = 10` new adventurers per mentor, against `412 / 100 = 4.12` in a full instance. If `p` depends on how many newcomers can talk to a mentor, the mentor stock is a live-ops metric, as the lecture's design judgment says.
</details>

48. *Week 11 · critique.* A studio reports: "Mentor channel A/B test: +2 points of day-7 retention. Mentors are players with 500 hours played. Not worth the moderation cost. Cancelling." Critique both the metric and the eligibility rule, and say what the studio should have measured.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Day 7 is the wrong horizon for a connection change, and hours played is a weak filter for helpers.

A mentor program acts on `p`. Its effect appears after the unattached group drains, weeks later. In the lecture's table, mentoring gained 4 points at day 7 and 11 at day 30. A 2-point day-7 gain is consistent with a meaningful day-30 gain. The studio should read day-30 retention, the attached share of survivors, or `p` estimated directly from player-days (lab 11).

Hours played says nothing about patience or conduct. It admits players who answer rudely (raising `a`) or use the channel as a stage (burying questions, lowering `p`). FFXIV's rule combines a record of play with strangers (1,000 duties), thanks from them (1,500 commendations) and role quests. A better rule adds a clean conduct record and removal after upheld reports.
</details>

## Week 12: Community management

Lecture: [w12-community-management.md](../lectures/w12-community-management.md).

49. *Week 12 · compute · new case.* (a) 15% of players dislike a change and unhappy players post 5 times as often as content ones. What share of the forum is negative? (b) Another forum is 65% negative. Report the implied unhappy share for voice ratios of 2, 4 and 6.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 46.9%. (b) 48.1%, 31.7% and 23.6%.

(a) `o = 0.15 × 5 / (0.75 + 0.85) = 0.75 / 1.6 = 46.9%`. One player in seven is unhappy and nearly half the forum is negative.

(b) `d = o / (o + ρ(1 − o))` with `o = 0.65`. At `ρ = 2`: `0.65 / 1.35 = 48.1%`. At 4: `0.65 / 2.05 = 31.7%`. At 6: `0.65 / 2.75 = 23.6%`. Without an estimate of `ρ`, the forum is consistent with anything from under a quarter to about half the players.
</details>

50. *Week 12 · compute · new case.* A game has 80,000 active players. 30% dislike a patch and post about it at 2%. The content 70% post at 1%. How many negative and positive posters are there, what share of posters is negative, and what share of players posted at all?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 480 negative, 560 positive, 46.2% negative, 1.3% of players posted.

Negative `80,000 × 0.30 × 0.02 = 480`. Positive `80,000 × 0.70 × 0.01 = 560`. Negative share `480 / 1,040 = 46.2%`, against a true 30% (`ρ = 2`). Posters are `1,040 / 80,000 = 1.3%` of players, in line with Nielsen's participation inequality.
</details>

51. *Week 12 · compute · new case.* A random survey of 500 active players finds 18% unhappy with a change. The forum's negative share of posters is 55%. (a) Give an approximate 95% interval for `d`. (b) Estimate `ρ` from the point estimate and at both ends of the interval. (c) Write the one-sentence report you would send the design team.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 14.6% to 21.4%. (b) 5.6, with a range of about 4.5 to 7.2. (c) See below.

(a) `SE = √(0.18 × 0.82 / 500) = 0.0172`, so `0.18 ± 1.96 × 0.0172 = 0.18 ± 0.034`.

(b) `ρ = o(1 − d) / (d(1 − o))`. At `d = 0.18`: `0.55 × 0.82 / (0.18 × 0.45) = 5.57`. At `d = 0.146`: 7.22. At `d = 0.214`: 4.50. A higher `d` means a smaller `ρ`.

(c) "The forum is 55% negative, but a random survey of 500 players puts dissatisfaction at 15% to 21%, so posters on this topic are about 4.5 to 7 times more likely to be unhappy than the player base." Record the `ρ` range for reuse on similar topics.
</details>

52. *Week 12 · explain · new case.* After a patch, the forum is only 25% negative and the team is relieved. A week later, a survey of players who logged in during the patch week finds 35% unhappy, and churn is up. Compute the voice ratio and explain it in Hirschman's terms. What would you change about the team's weekly report?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `ρ ≈ 0.62`. Unhappy players are choosing exit over voice.

`ρ = 0.25 × 0.65 / (0.35 × 0.75) = 0.1625 / 0.2625 = 0.62`. Unhappy players post at under two thirds the rate of content ones.

In Hirschman's terms, unhappy players are leaving without complaining, perhaps because they no longer believe voice works or because exit is cheap. A calm forum during a churn rise is a warning.

The weekly report should never read forum sentiment alone. Pair each topic's `o` with a behavioural measure (churn, playtime) and, where possible, a survey, and flag any topic where the forum is calm and exit rises. The survey here was drawn from players who logged in that week, so it may still miss players who had already left, which would push the true `d` higher.
</details>

## Week 13: Ethnography of online worlds

Lecture: [w13-ethnography-of-online-worlds.md](../lectures/w13-ethnography-of-online-worlds.md).

53. *Week 13 · compute · new case.* A server has three groups. 70% of players play 3 hours a week, 25% play 15 and 5% play 50. (a) What is the true mean? (b) What share of the people an in-game observer meets comes from each group? (c) What mean hours will the observer's honest interviewees report? Check it with the variance form.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 8.35 hours. (b) 25.1%, 44.9% and 29.9%. (c) 22.46 hours.

(a) `0.7 × 3 + 0.25 × 15 + 0.05 × 50 = 2.1 + 3.75 + 2.5 = 8.35`.

(b) `q_i = p_i h_i / 8.35`: `2.1 / 8.35 = 25.1%`, `3.75 / 8.35 = 44.9%`, `2.5 / 8.35 = 29.9%`. The 5% who play 50 hours are three in ten encounters.

(c) `Σ p h² = 0.7 × 9 + 0.25 × 225 + 0.05 × 2,500 = 6.3 + 56.25 + 125 = 187.55`, and `187.55 / 8.35 = 22.46`. Variance `= 187.55 − 8.35² = 117.83`, and `8.35 + 117.83 / 8.35 = 22.46`. Both forms agree, at 2.7 times the true mean.
</details>

54. *Week 13 · compute · new case.* You interviewed 40 players you met in a city hub. Twenty-four said they play about 30 hours a week and sixteen said about 6. Estimate the population share of 30-hour players. What does your raw sample say, and why is the corrected number still uncertain?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 23.1%, against 60% in the raw sample.

Weight each person by `1/h`: `24 / 30 = 0.8` and `16 / 6 = 2.667`. The 30-hour share is `0.8 / 3.467 = 23.1%`.

The estimate assumes self-reported hours are accurate and that meeting chance is proportional to hours in that hub. Self-reports are noisy, and the error need not be the same for both groups, so report the raw and corrected numbers together. The correction also cannot recover the reasons of light players you barely met. Only targeted recruitment can.
</details>

55. *Week 13 · compute · new case.* You plan 12 one-hour observation sessions spread over the week. (a) What is the chance of seeing a particular 6-hour-a-week player at least once? (b) How many sessions would give an 80% chance?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 35.4%. (b) 45 sessions.

(a) `1 − (1 − 6/168)^12 = 1 − 0.9643^12 = 1 − 0.646 = 35.4%`.

(b) Solve `1 − (1 − 6/168)^k ≥ 0.8`: `k ≥ ln 0.2 / ln 0.9643 = 44.25`, so 45 sessions. That is far more than a student project can run, which is why the lecture recommends recruiting light players directly or counting unique people with an automated census.
</details>

56. *Week 13 · compute · new case.* A five-member guild's friendship network has ties A-B, A-C, A-D, B-C and B-E. Compute the mean number of friends per member and the mean number of friends of a randomly chosen friend. Explain the gap in one sentence.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 2.0 and 2.4.

Degrees are A 3, B 3, C 2, D 1, E 1. Mean `10 / 5 = 2.0`. Mean friends of a friend `Σ d² / Σ d = (9 + 9 + 4 + 1 + 1) / 10 = 24 / 10 = 2.4`.

Picking a friend means picking the end of a friendship, so well-connected members are picked more often, the same length bias as meeting players in proportion to their hours.
</details>

57. *Week 13 · critique.* A student's field observation plan says: "I will join a small roleplay guild's voice chat without mentioning my project, record it, and quote the best lines with character names in my report. I will also count players on the bank steps of the capital city." Critique the plan against the week 13 ethics rules and the course's field observation brief.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The voice-chat part is not allowed as written. The bank-steps count is fine.

Joining a guild's voice chat is a private space. Consent scales with intimacy, so this needs the gatekeeper's and members' consent, and the course's field observation keeps to public spaces unless the instructor approves otherwise. Recording without telling anyone is covert observation of a private space.

Quoting chat with character names breaks two rules. Public (or here, semi-private) is not fair game, so paraphrase. And character names are searchable identities, so they need pseudonyms, as do guild and server names when the community is small.

Counting players on the bank steps is observation of a public space and needs no consent. The student should still use pseudonyms in the sighting sheet and correct the counts for length bias.
</details>

## Week 14: Designing for positive social play

Lecture: [w14-designing-for-positive-social-play.md](../lectures/w14-designing-for-positive-social-play.md).

58. *Week 14 · compute · new case.* A hunting spot has `S = 5` spawns a minute. Monsters have `H = 1,200` health, players deal `d = 60` damage per second and spend `t_s = 12` seconds searching. (a) Compute solo capacity `c` and the crossover `n* = S/c` for exclusive tagging. (b) Compute `r(2)` and `r(3)` under rule A, rule B and rule C with `s = 0.4`. (c) Give `Δr(2)` for each rule and say what the third player feels like.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `c = 1.875`, `n* = 2.67`. (b) and (c) below.

(a) Solo cycle `1,200 / 60 + 12 = 32` seconds, so `c = 60 / 32 = 1.875`. `n* = 5 / 1.875 = 2.67`, so the third player tips the spot into competition.

(b) and (c):

| Rule | `r(2)` | `r(3)` | `Δr(2)` | Third player |
|---|---|---|---|---|
| A, exclusive | 1.875 | 1.667 | −0.208 | a thief |
| B, shared | 2.727 | 3.214 | +0.487 | help |
| C, `s = 0.4` | 2.308 | 2.500 | +0.192 | mild help |

Rule A: `min(1.875, 5/3) = 1.667`. Rule B at `n = 3`: kill time `1,200 / 180 = 6.67` s, cycle 18.67 s, `r = 3.214`. Rule C at `n = 3`: health `1,200 × 1.8 = 2,160`, kill time 12 s, cycle 24 s, `r = 2.5`.
</details>

59. *Week 14 · compute · new case.* In the spot from question 58, eight players share credit under rule B. (a) How many credited kills per minute does the spot produce, and how many times the rule A total is that? (b) How long does a kill take, against the solo 20 seconds? (c) With a damage threshold of 6% for loot credit, how many equal contributors can all qualify?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 33.1 a minute, 6.6 times. (b) 2.5 seconds. (c) 16.

(a) Rule B at `n = 8`: kill time `1,200 / 480 = 2.5` s, cycle 14.5 s, `r = 4.138`. Spot credits `8 × 4.138 = 33.1`. Rule A's total is capped at `S = 5`, so the multiplier is `33.1 / 5 = 6.6`.

(b) 2.5 seconds, an eighth of the solo fight. Fine for a quest mob and useless for a boss.

(c) All qualify while `1/n ≥ 0.06`, so `n ≤ 16.7` and the answer is 16.
</details>

60. *Week 14 · design · new case.* Using the lecture's spot (`H = 1,000`, `d = 50`, `t_s = 10`), the design goal is that a second player raises each player's rate from 2.0 to exactly 2.2 kills a minute, a small positive `Δr`. What scaling factor `s` does rule C need? How long does the fight last with two players, against 20 seconds solo?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `s ≈ 0.727`, and the fight lasts about 17.3 seconds.

Rule C at `n = 2`: `60 / (1,000(1 + s) / 100 + 10) = 2.2`. So `10(1 + s) + 10 = 27.27`, `1 + s = 1.727` and `s = 0.727`.

Kill time with two players is `1,000 × 1.727 / 100 = 17.3` seconds. The fight stays close to its solo length, the stranger is mild help (`Δr(1) = +0.2`), and the spot's faucet grows much more slowly than under rule B. The trade-off is that each player feels the other's help only a little.
</details>

61. *Week 14 · critique.* A designer adds a "thank" button after dungeons. Each thank gives the recipient 10 gold, with no limits. Predict what happens in the first week and redesign it using the four-part rule from section 3.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Pairs and bots will thank each other in loops to mint gold. The button becomes an uncapped faucet and stops meaning anything.

Any reward for helping becomes a reward for appearing to help. With no cap and no pair limit, two friends can trade thanks every run, and bot groups can farm it continuously.

The four-part rule gives the redesign. Cap how often an act can be rewarded (for example 2 per dungeon, as Overwatch's endorsements cap at 2 per match). Stop the same pair trading it back and forth (a per-pair time window, Overwatch uses 12 hours). Make the reward decay, so standing measures recent behaviour. Pay in something the player values beyond currency, such as a standing level that unlocks chat or cosmetics, instead of tradeable gold.
</details>

## Integrative questions

These draw on several weeks. They are the closest match to viva questions on the final design.

62. *Weeks 3 and 6 · design · new case.* A 5-player cross-server queue draws from about 5,000 players. Players run about 20 dungeons a month. (a) What is the chance a given partner appears again within the next 20 runs, and how does it compare with Axelrod's bar of about 0.5 to 0.67? (b) Propose a reputation setting (`λ`, `a`, `b`) for the queue and give its newcomer score, half-life and ceiling. (c) Name the attack your setting is weakest against.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 1.6%, far below the bar. (b) One defensible setting is `λ = 0.95`, `a = 1`, `b = 3`, with newcomer 0.25, half-life 13.5 matches, ceiling 0.875. (c) Whitewashing is reduced but not removed, and the dues fall on honest newcomers.

(a) `p = 4 / 4,999 = 0.0008`, so `1 − (1 − p)^20 = 1.6%` (the week 3 table rounds this to 2%). Repeat meetings cannot carry cooperation here, so reputation must extend the shadow of the future.

(b) Newcomer `a / (a + b) = 1/4 = 0.25`. Half-life `ln 0.5 / ln 0.95 = 13.5`. Memory 20, so the ceiling is `(20 + 1) / (20 + 4) = 0.875`. Other settings earn full marks if the numbers are right and the choice is argued from the behaviour to catch.

(c) With free accounts, an always-bad player settles at `1 / 24 = 0.042` and gains about sixfold by starting over at 0.25. An entry fee or an account-level identity makes that more expensive. The second weak point is role bias in who gets rated, which calls for restricting and limiting who may rate.
</details>

63. *Weeks 4 and 5 · design · new case.* A raiding guild sits at 22 active members with `M = 20` and `R = 2` a week. The officers want to switch to earned-spent DKP with `e` set so that `ρ = 2`, to reward veterans. The raid has 20 players and 4 items a night. (a) Estimate the first-item wait for a recruit who joins after 40 nights. (b) Explain, using the week 4 model, why this loot rule could push the guild across its threshold. (c) Propose a rule that still rewards seniority.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 43 nights. (b) It lowers `R` and raises `c` for recruits and part-timers, with a margin of only 2 members. (c) For example, zero-sum with a small attendance bonus balanced by decay or a balance cap.

(a) `20/4 + 40 × 1 × 19/20 = 5 + 38 = 43` nights, about five months at two raids a week.

(b) Recruits who see a 43-night wait are less likely to join or stay, which lowers `R`. Part-timers fall behind for good under inflation (week 5's attendance table), which raises `c`. The guild has 2 members of margin above `M`. Once it drops below, churn switches to `c_high` and the rescue condition `R > c_high × M` asks for more recruiting at exactly the moment the loot rule is scaring recruits off.

(c) Seniority can be rewarded without growing the recruit gap. Options are a fixed cap on balances, which bounds the gap at the cap, EPGP-style decay, which stops the gap growing with guild age, or a separate non-loot reward for tenure such as a rank or title (a week 7 time signal).
</details>

64. *Weeks 7, 9 and 14 · critique · new case.* A game shows an endorsement level on each player. Model "high endorsement" as a status signal for good conduct. Suppose 60% of players behave well, 50% of them reach a high level, and 20% of poorly behaved players also reach it through friends endorsing each other. (a) Compute the signal's precision and lift. (b) A 12-hour per-pair limit cuts the friend route to 5%. Recompute. (c) Why is lift low in both cases, and what does that mean for how the level should be used?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Precision 78.9%, lift 1.32. (b) Precision 93.8%, lift 1.56. (c) Good conduct is common, so no signal can raise the odds much above the base rate.

(a) `f = 0.6 × 0.5 + 0.4 × 0.2 = 0.38`. Precision `0.30 / 0.38 = 78.9%`. Lift `0.789 / 0.6 = 1.32`.

(b) `f = 0.30 + 0.4 × 0.05 = 0.32`. Precision `0.30 / 0.32 = 93.8%`. Lift `1.56`.

(c) Lift is capped at `1 / s`, here `1 / 0.6 = 1.67`. A signal of a common trait tells you little about any one holder. It tells you more about the rare players who lack it. So the level works better as a gate on the low end (as Overwatch gates text chat below level 2) than as a badge of distinction at the top. The pair limit is still worth having, because it removes most of the collusion route.
</details>

65. *Weeks 11, 12 and 13 · design · new case.* Your final proposal includes a mentor program, and you must plan the study that will evaluate it. Assume the lecture's baseline and mentoring values (day-7 retention 50.1% and 54.1%, day-30 retention 12.6% and 23.7%). (a) How should the study assign players, and why? (b) You want the standard error of the difference between groups to be at most one third of the expected gap. How many players per group does that take for a day-30 comparison, and for a day-7 comparison? (c) Name one bias from weeks 12 or 13 the study design must avoid.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Randomise the invitation. (b) About 213 per group at day 30 and about 2,803 at day 7. (c) For example, recruiting study participants through the forum or by meeting them in-game.

(a) Players who choose to join a mentored channel differ from those who do not. Randomising the invitation, as the Teahouse study did, separates the effect of the program from the kind of player who seeks help.

(b) The standard error of a difference of two proportions with `n` per group is `√((p₁(1 − p₁) + p₂(1 − p₂)) / n)`. At day 30, `0.126 × 0.874 + 0.237 × 0.763 = 0.2910`. The gap is 11.1 points, so the target SE is 0.037 and `n ≥ 0.2910 / 0.037² = 212.5`, so 213. At day 7, `0.501 × 0.499 + 0.541 × 0.459 = 0.4983`. The gap is 4.0 points, the target SE is 0.0133 and `n ≥ 0.4983 / 0.0133² = 2,803`. The day-30 test takes longer and needs far fewer players, because the effect it looks for is almost three times larger.

(c) Surveying players through the forum brings in the voice ratio of week 12. Interviewing players met in-game brings in the length bias of week 13, oversampling heavy players who are the most likely to be attached anyway. Sample by account from the cohort log instead.
</details>
