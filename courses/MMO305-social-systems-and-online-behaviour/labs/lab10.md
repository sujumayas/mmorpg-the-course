# MMO305 · Lab 10: Chat channel load and design

**Week:** 10 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the field observation assessment (30%)

## Objective

Measure a real public channel, check the channel-load model from [week 10](../lectures/w10-communication-design-chat-emotes-pings.md) against a simulation, see what spammers and a rate limit do to everyone else's audience, and then design the channel set for a small MMO with numbers attached.

## Starter materials

- A game you play that has a public text channel (a city, zone, trade or global channel). Any MMO works. If you have no access, use a public Twitch chat or a busy public Discord channel and say so in your memo.
- A stopwatch and a spreadsheet for step 1.
- Python 3 with numpy and matplotlib (the program's reference stack).
- The formulas from week 10, section 2:
  - `M = s × L × r`, `T = 60 × W / M`, `c = min(1, R / M)`, `A = L × c`, `L* = R / (s × r)`
- The starter script below. Copy it into `lab10.py`. It simulates one channel minute by minute with Poisson posting.

```python
import numpy as np

rng = np.random.default_rng(10)

def simulate(L, s, r, R, minutes=60, spammers=0, spam_rate=0.0, cap=None):
    """Simulate one public channel minute by minute.
    Posters send Poisson(rate) messages per minute. Each listener reads
    up to R messages per minute, chosen at random from that minute's messages.
    Returns mean messages per minute, mean coverage, and mean reader-views
    per minute for one polite poster and for one spammer."""
    N = int(round(s * L))
    spammers = min(spammers, N)
    rate = np.full(N, r)
    rate[:spammers] = spam_rate
    if cap is not None:
        rate = np.minimum(rate, cap)
    M_list, cov_list, views_polite, views_spam = [], [], [], []
    for _ in range(minutes):
        sent = rng.poisson(rate)            # messages per poster this minute
        M = sent.sum()
        if M == 0:
            continue
        c = min(1.0, R / M)                 # share of messages each reader sees
        readers = rng.binomial(L, c, size=M)   # readers of each message
        owner = np.repeat(np.arange(N), sent)
        per_poster = np.bincount(owner, weights=readers, minlength=N)
        M_list.append(M); cov_list.append(c)
        views_polite.append(per_poster[spammers:].mean())
        if spammers:
            views_spam.append(per_poster[:spammers].mean())
    return (np.mean(M_list), np.mean(cov_list),
            np.sum(views_polite) / max(1, len(views_polite)),
            np.mean(views_spam) if views_spam else 0.0)

def split(L, s, r, R, k, **kw):
    """TODO (step 4): split listeners and spammers evenly over k channels
    and return the per-channel results of simulate()."""
    raise NotImplementedError
```

## Steps

1. **Field count (at home, 30 min).** Watch one public channel for three separate 10-minute windows at different times of day. For each window, record the number of messages, the number of distinct posters, and the number of messages that are repeats of an earlier message by the same player. Estimate `L` from the channel's member list or the population of the area (say how). Compute `M`, `s × r`, and `T` for a `W` that matches your chat window.
2. **Formula check.** Run `simulate` with `s = 0.1`, `r = 0.5`, `R = 20` for `L = 50, 200, 400, 1,000, 3,000`. Put the simulated `M`, coverage and polite views per minute next to the formula values (`r × A`) in one table.
3. **The knee.** Plot simulated and formula coverage against `L` from 100 to 800 in steps of 50. Near `L* = 400` the simulation falls below the formula. Explain why, in two or three sentences. (Hint: in a minute with more messages than average, coverage drops, and in a quiet minute it cannot rise above 100%.)
4. **Spam and its fixes.** At `L = 1,000`, add 10 spammers at 4 messages per minute. Record `M`, coverage, and views for a polite poster and a spammer. Then try three fixes separately: a rate cap of 0.5 per minute, a split into 2 channels (implement `split`), and a split into 3 channels. Make one bar chart of polite-poster views per minute for the four cases.
5. **Your channel.** Plug your field estimates from step 1 into the formulas. Is your channel above or below its saturation point? What share of messages were repeats, and does that fit the spam incentive from the lecture?
6. **Design brief.** Read the brief below and write your channel design.

**Brief:** *Lanternfall* is a fantasy MMO with one server of about 4,000 concurrent players, four cities, twelve zones, five-player dungeons and 20-player raids. It has an auction house and a group finder. The designers want new players to make friends in the first week, and they want traders to keep a lively city market without drowning out everything else.

## Deliverable

`lab10.py`, the tables from steps 1 and 2, the charts from steps 3 and 4, and a design memo of 600-800 words. The memo must list every public channel in your design with its audience, vocabulary, persistence and rate limit. For the busiest channel it must give an estimate of `L`, `s`, `r`, `R` and the resulting coverage. It must name one restricted-vocabulary or ping channel and the purpose it serves, and one route for harassment that your design leaves open, with the tool you would use against it.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Field count | Three windows, clear method for `L`, repeats counted, formulas applied correctly | Counts present, `L` guessed without method or one window only | Missing or no numbers | 20% |
| Formula check and knee | Table matches formula within noise; knee gap explained correctly | Table present, explanation vague | Missing or wrong | 20% |
| Spam and fixes | All four cases run and charted; the fixes compared with numbers | Cases run, comparison weak | Missing | 20% |
| Design memo | Channels serve named purposes, load estimate with numbers, a credible open harassment route and remedy | Channels listed, weak link to the model | Opinion without the model | 40% |

<details>
<summary>Instructor check values</summary>

- Formula, `s = 0.1, r = 0.5, R = 20`: `L = 50` gives M 2.5, c 100%, polite views 25. `L = 400` gives M 20, c 100%, views 200. `L = 1,000` gives M 50, c 40%, views 200. `L = 3,000` gives M 150, c 13.3%, views 200.
- Seed 10 simulation, same inputs, first calls in order: `L = 50` M ≈ 2.4, views ≈ 24; `L = 400` M ≈ 19.4, c ≈ 0.94, views ≈ 179; `L = 1,000` M ≈ 50.8, c ≈ 0.40, views ≈ 200; `L = 3,000` M ≈ 149, c ≈ 0.135, views ≈ 200. Values vary with call order; anything within about 5% of these is fine.
- Spam (10 at 4 per minute): M ≈ 85, c ≈ 0.24, polite ≈ 117, spammer ≈ 940. Formula: 85, 23.5%, 118, 941.
- Cap 0.5: M ≈ 50, polite ≈ 200, spammer ≈ 200.
- Split 2 (500 listeners and 5 spammers per channel): formula M = 42.5, c = 47.1%, A = 235, polite ≈ 118. Splitting alone does not help the polite poster here, because audience per message stays `R / (s × r_eff)` in each channel while the channel is saturated. Split 3 (333 listeners, 3.3 spammers): M ≈ 28.3, c ≈ 70.6%, A ≈ 235. Students who notice that the split changes coverage but not audience per message have understood the model; the cap is the fix that restores polite views.

</details>
