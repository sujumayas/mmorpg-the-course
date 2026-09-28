# MMO301 · Week 12 — Persistence and Time: What Should Last?

**Why this matters:** "Persistent world" sounds like a feature you either have or don't. In practice every object in your world needs an answer to one question: how long does this last? Get it wrong in one direction and the world fills with abandoned junk and empty houses. Get it wrong in the other and players lose the things that made the world theirs. This week gives you one equation that sizes the problem and a set of rules for deciding what earns permanence.

**You will be able to:**
- Describe a world's persistence using Bartle's ladder (what survives a reboot) and place real worlds on it.
- Compute the steady-state number of objects in a world with `S = λ × W`, and predict how long a world takes to reach it for fixed and random lifetimes.
- Design a persistence budget that assigns a lifetime to each class of object and justify each choice by who depends on the object.
- Convert between real time and an accelerated world clock and critique a world-time design.

**Before class:** Bartle, *Designing Virtual Worlds* (2003, free CC edition), chapter 1, "Dimensions: Change and Persistence" (pp. 73-83), and chapter 4, "Unending or Circular?" and "Reset Strategy." Reread the persistence and identity rules on Koster's "Laws of Online World Design" page from last week.

**Prerequisites from earlier courses:** [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) gives you the bathtub rule this week's model extends. [GS101 week 5, text adventures and MUD1](../../GS101-history-and-critical-study-of-games/lectures/w05-text-adventures-and-mud1.md) introduces MUD1's resets, the first answer to "what should last." [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) covers the `1 − e^(−t/W)` curve. [MMO304 week 8, item decay and destruction as sinks](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w08-item-decay-durability-and-destruction-as-sinks.md) treats the economic side of objects that do not last; this week treats the world side. Within this course, [week 10](w10-immersion-identity-and-the-avatar.md) on identity and [week 11](w11-kosters-laws-of-online-world-design.md) on Koster's Laws come first.

**Interactive:** [examples/w12-clutter-law.html](../examples/w12-clutter-law.html). Keep it open during section 2.

---

## 1. Persistence is a ladder too

Bartle's definition of a virtual world requires that it be persistent "at least to some degree." He then measures the degree with a blunt test: if you shut the whole system down and restart it, how much of the world's state comes back intact?

Every virtual world keeps something. What it keeps varies a lot. In his 2003 survey Bartle describes a ladder:

| Rung | What survives a reboot | Example Bartle gives (2003) |
|---|---|---|
| 1 | The world's starting state and each player character's record | AberMUDs |
| 2 | Also what characters were carrying | DikuMUDs |
| 3 | Also certain classes of object, such as corpses | EverQuest |
| 4 | The entire state of the world | Ultima Online |
| 5 | The entire world plus all functionality added since launch | MOOs |

The higher the rung, the more the world remembers. That sounds like "higher is better." It is not.

Bartle points out a reason to stay low. Adventure worlds often have puzzles with world-wide effects: a dam that bursts, a rocket that launches. You cannot un-burst a dam. If the world never resets, each of those puzzles can be solved once, by one group, and then it is gone for everyone who arrives later. Designers who spent weeks building a quest do not want it used by a handful of players. So they choose to reset, and to persist less.

### Circular or unending

Bartle frames the same choice at the scale of the whole world. A **circular** world reuses its content: the dragon respawns, the dam is rebuilt, and every player gets the same adventure. An **unending** world changes permanently: the dragon stays dead, and the next players get something else. Circular worlds are cheap and the same for everyone, but nothing a player does changes the world. Unending worlds make actions matter, but they are costly, because content is used up and new content has to be made to replace it.

Most commercial MMOs are circular for content (dungeons reset, quests repeat) and persistent for characters (levels, items and names last). That split is a design decision, not a law of nature.

### Resets: sudden and rolling

