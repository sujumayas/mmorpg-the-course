# PR401 · Week 01 — Pitch Development

**Why this matters:** Your capstone ends in PR402 with a public launch and a few weeks of live operation with real players. Whatever you pitch this week has to keep those players busy for that whole stretch, and it has to be built by the team in the room. Most capstone pitches that fail at the week 6 greenlight fail on one number they never wrote down, which is how long a player can play before they run out of things to do.

**You will be able to:**
- Write an MMO-scope pitch whose claims are each tagged as assumed, estimated or tested.
- Compute the one-pass content hours a team of seven can author before launch from its capacity and an authoring ratio.
- Compute exhaustion time and the locust ratio for a pitch at several player percentiles, and find the replay multiplier the pitch needs.
- Revise a pitch until its median player does not run out of content during the live period, and name the claim that makes it work.

**Before class:** Reread [MMO306 week 1, the content treadmill](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w01-the-content-treadmill-production-vs-consumption.md), section 2 (the exhaustion-time model, 20 minutes). Reread [MMO403 week 14, pitching to publishers and investors](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md), sections 1 and 4 (what a funder is buying, 20 minutes). Bring your team's PR301 post-mortem and two pitch ideas written on half a page each.

**Prerequisites from earlier courses:** [PR201 week 1](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w01-pitch-and-team-formation.md) for plannable hours per person and the discipline load test, which this guide reuses without re-deriving. [PR101 week 1](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w01-roles-on-a-game-team.md) for the channel cost `c × (n − 1)`. [GD101 week 14](../../GD101-introduction-to-game-design/lectures/w14-design-documents-one-pagers-and-pitch.md) for the one-pager and the three-minute pitch. [MMO306 week 1](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w01-the-content-treadmill-production-vs-consumption.md) for exhaustion time `T` and the locust ratio `L`. [PR301 week 13](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w13-beta-open-class-playtest.md) for the persistent world your team has already shipped once, to 50 or more concurrent players.

---

## 1. What the capstone asks you to ship

The capstone runs for two semesters. PR401 is pre-production and PR402 is production and launch. This semester you hand in three things, weighted as the [syllabus](../syllabus.md) shows. The pitch (20%) is judged at the greenlight review in week 6. Two prototypes (30%) are built in weeks 4 and 5. The pre-production package (50%) is due in week 15. It holds the technical design, economy plan, content plan, social systems plan, production plan and a vertical slice.

PR402 then gives you eight production weeks, an alpha, a closed and an open beta, a launch, and about four weeks of live operation with real players before the post-mortem. That last stretch is what makes this course different from PR301. In PR301 you ran a persistent world for a class playtest weekend. In PR402 strangers will log in and stay, or not.

"MMO-scope" in this course means four things, not a player count:

| Requirement | What it means for the capstone |
|---|---|
| Persistence | The world state outlives any one session and any one player ([MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md)) |
| Shared space | Players who have never met share a server and affect each other |
| A social structure | Some goal needs a group that persists beyond one session ([MMO305 week 4](../../MMO305-social-systems-and-online-behaviour/lectures/w04-guilds-formation-lifecycle-leadership.md)) |
| A reason to return | The game has something to do in week 4 of live operation that was not done in week 1 |

The fourth row is the one teams skip. It is the subject of this week's worked example.

## 2. Worked example: will the content last until the patch?

### The hook

*New World* launched on Steam on 28 September 2021. In October 2021 SteamCharts recorded an average of about 410,000 concurrent players and a peak of about 913,000. By January 2022 the monthly average was about 65,000, and by June 2022 it was about 13,600, roughly 3% of the launch month. The launch had other problems too (MMO407 week 6 covers the duplication exploits), and a player count on one store is not the whole audience. Still, a fall that steep is the pattern the content treadmill predicts. Players eat content faster than any team can make it, and a player with nothing left to do stops logging in.

Your team is about seven people, not several hundred. Your live period is four weeks, not years. The arithmetic is the same.

### The model

Two models you already know, joined at one number.

**Supply side (PR201 week 1).** Member `i` can plan `p_i = (1 − b) × (H − c × (n − 1)) × W` hours of work before launch. The team plans `Σ p_i`. A share `s` of those hours goes to authored content (zones, quests, encounters, items with hand-set stats). Authoring one hour of play costs `k` team hours. So the team can make

```
C = s × Σ p_i / k          one-pass content hours at launch
```

**Demand side (MMO306 week 1).** A player who plays `h` hours a week runs out of new things to do after

```
T = 7 × C × r / h          days until exhaustion
L = P / T                  locust ratio over a live period of P days
r_needed = h × P / (7 × C) the replay multiplier that makes L = 1
```

