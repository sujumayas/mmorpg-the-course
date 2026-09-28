# MMO301 · Exam bank: quiz, practice and viva questions

MMO301 has no written exam. The grade comes from three pieces of coursework, the case studies (40%, [case-studies-brief.md](case-studies-brief.md)), the player-type critique (20%, [player-type-critique-brief.md](player-type-critique-brief.md)) and the world design bible (40%, [world-bible-brief.md](world-bible-brief.md)). This bank does three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Weekly quizzes.** Most weeks open with a 10-minute ungraded quiz of two or three questions from this bank, usually one compute question and one explain or critique question.
- **Viva.** Each case study is followed by a 5-minute spot check, and the world bible is defended in a 15-minute viva in week 15. Examiners draw questions in the style of this bank and rewrite them with the numbers from your own sheets and chapters. If your bible says the capital's guards arrive in 20 seconds, expect question 26 with 20 seconds in it.

Every question is tagged with the week or weeks it draws on and a type. Forty-one of the 64 questions (the compute and design ones) ask you to apply a lecture model to numbers or a case you have not seen, and most explain and critique questions do the same with a new proposal.

- **compute**: apply a lecture model to numbers you have not seen before.
- **explain**: say why a model or a historical case behaves the way it does, with a number or a mechanism as evidence.
- **design**: choose values or rules that meet a stated goal and show that they meet it.
- **critique**: find what is wrong with a claim or proposal and say how to fix it.

All numbers are invented unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and era, and no question relies on a game fact the lectures do not state. The worlds in the questions (their realms, bosses, creators and shards) are fictional. Every numeric answer was recomputed in Python. Where rounding matters, the solution says how it was rounded. Write your own answer before you open the solution.

---

## Week 1: What is a virtual world?

1. *Week 1 · compute.* A realm has `C = 1,200` players online. A quarter of them are leveling, spread over 24 zones of 40 view cells each. (a) Find `n`, `M`, `λ` and `P(alone)` for a leveling player, using both `(1 − 1/M)^n` and `e^(−λ)`. (b) How many realms of the same size must share the leveling zones to bring `P(alone)` down to 20% or less? (c) What is `P(alone)` with that many?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `n = 300`, `M = 960`, `λ = 0.3125`, `P(alone)` 73.1% by both formulas. (b) 6 realms. (c) 15.3%.

(a) `n = k × f × C = 1 × 0.25 × 1,200 = 300`. `M = Z × v = 24 × 40 = 960`. `λ = 300 / 960 = 0.3125`. `e^(−0.3125) = 0.7316` and `(1 − 1/960)^300 = 0.7315`. The two agree to three decimals, which is why the lecture says `λ` is the only number you need to remember.

(b) `P(alone) ≤ 0.20` needs `λ ≥ ln 5 = 1.609`. So `n ≥ 1.609 × 960 = 1,545`. One realm gives 300, so `k ≥ 1,545 / 300 = 5.15`. Round up to 6.

(c) `λ = 6 × 300 / 960 = 1.875`, `P(alone) = e^(−1.875) = 15.3%`.
</details>

2. *Week 1 · compute.* On launch day 3,600 players are all in 4 starter zones of 50 view cells each (`f = 1`). (a) What is `λ`? (b) What is the smallest number of parallel copies (layers) that brings `λ` to 2.5 or below? (c) What is `P(alone)` with that many copies?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `λ = 18`. (b) 8 copies. (c) 10.5%.

(a) `M = 4 × 50 = 200`, `λ = 3,600 / 200 = 18`. Every view cell holds about 18 other players.

(b) Splitting into `L` copies sets `k = 1/L`, so `λ = 18 / L`. `18 / L ≤ 2.5` gives `L ≥ 7.2`. Seven copies give `λ = 2.57`, still above the target, so the answer is 8, with `λ = 2.25`.

(c) `e^(−2.25) = 0.105`.
</details>

3. *Week 1 · explain.* A leveling player on your realm is alone 70% of the time. A producer says, "If we pool twice as many players into those zones, players will be alone half as often, about 35%." What does the model predict instead, and roughly how many times as many players would you need to reach 35%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Doubling the players gives 49%, not 35%. Reaching 35% takes about 2.9 times as many players.

`P(alone) = e^(−λ)`. Doubling the players doubles `λ`, and `e^(−2λ) = (e^(−λ))^2`. So the new share is `0.7^2 = 0.49`. Pooling squares the chance of being alone. It does not halve it.

Today `λ = ln(1/0.7) = 0.357`. For 35% you need `λ = ln(1/0.35) = 1.050`, which is `1.050 / 0.357 = 2.94` times as many players in the band.

The producer's intuition treats loneliness as falling in proportion to players. It falls exponentially. Each extra unit of `λ` removes the same fraction of the loneliness that is left, not the same number of percentage points.
</details>

4. *Week 1 · critique.* A studio pools the leveling zones of 12 realms: four in Europe, four in North America and four in Asia. Its dashboard divides all pooled players by the view cells and reports `λ = 2.4`, so `P(alone)` looks like 9%. In any one region's evening, about a third of the pooled players are online. What is wrong with the dashboard, what is the real `P(alone)`, and which week 1 case made the same point?

<details>
<summary>Answer and worked solution</summary>

**Answer:** The dashboard counts players who are asleep. The real `λ` in any region's evening is about `2.4 / 3 = 0.8`, so `P(alone) = e^(−0.8) = 45%`, not 9%.

In the model, `n = k × f × C`, and `C` is players online *now*. Pooling realms from distant time zones adds to `k × C` on paper and adds nobody to your evening. The dashboard's 9% (`e^(−2.4) = 0.091`) describes a world where every pooled player is online at once, which never happens.

World of Warcraft met this in 2012. A hotfix on 20 September 2012, weeks after cross-realm zones arrived in patch 5.0.4, stopped the system from pooling players more than three time zones apart. The fix for the dashboard is to compute `λ` per hour from concurrent players, and to pool realms that share a prime time.
</details>

5. *Week 1 · explain.* Using Bartle's properties, name the one property each product lacks and one class of problem it therefore does not have. (a) A turn-based online strategy game in which each player runs an empire. (b) A tabletop role-playing campaign played over video call. (c) A social VR room where avatars chat and there are no world rules beyond movement.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Real time and character. It has no travel time and no one-body limit, since a player can act everywhere their empire is. (b) Physics, because a human referee decides what happens instead of automated rules. When players try something unexpected, the referee can improvise a ruling, so the game never faces the whole player base probing its rules at scale. (c) Physics. With almost no world rules, there is almost nothing to exploit.

The point of the list is that each near miss removes one property and with it a family of problems. VR is an interface, not a property. The VR room is a chat room with a body, and Bartle's list classifies it by what is on the other side of the headset.
</details>

## Week 2: MUD1, MUDs, MOOs and the text era

6. *Week 2 · compute.* A world opens with `S0 = 1,200` locations, designers add `D = 15` per week and a player explores `v = 45` per week. (a) In a designer-only world, how long until a player runs out? (b) Now let anyone build, with `b = 3` locations per player per week and `q = 0.2`. Find `N*`. (c) With a storage cap `K = 30,000`, find `T_out` and `T_full` at `N = 40` and at `N = 200`. (d) At `N = 200`, what share of storage is junk when it fills?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 40 weeks. (b) `N* = 50`. (c) At 40 players, `T_out = 200` weeks and `T_full = 213.3` weeks. At 200 players, `T_out` is never and `T_full = 46.8` weeks. (d) About 75%.

(a) `S0 / (v − D) = 1,200 / 30 = 40` weeks.

(b) `N* = (v − D) / (q × b) = 30 / 0.6 = 50`.

(c) At `N = 40`, `G = 15 + 0.6 × 40 = 39`, so `T_out = 1,200 / (45 − 39) = 200` weeks. `T_full = (30,000 − 1,200) / (15 + 3 × 40) = 28,800 / 135 = 213.3` weeks. At `N = 200`, `G = 135 > 45`, so nobody runs out. `T_full = 28,800 / 615 = 46.8` weeks.

(d) Junk share `= (1 − q) × b × N × T_full / K = 0.8 × 3 × 200 × 46.83 / 30,000 = 0.749`. The world does not run dry. It fills with rooms nobody wants to visit in under a year.
</details>

