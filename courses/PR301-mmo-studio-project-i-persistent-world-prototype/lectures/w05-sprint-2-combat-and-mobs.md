# PR301 · Week 05 — Sprint 2: Combat and Mobs

**Why this matters:** In PR201 a mob was something three players fought. In a persistent world a mob is also a resource that fifty players compete for, and a faucet that pays gold into your economy. A respawn timer that feels fine when you test with three people leaves fifteen players standing in an empty field on the alpha weekend. That is a supply problem, and you can size it before you build a single camp.

**You will be able to:**
- Plan sprint 2 from your measured sprint 1 focus factor, with combat and mobs as one playable loop.
- Compute the kill demand a crowd puts on a mob camp and the kill supply the camp can give, from time-to-kill, travel time, spawn count and respawn timer.
- Predict the share of time players wait for spawns at a given crowd, and design a respawn rule that keeps utilization at or below 0.8.
- Trace how a respawn timer changes the currency faucet per player.

**Before class:** Reread [MMO303 week 3](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w03-effective-hp-and-effective-dps.md) section 6 (the time-to-kill matrix), [MMO304 week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) (faucets and sinks) and [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) section 2 (why queues blow up near full use). Bring the tagged sprint 1 build on the test host, the soak logs, the sprint board and the draft sprint 2 input list. The sprint 1 review opens the session.

**Prerequisites from earlier courses:** [PR201 week 6](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w06-sprint-2-core-combat.md) for combat as a networking feature and the dependency rule for planning. [MMO302 week 5](../../MMO302-mmo-server-architecture/lectures/w05-tick-rate-for-mmos-vs-shooters.md) for tick budgets. [MMO302 week 6](../../MMO302-mmo-server-architecture/lectures/w06-simulation-authority-and-anti-cheat-by-design.md) for the server deciding hits. [CS203 week 6](../../CS203-artificial-intelligence-for-games/lectures/w06-finite-state-machines.md) for mob behaviour as a state machine. [MMO305 week 3](../../MMO305-social-systems-and-online-behaviour/lectures/w03-forced-vs-voluntary-grouping.md) for how shared kill credit changes whether strangers group.

**Interactive:** [Spawn supply model](../examples/w05-spawn-supply.html)

---

## 1. What sprint 2 has to prove

Sprint 2's goal for most teams reads something like this: "Players fight server-controlled mobs in the shared world, and the server decides every hit." The *Saltmarsh* version adds its world: "Twenty bots and three humans hunt the Reedbank wolf camp at once, and every kill, drop and death is decided and saved by the server."

PR201 week 6 taught the planning rule for combat. Commit the chain that makes the loop playable first (attack, damage, death, feedback, one enemy) and only then add stories that widen it. That rule still holds. The persistent world adds three things the slice never had.

- **Many players, one camp.** Mobs are shared. Who gets credit for a kill, who gets the drop, and how long until the next wolf appears are now design questions with economic effects.
- **Drops are persistent.** A wolf pelt that lands in an inventory is a database write. Your week 2 persistence map says loot is write-through, in one transaction with the kill credit.
- **Mobs cost CPU all the time.** A mob thinks every tick whether or not anyone fights it. Week 6 measures what one more mob costs. This week, keep the count you plan within the `m` you used in the week 2 capacity sheet.

Plan with your own number. The sprint 1 review, in the first part of this session, measured the *Saltmarsh* focus factor at 0.46, so each person has `0.46 × 13 = 6.0` hours of estimated work this sprint, and the team 38.2. Run the week 3 load check per person with those values before committing anything.

## 2. Worked example: will the camp feed the crowd?

### The hook

When World of Warcraft Classic launched on 26 August 2019, Blizzard did not run one copy of each starting zone per realm. It ran several. Each **layer** was a full copy of the outdoor world with its own NPCs and its own herbs and ore. Put the players of a busy realm into one copy and there would not be enough wolves, boars and quest mobs for them. Blizzard multiplied the supply by copying the world, and on 13 November 2019, once the crowds had spread out, went back to a single layer per realm.

You have one copy of the world and no layers. The question is the same. When fifteen people stand at your first camp on Friday night, is there enough to kill?

### The model

Treat a camp as a supplier of kills and the players at it as a demand for kills.

```
k   = 60 / (TTK + t)            kills per minute one player wants
λ   = P × k                     kills per minute the camp is asked for
μ   = M × 60 / T                kills per minute the camp can supply
ρ   = λ / μ                     utilization
idle = max(0, 1 − μ / λ)        share of their time players spend waiting for a spawn
```

