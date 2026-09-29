# MMO407 · Week 10 — Recovery strategies

**Why this matters:** A bad launch damages three things at different speeds. The build can be fixed in weeks, the players who left can be won back in months, and the public record of the launch can take years to move. Teams that treat recovery as one job ("ship the fix") are surprised when the fix is good and nothing changes. This week you learn to tell the three apart, measure how slowly the slowest one moves, and pick a recovery plan that works on the one you actually need.

**You will be able to:**
- Compute a game's all-time review share after a recovery, and the number of new reviews (and months) needed to lift it to a target.
- Explain, with the weighted-average model, why a recent-window score jumps after a fix while an all-time score crawls, and recognise the same model in three storefront rating systems.
- Size the lapsed-player pool after a bad launch and estimate what a recovery update can bring back.
- Design a recovery plan that names which of the three stocks (build, players, reputation) each step moves, how fast, and at what cost.

**Before class:** Valve, Steamworks documentation, "User Reviews" (the sections on review score and review bombs, about 15 minutes). Read the "Post-release" and "Updates" sections of the Wikipedia article "No Man's Sky" (about 20 minutes) and note every date. Reread MMO308 week 13, sections 1 and 4; this week starts where an incident ends.

**Prerequisites from earlier courses:** [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) (revert or fix forward, compensation, the incident postmortem). [MMO308 week 4, funnels and churn](../../MMO308-live-operations-analytics-and-experimentation/lectures/w04-funnels-and-churn.md) (churned and returning players). [DB201 week 14, backups and disaster recovery](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md) (rollback cost in lost progress). [MMO301 week 13, worlds that died](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w13-worlds-that-died-shutdowns-and-their-lessons.md) (merges and the empty-shard spiral). [Week 1 of this course](w01-launch-day-anatomy.md) (the launch pipeline) and [week 3](w03-beta-strategies.md) (what a beta could not see).

**Interactive:** [examples/w10-review-memory.html](../examples/w10-review-memory.html). Keep it open during section 2.

---

## 1. Three things a bad launch breaks

When a launch goes badly, players and press say "the game is broken." That sentence mixes three separate stocks. A **stock** here is anything that accumulates over time and can only change as fast as its inflows and outflows allow. You met the idea in MMO301 week 13, where the player population was a stock.

| Stock | What it is | What refills it | Typical speed |
|---|---|---|---|
| The build | the code, content and servers | patches | days to weeks per fix |
| The players | active players, plus the pool of people who bought or tried the game and left | returning players, new players | months |
| The reputation | the public record of what people thought: store reviews, press, forum threads, videos | new reviews and coverage that outweigh the old | years |

Each stock has its own clock. A patch changes the build the day it ships. It changes the player stock only when lapsed players hear about it and come back. It changes the reputation only when enough new opinions are written to outweigh the old ones.

MMO308 week 13 covered the first hours of a problem: stop the damage, revert or fix forward, compensate, and write the incident postmortem. This week is about the months after that. The incident is over. The servers are stable. And the game is still, in public, "the one that launched broken." The question is what you can do about each stock, and how long each will take to respond.

The slowest of the three is the reputation, and it is the one teams most often misjudge. So the worked example starts there.

## 2. Worked example: the review score that will not move

### The hook

No Man's Sky launched on 9 August 2016 on PlayStation 4, and on Windows on 12 August. Players on Steam and GOG used their review pages to protest missing features, and the game became a byword for a broken promise. Hello Games then shipped years of free updates. By late September 2026 the Steam store page showed two numbers side by side. Of the English-language reviews from the last 30 days, 91% were positive. Of all 186,136 English-language reviews since launch, 82% were positive.

Here is the puzzle. Ten years of updates, and the all-time number still sits nine points below what current players say. Why does it lag so far, and how long would it take to close the gap? The same question hits every MMO team that recovers from a bad launch. The build is good, the players who are there like it, and the number a stranger sees still tells the old story.

### The model

A review score is a weighted average. Name the parts.

- `N₀` is the number of reviews written before the recovery, and `s₀` the share of them that are positive.
- `r` is the share of new reviews that are positive after the recovery.
- `n` is the number of new reviews written per month.
- `N₁` is the number of new reviews since the recovery, so `N₁ = n × t` after `t` months.
- `S_all` is the all-time positive share, the lifetime number on the store page.
- `S_recent` is the positive share of reviews in a recent window, such as the last 30 days.