7. *Week 2 · design.* Keep question 6's world (`S0 = 1,200`, `D = 15`, `v = 45`, `K = 30,000`) and require storage to last at least 52 weeks. You expect the population to wander between 150 and 500 players. Choose a building policy, as values of `b` and `q`, whose working window contains that whole range. Show that the anyone-builds policy from question 6 fails.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Any policy with `b ≤ 1.078` and `q × b ≥ 0.2` works. One example is `b = 1.0`, `q = 0.3`, which gives a window from 100 to 539 players. The anyone-builds policy gives 50 to 180 and fails above 180 players.

The top of the window is `N_max = ((K − S0) / T_min − D) / b = (553.8 − 15) / b = 538.8 / b`. For `N_max ≥ 500` you need `b ≤ 1.078`.

The bottom of the window is `N* = (v − D) / (q × b) = 30 / (q × b)`. For `N* ≤ 150` you need `q × b ≥ 0.2`.

With `b = 1.0` and `q = 0.3`: `N* = 100`, `N_max = 538.8`. Both ends are inside the requirement.

The anyone-builds policy (`b = 3`, `q = 0.2`) has `N* = 50` and `N_max = 538.8 / 3 = 179.6`. At 500 players its storage fills in `28,800 / 1,515 = 19` weeks.

The design lesson is the LPMud one. The policy that meets the range builds a third as much and needs builders whose work is worth visiting half again as often. In practice that means some filter on who builds, such as an experience threshold or a review.
</details>

8. *Week 2 · critique.* A social platform plans to let every user write scripts for objects that can act on other users' avatars. The pitch says, "Moderation will handle abuse." Using week 2's account of LambdaMOO, write the critique you would give in five sentences or fewer, and name two mechanisms to ship on day one.

<details>
<summary>Answer and worked solution</summary>

**Answer (model).** Scripting that acts on other players is a tool and a weapon at once. LambdaMOO's March 1993 crisis came from a player-built object that made other characters appear to act without consent, so the feature and the harm were the same code. The community there took days and a meeting of nearly three hours without deciding, and a wizard acted alone. Governance comes with building whether you design it or not, and Curtis designed petitions, ballots and an eject command only after the crisis. Informal rules that worked with 40 people online failed with hundreds, so the plan must assume the platform's scale from the start.

Two mechanisms should ship on day one. The first is a per-user consent setting that blocks scripted objects from acting on your avatar unless you allow it. The second is an eject or block command any user can apply to an object or its owner, with a published appeal route. Other good answers include rate limits on scripts that target other avatars and a visible owner label on every scripted object.
</details>

9. *Week 2 · explain.* A designer-only world starts with 3,000 locations and adds 25 per week. Casual players explore 30 new locations a week and the top 5% explore 90. How long until each group runs out? Explain, with the model, why a bigger team building the same kind of content cannot fix the problem for the second group.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Casual players never run out, since `D ≥ v`. The top 5% run out after `3,000 / (90 − 25) = 46.2` weeks.

In a designer-only world `b = 0`, so supply is `D` and does not grow with the population. Content is non-rival, so each player faces their own `v − D`, and the player with the largest `v` sets the requirement. To keep the top group supplied, `D` must reach 90 a week, more than three times the current output, and every week after. The top explorers are also the ones who ask for high-end content loudest. That requirement is the treadmill week 4 names, and the model says why effort alone loses. Supply scales with team size. Demand scales with the fastest player's hours.
</details>

## Week 3: Ultima Online and the resource bank

10. *Week 3 · compute.* A closed world holds `R = 800,000` resource units. It can spawn at most `σ = 25,000` a day. There are 4,000 players who each want 5 units a day, and players return `d = 0.8%` of what they hold each day. (a) What is the steady supply and what share of demand does it meet? (b) How much do players hold at the end of a day in steady state? (c) What `R` would meet demand at this return rate? What `d` would meet it with this `R`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 6,400 a day, 32% of demand. (b) 793,600. (c) `R = 2,500,000`, or `d = 2.5%`.

(a) Demand is `4,000 × 5 = 20,000`. Steady supply is `min(σ, d × R, c × N) = min(25,000, 6,400, 20,000) = 6,400`. Share `6,400 / 20,000 = 32%`.

(b) `H* = (1 − d) × R = 0.992 × 800,000 = 793,600`. Players hold 99.2% of the world.

(c) `R = c × N / d = 20,000 / 0.008 = 2,500,000`, more than three times the world, almost all of it in houses. Or `d = 20,000 / 800,000 = 0.025`.
</details>

11. *Week 3 · critique.* The producer of question 10's world proposes to double `R` to 1,600,000 "so players can get what they need." A designer proposes instead to double `d` to 1.6% by adding consumables that players use up (arrows, food, repair kits). Compare the two on supply and on stock held, and say which Simpson lesson applies to launch timing.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Both give a steady supply of 12,800 a day, 64% of demand. Doubling `R` leaves players holding 1,587,200 units. Doubling `d` leaves them holding 787,200.

Doubling `R`: `s* = 0.008 × 1,600,000 = 12,800`, held `0.992 × 1,600,000 = 1,587,200`. Of the 800,000 units added, 99.2% ends up in players' possession.

Doubling `d`: `s* = 0.016 × 800,000 = 12,800`, held `0.984 × 800,000 = 787,200`.

Same supply, half the stored items. Supply in a closed loop is `d × R`, and `d` is the cheaper lever because it does not grow the hoard. This is what Origin's designers learned when they added resources and watched them flow into houses.

Timing matters. Simpson's lesson is that players accept drains that were there from the start and fight drains added later. Consumables that exist at launch read as part of play. The same consumables added after eight months read as the designers taking things away.
</details>

12. *Week 3 · compute.* A closed world with `R = 300,000` has two kinds of players. Casual players take 80% of each day's harvest and return 3% of their holdings a day. Collectors take 20% and return 0.3%. Spawn capacity and demand are large enough never to bind. (a) Use `s* = R / (1 + Σ ηᵢ(1 − dᵢ)/dᵢ)` from Lab 03 to find the steady supply. (b) Compare it with a world where everyone returns 3%. (c) Explain in one sentence why a minority of collectors does this to everyone.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 3,214 a day. (b) 9,000 a day, so the collectors cut supply by 64%. (c) Supply is what flows back, and collectors hold their share of each day's harvest ten times longer, so most of the world's stock sits with them.

(a) Casual term `0.8 × 0.97 / 0.03 = 25.87`. Collector term `0.2 × 0.997 / 0.003 = 66.47`. `s* = 300,000 / (1 + 25.87 + 66.47) = 300,000 / 93.33 = 3,214`. A day-by-day simulation run for 20,000 days settles on 3,214.3.

(b) With everyone at 3%, `s* = d × R = 9,000`. `1 − 3,214 / 9,000 = 0.643`.

(c) At steady state collectors hold `0.2 × 3,214 × 332.3 ≈ 213,600` units, about 71% of the whole world, while taking only 20% of each day's harvest.
</details>

13. *Week 3 · compute.* A forest holds 1,500 animals. 120 hunters each kill 5 per hour, spread evenly. (a) What is the kill rate per animal and the average lifespan? (b) A herd migration needs an animal to survive 4 hours before it shows. What share of animals get there? (c) How many hunters can the forest take if you want half of all animals to survive 4 hours?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `μ = 0.4` per hour, average lifespan 2.5 hours. (b) 20.2%. (c) 51 hunters.

(a) `μ = P × k / A = 120 × 5 / 1,500 = 0.4`. Average lifespan `1/μ = 2.5` hours.

(b) `e^(−0.4 × 4) = e^(−1.6) = 0.202`.

(c) Need `e^(−4μ) ≥ 0.5`, so `μ ≤ ln 2 / 4 = 0.1733`. `P ≤ 0.1733 × 1,500 / 5 = 52.0`. Since 52 hunters gives `μ = 0.1733...` just above the limit, the safe answer is 51.

This is Garriott's account of the ecology in numbers. Players set the lifespan of anything they can kill, and a behavior that needs hours will never show in a forest where lives last minutes.
</details>

## Week 4: EverQuest, the treadmill and the raid

