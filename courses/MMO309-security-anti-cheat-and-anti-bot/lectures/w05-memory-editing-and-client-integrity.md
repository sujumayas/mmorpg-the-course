# MMO309 · Week 05 — Memory editing and client integrity

**Why this matters:** The game client runs on a computer the cheater owns, so every byte of it can be read and changed. Server authority takes away most of what a memory edit could win, but not all of it. What is left is fought with client integrity checks, and with a choice most students never think about: when to ban someone you have already caught. Getting that timing wrong can leave more cheating in your game, not less.

**You will be able to:**
- Classify a cheat as tampered values, revealed information or automated input, and name the defense that fits each class.
- Compute the precision of an integrity signal from its detection rate, its false-positive rate and the share of players who cheat, and decide whether it may ban on its own.
- Compute bans per signature and cheating sessions for a ban delay `W`, and find the delay that leaves the least cheating.
- Critique a client-protection proposal by what it costs cheat makers, honest players and player privacy.

**Before class:** Hoglund, G. & McGraw, G. (2007), *Exploiting Online Games*, chapter 6 ("Hacking Game Clients", pp. 113-184). Read it as a defender and, for each technique, write down what the technique needs the client to hold or to trust. The Ninth Circuit's description of Warden in *MDY Industries v. Blizzard Entertainment* (2010), section V.A, one page.

**Prerequisites from earlier courses:** [CS202 week 4, server authority](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md) (clients send intent, the server decides results). [MA102 week 14, hypothesis testing](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (false positives and false negatives). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance a player shows up at least once in `n` days). From this course, [week 1](w01-threat-modeling-for-games.md) (the Glider and Warden story, and attackers as a business) and [week 2](w02-never-trust-the-client.md) (what the client can lie about and what it can learn).

**Interactive:** [Ban wave timing](../examples/w05-ban-wave-timing.html). Keep it open during section 3.

---

## 1. What a memory edit can win

A **memory edit** changes a value in the running game client: health, gold, a cooldown timer, a position, a flag that says whether a wall is visible. A **code patch** changes the client's instructions instead. An **injected module** is foreign code loaded into the client process, which can do both. And a separate program can read the client's memory without changing anything, or send keystrokes and mouse movements as if a person made them.

You cannot stop any of this on the attacker's machine. The attacker has administrator rights, a debugger, and all the time in the world. Every defense in this lecture raises the cost of cheating or shortens how long a cheat keeps working. None of them makes cheating impossible. Say that out loud in your first design meeting, because someone will propose a protection that "stops memory editing" and you should know what to ask next.

What a memory edit can *win* depends on your server, and it falls into three classes:

| Class | Examples | Does server authority stop it? | Defense that fits |
|---|---|---|---|
| Tampered values | edit gold to 999,999; zero a cooldown; set run speed to 3× | Yes, if the server holds the real value and validates intent | Server authority (CS202 week 4), movement validation ([week 3](w03-speed-hacks-and-movement-validation.md)) |
| Revealed information | see enemies through walls; show hidden traps; read another player's cooldowns | Only if the server never sent the information | Send less ([week 2](w02-never-trust-the-client.md)) |
| Automated input | aimbot, triggerbot, farming bot, perfect rotation script | No. Every input is legal, only its source is fake | Client integrity checks and behavioral detection (weeks 5, 7, 8) |

Read the table from top to bottom and it is also a priority list. The first row you can close completely by design. Many older games did not, because they let the client compute damage or movement to save server time, and memory editors were the result. In an authoritative MMO, editing your gold changes the number your own screen shows and nothing else. The server's number is the one that pays for things.

The second row you can shrink but not close. Week 2 put a number on it. The server must send some information early, or remote players pop into view late, and whatever is sent can be read.

The third row is where this week's tools live. A farming bot that walks to a tree, clicks it and banks the logs sends exactly the commands a human would send. The server sees legal intent. Only two things can tell the bot from the person. One is the software running next to the game, which is what client integrity checks look for. The other is the statistical shape of the behavior, which weeks 7 and 8 study.

## 2. The client integrity toolbox

Every tool below is a way of asking the attacker's machine to testify against itself. That is why each one works only until the attacker adapts, and why each one has a cost to honest players.

