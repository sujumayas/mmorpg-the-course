# MMO407 · Week 05 — Case: Star Wars Galaxies and the NGE

**Why this matters:** Sooner or later every live team proposes to fix a struggling game by changing what it is. The change is a launch aimed at new players, run on top of a world full of existing ones. Star Wars Galaxies tried it twice in 2005, and the second attempt, the New Game Enhancements, became the industry's standard warning. This week you learn to price a redesign before you ship it, in players lost now against players gained later, and to see why the answer depends most on the two numbers a team knows least.

**You will be able to:**
- Compute the immediate loss from a redesign from a segment table of player shares and departure rates.
- Compute the month at which a redesigned game passes the path it left, and show how that month depends on new-player retention and on the assumed decline without the change.
- Compute the combined loss of two redesigns in a row, and the second-round loss when departing players are social hubs.
- Critique a redesign plan by naming its segment losses, its counterfactual and its reversibility, and propose a lower-risk alternative.

**Before class:** Read Seth Schiesel, "For Online Star Wars Game, It's Revenge of the Fans" (*The New York Times*, 10 December 2005), about 10 minutes. Read Raph Koster's short essays on Star Wars Galaxies on raphkoster.com (search "SWG"; pick two, 20 minutes). Koster led the game's design before and just after launch, not during the 2005 changes, so read him as a primary source with a point of view.

**Prerequisites from earlier courses:** [MMO301 week 7, themepark versus sandbox](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w07-themepark-vs-sandbox.md) (why Galaxies' sandbox players valued what the NGE removed; the novelty model is not repeated). [MMO301 week 13, worlds that died](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w13-worlds-that-died-shutdowns-and-their-lessons.md) (Galaxies' history through its 2011 closure, and SWGEmu). [MMO402 week 1, worlds as polities](../../MMO402-emergent-society-governance-and-ethics/lectures/w01-worlds-as-polities.md) (the exit-or-voice model for a single player; this week adds up the players). [MMO305 week 2, playing alone together](../../MMO305-social-systems-and-online-behaviour/lectures/w02-playing-alone-together.md) (entertainers, cantinas and the inspiration buff). [MMO308 week 4, funnels and churn](../../MMO308-live-operations-analytics-and-experimentation/lectures/w04-funnels-and-churn.md) (net against gross subscriber change). [Week 4 of this course](w04-case-ffxiv-1-0-to-a-realm-reborn.md) (a rebuild that came with a relaunch).

**Interactive:** [examples/w05-redesign-break-even.html](../examples/w05-redesign-break-even.html). Keep it open during section 2.

---

## 1. What changed in 2005

Star Wars Galaxies launched in North America on 26 June 2003 as a sandbox. It had 34 professions at launch (6 basic and 24 advanced, with more added later), a player-driven crafting economy, player cities, and roles such as Entertainer that paid off by serving other players. MMO301 week 7 explains what that design gave its players. MMO305 week 2 describes the cantinas, where entertainers performed and their audiences earned a buff that helped them in combat.

Then, in one year, the game changed twice.

| Date | Event |
|---|---|
| Spring 2005 | The Combat Upgrade changes combat. Media criticize it, and subscription cancellations rise |
| 5 May 2005 | Expansion *Rage of the Wookiees* released |
| 19 August 2005 | Expansion *Trials of Obi-Wan* announced |
| 1 November 2005 | *Trials of Obi-Wan* released |
| Early November 2005 | The New Game Enhancements (NGE) announced, two days after the expansion's release, and put live about a week after it |
| November 2005 | After one to two weeks of protests, Sony Online Entertainment (SOE) offers refunds for the expansion to anyone who asks |
| July 2012 | SOE president John Smedley, in a Reddit interview, admits "stupid decisions" over the Combat Upgrade and the NGE |

The NGE replaced the profession system with nine fixed roles: Jedi, Bounty Hunter, Smuggler, Commando, Spy, Officer, Medic, Entertainer and Trader. Jedi, which players had spent months unlocking, became a choice at character creation. Ground combat became real-time, with a targeting reticule and mouse-click firing, closer to a shooter. Reviewers criticized the loss of depth and complexity.

