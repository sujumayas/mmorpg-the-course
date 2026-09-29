# MMO407 · Exam bank: practice, quiz and panel questions

MMO407 has no written exam. The grade comes from the case analyses (50%, see [case-analyses-brief.md](case-analyses-brief.md)) and the launch plan (50%, see [launch-plan-brief.md](launch-plan-brief.md)). This bank has three jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab goes quickly.
- **Lab quizzes.** Each lab session opens with a 10-minute ungraded quiz of two or three questions from this bank, usually one compute and one analysis question.
- **Panel questions.** The week 15 panel asks questions in this style, rewritten with the numbers from your own launch plan and your own case. The gate, tail and transfer questions from [week 14](../lectures/w14-presentations.md) are built the same way.

Every question is tagged with the week it draws on and one type.

- **compute**: apply a lecture model to values you have not seen before.
- **code**: say what a short piece of Python prints, using the lecture's definitions.
- **analysis**: explain why a model behaves as it does, with a number as evidence.
- **design**: choose a lever, a rule or a threshold for a stated situation and justify it with the model.
- **critique**: find what is wrong with a claim, a plan or a lesson and fix it.

All numbers are invented teaching values unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and version. Every code snippet runs as shown with the course Python (`.venv/bin/python`, Python 3), and every number in the answers was recomputed with the lecture's own model. Write your own answer before you open the solution.

---

## Week 1: Launch day anatomy

1. *Week 1 · compute.* A launch pipeline has five stages with these capacities in players per minute: patch check 6,000, authentication 900, entitlement 1,300, character select 1,100, world entry 1,000. Arrivals are 1,400 per minute. Find the throughput, the bottleneck and the backlog after 90 minutes.

<details>
<summary>Answer and worked solution</summary>

**Answer:** throughput 900 per minute, bottleneck authentication, backlog 45,000.

`X = min(1,400, 6,000, 900, 1,300, 1,100, 1,000) = 900`. The smallest capacity is authentication. The backlog grows at `1,400 − 900 = 500` per minute, so after 90 minutes it is `500 × 90 = 45,000` players waiting in front of authentication. World entry, at 1,000, runs below capacity and looks calm.
</details>

2. *Week 1 · analysis.* In question 1 the war room can double exactly one stage. For each choice, what is the new throughput? Then the team doubles authentication and adds 50% to world entry. What is the throughput, the bottleneck and the 60-minute backlog, and where do players now wait?

<details>
<summary>Answer and worked solution</summary>

**Answer:** only doubling authentication helps (to 1,000). With authentication doubled and world entry at 1,500, throughput is 1,100, the bottleneck is character select, and the 60-minute backlog is 18,000.

Doubling patch check, entitlement, character select or world entry leaves authentication at 900 as the minimum, so throughput stays 900. Doubling authentication to 1,800 raises the minimum to world entry at 1,000. The team bought 900 players per minute and got 100 of them.

With authentication 1,800 and world entry 1,500, the capacities are 6,000, 1,800, 1,300, 1,100 and 1,500. The minimum is character select at 1,100, so `X = 1,100` and the backlog grows at 300 per minute, `18,000` after an hour. Players now wait at character select, which is a spinner or an error, not a queue with a position. Week 1's advice is to make world entry the planned bottleneck, so the next budget line belongs to character select.
</details>

3. *Week 1 · code.* What does this print?

```python
stages = {"patch": 6000, "auth": 900, "entitlement": 1300,
          "char select": 1100, "world entry": 1000}

def funnel(stages, arrivals):
    name = min(stages, key=stages.get)
    through = min(arrivals, stages[name])
    return name, through, arrivals - through

for change in ({}, {"auth": 1800}, {"auth": 1800, "world entry": 1500}):
    print(funnel({**stages, **change}, 1400))
```

<details>
<summary>Answer and worked solution</summary>

```
('auth', 900, 500)
('world entry', 1000, 400)
('char select', 1100, 300)
```

Each line is the narrowest stage, the throughput and the backlog growth per minute. The dictionary merge `{**stages, **change}` replaces only the changed stages, so the bottleneck walks from authentication to world entry to character select as the plan widens the stages in front of it.
</details>

4. *Week 1 · compute.* Use the lecture's retry arithmetic. Authentication can do 600 units of work per minute. A success costs 1 unit and a rejection costs `c` units, so in a minute with `A` attempts the successes `s` satisfy `s + c × (A − s) = 600`.
   (a) With `c = 0.1` and 4,000 attempts, how many players get in?
   (b) At how many attempts per minute do successes reach zero?
   (c) Engineers move the load check before the password proof, so `c = 0.02`. Repeat (a).

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) about 222. (b) 6,000. (c) about 531.

Solve for `s`: `s = (600 − c × A) / (1 − c)`.

(a) `(600 − 0.1 × 4,000) / 0.9 = 200 / 0.9 = 222.2`. The stage has capacity for 600 successes and admits 222, because rejecting 3,778 attempts costs 378 units.

(b) `s = 0` when `c × A = 600`, so `A = 600 / 0.1 = 6,000` attempts. From there on the stage is congestion-collapsed, busy refusing and admitting no one.

(c) `(600 − 0.02 × 4,000) / 0.98 = 520 / 0.98 = 530.6`. Cheap early rejection recovers most of the capacity. It does not stop the retry loop from growing, which is why the lecture prefers a queue with a position.
</details>

5. *Week 1 · compute.* A launch night lasts 16 hours. Players need nine services that are each up 99.7% of the time, plus an in-game store that is up 99%.
   (a) What is the chance all ten are up, and how many minutes of the night should you expect some required service to be down?
   (b) The store goes behind a kill switch, so the game lets players in when it is down. Repeat (a).

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 96.4%, about 35 minutes. (b) 97.3%, about 26 minutes.

(a) `0.997⁹ × 0.99 = 0.9733 × 0.99 = 0.9636`. The night is `16 × 60 = 960` minutes, and `(1 − 0.9636) × 960 = 35.0` minutes.

(b) Only the nine services remain in the chain: `0.997⁹ = 0.9733`, and `(1 − 0.9733) × 960 = 25.6` minutes. One switch on the least reliable service removes about 9 minutes of lockout. The availabilities multiply, so the weakest link in the required set costs the most.
</details>

6. *Week 1 · design.* Your MMO serves three regions from one shared authentication service (capacity 1,000 per minute), with region-local worlds. In the first launch hour the regions would send 900, 600 and 300 players per minute. Compare a global unlock with an unlock staggered by region for the authentication stage and for a single world in the busiest region. Which would you choose, and what does your choice not fix?

<details>
<summary>Answer and worked solution</summary>

**Answer:** staggered. Global: authentication sees 1,800 per minute and builds 800 per minute of backlog. Staggered: its worst hour is 900 per minute, under capacity, so no backlog forms there. A single world sees the same spike either way.

The shared stage adds the regions' arrivals only if they arrive at the same time. Staggering turns one spike of 1,800 into three spikes of 900, 600 and 300, each under 1,000. A world in the busiest region still receives that region's whole spike at its unlock, so its queue is unchanged, and the world count or layers must handle it. A strong answer also names the cost of staggering: a longer launch window for the war room and a harder message for players in the late regions.
</details>

## Week 2: Capacity planning and login queues

7. *Week 2 · compute.* Use the lecture's launch (1,200 players per minute across the game for the first hour, 400 per minute in hours 2 and 3, 150 afterwards; `C = 4,000`, entry rate `a = 100`, `L = 160`), but open only 8 worlds. Find each world's arrival rates, the queue at hours 1 and 3, the back-of-queue wait at hour 3, and the minute the queue empties.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `λ` = 150, 50 and 18.75 per world. Queue 4,500 at hour 1 and 7,500 at hour 3 (the peak). Wait at hour 3 about 300 minutes. Empty at minute 1,380.

`μ = 4,000 / 160 = 25` once full. While filling, `λ = 150` against `a = 100`, so the queue grows by 50 a minute and the world is full at minute 40 with 2,000 waiting. Minutes 40 to 60 add `(150 − 25) × 20 = 2,500`, so 4,500 at hour 1. Minutes 60 to 180 add `(50 − 25) × 120 = 3,000`, so 7,500 at hour 3. Then `λ = 18.75 < 25`, so the queue shrinks by 6.25 a minute and takes `7,500 / 6.25 = 1,200` minutes to clear, ending at minute 1,380. The wait at hour 3 is `7,500 / 25 = 300` minutes. The lecture's simulation, run with 8 worlds and 1,500 minutes, prints the same numbers.
</details>

