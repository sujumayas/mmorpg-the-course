# MMO406 · Exam bank: quiz, practice and viva questions

MMO406 has no written exam. The grade comes from the exercises (40%, [exercises-brief.md](exercises-brief.md)) and the world bible (60%, [world-bible-brief.md](world-bible-brief.md)). This bank has three jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Weekly quizzes.** Most lab sessions open with a 10-minute ungraded quiz of two questions from this bank, usually one compute question and one analysis or critique question.
- **Bible defence.** In week 15 each student defends their world bible. One of the examiners' questions comes from this bank, rewritten with the numbers from your own bible.

Every question is tagged with the week it draws on and a type.

- **compute**: apply a lecture model to numbers you have not seen before.
- **analysis**: explain why a model behaves the way it does, with a number as evidence.
- **design**: choose values that meet a stated goal and show that they meet them.
- **critique**: find what is wrong with a proposal and say how to fix it.

All settings, factions and characters in this bank are invented. *Thornmere* is the course's sample world from the lectures. Every fact about a shipped game comes from the lecture of the tagged week, which cites its source and version. Every number was recomputed in Python from the lectures' own models, and every code block runs as shown with `.venv/bin/python`. Write your own answer before you open the solution.

---

## Week 1: Setting as system

Lecture: [w01, setting as system](../lectures/w01-setting-as-system.md). Model: the tension ledger, `P(t+1) = P(t) − c + R` with `R = g × S`.

1. *Week 1 · compute.* An invented archipelago setting launches with `P(0) = 15` plot tensions. Each expansion closes `c = 4` of them. The bible lists `S = 4` structural tensions, each spawning `g = 0.5` new plot tensions per expansion. Compute `R`, the drain `d`, the number of full expansions `N`, and the stock at the start of the first expansion that cannot be fully supplied.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `R = 2`, `d = 2`, `N = 6`. The stock at the start of expansion 7 is 3.

`R = g × S = 0.5 × 4 = 2`. The drain is `d = c − R = 4 − 2 = 2`. Then `N = floor((15 − 4) / 2) + 1 = floor(5.5) + 1 = 6`.

The stock runs 15, 13, 11, 9, 7, 5 at the starts of expansions 1 to 6. Each of those is at least 4, so each expansion ships a full story. At the start of expansion 7 the stock is 3, one short of `c`.
</details>

2. *Week 1 · design.* The archipelago team from question 1 can afford one change. Option A adds 6 more plot tensions to the launch bible. Option B ties each of the four structural tensions to a game system (a territory map, gathering nodes, a reputation pair, a shipping route), which the team estimates raises `g` from 0.5 to 0.75 for all four. Compute `N` for each option and recommend one.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Option A gives `N = 9`. Option B gives `N = 12`. Recommend B.

Option A: `P(0) = 21`, `d` stays 2, so `N = floor((21 − 4) / 2) + 1 = floor(8.5) + 1 = 9`.

Option B: `R = 0.75 × 4 = 3`, so `d = 1` and `N = floor((15 − 4) / 1) + 1 = 12`.

Six new plot tensions add three expansions. Raising refill by one tension per expansion halves the drain and adds six. That is the lecture's point about the denominator: near break-even, refill buys more lifetime than stock. B also keeps paying after expansion 12, because the systems keep producing situations whether writers use them or not.
</details>

3. *Week 1 · compute.* Predict what this code prints, then run it. Use the formula to explain the second line without the loop.

```python
def expansions(P0, c, R, cap=50):
    stock, n, history = P0, 0, [P0]
    while stock >= c and n < cap:
        stock = stock - c + R
        n += 1
        history.append(stock)
    return n, history

for args in [(10, 4, 1.5), (18, 5, 4.5)]:
    n, h = expansions(*args)
    print(n, h[:5])
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
3 [10, 7.5, 5.0, 2.5]
27 [18, 17.5, 17.0, 16.5, 16.0]
```

First line: `d = 4 − 1.5 = 2.5`, and `N = floor((10 − 4) / 2.5) + 1 = floor(2.4) + 1 = 3`. The history stops at 2.5 because the loop ends when the stock falls below `c`.

Second line: `d = 5 − 4.5 = 0.5`, so `N = floor((18 − 5) / 0.5) + 1 = 26 + 1 = 27`. A setting whose refill almost matches its consumption lasts 27 expansions from a smaller launch stock than many settings that last five. The history prints only its first five values.
</details>

4. *Week 1 · analysis.* Classify each tension as plot or structural, and give a plausible `g` for each structural one with a one-line reason. (a) A plague that a quest chain can cure. (b) Two guilds that both hold a royal charter to the same silver mine, and the mine's owner is set by a territory-control system. (c) An ancient seal under the capital that will fail "one day". (d) A salt road that is the only land route between two trade leagues, patrolled by player bounty hunters.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) plot. (b) structural, `g` about 1. (c) plot. (d) structural, `g` about 0.5 to 1.

(a) Once the cure ships, the tension is gone. It can be told once.

(b) Every change of owner in the territory system is a new situation: a siege, a betrayal, a new governor. A system that changes hands often supports about one new plot tension per expansion.

(c) A slow plot tension. It gives one climax whenever you choose to spend it. It can feed structural tensions (a cult that wants the seal broken) only if the bible builds them.

(d) Geography does not resolve, and a player-driven bounty system keeps making bandits, tolls and smugglers. Its `g` depends on how often the leagues' relationship changes. If nothing in the systems moves that relationship, 0.5 is safer than 1.
</details>

---

## Week 2: Geography and ecology

Lecture: [w02, geography and ecology](../lectures/w02-geography-and-ecology.md). Model: resource locality, `local share = C(r, k) / C(M, k)`.

5. *Week 2 · compute.* A world has `M = 7` raw resource types. A region holds `r = 4` of them. Compute the region's local share for recipes needing `k = 1`, `k = 2` and `k = 3` different types, and the travel pressure for `k = 3`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 57.1%, 28.6% and 11.4%. Travel pressure for `k = 3` is 88.6%.

- `k = 1`: `4 / 7 = 57.1%`.
- `k = 2`: `C(4, 2) / C(7, 2) = 6 / 21 = 28.6%`.
- `k = 3`: `C(4, 3) / C(7, 3) = 4 / 35 = 11.4%`.

Travel pressure is `1 − 0.114 = 88.6%`. The region holds more than half the resource types and can make about one three-ingredient recipe in nine at home.
</details>

6. *Week 2 · design.* A designer wants every region of a world with `M = 6` types to make at least half of all two-type recipes locally. What is the smallest `r` that meets the target? With that `r`, what share of three-type recipes can each region make, and what does that do to trade for advanced gear?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `r = 5`. Local share for triples is then 50%.

With `r = 4`: `C(4, 2) / C(6, 2) = 6 / 15 = 40%`, below target. With `r = 5`: `C(5, 2) / 15 = 10 / 15 = 66.7%`, which meets it.

For triples, `C(5, 3) / C(6, 3) = 10 / 20 = 50%`. Every region holds five of six types, so half of all advanced recipes can be made at home everywhere. The target for basic gear has removed most of the reason to trade for advanced gear too. If the design wants group or trade play at the top end, keep `r` lower and meet the basic-gear target another way, for example by making basic recipes use `k = 1`.
</details>