**Signature scanning.** The anti-cheat looks in memory for byte patterns known to belong to specific cheats. Valve Anti-Cheat (VAC), first released with Counter-Strike in 2002, scans memory and processes for signatures and sends anomalies for analysis. When engineers confirm a new cheat, its signature joins the database. Signatures are very precise, since a match means that exact cheat's code is present, and they are blind to anything new.

**Code integrity checks.** The anti-cheat checks that the game's own code has not been changed. In the Ninth Circuit's description, Blizzard's Warden (launched September 2005) had two parts. `scan.dll` scanned the computer's RAM before a player could connect. A resident part then ran periodically, asked the computer to report portions of the World of Warcraft code running in memory, and looked for patterns of known bots or cheats. The court also records the first counter-move. Glider's maker reconfigured it to load only after `scan.dll` finished its check.

**Moving the target.** The studio changes the client often, or hides and reshuffles the code a cheat depends on, so every cheat breaks and must be rebuilt. Valve's engineers have said that VAC itself is sent down in small, frequently updated pieces, so a cheat maker only ever sees part of it. RuneScape's ClusterFlutterer update of 25 October 2011 changed the client so that injection and reflection bots, which read the game's state directly from the Java client, stopped working. Jagex believed those made up 98% of the bots in the game. Section 3's cross-game notes return to it.

**Kernel-level drivers.** The anti-cheat runs with the operating system's highest privileges, so a cheat running at a normal privilege level cannot hide from it. Riot Vanguard, released with Valorant in April 2020 and added to League of Legends in April 2024, is the best-known example. Cheat makers answered by moving the cheat off the PC entirely, onto hardware that reads memory over the PCIe bus (a DMA card). The cheat now runs on a second computer the anti-cheat cannot see.

**Server-side statistics.** No client involvement at all. The server looks at what players do. Valve described a machine-learning system, VACNet, for Counter-Strike: Global Offensive in 2017 and at GDC in 2018, which flags suspicious players for human review. [Weeks 7](w07-bot-detection-behavioral-features.md) and [8](w08-machine-learning-for-detection-overview.md) cover this family.

Look at the pattern. Each tool forces a counter-move, and each counter-move costs the cheat maker time and money. That is the game you are really playing. Client integrity does not buy you truth. It buys you time, measured in the days between the moment a cheat stops working and the moment its fixed version ships. Section 3 is about spending that time well.

## 3. Worked example: why wait to ban a cheater you already caught?

### The hook

Valve Anti-Cheat flags an account as soon as it detects a known cheat, and the player is told nothing. The permanent ban arrives later, "days or even weeks" later in the phrase Wikipedia's article on VAC uses, and often for many accounts at once in what players call VAC waves. Valve never says which cheat was detected or when.

This looks backwards. If Valve knows you are cheating on Monday, every match you play until the wave is ruined for nine other people. Players complain about exactly that. Why would a studio let a caught cheater keep cheating?

Because the ban is a message. The moment a cheat's users start getting banned, its maker knows the signature is burned and ships a new build. The model below shows what that message costs, and why a short wait can leave less cheating in the game than an instant ban.

### The model

A cheat has `N` users. You ship a new detection signature on day 0. Track one **signature cycle**, the `S` days until your team can ship the next signature.

- `N` is the number of players using this cheat.
- `q` is the chance that a given user plays on a given day.
- `R` is the cheat maker's reaction time, in days from their first banned customer to a fixed build that evades the signature.
- `W` is your ban delay. You flag silently for `W` days, then ban every flagged account at once. `W = 0` means ban on detection.
- `S` is the cycle length, the days until your next signature. Assume `W ≤ S`.

The cheat maker learns nothing until the first ban, which comes at day `W`. After that the signature keeps catching players who log in for `R` more days, then the new build ships and it goes blind. So a user is caught if they play at least once in `W + R` days:

```
caught(W)   = N × (1 − (1 − q)^(W + R))
sessions(W) = q × N × W  +  q × (N − caught(W)) × (S − W)
```

The first line is the complement rule from MA102 week 3. The second counts cheating sessions over the cycle. Everyone cheats freely during the delay. After the wave, the users you missed keep cheating until the cycle ends. (To keep it hand-computable, the model ignores the few sessions during the `R` days after the wave and new users joining mid-cycle.)

The trade-off is visible in the formula. Raising `W` adds `q × N` sessions per day of waiting and shrinks the missed group by a factor of `(1 − q)` per day.

### Numbers you can check

