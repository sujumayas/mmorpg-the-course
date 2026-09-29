# MMO306 · Week 11 — Events and World Bosses

**Why this matters:** A world boss is the one piece of content whose fun depends on how many strangers turn up at the same time. Too few and it can't be beaten. Too many and it melts before anyone lands a hit. The number who turn up is set mostly by one decision you make in a spreadsheet: how often the event runs. Get that number wrong and no amount of encounter design saves it.

**You will be able to:**
- Compute the share of players who can reach a scheduled event and the crowd at each occurrence, from population, session length, join window and interval.
- Find the interval that gives every player a chance without thinning the crowd, and the population below which an event can no longer fill.
- Design a boss's health scaling so that kill time stays in a target band from a small group to a large crowd.
- Critique a shipped event schedule (fixed timetable, random spawn, weekly rotation) in terms of reach, crowd and contest.

**Before class:** Guild Wars 2 Wiki, "World boss" (the schedule and rewards sections, 15 minutes). Warcraft Wiki, "World boss" (the history section, 10 minutes). Reread [GD201 week 11](../../GD201-level-and-world-design/lectures/w11-shared-spaces-designing-for-many-players.md) section 3 on shared credit and scaling.

**Prerequisites from earlier courses:** [GD201 week 11, shared spaces](../../GD201-level-and-world-design/lectures/w11-shared-spaces-designing-for-many-players.md) (the comfortable range of a zone copy, shared credit, event scaling). [GD202 week 13, shared vs personal story](../../GD202-narrative-and-quest-design/lectures/w13-shared-vs-personal-story.md) (one-time world events and who sees them). [MMO301 week 4, EverQuest, the treadmill and the raid](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w04-everquest-the-treadmill-and-the-raid.md) (loot per raider for a contested boss). [MMO303 week 10, payoff matrices](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md) (two guilds and one world boss). [MMO302 week 1, scale targets](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md) (what a crowd costs the server).

**Interactive:** [`examples/w11-event-clock.html`](../examples/w11-event-clock.html). Keep it open during section 2.

---

## 1. Content that happens at a time

Almost everything else in this course is content that waits for the player. A dungeon is there whenever a group queues. A quest hub is there whenever someone walks in. **Events** are content that happens at a time, and the player must be there when it does.

A few kinds, from small to large:

- **Scheduled open-world events.** A boss or invasion that starts at known times in a shared zone and lasts minutes. Anyone present can join.
- **Triggered events.** Content that starts when players do something (finish a chain of smaller events, collect enough resources, kill a rare spawn).
- **World bosses.** Raid-strength enemies in the open world, fought by whoever turns up. The Warcraft Wiki describes them as raid-level monsters in the shared world rather than in an instance limited to a certain number of players.
- **Seasonal events.** Holidays and festivals that run for days or weeks, once a year.
- **One-time world events.** Content that runs once and changes the world. GD202 week 13 covers what those do to shared story.

These share one property that sets them apart. The crowd is not chosen by matchmaking. It is whoever happens to be online, near enough, at that moment. Your schedule, your rewards and your population together decide that number. This week gives you a model for it.

Three terms first.

- The **interval `T`** is the time between one start of an event and the next, in minutes. (In week 4 `T` was the enrage time; here it is always the interval.)
- The **join window `W`** is how long after the start a player can still arrive and take part.
- A **lockout** limits how often one player can earn the event's reward, for example once per day.

## 2. Worked example: the event clock

### The hook

Guild Wars 2 runs its core world bosses on a published timetable. Some world boss spawns every 15 minutes, somewhere in the world, and each individual boss comes back every two or three hours on a fixed clock. The large bonus chest can be earned once per account per day.

World of Warcraft's first world bosses worked the other way. The Warcraft Wiki's history of Azuregos and Lord Kazzak says killing them meant tracking the spawn, forming a raid and beating the encounter while fighting off the other faction. The bosses appeared on no published clock. Since Legion, Blizzard has run most new world bosses as weekly world quests instead, so a boss is available for a week at a time.

Three schedules for the same kind of content. Designers argue about them in terms of feel: a rare spawn "feels special," a timetable "feels like a chore." The model below shows that the choice is mostly arithmetic, and that the intuition "rarer means bigger crowds" is wrong.

### The model