When a circular world returns its content, it resets. MUD1 did this in one go: when the treasure was gone, everyone was told to leave and re-enter a fresh world (GS101 week 5 models its effect on players). Bartle calls this a **sudden reset**. A **rolling reset** returns content piecemeal, at roughly the rate players consume it, without closing the world. The monster that respawns five minutes after you kill it is a rolling reset. Bartle notes that both are anti-immersion. Sudden resets deliver a big jolt of "this is software," rolling resets a steady trickle of small ones.

### Who builds, and how long it lasts

Bartle's survey found one more pattern. Worlds where more kinds of people can add content (only paid staff, trusted players, or anyone) tend to persist more of what is added. LambdaMOO, where anyone could build, kept everything. He poses the choice as a question of trust. If you do not trust players to add content, go for low persistence and little change. If you trust them completely, go for high persistence and let them change the world.

Keep that framing. The rest of this lecture asks it about every object type, one at a time.

## 2. Worked example: the clutter law

### The hook

In Minecraft (Java Edition), an item dropped on the ground disappears after five minutes. Die far from home, and if you do not get back to your stuff in time, it is gone. Players complain about this constantly. It seems petty. The server has plenty of storage. Why not keep items forever?

In EVE Online, the wreck left by a destroyed ship lasts two hours before it despawns. In Final Fantasy XIV, a house whose owner has not entered it for 45 days is demolished. Three games, three lifetimes, spanning four orders of magnitude. Each looks arbitrary. They all come from the same equation.

### The model

Think of every object type in your world as a stock (GD102 week 2). Objects are created at some rate and each one lasts for some time before it despawns. Let:

- `λ` be the creation rate, in objects per day, across the whole world.
- `W` be the average lifetime of one object, in days.
- `S` be the number of objects in the world at a given moment.

Once the world has run for longer than a typical lifetime, the stock settles at:

```
S = λ × W
```

This is **Little's law**, a result from queueing theory that holds for any system in a steady state, whatever the distribution of lifetimes. The bathtub fills until the outflow matches the inflow, and the outflow is `S / W`. Set `S / W = λ` and you get the formula.

How fast does the world get there? That depends on how lifetimes are distributed.

- **Fixed lifetime** (every object lasts exactly `W`): `S(t) = λ × min(t, W)`. The stock rises in a straight line and stops at `λW` after exactly `W`.
- **Random lifetime** (each object has the same chance per moment of vanishing, so lifetimes are exponential with mean `W`): `S(t) = λW (1 − e^(−t/W))`. The stock reaches 63% of its ceiling at `t = W` and 95% at `t = 3W`.
- **No lifetime** (`W` infinite): `S(t) = λt`. No ceiling. The stock grows forever.

That last line is the one designers forget. "Persistent" objects with no expiry do not make a big stock. They make a stock with no upper limit.

### Numbers you can check

Take an invented world with 10,000 active players who each leave 4 objects in the world per day: dropped items, campfires, corpses, placed decorations. So `λ = 40,000` objects per day. Suppose each object record takes 200 bytes and the world has 20 zones.

| Lifetime `W` | `W` in days | Steady stock `S = λW` | Per zone | Storage at 200 bytes |
|---|---|---|---|---|
| 5 minutes | 0.00347 | 139 | 7 | 28 KB |
| 2 hours | 0.0833 | 3,333 | 167 | 0.67 MB |
| 1 day | 1 | 40,000 | 2,000 | 8 MB |
| 45 days | 45 | 1,800,000 | 90,000 | 360 MB |
| 1 year | 365 | 14,600,000 | 730,000 | 2.9 GB |
| Forever, after 5 years | no limit | 73,000,000 and rising | 3,650,000 | 14.6 GB and rising |

Check one row: `40,000 × 45 = 1,800,000`, and `1,800,000 / 20 = 90,000` per zone.

Storage is the least of the problems. A single gigabyte is cheap. What costs you is the per-zone column. Five-minute items give a zone 7 loose objects, which is a few items scattered on the ground. One-day items give 2,000, which already means every path is littered. At 45 days, 90,000 objects per zone overwhelms the renderer, the pathfinding and the player's eyes. The Minecraft choice looks petty from one player's seat. From the world's seat, it is what keeps the ground visible.