Take `N = 10,000`, `q = 0.5`, `R = 2` days and `S = 30` days.

```python
def one_signature(W, N=10_000, q=0.5, R=2, S=30):
    """Expected bans and cheating sessions for one signature cycle of S days."""
    caught = N * (1 - (1 - q) ** (W + R))
    sessions = q * N * W + q * (N - caught) * (S - W)
    return caught, sessions

print(" W  caught  sessions")
for W in (0, 1, 2, 3, 5, 7, 14):
    caught, sessions = one_signature(W)
    print(f"{W:2}  {caught:6.0f}  {sessions:8.0f}")

best = min(range(0, 31), key=lambda W: one_signature(W, q=0.2)[1])
print("best delay when q = 0.2:", best, "days")
```

It prints:

```
 W  caught  sessions
 0    7500     37500
 1    8750     23125
 2    9375     18750
 3    9688     19219
 5    9922     25977
 7    9980     35225
14   10000     70001
best delay when q = 0.2: 6 days
```

Check two rows by hand. At `W = 0`, `caught = 10,000 × (1 − 0.5²) = 7,500`, and the 2,500 you missed play half their days for 30 days: `0.5 × 2,500 × 30 = 37,500` sessions. At `W = 2`, `caught = 10,000 × (1 − 0.5⁴) = 9,375`. The wait costs `0.5 × 10,000 × 2 = 10,000` sessions, and the 625 you missed add `0.5 × 625 × 28 = 8,750`, for 18,750 in all.

Three things to notice.

1. **Instant bans are not the least cheating.** They leave twice as many cheating sessions as a two-day wait, because they tell the cheat maker to move while a quarter of the users have not logged in yet.
2. **Long waits are worse than instant bans.** At 14 days you catch every user and have let all of them cheat for two weeks first. The curve is U-shaped, and the bottom is narrow.
3. **The best delay depends on how often cheaters play.** With `q = 0.5` it is 2 days. With `q = 0.2` it is 6 days. Occasional cheaters take longer to show up, so a wave has to wait longer to catch them. With `q = 0.8` it is 0. If nearly everyone plays daily, the vendor's reaction time already catches most of them and waiting only adds harm.

### A visual you can move

Open the interactive. The left chart plots `caught(W)` against `W`. It climbs quickly and flattens near `N`, which is the view a detection team looks at: "a wave catches more." The right chart plots `sessions(W)` on the same axis. It is the view a player feels, and it is a U with a marked minimum. Drag `q` down and watch the minimum slide to the right. Drag `R` up (a slow cheat maker) and watch it slide to the left, because a slow maker already gives you the waiting for free. Drag `S` down, meaning your team ships signatures quickly, and the whole right curve falls while the minimum moves toward zero. Fast signature production is worth more than clever timing.

### Cross-game recognition

**Counter-Strike and other VAC games (2002 to now).** The hook. Detection is immediate and silent. Bans come after a delay of days or weeks, in waves, with no detail about the cheat. Wikipedia's article reports over 600,000 accounts banned in December 2018 alone. In the model, Valve chooses `W > 0` and keeps `R` from starting by revealing nothing.

**World of Warcraft, Warden and Glider (2005 to 2008).** Week 1 told this story as business. Here it is as timing. In September 2005 Blizzard used Warden to ban most Glider users at once. The maker learned instantly, reconfigured Glider to load after Warden's scan, sold detection-avoidance as a $5-a-month add-on, and afterwards Warden only occasionally detected it. One large ban told the cheat maker exactly what to fix, and the next signature was much harder to get. In the model, that is a short `R` and a very long `S`.

**RuneScape, ClusterFlutterer (25 October 2011).** Jagex did not ban on detection. It prepared a client change that broke injection and reflection bots, announced a countdown, and shipped it all at once with a wave of bans. At RuneFest that week, Jagex's Mark Gerhard said 7.7 million accounts had been banned for gold farming in four days. Rewrite it in the model: the "signature" was a whole client change, `W` was the development time, and the wave was one day. The model's logic applies to fixes as well as detections. Ship them together, not one at a time.

**RuneScape, Botwatch (September 2012).** For contrast, Jagex's behavioral detector banned accounts directly and automatically. Behavioral detection does not tell a bot maker which bytes were found, so it leaks less and the model's case for waiting is weaker. Week 7 picks up behavioral features. Botwatch also produced this week's most useful false-positive story, in section 4.

