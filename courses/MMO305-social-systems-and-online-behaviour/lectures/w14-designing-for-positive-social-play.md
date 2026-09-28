# MMO305 · Week 14 — Designing for Positive Social Play

**Why this matters:** Most of what players feel about strangers in your game is decided by your reward rules, long before anyone types a word. If another player showing up costs you loot, you will learn to resent them. If it earns you loot, you will learn to welcome them. This week turns that observation into a number you can compute for any system, and then asks what it costs to make that number positive.

**You will be able to:**
- Compute the stranger payoff `Δr`, the change in one player's reward rate when one more player arrives, for exclusive tagging, shared credit and shared credit with scaling.
- Recognise the same payoff structure in World of Warcraft tapping, Guild Wars 2 events and gathering, and Journey.
- Compute the faucet cost and the free-rider limit that come with shared credit, and choose a scaling rule deliberately.
- Design a low-cost prosocial action (endorsement, revive, mentor reward) with limits that stop it being farmed.

**Before class:** Steinkuehler & Williams (2006), "Where Everybody Knows Your (Screen) Name", the sections on third places and on bridging social capital. Reread your notes on Ducheneaut et al. (2006) from week 2. Guild Wars 2 Wiki, "Dynamic event" and "Loot" (current game).

**Prerequisites from earlier courses:** [GS101 week 5, text adventures and MUD1](../../GS101-history-and-critical-study-of-games/lectures/w05-text-adventures-and-mud1.md) (shared versus per-player resource pools, including Guild Wars 2 gathering). [MMO304 week 3, faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) (why doubling a faucet matters). [GD203 week 13, difficulty modes and scaling](../../GD203-combat-and-progression-design/lectures/w13-difficulty-modes-and-scaling.md) (scaling challenge to the player). [UX201 week 4, self-determination theory](../../UX201-game-ux-and-player-psychology/lectures/w04-self-determination-theory.md) (relatedness as a need). From this course: [week 1, social capital](w01-mmos-as-societies-social-capital.md), [week 10, communication design](w10-communication-design-chat-emotes-pings.md), [week 3, forced versus voluntary grouping](w03-forced-vs-voluntary-grouping.md) and [week 8, griefing](w08-griefing-typology-and-design-responses.md).

**Interactive:** [Is a stranger good news?](../examples/w14-stranger-payoff.html). Use it during section 2.

---

## 1. What "positive social play" means for a designer

This course has spent thirteen weeks on social ties, and most of the news has been cautionary. Grouping can be forced into resentment (week 3). Guilds burn out (week 4). Loot splits friendships (week 5). Griefers exploit every system that lets one player hurt another (week 8). Toxicity spreads through chat (week 9).

This final lecture asks the constructive question. What do systems look like that make strangers glad to see each other, and make small kind acts cheap and visible?

Define **positive social play** as interaction between players that leaves each of them better off than if the other had not been there. The definition is deliberately narrow. It does not require friendship, conversation, or even awareness of the other person. Ducheneaut and colleagues found in 2005 World of Warcraft that players spent much of their time outside groups yet did not experience the game as lonely. Other players were an audience and a presence, "alone together". Positive social play covers that too.

Steinkuehler and Williams (2006) supply the reason to care. Their argument is that MMOs work as "third places" (informal public spaces separate from home and work) and that they are especially good at building **bridging social capital**. That means weak ties between different kinds of people, as opposed to the deep **bonding** ties of close friends. Bridging ties form from many small, low-stakes positive encounters with strangers. Week 1 introduced the distinction. This week is about manufacturing those encounters on purpose.

There are four design levers, and the worked example covers the first.

1. **The sign of the encounter.** Does another player's presence raise or lower my reward?
2. **Cheap prosocial acts.** Can I help someone at low cost, and does anyone notice?
3. **Harm-proof communication.** Can I signal to a stranger without giving them a channel to abuse me?
4. **Measurement.** Do we know whether any of this worked?

## 2. Worked example: is a stranger good news?

### The hook

