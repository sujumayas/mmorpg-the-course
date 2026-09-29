# MMO306 · Week 05 — Telegraphing and Readability

**Why this matters:** A warning that 98% of players react to in time looks generous in a playtest with one tester. Put it in a 20-player raid and repeat it five times a pull, and most pulls end in a wipe. Group content multiplies every telegraph by the number of players and the number of repetitions, so the slowest few players, not the average one, decide whether your boss is fair.

**You will be able to:**
- Compute the chance that a whole raid resolves a telegraphed mechanic cleanly, from the telegraph length, the spread of player response times, the number of players targeted and the repetitions per pull.
- Derive the telegraph length a mechanic needs for a target clean-pull rate, and explain why it depends on the tail of the response-time distribution.
- Account for network latency and server snapshots in a telegraph budget.
- Critique an encounter's visual language for consistency, redundancy and clutter, and choose between wipe, death and damage as the failure outcome.

**Before class:** Sarah Carmody, "'World of Warcraft' VFX Pillars" (GDC 2023 Visual Effects Summit, GDC Vault). Read the Final Fantasy XIV Online Wiki pages "Common mechanics and markers", "Area of Effect" and "Snapshot" listed in Sources, and play or watch one boss fight in any MMO with the sound off, noting every warning you see.

**Prerequisites from earlier courses:** [GD101 week 12, the telegraph budget](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) (the time one player needs to react to one warning). [UX201 week 1, perception, attention and memory](../../UX201-game-ux-and-player-psychology/lectures/w01-perception-attention-memory.md). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) and [MA102 week 8, the normal curve](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md). [CS202 week 11, lag compensation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w11-lag-compensation-rewind-hit-detection.md) (for section 4). From this course, [week 4, encounter mechanics](w04-encounter-mechanics-tank-and-spank-to-dance-fights.md) (the cost of a death).

**Interactive:** [`examples/w05-raid-telegraph.html`](../examples/w05-raid-telegraph.html). Keep it open during section 2.

---

## 1. From one player to a raid

A **telegraph** is a warning that an attack is coming, shown early enough for the player to respond. In GD101 week 12 you built a budget for it: the warning time must cover simple reaction, the choice between possible responses, action start-up, display lag and any time the warning is hidden by other effects. With that course's assumptions, a player telling apart four warnings needs about 617 milliseconds.

**Readability** is how quickly and reliably a player can extract the right information from what the screen and speakers show. A readable telegraph is one that most players decode fast and few decode wrongly.

The GD101 budget answers a question about one average player facing one warning. Group content changes the question in three ways.

1. **Players differ.** The budget is a mean. Real players spread around it: some are faster, some slower, and the same player is slower when tired or when the screen is busy.
2. **Many players must all succeed.** In a 20-player raid, a mechanic that targets everyone is 20 separate trials. If one failure wipes the raid, all 20 must succeed.
3. **Mechanics repeat.** A boss that casts the same mechanic five times per pull runs the trial five times per player.

Each of these multiplies. That is the whole of this week's worked example.

## 2. Worked example: the raid multiplier

### The hook

World of Warcraft players have long used addons to warn them about boss abilities. Deadly Boss Mods is one of the best known. It is built from "boss modules", one per boss, that show alert messages and timer bars before each ability. By 2008 raid guides were already advising players to install it or BigWigs. When the Tempest Keep boss Void Reaver stopped targeting a player before casting Arcane Orb in patch 2.4.0, the addons could no longer see the orb coming and stopped warning about it. Players had to watch the sky, and a wiki note from January 2008 had already warned that the orb's explosion went off before its graphic appeared to land. A later patch, 2.4.3, added a combat log entry and the addon warnings came back.

On 20 January 2026, patch 12.0.0 (the systems patch for the Midnight expansion) did two things together. It added a built-in feature set called Boss Warnings: a Boss Timeline that shows upcoming boss casts in order, and text alerts in the centre of the screen at three levels, Minor, Medium and Critical. And it made wide-ranging changes to what addons may do in combat, focused on limiting their ability to automate combat tasks.

So after almost two decades of players supplying their own warnings, the developer built warnings into the game. Why would a telegraph that the boss already shows on screen not be enough for a raid? The answer is a multiplication.

