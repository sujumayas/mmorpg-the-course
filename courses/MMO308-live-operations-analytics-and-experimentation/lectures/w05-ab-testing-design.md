# MMO308 · Week 05 — A/B testing: design

**Why this matters:** Most failed experiments were lost before the first player saw them. The team randomized the wrong unit, measured the wrong players, or picked a metric that could not move in the time they had. In a shared world these mistakes are easier to make, because players trade, group and talk to each other. This week you learn to design a test that can answer its question before you spend a month of traffic on it.

**You will be able to:**
- Write a complete experiment plan: hypothesis, unit, trigger, primary and guardrail metrics, minimum detectable effect and duration.
- Compute the design effect and effective sample size of a test randomized by guild or server, and decide which unit a given change needs.
- Implement deterministic, per-experiment hash assignment and explain why it beats a coin flip at login.
- Compute how triggering, or failing to trigger, changes the sample size a test needs.

**Before class:** Kohavi, R., Tang, D. & Xu, Y. (2020), *Trustworthy Online Controlled Experiments*, chapter 7 (metrics for experimentation and the overall evaluation criterion), chapter 14 (choosing a randomization unit) and chapter 15 (ramping experiment exposure), plus the later chapters on triggering and on leakage and interference between variants. Andersen, E. et al. (2012), "The Impact of Tutorials on Games of Varying Complexity", CHI 2012, sections on the experiment design (free PDF from the authors' lab).

**Prerequisites from earlier courses:** [MA102 week 14, hypothesis testing and A/B](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (the two-proportion z-test, power, the sample-size formula and Lehr's rule, and the list of MMO problems in its section 5; this week turns that list into numbers). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (standard error of a rate). [DB201 week 10, telemetry design](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md) (events, properties and the tracking plan). [MMO304 week 6, auction houses](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w06-supply-demand-and-equilibrium-in-auction-houses.md) (one shared market sets one price). [MMO308 week 4, funnels and churn](w04-funnels-and-churn.md).

**Interactive:** [w05-cluster-design-effect.html](../examples/w05-cluster-design-effect.html). Keep it open during section 2.

---

## 1. The plan comes first

In MA102 week 14 you analysed a test someone else had designed. On a live team you are the someone. Before a single player is assigned, write down these eight things in a one-page **experiment plan**, and get it reviewed.

1. **Hypothesis.** One sentence naming the change, the metric and the direction. "Halving the gold cost of the first crafting recipe raises the share of new players who craft an item in their first 3 days."
2. **Variants.** Exactly what A and B are. If there are three variants, say so now, because each extra variant is another comparison (MA102 week 14, multiple comparisons).
3. **Unit of randomization.** Player, account, device, party, guild, server or region. Section 2 is about this choice.
4. **Population and trigger.** Which players are eligible, and at what moment a player counts as having entered the test. Section 4.
5. **Primary metric.** One metric that decides the result. Name its exact definition, the way DB201 week 12 taught you to define DAU.
6. **Guardrail metrics.** Numbers that must not get worse even if the primary wins, such as crash rate, day-7 retention or revenue per player.
7. **Minimum detectable effect and duration.** The smallest effect worth shipping, and the sample size and number of days needed to detect it at 80% power, from MA102's formula corrected for your unit.
8. **Decision rule.** What you will do for each outcome, including "not significant". Week 6 adds when you are allowed to look.

The plan protects you from yourself. A team that writes the primary metric after the data arrives will find one that won.

## 2. Worked example: player, guild or server?

### The hook

MA102 week 14 ended with a question about testing 20% cheaper potions on half the players of each server. Its answer was to randomize whole servers instead, and to "accept a smaller effective `n`". That phrase hides a number, and in an MMO the number can be startling.

Take a real shared market. In Guild Wars 2, the Trading Post lets players on every world, in both the North American and European regions, trade with each other. It is one market. Randomizing by world does not separate the groups at all, because a cheap item listed by a B player on one world is bought by an A player on another. And EVE Online runs its whole universe outside China as one server cluster, Tranquility. There is no second copy of its economy to use as a control.

So how much does randomizing by a bigger unit cost?

### The model

When players in the same cluster (a server, a guild) behave alike, each extra player in a cluster adds less new information than an independent player would. Survey statisticians measure this with the **design effect**, due to Leslie Kish:

```
deff  = 1 + (m − 1) × ρ
n_eff = n / deff
```

- `m` is the number of players per cluster (average cluster size).
- `ρ` (rho) is the **intraclass correlation** (ICC), the share of the metric's variance that comes from differences between clusters rather than between players in the same cluster. `ρ = 0` means clusters are no more alike inside than a random group. `ρ = 1` means everyone in a cluster has the same outcome.
- `n` is the number of players in one arm. `n_eff` is the number of independent players that would give the same precision.

The effective size then goes into the MA102 formulas in place of `n`. For a rate with baseline `p`, the minimum detectable effect at 80% power and `α = 0.05` is about:

```
MDE ≈ 2.80 × sqrt( 2 p (1 − p) / n_eff )
```

(2.80 is `1.96 + 0.8416` rounded, from MA102's power section. The tables below use the unrounded 2.8016.)

One more line shows the trap. With `k` clusters of size `m` in an arm, `n = k m`, and:

```
n_eff = k m / (1 + (m − 1) ρ)  →  k / ρ   as m grows
```

Once clusters are large, **the number of clusters sets the precision, not the number of players**. Twenty servers with `ρ = 0.01` can never be worth more than 2,000 independent players, whether each server holds 5,000 players or 50,000.

### Numbers you can check

Your MMO has 40 servers of 5,000 players, 200,000 in all. The primary metric is day-7 retention with a baseline of 30%. You give 20 servers to A and 20 to B, so `n = 100,000` per arm. Alternatively you randomize 5,000 guilds of 20 members, or single players.

| Unit | `m` | `ρ` (assumed) | deff | `n_eff` per arm | MDE on 30% D7 |
|---|---|---|---|---|---|
| Player | 1 | — | 1.00 | 100,000 | 0.57 points |
| Guild | 20 | 0.05 | 1.95 | 51,282 | 0.80 points |
| Server | 5,000 | 0.001 | 6.00 | 16,669 | 1.41 points |
| Server | 5,000 | 0.01 | 50.99 | 1,961 | 4.10 points |
| Server | 5,000 | 0.05 | 250.95 | 398 | 9.10 points |

Check the fourth row. `deff = 1 + 4,999 × 0.01 = 50.99`. `n_eff = 100,000 / 50.99 = 1,961`. `2 × 0.3 × 0.7 / 1,961 = 0.000214`, whose square root is 0.01464, and `2.80 × 0.01464 = 0.041`, or 4.1 points.

The same 200,000 players can detect a 0.57-point change or only a 4.1-point change, depending on the unit. Guilds cost you less than half your sample. Servers can cost you 98% of it.

The `ρ` values in the table are assumptions, chosen to span a plausible range. You must measure your own game's `ρ` for each metric, and you can, from data you already have. Take last month's per-server D7 retention. The spread of server means beyond what binomial noise alone would produce is the between-server variance `σ_b²`. Then `ρ = σ_b² / (σ_b² + p(1 − p))`. Lab 05 has you do it. Servers differ in age, language, time zone and the guilds that dominate them, so `ρ` is rarely zero.

### A visual you can move

Open `examples/w05-cluster-design-effect.html`. The left view draws the 40 servers as blocks, each filled with dots for players. Beside them are two bars: "players in the test" and "effective players". The right view plots the MDE against the number of servers per arm, one curve for each `ρ` in {0.001, 0.01, 0.05}, with a marker at your settings.

Drag the "players per server" slider from 1,000 to 20,000. The first bar grows twenty-fold. The effective bar barely moves once `m` passes a few hundred, and the MDE marker slides sideways without dropping. Now drag "servers per arm" from 5 to 40. The MDE falls fast. The picture makes the rule plain: to buy precision in a clustered test, buy clusters.

### Cross-game recognition

Each case is the same trade: the unit you must randomize to keep A and B apart, against the effective sample that unit leaves you.

**Refraction, Hello Worlds and Foldit (Andersen et al., CHI 2012).** The University of Washington's Center for Game Science tested eight tutorial designs across three games with over 45,000 players. Each new player was assigned at random to one condition, so `m = 1` and `deff = 1`. These are games where one player's tutorial does not change another's game, which is exactly when player-level randomization is safe. Even so, the unit caused trouble. In the two Flash games, players were tracked through local storage, so a player who cleared their Flash cache or switched computers came back as a "new" player in a possibly different condition. In Foldit, players who logged in from several machines were dropped to avoid counting anyone in two versions. The unit you randomize must be the unit you can recognize every time it returns.

**Guild Wars 2 (Trading Post, current).** One market spans every world in both regions. For a change to prices or to an item's supply, the only unit that keeps groups apart is the whole game, so `k = 1` per arm and no randomized comparison is possible. The options are a before-and-after study with its known weakness (MA102 week 14's League chat example), or a design that alternates the whole game between A and B in blocks of time, called a **switchback**, which works only when the effect stops quickly after you switch back.

**EVE Online (Tranquility).** The same, for the whole universe. CCP's other copies of the world are a test server and a separately run Chinese server, which differ in population and history. Using the Chinese world as a control group would be a comparison of two clusters, `k = 1` per arm, with every difference between them confounded with the change.

**Schools and clinics.** Education and public-health researchers randomize whole classrooms or clinics when students or patients influence one another, and they plan with this same design effect. Game analytics borrowed the tool from them. A guild is a classroom.

### Eyes-open design judgment

- **Randomize at the smallest unit that contains the interference.** Crafting UI: player. Group-finder rules: party or guild, because the change reaches everyone in the group. Auction-house fees: the market, which might be the whole game.
- **Guilds are often the sweet spot.** They contain most social spillover and are small enough that `deff` stays near 2. But guild membership changes. Fix each player's arm at the moment of assignment, and decide in the plan what happens when a player changes guild.
- **With few clusters, analyse clusters.** With 20 servers per arm you have 40 data points, not 200,000. Compare server-level means with a t-test on 40 values, or use methods built for clustered data. A player-level z-test on server-randomized data will report `p = 0.001` for noise.
- **Some questions have no randomized answer.** A global market change in Guild Wars 2 or EVE cannot be A/B tested. Say so in the plan, use a before-and-after design with a written list of other things that changed, and lower your confidence accordingly.

## 3. Assigning players: hash, don't flip

The obvious way to assign a player is to flip a coin when they log in. It fails in three ways. The player may get a different result next login, so they see both versions. You have to store every assignment and look it up on every server that needs it. And two experiments that flip independent coins are independent, but you cannot reproduce who was where if the store is lost.

The standard alternative is **deterministic hashing**. Feed the experiment's name and the unit's id to a hash function, turn the output into a number between 0 and 1, and compare it with the share you want in B.

```python
import hashlib
from collections import Counter

def bucket(unit_id, experiment):
    """A number in [0, 1) fixed by the unit and the experiment name."""
    digest = hashlib.sha256(f"{experiment}:{unit_id}".encode()).digest()
    return int.from_bytes(digest[:8], "big") / 2**64

def variant(unit_id, experiment, share_b=0.5):
    return "B" if bucket(unit_id, experiment) < share_b else "A"

print([variant(pid, "craft-cost-2026-10") for pid in (101, 102, 103, 104, 105)])
print([variant(pid, "craft-cost-2026-10") for pid in (101, 102, 103, 104, 105)])

split = Counter(variant(pid, "craft-cost-2026-10") for pid in range(100_000))
print(split["A"], split["B"])

both = Counter((variant(pid, "craft-cost-2026-10"), variant(pid, "new-tutorial-v3"))
               for pid in range(100_000))
print(sorted(both.items()))
```

Output:

```
['A', 'B', 'B', 'A', 'B']
['A', 'B', 'B', 'A', 'B']
49995 50005
[(('A', 'A'), 24789), (('A', 'B'), 25206), (('B', 'A'), 25064), (('B', 'B'), 24941)]
```

Read the four lines.

- The same player gets the same arm every time, on any server, with nothing stored. The game server, the web shop and the analytics job can each compute it.
- 100,000 players split 49,995 to 50,005. A fair coin would typically miss 50,000 by about 158 (the standard deviation `sqrt(100,000 × 0.25)`), so this is well within chance.
- The experiment name is the **salt**. Because the two experiments use different names, being in B of one says nothing about the other. All four combinations hold about a quarter of players. Leave the salt out, and every player in B of the crafting test would also be in B of the tutorial test. Their results would be tangled forever.

Three habits make hashing safe in practice.

- **Hash the unit you chose.** For a guild-level test, hash the guild id, not the player id.
- **Ramp by changing the share, not the salt.** Start at `share_b = 0.01` to catch crashes, then raise it to 0.5. Players already in B stay in B, because their bucket did not change. Changing the salt reshuffles everyone.
- **Log exposure as an event.** When a player first meets the change, send an `experiment_exposure` event carrying the experiment name, the arm and the time, following the tracking-plan rules of DB201 week 10. The analysis joins on this event. Without it you are guessing who saw what.

## 4. Triggering: count the players who could be affected

Suppose your change is to the crafting station's interface, and only 20% of new players open the crafting station in their first three days. The other 80% are assigned to A or B, but for them A and B are the same game. Including them adds noise and no signal.

**Triggering** means analysing only the players who reached the point where A and B differ, counted in both arms by the same rule. A player triggers when they open the crafting station, whether they see the old or the new interface.

The numbers show why it matters. Say that among players who open the station, the new interface raises the share who craft something from 30% to 35%, a 5-point effect. Among all assigned players, 80% cannot be affected, so the effect is diluted to 1 point on the same 30% base. Using MA102's sample-size formula:

| Analysis | Effect | `n` per arm needed | Assigned players per arm needed |
|---|---|---|---|
| Triggered players only | 5 points | 1,374 triggered | 6,870 (at 20% trigger rate) |
| All assigned players | 1 point | 33,272 | 33,272 |

Analysing everyone needs almost five times as many assigned players, so the test runs almost five times longer. The rule of thumb: diluting the effect by a factor `f` multiplies the required sample by about `1/f²`, and you save a factor of `1/f` back because more players are available. Net cost about `1/f`.

Two warnings. The trigger must be something that happens the same way in both arms, before the change can have acted. "Opened the crafting station" is fine. "Crafted an item" is not, since that is the outcome. And triggering changes the question. The result applies to players who open the station. If you need the effect on the whole game, multiply by the trigger rate.

## 5. Choosing the metric and the length

### Sensitive or meaningful

The metric you care about most is often the hardest to move. Day-30 retention or lifetime spend are what the studio lives on, but they take 30 days or more to observe, and a crafting UI changes them by a sliver. A metric close to the change, "share of triggered players who craft within 3 days", moves more and is visible sooner. The price is that it might not matter.

The usual answer is a pair. Pick the close metric as the primary, because it can reach significance. Watch the meaningful ones as guardrails, and require that they do not fall. For large changes, keep a small **long-term holdout**, say 5% of players who stay on A for months, so you can check later that the close metric's win showed up in retention.

### Whole weeks, and a trip through the funnel

Players on Saturday are not players on Tuesday. Weekend players are more casual, more social, and more often new. A test that runs Monday to Friday measures a weekday game. Run in whole weeks, and at least one full week, even when the sample size is reached sooner.

And give players time to reach the metric. Week 4's funnel lesson applies. If the primary metric is "reached level 20 within 14 days", nobody assigned in the last 14 days of the test has a complete result. Either stop assigning 14 days before the end, or analyse only complete cohorts, as DB201 week 12 did for retention.

### Duration, all together

Put the pieces into the plan. The crafting test needs 1,374 triggered players per arm. You get 3,000 new players a day, 20% trigger in their first three days, so about 600 triggered players a day, 300 per arm. That is 4.6 days of assignment. Round up to 7, a whole week, then add 3 days so the last cohort's three-day window completes. Ten days from launch to readout.

## 6. Players are people

A game test is run on people who talk to each other, and some of them pay you.

- **Visible differences get noticed.** If B's crafting recipe is cheaper, players will compare notes, and a forum thread will say the game charges some players more. Test changes players cannot directly compare (interfaces, pacing, onboarding order) at the player level. For prices and power, prefer a test server or a whole-game switchback.
- **Do not test harm.** A variant you believe makes the game worse for some players, or pushes vulnerable players to spend, should not run just to measure how much worse. [MMO402 week 12](../../MMO402-emergent-society-governance-and-ethics/lectures/w12-research-ethics-in-online-worlds.md) covers the ethics of research in online worlds, including consent, and [MMO403](../../MMO403-business-monetization-and-ethics-of-live-games/syllabus.md) covers monetization tests in detail.
- **Guardrails are promises.** If a guardrail breaks mid-test, such as a crash rate rising in B, stop B. That is a decision you make before launch and write in the plan.

## In-class activity (25 minutes)

In pairs. Each pair gets one proposed change from this list: (a) a new tutorial for the first 20 minutes, (b) a 10% lower auction-house listing fee, (c) a larger reward for completing a group dungeon with strangers, (d) a new shop layout.

1. **Choose the unit (7 min).** Name the smallest unit that contains the interference, and why. If the answer is "the whole game", say what design you would use instead.
2. **Size it (10 min).** Your game has 60,000 players on 30 servers and 3,000 guilds of about 15 active members. Baseline for your primary metric is 25%. Using `ρ = 0.02` for servers and `ρ = 0.05` for guilds, compute `n_eff` per arm and the MDE for your chosen unit, with the whole population split 50/50.
3. **Write the trigger (8 min).** State the exact event that makes a player count, and check that it can happen the same way in both arms.

Expected output: one filled experiment plan per pair. For step 2, a player-level test has `n_eff = 30,000` and an MDE of about 1.0 point. Guild-level: `deff = 1 + 14 × 0.05 = 1.70`, `n_eff ≈ 17,647`, MDE ≈ 1.3 points. Server-level: `deff = 1 + 1,999 × 0.02 = 40.98`, `n_eff ≈ 732`, MDE ≈ 6.3 points.

## Common misconceptions

- **"More players per server means a more precise test."** Once servers are large, precision is set by the number of servers, about `k / ρ`. Add servers, not players.
- **"Random assignment at login is random enough."** It lets the same player see both versions across logins. Hash a stable id with a per-experiment salt.
- **"Analysing everyone assigned is more honest than triggering."** It answers the same question with a diluted effect, and so needs far more players. Trigger on an event that happens equally in both arms.
- **"If it's significant on D1, it will show up on D30."** Close metrics can win while long-term ones stay flat. Keep guardrails and, for big changes, a holdout.

## Check yourself

1. A test randomizes 10 servers per arm of 8,000 players each. The metric's `ρ` is 0.005. Compute `deff` and `n_eff` per arm. What is the most `n_eff` could ever reach with 10 servers per arm?
2. Your team hashes players with `sha256(str(player_id))` for every experiment. Two tests run at once, each 50/50. What goes wrong?
3. A shop redesign affects only players who open the shop, 10% of daily players. The effect among them is +2 points on a 5% conversion rate. By roughly what factor does analysing all players instead of triggered players lengthen the test?
4. A guild-level test assigns guilds on 1 October. On 10 October a B-guild player leaves and joins an A guild. Which arm should the analysis put them in, and why?

<details>
<summary>Answers</summary>

1. `deff = 1 + 7,999 × 0.005 = 40.995`. `n_eff = 80,000 / 40.995 ≈ 1,951`. The ceiling is `k / ρ = 10 / 0.005 = 2,000`. The servers are already so large that adding players adds almost nothing.
2. Without a per-experiment salt, each player lands in the same bucket in both tests. Everyone in B of one is in B of the other, so the two effects cannot be separated.
3. The effect across all players is diluted by `f = 0.1`. Required sample rises by about `1/f² = 100`, and 10 times more players are available, so the test takes about 10 times longer.
4. B, the arm assigned at the start. Analysing by assigned arm (intention to treat) keeps the randomization intact. Moving players by later behavior lets the change itself decide who is in which group.

</details>

## Lab / assignment hook

[Lab 05, design an experiment for a shared world](../labs/lab05.md). You implement salted hash assignment and verify its split, estimate the intraclass correlation of day-7 retention from 40 servers of history, compute effective sample sizes and durations for player, guild and server designs, and write a full experiment plan for a change you choose. The plan is the design half of the A/B report assessment.

## Sources

- Andersen, E., O'Rourke, E., Liu, Y.-E., Snider, R., Lowdermilk, J., Truong, D., Cooper, S. & Popović, Z. (2012). "The Impact of Tutorials on Games of Varying Complexity." *Proceedings of CHI 2012*, doi:10.1145/2207676.2207687. Eight tutorial designs in Refraction, Hello Worlds and Foldit; over 45,000 players; random assignment of new players; Flash-cache tracking treating returning players as new if they cleared the cache or changed computers; Foldit players on several machines discarded. Read from the authors' PDF, September 2026.
- Guild Wars 2 Wiki, "Trading Post" (accessed 28 September 2026). The Trading Post lets players from all worlds, NA and EU, trade with each other.
- Wikipedia, "Eve Online" (accessed 28 September 2026). One universe on the Tranquility cluster for players outside China; Serenity serves China separately; Singularity is a public test server.
- Kish, L. (1965). *Survey Sampling*. Wiley. The design effect `1 + (m − 1)ρ`.
- Kohavi, R., Tang, D. & Xu, Y. (2020). *Trustworthy Online Controlled Experiments*. Cambridge University Press. Hash-based assignment, triggering, guardrail metrics, interference and cluster randomization.
- The design-effect table, triggered sample sizes, activity answers and hash outputs were computed by the author with the formulas and code shown; `ρ` values are illustrative assumptions.

## Interactive spec: examples/w05-cluster-design-effect.html

**The one insight.** In a test randomized by server, precision is bought with servers, not with players. Growing each server from 1,000 to 20,000 players barely moves the minimum detectable effect; adding servers moves it a lot.

**Layout.** Two linked views side by side on desktop, stacked on mobile.

- **Left view, "Who is in the test".** A grid of `2k` server blocks (A blocks in one color, B in another, labelled), each drawn as a small square whose area is proportional to `m` on a capped scale. Beside the grid, two horizontal bars on a shared log axis from 100 to 1,000,000: "players per arm" `n = k·m` and "effective players per arm" `n_eff`. Print both numbers and `deff`.
- **Right view, "Smallest effect you can detect".** x axis: clusters per arm `k`, 2 to 100 (log). y axis: MDE in percentage points, 0 to 15. Three curves for `ρ` = 0.001, 0.01, 0.05 at the current `m` and `p`, plus the player-level reference line (`ρ = 0`, same `n`). A marker at the current `k` on the current-`ρ` curve, labelled with its MDE. A dashed horizontal line for the MDE the student says they need (control below).
- **Readout row.** `p`, `m`, `k`, `ρ`, `n`, `deff`, `n_eff`, ceiling `k/ρ` (or "none" when `ρ = 0`), MDE, and "servers per arm needed for the target MDE".

**Controls (keyboard accessible, update immediately).**
- Unit preset buttons: Player (`m = 1`), Guild (`m = 20`, `ρ = 0.05`), Server (`m = 5,000`, `ρ = 0.01`).
- Players per cluster `m`: stepped slider [1, 5, 20, 100, 500, 1,000, 2,000, 5,000, 10,000, 20,000], default 5,000.
- Clusters per arm `k`: slider 2 to 100, default 20.
- ICC `ρ`: stepped slider [0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1], default 0.01.
- Baseline rate `p`: slider 5% to 90%, default 30%.
- Target MDE: slider 0.5 to 10 points, step 0.5, default 2.

**Formulas.**
- `n = k·m`; `deff = 1 + (m − 1)·ρ`; `n_eff = n / deff`; ceiling `k/ρ`.
- `MDE = (1.96 + 0.8416)·sqrt(2·p·(1 − p) / n_eff)`, shown in points (×100).
- Clusters needed for target `T` (as a proportion): `n_eff_needed = 2·p(1 − p)·(2.8016/T)²`; `k_needed = ceil(n_eff_needed · deff / m)`; if `n_eff_needed ≥ k/ρ` for every `k` up to 100, show "more than 100".

**Test values (p = 0.30).**
- Player, `n = 100,000`: `n_eff = 100,000`, MDE 0.57.
- `m = 20, ρ = 0.05, k = 5,000`: deff 1.95, `n_eff = 51,282`, MDE 0.80.
- `m = 5,000, k = 20`: `ρ = 0.001` → deff 6.00, `n_eff = 16,669`, MDE 1.41; `ρ = 0.01` → deff 50.99, `n_eff = 1,961`, MDE 4.10; `ρ = 0.05` → deff 250.95, `n_eff = 398`, MDE 9.10.
- `m = 20,000, k = 20, ρ = 0.01`: deff 200.99, `n_eff = 1,990`, MDE 4.07 (ceiling 2,000).
- `k` slider for the guild preset: allow up to 5,000 when `m ≤ 20` (switch the axis range to 2 to 10,000).

**First screen.** Server preset (`m = 5,000`, `k = 20`, `ρ = 0.01`, `p = 30%`). The "players per arm" bar reads 100,000 and the "effective" bar reads 1,961, side by side, with the MDE marker at 4.10 points above the dashed 2-point target.