Now the timing. With exponential lifetimes and `W = 45` days:

| Days since launch `t` | `t / W` | Share of ceiling `1 − e^(−t/W)` | Stock |
|---|---|---|---|
| 45 | 1 | 63.2% | 1,137,817 |
| 90 | 2 | 86.5% | 1,556,396 |
| 135 | 3 | 95.0% | 1,710,383 |

This matters for testing. A beta that runs for two weeks sees less than a third of the long-run clutter of a 45-day object. The problem appears months after launch, when the team has moved on to other things.

### A visual you can move

Open `examples/w12-clutter-law.html`. The left view, "The first month," plots the stock over 30 days. At a 45-day lifetime and a 1-year lifetime the two lines look almost the same: both climb steadily. The right view, "The long run," plots the same thing over five years on a log scale, with a dashed ceiling at `λW`. Now the lines separate by a factor of eight, and the "forever" line never stops. Switch the lifetime type between fixed and random and watch how the corner of the curve rounds off without moving the ceiling. The point to see: a month of data cannot tell you where the ceiling is.

### Cross-game recognition

**Minecraft (Java Edition, current versions).** Dropped items despawn after 6,000 game ticks, which is 5 minutes, but only while the chunk they are in is loaded. The timer pauses when no player is nearby to keep the chunk active. In the model, `W` is measured in observed time, not wall-clock time. Items left in unloaded chunks last indefinitely, but nobody sees them, so they add nothing to anyone's clutter. That is a neat trick: the world only pays for persistence where a player is looking. Bartle describes an old rolling-reset idea along the same lines, returning content only where players are not watching.

**EVE Online (current game).** Wrecks from destroyed ships persist for two hours. In a single-shard world ([week 6](w06-eve-online-the-single-shard-sandbox.md)) where combat never stops, a lifetime of days would leave every contested system filled with wrecks. Two hours is long enough for salvagers to reach a battlefield and for the loot to become a small economy of its own, and short enough to keep `λW` manageable. The lifetime was chosen for a player activity (salvaging) as well as for clutter.

**Final Fantasy XIV (current game, housing).** A house counts as abandoned if its owner, or for a Free Company house any member, does not enter it for 45 days. Warnings appear at day 30, then 35, then 42, and at day 45 the house is demolished and the plot returns to the pool. Apply Little's law to the abandoned houses only. Suppose a world has 1,000 owned plots and 10 owners quit the game each week. Then `λ = 10/7 = 1.43` newly abandoned houses per day, and `S = 1.43 × 45 = 64` abandoned houses standing at any time, 6.4% of plots. That is 64 plots that look lived in but are dead, while players who want a house wait for a lottery. With a 90-day rule, it is 129. With no rule, abandoned houses pile up until most plots are empty shells. Square Enix has at times suspended the timers for players in regions hit by real disasters, which is a reminder that `W` is a policy lever, not a technical constant.

Three games, three lifetimes, one equation. When you see a despawn timer, ask what `λ` it was sized against.

### Eyes-open design judgment

Little's law tells you the cost of a lifetime. It does not tell you which lifetime is right. That depends on who depends on the object.

- **Short lifetimes are cheap and cruel.** Five-minute items keep the world clean and punish the player who died far away. If you choose them, give players a way to protect what matters: a corpse that holds items longer than loose drops, or a marker on the map.
- **Long lifetimes turn objects into landmarks, then into junk.** A campfire that lasts a week makes the world feel lived in. A campfire that lasts forever makes it feel like a landfill. Pick the lifetime at which your per-zone count stops looking alive and starts looking littered.
- **Conditional lifetimes beat fixed ones for things people care about.** FFXIV's rule does not demolish houses after 45 days. It demolishes houses nobody has visited in 45 days. The clock resets whenever someone shows the house still matters. That is a much better signal than age.
- **Warn before you delete.** FFXIV's day 30, 35 and 42 warnings turn a surprise loss into a choice. Every expiry of something a player built should come with notice.
- **Watch the loop with scarcity.** If plots, names or spawn points are limited, the lifetime of abandoned ones sets how long new players wait. A generous lifetime for absent owners is a harsh lifetime for newcomers. MMO401 week 10 treats scarcity by design.

