# PR301 · Week 01 — Pitch and World Pillars

**Why this matters:** In PR201 you built 15 minutes of game that a stranger played once. This course asks for a world that 50 people live in for a weekend and come back to. That one change flips which pitches are cheap and which are ruinous. A story-led pitch that was the safe choice for a slice becomes the expensive choice for a persistent world, and you can show it with one line of arithmetic before anyone writes code.

**You will be able to:**
- Write three world pillars that each rule out at least one feature a teammate wants.
- Compute a persistent-world pitch's demand from its platform, system and authored-content costs and its replay factor.
- Find the break-even play time at which a systemic pitch becomes cheaper than an authored one.
- Change a pitch until its load is at or below 0.9, and record each change as a design constraint.

**Before class:** Reread [MMO301 week 11, Koster's laws of online world design](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w11-kosters-laws-of-online-world-design.md) and [MMO301 week 7, themepark vs sandbox](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w07-themepark-vs-sandbox.md). Skim [MMO306 week 1, the content treadmill](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w01-the-content-treadmill-production-vs-consumption.md), which you are taking alongside this course. Bring your PR201 team's final sprint record (points or hours committed and done) and one world idea on half a page.

**Prerequisites from earlier courses:** [PR201 week 1](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w01-pitch-and-team-formation.md) for the supply and load model and the skill matrix. [PR201 week 2](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w02-pre-production-pillars-and-scope.md) for pillars that decide things and the cut line. [MMO302 week 1](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md) for what 50 concurrent players cost a server. [MMO305 week 3](../../MMO305-social-systems-and-online-behaviour/lectures/w03-forced-vs-voluntary-grouping.md) for grouping that players choose rather than suffer.

---

## 1. What this course asks you to ship

By week 15 your team runs a **persistent world prototype**: a small online world whose state survives when players log out and when the server restarts. The single course outcome is concrete. The world must support 50 or more concurrent test players. Everything below follows from that sentence.

| Requirement | What it means in practice |
|---|---|
| Persistent | Characters, items and currency survive logout and a server restart. Proven by a restart during a playtest |
| 50+ concurrent players | Load-tested with bots at twice that (week 2), then played by real people at alpha (week 9) and beta (week 13) |
| An economy | At least one currency with named faucets and sinks ([MMO304 week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md)) and one way for players to trade or craft |
| Grouping | Players can form a party that shares something: credit, loot, a chat channel |
| One group encounter | A fight or event a solo player cannot finish |
| Server-authoritative | As in PR201. The client sends intent, the server decides |

The schedule has a rhythm. Weeks 1 and 2 are pre-production, with the pitch this week and a technical architecture review next week. Three two-week sprints follow. Each runs from one planning session to the next: sprint 1 from week 3 to week 5, sprint 2 from week 5 to week 7, and sprint 3 from week 7 to week 9. The sprint review takes the first part of the next planning session, so sprint 1 is reviewed at the start of week 5, sprint 2 at the start of week 7 and sprint 3 at the start of week 9. The week 4, 6 and 8 sessions fall mid-sprint. Each holds a stand-up, a playtest or load test and a burn-down check, around its own topic (soak testing, tick budgets, the alpha go/no-go). Week 9 is the first **persistent weekend**, an alpha where the world stays up from Friday to Sunday and the class plays it. Week 10 reads the telemetry from that weekend. Sprints 4 and 5 add social systems and the group encounter. Week 13 is an open beta, week 14 is stabilization, and week 15 is the showcase and post-mortem. The [syllabus](../syllabus.md) gives the three assessment components (milestones 50%, final world 30%, post-mortem and peer review 20%). The table in the [milestone 1 brief](../assessments/m1-pitch-and-pillars-brief.md) splits them into each milestone's weight, and every brief in `assessments/` states its own.

Teams carry over from PR201 where they can. A team that changes membership reruns the skill matrix from PR201 week 1 today.

## 2. Worked example: which pitch can a team of seven afford?

### The hook

Raph Koster's laws of online world design include one called "storytelling versus simulation". It says that any static story in an online world will be known to everyone within days, and that a design team cannot produce stories fast enough to supply everyone playing. You met the law in MMO301. Now you have to budget against it.

PR201 never tested it. A 15-minute slice is played once per tester, so a hand-built quest costs the same whether it holds one player or fifty. A persistent weekend is different. Each tester may play six hours, and everything they finish is gone for them. The team that pitched a lovingly written quest chain in PR201 and won will pitch one again this week. This example shows why it may now lose.

### The model

Start from the PR201 week 1 supply model, now for a whole team. With `n` people, each giving `H` hours a week, `c` hours per communication channel, `W` production weeks and a buffer `b`:

```
supply   = n × (1 − b) × (H − c × (n − 1)) × W
```

Split the pitch's demand into three parts.

```
authored = T / r
demand   = P + F + k × authored
load     = demand / supply
```

- `T` is the **target play hours** per player: how long one tester should be able to play before running out. For the alpha weekend use 6.
- `r` is the **replay factor**: how many hours of play one hour of authored content supports before it is stale. A quest played once has `r` close to 1. A mob camp, a gathering route or a crafting loop that players repeat has a larger `r`. MMO306 week 1 uses the same `r`.
- `authored` is the hours of content the team must build so a player can reach `T`.
- `P` is **platform** hours: server, login, persistence, grouping, the group encounter. Every pitch in this course pays it.
- `F` is **system** hours: the fixed cost of the machinery the pitch needs (a quest and dialogue system, a crafting system, respawn logic).
- `k` is the build cost of one authored content hour, in team hours.

The pitch passes when `load ≤ 0.9`. PR201 used 1.0 as the line. A persistent world has more parts that must all work together at the alpha, so this course keeps a 10% margin.

Setting two pitches' demands equal gives the **break-even play time**. Pitch A (authored-heavy) and pitch B (systemic) cost the same when

```
P + F_A + k_A × T / r_A = P + F_B + k_B × T / r_B
T* = (F_B − F_A) / (k_A / r_A − k_B / r_B)
```

Below `T*` the authored pitch is cheaper. Above it the systemic one is.

### Numbers you can check

A team of seven, each with `H = 8`, `c = 0.25`, `W = 12` (weeks 3 to 14) and `b = 0.3`. Each person has 6 channels, costing 1.5 hours a week, which leaves 6.5. Over 12 weeks that is 78 hours, and 70% of it is 54.6 plannable hours each.

```
supply = 7 × 0.7 × 6.5 × 12 = 382.2 hours
```

The team has two pitches. Both share the same platform estimate, `P = 110` hours.

*Lantern Coast* is a harbour town with a quest chain about a missing lighthouse keeper. It needs a quest and dialogue system (`F = 120`), and quests replay poorly (`r = 1.2`).

*Saltmarsh* is a marsh settlement where players hunt, gather reeds and salt, and craft gear that decays. It needs gathering, crafting and respawn systems (`F = 200`), and its loops repeat (`r = 4`).

Both teams estimate `k = 45` hours to build one hour of content (a quest, or a camp with its route and drops). The figure is the team's own guess from PR201, not an industry number.

| | Lantern Coast | Saltmarsh |
|---|---|---|
| Authored hours `6 / r` | 5.00 | 1.50 |
| Platform `P` | 110 | 110 |
| Systems `F` | 120 | 200 |
| Content `45 × authored` | 225 | 67.5 |
| Demand | 455.0 | 377.5 |
| Load (`/ 382.2`) | **1.19** | 0.99 |

*Lantern Coast* fails outright. Five hours of hand-built quests is more content than this team can make in a semester, before anyone has touched the economy.

*Saltmarsh* costs more to start (200 system hours against 120) and still wins, because its content goes four times as far. Its load is 0.99, which is not a pass. It is a bet.

The break-even play time is

```
T* = (200 − 120) / (45 / 1.2 − 45 / 4) = 80 / (37.5 − 11.25) = 80 / 26.25 = 3.05 hours
```

Below about three hours per player the quest pitch is cheaper. That is why it was the right call in PR201, where `T` was a quarter of an hour. Above three hours the systemic pitch is cheaper, and the gap grows by 26.25 hours for every extra hour of play you promise.

### Fixing the load

The *Saltmarsh* team has three moves.

1. **Cut system cost.** Crafting had three tiers of recipes. The designer cuts it to two, and the programmers re-estimate systems at `F = 160`. Demand falls to 337.5 and the load to 0.88. The pitch passes.
2. **Raise replay.** Make the camps and gathering routes feed the economy, so a player has a reason to go back (a material only one camp drops). This raises `r`, but the team cannot measure `r` until the alpha. Don't bank it yet.
3. **Lower the target.** A four-hour target would cut authored hours to 1.0. It would also mean testers run out on Saturday afternoon of a weekend that lasts until Sunday.

They choose move 1 and write it into the pitch as a constraint: "Crafting has two tiers. A third tier is out of scope for PR301." The designer now knows it before designing recipe number twelve.

The model also shows how fragile the pass is. If the alpha shows that players only repeat the camps three times, not four, authored hours rise to 2.0 and demand to 360, a load of 0.94. The pitch would be over the margin again. That sensitivity is why the week 10 telemetry review measures `r` directly.

Run `check_budget.py` from [lab 01](../labs/lab01.md) on the starter file to reproduce the table. Change *Saltmarsh*'s `system_hours` from 200 to 160 and it prints `PASS`.

### The same idea elsewhere

**EVE Online.** CCP's sandbox leans as far toward systems as any shipped MMO. Characters gather the raw materials for, and manufacture, almost all of the ships and modules in the game. Every ship destroyed in a fight is demand for a manufacturer. The fixed cost of those systems is enormous, and they have produced play for two decades without CCP writing a quest for each hour of it. In the model, `F` is huge and `r` is effectively unbounded.

**Guild Wars 2.** ArenaNet's dynamic events are authored content built to repeat. They are cyclical, restarting after they succeed or fail, often chained into longer meta-events, and they scale up and down with the number of players nearby. An event is a quest with a higher `r`: written once, replayed by each player many times and by many players at once.

**MMO306, week 1.** The content treadmill puts a clock on the same idea. There, a live team's exhaustion time `T = 7 × C × r / h` asks how long one content drop lasts. Here, `authored = T / r` asks how much you must build before the first drop exists. Same `r`, different question.

### Eyes-open judgment

Systemic pitches have their own failure. The fixed cost `F` is paid before any of it is fun, and a crafting system with no reason to craft is 160 hours of spreadsheets. The model assumes `r` arrives. It only arrives if the systems connect. The camp drops the reed, the reed makes the net, the net catches the fish the town buys. A systemic pitch must name that loop in one sentence, or its `r` is a hope.

Authored content is also not the enemy. One well-written moment gives a world its identity, and players remember it. The usual answer in shipped games is a systemic floor with a thin authored layer on top. For your budget that means one short quest chain as the front door to the systems, costed at `r = 1`.

Finally, `k = 45` came from a PR201 slice built by a different mix of people. Use it to compare pitches this week and replace it after sprint 1, when you have measured your own.

### Check yourself

1. A third pitch, *Ironfen*, has `F = 150` and `r = 2.5`, with the same `P` and `k`. Compute its load at `T = 6`. Does it pass the 0.9 margin?
2. The *Lantern Coast* team argues that its quests have `r = 2` because players will do them on two characters. Recompute its load. Would you accept the argument?
3. At what target play time `T` do *Lantern Coast* (`F = 120`, `r = 1.2`) and the cut *Saltmarsh* (`F = 160`, `r = 4`) cost the same?

<details><summary>Answers</summary>

1. Authored hours are `6 / 2.5 = 2.4`. Demand is `110 + 150 + 45 × 2.4 = 368`, and the load is `368 / 382.2 = 0.96`. It fails the margin.
2. Authored hours become 3, demand `110 + 120 + 135 = 365`, load 0.95. It still fails. The argument is also weak. Replaying a quest on an alt is a hope about a small share of players, and the value of `r` is an average over all of them.
3. `T* = (160 − 120) / (37.5 − 11.25) = 40 / 26.25 = 1.52` hours. Cutting the systemic pitch's fixed cost moved the break-even earlier.

</details>

## 3. Pillars for a world, not a slice

PR201 week 2 defined a pillar as a short statement that decides between two reasonable options. A pillar that decides nothing is decoration. For a persistent world, write three pillars and test each against the course requirements.

Each pillar needs three parts.

1. **The statement.** "The marsh feeds the town." Short enough to say in a meeting.
2. **What it rules in.** Gathering routes that end at the town market. Recipes that need materials from more than one camp.
3. **What it rules out.** At least one feature a teammate has asked for. "No fast travel between the camps and the town." If nothing on your wish list dies, the pillar is not doing work.

Test each pillar against the persistent-world requirements. A world pillar should say something about at least one of these:

- **Why come back tomorrow?** What changes overnight or accumulates while a player is away. This is the pillar that turns a slice into a world.
- **Why stand near other players?** Where paths cross, and what one player can offer another. [MMO305 week 3](../../MMO305-social-systems-and-online-behaviour/lectures/w03-forced-vs-voluntary-grouping.md) showed that grouping players choose lasts longer than grouping you force.
- **Where does money go?** A world with faucets and no sinks has inflation by Sunday afternoon. MMO304 teaches the sink catalogue. Your pillar only has to promise one sink the players will care about.

A good test is to hand your three pillars to another team and ask them to rule on two features from your backlog. If they rule the way you would, the pillars work.

## 4. The persistence promise

Before the week 2 review, the team writes down what the world promises to keep. This is a short list, not a schema. For each kind of state, say whether it survives logout, whether it survives a server restart, and how much of it a player may lose in a crash.

| State | Survives logout | Survives restart | Acceptable loss in a crash |
|---|---|---|---|
| Character level, gear, gold | Yes | Yes | None |
| Position in the world | Yes | Yes | Up to a minute of walking |
| Mob health mid-fight | No | No | All of it |
| Gathered nodes and respawn timers | n/a | No | All of it |
| Market listings | Yes | Yes | None |

The last column decides the architecture. "None" means the change is written through to the database inside a transaction, which you costed in [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) and built in [DB201 week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md). "Up to a minute" allows a periodic save. Next week's review checks your architecture against this table, so be deliberate. Every "None" costs engineering hours.

## 5. Choosing and committing

Each team shortlists two or three world pitches, runs the budget on each, and keeps the ones that pass after at most one written change. Then decide in the order PR201 used. Does it fit, is the reason to play together real, and does someone on the team want to build it for fourteen weeks? Rerun the PR201 discipline check too. The budget above is a team total, and a systemic pitch loads programmers and designers more than artists. The PR201 lab 01 checker still works for that.

## Studio session plan

The studio meets for 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:20 | Course brief: the persistent world requirements, sprint rhythm, the persistent weekend | Questions answered |
| 0:20 to 0:50 | Team check: rerun the PR201 skill matrix for any changed team; set `H`, `n` and your measured `k` from PR201 | Updated `team.csv` |
| 0:50 to 1:30 | Pitch round. Each person gives a 90-second world pitch ending with "why come back tomorrow" | Two or three shortlisted pitches per team |
| 1:30 to 1:40 | Break | |
| 1:40 to 2:20 | Budget. Estimate `P`, `F`, `k` and `r` for each shortlisted pitch, run `check_budget.py`, change the best pitch until it passes | One pitch at `PASS` |
| 2:20 to 2:45 | Pillars and persistence promise drafted; swap pillars with a neighbour team, who rule on two of your backlog features | Pillars tested |
| 2:45 to 3:00 | Instructor sign-off round: each team states its load, break-even `T*` and the change it made | Sign-off or a named concern |

## Deliverables

Due before the week 2 session, in `docs/pitch/` in the team repository.

- **World one-pager**: the pitch, the loop in one sentence, and the "why come back tomorrow" paragraph.
- **Three pillars**, each with what it rules in and what it rules out.
- **Budget sheet** (`pitches.csv`) and the saved output of `check_budget.py` showing `PASS`, with every change written as a constraint.
- **Persistence promise** table as in section 4.
- **Updated `team.csv`** with a primary and backup for every discipline.

The instructor reruns the checker on your CSV and reads the constraints. See [lab 01](../labs/lab01.md).

## Common failure modes

- **Pitching the PR201 game again.** The slice was good, so the team pitches its sequel. Fix: run the budget. A 15-minute slice rarely survives a six-hour target unchanged.
- **Replay by assertion.** The team sets `r = 6` because "players love crafting". Fix: `r` above 3 needs a named loop that connects at least two systems. Otherwise use 2.
- **Pillars that rule out nothing.** "Fun combat" and "a living world" survive any backlog. Fix: each pillar must kill a feature someone wanted.
- **Every state is precious.** The persistence promise says "None" for everything, including mob health. Fix: keep "None" for things a player would complain about losing.
- **Platform at zero.** The budget forgets login, persistence and the group encounter because "we did networking in PR201". Fix: every pitch pays `P`. Next week's review will check the number.

## Review checklist

The instructor signs off the pitch milestone when:

- [ ] `check_budget.py` prints `PASS` on the submitted file with the default parameters, or with changes justified in writing.
- [ ] Each change made to pass is written into the one-pager as a constraint.
- [ ] Any `r` above 3 is backed by a named loop between two systems.
- [ ] Each pillar rules out at least one named feature.
- [ ] The world has one faucet and one sink named, and one reason for players to group.
- [ ] The persistence promise covers characters, items, currency and position.
- [ ] Every discipline has a primary and a different backup.

## Sources

- Koster, R. "The Laws of Online World Design" (raphkoster.com, read September 2026). The law "storytelling versus simulation", paraphrased in section 2; also "persistence means it never goes away". Laws collected from several authors between the late 1980s and early 2000s.
- Wikipedia, "Eve Online" (read September 2026). Released in 2003; characters gather raw materials to manufacture almost all ships and modules; a single shared world with unscripted economic competition.
- Guild Wars 2 Wiki, "Event" (read September 2026, current game). Dynamic events are cyclical, often chained into meta-events, and scale up and down with the number of players participating or nearby.
- Wikipedia, "Guild Wars 2" (read September 2026). Developed by ArenaNet, released 28 August 2012; a dynamic event system replaces traditional questing.
- The team, the pitches *Lantern Coast* and *Saltmarsh*, and all hour figures in section 2 are invented for teaching. The defaults for `H`, `c`, `W`, `b` and the 0.9 margin are course conventions, not measurements.