Smedley defended the change at the time as necessary to reverse a decline his team could see in the subscriber base. Hold on to that claim. It is the most important number in this week's model, and nobody outside SOE could check it.

The servers closed on 15 December 2011. MMO301 week 13 warns you against drawing a straight line from the NGE to the closure, and this week keeps that warning. Our question is narrower and more useful to a designer. Before shipping a redesign, how would you know whether it pays?

## 2. Worked example: how many new players does a redesign need?

### The hook

A redesign like the NGE is two launches at once. For new players, it is a new game, simpler to learn and closer to the action game they expected from a Star Wars licence. For existing players, it is the removal of the game they chose. The loss arrives on day one and is concentrated in players you already know. The gain arrives slowly, one trial account at a time, from players you have never met.

SOE had just sold those existing players an expansion. The announcement two days later turned their purchase into a grievance, and the refund lowered the cost of leaving at the moment they were angriest (MMO402 week 1 frames this as lowering the switching cost). What would the numbers have had to look like for this to pay?

### The model

Split the current players into segments by what they value. Name the numbers.

- `S₀` is the number of subscribers the day before the change.
- `wᵢ` is the share of players in segment `i`, and `dᵢ` is the share of that segment who leave because of the change. The **departure share** of the whole game is `D = Σ wᵢ × dᵢ`.
- `L = S₀ × D` is the **immediate loss**, in players.
- `g_old` is the net number of players the game would lose per month if you changed nothing. This is the **counterfactual**, the path you are comparing against.
- `a` is the number of new and returning trial players per month that the redesign brings in, and `r` is the share of them who stay.
- `g_new` is the monthly churn among the players who stayed through the change.

Treat each path as a straight line over the next year or two:

```
no change:  S_old(t) = S₀ − g_old × t
redesign:   S_new(t) = S₀ − L + (a × r − g_new) × t
```

The redesign starts `L` players behind and closes the gap at `(a × r − g_new) + g_old` players per month. The **break-even month** is when the two lines cross:

```
t* = L / (a × r − g_new + g_old)          (never, if the denominator is 0 or less)
```

Two things in the denominator are guesses. You cannot measure `r` for players who have not arrived yet. And `g_old` is a claim about a future you are choosing not to have. The numerator, `L`, is the part you can research, because the players it describes are already in your game.

### Numbers you can check

Take an invented game in the spirit of Galaxies in late 2005, with `S₀ = 200,000` subscribers. The segment table comes from a player survey and from what each segment would lose.

| Segment | Share `wᵢ` | Leaves `dᵢ` | Players lost | Why they leave |
|---|---|---|---|---|
| Crafters and traders | 0.25 | 0.45 | 22,500 | crafting depth cut, markets change |
| Entertainers | 0.10 | 0.60 | 12,000 | their role no longer feeds combat players |
| Combat players | 0.45 | 0.15 | 13,500 | combat rules replaced |
| Jedi grinders | 0.20 | 0.25 | 10,000 | months of unlocking made worthless |
| **Total** | 1.00 | `D = 0.29` | **58,000** | |

Check `D` by hand: `0.25 × 0.45 + 0.10 × 0.60 + 0.45 × 0.15 + 0.20 × 0.25 = 0.1125 + 0.06 + 0.0675 + 0.05 = 0.29`. The combat players are the biggest segment and the least hurt, and they still lose 13,500 players. The small entertainer segment loses more than half its members.

Now the recovery. Suppose the game was losing `g_old = 4,000` players a month before the change, the redesign brings `a = 20,000` trial players a month, and `g_new = 3,000` of the remaining players leave each month. Everything turns on `r`:

| Arrivals retained `r` | Net change after redesign | Break-even month `t*` |
|---|---|---|
| 35% | +4,000 per month | 7.3 |
| 25% | +2,000 per month | 9.7 |
| 15% | 0 per month | 14.5 |
| 10% | −1,000 per month | 19.3 |
| 5% | −2,000 per month | 29.0 |

