# PR301 · Week 11 — Sprint 4: Social Systems

**Why this matters:** Your world now persists, has combat and has an economy, and the week 10 telemetry review told you what players did in it over the alpha weekend. What they could not do was play together on purpose. Next week's group encounter needs a working party, and the beta in week 13 needs 50 people who can find each other, talk and stay. Sprint 4 is also the first one-week sprint of the course, so the planning mistakes that a two-week sprint absorbs will show up by Friday. This week you plan a social sprint that fits the team you actually have, and you build the part of it the encounter depends on first.

**You will be able to:**
- Compute a one-week sprint capacity from your velocity history, availability and a bug reserve, and commit at the low end of it.
- Order a social backlog by dependency, so that the party system the week 12 encounter needs is never the item that slips.
- Rescope a feature into a smaller version that keeps its purpose, instead of cutting it whole or keeping it whole.
- Check the chat and presence load your social features put on the world server before you merge them.

**Before class:** Bring your week 10 telemetry review and its ranked input list, and export the done hours per sprint from your tracker for sprints 1 to 3. Re-read PR101 week 6, section 2 on estimation ranges (15 minutes) and MMO302 week 10, section 2 on fan-out (20 minutes). Skim MMO305 week 4 on how guilds form and fail (15 minutes).

**Prerequisites from earlier courses:** [PR101 week 4, scope, MVP and cut lists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) and [PR101 week 6, estimation and why it fails](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (the capacity arithmetic this guide uses without re-teaching). [PR101 week 7, task tracking and definitions of done](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md). [MMO302 week 10, chat, guild and social services](../../MMO302-mmo-server-architecture/lectures/w10-chat-guild-and-social-services.md) (fan-out, presence and token buckets). [MMO302 week 7, persistence strategies](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) (what to write and when). [MMO305 week 3, forced versus voluntary grouping](../../MMO305-social-systems-and-online-behaviour/lectures/w03-forced-vs-voluntary-grouping.md) and [MMO305 week 4, guilds](../../MMO305-social-systems-and-online-behaviour/lectures/w04-guilds-formation-lifecycle-leadership.md) (why these features exist at all). From this course, your week 10 telemetry review and the [syllabus](../syllabus.md).

---

## 1. What "social systems" means for a 50-player prototype

A shipped MMO has dozens of social features. Your prototype needs the few that let 50 testers group up for an encounter and come back the next day. In rough order of what depends on what:

- **Chat channels.** Say (nearby), zone, whisper and party at minimum. Everything else in this list uses the same channel code.
- **Party.** Invite, accept, leave, kick, a leader, and party frames that show members' health. The week 12 encounter cannot be tested without it.
- **Party rewards.** Shared experience and a loot rule inside a range. Without a loot rule the encounter's drop goes to whoever clicks first, which your testers will notice.
- **Friends and presence.** Who is online, and where. Cheap to show, expensive to keep current (section 3).
- **Guild.** A named, persistent group with a roster, a chat channel and, later, ranks and permissions.

MMO305 week 3 makes the design case for voluntary grouping, and week 4 describes what guilds do for retention. You don't need to re-argue either. Your pillars from week 1 already say which social behaviour your world is built around. Use them to decide which item on this list is the one players would miss most, and check that choice against your week 10 telemetry. If the alpha showed players forming ad hoc groups in one zone, the party is doing its job and the guild is the gap. If nobody grouped at all, the problem is upstream of any guild feature.

## 2. Planning a one-week sprint

Sprints 1 to 3 ran for two weeks each. Sprints 4 and 5 run for one week each, because the beta date in week 13 does not move. A one-week sprint has two properties that catch teams out.

First, there is no slack. In a two-week sprint, a sick day costs 5% of capacity. In a one-week sprint it costs 10%, and the review is four working days after planning.

Second, your velocity history is in the wrong unit. Since the sprint 1 review you have measured velocity as the estimated hours of stories that met the definition of done (the numerator of the focus factor in week 3). Your tracker says the team finished, say, 39.5 estimated hours in sprint 1. That was two weeks of work, from one planning session to the next. Convert every past sprint to estimated hours per team-week before you use it, and use the worst of the recent weeks as your planning figure, not the average. Week 7 used the same low-end rule for sprint 3. PR101 week 6 explains why estimates are biased low. A one-week sprint has no time to recover from that bias.

The planning rule for this course is:

```
capacity_low   = min(weekly velocity, last 3 sprints) × (available person-days / full person-days)
capacity_mean  = mean(weekly velocity, last 3 sprints) × (available person-days / full person-days)
commit         = capacity_low − bug reserve
stretch        = capacity_mean − bug reserve − commit
```

The **bug reserve** is the estimated size of the bugs from your week 10 input list that must be fixed before beta, or the 20% of the low forecast that week 7 reserved, whichever is larger. Put the bugs in the sprint as real items with estimates. A team that plans features to its full velocity and "fits bugs in around them" always ships the features half done and the bugs not at all.

## 3. The server cost of being social

Chat and presence are the only features in your world that touch every player at once. MMO302 week 10 derives the fan-out wall: one message in a channel of `L` members costs `L` deliveries, so a channel where every member talks costs deliveries that grow with `L²`. At 50 players you are far from that wall, but two things still go wrong in student builds.

- **No rate limit.** One tester with a macro, or one bot in your week 13 load test with a bug in its chat loop, can post hundreds of messages a second. Add a token bucket per player per channel now (MMO302 week 10, section 5). It is a dozen lines of code.
- **Presence storms.** When the server restarts, every player logs in within a minute or two, and each login tells every friend and guild member. With 50 players in one guild that is 50 × 49 = 2,450 presence updates in a burst. Your server will survive it. Your client's friends-list UI, redrawn 2,450 times, may not. Batch presence updates on the client, or send them at most once a second.

Write the worst case down before you merge, using the numbers in the worked example. The definition of done for any social feature in this sprint includes a bot test at 50 clients (section 5).

## 4. What persists and what does not

Your world server already has a persistence strategy from sprint 1 (MMO302 week 7). Social features split cleanly across it.

- **Party:** in memory only. If the server restarts, parties dissolve and players regroup. Every shipped MMO you have played treats parties this way for good reason.
- **Guild and friends:** persistent. A guild that vanishes after a restart is a data-loss bug, and in week 14 data-loss bugs sit at the top of the triage list.
- **Chat history:** not persisted by the world server. If you want a log for moderation or for telemetry, write it to a separate append-only store, not to the character database.
- **Party loot:** the item transfer is persistent and must use the same transactional path your economy sprint built (MMO302 week 8). A loot roll that grants an item twice is a duplication exploit, however small your world is.

## 5. Worked example: the *Saltmarsh* team plans sprint 4

### The hook

Even the largest games put hard limits on social features, because every limit is a scope decision someone could plan against. World of Warcraft capped guilds at 1,000 members in patch 4.0.1 in 2010, and guilds already above the cap could not invite anyone until they fell below it. A thousand is not a law of nature. It is a line drawn so that a team could build, test and support the feature, and so that players knew where the edge was. Your sprint 4 needs the same kind of line, drawn in hours.

### The team and its history

The *Saltmarsh* team from week 3 has seven members: three programmers (Ana, Ben and Chen), a designer (Dee), two artists (Eli and Fay) and a producer (Gus). Its world is a marsh settlement with a market square, reed beds and salt pans, built over sprints 1 to 3. Their tracker shows estimated hours of done stories per sprint of 39.5 (reviewed in week 5, a focus factor of 0.46), 44.8 (reviewed in week 7, 0.54) and 34 (reviewed in week 9). Each of those sprints was two weeks, so the weekly velocities are 19.75, 22.4 and 17 hours. (Sprint 3 was low because the economy sprint ran into the transactional item-transfer work described in MMO302 week 8.)

Dee has a mid-term exam on Wednesday and Thursday and will work half the week. The team counts 7 people × 5 days = 35 person-days in a full week. This week it has 32.5.

The week 10 telemetry review put four small items at the top of its input list, to go in before any guild feature can move copper. The team estimates them at 4 hours in all: write-through for both sides of mail send, trade and market completion (2 hours), correcting the three senders' balances with an `S_GM_CORRECTION` sink (0.5 hours), the `F_STARTER` reason code, rounding logged as applied and the residual alarm unmuted (0.5 hours), and the reed mat vendor price with the recipe check in the build pipeline (1 hour). They total 4 hours, and 20% of the low forecast is 3.2 hours, so the bug reserve is 4 hours.

### The capacity numbers

```
availability   = 32.5 / 35                      = 0.929
capacity_low   = 17 × 0.929                     = 15.8 hours
capacity_mean  = 19.72 × 0.929                  = 18.3 hours
commit         = 15.8 − 4                       = 11.8, so 11 hours of features
stretch        = 18.3 − 4 − 11                  = 3.3, so up to 3 hours
```

Round down, not to the nearest whole hour. The commit is the work the team tells the instructor will be done. The stretch is work that starts only after every committed item meets its definition of done. After choosing items, run the week 3 per-person load check on them too. A social sprint is heavy on code, so the team total can fit while a programmer is over 1. The *Saltmarsh* team gives the bot test scripts to Gus and Dee and the party frame and guild window art to Eli and Fay, which keeps the three programmers under 1.

### The backlog

Gus, as producer, brought this social backlog, estimated in hours by the team in planning poker (PR101 week 6).

| Item | Hours | Depends on | Why it matters |
|---|---|---|---|
| Party: invite, accept, leave, kick, leader, frames | 5 | none | Week 12 encounter needs it |
| Party chat channel | 1 | party | Coordination in the encounter |
| Shared XP and loot rule within 40 m | 3 | party | Encounter reward |
| Whisper and zone chat with token bucket | 2 | none | Beta testers need to find groups |
| Friends list with online presence | 3 | none | Return visits |
| Guild: create, invite, persisted roster | 5 | none | Pillar 2, "the settlement is run by its guilds" |
| Guild chat channel | 1 | guild | Pillar 2 |
| Guild ranks and permissions | 3 | guild | Pillar 2 |

The full backlog is 23 hours, twice the commit.

### Option A: take items in priority order

The team's first instinct is to go down the list until the hours run out. Party (5), party chat (1), shared XP and loot (3) and whisper and zone chat (2) add up to 11 exactly. The commit is full and the guild has not started.

That plan builds everything the encounter needs, but it leaves pillar 2 with nothing at beta. Fifty testers will arrive in a world whose pitch is about guilds and find no way to make one. The week 13 beta review will mark it, and it should.

### Option B: rescope, then fill

A better question than "which items fit?" is "what is the smallest version of each item that still does its job?" The team looks at the three guild items together. For the beta, a guild needs to exist, keep its members across restarts and let them talk. Ranks and permissions can wait, because with a week-old guild of eight testers, everyone is an officer anyway.

The team splits the work again:

| Item | Hours | Change |
|---|---|---|
| Guild lite: create, invite, leave, persisted roster, guild chat reusing the channel code | 3 | Replaces 5 + 1 |
| Shared XP within 40 m (no loot rule yet) | 1 | Split from the 3-hour item |
| Loot rule | 2 | Moved to sprint 5, where the encounter drops the loot |

Why is "guild lite" 3 hours when the guild items were 6? The roster and the invite flow share code with the party already in this sprint. Guild chat is a second instance of the channel class, not a new system. Leaving out ranks removes the permission checks from every guild action. The team estimated the lite version from scratch, in planning poker, rather than by subtracting. Subtracting estimates tends to keep the hidden work of the parts you removed.

The committed sprint becomes:

| Committed item | Hours |
|---|---|
| Party: invite, accept, leave, kick, leader, frames | 5 |
| Party chat channel | 1 |
| Whisper and zone chat with token bucket | 2 |
| Guild lite | 3 |
| **Features committed** | **11** |
| Bug reserve (4 items from week 10) | 4 |
| **Sprint total** | **15** |

Stretch, up to 3 hours: shared XP within 40 m (1). Deferred to sprint 5: loot rule (2). Deferred past the course: friends list (3) and guild ranks (3), both written into the post-mortem backlog with the reason. Friends are cut, not deferred, because presence is the riskiest piece (section 3) and the guild roster already shows who is online in the group that matters most.

### Check the order inside the sprint

A commit is also a sequence. The party is 5 of the 11 hours and everything in week 12 depends on it, so it starts on Monday with two people. If only one item finishes this week, it must be the party. Guild lite starts on Tuesday because it reuses the party's roster code. The token bucket goes in with the zone chat, not after it, so that the bot test on Thursday never runs against an unlimited channel.

### Check the server cost

Before merging chat, the team writes its worst case:

```
players in the zone channel      L = 50
token bucket                     5 messages per 10 s = 0.5 messages/s per player
worst-case posts                 50 × 0.5 = 25 messages/s
worst-case deliveries            25 × 50 = 1,250 deliveries/s
at about 150 bytes per delivery  1,250 × 150 = 187,500 bytes/s ≈ 1.5 Mbit/s outbound
login presence burst (one guild) 50 × 49 = 2,450 updates within about a minute
```

A world server on a student cloud instance handles 1,250 small messages a second. Without the bucket, a single looping bot at 100 messages a second produces 5,000 deliveries a second on its own, four times the whole rate-limited worst case. The bucket is what makes the worst case a number you can write down.

### What the example shows

Option A and option B commit the same 11 hours. Option B turns in a sprint that serves both the encounter and the pillar, because the team changed the size of the items, not the size of the sprint. Every rescope is written down with what was left out, so the week 15 post-mortem can say whether leaving it out was right.

### Check this example

1. Suppose Dee is away all week instead. Recompute the commit.
2. Gus proposes committing at the mean capacity "because sprint 3 was unusual." What would the commit be, and what do you say?
3. Why does the team start the party on Monday with two people, when the guild is the pillar feature?

<details>
<summary>Answers</summary>

1. Available person-days are 30 of 35, so availability is 0.857. `capacity_low = 17 × 0.857 = 14.6`, commit `= 14.6 − 4 = 10.6`, so 10 hours. Something has to leave the commit. Moving whisper and zone chat (2) to stretch leaves 9 hours committed, and the party plus guild lite still fit.
2. `18.3 − 4 = 14.3`, so 14 hours. Sprint 3 may have been unusual, but one of three sprints being low is normal, not unusual. Commit at the low figure and put the extra work in stretch, where it costs nothing if it doesn't happen.
3. The encounter in week 12 cannot be built or tested without the party, and a sprint 5 that starts without a working party has lost most of its week. Dependencies decide the order. Pillars decide what is in the sprint at all.

</details>

## Studio session plan

The studio meeting runs 180 minutes with one break.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Instructor briefing: one-week sprints, the capacity rule, rescoping versus cutting | None |
| 0:15-0:40 | Teams convert sprint 1 to 3 velocity to weekly figures, record availability and size the bug reserve from the week 10 input list | Capacity sheet (lab 11) |
| 0:40-1:20 | Planning poker on the social backlog; rescope at least one feature into a smaller version | Estimated backlog |
| 1:20-1:30 | Break | None |
| 1:30-1:55 | Commit, stretch and deferral decisions; order the committed items by dependency; run the lab 11 checker | Sprint plan that passes |
| 1:55-2:25 | Pair review with another team: each team explains its biggest rescope and its worst-case chat numbers | Challenge notes |
| 2:25-3:00 | Start work on the first dependency (usually the party); instructor walk-round signs off each plan | First commits on the sprint branch |

## Deliverables

Due at the start of the week 12 studio meeting, in the team repository under `production/week11/`.

1. **Sprint 4 plan** (lab 11) that passes `check_sprint.py`, with the checker output saved. Checked by rerunning the checker.
2. **Rescope note.** One paragraph per rescoped or deferred item, saying what was left out and why. Checked by reading it against the backlog.
3. **Social features merged**, each with its definition of done met: a bot test at 50 clients in which the feature was used, and the server log for that test. Checked in the week 12 build by forming a party, joining a guild and chatting.
4. **Bug reserve closed.** Each week 10 bug in the reserve is closed in the tracker with a commit link, or carried into sprint 5 with a reason.
5. **Sprint 4 review notes** at the end of the week: done hours against commit, and what the team will change in sprint 5 planning.

## Common failure modes

- **Using two-week velocity for a one-week sprint.** The team commits 39 hours and finishes 17. Convert every past sprint to hours per team-week first.
- **Committing at the average.** The average is the figure you miss half the time. Commit at the low end and use stretch for the rest.
- **Building the pillar feature first and the dependency last.** A beautiful guild window and no party on Friday means sprint 5 starts a week late.
- **Cutting whole features instead of rescoping them.** "No guild" and "full guild" are not the only choices. Ask what the smallest version that does the job is.
- **Chat without a rate limit.** It works in the team's test and falls over when one bot loops. Put the token bucket in the same commit as the channel.
- **Persisting the party or not persisting the guild.** Parties are in memory; guilds and friends are persistent. Getting either backwards creates bugs that surface only after a restart, which in this course means during the beta.
- **Bugs "fitted in around" features.** Put the reserve in the sprint as hours, or it will not happen.

## Review checklist

The instructor checks, at the week 12 meeting:

- [ ] Weekly velocities are derived from the tracker, and the commit is at or below `capacity_low − bug reserve`.
- [ ] Availability is recorded per person, not assumed to be full.
- [ ] Every committed item's dependencies are committed or already done.
- [ ] At least one feature was rescoped into a smaller version, with a written note of what was left out.
- [ ] The party works in the build: invite, accept, leave, frames, party chat.
- [ ] Chat has a per-player rate limit, and the worst-case delivery rate is written down.
- [ ] Guild data survives a server restart, shown live or in a recorded test.
- [ ] Sprint 4 review notes compare done hours with the commit, and name one change to sprint 5 planning.

## Sources

- Warcraft Wiki, "Guild" (accessed September 2026, retail World of Warcraft). Guild member cap of 1,000 introduced with patch 4.0.1 (2010); guilds above the cap could not invite until they had 999 or fewer members; `/g` guild chat and `/o` officer chat. https://warcraft.wiki.gg/wiki/Guild
- MMO302 week 10 (this program) for the fan-out model, presence storms and the token bucket, with its sources.
- PR101 weeks 4, 6 and 7 (this program) for cut lists, estimation ranges and definitions of done, with their sources.
- The *Saltmarsh* team, its velocities, backlog, estimates and bug list are a constructed teaching example, not data from any real team.