### The model

Let `T_i` be the time player `i` needs to respond to a warning: the GD101 budget, plus network delay, for that player at that moment. Across players and moments, `T_i` varies. Model it as a normal distribution with mean `μ` and standard deviation `σ`.

- `T_tel` is the telegraph length: the time from when the warning becomes visible to when the attack resolves.
- `p` is the chance one player responds in time: `p = Φ((T_tel − μ) / σ)`, where `Φ` is the standard normal cumulative distribution (MA102 week 8).
- `N` is the number of players each cast targets, and `k` is the number of casts per pull.
- `P_clean` is the chance the raid gets through every cast with no failures.

If failures are independent,

```
p       = Φ((T_tel − μ) / σ)
P_clean = p ^ (N × k)
```

This is MA102 week 3's complement rule in another form: the chance of at least one failure is `1 − p^(Nk)`.

Turn it around to design a telegraph. Pick a target clean-pull rate `P*`. Each individual trial must then succeed with `p* = P* ^ (1 / (N k))`, and

```
T_tel = μ + σ × z(p*)
```

where `z(p*)` is the standard normal value with `Φ(z) = p*`.

For this lecture use `μ = 700 ms` and `σ = 150 ms`. The mean is GD101's 617 ms for four distinct warnings, rounded to 620, plus 80 ms of network round trip (section 4). The spread is an assumption you will replace with measurements in the lab.

### Numbers you can check

A mechanic cast five times per pull (`k = 5`). Solo is `N = 1`, a light party is `N = 8`, a raid is `N = 20`.

| Telegraph `T_tel` | `z` | One player `p` | Solo, 5 casts | 8 players, 5 casts | 20 players, 5 casts |
|---|---|---|---|---|---|
| 900 ms | 1.33 | 90.9% | 62.0% | 2.2% | 0.0% |
| 1,000 ms | 2.00 | 97.7% | 89.1% | 39.8% | 10.0% |
| 1,100 ms | 2.67 | 99.62% | 98.1% | 85.8% | 68.1% |
| 1,200 ms | 3.33 | 99.957% | 99.8% | 98.3% | 95.8% |
| 1,300 ms | 4.00 | 99.997% | 100.0% | 99.9% | 99.7% |

Check one cell by hand. At 1,000 ms, `z = (1,000 − 700) / 150 = 2`, and `Φ(2) = 0.97725`. A raid of 20 facing five casts runs 100 trials: `0.97725^100 = 0.100`. One pull in ten is clean.

Now invert. What telegraph gives a 95% clean-pull rate?

| Group | Trials `N × k` | Needed per trial `p*` | `z(p*)` | Telegraph `T_tel` |
|---|---|---|---|---|
| Solo | 5 | 0.98979 | 2.32 | 1,048 ms |
| 8 players | 40 | 0.99872 | 3.02 | 1,152 ms |
| 20 players | 100 | 0.99949 | 3.28 | 1,193 ms |
| 20 players, 99% target | 100 | 0.99990 | 3.72 | 1,258 ms |

Read the two tables together, because they seem to disagree. The second says a raid needs only about 145 ms more warning than a solo player. The first says that at 1,000 ms the solo player succeeds 89% of the time and the raid 10%. Both are true. The raid's curve of success against telegraph length is a **cliff**: it goes from almost always failing to almost always succeeding over a few hundred milliseconds. A designer who tests the mechanic solo at 1,000 ms sees a comfortable 97.7% per cast and ships it. The raid then wipes on nine pulls out of ten. The fix is small in milliseconds, but only if you know which side of the cliff you are on.

### A visual you can move

Open [`examples/w05-raid-telegraph.html`](../examples/w05-raid-telegraph.html). The left view shows one player: the bell curve of response times, with a vertical line at the telegraph length. The area to the right of the line (players too slow) is shaded red. At 1,000 ms that red sliver is 2.3% of the curve, and it looks harmless. The right view shows the raid: clean-pull chance against telegraph length, one curve each for `N × k` of 5, 40 and 100. At 1,000 ms the 100-trial curve sits at 10%.