14. *Week 4 · compute.* A contested boss respawns every 4 days, drops 5 items and is killed by raids of 30. Seven guilds share it in rotation. (a) Find `s`, `i` and `W`. (b) The server grows to 14 guilds. What is `W` now? (c) The same boss is made instanced with a 7-day lockout. What is `W` at 7 guilds and at 14?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `s = 1.75`, `i = 0.0417`, `W = 24` weeks. (b) 48 weeks. (c) 6 weeks at either size.

(a) `s = 7 / 4 = 1.75` spawns a week. `i = s × d / (G × R) = 1.75 × 5 / 210 = 0.0417`. `W = 1 / i = 24` weeks.

(b) `W = G × R / (s × d)` is proportional to `G`, so doubling the guilds doubles the wait to 48 weeks.

(c) `W = L × R / (7 × d) = 7 × 30 / 35 = 6` weeks. `G` does not appear. That one missing symbol is the difference between contested and instanced content.
</details>

15. *Week 4 · compute.* A boss spawns once a week, drops 4 items and needs raids of 25. Five guilds want it, and the strongest takes 60% of spawns. The others split the rest evenly. (a) How long does a raider in the strongest guild wait for one item? (b) In each of the other guilds? (c) Compare both with rotation.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 10.4 weeks. (b) 62.5 weeks. (c) Rotation gives everyone 31.3 weeks.

(a) The top guild kills `0.6` a week. `W = R / (q × s × d) = 25 / (0.6 × 4) = 10.4`.

(b) Each other guild kills `(1 − 0.6) / 4 = 0.1` a week. `W = 25 / (0.1 × 4) = 62.5`, well over a year.

(c) `W = G × R / (s × d) = 125 / 4 = 31.25` for every guild.

The server's supply, 4 items a week, is the same in all three cases. A race only moves it. The winner gets stronger and wins more, which is the positive feedback loop week 4 builds from a respawn timer.
</details>

16. *Week 4 · design.* Ten guilds compete for a contested boss with raids of 40 and 3 drops per kill. You want a raider in rotation to wait no more than 26 weeks for one item. (a) What respawn timer `T` meets the target? (b) If you instance the boss instead, what is the longest lockout `L` that meets it? (c) Name what each choice costs.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `T ≤ 1.36` days. (b) `L ≤ 13.6` days, so a 7-day or 13-day lockout both work. (c) Below.

(a) `W = G × R / (s × d) ≤ 26` needs `s ≥ 400 / 78 = 5.13` spawns a week, so `T = 7 / s ≤ 1.365` days.

(b) `W = L × R / (7 × d) ≤ 26` needs `L ≤ 26 × 21 / 40 = 13.65` days.

(c) The contested boss now spawns more than five times a week. Rivalry, rotation politics and first-kill stories stay, but guilds organize their lives around a spawn every day and a half, and if the server grows the wait grows with it. The instanced boss makes the wait independent of server size, but other guilds stop mattering to your progress and the world becomes a lobby between instances. The decision is whether this reward should be rival.
</details>

17. *Week 4 · explain.* An invented game sets total XP at the end of level `L` to `L³ × H(L)`, with `H = 1.0` up to level 19 and `H = 1.2` from level 20. Compute the XP needed for levels 18 to 19, 19 to 20 and 20 to 21. Explain the pattern and give one way to remove it without changing the total cost of reaching level 21.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 1,027, then 2,741, then 1,513. Level 20 is a hell level.

XP for a level is the difference between two totals. `19³ − 18³ = 6,859 − 5,832 = 1,027`. `20³ × 1.2 − 19³ = 9,600 − 6,859 = 2,741`. `21³ × 1.2 − 20³ × 1.2 = 11,113.2 − 9,600 = 1,513.2`.

The level that crosses the step in `H` pays for the whole jump in the multiplier applied to all of `L³`. The next level is back on the smooth curve. This is the same mechanism the Project 1999 Wiki records for classic EverQuest's stepped level multiplier, where 40 to 41 cost more than 41 to 42.

To remove it, spread the step. For example let `H` rise by 0.04 a level from 16 to 20. Or keep the table of totals fixed and redistribute the per-level costs so they rise smoothly, which is what the September 2002 EverQuest patch note describes doing for levels 50 to 60 while keeping their total cost.
</details>

## Week 5: World of Warcraft and the price of dying

18. *Week 5 · compute.* A player progresses at `g = 0.3` levels per hour. Each death costs `t = 0.2` hours and `x = 0.08` levels. (a) Find `λ*`. (b) Find `P` and waste at one death per hour. (c) Find `P` at two deaths per hour and say what it means.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 2.14 deaths per hour. (b) `P = 0.16` levels per hour, waste 46.7%. (c) `P = 0.02`, almost no progress.

(a) `λ* = g / (g × t + x) = 0.3 / (0.06 + 0.08) = 2.143`.

(b) `P = 0.3 × (1 − 0.2) − 0.08 = 0.16`. Waste `= λ × (t + x / g) = 0.2 + 0.267 = 0.467`.

(c) `P = 0.3 × (1 − 0.4) − 0.16 = 0.02`. Two deaths an hour leaves the player just short of break-even. A slightly worse evening puts them behind where they started.
</details>

19. *Week 5 · design.* A game has `g = 0.2` levels per hour and a runback of `t = 0.1` hours. The team wants an experience penalty but insists that a player dying twice an hour must never go backward. What is the largest `x`? At that `x`, what is `P` at exactly two deaths an hour?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `x ≤ 0.08` levels per death. At the limit `P = 0` at two deaths an hour.

"Never go backward at two deaths an hour" means `λ* ≥ 2`. `0.2 / (0.2 × 0.1 + x) ≥ 2` gives `0.02 + x ≤ 0.1`, so `x ≤ 0.08`.

Check: `P = 0.2 × (1 − 0.2) − 2 × 0.08 = 0.16 − 0.16 = 0`. The limit is a knife edge. A team that wants a margin should pick something like `x = 0.05`, which gives `λ* = 2.86`.
</details>

20. *Week 5 · compute.* A new player progresses at `g = 0.25` and dies 1.5 times an hour. Compare three rules. Rule A: a 9-minute runback, no experience loss. Rule B: a 9-minute runback and 0.05 levels lost. Rule C: an instant respawn nearby (about 1 minute) and 0.05 levels lost. For each, give `(t, x)`, `P`, waste and `λ*`. Which rule hurts this player most, and why does a fast respawn not rescue rule C?

<details>
<summary>Answer and worked solution</summary>

**Answer.**

| Rule | `(t, x)` | `P` | Waste | `λ*` |
|---|---|---|---|---|
| A | (0.15, 0) | 0.194 | 22.5% | 6.67 |
| B | (0.15, 0.05) | 0.119 | 52.5% | 2.86 |
| C | (0.02, 0.05) | 0.168 | 33.0% | 4.55 |

Rule B hurts most. Rule A: `P = 0.25 × (1 − 0.225) = 0.194`, `λ* = 1 / 0.15`. Rule B subtracts `1.5 × 0.05 = 0.075` more. Rule C: `P = 0.25 × (1 − 0.03) − 0.075 = 0.1675`, `λ* = 0.25 / (0.005 + 0.05) = 4.55`.

The experience term `λ × x` does not depend on `t`. Cutting the runback only removes the time term, which for this player is `0.25 × 0.03 = 0.0075` levels an hour in rule C. The experience penalty still costs 0.075. A new player dies most, so the per-death experience loss dominates. That is why Final Fantasy XI, as the lecture describes it, takes no experience at level 30 or lower.
</details>

21. *Week 5 · critique.* A designer on a themepark MMO with queued dungeons says, "Death doesn't matter in our game. Let's add a 5% experience loss on every death at every level." Critique the proposal with the model and the week 5 cases, and offer an alternative that gets some of what the designer wants.

<details>
<summary>Answer and worked solution</summary>

**Answer (model).** Today the game's rule is time-only, so `λ* = 1 / t` and progress can never go negative. Any `x > 0` creates a finite `λ*`, and the players who reach it are new and less skilled players, who die most, and players with short sessions, for whom one bad evening is a large share of the week. In a queued group, one player's deaths also slow four strangers, so the penalty will be blamed on teammates the player will never see again, which is the weak-tie problem the Dungeon Finder already creates.