- `H` is weekly project hours per person. The course convention is 8 in PR401 (4 credits) and 12 in PR402 (6 credits).
- `c = 0.25` hours per channel per person per week, `n` is team size, `b = 0.3` is the buffer.
- `W` is production weeks before launch. PR402 weeks 1 to 8 give `W = 8`.
- `s` is the share of hours spent on authored content, as opposed to systems, tools, networking and polish.
- `k` is the authoring ratio. This guide uses `k = 20` team hours per play hour as a course assumption for a student team working in a known engine. It is not an industry figure. You will measure your own in weeks 4 and 5.
- `r` is the replay multiplier: how many times a player will do the content before it stops being worth doing. Systems (crafting, trading, territory, PvP, procedural layouts) raise `r`. Story quests sit near 1.
- `P = 28` days, the four-week live period in PR402.

`L ≤ 1` means the player still has something new when the live period ends. `L = 2` means they ran out halfway through.

### Numbers you can check

A team of seven in PR402. Coordination costs `0.25 × 6 = 1.5` hours a week, leaving 10.5. With the buffer, each person plans `0.7 × 10.5 × 8 = 58.8` hours, and the team plans 411.6 hours before launch.

The team has two pitches. *Lanternfall* is a story-led co-op MMO with a quest chain through three zones. It spends 40% of the team's hours on authored content and expects most players to replay it once with a second character, `r = 1.5`. *Emberfall* is a small co-op world with two classes, one dungeon and a crafting and trade loop, where every tool and weapon is made by a player and small groups hold towns. It spends only 25% on authored content, because the rest goes to crafting, market and town systems. The team claims `r = 8`: players will run the gather, craft and trade loop many times over.

`C` for *Lanternfall* is `0.40 × 411.6 / 20 = 8.2` hours. For *Emberfall* it is `0.25 × 411.6 / 20 = 5.1` hours.

Use four player types, set by weekly play time. The values are chosen for teaching, shaped like the long tail in MMO306 week 1, not measured.

| Player | `h` (h/week) | *Lanternfall* `T` (days) | `L` | *Emberfall* `T` (days) | `L` |
|---|---|---|---|---|---|
| Light | 3 | 28.8 | 0.97 | 96.0 | 0.29 |
| Median | 5 | 17.3 | **1.62** | 57.6 | 0.49 |
| Keen (p90) | 12 | 7.2 | 3.89 | 24.0 | **1.17** |
| Heavy | 25 | 3.5 | 8.10 | 11.5 | 2.43 |

Check the median *Lanternfall* cell. `C × r = 8.2 × 1.5 = 12.3` hours. `T = 7 × 12.3 / 5 = 17.3` days, and `L = 28 / 17.3 = 1.62`. The median player finishes before live-ops week 3 and spends the last 10.7 days with nothing new. The keen player is done in a week. To hold the median player, *Lanternfall* needs `r = 5 × 28 / (7 × 8.2) = 2.4`. To hold the keen player it needs 5.8.

*Emberfall* holds the median player with room to spare and runs out for the keen player four days before the end. It made fewer content hours and lasts longer, because its content is replayable.

The lab 01 checker reproduces this table from a pitch sheet. Change `content_share` to 0.40 and `replay` to 1.5 and it prints `FAIL: median L = 1.62`.

### What the table does not tell you

*Emberfall* passes on paper only because the team wrote `r = 8`. Nobody has measured it. If the real value is 3, the median `L` is 1.30 and *Emberfall* fails too. Every number in the *Lanternfall* column came from a capacity sum and an assumed `k`. The number that decides the *Emberfall* column came from optimism.

This is the most useful output of the calculation. It turns a vague worry ("will people keep playing?") into one named claim with a threshold. *Emberfall* players must repeat the core loop at least `r = 5 × 28 / (7 × 5.1) = 3.9` times per content pass, and 9.3 times if you want to hold the keen players too. That claim becomes the first risk on your week 4 prototype list. A pitch that passes this test with an untested `r` has not passed. It has told you what to prototype.

### The same idea elsewhere

**Albion Online.** Sandbox Interactive's MMO, released in July 2017, is built so that all equipment is made by players and the economy is player-driven. In the terms above, the studio spends its hours on systems that raise `r` rather than on content that raises `C`. Every item a player crafts is content another player uses.

**MMO306 week 1, design B.** The same 20 content hours made worth playing six times through tiers and repeatable rewards. Raising `r` moves every percentile by the same factor. A weekly gate moves only the top rows. Your pitch should say which one it relies on.