Check the 25% row. The net change is `20,000 × 0.25 − 3,000 = 2,000`. The gap closes at `2,000 + 4,000 = 6,000` per month. `58,000 / 6,000 = 9.7` months.

Look at the bottom rows. Even when the redesigned game keeps shrinking, it eventually passes the no-change path, because the no-change path is assumed to shrink faster. The whole case for the redesign in those rows rests on `g_old`. Set `g_old = 0`, meaning the old game was stable, and the 25% row's break-even moves from 9.7 months to `58,000 / 2,000 = 29` months. The 15% row never breaks even.

This script prints both tables:

```python
S0 = 200_000                      # subscribers the day before the redesign
segments = {                      # share of players, share who leave because of the change
    "crafters and traders": (0.25, 0.45),
    "entertainers":         (0.10, 0.60),
    "combat players":       (0.45, 0.15),
    "Jedi grinders":        (0.20, 0.25),
}
G_OLD = 4_000                     # net loss per month if nothing changes
ARRIVALS = 20_000                 # new and returning trial players per month after the change
G_NEW = 3_000                     # monthly churn among the players who stayed

D = sum(share * leave for share, leave in segments.values())
loss = S0 * D
print(f"departure share D = {D:.4f}, players lost = {loss:,.0f}")
for name, (share, leave) in segments.items():
    print(f"  {name:22} lose {S0 * share * leave:7,.0f}")

def months_to_break_even(r):
    """Month when the redesigned game passes the no-change path."""
    net_new = ARRIVALS * r - G_NEW
    closing = net_new + G_OLD            # how fast the gap between the paths closes
    return loss / closing if closing > 0 else float("inf")

for r in (0.35, 0.25, 0.15, 0.10, 0.05):
    print(f"retain {r:.0%} of arrivals: net {ARRIVALS * r - G_NEW:+7,.0f}/month, "
          f"break-even month {months_to_break_even(r):5.1f}")
```

It prints:

```
departure share D = 0.2900, players lost = 58,000
  crafters and traders   lose  22,500
  entertainers           lose  12,000
  combat players         lose  13,500
  Jedi grinders          lose  10,000
retain 35% of arrivals: net  +4,000/month, break-even month   7.3
retain 25% of arrivals: net  +2,000/month, break-even month   9.7
retain 15% of arrivals: net      +0/month, break-even month  14.5
retain 10% of arrivals: net  -1,000/month, break-even month  19.3
retain 5% of arrivals: net  -2,000/month, break-even month  29.0
```

### Move it yourself

Open the interactive. The top view plots both paths for 36 months. The no-change line slopes gently down from `S₀`. The redesign line drops by `L` at month 0 and then climbs or falls at its own rate. The area between them, while the redesign is behind, is shaded and labeled with its size in player-months. That shaded area is the true price of the change, the play time your game did not have. The bottom view is a stacked bar for month 0 and month 24, one band per segment plus a band for players who arrived after the change.

Start at `r = 25%`. Drag the entertainer departure slider from 0.6 to 0.2 and watch `L` shrink by 8,000 and the break-even move about a month and a third earlier. Then drag `r` from 25% to 15%. The break-even jumps five months. Now set `g_old` to 0. The line you were beating is suddenly flat, and the redesign may never pass it. The segment sliders move a number you can research. The `r` and `g_old` sliders move numbers you have to guess, and they move the answer more.

### Cross-game recognition

The same arithmetic runs under any change that trades a known group of current users for a hoped-for group of new ones.

**Star Wars Galaxies, NGE (November 2005).** In the model, SOE's public case was a large `g_old` (the decline Smedley said the change was needed to reverse) and a large `a × r` (a simpler, more action-driven game that new Star Wars fans would stay in). The segment loss came through the expansion refund at the moment of highest grievance. The record has no reliable subscriber series to check the outcome against, and section 5 explains why that matters as much as the outcome.