### Check yourself (worked example)

1. A survival MMO has 2,000 players online on average across a day, and each places 6 campfires per day. Campfires last 30 minutes. How many campfires exist at a typical moment?
2. The same world lets players build shelters. 5,000 players build 3 shelters per week each, and shelters last 7 days. What is the steady stock? What would it be after one year if shelters never decayed?
3. With random (exponential) lifetimes, a designer's two-week beta shows 400,000 shelters for an object with `W = 60` days. Roughly what ceiling should they expect?

<details>
<summary>Answers</summary>

1. `λ = 2,000 × 6 = 12,000` per day. `W = 30/1,440 = 0.0208` days. `S = 12,000 × 0.0208 = 250` campfires.
2. `λ = 5,000 × 3 / 7 = 2,143` per day. `S = 2,143 × 7 = 15,000` shelters. Without decay, after a year `S = 2,143 × 365 ≈ 782,000`, and still rising.
3. At `t = 14`, `t/W = 0.233`, and `1 − e^(−0.233) = 0.208`. So 400,000 is about 21% of the ceiling, which is about `400,000 / 0.208 ≈ 1.92` million.

</details>

## 3. World time

Persistence is about how long things last. Worlds also need an answer to what time it is.

### Real clock or world clock

Some worlds run on real time: when it is evening on the server, it is evening in the world. Others run an accelerated clock so players see day and night in a single session. Final Fantasy XIV's world clock, Eorzea time, runs one full in-game day in 70 real minutes. So:

```
acceleration = 1,440 real minutes per day / 70 = 20.57
one real week = 10,080 / 70 = 144 world days
one real year = 525,600 / 70 ≈ 7,509 world days
```

An accelerated clock lets a player who only plays evenings see dawn, and it lets designers tie events, weather or monster spawns to world time without locking out players in some time zones. Its cost shows up in Bartle's question about aging. If a world's calendar ran at 20.57 times real speed and counted 365-day years, a character played for three real years would be about 62 world-years older. No MMO ages its characters, so the fiction quietly ignores its own clock. Bartle's joke is that everyone must drink from a fountain of youth.

### Real calendars carry the feelings

Koster's collection includes a design rule about calendars: only real-world dates carry emotional weight. An in-game festival on the 12th of a fantasy month means nothing. A winter festival in December or an anniversary event on the day the servers opened means something, because players remember where they were. Many live MMOs follow this rule, running seasonal events on real dates even when they also have an in-world calendar.

### Resets as time

The other clock in most MMOs is the reset schedule: daily quests, weekly raid lockouts, seasons. These are sudden resets in Bartle's sense, applied to one player's progress rather than the whole world. They set the rhythm of a player's week. From this lecture's point of view they are persistence decisions: a weekly lockout says "your victory over this boss lasts seven days." Choose the period by asking what rhythm you want players to live by, and remember that the reset moment is also a moment of reminder that it is a game.

## 4. What should last: a persistence budget

Put the pieces together. A **persistence budget** is a table that lists every class of object in your world and assigns it a lifetime, a rule for when the clock resets, and a reason.

Here is a worked budget for an invented sandbox MMO, with the reasons written out.