Drag the telegraph slider from 900 to 1,300 ms. The red sliver on the left barely changes shape. The raid curve on the right sweeps from near 0 to near 100%. Then drag the players slider from 1 to 20 at a fixed 1,000 ms and watch the right-hand dot fall off the cliff. That is the one thing to take away: **a raid sees the tail of the distribution, not its middle.**

### Cross-game recognition

**World of Warcraft, Boss Warnings (patch 12.0.0, January 2026).** The Boss Timeline shows casts before the boss starts them, which raises the effective `T_tel` for every player. The text alerts come in three severity levels, which helps a player triage: a Critical alert tells them that this is the one that kills. In this week's terms both features lower `μ` and, more importantly, `σ`: they give the slowest readers the same information the fastest had. Addon warnings did that job for players who installed them. A raid with a mix of addon users and non-users has two distributions, and the slower one sets the clean-pull rate. Building warnings into the game gives every player the same distribution.

**World of Warcraft, Void Reaver (The Burning Crusade, patch 2.4.0 to 2.4.3).** When the boss stopped targeting before Arcane Orb, addon users lost their timer, and the whole raid fell back to watching for a slow orb in a large room. In the model, `μ` jumped and `σ` widened for every addon user at once. The wiki's earlier advice (January 2008) to start moving within the first second, because the explosion landed before the graphic did, is a report of a telegraph whose visible length was shorter than it looked.

**Final Fantasy XIV (A Realm Reborn onward).** Area attacks are usually shown as bright orange shapes on the ground: circles, donuts, lines and cones. The community wiki describes markers as the game's encounter design "language": learn them once and you can read attacks you have never seen. From Shadowbringers (2019) onward, the wiki notes, high-end and later normal content often shows the orange marker only just before the attack resolves, so players must read the boss's animation or cast name instead. That is a deliberate move along this model's axes. A shorter visible marker lowers `T_tel`, and reading a cast name instead of a shape raises `μ`. Both make the fight harder for everyone, and the raid multiplier makes them much harder for full parties than for a single tester.

Three cases, one model: a spread of response times, a telegraph length, and a power `N × k`. Wherever a group must all respond to a warning, ask what the slowest few players experience, not what the typical one does.

### Eyes-open design judgment

- **Tune to a clean-pull rate, not a per-player rate.** Write the target in your design document ("95% of pulls get through the eruptions for a group at our target skill"), then derive `T_tel`. A per-player success rate means nothing until you raise it to the power `N × k`.
- **Cut the exponent before you lengthen the telegraph.** Targeting 3 players instead of 20, or casting 3 times instead of 5, often does more than 100 ms of extra warning. Mechanics that target the whole raid are expensive in this currency.
- **Your model's tail is probably too thin.** Real response times are skewed. They have a long right tail of slow responses from distraction, a lagging frame or a moment's confusion. A normal curve fitted to the mean and standard deviation underestimates how often a response is very slow. The lab shows that on a realistic data set the normal model predicts a 95% clean pull at 1,200 ms, while the measured data give 37%. Measure your tail directly.
- **Learning moves the curve.** Both `μ` and `σ` fall as players practise a fight. The first night on a boss is far worse than the model at "trained" values predicts. That is acceptable for top-difficulty progression and hostile for content meant for groups formed by matchmaking.
- **Design the failure, not only the warning.** Section 5 shows how turning a wipe into a smaller penalty changes the maths from a product to a sum.

### Check yourself (worked example)

1. A 10-player raid faces a mechanic 4 times per pull with `T_tel = 1,100 ms`, `μ = 700`, `σ = 150`. What is the clean-pull chance?
2. For the same raid and mechanic, what telegraph gives a 90% clean-pull rate?
3. A designer reduces the targets of a 20-player mechanic from everyone to 4 random players, keeping `k = 5` and `T_tel = 1,000 ms`. What happens to the clean-pull chance?

<details>
<summary>Answers</summary>

1. `z = 400 / 150 = 2.67`, `p = 0.99617`. `N × k = 40`, so `P_clean = 0.99617^40 ≈ 0.858`, about 86%.
2. `p* = 0.9^(1/40) ≈ 0.99737`, `z ≈ 2.79`, `T_tel ≈ 700 + 150 × 2.79 ≈ 1,119 ms`.
3. Trials fall from 100 to 20. `0.97725^20 ≈ 0.631`, so the clean-pull chance rises from 10% to 63% without changing the telegraph.

