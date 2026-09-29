# MMO407 · Week 01 — Launch day anatomy

**Why this matters:** Launch day is the one day when every player arrives at once and every weakness shows in public. Most launch failures come from a chain of services, and the team fixes the link that looks worst instead of the link that limits the chain. This week you learn to read a launch as a pipeline, find the stage that sets its throughput, and plan the hours around the unlock so the team is fixing the right thing.

**You will be able to:**
- Compute the throughput of a serial login pipeline from its stage capacities, and the backlog it builds in a given time.
- Predict what an upgrade to any one stage buys, and name the stage the bottleneck moves to next.
- Compute the availability of a launch that depends on several services, and explain why a long dependency list lowers it.
- Design a launch-day timeline (preload, unlock, head start, war room roles, kill switches) and justify each item with a failure it prevents.

**Before class:** Read Google, *Site Reliability Engineering* (2016), chapter 14 "Managing Incidents" (the whole chapter, about 12 pages) and chapter 22 "Addressing Cascading Failures", the sections on overload, retries and load shedding. Reread your notes from MMO302 week 9 on login queues and reconnect storms.

**Prerequisites from earlier courses:** [MMO302 week 1, scale targets](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md) (CCU and peak targets). [MMO302 week 9, login and gateway services](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md) (the login stages, the `C / L` queue and jitter for reconnect storms). [MMO302 week 11, load testing with bots](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) (the latency knee). [MMO302 week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (what the war room watches). [MMO309 week 4, duplication exploits](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w04-duplication-exploits-and-transactional-design.md) (kill switches per value path).

**Interactive:** [examples/w01-launch-funnel.html](../examples/w01-launch-funnel.html). Keep it open during section 2.

---

## 1. What "the servers are down" means

On launch night, players say "the servers are down." The sentence hides at least five different machines. Between clicking Play and standing in a town, a player's request passes through a chain of stages, each run by a different service and often a different team.

| Stage | What it does | What a player sees when it is overloaded |
|---|---|---|
| Patch check | compares the client's files with the current build, sends any missing data from a content delivery network (CDN) | a launcher stuck at "checking for updates" |
| Authentication | checks the password, issues a session | an error such as "servers are busy, try again later" |
| Entitlement and account | confirms the account owns the game (or the head-start package) | "you do not own this product", even though they do |
| Character select and creation | reads character summaries, reserves names | a spinner, or "character creation is disabled on this world" |
| World entry | loads the character into a zone server | a queue with a position, or a loading screen that never ends |

A **stage** here is any step every player must pass, in order, to get into the game. A **serial pipeline** is a chain of stages where each player must clear stage 1 before stage 2, and so on. **Capacity** is the most players a stage can pass per minute when it is busy. **Throughput** is the number of players per minute that actually come out of the end of the chain.

MMO302 week 9 split the login path into stateless front stages and the stateful world, and showed that at a full world the queue moves at the logout rate. That was a two-stage version of this week's model. On launch day you face the general case. Every stage has a capacity, the capacities differ, and only one of them sets the pace at any moment.

## 2. Worked example: the narrowest pipe sets the pace

### The hook

Diablo III went live on 15 May 2012. Players who had bought the download could install the game a day early, so their clients were ready at the unlock. Within minutes, many of them saw error 37, a message saying the servers were busy and asking them to try again later. Connection errors continued through May, and they faded as Blizzard added servers and the rush levelled out.

Here is the puzzle a student should ask. The error came from the login stage. Suppose Blizzard had doubled the login servers that night. Would everyone have got in? The model's answer is no, unless login was the narrowest stage, and even then only up to the capacity of the next-narrowest one. Teams that skip this question buy capacity for the stage that is loudest in the logs and discover a new wall ten minutes later.

### The model

Name the numbers.

- `λ` (lambda) is the arrival rate, players per minute trying to get in.
- `c₁, c₂, …, cₙ` are the capacities of the `n` stages, players per minute each.
- `X` is the pipeline's throughput.
- `B(t)` is the backlog after `t` minutes: players who arrived but have not got through.

For a serial pipeline, every player passes every stage, so the chain cannot pass more players than its narrowest stage:

```
X = min(λ, c₁, c₂, …, cₙ)
bottleneck = the stage with the smallest c
B(t) = (λ − X) × t          while λ stays above X
```

The **bottleneck** is the stage with the smallest capacity. Stages upstream of it pass players on as fast as they arrive, and the pile forms at the bottleneck's door. Stages downstream are fed only `X`, so they run below capacity. The backlog builds in front of the bottleneck and nowhere else.

Two consequences follow, and both surprise teams under pressure.

1. **Upgrading a non-bottleneck stage buys nothing.** Its capacity does not appear in `min(…)` until it becomes the smallest.
2. **Upgrading the bottleneck buys less than you paid for.** Raising `c_b` raises `X` only up to the second-smallest capacity. Past that point, the bottleneck has moved.

This is the core claim of the theory of constraints, which Eliyahu Goldratt set out for factory lines in *The Goal* (1984). A factory's output is set by its slowest machine, and time saved at any other machine does not raise output at all. The launch pipeline is a factory whose product is "a player in the world."

### Numbers you can check

Take one launch hour with these invented teaching values. `λ = 1,000` players per minute try to get in. The stages can pass:

| Stage | Capacity `c` (players/min) |
|---|---|
| Patch check | 5,000 |
| Authentication | 600 |
| Character select | 1,500 |
| World entry (worlds still filling) | 900 |

Throughput is `min(1,000, 5,000, 600, 1,500, 900) = 600`. Authentication is the bottleneck. The backlog grows at `1,000 − 600 = 400` per minute, so after an hour `24,000` players have tried and not got through. The zone servers are at two thirds of their entry capacity. Their dashboards look calm.

Now compare four plans the war room might argue about.

| Plan | New capacities | Throughput `X` | Bottleneck after | Backlog after 60 min |
|---|---|---|---|---|
| As built | none | 600 | authentication | 24,000 |
| Double character select | 3,000 | 600 | authentication | 24,000 |
| Double authentication | 1,200 | 900 | world entry | 6,000 |
| Double authentication and world entry | 1,200 and 1,800 | 1,000 | none (arrivals) | 0 |

Check the third row by hand. After doubling, the capacities are 5,000, 1,200, 1,500 and 900. The smallest is 900, so `X = 900`. The team bought 600 players per minute of login capacity and got 300 of it. The backlog grows at `1,000 − 900 = 100` per minute, `6,000` after an hour. And the complaints change. Players stop seeing a login error and start seeing a world queue.

This script prints the same table:

```python
stages = {"patch check": 5000, "authentication": 600,
          "character select": 1500, "world entry": 900}   # players per minute
ARRIVALS = 1000                                           # players per minute

def funnel(stages, arrivals):
    """A serial pipeline passes the smallest capacity; the rest wait before it."""
    name = min(stages, key=stages.get)
    through = min(arrivals, stages[name])
    return name, through, arrivals - through

plans = {"as built": {},
         "2x character select": {"character select": 3000},
         "2x authentication": {"authentication": 1200},
         "2x auth + 2x world entry": {"authentication": 1200, "world entry": 1800}}
for label, change in plans.items():
    s = {**stages, **change}
    name, through, backlog = funnel(s, ARRIVALS)
    print(f"{label:26} narrowest {name:16} through {through:5}/min"
          f"  waiting after 60 min {backlog * 60:6,}")
```

It prints:

```
as built                   narrowest authentication   through   600/min  waiting after 60 min 24,000
2x character select        narrowest authentication   through   600/min  waiting after 60 min 24,000
2x authentication          narrowest world entry      through   900/min  waiting after 60 min  6,000
2x auth + 2x world entry   narrowest authentication   through  1000/min  waiting after 60 min      0
```

In the last row the narrowest stage is again authentication at 1,200, but arrivals are only 1,000, so the chain keeps up. When `λ` is below every capacity, the players themselves are the limit and no backlog forms.

### Move it yourself

Open the interactive. The top view draws the pipeline as a row of pipes, each as wide as its capacity, with a stream of dots flowing through. Dots pile up in front of the narrowest pipe and nowhere else. The bottom view plots throughput and backlog over the hour. Each pipe has a "×2" button. Press it on character select first. The pipe widens and the bottom chart does not move at all. Then press it on authentication. The pile of dots jumps to the next pipe, world entry, and the backlog line bends but keeps climbing. That jump is the lesson. The upgrade worked, and it moved the wall.

### Cross-game recognition

The same `min(…)` shows up in every launch post-mortem once you look for it. What changes is which stage is narrowest and how the game shows it to players.

**Diablo III (launch, May 2012).** Error 37 was the authentication stage telling clients it was full. Because the stage rejected players rather than queuing them, each rejected player clicked retry, so the stage's offered load grew above `λ`. Section 3 shows why that makes a narrow stage narrower. Blizzard's fix was the model's only lever: raise `c` at the bottleneck by adding servers, and wait for `λ` to fall.

**SimCity (March 2013).** The game required a connection to EA's servers, and at launch those servers were overloaded, with outages, disconnections and lost saves. Maxis added servers, and EA also shipped a server patch that turned off features it called non-critical, such as leaderboards, achievements and region filters. Turning features off lowers the work per player at the bottleneck, which raises its capacity in players per minute without new hardware. A senior producer also explained that servers stayed at maximum partly because players stayed connected for long sessions, which is MMO302's `C / L` in a city-builder.

**New World (launch, 28 September 2021).** Each world server admitted 2,000 players at once, and queues on the most popular worlds reached the queue's own 25,000-player limit. Two stages are visible there. The world cap was the bottleneck, and the queue itself was a stage with a capacity. Once it filled, players who arrived got no position at all. Amazon added servers in every region within two days and said it was testing a higher cap. Both raise `c` at the bottleneck. Week 2 models that world queue over the first hours.

**Outside games: a motorway lane closure.** Three lanes merge into one at a roadworks site. The traffic jam forms before the merge, and the road after it is nearly empty. Widening the road after the merge helps nobody. Opening the closed lane moves the jam to the next narrowing, often the exit ramp. Traffic engineers call the merge the bottleneck in the same sense we do.

Four settings, one rule. When a launch is slow, the first question is not "what is failing loudest?" but "which stage has the smallest capacity right now, and what is the second smallest?"

### Eyes-open design judgment

- **Know your capacities before the night.** Every stage needs a measured capacity from a load test (MMO302 week 11), in the same unit, players per minute. A launch plan with "auth: scalable" in the capacity column has a blank where the answer should be. Put the four numbers on one slide and the bottleneck is visible before anyone is paged.
- **Size stages as a set, not one at a time.** Because upgrades migrate the bottleneck, budget for the stage and the one behind it. In the example, buying login capacity without world-entry capacity bought half of what it cost.
- **Choose where the backlog should sit.** A backlog in front of authentication shows up as errors and retries. A backlog in front of world entry shows up as a queue with a position. Players tolerate a queue far better than an error, and a queue does not generate retry load. A common design is to make world entry the planned bottleneck, keep every front stage wider than it, and put the one visible queue there. Week 2 designs that queue.
- **Protect the stages you cannot widen quickly.** A stateless login service can grow in minutes. A database behind character select may take days to grow. Keep a wide margin on slow-to-grow stages and let the fast ones be the ones you top up on the night.
- **Do not trust the calm dashboards.** Every stage downstream of the bottleneck looks healthy precisely because it is starved. Healthy zone servers during a launch can mean the players are stuck somewhere else.

### Check this example

1. With the section 2 capacities and `λ = 1,000`, the team triples patch-check capacity. What is the new throughput?
2. The team doubles authentication (to 1,200) and adds 50% to world entry. What is the new bottleneck and the backlog after 60 minutes?
3. Arrivals fall to 700 per minute in the second hour, with the original capacities. How fast does the backlog grow now?

<details>
<summary>Answers</summary>

1. Still 600. Patch check was not the bottleneck.
2. World entry becomes 1,350 and authentication 1,200, so capacities are 5,000, 1,200, 1,500 and 1,350. The narrowest is authentication at 1,200, which is above `λ = 1,000`, so the chain keeps up and the backlog stays at 0.
3. `X = min(700, 600) = 600`, so it grows at 100 per minute. It stops growing only when arrivals fall below 600.

</details>

## 3. Why a rejecting stage gets narrower

The model above treats a stage's capacity as fixed. On launch night, a stage that rejects players with an error can lose capacity as the night goes on. The mechanism is the retry.

When authentication says "busy, try again," most players try again, and many launchers retry for them. Google's SRE book walks through the same effect in a web service. A backend serving 10,000 queries per second fails 100 of them, the clients retry, and the backend now receives 10,200. The failures grow each second, and a smaller share of requests succeed on their first try. Worse, a rejected request is not free. The server did some work before it gave up, so rejections use up part of the capacity that should have gone to successes.

A small calculation shows the size of the effect. Suppose authentication can do 600 units of work per minute. A success costs 1 unit and a rejection costs 0.1 units, because the server reads the request, checks its load and answers "busy." 1,000 new players arrive per minute, and every rejected player retries every 30 seconds until they get in. Solve `successes + 0.1 × rejections = 600` minute by minute:

| Minute | Players waiting to retry (start) | Attempts | Successes |
|---|---|---|---|
| 1 | 0 | 1,000 | 556 |
| 3 | 988 | 2,975 | 336 |
| 5 | 2,463 | 5,926 | 8 |
| 6 | 3,455 | 7,910 | 0 |

In minute 1 the stage lets in 556 players, close to its 600. By minute 6, rejecting 7,910 attempts costs 791 units, more than the whole budget, and nobody gets in at all. The stage is working as hard as it can and admitting no one. That is **congestion collapse**, a service so busy refusing work that it does none.

Three designs break the loop, and MMO302 week 9 already taught the client-side one.

- **Jitter and backoff on the client.** Spread retries out so the offered load stays near `λ`. MMO302 week 9 sized the jitter window for a reconnect storm. The same formula applies at launch.
- **Cheap, early rejection.** Reject before doing expensive work. Check the load before the password proof, not after. The cheaper a rejection, the more of the stage's capacity goes to successes.
- **A queue instead of an error.** Give the player a position and hold them. A queued player sends no retries. This turns a rejecting stage into a waiting stage and removes the loop entirely. It is why most MMOs put their visible queue at world entry and keep it there.

## 4. Dependencies multiply

The pipeline has a second weakness that has nothing to do with capacity. Every stage must be up for anyone to get in. If each of `k` independent services is available a fraction `a` of the time, the chance that all of them are up together is

```
A_launch = a₁ × a₂ × … × a_k
```

Eight services each up 99.5% of the launch night give `0.995⁸ = 0.961`, about 96%. On a 12-hour launch night that is roughly 28 minutes when some service in the chain is down, even though no single team missed its target by much. Add a store, a friends service, a voice-chat provider and an anti-cheat handshake, and twelve services at 99.5% give `0.995¹² = 0.942`, about 42 minutes.

The design response is to shorten the chain for the one thing players must be able to do, which is get into the world and play. Ask of every dependency, "if this is down, must the player be locked out?" The friends list, achievements, leaderboards and the in-game store can each fail to a safe state. The game shows "friends unavailable" and lets the player in. That is what EA's SimCity patch did in 2013, and it is what a **kill switch** is for. A kill switch is a runtime flag that turns one feature off without a new build. MMO309 week 4 made the case for one switch per value path, and New World's shutdown of all trading paths at once in November 2021 showed the cost of having only one big switch. A launch needs the same thing per feature, decided in advance, with the owner of each switch named on the runbook.

## 5. The launch timeline

A launch is a plan for the hours around the unlock. Most of what goes wrong on the night was decided weeks earlier, when the team chose how arrivals would be spread and who would decide what.

### Before the unlock

- **Preload.** Players download the client days early. This moves the heaviest transfer, often tens of gigabytes per player, out of launch hour and off the patch stage. Diablo III let digital buyers install the day before, which kept the download off the night and put every client at the login door at the same moment. Preload widens one stage and sharpens the arrival spike at the next. Plan for both.
- **Name reservation.** WoW Classic let players create characters and reserve names before the 2019 launch, without being able to play them. That spreads character-creation load over days and shows the team, per realm, how many players plan to arrive. It is a forecast you can read before the night.
- **Head start.** Guild Wars 2 let players who pre-purchased play from 25 August 2012, three days before the 28 August launch. FFXIV: A Realm Reborn ran early access from 24 August 2013 before the 27 August launch. Lost Ark's western release in February 2022 opened three days early for founder's pack buyers. A head start splits `λ` into two waves and puts the most committed players in first, which fills worlds before the general rush.

### The unlock itself

There are two ways to open the doors.

- **Global, one moment.** WoW Classic opened everywhere at once, at midnight Central European Summer Time on 27 August 2019, which was 3 p.m. Pacific time on 26 August in the Americas. One spike, the whole world arriving together. Simple to communicate, and the hardest shape for capacity.
- **Staggered by region.** New World opened each region at 8:00 a.m. local time on 28 September 2021, with Australia at 9:00 p.m. AEST. Each region's spike arrives at a different hour, so shared stages (authentication, entitlement, the store) see several smaller spikes instead of one large one.

A staggered unlock lowers the peak `λ` at shared stages. It does nothing for a world that serves one region, because that world's spike is the same size either way. Know which of your stages are shared before you pick.

### The war room

The war room is the group that runs launch night, physically or in a chat channel. Google's incident-management chapter, which draws on the Incident Command System used by emergency services, gives it a structure that fits a launch well.

- **Incident commander.** One person who holds the overall picture and makes the calls, including "turn off the store" and "stop selling." Everyone else reports to them.
- **Operations lead.** The only group that changes production during the event. This stops two engineers from "fixing" the same service in opposite directions.
- **Communications lead.** Posts status to players on a fixed rhythm and to the rest of the company. Week 9 of this course covers what to say.
- **Planning lead.** Tracks what has been tried, handles shift changes, and books the pizza. Launches run for days, and a war room without a shift plan makes its worst decisions at 4 a.m.

Give the war room three things before the unlock: the capacity slide from section 2 with the expected bottleneck marked, the list of kill switches with owners, and a set of **go/no-go criteria**. Those are written conditions for delaying the unlock, such as "entitlement error rate above 1% in the final rehearsal." Criteria written in advance let a tired team delay a launch without arguing about it at 11:55 p.m.

## In-class activity (25 minutes)

In groups of three. Your MMO launches in four weeks. Load tests measured these capacities, in players per minute: patch CDN 8,000, authentication 1,500, entitlement 1,100, character select 2,400, world entry (while worlds are filling) 1,800. Marketing forecasts 2,000 players per minute in the first launch hour. You have budget to double exactly one stage and to add 50% to one other.

1. Find the bottleneck and the backlog after one hour as built.
2. Choose your two upgrades. Give the new throughput, the new bottleneck and the backlog after one hour.
3. Decide where you want players to wait, and describe what they see there.
4. List three dependencies you would put behind a kill switch, and one you cannot.

Expected output: as built, entitlement at 1,100 is the bottleneck and the backlog is `900 × 60 = 54,000`. Doubling entitlement to 2,200 and adding 50% to authentication (2,250) gives capacities 8,000, 2,250, 2,200, 2,400 and 1,800, so world entry at 1,800 is the new bottleneck, with a backlog of `200 × 60 = 12,000` in a world queue with positions. Doubling entitlement alone leaves authentication at 1,500 as the bottleneck, with a backlog of 30,000 in front of a stage that shows errors. A group should prefer the plan that ends with the backlog in front of world entry.

## Common misconceptions

- **"Add servers to whatever is failing."** Only the bottleneck's capacity sets throughput. Adding capacity elsewhere changes nothing, and the loudest service in the logs is not always the narrowest.
- **"We doubled the bottleneck, so we doubled throughput."** Throughput rises only to the second-smallest capacity. Past that, the bottleneck has moved.
- **"A healthy world server means the launch is fine."** Stages after the bottleneck are starved, so they look calm. Look at the backlog in front of each stage.
- **"Each service is 99.5% up, so the launch is 99.5% up."** Availabilities multiply across required dependencies. Twelve at 99.5% give about 94%.

## Check yourself

1. A pipeline has capacities 3,000, 800, 1,200 and 950 players per minute, and 1,100 players arrive per minute. Find the throughput, the bottleneck and the backlog after 45 minutes.
2. In question 1, the team can raise one stage by 400. Which stage, and what is the new backlog growth rate?
3. A launch depends on 10 services, each available 99.8% of the time. What is the chance all are up? How many minutes of a 24-hour launch day would you expect some service to be down?
4. Explain in two or three sentences why a stage that rejects players with an error can lose throughput over the night, and give two designs that prevent it.
5. Your game serves players in three regions from one shared authentication service and region-local worlds. Compare a global unlock and a staggered one for the authentication stage and for a single world.

<details>
<summary>Answers</summary>

1. `X = min(1,100, 3,000, 800, 1,200, 950) = 800`. The bottleneck is the 800 stage. The backlog grows at 300 per minute, `300 × 45 = 13,500`.
2. Raise the 800 stage to 1,200. Now the smallest is 950, so `X = 950` and the backlog grows at 150 per minute. The bottleneck has moved to the 950 stage.
3. `0.998¹⁰ ≈ 0.980`. Expect about 2% of 1,440 minutes, roughly 29 minutes.
4. Rejected players retry, so the offered load climbs above the arrival rate, and each rejection costs some work, so less capacity is left for successes. Client jitter and backoff, cheap early rejection, or replacing the error with a queue that holds a position all prevent it.
5. Authentication is shared, so a staggered unlock turns one spike of the combined arrivals into three smaller spikes, which lowers its peak load. A single world serves one region, so its spike is the same size under either plan.

</details>

## Lab / assignment hook

[Lab 01, launch funnel and readiness review](../labs/lab01.md). You build a minute-by-minute simulator of a serial launch pipeline with retries and kill switches, reproduce this lecture's table, find the upgrade plan that clears a given launch hour at least cost, and write a one-page launch readiness review with go/no-go criteria. The simulator is reused in week 13's launch plan workshop.

## Sources

- Wikipedia, "Diablo III" (read September 2026). Release on 15 May 2012; digital buyers could install from 14 May; heavy server load at launch with error 37, whose message says the servers are busy and asks players to try again later; connection errors through May 2012, resolved as Blizzard added servers.
- Wikipedia, "SimCity (2013 video game)" (read September 2026). Closed betas in January and February 2013 for load testing; launch outages, disconnections and lost saves; added servers; a server patch disabling non-critical features including leaderboards, achievements and region filters; a senior producer's comment that servers stayed at maximum partly because players stayed connected for long periods.
- Wikipedia, "New World: Aeternum" (read September 2026). Global release on 28 September 2021, regions opening at 8:00 a.m. local time and Australia at 9:00 p.m. AEST; over 700,000 concurrent players on Steam on release day; 2,000 players per server; queues on popular servers reaching the 25,000-person limit; additional servers in all regions within two days; tests to raise the cap.
- Warcraft Wiki, "World of Warcraft: Classic" (read September 2026). Launch on 27 August 2019 at midnight CEST worldwide; name reservation before launch; temporary layering; extreme login queues and additional servers.
- Wikipedia, "Guild Wars 2" (read September 2026). Pre-purchasers could play from 25 August 2012; launch on 28 August 2012.
- Wikipedia, "Final Fantasy XIV: A Realm Reborn" section of "Final Fantasy XIV" (read September 2026). Early access from 24 August 2013, launch on 27 August 2013.
- Wikipedia, "Lost Ark (video game)" (read September 2026). Western release on 11 February 2022, founder's pack buyers playing from 8 February 2022.
- MMO309 week 4 (this program) for New World's November 2021 trading shutdown, with its sources.
- Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (eds.) (2016). *Site Reliability Engineering*. O'Reilly. Chapter 14, "Managing Incidents" (roles: incident commander, operations, communication, planning; based on the Incident Command System). Chapter 22, "Addressing Cascading Failures" (retry growth from 10,000 to 10,200 queries per second, load shedding, graceful degradation). https://sre.google/sre-book/
- Goldratt, E. M. & Cox, J. (1984). *The Goal*. North River Press. The theory of constraints.
- Stage capacities, arrival rates, availabilities and costs in sections 2 to 4 and the activity are invented teaching values.

## Interactive spec: examples/w01-launch-funnel.html

**The one insight:** a serial pipeline passes only as many players as its narrowest stage. Widening any other stage changes nothing, and widening the narrowest one moves the wall to the next-narrowest stage.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "the pipeline": four horizontal pipes in order (patch check, authentication, character select, world entry), each drawn with height proportional to its capacity on a shared scale, and a stream of generic dots entering from the left at rate `λ`. Dots that cannot pass pile up in a heap drawn in front of the narrowest pipe, using `--blood`. The narrowest pipe is outlined in `--blood`; the others in `--steel`. Each pipe shows its capacity and its utilization `X / c` as a percentage. Under each pipe, a "×2" button and a "reset" button.
- View B, "the hour": a chart with time 0 to 60 minutes on x. Two lines, throughput `X` (constant within a scenario, `--moss`) and backlog `B(t) = (λ − X) × t` (`--blood`). When the user changes a capacity, the old backlog line stays as a faint ghost so the change (or lack of it) is visible.

**Controls:**

- Arrival rate `λ` slider, 100 to 3,000 players per minute, step 50 (default 1,000).
- One capacity slider per stage, 100 to 6,000, step 50 (defaults 5,000, 600, 1,500, 900), plus the "×2" buttons.
- "Retries" toggle (default off). When on, a stage that is the bottleneck rejects instead of queuing. Parameters: retry interval `r` slider 10 to 120 seconds (default 30), rejection cost `k` slider 0 to 0.5 (default 0.1). The simulation then runs minute by minute (see formulas) and View B shows successes per minute falling.
- "Queue at world entry" toggle, visible only when retries are on. When on, the backlog is held in a queue with positions in front of world entry and no retries are generated.
- Preset buttons: "as built", "2× character select", "2× authentication", "2× auth + 2× world entry".

**Readout (always visible, `aria-live="polite"`):** throughput `X`, bottleneck name, second-narrowest stage and its capacity, backlog at 60 minutes, and after a "×2" press a sentence such as "You added 600/min to authentication. Throughput rose by 300/min. The bottleneck is now world entry."

**Formulas:**

```
X = min(λ, c_patch, c_auth, c_select, c_world)
B(t) = max(0, λ − X) × t
retries on (bottleneck stage b, per minute t):
  waiting_to_retry W starts at 0
  attempts = λ + W × 60 / r
  budget   = c_b                             (work units per minute; success costs 1)
  successes = max(0, min(attempts, (budget − k × attempts) / (1 − k)))   [clamp to ≥ 0]
  rejected  = attempts − successes
  W = W + λ − successes                      (everyone who has not got in keeps trying)
  throughput shown = successes
```

The successes formula solves `successes × 1 + (attempts − successes) × k = budget` for successes.

**Test values (must match):**

- Defaults: `X = 600`, bottleneck authentication, backlog 24,000 at minute 60.
- "2× character select": identical to defaults; the readout says throughput changed by 0.
- "2× authentication": `X = 900`, bottleneck world entry, backlog 6,000 at 60.
- "2× auth + 2× world entry": `X = 1,000`, backlog 0.
- Retries on, defaults: minute 1 attempts 1,000, successes `(600 − 100) / 0.9 = 555.6`; minute 3 attempts 2,975, successes 336.1; minute 5 attempts 5,926, successes 8.2; minute 6 onward successes 0 (attempts 7,910 at minute 6).
- Retries on with "queue at world entry": identical to retries off.

**First screen:** defaults, dots piling in front of authentication, world entry at 67% utilization in calm steel, and the caption "Authentication is the wall. Try doubling character select, then authentication."

**Accessibility:** every control keyboard operable with visible focus; the pipe heights also appear as numbers; readout in `aria-live="polite"`; with `prefers-reduced-motion` the dot stream is replaced by static heaps; respects `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only, no game art or logos.
