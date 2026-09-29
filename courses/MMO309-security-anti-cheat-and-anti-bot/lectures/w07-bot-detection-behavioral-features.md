# MMO309 · Week 07 — Bot Detection: Behavioral Features

**Why this matters:** Client-side anti-cheat can be bypassed by a bot that reads the screen and moves a real mouse. What a bot cannot hide is what it does in your world, hour after hour, because that behavior is the reason it exists. This week you learn to turn server logs into features that separate bots from people, and to tell a feature that will last from one the next bot update will erase.

**You will be able to:**
- Compute the coefficient of variation of action intervals and predict it for a jittered bot and for a log-normal human.
- Explain why raw timing features falsely flag skilled players on cooldown-gated rotations, and correct the feature with the slack transform.
- Compute a self-similarity score from hourly activity vectors with cosine similarity.
- Rank candidate features by what it costs a bot operator to fake them, and defend a feature set on that basis.

**Before class:** Lee, Woo, Kim, Mohaisen & Kim, "You Are a Game Bot!: Uncovering Game Bots in MMORPGs via Self-similarity in the Wild" (NDSS 2016), sections I to III (about 20 minutes). Hoglund & McGraw, *Exploiting Online Games* (2007), the chapter on bots, for the attacker's view. Reread [MA102 week 5 on variance](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w05-variance-and-swingy-designs.md).