**RuneScape and Old School RuneScape (2012 to 2013).** Jagex's Evolution of Combat update in 2012 brought ability-based combat to RuneScape. In February 2013, citing a declining player base and the negative reception of recent updates, Jagex put a poll to players about running a separate version of the game from an August 2007 backup. The poll drew 449,351 votes, enough to meet Jagex's threshold, and Old School RuneScape launched on 22 February 2013 for members at no extra fee. In 2014 the main game added a Legacy Mode with the older interface and combat. In the model, Jagex cut `dᵢ` for the unhappy segment by giving it somewhere to go that it still paid for. Week 7 of this course studies classic servers in depth.

**Final Fantasy XIV (2010 to 2013).** Week 4's case changed the game even more deeply than the NGE did, yet it did not become a cautionary tale. In the model, `S₀` was small after a failed launch, so `L` was small. The studio kept the old players on side with the Legacy Campaign, which lowered `dᵢ`. And the change came with a full relaunch, marketing and a new box, which raised `a`. The same formula, with very different inputs.

**Outside games: New Coke (1985).** The Coca-Cola Company replaced its formula on 23 April 1985 and stopped making the original that week. The public reaction was so hostile that on 11 July, 79 days later, the company announced the original's return as Coca-Cola Classic, and its sales rose. New Coke was a redesign aimed at new customers who preferred a sweeter taste in blind tests, run over existing customers attached to the old product. Coca-Cola's saving move was that the change was reversible, and it reversed it quickly. An MMO whose players have rebuilt their characters under new rules cannot put the old game back so easily.

Four products, one question. Before the change, write down `L` by segment, the counterfactual `g_old`, and the arrivals and retention you are betting on. If the case holds only for the most optimistic `r`, the team is not making a decision. It is hoping.

### Eyes-open design judgment

- **Research `L` before you ship.** The departure shares come from players you already have. Survey them, watch what each segment does, and run the change on a test server with each segment represented. A team that cannot fill in the segment table has not priced the change.
- **Write the counterfactual down and test it.** "We are declining anyway" is the most common justification for a risky redesign, and the easiest to overstate. Show the decline in your own telemetry, with its rate, and show that the redesign addresses its cause. If the old game was stable, the redesign has to win on `r` alone.
- **Watch the segments with outsized value.** The entertainers are 10% of the players, but in Galaxies they fed the combat players' buffs and filled the cantinas. Section 3 shows how their loss creates a second round of departures.
- **Do not let the timing punish the loyal.** Announcing the NGE two days after selling an expansion turned a design disagreement into a question of trust. Ship a redesign with a clear notice period, before any sale that depends on the old rules, and with the refund policy decided in advance.
- **Prefer a change you can reverse, or one you can split.** New Coke recovered because the old product came back in 79 days. Old School RuneScape kept the unhappy segment by giving it its own game. A redesign that cannot be reversed or split needs a much stronger case.

### Check this example

1. With the section 2 table, the team keeps crafting depth, so crafters' departure share falls from 0.45 to 0.15. What are the new `D`, `L` and break-even month at `r = 25%`?
2. What retention `r` does the redesign need to break even within 12 months, with the original `L = 58,000` and `g_old = 4,000`?
3. The team admits `g_old` might be 1,000, not 4,000. Recompute the break-even at `r = 25%`, and say what this does to the argument for the change.

<details>
<summary>Answers</summary>

1. `D = 0.25 × 0.15 + 0.06 + 0.0675 + 0.05 = 0.215`. `L = 43,000`. At `r = 25%` the gap closes at 6,000 per month, so `t* = 43,000 / 6,000 = 7.2` months, two and a half months sooner.
2. The gap must close at `58,000 / 12 = 4,833` per month. That needs `20,000 × r − 3,000 + 4,000 = 4,833`, so `r = 3,833 / 20,000 = 19.2%`.
3. The gap closes at `2,000 + 1,000 = 3,000` per month, so `t* = 58,000 / 3,000 = 19.3` months, twice as long. The redesign now depends mostly on new-player retention, which the team has not measured, instead of on a decline it has.