| Object class | Lifetime `W` | Clock resets when | Who depends on it | Reason |
|---|---|---|---|---|
| Loose dropped items | 10 minutes | never | the dropper, briefly | Clutter control; `λ` is huge |
| Player corpse with gear | 2 hours | owner returns | the owner | Death should cost, not destroy |
| Campfires, markers | 1 day | someone uses it | nearby players | Signs of life, not landfill |
| Player houses | 60 days | owner or co-owner enters | owner, visitors, neighbours | Protects active owners, frees plots |
| Guild halls | 120 days | any member enters | a whole guild | More people depend on it |
| Character names | permanent while account active; released after 1 year idle | owner logs in | everyone who knows the name | Identity (week 10) |
| Achievements, titles, history | permanent | — | the player's reputation | Identity and memory |
| World-changing events | permanent | — | everyone | Makes the world unending where it matters |

Four rules come out of building budgets like this.

**Persist what other people depend on.** The more players rely on an object (a guild hall, a road, a famous name), the longer it should last and the more people should be able to renew it. This is Bartle's trust-and-change link applied one object at a time.

**Persist identity.** Names, histories and achievements are cheap (`λ` is small, since they are created rarely) and they are what makes a persona possible. Week 10 showed that identity needs witnesses and continuity. Deleting a player's history is deleting their identity.

**Expire what only has value in the moment.** Loose items, temporary markers and wrecks exist for a scene. Let them go when the scene is over.

**Never break a persistence promise silently.** Koster's persistence rule says that once a world opens, players expect it to last. Every rollback, wipe or removal breaks that expectation. Sometimes you must (an exploit that ruined the economy, as in [MMO401 week 12](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w12-economic-shocks-exploits-and-rollbacks.md)). When you do, announce what is lost, why, and what persists. [Week 13](w13-worlds-that-died-shutdowns-and-their-lessons.md) looks at the ultimate broken promise, shutting a world down.

## In-class activity (25 minutes)

Pairs. Each pair receives a one-paragraph world concept from the instructor, for example "a frontier settlement world where players build farms and roads," "a city of 50,000 players with player-run shops," or "an ocean world of player ships and floating wreckage."

1. **(10 min)** List at least six object classes the world will create. For each, estimate `λ` (per day, whole world) from a player count of 20,000 and a guess at how often each player creates one.
2. **(10 min)** Assign each class a lifetime and a clock-reset rule. Compute `S = λW` for each. Divide by a zone count of your choice and mark any class whose per-zone count looks unreasonable.
3. **(5 min)** Choose the one class where your players will be angriest about the lifetime you chose. Write the warning message they will see before it expires.

Expected output: a six-row persistence budget with `λ`, `W`, `S` and per-zone counts, one flagged row, and one warning message. Two or three pairs present their angriest-player row.

## Common misconceptions

- **"More persistence is always better."** Every object that never expires is a stock with no ceiling. Some content, like puzzles with world-wide effects, needs resets to exist at all.
- **"Storage cost is why games despawn things."** Storage is cheap. Per-zone density, rendering, pathfinding and what the player can see are the real limits, along with scarce resources such as plots.
- **"If the beta looked fine, the live world will too."** A stock with lifetime `W` needs about `3W` to approach its ceiling. A two-week beta cannot show the clutter of a two-month object.
- **"The lifetime should be a fixed number of days."** For objects people care about, a clock that resets on use (conditional lifetime) protects active players and frees what is abandoned. Age alone is a poor signal.

## Check yourself

1. Place a single-player open-world game, a battle royale match and a player-built city server on Bartle's persistence ladder, and justify each in one sentence.
2. A world has 3,000 house plots. Owners quit at 1% per week. The demolition rule is 30 days without a visit. How many abandoned houses stand at a typical time, and what share of plots is that?
3. A designer wants to double the demolition period in question 2 to "be kinder to players." What is the cost, in plots, and who pays it?
4. A world clock runs one day per 90 real minutes. How many world days pass in a real week? A player logs in for two hours at the same real time every evening. Does that player ever see the full day and night cycle?
5. A team wants player-built statues to last forever. Players build 50 statues per day world-wide. What stock will the world have after 3 years, and what would you propose instead?

<details>
<summary>Answers</summary>