7. *Week 2 · analysis.* A world has `M = 6` types and four regions, each holding four types. (a) What is each region's local share for pairs and for triples? (b) At most how many of the 20 possible triples can be gathered inside a single region? (c) What is the smallest share of triples that must involve trade?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 40% for pairs, 20% for triples. (b) At most 14. (c) At least 30%.

(a) `6 / 15 = 40%` and `C(4, 3) / 20 = 4 / 20 = 20%`.

(b) Each region holds `C(4, 3) = 4` triples, so `4 × 4 = 16` is a first upper bound. It cannot be reached. Each region misses two types, and two regions share a triple exactly when their missing pairs share a type (they then have three types in common). Six types allow at most three disjoint missing pairs, so the fourth region's missing pair overlaps one of the others. The best arrangement, for example missing pairs {1, 2}, {3, 4}, {5, 6} and {1, 3}, gives 14 distinct triples. Enumerating every arrangement of four regions confirms 14 is the maximum.

(c) At least `20 − 14 = 6` triples, 30% of the total, can be made only when goods cross a border. The lecture's six-type, four-region example with `r = 3` gave at least 80%. One more type per region cuts the forced trade by more than half.
</details>

8. *Week 2 · compute.* A highland zone's spawn table has 60 mountain goats (50 kg each), 12 snow leopards (45 kg each) and 2 griffons (400 kg each). Compute prey and predator mass and the predator-to-prey ratio. Compare with the ten percent guide, and turn the result into one tension for the week 1 ledger.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Prey 3,000 kg. Predators 1,340 kg. Ratio about 45%, four and a half times the rough guide of 300 kg.

Prey: `60 × 50 = 3,000` kg. Predators: `12 × 45 = 540` plus `2 × 400 = 800`, total 1,340 kg. The ten percent rule is about production over time, so treat it as a loose guide. Even so, 45% is far past a plausible standing ratio.

A tension that explains it: the griffons do not hunt here at all. A lowland lord pays herders to drive goats up to the griffon eyries each spring, to keep the griffons from raiding the valley flocks. The herders want the payment to continue, and the lord wants to stop paying. That is a want and a block, and it gives the zone a quest hub.
</details>

---

## Week 3: Factions and conflict

Lecture: [w03, factions and conflict](../lectures/w03-factions-and-conflict.md). Model: structural balance and the tension index `T = unbalanced triads / complete triads`.

9. *Week 3 · compute.* Six factions form two blocs, {A, B, C} and {D, E, F}, with every pair inside a bloc allied and every pair across blocs hostile. (a) How many triads are there, and what is `T`? (b) B and E sign a secret pact. What is `T` now? (c) Later C and F also make peace. What is `T` after both changes?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 20 triads, `T = 0`. (b) `T = 4 / 20 = 20%`. (c) `T = 8 / 20 = 40%`.

(a) `C(6, 3) = 20`. A two-bloc web is balanced, so every triad is balanced.

(b) The B and E pair sits in `n − 2 = 4` triads, one with each of A, C, D and F. Each was balanced and now flips, so 4 are unbalanced.

(c) The C and F pair sits in 4 more triads. No triad contains both pairs, because that would need four factions. So 8 are unbalanced. Two flips across the same divide doubled the pressure without creating a new bloc.
</details>

10. *Week 3 · analysis.* A four-faction web has these relationships: Crown and Temple allied, Crown and Guild hostile, Temple and Guild hostile, Temple and Clans allied, Guild and Clans hostile. Crown and Clans are neutral. (a) How many complete triads are there, and what is `T`? (b) The first expansion must give Crown and Clans a sign. Compute `T` for "allies" and for "enemies". (c) Which is the better choice for a writer who wants the expansion to end with an open political question?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 2 complete triads, `T = 0`. (b) Allies: `T = 0 / 4`. Enemies: `T = 2 / 4 = 50%`. (c) Enemies.

(a) Only {Crown, Temple, Guild} (`+ − −`) and {Temple, Guild, Clans} (`− − +`) are complete. Both are balanced.