What the designer wants is caution and tension. Two alternatives do this without taking progress away. First, set `x = 0` below some level and apply a penalty only once players know the game, as Final Fantasy XI does at level 30 and below. Second, move tension into instanced difficulty, where the cost of failure is a failed attempt and a repair bill, which is how WoW has handled it since patch 1.1.0. Whatever rule ships, show `x` to the player before they take the risk.
</details>

## Week 6: EVE Online and the price of a crime

22. *Week 6 · compute.* A hauler has 90,000 EHP. Gank ships deal 700 damage per second and cost 15M ISK each, and half the cargo drops (`p = 0.5`). Use CONCORD's response times from the lecture, 14 s at 0.6 and 19 s at 0.5. (a) Find `n`, `C`, `V*` and `V* / H` at each level. (b) The hauler carries 250M. Where does a gank pay, and what is the expected profit?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) At 0.6, 10 ships, 150M, `V* = 300M`, 3,333 ISK per EHP. At 0.5, 7 ships, 105M, `V* = 210M`, 2,333 per EHP. (b) Only at 0.5, with expected profit 20M.

(a) At 0.6, each ship deals `700 × 14 = 9,800`. `90,000 / 9,800 = 9.18`, so `n = 10`, `C = 150M`, `V* = C / p = 300M`, `300M / 90,000 = 3,333`. At 0.5, each ship deals 13,300. `90,000 / 13,300 = 6.77`, so `n = 7`, `C = 105M`, `V* = 210M`, 2,333 per EHP.

(b) 250M is below 300M at 0.6, so the gank loses money there. At 0.5 it is above 210M. Expected loot `0.5 × 250M = 125M`, minus 105M, is 20M.
</details>

23. *Week 6 · compute.* In question 22, the gankers pull CONCORD before the attack at 0.5, adding about 6 seconds. Recompute `n`, `V*` and the expected profit on the 250M cargo. By what share did the trick lower the safe cargo value?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 6 ships, `V* = 180M`, expected profit 35M. The safe value falls by about 14%.

`T = 25`, so each ship deals `700 × 25 = 17,500`. `90,000 / 17,500 = 5.14`, so `n = 6`. `C = 90M`, `V* = 180M`. Profit `125M − 90M = 35M`. `1 − 180 / 210 = 0.143`.

The lecture's example moved `V*` by 30%, and this one by 14%, because `n` is rounded up. Here 5.14 still needs a sixth ship, so most of the gain from the longer window is lost to rounding. The realized price depends on where the hauler's EHP sits against the steps.
</details>

24. *Week 6 · explain.* With the lecture's assumed gank ships (`a = 500`, `c = 12M`, `p = 0.5`) at 0.5 security (`T = 19`), compare haulers with 57,000 EHP, 57,001 EHP and 66,000 EHP. What does this say about where a hauler should stop adding tank?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 57,000 EHP needs 6 ships and is safe below 144M. Both 57,001 and 66,000 need 7 ships and are safe below 168M.

Each ship deals `500 × 19 = 9,500`. `57,000 / 9,500 = 6.0` exactly, so 6 ships. One more point of EHP needs a seventh ship, and 66,000 (6.95 ships) still needs only seven. `V* = n × 12M / 0.5`.

The safe value rises in steps of `c / p = 24M`. The first point past a multiple of `a × T` buys a whole ship of protection. Everything between two steps buys nothing. A hauler should aim just past a step boundary, and a designer who wants tank to feel rewarding should know that the reward is lumpy.
</details>

25. *Week 6 · design.* With the lecture's gank ships (`a = 500`, `p = 0.5`), a designer wants the safe cargo value in 0.5 space to be at least 4,000 ISK per EHP. (a) Keeping `T = 19`, what ship cost `c` produces that? (b) Keeping `c = 12M`, what response time `T` produces it? (c) Check (b) on a 60,000 EHP hauler.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `c = 19M`. (b) `T = 12` s. (c) 10 ships, `V* = 240M`, exactly 4,000 per EHP.

`V* / H ≈ 2c / (a × T)`. (a) `c = 4,000 × 500 × 19 / 2 = 19,000,000`. (b) `T = 2 × 12M / (500 × 4,000) = 12`.

(c) Each ship deals `500 × 12 = 6,000`. `60,000 / 6,000 = 10`, so `C = 120M`, `V* = 240M`, `240M / 60,000 = 4,000`.

Response time is the lever a designer controls directly, and players can read it. Ship cost is set partly by the market, so it drifts. That is an argument for tuning `T`.
</details>

26. *Week 6 · design.* In your fantasy world's capital, town guards kill an attacker 30 seconds after an attack starts, and each attacker also pays a 2,000-gold bounty. Attackers deal 40 damage per second. A new player has 3,000 EHP and carries at most 5,000 gold of goods, and half drops on death. (a) Does attacking a new player in the capital pay? (b) What is the lowest bounty at which it still does not pay?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) No. The attack costs 6,000 gold and the expected loot is 2,500. (b) The bounty can fall to about 834 gold before an attack pays.

(a) Each attacker deals `40 × 30 = 1,200`. `3,000 / 1,200 = 2.5`, so 3 attackers. The bounty is the cost per attacker, so `C = 3 × 2,000 = 6,000` and `V* = 12,000`. The new player's 5,000 is well below it.

(b) The attack pays when `3 × fee < 0.5 × 5,000 = 2,500`, so when the fee is below 833.3. Any bounty of 834 or more keeps new players safe in practice, with no wall. This is the lecture's rule of setting the price against what new players can carry.
</details>

## Week 7: Themepark versus sandbox

27. *Week 7 · compute.* A studio ships 12 hours of new authored content a month. A player plays 48 hours a month, and `K = 250`. (a) Find `s_T` and `N*`. (b) With 500 players in reach, find `s_S` and `s_H`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `s_T = 0.25`, `N* = 83`. (b) `s_S = 0.667`, `s_H = 0.75`.

(a) `s_T = min(1, 12 / 48) = 0.25`. `N* = K × s_T / (1 − s_T) = 250 × 0.25 / 0.75 = 83.3`.

(b) `s_S = 500 / 750 = 0.667`. `s_H = 1 − 0.75 × 0.333 = 0.75`. A quarter of this player's time is a repeat.
</details>

28. *Week 7 · compute.* A sandbox has 12,000 players online and `K = 400`. (a) What is `s_S` per player with 8 equal shards and everyone on a shard in reach? (b) With one shard? (c) Two years later the population has fallen by 60% and there are still 8 shards. What is `s_S` now, and what would a themepark with `s_T = 0.25` have lost over the same two years?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 78.9%. (b) 96.8%. (c) 60%. The themepark loses nothing, since `s_T` has no `N` in it.

(a) `N = 1,500`, `s_S = 1,500 / 1,900 = 0.789`. (b) `12,000 / 12,400 = 0.968`. (c) `4,800 / 8 = 600` per shard, `s_S = 600 / 1,000 = 0.6`.

One structure is fragile to population, the other to play time. The sandbox is still ahead of a 25% themepark here, but it has lost 19 percentage points of novelty for reasons no designer shipped.
</details>

29. *Week 7 · design.* A devoted player plays 150 hours a month. A hybrid game gives them 200 players in reach with `K = 300`. You want at least half of their time to be new. What authored output `p` do you need? What would the crossover `N*` be for this player at `p = 10`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `p ≥ 25` hours a month. At `p = 10`, `N* = 21.4`.

`s_S = 200 / 500 = 0.4`. `s_H = 1 − (1 − s_T) × 0.6 ≥ 0.5` needs `1 − s_T ≤ 0.833`, so `s_T ≥ 0.167`. `p ≥ 0.167 × 150 = 25`.

At `p = 10`, `s_T = 10 / 150 = 0.0667`, `N* = 300 × 0.0667 / 0.9333 = 21.4`. For this player, 22 people in reach out-supply the whole content team. Authored supply must scale with play time. Player-driven supply scales with population.
</details>

30. *Week 7 · critique.* Read Star Wars Galaxies' 2005 changes through the novelty model. What did the team change about the sources of novelty, and why did the conversion cost more than the model alone suggests?

<details>
<summary>Answer and worked solution</summary>

