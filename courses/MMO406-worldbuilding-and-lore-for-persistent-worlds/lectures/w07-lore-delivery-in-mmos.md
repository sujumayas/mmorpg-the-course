# MMO406 · Week 07 — Lore Delivery in MMOs

**Why this matters:** In a single-player game, the story reaches every player who gets that far. In an MMO the story ships in patches over years, and the people playing today are not the people who were there when a chapter came out. Every piece of lore you deliver has a shelf life in your population. If you don't plan for it, your next expansion will be written for an audience that has mostly left.

**You will be able to:**
- Compute the share of today's players who experienced a story beat, from its first-week reach, the monthly churn rate and the chance that a newcomer still meets it.
- Derive the half-life of a time-limited story beat and the newcomer reach a beat needs to stay above a knowledge target.
- Classify a shipped MMO's lore channels by permanence (temporary, replaced, gated, permanent) and predict what each does to shared knowledge.
- Design an "assumed knowledge" rule for an expansion: which past beats the new content may take for granted and which it must retell.

**Before class:** Wolf, *Building Imaginary Worlds* (2012), chapter 6, "Transmedial Growth and Adaptation," the opening pages on how a world is entered through different works (use the contents page, about 15 pages). Guild Wars 2 Wiki, "Living World Season 1" (the introduction and release history, 10 minutes). Reread [GD202 week 10](../../GD202-narrative-and-quest-design/lectures/w10-lore-delivery-without-walls-of-text.md), sections 2 and 4.

**Prerequisites from earlier courses:** [GD202 week 10, lore delivery without walls of text](../../GD202-narrative-and-quest-design/lectures/w10-lore-delivery-without-walls-of-text.md) (the reading-decay model and the table of delivery channels; we use both and do not repeat them). [GD201 week 8, environmental storytelling](../../GD201-level-and-world-design/lectures/w08-environmental-storytelling.md) (clue reliability inside one space). [GD202 week 8, quest chains and zone storytelling](../../GD202-narrative-and-quest-design/lectures/w08-quest-chains-and-zone-storytelling.md) (order control inside a zone). [MMO308 week 3, cohorts and retention curves](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md) (what a churn rate measures). [MMO301 week 12, persistence and time](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w12-persistence-and-time-what-should-last.md) (deciding what lasts). This course: [week 4, history and timelines](w04-history-and-timelines.md) (the lore clock and the time gap a new player feels).

**Interactive:** [examples/w07-lore-memory.html](../examples/w07-lore-memory.html). Keep it open during section 2.

---

## 1. The three audiences of MMO lore

GD202 week 10 asked how much of a text one player reads. That is the right question for a single scene. In an MMO you need a second question on top of it. **Who is still around who read it?**

An MMO's story reaches three audiences, and each meets it on a different clock.

- **The live audience** plays a chapter in the weeks it comes out. They see the cinematic, do the quests while the forums argue about them, and remember where they were when the city fell.
- **The catch-up audience** arrives later. They join in year three, or return after a two-year break, and meet the chapter (if they meet it at all) in whatever form it now has in the game.
- **The relay audience** never plays the chapter. They learn it from a wiki page, a guildmate's summary or a lore video. You don't control this channel, but it is often where most of your population gets its lore.

A single-player writer can treat these as one audience, because the game on the disc is the same for all of them. An MMO writer cannot, because the game changes under the player. Content is added, replaced, removed and rearranged. Every chapter you ship has a **permanence**, a rule for whether and how later players can reach it.

Four permanence classes cover almost every case.

| Class | What happens after the release window | Typical form |
|---|---|---|
| Temporary | Gone. Nobody who arrives later can play it. | One-off live events, limited-time story installments |
| Replaced | The zone or quest is rebuilt; the old version is gone and a new one tells a different story | A world revamp, a rebuilt starting zone |
| Gated | Still in the game but behind a condition (a purchase, a login during the window, an optional menu) | Paid episode unlocks, optional campaigns |
| Permanent | Still in the game and on the main path | A required story chain |