8. *Week 2 · compute.* On a cumulative diagram, between minutes 60 and 150 the arrivals curve `A(t)` has slope 45 per minute and the admissions curve `D(t)` has slope 30. The gap at minute 60 is 800. What is the queue at minute 150, and the wait for the player at the back? At minute 150 arrivals drop to 20 per minute. When did the queue peak?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 2,150 players, a wait of about 72 minutes, and the peak is at minute 150.

The gap widens by `(45 − 30) × 90 = 1,350`, so `Q(150) = 800 + 1,350 = 2,150`. The wait at the back is the horizontal gap, about `2,150 / 30 = 71.7` minutes. The queue grows while `A` is steeper than `D` and shrinks once it is shallower. Arrivals fall below `μ = 30` at minute 150, so that is the peak.
</details>

9. *Week 2 · compute.* The lecture's 10-world launch runs with launch-week layers that raise each world's cap to 4,800 and its entry rate to 120, with `L = 160`. Find the queue at hours 1 and 3, the wait at hour 3, and when the queue empties. What happens to the day-30 population per world?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 1,800 at hour 1, 3,000 at hour 3, a wait of 100 minutes, empty at minute 380. Day 30 is unchanged at 3,000 per world once the layers close.

Per world, `λ` = 120, 40, then 15. The entry rate equals the rush, so the world fills with no queue at minute `4,800 / 120 = 40`. Then `μ = 4,800 / 160 = 30`. Minutes 40 to 60 add `(120 − 30) × 20 = 1,800`. Minutes 60 to 180 add `(40 − 30) × 120 = 1,200`, for 3,000 at hour 3. The wait is `3,000 / 30 = 100` minutes. After hour 3 the queue shrinks by `30 − 15 = 15` a minute and clears in 200 minutes, at minute 380. Layers change launch-week `C`, not the number of communities left on day 30.
</details>

10. *Week 2 · analysis.* For the lecture's 10-world launch, assume every session lasts exactly 160 minutes instead of ending at random. Compute the queue at minute 160 and at hour 3, and explain in two sentences why this is worse than the section 2 model with the same average `L`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 7,200 at minute 160 and 6,000 at hour 3, against 4,500 in the random-ending model.

The first players entered at minute 0, so nobody leaves before minute 160. By then arrivals total `120 × 60 + 40 × 100 = 11,200` and admissions are stuck at 4,000, so the queue is 7,200. From minute 160 the players who entered at 100 per minute during the fill leave at 100 per minute, so the queue shrinks by `100 − 40 = 60` a minute, to `7,200 − 60 × 20 = 6,000` at hour 3.

At a launch every session is young, so fixed-length sessions free almost no slots until `L` has passed, while random endings free `C / L` slots a minute from the moment the world fills. The steady-state formula is a floor for a launch queue, which is why the lecture asks for a range across session models.
</details>

11. *Week 2 · design.* The day-30 forecast is 32,000 players at the evening peak and a world feels alive with at least 2,500 at peak. What is the largest fixed world count that passes the day-30 test? For that count, what is the lecture launch's queue and wait at hour 3?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 12 worlds (2,667 per world on day 30). At hour 3 the queue is about 2,500 per world with a wait of about 100 minutes.

`32,000 / 12 = 2,667`, above 2,500. `32,000 / 13 = 2,462`, below it. With 12 worlds each sees 100, then 33.3, then 12.5 per minute. It fills at the entry rate with no queue by minute 40, then gains `(100 − 25) × 20 = 1,500` by hour 1 and `(33.3 − 25) × 120 = 1,000` by hour 3, about 2,500 in all, and `2,500 / 25 = 100` minutes of wait. If 100 minutes is too long, the lever is launch-week layers on 12 worlds, not a 13th world.
</details>

12. *Week 2 · critique.* A producer says, "Our login servers were upgraded to admit 400 characters per minute per world, four times the old rate, so the hour-3 queue will be about a quarter of what the model said." Using the lecture's 10-world launch, what is wrong, and which inputs would actually move the hour-3 queue?

<details>
<summary>Answer and worked solution</summary>

**Answer:** the entry rate matters only while worlds fill. The lecture's interactive shows the hour-3 queue falling only from 4,500 to about 4,350 when `a` goes from 100 to 400.

By hour 3 every world is full and admits `C / L = 25` per minute whatever `a` is. A faster entry path fills the world a few minutes sooner and changes nothing after that. The inputs that change the slopes after the world is full move hour 3: the cap `C` (layers), the session length `L`, the number of worlds (which splits `A(t)`), and the arrivals themselves (head start, staggered access, sales).
</details>

## Week 3: Beta strategies

13. *Week 3 · compute.* A closed beta has 6,000 testers playing 30 hours each. Launch week is forecast at 250,000 players playing 16 hours each. A crash fires once per 120,000 player-hours. What is the chance the beta sees it at least once, and how many times should you expect it in launch week?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 77.7%, and about 33 firings in launch week.

`E_beta = 6,000 × 30 = 180,000` player-hours. `r × E_beta = 180,000 / 120,000 = 1.5`, and `1 − e^(−1.5) = 0.777`. `E_launch = 250,000 × 16 = 4,000,000`, so the expected launch firings are `4,000,000 / 120,000 = 33.3`. Even a bug the beta probably sees can appear dozens of times at launch, because launch exposure is 22 times the beta's.
</details>

14. *Week 3 · compute.* The same beta sees no instance of a save-corruption bug. What does the rule of three say about its rate, and what is the most firings you should plan for in launch week?

<details>
<summary>Answer and worked solution</summary>

**Answer:** the rate is below 1 per 60,000 player-hours (95% confidence), so plan for up to about 67 firings.

`r < 3 / 180,000`, which is once per 60,000 player-hours. At launch exposure, `3 × 4,000,000 / 180,000 = 66.7`. A clean beta bounds the rate. It does not show the bug is absent.
</details>

15. *Week 3 · compute.* You must see, with 95% confidence, any crash that fires once per 250,000 player-hours or more often. How many beta player-hours do you need by the rule of three, and how many testers at 25 hours each? If the producer asks for 99% confidence, what are the exact numbers?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 750,000 player-hours, 30,000 testers. At 99%, about 1,151,000 player-hours and about 46,100 testers.

The rule of three needs `E ≥ 3 / r = 3 × 250,000 = 750,000`, and `750,000 / 25 = 30,000` testers. The exact multiplier for confidence `c` is `−ln(1 − c)`. For 95% it is 2.996, so the rule of three is within 0.2%. For 99% it is `ln 100 = 4.605`, so `E ≥ 4.605 × 250,000 = 1,151,293` player-hours, or `46,052` testers at 25 hours. The last percent of confidence costs half as much beta again.
</details>

16. *Week 3 · analysis.* A beta logs 400,000 player-hours, and telemetry shows 3% of play reached the endgame zones. No endgame bug was seen. What can you say about endgame bugs? The design lead then proposes a level cap that blocks the endgame entirely. What does the rule of three say then, and what would you do instead?

<details>
<summary>Answer and worked solution</summary>

**Answer:** the endgame had 12,000 player-hours, so its bug rate is only bounded below 1 per 4,000 player-hours. With a cap, its exposure is zero and the rule of three bounds nothing.

`E_path = 0.03 × 400,000 = 12,000`, and `3 / 12,000` is once per 4,000 player-hours, a very weak statement for content the most devoted players reach first. A cap makes `E_path = 0`. Keep the cap if the team wants a fresh endgame at launch, but add a targeted phase with pre-levelled characters on that path, or write the gap into the risk-to-exposure table with a launch-night response (kill switch, fast patch). Either way, make it a written decision.
</details>

17. *Week 3 · design.* The starting zone is forecast to peak at 3,000 players at launch. The beta's busiest weekend put 800 players there. A producer proposes doubling the number of beta testers and running two more weekends. Explain why that does not close the gap and specify a stress test that does.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the gap is crowd exposure, not player-hours. A stress test needs at least `1.2 × 3,000 = 3,600` players in the starting zone at once, for long enough to see tick behaviour settle (about an hour).

More testers over more weekends raise `E_beta` in player-hours, which bounds rates of bugs any player can trigger. A problem that appears only above some concurrency in one zone needs that concurrency, and a beta spread over weekends may never reach it. Use a scheduled session with a level cap that keeps everyone in the starting zone, a 20% margin over the forecast peak, and telemetry on the zone server's tick time.
</details>

18. *Week 3 · critique.* A studio's launch plan says, "The closed beta ran 250,000 player-hours with no crashes of this kind, so the rate is at most 1 in 250,000." Fix the statement and give the launch-week consequence for a launch of 3 million player-hours.

