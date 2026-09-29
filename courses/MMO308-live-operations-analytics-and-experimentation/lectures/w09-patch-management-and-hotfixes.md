# MMO308 · Week 09 — Patch Management and Hotfixes

**Why this matters:** Every patch is a bet that nothing you changed breaks for anyone. Most patches win the bet, and the ones that lose tend to lose for a small group of players with some unusual setup, which your test lab never had. This week you learn to size that bet: how many players a bad change reaches before you notice, how a staged rollout caps the damage, and when a bug is worth a hotfix instead of waiting for the next patch.

**You will be able to:**
- Compute the expected number of players hit by a bad change under a big-bang release and under a staged rollout, from the bug rate, the detection rate and the stage sizes.
- Choose stage sizes for a target bug rate using the complement rule, and explain why detection quality matters as much as staging.
- Decide between a hotfix and waiting for the scheduled patch by comparing expected harm with the hotfix's own cost and risk.
- Design a patch plan for a shared-world MMO that says which parts can be staged, which must ship at once, and how each part is turned off.

**Before class:** Beyer, Jones, Petoff & Murphy (eds.), *Site Reliability Engineering* (O'Reilly, 2016, free at sre.google), chapter 8 "Release Engineering" (about 25 minutes). CCP Games, "About the boot.ini issue" (EVE Online news, December 2007, 5 minutes). Reread your DB201 week 9 notes on expand, migrate and contract.

**Prerequisites from earlier courses:** [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one event in `n` tries). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (the rule of three). [DB201 week 9, schema migrations in a live game](../../DB201-data-persistence-and-telemetry/lectures/w09-schema-migrations-in-a-live-game.md) (expand, migrate, contract). [MMO302 week 13, cloud deployment](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md) (draining servers) and [week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (alerts). [MMO303 week 14, communicating balance changes](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w14-communicating-balance-changes.md) (patch notes). [MMO307 week 13, meta-game and patch cycles](../../MMO307-game-balance-ii-pvp-progression-and-endgame/lectures/w13-meta-game-and-patch-cycles.md) (how often to patch). From this course, [week 13, incident response](w13-incident-response.md), which picks up where this week stops: the bad change is already live and you must revert or fix forward.

**Interactive:** [Staged rollout harm](../examples/w09-staged-rollout.html). Keep it open during section 2.

---

## 1. What a live game ships, and how

A live MMO changes in several ways, and each has its own path to players.

- A **client patch** changes files on the player's machine. Players download it, usually at a maintenance window or at login.
- A **server patch** changes code on your servers. Players download nothing, but servers may restart.
- A **hotfix** is a change urgent enough that it cannot wait for the next regular patch. The Warcraft Wiki describes World of Warcraft's hotfixes as server-side changes that need no client download and go live with no downtime or a short realm restart, announced on the forums and in game rather than in downloadable patch notes.
- A **data or configuration change** edits a tuning table, a drop rate or a flag without new code.

Games also settle into a **cadence**, a regular rhythm for patches. Old School RuneScape releases game updates on Wednesdays at 11:30 UK time, with no downtime unless the team announces otherwise. MMO307 week 13 covers how often to patch for balance reasons. This week is about how each patch reaches players safely.

Five more terms:

- A **rollout** is the process of moving players from the old version to the new one.
- A **big-bang** release gives the new version to everyone at once.
- A **staged rollout** gives it to a growing share of players in steps, called **stages**, and checks for problems between steps. The first, smallest stage is the **canary**, named after the birds miners carried to detect gas.
- **Soak time** is how long each stage runs before you decide to continue.
- A **halt** stops a rollout from reaching more players. It does not undo the change for players who already have it. Undoing is a **revert**, and week 13 covers when to do that.

A **feature flag** (or kill switch) is a runtime setting that turns one feature on or off without a deploy. DB201 week 6 showed New World using switches to turn off trading paths during a duplication exploit, and MMO306 week 12 showed switches for single quests and bosses. Flags matter here for one reason: they let you **deploy** code (put it on servers, turned off) separately from **releasing** it (turning it on for players). A flag can release to 1% of players on a server that runs the same code for everyone.

## 2. Worked example: how big should the first stage be?

### The hook

On Wednesday, 5 December 2007, at 22:04 GMT, CCP released EVE Online's Trinity expansion, including a graphics upgrade from "Classic" to "Premium" content. Reports soon came in that the upgrade was deleting `C:\boot.ini`, a file Windows XP needs to start. CCP pulled the upgrade at about 03:40 GMT on 6 December and shipped a corrected installer at 06:08 GMT.

CCP's own account traced it to one line in the installer script. The line was meant to delete EVE's own file called `boot.ini` in the game folder. It was written without the folder path, so on some machines it deleted the Windows file of the same name at the root of the drive. Fewer than 215 players were affected: 170 contacted support by petition and 45 by phone. CCP said its test setups had lacked enough variety of hardware and operating systems.

Look at the shape of that failure. The bug hit only players who took one upgrade path on one version of Windows, which was a small share of the people patching. Every player got the patch at once. It took about five and a half hours to pull. If the upgrade had gone to 1% of players first, and CCP had waited for reports before sending it to everyone, how many of those players would have been spared?

### The model

A patch goes out in stages. Stage `i` brings the cumulative share of players who have the new version up to `f_i`, and the last stage reaches `f = 1`. Between stages you wait and watch. If anyone reports the bug during a stage, you halt before the next one.

```
q = p × d
P(reach stage i) = (1 − q) ^ (N × f_{i−1})
E[players hit] = Σ_i  P(reach stage i) × N × (f_i − f_{i−1}) × p
```

- `N` is the number of players who will take the patch.
- `p` is the **bug rate**, the chance that the bug hits a given player who takes the patch.
- `d` is the **detection rate**, the chance that a hit player's problem reaches you before the next stage. Automatic crash reports push `d` toward 1. Relying on forum posts and support tickets can put it well below that.
- `q` is the chance a given exposed player is both hit and detected.
- `f_0 = 0`, so you always reach the first stage.

The second line is MA102 week 3's complement rule. The rollout continues past a stage only if none of the players exposed so far has produced a detected hit. The third line adds up, stage by stage, the players each stage newly exposes, times the chance you got that far, times the chance each of them is hit.

The formula assumes players are hit independently, that everyone hit in a stage stays hit (halting does not help them), and that a single detection is enough to halt. Those are the right assumptions for a first estimate.

### Numbers you can check

Take `N = 200,000` players and a bug that hits one player in 2,000 (`p = 0.0005`). A big bang exposes everyone, so the expected number hit is `200,000 × 0.0005 = 100`.

Now stage it at 1%, then 10%, then everyone, with perfect detection (`d = 1`).

| Stage | Cumulative share | Newly exposed | P(reach stage) | Expected hit in stage |
|---|---|---|---|---|
| 1 (canary) | 1% | 2,000 | 1 | 1.00 |
| 2 | 10% | 18,000 | 0.368 | 3.31 |
| 3 | 100% | 180,000 | 0.00005 | 0.004 |
| **Total** | | | | **4.3** |

Check stage 2's row. The canary has 2,000 players, each hit and detected with chance 0.0005, so the chance the canary stays clean is `0.9995^2,000 ≈ e^−1 ≈ 0.368`. Stage 2 exposes 18,000 players, of whom `18,000 × 0.0005 = 9` would be hit, and you get there 36.8% of the time, so `9 × 0.368 = 3.31`. Stage 3 happens only if 20,000 players all came through clean, `0.9995^20,000 ≈ 0.00005`. The staged rollout cuts expected harm from 100 players to about 4.3.

Now make detection realistic. Suppose only one hit player in five reports the problem in time (`d = 0.2`), because nothing sends a crash report automatically.

| Plan | `d = 1` | `d = 0.2` |
|---|---|---|
| Big bang | 100 | 100 |
| 1% → 10% → 100% | 4.3 | 20.5 |
| 1% → 5% → 25% → 100% | 2.6 | 12.1 |

With poor detection, the same three-stage plan leaves nearly five times as many players hit, because the canary often passes without anyone noticing. A fourth stage wins some of that back. Better telemetry wins more.

The bug rate matters too. Hold the 1% → 10% → 100% plan with `d = 1` and vary `p`:

| Bug rate `p` | Big bang | Staged |
|---|---|---|
| 1 in 100,000 | 2 | 1.7 |
| 1 in 10,000 | 20 | 4.1 |
| 1 in 2,000 | 100 | 4.3 |
| 1 in 1,000 | 200 | 4.4 |
| 1 in 100 | 2,000 | 20 |

Two lessons are in that table. For a rare bug, staging barely helps, because the canary is too small to see it. For a common bug, the harm is roughly the canary's size times `p`, because it is caught in the canary every time. In between, staging holds the harm to a handful of players whatever the rate. **The first stage sets the price of a common bug. The gap between stages sets the price of a rare one.**

The model in code, which runs as shown:

```python
def expected_harm(N, p, d, stages):
    """Expected players hit by a bug of rate p under a staged rollout."""
    q = p * d                    # chance an exposed player is hit and detected
    total, prev, reach = 0.0, 0.0, 1.0
    for f in stages:             # cumulative fractions, last one is 1.0
        newly_exposed = N * (f - prev)
        total += reach * newly_exposed * p
        reach *= (1 - q) ** newly_exposed
        prev = f
    return total

N, p = 200_000, 1 / 2_000
for d in (1.0, 0.2):
    for plan in ([1.0], [0.01, 0.10, 1.0], [0.01, 0.05, 0.25, 1.0]):
        print(f"d={d}  stages={plan}  expected players hit {expected_harm(N, p, d, plan):6.1f}")
```

Output:

```
d=1.0  stages=[1.0]  expected players hit  100.0
d=1.0  stages=[0.01, 0.1, 1.0]  expected players hit    4.3
d=1.0  stages=[0.01, 0.05, 0.25, 1.0]  expected players hit    2.6
d=0.2  stages=[1.0]  expected players hit  100.0
d=0.2  stages=[0.01, 0.1, 1.0]  expected players hit   20.5
d=0.2  stages=[0.01, 0.05, 0.25, 1.0]  expected players hit   12.1
```

### Sizing the canary from the rule of three

Turn the question round. How large must the canary be to catch a bug of rate `p` with 95% probability? You need `1 − (1 − q)^n ≥ 0.95`, so:

```
n ≥ ln(0.05) / ln(1 − q)  ≈  3 / q
```

That is MA102 week 13's rule of three, read as a design rule. To catch a one-in-5,000 bug with perfect detection, the canary needs about 15,000 players. With `d = 0.2` it needs about 75,000, which on a 200,000-player game is not a canary anymore. Decide the smallest bug rate you want the canary to catch, and let that set its size and the telemetry you need.

### The visual

Open `examples/w09-staged-rollout.html`. The top view is a timeline of the rollout: a bar for each stage whose width is the share of players exposed, with the expected number of hit players drawn as dots inside it and the chance of reaching each stage printed above. The bottom view plots expected players hit against the bug rate on a log scale, one line for the big bang (a straight diagonal) and one for your staged plan (a curve that bends flat across the middle).

Move the detection slider from 1 down to 0.2 and watch the staged curve rise toward the big-bang line. Then drag the canary size up and watch the right end of the curve lift while the middle stays flat. There is no free canary size. Each choice moves the harm from one kind of bug to another.

### Cross-game recognition

**Google Play staged rollouts (current documentation).** Android developers choose the percentage of users who receive a new version and raise it by hand. If they find a problem, they can halt the rollout. Google's documentation says users who already received the version stay on it, and no new users get it. That is this model's assumption made official: halting protects the players not yet exposed, and does nothing for the ones already hit. The percentages are the developer's `f_i`, and whatever crash reporting the developer watches between steps sets `d`.

**CrowdStrike Falcon, 19 July 2024.** A faulty content update for CrowdStrike's security sensor went out at 04:09 UTC and was reverted at 05:27 UTC, 78 minutes later. Microsoft estimated that it affected 8.5 million Windows devices, less than 1% of all Windows machines, which then crashed on boot. In its preliminary post-incident review, CrowdStrike committed to deploying this kind of update gradually to larger portions of the sensor base, starting with a canary deployment. In this model's terms the bug had a very high `p` among the Windows machines that received it, so a canary would have set the harm by itself: a few thousand crashed machines in the first stage instead of millions.

**World of Warcraft's Public Test Realm (current).** Blizzard runs a PTR where anyone with a Battle.net account can test upcoming patches, copying characters from live realms, with wipes and downtime expected. A PTR is a stage 0 of volunteers before any live player is exposed. It has a known weakness in this model's terms. PTR players are not a random sample of the live population, so `p` on the PTR can differ from `p` on live. The volunteers are keen testers on well-kept machines, which is exactly the variety CCP said its own test setups lacked in 2007. A PTR is valuable for design feedback and for bugs everyone hits. It is weak against bugs that live only in unusual setups.

Three contexts, one model. Expected harm is exposure times rate, summed over the stages you reach, and the chance of reaching each stage is the complement rule applied to everyone exposed so far.

### Eyes-open design judgment

- **Invest in `d` before you add stages.** Going from `d = 0.2` to `d = 1` cut harm from 20.5 to 4.3 in the table. Automatic crash reports, login-failure counters and error-rate alerts per build (MMO302 week 14) are what make a canary mean something. A canary nobody watches is a delayed big bang.
- **Soak time must outlast the bug.** The model counts detection within a stage. A bug that shows only at the weekly reset, or after 20 hours of play, passes any canary that soaks for two hours. Name the slowest failure you care about and soak at least that long, or accept that the canary does not cover it.
- **Some changes cannot be staged in a shared world.** A client patch, a server binary on one realm, or a feature behind a flag can be staged. An economy change on a single-shard world, a cross-realm auction house or a change to how two versions talk to each other cannot be split by player, because every player shares it. Stage those by realm when you can (one realm as the canary), and ship them behind a kill switch when you cannot.
- **Staging costs time.** Three stages with four-hour soaks delay the full release by eight hours. For a fix that stops ongoing harm, that delay is itself harm. Stage new features generously and stage urgent fixes lightly.

## 3. Hotfix now, or wait for the patch?

Not every bug needs a hotfix. A hotfix is itself a change: it can break something, and if it needs a restart it costs play time. Compare the two options in the same unit, player-hours.

```
wait cost   = h × T
hotfix cost = D + r × H
```

- `h` is the harm the bug does per hour, in player-hours lost or an equivalent you agree on.
- `T` is the hours until the next scheduled patch.
- `D` is the disruption of applying the hotfix: restart minutes times concurrent players, in player-hours.
- `r` is the chance the hotfix itself causes a new problem, and `H` the harm if it does.

Hotfix when `h × T > D + r × H`.

Take a bug that locks players out of a dungeon, costing about 400 player-hours per hour. The next patch is Wednesday, 60 hours away. Waiting costs `400 × 60 = 24,000` player-hours. A hotfix needs a 10-minute restart with 30,000 players online, `D = 30,000 × 10/60 = 5,000`, and carries a 10% chance of a problem costing 20,000, so `r × H = 2,000`. The hotfix costs 7,000 against 24,000 for waiting. Hotfix.

Now a cosmetic bug costing 20 player-hours per hour. Waiting costs `20 × 60 = 1,200`, well under 7,000. Wait for Wednesday. The break-even harm rate is `7,000 / 60 ≈ 117` player-hours per hour.

Look at what moves the break-even. If your hotfixes need no restart, as WoW's server-side hotfixes often do, `D` drops to zero, the hotfix costs 2,000, and the break-even falls to about 33 player-hours per hour. Hotfix infrastructure is a design investment that makes many more bugs worth fixing today. When the bug is an active exploit, `h` includes damage to the economy that grows with time, and the answer is almost always to flip a kill switch now and fix later, which is week 13's revert-first logic.

## 4. Versions, compatibility and the way back

### Two versions at once

During any rollout, old and new versions run side by side. Some servers run build N while others run N − 1, and some clients have downloaded the patch while others have not. Every message between them must be understood by both. That has three consequences.

- **Version the protocol.** The client sends its version at login, and the server either supports it or refuses with a clear message. Never let a mismatch fail silently.
- **Change data in steps.** DB201 week 9's expand, migrate and contract sequence exists for exactly this. Add the new column first, write both forms during the rollout, and remove the old form only when no N − 1 code remains.
- **Draining decides when the old build is gone.** MMO302 week 13 showed that emptying a server of players takes hours. The old build lives until its last player leaves or the maintenance window forces a restart.

### Every change needs a way back

Before a patch ships, write down how each part of it is turned off.

| Part of the patch | Way back | Time to take effect |
|---|---|---|
| New feature behind a flag | turn the flag off | seconds |
| Server code change | redeploy previous build | minutes, plus draining |
| Client change | ship a new client patch | hours, and players must download |
| Data migration that rewrote values | restore from backup, or migrate forward | hours, and may erase player progress |

The bottom row is the dangerous one. Once a migration has rewritten player data, the old code cannot read it, and "undo" means a restore from backup that erases everything players did since. Week 13 treats that choice. The patch plan's job is to keep as much of the patch as possible in the top row: new behavior behind flags, migrations additive until the contract step, client changes small.

### Telling players

Patch notes are part of the patch. MMO303 week 14 covered writing balance changes so players understand them. For patch management, add two habits. Announce known issues and their workarounds the moment you confirm them, and say when a staged or hotfixed change will reach everyone. Players who can see a rollout's plan are more patient with its stages.

## In-class activity (25 minutes)

In groups of three. Your MMO has 150,000 active players on 10 realms of equal size. Next Wednesday's patch contains:

- a new crafting profession behind a feature flag;
- a client-side graphics option;
- a change to the shared cross-realm auction house's fee;
- a database migration that adds a column to the item table.

1. For each part, say whether it can be staged by player, by realm, or not at all, and write its way back.
2. For the parts you can stage, choose stage sizes so that a bug with `p = 1/2,000` hits fewer than 5 players in expectation with `d = 0.5`. Compute the expected harm of your plan.
3. Size a canary that catches a `p = 1/10,000` bug with 95% probability at `d = 0.5`. Is it realistic for this game?
4. A bug in the auction-house fee change is found on Thursday. It costs 150 player-hours per hour. The next patch is in 6 days. A hotfix needs a 15-minute restart with 25,000 players online, with a 5% risk of a 20,000 player-hour problem. Hotfix or wait?

Expected output: a one-page plan table, the harm calculation (for example, 1% → 4% → 15% → 50% → 100% gives about 4.2 players, while 1% → 10% → 100% gives about 7.0 and misses the target), the canary size (about 60,000 players, which is 40% of the game and not realistic, so improve `d` instead), and the hotfix decision (wait costs 21,600, hotfix costs about 7,250, so hotfix).

## Common misconceptions

- **"Halting a rollout fixes it for players who have it."** A halt stops new exposure. Players already on the bad version stay there until you revert or fix forward.
- **"A 1% canary protects against every bug."** It catches bugs common enough to show up in 1% of players within the soak time. Rare bugs and slow bugs pass straight through.
- **"The test server found nothing, so the patch is safe."** Test-server players are volunteers, not a sample of your population. EVE's 2007 bug lived in exactly the setups a test lab lacked.
- **"Hotfixes are always the responsible choice."** A hotfix is another change with its own risk and restart cost. Below the break-even harm rate, waiting for the scheduled patch is the safer choice.

## Check yourself

1. A game has `N = 100,000` players. A bug hits one player in 1,000 and detection is perfect. Compute the expected number of players hit under a big bang and under stages of 2%, 20% and 100%.
2. How large a canary do you need to catch a one-in-5,000 bug with 95% probability at `d = 1`? What if `d = 0.5`?
3. A bug costs 50 player-hours per hour, the next patch is 36 hours away, and a hotfix needs a 15-minute restart with 20,000 players online and carries a 5% risk of a 10,000 player-hour problem. Hotfix or wait? What changes if the hotfix needs no restart?
4. Your team proposes a 0.1% canary before every patch "for safety", with detection from forum reports only. Using the model, explain what this canary does and does not protect against.

<details>
<summary>Answers</summary>

1. Big bang `100,000 × 0.001 = 100`. Staged: canary `2,000 × 0.001 = 2`; reach stage 2 with `0.999^2,000 ≈ 0.135`, so `18,000 × 0.001 × 0.135 ≈ 2.43`; stage 3 is reached with probability about `2 × 10^−9`, so ≈ 0. Total about 4.4.
2. `n ≈ ln(0.05) / ln(1 − 0.0002) ≈ 14,977`, about `3 / p = 15,000`. At `d = 0.5`, `q = 0.0001`, so about 30,000.
3. Wait costs `50 × 36 = 1,800`. Hotfix costs `20,000 × 0.25 + 0.05 × 10,000 = 5,000 + 500 = 5,500`. Wait. With no restart the hotfix costs 500, less than 1,800, so hotfix.
4. With 0.1% of players and poor detection, `N × 0.001 × p × d` is tiny for any bug that is not very common, so the canary almost always passes. It protects against bugs that hit a large share of players, such as a crash on login. It gives almost no protection against the uncommon, setup-specific bugs that cause most rollout incidents. Improve detection first, then size the canary with the rule of three.

</details>

## Lab / assignment hook

[Lab 09, rollout planner](../labs/lab09.md). You implement the expected-harm model, confirm it with a Monte Carlo simulation of rollouts (MA102 week 11), search for the stage plan that minimizes harm under a time budget, and apply the hotfix rule to a queue of real-looking bug reports. Deliverable: passing tests and a one-page rollout policy for a small MMO team.

## Sources

- CCP Games, "About the boot.ini issue", EVE Online news (December 2007). Trinity released 22:04 GMT on Wednesday 5 December 2007; upgrade pulled at about 03:40 GMT on 6 December; fixed installer at 06:08 GMT; installer deleted `boot.ini` without the install-folder path; fewer than 215 users affected (170 by petition, 45 by phone); CCP cited too little variety of hardware and operating systems in testing. https://www.eveonline.com/news/view/about-the-boot.ini-issue
- Warcraft Wiki, "Hotfix" (accessed September 2026). Server-side changes that need no client download, applied with no downtime or a short realm restart, announced on forums and in game.
- Warcraft Wiki, "Public Test Realm" (accessed September 2026). Open to Battle.net accounts; character copy from live realms; wipes and downtime expected.
- Old School RuneScape Wiki, "Game updates" (accessed September 2026). Updates on Wednesdays at 11:30 UK time with no downtime unless noted beforehand.
- Google, Play Console Help, "Release app updates with staged rollouts" (accessed September 2026). Developer-chosen percentages; halting stops new users receiving the version; users who already have it stay on it.
- CrowdStrike, "Falcon Content Update Remediation and Guidance Hub: Preliminary Post Incident Review" (July 2024). Channel File 291 deployed 04:09 UTC and reverted 05:27 UTC on 19 July 2024; commitment to staggered deployment starting with a canary.
- Weston, D. (Microsoft), "Helping our customers through the CrowdStrike outage", Official Microsoft Blog (20 July 2024). 8.5 million Windows devices affected, less than 1% of all Windows machines.
- Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (eds.) (2016). *Site Reliability Engineering*. O'Reilly. Chapter 8, "Release Engineering".

## Interactive spec: examples/w09-staged-rollout.html

**The one insight.** A staged rollout holds the expected number of players hit to a small number across a wide range of bug rates, while a big bang grows in a straight line. The canary size sets the harm for common bugs, the gaps between stages set it for rare ones, and poor detection pushes the staged curve back toward the big bang.

**Layout.** Two linked views stacked on all widths. Top: "This bug, this plan", a horizontal bar per stage whose length is its newly exposed share, labelled with the cumulative share, `P(reach)` above it, and the expected players hit in that stage as a number plus up to 50 dots (one dot per expected player, rounded; show "+n" beyond 50). Bottom: "Every bug rate", expected players hit (log y from 0.1 to 100,000) against bug rate `p` (log x from 1e−6 to 1e−1), with a straight big-bang line `N × p` and the staged curve. A vertical marker shows the current `p` and links the two views. Controls sit between the views.

**Controls.**
- Players `N`: 10,000 to 1,000,000 (log slider), default 200,000.
- Bug rate `p`: log slider from 1e−6 to 1e−1, default 5e−4, with the value shown as "1 in X".
- Detection `d`: 0.05 to 1.0 in steps of 0.05, default 1.0.
- Stages: an editable list of cumulative shares (up to 6), each a number input in percent, kept strictly increasing, last fixed at 100%. Presets: "Big bang" [100], "1-10-100" (default) [1, 10, 100], "1-5-25-100", "0.1-1-10-100".
- A "rule of three" readout: the canary size needed to catch the current `p` with 95% probability at the current `d`, `ceil(ln 0.05 / ln(1 − p·d))`, and whether the current first stage meets it.

**Formulas.**
- `q = p × d`; `f_0 = 0`; for each stage i: `new_i = N (f_i − f_{i−1})`; `reach_1 = 1`; `reach_{i+1} = reach_i × (1 − q)^{new_i}`; `harm_i = reach_i × new_i × p`; total = Σ harm_i. Compute `(1 − q)^n` as `exp(n × log1p(−q))` for accuracy.
- Big bang: `N × p`.

**Readouts.** Total expected players hit, big-bang value, the ratio between them, and the per-stage table (stage, cumulative share, newly exposed, P(reach), expected hit) with values students can copy into the lecture's table.

**Test values** (N = 200,000 unless stated).
- `p = 1/2,000`, `d = 1`, 1-10-100: per-stage 1.00, 3.31, 0.004; total 4.3; P(reach) 1, 0.368, 0.0000453.
- Same with `d = 0.2`: total 20.5 (per-stage 1.00, 7.37, 12.18).
- 1-5-25-100: 2.6 at `d = 1`, 12.1 at `d = 0.2`.
- 1-10-100, `d = 1`: `p = 1e−5` → 1.67; `p = 1e−4` → 4.11; `p = 1e−3` → 4.43; `p = 1e−2` → 20.0 (big bang 2, 20, 200, 2,000).
- `N = 100,000`, `p = 1/1,000`, `d = 1`, stages [2, 20, 100]: total 4.43.
- Rule of three at `p = 1/5,000`, `d = 1`: 14,978 players (ceil of 14,977.2).

**Accessibility and style.** Native inputs with labels; the per-stage table is a real table; the log-scale chart has tick labels in "1 in X" form and a text summary. Respect `prefers-reduced-motion` (no dot animation). Palette from `templates/interactive-tokens.css`. No game art or logos.