A **story beat** here is one piece of story you want players to know: "the admiral betrayed the fleet," "the capital burned," "the dragon is not dead." Permanence is a property of how a beat was delivered, not of the beat. The same beat can be temporary in a live event and permanent in a retold cutscene added a year later. That gap is the one this lecture is about.

### Why an MMO forgets

Your population is not a fixed set of people. Every month some players leave and others arrive. Analysts call the leaving rate **churn**, the share of active players in one month who are gone the next. MMO308 week 3 showed how to read churn from a retention curve. For this lecture you need only one fact about it. **Churn works on your lore too.** A player who saw the city burn and then quits takes that memory with them, and the newcomer who replaces them has not seen it unless the game still shows it.

This is not the same problem as players skipping text. A player who skipped the text never knew. A player who left knew, but no longer counts. The first is a writing problem. The second is a delivery-permanence problem, and writing better does nothing for it.

## 2. Worked example: who still knows?

### The hook

Guild Wars 2's first season of Living World ran from January 2013 to March 2014 in temporary installments, released roughly every two weeks. It introduced a major villain, Scarlet Briar, and ended with her attack on Lion's Arch, the game's central hub city, and the Battle for Lion's Arch. The story changed the capital that every player passed through.

Then it was gone. Unlike the seasons that followed, most of Season 1 could not be played by anyone who arrived later. For eight years, new players walked through a city whose destruction they had never seen, and later chapters referred to events they could only read about. On 22 March 2022 ArenaNet announced that key moments would be re-released as replayable episodes, starting on 19 April 2022, free for all players.

[MMO306 week 13](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w13-content-budgets-and-cadence-planning.md) used this season to count the teams a two-week cadence needs. Here the question is what happened to the story afterwards.

Here is the puzzle. In March 2014 the Battle for Lion's Arch was the most-played story in the game. Almost everyone active knew what happened to the city. How can a beat that nearly everyone saw become a beat that almost nobody in the population has seen, without a single player forgetting anything?

### The model

Take a population that stays the same size. Each month a share `c` of active players leave, and the same number of newcomers arrive. A story beat ships at month 0.

```
s     = 1 − c                        monthly survival of a player
K(m)  = a × s^m  +  r × (1 − s^m)    share of month-m players who know the beat
K(∞)  = r                            long-run share
t½    = ln 2 / (−ln s)               half-life of the release cohort, in months
```

- `m` is months since the beat shipped.
- `c` is monthly churn. `s = 1 − c` is the chance a player active this month is still active next month.
- `a` is the **live reach**, the share of players active at month 0 who experienced the beat in its release window.
- `r` is the **catch-up reach**, the chance that a player who arrives later meets the beat. For a temporary beat, `r = 0`. For a beat on the required main story, `r` is close to 1.
- `K(m)` is the **knowledge share**, the share of the population at month `m` who experienced the beat first-hand.

Read the formula as two groups. `s^m` is the share of today's players who were already here at month 0. Of those, a share `a` saw the beat. The rest of today's players, `1 − s^m`, arrived later, and a share `r` of them met the beat afterwards. Add the two and you have `K(m)`.

The formula assumes a newcomer who meets the beat does so soon after arriving, and that churn is the same for everyone. Neither is exactly true. Section 3 and the lab come back to both. The simple version is enough to see the shape of the problem, and every number in it can be checked by hand.

### Numbers you can check

Take a beat with live reach `a = 0.8` in a game with 10% monthly churn, so `s = 0.9`. The half-life of the release cohort is `ln 2 / −ln 0.9 = 0.693 / 0.105 = 6.6` months. Half the people who were there on release day are gone after six and a half months.

Now compare three permanence choices.

