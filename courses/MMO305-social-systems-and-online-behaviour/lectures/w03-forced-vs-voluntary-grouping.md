# MMO305 · Week 03 — Forced vs Voluntary Grouping

**Why this matters:** Every MMO team argues about grouping. One side says "make content that needs groups, or nobody will meet anyone." The other says "let people solo, or they will quit while waiting for a tank." Both sides are right about something, and both usually miss the variable that decides whether grouping makes friends at all, which is how often you meet the same person twice. This week you will compute it.

**You will be able to:**
- Place a game's grouping design on the spectrum from forced to voluntary, and compute when grouping beats soloing for a player who wants progress.
- Compute, with the binomial model, how many distinct people a player meets, how many they meet again, and how many become acquaintances, for a given pool size.
- Explain why large matchmaking pools make groups faster to form and slower to produce ties, and connect this to the "shadow of the future."
- Design a grouping system that sets pool size and repeat encounters deliberately, and critique WoW, EverQuest, Final Fantasy XIV and Guild Wars 2 in those terms.

**Before class:** Reread the "social factor" section of Ducheneaut et al. (2006) from week 2, on grouping and levelling speed. Robert Axelrod, *The Evolution of Cooperation* (1984), chapter 1 and the first half of chapter 7 ("How to Promote Cooperation"), which introduces the shadow of the future.

**Prerequisites from earlier courses:** [MMO305 week 1, social capital](w01-mmos-as-societies-social-capital.md) and [MMO305 week 2, playing alone together](w02-playing-alone-together.md). [MA102 week 6, the binomial distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md), which this week's model uses directly. [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md), for `1 − (1 − p)^r`. [MMO303 week 5, the holy trinity](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w05-the-holy-trinity-tank-healer-dps.md), which already worked out role bottlenecks and queue math; we do not repeat it. [MMO303 week 10, game theory and payoff matrices](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md), for the prisoner's dilemma in section 4. [MMO301 week 4, EverQuest](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w04-everquest-the-treadmill-and-the-raid.md), for the group-centered design we contrast with WoW.

**Interactive:** [examples/w03-reencounter.html](../examples/w03-reencounter.html). Use it during section 3.

---

## 1. The grouping spectrum

"Forced" and "voluntary" are not two boxes. They are ends of a line, and every piece of content sits somewhere on it.

- **Forced grouping.** The content cannot be done alone at any reasonable rate. EverQuest's design put group combat at the center of play, and its hardest monsters needed many groups organized by a guild. If you wanted to progress, you found people.
- **Incentivized grouping.** Soloing works, but groups get a bonus (more experience, better drops, access to content). Players choose, and the size of the bonus decides the choice.
- **Implicit or open grouping.** Players help each other without forming a group. Guild Wars 2's dynamic events give every participant full experience and their own loot roll, so strangers in the same place are allies by default.
- **Matchmade grouping.** A tool assembles a group for you from a pool, so the formation cost falls to a queue. World of Warcraft's Dungeon Finder, added in patch 3.3.0 (December 2009), drew from every realm in a battlegroup.
- **Grouping with NPCs.** The game replaces missing players with computer-controlled companions. EverQuest added hireable NPC mercenaries in Seeds of Destruction (October 2008). Secondary accounts tie the feature to the growing difficulty of finding players of the right level; we found no SOE statement of the reason. Final Fantasy XIV's Duty Support system lets players run main-story dungeons with a party of NPCs.

Moving right along this list lowers the cost of getting a group. It also changes *who* you group with, and that is the part designers overlook.

### When does a rational player group?

Last week's census found WoW characters who never grouped levelled about twice as fast as those who grouped. A simple rule explains why they soloed.

```
group if  R_g × (1 − w)  >  R_s
```

- `R_s` is the reward rate soloing (experience, loot or currency per hour of play).
- `R_g` is the reward rate once a group is running.
- `w` is the share of the session lost to forming the group (waiting, travelling, replacing people who leave).