Take a map with `N` players each day who want this event. Keep the assumptions simple so the arithmetic is visible:

- Each player plays one session a day of length `S` minutes, starting at a random time of day.
- The event starts every `T` minutes, around the clock.
- A player can join if they are online at any moment from the start until `W` minutes after it.
- The reward is once per day, so a player attends the first occurrence they catch and skips the rest.

A player catches an occurrence if one starts no earlier than `W` minutes before their session begins and no later than the end of the session. That is a stretch of `S + W` minutes. Starts come every `T` minutes, so:

```
reach  R(T) = min(1, (S + W) / T)          share of daily players who can attend
crowd  C(T) = N × min(S + W, T) / 1440     players at one occurrence
```

- `N` is the daily players who want the event.
- `S` is the session length, `W` the join window, `T` the interval, all in minutes.
- 1,440 is the number of minutes in a day.

The crowd line comes from counting. Per day, `N × R` players attend, spread over `1440 / T` occurrences. Multiply `N × min(1, (S + W)/T)` by `T / 1440` and you get `C`.

Look at the `min` in both lines. There is a **knee** at `T = S + W`.

- **Below the knee** (`T < S + W`), everyone who plays that day catches an occurrence, so reach is 100%. But the day's players are spread over more occurrences, so each crowd is smaller. Running the event twice as often halves the crowd.
- **Above the knee** (`T > S + W`), each occurrence gets everyone who is online around it, `N (S + W) / 1440`, and no more. Making the event rarer does not make the crowd bigger. It only shuts out the players whose sessions fall between occurrences.

So the knee is the interval that gives the largest crowd possible and still lets every player attend.

### Numbers you can check

A map with `N = 3,000` interested daily players, 90-minute sessions and a 15-minute join window, so `S + W = 105`:

```python
DAY = 1440          # minutes in a day
N = 3000            # daily players who want this event
S = 90              # session length, minutes
W = 15              # minutes after the start in which you can still join

def reach(T):
    """Share of daily players whose session catches at least one start."""
    return min(1.0, (S + W) / T)

def crowd(T):
    """Players at one occurrence when the reward is once per day."""
    return N * min(S + W, T) / DAY

for T in (30, 60, 105, 120, 180, 360, 1440):
    print(f"every {T:4d} min  reach {reach(T):5.1%}  crowd {crowd(T):6.1f}")

n_min = 40
print("N needed for", n_min, "=", round(DAY * n_min / (S + W), 1))
```

It prints:

```
every   30 min  reach 100.0%  crowd   62.5
every   60 min  reach 100.0%  crowd  125.0
every  105 min  reach 100.0%  crowd  218.8
every  120 min  reach 87.5%  crowd  218.8
every  180 min  reach 58.3%  crowd  218.8
every  360 min  reach 29.2%  crowd  218.8
every 1440 min  reach  7.3%  crowd  218.8
N needed for 40 = 548.6
```

| Interval `T` | Reach | Crowd per occurrence | Players shut out per day |
|---|---|---|---|
| 30 min | 100% | 62.5 | 0 |
| 60 min | 100% | 125.0 | 0 |
| 105 min (the knee) | 100% | 218.8 | 0 |
| 3 hours | 58.3% | 218.8 | 1,250 |
| 6 hours | 29.2% | 218.8 | 2,125 |
| once a day | 7.3% | 218.8 | 2,781 |

Check the 3-hour row by hand. Reach is `105 / 180 = 0.583`. The crowd is `3,000 × 105 / 1440 = 218.75`. Shut out is `3,000 × (1 − 0.583) = 1,250`.

The once-a-day boss draws exactly the same crowd as the one every 105 minutes. It just turns away 38 players out of every 41 who wanted it. The "special" feeling of a rare boss doesn't come from a larger crowd. If it comes from anything, it comes from the players who arrange their evening around it, which the next section adds.

A small simulation with random session starts, one session per player per day and first-occurrence attendance agrees with the formulas within a few players (it is in the lab starter): at `T = 60` it gives 100% reach and 125.0 per occurrence; at `T = 360`, 29.2% reach and 219.2 per occurrence.

### The floor: when an event can no longer fill

Suppose the boss needs at least `n_min = 40` players to be beaten in time, or to feel like a world event. The largest crowd any interval can give is at the knee, `N (S + W) / 1440`. So the event can fill only if