1. The single-player open world persists the whole world state in the player's save, but it is not shared, so it is not a virtual world at all. The battle royale persists only character or account records between matches (rung 1 at best), and the match state resets each round. A player-built city server that keeps every structure persists the entire world state (rung 4).
2. `λ = 3,000 × 0.01 / 7 = 4.29` abandoned houses per day. `S = 4.29 × 30 ≈ 129` houses, about 4.3% of plots.
3. At 60 days, `S ≈ 257` abandoned houses, about 8.6% of plots, so about 129 more plots are locked up by absent owners. The cost is paid by players waiting for a plot, usually newer players. Being kind to absent owners is being harsh to present newcomers.
4. `10,080 / 90 = 112` world days per real week. Yes. A two-hour session is 120 minutes, longer than one 90-minute world day, so every session covers a full cycle. (With a 150-minute day it would not.)
5. `50 × 365 × 3 = 54,750` statues, with no ceiling. Propose a conditional lifetime, for example statues decay unless visited or maintained by any player within 90 days, giving at most about `50 × 90 = 4,500` standing unmaintained at once, while statues players care about last as long as they keep caring. Alternatively make a small, curated set permanent (event winners, server-first achievements) and let the rest decay.

</details>

## Lab / assignment hook

[Lab 12, the persistence budget](../labs/lab12.md). You will build a spreadsheet persistence budget for your own world concept, with at least ten object classes, steady-state stocks, per-zone density, time to reach 95% of the ceiling, and a warning plan. The budget becomes the persistence chapter of your world design bible.

## Sources

- Bartle, R. A. (2003). *Designing Virtual Worlds*. New Riders, free CC edition. Chapter 1, "Dimensions: Change and Persistence" and Table 1.3 (pp. 73-83): persistence as what survives a reboot; the ladder from AberMUDs to MOOs; the link between who can build and how much persists; the four trust options. Chapter 4, "Unending or Circular?" (pp. 336-337) and "Reset Strategy" (pp. 462-465): sudden and rolling resets, resets as anti-immersion, the rolling reset that returns content where players are not looking. Chapter 5, "Long-Term Characters" (pp. 505-506): the aging problem in worlds with a day-night cycle.
- Koster, R., "The Laws of Online World Design" (raphkoster.com, page updated 2023). Design rules that worlds are expected never to close and that only real-world calendar dates carry emotional weight.
- Minecraft Wiki, "Item (entity)" (Java Edition, current versions, accessed September 2026). Dropped items despawn after 6,000 ticks (5 minutes) in a loaded, entity-ticking chunk; the timer pauses when the chunk is unloaded.
- EVE University Wiki, "Salvaging" (current game, accessed September 2026). Wrecks persist for two hours.
- Final Fantasy XIV Online wiki (consolegameswiki), "Housing" (current game, patch 6.1 lottery onward, accessed September 2026). Automatic demolition after 45 days without the owner (or a Free Company member) entering; notifications at days 30, 35 and 42; timers suspended for some regions after major disasters.
- Final Fantasy XIV Online wiki (consolegameswiki), "Eorzea Time" (current game, accessed September 2026). One Eorzean day equals 70 real minutes.
- Little's law (`L = λW`) is a standard result of queueing theory (Little, J. D. C., 1961, "A Proof for the Queuing Formula L = λW," *Operations Research* 9(3), 383-387).

## Interactive spec: examples/w12-clutter-law.html

**The one insight:** the number of objects in a world settles at `S = λ × W`, and a month of data cannot tell a 45-day lifetime from a 1-year lifetime or from "forever." The long-run view reveals ceilings that differ by orders of magnitude, and no ceiling at all for permanent objects.

**Layout.** Two linked views, side by side on desktop, stacked on mobile (short-run view on top).