Take the 2005 census case, where soloing was about twice as fast, so `R_s = 2 × R_g`. Even with instant groups (`w = 0`), `R_g < R_s`, so the rule says solo. Suppose forming a group eats a quarter of the session, `w = 0.25`. Then grouping only wins if `R_g > R_s / 0.75 = 1.33 × R_s`. Starting from the 2005 numbers, the group reward rate would need to rise by a factor of `2 × 1.33 = 2.67` before grouping pays.

Two design levers follow directly. You can raise `R_g` (bonuses, group-only rewards), or you can shrink `w` (matchmaking, teleports to the dungeon, NPC fill-ins). Forced grouping is the special case where `R_s` is near zero, so any `R_g` wins. Every one of these levers changes the rewards. None of them says anything about whether the group becomes a set of friends. For that we need a different model.

## 2. Groups, ties and repeat encounters

Week 1 said bonding ties need repeated contact. Week 2 showed that co-activity is the layer where real ties form. Put those together. A pick-up group is co-activity, but a tie forms only if you meet that person again, and again. Granovetter's tie strength grows with time spent together. One dungeon run with a stranger is one unit of time. Three runs with the same stranger is the start of an acquaintance.

So the question for any grouping design is "given how groups are formed, how often will a player meet the same person again?" That depends mostly on one number, the size of the pool the group is drawn from.

## 3. Worked example: strangers in the queue

### The hook

World of Warcraft's Dungeon Finder places a "Dungeon Deserter" debuff on players who leave a group before a boss dies, blocking them from the Dungeon and Raid Finder for 30 minutes. It also lets a group vote to kick a member. Why would a group-making tool need formal punishments and votes? On an old server where groups formed from whoever was in the zone, leaving a group early cost you your name. People remembered. In the Dungeon Finder, the four people you abandon come from many realms, and you will probably never see them again. The penalty exists because the pool is so big that reputation stopped working. Let us measure how big "big" has to be.

### The model

Each run, a player is placed in a group with `m` other players, drawn at random from the `N − 1` other players in the pool. Over `r` runs, the number of times you meet any one specific other player follows a binomial distribution.

```
p = m / (N − 1)                  chance a given player is in your group on one run
X ~ Binomial(r, p)                times you meet that player in r runs

distinct people met    D = (N − 1) × (1 − (1 − p)^r)
repeat encounters      = m × r − D
acquaintances          A = (N − 1) × P(X ≥ k)
chance a partner shows up again in your next r runs  = 1 − (1 − p)^r
```

- `N` is the pool size, the number of players who could be put in your group.
- `m` is the number of other players per group. For a 5-player dungeon, `m = 4`.
- `r` is the number of runs, for example over a month.
- `k` is how many encounters it takes to recognize someone and want to play with them again. We use `k = 3`. It is a design assumption, not a fact of psychology, and the interactive lets you change it.

`D` comes from the complement rule you met in MA102 week 3. Any one of the `N − 1` others is missed on a run with chance `1 − p`, and missed on all `r` runs with chance `(1 − p)^r`. So they are met at least once with chance `1 − (1 − p)^r`. Multiply by the number of people to get the expected number met.

### Numbers you can check

Take `m = 4` and `r = 20` runs, about a month of evenings.

| Pool size N | p per run | Distinct people met | Repeat encounters | Acquaintances (met 3+ times) | Chance a partner reappears in next 20 runs |
|---|---|---|---|---|---|
| 60 | 0.0678 | 44.5 | 35.5 | 8.9 | 75% |
| 200 | 0.0201 | 66.4 | 13.6 | 1.4 | 33% |
| 1,000 | 0.0040 | 77.0 | 3.0 | 0.07 | 8% |
| 5,000 | 0.0008 | 79.4 | 0.6 | 0.00 | 2% |
| 20,000 | 0.0002 | 79.8 | 0.15 | 0.00 | 0.4% |

