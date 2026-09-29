# MMO407 · Week 08 — Case: EVE's large-scale events

**Why this matters:** Most launches have one peak you can plan for. EVE Online has player-made peaks every few months, when two coalitions decide to throw everything they own into one star system. The server survives them by slowing time. This week shows the side effect that the time-dilation formula does not see: a slow fight lasts longer in real time, a longer fight gives reinforcements time to arrive, and more pilots make the fight slower still. You learn to model that loop, to read EVE's battle reports as post-mortems, and to choose the levers that keep a player-scheduled event from growing past what your hardware can serve.

**You will be able to:**
- Compute the real length, final headcount and pilot-hours of a dilated battle when reinforcements arrive in real time, and compare them with an undilated fight.
- Explain why halving the arrival rate or doubling node capacity shortens a dilated fight by more than half, while shrinking the pool of available pilots barely changes its length.
- Evaluate the levers an operator and a designer control (arrival friction, objective size, real-time deadlines, node capacity) with numbers from the model.
- Extract transferable lessons from EVE's battle reports and post-battle coverage for any game where players schedule their own peaks.

**Before class:** CCP Convict, "Fury at FWST-8 Battle Report" (EVE Online news, 2020), the timeline section (10 minutes). Steven Messner, "Why EVE Online's million dollar battle was a huge bust" (PC Gamer, 25 January 2018) (10 minutes). Reread MMO302 week 12 sections 2 and 4. You need the dilation model and the list of clocks that do not dilate, and neither is re-taught here.