Four systems, one question: **what does my ban teach the attacker, and how fast can they use it?** If the answer is "which code to change, within days," a short delay pays. If the answer is "very little," ban fast.

### Eyes-open design judgment

- **Waves buy review time.** A delay also gives your team days to check flagged accounts by hand before banning, which catches detector bugs before they hit thousands of innocent players. Section 4 shows why that matters.
- **Waves cost victims now.** Every day of delay is a day of ruined matches for honest players. A competitive shooter with high `q` and ranked stakes may choose short `W` for that reason alone. Measure `q` from your data instead of guessing.
- **Separate the penalty from the ban.** You can quietly remove a flagged player's rewards, or match flagged players with each other, during the delay. That cuts the harm term without teaching the cheat maker anything, at the price of hiding the penalty from the player, which raises fairness and transparency questions for [week 12](w12-legal-and-ethical-considerations.md).
- **Waves help bots.** A bot farm earns money every day it runs, including the days between detection and the wave. Week 6 puts that number in dollars, and it points the other way.

### Check yourself (worked example)

1. With `N = 10,000`, `q = 0.5`, `R = 2`, `S = 30`, compute `caught` and `sessions` for `W = 4`.
2. A cheat maker now fixes their build within 12 hours of the first ban (`R = 0.5`). Does the best `W` go up or down? Explain with the model, not intuition.
3. Your cheaters play 20% of days. Management wants instant bans "because they look strong". Using the model with `N = 10,000`, `R = 2`, `S = 30`, how many more cheating sessions does instant banning leave than the best delay?

<details>
<summary>Answers</summary>

1. `caught = 10,000 × (1 − 0.5⁶) = 9,844`. `sessions = 0.5 × 10,000 × 4 + 0.5 × 156 × 26 = 20,000 + 2,031 ≈ 22,031`.
2. It goes up. With a faster maker, an instant ban catches only users who play within half a day, so the missed group `N(1 − q)^(W+R)` is much larger at `W = 0`, and waiting a little longer lets you catch them before the maker even learns. The benefit side of the trade-off grows, the cost side (`q × N` per day) does not change.
3. At `W = 0`, `caught = 10,000 × (1 − 0.8²) = 3,600` and `sessions = 0.2 × 6,400 × 30 = 38,400`. At the best delay, 6 days, `caught = 10,000 × (1 − 0.8⁸) = 8,322.3`, so 1,677.7 are missed, and `sessions = 0.2 × 10,000 × 6 + 0.2 × 1,677.7 × 24 = 12,000 + 8,053 = 20,053`. (Rounding the missed group to 1,678 first gives 20,054.) Instant banning leaves about 18,350 more sessions, nearly twice as many.

</details>

## 4. Precision: who pays for a false positive

A detection signal has a **recall** (the share of cheaters it flags) and a **false-positive rate** (the share of honest players it flags). What decides whether it may ban on its own is its **precision**, the share of flagged players who are really cheating:

```
precision = recall × cheaters / (recall × cheaters + false-positive rate × honest players)
```

You met this as a base-rate problem in MA102 week 14. It bites hard in anti-cheat, because the share of players who cheat is small, and the honest players far outnumber the cheaters even when both rates look good.

Compare three signals on a game with 1,000,000 players. "Unknown module" fires when unrecognized code is loaded into the game process. It catches 95% of cheaters, and it also fires on 0.2% of honest players, whose overlays, recorders, accessibility tools and drivers inject code too. "Known cheat signature" catches only the 60% of cheaters using a cheat you have seen, but almost never fires on anyone else. "Module and behavior" requires the unknown module and an independent behavioral anomaly that fires on 1% of honest players and 70% of cheaters.

```python
def precision(players, base_rate, recall, fpr):
    cheaters = players * base_rate
    honest = players - cheaters
    true_pos = recall * cheaters
    false_pos = fpr * honest
    return true_pos, false_pos, true_pos / (true_pos + false_pos)

signals = {
    "unknown module":        (0.95, 0.002),
    "known cheat signature": (0.60, 0.00001),
    "module AND behavior":   (0.95 * 0.70, 0.002 * 0.01),
}
for base_rate in (0.01, 0.001):
    print(f"base rate {base_rate:.1%} of 1,000,000 players")
    for name, (recall, fpr) in signals.items():
        tp, fp, prec = precision(1_000_000, base_rate, recall, fpr)
        print(f"  {name:22} caught={tp:6.0f} innocent flagged={fp:5.0f} precision={prec:.1%}")
```