```
S_all    = (N₀ × s₀ + N₁ × r) / (N₀ + N₁)
S_recent = r                         once the window holds only post-recovery reviews
```

The all-time score is a mixture of the old reviews and the new. Each new review pulls the average toward `r`, and it pulls less and less as the pile grows.

Solve the first line for `N₁` to find how many new reviews you need to reach a target share `T`:

```
N₁ = N₀ × (T − s₀) / (r − T)          valid only when s₀ < T < r
months to target = N₁ / n
```

Two features of this formula matter for design.

1. **`N₀` multiplies everything.** The louder the bad launch (the more reviews written in anger), the more new reviews each point of recovery costs. A launch that drew 40,000 reviews needs twice the recovery volume of one that drew 20,000, at the same shares.
2. **The denominator `r − T` explodes as the target approaches `r`.** You can never lift the all-time score to the share current players give. Every point closer costs more than the last.

The recent-window score behaves in the opposite way. It forgets. Once 30 days have passed since the recovery, every review in the window is new, and `S_recent = r`. So a store page that shows both numbers shows the gap between "what players think now" and "what players have thought on average since launch." The size of that gap is a measure of how much of the launch the page still remembers.

### Numbers you can check

Take an invented MMO. Its launch window drew `N₀ = 40,000` Steam reviews at `s₀ = 35%` positive. The team fixes the servers and the worst systems. After the fix, `r = 85%` of new reviews are positive, and `n = 1,500` new reviews arrive each month.

| Months since the fix | New reviews `N₁` | All-time share `S_all` | Last-30-days share |
|---|---|---|---|
| 0 | 0 | 35.0% | 35% |
| 6 | 9,000 | 44.2% | 85% |
| 12 | 18,000 | 50.5% | 85% |
| 24 | 36,000 | 58.7% | 85% |
| 36 | 54,000 | 63.7% | 85% |
| 60 | 90,000 | 69.6% | 85% |

Check the 12-month row by hand. Positive reviews are `40,000 × 0.35 + 18,000 × 0.85 = 14,000 + 15,300 = 29,300`. Total reviews are `58,000`. The share is `29,300 / 58,000 = 50.5%`.

Now ask the planning question. How long to reach each target?

| Target all-time share | New reviews needed `N₁` | Months at 1,500 per month |
|---|---|---|
| 50% | 17,143 | 11.4 |
| 60% | 40,000 | 26.7 |
| 70% | 93,333 | 62.2 |
| 80% | 360,000 | 240.0 |

Check the 60% row. `N₁ = 40,000 × (0.60 − 0.35) / (0.85 − 0.60) = 40,000 × 0.25 / 0.25 = 40,000`. At 1,500 per month that is 26.7 months. The step from 70% to 80% costs almost four times as many reviews as everything before it. That is the `r − T` denominator at work.

This script prints both tables:

```python
LAUNCH_REVIEWS, LAUNCH_SHARE = 40_000, 0.35   # reviews written in the bad launch window
NEW_SHARE, PER_MONTH = 0.85, 1_500            # after the fix: share positive, reviews per month

def lifetime_share(new_reviews):
    """All-time positive share once `new_reviews` more have arrived at NEW_SHARE."""
    positive = LAUNCH_REVIEWS * LAUNCH_SHARE + new_reviews * NEW_SHARE
    return positive / (LAUNCH_REVIEWS + new_reviews)

def reviews_needed(target):
    """New reviews at NEW_SHARE that lift the all-time share to `target`."""
    return LAUNCH_REVIEWS * (target - LAUNCH_SHARE) / (NEW_SHARE - target)

for months in (0, 6, 12, 24, 36, 60):
    print(f"month {months:2}  all-time {lifetime_share(PER_MONTH * months):5.1%}")
for target in (0.50, 0.60, 0.70, 0.80):
    n = reviews_needed(target)
    print(f"reach {target:.0%}: {n:7,.0f} new reviews = {n / PER_MONTH:5.1f} months")
```

It prints:

```
month  0  all-time 35.0%
month  6  all-time 44.2%
month 12  all-time 50.5%
month 24  all-time 58.7%
month 36  all-time 63.7%
month 60  all-time 69.6%
reach 50%:  17,143 new reviews =  11.4 months
reach 60%:  40,000 new reviews =  26.7 months
reach 70%:  93,333 new reviews =  62.2 months
reach 80%: 360,000 new reviews = 240.0 months
```

Now apply the model to the hook. No Man's Sky's English page showed `N₀ = 186,136` at about 82%, with recent reviews at 91% and 5,156 of them in 30 days. To lift the all-time share to 85%, it needs `186,136 × (0.85 − 0.82) / (0.91 − 0.85) ≈ 93,000` more reviews at 91%, which is about 18 months at the current rate. Both input shares are rounded to whole percents, so treat this as a rough answer. The shape is the point. A decade of good updates has moved the all-time number from its launch-era low to 82%, and each further point now costs more.

### Move it yourself

Open the interactive. The left view shows the recent-window score over five years. It drops at launch and jumps to `r` 30 days after the fix. The right view shows the all-time score over the same five years, crawling up a curve that never reaches `r`. Drag the "launch reviews" slider from 40,000 to 10,000. The recent view does not change at all. The all-time curve rises much faster. The size of the bad launch is invisible in the score players see today and dominant in the score strangers see.

Then press "relaunch event." It adds one month with 20,000 reviews at `r`, the kind of spike a major update, a free weekend or a new platform brings. Watch the all-time curve jump. One month of volume does what 13 months of trickle would.

### Cross-game recognition

Every rating system you will meet is the same weighted average with a different choice of weights. Write it once in general form:

```
score = Σ w(age_i) × x_i / Σ w(age_i)
```

Here `x_i` is 1 for a positive review and 0 for a negative one (or a star value), `age_i` is how old review `i` is, and `w` is the weight the platform gives a review of that age. The whole design question is the shape of `w`.

**Steam (current store, read September 2026).** Steam shows two scores at the top of a store page, one for the past 30 days and one for the product's lifetime. In the general form, the lifetime score is `w = 1` for every review. The recent score is `w = 1` if the review is 30 days old or less and `w = 0` otherwise. Only reviews from accounts that bought the game on Steam count toward the score. Valve also marks bursts of off-topic reviews (review bombs) and removes them from the score, which is a third weight, `w = 0` for flagged reviews of any age.

**Fallout 76 (Bethesda, 2018 launch, Steam release April 2020).** Fallout 76 launched on 14 November 2018, outside Steam, to poor reviews from critics and players. When it arrived on Steam in April 2020 with the Wastelanders update, the Steam page started with `N₀ = 0`. No launch reviews were in the pile, because none had been written there. The history still found a way in. Players upset about the original launch review-bombed the new page, and other players answered with positive reviews. A new storefront gives you a fresh denominator, not a fresh audience. By September 2026 the page showed 75% positive of 46,837 English reviews and 72% of the last 30 days, so on this page the two numbers roughly agree.

**Apple App Store (current rules).** Apple lets a developer reset an app's summary rating when releasing a new version. In the general form, that sets `w = 0` for every rating older than the reset. Apple advises using it sparingly, because a page with few ratings can put people off, and a reset does not remove written reviews. This is the "relaunch" lever built into a platform.

**Google Play (current rules).** Google's help pages say the rating users see is weighted toward more recent ratings, so that updates show up in the score. Google does not publish the weights. In the general form, `w` falls with age, somewhere between Steam's lifetime score (flat) and its recent score (a 30-day box).

Four platforms, one formula, four choices of `w`. When you meet a new rating system, ask what its `w` is. That tells you how long your launch will follow you there.

### Eyes-open design judgment

- **Know which number your next customer reads.** A returning player reads patch notes and the recent score. A stranger deciding whether to buy often reads the all-time score first. A recovery aimed at lapsed players can succeed while the store page still fails strangers. Decide which audience the next six months are for.
- **Volume is a lever, and it is cheaper than time.** The all-time score moves with the number of new reviews, not with the calendar. A relaunch event that draws a month of 20,000 reviews at 85% lifts the example from 35% to 51.7% at once, where the trickle needed 13 months. Free weekends, a new platform and a large update all raise `n`. None of them help if `r` is still low, because you then add volume to the old story.
- **A reset is a real option with a real cost.** Moving to a new store page, a new product, or using a platform's reset wipes `N₀`. It also wipes every good review you had, and players notice when a game appears to hide its history. Fallout 76's Steam launch shows the old opinions can follow you. Use it when the product really is different, and say so openly.
- **Do not argue with the recent score.** If `r` is low after the fix, the fix did not work for the people playing. The model says nothing will lift the all-time number above `r`. Go back to the build.
- **Keep your own recent-window metric.** You can compute the model from your own store's review export each week. Track `S_recent`, `S_all` and the months-to-target from the formula on the recovery dashboard, next to the player numbers from section 3.

