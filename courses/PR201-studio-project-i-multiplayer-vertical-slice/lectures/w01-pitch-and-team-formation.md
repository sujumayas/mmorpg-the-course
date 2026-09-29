# PR201 · Week 01 — Pitch and Team Formation

**Why this matters:** This week you choose the people you will work with for fifteen weeks and the game you will build with them. Both choices are hard to undo. Most student teams that miss their final milestone picked a game that needed more of one skill than the team had, and they found out in week 9. You can find out today, with one table and some division.

**You will be able to:**
- Pitch a multiplayer RPG slice in 90 seconds, naming what players do together that they could not do alone.
- Build a skill matrix for a team of five to seven and find every discipline with no backup.
- Compute each discipline's supply and load for a pitch, and decide whether the pitch fits the team.
- Change a pitch (cut, reuse or move work) until its largest load is at or below 1, and record the change.

**Before class:** Reread [GD101 week 14, design documents, one-pagers and the pitch](../../GD101-introduction-to-game-design/lectures/w14-design-documents-one-pagers-and-pitch.md), sections 2 and 4 (the pillar-mechanic map and the three-minute pitch). Reread [PR101 week 1, roles on a game team](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w01-roles-on-a-game-team.md), sections 2, 4 and 5 (the channel model, the bus factor and the team charter). Bring one pitch idea written on half a page.

**Prerequisites from earlier courses:** [PR101 week 1](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w01-roles-on-a-game-team.md) for useful capacity `n × H − c × n × (n − 1)`. [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) for the vertical slice and the buffer. [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) for why a 30% buffer is a starting guess, not a safe number. [CS202 week 3](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w03-topologies-peer-to-peer-client-server-relay.md) for what "client-server" will commit you to.

---

## 1. What this course asks you to ship

PR201 is the first time you build a networked game as a cross-discipline team. By week 15 your team hands in a **multiplayer vertical slice**: 10 to 15 minutes of an RPG that two to four players can play together over a network, built to final quality in every layer. PR101 week 4 defined the vertical slice as a thin strip cut through code, art, sound, UI and feedback. This course keeps that definition and adds a network through the middle of it.

The slice has fixed requirements. Everything else is yours to choose.

| Requirement | What it means in practice |
|---|---|
| 2 to 4 players on separate machines | Not split-screen, not two windows on one laptop |
| Server-authoritative | Clients send intent, the server decides results ([CS202 week 4](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md)) |
| One zone, one encounter worth remembering | A fight, a puzzle or an event that needs more than one player |
| One step of progression | Players leave the slice stronger, richer or changed |
| Original art and audio through a real pipeline | Assets go from source files into a build by a written process |
| A build a stranger can run | From a clean machine, with a version number |

The course follows the milestones in the [syllabus](../syllabus.md). Weeks 1 to 3 are pre-production: pitch and team, pillars and scope, then the technical design document. Sprint 1 starts in week 4 and ends with a review in week 5. Alpha, beta and the release candidate follow in weeks 10, 13 and 14. The rest of this guide is about the two decisions you make this week.

## 2. Worked example: does the pitch fit the team?

### The hook

In February 2021 Iron Gate released *Valheim* into Steam early access. It was a co-operative survival game for up to ten players, made by a five-person team, and it sold over five million copies in its first month. Small teams ship multiplayer games. What they cannot do is ship a game whose work lands on the one person who can do it. A team of six with one artist has six people's hours and one person's worth of art hours. The pitch has to fit both numbers.

Student teams almost always check only the first one. They add up everyone's hours, compare it with a rough total for the game, see that it fits, and start. Nine weeks later the programmers are waiting for animations and the artist is working weekends.

### The model

Start from PR101 week 1. Each member `i` gives the project `H_i` hours a week outside the studio session. In a team of `n`, each person spends `c` hours a week per communication channel and has `n − 1` channels. Over `W` production weeks, and after holding back a buffer `b` for estimates that run long, member `i` can plan

```
p_i = (1 − b) × (H_i − c × (n − 1)) × W
```

Group people by their **primary discipline** `d` (code, design, art, audio, production). The team's **supply** of discipline `d` is the sum of `p_i` over the people whose primary is `d`. The pitch has a **demand** `q_d`, your first rough estimate of the hours it needs from that discipline. Then