</details>

## 3. Readability: a visual grammar

The model tells you how much warning a raid needs. Readability decides how much of that warning players can use. Every telegraph carries answers to four questions, and each question has a channel that suits it.

| Question | Best channel | Examples |
|---|---|---|
| Where? | Shape on the ground or around a player | Circle, cone, line, donut |
| What kind? | Colour, icon above a player | "Move out" vs "stack together" vs "tank only" |
| When? | A timer drawn on the telegraph | Filling cast bar, shrinking ring, countdown number |
| Is it me? | Marker on or above the targeted player, plus sound | Personal icon, a distinct sound only the target hears |

Four rules follow from the model.

**Consistency lowers `μ`.** GD101's choice cost grows with the number of warnings a player must tell apart. If every boss invents its own look, `n` grows with every boss. If the whole game uses one grammar (orange ground shapes always mean "leave", one stack icon always means "join"), players carry what they learned from boss to boss. Final Fantasy XIV's marker set, which its community describes as a language, is the clearest shipped case. The cost is that a fixed grammar limits surprise, so designers who want to surprise must do it with combinations of known markers, not new ones.

**Redundancy trims the tail.** A telegraph shown in one channel only fails every player who misses that channel: a colour-blind player on a colour-only cue, a player looking at the healing frames on a ground-only cue, a player with sound off on an audio-only cue. Two channels carrying the same message catch most of the players the first channel missed. That lowers `σ` much more than it lowers `μ`, which is exactly what the raid multiplier rewards. Week 14 returns to this for accessibility.

**Clutter hides warnings.** In a raid, 20 players' spell effects share the screen with the boss's telegraphs. GD101 called the time a warning is covered `t_hidden`. In group content it is not a fixed number: it is largest for melee players, who stand where effects are densest. Reserve a colour and a drawing layer for hazards, draw them above player effects, and keep player effects away from that colour. Carmody's GDC 2023 talk on World of Warcraft's visual effects shows the style guides and shared reference material the effects team uses to keep its art direction consistent. Consistency across a whole art department is what makes a reserved hazard colour possible.

**The picture must match the rule.** If the damage area is larger than the drawn shape, or the attack resolves before the animation lands, the telegraph lies. Players who trust it get hit, and the lesson they learn is to stop trusting telegraphs, which raises `μ` for every later warning. The Void Reaver note from 2008 is a record of exactly that mismatch.

## 4. Latency and the snapshot

MMO combat is decided on the server. That changes the telegraph budget in a way single-player games never face.

When the server starts a telegraph, the client sees it one one-way network delay later. When the player moves out, the server learns about it one one-way delay after that. So the round-trip time, `RTT`, comes straight off the telegraph. Then the server resolves the attack at a fixed moment. Final Fantasy XIV players call that moment the **snapshot**: the game's community wiki explains that ground attacks register when the orange marker disappears, not when the attack animation finishes, and that the higher a player's latency, the earlier they must move. Some servers also resolve on a tick, a fixed update interval (MMO302 week 5), which can add up to one tick of extra delay.

Write it into the model as a player-specific mean:

```
μ_i = μ_local + RTT_i        (plus up to one server tick, if the server resolves on ticks)
```

With `μ_local = 620 ms` and `σ = 150 ms`:

| Player's round trip | `μ_i` | `p` at 1,000 ms | `p` at 1,100 ms | `p` at 1,200 ms |
|---|---|---|---|---|
| 20 ms | 640 | 99.18% | 99.89% | 99.99% |
| 80 ms | 700 | 97.72% | 99.62% | 99.96% |
| 150 ms | 770 | 93.74% | 98.61% | 99.79% |
| 250 ms | 870 | 80.69% | 93.74% | 98.61% |

A player on a 250 ms connection needs about 170 ms more telegraph than a player on 80 ms to reach the same per-cast success. Now put that player in a raid. With 19 players at 80 ms and one at 250 ms, a 1,100 ms telegraph cast five times at everyone gives `0.99617^95 × 0.93738^5 ≈ 0.50`, down from 0.68 with all 20 at 80 ms. **One player on a distant connection costs the raid about a quarter of its clean pulls.**