(b) Allies completes {Crown, Temple, Clans} as `+ + +` and {Crown, Guild, Clans} as `− − +`, both balanced. The web becomes two camps, {Crown, Temple, Clans} against {Guild}. Enemies makes {Crown, Temple, Clans} `+ + −` (the Temple's two friends hate each other) and {Crown, Guild, Clans} `− − −`. Two unbalanced triads.

(c) Allies closes the political story into a three-against-one war. Enemies leaves the Temple pulled between the Crown and the Clans, which is the next expansion's beat. The neutral edge was a reserved choice, and the model tells you what each way of spending it buys.
</details>

11. *Week 3 · compute.* Six factions are all at war with each other. What is the smallest number of relationships you must change to allied to reach zero tension? Show the camp sizes you compared.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 6.

Zero tension needs at most two camps, all positive inside and all negative across. Cross-camp edges are already negative, so the cost is the number of edges inside the camps.

| Camps | Edges to make allied |
|---|---|
| 3 and 3 | `3 + 3 = 6` |
| 2 and 4 | `1 + 6 = 7` |
| 1 and 5 | `0 + 10 = 10` |
| one camp of 6 | 15 |

Two equal camps are cheapest. Pacifying an all-against-all world takes six separate treaties, which is a lot of story, and it ends in a two-bloc war.
</details>

12. *Week 3 · analysis.* In The Burning Crusade, the Warcraft Wiki's rule is that reputation gained with the Scryers comes with a loss 10% larger with the Aldor, and the reverse. (a) A player earns 1,500 Scryer reputation. How much Aldor reputation do they lose? (b) Explain in balance terms why a two-faction player war like World of Warcraft's Horde and Alliance can never be unbalanced, while this reputation pair needed a rule.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 1,650. (b) Two factions form no triad. The reputation pair forms a triad once the player is a node.

(a) `1,500 × 1.1 = 1,650`.

(b) With two factions there is one relationship and no triad, so `T` is not defined and nothing can pull the war toward a new alignment. The Aldor and Scryers are a hostile pair, and the player is a third node. A player friendly with both would sit in a `+ + −` triad, which is unbalanced. The rule forces the player's edge with one side negative as the other rises, so the player's triad stays balanced by construction. Without it, players could farm both sides at no cost, which the lecture calls a design leak.
</details>

---

## Week 4: History and timelines

Lecture: [w04, history and timelines](../lectures/w04-history-and-timelines.md). Model: the lore clock, `w(t) = w0 + r × t + J × floor(t / T)`.

13. *Week 4 · compute.* A game launches in the year 800 of its calendar. It drifts `r = 0.5` in-world years per real year and jumps `J = 2` years with each expansion, shipped every `T = 2` real years. It ships 5 story beats per real year. A regent is 20 at launch. At real year 7, compute the in-world year, the span, the density, the regent's age and the time gap for a new player.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Year 809.5, span 9.5, density 3.7 beats per in-world year, regent 29.5, time gap 9.5 years.

Expansions shipped: `floor(7 / 2) = 3`. `w = 800 + 0.5 × 7 + 2 × 3 = 800 + 3.5 + 6 = 809.5`. The span is 9.5. Beats: `5 × 7 = 35`, so `D = 35 / 9.5 = 3.68`. The regent is `20 + 9.5 = 29.5`. The time gap is the span seen from the starting zone, 9.5 years.
</details>

14. *Week 4 · analysis.* An invented MMO launched in the year 300. Eight real years later its newest content is dated 312. It shipped three expansions in that time, and each opened with "two years later". What is its effective drift `r`, once the jumps are removed? Why is this worth separating from the total?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `r = 0.75`.

Total span 12 years. Jumps account for `3 × 2 = 6`. The other 6 years came from drift over 8 real years, so `r = 6 / 8 = 0.75`.

The two parts have different costs. Jumps happen between expansions, so characters change off screen and the jump can hide a lot. Drift happens inside an expansion's patch cycle, so NPCs age while players watch, and players who do the arithmetic notice. A team that wants to slow the clock needs to know which lever it has been pulling.
</details>

15. *Week 4 · design.* A director wants characters to age "a little" over the first ten real years, with the in-world span no larger than 3 years, and no expansion jumps. The game ships 6 beats per real year. Choose `r`, then give the density and the time gap at year 10. What does the team give up?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `r = 0.3`. Density 20 beats per in-world year, time gap 3 years.

With `J = 0`, the span at year 10 is `10r ≤ 3`, so `r ≤ 0.3`. At `r = 0.3`, `S = 3`, `D = 60 / 3 = 20`, and the time gap is 3 years.

The team gives up room for consequence. Twenty world-changing beats per in-world year is a crowded calendar. A three-year gap is small enough that most launch zones can stay undated or mark themselves as "three years ago" with one line. A war can end, but only a short one.
</details>

16. *Week 4 · analysis.* A student's history chapter dates every event in the deep past to the exact year, from the founding of the first kingdom 2,400 years ago to last spring. Using the precision gradient and week 11's blast radius, explain what this costs a live team, and rewrite the rule the chapter should follow.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Every exact date is a constraint on future writers, and old dates tend to be roots with large blast radii.

The deep past sits under many later facts: dynasties, ruins, grudges. In week 11 terms these are roots, and a root's blast radius covers everything built on it. An exact date at a root means any later story that needs the past to move has to review all of it. A vague date ("in the age of the Twin Crowns") is a small reservoir of freedom.

The rule: exact years and named people for the last fifty years, approximate dates for the last five centuries, and only order ("this before that") for the deep past. Players read the vagueness as realism, since real societies know their recent past better than their distant past.
</details>

---

## Week 5: Cultures, languages, names

Lecture: [w05, cultures, languages, names](../lectures/w05-cultures-languages-names.md). Model: name overlap, `P_amb(L) = (1 − m) × o^L`.

17. *Week 5 · compute.* Two invented cultures. The Kethri use eight syllables: *ko* 0.25, *ri* 0.15, *ma* 0.10, and *ul*, *ten*, *sa*, *vo*, *dre* at 0.10 each. The Garthun use six: *ko* 0.05, *ri* 0.05, *ma* 0.05, *gar* 0.30, *thu* 0.30, *dak* 0.25. Compute the count view and the weighted overlap in both directions, and `P_amb(2)` and `P_amb(3)` for each culture with no marker.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Direction | `o_count` | weighted `o` | `P_amb(2)` | `P_amb(3)` |
|---|---|---|---|---|
| Kethri could pass for Garthun | 0.375 | 0.50 | 25.0% | 12.5% |
| Garthun could pass for Kethri | 0.500 | 0.15 | 2.25% | 0.34% |

Shared syllables: *ko*, *ri*, *ma*. Kethri count view `3 / 8 = 0.375`. Garthun `3 / 6 = 0.5`. Weighted: Kethri `0.25 + 0.15 + 0.10 = 0.50`, Garthun `0.05 × 3 = 0.15`.

The count view says Garthun names are the more confusable ones. The weighted view says the reverse, by a factor of more than ten at two syllables. The Kethri lean on the shared syllables, and the Garthun barely touch them.
</details>

18. *Week 5 · design.* For the Kethri in question 17, what share of names `m` must carry a structural marker so that `P_amb(2)` is at most 5%? Name a marker that would fit a culture whose names come from a river people's glossed morphemes.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `m ≥ 0.8`.

`(1 − m) × 0.5² ≤ 0.05` gives `1 − m ≤ 0.2`. Four names in five need the marker.

A fitting marker is a fixed ending that the Garthun never use, for example a glossed suffix meaning "of the river", attached to every personal name. It works because it identifies the culture whatever the other syllables are, and because it carries meaning, so it doesn't read as decoration.
</details>

19. *Week 5 · compute.* Predict what this code prints, then run it. What does the second number say about markers compared with length?

```python
def ambiguity(o, L, m=0.0):
    return (1 - m) * o ** L

lengths = {2: 0.4, 3: 0.6}   # share of names with 2 and 3 syllables
mixed = sum(share * ambiguity(0.5, L) for L, share in lengths.items())
print(round(mixed, 4))
print(round(ambiguity(0.5, 2, m=0.5), 4))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
0.175
0.125
```

The mix is `0.4 × 0.25 + 0.6 × 0.125 = 0.1 + 0.075 = 0.175`. Moving 60% of names to three syllables brings the average down to 17.5%.

The second line is two-syllable names with half of them marked: `0.5 × 0.25 = 0.125`. Marking half the names does better than lengthening most of them, and it costs no screen space. It does cost a rule writers must follow, so it needs a generator or a name list.
</details>

20. *Week 5 · analysis.* In the lecture's in-class activity, most pairs find that their hand-written names are more ambiguous than their inventories predicted. Explain why using the weighted model, and say what fix follows.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Writers overuse the easy syllables, and the easy syllables tend to be the shared ones, so the real `o` is higher than the planned one.

The inventory records the weights the designer intended. Writing by hand draws on habit. Short open syllables like *an*, *el* or *ko* are easy to write and appear in many cultures' inventories, so a hand-written list leans on them. That raises the weighted overlap, and `P_amb` rises as a power of it. Because the model is directional, the culture that leans hardest on shared syllables suffers most.

The fix is to measure the weights from the names actually written, not from the plan, and to hold writers to the plan with a name list or a generator. A marker is the backup, since it works whatever the weights turn out to be.
</details>

---

## Week 6: Religion and myth in fiction

Lecture: [w06, religion and myth in fiction](../lectures/w06-religion-and-myth-in-fiction.md). Model: myth triangulation, settled `S`, answerable `A` and unrecoverable `U`.

21. *Week 6 · compute.* With `k = 3` accounts, `p = 0.5` and `q = 0.1`, compute the shares of core facts that end up settled, answerable and unrecoverable. Check `A` by hand.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `S = 42.5%`, `A = 7.5%`, `U = 50%`.

`s = 1 − 0.5 − 0.1 = 0.4`.

`U = 0.5³ + 3 × 0.5 × 0.5² = 0.125 + 0.375 = 0.5`.

`S = 0.9³ − 0.4³ − 3 × 0.5 × 0.4² = 0.729 − 0.064 − 0.240 = 0.425`.

`A = 1 − 0.5 − 0.425 = 0.075`. By hand: with three accounts, two or more true tellings plus a distortion means exactly two true and one distorted, `3 × 0.5² × 0.1 = 0.075`.
</details>

22. *Week 6 · analysis.* Keep `p = 0.5` and `q = 0.1`, and compute the split for `k = 4` and `k = 5`. For a ledger of 20 core facts at `k = 4`, how many facts land in each outcome? The lecture found that settled facts peak and fall as `k` grows at `q = 0.2`. Do they fall here by `k = 5`? Why?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| `k` | Settled | Answerable | Unrecoverable |
|---|---|---|---|
| 4 | 50.25% | 18.5% | 31.25% |
| 5 | 51.6% | 29.6% | 18.75% |

At `k = 4` with 20 facts: about 10.05 settled, 3.7 answerable and 6.25 unrecoverable.

Settled still rises from 4 to 5 accounts here, only slightly. Each new account can settle a fact by adding a second true telling, and can unsettle one by distorting it. With `q = 0.1`, distortion is rare, so the settling effect still wins at five accounts. At `q = 0.2` the unsettling effect catches up sooner. The peak exists for any `q > 0`, but low distortion pushes it to larger `k`.
</details>

23. *Week 6 · compute.* A casual player reads only one account, with `p = 0.35` and `q = 0.15`. What share of the core facts does it state, and what share of its statements are true? What does the lecture say this means for how you write each account?

<details>
<summary>Answer and worked solution</summary>

**Answer:** It states 50% of the facts, and 70% of its statements are true.

`p + q = 0.5` stated. `0.35 / 0.5 = 0.7` true. The reader has no way to tell which 30% are wrong.

Each account has to work as a good story on its own, in its own voice, because that single-reader view is what most players get. Nothing a player needs to follow the main story (GD202 week 10's need-to-know tier) should depend on comparing accounts.
</details>

24. *Week 6 · analysis.* A myth has six core facts and four accounts. Account 4 is a translation of account 3 and repeats its distortions exactly. T is a true telling, D a distorted one, and a blank is silence. Classify each fact the way a player comparing accounts would see it, and say which classifications are wrong once you know about the translation.

| Fact | Acc 1 | Acc 2 | Acc 3 | Acc 4 (copy of 3) |
|---|---|---|---|---|
| F1 | T | T | T | T |
| F2 | T | D | | |
| F3 | T | | T | T |
| F4 | | | | |
| F5 | | T | D | D |
| F6 | T | T | D | D |

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Fact | What players see | What is really supported |
|---|---|---|
| F1 | Settled | Settled (accounts 1, 2 and the 3-4 pair) |
| F2 | Unrecoverable (one true telling against a distortion) | Unrecoverable |
| F3 | Settled (three true tellings) | Settled, but by two independent witnesses, not three |
| F4 | Unrecoverable | Unrecoverable |
| F5 | The false version looks confirmed (told twice); the truth is told once | Unrecoverable. The false version is one witness, copied |
| F6 | Two versions each told twice: looks like an even dispute | Answerable. Two independent true tellings against one distortion |

A copied pair is one witness. It inflates agreement on everything the original says. On F5 it manufactures false consensus, which the lecture warns is an embarrassment unless you planned it. On F6 it turns a fact that fans could solve into one that looks like a coin toss.
</details>

---

## Week 7: Lore delivery in MMOs

Lecture: [w07, lore delivery in MMOs](../lectures/w07-lore-delivery-in-mmos.md). Model: lore memory, `K(m) = a × s^m + r × (1 − s^m)`.

25. *Week 7 · compute.* A story beat reaches `a = 0.7` of the live audience. Monthly churn is 8%. Compute the half-life of the release cohort, and the knowledge share at 12 and 24 months if the beat is temporary (`r = 0`) and if newcomers find it with `r = 0.6`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Half-life 8.3 months. Temporary: 25.7% and 9.5%. With `r = 0.6`: 63.7% and 61.4%.

`s = 0.92`. Half-life `ln 2 / −ln 0.92 = 0.693 / 0.0834 = 8.3` months.

`0.92^12 = 0.368` and `0.92^24 = 0.135`.

Temporary: `0.7 × 0.368 = 0.257` and `0.7 × 0.135 = 0.095`.

With `r = 0.6`: `0.257 + 0.6 × 0.632 = 0.637` and `0.095 + 0.6 × 0.865 = 0.614`. The curve drifts from 70% down toward 60%, because `r < a`.
</details>

26. *Week 7 · design.* An expansion ships 18 months after a foundation beat with `a = 0.85`. Churn is 5% a month. The team wants `K ≥ 0.6` at the expansion's release so the opening scene can assume players were there. What catch-up reach does the beat need?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `r ≈ 0.44`.

`s^18 = 0.95^18 = 0.397`. `r = (0.6 − 0.85 × 0.397) / (1 − 0.397) = (0.6 − 0.338) / 0.603 = 0.435`.

About 44% of newcomers must still meet the beat. A gated or optional replay rarely reaches that. The team should put the beat on the main path, raise `r` with a re-release, or rewrite the opening scene so it assumes only "has heard of it".
</details>

27. *Week 7 · compute.* A one-off live event reaches 90% of the live audience, and churn is 10% a month. In which whole month after release does its knowledge share first fall below 50%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Month 6.

`K(m) = 0.9 × 0.9^m`. At month 5, `0.9 × 0.590 = 0.531`. At month 6, `0.9 × 0.531 = 0.478`. Solving directly, `m = ln(0.5 / 0.9) / ln 0.9 = 5.6`.

Nobody forgot the event. Half a year of turnover replaced enough of the population that most players were never there.
</details>

28. *Week 7 · compute.* A beat sits on the required main story with `a = 0.8`, `r = 0.9` and 10% monthly churn. At month 12 the studio removes the chapter from the game, as Destiny 2's content vault did to its campaigns, and `r` drops to zero. Compute `K` at month 12, and at month 24 with and without the removal.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `K(12) = 87.2%`. At month 24: 24.6% after removal, 89.2% if kept.

`K(12) = 0.8 × 0.282 + 0.9 × 0.718 = 0.872`.

After the removal nobody new meets the beat, so `K` decays at the churn rate from 87.2%: `0.872 × 0.9^12 = 0.872 × 0.282 = 0.246`.

If kept, `K(24) = 0.8 × 0.080 + 0.9 × 0.920 = 0.892`. One decision moves the beat from the best-known fact in the setting to one that three players in four never saw, within a year.
</details>

29. *Week 7 · analysis.* A writer argues: "The launch event had 85% participation, so the expansion can treat it as common knowledge." Using the model, give two reasons this is wrong a year later, and say which of the lecture's two kinds of beat the event should have been.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Participation is `a`, and after two half-lives `K` is set by `r`, not `a`. And first-hand knowledge is not the same as having heard of it.

First, 85% of players active that month took part. With 10% monthly churn, only 28% of the population a year later was active that month. If the event was temporary, `K(12) = 0.85 × 0.282 = 24%`.

Second, many of the rest may know the fact from a wiki or a guildmate, which is enough for a line of dialogue but not for a scene whose weight depends on "you were there".

If the expansion depends on the event, it was a foundation and needed high `r`: delivery on the main path, in world geometry, or a replayable version. Delivering a foundation as a moment is the mistake behind most "what happened to the city?" threads.
</details>

---

## Week 8: Player agency vs canon

Lecture: [w08, player agency vs canon](../lectures/w08-player-agency-vs-canon.md). Model: canon fit, `F = p_1 × … × p_n`, and expected contradictions `E`.

30. *Week 8 · compute.* An expansion canonizes the majority option of six earlier choices, with take rates 0.85, 0.70, 0.65, 0.55, 0.50 and 0.50. Compute the fit, the expected number of contradictions, and the most common number of contradictions per player.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `F = 5.3%`, `E = 2.25`. The most common experience is being contradicted twice.

`F = 0.85 × 0.70 × 0.65 × 0.55 × 0.50 × 0.50 = 0.053`.

`E = 0.15 + 0.30 + 0.35 + 0.45 + 0.50 + 0.50 = 2.25`.

The Poisson binomial distribution, built one choice at a time as in the lecture's code:

| Contradictions | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| Share | 5.3% | 21.1% | 33.3% | 26.6% | 11.2% | 2.3% | 0.2% |

Every canon option is a majority or a tie, and about one player in nineteen has a history the expansion fully matches.
</details>

31. *Week 8 · design.* The team in question 30 can afford to honor two of the six choices. Which two should it honor, and what are `F` and `E` then? Compare with honoring the two most lopsided choices.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Honor the two 50/50 choices. `F = 21.3%` and `E = 1.25`. Honoring the 0.85 and 0.70 choices gives only `F = 8.9%`.

Honoring choice `i` multiplies `F` by `1 / p_i`, which is largest for the smallest `p_i`.

- Honor both 0.50 choices: `F = 0.85 × 0.70 × 0.65 × 0.55 = 0.213`. `E = 0.15 + 0.30 + 0.35 + 0.45 = 1.25`.
- Honor 0.85 and 0.70: `F = 0.65 × 0.55 × 0.50 × 0.50 = 0.089`.

The same writing budget gives more than twice the fit when it goes to the even splits.
</details>

32. *Week 8 · compute.* (a) Convert the six take rates in question 30 into dissonance bits and check that they reproduce `F`. (b) A choice had three options chosen by 50%, 30% and 20% of players. For story reasons the team canonizes the 30% option. How many bits does it cost, and how does that compare with canonizing the majority?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) The bits are 0.23, 0.51, 0.62, 0.86, 1.00 and 1.00, summing to 4.23, and `2^(−4.23) = 0.053`. (b) 1.74 bits, against 1.00 bit for the majority option.

(a) `−log2(p)` for each take rate: `−log2(0.85) = 0.23`, `−log2(0.70) = 0.51`, `−log2(0.65) = 0.62`, `−log2(0.55) = 0.86`, and 1.00 for each 0.50.

(b) `−log2(0.30) = 1.74`. The story choice costs 0.74 bits more than the majority, which lowers `F` by a factor of `2^0.74 = 1.67`. That may be worth paying, and the model tells you the price in the same unit as everything else in the expansion.
</details>

33. *Week 8 · analysis.* Half the players are loyalists, who pick the canon option on each of four choices with probability 0.95. The other half are rebels, who pick it with probability 0.35. Compute the take rate per choice, the fit under the independence assumption and the real fit. What does the per-choice telemetry report hide?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Take rate 0.65. Independent fit 17.9%. Real fit 41.5%.

Take rate: `0.5 × 0.95 + 0.5 × 0.35 = 0.65`. Independent: `0.65^4 = 0.179`. Real: `0.5 × 0.95^4 + 0.5 × 0.35^4 = 0.5 × 0.815 + 0.5 × 0.015 = 0.415`.

The report shows four choices at 65% agreement each. It hides that loyalists fit 81% of the time and rebels 1.5% of the time. The contradictions fall almost entirely on one half of the population, who learn that the game never listens to them. You need the per-player distribution split by segment, which lab 08 builds.
</details>

34. *Week 8 · critique.* A narrative lead writes: "We'll honor the execution of the smuggler, because it's the most dramatic choice in the launch story. It went 92/8. Everything else we canonize by majority." Critique the plan with the model and propose a better rule.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Honoring a 92/8 choice multiplies fit by only `1 / 0.92 = 1.09`. The budget should go to the most even split.

A choice where 92% of players agree with the canon option contradicts 8% of players and costs 0.12 bits. Honoring it removes almost nothing. The same variant budget spent on a 50/50 choice doubles the fit.

Better rule: honor the most even splits, canonize the lopsided ones, absorb the ones that matter little. If the dramatic choice matters to the story, canonize it and give the 8% a personal-canon acknowledgement in their own dialogue. Decide the answer for each choice when it is written, not when the expansion needs it.
</details>

---

## Week 9: Living world events

Lecture: [w09, living world events](../lectures/w09-living-world-events.md). Model: the realm clock, `R = N × q × u`, with fatigue `d` and ceiling `q × u / (1 − d)` per active player.

35. *Week 9 · compute.* Two realms of 2,000 and 8,000 active players face a fixed collective goal of 360,000 units. Participation is `q = 0.15` and each participant delivers `u = 12` units a day, with no fatigue. Compute each realm's daily rate, finish day and goal per active player.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Small realm 3,600 a day, day 100, 180 units per player. Large realm 14,400 a day, day 25, 45 units per player.

`R = N × 0.15 × 12 = 1.8N`. Small: `R = 3,600`, `T = 360,000 / 3,600 = 100`. Large: `R = 14,400`, `T = 25`.

Goal per player: `360,000 / 2,000 = 180` and `360,000 / 8,000 = 45`. A four-fold spread in population becomes a four-fold spread in finish dates and in effort per player.
</details>

36. *Week 9 · compute.* Add daily fatigue `d = 0.98` to question 35. What is the ceiling per active player? On which day does each realm finish, if ever?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Ceiling 90 units per player. The small realm never finishes. The large realm finishes on day 35.

Ceiling: `q × u / (1 − d) = 1.8 / 0.02 = 90`.

Small realm: its goal of 180 per player is twice the ceiling, so it is never reached.

Large realm: `x = 1 − 360,000 × 0.02 / 14,400 = 1 − 0.5 = 0.5`. `ln 0.5 / ln 0.98 = 34.3`, so day 35.
</details>

37. *Week 9 · design.* Switch the event in question 36 to a scaled goal. The narrative window runs from day 14 to day 40, and fatigue stays at 0.98. What is the largest goal per player `g` that finishes by day 40? Pick a round `g` below it and give the finish day with and without fatigue.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `g ≤ 49.9`. With `g = 45`, every realm finishes on day 35 with fatigue and day 25 without.

By day 40 a realm can deliver `90 × (1 − 0.98^40) = 90 × 0.554 = 49.9` units per player.

At `g = 45`: without fatigue, `T = 45 / 1.8 = 25`. With fatigue, `x = 1 − 45 × 0.02 / 1.8 = 0.5`, so again day 35. Both land inside the window on every realm, since a scaled goal makes the finish day independent of population.
</details>

38. *Week 9 · analysis.* A designer argues that a fixed goal is fairer, since "everyone faces the same number". Give the model's answer, and then give one story in which the fixed goal's spread of dates is the point rather than a bug.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The same total asks each player on a small realm to do more, in inverse proportion to population. A fixed goal is still right when "our realm did it, whenever we managed it" is the story.

With a fixed goal, effort per player is `G / N`. In question 35 the small realm's players each owe four times what the large realm's owe. Equal effort per player is a scaled goal.

A spread can be the point. If the event is "each realm's players open the gates themselves", a small realm that finishes after weeks has a story the large realm does not. The cost is several histories at once, so write "during" content about the effort, "after" content that does not depend on the date, and a fallback on `D_max` for realms that stall under fatigue.
</details>

---

## Week 10: Expansion planning

Lecture: [w10, expansion planning](../lectures/w10-expansion-planning.md). Model: the foreshadow horizon, `E(d) = s^d × v × d − (1 − s^d) × D` and `d* = −1 / ln(s) − D / v`.

39. *Week 10 · compute.* A team with plan-change rate `ρ = 0.25` plants a hook with `v = 1` and `D = 1`. Compute `d*`, and `E(d)` at the two nearest whole numbers.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `d* = 2.48`. `E(2) = E(3) = 0.69`.

`s = 0.75`. `−1 / ln 0.75 = 3.48`, so `d* = 3.48 − 1 = 2.48`.

`E(2) = 0.5625 × 2 − 0.4375 × 1 = 1.125 − 0.4375 = 0.6875`.
`E(3) = 0.4219 × 3 − 0.5781 × 1 = 1.2656 − 0.5781 = 0.6875`.

They tie, as they should when the continuous optimum sits almost exactly between them.
</details>

40. *Week 10 · compute.* Your studio's last roadmap planned 24 hooks for the next cycle, and 6 of them changed. Estimate `ρ`. With `v = 1`, compute `d*` for a named villain (`D = 2`) and for an on-stage announcement (`D = 4`). When should each first appear?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `ρ = 0.25`. Named: `d* = 1.48`, plant one or two cycles ahead (`E = 0.25` either way). Announced: `d* = 0`, do not announce ahead.

`ρ = 6 / 24 = 0.25`, and `−1 / ln 0.75 = 3.48`.

Named: `3.48 − 2 = 1.48`. `E(1) = 0.75 − 0.25 × 2 = 0.25`. `E(2) = 0.5625 × 2 − 0.4375 × 2 = 0.25`.

Announced: `3.48 − 4 = −0.52`, floored at 0. At this team's stability, any lead time loses value in expectation, so a public roadmap is a bet the team should not make. Plant vague hooks early instead and name the villain late.
</details>

41. *Week 10 · analysis.* A stable team (`ρ = 0.15`, `v = 1`) wants to plant a hook four cycles ahead. Compare `E(4)` for a vague hook (`D = 0.5`) and an announced one (`D = 4`), and give each hook's `d*`. What does the difference say about specificity?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Vague `E(4) = 1.85`, `d* = 5.65`. Announced `E(4) = 0.18`, `d* = 2.15`.

`s^4 = 0.85^4 = 0.522`. Vague: `0.522 × 4 − 0.478 × 0.5 = 2.088 − 0.239 = 1.85`. Announced: `2.088 − 0.478 × 4 = 2.088 − 1.912 = 0.18`.

`−1 / ln 0.85 = 6.15`, so `d*` is `6.15 − 0.5 = 5.65` and `6.15 − 4 = 2.15`.

Same lead time, same team, a tenfold difference in expected value. Specificity is a cost you add as the payoff approaches. This is week 4's precision gradient pointed at the future.
</details>

42. *Week 10 · compute.* Predict what this code prints, then run it. Which whole lead time is best, and what kind of team and hook does it describe?

```python
import math

def expected_value(d, v, D, rho):
    s = 1 - rho
    return s**d * v * d - (1 - s**d) * D

rho, D = 0.3, 0.5
print([round(expected_value(d, 1, D, rho), 2) for d in range(6)])
print(round(max(0.0, -1 / math.log(1 - rho) - D), 2))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
[0.0, 0.55, 0.72, 0.7, 0.58, 0.42]
2.3
```

The best whole lead time is 2 cycles, with `E = 0.72`. It describes a volatile team (`ρ = 0.3`) planting a vague hook. The lecture showed that the same team with a named hook (`D = 2`) had `d* = 0.80` and lost value past one cycle. Making the hook vague buys this team about one and a half extra cycles of lead time.
</details>

43. *Week 10 · critique.* After a stakes climb that ended at rung 5, a producer proposes: "Next expansion: a new villain who threatens reality itself, announced on stage now with a three-year roadmap." The team's `ρ` is 0.2. Critique the proposal with both parts of the lecture.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The announcement's `d*` is 0.48 at this `ρ`, so a three-cycle roadmap has negative expected value. And a second rung-5 threat invites an invented rung 6.

Foreshadowing: with `ρ = 0.2`, `D = 4` and `v = 1`, `d* = 4.48 − 4 = 0.48`. A three-cycle lead has `E(3) = 0.512 × 3 − 0.488 × 4 = 1.536 − 1.952 = −0.42`.

Stakes: after the fabric of reality, "bigger" means inventing a rung above the top, or repeating the top. Better plan: step down or change the kind of stakes (a personal succession at rung 1 or 2), and keep the world-scale thread alive with a vague hook (`D` about 0.5) that can be planted now and named later. Write the step-down into the bible alongside the climax so it reads as a new season.
</details>

---

## Week 11: Retcons and continuity

Lecture: [w11, retcons and continuity](../lectures/w11-retcons-and-continuity.md). Model: the retcon blast radius, `radius(x) = |Desc(x)|` and cost `W(x)`.

44. *Week 11 · compute.* Extend the lecture's *Thornmere* canon graph with two nodes. Q2 is a new quest chain, "The Signet Road" (cost 6 writer-days), that depends on T1 (the Tidewarden reputation faction) and I1 (the signet's item text). S1 is a printed art book caption about Harrow's tomb, which depends on R1 and is frozen. Compute the radius, cost and frozen set for F2, F3, F4 and T1.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Fact | Radius | Cost `W` | Frozen touched |
|---|---|---|---|
| F2 | 8 | 64.5 | S1 |
| F3 | 8 | 51.5 | N1, S1 |
| F4 | 4 | 37.5 | S1 |
| T1 | 1 | 11 | none |