```
supply_d = Σ p_i over members with primary d
load_d   = q_d / supply_d
fits     ⇔  max over d of load_d ≤ 1
```

- `H_i` is weekly hours on the project outside class. The default for this 4-credit course is 8.
- `c` is coordination hours per channel per person per week. Use 0.25 until you have measured your own.
- `W` is production weeks. Weeks 4 to 14 give `W = 11`.
- `b` is the buffer fraction. Start at 0.3 and replace it after sprint 1 (week 5 shows how).
- `load_d` above 1 means the pitch asks discipline `d` for more hours than the team has.

The total check `Σ q_d ≤ Σ supply_d` is **necessary but not sufficient**. A pitch passes only when its worst discipline passes.

### Numbers you can check

Take a team of six, each with `H = 8`, `c = 0.25`, `W = 11`, `b = 0.3`. Each person has 5 channels, so coordination costs 1.25 hours a week, leaving 6.75. Over 11 weeks that is 74.25 useful hours, and 70% of it is 51.975 plannable hours, about 52 per person. The team has two programmers and one person in each other discipline.

The team has two pitches. *Sunken Keep* is a four-player dungeon with three classes, five enemy types, a boss and two zones. *Hollowmarch* is a three-player co-op run through one zone of rooms to a boss, with two classes and three enemy types. Rough demand estimates came from a 20-minute session with the whole team.

| Discipline | People | Supply (h) | Sunken Keep demand | Hollowmarch demand | Hollowmarch load |
|---|---|---|---|---|---|
| Code | 2 | 103.9 | 150 | 95 | 0.91 |
| Design | 1 | 52.0 | 60 | 45 | 0.87 |
| Art | 1 | 52.0 | 120 | 70 | **1.35** |
| Audio | 1 | 52.0 | 40 | 30 | 0.58 |
| Production | 1 | 52.0 | 30 | 25 | 0.48 |
| Total | 6 | 311.8 | 400 | 265 | 0.85 |

*Sunken Keep* fails the total: 400 hours against 311.8, a load of 1.28. Nobody argues about that one.

*Hollowmarch* passes the total with 15% to spare, and this is where teams stop checking. Its art load is 1.35. The artist would need 70 plannable hours and has 52. The code and design loads look healthy only because nobody has yet asked who will animate the three enemies they are scripting.

### Fixing the bottleneck

There are three moves, and they have different prices.

1. **Cut art demand.** The team agrees on one modular tileset for the whole zone and one enemy rig reused by all three enemy types with different colors and weapons. The artist re-estimates art at 48 hours. The load drops to 0.92 and the pitch fits. Total demand falls to 243 hours.
2. **Move work to someone with slack.** Audio sits at 0.58. The audio student's backup skill is art, so they could take UI icons. Work done outside your main skill is slower. If 10 hours of art take 15 in someone else's hands, art falls to 60 hours (load 1.15, still over) and audio rises to 45 (0.87). Moving helps, but here it doesn't finish the job alone.
3. **Add supply.** On a fixed student team you can't hire. You can agree that the artist gets 10 hours a week instead of 8 while others cover the artist's share of meetings. That borrows from another discipline and adds a channel cost the model already charges. Use it last.

The team chose move 1. It went into their pitch sheet as a written decision: "all enemies share one rig; the zone uses one tileset." This decision is part of the pitch now. It limits the design as much as any pillar does, and the designer needs to know it before designing enemy number three.

Run the lab 01 checker on the starter files to reproduce this table. Change the art line from 70 to 48 and it prints `PASS`.

### The same idea elsewhere

**Factories.** Eliyahu Goldratt's *The Goal* (1984) introduced the theory of constraints. Its first idea is the one above. A system's output is set by its slowest step, so improving any other step changes nothing. His first focusing step, "identify the constraint", is what the load column does. His second and third, exploit the constraint and subordinate everything else to it, are moves 1 and 2.

**Team size.** In PR101 week 1 you found that adding a person adds `n − 1` channels, so the best team size is `(H + c) / (2c)`. The load model adds that the *mix* matters as much as the size. A seventh person who is a third programmer lowers code load and raises every coordination cost. It does nothing for art.