**Answer (model).** Galaxies launched in June 2003 as a sandbox, with 34 professions, a crafting economy and player cities. With a shrinking subscriber base, `N` and so `s_S` were falling. The May 2005 expansion added instanced dungeons on Kashyyyk, and the November 2005 New Game Enhancements cut the professions to nine, moving the game toward authored content, whose novelty does not depend on population. SOE's president defended the change as a response to subscriber decline.

The model sees a swap of one supply for another. It does not see who the supply is for. The players who had stayed chose the game for the sandbox, so the change removed what they came for and many left. That lowers `N` further. The players the new structure suited were already playing themeparks built that way from launch. A conversion changes which players a game is for, and the model's single `N` treats all players as interchangeable.
</details>

## Week 8: Bartle's player types and the population model

31. *Week 8 · compute.* Use the week 8 population model (populations in hundreds, one step a week). Start from `A = 3, E = 2, S = 4, K = 1`, open killing (`protection = 0`) and `c = 1`. (a) Compute `N`, `room`, `w` and `g`. (b) Compute all four populations after one week. (c) Using the survival line, what is the smallest protection level at which this socialiser community grows on its own at this `room`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `N = 10`, `room = 0.75`, `w = 0.5`, `g = 0.375`. (b) About 305 achievers, 198 explorers, 358 socialisers and 114 killers. (c) Protection above 60%.

(b) With `q = 1`:

- `A' = 3 + 0.375 − 3 × (0.03 + 0.08 × 1) = 3.375 − 0.33 = 3.045`
- `E' = 2 + 0.15 × 0.375 − 2 × (0.03 + 0.01 × 1) = 2.05625 − 0.08 = 1.97625`
- `S' = 4 + 0.05625 + 4 × (0.04 × 4 × 0.75 − 0.04 − 0.20 × 1) = 4.05625 − 0.48 = 3.57625`
- `K' = 1 + 0.0375 + 1 × (0.04 × 7 − 0.08 − 0.05 × 2) = 1.0375 + 0.10 = 1.1375`

Socialisers fell about 11% in a week even though they outnumber killers four to one.

(c) Socialisers grow, before arrivals, when `q × K < 0.2 × S × room − 0.2 = 0.2 × 4 × 0.75 − 0.2 = 0.4`, in hundreds. Here `K = 1`, so `q < 0.4` and protection `> 0.6`. In players, the survival line `0.15 × S − 20` gives 40 killers tolerated against 100 present.
</details>

32. *Week 8 · compute.* A world has 800 socialisers and `room = 0.75`. (a) How many killers can they tolerate under open killing? (b) There are 120 killers. What protection level is needed for the socialisers to grow? (c) Below what socialiser count does the community shrink even with no killers?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 100. (b) Protection above about 17%. (c) About 133 socialisers.

(a) The survival line is `0.15 × S − 20 = 0.15 × 800 − 20 = 100`.

(b) Need `q × 120 < 100`, so `q < 0.833` and protection `> 0.167`.

(c) `0.15 × S − 20 = 0` at `S = 133`. That is the model's version of Bartle's critical mass. Below it, the socialisers' self-attraction is weaker than their base loss.

The line uses `room = 0.75`, its value at 1,000 players. In a fuller world `room` falls and the line moves, so these numbers hold only near that population.
</details>

33. *Week 8 · explain.* Place each player on the interest graph and give the eight-type label. (a) A player who buys every copy of a crafting reagent to ruin rival crafters and become known as the person who controls that market. (b) A player who logs in each night to chat with the same four guildmates and does whatever they are doing. (c) A player who spots a glowing rock, hits it to see what drops, then wanders off after the next shiny thing, with no plan.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Politician (acting on players, explicit). (b) Friend (interacting with players, implicit). (c) Opportunist (acting on the world, implicit).

(a) is the lecture's point that "killer" means imposing on other players, not fighting. Cornering a market acts on players, and doing it to build a reputation is the explicit, planned side. (b) enjoys the company of people they already know without seeking new contacts, which separates the friend from the networker. (c) is after in-game gains, so it is achievement, and it takes chances as they appear, which is implicit.
</details>

34. *Week 8 · critique.* A lead designer says, "Killers drive away everyone else. We'll set protection to 1 everywhere and get a healthy world." Using the model's week-520 results and Bartle's paper, critique the plan.

<details>
<summary>Answer and worked solution</summary>

**Answer (model).** In the model, full protection from the lecture's starting mix ends at about 69 achievers, 10 explorers, 3,813 socialisers and 2 killers. That is Bartle's second configuration, a socialiser-dominated world. The achievers and explorers were squeezed out by crowding once the socialisers' positive feedback filled the server, not by killers. So "healthy" here means healthy for one group.

The model also flatters protection. Bartle notes that achievers in a world with no threat can feel that anyone could win, and the model has no term for that. Lab 08's option (b) adds it.

If the goal is a mix, the lecture's runs say you need two levers, partial protection and a steady supply of new things for explorers (50% protection with `c = 3` stands at 797, 501, 287 and 30 at week 520, though that world never settles and keeps cycling between about 1,050 and 2,800 players). The honest alternative to one rule for everyone is Trammel's or War Mode's, which let players choose, at the cost of splitting `N`.
</details>

35. *Week 8 · explain.* Bartle maps Campbell's hero's journey onto a player's time in a virtual world. What is missing at "the ultimate boon" in most commercial worlds, and why does Bartle raise it as a question of ethics? Give one design that offers a boon without ending the game for everyone.

<details>
<summary>Answer and worked solution</summary>

**Answer (model).** In Campbell's structure the hero gains something and goes home. Bartle points out that most studios do not want players to leave, so they offer no boon and add content to keep the player instead. He asks whether it is ethical to design a journey whose end is withheld on purpose, since for him "master of the two worlds", when the player no longer needs the world to be who they are, is the finished journey and the right time to stop.

One design is a capstone that the player can complete and that marks their character as finished, such as retiring a character into a permanent place in the world's history (a statue, a name in a hall), with a legacy passed to a new character or to the guild. The player gets an ending that belongs to them, and the world keeps the history. Treat the whole mapping as a lens, not a finding. Folklorists criticize the monomyth for fitting examples chosen to fit.
</details>

## Week 9: Motivation research beyond Bartle

36. *Week 9 · compute.* Assume independent components and scores that are uniform percentiles. What share of players does a primary-motivation rule label (a) with 5 components and `c = 0.7`, (b) with 3 components and `c = 0.5`, (c) with Bartle's 4 types and Yee's `c = 0.75`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 24.0%. (b) 25.0%. (c) 42.2%.

`P(typed) = c^(k − 1)`. (a) `0.7^4 = 0.2401`. (b) `0.5^2 = 0.25`. (c) `0.75^3 = 0.4219`.

A strict rule on three components and a mild rule on five label about the same quarter of players. Either way, most players get no single label.
</details>

37. *Week 9 · compute.* Apply Yee's rule (`c = 0.75`) and a forced label to three players, with percentiles in the order achievement, social, immersion. P7 = (0.55, 0.42, 0.61). P8 = (0.30, 0.80, 0.58). P9 = (0.12, 0.09, 0.10). What does P9 show about forced labels?

<details>
<summary>Answer and worked solution</summary>

**Answer:** P7 none (forced label immersion). P8 social (forced label social). P9 none (forced label achievement).

P7: top 0.61, second 0.55, ratio 0.90, not below 0.75. P8: top 0.80, second 0.58, ratio 0.725, below 0.75, so social. P9: top 0.12, second 0.10, ratio 0.83, so none.

P9 is below the 13th percentile on everything. A forced label calls them an achiever because 0.12 beats 0.10. The label says more about the test than about the player, and a design that "serves achievers" will not reach someone who is barely motivated by any of the three.
</details>

38. *Week 9 · compute.* A studio calls a player "high" on a component if they are in the top 25%. With four independent components, what share of players is high on none, on exactly one, and on two or more?

<details>
<summary>Answer and worked solution</summary>

**Answer:** None 31.6%. Exactly one 42.2%. Two or more 26.2%.

None: `0.75^4 = 0.3164`. Exactly one: `4 × 0.25 × 0.75^3 = 0.4219`. Two or more: `1 − 0.3164 − 0.4219 = 0.2617`.

About a third of players are moderate on everything. They play and pay, and they need a game that is pleasant at moderate intensity on every component. A persona set built from "the achiever", "the socialiser" and so on describes none of them.
</details>