Check the `N = 200` row by hand. `p = 4 / 199 = 0.0201`. The chance of missing a given player for 20 runs is `0.9799^20 ≈ 0.666`, so `D = 199 × 0.334 = 66.4`. Twenty runs have `4 × 20 = 80` partner slots, so `80 − 66.4 = 13.6` slots went to people you had already met. For acquaintances, add up the chance of meeting a given person 0, 1 or 2 times, `0.666 + 0.273 + 0.053 = 0.993`, so `P(X ≥ 3) = 0.007` and `A = 199 × 0.007 ≈ 1.4`.

Read down the columns. The number of distinct people met barely changes. It rises from 44.5 to 79.8, capped by the 80 slots. The number of acquaintances collapses from about 9 to zero. Somewhere between a pool of 200 and a pool of 1,000, **grouping stops making acquaintances**, however many groups a player joins.

### The visual

Open the interactive. The left view plots, against pool size on a log scale from 20 to 50,000, the distinct people met in `r` runs. It rises and flattens. It looks like bigger pools are more social, since you meet more people. The right view plots, on the same axis, repeat encounters and acquaintances. They fall off a cliff. Drag the pool size slider and watch both views move together. Then raise `r` to 100 runs (a heavy player's season) and see how far right the cliff moves. It moves, but not by much. The play volume needed to keep acquaintances in a large pool grows roughly in proportion to the pool.

A second tab runs a simulation of 1,000 players with seeded random matching, so you can check that the formula's averages match what individual players experience, and see the spread around them.

### Why it works this way

The chance of meeting a specific person on any run is `p = m/(N − 1)`. For small `p`, the expected number of meetings with one person over `r` runs is `r × p`. To meet the same person three times on average, you need `r × p ≈ 3`, so `r ≈ 3 × (N − 1)/m`. In a pool of 200 that is about 150 runs. In a pool of 20,000 it is about 15,000 runs. No player runs that many dungeons. So in a large pool, repeat meetings are rare accidents. The tool makes groups efficiently and makes ties almost never.

This is a trade-off, not a bug. The same big `N` that kills repeat encounters is what makes the queue short. MMO303 week 5 showed that group formation is limited by the scarcest role. A bigger pool has more of every role, so the queue pops sooner. Pool size buys speed and costs familiarity.

### Cross-game recognition

Rewrite each game as a pool size `N`, a group size `m`, and a rule for whether you can meet people again on purpose.

**EverQuest (1999 onward).** Groups formed on one server, often in one zone, among players of similar level. The effective pool at any moment was the handful of players in your level range nearby, a pool of tens to low hundreds. By the table, players in such pools meet the same people repeatedly, and reputation follows. When population shrank and pools got too small to form groups at all, the 2008 mercenaries replaced missing players with NPCs. In the model, that sets the human part of the group to zero. The group always forms, and it produces no ties.

**World of Warcraft Dungeon Finder (patch 3.3.0, December 2009 onward).** The tool connects all realms in a battlegroup and assembles 5-player groups automatically. That is `m = 4` with `N` in the thousands. By the table, the chance of a partner reappearing is a few percent a month. The Dungeon Deserter debuff and vote-kick replace the social memory a small pool provides. WoW also has a Looking for Group channel in capital cities, for forming groups by hand from people you can see and talk to.

**Final Fantasy XIV Duty Finder (current era).** It matches across the worlds of a data center. The game offers two levers the model recognizes. Duty Roulette pays an "In Need" bonus to whichever role (tank, healer or DPS) is most needed, which shortens queues by changing role supply. Duty Support lets players run main-story dungeons with NPCs. That gives a solo player a guaranteed group with no social cost, and also no chance of a tie.

**Guild Wars 2 dynamic events (2012 onward).** Events set `m` to everyone nearby and remove the formal group. Anyone who participates gets full experience and their own loot. The pool is "whoever is on this map now," which can be large, but map events repeat on a cycle in the same places, so the same regulars can meet at the same event repeatedly. It is a design where co-activity is free and repeat meetings depend on routine, not on a queue.

Four games, one model. Ask of any grouping system, "what is `N`, what is `m`, and does anything let players meet the same people again on purpose?"

### Eyes-open design judgment

- **Choose `N` deliberately.** A large pool gives short queues and zero acquaintances. A small pool gives familiarity and long waits, or no group at all. Neither is correct. Decide which content should build ties (weekly group content, guild activities) and which should just be available (a daily dungeon for someone with 30 minutes).
- **Give players a way to beat the odds.** The model assumes random matching. One button such as "queue again with this group," or a friend request after a good run, breaks the randomness. It turns one lucky pairing into a repeat. This is the cheapest bonding feature a matchmaker can have.
- **Expect to replace reputation with rules.** When repeat encounters fall below a few percent, people who leave early or loot unfairly suffer nothing socially. Deserter penalties, vote kicks and commendations are the rules you will need. They work, but they are blunt, and they create griefing opportunities of their own (week 8).
- **NPC fill-ins remove the social cost and the social benefit.** EverQuest's mercenaries and FFXIV's Duty Support fix the "no group" problem and help newcomers and players on odd schedules. They also mean a player can finish the game without once depending on another person. Decide which content is allowed to be solo-with-NPCs.
- **Forced grouping only builds ties in small pools.** Forcing groups in a huge, matchmade pool gives you the costs of forced grouping (waiting, strangers who leave) with none of the social benefit.

## 4. The shadow of the future

Why does meeting again matter so much? Game theory gives a sharp answer. MMO303 week 10 introduced the prisoner's dilemma. Two players each choose to cooperate (stay in the group, share loot fairly) or defect (leave when it suits them, take the loot). Name the payoffs `T` (temptation, you defect while they cooperate), `R` (reward for mutual cooperation), `P` (punishment for mutual defection) and `S` (sucker's payoff), with `T > R > P > S`. In a single encounter, defecting is always better for you.