| Months since release | `s^m` (still here from month 0) | Temporary, `r = 0` | Gated, `r = 0.3` | Main story, `r = 0.9` |
|---|---|---|---|---|
| 0 | 1.000 | 80.0% | 80.0% | 80.0% |
| 3 | 0.729 | 58.3% | 66.5% | 82.7% |
| 6 | 0.531 | 42.5% | 56.6% | 84.7% |
| 12 | 0.282 | 22.6% | 44.1% | 87.2% |
| 24 | 0.080 | 6.4% | 34.0% | 89.2% |
| 36 | 0.023 | 1.8% | 31.1% | 89.8% |

Check the 12-month row by hand. `0.9^12 = 0.2824`. Temporary: `0.8 × 0.2824 = 0.226`. Gated: `0.8 × 0.2824 + 0.3 × 0.7176 = 0.226 + 0.215 = 0.441`. Main story: `0.226 + 0.9 × 0.7176 = 0.226 + 0.646 = 0.872`.

Three things stand out.

First, the temporary beat falls to a quarter of its release-day share in a year, and to almost nothing by year three. No player forgot anything. The population was replaced around the memory.

Second, every column converges to its own `r`. Live reach decides the first few months. Catch-up reach decides everything after. **After two half-lives, how you delivered a beat matters more than how many people saw it at launch.**

Third, the main-story column goes *up*. A beat that newcomers meet more often than the live audience did (because `r = 0.9 > a = 0.8`) becomes better known over time. A required chain is the only delivery that can do that.

You can reproduce the table in a few lines.

```python
import math

def knowledge(a, c, r, m):
    s = 1 - c
    return a * s**m + r * (1 - s**m)

print(f"half-life {math.log(2) / -math.log(0.9):.1f} months")
for m in (0, 3, 6, 12, 24, 36):
    row = [knowledge(0.8, 0.10, r, m) for r in (0.0, 0.3, 0.9)]
    print(m, " ".join(f"{100 * k:5.1f}%" for k in row))
```

```
half-life 6.6 months
0  80.0%  80.0%  80.0%
3  58.3%  66.5%  82.7%
6  42.5%  56.6%  84.7%
12  22.6%  44.1%  87.2%
24   6.4%  34.0%  89.2%
36   1.8%  31.1%  89.8%
```

### Turning it around: how much catch-up reach do you need?

Suppose your writers want next year's expansion to open with a scene that assumes players know the beat. You set a target. At least half the population, `K* = 0.5`, should have experienced it first-hand 12 months after release. Solve `K(M) = K*` for `r`:

```
r = (K* − a × s^M) / (1 − s^M)
```

With `a = 0.8`, `s = 0.9`, `M = 12`: `r = (0.5 − 0.226) / 0.718 = 0.38`. Some 38% of newcomers must still find the beat. At `M = 24` the same target needs `r = 0.47`, because by then almost everyone is a newcomer and the live audience barely counts.

A temporary beat can never meet that target past about 4.5 months, since `K(m) = 0.8 × 0.9^m` falls below 0.5 at `m = 4.5`. No amount of live-event polish changes that. The only levers that move `K` in year two are `r` and `c`.

### A visual you can move

Open [`w07-lore-memory.html`](../examples/w07-lore-memory.html). The left chart shows the knowledge share over 36 months for the permanence choice you pick, with the release-day figure as a flat dashed line. That dashed line is what a team sees in its launch-week report. The right panel shows today's population as a bar, split into four groups: veterans who saw it, veterans who didn't, newcomers who found it, newcomers who didn't. Drag the month slider. The dashed line says 80%. The bar fills with newcomers who never saw anything. Then raise `r` and watch the newcomer half of the bar change color.

### Cross-game recognition

Each case below is one choice of `r`, often made for reasons that had nothing to do with story.