```
N ≥ N_crit = 1440 × n_min / (S + W)
```

For our map, `N_crit = 1440 × 40 / 105 = 548.6`. Above 549 daily players, some interval works. Below it, no interval does, however you schedule. That is how world bosses die in an ageing game: the population falls below `N_crit`, and each occurrence has 20 players at a boss built for 40. The Warcraft Wiki's history describes exactly this for the Burning Crusade world bosses, which went unkilled for long periods once better loot was available in instances.

Your levers against the floor each change a term:

- **Lower `n_min`** by scaling the boss to the crowd (section 3).
- **Raise `N` per copy** by merging players from several servers or map copies into one, as GD201 week 11 describes for the Guild Wars 2 megaserver.
- **Raise `S + W`** with a longer join window, or with warnings that bring players online in time.

### Planners change the picture

The model assumes sessions start at random. Some players don't wait for the event to find them. They log in for it. Call the share of interested players who plan around a published time `p`. For a fixed timetable, planners attend whatever the interval, as long as the time suits them. Now rarity starts to matter. A once-a-day boss with `p = 0.2` adds `0.2 × 3,000 = 600` planners to its 219 random arrivals. A boss every hour spreads the same 600 planners over 24 occurrences, 25 each.

This is the honest case for a rare event. It concentrates the players who care into one place. The cost is on everyone else. Those planners had to rearrange their evening, and a player whose session doesn't cover the time never sees the boss at all. Guild Wars 2's timetable shows one way to get both. Each boss is rare enough (every two or three hours) to gather a crowd, but bosses are staggered so that some boss starts every 15 minutes. A player with any session length finds some boss, and players who plan can target a particular one.

### A visual you can move

Open the interactive. The top view is a 24-hour clock strip. Each occurrence is a tick, and 60 sample players' sessions are drawn as bars underneath, coloured when they catch an occurrence and grey when they don't. The bottom view plots reach and crowd against `T`. Drag `T` from 15 minutes to 24 hours. Reach stays flat at 100% until the knee and then falls. The crowd rises until the knee and then goes flat. The two lines break at the same point, and it is the only point where both are at their best. Then slide `N` down and watch the crowd line drop under the `n_min` band. Past `N_crit`, there is no `T` that lifts it back.

### Cross-game recognition

**Guild Wars 2, world bosses (core Tyria, current).** A fixed timetable with staggered bosses. Some boss starts every 15 minutes, each boss repeats every two or three hours, and the bonus chest has a once-per-account daily lockout, so the model's lockout assumption holds. Per boss, `T` is 120 or 180 minutes, above the knee for most sessions, which gathers the full crowd. For "any boss," the effective `T` is 15 minutes, far below the knee, so reach is near 100%. The stagger splits the two jobs between two clocks.

**World of Warcraft, classic-era world bosses (2004 onward).** Unannounced spawns with no published time. In the model, random arrivals are nearly zero (few players happen to walk past), and the crowd is almost all planners: guilds that tracked the spawn. That gives a contested fight between guilds, which MMO303 week 10 analyses as a game and MMO301 week 4 as loot per raider. Reach for an ordinary player is close to 0%.

**World of Warcraft, weekly world bosses (Legion onward).** The boss is available for a week through a world quest. The join window `W` is days long, so `S + W` is far larger than `T` and reach is effectively 100% for anyone who plays that week. The crowd at any one moment is small. This design gives up the crowd on purpose in exchange for reach.

**The same model outside bosses.** Any content with a start time fits. A battleground that pops only when enough players queue, a guild's scheduled raid night, a seasonal festival's hourly fireworks. Each has an interval, a join window and a population. The knee tells you whether the schedule is wasting players or thinning crowds.

### Eyes-open design judgment

- **Start at the knee.** Set `T ≈ S + W` using your real median session length from telemetry. That gives the largest crowd without shutting anyone out. Move away from it only on purpose.
- **Rarer only if players plan.** A rare event gathers a bigger crowd only through planners. If you want that, publish the time, warn in advance, and accept that players without control of their evening will miss it.
- **Split jobs across clocks.** If you have several events, stagger them so that "some event" is frequent (reach) while "this event" is rare enough to gather a crowd.
- **Recompute `N_crit` every season.** Populations fall. When `N` approaches `N_crit`, change something (scaling, merging copies, a longer window) before players find a dead boss.
- **Remember the top end too.** A crowd above your zone's comfortable range (GD201 week 11) must be split into copies, and each copy must still exceed `n_min`.