Now suppose that after each encounter there is a chance `w` that you will meet the same person again. Axelrod called `w` the **shadow of the future**. A player who always defects against a partner who cooperates first and then copies the last move (tit-for-tat) gets `T` once and then `P` for every later encounter. A cooperator gets `R` every time. Comparing the two expected totals gives the condition for defection to stop paying:

```
w ≥ (T − R) / (T − P)
```

With Axelrod's standard payoffs `T = 5, R = 3, P = 1, S = 0`, the threshold is `(5 − 3) / (5 − 1) = 0.5`. Axelrod's full condition for tit-for-tat to be stable adds a second test, `w ≥ (T − R) / (R − S) = 0.67` with these payoffs, so the practical bar is about two in three.

Compare that with the last column of the table in section 3. In a pool of 60, a partner reappears within your next 20 runs with chance 0.75, above the bar. In a pool of 200, 0.33. In a matchmade pool of thousands, a few percent. **The pool size decides whether cooperation can sustain itself or needs to be enforced.** That is the formal version of the Dungeon Deserter story.

Two cautions. First, `w` here is a crude stand-in. Real players also care about their reputation with third parties (a guild that hears what you did), which raises the effective shadow even with strangers. Week 6 studies reputation systems that try to do this at scale. Second, the prisoner's dilemma is a model of incentives, not of people. Many players cooperate with strangers they will never meet again, because they are decent. Design for the ones who respond to incentives without assuming everyone does.

## 5. A design vocabulary for grouping

Pulling the week together, a grouping system has five knobs.