<details>
<summary>Answer and worked solution</summary>

**Answer:** with 95% confidence the rate is below `3 / 250,000`, about 1 in 83,333, three times higher than claimed. Launch week may then see up to `3 × 3,000,000 / 250,000 = 36` firings.

Zero events in `E` player-hours bound the rate at `3 / E`, not `1 / E`. The corrected sentence also belongs next to a launch response (telemetry alert on the crash signature, a patch pipeline, a kill switch where one applies).
</details>

## Week 4: Case, Final Fantasy XIV 1.0 to A Realm Reborn

19. *Week 4 · compute.* A team has `G = 500` fix-units, `φ = 0.35`, `F = 12` fix-units per month and a rebuild estimate `T_r = 28` months. It measures `m = 2.5`. Compute `T_patch`, `T_rebuild` and `m*`, and name the faster path.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `T_patch` ≈ 63.5 months, `T_rebuild` ≈ 55.1 months, `m*` = 1.92. Rebuild, by about 8.5 months.

`T_patch = 500 × (0.35 × 2.5 + 0.65) / 12 = 500 × 1.525 / 12 = 63.54`. `T_rebuild = 28 + 0.65 × 500 / 12 = 28 + 27.08 = 55.08`. `m* = 28 × 12 / (0.35 × 500) = 1.92`, and 2.5 is above it.
</details>

20. *Week 4 · analysis.* Spolsky's warning is that rebuild estimates run long. Pad `T_r` in question 19 by 50%. Does the decision survive? What is the new `m*`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** no. With `T_r = 42`, `T_rebuild` ≈ 69.1 months against a patch time of 63.5, so patching wins by about 5.5 months. The new `m*` is 2.88, above the measured 2.5.

`T_rebuild = 42 + 27.08 = 69.08`. `m* = 42 × 12 / 175 = 2.88`. The case sits between the lecture's games B and C. A decision that flips under the lecture's recommended padding is not safe to act on, so the team should measure `m` on more structural fixes before committing.
</details>

21. *Week 4 · compute.* Keep `T_r = 28` from question 19. The studio keeps `s = 0.2` of the team on the old game, and `c = 0.4` of that work carries over. Compute the build phase, the fix-units carried, and the new rebuild time. Is the parallel plan still faster than patching?

<details>
<summary>Answer and worked solution</summary>

**Answer:** build 35 months, 33.6 units carried, rebuild about 59.3 months. It still beats patching (63.5), by about 4 months.

`build = 28 / 0.8 = 35`. `carried = 0.4 × 0.2 × 12 × 35 = 33.6`. `rest = 0.65 × 500 − 33.6 = 291.4` units, which take `291.4 / 12 = 24.3` months. Total `35 + 24.3 = 59.3`. The parallel plan costs about 4.2 months against a plain rebuild (55.1) and buys players, proof and a story, as in the lecture's section 3.
</details>

22. *Week 4 · analysis.* For question 19, you can spend a month improving one estimate. Which matters more to the decision, an error of ±0.5 in `m` or an error of ±30% in `T_r`? Use the formulas' slopes.

<details>
<summary>Answer and worked solution</summary>

**Answer:** they are close, and `T_r` is slightly larger. A ±0.5 error in `m` moves `T_patch` by about ±7.3 months. A ±30% error in `T_r` moves `T_rebuild` by ±8.4 months. The current margin is 8.5 months, so either error can nearly erase it.

`∂T_patch / ∂m = G × φ / F = 500 × 0.35 / 12 = 14.6` months per unit of `m`, so ±0.5 is ±7.3. `∂T_rebuild / ∂T_r = 1`, so ±30% of 28 is ±8.4. Because `T_r` estimates tend to run long rather than short, the asymmetric risk is on the rebuild side. A good answer recommends measuring `m` on two more structural fixes and padding `T_r` before deciding.
</details>

23. *Week 4 · critique.* A studio's gap list is 70% "the subscription is too expensive for the content" and 30% content and tuning. Its lead engineer argues for a rebuild "because the problem is fundamental." Use the model and one case from the lecture to respond.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the pricing part has `φ = 0` for engineering, and neither path in the model touches it. Change the business model first (The Elder Scrolls Online's March 2015 move to buy-to-play is the lecture's example), then treat the 30% content gap as a patch job.

"Fundamental" describes how the problem feels, not where it lives. A rebuild spends `T_r` months on the foundation and leaves the price exactly where it was. The model recommends a rebuild only when `φ × m` is large, and here `φ` for the code is small.
</details>

## Week 5: Case, Star Wars Galaxies and the NGE

24. *Week 5 · compute.* An MMO with `S₀ = 150,000` subscribers plans a redesign. Its segments (share, departure share) are crafters (0.30, 0.40), entertainers (0.15, 0.50), combat players (0.40, 0.10) and collectors (0.15, 0.30). Compute `D`, the immediate loss `L`, and each segment's loss.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `D = 0.28`, `L = 42,000`. Crafters lose 18,000, entertainers 11,250, combat players 6,000, collectors 6,750.

`D = 0.30 × 0.40 + 0.15 × 0.50 + 0.40 × 0.10 + 0.15 × 0.30 = 0.12 + 0.075 + 0.04 + 0.045 = 0.28`. `L = 0.28 × 150,000 = 42,000`. The largest segment, combat players, loses the fewest.
</details>

25. *Week 5 · compute.* For question 24, the redesign brings `a = 18,000` trial players a month, of whom `r = 20%` stay. Churn among remaining players is `g_new = 2,500` a month, and the team claims the game would lose `g_old = 3,000` a month without the change. When does the redesign break even? What if `g_old` is really 0?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about month 10.2. With `g_old = 0`, about month 38.

The gap closes at `18,000 × 0.20 − 2,500 + 3,000 = 4,100` a month, so `t* = 42,000 / 4,100 = 10.2`. With `g_old = 0` it closes at `1,100` a month, so `t* = 42,000 / 1,100 = 38.2`. Most of the case rests on the counterfactual decline, which is the number the team can least observe.
</details>

26. *Week 5 · compute.* In question 25 (with `g_old = 3,000`), what retention `r` does the redesign need to break even within 12 months?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 16.7%.

The gap must close at `42,000 / 12 = 3,500` a month. `18,000 × r − 2,500 + 3,000 = 3,500` gives `r = 3,000 / 18,000 = 0.167`.
</details>

27. *Week 5 · compute.* Crafters and entertainers are hubs. Using question 24's numbers and a second-round rate `h = 0.5`, compute the second-round loss and the new total loss. With question 25's gap-closing rate, when does the redesign now break even?

<details>
<summary>Answer and worked solution</summary>

**Answer:** second round about 6,800 players, total about 48,800, break-even about month 11.9.

Hub share lost `= (18,000 + 11,250) / 150,000 = 0.195`. Non-hubs remaining after round one: combat `60,000 × 0.9 = 54,000` and collectors `22,500 × 0.7 = 15,750`, so 69,750. Second round `= 0.5 × 0.195 × 69,750 = 6,800.6`. Total `42,000 + 6,801 = 48,801`, and `48,801 / 4,100 = 11.9` months. Protecting the hubs is worth more than their headcount suggests.
</details>

28. *Week 5 · analysis.* A game makes three changes in a year, losing 8%, then 15% of those left, then 20% of those left. What share of the original base remains? A designer adds the three losses and says the game lost 43%. What is wrong, and in which direction might the true loss differ from even your corrected number?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `0.92 × 0.85 × 0.80 = 0.6256`, so 62.6% remains and the combined loss is 37.4%, not 43%.

Each change can only drive away players the earlier ones left, so losses compound instead of adding. The lecture adds a warning in the other direction. The players who stayed through one change are often the ones who valued what the next change removes, so the independent `D₂` and `D₃` are optimistic, and the true loss may be above 37.4%.
</details>

29. *Week 5 · critique.* A student's case analysis says, "The NGE cost Star Wars Galaxies 60% of its players within a month." Using the lecture's section 5, explain what the public record supports and rewrite the sentence.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the public record has no subscriber series. It has SOE's August 2005 claim of one million boxed copies sold, an unconfirmed early-2006 report of 10,363 players on one Friday night that Smedley denied, and agreement across sources on the sequence of events and the size of the backlash. No percentage loss is supported.

A defensible rewrite: "The public record shows a large backlash, refunds offered for the expansion, and later statements by SOE's president calling the changes mistakes, but no reliable subscriber numbers. The model can say what had to be true for the NGE to pay (a real decline without it, and new players who stayed). The record cannot say whether either held."
</details>

## Week 6: Case, duplication exploits after launch (New World 2021)

