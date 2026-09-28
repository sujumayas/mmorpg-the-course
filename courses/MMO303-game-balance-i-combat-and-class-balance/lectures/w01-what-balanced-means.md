# MMO303 · Week 01 — What "Balanced" Means: Fairness, Viability, Diversity

**Why this matters:** Every patch note you will ever write claims to "improve balance," and players will argue with it in their thousands. If you cannot say which property you are fixing and how you would measure it, you are tuning numbers by mood, and the players will notice before you do.

**You will be able to:**
- Distinguish fairness, viability and diversity, and give a game where each one holds while another fails.
- Compute the effective number of classes from a pick-share table and convert it to a concentration index (HHI).
- Correct an observed win rate for mirror matches and explain why raw win rates mislead.
- Write a measurable balance target for an MMO class roster and critique one written by someone else.

**Before class:** Sirlin, "Balancing Multiplayer Games, Part 1: Definitions" and "Part 2: Viable Options" (sirlin.net, about 20 minutes together); Schreiber & Romero, *Game Balance* (2021), the opening chapter on what balance is.

**Prerequisites from earlier courses:** probability, shares and expected value from MA102 weeks 1 to 5 ([week 1, sample spaces and events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w01-sample-spaces-and-events.md) through [week 5, variance](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w05-variance-and-swingy-designs.md)); confidence intervals from [MA102 week 13](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (used briefly in section 3); stats and damage formulas from [GD203 week 1](../../GD203-combat-and-progression-design/lectures/w01-stats-as-design-language.md) and [GD203 week 2](../../GD203-combat-and-progression-design/lectures/w02-damage-formulas.md). Next week's lecture on [armor and damage mitigation](w02-armor-and-damage-mitigation.md) assumes the vocabulary you learn here.

**Interactive:** [examples/w01-effective-classes.html](../examples/w01-effective-classes.html) (built from the spec at the end of this lecture). Keep it open during section 3.

---

## 1. Three words players use as one

Open any class forum the week after a patch and you will read "this game is unbalanced." Ask five posters what they mean and you will get at least three different complaints.

- "The player who goes first always wins." That is a complaint about **fairness**.
- "My class can't clear the raid, so nobody invites me." That is a complaint about **viability**.
- "Everyone plays the same two classes." That is a complaint about **diversity**.

These are different properties. A game can have one and lack the others, and the fixes for each pull in different directions. Your first job as a balance designer is to name which one is broken. This lecture defines each, gives you a number for each, and spends most of its time on diversity, because it is the one MMO teams most often fail to measure.

A quick definition first. A **class** is a starting choice a player locks in before play, such as a character class, race, faction or deck. In modern MMOs the relevant unit is often the **spec** (specialization), a sub-choice within a class that changes its role and abilities. Everything in this lecture works the same for classes, specs, heroes or deck archetypes, so we will say "class" and mean whichever unit your game uses.

### Fairness

David Sirlin, a fighting-game designer who was lead designer of *Super Street Fighter II Turbo HD Remix* (Capcom, 2008), defines fairness narrowly. A game is fair if players of equal skill have roughly equal chances to win, whatever starting options they chose. Fairness is about the locked-in start, not about things you pick up during play.

The cleanest fairness problem has no classes at all. It is simply going first.

- In chess, White moves first. Across a large database of 731,740 games compiled by *New In Chess* in 2000, White scored 54.8%. Most collections put White between 52% and 56%.
- Go compensates the second player with **komi**, free points added to White's score. Standard komi is 6.5 points under Japanese and Korean rules and 7.5 under Chinese rules. The half point prevents ties.
- In *Hearthstone*, the player going first starts with 3 cards. The player going second starts with 4 cards plus The Coin, a spell that grants one extra mana crystal for a single turn.
- In *Magic: The Gathering*, the player who goes first in a two-player game skips the draw on their first turn.

Four games, one move. Measure the first-mover's win rate, then hand the second player a resource worth the difference. Notice that none of these games removed the asymmetry. They priced it.

For MMOs, the fairness question shows up in faction choice (does one side of a faction war win more battlegrounds?), in race or origin bonuses (does one race's passive ability win duels?), and in any open-world PvP where one class chooses when a fight starts. The measurement is the same as chess. Match players of similar rating, count wins by starting choice, and check the gap.

### Viability

Sirlin's definition of balance is about options, not outcomes. Paraphrased, a multiplayer game is balanced if a reasonably large number of the options available to the player are viable, especially at expert level. An option is **viable** if choosing it is a reasonable way to try to win. It does not need to be the best. It needs to be good enough that a skilled player picking it is not making a mistake.

Viability is a threshold, not a ranking. That matters a lot in MMOs.

- In PvP, the threshold is a win-rate band. A class that wins 50% of even matches is viable. One that wins 44% is not.
- In PvE, the threshold is the content. A raid boss with an **enrage timer** (a hard limit after which the boss kills everyone) sets a minimum group damage. A spec is viable for that boss if a normal group containing it clears the timer. Whether it does 3% less damage than the top spec is a separate question.

Riot Games made this kind of threshold public. Their Champion Balance Framework for *League of Legends*, published in May 2019, flags a champion as overpowered in the Average Play segment (everyone below the top 10% of solo queue) at a 54.5% win rate when its ban rate is low, sliding down to 52.5% as its ban rate rises. It flags a champion as underpowered below 49%. For professional play, where win rates are too noisy, the signal is presence (picked or banned): 90% presence in one patch, or 80% across consecutive patches, marks a champion overpowered, and 5% or less marks it underpowered.

Read those numbers as a designer. The band between 49% and about 54% is Riot's working definition of "viable." Inside it, they leave a champion alone.

### Diversity

**Diversity** is about what the population actually does. A game can have ten viable classes on paper and still see most players choose two. That happens when one class is a little better, a little easier, a little more fashionable, or simply the one the top guild uses. Small edges compound, because players copy what wins.

Diversity is the property players feel most directly ("every group has the same comp") and the one designers most often forget to measure. The rest of this lecture gives you the number.

### They come apart

Before the math, fix in your head that these three properties are independent.

| Situation | Fair? | Viable? | Diverse? |
|---|---|---|---|
| Chess with no komi-style fix | Slightly unfair (White 52-56%) | Yes | — (no class choice) |
| Eight classes, all within 49-53% win rate, but 70% of players pick one | Yes | Yes | No |
| One class wins 60% of duels, everyone plays it | No | No (others are mistakes) | No |
| A mirror-only game where everyone plays the same class by design | Yes | Yes | No, on purpose |

The second row is the MMO case that catches designers out. Every dashboard says "balanced," and the game still feels samey.

## 2. Worked example: how many classes do you really have?

### The hook

In 2019, *Overwatch* had a roster of dozens of heroes across three roles. Professional teams converged on a composition called **GOATS**, three tanks and three supports, with no damage heroes at all. It was strong enough that it dominated the Overwatch League and was widely called stale to watch. Blizzard's response was structural. It introduced **Role Queue**, which locks every team into two tanks, two damage and two supports. Role Queue reached the Overwatch League in Stage 4 of the 2019 season and the public competitive ladder at the start of Season 18 in September 2019.

The puzzle for you is this. The hero list never got shorter. Every hero was still in the game and every one was technically selectable. So in what sense did the game have "fewer" heroes during GOATS? And how would you have put a number on it before the audience got bored?

### The model

Let a roster have `n` classes. Let `p_i` be the share of picks that class `i` receives, so all the shares add to 1. The **effective number of classes** is

```
N_eff = 1 / (p_1² + p_2² + ... + p_n²)
```

- `n` is the number of classes on paper.
- `p_i` is class i's pick share, a number between 0 and 1.
- `Σ p_i²` is the chance that two picks drawn at random are the same class. Ecologists call this the Simpson concentration.
- `N_eff` is the number of equally popular classes that would give the same concentration.

Two facts make this easy to read.

1. If `k` classes are picked equally and the rest never, then `N_eff = k` exactly. Eight classes at 12.5% each give `N_eff = 8`. Four at 25% each give 4.
2. `N_eff` can never exceed `n`, and it can never exceed `1 / p_max²`, where `p_max` is the largest share. If your top class has 40% of picks, you have at most 6.25 effective classes, no matter how the rest split.

The squared shares are what make this work. Squaring shrinks small shares much more than large ones, so a class with 2% of picks contributes 0.0004 and barely counts, while a class with 60% contributes 0.36 and dominates. `N_eff` counts classes weighted by how much of the game they occupy.

A closely related number is the **Herfindahl-Hirschman Index** (HHI), used by competition regulators. It is the same sum with shares written as percentages: `HHI = Σ (100 × p_i)²`, which is `10,000 × Σ p_i²`. So `HHI = 10,000 / N_eff`.

### Numbers you can check

Take an eight-class MMO and three possible pick distributions for its rated battleground ladder. These are illustrative figures for a fictional game, chosen so you can check them by hand.

| Class | A: even | B: healthy lean | C: one dominant |
|---|---|---|---|
| 1 | 12.5% | 30% | 60% |
| 2 | 12.5% | 20% | 10% |
| 3 | 12.5% | 15% | 10% |
| 4 | 12.5% | 10% | 5% |
| 5 | 12.5% | 10% | 5% |
| 6 | 12.5% | 5% | 5% |
| 7 | 12.5% | 5% | 3% |
| 8 | 12.5% | 5% | 2% |

Work distribution B.

```
Σ p² = 0.30² + 0.20² + 0.15² + 0.10² + 0.10² + 3 × 0.05²
     = 0.09 + 0.04 + 0.0225 + 0.01 + 0.01 + 0.0075
     = 0.18
N_eff = 1 / 0.18 = 5.56
HHI = 10,000 × 0.18 = 1,800
```

Now distribution C.

```
Σ p² = 0.36 + 0.01 + 0.01 + 3 × 0.0025 + 0.0009 + 0.0004
     = 0.3888
N_eff = 1 / 0.3888 = 2.57
HHI = 3,888
```

| Distribution | Classes on paper | Σ p² | N_eff | HHI |
|---|---|---|---|---|
| A: even | 8 | 0.125 | 8.00 | 1,250 |
| B: healthy lean | 8 | 0.180 | 5.56 | 1,800 |
| C: one dominant | 8 | 0.389 | 2.57 | 3,888 |

In C, every class is still played by someone. Class 8 still has 2% of picks. A player browsing the ladder would see all eight. Yet the game behaves as if it had two and a half classes. That is the GOATS situation in a number. The roster stayed the same size and the effective roster collapsed.

Look at B again. It is uneven, and one class takes almost a third of picks. It still keeps more than five effective classes. Perfect evenness is neither expected nor needed. Some classes will always be more popular for reasons of fantasy and look. The model lets you set a floor instead of chasing equality.

### A visual you can move

Open the [effective classes interactive](../examples/w01-effective-classes.html). The left panel shows the roster as the player sees it, eight class cards, all present. The right panel shows the same roster redrawn with each card's area proportional to its pick share, beside a large `N_eff` readout. Drag the "concentration" slider from even toward dominant and watch the left panel do nothing while the right panel collapses. Then press the "B: healthy lean" preset and confirm the readout says 5.56. (Building B by hand with the share sliders is slow, because each slider rescales the other seven.)

Try one experiment in particular. Start at distribution A and move 30 percentage points to class 1, taken evenly from the other seven. By hand, class 1 has 42.5% and each other class has 57.5 / 7 = 8.21%, so `Σ p² = 0.1806 + 7 × 0.0067 = 0.2279` and `N_eff` falls from 8 to 4.39. The share sliders move in whole percents, so in the interactive drag class 1 to 42% (readout 4.46) and then 43% (readout 4.32). The exact 42.5% sits between them. The left panel is unchanged throughout. The per-class table in the interactive shows that almost all of the loss comes from class 1's growth. The seven other classes each lost only about 4 points.

### Cross-game recognition

The same formula shows up wherever people want to count "how many really" from shares.

**Overwatch, 2019.** Role Queue is a structural floor on diversity. With two slots per role, no role can take more than a third of a team's picks. The designers did not make the other heroes stronger. They changed the rules so the concentration could not happen at the role level. That is a design choice worth noticing, because it trades player freedom for guaranteed variety.

**League of Legends.** Riot's professional-play rule, 90% presence flags a champion as overpowered, is a concentration signal. It does not look at win rate at all. It says that when one option appears in almost every game, the game has lost diversity, whatever the win rates say.

**Competition policy.** The United States 2023 Merger Guidelines treat a market with HHI above 1,800 as highly concentrated. Rewritten as `N_eff`, that is `10,000 / 1,800 = 5.56` effective firms, which is exactly distribution B. Regulators and balance designers are asking the same question about different populations.

**Political science.** Laakso and Taagepera (1979) proposed the "effective number of parties" as `1 / Σ s_i²`, where `s_i` is each party's share of seats or votes. It is the same formula, used to tell a real multi-party system from a two-party system with some small parties at the edges.

**Ecology.** Hill (1973) showed that species richness, Shannon entropy and the Simpson index are members of one family of "effective number of species" measures. `N_eff` is the member Hill called order 2. It pays the most attention to common species and the least to rare ones, which is what you want when the question is "what will a typical player see in a typical match?"

When you see a pick-rate chart, a meta report or a market-share table, your first move should be to square the shares, add them, and invert.

### Eyes-open design judgment

`N_eff` is a good instrument and a bad goal. Use it knowing what it hides.

- **It ignores win rates.** A class can be popular because it is fun, easy or looks good. A low `N_eff` driven by an easy, weak class is a different problem from one driven by a strong class. Always read `N_eff` next to win rates.
- **It depends on the unit you count.** Counting classes, specs, roles or full team compositions gives different answers. A raid can have high class diversity and very low composition diversity if every group runs the same template. Pick the unit players experience.
- **It depends on the population.** Diversity at the top of a rated ladder is usually lower than across all players, because experts converge on the best option faster. Measure by bracket, as Riot does.
- **Structural fixes cost freedom.** Role Queue raised the floor on role diversity by removing some choices. A designer can also cap duplicates in a group, or give bonuses for mixed groups. Each one makes the game less free in order to make it less samey. Decide deliberately.
- **Uniformity is not the target.** A game where every class has 12.5% has probably homogenized its classes until they feel the same. Set a floor, such as "`N_eff` at least 6 of 8 in every bracket," and stop there.

### Check yourself (worked example)

Questions 1 to 3 in the Check yourself section at the end of this lecture use this model directly. Try them now, before section 3, while the formula is fresh. One extra to do in your head: what is `N_eff` for shares of 25%, 25%, 25%, 25% and four classes at 0%? (It is 4, by the first fact above.)

## 3. Viability in numbers: win rates and why they lie

Win rate is the default viability metric, and it is harder to read than it looks. Three traps catch almost everyone.

### Trap 1: mirror matches pull win rates toward 50%

When a class fights itself, one copy wins and one loses. Those games contribute exactly 50% to the class's win rate, whatever its strength. In team games, where the same class often appears on both sides, this is a large effect.

Let `w` be the class's true win rate in games where it does not face itself, and `m` the share of its games that are mirrors. The observed win rate is

```
observed = (1 − m) × w + m × 0.5
```

Suppose a class truly wins 58% of non-mirror games, and because it is popular, 40% of its games include a copy on the other team. Observed win rate is `0.6 × 0.58 + 0.4 × 0.5 = 0.548`, or 54.8%. The dashboard shows a borderline case. The class is in fact dominant. Solve for `w` before you judge: `w = (observed − 0.5m) / (1 − m)`.

The more popular a class becomes, the more mirrors it plays, and the more its win rate understates its strength. This is one reason concentration and win rate must be read together.

### Trap 2: who picks the class changes the win rate

Win rate measures the class and its players together. A popular, easy class draws in new and returning players, which drags its win rate down. A difficult class played mostly by specialists shows an inflated win rate, because only people who have mastered it stay with it.

The standard defence is to compare within a skill bracket, as Riot does with its four segments. A second defence is to look at win rate by games played on that class, which shows whether the class is weak or merely has many beginners.

### Trap 3: small samples

A class with 300 games at 53% is not measurably different from 50%. [MA102 week 13](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) covers confidence intervals. The short version for 300 games is that the 95% interval is about ±5.7 percentage points, so the number tells you almost nothing. Rare classes have the noisiest win rates, which is where you are most tempted to act.

### PvE viability is a threshold

For raids and dungeons, win rate does not exist. Use the content's requirements instead. If a boss has 12,000,000 health and a 6-minute enrage timer, the group needs `12,000,000 / 360 = 33,333` damage per second. With 14 damage dealers contributing most of that, a spec is viable if a normal player of it contributes a reasonable share of the requirement. [Week 3](w03-effective-hp-and-effective-dps.md) builds the tools to compute what a spec actually contributes (effective DPS), and [week 5](w05-the-holy-trinity-tank-healer-dps.md) turns this into role requirements.

The design judgment is that PvE viability depends on your tuning margin. If the enrage check needs every spec to perform at the top of the list, then a 5% gap between specs decides who gets invited. If the check has a 10% margin, the same 5% gap does not matter for clearing, though some players will still invite the top spec. You set the margin. That is a balance decision, not a tuning accident.

## 4. Writing a balance target

Put the three properties together and you can write a target a team can test.

A weak target reads "all classes should feel balanced." Nobody can check it.

A testable target names the property, the metric, the population and the threshold.

- **Fairness.** "In rated 3v3, no faction's win rate differs from 50% by more than 1.5 points at any rating bracket, over at least 10,000 games per bracket."
- **Viability.** "Every spec's mirror-corrected win rate is between 48% and 53% in each of our three rating brackets."
- **Viability (PvE).** "Every damage spec, played at the median of its population, reaches at least 90% of the enrage requirement for each current raid boss."
- **Diversity.** "`N_eff` of specs in the top 10% of the ladder stays at or above 60% of the number of specs."

Notice what these do. Each can be computed from telemetry. Each sets a band, not a single point, so the team is not chasing noise. And each target can fail independently of the others, which is the point of separating the three ideas.

Targets also create trade-offs you must decide in advance. Raising diversity by buffing an unpopular class may push it past the viability band. Fixing faction fairness by buffing one side's racial ability may concentrate picks on that race. Write down which target wins when two conflict.

## 5. What balance is not

Three ideas are often confused with balance. Clear them away before week 2.

**Balance is not symmetry.** Chess is symmetric and slightly unfair. *Hearthstone* is asymmetric by turn order and made fair by a priced compensation. Symmetric design is the easy route to fairness, and it costs you diversity, because identical options are not really different options. Sirlin puts games on a spectrum from symmetric to highly asymmetric and argues that the asymmetric end is harder to balance and more interesting when it works.

**Balance is not sameness.** If you balance classes by giving them the same tools with different names, `N_eff` may rise while the meaningful diversity falls. Players will still pick "the best-looking copy." Diversity you want is diversity of play, not of labels.

**Balance is not a finished state.** Players discover new strategies, patches change numbers, and the population changes. Balance is something you measure every week. That is why the targets in section 4 use ongoing telemetry, and why week 14 of this course is about communicating change.

## In-class activity (25 minutes)

Pairs. You are the balance team for a fictional MMO with six specs: Guardian, Warden, Mender, Chanter, Striker and Arcanist. The live dashboard for the top rating bracket last week showed the following.

| Spec | Pick share | Observed win rate | Mirror share of its games |
|---|---|---|---|
| Guardian | 35% | 52.0% | 30% |
| Warden | 10% | 50.5% | 5% |
| Mender | 25% | 51.0% | 20% |
| Chanter | 5% | 47.0% | 1% |
| Striker | 20% | 50.0% | 15% |
| Arcanist | 5% | 49.5% | 1% |

1. Compute `N_eff` for this bracket. (Expected: 4.17.)
2. Correct Guardian's win rate for mirrors. Is it inside a 48-53% viability band? (Expected: 52.9%, at the top edge.)
3. Decide which property is failing most. Write a two-sentence argument.
4. Propose one change and predict its effect on all three properties. Name one way your change could backfire.
5. Swap with another pair and critique their proposal using only the numbers.

Expected output: one index card per pair with `N_eff`, the corrected Guardian win rate, the diagnosis and the proposal.

## Common misconceptions

- **"Balanced means every class wins 50%."** Viability is a band, and a class at 51.5% is not a problem. Chasing exactly 50% chases noise.
- **"If every class is picked sometimes, diversity is fine."** Presence is not diversity. Distribution C has every class present and only 2.57 effective classes.
- **"A 52% win rate means the class is only slightly strong."** Popular classes play many mirror matches, which hide their strength. Correct for mirrors before judging.
- **"Symmetric design is balanced design."** Symmetry gives fairness at the cost of diversity, and it does not remove first-mover advantage. Chess is the proof.

## Check yourself

1. A four-class game has shares 40%, 30%, 20% and 10%. Compute `N_eff` and HHI.
2. Your top class has 50% of picks in an eight-class game. What is the largest possible `N_eff`? What would the other seven shares be?
3. A designer says "all twelve specs appear in the top 100, so diversity is fine." What number would you ask for, and why doesn't their evidence answer the question?
4. A class shows a 53% observed win rate, and 50% of its games are mirrors. What is its true non-mirror win rate? Does it pass Riot's Average Play threshold for "overpowered" at low ban rate?
5. A PvE boss needs 40,000 group DPS for 5 minutes. Your raid's specs, at median play, produce 42,000. A patch nerfs one spec that makes up a fifth of the group's damage by 8%. Does the group still clear? What does this say about tuning margin?

<details>
<summary>Answers</summary>

1. `Σ p² = 0.16 + 0.09 + 0.04 + 0.01 = 0.30`, so `N_eff = 3.33` and HHI = 3,000.
2. The 50% class contributes 0.25 to `Σ p²` whatever else happens, so `N_eff ≤ 4`. The true maximum comes when the other 50% is split evenly, `0.5 / 7 = 7.14%` each. Then `Σ p² = 0.25 + 7 × 0.0051 = 0.2857` and `N_eff = 3.5`. One class at 50% caps an eight-class game at 3.5 effective classes.
3. Ask for `N_eff` (or HHI) of specs in that bracket. "Appears in the top 100" is presence. Eleven specs at 1% each and one at 89% would pass their test with `N_eff` of about 1.26.
4. `w = (0.53 − 0.5 × 0.5) / (1 − 0.5) = 0.28 / 0.5 = 0.56`. The true win rate is 56%, above the 54.5% line, so it would be flagged. The observed 53% would not have been.
5. The nerfed spec provided `0.2 × 42,000 = 8,400` DPS and loses 8% of that, which is 672. The group now does 41,328, still above 40,000, so it clears. The 5% margin (2,000 DPS) absorbed an 8% nerf to one spec. A thinner margin would have turned the same nerf into a failed clear and a spec nobody invites.

</details>

## Lab hook

**Lab 01: Reading a balance dashboard** ([labs/lab01.md](../labs/lab01.md)). You receive a synthetic match log for an eight-spec game across three rating brackets. You compute `N_eff`, mirror-corrected win rates and first-mover win rates per bracket, diagnose which property is failing where, and write a one-page balance target document. The same targets come back in the final balance pass in week 15.

## Sources

- Sirlin, D. (pages dated August 2014). "Balancing Multiplayer Games, Part 1: Definitions" and "Part 2: Viable Options." sirlin.net. Definitions of fairness, viable options and balance, and the symmetric-to-asymmetric spectrum (paraphrased). The same material underlies his GDC 2009 talk "Balancing Multiplayer Competitive Games" (handout on sirlin.net).
- Wikipedia, "Super Street Fighter II Turbo HD Remix." Sirlin as lead designer (Backbone Entertainment for Capcom, 2008).
- Wikipedia, "First-move advantage in chess." White's score of 52-56% in most collections; *New In Chess* Yearbook 2000 database of 731,740 games with White at 54.8%.
- Wikipedia, "Komi (Go)." Standard komi of 6.5 under Japanese and Korean rules, 7.5 under Chinese, Ing and AGA rules.
- Hearthstone Wiki (hearthstone.wiki.gg), "The Coin," and Hearthstone Wiki (Fandom), "Mulligan." Player going second receives 4 starting cards and The Coin; player going first receives 3. Current rules, 2014 onward.
- HearthstoneJSON card data (latest build, checked 2026), card GAME_005 "The Coin": cost 0, gain 1 Mana Crystal this turn only. https://api.hearthstonejson.com/v1/latest/enUS/cards.json
- Wizards of the Coast, *Magic: The Gathering Comprehensive Rules* (April 4, 2025 edition), rule 103.8a. The first player in a two-player game skips the draw step of their first turn.
- Riot Games (May 30, 2019). "/dev: Champion Balance Framework." leagueoflegends.com. Segments, win-rate and ban-rate thresholds, professional presence thresholds.
- Shacknews (2019), "Overwatch Role Queue kills GOATS forever with 2-2-2 lineups," and PCGamesN (2019) on Role Queue. GOATS as three tanks and three supports; Role Queue in Overwatch League 2019 Stage 4 and on the live game at the start of competitive Season 18, September 2019.
- Overwatch Wiki, "Competitive Play" (Season 18, September 3 to November 7, 2019, the first with Role Queue) and Wikipedia, "2019 Overwatch League season" (2-2-2 enforced from Stage 4). https://overwatch.fandom.com/wiki/Competitive_Play
- U.S. Department of Justice and Federal Trade Commission (December 2023). *Merger Guidelines*. HHI above 1,800 is highly concentrated.
- Laakso, M. & Taagepera, R. (1979). "'Effective' Number of Parties: A Measure with Application to West Europe." *Comparative Political Studies* 12(1), 3-27.
- Hill, M. O. (1973). "Diversity and Evenness: A Unifying Notation and Its Consequences." *Ecology* 54(2), 427-432.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w01-effective-classes.html

**The one insight.** The roster the player sees stays the same size while the effective roster collapses. The left view must look unchanged as the right view shrinks.

**Layout.** Two linked panels side by side on desktop, stacked on mobile (left panel on top).

- Left panel, "Roster (what players see)": eight generic class cards in a 4×2 grid, labelled Class 1 to Class 8, each with its pick share as text. Cards never change size. A class with share below 1% gets a faint "rarely seen" tag, nothing more.
- Right panel, "Effective roster": a treemap or single row of rectangles whose areas are proportional to `p_i`, plus a large readout `N_eff = X.XX of 8` and a smaller line `HHI = X,XXX`. Draw a row of eight outline "slots" under the readout and fill `floor(N_eff)` of them solid plus a partial fill for the fraction, so 5.56 shows five full slots and one 56% slot.

**Controls.**
- Preset buttons: "A: even", "B: healthy lean", "C: one dominant", "GOATS-like" (see test values).
- Concentration slider `c` from 0 to 1 (step 0.01). Interpolates linearly between the even distribution and distribution C: `p_i = (1 − c) × 0.125 + c × C_i`.
- Eight vertical share sliders (one per class), 0 to 100 in steps of 1. When one is moved, rescale the other seven proportionally so shares always sum to 100%. If all others are zero, split the remainder evenly.
- Toggle "Show HHI threshold": draws a marker on an `N_eff` bar at 5.56 labelled "HHI 1,800 (U.S. 2023 'highly concentrated' line)".
- All controls keyboard reachable; sliders respond to arrow keys.

**Formulas.**
- `S = Σ p_i²` with `p_i` as fractions.
- `N_eff = 1 / S`, shown to two decimals.
- `HHI = round(10000 × S)`.
- Upper bound readout: `max N_eff given top share = 1 / (p_max² + (1 − p_max)² / 7)`, shown as "Most you could have with this top class: X.XX".

**Test values (must match exactly).**

| Preset | Shares (%) | Σ p² | N_eff | HHI |
|---|---|---|---|---|
| A: even | 12.5 ×8 | 0.1250 | 8.00 | 1,250 |
| B: healthy lean | 30, 20, 15, 10, 10, 5, 5, 5 | 0.1800 | 5.56 | 1,800 |
| C: one dominant | 60, 10, 10, 5, 5, 5, 3, 2 | 0.3888 | 2.57 | 3,888 |
| GOATS-like | 16, 16, 16, 16, 16, 16, 2, 2 | 0.1544 | 6.48 | 1,544 |
| Slider c = 0.5 | 36.25, 11.25, 11.25, 8.75, 8.75, 8.75, 7.75, 7.25 | 0.1910 | 5.24 | 1,910 |

Upper-bound readout for B (`p_max = 0.30`): `1 / (0.09 + 0.49/7) = 1 / 0.16 = 6.25`.

Note the GOATS-like preset is a teaching trap. Six heroes share picks evenly, so `N_eff` looks high for heroes. Add a second readout for this preset only, "by role": treat classes 1-3 as Tank and 4-6 as Support and 7-8 as Damage, giving role shares 48%, 48%, 4% and role `N_eff = 1 / (0.2304 + 0.2304 + 0.0016) = 2.16 of 3`. The point is that the unit you count changes the answer.

**Visual rules.** Use `templates/interactive-tokens.css` inline. Generic coloured shapes only, no hero or class art. Numbers are selectable text. Respect reduced motion (no animated transitions when set).