39. *Week 9 · critique.* A design document says, "Our research shows 20% of MMO players are achievers, so we'll design one persona for them. It is based on Yee's survey." Name three problems with using Yee's findings this way.

<details>
<summary>Answer and worked solution</summary>

**Answer (model).** First, the 20% are achievement-primary under a rule Yee called somewhat lax, and 43% of respondents had no primary motivation at all. A persona for "the achiever" covers one player in five and leaves out the largest group.

Second, a primary label is not a type. Components are nearly independent (correlations around 0.10), and achievement and socializing correlate slightly positively, so many achievement-primary players are also social or immersive. Achievement also includes Competition, which correlated about 0.41 with Advancement, so this persona overlaps Bartle's killers.

Third, the sample. Respondents chose to answer an online survey in the mid-2000s, about 2,769 of roughly 3,200 were male, and the items are self-reports. The shares describe those respondents, not a 2026 audience. Use component scores for features ("this serves Advancement and Teamwork"), and check them against behavior data before budgeting.
</details>

## Week 10: Immersion, identity and the avatar

40. *Week 10 · compute.* A creator offers 5 faces, 12 hairstyles and 10 hair colours, all chosen evenly. (a) What is `M`? (b) About how many players in view give even odds of a twin pair? (c) What is the chance of at least one twin pair among 40 players?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 600. (b) About 29. (c) 72.7%.

(a) `M = 5 × 12 × 10 = 600`, `c = 1/600`.

(b) `n ≈ ½ + √(¼ + 2 ln 2 / c) = ½ + √(0.25 + 831.8) = 29.3`.

(c) Pairs `= 40 × 39 / 2 = 780`. `E = 780 / 600 = 1.3`. `P = 1 − e^(−1.3) = 0.727`.
</details>

41. *Week 10 · compute.* A creator has three categories of 10 options each. Half of all players keep the default in each category, and the rest spread evenly over the other nine. (a) Find `c_j`, `c` and `M_eff`. (b) What share of players keep every default? (c) At what crowd size is a twin more likely than not?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `c_j = 0.278`, `c = 0.0214`, `M_eff ≈ 47`. (b) 12.5%. (c) About 9 players.

(a) `c_j = 0.5² + 0.5² / 9 = 0.25 + 0.0278 = 0.2778`. `c = 0.2778³ = 0.02143`. `M_eff = 46.7`. The creator promises 1,000 looks and the crowd sees 47.

(b) `0.5³ = 0.125`. One player in eight is the same default character.

(c) `n ≈ ½ + √(0.25 + 1.386 / 0.02143) = 8.6`, so 9 players.
</details>

42. *Week 10 · design.* Keep question 41's creator. The art team can afford one change. Option A removes the default from one category, so its choices become even. Option B adds 10 new options to one category but keeps the 50% default. Which raises `M_eff` more, and by how much?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Option A gives `M_eff ≈ 130`. Option B gives about 49. Option A gives about 2.6 times as much and costs no art.

Option A: the category becomes `1/10 = 0.1`. `c = 0.1 × 0.2778² = 0.00772`, `M_eff = 129.6`.

Option B: the category has 20 options with a 50% default, `c_j = 0.25 + 0.25 / 19 = 0.2632`. `c = 0.2632 × 0.2778² = 0.0203`, `M_eff = 49.2`.

The popularity effect again. A default held by half the players contributes `0.25` to `c_j`, and the other options together contribute at most `0.028`. Adding options only shrinks the small term. Removing the default attacks the large one. The cost of option A is time at creation, which a random start from curated presets can reduce.
</details>

43. *Week 10 · explain.* Place each quote on Bartle's immersion ladder and name one design feature that would matter more to that player than the character creator. (a) "The quest bugged, the program never gave me the item." (b) "Mira would never sell out her guild, so I turned the offer down." (c) "My guy's got the best sword on the server."

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Player level. (b) Character level. (c) Avatar level.

(a) treats the world as software. Reliable systems and clear feedback matter most. Fixing the bug keeps them from dropping further. (b) speaks about a rounded personality the player puts on and whose choices they honor. Challenges that ask who the character is (loyalty, betrayal, responsibility) and continuity of name and history matter most. (c) treats the character as a puppet that carries gear. Gear, its visible appearance and the progression system matter most, which is why appearance systems that let players show one item while wearing another are for this player.

None of them is at persona level, where the player would say "I" and mean it. Bartle argues that level needs witnesses and continuity, which is why names and history carry so much weight.
</details>

44. *Week 10 · critique.* A studio plans to let every character pick a display name that need not be unique, with no hidden ID, "so nobody ever sees a 'name taken' message." Using week 10's name policy discussion and the Discord case, say what this gives up and propose a fix.

<details>
<summary>Answer and worked solution</summary>

**Answer (model).** Names are the most stable identifier a world has. If any number of characters can share a name and nothing else tells them apart, players cannot find a friend, trust a trader or hold a scammer to account, because reputation has nothing to attach to. A world with trading and scams needs names people can trust.

Discord's 2023 change shows the other side. Its old `Name#1234` scheme was technically unique but hard to use. Popular base names ran out of discriminators, and the company reported that nearly half of friend requests failed from mistyped names. It moved to unique usernames with a separate free-form display name.

A fix in the same shape pairs a free display name for what others see in the world with a unique handle or hidden ID used for friends, trade, mail and reports, shown on inspect. The cost is some complexity at creation and a second name for players to learn.
</details>

## Week 11: Koster's Laws of Online World Design

45. *Week 11 · compute.* A loophole has `q = 3 × 10⁻⁶` per player-hour. Find the chance it is found by (a) 40 QA testers playing 250 hours each, (b) a beta of 8,000 players playing 15 hours each, (c) 150,000 players on launch day playing 4 hours each, (d) the same players over launch week at 25 hours each. (e) With 45,000 players online at peak, how long until the first expected discovery?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 3.0%. (b) 30.2%. (c) 83.5%. (d) More than 99.99%. (e) 7.4 hours.

`P = 1 − e^(−qH)`. (a) `H = 10,000`, `qH = 0.03`, `P = 0.0296`. (b) `H = 120,000`, `qH = 0.36`, `P = 0.302`. (c) `H = 600,000`, `qH = 1.8`, `P = 0.835`. (d) `H = 3,750,000`, `qH = 11.25`, `P = 0.99999`. (e) `1 / (45,000 × 3 × 10⁻⁶) = 7.4` hours.

QA's careful 10,000 hours are 1.7% of launch day's player-hours. What matters is `qH`, not `q`.
</details>

46. *Week 11 · compute.* A dungeon fails if any one player in the group deliberately stands in the wrong place, and 0.8% of players will. (a) What share of 30-player groups contain at least one such player? (b) What is the largest group size that keeps that share at or below 10%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 21.4%. (b) 13 players.

(a) `1 − 0.992^30 = 1 − 0.786 = 0.214`.

(b) Need `0.992^n ≥ 0.9`, so `n ≤ ln 0.9 / ln 0.992 = 13.1`. Thirteen players.

The design rule from the lecture follows. Do not build a mechanic whose worst case needs zero bad actors in a group of 30. Either make the mechanic survive one saboteur or accept that one group in five will fail for reasons unrelated to skill.
</details>

47. *Week 11 · compute.* A world has 40 systems. The team plans to add 5 more. (a) How many new pairs of systems does that create? (b) If each pair has a 0.1% chance of hiding an exploitable interaction, what is the chance at least one of the new pairs does? (c) What does Lambert's Law predict about the fifth of those five systems compared with the first?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 210. (b) 19.0%. (c) The fifth adds 44 pairs, the first 40.

(a) Before, `40 × 39 / 2 = 780`. After, `45 × 44 / 2 = 990`. New pairs, 210.

(b) `1 − 0.999^210 = 0.1895`, about 19.0%.

(c) A new system pairs with every system already there. The first of the five adds 40 new pairs, the fifth adds 44. Late features are the riskiest, and they are also the least tested against everything else. Isolation rules ("pets reset when they leave an instance") delete whole rows of pairs, which is cheaper than testing each one.
</details>