30. *Week 6 · compute.* A find log shows 9 value-path exploits by week 3 and 15 by week 6. Fit `a` and `b` by the two-point method. How many are still hidden at week 6?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `a = 27`, `b ≈ 0.135` per week, 12 still hidden.

`x = 15 / 9 − 1 = 0.667`. `a = 9 / (1 − 0.667) = 27`. `b = −ln(0.667) / 3 = 0.1352`. `R(6) = 27 × 0.667² = 12`. Only 56% of the game's exploits have been found, and the curve is flattening slowly.
</details>

31. *Week 6 · compute.* For question 30, what is the chance of at least one new exploit in the week after week 6?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 78%.

`E = 12 × (1 − e^(−0.1352)) = 12 × 0.1264 = 1.517`. `P = 1 − e^(−1.517) = 0.781`. Reopening trading now means betting against a better than three-in-four chance of another exploit.
</details>

32. *Week 6 · compute.* Use the lecture's fit (`a = 12`, `b = 0.3466` per week). With a risk limit of 10%, trading reopens at about week 10.1. At which week does it reopen with a limit of 20%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about week 7.95, roughly two weeks earlier.

Each remaining exploit is found in a given week with chance `1 − e^(−0.3466) = 0.2929`. Reopen when `R × 0.2929 < −ln(0.8) = 0.2231`, so `R < 0.762`. With `R(t) = 12 × 2^(−t/2)`, `t = 2 × log₂(12 / 0.762) = 7.95`. The risk limit is a policy choice. Doubling it buys two weeks of trading and a one-in-five weekly chance of a new exploit.
</details>

33. *Week 6 · compute.* In the lecture's game, a release in week 4 adds a new value path with 5 exploits of its own, found at the same rate. What is the hidden count at week 6 and the chance of a new exploit in the following week? When does trading reopen at a 10% limit?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 4.0 hidden, 69% chance, reopening at about week 12.95 instead of 10.1.

`R(6) = 12 × e^(−0.3466 × 6) + 5 × e^(−0.3466 × 2) = 1.5 + 2.5 = 4.0`. `E = 4.0 × 0.2929 = 1.172`, `P = 1 − e^(−1.172) = 0.690`. For reopening, `R(t) = 12 × 2^(−t/2) + 5 × 2^(−(t−4)/2) = 32 × 2^(−t/2)`, and it must fall below 0.360, so `t = 2 × log₂(32 / 0.360) ≈ 12.95`. The release cost almost three weeks of closed trading.
</details>

34. *Week 6 · analysis.* By week 4 after launch, 250,000 active players hold 1,500 coins each on average. By week 40, 80,000 active players hold 15,000 each. A dupe creates 45 million coins. How much does it add to the money supply at each time, and what else makes the week 4 dupe worse?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 12% at week 4 (`M` = 375 million) against 3.75% at week 40 (`M` = 1.2 billion), 3.2 times the damage.

`45 / 375 = 0.12` and `45 / 1,200 = 0.0375`. Section 3 adds two reasons. Prices are still being discovered at launch, so a duped flood is hard to tell from normal volatility, and the most dedicated players, who set early prices and lead guilds, are the most exposed. This is why a launch plan tightens caps and logging in the first weeks.
</details>

35. *Week 6 · analysis.* A team's find log shows 7 exploits by week 2 and 14 by week 4. The producer asks when trading can reopen. What does the model say, and what should the team do?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `x = 14 / 7 − 1 = 1`, so the curve shows no flattening and the two-point fit cannot estimate `a`. The honest answer is that the model cannot promise a quiet week yet.

The team should keep the affected paths closed or tightly capped, keep the find log, fit by least squares once five or six weeks exist, and hold any release that adds a value path. A good answer also checks whether the player population changed, because a falling searcher count lowers `b` and can make a later quiet week look safer than it is.
</details>

36. *Week 6 · critique.* A student's case analysis says, "Fitting New World's public record gives `a` = 9 exploits, so Amazon reopened trading at the right time." What is wrong, and what can the public record support?

<details>
<summary>Answer and worked solution</summary>

**Answer:** the public record does not list every exploit found, so there is no honest find log to fit, and a fitted `a` would be invented precision.

The record supports the model's shape. Finds came quickly after launch (days 20, 30 and 35 in the lecture's table), a patch did not end them, a different system (housing) produced a fresh dupe after the coin dupe was fixed, and the team's own database change on 25 November needed the same response kit. The record also does not say on what criterion trading reopened, which is itself a finding.
</details>

## Week 7: Case, classic and legacy servers

37. *Week 7 · compute.* With the lecture's constants (`J = 1,000`, `c = 5%`, `k = 2`, `e = 0.2`), a realm is at 62/38. What share of newcomers picks the bigger faction, and what is the smaller faction's total weekly leaving rate?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 72.7% of newcomers, and 9.8% a week.

`p = 0.62² / (0.62² + 0.38²) = 0.3844 / 0.5288 = 0.727`. `gap = |2 × 0.62 − 1| = 0.24`, so the smaller faction loses `5% + 0.2 × 0.24 = 9.8%`.
</details>

38. *Week 7 · compute.* Step one week from `A = 6,000`, `B = 4,000` with the lecture's constants. What are the new `A`, `B` and A's share?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `A` ≈ 6,392, `B` ≈ 3,948, share 61.8%.

`s = 0.6`, `p = 0.36 / 0.52 = 0.692`, so 692 newcomers to A and 308 to B. `gap = 0.2`, so B loses `5% + 4% = 9%`. `A = 6,000 × 0.95 + 692.3 = 6,392.3`. `B = 4,000 × 0.91 + 307.7 = 3,947.7`. The share rises from 60% to 61.8% in one week.
</details>

39. *Week 7 · code.* Using the lecture's `week` function (reproduced here), what does this print?

```python
def week(A, B, J=1000, c=0.05, k=2, e=0.2):
    s = A / (A + B)
    p = s**k / (s**k + (1 - s)**k)
    gap = abs(2 * s - 1)
    leave_A = c + (e * gap if s < 0.5 else 0)
    leave_B = c + (e * gap if s > 0.5 else 0)
    return A * (1 - leave_A) + J * p, B * (1 - leave_B) + J * (1 - p)

def first_week(threshold, **kw):
    A, B = 5500, 4500
    for w in range(200):
        if A / (A + B) >= threshold:
            return w
        A, B = week(A, B, **kw)

print(first_week(0.7), first_week(0.9))
print(first_week(0.7, k=1.5, e=0.1), first_week(0.9, k=1.5, e=0.1))
```

<details>
<summary>Answer and worked solution</summary>

```
9 16
18 32
```

The first line is the lecture's realm: 70/30 in week 9 and 90/10 in week 16. Weakening both loops (`k = 1.5`, `e = 0.1`) doubles the time to each threshold, but the realm still tips. Any `k > 1` or `e > 0` leaves the even split unstable, so softer parameters buy time, not safety.
</details>

40. *Week 7 · analysis.* A designer proposes an underdog bonus that lowers `k` to 0.5, and leaves `e = 0.2`. At `s = 0.6`, what share of newcomers picks the bigger faction? Explain, from the model, why the realm can still tip.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `p = √0.6 / (√0.6 + √0.4) = 0.551`, so the bigger faction gets 55% of newcomers while holding 60% of the realm. Newcomers now pull toward even.

The bonus acts only on newcomers, about 1,000 players a week. The outnumbered penalty removes `e × gap` of the whole smaller faction every week. At 60/40 that is an extra 4% of about 4,000 players, 160 a week, on top of normal churn, and it grows as the gap grows. The lecture's run with `k = 0.5` and `e = 0.2` still reaches 70/30 within about half a year. A bonus needs a companion change that makes the smaller side less miserable, so `e` falls.
</details>

41. *Week 7 · compute.* Three fresh realms hold 5,000, 3,000 and 2,000 players. Newcomers choose realms by `pop^k / Σ pop^k` with `k = 2`. What share of newcomers does each realm get, and what does that mean for the smallest?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 65.8%, 23.7% and 10.5%.

`5,000² : 3,000² : 2,000² = 25 : 9 : 4`, out of 38. The smallest realm holds 20% of the players and gets 10.5% of the newcomers, so it shrinks relative to the others every week, and MMO301's empty-realm spiral then raises its churn. If the technology can hold a large realm, finishing the concentration (as Blizzard's 2025 mega realms did) can be the right answer. If it cannot, plan the merge before the spiral does its work.
</details>

42. *Week 7 · design.* You launch a fresh legacy PvP realm. Choose between a day-one creation lock at 55%, a transfer price that rises with faction share, and a monthly reshuffle in the style of Guild Wars 2's World Restructuring. For your choice, name the model parameter it changes, the social tie it breaks, and the dashboard alert that goes with it.