| Knob | Lowers formation cost `w` | Raises group reward `R_g` | Raises repeat encounters |
|---|---|---|---|
| Solo viability (how good `R_s` is) | — | — | — |
| Group bonus or group-only rewards | No | Yes | No |
| Pool size `N` (local vs cross-server) | Larger `N` lowers `w` | No | Smaller `N` raises it |
| Re-meet tools (requeue together, friend prompts, guild groups) | Slightly | No | Yes |
| NPC fill-ins | Yes | Usually lower | No human ties at all |

Solo viability has no arrows because it is the baseline every other knob is measured against. Two design patterns come out of the table.

**Tiered content.** Give each kind of content its own knob settings. Daily, short content uses a big pool and solo options, so busy players can always play. Weekly or guild content uses small pools or pre-made groups and higher group rewards, so ties form where they are wanted.

**The funnel.** Use big pools to let people meet, and re-meet tools to let them keep the good ones. A matchmaker that makes 80 introductions a month and a button that turns three of them into regular partners gives both bridging (week 1) and a path to bonding.

## In-class activity (25 minutes)

Groups of three. Materials: the interactive and the table in section 3.

1. (5 min) Your game has 3,000 players online at peak on one server. You are designing a weekly 4-player dungeon (`m = 3`). Write down two pool options, "server only, same level band" (estimate `N` yourselves) and "cross-server" (`N = 30,000`).
2. (8 min) For each option, use the interactive with `r = 12` runs (three a week for a month) and `k = 3`. Record distinct people met, acquaintances, and the chance a partner reappears.
3. (7 min) Choose one of the two, or a hybrid (for example, big pool plus "requeue with this group"). Estimate in the interactive what `N` your hybrid behaves like. A hybrid where half your runs repeat a previous group is one you can approximate by halving `r` for strangers.
4. (5 min) State one rule you would need to replace reputation (a deserter penalty, a vote kick, a commendation), and one way players could abuse it.

Expected output: two rows of numbers, a chosen design with one sentence of justification, and one rule with its abuse case.

## Common misconceptions

- **"Matchmaking makes games more social because you meet more people."** It raises distinct people met, which is bridging contact. It almost removes repeat encounters, which is what ties need. Say which one you mean.
- **"Forced grouping builds community."** Only in small pools, where the same people meet again. Forced grouping in a large matchmade pool builds queues and strangers.
- **"Players solo because they are antisocial."** The week 2 census and the grouping rule in section 1 show that players solo when soloing pays better. Change `R_g`, `R_s` or `w` and behavior follows.
- **"A desertion penalty is a sign of a toxic community."** It is a sign of a large pool. Once `w` falls below the cooperation threshold, some enforcement is needed whatever the community is like.

## Check yourself

1. A dungeon queue has a pool of `N = 500` and 5-player groups. A player runs 30 dungeons. Compute `p`, the expected distinct people met, and the number of repeat encounters.
2. In the grouping rule `R_g × (1 − w) > R_s`, soloing gives 100 experience per minute and a group gives 180 once running. What is the largest share of the session formation can take before soloing wins?
3. Use the approximation `r ≈ k × (N − 1) / m` to estimate how many runs a player needs in a pool of 2,000 (5-player groups) to meet a given partner 3 times on average. Is that realistic for a month?
4. With payoffs `T = 6, R = 4, P = 1, S = 0`, what value of `w` does the first condition in section 4 require? Which pool sizes in the section 3 table (20 runs ahead) clear it?
5. A designer wants a matchmade weekly raid for 10 players to build ties. Name two changes to the matchmaker (not to the raid) that raise repeat encounters, and say which symbol in the model each one changes.

<details>
<summary>Answers</summary>