F2 already reached F4, Y1, D1, I1, R1 and Y2. Q2 hangs under I1 and S1 under R1, so both join: radius 8, cost `58.5 + 6 = 64.5`, and the frozen caption now sits under F2.

F3 reached F4, Q1, T1, N1, I1 and R1. Q2 joins through T1 and I1 (counted once), S1 through R1: radius 8, cost `45.5 + 6 = 51.5`, frozen {N1, S1}.

F4: descendants I1, R1, Q2, S1. Cost `1 + 0.5 + 30 + 6 = 37.5`.

T1: descendant Q2. Cost `5 + 6 = 11`.

One art book caption has made Harrow's death (F4), both of its parents (F2, F3) and the root F1 impossible to change cleanly. That is what "price frozen media before you publish" means.
</details>

45. *Week 11 · compute.* A new expansion's main quest touches 40 canon facts. (a) With a per-fact memory error of `ε = 0.015`, what is the chance it contradicts something? (b) How low must `ε` be to bring that under 10%? (c) What is the chance with a continuity database that gets `ε` to 0.002?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 45.4%. (b) `ε ≤ 0.0026`. (c) 7.7%.

(a) `1 − 0.985^40 = 1 − 0.546 = 0.454`.

(b) `(1 − ε)^40 ≥ 0.9` gives `1 − ε ≥ 0.9^(1/40) = 0.99737`, so `ε ≤ 0.0026`.