Picture a quest that asks you to kill a named monster. In classic World of Warcraft, when another player jogs up to that monster, you tense. Only the first player (and that player's party) to hit it gets credit. Their arrival is a threat. In retail World of Warcraft since patch 7.0.3 (July 2016, the Legion pre-patch), up to five players who are not grouped with you can tap the same monster, and players beyond five share quest credit for named monsters. The same stranger jogging up is now help. In Guild Wars 2, every player who contributes enough to a kill gets loot calculated as if they were the only participant.

Same encounter, same monster, opposite feeling. The game has not changed how friendly its players are. It has changed the sign of one number.

### The model

Consider a hunting spot with `n` players in it. Define:

- `S` is the spawn rate, monsters per minute available in the spot.
- `H` is a monster's health.
- `d` is one player's damage per second.
- `t_s` is the search time in seconds between kills (walking, looting, finding the next target).
- `r(n)` is one player's reward rate in credited kills per minute when there are `n` players.

Alone, a player's cycle is `H/d + t_s` seconds, so their solo capacity is `c = 60 / (H/d + t_s)` kills per minute.

The **stranger payoff** is the change in my reward rate when one more player arrives:

```
Δr(n) = r(n + 1) − r(n)
```

When `Δr` is negative, strangers are competitors. When it is zero, they are furniture. When it is positive, they are help. The whole worked example is about the sign of `Δr`.

Now write `r(n)` under three rules.

**Rule A, exclusive tag.** Each kill belongs to one player. Players hunt separately and share the spawn supply.

```
r_A(n) = min(c, S / n)
```

**Rule B, shared credit.** Everyone who hits a monster gets full credit. Players converge on the same target, so it dies `n` times faster.

```
r_B(n) = min(S, 60 / (H / (n × d) + t_s))
```

**Rule C, shared credit with scaling.** As rule B, but monster health grows with the crowd, `H(n) = H × (1 + s × (n − 1))`, where `s` is the scaling factor.

```
r_C(n) = min(S, 60 / (H × (1 + s(n − 1)) / (n × d) + t_s))
```

With `s = 0`, rule C is rule B. With `s = 1`, the time to kill stays `H/d` no matter how many players arrive, so `r_C(n) = c` for everyone and `Δr = 0`.

### Numbers you can check

Use `H = 1,000`, `d = 50` (a 20-second solo kill), `t_s = 10` seconds, and `S = 6` monsters per minute. Solo capacity is `c = 60 / 30 = 2` kills per minute.

| Players `n` | Rule A, exclusive | Rule B, shared | Rule C, shared, `s = 0.5` |
|---|---|---|---|
| 1 | 2.00 | 2.00 | 2.00 |
| 2 | 2.00 | 3.00 | 2.40 |
| 3 | 2.00 | 3.60 | 2.57 |
| 4 | 1.50 | 4.00 | 2.67 |
| 6 | 1.00 | 4.50 | 2.77 |
| 12 | 0.50 | 5.14 | 2.88 |

Check two cells by hand. Rule B at `n = 4`: the kill takes `1,000 / 200 = 5` seconds, plus 10 seconds of search, so 15 seconds per kill and 4.00 per minute. Rule C at `n = 4`: health is `1,000 × 2.5 = 2,500`, time to kill is `2,500 / 200 = 12.5` seconds, plus 10 is 22.5, so 2.67 per minute.

Now the stranger payoff, going from 3 to 4 players:

| Rule | `r(3)` | `r(4)` | `Δr(3)` | What the fourth player feels like |
|---|---|---|---|---|
| A, exclusive | 2.00 | 1.50 | −0.50 | a thief |
| B, shared | 3.60 | 4.00 | +0.40 | help |
| C, `s = 0.5` | 2.57 | 2.67 | +0.10 | mild help |
| C, `s = 1` | 2.00 | 2.00 | 0.00 | furniture |

Rule A is fine until the spot is full. Here the first three players never notice each other, because `S / n` stays at or above `c` up to `n = 3`. The fourth player is where the spot tips into competition, and every further player makes it worse. The crossover is `n* = S / c`, here 3.

Open the interactive. The left panel plots `r(n)` for all three rules. The right panel shows `Δr` for the current `n` as a bar that turns from red (below zero) through grey to green (above zero). Drag `n` from 1 to 12 and watch rule A's bar flip red at the fourth player while rule B's stays green. Then drag the scaling slider `s` from 0 to 1 and watch rule C's green bar shrink to grey.

### Cross-game recognition

**World of Warcraft, classic versus retail.** Classic tapping is rule A with one twist. A party taps as a unit, so inviting the stranger turns them from a thief into a party member. The Warcraft Wiki records the etiquette that grew from this. In classic you invite a player who wants the same monster, and deliberately tapping monsters to block someone else's quest is griefing. Patch 7.0.3 moved retail to rule B with a cap: up to five ungrouped players can tap a monster, and players beyond five still share quest credit for named monsters. Within the cap, `Δr` is positive. Beyond it, players who miss the tap compete again. Even earlier, Blizzard had used shared credit for special cases. A January 2011 hotfix gave quest credit for the Tol Barad Peninsula quest bosses to everyone who took part, grouped or not.

**Guild Wars 2 events and gathering (current game).** Guild Wars 2 is the clearest rule C in the genre. Each enemy has a damage threshold, about 5% to 10% of its health by the wiki's account, and any player who passes it gets their own loot "as if they were the only participant". Dynamic events give every participant full experience without needing a party. Events also scale with the crowd, and they do more than add health. More enemies spawn, veterans or champions appear, enemies gain abilities, and objectives grow. The scaling factor `s` is real, and ArenaNet chose it. The same idea covers gathering. As GS101 week 5 showed, most Guild Wars 2 resource nodes can be harvested by each character separately. That makes a stranger at your ore vein cost you nothing, `Δr = 0`, where MUD1's shared pool made them a thief.

**Journey (thatgamecompany, 2012).** Journey has no loot, but the same logic applies to the only resource it has, which is progress and company. Two anonymous players can meet and help each other. They cannot speak or type, and their only signal is a musical chime. There is no action one player can take that harms the other. The designers set out to move beyond what its designer, Jenova Chen, called the typical "defeat/kill/win" framing. In the terms of this lecture, Journey forces `Δr ≥ 0` by removing every negative channel. It is the extreme point of the design space. It gets strong positive encounters and gives up competition entirely.

Three games, one question. Whenever a stranger arrives, what happens to my rate of reward? Classic WoW answers negative, retail WoW and Guild Wars 2 answer positive within limits, and Journey answers never negative by construction.

### Eyes-open design judgment

Making `Δr` positive is not free. Every game above paid for it somewhere.

**The faucet grows with the crowd.** Under rule A, the spot can never produce more than `S` kills per minute in total, here 6. Under rule B every kill is credited to everyone. At `n = 6` the spot credits `6 × 4.50 = 27` kills per minute, 4.5 times as much loot from the same monsters. At `n = 12` it credits `12 × 5.14 ≈ 61.7`. If each credited kill drops currency, shared credit is a faucet that multiplies with crowd size (MMO304 week 3). Guild Wars 2's scaling (rule C) and a participation cap exist partly to hold this in check. The wiki reports a soft limit of around the first 50 qualifying players per enemy.

**Challenge collapses.** Rule B makes a monster die `n` times faster. At `n = 12` a 20-second fight lasts under 2 seconds. That is fine for a quest mob and fatal for a boss. Scaling restores the fight, but at `s = 1` it also removes the reward for cooperating. Somewhere between 0 and 1 is a choice about how much the crowd should help.

**Free riders.** Shared credit invites players who contribute almost nothing. A damage threshold `θ` limits this, and it also caps how many equal contributors can qualify. If `n` players split the damage evenly, each deals a share `1/n`, so all of them qualify only while `1/n ≥ θ`. At `θ = 10%` that is 10 players. At `θ = 5%` it is 20. Beyond that, some honest players miss out. That is why Guild Wars 2 counts support actions, such as healing and boons, toward the reward.

**Negative `Δr` has uses.** Rule A produced the classic-WoW invitation etiquette. A small conflict gave strangers a reason to talk and a cheap way to resolve it by grouping. Week 3 showed that forced interaction can build ties as well as resentment. Removing every conflict can also remove every reason to speak. Journey accepts that trade. A game that wants guilds to form out of chance meetings may not.

The decision to make deliberately is where on the curve you want each kind of content. You might want `Δr > 0` for open-world quest monsters, `Δr ≈ 0` for gathering, and a controlled negative for contested rare spawns that exist to create stories. Write the choice into your design document for each system, so nobody sets it by accident.

## 3. Cheap prosocial acts, and how to keep them honest

The second lever is the price of kindness. A **prosocial act** is one that benefits another player at some cost to you. Examples are reviving someone, answering a newcomer's question, giving directions, or tanking for a pickup group. Designers can lower the cost (make reviving quick), raise the visibility (show who helped), or pay for it (reward the helper).

Paying is the risky one. Any reward for helping becomes a reward for *appearing* to help, and players will farm it. Overwatch's endorsement system shows the kind of guard rails this needs. The Overwatch Wiki describes the current Overwatch 2 rules like this:

- You may endorse at most 2 players per match, and the same player at most once every 12 hours.
- Endorsing someone earns *you* a small battle pass reward, so giving is paid as well as receiving.
- Endorsement level runs from 1 to 5 and decays a little after every match, so it measures recent behaviour, not lifetime totals.
- Penalties from the report system can drop a player to level 0, and match and team text chat need level 2.

Read those rules against the farming problem. The 2-per-match limit keeps an endorsement scarce enough to mean something. The 12-hour limit stops two friends endorsing each other every game. Decay means a player cannot bank goodwill and then turn toxic. Gating chat on endorsement level links the positive system to the negative one (week 9), so good behaviour earns a voice.

The general rule has four parts. Cap how often an act can be rewarded. Stop the same pair trading it back and forth. Make the reward decay. Tie the reward to something the player values beyond the currency itself.

## 4. Harm-proof communication

The third lever is signalling. Week 10 covered chat, emotes and pings. The point to add here is that every communication channel is also a channel for harm, and the most positive systems restrict the vocabulary on purpose.

Journey is the extreme case, with only a chime and no text, voice or names until the credits. Between Journey and open chat lies a spectrum of **constrained communication**. Examples are context pings that say "enemy here" or "on my way", a fixed set of emotes, and pre-written thank-you messages. Each removes the ability to insult while keeping the ability to coordinate and thank. The trade-off is expressiveness. A game that restricts communication too far loses the friendships that need real conversation. A common pattern is to layer the channels. Everyone gets constrained signals with strangers. Friends, guildmates and players with a good record (as in Overwatch's chat gating) unlock open chat.

## 5. Measuring whether it worked

The fourth lever is measurement. Positive social play is easy to claim and hard to show. Useful measures to put on your dashboard include:

- **Stranger co-presence rate.** The share of kills, events or gathering actions done within some radius of a non-grouped player. It shows whether the open world is actually shared.
- **Conversion to ties.** The share of stranger encounters that end in a friend request, party invite or guild invite within a set time. This is the bridging-capital measure from week 1.
- **Repeat co-play.** How often two players who met by chance play together again within a week.
- **Prosocial action rates.** Revives of non-group members, endorsements, and mentor sessions per active hour.
- **The counterweight.** Report rates and blocks per stranger encounter, measured at the same time. If co-presence rises and reports rise faster, you built crowding, not community.

Remember week 13's warning before you read any of these. Per-hour and per-encounter rates are length-biased toward heavy players, so segment by play time. An A/B test (MA102 week 14) that changes one tagging rule on half the servers is the cleanest way to see what `Δr` does to behaviour.

## In-class activity (30 minutes)

Groups of three. Each group gets one card naming a system from a shipped game: classic WoW rare-spawn camping, a Guild Wars 2 world boss, a shared gathering node, a battle royale's loot on the ground, or an MMO trading post.

1. (10 min) Write the system's reward rule as rule A, B or C, or a mix. Choose plausible values of `S`, `H`, `d` and `t_s`, state that they are your assumptions, and compute `r(n)` and `Δr(n)` for `n = 1` to `6` in the interactive's custom mode or a spreadsheet.
2. (10 min) Decide whether the sign of `Δr` suits what the system is for. If not, redesign it with one change (a cap, a threshold, a scaling factor, per-player instancing). Recompute.
3. (10 min) Name the cost of your change using section 2's list (faucet, challenge, free riders, lost reasons to talk) and give its size where you can.

Expected output: a before-and-after table of `Δr`, one sentence on the purpose of the system, and one number for the cost of the change.

## Common misconceptions

- **"Positive social play means making players talk to each other."** Many positive encounters are silent. Ducheneaut and colleagues found WoW players valued an audience and a presence even when they played alone. The measurable thing is whether presence helps, not whether anyone speaks.
- **"Shared credit is free generosity."** It multiplies the loot faucet by the crowd size (27 credited kills a minute instead of 6 at `n = 6` in section 2) and speeds up fights. Both need a deliberate counterweight.
- **"Scaling to `s = 1` is the fair setting."** At `s = 1` the stranger payoff is exactly zero, so cooperation brings no reward. Choose `s` for the feeling you want, not for symmetry.
- **"Rewarding kindness makes players kinder."** It makes the rewarded behaviour more common, including fake versions of it. Without caps, pair limits and decay, an endorsement system becomes a trading system.

## Check yourself

1. A spot has `S = 4` monsters per minute and each player's solo capacity is `c = 2`. Under exclusive tagging, which player's arrival first makes `Δr` negative, and by how much?
2. Using the section 2 values (`H = 1,000`, `d = 50`, `t_s = 10`), compute `r_C(2)` for `s = 0.25`. Is the second player help or a thief?
3. A game uses a damage threshold of 8% for loot credit. What is the largest number of equal contributors who all qualify?
4. Under rule B at `n = 6`, how many credited kills per minute does the spot produce, and how many times the rule A total is that?
5. A designer adds "thank" buttons that give the thanked player 10 gold each, with no limits. Predict what players will do in the first week, and name two limits from section 3 that fix it.

<details>
<summary>Answers</summary>

1. `r_A(n) = min(2, 4/n)`. At `n = 2`, `r = 2`. At `n = 3`, `r = 4/3 ≈ 1.33`. The third player's arrival makes `Δr(2) ≈ −0.67`.
2. `H(2) = 1,000 × 1.25 = 1,250`. Time to kill is `1,250 / 100 = 12.5` seconds, plus 10 is 22.5 seconds, so `r_C(2) = 60 / 22.5 ≈ 2.67`. That beats the solo 2.00, so `Δr(1) ≈ +0.67` and the second player is help.
3. All qualify while `1/n ≥ 0.08`, so `n ≤ 12.5`. The answer is 12.
4. `6 × 4.50 = 27` credited kills per minute. Rule A's total is capped at `S = 6`, so the ratio is 4.5.
5. Pairs and small groups will thank each other in a loop to mint gold, and bots will join them. The button becomes a faucet (MMO304 week 3) and stops meaning anything. Fixes: cap thanks per match or per day, and block repeat thanks between the same pair within a time window. Better still, pay in a decaying standing that unlocks something (as Overwatch does with chat) rather than in tradeable gold.

</details>

## Lab / assignment hook

[Lab 14, positive-sum audit](../labs/lab14.md). You model one social system from a shipped game in a spreadsheet, compute its stranger payoff, faucet multiplier and free-rider limit, and propose a redesign. The lab feeds directly into the final assessment (week 15), the social system design and research proposal. That proposal should state the intended sign of `Δr` for each system it designs.

## Sources

- Warcraft Wiki, "Tap" (accessed September 2026). Classic rule (first player and party); retail rule of up to five non-grouped players tapping, with players beyond five sharing quest credit for named monsters; patch 7.0.3 change; January 7, 2011 hotfix for Tol Barad Peninsula quest bosses; etiquette and tap-denial as griefing. https://warcraft.wiki.gg/wiki/Tap
- Guild Wars 2 Wiki, "Loot" (current game, accessed September 2026). Per-player loot, damage threshold of about 5% to 10% of enemy health, support counting toward rewards, an observed cap of about 50 players. https://wiki.guildwars2.com/wiki/Loot
- Guild Wars 2 Wiki, "Dynamic event" (current game, accessed September 2026). Full experience to all participants without a party, loot calculated per participant, and scaling by enemy count, level, abilities, veteran and champion upgrades and objective size. https://wiki.guildwars2.com/wiki/Dynamic_event
- Guild Wars 2 Wiki, "Gathering", as cited in GS101 week 5. Per-character resource nodes.
- Wikipedia, "Journey (2012 video game)" (accessed September 2026). thatgamecompany, released on PlayStation 3 in March 2012; anonymous co-players who cannot speak or type and communicate with a musical chime; the design aim of moving past the "defeat/kill/win" framing.
- Overwatch Wiki, "Endorsements" (Overwatch 2, 2026 seasons, accessed September 2026). Two endorsements per match, 12-hour limit per player, levels 1 to 5 with per-match decay, level 0 after report penalties, chat gated at level 2, battle pass reward for giving. https://overwatch.fandom.com/wiki/Endorsements
- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2006). "Alone Together? Exploring the Social Dynamics of Massively Multiplayer Online Games." *Proceedings of CHI 2006*. World of Warcraft, 2005; players valued others as audience and presence.
- Steinkuehler, C. A. & Williams, D. (2006). "Where Everybody Knows Your (Screen) Name: Online Games as 'Third Places'." *Journal of Computer-Mediated Communication* 11(4), 885-909.
- The hunting-spot numbers in section 2 (`H`, `d`, `t_s`, `S`) are invented for teaching and are not taken from any game.

## Interactive spec: examples/w14-stranger-payoff.html

**The one insight:** the same stranger is a thief, furniture or help depending only on the reward rule, and the sign of `Δr` is something the designer sets. The student should see rule A's payoff bar flip from grey to red as the spot fills, rule B's stay green, and rule C's shrink toward grey as scaling rises.

**Layout.** Two linked panels.
- Left: line chart of `r(n)` for `n = 1` to `20` (x axis, integers) for rules A, B and C, in three palette colours, with a vertical marker at the current `n`. A dashed horizontal line marks `S`, and a dotted one marks solo capacity `c`.
- Right: three horizontal bars showing `Δr(n) = r(n+1) − r(n)` for each rule at the current `n`. Bar colour runs from red (below −0.01) through grey (within ±0.01) to green (above +0.01), with the value printed to two decimals and a label: "thief", "furniture", "help".
- Below: a readout table for the current `n` with, per rule, `r(n)`, `Δr(n)`, credited kills per minute for the whole spot (`n × r(n)` for B and C, `min(n × c, S)` for A), the faucet multiplier relative to rule A, and fight length in seconds (`H/d` for A, `H/(n d)` for B, `H(1+s(n−1))/(n d)` for C).
- Second tab, "Free riders": slider for threshold `θ` (1% to 25%, step 1%). Show `n_max = floor(1/θ)` and, on the left chart, shade the region `n > n_max` for rules B and C.

**Controls.** Sliders for `n` (1-20), `S` (1-20 per minute), `H` (100-5,000, step 100), `d` (10-200, step 10), `t_s` (0-60 seconds), `s` (0-1.5, step 0.05). All keyboard operable. A reset button restores the defaults.

**Formulas.**
- `c = 60 / (H/d + t_s)`
- `r_A(n) = min(c, S/n)`
- `r_B(n) = min(S, 60 / (H/(n d) + t_s))`
- `r_C(n) = min(S, 60 / (H(1 + s(n − 1))/(n d) + t_s))`

**Defaults.** `n = 3`, `S = 6`, `H = 1,000`, `d = 50`, `t_s = 10`, `s = 0.5`, `θ = 10%`.

**Test values (two decimals).**
- Defaults: `c = 2.00`. `r_A(3) = 2.00`, `r_A(4) = 1.50`, `Δr_A = −0.50`. `r_B(3) = 3.60`, `r_B(4) = 4.00`, `Δr_B = +0.40`. `r_C(3) = 2.57`, `r_C(4) = 2.67`, `Δr_C = +0.10`.
- `n = 6`: `r_A = 1.00`, `r_B = 4.50`, `r_C = 2.77`. Spot credits: A 6.00, B 27.00, C 16.62. Faucet multiplier for B is 4.50.
- `n = 12`: `r_A = 0.50`, `r_B = 5.14`, `r_C = 2.88`.
- `s = 1`: `r_C(n) = 2.00` for all `n` and `Δr_C = 0.00` (grey, "furniture").
- `θ = 10%`: `n_max = 10`. `θ = 5%`: `n_max = 20`. `θ = 8%`: `n_max = 12`.

**No game art.** Players and monsters, if drawn at all, are plain shapes. Games are named only in the explanatory text.