- `TTK` is time to kill one mob in seconds, from [MMO303 week 3](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w03-effective-hp-and-effective-dps.md): the mob's effective HP divided by the player's effective DPS.
- `t` is the seconds between kills when a mob is available: walking, looting, resting.
- `P` is the number of players hunting at the camp.
- `M` is the number of spawn points, and `T` is the respawn timer in seconds, started when the mob dies. At best each spawn point produces one kill every `T` seconds.
- `ρ` above 1 means players ask for more kills than the camp can supply. The camp then delivers `μ`, and each player gets `μ / P` kills a minute instead of `k`.

The target is `ρ ≤ 0.8`, not 1. Players arrive and kill at random moments, not in a neat rotation. [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) showed that waiting in a queue grows sharply as utilization approaches 1, long before it reaches it. The simple `idle` formula is zero below `ρ = 1`. Real players start waiting earlier. The 0.8 target leaves room for that.

A **dynamic respawn** sets `T` from the crowd instead of fixing it:

```
T(P) = clamp( M × 60 × 0.8 / λ,  T_min,  T_max )
```

It solves `ρ = 0.8` for `T`, then keeps the answer between a floor `T_min` (so a mob never pops back on top of the player who killed it) and a ceiling `T_max` (so a quiet camp still looks like the designer intended).

### Numbers you can check

The Reedbank camp has `M = 12` wolves on a fixed timer of `T = 90` seconds, which the designer chose while testing with three people. A wolf has 600 effective HP against a starting character's 30 effective DPS, so `TTK = 20` seconds, and looting and walking to the next wolf take `t = 10`. So `k = 60 / 30 = 2` kills a minute, and supply is `μ = 12 × 60 / 90 = 8` kills a minute.

| Players `P` | Demand `λ` | Supply `μ` (`T = 90`) | `ρ` | Idle |
|---|---|---|---|---|
| 3 | 6 | 8 | 0.75 | 0% |
| 6 | 12 | 8 | 1.50 | 33% |
| 10 | 20 | 8 | 2.50 | 60% |
| 15 | 30 | 8 | 3.75 | 73% |
| 20 | 40 | 8 | 5.00 | 80% |

Check the 10-player row: `λ = 10 × 2 = 20`, `ρ = 20 / 8 = 2.5`, and `idle = 1 − 8 / 20 = 0.6`. At ten players, each spends 60% of their time standing around. At the design test with three people the camp looked perfect.

**Fix 1: a shorter fixed timer.** At `T = 30`, supply is 24 kills a minute. Ten players give `ρ = 0.83`, fifteen give 1.25 and a 20% idle share, twenty give 1.67 and 40%. Better, and still failing at the crowd the alpha will bring. It also means three players meet a wolf respawning 30 seconds after they killed it, in a camp that never clears.

**Fix 2: dynamic respawn.** With `T_min = 20` and `T_max = 90`:

| Players | Demand | `T(P)` | Supply | `ρ` | Idle |
|---|---|---|---|---|---|
| 3 | 6 | 90.0 (ceiling) | 8.0 | 0.75 | 0% |
| 6 | 12 | 48.0 | 15.0 | 0.80 | 0% |
| 10 | 20 | 28.8 | 25.0 | 0.80 | 0% |
| 15 | 30 | 20.0 (floor) | 36.0 | 0.83 | 0% |
| 20 | 40 | 20.0 (floor) | 36.0 | 1.11 | 10% |

Check `T(10)`: `12 × 60 × 0.8 / 20 = 576 / 20 = 28.8` seconds. The rule holds the camp at 0.8 until the floor stops it. Above about 14 players, twelve spawn points cannot keep up without wolves appearing on top of people.

**Fix 3: more spawn points, with dynamic respawn.** At `M = 18`, the floor is not reached until about 21 players. At 20 players `T = 21.6` seconds, supply is 50 and `ρ = 0.80`. Every row from 3 to 20 players sits at or below 0.8. The cost is six more wolves thinking every tick, which is within the `m = 60` the week 2 capacity sheet allowed for the whole area.

Run `check_camps.py` from [lab 05](../labs/lab05.md) to reproduce all three tables. The starter file holds all three designs and fails. Keep only the dynamic design, change its `spawns` to 18, and it prints `PASS`.

### What the timer does to the economy