Two design responses follow. Tune telegraphs for the round-trip time of your worst-served region, not your office. And prefer mechanics whose success is judged by position well before the snapshot (a zone the player must reach and hold) over those judged at an exact moment (a dodge at the last 100 ms). CS202 week 11 explains why the server cannot simply rewind time to forgive the late player in a shared world: the other 19 players would see an attack that hit someone standing in it do nothing.

## 5. Designing the failure

Everything so far assumed that one failure wipes the raid. That is only one option, and choosing the failure outcome changes the maths more than any telegraph tweak.

| Failure outcome | What one miss costs | Maths |
|---|---|---|
| Wipe | The pull | Clean-pull chance `p^(Nk)`, a product |
| Death | That player's share for the rest of the fight (week 4) | Expected deaths `N k (1 − p)`, a sum |
| Damage or debuff | Healing, or a share of damage for a while | Expected misses `N k (1 − p)`, each cheap |
| Shared damage | The whole raid takes more damage | Expected misses, cost spread over everyone |

With a wipe, the raid's success is a product and collapses fast. With any of the others it is a sum, and you can read the cost straight off the expected number of misses per pull. At `T_tel = 1,000 ms` and 100 trials, the expected number of misses is `100 × 0.02275 ≈ 2.3`. As a wipe mechanic that is a 10% clean-pull rate. As a death mechanic it is about two deaths a pull, which week 4 showed can cost a tight enrage. As a small damage-over-time debuff it is noise.

This gives you a design dial with three settings:

- **Wipe mechanics** belong where you want the fight to demand perfection, and only with long telegraphs or small `N × k`. Top-difficulty raids use them to create memorable moments. Content formed by matchmaking should almost never use them.
- **Death mechanics** make the fight forgiving of one or two slips, and tie readability to the enrage through week 4's deaths budget.
- **Penalty mechanics** keep the fight moving and punish mostly the player who failed. They suit large groups and players who are still learning.

World of Warcraft's Raid Finder difficulty, which week 6 looks at, is described by the Warcraft Wiki as removing or modifying mechanics that make the raid depend on the performance of a single player. In this week's model that means moving mechanics from the first row of the table to the lower rows.

## In-class activity (25 minutes)

In pairs, with the interactive and a calculator.

1. (5 min) Each person runs the reaction test in the interactive's "measure me" panel 20 times. Pool the class's results on the board and compute the class mean and standard deviation.
2. (5 min) Using the class values, find the telegraph that gives a 95% clean pull for a 10-player group facing a mechanic 4 times per pull.
3. (10 min) Design one mechanic for that group: write its shape, colour, timer, target marker and sound, using the table in section 3. Decide its failure outcome from section 5 and justify it in one sentence.
4. (5 min) Swap with another pair. Name the player your partners' telegraph fails most often (by colour vision, attention, latency or position) and propose one change that helps that player without lengthening the telegraph.

Expected output: the class `μ` and `σ`, your telegraph length, a one-paragraph mechanic spec and the other pair's critique.

## Common misconceptions

- **"If 98% of players dodge it, it's fair."** For one player, maybe. For 20 players facing it five times, 98% per cast gives about a 13% clean-pull rate. Always raise the per-player rate to the power `N × k`.
- **"Longer telegraphs make fights easier in proportion."** The raid curve is a cliff. Near the cliff, 100 ms changes everything. Far above it, another 500 ms changes nothing and makes the fight dull.
- **"Players with high latency should just move earlier."** They must, and they can't see the warning earlier. Every millisecond of round trip comes off their budget. Tuning for low latency alone excludes whole regions.
- **"A normal curve is a safe model for reaction times."** It is a convenient one. Real response times have a heavier slow tail, and raids live in that tail. Fit your telegraphs to measured percentiles.

## Check yourself