<details>
<summary>Answer and worked solution</summary>

**Answer (one defensible choice):** a day-one creation lock at 55%. It overrides the newcomer rule for the dominant faction. It breaks the tie between new players and friends already on the big side. Alert: faction share above 55% for 24 hours on any PvP realm, owned by the live-ops lead, who confirms the lock is active.

Any of the three can be defended. A rising transfer price lowers `k` for transfers and breaks the tie of guilds that move in stages. A reshuffle resets `s` to 50% and breaks rivalries and server identity. A strong answer notes that a lock must start early (the lecture's lock from week 0 holds the realm between 53% and 56% all year and costs about 16% of its year-end population), and that on a PvE realm the imbalance costs little.
</details>

## Week 8: Case, EVE's large-scale events

43. *Week 8 · compute.* With the lecture's constants (`a = 0.3` ms, `b = 1` µs, `C = 1`, floor 0.1), what is the game speed at 1,200 pilots and at 3,000 pilots? How many real minutes does one game-minute take at each?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0.556 at 1,200 pilots (1.8 real minutes per game-minute) and 0.101 at 3,000 pilots (about 9.9 real minutes).

At 1,200, `W = 0.0003 × 1,200 + 0.000001 × 1,200² = 0.36 + 1.44 = 1.80`, so `f = 1 / 1.8 = 0.556`. At 3,000, `W = 0.9 + 9.0 = 9.9`, so `f = 0.101`, just above the floor.
</details>

44. *Week 8 · compute.* At how many pilots does the speed reach the 0.1 floor on the lecture's node? On a node twice as fast (`C = 2`)?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 3,016 pilots with `C = 1`, about 4,325 with `C = 2`.

The floor is reached when `W = C / 0.1`. For `C = 1`, solve `0.000001 n² + 0.0003 n = 10`, so `n = (−0.0003 + √(0.0003² + 4 × 0.000001 × 10)) / (2 × 0.000001) = 3,016`. For `C = 2`, the right side is 20 and `n = 4,325`. Because `W` grows with `n²`, doubling `C` raises the floor headcount by only about 43%, yet the lecture's battle ends 2.9 times sooner, because the fight spends far less of its objective at the floor.
</details>

45. *Week 8 · compute.* A siege starts with 1,500 pilots, adds 25 per real minute up to a pool of 5,000, and needs `G = 45` game-minutes. Estimate its real length with the two-phase method, then compare with the model's answer of 393 minutes.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the floor comes at about minute 61, with about 11.8 game-minutes done. The remaining 33.2 game-minutes at 0.1 take about 332 real minutes, for about 393 in total, matching the model.

Pilots reach about 3,016 after `(3,016 − 1,500) / 25 ≈ 61` minutes. Summing `f` minute by minute over that stretch gives 11.8 game-minutes. `(45 − 11.8) / 0.1 = 332`, and `61 + 332 = 393`. The model ends with the pool full at 5,000 pilots and about 28,600 pilot-hours. An undilated server would finish in 45 minutes.
</details>

46. *Week 8 · analysis.* In the lecture's battle, `G = 60` lasts 419 real minutes, `G = 90` lasts 719, and `G = 120` lasts 1,019. Explain the constant step of 300 real minutes per 30 game-minutes, and say what it means for a designer setting structure hit points.

<details>
<summary>Answer and worked solution</summary>

**Answer:** every version reaches the floor at the same minute with the same work done, so each extra game-minute is fought at 0.1 speed and costs 10 real minutes.

The opening (arrivals, the speed falling, the floor at about minute 101 with 28.3 game-minutes done) is identical for all three objectives. After that the speed is fixed at 0.1, so 30 more game-minutes add exactly 300 real minutes. For a designer, structure hit points in a dilated game are a capacity number. Past the floor, every extra minute of shooting becomes ten minutes of real time with the whole fleet in the system.
</details>

47. *Week 8 · analysis.* In the lecture's model, raising arrivals from 20 to 30 per minute makes the fight last 478 minutes instead of 419, while halving the pool from 6,000 to 3,000 changes it only to 416. Explain both results with the loop.

<details>
<summary>Answer and worked solution</summary>

**Answer:** faster arrivals push `n` to the floor sooner with fewer game-minutes done, so more of the objective is fought at 0.1. The pool matters little because, once the fight is at the floor, extra pilots do not slow it further in this model.

The length is set mostly by how much of `G` is left when the floor arrives. `r` controls that directly. The pool caps the headcount, but in the lecture's battle both pools are above the floor headcount of about 3,016, so the time at the floor barely changes. What the pool does change is load past the floor, where MMO302's backlog grows and commands arrive late, and the pilot-hours, which fall by about 40%.
</details>

48. *Week 8 · design.* Your MMO has a monthly world boss that players can summon. The boss fight takes 30 game-minutes, players arrive at 40 a minute once the summon is announced, and the server dilates like the lecture's node. Name two levers from the lecture's section 3 table you would pull, say who controls each, and state the real-time brake you would publish to players.

<details>
<summary>Answer and worked solution</summary>

**Answer (one defensible design):** lower `r` with an arrival rule (for example, the summon opens the zone to new entrants for 15 real minutes, then closes it), and keep `G` small, because each game-minute past the floor costs 10 real minutes. Both are designer levers. Brake: "The boss despawns 90 real minutes after the summon, whatever its health", published in advance, with the note that it favours the side that is ahead when the clock runs out.

The lecture's table ranks objective size and arrival friction as the strongest design levers, and capacity as the operator's lever when players give warning. A real-time deadline caps the loop and decides outcomes, so it must be public before the event, not improvised during it.
</details>

## Week 9: Communication during crises

49. *Week 9 · compute.* Use the lecture's log of 20 outages (15, 20, 25, 30, 30, 35, 40, 45, 50, 60, 60, 75, 90, 105, 120, 150, 180, 240, 360, 600 minutes). With `c_late = 4` and `c_early = 1`, what is the critical ratio, and which time should you announce? With `c_late = 1` and `c_early = 3`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** ratio 0.8, announce 150 minutes. Ratio 0.25, announce 30 minutes.

`4 / (4 + 1) = 0.8`. The smallest duration with at least 80% of the log at or below it is the `ceil(0.8 × 20) = 16`th value, 150. `1 / (1 + 3) = 0.25` picks the 5th value, 30. A studio whose players leave for another game when told "four hours" has a high `c_early` and should announce early.
</details>

50. *Week 9 · compute.* With `c_late = 2` and `c_early = 1`, compute by hand the expected cost of announcing 180 minutes on the lecture's log. Compare it with the best announcement's cost of 141.5.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 162.5, about 15% worse than the best (105 minutes).

Three outages ran past 180 (240, 360, 600), late by 60, 180 and 420, total 660, so lateness costs `2 × 660 / 20 = 66.0`. The other 17 finished at or before 180, early by a total of 1,930 minutes, so the early cost is `1,930 / 20 = 96.5`. The total is `162.5`. Announcing well past the critical ratio wastes player time on the many short outages.
</details>

51. *Week 9 · compute.* An outage has lasted 90 minutes. Using the lecture's log, how long do the outages still running have to go on average? Compare with the 116.5 minutes at the start and explain what it means for the next announcement.

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 161 minutes, more than at the start.

The outages longer than 90 are 105, 120, 150, 180, 240, 360 and 600, with 15, 30, 60, 90, 150, 270 and 510 minutes to go. The total is 1,125, and `1,125 / 7 = 160.7`. In a heavy-tailed log, an outage that has outlasted the easy cases is more likely to be a hard one. The next announcement should come from the outages still running, not add a fixed 30 minutes.
</details>

52. *Week 9 · compute.* Compare the lecture's two extension policies on a 240-minute outage. Policy A announces 60 minutes and adds 30 on each miss. Policy B announces the 2/3 quantile and, on each miss, re-forecasts from the logged outages longer than the last announcement. List each policy's announcements and count the broken promises.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Policy A announces 60, 90, 120, 150, 180, 210, 240 and breaks 6 promises. Policy B announces 105, then 240, and breaks 1.

Policy B's first announcement is the 14th value, 105. The outages longer than 105 are 120, 150, 180, 240, 360 and 600. Their 2/3 quantile is the `ceil(4) = 4`th value, 240. The outage ends at 240, so the second promise holds. Fixed small increments assume the end is always near, which is rarely true in a heavy-tailed log.
</details>

53. *Week 9 · code.* What does this print?

```python
import math

LOG = [15, 20, 25, 30, 30, 35, 40, 45, 50, 60,
       60, 75, 90, 105, 120, 150, 180, 240, 360, 600]

def quantile(log, q):
    s = sorted(log)
    return s[math.ceil(q * len(s)) - 1]

def mean_left(log, t):
    rest = [d - t for d in log if d > t]
    return sum(rest) / len(rest)

print(quantile(LOG, 0.5), quantile(LOG, 2 / 3), quantile(LOG, 0.8))
print(round(mean_left(LOG, 30), 1), round(mean_left(LOG, 90), 1))
```

<details>
<summary>Answer and worked solution</summary>

```
60 105 150
117.3 160.7
```

`ceil(10) = 10`, `ceil(13.33) = 14` and `ceil(16) = 16` pick the 10th, 14th and 16th values. After 30 minutes, the 15 outages still running have 1,760 minutes to go in total, 117.3 on average, already above the 116.5 at the start.
</details>

54. *Week 9 · design.* A database restore has been running for 90 minutes. Your log of past restores is 60, 75, 90, 300 and 480 minutes. Compute the average time still to go, and write the next player update's time line (one sentence) following the lecture's section 3.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the restores still running after 90 minutes are 300 and 480, with 210 and 390 to go, an average of 200 minutes.

With two relevant records the forecast is shaky, so the update should promise the next update, not an end time. For example: "The restore is still running and is taking longer than most; we will post the next update at 21:00 UTC (22:00 CET) whether or not it has finished." That keeps the one promise the team controls.
</details>

55. *Week 9 · critique.* During a suspected breach, a studio's first player message says, "We will share details once our investigation is complete." Critique it against the lecture's section 3 and the GDPR timing rule, and rewrite the first sentence.

<details>
<summary>Answer and worked solution</summary>

**Answer:** it answers none of the three player questions and promises nothing the team controls. Under GDPR Article 33 the studio must notify the supervisory authority without undue delay and, where feasible, within 72 hours of becoming aware of a personal data breach. Sony's 2011 week of silence drew criticism from officials for this reason.

A rewrite: "We are investigating a possible security breach affecting account data; we do not yet know what, if anything, was taken, and as a precaution we recommend changing your password now. Next update at 18:00 UTC." It states what is happening, what players should do, what is unknown, and when the next update comes.
</details>

## Week 10: Recovery strategies

56. *Week 10 · compute.* An MMO's launch window drew 50,000 Steam reviews at 30% positive. After the fix, 80% of new reviews are positive and 2,500 arrive a month. What is the all-time share after 12 months, and how many months until it reaches 60%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 48.75% after 12 months. 60% takes 75,000 new reviews, 30 months.

After 12 months, `N₁ = 30,000`. `S_all = (50,000 × 0.30 + 30,000 × 0.80) / 80,000 = (15,000 + 24,000) / 80,000 = 0.4875`. For 60%, `N₁ = 50,000 × (0.60 − 0.30) / (0.80 − 0.60) = 75,000`, and `75,000 / 2,500 = 30` months.
</details>

57. *Week 10 · analysis.* For question 56, a relaunch event brings 30,000 reviews at 80% in its first month after the fix. What is the all-time share after that month? Compare with question 56, and say what the event cannot do.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 48.75%, the same as 12 months of trickle.

The mixture depends only on how many new reviews arrive, not when. `(15,000 + 30,000 × 0.80) / 80,000 = 0.4875`. Volume is cheaper than time. The event cannot lift the all-time share above `r = 80%`, and if `r` were low it would only add volume to the old story.
</details>

58. *Week 10 · compute.* For question 56, how many reviews does it take to reach 70% all-time? Compare the step from 60% to 70% with the step to 60%.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 200,000 reviews, 80 months. The last 10 points cost 125,000 reviews, 1.7 times everything before them.

`N₁ = 50,000 × 0.40 / 0.10 = 200,000`. The denominator `r − T` shrinks from 0.20 to 0.10, so each point closer to `r` costs more than the last.
</details>

59. *Week 10 · compute.* A game sold 2,000,000 copies and has 150,000 monthly active players. A recovery update reactivates 3% of the lapsed pool, and 45% of those returners are still playing a month later. How many net players does it add after a month? What should the update's first hour be designed for?

<details>
<summary>Answer and worked solution</summary>

**Answer:** lapsed pool 1,850,000, returners 55,500, about 24,975 still playing after a month.

`L = 2,000,000 − 150,000 = 1,850,000`. `0.03 × 1,850,000 = 55,500`. `0.45 × 55,500 = 24,975`. Most of the update's audience are people who left. Their first hour needs a catch-up path, a summary of what changed and a fix for progress lost to rollbacks, or `ρ` is spent.
</details>

60. *Week 10 · analysis.* Write Steam's lifetime score, Steam's 30-day score and a platform that weights ratings with a half-life of 90 days in the lecture's general form `Σ w(age) × x / Σ w(age)`. Which one does a stranger usually read first, and which does a returning player care about?

<details>
<summary>Answer and worked solution</summary>

**Answer:** lifetime `w = 1` for every review. 30-day `w = 1` if the review is 30 days old or less, else 0. Half-life 90 days `w = 0.5^(age / 90)`, with age in days.

A stranger deciding whether to buy often reads the all-time score first, which remembers the launch. A returning player cares about the recent score and patch notes, which reflect the build as it is. A recovery can succeed with lapsed players while the store page still fails strangers. The exponential weight sits between Steam's two scores: a short half-life approaches the 30-day box, a very long one approaches the lifetime score.
</details>

61. *Week 10 · design.* Your all-time share is 45% and `r` is only 70%. You can fund either a free weekend (12,000 reviews at 70%) or three months of fixes expected to raise `r` to 85% with no extra volume. Which do you fund first, and what single number decides it?

<details>
<summary>Answer and worked solution</summary>

**Answer:** fix first, then buy volume. The deciding number is `r` against the target.

Volume at `r = 70%` moves the all-time share toward 70% at best, and a low `r` says current players are still unhappy, so word of mouth and the recent score stay weak. Raising `r` to 85% lifts the ceiling for every later review, and a free weekend after that buys more per review. The lecture's rule is not to argue with the recent score.
</details>

## Week 11: Shutdowns and emulation communities

62. *Week 11 · compute.* A fan team has 30 volunteers at 7 hours a week. The game has `B = 2,500` behaviours, `w = 50` hours each with evidence, `g = 5`, and evidence `q = 0.75`. How long is the full rebuild, and when is the faithful part done?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 22.9 years in all. The faithful part is done at about 8.6 years.

`V = 210`. Bracket `0.75 + 5 × 0.25 = 2.0`. `H = 2,500 × 50 × 2.0 = 250,000` hours, `250,000 / 210 = 1,190` weeks, 22.9 years. Faithful part `2,500 × 0.75 × 50 / 210 = 446` weeks, 8.6 years. The guessed quarter of the game takes almost twice as long as the recorded three quarters.
</details>

63. *Week 11 · compute.* In question 62, at what evidence share does the guessed tail take exactly as long as the faithful part? How many weeks does each percentage point of `q` add to the full rebuild?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `q = g / (1 + g) = 5 / 6 ≈ 0.833`. Each point adds about 23.8 weeks.

The tail equals the faithful part when `q = g × (1 − q)`. Per point, `ΔT = 0.01 × B × w × (g − 1) / V = 0.01 × 2,500 × 50 × 4 / 210 = 23.8` weeks. A capture window that raises `q` by 10 points before the servers close saves about four and a half years.
</details>

64. *Week 11 · compute.* In question 62, the studio could release server binaries with a hosting licence, giving `w_s = 4` hours a behaviour, but licensor consent is rated at 40%. The fallback is a capture window that raises `q` to 0.9. Compute `T` with source, `T` with the fallback, and the expected `T` of "try the licence, fall back to the capture window".

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 0.9 years with source, about 16.0 years with the capture window, and about 10.0 years expected.

Source: `2,500 × 4 / 210 = 47.6` weeks, 0.92 years. Capture window: bracket `0.9 + 5 × 0.1 = 1.4`, `H = 175,000`, 833 weeks, 16.03 years. Expected: `0.4 × 0.92 + 0.6 × 16.03 = 9.98` years. The capture window costs almost nothing and should run in any case, and the licence request must start while the team that knows the code still exists.
</details>

65. *Week 11 · analysis.* Place Asheron's Call (servers off 31 January 2017) and Ryzom (source released under the AGPL on 6 May 2010) on the rebuild model. For each, name the parameter that changed and in which direction.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Asheron's Call raised `q` in the last weeks. Ryzom set `w_s` for any future community before any shutdown.

ACEmulator's repository was created on 16 January 2017, fifteen days before the servers closed, and its organisation hosts a packet capture tool and capture data used for the world database. Players recording sessions raised `q` while it could still be raised, and the eras with fewer recordings are the slow tail. Ryzom's operator released client and server source while the game was running, which moves any revival onto the source line with no leak, capture or guessing needed.
</details>

66. *Week 11 · critique.* A studio executive says, "If we release nothing, the game is gone and our brand is protected." Use the lecture's cases to respond in three sentences.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Meridian 59, Star Wars Galaxies and City of Heroes all had their server code leak after shutdown, so releasing nothing mostly decides whether the studio has a say. City of Heroes shows the pattern: servers off in November 2012, code public in April 2019 and public servers within days, then a hosting licence in January 2024. A studio that plans a handover (a capture window at least, a licence if the paperwork allows) keeps control of its brand rules and its players' safety instead of leaving both to an unlicensed revival years later.
</details>

## Week 12: Writing a post-mortem

67. *Week 12 · compute.* In a set of 16 troubled and 24 smooth launches, "no rollback drill before launch" appears in 10 troubled and 6 smooth. Compute `f_T`, `f_S` and `L`. What happens to `L` if one more smooth launch had the factor?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `f_T = 62.5%`, `f_S = 25%`, `L = 2.5`. With one more smooth launch, `L = 0.625 / (7 / 24) = 2.14`.

`10 / 16 = 0.625` and `6 / 24 = 0.25`, so `L = 2.5`. One launch moves `f_S` by about 4 points and `L` by about 0.36. Report the counts (10/16 against 6/24) next to `L` so readers can judge the noise.
</details>

68. *Week 12 · compute.* A factor appears in 5 of 20 troubled launches and 0 of 25 smooth ones. What is `L` as written? Recompute it after adding one half to each of the four counts.

<details>
<summary>Answer and worked solution</summary>

**Answer:** infinite as written. About 13.6 with the correction.

Troubled with it 5.5, without 15.5, so `f_T = 5.5 / 21 = 0.262`. Smooth with it 0.5, without 25.5, so `f_S = 0.5 / 26 = 0.0192`. `L = 0.262 / 0.0192 = 13.6`. Report the raw counts next to it and say that you corrected them.
</details>

69. *Week 12 · analysis.* In the lecture's 40-launch set, "no full-scale load test" appears in 12 of 20 troubled and 3 of 20 smooth launches (`L = 4.0`), and "day-one queue over an hour" in 14 of 20 and 13 of 20 (`L = 1.08`). Recompute each `L` if `b` moves by one launch in either direction. Which verdict survives the noise?

<details>
<summary>Answer and worked solution</summary>

**Answer:** load test: `L` = 3.0 or 6.0, above 3 either way, so it stays a strong candidate. Queue: `L` = 1.0 or 1.17, near 1 either way, so it stays "no lesson".

`0.60 / 0.20 = 3.0` and `0.60 / 0.10 = 6.0`. `0.70 / 0.70 = 1.0` and `0.70 / 0.60 = 1.17`. Neither verdict flips, but the size of the load-test contrast is uncertain by a factor of two, which is why a high `L` is a filter for a closer look, not a verdict.
</details>

70. *Week 12 · compute.* A launch post-mortem says the peak world queue at hour 3 was 71% above plan. Use the lecture's 10-world launch from week 2 as the plan (4,500 at hour 3). Actual arrivals were 20% above forecast in every phase, and launch-night sessions averaged 208 minutes instead of 160. Compute the hour-3 queue with each error alone and with both. Which input explains more of the gap?

<details>
<summary>Answer and worked solution</summary>

**Answer:** arrivals alone give 6,900, sessions alone 5,308, both together 7,708 (71% above plan). The arrivals error explains more.

Arrivals +20%: per world 144, 48 and 18 per minute, `μ = 25`. The fill adds `(144 − 100) × 40 = 1,760`, minutes 40 to 60 add `(144 − 25) × 20 = 2,380`, minutes 60 to 180 add `(48 − 25) × 120 = 2,760`, for 6,900. Sessions of 208 minutes: `μ = 4,000 / 208 = 19.2`, so `800 + (120 − 19.2) × 20 + (40 − 19.2) × 120 = 5,308`. Both: `1,760 + (144 − 19.2) × 20 + (48 − 19.2) × 120 = 7,708`. Tracing errors to inputs before calling the queue a surprise is step 2 of the lecture's template.
</details>

71. *Week 12 · critique.* Grade each lesson A, B or C with the lecture's scale, and fix the weakest.
   (a) "Our long queue made players angry."
   (b) "Launches without a rollback drill were 2.5 times as likely to be troubled in our 40-launch set (10/16 against 6/24), and DB201's restore model explains why an untested restore turns a data bug into a multi-day outage."
   (c) "After we doubled authentication, the bottleneck moved to world entry, as week 1 predicts."

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) C, (b) A, (c) B.