### Check yourself (worked example)

1. With `N = 2,000`, `S = 60`, `W = 10`, find the knee, the crowd at the knee, and reach at `T = 4` hours.
2. The same map's boss needs 60 players. Does it fill at the knee? What is `N_crit`?
3. Planners are 10% of `N = 2,000`. At a once-a-day boss, what is the crowd, counting random arrivals and planners?

<details>
<summary>Answers</summary>

1. Knee at `T = 70` minutes. Crowd `2,000 × 70 / 1440 = 97.2`. Reach at 240 minutes is `70 / 240 = 29.2%`.
2. Yes. The knee crowd of 97.2 is above 60. `N_crit = 1440 × 60 / 70 = 1,234.3`, and 2,000 is above it, so the event survives a population drop of about 38% before it fails.
3. Random arrivals `97.2` plus planners `200`, about 297.

</details>

## 3. Designing the fight for an unknown crowd

The schedule sets the crowd. The encounter must work across whatever crowd arrives. For a world boss, you know neither the group size nor its make-up, and every player is a stranger.

### Scaling health to the crowd

Let each participant deal `d` damage per second on average. A boss with fixed health `H` dies in `H / (n × d)` seconds with `n` players. That is [week 4's](w04-encounter-mechanics-tank-and-spank-to-dance-fights.md) `H / P` with the raid's damage `P = n × d`, and no mechanics. Kill time falls as `1/n`. With `H = 6,000,000` and `d = 500`, 10 players need 1,200 seconds (20 minutes) and 150 players need 80 seconds. Neither is a good fight.

A common fix is to scale health with the number of participants:

```
H(n) = H_0 + h × n
kill time t(n) = H(n) / (n × d) = H_0 / (n × d) + h / d
```

- `H_0` is the base health, which only matters for small crowds.
- `h` is the health added per participant.

As `n` grows, the first term shrinks and kill time settles at `h / d`. With `H_0 = 200,000`, `h = 60,000` and `d = 500`, kill time is `400 / n + 120` seconds:

| Participants `n` | Fixed health (6,000,000) | Scaled health | Scaled kill time |
|---|---|---|---|
| 10 | 1,200 s | 800,000 | 160 s |
| 40 | 300 s | 2,600,000 | 130 s |
| 150 | 80 s | 9,200,000 | 122.7 s |

Scaled health holds kill time between two and three minutes over a fifteenfold range of crowd. `H_0` sets how much a small crowd suffers. `h / d` sets the floor. If you want larger crowds to be faster (so the crowd feels powerful) make health grow more slowly than `n`. If you want them slower, grow it faster. Choose deliberately.

Guild Wars 2's dynamic events scale up and down with the number of players taking part, as GD201 week 11 describes. That lecture also covers why shared credit (every contributor gets their own loot) turns a crowd from competitors into help. For world bosses, it is what makes the crowd welcome at all.

### Mechanics a crowd can read

The rules for mechanics and telegraphs from [week 4](w04-encounter-mechanics-tank-and-spank-to-dance-fights.md) and [week 5](w05-telegraphing-and-readability.md) still apply, with two changes.

- **Every mechanic must work with strangers.** Mechanics that need assigned roles ("the two tanks swap at three stacks") fail when nobody knows anybody. Prefer mechanics each player can solve alone by reading the ground: move out of the red circle, stand in the safe zone, break the add that targets you.
- **Every telegraph must read in a crowd.** With 150 players, spell effects cover the ground. Boss telegraphs need to draw above player effects, and player effects may need to be reduced in large groups. Test at your expected crowd, not at five.

### What a crowd costs the server

A boss with 150 players in view means every player's client receives updates about 150 others and the boss. MMO302 week 1 showed that this cost grows with the square of the crowd in one area. When you set `T`, `n_min` and your zone's copy size, send the expected peak crowd to the server team. The crowd your schedule invites is a load test you schedule yourself.

## 4. Calendars: events competing for the same players

A live game runs many events at once: daily bosses, weekly rotations, a seasonal festival, a raid night. They draw on the same `N`.

If two events start at the same time and a player can attend only one, the crowd splits. With two equally attractive events, each gets about half. The model's crowd line then halves too, and an event that filled alone may fall below `n_min`. Staggering the start times fixes this for free. A 15-minute stagger between two 15-minute events lets a player do both.

Seasonal events stack differently. A festival running for two weeks has a very large `W`, so reach is effectively 100%. Its risk is not missed players but fatigue, when the festival's daily tasks sit on top of the game's other dailies. [Week 8's treatment of repeatable content](w08-repeatable-content-dailies-dungeons-rotations.md) applies to them.

A practical rule for the event calendar is to draw it as the clock strip from the interactive, one row per event, and check three things. No two events that need a crowd start in the same slot. Every hour of the day has something for a player who logs in then. And every event's crowd, at your current `N` and after splitting, is above its `n_min`.

## In-class activity (25 minutes)

In groups of three. You are designing a world boss for a new zone.

1. **(5 min)** Use `N = 4,000` interested daily players, `S = 75` minutes and a join window you choose. Compute the knee and the crowd at the knee.
2. **(5 min)** Choose `n_min` and a health rule `H(n) = H_0 + h n` so that kill time stays between 2 and 4 minutes from `n_min` to 3 times the knee crowd. Use `d = 400`.
3. **(5 min)** The population falls to 40% of launch in a year. Is the event still above `N_crit`? If not, choose one lever and recompute.
4. **(10 min)** Swap with another group. Propose a second boss that shares the zone. Stagger the two and draw both on a 6-hour clock strip.

Expected output: `T`, crowd, `n_min`, `H_0`, `h`, the kill times at three crowd sizes, the year-two check, and the clock strip.

## Common misconceptions

- **"A rarer event draws a bigger crowd."** Only planners make it bigger. Random arrivals top out at `N (S + W) / 1440` once `T` passes the knee, so rarity beyond that only shuts players out.
- **"A more frequent event is more generous."** Below the knee, it is equally generous (everyone can attend) and thins every crowd. Hourly bosses at low population can mean every occurrence fails.
- **"Scaling fixes everything."** Scaling lowers `n_min`, but not to 1. A world boss that one player can beat alone is no longer a world boss.
- **"The schedule is a live-ops detail."** It is a design value, as important as boss health, and it should be computed from session length before launch.

## Check yourself

1. A map has `N = 1,200`, `S = 45`, `W = 15`. The team runs a boss every 30 minutes with `n_min = 30`. What is the crowd? Does it fill? What interval would you suggest?
2. For the same map, what is `N_crit` for `n_min = 30`?
3. A boss has `H_0 = 0` and `h = 50,000`, and each player does 250 DPS. What is the kill time with 20 players? With 200?
4. A designer wants 200 players to kill the boss in half the time 20 players take. Propose a health rule and check it.
5. Two bosses need 80 players each and start at the same time on a map whose knee crowd is 140. What happens? What is the cheapest fix?

<details>
<summary>Answers</summary>

1. Crowd `1,200 × 30 / 1440 = 25`, below 30, so it fails. At the knee (`T = 60`), the crowd is `1,200 × 60 / 1440 = 50` with 100% reach. Suggest 60 minutes.
2. `1440 × 30 / 60 = 720`.
3. `t = h / d = 200` seconds in both cases, because with `H_0 = 0` kill time doesn't depend on `n`.
4. One option: `H(n) = H_0 + h n` with `t(20) = 2 t(200)`. `H_0 / (20 d) + h/d = 2 (H_0 / (200 d) + h/d)`, so `H_0 / 20 − H_0 / 100 = h`, giving `H_0 = 25 h`. With `h = 50,000` and `d = 250`: `H_0 = 1,250,000`, `t(20) = 250 + 200 = 450` s and `t(200) = 25 + 200 = 225` s. Other rules (health growing as a power of `n` below 1) also work if checked.
5. If players split evenly, each boss gets 70, below 80, and both fail. Staggering them so a player can attend both restores 140 to each. That costs nothing but a clock change.

</details>

## Lab / assignment hook

[Lab 11, the event clock](../labs/lab11.md). You implement reach and crowd, test them against a session simulation, add a prime-time population curve (the uniform assumption breaks), and plan a zone's calendar of two world bosses and one hourly event at launch and at 40% population. The calendar and boss scaling feed the encounter designs assignment.

## Sources

- Guild Wars 2 Wiki, "World boss" (accessed September 2026). Core Tyria world bosses spawn on a fixed timetable, with some boss spawning every 15 minutes and each boss repeating every two or three hours; the bonus chest is limited to once per account per day, and the ground chest once per character per day per boss. Full schedule table checked September 2026. https://wiki.guildwars2.com/wiki/World_boss
- Guild Wars 2 Wiki, "Dynamic event" (accessed September 2026, as cited in GD201 week 11). Events scale with the number of participating players.
- Warcraft Wiki, "World boss" (accessed September 2026). Definition as raid-level monsters in the shared world; Azuregos and Lord Kazzak required tracking spawns and fending off the other faction (classic era); Burning Crusade world bosses left unkilled for long periods; since Legion, a weekly world boss with a world quest.

## Interactive spec: examples/w11-event-clock.html

**Insight the visual must make obvious:** reach and crowd trade off only below the knee `T = S + W`. Above it, the crowd stops growing and only reach falls. The knee is the one interval where both are at their best, and below `N_crit` no interval fills the event.

**Layout.** Two linked views, stacked on all widths (clock strip on top).

- **Top view, "A day on the map."** A horizontal 24-hour strip (0:00 to 24:00). Occurrence starts are vertical blood-red ticks every `T` minutes, each with a light shaded join window of width `W`. Under the strip, 60 sample player sessions drawn as horizontal bars of length `S` at seeded random start times. A bar is ochre if it catches an occurrence (some start `t` with `session_start − W ≤ t ≤ session_start + S`), grey if not. Label: "caught X of 60." Planners, when `p > 0`, are drawn as short steel bars aligned with the chosen "planned occurrence" (the 20:00 occurrence, or the nearest one to 20:00).
- **Bottom view, "Reach and crowd against the interval."** X axis `T` on a log scale from 15 minutes to 1,440 minutes, labelled in minutes and hours. Left Y axis reach 0 to 100% (moss line). Right Y axis crowd in players (blood line) for random arrivals, plus a dashed blood line for random arrivals plus planners at the planned occurrence (`C + p × N`, only for the planned occurrence). A vertical ink line at the knee `T = S + W`, labelled. A horizontal ochre band from `n_min` to `n_max` on the crowd axis. A cursor dot on both lines at the current `T`.

**Controls (labelled, keyboard reachable):**
- `T` slider, log-scaled, 15 to 1,440 minutes, snapping to 15, 30, 45, 60, 90, 105, 120, 180, 240, 360, 720, 1,440. Default 60.
- `N` slider 100 to 10,000, step 100. Default 3,000.
- `S` slider 15 to 240 minutes, step 5. Default 90.
- `W` slider 0 to 60 minutes, step 5. Default 15.
- `n_min` slider 5 to 200. Default 40. `n_max` slider 50 to 500. Default 300.
- `p` (planners) slider 0 to 0.5, step 0.05. Default 0.
- Button "Snap to knee" sets `T = S + W` (allowed off the snap list).

**Readouts:** reach `min(1, (S + W)/T)` as a percent to one decimal; crowd `N × min(S + W, T)/1440` to one decimal; players shut out per day `N × (1 − reach)`; `N_crit = 1440 × n_min/(S + W)` to one decimal; a status line: "fills" if crowd ≥ `n_min`, "too thin" otherwise, "over the band, needs copies" if crowd > `n_max`.

**Test values (defaults `N = 3,000`, `S = 90`, `W = 15`):**
- `T = 30`: reach 100.0%, crowd 62.5.
- `T = 60`: reach 100.0%, crowd 125.0.
- `T = 105`: reach 100.0%, crowd 218.8.
- `T = 120`: reach 87.5%, crowd 218.8.
- `T = 180`: reach 58.3%, crowd 218.8, shut out 1,250.
- `T = 1,440`: reach 7.3%, crowd 218.8.
- `n_min = 40`: `N_crit = 548.6`.
- `N = 2,000`, `S = 60`, `W = 10`: knee 70, crowd at knee 97.2, reach at `T = 240` is 29.2%.
- `p = 0.2`, `T = 1,440`: planned-occurrence crowd 818.8.

Use the program palette from `templates/interactive-tokens.css`. No game names or art; label it "world boss."