1. A 25-player raid faces a raid-wide mechanic 6 times per pull. With `μ = 700`, `σ = 150`, what telegraph gives a 90% clean pull?
2. Using the table in section 2, a designer has a wipe mechanic at 1,000 ms on 20 players with `k = 5`. They can either lengthen the telegraph to 1,100 ms or reduce the targets to 5 players at 1,000 ms. Which gives the higher clean-pull chance?
3. A player's round trip is 180 ms. With `μ_local = 620` and `σ = 150`, what telegraph gives this player a 99.5% chance per cast?
4. Convert the 1,000 ms, 20-player, 5-cast mechanic from a wipe to a death. How many deaths per pull should the design expect? If the boss's week 4 deaths budget is one death, is this acceptable?
5. A mechanic uses a red circle on the ground and nothing else. Name two groups of players for whom `σ` rises, and one change for each.

<details>
<summary>Answers</summary>

1. `N × k = 150`. `p* = 0.9^(1/150) ≈ 0.999298`, `z ≈ 3.19`, `T_tel ≈ 700 + 150 × 3.19 ≈ 1,179 ms`.
2. Lengthening: `0.99617^100 ≈ 0.681`. Reducing targets: `0.97725^25 ≈ 0.563`. Lengthening wins here, 68% against 56%. (Cutting to 3 targets would give `0.97725^15 ≈ 0.708` and win.)
3. `μ_i = 800`. `z(0.995) ≈ 2.576`. `T_tel ≈ 800 + 150 × 2.576 ≈ 1,186 ms`.
4. Expected deaths `100 × 0.02275 ≈ 2.3` per pull. With a one-death budget, most pulls fail the enrage, so no. Lengthen to about 1,100 ms (expected deaths `100 × 0.00383 ≈ 0.4`) or cut the targets.
5. Colour-blind players (add a distinct shape edge or pattern, or an icon above targeted players). Players looking away, such as healers watching raid frames (add a sound or a personal marker). Melee players in dense effects are a third group (draw hazards above player effects).

</details>

## Lab / assignment hook

[Lab 05, telegraph tuning from measured data](../labs/lab05.md). You fit the normal model to a data set of 400 response times, compare its tail with the measured one, and tune three mechanics for a 20-player raid to a 95% clean-pull target using the measured percentiles. The mechanics go into your encounter-design portfolio alongside the bosses from lab 04.

## Sources

- Warcraft Wiki, "Patch 12.0.0" (Midnight systems patch, released 20 January 2026). The Boss Warnings feature set (Boss Timeline and Minor, Medium and Critical text alerts, enabled by default) and the changes limiting addons' ability to automate combat tasks. https://warcraft.wiki.gg/wiki/Patch_12.0.0
- Warcraft Wiki, "Deadly Boss Mods". Description of the addon as a boss alert mod made of per-boss modules with alert messages and timer bars. https://warcraft.wiki.gg/wiki/Deadly_Boss_Mods
- Warcraft Wiki, "Void Reaver" (Tempest Keep, The Burning Crusade). Patch 2.4.0 removed the pre-cast targeting that addons used to warn of Arcane Orb; patch 2.4.3 added a combat log entry; a January 2008 note that the explosion went off before the graphic landed. https://warcraft.wiki.gg/wiki/Void_Reaver
- Warcraft Wiki, "Raid Finder" (current). Raid Finder removes or modifies mechanics that make the raid depend on a single player's performance. https://warcraft.wiki.gg/wiki/Raid_Finder
- Final Fantasy XIV Online Wiki (consolegameswiki), "Common mechanics and markers", "Area of Effect" and "Snapshot" (accessed September 2026). Markers as the game's encounter design language; orange ground telegraphs; late markers in high-end content from Shadowbringers onward; attacks register when the telegraph disappears, and higher latency means moving earlier. https://ffxiv.consolegameswiki.com/wiki/Mechanic , https://ffxiv.consolegameswiki.com/wiki/Area_of_Effect , https://ffxiv.consolegameswiki.com/wiki/Snapshot
- Carmody, S. "Visual Effects Summit: 'World of Warcraft' VFX Pillars." GDC 2023, GDC Vault. https://gdcvault.com/play/1029418/Visual-Effects-Summit-World-of
- The response-time values `μ = 700 ms`, `σ = 150 ms` and `μ_local = 620 ms` are teaching assumptions built on the GD101 week 12 budget, not measurements from a game.