(a) is one case with no comparison, and a queue is partly a symptom of a big launch. (b) has a contrast with counts and a mechanism. (c) has a mechanism confirmed in one launch, with no contrast. A fixed (a) names a choice made before launch and a number: "We planned 10 worlds with no launch layers; week 2's model with our measured arrivals and sessions gives the hour-3 queue we saw. Grade B. Action: the capacity lead adds a layering trigger at 2,000 per world to the next plan, metric hour-3 wait."
</details>

72. *Week 12 · analysis.* A studio has shipped four launches, all troubled, all with the same publisher. Its post-mortem of the fifth concludes "the publisher is the cause." Name the bias and say what data would support or refute the claim.

<details>
<summary>Answer and worked solution</summary>

**Answer:** there is no comparison group, so `f_S` is undefined and nothing separates the publisher from anything else the five launches shared. This is the missing column from section 2, and the claim also invites hindsight bias.

The studio needs launches with other publishers, or smooth launches with this one, recorded with the same factor checklist before outcomes were known. Until then, the finding is a grade C question.
</details>

## Week 13: Launch plan workshop

73. *Week 13 · compute.* A register has three risks: R1 `p = 0.6`, `I = 80` k ph; R2 `p = 0.2`, `I = 150`; R3 `p = 0.04`, `I = 500`. The disaster line is `D = 200`. Compute `E[L]` and `P(L > 200)`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `E[L] = 98` k ph and `P(L > 200) = 0.155`.