**PR201 week 1.** There the question was whether a pitch fits the team's hours in each discipline. Here it is whether the pitch fits the players' hours. A capstone pitch has to pass both. It is easy to raise `C` by pouring art hours into zones and then fail the discipline load test for art.

### Eyes-open judgment

The model has four numbers you cannot know in week 1: `k`, `r`, the play-time distribution and `P` if PR402's live period shifts. Use it to compare pitches and to find the claim that carries the most weight. Do not use it to promise anyone a retention figure.

Two traps. First, raising `r` by grinding (make the loop take ten times longer) passes the test and fails the player. Replay has to come from decisions that change each time, such as a market price that moved or a rival group that took your town. Second, a gate (daily limits, timers) looks like a free fix because it lowers `L` for heavy players. It does nothing for the median player, and a four-week launch with a daily cap can feel empty to the people who arrive keen. Decide deliberately which players you are designing the live period for, and write it in the pitch.

### Check yourself

1. The *Lanternfall* team raises its authored share to 55% and keeps `r = 1.5`. What is the median `L` now? What happens to the discipline load for art and design, and why might that make the pitch worse?
2. *Emberfall* measures `r = 4` in its week 4 prototype. Which player types still reach `L ≤ 1`? What is the smallest `r` that holds the keen player?

<details><summary>Answers</summary>

1. `C = 0.55 × 411.6 / 20 = 11.3`, `C × r = 17.0`, `T = 7 × 17.0 / 5 = 23.8` days, `L = 1.18`. Still above 1. The extra 61.7 team hours of content work come mostly from art and design, so their loads rise, and 15 points of share came out of systems or polish. More content closed about 70% of the gap (`L` fell from 1.62 to 1.18) and still left the median player four days short, at the price of the rest of the plan.
2. `C × r = 5.1 × 4 = 20.6`. Light: `T = 48` days, `L = 0.58`. Median: `T = 28.8`, `L = 0.97`, just holds. Keen: `T = 12.0`, `L = 2.33`. To hold the keen player, `r = 12 × 28 / (7 × 5.1) = 9.3`.

</details>

## 3. The capstone pitch

Use the GD101 week 14 one-pager as the base. A capstone pitch adds sections a funder or a greenlight panel will ask for, as MMO403 week 14 describes. Keep the whole thing to two pages plus a one-page appendix of numbers.

1. **The moment.** One scene a player will describe to a friend.
2. **Why persistent, why together.** What in this game only works because the world outlives the session and other players are in it. "You can see other players" is not an answer.
3. **The content engine.** Which systems generate repeat play, the `C` and `r` the pitch assumes, and the table from section 2.
4. **The live period.** What a player does in week 1, week 2 and week 4 of PR402 live operation.
5. **Comparables.** Two to four shipped games your players already know. Week 2 turns this into a market analysis.
6. **Team fit.** The PR201 discipline load table for the pitch.
7. **Claims and unknowns.** The list in section 4.

## 4. A pitch is a list of claims

A greenlight panel does not judge whether your idea is good. It judges whether your claims are believable and whether you know which ones are weak. So write them down.

A **claim** is a sentence the pitch depends on that could turn out false. "Players will repeat the craft and trade loop at least three times per pass" is a claim. "The server can hold 60 players in one town with shared storage" is a claim. "Our artist can make a modular town kit in 40 hours" is a claim.

Tag each claim with its **evidence level**:

- **Assumed.** Nobody has checked. Most week 1 claims.
- **Estimated.** Derived from a model or a comparable, like `C` above or a comparable's player count in week 2.
- **Tested.** Checked against a prototype, a measurement or a playtest. Weeks 4 and 5 move claims here.

Then mark which claims are **load-bearing**, meaning the pitch fails if the claim is false. For *Emberfall*, `r ≥ 3.9` is load-bearing and assumed. That combination is the pitch's biggest risk, and naming it is a strength at greenlight, not an admission.

Aim for eight to fifteen claims. Fewer usually means the team has not looked. Many more usually means the team has listed tasks.

## 5. Choosing between two pitches

Every team brings two pitches. By the end of the session keep one, in this order:

1. **Does it hold the median player?** Run the section 2 table. A pitch that needs `r` above 5 for the median player is asking one loop to do too much.
2. **Does it fit the team?** Run the PR201 week 1 load test with PR402 hours.
3. **Is its riskiest claim testable in two weeks?** If the load-bearing assumption can only be tested with 200 players, you will reach greenlight with nothing to show.
4. **Does the team want to build it for thirty weeks?** A pitch that passes and bores everyone will lose to one that almost passes and that people care about. Then fix the one they care about.