**Guild Wars 2, Living World Season 1 (January 2013 to March 2014) and Season 2 (July 2014 to January 2015).** Season 1 was temporary, `r = 0`, until the 2022 re-release raised `r` for everyone who arrived after April 2022. Season 2 changed the rule. Each episode unlocked for free for anyone who logged in during its roughly two-week window, and anyone else could buy it for 200 gems. That is a gated beat. Its `r` is the share of newcomers who pay or who were given it in a later promotion. ArenaNet made Season 2 free again during "Spotlight Weeks" in May and June 2021, which is a temporary jump in `r`.

**World of Warcraft, the Cataclysm revamp (patch 4.0.3a, November 2010) and Chromie Time (patch 9.0.1, October 2020).** Patch 4.0.3a rebuilt the original continents with thousands of new quests. The original zone stories were replaced, which sets `r = 0` for the old versions and starts a new beat with its own `a` and `r`. Ten years later, Chromie Time let players choose which expansion's campaign to level through. That raised `r` for older expansion stories that newcomers had previously skipped on the way to current content.

**Final Fantasy XIV (A Realm Reborn onward).** The Main Scenario quest chain is required to unlock much of the game, and past patches' story stays in it. That is the main-story column, `r` near 1. Square Enix also sells story-skip items, which lower `r` for buyers, and the in-game furnishing the Unending Journey (patch 3.1) lets players rewatch cutscenes of quests they have completed. The skip moves players out of the "found it" group. The rewatch item helps those already in it to refresh.

**Destiny 2, the Destiny Content Vault (10 November 2020).** With the Beyond Light expansion, Bungie removed five destinations, their campaigns and the first Destiny's content from the game. Every beat told only in those campaigns went from gated or permanent to temporary in a day. MMO308 week 14 treats the same decision as a sunsetting problem. In this model it is a step change in `r` to zero, and `K` then decays at the churn rate.

Four games, four delivery policies, one curve. When you read about a game's story updates, ask two questions. What was `a`? What is `r` now?

### Eyes-open design judgment

The model argues for permanence. A designer should not follow it by reflex.

- **Strength of temporary delivery.** It creates the shared moment. Players who were there for the Battle for Lion's Arch share a memory that newcomers can't buy, which MMO304 calls hedonic and social value. A temporary beat can be worth doing *because* `r = 0`.
- **Cost of temporary delivery.** The beat stops being usable as a foundation. Later content that depends on it must retell it.
- **Strength of permanent delivery.** Knowledge share stays high, so later expansions can build on it.
- **Cost of permanent delivery.** Every permanent chapter lengthens the path a newcomer walks before reaching the present. FFXIV sells skips for a reason. A main story with ten years of chapters asks a newcomer for hundreds of hours, and churn rises among players stuck in it. In the model, forcing `r` up can raise `c`.
- **Gating is a price.** A gated beat has an `r` you set with a price, a login rule or a menu. Setting it is a business decision that is also a story decision. Say so in the design review.
- **Decide deliberately:** which beats are **foundations** (later content depends on them) and which are **moments** (their value is having been there). Foundations need high `r`. Moments can be temporary. Delivering a foundation as a moment is the mistake behind most "what happened to the city?" forum threads.

### Check yourself (worked example)

1. A beat reaches `a = 0.6` of the live audience. Churn is 5% a month. What is its half-life, and what share knows it after 12 months if it is temporary?
2. Same beat, but newcomers find it with `r = 0.5`. What share knows it after 24 months? Is that above or below the release-day share?

<details>
<summary>Answers</summary>

1. `s = 0.95`, half-life `0.693 / 0.0513 = 13.5` months. `K(12) = 0.6 × 0.95^12 = 0.6 × 0.540 = 0.324`, about 32%.
2. `0.95^24 = 0.292`. `K(24) = 0.6 × 0.292 + 0.5 × 0.708 = 0.175 + 0.354 = 0.529`, about 53%. That is below the 60% release-day share, since `r < a`, and the curve drifts from 60% down toward 50%.

</details>

## 3. Where the simple model breaks

The model has two assumptions you should question before trusting its numbers.