`E = 0.6 × 80 + 0.2 × 150 + 0.04 × 500 = 48 + 30 + 20 = 98`. Losses above 200 need R3 (500) or R1 and R2 together (230). `P(not above 200) = (1 − 0.6 × 0.2) × 0.96 = 0.88 × 0.96 = 0.8448`, so `P = 0.1552`.
</details>

74. *Week 13 · analysis.* For question 73, you can buy one fix: cut R1's `p` to 0.2, or cut R3's `I` to 100. Compute `E` and `P(L > 200)` for each. Is there a disaster penalty `B` at which the containment fix is cheaper?

<details>
<summary>Answer and worked solution</summary>

**Answer:** R1 fix: `E = 66`, `P = 0.078`. R3 fix: `E = 82`, `P = 0.123`. The R1 fix is better on both numbers, so no `B` makes the R3 fix cheaper.

R1 fix: `E = 16 + 30 + 20 = 66`, and `P = 1 − (1 − 0.2 × 0.2) × 0.96 = 0.0784`. R3 fix: `E = 48 + 30 + 4 = 82`. With R3 at 100, the crossing combinations are R1 with R2 (230) and R2 with R3 (250), while R1 with R3 is 180 and does not cross. `P = 0.2 × (1 − 0.4 × 0.96) = 0.2 × 0.616 = 0.1232`. Containment cuts the tail only when it brings the risk's impact, and its combinations, under the line. Here R2 is inside every remaining disaster.
</details>

75. *Week 13 · compute.* A different register: R1 `p = 0.7`, `I = 60`; R2 `p = 0.3`, `I = 90`; R3 `p = 0.03`, `I = 800`; `D = 250`. Fix A cuts R1's `p` to 0.1. Fix B cuts R3's `I` to 100. Compute `E`, `P(L > 250)` and the worst possible week for each, and the penalty `B` at which the two plans cost the same.

<details>
<summary>Answer and worked solution</summary>

**Answer:** no fix: `E = 93`, `P = 0.03`. Fix A: `E = 57`, `P = 0.03`, worst week 950. Fix B: `E = 72`, `P = 0`, worst week 250. They tie at `B = 500`.