### Check this example

1. The section 2 game gets a better fix, with `r = 90%` and the same 1,500 reviews per month. How many months to reach 60% all-time?
2. A second game launched with 10,000 reviews at 35%, with `r = 85%` and 1,500 per month after its fix. How many months to reach 60%? Compare with the 26.7 months of the section 2 game and explain the difference in one sentence.
3. A producer wants the all-time share at 85% within two years, with `r = 85%`. What does the model say?

<details>
<summary>Answers</summary>

1. `N₁ = 40,000 × 0.25 / 0.30 = 33,333`, which is 22.2 months.
2. `N₁ = 10,000 × 0.25 / 0.25 = 10,000`, which is 6.7 months. The formula is proportional to `N₀`, so a launch with a quarter of the reviews recovers in a quarter of the time at the same shares.
3. It is impossible. The all-time share approaches `r` but never reaches it, so the target must be below 85%, or `r` must rise above it.

</details>

## 3. The recovery menu

The review model tells you how slowly reputation moves. The rest of a recovery is choosing what to do while it moves. Here are the standard moves, each described by the stock it works on, how fast, and what it costs. None of them is a default. Pick them against the diagnosis.

| Move | Stock it works on | Speed | Main cost or risk |
|---|---|---|---|
| Stabilise and compensate | build, players | days | MMO308 week 13 covers it |
| Roll back corrupted data | build | hours to days | lost player progress (DB201 week 14) |
| Fix the core loop | build, then players | months | the whole team, and a period with nothing new to announce |
| Change the business model | players | a season | revenue per player falls; paying players may feel cheated |
| Merge worlds | players | weeks | the "dying game" signal; name clashes and lost housing |
| Relaunch | all three | a year or more | nearly a second launch budget |
| Wind down | none | months | MMO308 week 14 covers when and how |

**Stabilise and compensate** is the incident response from MMO308 week 13, and it is not repeated here. What matters for the rest of a recovery is that it ends. At some point the servers are stable, the rollbacks are done, and the war room from week 1 goes home. If the team is still in incident mode a month after launch, the next moves never start.

**Change the business model.** Three well-known subscription MMOs switched models after launch. The Lord of the Rings Online added a free-to-play option with an in-game store in North America on 10 September 2010, and in Europe on 2 November 2010. Star Wars: The Old Republic made its free-to-play option live on all servers on 15 November 2012, less than a year after launch. The Elder Scrolls Online launched on Windows and Mac on 4 April 2014 with a required subscription. In March 2015 it was rereleased as The Elder Scrolls Online: Tamriel Unlimited, buy-to-play with microtransactions and an optional subscription, and its reception improved. A model change lowers the price of entry, which raises the flow of new and returning players. It does nothing for a broken build, and it changes who your players are. The business case belongs to [MMO403](../../MMO403-business-monetization-and-ethics-of-live-games/syllabus.md), not this week.

**Merge worlds.** Week 2 showed why launch teams open more worlds than they need a month later. A merge fixes the empty-world spiral from MMO301 week 13. It also tells players, correctly, that numbers fell. Do it early and plainly, before the spiral has done its work.

**Relaunch.** A relaunch rebuilds the game and releases it again, usually with a new name. [Week 4 of this course](w04-case-ffxiv-1-0-to-a-realm-reborn.md) is the full case of Final Fantasy XIV's relaunch as A Realm Reborn, and it is not retold here. In this week's model, a relaunch is the only move that works on all three stocks at once. It changes the build, it gives lapsed players an event to come back for, and a new name starts a new pile of reviews and press. It also costs close to a second launch.

**Wind down.** Sometimes the honest answer is that no recovery pays. MMO308 week 14 covers how to forecast that month and plan the ending.

## 4. The pool of players who left

