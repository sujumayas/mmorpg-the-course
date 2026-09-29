# MMO306 · Week 10 — Player-Generated Content

**Why this matters:** No studio can write content as fast as a million players eat it, so sooner or later someone proposes letting the players write it. Player-made content can be a game's best source of fresh play or the fastest leak in its economy. Which one you get depends on a few rules you set before the first creator opens the editor: who decides the rewards, how content reaches players, and how many creations can pay out.

**You will be able to:**
- Compute how the best of `N` player-made missions pulls away from the typical one, and predict the reward rate players will actually farm.
- Compare reward caps, server-computed rewards, separate currencies and curated pools by their effect on that best-case rate.
- Design a publication funnel (test gate, review pool, ratings, removal) for a player-content system and estimate how many creations reach the public list.
- Critique a shipped player-content system for where its rewards, curation and moderation rules succeed or leak.

**Before class:** Paragon Wiki (City of Heroes archive), "Mission Architect" and "Issue 14" (about 20 minutes). Neverwinter Wiki, "Foundry", the frequently asked questions (10 minutes). Reread your notes on faucets from MMO304 week 3.

**Prerequisites from earlier courses:** [GD202 week 9, emergent narrative](../../GD202-narrative-and-quest-design/lectures/w09-emergent-narrative.md) (stories players make without an editor; this week is about the ones they make with one). [GD202 week 6, quest anatomy](../../GD202-narrative-and-quest-design/lectures/w06-quest-anatomy-hook-objective-complication-reward.md) (what a quest is made of, which is what your editor must expose). [MMO304 week 3, faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) (a reward is a faucet). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) and [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (waiting times; this lecture introduces its continuous cousin, the exponential distribution, where it is used). From this course, [week 1, the content treadmill](w01-the-content-treadmill-production-vs-consumption.md), for why studios want player content at all.

**Interactive:** [`examples/w10-best-farm.html`](../examples/w10-best-farm.html). Keep it open during section 2.

---

## 1. What players can make, and what it is for

**Player-generated content** (often called user-generated content, or UGC) is anything in the game that a player authored and other players experience. It comes in several forms, and they carry very different risks.

- **Expressive content.** Houses, decorated guild halls, costume designs, emblems. Other players look at it. It rarely pays anyone anything, so it rarely breaks an economy. Its risk is offensive or infringing content.
- **Social content.** Player-run events, roleplay nights, races, tournaments organised by guilds. The game supplies tools (calendars, arenas, chat) and players supply the plan. MMO305 covers the social side.
- **Authored play.** Missions, quests, dungeons or levels built in an editor and played by strangers. This is the form that competes with the studio's own content, and the form this lecture is about.

Authored play is attractive for a simple reason. Week 1 showed that a team spends months building content that players clear in hours. If even 1% of your players build, and each of them builds one hour of play per month, a game with 200,000 players gets 2,000 hours of new play every month, more than any content team ships. The catch is in the words "new play." An hour of player-made content is only worth something if it is fun, if players can find it, and if it doesn't wreck the reward economy you tuned for the studio's content.

Three rules decide which way it goes:

1. **Reward rule.** Who decides what a creation pays, and how much can it pay?
2. **Publication rule.** What must a creation pass before strangers see it, and how is the list sorted?
3. **Moderation rule.** How are harmful or infringing creations found and removed?

This week's worked example takes the first rule, because it breaks first and breaks worst.

## 2. Worked example: the best farm wins

### The hook

City of Heroes launched its Mission Architect in Issue 14, released on 8 April 2009. Players could build missions and story arcs, with their own maps, enemies, objectives and dialogue, and publish them for everyone. Defeating enemies in a player-made mission gave full experience. In place of normal item drops, players earned Tickets, a separate currency spent at special vendors.

Within the system's life the developers had to change it several times to stop players from using it to gain extra rewards. The Paragon Wiki lists the kinds of changes: enemies were altered to give different rewards inside the Architect than outside it, and maps were changed or removed. The editor's limits, such as not letting authors place enemies exactly where they liked, were there on purpose to stop it becoming a power-levelling tool.

Here is the puzzle. Most authors weren't trying to exploit anything. They were writing stories. So why did a system full of honest authors need patch after patch? The answer is that it doesn't matter what the typical author does. Players don't play the typical mission when rewards are on the line. They play the best-paying one, and the best of thousands is far from typical.

### The model

Measure every mission by its **reward rate** relative to studio content: experience (or gold, or items) per minute, divided by what a comparable studio mission pays per minute. A rate of 1.0 means "pays like our content." A rate of 1.3 means 30% more.

Assume each of `N` published missions has a rate

```
r_i = 1 + X_i
```

where `X_i` is how much that mission overpays. Most missions overpay a little, because authors pick enemy mixes that feel good to fight, and a few overpay a lot. The simplest distribution with that shape is the **exponential distribution** with mean `m`: small values are common, large values are rare, and there is no hard ceiling. With `m = 0.10`, the average mission pays 10% over studio rate and the median mission pays about 7% over.

Players seeking rewards play the mission with the largest `r_i`. For exponential `X`, the expected largest of `N` draws has a clean form:

```
E[best rate] = 1 + m × H_N
H_N = 1 + 1/2 + 1/3 + ... + 1/N  ≈  ln N + 0.577
```

- `N` is the number of missions that pay rewards.
- `m` is the mean overpay of one mission, as a share of studio rate.
- `H_N` is the `N`th harmonic number. It grows like the natural logarithm of `N`.

The whole lesson is in `ln N`. The typical mission never changes as the catalogue grows. The best mission keeps climbing, forever, by the same amount each time the catalogue grows tenfold (about `m × 2.3`). The more successful your editor is, the more missions there are, and the more the best one overpays.

### Numbers you can check

With `m = 0.10`:

```python
import math

def harmonic(n):
    return sum(1 / k for k in range(1, n + 1))

m = 0.10   # average bonus over the official rate, as a share of it
median = 1 + m * math.log(2)
print(f"median mission  {median:.3f}x")
for n in (1, 10, 100, 1_000, 10_000, 100_000):
    best = 1 + m * harmonic(n)
    print(f"N={n:>7,}  best mission {best:.3f}x official")
```

It prints:

```
median mission  1.069x
N=      1  best mission 1.100x official
N=     10  best mission 1.293x official
N=    100  best mission 1.519x official
N=  1,000  best mission 1.749x official
N= 10,000  best mission 1.979x official
N=100,000  best mission 2.209x official
```

Check the `N = 10` row by hand. `H_10 = 1 + 0.5 + 0.333 + 0.25 + 0.2 + 0.167 + 0.143 + 0.125 + 0.111 + 0.1 = 2.929`, so the best mission pays `1 + 0.1 × 2.929 = 1.293` times studio rate.

| Missions paying rewards `N` | Median mission | Best mission (expected) | Best vs median |
|---|---|---|---|
| 10 | 1.07× | 1.29× | +21% |
| 1,000 | 1.07× | 1.75× | +64% |
| 10,000 | 1.07× | 1.98× | +85% |
| 100,000 | 1.07× | 2.21× | +107% |

At ten thousand missions, the best one pays almost double what your own content pays, even though the median author is honest and the average overpay is only 10%. Nobody needed to write an exploit. Selection did the work.

The formula is an expected value. A simulation that draws the missions at random agrees:

```python
import random, statistics

def best_of(n, m, rng):
    return 1 + max(rng.expovariate(1 / m) for _ in range(n))

rng = random.Random(306)
for n in (10, 1_000):
    trials = [best_of(n, 0.10, rng) for _ in range(2_000)]
    print(f"N={n:>5,}  simulated mean best {statistics.mean(trials):.3f}x")
```

```
N=   10  simulated mean best 1.296x
N=1,000  simulated mean best 1.746x
```

### What the best farm does to the economy

A reward is a faucet (MMO304 week 3). Suppose a share `φ` of all play time moves to the best mission, which pays `b` times studio rate. Total reward inflow becomes

```
inflow multiplier = 1 + φ × (b − 1)
```

With `φ = 0.3` and `b = 1.98` (the 10,000-mission row), inflow rises by `0.3 × 0.98 = 0.294`, so 29% more experience or gold enters the game than you planned. Levelling speeds up by the same factor, and week 1's content clock runs 29% faster for everyone who farms. The players who don't farm fall behind the ones who do, which pushes more players to farm, which raises `φ`.

### A visual you can move

Open the interactive. The left view is a histogram of all `N` missions' reward rates, drawn from the model. The right view plots the best mission's rate against `N` on a logarithmic axis, with the median as a flat line underneath.

Drag `N` from 10 to 100,000. The histogram barely changes shape; it just gets taller. It looks like a healthy system of mostly fair missions. The right view shows the best-case line climbing steadily away from the median. The left view is what a moderator sees when browsing. The right view is what farmers see. Then turn on the lever toggles (cap, server-computed reward, curated pool) and watch which ones flatten the right-hand line.

### Cross-game recognition

The same selection effect appears wherever players can choose among many creations and one number matters.

**City of Heroes, Mission Architect (Issue 14, April 2009).** Here the chosen number was experience per minute. The developers' answers map onto the model's terms. Replacing drops with Tickets moved part of the reward into a separate currency, so that part of `b` couldn't leak into the main item economy. Leaving out the end-of-mission experience bonus lowered `m`. Changing how custom enemies paid out inside the Architect attacked the tail of `X` directly. The Developer's Choice designation let chosen arcs pay normal rewards, which is a small curated pool.

**Neverwinter, the Foundry (2013 onward).** Cryptic Studios, which had built the original City of Heroes, took the reward decision away from authors. The Neverwinter Wiki's Foundry FAQ lists the limits: rewards and loot are generated by the game engine, not the author, each quest gets one end-of-quest chest, random treasure chests and skill-based resource nodes are unavailable, and each map may have only one respawn campfire. In the model, that is an attempt to make `X` close to zero for every mission, so the best is barely above the median. A daily quest that paid extra for playing Foundry quests existed until September 2015 and required each quest to be eligible for rewards, which again restricted the pool that paid.

**Super Mario Maker (Wii U, 2015).** Levels pay no reward, so no one farms a best level for gain. The same selection shows up in a different number, difficulty. Players browsing the most-starred or hardest courses meet the extreme tail, not the typical course. The game's 100 Mario Challenge sorts courses into difficulty bands by clear rate, so the game controls which part of the distribution a player sees. With no reward attached, the extremes are entertainment rather than an exploit.

Three systems, one model. When players choose from `N` creations by a number, the number you get is the maximum, not the average. City of Heroes fought the tail after launch. Neverwinter tried to remove it by design. Super Mario Maker had no reward in the number, so its tail became a feature.

### Eyes-open design judgment

You have four levers. Each one flattens the best-case curve and each has a cost.

| Lever | What it does in the model | Best rate at `N = 10,000`, `m = 0.10` | Cost |
|---|---|---|---|
| None | — | 1.98× | Economy leaks, farming crowds out stories |
| Hard cap at 1.2× | `best = min(1 + m H_N, cap)` | 1.20× | Farmers still find the cap and sit on it; every creation near the cap looks the same |
| Server-computed reward (`m` cut to 0.02) | Shrinks the whole tail | 1.20× | Authors lose control of pacing and payoff; the server must measure difficulty honestly |
| Curated pool of 50 paying missions | `N` cut to 50 for rewards | 1.45× | Most creators get no rewards for their players, so fewer players try them |
| Separate currency (tickets) | Moves the leak to a closed shop | 1.98× in tickets | You must design and police a second economy |

Check the server-computed row: `1 + 0.02 × H_10,000 = 1 + 0.02 × 9.788 = 1.196`. Check the curated row: `H_50 = 4.499`, so `1 + 0.1 × 4.499 = 1.45`.

Some judgments that follow:

- **Decide what player content is for.** If it is for stories, pay a flat, low reward per minute of play regardless of content, and let authors compete on fun. If it is for progression, the server must price every enemy and objective, and authors become level designers inside your budget.
- **Price on measured outcomes, not on configuration.** A reward computed from what actually happened (time spent, damage taken, enemies of each tier defeated, deaths) is harder to game than one computed from what the author placed. City of Heroes' change to custom enemy payouts is a move in this direction.
- **Treat the cap as the real rate.** If you set a cap, assume farmers will sit exactly on it. Tune the economy as if every farming player earns the cap.
- **Watch the tail, not the mean.** Your dashboard should show the top ten missions by reward per minute, not the average. The average will look fine until long after the economy has moved.

### Check yourself (worked example)

1. With `m = 0.05`, what is the expected best reward rate at `N = 1,000`? Compare it with `m = 0.10`.
2. A team caps the reward at 1.5× and publishes 100 paying missions with `m = 0.10`. Does the cap bind? What if they publish 10,000?
3. With `φ = 0.2` of play time on the best mission at 1.75×, by how much does reward inflow rise?

<details>
<summary>Answers</summary>

1. `1 + 0.05 × 7.485 = 1.374`. Halving `m` halves the overpay at every `N` (0.749 becomes 0.374).
2. At `N = 100` the expected best is 1.519, just over 1.5, so the cap binds narrowly. At 10,000 it is 1.979, and the cap binds hard; the best mission earns exactly 1.5×.
3. `1 + 0.2 × 0.75 = 1.15`, so 15% more.

</details>

## 3. The publication funnel

Rewards decide what players farm. Publication decides what players find. A system with 100,000 creations and a list sorted by date shows everyone the newest, mostly untested ones. A system sorted by rating shows everyone the same twenty, and new authors never get a player.

A **publication funnel** is the sequence of gates a creation passes on its way to strangers. Shipped systems use a small set of gates.

- **Proof of completion.** Super Mario Maker required a creator to be able to complete their own course before sharing it online. One rule removes every impossible level, because the creator has shown it can be done.
- **A reviewer pool.** Neverwinter's Foundry kept new quests off the general catalogue until they met minimum criteria, such as average play time and a minimum number of star ratings. Until then, only players who opted in as Foundry reviewers saw them. Volunteers take the risk of playing untested content, and everyone else sees work that has been through them.
- **Upload limits earned by quality.** Super Mario Maker started players with 10 upload slots and gave more as their courses earned stars.
- **Removal of the unplayed.** Super Mario Maker could remove courses that went a set time without a single star. The catalogue stays smaller, and search stays useful.
- **Report-driven hiding.** City of Heroes automatically hid heavily reported arcs from search, and a banned arc kept taking up one of its author's slots until a moderator re-evaluated it. The penalty lands on the author's future capacity, which gives authors a reason to care.

You can estimate a funnel's output with multiplication. Suppose 5,000 creations are submitted in a month, 60% pass a completion check, 30% of those get enough reviewer plays to be rated, and 40% of the rated ones clear the rating bar. The public list gains `5,000 × 0.6 × 0.3 × 0.4 = 360` creations a month. That is a manageable list. It is also 4,640 creations whose authors got little or no audience, and author motivation is the resource that keeps the system running. The lab asks you to design a funnel for a target list size and then count who pays for it.

Two rules help authors. Give every new creation a guaranteed small audience (for example, a slot in a "new and rising" list for a few days) before the rating bar applies. And show authors their numbers: plays, completion rate, where players quit. Neverwinter's Dungeon Master ranks (titles first, later capes, companions and mounts) and City of Heroes' Hall of Fame and Developer's Choice designations rewarded authors for being played. That gives creators a reason to build that doesn't depend on how much their missions pay players.

## 4. Moderation and ownership

Player-made content brings two problems studio content doesn't have.

**Harmful content.** Every free-text field (mission titles, dialogue, signs in a player house) will be used for slurs, harassment, spam and advertising for gold sellers. Your pipeline needs a filter at submission, a report button on every creation, and a moderator queue. Report-driven auto-hiding, as in City of Heroes, is cheap and fast, but it can be abused by groups reporting a rival's work, so hidden content should go to a human, not straight to deletion. [MMO305 week 12](../../MMO305-social-systems-and-online-behaviour/lectures/w12-community-management.md) covers the community team that runs such a queue, and [MMO305 week 8](../../MMO305-social-systems-and-online-behaviour/lectures/w08-griefing-typology-and-design-responses.md) the griefing it has to handle.

**Infringing content.** Players will rebuild famous characters, levels and stories. Your terms of service need to say who owns a creation and what happens when a rights holder complains. Super Mario Maker prevented players from re-uploading a downloaded and altered copy of someone else's course, which protects authors from each other as well.

**Exploits by construction.** A player editor is a tool for building situations your designers never tested. Every editor option multiplies the space of possible missions. The Foundry's limits on campfires and chests, and City of Heroes' restriction on exact enemy placement, both remove options that made exploits easy to build. Your editor's feature list is also its exploit surface, so review each option with "what is the most profitable thing someone can build with this?" MMO309 week 1 teaches the threat-modelling method for that question: [threat modeling for games](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w01-threat-modeling-for-games.md).

## 5. When to build a player-content system at all

A player-content editor is a large, permanent project. It needs its own tools team, moderators, discovery features and economy rules, and it is never finished. Before you build one, ask:

- **Is your bottleneck content, or content your players want?** If players leave because they have nothing to do at the level cap, player missions might help. If they leave because the class balance is bad, they won't.
- **Can your editor produce your game's best experience?** If your best content depends on voiced cinematics, bespoke boss scripts and custom art, player missions will feel like a lesser version. Player content fits games whose core pleasure comes from combining existing pieces.
- **Can you afford the moderation?** Estimate submissions per month and minutes per review. At 5,000 submissions and 3 minutes of human time for each flagged one, flagging 10% costs 25 hours a month. Flagging 50% costs 125.
- **What happens when you turn it off?** Player content lives on your servers. If the system is removed, your authors lose their work. Decide in advance whether you will offer an export.

## In-class activity (25 minutes)

In groups of three, design the reward and publication rules for a player-made dungeon system in an MMO with 300,000 monthly players.

1. **(5 min)** Choose a purpose: stories, progression, or both. Write it in one sentence.
2. **(8 min)** Choose a reward rule. Estimate `m` for your rule and the number of paying dungeons `N` after a year. Compute the expected best rate. If it exceeds 1.25×, change a lever until it doesn't, and write down the cost of that lever.
3. **(7 min)** Design a funnel with at least three gates. Estimate the rate of each and the number of dungeons reaching the public list per month from 3,000 submissions.
4. **(5 min)** Swap with another group. Find the most profitable dungeon someone could build under their rules.

Expected output: purpose sentence, reward rule with `m`, `N` and best rate, funnel with numbers, and the exploit the other group found.

## Common misconceptions

- **"Most authors are honest, so the reward system is safe."** Farmers don't play the typical mission. The best of `N` sets the real rate, and it grows with `ln N` even when every author is honest.
- **"A reward cap solves it."** A cap sets the rate farmers will earn. You must tune the economy as if farming players earn exactly the cap, all the time.
- **"More creations means more good content for players."** Only if they can be found. Without a funnel, a larger catalogue is harder to search, and new authors never reach an audience.
- **"Player content is free content."** It costs a tools team, moderators, discovery features and a second set of economy rules, for as long as the system runs.

## Check yourself

1. A player-mission system has `m = 0.08` and 5,000 paying missions. What is the expected best rate? (Use `H_5,000 ≈ 9.09`.)
2. The team wants the expected best to stay under 1.3× at `N = 5,000` without a cap. What `m` must the server-side reward rule achieve?
3. A curated pool is proposed instead: only featured missions pay, and `m` stays 0.08. How large can the pool be while the best stays under 1.3×? (Use `H_N ≈ ln N + 0.577`.)
4. A funnel receives 8,000 submissions. 50% pass a completion test, 25% of those get enough reviewer plays, and 50% of those clear the rating bar. How many reach the public list? What share of authors never reach it?
5. Why did Super Mario Maker's extreme courses not cause the problem City of Heroes had? Answer in terms of the model.

<details>
<summary>Answers</summary>

1. `1 + 0.08 × 9.09 = 1.727`, about 1.73×.
2. `m × 9.09 < 0.3`, so `m < 0.033`.
3. `0.08 × H_N < 0.3` means `H_N < 3.75`, so `ln N < 3.173` and `N < 23.9`. About 23 missions.
4. `8,000 × 0.5 × 0.25 × 0.5 = 500` reach the list. `7,500 / 8,000 = 93.75%` of authors don't.
5. The number players selected on (difficulty, stars) carried no reward, so the maximum of `N` didn't feed into any faucet. The tail was still there, but it was entertainment. City of Heroes attached experience to the number, so the tail became a faucet.

</details>

## Lab / assignment hook

[Lab 10, the best-farm simulator](../labs/lab10.md). You implement the best-of-`N` model, test it against simulation for the exponential and one other distribution, compare the four levers at your own `N`, and design a publication funnel for a target list size. This feeds the encounter designs assignment if your dungeon includes a player-content layer.

## Sources

- Paragon Wiki (City of Heroes archive), "Issue 14" (accessed September 2026), https://archive.paragonwiki.com/wiki/Issue_14. Issue 14 "Architect" released to live servers on 8 April 2009; closed beta from 17 February 2009.
- Paragon Wiki (City of Heroes archive), "Mission Architect" (accessed September 2026), https://archive.paragonwiki.com/wiki/Mission_Architect. Full experience for defeats in player content; Tickets in place of drops and the end-of-mission experience bonus; Developer's Choice arcs may use standard rewards; limits on enemy placement to prevent power levelling; changes made several times to curb exploits, including different enemy rewards inside the Architect and changed or removed maps; heavily reported arcs auto-hidden from search; banned arcs occupy a slot until re-evaluated.
- Neverwinter Wiki (Fandom), "Foundry" (read September 2026), https://neverwinter.fandom.com/wiki/Foundry. Rewards generated by the game engine, not the author; one end-of-quest chest; one respawn campfire per map; no random chests or skill nodes; catalogue listing requires minimum average play time and ratings, with opt-in reviewers seeing new quests first; "Daily Foundry Quests" for astral diamonds removed in September 2015 (the wiki gives no patch or Cryptic source); Dungeon Master ranks.
- Super Mario Wiki, "Super Mario Maker" (accessed September 2026), https://www.mariowiki.com/Super_Mario_Maker. Players must be able to complete a course to share it; 10 upload slots at first, more earned through stars; courses without a star within a set time may be removed; altered downloads cannot be re-uploaded; 100 Mario Challenge difficulty chosen by clear percentage; uploads ended 31 March 2021.
- Wikipedia, "Neverwinter (video game)" and "City of Heroes" (accessed September 2026). Neverwinter developed by Cryptic Studios, released 20 June 2013; City of Heroes developed first by Cryptic Studios (2004), later by Paragon Studios.
- The harmonic-number result for the expected maximum of exponential variables is standard; see any probability text on order statistics (for example Ross, *A First Course in Probability*, the chapter on order statistics). You can also check it by simulation with the MA102 week 11 Monte Carlo method.

## Interactive spec: examples/w10-best-farm.html

**Insight the visual must make obvious:** as the number of missions grows, the distribution of reward rates looks the same, but the best mission keeps climbing away from the median. The left view (what a moderator browsing sees) looks harmless; the right view (what a farmer sees) shows the leak.

**Layout.** Two linked panels side by side on desktop, stacked on mobile (histogram first).

- **Left panel, "All missions."** Histogram of `N` simulated reward rates `r = 1 + X`, `X ~ Exponential(mean m)`, bins of width 0.05 from 1.0 to 3.0 (last bin catches everything above). Y axis is count. Draw the median as a vertical ink line labelled with its value and the maximum as a vertical blood-red line labelled "best". For `N > 5,000`, simulate 5,000 missions and scale bar heights by `N / 5,000` so the page stays fast, but compute the "best" marker by a direct draw of the max: `max = m × (−ln(1 − U^(1/N)))` for one uniform `U`, which samples the maximum of `N` exponentials exactly.
- **Right panel, "Best mission vs catalogue size."** X axis `N` on a log scale from 1 to 100,000. Plot `1 + m × H_N` as a blood-red curve (expected best), `1 + m ln 2` as a flat ink line (median), and a dot at the current `N` showing the most recent simulated best. If the cap is on, draw it as a steel horizontal line and clip the curve to it. If the curated pool is on, show a ochre marker at `N_pool` and the flat value `1 + m × H_{N_pool}` extended as a dashed line to the right.

**Controls (all keyboard reachable, labelled):**
- `N` slider, log-scaled, snapping to 1, 10, 30, 100, 300, 1,000, 3,000, 10,000, 30,000, 100,000. Default 10,000.
- `m` slider, 0.01 to 0.30, step 0.01. Default 0.10.
- Toggle "Server-computed reward": when on, `m` used by the model becomes `m_server` (slider 0.00 to 0.10, default 0.02).
- Toggle "Cap": when on, cap slider 1.0 to 2.0, step 0.05, default 1.20. The best is `min(best, cap)`.
- Toggle "Curated pool": when on, pool slider 1 to 500, default 50. The paying `N` becomes `min(N, pool)`.
- Button "Redraw missions" (new random seed).

**Readouts next to the visual:** median rate, expected best `1 + m H_N`, simulated best, and "farmers earn X% more than your content" = `(best − 1) × 100`. Also the inflow multiplier `1 + φ(best − 1)` with a `φ` slider from 0 to 0.5 (default 0.3).

**Test values (must match exactly, three decimals):**
- `m = 0.10`: `N = 1` gives 1.100; `N = 10` gives 1.293; `N = 100` gives 1.519; `N = 1,000` gives 1.749; `N = 10,000` gives 1.979; `N = 100,000` gives 2.209. Median 1.069.
- Server-computed `m = 0.02`, `N = 10,000`: 1.196.
- Curated pool 50, `m = 0.10`: 1.450.
- Cap 1.20, `N = 10,000`, `m = 0.10`: 1.200.
- `φ = 0.3`, best 1.979: inflow multiplier 1.294.

Compute `H_N` exactly by summation for `N ≤ 100,000`. Use a seeded PRNG so "Redraw" is reproducible within a session. Palette from `templates/interactive-tokens.css`: missions in steel, best in blood, median in ink, cap in steel, curated pool in ochre. No game names or art in the drawing; label it "player-made missions."