(c) `1 − 0.998^40 = 0.077`.

A writer who is right 98.5% of the time contradicts canon in almost half of expansion-sized stories. The fix is cheap lookups, not better memory.
</details>

46. *Week 11 · design.* The design lead wants Queen Adelmar's death to have been murder, not illness, to set up the next expansion. In the extended graph of question 44, the fact of her death is a new node that nothing yet depends on, but the illness is stated in the coronation chain Y2 (cost 10). Propose the cheapest retcon type that delivers the goal, and price it against a substitutive rewrite of Y2.

<details>
<summary>Answer and worked solution</summary>

**Answer:** An additive retcon: keep the illness true and add a new fact that someone caused it. Its cost is the new content only. A substitutive rewrite of Y2 costs 10 writer-days plus Y2's own descendants, which are none in this graph.

Additive: "The illness was real, and it was poison." Every shipped line in Y2 stays true. The new node depends on Y2 and has no descendants yet, so the review set is the new content plus a check of Y2's wording.

Substitutive: rewriting Y2 to say murder costs its 10 days and contradicts what players already saw in the coronation chain, which is a voiced quest.

The additive version wins because it keeps what players already saw true and changes only what it meant. It is the same move as the lecture's spy retcon for Harrow.
</details>

47. *Week 11 · analysis.* Two game-tier facts disagree: the item text on Harrow's Signet (I1, cost 0.5) says the signet is silver, and the raid Harrow's Tomb (R1, cost 30) shows it as gold. A tie-in comic, frozen, also shows it as gold. Using the tier rules, say which fact wins and what the team should do.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Within a tier, a conflict is a bug, so one of the two game-tier facts must be fixed. Fix I1, the cheaper one, to gold. The comic then agrees with the game.