1. `p = 4 / 499 = 0.00802`. `(1 − p)^30 = 0.99198^30 ≈ 0.785`, so `D = 499 × 0.215 ≈ 107.0`. Slots are `4 × 30 = 120`, so repeat encounters are `120 − 107.0 = 13.0`.
2. `180 × (1 − w) > 100` gives `1 − w > 0.556`, so `w < 0.444`. If forming the group takes more than about 44% of the session, soloing wins.
3. `r ≈ 3 × 1,999 / 4 ≈ 1,500` runs. At one run a day that is about four years, so it is not realistic. In practice a player in this pool will almost never meet a random partner three times.
4. `w ≥ (6 − 4) / (6 − 1) = 0.4`. From the table, `N = 60` (0.75) clears it, `N = 200` (0.33) does not, and the larger pools are far below. (The second condition, `(T − R)/(R − S) = 0.5`, raises the bar further.)
5. Examples: restrict the pool to one server or to players with similar schedules, which lowers `N`; add a "keep this raid together next week" option, which replaces random matching for returning members so they meet with chance close to 1 instead of `p`; give priority matching with previous partners, which raises the effective `p` above `m / (N − 1)`.

</details>

## Lab / assignment hook

[Lab 03, simulating strangers](../labs/lab03.md). You will run a seeded Monte Carlo of a matchmaker, check it against the binomial formulas in section 3, then add a "requeue with this group" rule and find the pool size at which a player still makes three acquaintances a month. Deliverable: the script output, one chart and a 300-word recommendation.

## Sources

- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2006). "'Alone Together?' Exploring the Social Dynamics of Massively Multiplayer Online Games." *Proceedings of CHI 2006*, ACM, 407-416. https://doi.org/10.1145/1124772.1124834. Characters who never grouped levelled about twice as fast; grouping below 40% until after level 55 (World of Warcraft, classic era, 2005 data).
- Warcraft Wiki, "Patch 3.3.0" (released December 8, 2009). Cross-realm Dungeon Finder connecting all realms within a battlegroup. https://warcraft.wiki.gg/wiki/Patch_3.3.0
- Warcraft Wiki, "Dungeon Finder" (current page; parts marked out of date). Dungeon Deserter debuff blocks the Dungeon and Raid Finder for 30 minutes after leaving early; vote kick; Looking for Group channel in capital cities; 5-player groups drawn from the battlegroup. https://warcraft.wiki.gg/wiki/Dungeon_Finder
- Wikipedia, "EverQuest" and "EverQuest: Seeds of Destruction" (accessed 29 September 2026). Seeds of Destruction released 21 October 2008 with mercenaries that join groups in place of human players. The "difficulty finding groups" motive is Wikipedia's account; no SOE source was reachable.
- MMO301 week 4 and GS101 week 9 of this program, for EverQuest's group- and raid-centered design (Game Developers Choice Online Awards Hall of Fame, 2011).
- Final Fantasy XIV Online Wiki (consolegameswiki), "Duty Roulette" (current era). "In Need" bonus for the most needed role. https://ffxiv.consolegameswiki.com/wiki/Duty_Roulette
- Final Fantasy XIV Online Wiki, "Duty Finder" and "Duty Support" (current era, patch 7.5). Matching within a data center; tanks and healers tend to get faster queues; Duty Support runs main-scenario dungeons and 4-player trials with NPCs. https://ffxiv.consolegameswiki.com/wiki/Duty_Support
- Guild Wars 2 Wiki, "Dynamic event" (current era). Full experience for every participant without a party; loot per participant; scaling with participants; cyclical events and meta-events. https://wiki.guildwars2.com/wiki/Dynamic_event
- Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books. The shadow of the future and the stability conditions for tit-for-tat in the repeated prisoner's dilemma, with standard payoffs 5, 3, 1, 0.
- Granovetter, M. S. (1973). "The Strength of Weak Ties." *American Journal of Sociology* 78(6), 1360-1380. Tie strength grows with time spent together.
- The pool-size table in section 3 is computed for this lecture from the binomial model with `m = 4`, `r = 20` and `k = 3`. Pool sizes are illustrative and not measurements of any game.

## Interactive spec: examples/w03-reencounter.html

**The one insight.** A bigger matchmaking pool makes you meet more people and meet nobody twice. The left view (distinct people met) rises and looks good. The right view (repeat encounters and acquaintances) collapses between a pool of about 200 and 1,000.