It prints:

```
base rate 1.0% of 1,000,000 players
  unknown module         caught=  9500 innocent flagged= 1980 precision=82.8%
  known cheat signature  caught=  6000 innocent flagged=   10 precision=99.8%
  module AND behavior    caught=  6650 innocent flagged=   20 precision=99.7%
base rate 0.1% of 1,000,000 players
  unknown module         caught=   950 innocent flagged= 1998 precision=32.2%
  known cheat signature  caught=   600 innocent flagged=   10 precision=98.4%
  module AND behavior    caught=   665 innocent flagged=   20 precision=97.1%
```

The rates are invented for teaching. The lesson is not. The unknown-module signal flags about 2,000 innocent players whatever the base rate. When cheaters are rare, those innocents are two thirds of everyone flagged. A signal like that is evidence to combine with other evidence, never a verdict. Requiring two independent signals multiplies the false-positive rates (`0.002 × 0.01`), which is why the combined rule keeps high precision while catching more than the signature alone. The independence assumption is doing real work there. If an honest player's overlay also makes their play look unusual, the two signals are not independent, and the combined false-positive rate is higher than the product.

False positives are not hypothetical. Three that made the news:

- **Call of Duty: Modern Warfare 2 on Steam (July 2010).** About 12,000 owners were VAC-banned when a Steam update changed a DLL on disk after the game had loaded it into memory, which looked like tampering. Valve revoked the bans and gave the affected players a copy of Left 4 Dead 2.
- **RuneScape, Botwatch (27 September 2012).** A heuristic from the testing phase was switched on by accident and banned around 40,000 accounts permanently within an hour. Jagex unbanned every one, but items the affected players dropped while being removed were destroyed and not refunded.
- **Counter-Strike 2 (October 2023).** A driver update for some AMD graphics cards added a feature that detoured game DLL functions. VAC flagged it as a cheat. AMD withdrew the update and Valve said it would unban the affected users.

Each of these fits the model. A benign change to honest players' machines raised the false-positive rate of an integrity signal overnight, while the base rate of cheating stayed the same. A delay with human review, from section 3, would have caught all three before a single ban. It is one more reason the best systems separate "flag" from "ban".

## 5. What client integrity costs honest players

Every client protection runs on hardware you do not own, and the owners are mostly innocent. Weigh four costs every time.

- **Privacy.** A scanner that looks at other processes may see things that are none of your business. Wikipedia's Blizzard article notes that Warden scans processes beyond the game, and that this led to accusations of spyware from privacy advocates. Collect the least you need, send hashes and verdicts rather than raw memory where you can, and say plainly in your terms what you scan.
- **Security.** A kernel driver is code with the highest privileges on the player's PC. An attacker who finds a bug in it can use that bug against the player's whole machine. That is why Riot runs a bug bounty for its driver ([week 13](w13-bug-bounty-and-disclosure.md) has the numbers), and why some players refuse kernel anti-cheat outright.
- **Compatibility.** Integrity checks break on unusual but legitimate setups: compatibility layers, overlays, accessibility software, new drivers. The AMD case above is one example. Every exception you add is also a place a cheat can hide.
- **Performance.** Scans and obfuscation cost CPU time. RuneScape's ClusterFlutterer changes hurt frame rates for many players, and Jagex reworked them in May 2012 because of it.

The eyes-open rule for this whole lecture: **spend client integrity on the automated-input class, where nothing else works, and spend server design on the other two classes, where client integrity is the weaker tool.** A studio that uses a kernel driver to stop players editing their gold has picked a costly tool for a problem an authoritative server solves for free.

## In-class activity (25 minutes)

Groups of three. You get a one-page description of a small action MMO. Its client holds: its own health and position, all monsters within 150 meters with their health, the loot table of the monster being fought, other players' positions within 100 meters, a local auto-attack timer, and a crafting minigame whose timing is scored on the client.

1. For each item, name what a memory edit or memory read could win and put it in one of the three classes (10 minutes).
2. For each tampered-value or revealed-information item, propose a server-side change and name its cost (8 minutes).
3. For the automated-input items, choose between a signature, an integrity check or behavioral detection. Using the section 3 model, estimate a ban delay for a population where you expect `q = 0.3` and `R = 3` days, with `S = 21` (7 minutes).