The tier table only settles conflicts between tiers. Two game-tier facts disagreeing is a bug, and the blast radius tells you which is cheaper to fix: I1 at half a day against R1 at 30. Choosing gold also matches the frozen comic, which can never be changed, so no permanent contradiction remains. Log the conflict so the team learns where `ε` is high.
</details>

---

## Week 12: Transmedia

Lecture: [w12, transmedia](../lectures/w12-transmedia.md). Model: required versus optional media, `C = s_1 × … × s_k` and `X = 1 − (1 − s_1) × … × (1 − s_k)`, with the Fréchet bounds.

48. *Week 12 · compute.* An expansion's plan has three outside pieces: an animated short (reach 50%), a printed novel (20%) and a web comic (40%). Compute `n`, `C` if all three are required, `X` if all three are optional, and the best and worst cases for both.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `n = 1.1`. `C = 4%` (bounds 0% to 20%). `X = 76%` (bounds 50% to 100%).

`n = 0.5 + 0.2 + 0.4 = 1.1`.

`C = 0.5 × 0.2 × 0.4 = 0.04`. Best case `min = 0.2`, worst `max(0, 1.1 − 2) = 0`.

`X = 1 − 0.5 × 0.8 × 0.6 = 1 − 0.24 = 0.76`. Worst case `max = 0.5`, best `min(1, 1.1) = 1`.