**Your jam.** In the PR101 jam, one person probably ended up doing all the sound in the last six hours. That was a load above 1 that nobody computed, fixed by crunch.

### Eyes-open judgment

These numbers are rough. Week 1 estimates are off by 50% in either direction, and PR101 week 6 showed they run long more often than short. So use loads to **compare pitches and find the bottleneck**, not to promise a date. A pitch with every load under 0.8 survives a bad estimate. A pitch at 0.99 is a bet.

Two cases need judgment the model can't give you. A discipline with no primary person has zero supply and infinite load. You can't fix that by moving hours. Either someone becomes that discipline's primary and accepts the learning cost, or the pitch drops that discipline's work. The second case is a pitch whose load is fine but whose one big item is new to everyone, such as networked physics. Load measures hours, not risk. Week 3 deals with risk.

### Check yourself

1. The *Hollowmarch* team adds a seventh member, a second artist with `H = 8`. Recompute one person's plannable hours and the art load for 70 hours of demand. Does the pitch fit without any cut?
2. A team's loads are 0.95, 0.70, 0.60, 0.55, 0.40. The producer suggests cutting 20 hours of audio work "to be safe". What does that do to the largest load, and what would you cut instead?

<details><summary>Answers</summary>

1. With `n = 7`, coordination is `0.25 × 6 = 1.5` hours a week, leaving 6.5. Over 11 weeks that is 71.5 useful hours, and 70% gives 50.05 per person. Two artists supply 100.1 hours, so art load is `70 / 100.1 = 0.70`. It fits, but every other discipline's supply fell from 52 to 50.05, so recheck them all.
2. Nothing. The largest load stays 0.95 because audio was not the constraint. Cut in the discipline at 0.95, or accept that it has no margin and write down which of its tasks go first.

</details>

## 3. Pitching a multiplayer slice

Use the three-minute pitch structure from GD101 week 14 for the team pitch at the end of this session. For the individual pitch fair at the start, cut it to 90 seconds with four parts:

1. **The moment** (20 s). The one thing players remember afterwards, told as a scene.
2. **Why together** (30 s). What two to four players do that one player can't. "You can play with friends" is not an answer. "One player holds the lantern and can't fight, so the others must protect them" is.
3. **One minute of play** (30 s). What each player's hands do, with one decision in it.
4. **The biggest unknown** (10 s). Name the part you are least sure you can build.

The "why together" part decides most pitches in this course. A game that works the same with one player will get a networking layer that costs 30% of the code hours and adds nothing players feel. Look for **interdependence**: roles that need each other, resources one player has and another needs, or events that need two people at once.

Keep the scale honest. An RPG pitch drifts toward classes, crafting, quests, towns and a world map. None of those fit. One zone, one encounter and one progression step is the slice. Everything else goes in a section of the one-pager called "the full game", which you won't build.

## 4. Forming the team

Teams have five to seven members and must cover code, design, art, audio and production. A person can hold more than one role. Every discipline needs a named **primary**, the person who owns that discipline's work, and a **backup**, a different person who can keep it moving for a week if the primary is ill. PR101 week 1 called the number of people who must disappear before work stops the **bus factor**. A discipline with no backup has a bus factor of 1.

Build the **skill matrix** before you choose a pitch. Each person rates themselves from 0 to 3 in each discipline, where 0 is "never done it" and 3 is "could teach it". Then assign primaries and backups from the matrix, not from what people want to do. You can record wants in a separate column and honour them where the matrix allows.

Three patterns cause trouble:

- **Four programmers and a designer.** The load table will show art and audio at infinity. The team either recruits or pitches a game with almost no art, and "almost no art" still needs a UI.
- **The friend group.** Friends form teams quickly and resolve conflict slowly, because nobody wants to be the one who complains. Write the lateness rule in the charter anyway.
- **The absent producer.** Production is a discipline with real hours: running the board, the build and the reviews. A team that gives it to "whoever has time" gives it to nobody.

Then write the **team charter** from PR101 week 1 section 5. Add two lines for this course: who owns the build, and who is the product owner who breaks scope ties.

## 5. Choosing between pitches

By the end of the session each forming team shortlists two or three pitches from the fair and runs the fit test on each. Pick with three questions in order:

1. **Does it fit?** Largest load at or below 1 after at most one written change.
2. **Is "why together" real?** Can you name the moment where one player needs another?
3. **Does someone care?** A pitch that fits and that nobody wants to work on for fifteen weeks will lose to one that is slightly over and loved. Then you fix the loved one's load.

Don't vote by counting hands. Use the fit test to remove pitches, then let the product owner decide between the survivors after hearing everyone.

## Studio session plan

The studio meets for 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:20 | Course brief: the slice requirements, milestones, assessment | Questions answered |
| 0:20 to 1:05 | Pitch fair. Everyone gives a 90-second pitch. Listeners score "why together" from 0 to 2 on a shared sheet | Ranked list of pitches |
| 1:05 to 1:15 | Break | |
| 1:15 to 1:45 | Skill matrix. Everyone fills in the shared matrix. Instructors propose team groupings that cover all five disciplines | Draft teams of 5 to 7 |
| 1:45 to 2:30 | Fit test. Each team picks two or three pitches, estimates demand by discipline in 15 minutes, runs `check_fit.py`, and changes the best pitch until it passes | One pitch at `PASS` |
| 2:30 to 2:50 | Team pitch. Each team pitches its chosen game in 90 seconds, then states its bottleneck discipline and the change that fixed it | Instructor sign-off or a named concern |
| 2:50 to 3:00 | Charter started, roles assigned, first meeting booked | Charter draft in the repository |

## Deliverables

Due before next week's studio session. Put everything in your team repository under `docs/`.

- **Team charter** (one page), with RACI for the pre-production milestones, the build owner and the product owner.
- **Skill matrix** (`team.csv` in the lab 01 format) with a primary and a backup for every discipline.
- **Pitch one-pager** using the GD101 week 14 template, plus the "why together" paragraph and the "full game" section.
- **Fit sheet** (`pitch_demand.csv`) and the output of `check_fit.py` showing `PASS`, with each change you made to reach it written as a decision.

The instructor checks them by running the checker on your files and reading the decisions. See [lab 01](../labs/lab01.md).

## Common failure modes

- **Checking only the total.** The team compares total hours and never looks at the discipline with one person. Fix: the checker prints every load, so read the whole column.
- **Designing for the team you wish you had.** The pitch assumes animation from someone who has never animated. Fix: use the skill matrix, and put learning time into the demand.
- **"Why together" is chat.** The only multiplayer feature is seeing each other. Fix: find one moment where a player cannot succeed alone, and build the pitch around it.
- **Demand estimated by one person.** The programmer estimates art. Fix: each discipline's primary estimates their own line.
- **The charter as a formality.** It is written in five minutes and never read. Fix: make the lateness rule and the scope tie-breaker specific enough that you could apply them today.

## Review checklist

The instructor signs off the pitch at the start of week 2 when the items below hold. Milestone 1 marks them together with the week 2 scope sheet ([M1 brief](../assessments/m1-pitch-and-preproduction-brief.md)):

- [ ] Every discipline has a primary and a different backup.
- [ ] `check_fit.py` prints `PASS` on the submitted files, with the default parameters or with changes the team has justified in writing.
- [ ] Every change made to reach `PASS` appears in the pitch as a design constraint.
- [ ] The pitch names a moment of interdependence between players.
- [ ] The slice stays within one zone, one encounter and one progression step.
- [ ] The charter names the build owner, the product owner and a lateness rule.
- [ ] The biggest unknown is named and owned by someone.

## Sources

- Wikipedia, "Valheim" (accessed September 2026). Developer Iron Gate Studio; early access release on 2 February 2021; made by a five-person team; co-operative play for up to ten players; over five million copies sold a month after release.
- Wikipedia, "Theory of constraints" (accessed September 2026). Introduced by Eliyahu M. Goldratt in *The Goal* (1984); the five focusing steps (identify, exploit, subordinate, elevate, repeat).
- Brooks, F. P. (1975, anniversary ed. 1995). *The Mythical Man-Month*. Addison-Wesley. Chapter 2 on communication overhead, as used in PR101 week 1.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Background on cross-discipline teams.
- The *Hollowmarch* team (six people, followed through all 14 weeks), the two pitches and all hour figures in section 2 are invented for teaching. The default values for `H`, `c`, `W` and `b` are course conventions, not measurements.