Use the numbers to remove pitches. Let the product owner decide between survivors after hearing everyone.

## Studio session plan

The studio meets for 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:20 | Capstone brief: PR401 and PR402 milestones, the four MMO-scope requirements, assessment | Questions answered |
| 0:20 to 0:50 | PR301 carry-over. Each team reads its PR301 post-mortem aloud in 3 minutes: one thing to keep, one to never repeat | One line each in the charter |
| 0:50 to 1:30 | Two-pitch round. Each team gives both pitches in 90 seconds each. Another team writes down every claim it hears | Claim lists, written by outsiders |
| 1:30 to 1:40 | Break | |
| 1:40 to 2:20 | Content budget. Teams fill the lab 01 pitch sheet for both pitches and run the checker. Instructor circulates and asks where `k` and `r` came from | Section 2 table for both pitches |
| 2:20 to 2:45 | Claims sheet. Teams merge their own claims with the list the other team wrote, tag evidence levels and mark load-bearing claims | Draft `claims.csv` |
| 2:45 to 3:00 | Decision. Each team names its chosen pitch, its median `L`, and its riskiest load-bearing claim in one minute | Instructor sign-off or a named concern |

## Deliverables

Due before next week's studio session.

One folder convention holds for the whole course. Each week's hand-in (sheets, checker output, logs, records) goes in `preproduction/weekNN/` in your team repository, so this week's goes in `preproduction/week01/`. Documents that later weeks keep updating live in `docs/` (the pitch, the claims sheet, the market section, the vision page, the TDD, the economy, content and social plans). Data files the game reads live in `data/`, and prototype builds in `prototypes/p1/` and `prototypes/p2/`. The week 15 package links to all of them.

This week, `docs/pitch.md` and `docs/claims.csv` start their life, and everything else goes in `preproduction/week01/`.

- **Pitch draft** (two pages plus the numbers appendix) with the seven sections from section 3. The comparables section may be a list of names this week.
- **Pitch sheet** (`pitch.csv`) and the checker output for the chosen pitch, plus the output for the rejected one.
- **Claims sheet** (`claims.csv`) with 8 to 15 claims, each with an evidence level, a load-bearing flag and an owner.
- **Team charter update** carried over from PR301, with the two PR301 lessons and the PR402 hours convention (`H = 12`) agreed by every member.

The instructor reruns the lab 01 checker on your files. See [lab 01](../labs/lab01.md).

## Common failure modes

- **Pitching the full game.** The pitch describes a world of ten zones and five classes. Fix: pitch what PR402 will launch. Put the rest under "the full game" and keep it to one paragraph.
- **No reason to return.** Every activity is a one-time quest. Fix: run the section 2 table. If the median `L` is above 1, name the system that raises `r`, or cut the live period plan to match.
- **Grind as replay.** The team raises `r` by making the loop slower. Fix: for each repeat, name what is different about it for the player.
- **Claims hidden as features.** "Dynamic economy" appears as a feature with no claim behind it. Fix: rewrite each feature as the claim it depends on, and tag it.
- **One author.** The producer writes the pitch alone. Fix: each discipline's primary writes the claims for their own discipline.

## Review checklist

The instructor signs off the week 1 pitch draft when:

- [ ] The pitch meets all four MMO-scope requirements in section 1, and says how.
- [ ] `check_pitch.py` runs on the submitted `pitch.csv` and prints a median `L` at or below 1, or the pitch states why it accepts a higher value.
- [ ] The values of `k` and `r` are marked as assumed or estimated, with a note on where they came from.
- [ ] The claims sheet has at least one load-bearing claim tagged "assumed", and it has an owner.
- [ ] The live period section names what a player does in week 4.
- [ ] The rejected pitch and the reason it lost are recorded.
- [ ] Every member has agreed the charter update.

## Sources

- SteamCharts, "New World: Aeternum" (app 1063730), monthly average and peak concurrent players, October 2021 to June 2022 (accessed September 2026). SteamCharts samples Steam's public concurrent-player counts; it covers Steam only.
- Wikipedia, "New World: Aeternum" (accessed September 2026). Windows release on 28 September 2021; over 700,000 concurrent players recorded on Steam on launch day.
- Wikipedia, "Albion Online" (accessed September 2026). Developer Sandbox Interactive (Berlin); full release 17 July 2017; free to play from April 2019; all equipment made by players; player-driven economy.
- MMO306 week 1 for the exhaustion-time model, and PR201 week 1 for the capacity model, both in this repository.
- The two pitches, the authoring ratio `k = 20`, the play-time percentiles and the `H = 12` convention for PR402 are invented for teaching or are course conventions. They are not measurements.