Each wolf drops an average of 5 copper. A player who is never kept waiting earns `2 × 60 × 5 = 600` copper an hour. On the fixed 90-second timer with ten players, each gets `8 / 10 = 0.8` kills a minute, which is `0.8 × 60 × 5 = 240` copper an hour, 40% of what the designer planned. With dynamic respawn and 18 spawn points, every player earns 600 at any crowd size from 3 to 20.

That is the connection to [MMO304 week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md). A respawn timer is a faucet valve. With a fixed timer, the camp's total output is capped, so income per player falls as the crowd grows, and the players who log in during a busy hour are poorer. With a dynamic timer the faucet scales with the population, and total currency entering the world is proportional to player-hours. Choose deliberately. Some worlds want crowds to compete for scarce spawns. Most first worlds just want players to play.

### The same idea elsewhere

**WoW Classic layering.** Layers raised `μ` by copying the whole camp, `M` and all, once per layer. It worked at launch, and it also split players who wanted to see each other. Wikipedia's article on WoW Classic records that players were found using layers to exploit the in-game economy. More supply in a copy is still more faucet.

**Guild Wars 2 dynamic events.** ArenaNet scales events up and down with the number of players nearby, and even a player who is not taking part scales an event up. That is the same move as dynamic respawn, applied to the enemies in an event rather than to a timer. Supply follows demand.

**World of Warcraft's fast respawn.** The Warcraft Wiki describes a fast respawn mode that switches on when an area is farmed heavily and mobs die soon after they spawn. Mobs and resource nodes then return much more quickly, usually within a minute. The wiki does not date the change, so treat it as current retail behaviour. It is a dynamic respawn with a trigger on kill speed instead of on player count.

**Your login queue.** MMO302 week 9 found that a full world admits players at the rate others leave. A camp at `ρ > 1` is the same: the next kill happens when the next wolf appears, however many players are waiting.

### Eyes-open judgment

The model ignores who gets the kill. Twenty players at `ρ = 0.8` still compete for each spawn. If kill credit goes to the first hit, players race to tag wolves and nobody groups. If credit is shared by everyone who damaged the mob, strangers help each other, and demand per player falls because shared kills count for several people. Decide the credit rule this sprint. It changes `k`, and [MMO305 week 3](../../MMO305-social-systems-and-online-behaviour/lectures/w03-forced-vs-voluntary-grouping.md) showed it changes behaviour more than any timer.

The floor `T_min` is a feel decision, not a maths one. Twenty seconds keeps a wolf from appearing behind the player who just killed it, most of the time. Test it with humans.

A camp that is always full of wolves at any crowd removes a signal. Some designers want a busy camp to feel busy, so players spread out on their own. If that is your pillar, keep the fixed timer and build a second camp, and say so in the design. Just don't do it by accident.

Finally, `TTK` will change. Sprint 3's gear and levels raise effective DPS, which shortens `TTK`, which raises `k` and the demand on every camp. Put the camp table in a sheet linked to the combat numbers so it updates when balance changes.

### Check yourself

1. Starting characters get a new ability, and `TTK` falls to 14 seconds with `t = 10`. With `M = 18`, dynamic respawn, `T_min = 20` and 20 players, what are `k`, `λ`, `T` and `ρ`?
2. A camp has 8 spawn points on a fixed 60-second timer. What is the largest crowd with `ρ ≤ 0.8` at `k = 2`?
3. The economy designer wants income per player to fall by half when a camp is crowded, to push players outward. Which timer design gives that, and at what `ρ`?

<details><summary>Answers</summary>

1. `k = 60 / 24 = 2.5`, `λ = 50`. `T = 18 × 60 × 0.8 / 50 = 17.3`, below the floor, so `T = 20`. Supply `18 × 60 / 20 = 54`, `ρ = 50 / 54 = 0.93`. Over target. Faster combat needs more spawn points or a second camp.
2. `μ = 8 × 60 / 60 = 8`. `ρ ≤ 0.8` needs `λ ≤ 6.4`, so `P ≤ 3.2`. Three players.
3. A fixed timer. Each player gets `μ / P` kills instead of `k`, so income halves when `μ / λ = 0.5`, which is `ρ = 2`. On the 90-second Reedbank camp that is 8 players.

</details>

## 3. Combat on a shared server

PR201 week 6 established that combat is a networking feature. The client sends intent, the server resolves range, cooldown and damage, and the client shows the result. A persistent world adds two rules.

**Resolution and persistence in one place.** The server that decides a kill also writes its consequences. Kill credit, the drop and the experience go into one transaction. If the process crashes between "the wolf died" and "the pelt was saved", the week 2 persistence map says the pelt was never dropped. That is acceptable. The reverse, a pelt saved for a wolf that is still alive after the restart, is a duplication bug.