48. *Week 11 · critique.* A feature brief says: "Players may place a campfire anywhere. It heals everyone within 10 metres and lasts until someone puts it out." Review it against four of the laws, name the law each risk comes from, and propose two isolation rules.

<details>
<summary>Answer and worked solution</summary>

**Answer (model).**

- Hyrup's Loophole Law (anything exploitable will be). Campfires placed inside boss arenas, in PvP chokepoints or stacked twenty deep will be found on day one, because `qH` at launch is large.
- John Hanke's Law (a fixed share of troublemakers). A fire placed on a quest-giver or a bank door that heals enemies of the people standing there, or that blocks a path, needs only one player in a thousand to wreck a busy square.
- Lambert's Laws (more actions, more exploits). Healing pairs with combat, PvP flagging, safe zones, instanced dungeons and housing. Each pair is a row of risk.
- Schubert's Law (new players expect a single-player story). A new player whose fight is healed by a stranger's fire, or whose town is full of fires, will read it as interference.
- The persistence rule and week 12's clutter law. "Lasts until someone puts it out" is `W` infinite, a stock with no ceiling.

Two isolation rules would help. Campfires cannot be placed in instances, arenas or within a set distance of NPCs and doors, and each campfire expires after a fixed time (for example 30 minutes, which gives a bounded `λW`) with a limit of one active fire per player.
</details>

## Week 12: Persistence and time

49. *Week 12 · compute.* A world has 8,000 active players who each drop 30 items a day. Dropped items last 15 minutes. The world has 25 zones. (a) How many dropped items exist at a typical moment, and how many per zone? (b) What would the count be after one year if items never despawned?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 2,500 in the world, 100 per zone. (b) 87.6 million and still rising.

(a) `λ = 8,000 × 30 = 240,000` a day. `W = 15 / 1,440 = 0.01042` days. `S = λW = 2,500`. Per zone, 100.

(b) With no lifetime, `S(t) = λt = 240,000 × 365 = 87,600,000`, with no ceiling. Items that never expire do not make a large stock. They make a stock that never stops growing.
</details>

50. *Week 12 · compute.* A world has 2,000 house plots. 1.5% of owners quit each week. Houses are demolished after 60 days without a visit. (a) How many abandoned houses stand at a typical time, and what share of plots is that? (b) What would it be with a 30-day rule? (c) Who pays for the longer rule?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 257 houses, 12.9% of plots. (b) About 129, 6.4%. (c) Players waiting for a plot, usually newer players.

(a) `λ = 2,000 × 0.015 / 7 = 4.286` newly abandoned houses a day. `S = 4.286 × 60 = 257`. `257 / 2,000 = 0.129`.

(b) `4.286 × 30 = 129`.

(c) The extra 128 plots are held by owners who are not coming back. Being kind to absent owners is being harsh to present newcomers. Final Fantasy XIV's version, as the lecture describes it, uses 45 days with warnings at 30, 35 and 42, and a clock that resets whenever the owner or a Free Company member enters.
</details>

51. *Week 12 · compute.* (a) A world clock runs one world day per 120 real minutes. How many world days pass in a real week? A player always logs in at the same real time and plays for 90 minutes. Do they ever see the whole day-night cycle? (b) A two-week beta ends with 300,000 standing shelters. Shelters have random (exponential) lifetimes with a mean of 90 days. What long-run ceiling should the team expect?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 84 world days a week, and no, the player never sees the last quarter of the cycle. (b) About 2.1 million shelters.

(a) `10,080 / 120 = 84`. A 90-minute session covers three quarters of a world day. A real day is `1,440 / 120 = 12` world days exactly, so a player who starts at the same real time every day starts at the same world hour every day and always sees the same three quarters. Compare Final Fantasy XIV's 70-minute day from the lecture. `1,440 / 70` is not a whole number, so the starting world hour moves from one real day to the next and a fixed schedule eventually sees everything. The length of a world day should not divide a real day evenly.

(b) With exponential lifetimes the stock is `λW(1 − e^(−t/W))`. At `t = 14` days, `1 − e^(−14/90) = 0.144`. So 300,000 is 14.4% of the ceiling, and the ceiling is `300,000 / 0.144 ≈ 2.08` million. The beta has seen about a seventh of the long-run clutter, and the stock reaches 95% only at `3W = 270` days.
</details>

52. *Week 12 · design.* Guilds create 400 guild halls a month and nobody deletes them. (a) How many halls stand after four years? (b) Propose a lifetime rule, compute the standing stock of abandoned halls it allows, and justify it with the persistence-budget rules.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 19,200 and rising. (b) One defensible rule: a hall is removed after 120 days in which no member enters it, with warnings at 60, 90 and 110 days. If every hall were eventually abandoned, at most about `13.3 × 120 = 1,600` abandoned halls would stand at once.

(a) `400 × 12 × 4 = 19,200`, with no ceiling.

(b) `λ = 400 / 30 = 13.3` halls a day. With a conditional 120-day lifetime, only halls nobody visits count down, so the abandoned stock is at most `λW = 1,600`, and less if many guilds stay active. The budget rules support it. Persist what other people depend on, so a hall that a whole guild relies on gets a long lifetime renewable by any member, longer than a personal house. Warn before you delete anything a player built. The number 120 is a judgment. Say whose wait it lengthens (guilds looking for a hall plot) if plots are scarce.
</details>

## Week 13: Worlds that died

53. *Week 13 · compute.* Use the lecture's density-churn parameters (`c0 = 0.03`, `c1 = 0.20`, `H = 2,000`, `A = 6,000`, `p = $15`, `F = $900,000`, `k = $10,000`). A world has 120,000 players on 30 shards. (a) Compute this month's churn and next month's population. (b) What is the break-even population? (c) What would churn be this month if the same players were on 10 shards?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 9.67% churn, next month 114,400. (b) 80,000. (c) 5.86%.

(a) `d = 120,000 / 30 = 4,000`. `H / (H + d) = 2,000 / 6,000 = 0.333`. `c = 0.03 + 0.20 × 0.333 = 0.0967`. Lost `= 11,600`. Next `= 120,000 − 11,600 + 6,000 = 114,400`.

(b) `N_be = (900,000 + 10,000 × 30) / 15 = 80,000`.

(c) `d = 12,000`, `H / (H + d) = 0.143`, `c = 0.03 + 0.0286 = 0.0586`.
</details>

54. *Week 13 · compute.* The world in question 53 launched with 200,000 players on 30 shards. (a) Show that its resting population is 40,000, and give its churn at rest. (b) Is it profitable at rest? (c) Run from launch, it first falls below break-even in month 20. A merge to 10 shards at month 20 leaves it with no months below break-even over five years. Explain why the same merge counts as "on time" for this world.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) At `N = 40,000`, churn is 15% and `N × c = 6,000 = A`. (b) No. Break-even is 80,000, twice the resting population. (c) Below.

(a) `d = 40,000 / 30 = 1,333`. `H / (H + d) = 2,000 / 3,333 = 0.6`. `c = 0.03 + 0.12 = 0.15`. `40,000 × 0.15 = 6,000`, which equals `A`, so the population stays put.

(b) Revenue at rest is `$600,000` against `$1,200,000` of cost. It loses money every month forever.

(c) The merge lowers break-even from 80,000 to `1,000,000 / 15 = 66,667` on the day it happens, and raises density, which cuts churn. At month 20 the population is about 78,400, above the new break-even, so the world never records a losing month. The model's lesson is that the resting point depends only on `S`, but the losses depend on when you move `S`. The same merge at month 32 reaches the same resting point, but only after 24 months below break-even (months 20 to 43), and publishers looking at two years of losses do not wait for the curve to turn.
</details>

55. *Week 13 · explain.* Suppose emptiness does not affect churn (`c1 = 0`), with `c0 = 0.025` and `A = 4,500`. What is the resting population, and how does it depend on the number of shards? What does this tell you about why shard count matters at all?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 180,000, whatever the shard count.

At rest `N × c = A`. With `c1 = 0`, `c = c0` for every `S`, so `N* = A / c0 = 4,500 / 0.025 = 180,000`. `S` has dropped out.

Shard count matters only because other players are the content. When a shard empties, each remaining player gets less from the world and more of them leave. That is the `c1 × H / (H + d)` term. If you believe your game's churn does not depend on how many people a player meets, shards are free. If it does, and the lecture's cases suggest it usually does, every shard you add at launch is a bet on a crowd staying.
</details>