However loyal the fans, no more than one player in five can follow a story that requires the novel.
</details>

49. *Week 12 · compute.* Marketing offers either three paid novellas, each read by 10% of players, or one free in-client story read by 60%. All are optional. Which gives the higher extra share `X` on its own? Which gives more pieces per player?

<details>
<summary>Answer and worked solution</summary>

**Answer:** The in-client story: `X = 60%` against 27.1%. It also gives more pieces per player, 0.6 against 0.3.

Three novellas: `X = 1 − 0.9^3 = 1 − 0.729 = 0.271`, `n = 0.3`. In-client story: `X = 0.6`, `n = 0.6`.

Raise reach before you raise count. Three pieces that each reach a tenth of players leave nearly three quarters of the population with nothing extra.
</details>

50. *Week 12 · compute.* Existing optional media give `X = 50%`. You can add one more optional piece reaching 45%, or two reaching 25% each. Which raises `X` more, and by how much?

<details>
<summary>Answer and worked solution</summary>

**Answer:** The single 45% piece gives 72.5%. The two 25% pieces give 71.9%. The single piece wins by 0.6 points.

The missed-everything share is 0.5. One piece: `0.5 × 0.55 = 0.275`, so `X = 72.5%`. Two pieces: `0.5 × 0.75 × 0.75 = 0.281`, so `X = 71.9%`.

The two options are close because 0.55 and `0.75² = 0.5625` are close. Here the choice should turn on cost and on which piece carries a retell line better, not on `X`.
</details>

51. *Week 12 · analysis.* A raid's final cutscene assumes players know that the Tidewardens split, a fact established only in a web comic with 25% reach. The comic in turn depends on a quest chain in the game. Draw the arrows, say whether `C` or `X` applies to the raid, and write what the raid team must do.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Quest chain → comic → raid. The raid depends on the comic, so `C` applies and at most 25% of players can follow the cutscene. The raid team must add a retell line in the game.

The comic depending on the quest chain is safe. The raid depending on the comic makes it an AND over the comic's reach. Overlap can only lift `C` toward 25%.

The fix is a retell line on the main path before the raid, for example a Tidewarden quest-giver who refuses to work with "the other half of the order". It states the one fact the scene needs. With it, the comic becomes optional, and it moves from `C` to `X`, where every reader is a bonus.
</details>

---

## Week 13: Community lore and roleplay

Lecture: [w13, community lore and roleplay](../lectures/w13-community-lore-and-roleplay.md). Model: hub sizing, `λ = Λ / H`, live hubs `V = H × P_k(λ)` and scene share `S = P_{k−1}(λ)`.

52. *Week 13 · compute.* At 10 p.m., 20 roleplayers are in your capital looking for scenes that need `k = 3` people. Use the lecture's best-crowd table to estimate the best number of hubs, then check the neighbours with `V`. What is `S` at your choice?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Six hubs, `V = 3.88`, `S = 84.5%`.

For `k = 3`, `λ* = 3.38`, so `H ≈ 20 / 3.38 = 5.9`.

| `H` | `λ` | `P_3` | `V` | `S` |
|---|---|---|---|---|
| 5 | 4.00 | 76.2% | 3.81 | 90.8% |
| 6 | 3.33 | 64.7% | 3.88 | 84.5% |
| 7 | 2.86 | 54.4% | 3.81 | 77.9% |

Six hubs give the most live scenes by a small margin. Five gives almost as many and puts six more roleplayers in a hundred in a scene. A small or new community should take five.
</details>

53. *Week 13 · compute.* At 3 a.m. only 5 roleplayers are online, and tavern scenes need `k = 4`. Compute `V` and `S` for one and two hubs, and say what the bible should supply.

<details>
<summary>Answer and worked solution</summary>

**Answer:** One hub: `V = 0.74`, `S = 87.5%`. Two hubs: `V = 0.48`, `S = 45.6%`.

One hub, `λ = 5`: fewer than four is `e^(−5) × (1 + 5 + 12.5 + 20.83) = 0.00674 × 39.33 = 0.265`, so `P_4 = 0.735`. `S` needs at least three others: `1 − e^(−5) × (1 + 5 + 12.5) = 1 − 0.125 = 0.875`.

Two hubs, `λ = 2.5`: `P_4 = 0.242`, `V = 0.48`, `S = P_3(2.5) = 0.456`.

Two hubs at night leave more than half the roleplayers in empty rooms. The bible should name one "never closes" hub with an in-world reason (a night-watch tavern, a watch-fire), so the community's night convention has a home.
</details>

54. *Week 13 · compute.* A harvest festival draws 40 roleplayers for pageant scenes that need `k = 8`. Compare one to five districts with `V` and `S`, and recommend a number.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Four districts give the most live scenes (`V = 3.12`), but three give almost as many (2.86) with `S = 97.9%` against 87.0%. Recommend three.

| Districts | `λ` | `V` | `S` |
|---|---|---|---|
| 1 | 40.0 | 1.00 | 100% |
| 2 | 20.0 | 2.00 | 99.97% |
| 3 | 13.3 | 2.86 | 97.9% |
| 4 | 10.0 | 3.12 | 87.0% |
| 5 | 8.0 | 2.73 | 68.7% |