## Interactive spec: examples/w05-raid-telegraph.html

**Purpose.** Show that a telegraph that looks safe for one player fails a raid, because the raid's clean-pull chance is `p^(N k)` and so depends on the slow tail. The first screen must show `T_tel = 1,000 ms`, `N = 20`, `k = 5`: the left view with a thin red tail (2.3%) and the right view with the raid dot at 10%.

**Model (exact).** `p = Φ((T_tel − μ_i) / σ)` with `μ_i = μ_local + RTT`. Clean-pull chance `P_clean = p^(N × k)`. For the mixed-latency toggle, `N − 1` players use `RTT` and one player uses `RTT_slow`: `P_clean = p^((N − 1) k) × p_slow^k`. Required telegraph for a target `P*`: `T_tel = μ_i + σ × Φ⁻¹(P*^(1/(N k)))`. Expected misses per pull `N k (1 − p)`. Implement `Φ` with a standard erf approximation (Abramowitz and Stegun 7.1.26 is accurate enough; error below 1.5e-7) and `Φ⁻¹` with Acklam's rational approximation or bisection on `Φ`.

**Left view, "One player."** Normal density curve of response time from 200 to 1,600 ms, mean `μ_i`, sd `σ`. Vertical line at `T_tel` (ink, labelled "Attack lands"). Area left of the line in steel, labelled "In time: 97.7%"; area right of it in blood red, labelled "Too slow: 2.3%". Optional histogram overlay of the lab's 400-sample data set (embed the numbers inline as a JSON array copied from `labs/lab05-starter/reaction_times.csv`) when the "measured data" toggle is on, with the empirical share too slow shown beside the model's.

**Right view, "The raid."** x axis `T_tel` 600 to 1,600 ms; y axis clean-pull chance 0 to 100%. Three reference curves for `N × k` = 5, 40 and 100 (thin, labelled "solo ×5", "8 ×5", "20 ×5") and a thick curve for the current `N × k`. A dot at the current `T_tel` on the thick curve with its value. A horizontal dashed line at the target `P*` and a vertical marker at the required telegraph, labelled "Needed: 1,193 ms".

**Controls.** Sliders: `T_tel` 600 to 1,600 ms step 10; players `N` 1 to 40; casts per pull `k` 1 to 10; `σ` 50 to 300 step 5; `RTT` 0 to 300 ms step 10; target `P*` 50% to 99% step 1. `μ_local` numeric input, default 620. Toggles: "one slow player" (adds `RTT_slow` slider 0 to 400, default 250), "measured data". Failure outcome selector: Wipe (show `P_clean`) or Death/Penalty (show expected misses per pull instead, same curves replaced by `N k (1 − p)` on a 0 to 10 axis). A small "measure me" panel: a start button, a random delay of 1 to 3 s, then a circle appears and the student presses Space or taps; record 20 trials and show the student's mean and sd with a button "use my numbers" that sets `μ_local` and `σ`. All controls keyboard operable.

**Readout.** `p`, `N × k`, `P_clean`, expected misses, required `T_tel` for `P*`.

**Test values.** Defaults (`μ_local = 620`, `RTT = 80`, `σ = 150`): at 1,000 ms `p = 0.97725`, `P_clean` 89.1% (N 1), 39.8% (N 8), 10.0% (N 20); at 1,100 ms, 68.1% for N 20; at 1,200 ms, 95.8%. Required telegraph for 95%: 1,048 (N 1), 1,152 (N 8), 1,193 (N 20); for 99% at N 20, 1,258. Expected misses at 1,000 ms, N 20, k 5: 2.28. Mixed latency at 1,100 ms, N 20, k 5, RTT 80, RTT_slow 250: 50.3%.

**The one insight.** Dragging `T_tel` from 900 to 1,300 must barely change the left picture and sweep the right one across its full range. Caption: "One player sees the middle of the curve. The raid sees its tail."

**Style and accessibility.** Program tokens inline. Red tail also hatched so it reads without colour. Curves distinguished by thickness and dash. The reaction test must offer a keyboard and a touch path, must not flash (a steady circle appears, no strobing) and respects `prefers-reduced-motion`. Works at 390 px with views stacked.