**Model.**

```
p = m / (N − 1)
q = 1 − p
D(N) = (N − 1)(1 − q^r)                          distinct people met
Rep(N) = m r − D(N)                              repeat encounters
A(N) = (N − 1) × (1 − Σ_{j=0}^{k−1} C(r, j) p^j q^(r−j))   acquaintances
again(N) = 1 − q^r                               chance a given partner reappears in the next r runs
```

**Layout.** Two linked charts sharing an x-axis of pool size `N`, log scale from 20 to 50,000.

- **Left, "People you meet."** Line of `D(N)`, with a dashed horizontal line at `m × r` labelled "all partner slots."
- **Right, "People you meet again."** Two lines, `Rep(N)` and `A(N)`, and on a secondary 0-100% axis `again(N)`. A dashed horizontal line on the percent axis at the cooperation threshold `w*` (see controls).
- A vertical cursor at the current `N` in both charts, with a readout table: `p` (4 decimals), `D` (1 decimal), `Rep` (1 decimal, or 2 decimals when below 0.5, so that 0.15 shows), `A` (2 decimals), `again` (percent, 1 decimal).

**Controls.**
- `N` slider (log, 20 to 50,000, default 200), with a numeric input.
- `m` (1 to 9, default 4; label "other players per group").
- `r` (1 to 200, default 20; label "runs").
- `k` (1 to 10, default 3; label "meetings to become an acquaintance").
- Payoffs `T, R, P` (defaults 5, 3, 1) to compute `w* = (T − R)/(T − P)`, shown as the threshold line. Show an error if `T > R > P` fails.
- Preset buttons: "Local zone (N = 60)", "Server band (N = 200)", "Cross-server (N = 5,000)".

**Simulation tab.** Simulate the whole pool of `N` players (round `N` down to a multiple of `m + 1`; cap at 5,000). Each run shuffles the pool and cuts it into groups of `m + 1` (seeded PRNG, seed shown, default 305, "reroll" button). After `r` runs, show a histogram of each player's acquaintance count and each player's distinct-people count, with the formula means drawn as vertical lines. When `N < 1,000`, repeat over 20 seeds and pool the players, so the histogram has at least 1,000 samples. The pooled means must be within 5% of `D` and within 0.3 of `A` (reference, 20 seeds: `N = 60` gives 44.4 and 9.0; `N = 200` gives 66.4 and 1.44). Optional control: requeue share `s` (0 to 1, default 0), the chance a whole group stays together for the next run, matching Lab 03.

**Test values (`m = 4`, `r = 20`, `k = 3`, must match to the shown precision).**
- `N = 60`: `p` 0.0678, `D` 44.5, `Rep` 35.5, `A` 8.87, again 75.4%.
- `N = 200`: `p` 0.0201, `D` 66.4, `Rep` 13.6, `A` 1.43, again 33.4%.
- `N = 1,000`: `p` 0.0040, `D` 77.0, `Rep` 3.0, `A` 0.07, again 7.7%.
- `N = 5,000`: `D` 79.4, `Rep` 0.6, `A` 0.00, again 1.6%.
- `N = 20,000`: `D` 79.8, `Rep` 0.15, `A` 0.00, again 0.4%.
- Default payoffs give `w* = 0.50`.
- Check-yourself value: `N = 500`, `r = 30`: `p` 0.0080, `D` 107.0, `Rep` 13.0.

**Edge cases.** If `m ≥ N − 1`, set `p = 1` and show "everyone is in every group." Use log-space or a stable recurrence for binomial terms when `r` is large.

**Accessibility.** Lines differ by dash pattern and direct labels, not only color. All sliders keyboard-operable with visible focus and live-region readouts. Respect `prefers-reduced-motion` (no animated transitions of the curves) and `prefers-color-scheme`.