For `k = 8`, the best crowd per hub is about 10.4, so `H* ≈ 40 / 10.4 = 3.8`. The peak of `V` is at four. A festival is a one-night event where a roleplayer who walks into an empty district may not try again, so `S` matters more than a quarter of a scene.
</details>

55. *Week 13 · critique.* A student bible says: "The Order of the Tidewatch was wiped out at the Siege of Dikeholm. Only Sister Maelis survived, and she now runs the Anchor Inn, the only tavern in the city." Find the two problems for a roleplay community and rewrite the passage.

<details>
<summary>Answer and worked solution</summary>

**Answer:** It sets a "last of" trap, and it names a single hub with no fallback convention or open slots.

The "last of" trap: the lone survivor of a destroyed order is the most attractive character concept in the setting, and the lore forbids it. Players will play Tidewatch survivors anyway and contradict canon and each other.

The single tavern is fine at night but too few hubs at prime time for most communities, and it ties the hub to a named canon character that roleplayers cannot touch.

Rewrite: "The Order of the Tidewatch was broken at the Siege of Dikeholm. Its scattered sisters still keep the watch oath in secret, and nobody knows how many survive. They are said to meet at the Anchor Inn, which never closes, but the dockside taverns and the market steps are busier on market days."
</details>

---

## Week 14: Bible workshop

Lecture: [w14, bible workshop](../lectures/w14-bible-workshop.md). Model: the question queue, `λ_e = (1 − a) × λ` and `W = 1 / (μ − λ_e)`.

56. *Week 14 · compute.* A team of 15 writers asks 4 lore questions each per week. The lore lead answers 25 a week. Compute `a_min`, the answer rate for a one-working-day wait, and the load, wait and questions on the desk at `a = 70%`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `a_min = 58.3%`. One-day wait needs `a = 66.7%`. At 70%: load 0.72, wait 0.71 working days, 2.6 questions on the desk.

`λ = 60`, `μ = 25`. `a_min = 1 − 25 / 60 = 0.583`.

A one-day wait is `W = 0.2` weeks, so spare capacity must be 5 per week: `a = 1 − (25 − 5) / 60 = 0.667`.

At 70%, `λ_e = 0.3 × 60 = 18`. Load `18 / 25 = 0.72`. `W = 1 / 7 = 0.143` weeks, `× 5 = 0.71` days. By Little's law, `18 × 0.143 = 2.6` questions waiting or being answered.
</details>

57. *Week 14 · compute.* The team in question 56 doubles to 30 writers for an expansion, and the lead's capacity does not change. What are `a_min` and the answer rate for a one-day wait now? What happens at the old answer rate of 70%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `a_min = 79.2%` and a one-day wait needs 83.3%. At 70% the desk never clears.

`λ = 120`. `a_min = 1 − 25 / 120 = 0.792`. One day: `1 − 20 / 120 = 0.833`.

At 70%, `λ_e = 36`, which is more than `μ = 25`. The pile grows every week. To keep the same wait the bible has to answer a much larger share of questions than it did at launch.
</details>

58. *Week 14 · analysis.* A question test finds 22 of 32 questions answered or derivable. Compute `a` and its approximate 95% margin. For the team in question 56, can you say whether the desk is stable?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `a = 68.8%`, margin about 16.1 points, so roughly 52.7% to 84.8%. No, because the interval straddles `a_min = 58.3%`.

`a = 22 / 32 = 0.6875`. Margin `1.96 × √(0.6875 × 0.3125 / 32) = 1.96 × 0.0819 = 0.161`.

The point estimate is above `a_min`, and the low end is below it. One test finds gaps; it cannot certify stability. Fix the gaps by the ranking, then run a second test with new askers and new questions.
</details>

59. *Week 14 · compute.* For the team in question 56, the lead goes on leave and a junior writer covers at `μ = 10`. What answer rate does the bible need to stay stable during the leave? Name one other fix from the lecture.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `a ≥ 83.3%`.

`a_min = 1 − 10 / 60 = 0.833`. At the bible's current 70%, `λ_e = 18`, well above 10, so the desk would grow for the whole leave.

Another fix: train a second reader before the leave, so `μ` never drops that far. The lecture's point is that `μ` is fragile, and one person answering in order is a single point of failure.
</details>

60. *Week 14 · analysis.* A gap ranking from a question test gives: History 3 missing, 0 contradicted; Cultures 1 missing, 2 contradicted; Factions 2 missing, 1 contradicted; Community 4 missing, 0 contradicted. Which chapter do you fix first? A colleague says "Community has the most missing answers, so start there." Answer them.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Fix Cultures first (score 5), with Community close behind (4).

Scores are `missing + 2 × contradicted`: History 3, Cultures `1 + 4 = 5`, Factions `2 + 2 = 4`, Community 4.

A missing answer makes the writer ask, which costs a wait. A contradiction lets the writer find one of two answers and never ask, which ships an error. That is why contradictions count double, and why Cultures goes first even though it has the fewest missing answers.
</details>

---

## Across the course

These questions join models from different weeks. They are the kind the bible defence uses.

61. *Weeks 7 and 12 · compute.* An expansion's opening scene assumes players both took part in a temporary live event (`a = 0.8`, 10% monthly churn, the expansion ships 12 months later) and read a prequel novel with 15% reach. Assuming independence, what share of players at release can follow the scene as written? Name the two fixes, one from each week.

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 3.4%.

Week 7: `K(12) = 0.8 × 0.9^12 = 0.8 × 0.282 = 0.226`. Week 12: the scene is an AND over first-hand knowledge and the novel, so `0.226 × 0.15 = 0.034`.

Fixes: raise `r` for the event (a replayable version or a main-path retelling, week 7), and add a retell line for the novel's fact so it moves from `C` to `X` (week 12). Better still, rewrite the scene so it assumes "has heard of it" rather than "was there".
</details>

62. *Weeks 4, 10 and 11 · analysis.* Three lectures give the same advice from three directions: keep the deep past vague, plant vague hooks early, keep roots vague. State the shared principle in one sentence and give the number from each week that measures it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The more a fact will be depended on, or the longer it must hold, the less precise it should be.

- Week 4: the precision gradient. Exact years only for the last fifty years, because each exact date is a constraint on every later writer.
- Week 10: the broken-promise cost `D`. A vague hook with `D = 0.5` at `ρ = 0.2` has `d* = 3.98`, against 2.48 for a named one with `D = 2`.
- Week 11: the blast radius. The root F1 in *Thornmere*'s graph has radius 11 and reaches a frozen novella, so any precise detail placed there is the most expensive fact in the bible to change.
</details>

63. *Weeks 1, 3 and 9 · design.* Your ledger lists a structural tension: two port cities both claim the only deep-water harbour. Describe one collective-goal or contested event that spends a plot tension drawn from it, and say what the event should leave in the world so that the structural tension keeps producing plot tensions afterwards.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Any event whose outcome changes who holds the harbour for now, while leaving both claims alive, works.

Example: a contested outcome in which players on each realm back one city's fleet to rebuild the harbour wall. The winning city holds the harbour until the next event. The event spends one plot tension (who rebuilds the wall) and leaves changed geometry (a wall with one city's banners), a record of who did it (a monument per realm), and a grievance for the losing city.

The structural tension survives because the event never resolves the two claims. Week 1: `g` stays positive. Week 3: the two cities' edge stays negative, and any faction that helped the winner gains a new edge that can flip later. Week 9: write the fallback on `D_max` and the "after" state so it does not depend on the finish date.
</details>