</details>

## 3. Two redesigns in a row, and the second round

### Losses compound

Galaxies changed combat in spring 2005 and changed everything else in November. Each change drives away a share of the players who were left after the one before:

```
remaining = S₀ × (1 − D₁) × (1 − D₂)
```

If the Combat Upgrade had cost 10% of players and the NGE 29% of the rest, the game would keep `0.90 × 0.71 = 0.639`, or 63.9% of its base, a combined loss of 36.1%. That is less than 10% plus 29%, because the second change can only drive away players the first one left. It is still a large bite. The players who stayed through the first change are also the ones most likely to have valued what the second one removed. They stayed because the core of the game, the professions and the economy, was still there. The model's independent `D₂` is optimistic for them.

A second redesign also resets the recovery clock. Every month spent learning `r` for the first change is lost when the second one changes what new players arrive to.

### Hubs take others with them

Some players matter to others more than their share suggests. A crafter supplies armor to dozens of fighters. An entertainer in Galaxies gave the players in her audience a buff that helped them fight (MMO305 week 2). When a hub leaves, the players who depended on them lose something too, and some of them leave in a **second round**.

A simple way to price it: let `h` be the share of remaining non-hub players who leave for each unit of hub share lost. In the section 2 table, the hub segments (crafters and entertainers) lose `22,500 + 12,000 = 34,500` players, or 17.25% of `S₀`. The non-hub segments keep `76,500 + 30,000 = 106,500` players after round one. With `h = 0.5`, the second round removes `0.5 × 0.1725 × 106,500 ≈ 9,186` more players, and the total loss rises from 58,000 to about 67,200.

The number `h` is hard to measure, but its sign is not. A redesign that hits the hubs hardest, as the NGE hit crafters and entertainers, costs more than its segment table says. A redesign that protects the hubs can afford to hurt other segments more.

## 4. Alternatives to a forced conversion

A redesign swaps one audience for another in a single step. The alternatives keep the known players while the team finds out whether the new ones exist.

**Split the game.** Run the new rules on new servers and the old rules on the existing ones, or add a mode. Old School RuneScape is the case, and RuneScape's own Legacy Mode is a second, smaller version of the idea. The cost is two rule sets to maintain, and a population split that MMO301 week 13's empty-shard spiral warns about. Week 7 covers classic servers.

**Stage the change.** Ship one piece at a time, measure `dᵢ` and `r` after each, and stop if the numbers are bad. A staged change gives up the marketing moment of one big relaunch in return for real data before the commitment is total.

**Test it on a copy first.** Put the change on a public test server with players from every segment. Measure who plays it, who leaves it, and what they say. Week 3's exposure arithmetic applies here too, and a small test cannot see a small `dᵢ`.