The player stock has a feature that makes recovery possible at all. After a bad launch, most people who bought the game have left, but they still own it or still have an account. They are the **lapsed pool**, players who tried the game and stopped. MMO308 week 4 showed how to measure churn and return with care. Here we need only the arithmetic of the pool's size.

Take an invented buy-to-play MMO that sold `B = 1,000,000` copies in launch month. Six months later it has `A = 80,000` monthly active players. The lapsed pool is

```
L = B − A = 920,000
```

A recovery update brings back a fraction `ρ` (rho) of the lapsed pool in its first month. If `ρ = 5%`, that is `46,000` returning players, more than half the size of the current active base. Only a small share of those returners come from people who never heard of the game. The update's main audience is the people who already left.

Two consequences follow.

1. **Plan the update for returners.** They log in to a character they abandoned months ago, often into a world that has since been merged, with systems they no longer recognise. A returner's first hour needs its own design: a catch-up path, a summary of what changed, and a fix for any progress the rollbacks took away. If that first hour fails, `ρ` is spent and the second chance is gone.
2. **Returners churn faster than the base.** Some came to check whether the game is fixed. Budget for a large share of them leaving again within weeks, and judge the update by how many stay after the first month, not by the peak.

The pool also shrinks with time. Players uninstall, move on and forget their passwords. A recovery that takes three years to ship reaches a smaller and colder pool than one that takes one year. This is the hidden cost of the "fix the core loop" move in section 3, and a reason to ship in visible steps.

No Man's Sky's recovery used a pattern you can copy. After the launch, which had over-promised, Hello Games said little in public and preannounced most major updates only two or three days before release. That kept expectations from outrunning the build, which is exactly the gap that filled the launch reviews with anger. [Week 9 of this course](w09-communication-during-crises.md) covers crisis communication in detail.

## In-class activity (25 minutes)

Groups of three. You run recovery for an invented MMO six months after a bad launch. Your numbers:

- Steam: 60,000 launch-window reviews at 30% positive. Since the stabilisation patch, 2,000 reviews a month at 80% positive.
- Sales: 1,500,000 copies. Monthly active players: 110,000.
- Budget for the next year: one of (a) a large content update with a free weekend, expected to bring 25,000 reviews in its month at 80% and to reactivate 6% of the lapsed pool; (b) a relaunch on a new store page in 12 months, starting a fresh review pile; (c) a business-model change to free-to-play, expected to raise new players but not reviews.

1. Compute the all-time share after 12 months with no event.
2. Compute it after 12 months if option (a) happens in month 6.
3. Size the lapsed pool and the returners under option (a).
4. Choose an option and write three sentences defending it, naming which stock each part of your plan moves and when.

Expected output. Without an event, 12 months add 24,000 reviews, and the share is `(18,000 + 19,200) / 84,000 = 44.3%`. With option (a), the extra 25,000 reviews add 20,000 positive, giving `(18,000 + 19,200 + 20,000) / 109,000 = 52.5%`. The lapsed pool is `1,500,000 − 110,000 = 1,390,000`, so 6% is 83,400 returners, most of them expected to leave again. A strong answer notices that option (b) resets the store number but not the audience (Fallout 76), and that option (c) works on the player stock only.

## Common misconceptions

- **"Once the game is good, the score will catch up."** The recent score catches up in 30 days. The all-time score approaches `r` but never reaches it, and the time it takes grows with the size of the bad launch.
- **"A recovery update is for new players."** Most of its audience is the lapsed pool. Design the first hour for people coming back to an abandoned character.
- **"A new store page gives you a clean slate."** It resets the denominator, not the memory of the audience. Fallout 76's Steam page was review-bombed by players still angry about the 2018 launch.
- **"Going free-to-play is a recovery."** It changes the price of entry, which moves the player stock. If the build is still broken, it brings more people to a game that will lose them again.

## Check yourself