- **Left view, "The first month":** stock `S(t)` for `t` from 0 to 30 days, linear axes. Plot the current lifetime as a thick accent line and, as thin comparison lines, the preset lifetimes 1 day, 45 days, 1 year and forever (toggleable via a "show comparisons" checkbox, default on). Label each line at its right end.
- **Right view, "The long run":** the same lines for `t` from 0 to 1,825 days (5 years), vertical axis logarithmic from 10 to 1e9. Draw each finite lifetime's ceiling `λW` as a dashed horizontal line in the line's colour. Mark `t = W` and `t = 3W` for the current lifetime with small ticks labelled "63%" and "95%" (random mode) or "100%" at `t = W` (fixed mode).
- **Below both views, "Per zone":** a row of `Z` small squares (cap drawing at 50), each filled with a dot density proportional to `log10(S/Z)`, with the text "Per zone at steady state: N objects".
- **Readouts (copyable):** `λ` (per day), `W` in days (5 decimals when below 1), steady stock `S = λW` (whole number), per zone `S/Z` (whole number), storage `S × bytes` (auto units KB, MB, GB, 2 decimals), stock at day 30 and at day 365 for the current lifetime, time to 95% of ceiling (`3W` in random mode, `W` in fixed mode).

**Controls (keyboard accessible, labelled):**

1. Active players `N`: log slider 100 to 1,000,000, default 10,000.
2. Objects per player per day `k`: slider 0.1 to 50, step 0.1, default 4.
3. Lifetime `W`: preset buttons "5 min", "2 h", "1 day", "7 days", "45 days", "1 year", "Forever", plus a log slider from 1 minute to 5 years for custom values. Default 45 days.
4. Lifetime type: radio "Fixed" / "Random (exponential)". Default Random.
5. Zones `Z`: slider 1 to 200, default 20.
6. Bytes per object: slider 50 to 2,000, step 50, default 200.
7. Reset button.

**Formulas.**

```
λ          = N × k                                   objects per day
S_ceiling  = λ × W
S_fixed(t) = λ × min(t, W)
S_rand(t)  = λ × W × (1 − exp(−t / W))
S_forever  = λ × t
per_zone   = S_ceiling / Z
storage    = S_ceiling × bytes
t95        = 3W (random), W (fixed)
```

**Test values** (`N = 10,000`, `k = 4`, so `λ = 40,000`; `Z = 20`; 200 bytes):

| `W` | `S` | Per zone | Storage |
|---|---|---|---|
| 5 min (0.00347 d) | 139 | 7 | 27.78 KB |
| 2 h (0.08333 d) | 3,333 | 167 | 666.67 KB |
| 1 day | 40,000 | 2,000 | 8.00 MB |
| 45 days | 1,800,000 | 90,000 | 360.00 MB |
| 1 year | 14,600,000 | 730,000 | 2.92 GB |
| Forever, at 5 years | 73,000,000 | 3,650,000 | 14.60 GB |

Random mode, `W = 45`: `S(45) = 1,137,817`; `S(90) = 1,556,396`; `S(135) = 1,710,383`; `S(30) = 40,000 × 45 × (1 − e^(−0.6667)) = 875,849`. Fixed mode, `W = 45`: `S(30) = 1,200,000`; `S(45) = 1,800,000`.

Random mode, `W = 365`, `S(30) = 40,000 × 365 × (1 − e^(−0.08219)) = 1,152,009`. Forever: `S(30) = 1,200,000`. These three day-30 values (875,849, 1,152,009, 1,200,000) must be visibly close on the left chart; that is the point.

Houses variant for the check: `N = 1,000` owners, `k = 1/700` (1% quitting per week), `W = 45`: `λ = 1.4286`, `S = 64`.

**First screen:** `W = 45` days, random mode, comparisons on. Caption above both views: "After 30 days, 45-day, 1-year and permanent objects look alike. After 5 years: 1.8 million, 14.6 million, and 73 million and climbing."

**Content rules.** No game art. Objects are plain dots, zones are plain squares. Small text under the views: "Invented world. Little's law holds for any lifetime distribution; only the approach to the ceiling depends on the distribution."