**Churn is not the same for everyone.** MMO308 week 3 showed that retention curves mix short-stay players, who leave in the first weeks, with long-stay players, who churn slowly. The live audience of a mid-expansion story patch is mostly long-stay players, because short-stay players have already left by the time a patch ships. So the release cohort decays more slowly than the average churn rate suggests, and your temporary beat lasts longer than the simple table says. Lab 07 builds the two-group version and measures how much.

**Newcomers meet beats late, or in the wrong order.** The model assumes a newcomer who meets a beat does so right away. In a long main story, a newcomer may take months to reach a chapter from year two, and many leave before they do. That makes the effective `r` for late chapters lower than the share of players who *eventually* reach them. In a game with a required chain, measure `r` per chapter, not for the story as a whole.

A third breakage is harder to model. **Relay knowledge is not first-hand knowledge.** A player who read a wiki summary of the Battle for Lion's Arch knows the fact. They don't have the memory. For planning your next expansion, the distinction matters in both directions. A fact from the wiki is enough for a line of dialogue to make sense. It is not enough for a scene whose payoff is "you were there." Keep two numbers in mind, `K` for first-hand experience and a larger, fuzzier figure for "has heard of it."

## 4. The lore delivery stack in an MMO

GD202 week 10 listed the channels one scene can use: quest dialogue, barks, item text, notes, audio logs, environment, codex entries and names. An MMO adds channels with their own permanence. Here they are, ordered by roughly how high their `r` tends to be.

| Channel | Example | Typical permanence | Typical `r` |
|---|---|---|---|
| World geometry and names | A ruined district, a renamed city | Permanent until the zone is rebuilt | Near 1 for "something happened," low for "what happened" |
| Required story chain | Main scenario, class story | Permanent | High, falls for late chapters |
| Optional story chain | Side campaign, replayable episode | Gated | Low to medium |
| Journal, codex, rewatch | In-game encyclopedia, cutscene replay | Permanent | Low, but it reaches exactly the players who care |
| Limited-time event | Invasion, festival arc | Temporary | Zero |
| Out-of-game media | Short stories, comics, trailers | Permanent outside the game | Low, and outside your telemetry |
| Community relay | Wikis, lore videos, guild chat | Outside your control | Often the largest by reach, second-hand only |

The first row deserves attention. When Lion's Arch was destroyed, the city itself carried the beat. Every newcomer could see that *something* had happened, even if they could not play it. World geometry has the highest `r` of any channel, because nobody can skip walking through a city. Its weakness is that it shows the result, not the cause. GD201 week 8 gives you the tools to make a ruin readable. A readable ruin raises `r` for "what happened" too.

### The assumed-knowledge rule

Every expansion script relies on the player knowing some past beats. Make that list explicit. For each beat the new content depends on, write:

1. **The beat** in one sentence.
2. **Its delivery and permanence** today.
3. **Its predicted `K`** at the new content's release date, from the model.
4. **The assumption the new content makes**: none, "has heard of it," or "was there."
5. **The action**, if `K` is below the threshold you set for that assumption. Retell it (a recap scene, a companion who explains), re-release it (raise `r`), or rewrite the new content so it doesn't depend on it.

A workable default threshold is `K ≥ 0.5` for "was there" assumptions, with a one-line in-scene retelling for anything below. You will argue about the number in your team. That argument is the point. Without the rule, every writer quietly assumes the audience remembers everything the writer remembers.

### Recaps are cheap `r`