**Prerequisites from earlier courses:** [MA102 week 5, variance and standard deviation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w05-variance-and-swingy-designs.md). [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (skewed distributions and why the median beats the mean for them). [DB201 week 10, telemetry design](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md) (the events you need must be logged before you can detect anything). [MMO304 week 11, real-money trade and gold farming](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) (the farmer's cost per hour). From this course, [week 5 on client integrity](w05-memory-editing-and-client-integrity.md) and [week 6 on botting economics](w06-botting-economics.md).

**Interactive:** [Bot vs human click timing](../examples/w07-click-timing.html). Use it during section 2.

---

## 1. What a bot is, and what you can observe

A **bot** is a program that plays the game for a person. In an MMO the usual goal is money. The bot farms gold, materials or experience that its operator sells, or it levels accounts for sale. Week 6 built the operator's profit model. This week starts from the other side of the same fact. Because a bot exists to produce value, it has to spend many hours doing the same productive thing. That behavior lands in your logs whether the bot is clever or not.

Bots come in roughly three families, and they differ in what the client can see.

- **Injection and reflection bots** run inside or alongside the game client and read its memory. [Week 5](w05-memory-editing-and-client-integrity.md)'s client-integrity tools aim at these.
- **Colour or pixel bots** read the screen, the way a person does, and send ordinary operating-system mouse and keyboard events to the official client. The client has almost nothing to detect.
- **Headless bots** skip the client entirely and speak the network protocol directly. Only the server sees them.

Your server sees every family. It records each action the client sends, when it arrived, where the character was, what dropped, who traded with whom. A **behavioral feature** is a number computed from those records for one account over some period that tends to differ between bots and people. Detection is the craft of choosing features, combining them into a decision, and keeping them working after the bot authors notice.

Three properties decide whether a feature is worth keeping.

1. **Separation.** How far apart are bots and humans on it? Measure this on labelled accounts.
2. **Robustness to innocent variation.** Does it misfire on some honest group of players? Every false positive is a real person you accuse.
3. **Cost to fake.** If the bot author learns about the feature, what does it cost them to move their bot into the human range? A feature that costs one line of code to defeat has a short life. A feature that costs the operator income lasts.

The worked example takes the most famous feature, action timing, through all three tests.

## 2. Worked example: bot vs human click timing

### The hook

In 2006, researchers at Academia Sinica studied the network traffic of Ragnarok Online players and the bots that were common in that game at the time. The first difference they reported was **how regularly the client released its commands**. Bots issued commands on a tighter schedule than any person. Their conservative detection scheme, built partly on this, made no false accusations against the genuine players in their data sets.

It sounds too easy. A human clicking every second or so and a bot clicking every second look the same on average. The difference is in the spread. That is what this example measures, and then breaks.

### The model

Take the sequence of times between consecutive actions for one account, the **action intervals** `g₁, g₂, ..., gₙ` in milliseconds. Compute the mean `μ` and the standard deviation `σ`, as in MA102 week 5. The feature is the **coefficient of variation**:

```
CV = σ / μ
```

CV has no units. It measures spread relative to the typical gap, so a slow player and a fast player can be compared on one scale. A CV of 0.1 means the gaps typically wander about 10% from their mean.

Two simple models predict CV before you look at any data.

**A jittered bot.** The simplest bot waits a fixed delay `d` and adds uniform random jitter between `−j` and `+j`. A uniform distribution of width `2j` has standard deviation `j / √3`. So:

```
CV_bot = j / (d × √3)
```

**A human.** Human response times are right-skewed. Most gaps cluster near a typical value, and a long tail comes from looking away, reading chat, deciding. A **log-normal** distribution is a standard model for this shape. If `ln(g)` is normal with standard deviation `s` (the **shape**), the CV depends on `s` alone:

```
CV_human = √(e^(s²) − 1)
```

The median gap does not enter. A fast human and a slow human with the same shape have the same CV.

### Numbers you can check

With `d = 1,000 ms` and teaching values for the human shape `s`, the models give:

| Account | Parameters | Predicted CV |
|---|---|---|
| Naive bot | `d = 1,000`, `j = 100` | `100 / (1,000 × 1.732) = 0.058` |
| Jitter bot | `d = 1,000`, `j = 400` | `400 / 1,732 = 0.231` |
| Human | log-normal, `s = 0.6` | `√(e^0.36 − 1) = √0.433 = 0.658` |
| Human, steadier | log-normal, `s = 0.4` | `√(e^0.16 − 1) = √0.174 = 0.417` |

The jitter bot quadrupled its randomness and still sits far below the human. A rule such as "flag if CV < 0.35" separates all four rows. You can verify each value on a calculator.

Now the same idea on simulated accounts, 200 intervals each, including two kinds of account the table left out. The code below runs with the standard library only.

```python
import math
import random
import statistics

rng = random.Random(7)
N = 200         # action intervals sampled per account
GCD = 1500      # ms, a global cooldown that gates the rotation

def cv(xs):
    return statistics.pstdev(xs) / statistics.mean(xs)

def lognormal(median, shape):
    return median * math.exp(rng.gauss(0, shape))

accounts = {
    # name: (function returning one interval in ms, cooldown that gated it)
    "naive bot":      (lambda: 1000 + rng.uniform(-100, 100), 0),
    "jitter bot":     (lambda: 1000 + rng.uniform(-400, 400), 0),
    "mimic bot":      (lambda: lognormal(900, 0.6), 0),
    "casual human":   (lambda: lognormal(900, 0.6), 0),
    "rotation human": (lambda: GCD + lognormal(150, 0.7), GCD),
    "rotation bot":   (lambda: GCD + 60 + rng.uniform(-20, 20), GCD),
}

print(f"{'account':15s} {'raw CV':>7s} {'slack CV':>9s}")
for name, (draw, cooldown) in accounts.items():
    gaps = [draw() for _ in range(N)]
    slack = [g - cooldown for g in gaps]   # time after the action became available
    print(f"{name:15s} {cv(gaps):7.3f} {cv(slack):9.3f}")
```

Output:

```
account          raw CV  slack CV
naive bot         0.060     0.060
jitter bot        0.236     0.236
mimic bot         0.640     0.640
casual human      0.651     0.651
rotation human    0.084     0.759
rotation bot      0.008     0.203
```

The first three rows match the table within sampling noise. The last three rows are the lesson.

### Break 1: the honest player your rule would ban

Look at the **rotation human**. This is a skilled player pressing abilities on a 1.5-second **global cooldown** (GCD), the shared lockout many MMOs apply after most abilities. They press the next key a moment after the cooldown ends, usually within a few hundred milliseconds. Their raw CV is 0.084, lower than the jitter bot's and far below the 0.35 rule. Every good player in your game who plays a cooldown-gated class would be flagged.

The cause is simple once you see it. The cooldown contributes a fixed 1,500 ms to every gap, which inflates `μ` while adding nothing to `σ`. CV shrinks. The game design, not the player, made the gaps regular.

The fix is to measure only what the player controls. Define the **slack** of each action as the gap minus the cooldown that gated it:

```
slack_i = g_i − cooldown_i
```

Slack is the reaction delay after the action became available. The rotation human's slack CV is 0.759 in this sample, back in the human range. The model predicts `√(e^0.49 − 1) = 0.795` for a log-normal of shape 0.7. The gap is sampling noise from 200 intervals. Other seeds scatter around 0.795. The rotation bot, which reacts 60 ± 20 ms after every cooldown, has slack CV 0.203, still clearly a bot. To compute slack the server must log which cooldown gated each action, which is a telemetry decision (DB201 week 10) someone has to make before launch.

This break generalizes. Any feature that looks at raw behavior will absorb the structure of your own game design: cooldowns, cast times, fixed respawn timers, movement speed caps. Before you trust a feature, list the design rules that could make an honest player look regular on it.

### Break 2: the bot that copies the histogram

Now look at the **mimic bot**. Its author read the same papers you did and drew its delays from a log-normal with the human shape. Its CV is 0.640, indistinguishable from the casual human's 0.651. The whole timing feature is gone, and it cost the bot author about one line of code.

This is the pattern you should expect. A feature that describes *how* the bot acts can be copied cheaply, because the bot author controls how it acts. Open the interactive and set the bot type to "mimic". The left panel, the interval histogram, shows two curves you can no longer tell apart.

### The second view: when the account is active

The right panel of the interactive shows a different picture of the same accounts. Each row is one day, each cell one hour, and a filled cell means the account did something in that hour. The casual human has a few blocks of two to four hours, at different times on different days. The mimic bot fills about 22 hours of every day.

Why doesn't the mimic bot also copy human hours? Because hours are its income. The NCSOFT study of Lineage, Aion and Blade & Soul makes this concrete. In its activity statistics, most accounts that were blocked as bots played more than 8,000 minutes (about 130 hours) in a week of 168. A large share of the accounts that were not blocked played under 5,000 minutes (about 80 hours). The authors also ran the operator's arithmetic for Lineage. At the time, a subscription cost US$25 a month, worth about 6 million gold, and no bot in their data earned more than about 50,000 gold per hour. So a bot had to run at least 120 hours a month just to pay for its own account.

That is the difference between the two views. The bot author can reshape the timing histogram for free. Reshaping the activity calendar means earning less. A bot that plays four hours a day like a person earns less than a fifth of what it earns playing 22, while its account, its IP address and its ban risk cost the same. Week 6's profit model and MMO304 week 11's farmer cost both say the same thing: some bot operators will accept the cut, but many will not, and each one that does is producing far less gold.

### Cross-game recognition

The same idea, "measure the regularity or the volume the bot needs, not a signature of its code," appears across games and data sources.

**Ragnarok Online (study published 2006, extended 2009).** Chen and colleagues used network traffic only: the timing of client commands, how bursty the traffic was across several time scales, and how the client reacted to changes in network conditions. A human reacts to lag. A bot's schedule often doesn't. This is timing CV measured on packets instead of game events.

**World of Warcraft (study published 2009).** Gianvecchio and colleagues proposed **human observational proofs**. Instead of a CAPTCHA, which interrupts play, the system passively watches keyboard and mouse input for actions that were hard for the bots of the day to perform in a human-like way, and classifies them with a neural network. Same idea as slack CV, measured one layer closer to the player's hands. It needs client-side input capture, which raises privacy questions server logs do not.

**Lineage, Aion and Blade & Soul (NCSOFT data, ground truth built December 2013 to March 2015, published 2016).** Lee and colleagues grouped each account's logs into time windows, turned each window into a vector of activity counts, and measured how similar the windows were to each other with cosine similarity. They call it **self-similarity**. A bot repeats the same routine, so its windows point the same way. Section 3 builds this feature.

**RuneScape (the ClusterFlutterer update, 25 October 2011).** Jagex's update targeted injection and reflection bots, the kinds that read the client's memory, which Jagex believed made up 98% of the bots in the game. The RuneScape Wiki notes that colour bots, which play through the official client by reading the screen, are a different family. Client integrity can remove whole bot families in a day ([week 5](w05-memory-editing-and-client-integrity.md) covers the timing and [week 6](w06-botting-economics.md) the operators' costs). The bots it cannot see still have to farm, and their farming is what behavioral features catch.

Four games, four data sources (packets, input devices, game logs, client code), one principle. Look for the thing the bot has to do to earn its keep.

### Eyes-open design judgment

- **Prefer features the operator pays to fake.** Hours played, output per hour, repetition across days and trade flows to a few collector accounts all cost the operator income or organization to disguise. Timing histograms and path wobble cost a line of code. Use the cheap features, since many bots never bother, but don't build your system on them.
- **Normalize away your own design.** Slack CV exists because cooldowns exist. Every time the game adds a mechanic that imposes rhythm (auto-attack timers, fishing bite windows, crafting queues), audit the features that might now misfire.
- **Some honest players look like bots on any single feature.** Heavy players, players who use accessibility tools or permitted macros, and players who repeat one activity for hours all exist. Combine features, require agreement, and send the borderline cases to people (week 8).
- **Keep the feature list private.** Publishing "we ban accounts with CV below 0.35" tells every bot author exactly what to change. Publish the rule ("automation is not allowed") and the outcome (ban counts), never the features.
- **Collect only what the feature needs.** Hourly counts of actions are enough for self-similarity. Raw mouse traces are far more sensitive and rarely needed on the server. DB201 week 13 covers retention and consent.

### Check yourself (worked example)

1. A bot waits 800 ms plus uniform jitter of ±200 ms. What CV do you predict? Does it pass a CV < 0.35 rule?
2. A player's gaps are all 2,000 ms cooldowns plus a reaction that is log-normal with median 200 ms and shape 0.5. Estimate the raw CV and the slack CV. Which one should a detector use?
3. A bot author makes the bot sleep 8 hours every night to look human. Using the Lineage numbers above, how much does that cut the bot's daily output, compared with 22 hours a day?

<details>
<summary>Answers</summary>

1. `200 / (800 × 1.732) = 0.144`. It is flagged.
2. Slack CV is `√(e^0.25 − 1) = √0.284 = 0.533`. The slack mean is `200 × e^0.125 ≈ 227` ms and its standard deviation about `0.533 × 227 ≈ 121` ms. The raw mean is about `2,227` ms, so raw CV is about `121 / 2,227 = 0.054`. Use slack CV; the raw one would flag an honest player.
3. It runs 16 hours instead of 22, so it earns `16 / 22 = 73%` as much, a 27% cut. At 50,000 gold per hour that is 300,000 gold a day less. The account still costs the same.

</details>

## 3. Repetition: self-similarity with cosine

Timing tells you about single actions. Repetition tells you about the routine. The NCSOFT feature is simple enough to compute by hand.

### Activity vectors

Split an account's play into windows, say one per active hour. For each window count a fixed list of actions, for example `[kills, loots, moves, chats, trades, crafts]`. A combat hour might be `[62, 60, 118, 0, 0, 0]`. A social hour might be `[6, 4, 30, 45, 3, 0]`.

### Cosine similarity

Two windows are similar if their vectors point in the same direction, whatever their length. The **cosine similarity** of vectors `a` and `b` is

```
cos(a, b) = (a · b) / (|a| × |b|)
```

where `a · b` is the sum of the products of matching entries and `|a|` is the square root of the sum of squares. For non-negative counts it runs from 0 (nothing in common) to 1 (same proportions). Doubling every count in a window leaves the cosine unchanged, so a fast bot and a slow bot doing the same routine both score near 1.

**Self-similarity** is the mean cosine over every pair of an account's windows.

```python
import math
from itertools import combinations

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

def self_similarity(windows):
    """Mean cosine similarity over every pair of activity windows."""
    pairs = list(combinations(windows, 2))
    return sum(cosine(a, b) for a, b in pairs) / len(pairs)

# One vector per hour of play: [kills, loots, moves, chats, trades, crafts]
bot = [[62, 60, 118, 0, 0, 0], [59, 57, 121, 0, 0, 0],
       [61, 61, 117, 0, 0, 0], [60, 58, 120, 0, 0, 0]]
human = [[40, 31, 95, 12, 1, 0], [6, 4, 30, 45, 3, 0],
         [0, 0, 12, 5, 9, 40], [35, 30, 88, 2, 0, 0]]

print(f"bot   self-similarity {self_similarity(bot):.4f}")
print(f"human self-similarity {self_similarity(human):.4f}")
print(f"human hours 1 and 4   {cosine(human[0], human[3]):.4f}")
```

Output:

```
bot   self-similarity 0.9996
human self-similarity 0.4939
human hours 1 and 4   0.9955
```

The last line matters. The human's two combat hours are as similar as the bot's hours. Any single window, or any pair, can look robotic. The separation appears only across many windows, where the human drifts between combat, chat and crafting and the bot never leaves its loop. That is why the feature needs days of data, and why the NCSOFT authors reported that it could not catch bots that played only briefly. In one incident they described, a large group of bots on a single server played under 10 hours a week on average, while typical bots in the same week played about 160.

### The honest repeater

Some people really do repeat one thing for hours: fishing, crafting a long queue, standing at a market. On self-similarity alone they look like bots. Lab 7 includes a small group of such players on purpose. The way out is the same as in section 2. Combine features, so that a repetitive routine alone is not enough, and ask what else a bot must do. A fisher plays three hours and logs off. A fishing bot plays twenty.

## 4. A feature catalog, ranked by cost to fake

Here is a working catalog. The last column is the one to argue about.

| Family | Example features | Data needed | Cost for the operator to fake |
|---|---|---|---|
| Timing | Slack CV, share of reactions under 150 ms, reaction to lag spikes | Action events with cooldown IDs | Low. A random delay from a human-shaped distribution. |
| Movement | Path repetition, straight-line segments, stops at identical coordinates | Position samples | Low to medium. Noise on waypoints; varied routes cost some efficiency. |
| Sessions | Active hours per day, longest session, days without a gap | Login and activity times | High. Every hour removed is income lost. |
| Output | Gold, experience or drops per hour relative to zone norms | Economy events | High. Earning less per hour is the point of the disguise. |
| Repetition | Self-similarity across windows and days | Hourly action counts | Medium to high. Varying activities means time off the profitable loop. |
| Economy graph | Trades flowing to a few collector accounts, new accounts sending everything onward | Trade and mail logs | High. The gold has to reach a seller eventually. |
| Social | Chat, grouping, friends, response to being spoken to | Chat metadata, group events | Medium. Scripted replies are cheap; real conversation is not. |

The NCSOFT paper points at the economy-graph row as a complement for the short-playing bots it missed. Those bots traded in a star shape, many accounts sending to one hub. [Week 10](w10-gold-sellers-and-rmt-networks.md) builds that feature for gold-seller networks.

Notice the pattern down the last column. Features about the bot's **manner** (timing, movement, chat style) are cheap to fake. Features about its **purpose** (hours, output, where the gold goes) are expensive, because faking them means not doing the job. A durable detection system leans on purpose features and uses manner features as cheap early warnings.

## 5. From features to a decision

A single feature with a threshold is a **rule**: "flag if slack CV < 0.35." Rules are transparent, easy to explain in an appeal, and easy for a bot author to learn by trial. Combine several and you get a rule set:

```
flag if  slack_cv < 0.35
     or  hours_per_day > 18
     or  (self_similarity > 0.97 and hours_per_day > 5)
```

Read the third line carefully. It encodes the judgment from section 3. High repetition is suspicious only when the account also plays long enough for repetition to be a business. This is the kind of rule you will write in Lab 7.

Hand-written rules stop scaling around a dozen features, and they give you no principled way to choose the thresholds. Next week replaces the hand-picked thresholds with a model trained on labelled accounts and, more important, shows how to measure what any detector really costs you in false accusations. Keep one fact in mind until then. Everything in this lecture was measured on a mix of bots and humans chosen by the author. In your live game, most accounts are human. That changes what "95% accurate" means.

## In-class activity (25 minutes)

Work in groups of three. Your game has three activities with built-in rhythm: melee auto-attack every 2.0 s, a fishing minigame where a bite appears after a random 5 to 15 s wait, and a crafting queue that finishes one item every 4 s without input.

1. For each activity, predict what a raw timing CV would look like for an honest player and explain why. (5 minutes)
2. Design the slack transform for each activity. What must the server log for it to work? (10 minutes)
3. Pick one feature from the section 4 catalog that a fishing bot could not fake without losing income. Write its definition in one sentence precise enough to code. (5 minutes)
4. Swap with another group. Name one honest player your partners' fishing feature would flag. (5 minutes)

Expected output: a three-row table (activity, raw CV prediction, slack definition and log fields), one feature definition, and the counterexample your partners found.

## Common misconceptions

- **"Bots are regular, humans are random."** Humans are regular whenever the game design makes them so, as the rotation human shows. Measure the part of the behavior the player controls.
- **"Once we find the bot's timing signature, we're done."** Timing is the cheapest feature to fake. Expect it to stop working the first time a bot author reads your ban notice or your conference talk.
- **"Client anti-cheat makes behavioral detection unnecessary."** Colour bots and headless bots are invisible or nearly invisible to the client. The server sees everyone.
- **"High playtime proves botting."** It is strong evidence, not proof. Some people play very long hours, and some accounts are shared. Use playtime together with output, repetition and economy features, and let people review the edge cases.

## Check yourself

1. A bot author changes their bot's delay from uniform `1,000 ± 400` ms to log-normal with median 1,000 ms and shape 0.6. By how much does its CV change, and which of your features still catch it?
2. Two hourly windows are `[30, 30, 60, 0, 0, 0]` and `[0, 0, 20, 40, 0, 0]`. Compute their cosine similarity.
3. Your game adds a new zone where every enemy respawns exactly 10 s after death. Which features in the section 4 catalog might start flagging honest players there, and how would you adjust them?
4. A designer proposes publishing the list of detection features "for transparency." Give one argument for and one against, then state what you would publish instead.

<details>
<summary>Answers</summary>

1. From `400 / 1,732 = 0.231` to `√(e^0.36 − 1) = 0.658`, into the human range. Timing features stop working. Hours per day, output per hour, self-similarity over days and the economy graph still apply, because the bot still farms the same loop for the same hours.
2. `a · b = 0 + 0 + 1,200 + 0 = 1,200`. `|a| = √(900 + 900 + 3,600) = √5,400 ≈ 73.5`. `|b| = √(400 + 1,600) = √2,000 ≈ 44.7`. Cosine `≈ 1,200 / 3,286 ≈ 0.365`.
3. Timing features on kill events (every kill waits on the same respawn), movement repetition (players stand at the spawn points) and output per hour (efficient honest players converge on the same rate). Measure slack from the respawn event, compare output with the zone's own norms instead of global ones, and weight session and economy features more there.
4. For: players can check that bans are not arbitrary, and appeals are easier to argue. Against: bot authors tune their bots to the list, so the features stop working and more bots stay. Publish the rules of conduct, the review and appeal process, and aggregate ban numbers.

</details>

## Lab / assignment hook

[Lab 07, behavioral features](../labs/lab07.md). You implement slack CV, active hours per day and self-similarity on 150 synthetic accounts, including rotation players and honest repeaters designed to trip naive rules, then write a rule that reaches the lab's precision and recall targets and a short memo ranking your features by cost to fake.

## Sources

- Chen, K.-T., Jiang, J.-W., Huang, P., Chu, H.-H., Lei, C.-L. & Chen, W.-C. (2006). "Identifying MMORPG Bots: A Traffic Analysis Approach." *Proceedings of ACE 2006*, ACM. doi:10.1145/1178823.1178829. Extended version in *EURASIP Journal on Advances in Signal Processing* (2009), article 797159, doi:10.1155/2009/797159. Ragnarok Online; bot and human traffic differ in the regularity of command release times, burstiness at several time scales, and sensitivity to network conditions; the conservative scheme made no false accusations on the authors' data sets.
- Gianvecchio, S., Wu, Z., Xie, M. & Wang, H. (2009). "Battle of Botcraft: Fighting Bots in Online Games with Human Observational Proofs." *Proceedings of the 16th ACM Conference on Computer and Communications Security (CCS 2009)*, 9 November 2009, pp. 256-268. doi:10.1145/1653662.1653694. From the abstract (read via OpenAlex, September 2026): user-input traces collected in World of Warcraft; HOPs passively monitor input actions that are hard for current bots to perform in a human-like way; a cascade-correlation neural network separates bots from humans.
- Lee, E., Woo, J., Kim, H., Mohaisen, A. & Kim, H. K. (2016). "You Are a Game Bot!: Uncovering Game Bots in MMORPGs via Self-similarity in the Wild." *NDSS 2016*. Lineage, Aion and Blade & Soul; ground truth built by game masters from December 2013 to March 2015; most blocked accounts above 8,000 minutes (about 130 hours) of play per week, a significant number of unblocked accounts below 5,000 minutes; self-similarity from cosine similarity of windowed log vectors; Lineage subscription US$25 per month, about 6 million gold; bots earning under 50,000 gold per hour; at least 120 hours per month to profit; the incident of bots playing under 10 hours per week against a typical 160; star-shaped trade networks among short-playing bots.
- RuneScape Wiki, "Bot Nuke Day" (ClusterFlutterer, 25 October 2011). Targeted injection and reflection bots, which Jagex believed were 98% of bots; Jagex's statement that over 1.5 million bots had recently been banned; description of colour bots running through the official client.
- Hoglund, G. & McGraw, G. (2007). *Exploiting Online Games: Cheating Massively Distributed Systems*. Addison-Wesley.
- All distribution parameters in section 2 (delays, jitter, log-normal shapes, the 1.5 s cooldown) and the activity vectors in section 3 are invented for teaching. They do not describe any specific bot or game.

## Interactive spec: examples/w07-click-timing.html

**The one insight:** a bot can make its timing histogram look human for free, but it cannot make its activity calendar look human without earning less. Two linked views of the same accounts show this: the left view converges as mimicry rises, the right view does not.

**Layout.** Two panels side by side on desktop, stacked on mobile (histogram first).

- **Left panel, "How it clicks."** Overlaid histograms of action intervals (ms, x-axis 0 to 3,000 in 50 ms bins, y-axis share of intervals) for one human (fixed, neutral colour) and one bot (accent colour). 400 intervals each, regenerated from a seeded PRNG (mulberry32, seed 7) when controls change. Under the chart, for each account: mean, standard deviation, raw CV, slack CV, each to three decimals.
- **Right panel, "When it plays."** Two 7 × 24 grids (rows days, columns hours), one per account, cells filled when active. Under each: active hours per day to one decimal, and self-similarity (mean pairwise cosine of that account's hourly activity vectors, first 40 windows) to three decimals.
- **Verdict strip** across the bottom: three rule chips, each showing whether it flags the bot and whether it flags the human. Rule A: raw CV < 0.35. Rule B: slack CV < 0.35. Rule C: hours per day > 18, or self-similarity > 0.97 with hours per day > 5.

**Controls.**
- Bot type (segmented control): Naive (uniform `1000 ± j`), Mimic (log-normal, median 900 ms, shape `s_bot`), Rotation bot (cooldown 1,500 ms plus `60 ± 20` ms).
- Jitter `j` slider, 0 to 500 ms, step 10, default 100 (Naive only).
- Bot shape `s_bot` slider, 0.1 to 1.0, step 0.05, default 0.6 (Mimic only).
- Human type toggle: Casual (log-normal median 900 ms, shape 0.6, no cooldown) or Rotation human (1,500 ms cooldown plus log-normal median 150 ms, shape 0.7).
- Bot hours per day slider, 4 to 23, default 22. Human hours per day fixed at a random 1 to 5 per day (seeded), blocks placed at seeded random start hours.
- "Reseed" button.

**Activity vectors for self-similarity.** Bot: every active hour is `[55, 50, 110, 3, 0, 0]` with each entry multiplied by a uniform 0.95 to 1.05. Human: each active hour picks one of five modes (combat `[55, 50, 110, 3, 0, 0]`, social `[2, 1, 25, 45, 2, 0]`, crafting `[0, 0, 15, 4, 3, 40]`, trading `[0, 0, 20, 10, 25, 2]`, questing `[25, 20, 160, 5, 1, 1]`), each entry multiplied by uniform 0.4 to 1.6 plus uniform 0 to 4, rounded.

**Formulas.** CV `= pstdev / mean`. Slack `= gap − cooldown` (cooldown 0 when none). Cosine `= a·b / (|a||b|)`, 0 if either is all zeros. Predicted CV shown as a small grey label next to the bot's measured CV: Naive `j / (1000√3)`, Mimic `√(e^(s²) − 1)`.

**Test values (for the builder to verify, tolerance ±0.02 on measured values).** Naive with `j = 100`: predicted 0.058. Naive with `j = 400`: predicted 0.231. Mimic with `s = 0.6`: predicted 0.658; Rule A and Rule B both clear the bot, Rule C flags it at 22 hours and clears it at 4 hours, because `hours > 5` fails there. Rotation human: raw CV about 0.08 (Rule A flags the human, shown as a red "false positive" chip), slack CV about 0.80, the model value `√(e^0.49 − 1) = 0.795` (Rule B clears). The lecture's 0.759 is one sample from its own seed and is not a test value.

**First screen.** Mimic bot, `s = 0.6`, 22 hours; casual human. The histograms overlap almost completely while the right panel shows one nearly full grid and one sparse grid.