**Mobs are cheap only when idle.** A wolf with no player within its aggro radius should cost almost nothing per tick. Write the mob state machine ([CS203 week 6](../../CS203-artificial-intelligence-for-games/lectures/w06-finite-state-machines.md)) with an explicit idle state that skips pathfinding and target checks. Week 6 measures the cost of an active mob and an idle one separately. If your idle mob costs the same as your active one, you will find out at the alpha.

## 4. Planning sprint 2

Use the dependency rule from PR201 week 6 on the combat chain, then add the persistent-world stories.

1. **The combat loop**: attack, server-side damage, death and respawn of the player, hit feedback, one mob type with a state machine.
2. **The camp**: spawn points, respawn rule, kill credit rule.
3. **The drop**: loot table, pickup, write-through to the inventory in one transaction with the kill.
4. **The bot**: Dee's bot client from sprint 1 learns to find a wolf, attack it and loot. Without it, the review cannot show twenty hunters at one camp.
5. **Stubs coming due** from sprint 1, ranked against the above by the product owner.

At 38.2 hours, *Saltmarsh* cannot do all of it. Their cut keeps one mob type, a fixed loot table and a first-hit credit rule, with shared credit in the backlog for sprint 3. They keep dynamic respawn because the camp table shows the alpha fails without it.

## Studio session plan

The studio meets for 3 hours. The first part is the sprint 1 review, run as week 4 describes. Teams are paired and each runs the other's restart.

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:50 | Sprint 1 review, both paired teams: goal read aloud and answered yes or no on the tagged build, restart by the other team, final soak read from the log, `f` computed, retrospective | Review record, sprint 1 `f` |
| 0:50 to 1:00 | Briefing: the camp model, the faucet link, the 0.8 target | |
| 1:00 to 1:25 | Camp sizing. Each team fills `camps.csv` for every camp in its starting area from its MMO303 time-to-kill numbers and runs `check_camps.py` | Camp table at `PASS` |
| 1:25 to 1:35 | Break | |
| 1:35 to 1:55 | Credit and drop rules: decide first-hit or shared credit; write the kill transaction as a list of row changes | Rules in `docs/combat.md` |
| 1:55 to 2:40 | Sprint 2 planning with the `f` just measured: dependency order, per-person loads, drop order | `sprint.csv` at `PASS` in the lab 03 checker |
| 2:40 to 3:00 | Bot scenario and instructor check: the hunting bot's steps; each team reads its goal, its camp table at the alpha crowd, and its first cut | Bot scenario list; sign-off |

## Deliverables

The sprint 1 review record and focus factor are due in this session (see week 4). The items below are due at the end of this session, with the burn-down updated through the sprint. Put everything in `production/sprint2/`.

- **Sprint plan** checked with the lab 03 checker at your measured `f`, with goal and drop order.
- **Camp table** (`camps.csv`) for every camp in the starting area, and the saved `check_camps.py` output showing `PASS` at the alpha's expected peak crowd.
- **Combat rules**: kill credit, drop table, respawn rule, and the kill transaction's row changes.
- **Faucet line**: copper per player-hour at the alpha peak, added to the economy sheet.
- **Bot scenarios** for the sprint 2 review.

At the week 6 mid-sprint session: the midpoint build with bots hunting at the camp, and a tick-time log for the load runs. At the sprint 2 review, at the start of week 7: the tagged build and the sprint's evidence. See [lab 05](../labs/lab05.md).

## Common failure modes

- **Tuned with three.** The respawn timer was set while the team played. Fix: size every camp at the alpha's expected peak crowd.
- **Credit by accident.** Whoever's code resolved kills first chose first-hit credit. Fix: decide the rule and write its social effect in one sentence.
- **Loot outside the transaction.** The drop is saved in a later write. Fix: kill credit, drop and experience in one transaction, checked by a restart test.
- **Every mob awake.** Mobs path and scan every tick with nobody near. Fix: an idle state that does nothing.
- **Borrowed focus factor.** The plan uses 0.62 again because 0.46 "was a bad sprint". Fix: plan with the measured value. Revise it after sprint 2 with two data points.

## Review checklist

The instructor checks the sprint 2 plan when:

- [ ] The plan uses the focus factor measured at the sprint 1 review, and every person's load is at or below 1.
- [ ] The combat loop chain is committed before any widening story.
- [ ] `check_camps.py` prints `PASS` for every starting-area camp at the alpha's expected peak crowd.
- [ ] Kill credit and the respawn rule are written down with their intended effect on players.
- [ ] The kill, drop and experience are one transaction, and a restart test for it is in the bot scenarios.
- [ ] The camp faucet appears in the economy sheet in currency per player-hour.

## Sources

- Wikipedia, "World of Warcraft Classic" (read September 2026). Released 26 August 2019; layering at launch; players found using layers to exploit the in-game economy.
- Warcraft Wiki, "Layering" (read September 2026). Added in patch 1.13.2 at the Classic launch; each layer a copy of the outdoor world with its own NPCs and objects such as herbs and mining nodes; realms reduced to a single layer on 13 November 2019.
- Guild Wars 2 Wiki, "Event" (read September 2026, current game). Events scale up and down with the number of players participating, and players nearby who are not participating still scale an event up.
- Warcraft Wiki, "Respawn" (read September 2026, current retail game, no patch date given). A fast respawn mode for heavily farmed areas, returning mobs and resource nodes much more quickly, usually within one minute.
- The *Saltmarsh* team, the Reedbank camp, its wolves, their HP, damage, drops and all timings are invented for teaching. The 0.8 utilization target and the 20-second floor are course conventions.

## Interactive spec

**File:** `examples/w05-spawn-supply.html`

**The one insight:** a respawn timer that looks right at three players starves a crowd, because supply is fixed while demand grows with every player. The idle share stays at zero and then climbs steeply once demand passes supply. A dynamic timer holds utilization flat until it hits its floor, and the only fix beyond the floor is more spawn points.

**Layout:** two linked views, stacked on narrow screens, side by side on wide ones.

- **Left, "Players waiting":** x-axis is players at the camp `P`, from 1 to 30. y-axis is idle share, 0% to 100%. Two lines: fixed timer and dynamic timer. A shaded band marks `ρ > 0.8` for the fixed timer. A vertical marker shows the current `P`.
- **Right, "Income per player":** same x-axis. y-axis is currency per player-hour. Two lines: fixed and dynamic. A dashed horizontal line marks the unconstrained income `k × 60 × drop`.

**Controls:**

| Control | Range | Default |
|---|---|---|
| Players at camp `P` | 1 to 30, step 1 | 10 |
| Spawn points `M` | 4 to 30, step 1 | 12 |
| Fixed respawn `T` (s) | 10 to 180, step 5 | 90 |
| Time to kill `TTK` (s) | 5 to 60, step 1 | 20 |
| Travel and loot `t` (s) | 0 to 30, step 1 | 10 |
| Drop value (copper) | 1 to 20, step 1 | 5 |
| Dynamic `T_min`, `T_max` (s) | 5 to 60; 30 to 180 | 20; 90 |
| Target utilization | 0.5 to 1.0, step 0.05 | 0.8 |

**Readout panel** beside the controls, for the current `P`, showing both timers: `k`, `λ`, `μ`, `T`, `ρ`, idle share, kills per player per minute and income per player-hour, to two decimals.

**Formulas:**

```
k        = 60 / (TTK + t)
λ        = P × k
T_fixed  = T
T_dyn    = clamp(M × 60 × target / λ, T_min, T_max)
μ        = M × 60 / T_used
ρ        = λ / μ
idle     = max(0, 1 − μ / λ)
kills/player/min = min(k, μ / P)
income/player/h  = kills/player/min × 60 × drop
```

**Test values** (defaults unless stated):

| Case | Expected |
|---|---|
| `P = 10`, fixed | `k = 2`, `λ = 20`, `μ = 8`, `ρ = 2.50`, idle 60%, income 240 |
| `P = 10`, dynamic | `T = 28.8`, `μ = 25`, `ρ = 0.80`, idle 0%, income 600 |
| `P = 20`, dynamic | `T = 20` (floor), `μ = 36`, `ρ = 1.11`, idle 10%, income 540 |
| `P = 20`, dynamic, `M = 18` | `T = 21.6`, `μ = 50`, `ρ = 0.80`, idle 0%, income 600 |
| `P = 3`, fixed | `μ = 8`, `ρ = 0.75`, idle 0%, income 600 |

**Accessibility and style:** keyboard-operable sliders with visible values; the fixed and dynamic lines differ by dash pattern as well as colour; the `ρ > 0.8` band carries a text label. Shared palette from `templates/interactive-tokens.css`. No game art; draw the camp as generic dots if a picture is used at all.