Expected output: a table with one row per item (class, win, defense, cost), and one ban delay with the calculation that supports it.

## Common misconceptions

- **"Kernel anti-cheat stops memory editing."** It raises the cost of software cheats on the same PC. Hardware that reads memory from a second device, or a person with a debugger and patience, can still read and change the client. It buys time, not certainty.
- **"If we caught them, ban them now."** An instant ban tells the cheat maker which signature to beat. When cheaters play on only some days, a short delay catches more of them and leaves less cheating overall.
- **"A detector that is 99.8% accurate on honest players is safe to auto-ban with."** A 0.2% false-positive rate across a million honest players is 2,000 wrongful bans. Precision depends on how rare cheaters are, not only on the detector.
- **"Server authority makes client anti-cheat unnecessary."** It removes the tampered-value class. Revealed information and automated input remain, and authority cannot see either.

## Check yourself

1. A shooter sends every enemy's position to every client each tick. A player uses a program that reads those positions from memory and draws boxes around enemies. Which class is this? Which defense removes most of it, and what does that defense cost?
2. A new "debugger attached" signal fires on 90% of cheaters and 0.5% of honest players. Your game has 2,000,000 players and about 0.2% cheat. What is its precision? Would you let it ban on its own?
3. You combine it with a signature that fires on 50% of cheaters and 0.001% of honest players, and require both. Assuming independence, what are the combined recall, false-positive rate and precision?
4. With `N = 5,000`, `q = 0.4`, `R = 1`, `S = 20`, compute `sessions` for `W = 0`, `W = 3` and `W = 6`. Which is best?
5. A colleague proposes moving the crafting minigame's scoring to the client "to save server CPU", protected by an integrity check. Using section 1's table and section 5's costs, argue for or against.

<details>
<summary>Answers</summary>

