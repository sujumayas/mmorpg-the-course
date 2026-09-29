# MMO309 · Week 08 — Machine Learning for Detection (Overview)

**Why this matters:** A detector that is "99% accurate" can still accuse more innocent players than it catches bots. Whether it does depends on a number the model never sees, the share of your players who are bots. This week you learn what a trained detector is, how to read its errors in the population you actually run, and how to turn its scores into bans, reviews and silence without hurting the players you exist to protect.

**You will be able to:**
- Compute precision from recall, false positive rate and prevalence, and predict how precision changes after a ban wave.
- Explain a logistic-regression detector as a weighted sum of features, and read what its weights say.
- Choose a decision threshold from the costs of false bans and missed bots, and design a three-band triage (act, review, ignore) under a review budget.
- Critique a detection pipeline for label bias, drift and adversarial adaptation.

**Before class:** Lee et al., "You Are a Game Bot!" (NDSS 2016), sections IV and V, on ground truth and evaluation (about 20 minutes). The session description of John McDonald's GDC 2018 talk "Robocalypse Now: Using Deep Learning to Combat Cheating in Counter-Strike: Global Offensive" (GDC Vault, free abstract). Reread [MA102 week 14, section 3](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) on false positives and false negatives.

**Prerequisites from earlier courses:** [MA102 week 14, hypothesis testing](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (false positive and false negative rates). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (why a small labelled set gives shaky rates). [MMO402 week 7, justice systems](../../MMO402-emergent-society-governance-and-ethics/lectures/w07-justice-systems-reports-reviews-appeals.md) (review panels and appeals, where this week's flagged accounts go next). From this course, [week 5, section 4](w05-memory-editing-and-client-integrity.md) (precision for client-side signals) and [week 7, behavioral features](w07-bot-detection-behavioral-features.md).

**Interactive:** [Base rate and threshold](../examples/w08-base-rate-threshold.html). Use it during sections 2 and 3.

---

## 1. What a trained detector is

Last week you wrote rules by hand: "flag if slack CV < 0.35 or hours per day > 18." Machine learning replaces the hand-picked thresholds with numbers fitted to examples. The vocabulary is small.

- A **label** is the answer for one account: bot (1) or human (0). Labels come from people, usually game masters or support staff who reviewed the account.
- A **feature vector** is the list of numbers you computed for that account, such as `[slack_cv, hours_per_day]`.
- A **model** is a function from a feature vector to a **score**, a number where higher means "more bot-like."
- **Training** is choosing the model's parameters so that its scores agree with the labels as well as possible.
- A **threshold** turns a score into a decision. Flag if score ≥ `t`.

The threshold is not part of the model. The model ranks accounts. You decide where to cut the ranking. Most of this lecture is about that decision, because that is where the harm or the value lands.

### The simplest useful model: logistic regression

The NCSOFT study from last week used **logistic regression**. It computes a weighted sum of the features plus an intercept, then squashes the sum into the range 0 to 1:

```
z = w₀ + w₁·x₁ + w₂·x₂ + ...
score = 1 / (1 + e^(−z))
```

The squashing function is the **sigmoid**. A large positive `z` gives a score near 1, a large negative `z` a score near 0, and `z = 0` gives exactly 0.5. Training nudges the weights repeatedly in the direction that reduces the gap between each score and its label. That procedure is **gradient descent**.

Here is the whole thing on the two features from week 7. Bots have low slack CV and long hours. In "month 2" the bot authors switch to human-shaped timing (the mimic bot), and the model trained on month 1 meets them.

```python
import math
import random

rng = random.Random(8)

def account(is_bot, mimic=False):
    """Two features from week 7: slack CV and active hours per day."""
    if is_bot:
        cv = rng.gauss(0.65, 0.10) if mimic else rng.gauss(0.25, 0.08)
        hours = rng.gauss(19, 3)
    else:
        cv = rng.gauss(0.70, 0.12)
        hours = min(rng.expovariate(1 / 3), 20)
    return [cv, hours / 10], int(is_bot)   # hours scaled to a similar range

def sample(n_bots, n_humans, mimic=False):
    return ([account(True, mimic) for _ in range(n_bots)] +
            [account(False) for _ in range(n_humans)])

def score(w, x):
    z = w[0] + w[1] * x[0] + w[2] * x[1]
    return 1 / (1 + math.exp(-z))

def train(data, epochs=400, rate=0.5):
    w = [0.0, 0.0, 0.0]
    for _ in range(epochs):
        grad = [0.0, 0.0, 0.0]
        for x, y in data:
            err = score(w, x) - y
            grad[0] += err
            grad[1] += err * x[0]
            grad[2] += err * x[1]
        w = [wi - rate * g / len(data) for wi, g in zip(w, grad)]
    return w

def evaluate(w, data, threshold=0.9):
    tp = sum(1 for x, y in data if y == 1 and score(w, x) >= threshold)
    fp = sum(1 for x, y in data if y == 0 and score(w, x) >= threshold)
    bots = sum(y for _, y in data)
    return tp / bots, fp, tp / max(tp + fp, 1)

w = train(sample(500, 500))
print("weights", [round(v, 2) for v in w])
for label, test in [("month 1, old bots", sample(200, 9800)),
                    ("month 2, mimic bots", sample(200, 9800, mimic=True))]:
    recall, fp, precision = evaluate(w, test)
    print(f"{label:20s} recall {recall:.1%}  humans flagged {fp:3d}  precision {precision:.1%}")

w2 = train(sample(500, 500, mimic=True))   # retrain on newly labelled month-2 bots
recall, fp, precision = evaluate(w2, sample(200, 9800, mimic=True))
print("retrained weights", [round(v, 2) for v in w2])
print(f"{'month 2, retrained':20s} recall {recall:.1%}  humans flagged {fp:3d}  precision {precision:.1%}")
```

Output:

```
weights [-2.72, -4.3, 4.34]
month 1, old bots    recall 92.5%  humans flagged  18  precision 91.1%
month 2, mimic bots  recall 63.5%  humans flagged  25  precision 83.6%
retrained weights [-3.76, -2.69, 5.08]
month 2, retrained   recall 89.0%  humans flagged  62  precision 74.2%
```

Read the weights. The slack-CV weight is negative (lower CV, more bot-like) and the hours weight is positive (more hours, more bot-like), which matches week 7. When the bots start mimicking human timing, **recall**, the share of bots caught, drops from 92.5% to 63.5%. Retraining on newly labelled mimic bots moves weight from timing onto hours and wins back recall. But look at the cost. The retrained model flags 62 humans instead of 18, because the feature it now leans on also describes heavy human players. Section 4 returns to this. First, the question every detector has to answer: when it flags someone, how often is it right?

## 2. Worked example: the base-rate trap

### The hook

Valve announced in February 2017 that it planned a machine-learning system for spotting cheaters in Counter-Strike: Global Offensive, and described it at GDC in March 2018 under the name VACNet. According to the talk's abstract, it worked from gameplay data without client-side instrumentation, was retrained regularly, and cut certain kinds of cheating by a factor of one hundred. Yet VACNet did not ban anyone by itself. It sent the accounts it suspected to **Overwatch**, Valve's system of experienced players who review replays and vote (MMO402 week 7).

Why put a slow human step behind a model that good? The answer is arithmetic, and it applies to every bot detector in every MMO.

### The model

Run a detector over a population of `N` accounts. A share `π` of them are bots. This share is the **prevalence** or **base rate**. The detector has two error rates, measured on labelled data:

- **Recall** (also called true positive rate), `R`: the share of bots it flags.
- **False positive rate**, `F`: the share of humans it flags.

Among the accounts it flags, the share that really are bots is the **precision**. You met it in [week 3, section 4](w03-speed-hacks-and-movement-validation.md) for movement violations and in [week 5, section 4](w05-memory-editing-and-client-integrity.md) for client-side cheat signals, both written as counts. Divide those counts by `N` and you get the form below. This week the focus moves to the one term the detector does not control:

```
flagged bots   = R × π × N
flagged humans = F × (1 − π) × N

precision = R·π / (R·π + F·(1 − π))
```

Every symbol except `π` describes the detector. `π` describes your game on the day you run it. Precision depends on both.

### Numbers you can check

One million active accounts. The code computes the four rows, and you can reproduce each by hand from the formula.

```python
def outcomes(n, prevalence, recall, fpr):
    bots = n * prevalence
    humans = n - bots
    tp = recall * bots
    fp = fpr * humans
    return tp, fp, tp / (tp + fp)

print(f"{'prevalence':>10s} {'recall':>6s} {'FPR':>6s} {'bots caught':>11s} {'humans hit':>10s} {'precision':>9s}")
for prevalence, recall, fpr in [(0.02, 0.95, 0.01), (0.02, 0.95, 0.001),
                                (0.002, 0.95, 0.001), (0.2, 0.95, 0.01)]:
    tp, fp, precision = outcomes(1_000_000, prevalence, recall, fpr)
    print(f"{prevalence:10.1%} {recall:6.0%} {fpr:6.1%} {tp:11,.0f} {fp:10,.0f} {precision:9.1%}")
```

Output:

```
prevalence recall    FPR bots caught humans hit precision
      2.0%    95%   1.0%      19,000      9,800     66.0%
      2.0%    95%   0.1%      19,000        980     95.1%
      0.2%    95%   0.1%       1,900        998     65.6%
     20.0%    95%   1.0%     190,000      8,000     96.0%
```

Row 1 is the trap. The detector is right about 99% of humans and 95% of bots, and one in three accounts it flags belongs to an honest player. That is 9,800 people. The reason is that there are 49 humans for every bot, so a 1% error on the large group outweighs the 95% success on the small one.

Row 2 cuts the false positive rate tenfold and precision recovers to 95%. False positive rate is the lever that matters when bots are rare.

Row 3 is the one that surprises teams in production. The same detector as row 2, after a successful ban wave has cut prevalence from 2% to 0.2%. Nothing about the model changed. Its precision fell from 95% back to 66%, because there are now ten times fewer bots to find and just as many humans to misjudge. **Success at removing bots makes the same detector worse at being right.**

Row 4 shows the opposite. On a fresh server swarmed by bots, even the sloppy row-1 detector is 96% precise. This is how a team tunes a detector during a bot surge, sees excellent precision, and ships a threshold that becomes harmful a month later.

Open the interactive. The left view shows the two score distributions and a threshold line, the way a model developer sees them. The right view shows 1,000 accounts as dots, coloured by what the threshold did to them. Drag the prevalence slider from 20% down to 0.5% without touching the threshold. The left view barely changes. In the right view the red dots, innocent players flagged, grow from a sprinkle to a majority of everything flagged.

### Cross-game recognition

The base rate shapes every published detection system. Rewrite each one in terms of `R`, `F` and `π`.

**Counter-Strike: Global Offensive, VACNet (announced 2017, GDC talk 2018).** The model's output is not the verdict. It chooses which cases humans review. In the formula's terms, the model raises `π` for the reviewers. Among all players, cheaters are rare. Among cases VACNet sends to Overwatch, they are common, so the reviewers' own error rate costs far less. MMO402 week 7 models the review panel itself.

**Lineage, Aion and Blade & Soul (NCSOFT, published 2016).** The NDSS paper reports **AUC** for its logistic-regression model. AUC, the area under the ROC curve, is the probability that a randomly chosen bot scores higher than a randomly chosen human. Its final models reached 0.9455 for Lineage, 0.9942 for Aion and 0.9399 for Blade & Soul. Notice what AUC does not contain: `π`. It summarizes ranking quality and says nothing about precision in the live population. The authors also rebuilt the model as new bot behavior appeared, which section 4 explains.

**Ragnarok Online (published 2006).** Chen and colleagues offered two ways to combine their traffic features. The conservative scheme made no false accusations on their data. The progressive scheme caught bots more aggressively. That is the threshold trade-off before anyone called it that, offered as a choice to the operator rather than hidden inside the model.

**Outside games: medical screening.** A screening test with 99% specificity for a rare condition produces mostly false alarms, which is why screening results lead to a second, more careful test, not straight to treatment. A detection score leading to human review follows the same structure for the same reason.

### Eyes-open design judgment

- **Report precision at today's prevalence, not accuracy.** Accuracy, the share of all accounts classified correctly, is 99% in row 1 and hides 9,800 wrongful flags. Ask for recall, false positive rate and an estimate of `π`, then compute precision.
- **Re-estimate prevalence after every ban wave.** Sample a few hundred accounts at random and have them reviewed. It is the only way to know `π`, and `π` moves exactly when you succeed.
- **Let the model rank and people decide, unless precision is very high.** Automatic action is defensible only in a score band where measured precision is near 1, and even then with an appeal path.
- **Beware of flattering test sets.** A test set with half bots and half humans makes every detector look precise. That is how the month-1 numbers in section 1 were measured, and why they are optimistic.

### Check yourself (worked example)

1. A detector has recall 90% and false positive rate 0.5%. What is its precision at a prevalence of 1%? At 10%?
2. What false positive rate would the detector in question 1 need to reach 95% precision at 1% prevalence?
3. After a ban wave, reviewers report that more flagged accounts than before turn out to be human. Nothing in the model changed. Give the most likely explanation in one sentence.

<details>
<summary>Answers</summary>

1. At 1%: `0.009 / (0.009 + 0.005 × 0.99) = 0.009 / 0.01395 = 64.5%`. At 10%: `0.09 / (0.09 + 0.0045) = 95.2%`.
2. Solve `0.009 / (0.009 + F × 0.99) = 0.95`. Then `F × 0.99 = 0.009 × (1/0.95 − 1) = 0.000474`, so `F ≈ 0.048%`, about one human in 2,100.
3. The ban wave cut prevalence, so the same false positive rate now produces a larger share of the flags.

</details>

## 3. Choosing the threshold

Every threshold trades false positives against false negatives. The right trade depends on what each error costs you.

### Costs

A **false positive** here is a wrongful sanction. It costs a support ticket and an appeal review, often a paying player who leaves, and some trust from everyone who hears about it. A **false negative** is a bot that keeps farming until the next pass. It costs the gold it adds to the economy (MMO304 week 11), the resources it takes from players, and the time it keeps its operator in business. Call the costs `C_FP` and `C_FN`. Only their ratio matters for choosing the threshold.

For a detector whose bot and human scores are normal distributions with the same spread, separated by `d` standard deviations, the cost-minimizing threshold has a closed form. You flag where the evidence ratio exceeds `(C_FP / C_FN) × (1 − π) / π`. The code computes it at 2% prevalence with `d = 3`, a strong detector (AUC about 0.98).

```python
import math

def phi(z):                       # standard normal CDF
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))

d = 3.0                           # separation between human and bot score means
prevalence = 0.02
for c_fp, c_fn in [(10, 10), (200, 10), (1000, 10)]:
    ratio = (c_fp / c_fn) * (1 - prevalence) / prevalence
    t = (math.log(ratio) + d * d / 2) / d
    fpr, tpr = 1 - phi(t), 1 - phi(t - d)
    precision = tpr * prevalence / (tpr * prevalence + fpr * (1 - prevalence))
    print(f"C_FP/C_FN {c_fp/c_fn:5.0f}  threshold {t:.2f}  recall {tpr:.1%}  "
          f"FPR {fpr:.4%}  precision {precision:.1%}")
```

Output:

```
C_FP/C_FN     1  threshold 2.80  recall 58.0%  FPR 0.2577%  precision 82.1%
C_FP/C_FN    20  threshold 3.80  recall 21.3%  FPR 0.0074%  precision 98.3%
C_FP/C_FN   100  threshold 4.33  recall 9.1%  FPR 0.0007%  precision 99.6%
```

If a wrongful ban costs 20 times a missed bot, which is a modest guess for a subscription game, the best automatic threshold catches only about a fifth of the bots. That is not a failure of the model. It is the correct answer to "which accounts is it worth punishing without a second look?" [Week 12](w12-legal-and-ethical-considerations.md) rewrites this rule for one player as `P(cheat) ≥ C / (C + 1)` and gives each rung of the sanction ladder its own cost ratio `C`.

### Three bands

The way out is to stop treating the decision as binary. Split the score range into three bands:

| Band | Action | Chosen so that |
|---|---|---|
| Above `t_act` | Automatic action (suspend, flag for the next ban wave) | Measured precision in this band is near 1 |
| From `t_review` up to `t_act` | Human review queue | The number of accounts fits the reviewers' daily capacity |
| Below `t_review` | No action; keep watching | Everything else |

The review band is where most bots are caught in practice. Its lower edge is set by capacity, not by the model. If your team can review 400 accounts a day, `t_review` is the score at which the band holds 400 accounts. Lab 8 asks you to compute exactly that on a 20,000-account validation set. There, the threshold for 99% precision catches only 12.5% of bots automatically, and a 400-case review band adds 276 more bots out of 536, more than half the total.

### Timing is part of the decision

A flag does not have to mean an immediate ban. Many studios collect flagged accounts and ban them together in a **ban wave**. Delay has costs (the bot farms longer) and benefits (the bot author cannot tell which change got them caught, and reviewers get time). [Week 5](w05-memory-editing-and-client-integrity.md) models that choice as cheating sessions per signature cycle, and [week 6](w06-botting-economics.md) shows what the same delay is worth to a bot operator.

## 4. Drift, adversaries and labels

A detector is trained on the past and used on the future. Three things make the future different.

### Drift

**Concept drift** means the relationship between features and labels changes over time. In games it happens constantly: a patch changes cooldowns, a new zone changes gold per hour, an event doubles playtime for everyone. Any of these moves honest players across a threshold that used to be safe. The NCSOFT paper describes rebuilding its model as new bot behavior appeared. VACNet's abstract says the network is retrained regularly and picks up new cheating behavior within hours. Plan for retraining from the start, with labelled data flowing in continuously.

Test a detector the way you will use it. Train on older data and test on newer data. A random split mixes the future into the training set and hides drift.

### Adversaries

Drift in spam or fraud or bots is partly deliberate. The section 1 code shows the result. When bots changed their timing, the model's recall fell from 92.5% to 63.5%. Retraining restored recall to 89% by leaning on hours played. It also flagged 62 humans instead of 18, because hours played is a feature some humans share. Every round of the arms race pushes the model toward the features bots cannot abandon, and those are often the features heavy players share too. Week 7's "cost to fake" ranking predicts where the model will end up, and warns you who will pay for it.

There is a second lesson in the output. The model was trained on equal numbers of bots and humans and then used at 2% prevalence. Its scores therefore overstate the probability that an account is a bot. A score of 0.9 does not mean 90% likely. Either **calibrate** the scores against a sample at live prevalence, or choose thresholds from measured precision in the live population, as Lab 8 does.

### Labels

Your labels are someone's past decisions. That creates two problems.

- **Selection bias.** If labels come from past bans, the training set contains only the bots your old methods caught. The model learns to find more of the same and stays blind to the kinds you never caught. The NCSOFT team avoided this by having game masters observe randomly sampled accounts, with at least two reviewers per case and written reasons, which cost far more than reusing a ban list.
- **Feedback loops.** If you train on bans, and bans come from the model, the model's mistakes become next month's labels. Keep a random-sample audit that does not depend on the model.

## 5. What a model does not fix

**Explanations for appeals.** A player who is banned will ask why. A logistic regression can say which features pushed the score up. A deep network usually cannot say it as simply. Either way, you should not reveal the features themselves (week 7), so the explanation is about behavior ("sustained automated farming patterns over 14 days"), backed by a reviewer's judgment for anything in the review band.

**Fairness across groups.** If one group of honest players shares a feature with bots (players who use accessibility input tools, players in regions with high latency, players who share a family computer), the false positive rate for that group will be higher than the average. Measure `F` separately for groups you can identify, and treat a gap as a bug.

**Privacy.** More features usually means more data about people. The GDC abstract's point that VACNet needed no client-side instrumentation is also a privacy point. Server-side gameplay data is data the player already sends to play.

## In-class activity (25 minutes)

Pairs. Your MMO has 400,000 active accounts. A random audit last month estimated 3% bots. Your detector, measured on the audit sample, has recall 88% and false positive rate 0.4%. Your review team can clear 600 cases a day.

1. How many accounts does the detector flag per daily run, and what is its precision? (5 minutes)
2. The team wants to auto-suspend all flagged accounts. Write a two-sentence response with numbers. (5 minutes)
3. Suppose that among the 1,500 highest-scoring accounts per run, 1,470 were bots in the audit. Propose `t_act` and a review band that fits 600 cases a day. What share of flagged bots are handled automatically? (10 minutes)
4. A ban wave next week will cut prevalence to 1%. Recompute precision for the full flagged set. What should change in your process? (5 minutes)

Expected output: four short answers with numbers, and a one-line process change.

## Common misconceptions

- **"99% accuracy means 99% of flagged accounts are bots."** Accuracy mixes both groups. Precision depends on prevalence, and at low prevalence it can be far below accuracy.
- **"A better model removes the need for human review."** Better separation raises precision, but the base rate still punishes any remaining false positive rate. Review is the second test that makes a strong screen safe.
- **"Once trained, a detector keeps working."** Patches cause drift and bot authors adapt on purpose. Detection is an ongoing operation with a retraining schedule and a labelled data pipeline.
- **"Past bans are good training labels."** They teach the model your old blind spots. Random-sample audits are slower and more honest.

## Check yourself

1. A detector has recall 80% and false positive rate 0.2%. Prevalence is 5%. Out of 200,000 accounts, how many are flagged, and how many of those are human?
2. Explain in two sentences why AUC cannot tell you how many innocent players a detector will flag.
3. In the section 1 code, the retrained model flagged more humans. Name the feature responsible and one honest group likely to be over-represented among those 62.
4. A studio's detector was tuned during a bot surge at 25% prevalence, reaching 97% precision with false positive rate 1%. Six months later prevalence is 2% and recall is still 95%. What is the precision now?

<details>
<summary>Answers</summary>

1. Bots `= 10,000`, flagged `0.8 × 10,000 = 8,000`. Humans `= 190,000`, flagged `0.002 × 190,000 = 380`. 8,380 flagged, 380 human (precision 95.5%).
2. AUC measures how well the model ranks a random bot above a random human, and that probability does not depend on how many bots there are. The count of innocent players flagged depends on the threshold and on prevalence, and AUC contains neither.
3. Hours played per day. Heavy honest players, for example students on a break or players who idle logged in, will be over-represented.
4. `0.95 × 0.02 / (0.019 + 0.01 × 0.98) = 0.019 / 0.0288 = 66.0%`. One flag in three is now an honest player.

</details>

## Lab / assignment hook

[Lab 08, from scores to decisions](../labs/lab08.md). You implement the confusion matrix, precision and recall, a threshold search for a target precision, a cost function, precision under a new prevalence, and a review band under a capacity limit, all on a 20,000-account validation set. The deliverable includes a one-page detection policy with numbers.

## Sources

- Valve Anti-Cheat, Wikipedia (accessed September 2026). February 2017 announcement of plans for a machine-learning approach in CS:GO that marks players for review by Overwatch; March 2018 GDC talk naming it VACNet.
- McDonald, J. (2018). "Robocalypse Now: Using Deep Learning to Combat Cheating in 'Counter-Strike: Global Offensive'." GDC 2018, Programming track. GDC Vault session description (gdcvault.com/play/1024994). No client-side instrumentation; regular retraining picks up new cheating behavior within hours; certain types of cheats reduced by a factor of one hundred.
- Lee, E., Woo, J., Kim, H., Mohaisen, A. & Kim, H. K. (2016). "You Are a Game Bot!: Uncovering Game Bots in MMORPGs via Self-similarity in the Wild." *NDSS 2016*. Logistic regression; ground truth from game masters observing randomly selected accounts, at least two per case, December 2013 to March 2015; final AUC 0.9455 (Lineage), 0.9942 (Aion), 0.9399 (Blade & Soul); model maintenance with newly updated bot behaviors.
- Chen, K.-T. et al. (2006). "Identifying MMORPG Bots: A Traffic Analysis Approach." *ACE 2006*, ACM. doi:10.1145/1178823.1178829. Conservative scheme with no false accusations on the authors' data; progressive scheme more aggressive.
- All prevalences, error rates, costs, feature distributions and team sizes in sections 1 to 3, the in-class activity and the questions are invented for teaching. They do not describe the performance of VACNet, NCSOFT's models or any other real system.

## Interactive spec: examples/w08-base-rate-threshold.html

**The one insight:** the same detector and the same threshold give very different precision at different prevalence. The model developer's view (two score curves) hides this; the population view (dots) shows it.

**Layout.** Two panels side by side on desktop, stacked on mobile.

- **Left panel, "What the model sees."** Two normal density curves on a score axis from −4 to 7: humans `N(0, 1)` and bots `N(d, 1)`. Each curve is normalized to its own area (so prevalence does not change their heights). A draggable vertical threshold line `t`. Shade the area of the human curve right of `t` (false positive rate, red) and of the bot curve right of `t` (recall, accent). Readouts: recall `1 − Φ(t − d)`, FPR `1 − Φ(t)`, AUC `Φ(d / √2)`, each to 3 decimals (FPR to 4).
- **Right panel, "Who gets flagged."** 1,000 dots in a 40 × 25 grid. The number of bot dots is `round(1000 × π)`, placed at seeded random positions (mulberry32, seed 8). Each dot is coloured by outcome: bot flagged (accent, filled), bot missed (accent, hollow), human flagged (red, filled), human not flagged (neutral, small). Use expected counts, not random draws: flagged bots `= round(R × bots)`, flagged humans `= round(F × humans)`, with the flagged ones chosen deterministically from the seeded order. Readouts under the grid: flagged total, of which human, precision to 1 decimal percent, computed with the exact formula (not the rounded dot counts).
- **Three-band strip** (collapsed by default, "Show triage"): adds a second draggable line `t_review < t`, shades the review band amber in both panels, and shows accounts per day in the band for `N` accounts (input, default 1,000,000) against a capacity input (default 400).

**Controls.** Prevalence `π` slider, log scale from 0.1% to 30%, default 2%. Separation `d` slider 1.0 to 4.5, step 0.1, default 3.0. Threshold `t` (drag or slider) −1 to 6, step 0.01, default 2.33. Presets: "Surge server" (π 20%), "Normal" (2%), "After ban wave" (0.2%).

**Formulas.** `Φ` via an erf approximation (Abramowitz and Stegun 7.1.26 is accurate enough). Precision `= Rπ / (Rπ + F(1 − π))`.

**Test values.** `d = 3.0`, `t = 2.33`: FPR 0.0099, recall 0.749. At π = 2%: precision `0.749 × 0.02 / (0.01498 + 0.0099 × 0.98) = 60.7%`. At π = 20%: 95.0%. At π = 0.2%: 13.2%. `d = 3.0` gives AUC 0.983; `d = 2.2` gives AUC 0.940.

**First screen.** π = 2%, d = 3.0, t = 2.33. Then the prevalence preset buttons invite the student to watch the red dots grow while the left panel stays the same.