1. An MMO has 25,000 reviews at 40% positive. After a fix, `r = 88%` and `n = 1,000` per month. How many months until the all-time share reaches 70%?
2. Two teams face the same launch pile, 30,000 reviews at 30%. Team A reaches `r = 80%` at 1,000 reviews a month. Team B reaches `r = 90%` at 500 reviews a month. Which reaches 60% all-time first, and by how much?
3. Write Apple's summary-rating reset and Steam's 30-day score in the general form `Σ w × x / Σ w`. What is `w` in each?
4. A game sold 600,000 copies and has 45,000 monthly active players. A recovery update reactivates 4% of the lapsed pool, and half of those returners leave within a month. How many net players does it add after one month?
5. Your recovery plan has one budget line left. Option 1 is a free weekend, expected to bring 12,000 reviews at your current `r`. Option 2 is three more months of quality fixes, expected to raise `r` from 70% to 85% with no extra volume. Your all-time share is 45%. Which would you pick, and what single number decides it?

<details>
<summary>Answers</summary>

1. `N₁ = 25,000 × (0.70 − 0.40) / (0.88 − 0.70) = 25,000 × 0.30 / 0.18 = 41,667`, about 41.7 months.
2. Team A: `30,000 × 0.30 / 0.20 = 45,000` reviews, 45 months. Team B: `30,000 × 0.30 / 0.30 = 30,000` reviews, 60 months. Team A gets there 15 months sooner, because its extra volume outweighs Team B's higher share for this target.
3. Apple reset: `w = 1` for ratings after the reset, `w = 0` before it. Steam recent: `w = 1` for reviews 30 days old or less, `w = 0` for older ones. (Steam's lifetime score is `w = 1` for all.)
4. Lapsed pool `600,000 − 45,000 = 555,000`. 4% is 22,200 returners, half stay, so about 11,100 net.
5. It depends on `r`, and here `r` is only 70%. Adding 12,000 reviews at 70% moves the all-time share toward 70%, but a low `r` also tells you current players are still unhappy, so the recent score and word of mouth stay weak. Most teams should fix first (option 2), then buy volume once `r` is high. The deciding number is `r` against the target: volume at a low `r` only buys a low ceiling.

</details>

## Lab / assignment hook

[Lab 10, recovery dashboard](../labs/lab10.md). You build a small library that computes all-time, recent-window and weighted review scores from a daily review log, reproduce this lecture's tables, find the months-to-target for three recovery plans, and write a one-page recovery plan that names the stock each step moves. The plan feeds the week 13 launch plan workshop, where every launch plan needs a recovery section.

## Sources

- Wikipedia, "No Man's Sky" (read September 2026). Release on 9 August 2016 (PlayStation 4) and 12 August 2016 (Windows); negative player reviews on Steam and GOG at launch over missing features; later major updates preannounced only two or three days before release; the Next update in July 2018.
- Steam store page, No Man's Sky, app 275850 (read 28 September 2026). 91% of 5,156 English reviews in the last 30 days positive; 82% of 186,136 English reviews positive. Numbers change daily.
- Steam store page, Fallout 76, app 1151340 (read 28 September 2026). 72% of 355 English reviews in the last 30 days positive; 75% of 46,837 English reviews positive.
- Wikipedia, "Fallout 76" and "Review bomb" (read September 2026). Release on 14 November 2018 and poor reception at launch; Steam release with Wastelanders in April 2020; review bombing on Steam by players upset over the launch, and a counter-campaign of positive reviews. Valve added review histograms in 2017.
- Valve, Steamworks documentation, "User Reviews" (partner.steamgames.com, read September 2026). Two review scores on the store page, the past 30 days and the lifetime; only purchases by the reviewing account count toward the score; off-topic review bombs do not count toward the score.
- Apple Developer, "Ratings, Reviews, and Responses" (developer.apple.com/app-store/ratings-and-reviews, read September 2026). The summary rating can be reset with a new version; Apple advises using the reset sparingly; written reviews are not reset.
- Google Play Console Help, "View and analyze your app's ratings and reviews" (support.google.com, answer 138230, read September 2026). The rating users see is weighted toward more recent ratings.
- Wikipedia, "The Lord of the Rings Online" (read September 2026). Free-to-play in North America on 10 September 2010 and in Europe on 2 November 2010.
- Wikipedia, "Star Wars: The Old Republic" (read September 2026). Free-to-play option live on all servers on 15 November 2012.
- Wikipedia, "The Elder Scrolls Online" (read September 2026). Release on 4 April 2014 for Windows and Mac with a monthly subscription; March 2015 rerelease as Tamriel Unlimited, buy-to-play with microtransactions and an optional subscription; improved reception.
- All other review counts, shares, sales and reactivation rates in sections 2 to 4 and the activity are invented teaching values.

## Interactive spec: examples/w10-review-memory.html

**The one insight:** after a fix, the recent-window score jumps to the new share within 30 days, while the all-time score crawls toward it and never arrives. The size of the bad launch is invisible in one view and dominant in the other.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "what players say now": a line chart, x = months 0 to 60 after the fix, y = 0% to 100%. One line, the 30-day score (`--moss`). A dashed horizontal line at `r`. A shaded band before month 1 shows the launch window at `s₀`.
- View B, "what the store page remembers": same axes. The all-time score `S_all(t)` (`--blood`), the dashed line at `r`, and a dotted horizontal target line at `T` with a marker where `S_all` crosses it (or a label "never" if `T ≥ r`). When a slider changes, the previous `S_all` curve stays as a faint ghost for comparison.

**Controls:**

- Launch reviews `N₀`, slider 1,000 to 200,000, step 1,000 (default 40,000).
- Launch share `s₀`, slider 5% to 80%, step 1% (default 35%).
- New share `r`, slider 40% to 99%, step 1% (default 85%).
- Reviews per month `n`, slider 100 to 20,000, step 100 (default 1,500).
- Target `T`, slider 30% to 95%, step 1% (default 60%).
- "Relaunch event" toggle and month slider (1 to 48, default 6). When on, one month gets an extra `E` reviews at share `r`, with `E` slider 0 to 100,000, step 1,000 (default 20,000).
- Weighting selector for View B: "lifetime (Steam)", "reset at the fix (App Store style)", "exponential, half-life H months (illustrative)". With exponential, a slider `H` 1 to 36 months (default 12). Label the exponential mode as illustrative because Google does not publish its weights.
- Preset buttons: "section 2 example", "smaller launch (10,000)", "No Man's Sky, Sept 2026 (rough)" which sets `N₀ = 186,136`, `s₀ = 82%`, `r = 91%`, `n = 5,156`, `T = 85%`, months axis starting at 0 = September 2026.

**Readout (always visible, `aria-live="polite"`):** `S_all` at months 12, 24 and 60; reviews needed `N₁` and months to `T`, or "never: target is at or above r"; and a sentence such as "The recent score reached 85% at month 1. The all-time score reaches 60% at month 26.7."

**Formulas:**

```
monthly reviews: month 0 holds the launch pile N₀ at s₀; months 1..60 hold n at r
(plus E at r in the event month if the toggle is on)
lifetime:     S_all(t) = Σ_{m ≤ t} pos_m / Σ_{m ≤ t} tot_m
reset:        same sums over months 1..t only (month 0 excluded); undefined at t = 0
exponential:  weight of month m at time t is 0.5^((t − m) / H)
recent (View A): pos_t / tot_t for the month ending at t (month 0 shows s₀)
months to T (lifetime, no event): N₁ = N₀ (T − s₀) / (r − T); months = N₁ / n; "never" if T ≥ r
```

**Test values (must match):**

- Defaults: `S_all` 35.0% at 0, 44.2% at 6, 50.5% at 12, 58.7% at 24, 63.7% at 36, 69.6% at 60. Months to 60% = 26.7 (40,000 reviews). Months to 70% = 62.2.
- `T = 85%` with `r = 85%`: readout "never".
- `N₀ = 10,000`: months to 60% = 6.7; View A identical to defaults.
- Relaunch on at month 6 with `E = 20,000`: at month 6, total reviews `40,000 + 9,000 + 20,000 = 69,000`, positive `14,000 + 7,650 + 17,000 = 38,650`, `S_all = 56.0%`. (For comparison, an event alone at month 0 gives `(14,000 + 17,000) / 60,000 = 51.7%`.)
- Reset mode: `S_all = 85%` from month 1.
- No Man's Sky preset: `N₁ ≈ 93,068`, months to 85% ≈ 18.1.

**First screen:** defaults, both views drawn, View A already at 85% and View B at 35% rising slowly, with the caption "Players now say 85%. The store page will take 27 months to show 60%."

**Accessibility:** every control keyboard operable with visible focus; readout in `aria-live="polite"`; all chart values also shown in a small table under View B (months 0, 6, 12, 24, 36, 60); `prefers-reduced-motion` disables curve animation; respects `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only, no game art, logos or store screenshots.