**Prerequisites from earlier courses:** [MMO302 week 12, single-shard architectures and time dilation](../../MMO302-mmo-server-architecture/lectures/w12-single-shard-architectures-and-time-dilation.md) (the load model `W(n) = a n + b n²`, the speed `f = clamp(C / W(n), f_min, 1)`, the backlog past the floor, and which clocks dilate; this week uses its invented constants unchanged). [MMO404 week 7, time dilation revisited](../../MMO404-advanced-networked-simulation/lectures/w07-time-dilation-revisited.md) (the fleet fight notification and node reinforcement; this week does not repeat them). [MMO404 week 6, massive battles](../../MMO404-advanced-networked-simulation/lectures/w06-massive-battles.md) (what a big fight costs in bandwidth). [MMO402 week 4, wars, betrayals and meta-gaming](../../MMO402-emergent-society-governance-and-ethics/lectures/w04-wars-betrayals-and-meta-gaming.md) (B-R5RB's real-money value; not recomputed here). [Week 1 of this course](w01-launch-day-anatomy.md) (why a rejecting stage gets narrower).

**Interactive:** [examples/w08-battle-escalation.html](../examples/w08-battle-escalation.html). Keep it open during section 2.

---

## 1. Peaks the players schedule

EVE Online runs one universe, Tranquility, for almost all of its players. It set its record for concurrent players, 65,303, on 5 May 2013. Most of those players spread across thousands of star systems. A **large-scale event** is what happens when several thousand of them decide to be in the same system at the same time.

Nobody at CCP schedules these events. Players do, through the game's own rules. When an attacker damages a player-owned structure enough, the structure enters a **reinforcement** state and becomes vulnerable again at a known later time, often days away. Both sides now know when and where the decisive fight will be. They spend the days in between calling in allies. Some wars are years in the making, and the fight at the final timer is the payoff.

For an operator, that is both a blessing and a hazard. It is a blessing because the peak is announced in advance, which is why CCP lets fleet commanders file a fleet fight notification and moves the named systems onto dedicated nodes (MMO404 week 7). It is a hazard because players choose the size, and every side has a reason to bring more than the other.

The records show how large the choice can get.

| Battle | When | Pilots in the system at peak | Real length | What limited it |
|---|---|---|---|---|
| 6VDT-H | July 2013 | 4,070 | — | Time dilation at its floor for most of the fight (MMO302 week 12) |
| B-R5RB | 27-28 January 2014 | 2,670 (6,058 in the system over the fight, 7,548 overall) | about 21 hours | Time dilation at its 10% floor |
| 9-4RP2 | January 2018 | about 6,100 | a few hours | Players could not act; the attack was abandoned |
| FWST-8 | 6-7 October 2020 | 6,557 (8,825 over the fight) | 11 hours 44 minutes of shooting the structure | Time dilation at its floor throughout |
| M2-XFE | 31 December 2020 | about 5,000 involved | about 14 hours | Ended with the daily downtime |

Two limits appear again and again: the time-dilation floor, and the **daily downtime**, a 15-minute maintenance window at 11:00 UTC when the whole cluster goes offline and every player is logged out. Keep both in mind. Section 3 shows that they are the two most important controls on the loop you are about to model.

## 2. Worked example: the fight that grows because it is slow

### The hook

CCP's report on the battle for FWST-8 gives a timeline. On 6 October 2020, the defending coalition's fleet landed at 16:34 UTC. By 16:52 more than 4,000 pilots were in the system. By 17:36 more than 6,000. The peak, 6,557, came at 18:16, a new Guinness World Record for the most concurrent participants in a video game PvP battle. The report says time dilation set in almost immediately and stayed at its maximum for the entire battle. The attackers then shot the structure for 11 hours and 44 minutes, destroying it at 05:27 the next morning.

At normal speed, the destruction of a structure of that size is a few hours of shooting at most. At one tenth speed it took most of a night, and the headcount kept rising while it did. Ten weeks later, at M2-XFE, a member of one coalition described the fight to IGN as both sides escalating to the absolute maximum of their resources. Here is the puzzle. MMO302 showed that time dilation keeps a crowded node consistent. Does it also make the crowd bigger?

### The model

Take one node and one fight. Step forward one real minute at a time.

```
f(n)       = clamp(C / (a n + b n²), f_min, 1)     game speed (MMO302 week 12)
game(t+1)  = game(t) + f(n(t))                     game-minutes of fighting done
n(t+1)     = min(pool, n(t) + r)                   pilots in the system
the fight ends when game ≥ G;  T is the real minute it ends
pilot-hours = Σ n(t) / 60
```

- `n` is the number of pilots in the system, starting at `n0`.
- `r` is the **arrival rate**, pilots joining per real minute. Reinforcements travel, dock, undock and jump on real clocks. Nobody's alarm clock dilates.
- `pool` is the number of pilots who could come at all.
- `G` is the **objective size**, the game-minutes of fighting needed to decide the fight, for example the time to grind through a structure's hit points.
- `f`, `C`, `a`, `b` and `f_min` are MMO302's. This lecture uses its invented constants unchanged: `a = 0.3` ms, `b = 1` µs, `C = 1` CPU-second per real second, `f_min = 0.1`. They are not CCP's measurements.

The model has one new idea. MMO302 computed the real length of a fight of fixed size as `G / f`. Here the size is not fixed. **Real time brings pilots. Game time ends the fight.** When the fight slows, the gap between the two clocks is filled with reinforcements, and each reinforcement slows the fight further. That is a loop, and loops are what this course keeps finding at the root of launch failures.

### Numbers you can check

The lecture battle starts with 1,000 pilots, adds 20 per real minute up to a pool of 6,000, and needs 60 game-minutes of fighting.

| Real minute | Pilots `n` | Work `W(n)` (CPU-s per game-s) | Speed `f` | Game-minutes done |
|---|---|---|---|---|
| 0 | 1,000 | 1.30 | 0.769 | 0.0 |
| 20 | 1,400 | 2.38 | 0.420 | 11.5 |
| 40 | 1,800 | 3.78 | 0.265 | 18.3 |
| 60 | 2,200 | 5.50 | 0.182 | 22.7 |
| 80 | 2,600 | 7.54 | 0.133 | 25.8 |
| 100 | 3,000 | 9.90 | 0.101 | 28.2 |
| 120 | 3,400 | 12.58 | 0.100 (floor) | 30.2 |

Check any row by hand. At 2,200 pilots, `W = 0.0003 × 2,200 + 0.000001 × 2,200² = 0.66 + 4.84 = 5.50`, so `f = 1 / 5.5 = 0.182`. The last column is the running sum of `f`, one value per minute.

At minute 60 an undilated server would already be done. This one has done 22.7 game-minutes of the 60, and it has 1,000 more pilots than it would have had.

You can estimate the ending by hand in two phases. The speed hits its floor at about 3,020 pilots, around minute 101, with about 28.3 game-minutes done. After that the fight advances at exactly 0.1 game-minutes per real minute, so the remaining 31.7 game-minutes take about 317 real minutes. Total, about 418 minutes. The simulation says 419:

```python
A_COST, B_COST, FLOOR = 0.0003, 0.000001, 0.1     # MMO302 week 12's invented constants

def speed(n, C=1.0):
    """Game speed f for n pilots on a node of capacity C (MMO302 week 12)."""
    return max(FLOOR, min(1.0, C / (A_COST * n + B_COST * n * n)))

def battle(n0=1000, r=20, G=60, pool=6000, C=1.0, deadline=None, dilate=True):
    """Real minutes until G game-minutes of fighting are done.
    Reinforcements arrive at r pilots per real minute until the pool is empty."""
    n, game, t, pilot_min = n0, 0.0, 0, 0
    while game < G and (deadline is None or t < deadline):
        game += speed(n, C) if dilate else 1.0
        pilot_min += n
        t += 1
        n = min(pool, n + r)
    return t, n, pilot_min / 60, game

for label, kw in [("no dilation needed", {"dilate": False}),
                  ("lecture battle", {}),
                  ("half the arrivals", {"r": 10}),
                  ("smaller pool", {"pool": 3000}),
                  ("node twice as fast", {"C": 2.0}),
                  ("hard stop at 240 min", {"deadline": 240})]:
    t, n, ph, game = battle(**kw)
    print(f"{label:20s} {t:4d} min  {n:5d} pilots  {ph:7,.0f} pilot-hours  {game:5.1f} game-min")
```

Output:

```
no dilation needed     60 min   2200 pilots    1,590 pilot-hours   60.0 game-min
lecture battle        419 min   6000 pilots   31,442 pilot-hours   60.1 game-min
half the arrivals     240 min   3400 pilots    8,780 pilot-hours   60.0 game-min
smaller pool          416 min   3000 pilots   19,117 pilot-hours   60.1 game-min
node twice as fast    146 min   3920 pilots    5,962 pilot-hours   60.0 game-min
hard stop at 240 min  240 min   5800 pilots   13,560 pilot-hours   42.2 game-min
```

Read the first two lines together. The same fight, needing the same 60 game-minutes, lasts 60 real minutes on a server that never needs to dilate and 419 on ours. It ends with 6,000 pilots instead of 2,200, and it consumes 31,442 pilot-hours instead of 1,590, twenty times as much. None of that comes from players deciding to fight longer. It comes from the loop.

The other lines are the levers, and they are uneven. Halving the arrival rate cuts the fight from 419 to 240 minutes, and the pilot-hours by 72%. Doubling the node's capacity cuts it to 146 minutes, because a faster node stays above the floor longer, so fewer reinforcements arrive before the end. Halving the pool barely changes the length (416 minutes). Once the fight is at the floor, extra pilots do not slow it further in this model. They only make it heavier, and past the floor MMO302's backlog begins to grow, so commands arrive late. The hard stop ends the fight on time but undecided, with 42 of the 60 game-minutes done.

### Move it yourself

Open the interactive. The top chart shows pilots in the system against real time, with the undilated fight drawn as a short grey line that ends at minute 60. The bottom chart shows game-minutes done against real time, with a dashed line at `G`. Where the game-time curve bends flat, the pilot curve is still rising. That is the loop, visible as two curves pulling apart. Drag the arrival rate from 20 down to 5 and watch the fight end at minute 119 with 1,595 pilots. Then set it back to 20 and double `C`. The fight shortens by two thirds with no change in player behaviour.

### Cross-game recognition

The shape to look for is a mitigation that stretches an event, while demand for the event arrives on the real clock.

**EVE Online, B-R5RB (January 2014) and M2-XFE (December 2020).** B-R5RB began because a corporation missed a routine sovereignty payment, so the system became open to capture on a Monday working day. Wikipedia's account, drawing on CCP's report, says each side then tried to rush every available pilot into the system as time dilation engaged, and the fight ran for about 21 hours. M2-XFE also ended at downtime, after about 14 hours. In both, `r` stayed high for hours because the fight was still undecided, and it was undecided because it was slow.

**Diablo III (launch, May 2012).** Week 1 showed how the authentication stage rejected players, and each rejected player clicked retry, so the stage's offered load grew above the true arrival rate. The mitigation (reject rather than queue) created more demand for the stage it was protecting. The loop is the same shape. A fight that slows down draws more pilots, and a login stage that rejects draws more retries.

**Outside games: induced demand on roads.** Transport economists find that when a road gets faster, traffic grows to fill it. Reviews of the research put the elasticity of traffic with respect to travel time at around −0.5 in the short run and −1.0 in the long run. Duranton and Turner (2011) found that vehicle-kilometres travelled in US cities rise about one for one with new road capacity. It is the same loop with the sign turned around. A road that gets faster draws more cars, and a fight that gets slower draws more pilots. In both, the demand responds to the service, so you cannot size the service from demand measured before the change.

### Eyes-open design judgment

- **Dilation is still the right call for EVE.** MMO302 compared the alternatives. A cap turns people away from a fight they spent months preparing for, and copies break the single shard's promise. The loop does not argue against dilation. It argues for pricing in the side effect and adding a second control.
- **The expensive part is the arrival rate, not the headcount.** In the model, shrinking the pool leaves the length almost unchanged, while halving `r` cuts it by 43%. Designers control `r` through travel rules. CCP's jump fatigue, added in the Phoebe release in 2014, makes capital ships wait longer after each long jump. Since the fatigue decays in real time, a long dilated fight still gives it time to wear off, so the lever is weaker in exactly the fights where it matters.
- **Capacity buys more than its ratio.** Doubling `C` gave a 2.9-times shorter fight, because it moved the whole fight away from the floor. When you size hardware for player-scheduled peaks, measure what capacity does to the event's length, not only its speed. This is why the fleet fight notification (MMO404 week 7) is worth so much.
- **A real-time deadline caps the loop, and picks a winner.** The daily downtime ends every fight by 11:00 UTC. That bounds real length, but the outcome now depends on who was ahead when the clock ran out. MMO302 week 12 warned that any real-time timer during a dilated fight is a lever players will pull. The downtime is the biggest one in the game.

### Check this example

1. With the lecture's constants, what is the speed at 2,500 pilots? How many real minutes does one game-minute take?
2. The objective shrinks from 60 to 30 game-minutes, everything else unchanged. Estimate the real length with the two-phase method, then compare with the model's answer of 119 minutes.
3. A studio proposes to halve the pool of pilots who can join by adding an entry limit per alliance. Using the model, will fights get shorter? What will get better?

<details>
<summary>Answers</summary>

1. `W = 0.75 + 6.25 = 7.0`, so `f = 1 / 7 = 0.143`. One game-minute takes 7 real minutes.
2. From the table, the fight has 28.2 game-minutes done at minute 100 and is almost at the floor. The last 1.8 game-minutes at 0.1 take about 18 more minutes, so the estimate is about 118 minutes. The model says 119, with 3,380 pilots at the end. Halving the objective cut the length by 72%, because the shorter fight ends before the long stretch at the floor.
3. Barely. Halving the pool from 6,000 to 3,000 changes the length from 419 to 416 minutes, because once the fight sits at the floor, extra pilots do not slow it further. What improves is the load past the floor: 3,000 pilots is near where the floor still covers the work, while 6,000 builds a growing backlog, so commands would arrive on time instead of minutes late. Pilot-hours also fall by about 40%.

</details>

## 3. The levers, side by side

Every lever in the model belongs to someone. Some belong to the operator, some to the game designer, and one belongs to the calendar.

| Lever | Model parameter | Who controls it | Effect in the model (from 419 min, 6,000 pilots) | Cost |
|---|---|---|---|---|
| Faster node | `C` × 2 | Operator, if warned in advance | 146 min, 3,920 pilots | Hardware, and a notice system players must use |
| Travel friction | `r` ÷ 2 | Designer | 240 min, 3,400 pilots | Slower response for defenders everywhere, every day |
| Smaller objective | `G` ÷ 2 | Designer | 119 min, 3,380 pilots | Structures matter less, and wars move faster |
| Real-time deadline | stop at 240 | Designer or schedule | 240 min, undecided at 42 of 60 game-min | Who wins depends on the clock, not the fight |
| Smaller pool | `pool` ÷ 2 | Designer (entry limits) | 416 min, 3,000 pilots | Turns away players, with little gain in length |

Two rows deserve more thought.

**Objective size is the most powerful design lever, and the most visible.** Doubling `G` to 120 game-minutes in the model makes the fight last 1,019 real minutes, about 17 hours. The relationship is far from linear, because a bigger objective spends more of its length at the floor, where the loop has already run to its end. Structure hit points look like a balance number. In a dilated game they are also a capacity number.

**The real-time clocks are the loop's brakes.** EVE already separates dilated clocks from real ones. The EVE University wiki lists what stays on real time under dilation: the server clock, skill training, industry and, most important here, the repair timers of player structures. FWST-8's report records the attackers pausing a repair timer with 8 minutes left before settling in to shoot. A real-time timer is what stops a slow fight from lasting for ever. It is also what makes the size of the fight a weapon, as MMO302 warned. When you design an event system for your own game, decide which real-time clock ends a fight, and publish it.

## 4. Running an event you did not schedule

An operator cannot stop a player-scheduled event and should not try. It is often the best thing that happens to the game that year. What the operator can do is prepare, watch and tell the story afterwards.

### Before

- **Ask for warning.** A notice system only works if commanders use it and the node map can change in time. MMO404 week 7 covers the fleet fight notification and its downtime deadline.
- **Estimate the event with the loop, not a headcount.** Ask the commanders how many pilots they expect, then assume the fight will draw more if it slows. The model's `r` and `G` are the numbers to ask about: how fast can each side reinforce, and how big is the objective?
- **Decide in advance what happens past the floor.** MMO302 listed the options. Write down which one you will take, and who can take it at 03:00.

### During

- **Do not restart the node.** A restart logs thousands of players out mid-fight and decides the battle for them. If the node is failing, the post-mortem must show that the alternative was worse.
- **Watch the backlog, not only the speed.** Time dilation at 10% is working as designed. A growing backlog past the floor means commands are late, and that is where fights feel broken. 9-4RP2 is the example. PC Gamer's account describes pilots waiting minutes for a single command to take effect, clients crashing while trying to draw about 6,100 ships, and an attack abandoned after a few hours. About US$10,000 worth of ships were destroyed, against expectations of the most destructive battle in the game's history.
- **Tell players what the server is doing.** EVE shows the dilation factor in the client. That one number turns "the game is broken" into "the game is slow on purpose."

### After

- **Publish the numbers.** CCP's battle reports give timelines, peaks, unique participants and losses. The FWST-8 report is a post-mortem written for players, and it earned the game a Guinness record and press coverage.
- **Mark the event in the world.** CCP placed a monument of titan wrecks, Titanomachy, in B-R5RB after that battle. After M2-XFE, IGN reported a monument bearing the names of the pilots involved. The event becomes part of the world's history, which MMO301 argued is what a single shard is for.
- **Feed the numbers back into the model.** Every report gives you `n` over time and the length of the fight. Fit `r` and `G` from it, and the next estimate improves.

### Transferable lessons

Strip away the spaceships and four lessons carry to any game where players choose their own peaks: guild sieges, world bosses, server-wide events.

1. A mitigation that stretches an event in real time invites more demand while the event is stretched. Model the loop, not only the peak.
2. Arrival friction and objective size are capacity decisions, even when they are designed as gameplay.
3. A real-time deadline is the brake. Choose it deliberately and say what happens to the outcome when it fires.
4. An event that fails in public (9-4RP2) costs more than the server time. Players had built toward it for months.

## In-class activity (25 minutes)

Groups of three. Your fantasy MMO has one world and quarterly siege battles over castles. Castle walls have hit points, and your server slows time under load, using this lecture's model and constants.

1. A siege starts with 1,000 players, reinforcements arrive at 15 per minute, and at most 4,000 players can take part. Your designers want it to last about two hours of real time. Find the objective size `G` that gives a two-hour siege. (8 min)
2. Marketing wants to double the number of guilds that can join (pool from 4,000 to 8,000). Show the effect on length and pilot-hours. (5 min)
3. Pick one real-time brake and write the rule players will read. Say who it favours. (7 min)
4. Present your `G`, your brake and one sentence on what you would watch during the first siege. (5 min)

Expected output: `G`, a before-and-after table for step 2, and a one-sentence brake rule.

## Common misconceptions

- **"Time dilation keeps big fights from overloading the server."** It keeps the node consistent down to its floor. Past the floor, the backlog grows and commands arrive late. And by making the fight longer, dilation can bring in the extra pilots that push it past the floor.
- **"Twice the hardware makes the fight twice as fast."** In the model it made the fight 2.9 times shorter, because the loop amplifies capacity changes in both directions.
- **"Fewer pilots means shorter fights."** Limiting the pool barely changes the length once the fight is at the floor. The arrival rate and the objective size set the length.
- **"Downtime ending a battle is an operational accident."** It is the strongest brake in the game, and it is a design decision with consequences for who wins.

## Check yourself

1. Arrivals rise to 30 pilots per minute. Without running the model, will the fight last more or less than 419 minutes? Explain with the loop. (The model gives 478.)
2. At what arrival rate does the lecture fight last about four hours? What headcount does it reach?
3. A fight starts with 2,000 pilots instead of 1,000. Use the two-phase method to estimate its length. The model says 576 minutes; explain why starting bigger adds more than the extra time at the floor.
4. You can either double `C` or halve `G` for a given battle. Using the section 3 table, which buys the shorter fight, and which is cheaper to do for every battle in the game?

<details>
<summary>Answers</summary>

1. Longer. Faster arrivals push `n` up sooner, so the speed reaches the floor sooner, with fewer game-minutes done by then. More of the objective is then fought at 0.1. The pool of 6,000 is reached sooner too, so the extra length comes from time at the floor.
2. `r = 10` gives 240 minutes, four hours, with 3,400 pilots at the end.
3. At 2,000 pilots, `W = 0.6 + 4.0 = 4.6` and `f = 0.217`. The fight reaches the floor at about 3,020 pilots after 51 minutes, with only about 7.6 game-minutes done (the lecture fight had 28.3 at that point). The remaining 52.4 game-minutes at 0.1 take about 524 minutes, for about 575 in total, close to the model's 576. Starting bigger costs more than the extra 1,000 pilots suggest, because it removes the fast opening in which the lecture fight did almost half its work.
4. Halving `G` gives 119 minutes, shorter than doubling `C` (146 minutes). Doubling `C` must be done for each battle on reserved hardware, which needs warning. Halving `G` applies to every battle automatically but changes the game for everyone, including small fights that never needed it.

</details>

## Lab / assignment hook

[Lab 08, battle escalation model](../labs/lab08.md). You implement the loop, reproduce the lecture's lines, fit `r` and `G` to a battle timeline, and write an event plan for a player-scheduled siege. The plan becomes the "player-scheduled peaks" section of your final launch plan.

## Sources

- CCP Convict, "Fury at FWST-8 Battle Report" (EVE Online news, 2020). Timeline for 5-7 October 2020: defending fleet on grid 16:34, over 4,000 pilots 16:52, over 6,000 by 17:36, peak 6,557 at 18:16; 8,825 unique characters; system reinforced on a powerful node; time dilation at maximum for the entire battle; repair timer paused with 8 minutes left; structure destroyed after 11 hours 44 minutes. https://www.eveonline.com/article/qlafta/fury-at-fwst-8-battle-report
- Wakeham, L., "EVE Online's record-breaking Fury at FWST-8" (Guinness World Records news, 29 October 2020). Records for the largest multiplayer PvP battle and the most concurrent participants.
- Knoop, J., "EVE Online Breaks Its Own Guinness World Record for the Costliest Video Game Battle in History" (IGN, February 2021). M2-XFE on 31 December 2020; about 5,000 players; about 14 hours; fighting stopped at scheduled downtime; a cyno jammer disabled earlier in the day let reinforcements in; the participant's comment on escalation; monument with participants' names.
- Messner, S., "Why EVE Online's million dollar battle was a huge bust" (PC Gamer, 25 January 2018). 9-4RP2: over 6,100 pilots in the system, another 6,000 nearby; commands taking minutes; client crashes; the attack abandoned; about US$10,000 destroyed.
- Wikipedia, "Battle of B-R5RB" (accessed September 2026), drawing on CCP's report. 27-28 January 2014; missed sovereignty payment on a Monday; each side rushing pilots in as dilation engaged; 21 hours; 7,548 characters, 6,058 in the system, peak 2,670; commemorated with the Titanomachy wrecks; FWST-8 and M2-XFE records.
- CCP Logibro, "Battle for 6VDT-H: summary and numbers" (EVE Online news, 30 July 2013), as cited in MMO302 week 12 and in Wikipedia, "Battle of B-R5RB". Peak of 4,070 pilots in one system; time dilation at one tenth speed for most of the fight. The report gives no single real length, so the table leaves it blank.
- Wikipedia, "Eve Online" (accessed September 2026). Concurrency record of 65,303 on 5 May 2013.
- EVE University Wiki, "Downtime" (accessed September 2026). Daily downtime from 11:00 UTC, nominally 15 minutes since May 2016; all players logged off.
- EVE University Wiki, "Time Dilation" (accessed September 2026). Dilation per node; server time, industry, skill training and Upwell structure repair timers unaffected.
- EVE University Wiki, "Jump Drives" (accessed September 2026). Jump fatigue since the Phoebe release (2014), decaying in real time, capped at 5 hours; cynosural inhibitors.
- Wikipedia, "Induced demand" (accessed September 2026). Elasticity of traffic with respect to travel time about −0.5 short run, −1.0 long run.
- Duranton, G. & Turner, M. A. (2011). "The Fundamental Law of Road Congestion: Evidence from US Cities." *American Economic Review* 101(6), 2616-2652.
- The model's cost constants are MMO302 week 12's, invented for teaching. The arrival rates, pools and objective sizes are invented too.

## Interactive spec: examples/w08-battle-escalation.html

**The one insight:** under time dilation, reinforcements arrive in real time while the fight progresses in game time. A slow fight lasts longer, draws more pilots and gets slower, so a 60-game-minute fight becomes a seven-hour, 6,000-pilot event. The arrival rate and the objective size, not the pool, set the length.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "pilots in the system": x is real minutes from 0 to 600 (labelled in hours), y is pilots from 0 to the pool. A step line for `n(t)` in `--blood`, with a shaded band above 3,016 pilots in a light `--ochre` wash labelled "past the floor: backlog grows." Draw the undilated fight (`f = 1`) as a thin `--ink-soft` line that ends at its own end minute. Mark the end of the dilated fight with a vertical line and label it with the minute.
- View B, "game-minutes done": the same x axis. A line for `game(t)` in `--steel`, a dashed horizontal line at `G` labelled "objective," and a second thin line for the undilated fight (slope 1). Below the chart, a thin strip coloured by `f` (from `--moss` at 1.0 to `--blood` at the floor).
- A cursor (draggable, default at minute 60) linked across both views, with a readout of `n`, `W(n)`, `f` and game-minutes done at that minute.

**Controls:**

- Starting pilots `n0`, 200 to 4,000, step 100 (default 1,000).
- Arrival rate `r`, 0 to 60 pilots per real minute, step 1 (default 20).
- Pool, 1,000 to 10,000, step 250 (default 6,000).
- Objective `G`, 10 to 180 game-minutes, step 5 (default 60).
- Node capacity `C`, 0.5 to 4.0, step 0.25 (default 1.0).
- Floor `f_min`, 0.05 to 0.5, step 0.05 (default 0.1).
- Real-time deadline toggle with a slider, 60 to 900 minutes, step 10 (default off, 240 when switched on).
- Presets: "Lecture battle" (defaults), "Half the arrivals" (`r = 10`), "Smaller pool" (3,000), "Node twice as fast" (`C = 2`), "Downtime at 240 min".

**Readout (always visible, `aria-live="polite"`):** real length `T` in minutes and hours, pilots at the end, pilot-hours, game-minutes done (and "undecided" when a deadline fires first), minutes spent at the floor, and the ratio of `T` to the undilated length. A sentence such as "The same fight at full speed: 60 min, 2,200 pilots. Here: 419 min, 6,000 pilots."

**Formulas (one-minute steps, `t = 0, 1, …` until the fight ends or 1,440):**

```
a = 0.0003, b = 0.000001
f(n) = max(f_min, min(1, C / (a n + b n²)))
each minute: game += f(n); pilot_min += n; t += 1; n = min(pool, n + r)
stop when game ≥ G, or t ≥ deadline if the deadline is on
T = t; pilot-hours = pilot_min / 60
undilated: same loop with f = 1
past the floor when f_min × W(n) > C
```

**Test values (must match, defaults unless stated):**

- Defaults: `T = 419`, 6,000 pilots, 31,442 pilot-hours. Undilated: `T = 60`, 2,200 pilots, 1,590 pilot-hours Minutes at the floor (defaults): 318.
- At minute 60: `n = 2,200`, `W = 5.50`, `f = 0.182`, game-minutes done 22.7. At minute 100: 3,000 pilots, `f = 0.101`, 28.2 done.
- `r = 10`: 240 min, 3,400 pilots, 8,780 pilot-hours. `r = 5`: 119 min, 1,595 pilots.
- Pool 3,000: 416 min, 19,117 pilot-hours. `C = 2`: 146 min, 3,920 pilots, 5,962 pilot-hours.
- `G = 30`: 119 min, 3,380 pilots. `G = 120`: 1,019 min.
- Deadline 240: stops at 240 min with 5,800 pilots, 42.2 game-minutes done, "undecided."

**First screen:** defaults with the cursor at minute 60. Caption: "At full speed this fight would be over now, with 2,200 pilots. Here it is barely a third done, and 1,000 more pilots are on their way. Drag the arrival rate."

**Accessibility:** all controls keyboard operable with visible focus; the cursor moves with arrow keys (1 minute) and Shift plus arrows (10 minutes); readout in `aria-live="polite"`; both series available as a collapsible table every 10 minutes; respects `prefers-reduced-motion` (no animated transitions) and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only: dots and lines, no ships, logos or game art.