1. Revealed information. Sending only what each client may see (week 2's visibility and line-of-sight policies) removes most of it. The cost is server CPU for visibility checks and some pop-in when the look-ahead is too small.
2. Cheaters `4,000`, honest `1,996,000`. True positives `3,600`, false positives `0.005 × 1,996,000 = 9,980`. Precision `3,600 / 13,580 = 26.5%`. No. Three of every four flagged players would be innocent.
3. Recall `0.9 × 0.5 = 0.45`, false-positive rate `0.005 × 0.00001 = 0.00000005`. True positives `1,800`, false positives about `0.1`. Precision about 99.99%. You catch fewer cheaters, and almost no innocents.
4. `W = 0`: `caught = 5,000 × (1 − 0.6¹) = 2,000`, `sessions = 0.4 × 3,000 × 20 = 24,000`. `W = 3`: `caught = 5,000 × (1 − 0.6⁴) = 4,352`, `sessions = 0.4 × 5,000 × 3 + 0.4 × 648 × 17 = 6,000 + 4,406 = 10,406`. `W = 6`: `caught = 5,000 × (1 − 0.6⁷) = 4,860`, `sessions = 12,000 + 0.4 × 140 × 14 = 12,000 + 784 = 12,784`. `W = 3` is best of the three.
5. Against. Client-side scoring moves the minigame from the tampered-value row, which server authority closes for free, into a row that only client integrity can defend. You trade a small CPU cost for a permanent detection problem with privacy, compatibility and false-positive costs. If CPU is the issue, validate a sampled share of results on the server instead (week 2's sampled validation).

</details>

## Lab / assignment hook

No new lab this week. Add every automated-input threat from the in-class game to your [Lab 01](../labs/lab01.md) threat ledger, with the ban delay you would choose and the section 3 calculation behind it. Lab 06 next week reuses the delay `W` in a bot farm's profit model, where it has the opposite effect.

## Sources

- *MDY Industries, LLC v. Blizzard Entertainment, Inc.*, 629 F.3d 928 (9th Cir. 2010), opinion filed 14 December 2010. Section V.A describes Warden's `scan.dll` and resident component, and Glider loading after `scan.dll`; the statement of facts gives Warden's launch in September 2005, the ban of most Glider users, Glider Elite at five dollars a month, and Warden only occasionally detecting Glider afterwards. Retrieved from CourtListener, September 2026.
- Wikipedia, "Valve Anti-Cheat" (retrieved September 2026). First release with Counter-Strike in 2002; signature scanning; immediate silent flagging and bans after "days or even weeks"; VAC waves; over 600,000 accounts banned in December 2018; the July 2010 Modern Warfare 2 false positives (about 12,000 accounts, bans revoked, Left 4 Dead 2 given); the October 2023 AMD Anti-Lag+ bans in Counter-Strike 2; VACNet announced 2017 and presented at GDC 2018; John Cook's description of VAC delivered in small portions.
- Wikipedia, "Riot Vanguard" (retrieved September 2026). Kernel-level anti-cheat; released with Valorant in April 2020; added to League of Legends on 11 April 2024; DMA cards as a documented cheating method; questions about kernel-level security risks.
- Wikipedia, "Blizzard Entertainment", section on the Warden client (retrieved September 2026). Warden scanning processes beyond the game and the resulting spyware accusations.
- RuneScape Wiki, "ClusterFlutterer" (retrieved September 2026). 25 October 2011; injection and reflection bots disabled; Jagex's 98% estimate; 7.7 million accounts banned between 25 and 29 October as stated at RuneFest; frame-rate problems and the 3 May 2012 changes. https://runescape.wiki/w/ClusterFlutterer
- RuneScape Wiki, "Botwatch" (retrieved September 2026). Behavioral detection with direct bans from September 2012; the rogue ban glitch of 27 September 2012, around 40,000 accounts, all unbanned, dropped items not refunded. https://runescape.wiki/w/Botwatch
- Hoglund, G. & McGraw, G. (2007). *Exploiting Online Games: Cheating Massively Distributed Systems*. Addison-Wesley. Chapter titles and page numbers from the publisher's table of contents (InformIT).

## Interactive spec: examples/w05-ban-wave-timing.html

**The one insight:** a wave catches more cheaters the longer you wait, but cheating sessions follow a U-shape. Instant bans and long waits both leave more cheating than a short, well-chosen delay, and the best delay moves with how often cheaters play.

**Layout.** Two charts side by side on desktop, stacked on mobile with the sessions chart first. Controls above, readout table below.

**Left chart, "what the detection team sees".** x-axis `W` from 0 to `S` days (integer steps). y-axis `caught(W)`, 0 to `N`. Draw the curve and a dot at the current `W`. Label the value.

**Right chart, "what players feel".** Same x-axis. y-axis `sessions(W)`. Draw the curve, a dot at the current `W`, and a highlighted marker at the minimum over integer `W` with its label ("best delay: 2 days, 18,750 sessions"). Shade the region where `sessions(W) < sessions(0)` so students see how wide the "better than instant" band is. Draw a horizontal dashed line at `sessions(0)`.

**Controls.**
- `W` ban delay: slider 0 to `S`, step 1, default 0. Also a button "Jump to best".
- `q` daily play chance: 0.05 to 0.95, step 0.05, default 0.5.
- `R` cheat maker reaction, days: 0.5 to 10, step 0.5, default 2.
- `S` days until next signature: 5 to 60, step 1, default 30. Clamp `W` to `S`.
- `N` users: 1,000 to 100,000, default 10,000 (both charts scale linearly, so this only changes the labels).

**Model.** `caught(W) = N (1 − (1 − q)^(W + R))`; `sessions(W) = qNW + q (N − caught(W)) (S − W)`. Search the minimum over integer `W` from 0 to `S`.

**Readout table** (copyable): `W`, `caught`, `missed`, `sessions`, `sessions(0)`, best `W`, `sessions` at best, percent change from instant.

**Test values.**
- Defaults: `W = 0` gives 7,500 and 37,500; `W = 1` gives 8,750 and 23,125; `W = 2` gives 9,375 and 18,750 (best); `W = 3` gives 9,688 and 19,219; `W = 14` gives 10,000 and 70,001.
- `q = 0.2`: best `W = 6`, `caught = 8,322`, `sessions = 20,053`; `W = 0`: 3,600 and 38,400.
- `q = 0.8`: best `W = 0`, 9,600 and 9,600.
- `N = 5,000`, `q = 0.4`, `R = 1`, `S = 20`: `W = 3` gives 10,406 sessions (check-yourself question 4).

**Accessibility.** Sliders keyboard operable with visible values. The minimum marker is labelled in text, not color only. A live region announces "best delay N days" when parameters change. No animation under `prefers-reduced-motion`.