56. *Week 13 · critique.* A classmate's post-mortem says, "WildStar died because it was a bad game with an empty world." Using only the facts in the week 13 lecture, critique this and rewrite the cause analysis using the four families.

<details>
<summary>Answer and worked solution</summary>

**Answer (model).** "Bad game" is not an analysis, and "empty world" is asserted without evidence. The recorded facts point to a business decision as the main cause. WildStar launched on 3 June 2014 with a subscription and moved to free-to-play on 29 September 2015. On 6 September 2018 NCSoft closed Carbine Studios at once and said it would wind the game down, and the servers went off on 28 November 2018.

A better analysis names a business decision as the main cause, since the owner closed the studio first and then set a date. An empty-world spiral is a possible contributing cause, suggested by the switch to free-to-play about 15 months after launch. To support it you would need falling players per server, merges, or statements naming population, and the lecture gives none, so say it is unproven. The design lesson from this case is the order of events. Once the team that knows the code is gone, a final event, a merge or a server-software release all become harder, so a sunset plan has to be written while the team still exists.
</details>

## Week 14: Designing a world concept

57. *Week 14 · compute.* A world has 6,000 concurrent players at peak on one shard, 35% of them in hubs, and a view radius of 100 m. (a) What field area gives 3 other players in view at peak? (b) At a trough of 30% of peak, what is `E`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 40.8 km². (b) 0.9.

(a) View area `= π × 100² = 31,416 m²`. Field players `= 0.65 × 6,000 = 3,900`. `A = 3,900 × 31,416 / 3 = 40,840,704 m² ≈ 40.8 km²`, a square about 6.4 km across.

(b) `E` is proportional to `P`, so `E = 3 × 0.3 = 0.9`. At the trough a player is more likely than not to see nobody else in the field.
</details>

58. *Week 14 · compute.* A world is sized so that `E = 3` at the 3 a.m. trough. Peak concurrency is 4 times the trough. The crowding limit is `E_max = 5`. How many map copies are needed at peak, and what is `E` per copy?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 3 copies, `E = 4` per copy.

With one copy, peak `E = 3 × 4 = 12`. `n = ceil(12 / 5) = 3`. `E` per copy `= 12 / 3 = 4`. The day now runs between 3 and about 5 others in view instead of 3 to 12. The cost is recognition. Players who met last night may be in different copies tonight unless placement keeps friends and guilds together.
</details>

59. *Week 14 · compute.* A Minecraft Java Edition server keeps the default 20 players (`max-players=20`) but sets the view distance to 8 chunks. Chunks are 16 by 16 blocks. With all 20 online and a target of 3 others in view, how wide can the shared build area be?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 702 blocks wide.

The view region is a square `(2 × 8 + 1) × 16 = 272` blocks on a side, area `73,984` square blocks. Following the lecture's Minecraft calculation, `A = 20 × 73,984 / 3 = 493,227` square blocks, and `√493,227 ≈ 702`. Players who settle farther apart than that will mostly be alone, and on a small server the players, not the designer, make that choice.
</details>

60. *Week 14 · critique.* A classmate's concept says, "Our world is huge, so explorers will love it," with 1,200 players at peak on one shard, 20% in hubs, a view radius of 80 m and a 60 km² field. Compute `E` at peak, apply the night-shift test, and write the critique you would hand back.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `E ≈ 0.32` at peak, so a field player is alone about 72% of the time.

View area `= π × 80² = 20,106 m²`. Field players `= 0.8 × 1,200 = 960`. `E = 960 × 20,106 / 60,000,000 = 0.32`. So at peak a field player sees nobody `e^(−0.32) = 72%` of the time. At a trough of a quarter of peak, `E = 0.08` and they are alone 92% of the time.

Critique: "At peak your players see nobody in the field almost three times out of four, and at night more than nine times out of ten. That is a single-player game with a chat window. Explorers still want someone to tell about what they found. Either shrink the field to about 19 km², which gives `E = 1` at peak, pull players onto routes and landmarks, or widen the view radius where you want meetings. Then say what a solo explorer does at 3 a.m." Size to the population you expect, and add space only where emptiness is the design.
</details>

## Across weeks

61. *Weeks 1 and 14 · explain.* Show that week 14's density budget and week 1's view-cell model are the same model. Take the week 14 lecture's world (1,800 field players, 31.8 km², `r = 150` m). How many view cells is the field, what is `λ`, and what is `P(alone)`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 450 view cells, `λ = 4`, `P(alone) = e^(−4) = 1.8%`.

A view cell in week 1 is the patch you can see from one spot. In week 14 that patch is a circle of area `π r² = 70,686 m²`. So the field holds `M = A / (π r²) = 31,808,626 / 70,686 = 450` cells. With `n = 1,800` field players, `λ = n / M = 4.0`, which is week 14's `E`. Week 1's `P(alone) = e^(−λ)` then says a field player sees nobody 1.8% of the time at peak, and at the 3 a.m. trough (`E = 1`) 37% of the time. Week 1 asks how to move `λ` with pooling and splitting. Week 14 asks how to size `A` and `r` before anyone builds. They are the same dial.
</details>

62. *Weeks 3 and 12 · explain.* Week 3's faucet world holds `σ(1 − d)/d` units at steady state. Show that this is Little's law from week 12, and explain the small difference between `σ/d` and `σ(1 − d)/d` for `σ = 6,000` and `d = 0.005`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Little's law gives `S = λ × W = 6,000 × 200 = 1,200,000`. The week 3 formula gives 1,194,000. The 6,000 difference is one day's harvest, which the week 3 model counts at the end of the day after returns.

In the faucet world, items enter players' hands at `λ = σ` a day and leave at a daily rate `d`, so the average holding time is `W = 1/d = 200` days. Little's law says the stock is `λW = σ/d`. The week 3 simulation records `H` after that day's returns, which removes `d × H` and gives `σ(1 − d)/d`. The two differ by `σ`, one day's inflow.

The same law explains both lectures. The hoard in Ultima Online's faucet economy and the clutter of dropped items are the same stock-and-lifetime problem. Only the name of the object changes.
</details>

63. *Weeks 7 and 13 · compute.* 30,000 players are split across either 10 or 3 shards. With `K = 300`, compute `s_S` per player. With week 13's churn parameters (`c0 = 0.03`, `c1 = 0.20`, `H = 2,000`), compute monthly churn. What do the two models agree on?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 10 shards: `s_S = 90.9%`, churn 11.0%. 3 shards: `s_S = 97.1%`, churn 6.3%.

10 shards: 3,000 per shard, `s_S = 3,000 / 3,300 = 0.909`, `c = 0.03 + 0.2 × 2,000 / 5,000 = 0.11`. 3 shards: 10,000 per shard, `s_S = 10,000 / 10,300 = 0.971`, `c = 0.03 + 0.2 × 2,000 / 12,000 = 0.063`.

Both models depend on players per shard, not on total players. Both have the saturating shape `x / (x + K)`, so the first merges help most. They measure different harms. Week 7 counts lost novelty for the players who stay. Week 13 counts the players who leave. The novelty gain from 10 to 3 shards looks small (6 points), but the churn falls by 4.7 points a month, which compounds.
</details>

64. *Weeks 4 and 5 · explain.* Explain why an instanced raid with a lockout (week 4) and a time-only death rule (week 5) make the same promise to a player with 45 minutes a night, and name what each takes away from the world.

<details>
<summary>Answer and worked solution</summary>

**Answer (model).** Both remove other players and bad luck from a player's progress. An instanced raid's loot rate `W = L × R / (7 × d)` does not contain `G`, so it does not depend on how many other guilds exist or who got there first. A time-only death rule has `x = 0`, so `P = g × (1 − λt)` is never negative. Together they let a game promise that time spent always moves you forward, which is the promise a short-session player needs.

Each takes something away from the world. Instancing removes the rivalry, rotation politics and shared server history that contested bosses created, so other guilds stop mattering and the world becomes a lobby. The time-only rule removes the danger that made players group up, value a healer they knew and learn an area before pushing into it. Week 5 calls this a loss of dependence. The lowest barriers and the strongest ties cannot come together, so a designer chooses where each piece of content sits.
</details>