A retelling scene raises second-hand knowledge for everyone who plays the new content, at the cost of a few lines. It does not raise first-hand `K`. The best recaps do three things. They put the need-to-know sentence first (GD202 week 10's reading-decay model applies in full). They come from a character with a reason to talk about it. And they point to the place where the player can experience the original, if it still exists. That last step turns a recap into a channel that raises `r`.

Series television solved this long ago with "previously on." MMOs keep reinventing it. Build it into your content template so each chapter ships with its own one-paragraph recap and a flag for whether the original is still playable.

## 5. Writing lore for a population that turns over

Four practical rules follow from the model.

**Put foundations on the path.** If an expansion's premise depends on a beat, deliver the beat in content that stays on the main path, or in world geometry. Save temporary delivery for moments.

**Retell in the present tense of the world.** A newcomer doesn't need the battle. They need to know why the harbor is full of wreckage and who they should be angry at. Write the recap as the world's current state, not as a history lesson.

**Tag every beat with its permanence in the setting bible.** Your world bible (the course's final deliverable) should record, for each major event, how it was delivered and whether a player can still reach it. When the delivery changes, for example a campaign is removed or a season is re-released, update the tag. Week 11 on retcons and continuity uses these tags.

**Measure `a` and `r`.** You can't compute `K` without them. `a` is easy, since it is the completion rate of the release content among players active that month. `r` needs a cohort view. Among players who joined after the release window, what share completed the beat within, say, their first 90 days? DB201 and MMO308 cover the telemetry. The point here is to ask for these two numbers for every foundation beat.

## In-class activity (25 minutes)

Work in groups of three with your setting bible draft from weeks 1 to 6.

1. List the five story beats your world's opening expansion depends on most (5 minutes).
2. For each beat, choose a delivery and permanence class, and estimate `a` and `r`. Use 8% monthly churn (6 minutes).
3. Compute `K` at 12 and 24 months for each beat, by hand or with the interactive (6 minutes).
4. Your second expansion ships at month 18. Write its assumed-knowledge table for the five beats, with an action for every beat below `K = 0.5` (8 minutes).

Expected output: a five-row table with `a`, `r`, `K(12)`, `K(24)`, the assumption and the action. Groups will present one beat whose delivery they changed after seeing the numbers.

## Common misconceptions

- **"Everyone saw it, so everyone knows it."** Everyone active that month saw it. With 10% monthly churn, a year later only 28% of the population was active that month.
- **"Players forget lore, so we must repeat it."** Forgetting is part of it, but even a population that forgets nothing loses knowledge through turnover. Repetition by itself does not fix turnover. Only newcomer reach does.
- **"A wiki page solves it."** A wiki gives second-hand knowledge to players who go looking. That can carry a line of dialogue. It cannot carry a scene whose weight depends on having been there.
- **"Permanent is always better."** Permanent delivery keeps `K` high and lengthens the newcomer path. Some beats earn their value from being temporary.

## Check yourself

1. Churn is 15% a month. A temporary beat reached 90% of the live audience. After how many whole months does its knowledge share first fall below 25%?
2. A designer can either raise live reach from 0.7 to 0.9 with a better launch event, or raise catch-up reach from 0 to 0.2 by keeping the chapter replayable. Churn is 10% a month. Which gives a higher knowledge share at month 12? At month 3?
3. Your expansion ships 20 months after a beat with `a = 0.8` and churn 6% a month. You need `K ≥ 0.5` at release. What catch-up reach does the beat need?
4. Explain in terms of the model why a required main story can make a beat *better* known over time, and name one cost of doing it.

<details>
<summary>Answers</summary>

1. `s = 0.85`. We need `0.9 × 0.85^m < 0.25`, so `0.85^m < 0.278`. `0.85^7 = 0.321`, `0.85^8 = 0.272`. Month 8.
2. At month 12, `s^12 = 0.282`. Better launch: `0.9 × 0.282 = 0.254`. Replayable: `0.7 × 0.282 + 0.2 × 0.718 = 0.198 + 0.144 = 0.341`. Replayable wins. At month 3, `s^3 = 0.729`. Better launch: `0.656`. Replayable: `0.510 + 0.054 = 0.564`. The launch event wins early. The two options are equal where `0.2 × s^m = 0.2 × (1 − s^m)`, so at `s^m = 0.5`, which is the half-life of 6.6 months.
3. `s^20 = 0.94^20 = 0.290`. `r = (0.5 − 0.8 × 0.290) / (1 − 0.290) = (0.5 − 0.232) / 0.710 = 0.377`, so about 38%.
4. `K` moves from `a` toward `r`. When newcomers are more likely to meet the beat than the live audience was (`r > a`), the population fills with players who have seen it. The cost is a longer newcomer path, which can raise churn, and a growing backlog that pushes studios to sell skips, which lowers `r` again.

</details>

## Lab / assignment hook

[Lab 07, lore memory](../labs/lab07.md). You implement the knowledge-share model, extend it to a population of short-stay and long-stay players, and use it to audit the foundation beats of your own setting bible. Deliverable: the passing code, a beat table with predicted `K` at 12 and 24 months, and a one-page assumed-knowledge rule for your first expansion. It counts toward the exercises grade and feeds the continuity section of your world bible.

## Sources

- Wolf, M. J. P. (2012). *Building Imaginary Worlds: The Theory and History of Subcreation*. Routledge. Course text; how a world is experienced across works and entry points. Chapter titles checked against the publisher's table of contents (Routledge, September 2026): 1 "Worlds within the World", 3 "World Structures and Systems of Relationships", 4 "More Than a Story: Narrative Threads and Narrative Fabric", 6 "Transmedial Growth and Adaptation", 7 "Circles of Authorship".
- Guild Wars 2 Wiki, "Living World Season 1" (read September 2026). Ran from 28 January 2013 (Flame and Frost: Prelude) to 18 March 2014 (Battle for Lion's Arch: Aftermath) in temporary bi-weekly installments; most of it unavailable for years; re-release announced 22 March 2022 with episodes from 19 April 2022, permanently free. https://wiki.guildwars2.com/wiki/Living_World_Season_1
- Guild Wars 2 Wiki, "Living World Season 2" (read September 2026). Episodes free to players who logged in during each release window, otherwise 200 gems each or as a discounted bundle; first episode 1 July 2014, last 13 January 2015; free again during Spotlight Weeks in May and June 2021. https://wiki.guildwars2.com/wiki/Living_World_Season_2
- Guild Wars 2 Wiki, "Lion's Arch" (read September 2026). The city's destruction by Scarlet Briar and its later reconstruction in the game's history. https://wiki.guildwars2.com/wiki/Lion%27s_Arch
- Warcraft Wiki, "Patch 4.0.3a" (released 23 November 2010). Rebuilt Eastern Kingdoms and Kalimdor with thousands of new quests. https://warcraft.wiki.gg/wiki/Patch_4.0.3a
- Warcraft Wiki, "Chromie Time" (redirects to "Timewalking Campaigns"; read September 2026). Timewalking campaigns introduced in patch 9.0.1 on 13 October 2020, letting players level through a chosen expansion's campaign. https://warcraft.wiki.gg/wiki/Chromie_Time
- Final Fantasy XIV Online Wiki (consolegameswiki), "Main Scenario Quests" (Dawntrail era, 2026). The MSQ is required for many features; story skips sold in the online store. https://ffxiv.consolegameswiki.com/wiki/Main_Scenario_Quests
- Final Fantasy XIV Online Wiki (consolegameswiki), "The Unending Journey" (read September 2026). Furnishing introduced in patch 3.1 for rewatching completed quest cutscenes. https://ffxiv.consolegameswiki.com/wiki/The_Unending_Journey
- Wikipedia, "Destiny 2: Beyond Light" (read September 2026). Released 10 November 2020; five destinations with their campaigns, Year 2 annual pass activities and the original Destiny content moved to the Destiny Content Vault. https://en.wikipedia.org/wiki/Destiny_2:_Beyond_Light
- The churn rates, live reach and catch-up reach in the worked example and activities are invented for teaching.

## Interactive spec: examples/w07-lore-memory.html

**Purpose.** Let students see that the share of today's players who experienced a story beat falls away from the release-day figure at the churn rate, and that after about two half-lives only catch-up reach `r` decides where it ends up.

**The one insight the visual must make obvious.** The dashed "release week" line stays at `a` while the real knowledge share slides toward `r`. The population bar shows why: it fills with newcomers, and their color depends only on `r`.

**Layout.** Two linked views side by side at 1280 px, stacked at 390 px (chart on top), with a results strip underneath.

- Left, "Who knows it now": a line chart. x axis is months since release, 0 to 36. y axis is share of current players, 0 to 100%. Solid line is `K(m)` for the current settings. Dashed horizontal line at `a`, labeled "release week". Dotted horizontal line at `r`, labeled "long run". A vertical marker at the selected month `m`, with the value of `K(m)` printed beside it. Optional ghost lines (thin, neutral token) for the three presets, so students can compare their setting to them. A small tick on the x axis marks the half-life `t½`.
- Right, "Today's population": one horizontal 100% bar, split into four segments, in this order: veterans who saw it (`a × s^m`), veterans who missed it (`(1 − a) × s^m`), newcomers who found it (`r × (1 − s^m)`), newcomers who never met it (`(1 − r) × (1 − s^m)`). "Saw or found" segments use the accent token, the others the neutral token, and veteran segments get a hatch pattern as a second cue that does not rely on color. Each segment's percentage is printed below the bar.
- Results strip: "Knowledge share K(m)", "Half-life t½", "Long-run share r", and "Catch-up reach needed for target", computed from the target control.

**Controls** (keyboard accessible, values printed next to each):

- Live reach `a`: slider 0.10 to 1.00, step 0.05, default 0.80.
- Monthly churn `c`: slider 0.02 to 0.30, step 0.01, default 0.10.
- Catch-up reach `r`: slider 0.00 to 1.00, step 0.05, default 0.00.
- Presets, segmented buttons that set `r`: "Temporary" (0.0), "Gated" (0.3), "Main story" (0.9). Default "Temporary".
- Month `m`: slider 0 to 36, step 1, default 12.
- Target `K*`: slider 0.10 to 0.90, step 0.05, default 0.50, and target month `M`: stepper 1 to 36, default 12.
- Reset button.

**Formulas.**

- `s = 1 − c`.
- `K(m) = a × s^m + r × (1 − s^m)`.
- `t½ = ln 2 / (−ln s)`, printed to one decimal.
- Needed catch-up reach `r_need = (K* − a × s^M) / (1 − s^M)`. Print "0 (already met by live reach alone)" if `r_need ≤ 0` and "not reachable" if `r_need > 1`.

**Test values** (must match to one decimal place in percent).

| a | c | r | m | K(m) |
|---|---|---|---|---|
| 0.80 | 0.10 | 0.00 | 12 | 22.6% |
| 0.80 | 0.10 | 0.30 | 12 | 44.1% |
| 0.80 | 0.10 | 0.90 | 12 | 87.2% |
| 0.80 | 0.10 | 0.00 | 24 | 6.4% |
| 0.80 | 0.10 | 0.30 | 36 | 31.1% |
| 0.60 | 0.05 | 0.50 | 24 | 52.9% |

Half-life at `c = 0.10`: 6.6 months; at `c = 0.05`: 13.5 months. Needed `r` at `a = 0.8`, `c = 0.10`, `K* = 0.5`: 38.2% for `M = 12` and 47.4% for `M = 24`. Population bar at the defaults (`m = 12`): 22.6% / 5.6% / 0.0% / 71.8%.

**First screen.** Defaults (temporary beat, month 12). Caption above the views: "80% saw it at launch. Who has seen it now?" The chart shows the solid line well below the dashed line, and the bar is mostly newcomers who never met the beat.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css` inline, light and dark themes, `prefers-reduced-motion` respected (no animated transitions when set). An `aria-live` text summary under the views states `K(m)` and the four population shares after every change. No game art, logos or screenshots; labels are generic ("story beat", "veterans", "newcomers").