**Make it reversible, and say so.** Coca-Cola could go back in 79 days. An MMO can promise a review date and keep the old code path alive until then. A player who knows a change can be undone argues about it instead of leaving (MMO402 week 1's voice instead of exit).

**Relaunch properly.** If the change is big enough to be a new game, make it one. Week 4's Final Fantasy XIV case paired a deep change with a new launch, a marketing push and rewards for the players who stayed. That raises `a` and lowers `dᵢ` together.

None of these is free. Each one trades speed, clarity or money for information. The NGE took none of them, and shipped the change in one step, days after an expansion sale.

## 5. Reading the evidence in this case

A post-mortem is only as good as its evidence, and this case is a lesson in thin evidence. Practise the habits you will need in week 12.

**Separate what was said from what was measured.** The record has SOE's statement in August 2005 that it had sold one million boxed copies. It has unconfirmed reports in early 2006 that only 10,363 subscribers were playing on one Friday night, which Smedley denied. It has no published subscriber series. Boxes sold is not subscribers. A Friday-night count is not subscribers. A denial is not a number. Any claim that "the NGE cost Galaxies X% of its players" is not supported by the public record, and you should not repeat one.

**Weigh each source by what it saw.** Smedley had the data and a reason to defend the decision in 2005, and a different reason to criticize it in 2012. Koster designed the original game and left before the changes. The *New York Times* reported the players' anger and SOE's reasoning at the time. None of them is neutral. Together they agree on the sequence of events and on the size of the backlash. They disagree on why the change was made.

**Look for evidence that does not depend on anyone's account.** In 2004, before the redesigns, fans founded SWGEmu to rebuild the game as it was in April 2005, before the Combat Upgrade. After the closure was announced in 2011, a second project, Project SWG, set out to emulate the later version. Volunteers spent years rebuilding a specific version of the rules. That is behavioral evidence of what one segment valued, stronger than any poll.

**State what the model can and cannot say.** The model says what the NGE needed to be true to pay: a real decline without it, and new players who stayed. The public record cannot tell you whether either held. A good post-mortem says so plainly, then extracts the lesson that does not depend on the missing numbers. Price the loss by segment, write down the counterfactual, and keep a way back.

## In-class activity (25 minutes)

Groups of four. Your MMO has `S₀ = 120,000` subscribers. The design lead proposes replacing the skill-based progression with classes, to make the game easier for new players. You have one week before the decision meeting.

1. Build a segment table with at least four segments. Estimate `wᵢ` and `dᵢ`, and write one sentence per segment on what they lose. Compute `D` and `L`.
2. Marketing estimates `a = 15,000` trial players per month after the change. Telemetry shows the game losing 1,500 players a month now. Assume `g_new = 2,000`. Find the `r` needed to break even within 12 months.
3. Identify the hub segment and estimate a second-round loss with `h = 0.4`.
4. Propose one alternative from section 4 and say which parameter it changes.

Expected output for a table with crafters (0.20, 0.50), guild leaders and organizers (0.10, 0.40), soloists (0.40, 0.10) and PvP players (0.30, 0.20): `D = 0.10 + 0.04 + 0.04 + 0.06 = 0.24`, `L = 28,800`. Break-even in 12 months needs the gap to close at 2,400 per month, so `15,000 × r − 2,000 + 1,500 = 2,400`, `r = 19.3%`. With crafters and organizers as hubs, hub share lost is `(12,000 + 4,800) / 120,000 = 14%`, non-hubs remaining are `43,200 + 28,800 = 72,000`, and the second round is `0.4 × 0.14 × 72,000 ≈ 4,032`.

## Common misconceptions

- **"If new players like the new version, the redesign works."** New players' approval shows up as `a` and `r`. The loss `L` happens on day one, whatever they think. The redesign pays only after `t*` months, and only if the counterfactual was as bad as claimed.
- **"The biggest segment is the one to protect."** Protect the segments whose departure costs the most, counting the second round. In the example, the entertainers are 10% of players and the most likely to leave, and they feed everyone else.
- **"Two changes of 10% and 29% lose 39% of players."** Losses compound on what is left: `1 − 0.90 × 0.71 = 36.1%`. And the players left after the first change are often the ones the second change hurts most.
- **"The NGE killed Star Wars Galaxies."** The game ran for six more years and closed by agreement between SOE and LucasArts. The public record does not show how much of its decline the NGE caused. Say what the evidence supports.

## Check yourself

1. A game with `S₀ = 80,000` has three segments: explorers (0.3, 0.4), raiders (0.5, 0.1) and crafters (0.2, 0.5). Compute `D` and `L`.
2. For question 1, `a = 10,000`, `r = 0.2`, `g_new = 1,500` and `g_old = 2,000`. When does the redesign break even?
3. A studio made two redesigns, the first losing 15% of players and the second 20% of those left. What share of the original base remains?
4. Explain why the break-even month is more sensitive to `r` than to any single `dᵢ` in the section 2 example, using the formula.
5. A producer says, "we'll know within a month whether the redesign worked." Using the model, say what they can know in a month and what they cannot.

<details>
<summary>Answers</summary>

1. `D = 0.12 + 0.05 + 0.10 = 0.27`. `L = 0.27 × 80,000 = 21,600`.
2. The gap closes at `10,000 × 0.2 − 1,500 + 2,000 = 2,500` per month. `t* = 21,600 / 2,500 = 8.6` months.
3. `0.85 × 0.80 = 0.68`, so 68% remains.
4. `t* = L / (a × r − g_new + g_old)`. A change in one `dᵢ` changes `L` by `S₀ × wᵢ × Δdᵢ`, one segment's worth. A change in `r` changes the denominator by `a × Δr`, and when the denominator is small, as it is here (6,000), small changes in it move `t*` a lot. Dropping `r` from 25% to 15% cuts the denominator from 6,000 to 4,000 and adds five months.
5. In a month they can measure `L` and most of the `dᵢ`, because departures are fast, and an early value of `a`. They cannot measure `r` well, because retention of new players is a long-run number, and they can never observe `g_old`, because the no-change path did not happen.

</details>

## Lab / assignment hook

[Lab 05, redesign break-even](../labs/lab05.md). You implement the segment loss, the two-path break-even, compounding and the hub second round, reproduce the section 2 tables, and add a Monte Carlo over the uncertain inputs (`r`, `g_old`, each `dᵢ`) to report the chance the redesign has broken even by month 12. Then you write a 600-word case analysis of the NGE with your own segment table, justified from the sources, and a recommendation of what SOE could have done instead. The case analysis counts toward the course's case-analysis grade.

## Sources

- Wikipedia, "Star Wars Galaxies" (read September 2026). North American launch 26 June 2003; 34 professions at launch (6 basic, 24 advanced); Combat Upgrade in spring 2005, after publish 14.1 of April 2005 (press criticism archived from May 2005), with rising cancellations; *Rage of the Wookiees* released 5 May 2005; *Trials of Obi-Wan* announced 19 August 2005 and released 1 November 2005; NGE implemented about a week after, announced two days after the expansion's release; nine professions after the NGE; refunds after one to two weeks of protest; Smedley's defense as reversing deterioration in the subscriber base; one million boxed copies reported in August 2005; the unconfirmed report of 10,363 subscribers on a Friday night in early 2006 and Smedley's denial; Smedley's July 2012 Reddit comments on "stupid decisions"; closure on 15 December 2011 announced 24 June 2011; SWGEmu founded 2004 to recreate the game through publish 14.1 (April 2005, pre-Combat Upgrade); Project SWG founded 2011.
- Schiesel, S. "For Online Star Wars Game, It's Revenge of the Fans." *The New York Times*, 10 December 2005. Contemporary account of the NGE backlash.
- Wikipedia, "Old School RuneScape" (read September 2026). February 2013 poll citing a declining player base and the reception of updates; 449,351 votes, meeting the launch threshold; launch on 22 February 2013 from an August 2007 backup, for members at no extra fee.
- Wikipedia, "RuneScape" (read September 2026). Evolution of Combat in 2012 introducing ability-based combat; Legacy Mode with the older interface and combat added in 2014.
- Wikipedia, "New Coke" (read September 2026). Introduced 23 April 1985, original production ended that week; return of the original formula announced 11 July 1985, 79 days later, as Coca-Cola Classic, followed by a rise in sales.
- MMO305 week 2 (this program) for the Galaxies entertainer and inspiration-buff mechanics, with its sources.
- Subscriber counts, segment shares, departure shares, arrival rates, retention rates, churn rates and the hub factor in sections 2 and 3 and the activity are invented teaching values. They are not estimates of Star Wars Galaxies' real numbers, which are not public.

## Interactive spec: examples/w05-redesign-break-even.html

**The one insight:** a redesign's loss is immediate and can be researched in advance, while its gain depends on new-player retention and on a counterfactual decline, both guessed. The break-even month moves far more with the guesses than with the researched part.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "two paths": x axis months 0 to 36, y axis players 0 to `S₀`. Line 1 (no change, `--steel`): `S_old(t) = max(0, S₀ − g_old × t)`. Line 2 (redesign, `--moss`): `S_new(t) = max(0, S₀ − L_total + (a × r − g_new) × t)`, where `L_total` includes the second round when that toggle is on. While `S_new < S_old`, shade the area between them in pale `--blood` and label it with its size in player-months (sum over months 0 to 36 of `S_old − S_new` where positive, monthly steps). Mark `t*` with a vertical line and label, or show "no break-even within 36 months".
- View B, "who is playing": two stacked bars, month 0 (just after the change) and month 24. Month 0 bands: each segment's remaining players `S₀ × wᵢ × (1 − dᵢ)`, minus its part of the second round if on (take the second round from non-hub segments in proportion to their remaining size). Month 24 bands: the month-0 old-segment bands scaled by `max(0, 1 − g_new × 24 / S_after)` where `S_after = S₀ − L_total`, plus a "new arrivals" band of `a × r × 24` in `--ochre`. Label each band with its count.

**Controls:**

- `S₀` fixed at 200,000 (displayed).
- For each of the four segments (crafters and traders, entertainers, combat players, Jedi grinders): a departure slider `dᵢ` 0 to 1, step 0.05 (defaults 0.45, 0.60, 0.15, 0.25). Shares `wᵢ` fixed at 0.25, 0.10, 0.45, 0.20 and shown.
- `a` slider 0 to 40,000 per month, step 1,000 (default 20,000).
- `r` slider 0 to 0.6, step 0.01 (default 0.25).
- `g_old` slider 0 to 10,000 per month, step 500 (default 4,000).
- `g_new` slider 0 to 10,000 per month, step 500 (default 3,000).
- "Second round from hubs" toggle (default off) with `h` slider 0 to 1, step 0.1 (default 0.5). Hubs are crafters and entertainers.
- Buttons: "Reset", "Protect crafting" (crafters `d` to 0.15), "Stable old game" (`g_old` to 0).

**Readout (always visible, `aria-live="polite"`):** `D`, `L` (and `L_total` with the second round), players lost per segment, net monthly change after the redesign, `t*` in months (one decimal) or "never", and the shaded player-months.

**Formulas:**

```
D        = Σ wᵢ × dᵢ
L        = S₀ × D
hub_lost = S₀ × (w_craft × d_craft + w_ent × d_ent)
nonhub   = S₀ × (w_combat × (1 − d_combat) + w_jedi × (1 − d_jedi))
second   = h × (hub_lost / S₀) × nonhub          (0 when toggle off)
L_total  = L + second
t*       = L_total / (a × r − g_new + g_old)     ("never" if the denominator ≤ 0)
```

**Test values (must match):**

- Defaults: `D = 0.29`, `L = 58,000`, losses 22,500 / 12,000 / 13,500 / 10,000, net +2,000 per month, `t* = 9.7`.
- `r = 0.35`: `t* = 7.3`. `r = 0.15`: net 0, `t* = 14.5`. `r = 0.10`: `t* = 19.3`. `r = 0.05`: `t* = 29.0`.
- "Stable old game" with defaults: `t* = 29.0`. With `r = 0.15` too: "never".
- "Protect crafting": `D = 0.215`, `L = 43,000`, `t* = 7.2`.
- Second round on, `h = 0.5`, defaults: hub_lost 34,500, nonhub 106,500, second 9,185.6 (display 9,186), `L_total = 67,186`, `t* = 11.2`.

**First screen:** defaults, with the shaded area visible and the caption "The redesign costs 58,000 players on day one. Whether it ever pays depends on two sliders you cannot measure in advance: r and g_old."

**Accessibility:** all controls keyboard operable with visible focus; readout in `aria-live="polite"`; bar bands labeled with text as well as color; respects `prefers-reduced-motion` and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only, no game art, logos, Star Wars imagery or screenshots.