Only R3 can cross 250, since R1 and R2 together make 150. Fix A lowers the average by 36 and leaves the tail at exactly 3%. Fix B makes the worst week `60 + 90 + 100 = 250`, not above the line. Costs are `57 + 0.03B` and `72`, equal at `B = 500` k ph. Above that penalty, buy containment.
</details>

76. *Week 13 · compute.* Add a scenario row to question 73's register: "demand three times forecast", probability `s = 0.1`, under which R1 and R2 both fire. Outside it, R1 and R2 keep their overall rates. What are their probabilities outside the scenario, and what are `P(R1 and R2)` and `P(L > 200)` now?

<details>
<summary>Answer and worked solution</summary>

**Answer:** outside the scenario R1 has `p = 0.556` and R2 `p = 0.111`. `P(R1 and R2)` rises from 0.120 to 0.156, and `P(L > 200)` from 0.155 to 0.189. `E[L]` is unchanged at 98.

`(0.6 − 0.1) / 0.9 = 0.556` and `(0.2 − 0.1) / 0.9 = 0.111`. `P(both) = 0.1 + 0.9 × 0.556 × 0.111 = 0.156`. `P(L > 200) = 1 − (1 − 0.156) × 0.96 = 0.189`. The correlation leaves the average alone and fattens the tail, because the pair crosses the disaster line only when both fire.
</details>

77. *Week 13 · compute.* Use week 2's 10-world launch, where the per-world queue is 800 at minute 40 and grows by 95 a minute until minute 60, then by 15 a minute. A layering trigger fires when the queue passes a threshold and takes `T = 20` minutes to land.
   (a) With a threshold of 3,000 per world, when does it fire and land?
   (b) The team wants the layers live before the rush ends at minute 60. What is the highest threshold that achieves that?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) fires at minute 80, lands at minute 100. (b) about 800 per world, reached at minute 40.

(a) The queue is 2,700 at minute 60 and grows by 15 a minute, so it passes 3,000 at `60 + 300 / 15 = 80`, and `80 + 20 = 100`. That still cuts the shoulder before hour 3, but misses the rush. (b) `t_s + 20 ≤ 60` needs `t_s ≤ 40`, when the queue is 800 per world. The lead-time check `t_s + T ≤ t_h` sets the threshold, not the other way round.
</details>

78. *Week 13 · analysis.* In the lecture's worked example (`D = 300`), the expected-loss ranking picks M1+M2 and leaves the disaster chance at 6.9%. Move the disaster line to `D = 100`. Compute `P(L > 100)` for no fixes, M1+M2 and M3+M4, and explain why the choice of `D` must be agreed before the plan is costed.

<details>
<summary>Answer and worked solution</summary>

**Answer:** no fixes 0.367, M1+M2 0.088, M3+M4 0.359. At `D = 100`, the prevention pair now cuts the tail more than the containment pair.

At `D = 100`, R1 and R2 together (125) cross the line, so fixes to R1 and R2 matter for the tail. M3+M4 leaves R1 and R2 untouched and barely moves `P`. The line decides which risks count as disaster risks, so a team that chooses `D` after seeing the costs can pick the line that agrees with its favourite plan.
</details>

79. *Week 13 · critique.* A plan's trigger reads, "If authentication errors look bad, the team will discuss adding servers." Rewrite it in the lecture's six-part form and check its lead time, given that emergency servers take 45 minutes and the evening peak starts about 60 minutes after errors usually pass 2%.

<details>
<summary>Answer and worked solution</summary>

**Answer (one version):** signal, authentication error rate on the war-room dashboard. Threshold, above 2% for 5 minutes. Action, bring pre-warmed authentication servers online. Owner, operations lead, without a meeting. Lead time, 45 minutes. Stand-down, error rate below 0.5% for 2 hours.

Check: the signal crosses at `t_s`, the servers land at `t_s + 45`, and the peak starts at about `t_s + 60`, so `t_s + T ≤ t_h` holds with 15 minutes to spare. The original has no number, no owner and no stand-down, and "the team will discuss" is a meeting, not a trigger.
</details>

## Week 14: Presentations

80. *Week 14 · compute.* Use the lecture's scorecard (weights 3, 2, 2, 2, 2, 1 for capacity, beta exposure, restore drill, kill switches, player comms and low-end platform; gates of 0.7 on capacity, restore drill, kill switches and low-end platform). A plan scores 0.9, 0.6, 0.8, 0.75, 1.0 and 0.65. Compute `S`, `G` and the gate result, and give the verdict under each of the three rules with a launch line of 0.8.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `S ≈ 0.804`, `G ≈ 0.793`, the low-end platform gate fails. Average rule go, geometric rule no-go, gated rule no-go.

`S = (2.7 + 1.2 + 1.6 + 1.5 + 2.0 + 0.65) / 12 = 9.65 / 12 = 0.804`. `G = Π sᵢ^(wᵢ/12) = 0.793`. The low-end score 0.65 is below its 0.7 gate. Beta exposure at 0.6 has no gate, so it does not fail anything.
</details>

81. *Week 14 · compute.* For question 80, what is the smallest total score increase that makes the plan "go" under the gated rule? What are `S` and `G` after the fix?

<details>
<summary>Answer and worked solution</summary>

**Answer:** raise the low-end platform from 0.65 to 0.70, an increase of 0.05. Then `S ≈ 0.808`, `G ≈ 0.797`, and every gate passes.

The only failed gate is the low-end platform, and `S` is already above 0.8, so the fix is exactly the gap to that gate. `S = 9.70 / 12 = 0.808`. The geometric score stays just under 0.8, so the geometric rule would still say no-go. The fix must be measured (for example, a frame-rate target met on the low-end build), not a changed opinion.
</details>

82. *Week 14 · compute.* With the lecture's weights, what is the highest weighted average a plan can reach with the restore drill at zero? With capacity at zero? Can either launch under the average rule at 0.8?

<details>
<summary>Answer and worked solution</summary>

**Answer:** restore drill at zero, `1 − 2/12 = 0.833`, which can launch. Capacity at zero, `1 − 3/12 = 0.75`, which cannot.

A compensatory score hides a zero in proportion to its weight. The restore drill is gated, so the gated rule stops the first plan whatever its average.
</details>

83. *Week 14 · analysis.* A plan scores 0.7 on every criterion of the lecture's scorecard. Another scores 1.0 everywhere except the low-end platform at 0.05. Compute `S`, `G` and the gate result for both, and give each verdict under the three rules at 0.8. What does the pair show?

<details>
<summary>Answer and worked solution</summary>

**Answer:** even plan: `S = G = 0.70`, all gates pass (0.7 meets 0.7), no-go under the average and geometric rules, and no-go under the gated rule because `S` is below the line. Spiky plan: `S = 0.921`, `G = 0.779`, low-end gate fails. Average go, geometric no-go, gated no-go.

`S = (11 + 0.05) / 12 = 0.921`. `G = 0.05^(1/12) = 0.779`. The spiky plan tops the average with a platform at 5% of its target, and only the gate and, here, the geometric score stop it. The even plan fails honestly on its level, not on one hidden criterion.
</details>

84. *Week 14 · design.* You are designing the readiness scorecard for an MMO that sells on PC and one console, with a player-driven economy. Say which of these you make gates and which weighted criteria: tested restore, console performance, trading kill switch flipped in test, beta survey satisfaction, launch trailer views, queue forecast within target. Justify each in one line.

<details>
<summary>Answer and worked solution</summary>

**Answer (one defensible design):** gates on tested restore (data loss sits above any disaster line), console performance (you sell there, and Cyberpunk 2077's December 2020 last-generation console launch shows the cost), trading kill switch (containment for dupes, week 6 and week 13), and queue forecast (capacity, week 2). Weighted criteria for beta survey satisfaction and trailer views, which inform demand and tuning but cannot sink the launch on their own.

A gate needs a measured score, so each gated row needs its measurement named (restore time against target, frame rate on the console build, switch flipped in a rehearsal, hour-3 wait from the lab 2 model).
</details>

85. *Week 14 · critique.* A group's post-mortem analysis ends with the lesson "Test more before launch." Rewrite it so it transfers, in a form from the lecture's section 4, using a model from this course.

<details>
<summary>Answer and worked solution</summary>

**Answer (one version):** "Size the beta from the rarest crash class we must find: `E_beta ≥ 3 / r`. For a crash at once per 150,000 player-hours, that is 450,000 player-hours, and the testing section's gate is 'beta exposure at least 450,000 player-hours, measured from telemetry' (gate 0.7 on the share of that target reached)."

"Test more" changes no number in any plan. The rewrite fits as a gate in the scorecard with a measured score, so a panel can check whether a different game's plan meets it.
</details>
