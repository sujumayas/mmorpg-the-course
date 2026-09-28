# MMO305 · Week 09 — Toxicity: Research and Interventions

**Why this matters:** Toxic behaviour drives players out of team games, and it is the first thing new players meet in many of them. Teams that treat toxicity as a few bad apples to ban often spend years punishing and see little change. The research points somewhere less comfortable. Most toxic moments come from ordinary players on a bad day, and fixing that takes design as well as moderation.

**You will be able to:**
- Compute the share of toxic incidents that come from occasional versus persistent offenders, and the share of matches a player will find toxic, from a two-group model.
- Compare punishment (catching the persistent few) with situational design (lowering everyone's rate) and predict the ceiling on each.
- Compute how many innocent players a detection system punishes for each guilty one, from its recall and false-positive rate.
- Critique a real intervention (crowd review, chat defaults, segregated queues, rewards for good conduct) by the part of the model it changes.

**Before class:** Kou, Y. (2020), "Toxic Behaviors in Team-Based Competitive Gaming: The Case of League of Legends", *Proceedings of CHI PLAY 2020*, pp. 81-92, read in full. Kwak, H., Blackburn, J. & Han, S. (2015), "Exploring Cyberbullying and Other Toxic Behavior in Team Competition Online Games", *Proceedings of CHI 2015*, pp. 3739-3748, sections 1-3.

**Prerequisites from earlier courses:** [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one event across many trials). [MA102 week 14, hypothesis testing and A/B](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (how you would know an intervention worked). [UX201 week 3, flow and difficulty](../../UX201-game-ux-and-player-psychology/lectures/w03-flow-and-difficulty.md) (frustration when challenge outruns skill). [MMO305 week 8, griefing](w08-griefing-typology-and-design-responses.md) (the reservoir idea, which returns here as the persistent few). [MMO305 week 6, trust and reputation systems](w06-trust-and-reputation-systems.md). Moderation as governance is picked up again in MMO402 weeks [6](../../MMO402-emergent-society-governance-and-ethics/lectures/w06-moderation-at-scale.md) and [7](../../MMO402-emergent-society-governance-and-ethics/lectures/w07-justice-systems-reports-reviews-appeals.md).

**Interactive:** [examples/w09-toxicity-levers.html](../examples/w09-toxicity-levers.html) (spec at the end of this lecture). Keep it open during section 2.

---

## 1. What researchers mean by toxicity

### No single definition

"Toxic" is a word players use for everything from slurs to a teammate who picks an unusual character. Researchers have struggled with that looseness. Yubo Kou's 2020 study of League of Legends starts from the observation that there is little agreement on what counts, and that developers' own categories often lag behind what players actually experience. Kou treats toxic behaviour as situated action. The same act can be toxic or not depending on the match, the stakes and the people involved.

From players' accounts, Kou identified five primary types of toxic behaviour in League and five contextual factors that lead to it (both counts are in the paper's abstract). The type names below follow how later papers citing Kou summarise them; check them against the paper when you read it.

| Type | What it looks like |
|---|---|
| Communicative aggression | Flaming, insults, blaming and harassment in chat or pings |
| Cheating | Using hacks or exploits to gain an unfair edge |
| Hostage holding | Keeping teammates in a bad situation, for example refusing to surrender a lost match so everyone must play it out |
| Mediocritizing | Deliberately not trying hard to win |
| Sabotaging | Consciously lowering the team's chances, such as feeding the enemy on purpose |

Only the first is about words. The other four are about play. That matters for design. A chat filter touches one row of this table.

Kou also found contextual factors that push players toward toxic acts. As later papers summarise them, competitiveness, conflict inside the team and the sense that the match is already lost stand out. Some players who flame in frustration do not see their own behaviour as toxic. Toxicity, on this view, is often a reaction to a situation the game created.

### Toxicity and griefing

Last week's griefing overlaps with this week's topic but is not identical. A griefer usually sets out to spoil someone's experience and enjoys it. Much toxic behaviour in team games is not planned. A player who types an insult after a lost fight did not log in to hurt anyone. The distinction matters because the payoff analysis from week 8 assumed a deliberate actor weighing benefit against cost. Many toxic acts are not decisions of that kind at all, which is why punishment alone reaches only part of the problem.

### What the large datasets show

League of Legends has been studied more than any other game because Riot Games made unusual data available. For several years the game ran the Tribunal, a system in which experienced players reviewed reported cases and voted on whether to punish. Blackburn and Kwak (2014) and Kwak, Blackburn and Han (2015) analysed over 10 million player reports about 1.46 million reported players, together with the crowd's verdicts. They trained classifiers that could predict the crowd's decision for the clear-cut cases, which points toward automating the review step.

Riot's own researchers reported a finding that shaped the company's later approach. According to Jeffrey Lin, then the lead designer of social systems, most bad behaviour in League came from players who were usually fine and occasionally acted out, not from a small core of consistently toxic players. Lin later argued that eliminating toxicity was an unrealistic goal and that rewarding good behaviour mattered more. Riot's 2017 rework of its Honor system followed that line. Players give teammates recognition after matches, and a higher honor level earns rewards over time.

The worked example turns that finding into numbers.

## 2. Worked example: the few, the many and the match

### The hook

Suppose a team game has a small group of truly toxic players, 2% of the population, who behave badly in half their matches. Everyone else behaves badly only occasionally. The team's first plan is to find the 2% and ban them.

Yet a new player's experience is that a third of their matches contain something nasty. How can a 2% problem show up in a third of matches? And if you ban every one of the 2%, how much better does it get?

### The model

Split players into two groups.

```
q = (1 − p) × r_o + p × r_h

share from occasional offenders = (1 − p) × r_o / q
share from persistent offenders = p × r_h / q

P(match has at least one incident) = 1 − (1 − q)^n
```

- `p` is the share of players who are **persistent** offenders.
- `r_h` is the chance that a persistent offender commits at least one toxic act in a given match.
- `r_o` is the same chance for an **occasional** offender, meaning everybody else.
- `q` is the average chance per player per match. It is also the expected number of toxic players per match divided by the number of players, when each player commits at most one incident per match.
- `n` is the number of players in a match. For a 5v5 game, `n = 10`.
- The last line is the complement rule from MA102 week 3. A match is clean only if all `n` players stay clean, which happens with probability `(1 − q)^n`, assuming players are drawn independently.

Two families of intervention act on different parts of the model:

```
Punishment (catch the persistent few with recall k):
    q_after = (1 − p) × r_o + p × r_h × (1 − k)

Situational design (lower everyone's rate by a fraction x):
    q_after = (1 − x) × [(1 − p) × r_o + p × r_h]

Both:
    q_after = (1 − x) × [(1 − p) × r_o + p × r_h × (1 − k)]
```

- `k` is the **recall** of your detection and punishment system: the share of persistent offenders you catch and remove from play.
- `x` is the fractional drop in everyone's rate from a design change: chat defaults, clearer surrender rules, better matchmaking, rewards for good conduct.

Punishment also has a cost that the second family does not. Any real detection system flags some innocent players. If `fpr` is the **false-positive rate** (the share of occasional players wrongly punished) and the population is `M`:

```
correctly punished = k × p × M
wrongly punished   = fpr × (1 − p) × M
precision of punishment = correct / (correct + wrong)
```

### Numbers you can check

Take `p = 2%`, `r_h = 0.5`, `r_o = 0.03`, `n = 10`, and a population of `M = 10,000`. These are teaching numbers chosen to match the shape of the published finding, not Riot data.

**Where the incidents come from.**

```
q = 0.98 × 0.03 + 0.02 × 0.5 = 0.0294 + 0.0100 = 0.0394
occasional share = 0.0294 / 0.0394 = 74.6%
persistent share = 0.0100 / 0.0394 = 25.4%
P(toxic match) = 1 − (1 − 0.0394)^10 = 1 − 0.669 = 33.1%
```

Each persistent player is about 17 times as likely to be toxic in a match as an ordinary player (`0.5 / 0.03`), and together they are still only a quarter of the problem. Three quarters come from the 98% who are usually fine. And because ten players share each match, a per-player rate under 4% turns into toxicity in one match out of three.

**What each intervention buys.**

| Intervention | `q` after | Incidents removed | Toxic matches |
|---|---|---|---|
| None | 0.0394 | 0% | 33.1% |
| Catch 70% of persistent (`k = 0.7`) | 0.0324 | 17.8% | 28.1% |
| Catch all persistent (`k = 1`) | 0.0294 | 25.4% | 25.8% |
| Lower everyone's rate 20% (`x = 0.2`) | 0.0315 | 20.0% | 27.4% |
| Lower everyone's rate 30% (`x = 0.3`) | 0.0276 | 30.0% | 24.4% |
| Both (`k = 0.7`, `x = 0.2`) | 0.0259 | 34.2% | 23.1% |

Check the "both" row: `0.8 × (0.0294 + 0.02 × 0.5 × 0.3) = 0.8 × 0.0324 = 0.02592`, and `1 − 0.02592 / 0.0394 = 34.2%`.

Three things stand out.

- **Punishment has a ceiling.** Even perfect detection, catching every persistent offender, removes only the persistent share, 25.4%. One match in four is still toxic.
- **A modest design change beats good punishment.** Lowering everyone's rate by 20% removes more incidents than catching 70% of the worst players.
- **The two stack.** Because they act on different parts of `q`, combining them removes more than either alone.

**What punishment costs.** Suppose your system catches 70% of persistent offenders and wrongly flags 0.5% of occasional players. In a population of 10,000:

```
correctly punished = 0.7 × 0.02 × 10,000 = 140
wrongly punished   = 0.005 × 0.98 × 10,000 = 49
precision = 140 / 189 = 74%
```

A false-positive rate of half a percent sounds tiny. Yet one punished player in four did not deserve it, because the innocent group is 49 times larger than the guilty one. This is the same base-rate effect you met in week 7, turned around. There you asked what a badge says about its owner, here you ask what a ban says about its target.

### A visual you can move

Open `examples/w09-toxicity-levers.html`. The left view is a stacked bar of incidents per 1,000 player-matches, split into occasional and persistent. The right view shows the share of toxic matches as you change `k` and `x`, with a dotted line marking the punishment ceiling (the best you can do with `x = 0`). A small panel below shows the ban ledger: correct bans, wrong bans and precision. Drag `k` to 100% and watch the toxic-match line stop at the ceiling. Then drag `x` and watch it pass through. Raise `p` to 10% and see when punishment starts to win.

### Cross-game recognition

The model sorts every anti-toxicity measure into two families. Either you remove or isolate the persistent few, or you change the situation for the many. Real games use both.

**League of Legends: from the Tribunal to Honor (Riot Games, 2010s).** The Tribunal was a punishment system. Reports went to player reviewers, and enough guilty votes triggered penalties. The research on its data (Blackburn and Kwak 2014) showed that a classifier could reproduce the crowd's verdict on clear cases, which raises `k` cheaply but leaves the false-positive question open. Riot's later emphasis on the occasional offender, and the 2017 Honor rework that rewards good conduct, act on `x`. Riot moved from the persistent family toward the situational family as its own data showed where most incidents came from.

**Dota 2, the low-priority queue (Valve, current).** Players who abandon games repeatedly, get reported many times, or trip Valve's griefing detection are placed in low priority. There they wait longer, can only queue for one unranked mode, play only with other low-priority players, and must win a set number of games to get out. This acts on the persistent group without banning them. It is segregation from week 8: it lowers contact between persistent offenders and everyone else. In the model it works like raising `k` for the purpose of other players' matches, since low-priority players no longer appear in normal matches. And because leaving requires winning games with other low-priority players, it rewards changed behaviour instead of just waiting out a timer.

**Grand Theft Auto Online, "bad sport" lobbies (Rockstar Games, current).** Players flagged for disruptive behaviour are marked as bad sports and placed in lobbies with other bad sports. Same family, same mechanism. Isolate the persistent group so its incidents land on each other.

Three games, one split. Every intervention either targets the few or changes the situation for the many, and the model tells you how much each family can deliver in a given population.

### Eyes-open design judgment

- **Measure the split before you choose.** If `p × r_h` is most of `q`, punishment will work. If `(1 − p) × r_o` is most of `q`, as Riot reported for League, punishment has a hard ceiling and design must carry the rest. You get the split from your own data. Count incidents per player and see how concentrated they are.
- **Punishment still matters.** Removing persistent offenders removes a quarter of incidents in the example, and those offenders make some matches unbearable. The model argues against punishment alone, not against punishment.
- **Every false positive is a player you taught that reporting is a weapon.** At 74% precision, one ban in four hits an innocent player. Wrongly punished players leave, or they learn to distrust the system. Publish how appeals work and keep punishment for cases with strong evidence.
- **Situational fixes aim at the triggers Kou found.** Competitiveness, team conflict and the sense of a lost match are all things you can design. Surrender votes shorten hostage holding. Fewer blame-friendly stats on the end screen reduce blaming. Matchmaking that avoids hopeless stomps lowers the "already lost" feeling that UX201 week 3 would call frustration past the flow channel.
- **Check with an experiment, not a feeling.** Changes to `x` are small per player and hard to see by eye. Test them as A/B experiments (MA102 week 14) on report rates and toxic-match share, and watch for players simply reporting less.

## 3. Intervention families in more detail

### Punish and remove

Reports, review (by staff, crowds or classifiers) and penalties from chat restrictions to permanent bans. Strengths: clear message, removes the worst offenders, and satisfies victims. Weaknesses: capped by the persistent share, costly per case, and exposed to false positives and to report abuse, where groups mass-report a player they dislike. Speed matters too. A penalty that arrives weeks after the match is hard for the player to connect with what they did.

### Isolate

Segregated queues, separate lobbies, and matchmaking that avoids pairing a reported player with the player who reported them. Strength: protects everyone else without a ban. Weakness: the isolated pool can become a trap for players placed there by mistake, and a small pool means long waits.

### Reshape the situation

Chat defaults, surrender rules, role selection before a match so no one fights over roles, pings that give fast non-verbal communication, and matchmaking quality. These lower `r_o` for everyone. Strength: acts on the largest slice. Weakness: each change is small, costs something (a chat default that hides the enemy team's messages also hides friendly banter), and needs an experiment to measure. Week 10 on communication design takes this family further.

### Reward good conduct

Honor, endorsements and commendations, with small rewards attached. The theory is that visible recognition raises the value of good behaviour and gives players a social signal for it. Week 7 applies here. A commendation is a status signal, and its precision depends on who can earn it. If friends can freely commend each other, it signals friendship, not conduct. Reward systems also have a risk that punishment does not. Players who are rewarded for not being toxic may feel paid for something they would have done anyway, which some motivation research warns can weaken the behaviour (UX201 week 4).

### Nudge in the moment

Warnings shown when a player types a flagged phrase, a cooling-off message after a lost fight, or a reminder of the rules at the start of a match. These act on `r_o` at the moment of choice. They are cheap to try, and their effects are easy to overstate, so test them.

## In-class activity (25 minutes)

Your team runs a 5v5 game with 50,000 players. Last month's data for a random sample of 5,000 of them is in [Lab 09's starter file](../labs/lab09-starter/incidents.csv): matches played and matches with at least one incident, per player.

1. From the incident counts, estimate `p`, `r_h` and `r_o`. Decide where to draw the line between persistent and occasional, and justify it in one sentence.
2. Compute `q`, the occasional share and the toxic-match share.
3. Detection currently catches 40% of persistent offenders. You have a budget for one of two projects. Project A raises recall to 80%. Project B keeps recall at 40% and adds situational changes expected to lower everyone's rate by 15%. Compute the toxic-match share after each, and the number of players wrongly punished per month at a false-positive rate of 0.3%.
4. Write a two-sentence recommendation to your producer, with the numbers.

Expected output: the parameter estimates with the cut line, a two-row comparison table, and the recommendation.

## Common misconceptions

- **"Toxicity is caused by a small group of toxic people."** Some of it is. In the example, the 2% who are persistently toxic cause 25% of incidents. The other 75% come from ordinary players, which matches what Riot reported for League.
- **"If only 4% of player-matches are toxic, most players rarely see it."** With ten players per match, a 3.9% per-player rate means one match in three contains toxicity. Exposure grows with the number of people you share a match with.
- **"A 0.5% false-positive rate is negligible."** It is applied to the large innocent group. In the example it produces one wrong ban for every three correct ones.
- **"Chat filters solve toxicity."** Four of Kou's five types (cheating, hostage holding, mediocritizing, sabotaging) happen through play, not words.

## Check yourself

1. A game has `p = 5%`, `r_h = 0.4`, `r_o = 0.02`, and `n = 6` players per match. Compute `q`, the persistent share of incidents and the chance a match is toxic.
2. In the lecture's example (`p = 2%`, `r_h = 0.5`, `r_o = 0.03`), what everyone-rate reduction `x` removes the same share of incidents as perfect punishment (`k = 1`)?
3. A detection system has recall 90% and a false-positive rate of 1%. With `p = 2%` and 10,000 players, what is its precision? What false-positive rate would it need for 90% precision?
4. A designer proposes to remove all text chat. Which of Kou's five types does this affect, and which part of the model? Name one cost.

<details>
<summary>Answers</summary>

1. `q = 0.95 × 0.02 + 0.05 × 0.4 = 0.019 + 0.020 = 0.039`. Persistent share `= 0.020 / 0.039 = 51.3%`. `P(toxic match) = 1 − 0.961^6 ≈ 1 − 0.788 = 21.2%`. Here punishment could remove at most about half of incidents, so it matters more than in the lecture's example.
2. Perfect punishment removes 25.4% of incidents. A uniform reduction removes exactly `x` of incidents, so `x = 25.4%`.
3. Correct `= 0.9 × 200 = 180`. Wrong `= 0.01 × 9,800 = 98`. Precision `= 180 / 278 = 64.7%`. For 90% precision, wrong bans must be at most `180 / 9 = 20`, so the false-positive rate must be at most `20 / 9,800 ≈ 0.2%`.
4. It affects communicative aggression only, and only its text form (pings and voice may remain). It lowers `r_o` and `r_h` for that type, a situational change. Costs: players lose coordination and friendly talk, and aggression may move into pings or into play (sabotaging), which the change does not touch.

</details>

## Lab / assignment hook

[Lab 09, toxicity intervention memo](../labs/lab09.md). You receive a synthetic month of match data with per-player incident counts, fit the two-group model, compare three intervention packages under a budget, and write a 400-word memo to a producer. The field observation assignment asks you to log toxic incidents you observe in real matches using Kou's five types; the lab gives you the model to interpret them.

## Sources

- Kou, Y. (2020). "Toxic Behaviors in Team-Based Competitive Gaming: The Case of League of Legends." *Proceedings of the Annual Symposium on Computer-Human Interaction in Play (CHI PLAY '20)*, pp. 81-92. doi:10.1145/3410404.3414243. Toxic behaviour as situated action; five types (communicative aggression, cheating, hostage holding, mediocritizing, sabotaging) and contextual factors including competitiveness, intra-team conflict and perceived defeat, as summarised in later papers citing it.
- Kwak, H., Blackburn, J. & Han, S. (2015). "Exploring Cyberbullying and Other Toxic Behavior in Team Competition Online Games." *Proceedings of CHI 2015*, pp. 3739-3748. doi:10.1145/2702123.2702529. Over 10 million reports on 1.46 million toxic players with crowdsourced decisions.
- Blackburn, J. & Kwak, H. (2014). "STFU NOOB!: Predicting Crowdsourced Decisions on Toxic Behavior in Online Games." *Proceedings of WWW 2014*, pp. 877-888. doi:10.1145/2566486.2567987. The Tribunal as a two-stage crowdsourced system and a classifier predicting its decisions.
- Wikipedia, "League of Legends" (accessed September 2026), section on player behaviour, citing Webster (The Verge, 6 March 2015) for Jeffrey Lin's statement that most problem behaviour came from players occasionally acting out; Alexander (2018) for Lin's view that eliminating toxicity was unrealistic; and Lee (13 June 2017) for the Honor rework.
- Lin, J. (2013). "The Science Behind Shaping Player Behavior in Online Games." Game Developers Conference 2013 (GDC Vault session description). The Tribunal and Honor as Riot's early behaviour systems.
- Liquipedia Dota 2 Wiki, "Priority" (accessed September 2026). Low priority triggers (repeated abandons, repeated reports, griefing detection), restrictions (one unranked mode, only other low-priority players, longer queues) and exit by winning a set number of games.
- Wikipedia, "Griefer" (accessed September 2026). Grand Theft Auto Online's "bad sport" designation and lobbies.

## Interactive spec: examples/w09-toxicity-levers.html

**Purpose.** Show that when most toxic incidents come from occasional offenders, punishment has a hard ceiling, and population-wide design changes are needed to pass it. Show the false-positive cost of punishment alongside.

**The one insight.** Catching every persistent offender removes only their share of incidents. Drag recall to 100% and the toxic-match line stops at a ceiling; only the everyone-rate lever moves past it.

**Model (exact).**

```
q0      = (1-p)*r_o + p*r_h
q       = (1-x) * ((1-p)*r_o + p*r_h*(1-k))
occ     = (1-x)*(1-p)*r_o          // occasional incidents per player-match
per     = (1-x)*p*r_h*(1-k)        // persistent incidents per player-match
removed = 1 - q/q0
toxicMatch   = 1 - (1-q)^n
ceilingMatch = 1 - (1-(1-p)*r_o)^n     // best possible with x = 0
correct = k*p*M
wrong   = fpr*(1-p)*M
precision = correct / (correct + wrong)   // show "n/a" if both are 0
```

**Layout.**
- Left chart: stacked bar "incidents per 1,000 player-matches". Two bars side by side, "before" (`1000*(1-p)*r_o` and `1000*p*r_h`) and "after" (`1000*occ` and `1000*per`). Occasional and persistent in two distinct colours plus hatching on persistent.
- Right chart: toxic-match share on the y-axis (0 to 100%) against recall `k` on the x-axis (0 to 100%), one line for the current `x`, one faint line for `x = 0`. Horizontal dotted line at `ceilingMatch` labelled "punishment ceiling". A dot at the current `k`.
- Ban ledger panel under the charts: correct bans, wrong bans, precision, and "one wrong ban per N correct" where `N = correct/wrong` rounded to one decimal.

**Controls.**
- Slider `p`, 0.5% to 20%, step 0.5%. Default 2%.
- Slider `r_h`, 0.1 to 1.0, step 0.05. Default 0.5.
- Slider `r_o`, 0.005 to 0.10, step 0.005. Default 0.03.
- Slider `n`, 2 to 20. Default 10.
- Slider `k` (recall), 0 to 100%, step 5%. Default 70%.
- Slider `x` (everyone-rate reduction), 0 to 50%, step 1%. Default 0%.
- Slider `fpr`, 0 to 3%, step 0.1%. Default 0.5%.
- Number input `M`, default 10,000.
- Preset buttons: "Ban the few" (k 100%, x 0%), "Nudge the many" (k 0%, x 20%), "Both" (k 70%, x 20%), "Few really are the problem" (p 10%, r_h 0.6, r_o 0.01).

**Test values (M = 10,000, n = 10, p = 2%, r_h = 0.5, r_o = 0.03, fpr = 0.5%).**

| k | x | q | removed | toxicMatch | correct | wrong | precision |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0.0394 | 0% | 33.1% | 0 | 49 | 0% |
| 0.7 | 0 | 0.0324 | 17.8% | 28.1% | 140 | 49 | 74.1% |
| 1.0 | 0 | 0.0294 | 25.4% | 25.8% | 200 | 49 | 80.3% |
| 0 | 0.2 | 0.03152 | 20.0% | 27.4% | 0 | 49 | 0% |
| 0.7 | 0.2 | 0.02592 | 34.2% | 23.1% | 140 | 49 | 74.1% |

`ceilingMatch` at defaults = `1 − 0.9706^10` = 25.8%.

**First screen.** Load with k = 100% and x = 0% so the line sits on the ceiling and the "after" bar is still three quarters full.

**Accessibility.** Keyboard-operable sliders with `aria-valuetext`; colour plus hatching for the two groups; reduced-motion respected. No game art, logos or chat screenshots.
