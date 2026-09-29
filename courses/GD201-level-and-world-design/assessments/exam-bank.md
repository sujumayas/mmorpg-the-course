# GD201 · Exam bank: practice, spot-check and crit questions

GD201 has no written exam. The grade comes from the blockouts (40%, see [blockouts-brief.md](blockouts-brief.md)), the analysis work (20%, see [teardown-brief.md](teardown-brief.md)) and the final greybox zone with its design document (40%, see [final-zone-brief.md](final-zone-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Lab spot checks.** In each lab session from week 2 on, a marker asks two or three students two questions from this bank, rewritten with the numbers from their own blockout.
- **Crits and viva.** The week 8 blockout crit and the week 15 final-zone crit end with questions in this style, using your own zone's metrics, speeds and playtest data.

Every question is tagged with the week or weeks it draws on and one type.

- **compute**: apply a lecture model to values you have not seen before.
- **analysis**: read numbers, a table or a playtest result and say what they mean for a level.
- **code**: trace what a short piece of Python prints.
- **design**: choose a layout or setting for a stated situation and justify it with a number.
- **critique**: find what is wrong with a plan, a map or a claim, and say how to fix it.

All numbers are invented teaching values unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and version. Every code snippet runs as shown with Python 3.13 (`.venv/bin/python`), and every number was recomputed in Python from the lectures' own models. Write your own answer before you open the solution.

---

## Week 1: Level design as teaching

1. *Week 1 · compute.* A dash challenge takes `t = 12` s per attempt. The respawn delay is `s = 3` s, the checkpoint is 45 m before the challenge and the player runs at 5 m/s.
   (a) What is the recovery time `r`?
   (b) Compute `E[T]` and the penalty ratio at `p = 0.3` and at `p = 0.8`.
   (c) How many seconds per clear does the layout add at each `p`?
   (d) Move the checkpoint to the challenge. What is `E[T]` at `p = 0.3` now?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 12 s. (b) 68.0 s and 1.70 at `p = 0.3`; 18.0 s and 1.20 at `p = 0.8`. (c) 28.0 s and 3.0 s. (d) 47.0 s.

(a) `r = s + d / v = 3 + 45 / 5 = 12` s.

(b) `E[T] = (t + r(1 − p)) / p`. At `p = 0.3`: `(12 + 12 × 0.7) / 0.3 = 20.4 / 0.3 = 68.0` s. Penalty ratio `1 + (r/t)(1 − p) = 1 + 1 × 0.7 = 1.70`. At `p = 0.8`: `(12 + 2.4) / 0.8 = 18.0` s, ratio `1 + 0.2 = 1.20`.

(c) Subtract the instant-retry time `t / p`. The learner loses `68 − 40 = 28` s per clear. The master loses `18 − 15 = 3` s.

(d) With `d = 0`, `r = 3`. `E[T] = (12 + 3 × 0.7) / 0.3 = 14.1 / 0.3 = 47.0` s. The move saves the learner 21 s per clear and the master under 3 s, the pattern of the lecture's table.
</details>

2. *Week 1 · code.* The function below is the lecture's segment model. Three challenges sit between two checkpoints, each with `c = 10` s, and the respawn delay is 2 s. Predict what the code prints. Then say where you would put one extra checkpoint for the `easy_first` order, and compute the new total.

```python
def segment_time(costs, probs, respawn):
    reach, run = 1.0, 0.0
    for c, p in zip(costs, probs):
        run += c * reach
        reach *= p
    return (run + respawn * (1 - reach)) / reach

easy_first = segment_time([10, 10, 10], [0.9, 0.6, 0.4], 2)
hard_first = segment_time([10, 10, 10], [0.4, 0.6, 0.9], 2)
print(f"{easy_first:.1f} {hard_first:.1f}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints `120.2 83.2`. The extra checkpoint goes just before the `p = 0.4` challenge, and the total falls to 64.9 s.

Easy first: `run = 10 + 10 × 0.9 + 10 × 0.54 = 24.4`, `P = 0.9 × 0.6 × 0.4 = 0.216`, so `E = (24.4 + 2 × 0.784) / 0.216 = 25.968 / 0.216 = 120.2` s. Hard first: `run = 10 + 4 + 2.4 = 16.4`, same `P`, `E = (16.4 + 1.568) / 0.216 = 83.2` s. The same three jumps in a different order cost 37 s more, because every failure at the last challenge throws away a run that already paid for the first two.

One extra checkpoint, before challenge 3: `segment_time([10, 10], [0.9, 0.6], 2) = 19.92 / 0.54 = 36.9` plus `segment_time([10], [0.4], 2) = 11.2 / 0.4 = 28.0`, total 64.9 s. Before challenge 2 instead: `10.2 / 0.9 = 11.3` plus `17.52 / 0.24 = 73.0`, total 84.3 s. Isolate the likeliest failure.
</details>

3. *Week 1 · analysis.* A grapple challenge has `t = 6` s, `p = 0.25` and `r = 40` s.
   (a) What fraction of players fail 8 or more times in a row before their first clear?
   (b) How long do those 8 failures cost them?
   (c) How many attempts per hour does the layout allow, and how many with `r = 4`? Why does this matter for learning, not only for patience?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 10.0%. (b) 368 s, about 6.1 minutes. (c) 100 attempts per hour against 400.

(a) Eight failures in a row has chance `0.75⁸ = 0.100`, so one player in ten.

(b) Each failure costs the attempt and the recovery, `6 + 40 = 46` s. Eight of them cost `8 × 46 = 368` s.

(c) An average attempt costs `t + r(1 − p) = 6 + 40 × 0.75 = 36` s, so `3600 / 36 = 100` attempts an hour. With `r = 4`: `6 + 3 = 9` s, 400 an hour. Practice is how `p` rises, so a long `r` slows learning as well as annoying the player. The tail from (a) is who quits.
</details>

4. *Week 1 · critique.* A student hands in this lesson matrix for a level about a dash.

| Beat | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Jump | I | P | C | C | T |
| Dash | — | I | T | P | T |
| Crumbling floor | — | I | — | C | T |
| Recovery `r` (s) | 2 | 30 | 4 | 6 | 25 |

Find three violations of the lecture's rules. For beat 2, with `t = 8` s and `p = 0.2`, compute the penalty ratio at `r = 30` and at `r = 2`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Beat 2 introduces two things. The dash is tested in beat 3 before it is ever practised. Beat 2 puts a 30-second recovery on the two introductions. Penalty ratio 4.0 at `r = 30`, 1.2 at `r = 2`.

- **One new thing per beat.** Column 2 holds two `I` letters (dash and crumbling floor). Move the floor's introduction to beat 3.
- **No test before practice.** The dash row goes `I, T, P`. Swap beats 3 and 4 for the dash, or make beat 3 a practice beat.
- **Recovery rises with mastery.** The highest `r` before the finale sits under two introductions, the worst cell in any level.

Beat 2 at `r = 30`: `1 + (30 / 8) × 0.8 = 4.0`. At `r = 2`: `1 + (2 / 8) × 0.8 = 1.2`. Learners there would spend four times as long as the challenge itself requires.
</details>

## Week 2: Blockout and greyboxing

5. *Week 2 · compute.* A level has `N = 50` layout problems and each playtest round finds 40% of what is left. The budget is 36 hours. How many problems remain with 4-hour rounds, and with 12-hour rounds?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 0.50 with 4-hour rounds, 10.8 with 12-hour rounds.

4-hour rounds: `k = floor(36 / 4) = 9`, remaining `50 × 0.6⁹ = 0.50`. 12-hour rounds: `k = 3`, `50 × 0.6³ = 10.8`. The same budget leaves about 21 times as many problems when each round costs three times as much. That is the case for keeping `c_g` small.
</details>

6. *Week 2 · compute.* Each tester has a 25% chance of running into a given layout problem during a round.
   (a) With 4 testers, what is the discovery rate `f`?
   (b) How many testers do you need for `f ≥ 0.9`? Check your answer by computing the miss chance, not only the logarithm.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `f = 0.684`. (b) 9 testers.

(a) `f = 1 − 0.75⁴ = 1 − 0.316 = 0.684`.

(b) You need `0.75ⁿ ≤ 0.1`. `n = ln(0.1) / ln(0.75) = 8.004`, so round up to 9. The check matters here: `0.75⁸ = 0.1001`, just above 0.1, so 8 testers fall a hair short. `0.75⁹ = 0.075` passes. A value like 8.004 is the kind of result where "round to nearest" gives the wrong design.
</details>

7. *Week 2 · compute.* Use the switch-point model with `N = 30`, `M = 8`, `f = 0.5`, `B = 100`, `A = 40`, `c_g = 5` and `c_a = 20`.
   (a) Compute `R` for `S` = 0, 10, 15, 20, 25, 40 and 60.
   (b) Which switch point is best, and why does `R` jump between 20 and 25?
   (c) If art revealed nothing new (`M = 0`), where would the best switch point move?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 4.75, 3.88, 2.94, 2.47, 4.47, 4.06, 8.01. (b) `S = 20`. At 25 the budget loses its second art round. (c) To the far end, `S = 60`, with 0.007 problems.

Use `g = floor(S / 5)`, `a = floor((100 − S − 40) / 20)` and `R = (30 × 0.5^g + 8) × 0.5^a`.

| `S` | `g` | `a` | Left after greybox | `R` |
|---|---|---|---|---|
| 0 | 0 | 3 | 38.0 | 4.75 |
| 10 | 2 | 2 | 15.5 | 3.88 |
| 15 | 3 | 2 | 11.75 | 2.94 |
| 20 | 4 | 2 | 9.875 | 2.47 |
| 25 | 5 | 1 | 8.94 | 4.47 |
| 40 | 8 | 1 | 8.12 | 4.06 |
| 60 | 12 | 0 | 8.01 | 8.01 |

(b) At `S = 20` the remaining 40 hours buy exactly two art rounds. At `S = 25` only 35 hours remain, which buys one. The fifth greybox round removes less than one layout problem, while losing an art round leaves half of the 8 art-only problems in place. The floor in `a` makes the U jagged, so check the values just before and after each art round drops out.

(c) With `M = 0` every extra greybox round helps and art rounds find nothing new, so `R` falls all the way to `30 × 0.5¹² = 0.007` at `S = 60`. The best switch point exists only because `M > 0`.
</details>

8. *Week 2 · compute.* Your blockout kit has a 6 m corridor piece.
   (a) Every how many metres does it realign with a 9 m room piece?
   (b) Which of the room sizes 12, 15, 18 and 24 m tile with both a 4 m and a 6 m corridor?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Every 18 m. (b) 12 and 24 m.

(a) Pieces realign every `lcm(6, 9) = 18` m, so a loop that mixes them only closes cleanly at multiples of 18.

(b) A room tiles with both corridors if its size is a multiple of `lcm(4, 6) = 12`. 12 and 24 qualify. 15 is not a multiple of 4 or 6, and 18 is not a multiple of 4.
</details>

## Week 3: Flow, pacing and intensity graphs

9. *Week 3 · compute.* With `d = 0.5`, compute the intensity curve for the encounter list `E = 20, 20, 0, 0, 0, 40`. Give the maximum, peak time (`I ≥ 35`), calm time (`I < 10`) and number of peaks.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `I = 20, 30, 15, 7.5, 3.75, 41.9`. Maximum 41.9, peak time 10 s, calm time 20 s, one peak.

Each step halves the previous value and adds the new threat. Step 6: `0.5 × 3.75 + 40 = 41.875`. Only step 6 is at or above 35, so there is one peak of 10 s. Steps 4 and 5 are below 10, so 20 s of calm. The first pulse of 40 units never reached the peak band because it was spread over two steps. The second pulse of the same size, delivered in one step, did.
</details>

10. *Week 3 · compute.* A team chooses `d = 0.6` per 10-second step.
    (a) What is the half-life of intensity?
    (b) What intensity does a constant drip of 8 units per step settle at?
    (c) What constant threat per step holds intensity exactly at the peak threshold of 35?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 13.6 s. (b) 20. (c) 14 units per step.

(a) Half-life `= 10 × ln 0.5 / ln 0.6 = 10 × 0.693 / 0.511 = 13.6` s.

(b) `I* = E / (1 − d) = 8 / 0.4 = 20`.

(c) `E = 35 × (1 − 0.6) = 14`. With a slower decay, less steady threat is needed to sit at the threshold, and the same bursts stack more easily.
</details>

11. *Week 3 · code.* This is the lecture's Director rule with a smaller population. Predict the output. How many steps does Build Up take, and what would happen if the peak threshold were 30 instead of 28?

```python
def director(steps, full=15, peak=28, relax=2, d=0.5):
    I, rest, out = 0.0, 0, []
    for _ in range(steps):
        e = 0 if rest > 0 else full
        rest = max(0, rest - 1)
        I = d * I + e
        out.append((e, round(I, 2)))
        if e > 0 and I >= peak:
            rest = relax
    return out

print(director(8))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints `[(15, 15.0), (15, 22.5), (15, 26.25), (15, 28.12), (0, 14.06), (0, 7.03), (15, 18.52), (15, 24.26)]`. Build Up takes 4 steps. With a threshold of 30 the Director never peaks.

Intensity crosses 28 at step 4 (28.125, which Python rounds to 28.12), so steps 5 and 6 send nothing. Step 7 starts the next Build Up from 7.03.

The equilibrium of a full population is `15 / (1 − 0.5) = 30`. The curve approaches 30 but never reaches it, so a threshold of 30 or more is never crossed and the Director stays in Build Up forever: a drip at 30. Check any Director setting against `full / (1 − d)` before you tune the threshold.
</details>

12. *Week 3 · analysis.* A fight ends with intensity at 60. Your calm threshold is 10.
    (a) With `d = 0.5` per 10 s, how long a rest brings intensity below 10?
    (b) With `d = 0.7`?
    (c) The beat chart gives this rest 40 s. Is that enough under each decay?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 30 s. (b) 60 s. (c) Yes at `d = 0.5`, no at `d = 0.7`.

(a) `60 × 0.5³ = 7.5 < 10`, while `60 × 0.5² = 15`. Three steps, 30 s.

(b) `60 × 0.7⁵ = 10.08`, which is not below 10. `60 × 0.7⁶ = 7.06`. Six steps, 60 s.

(c) A 40-second rest resets the curve under the faster decay and leaves it at `60 × 0.7⁴ = 14.4` under the slower one. The rest length a chart needs depends on the `d` your team chose, which is why Lab 03 asks you to rerun the curve at 0.3 and 0.7.
</details>

## Week 4: Guiding the player: landmarks, light, weenies

13. *Week 4 · compute.* A 40 m tower stands 1,500 m from the player, who uses a 90° horizontal view at 16:9.
    (a) What fraction of the screen height does it fill?
    (b) How many pixels is that at 1080p and at 1440p?
    (c) Is it legible at `f_min = 2%`, and what is its `d_max`?
    (d) Is the tower easier to notice for the 1440p player?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 2.37%. (b) 25.6 px and 34.1 px. (c) Yes, `d_max = 1,778` m. (d) No.

(a) `f = 40 / (1.125 × 1,500) = 0.0237`.

(b) `0.0237 × 1080 = 25.6` px and `0.0237 × 1440 = 34.1` px.

(c) `f > 0.02`, so yes. `d_max = 40 / 0.0225 = 1,778` m.

(d) On the same monitor the tower covers the same share of the player's view at both resolutions. Legibility depends on `f`, not on the pixel count.
</details>

14. *Week 4 · compute.* A player on a 21:9 monitor sets a 100° horizontal field of view and says "my view is wider than yours at 90°, so landmarks look smaller for me." The game uses Hor+ scaling.
    (a) Compute this player's vertical field of view and `2 tan(V/2)`.
    (b) Compute `d_max` for a 60 m landmark at `f_min = 2%` for this player and for a 16:9 player at 90°.
    (c) Is the player right?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `V = 54.1°`, `2 tan(V/2) = 1.022`. (b) 2,937 m against 2,667 m. (c) No, the landmark reads slightly larger for them.

(a) `V = 2 atan(tan(50°) / (21/9)) = 2 atan(1.1918 / 2.333) = 2 atan(0.5108) = 54.1°`. Then `2 tan(V/2) = 1.022`.

(b) `d_max = h / (2 f_min tan(V/2))`. This player: `60 / (0.02 × 1.022) = 2,937` m. The 16:9 player at 90°: `60 / 0.0225 = 2,667` m.

(c) Screen fraction depends on the vertical angle. Under Hor+, a wider monitor adds view at the sides and keeps the vertical angle. So a horizontal number means nothing until you know the aspect ratio. At 90° on 21:9 the vertical angle is only 46.4°. Test landmarks at the widest vertical angle your settings allow.
</details>

15. *Week 4 · compute.* A torch-lit door has relative luminance 0.30 against a wall of 0.05.
    (a) What is the contrast ratio? Does it meet 3:1 and 4.5:1?
    (b) Keeping the wall, what door luminance reaches 4.5:1?
    (c) Keeping the door, how dark must the wall be for 4.5:1?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 3.5:1. It meets 3:1, not 4.5:1. (b) 0.40. (c) At most 0.028.

(a) `(0.30 + 0.05) / (0.05 + 0.05) = 0.35 / 0.10 = 3.5`.

(b) `(L + 0.05) / 0.10 = 4.5` gives `L = 0.40`.

(c) `0.35 / (L_wall + 0.05) = 4.5` gives `L_wall = 0.35 / 4.5 − 0.05 = 0.028`. Darkening the surroundings works as well as brightening the target, and it is often cheaper than more light.
</details>

16. *Week 4 · analysis.* You measure a shipped game's tower from 1080p screenshots, assuming a 90° horizontal view at 16:9. At a map distance of 600 m it is 45 px tall. At 300 m it is 80 px tall.
    (a) What height does the first screenshot give?
    (b) What does the model predict for the second screenshot?
    (c) A teammate says the mismatch proves the field-of-view assumption is wrong. Is that right? What does the mismatch point to, and how would you test the field of view instead?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 28.1 m. (b) 90 px. (c) No. Two shots of one object test the distances, not the field of view. Test the field of view with an object of known size.

(a) `h = P × 2d tan(V/2) / S = 45 × 600 × 1.125 / 1080 = 28.1` m.

(b) `P` is proportional to `1 / d`, so halving the distance doubles it: 90 px.

(c) Rearrange the model: `P × d = h × S / (2 tan(V/2))`. The right side is the same for both shots whatever the field of view is. So `P × d` must match across the two shots under any assumption: `45 × 600 = 27,000`, `80 × 300 = 24,000`. A wrong field of view changes the height you compute, but never the ratio between the shots. The mismatch means one distance is not what you think. The map may measure to the tower's centre or foot rather than along the view, the camera may not be level, or the game may have changed its view between shots (a sprint or zoom). To check the field of view itself, photograph something whose height you know, such as a door or a character, at a known distance.
</details>

## Week 5: Affordances and signposting

17. *Week 5 · compute.* Every player notices a signpost with `p = 0.35`. How many signposts does a route need for 90% of players to find it? Check your answer by computing P(find) for the two nearest counts.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 6 signposts.

`n = ln(0.1) / ln(0.65) = 5.35`, so round up to 6. Check: `1 − 0.65⁵ = 88.4%`, short of 90%. `1 − 0.65⁶ = 92.5%`, which passes.
</details>

18. *Week 5 · compute.* A playtest suggests 60% scanners with `p = 0.6` and 40% tunnelers with `p = 0.08`. The route has 6 subtle signposts.
    (a) What share of players finds the route?
    (b) What share of the lost players are tunnelers?
    (c) Add one loud signpost with `p = 0.85` for both groups. What share finds the route now?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 75.5%. (b) 99.0%. (c) 96.3%.

(a) Scanners lost: `0.6 × 0.4⁶ = 0.0025`. Tunnelers lost: `0.4 × 0.92⁶ = 0.2425`. Total lost 0.2450, so 75.5% find it.

(b) `0.2425 / 0.2450 = 99.0%`. Scanners are saturated. Nearly every lost player is a tunneler.

(c) Every lost player must also miss the loud sign, with chance 0.15: `0.2450 × 0.15 = 0.0368`, so 96.3% find the route.
</details>

19. *Week 5 · analysis.* Use the lecture's population (70% scanners at 0.5, 30% tunnelers at 0.05). A route has 6 subtle signposts. The team can afford one of three changes: (A) 10 more subtle signposts, (B) one loud signpost at `p = 0.9` for everyone, or (C) an escalation cue that only players who have been stuck for a while meet, also at `p = 0.9`. Compute P(find) for each and say which you would choose.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Now 76.9%. (A) 86.8%. (B) 97.7%. (C) 97.7%. Choose C if you can afford the trigger work, otherwise B.

Now: `0.7 × (1 − 0.5⁶) + 0.3 × (1 − 0.95⁶) = 0.689 + 0.079 = 0.769`.

(A) With 16 subtle signposts: `0.7 × (1 − 0.5¹⁶) + 0.3 × (1 − 0.95¹⁶) = 0.700 + 0.168 = 0.868`. Scanners were already at 98.4% with 6, so ten more cues only lift tunnelers from 26.5% to 56.0%.

(B) Lost `0.231 × 0.1 = 0.023`, so 97.7%.

(C) The escalation cue enters the formula the same way, a factor `(1 − 0.9)` on the lost share, so it also gives 97.7%. The difference is who pays. Scanners who found the route never meet the cue, so its immersion cost falls only on players who needed it. The cost moves to design and testing time, because the trigger must fire for lost players and not for explorers.
</details>

20. *Week 5 · analysis.* Eight testers walked a route with 4 signposts. Their notice rates were 0.6, 0.5, 0.7, 0.6, 0.5, 0.4, 0.6 and 0.5. Which model should you use? Predict P(find) and say how far you would trust it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Model 1 with `p = 0.55`, which predicts 95.9%. Treat it as a rough estimate.

The rates form one hump between 0.4 and 0.7, with nobody near 0 or 1. There is no sign of a separate tunneler group, so a single `p` is reasonable: `p̄ = 4.4 / 8 = 0.55`. P(find) `= 1 − 0.45⁴ = 95.9%`.

Eight testers is a small sample. A tunneler group of 10 to 20% could easily be missing from it by chance. Before relying on 95.9% for a critical-path route, test with a distraction task (as in the lecture's in-class activity) or with more testers.
</details>

## Week 6: Combat spaces: cover, lanes, chokepoints

21. *Week 6 · compute.* In an open field, 24 attackers with a 10-second time-to-kill meet 15 defenders with an 8-second time-to-kill. Who wins, and how many are left?

<details>
<summary>Answer and worked solution</summary>

**Answer:** The attackers win with about 17.2 left.

`a = 1/10 = 0.1`, `b = 1/8 = 0.125`. Attackers' strength `a A₀² = 0.1 × 576 = 57.6`. Defenders' `b D₀² = 0.125 × 225 = 28.1`. The attackers win with `sqrt(576 − (0.125/0.1) × 225) = sqrt(294.75) = 17.2` left. Better individual fighters do not make up for being outnumbered in the open, because numbers count squared.
</details>

22. *Week 6 · compute.* Twelve defenders hold a gate 3 fighters wide. Everyone has a 12-second time-to-kill.
    (a) What does the chokepoint law give for attacker losses and fight length?
    (b) Is the formula valid for 30 attackers? For 26?
    (c) A tick simulation gives these results: 30 attackers win with 6.0 left after 48.0 s; 26 attackers win with 1.7 left after 52.0 s; 24 attackers lose, leaving 3.0 defenders after 41.6 s. Explain the 26-attacker result.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 24 attackers, 48 s. (b) Valid for 30, not for 26. (c) Past the limit, fewer than `w` attackers fight in the last seconds, so the fight lasts longer and the formula's "2 left" is only roughly right.

(a) `a = b = 1/12`. Losses `= b D₀² / (2 a w) = 144 / 6 = 24`. `T = D₀ / (a w) = 12 / (3/12) = 48` s.

(b) The law needs `A₀ ≥ losses + w = 27`. 30 qualifies: 6 left, 48 s, as the simulation shows. 26 does not.

(c) With 26, the attackers fall below 3 alive before the last defenders die, so fewer than 3 are firing. Defenders then fall more slowly than `a w` per second, the fight stretches to 52 s, and the attackers finish with 1.7 instead of the formula's 2. With 24 the shortfall is worse and the attackers lose. Near the edge of validity, trust the simulation.
</details>

23. *Week 6 · compute.* Eight defenders hold a gate 2 wide, equal fighters with a 10-second time-to-kill. The defenders have full cover in XCOM terms (rookie aim 65, +40 defense), and their grenades hit 1.5 attackers on average.
    (a) What are the attacker losses without cover or splash, and with both?
    (b) How long does the fight last with both?
    (c) Name one layout change that removes the splash factor.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 16, then 62.4. (b) 104 s. (c) Widen the space in front of the gate or add a second entrance.

(a) Base: `0.1 × 64 / (2 × 0.1 × 2) = 16`. Full cover multiplies the attacker kill rate by `25/65`, so the cost by `65/25 = 2.6`. Splash multiplies the defender kill rate by 1.5. Losses `= 16 × 2.6 × 1.5 = 62.4`.

(b) Fight length depends only on the attackers' kill rate: `T = 8 / (0.1 × 25/65 × 2) = 104` s. Splash makes the fight more costly, not longer.

(c) Splash depends on attackers bunching. Room to spread out, or a second approach, brings `k` back toward 1. A flank route that ignores the cover would also restore `a`.
</details>

24. *Week 6 · analysis.* Nine defenders guard a map with three lanes, each with a chokepoint 2 wide. Equal fighters, `a = 0.1`.
    (a) How much cheaper is one lane to break with a 3/3/3 split than a single choke holding all nine?
    (b) Which split maximises the time the weakest lane survives, and how long is it?
    (c) The rotation route from the far lane is 110 m at 6 m/s. Does help arrive in time? What is the longest rotation route the split tolerates?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 9 times cheaper (2.25 against 20.25). (b) 3/3/3, 15 s. (c) No, it takes 18.3 s. The limit is 90 m.

(a) Single choke: `0.1 × 81 / (2 × 0.1 × 2) = 20.25`. One lane with 3: `9 / 4 = 2.25`. The ratio is `3² = 9`.

(b) A lane falls in `T = D / (a w) = D / 0.2`. The weakest lane decides, so maximise the smallest group. 3/3/3 gives 15 s. 4/3/2 and 5/2/2 give 10 s, and 4/4/1 gives 5 s.

(c) `110 / 6 = 18.3` s, longer than 15 s, so the lane falls first. The route must be at most `15 × 6 = 90` m. Shorten the defenders' rotation path by 20 m, or narrow that lane's choke to 1 (which doubles its fall time to 30 s).
</details>

## Week 7: Verticality and navigation

25. *Week 7 · compute.* A game uses `g = 25` m/s² and a climb speed of 2 m/s. For a 9 m edge, compute the drop time, the climb time and the asymmetry ratio.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Drop 0.85 s, climb 4.5 s, ratio 5.30.

Drop `= sqrt(2 × 9 / 25) = sqrt(0.72) = 0.85` s. Climb `= 9 / 2 = 4.5` s. Ratio `= 4.5 / 0.85 = 5.30`, or from the one-line form, `sqrt(25 × 9 / 2) / 2 = 10.61 / 2 = 5.30`.
</details>

26. *Week 7 · compute.* A watchtower level uses the lecture's constants (`g = 20`, `h_safe = 8` m, climb 1.5 m/s). The Tower top T is 16 m up, a Balcony B is at 8 m and the Courtyard C is on the ground. Edges: T → B drop 8 m; B → C drop 8 m; stairs C → T 120 m at 4 m/s uphill and T → C 120 m at 6 m/s downhill; C ↔ Gate G, 30 m run at 6 m/s.
    (a) Compute the out time T → G, the back time G → T and the return ratio.
    (b) A designer adds a 16 m ladder from C to T. New return ratio?
    (c) A second designer instead adds an 8 m ladder from C to B. What happens, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 6.79 s out, 35.0 s back, ratio 5.16. (b) 2.31. (c) Nothing changes.

(a) Out: `0.894 + 0.894 + 5 = 6.79` s via the two drops (the stairs take `20 + 5 = 25` s). Back: the drops only go down, so `5 + 30 = 35` s by the stairs. Ratio `35 / 6.79 = 5.16`.

(b) Ladder: `16 / 1.5 = 10.67` s. Back `= 5 + 10.67 = 15.67` s. Ratio `15.67 / 6.79 = 2.31`, still above 2. A lift or a faster climb would be needed to reach 2.

(c) The ladder reaches B, but B has no up edge to T, only the one-way drop down. Shortest paths only use edges that exist in the direction of travel, so the back trip is still 35 s. A shortcut must connect to somewhere with a way home.
</details>

27. *Week 7 · compute.* With `h_safe = 6` m, how many ledges does a 50 m cliff need for a safe descent, and how tall is each drop? A climbing game gives 12 s of stamina at 1.2 m/s. How many rest platforms does a 50 m tower need?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 8 ledges, drops of about 5.6 m. 3 rest platforms.

Ledges: `ceil(50 / 6) − 1 = 9 − 1 = 8`, splitting the cliff into 9 drops of `50 / 9 = 5.56` m.

Climb limit `h_max = 1.2 × 12 = 14.4` m. Rests `= ceil(50 / 14.4) − 1 = 4 − 1 = 3`, splitting the tower into four sections of 12.5 m.
</details>

28. *Week 7 · compute.* In Minecraft (Java Edition, 1.21 era), a player at full health (20) keeps dropping 10 blocks at a time instead of placing ladders. How much health does each drop cost, and how many can they take in a row without healing? How long would climbing back up one 10-block ladder take?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 7 health per drop, 2 drops in a row. About 4.3 s up the ladder.

Each drop costs `floor(10 − 3) = 7`. After two drops the player has `20 − 14 = 6` health, and a third drop costs 7, which kills. Climbing 10 blocks at about 2.35 blocks per second takes `10 / 2.35 = 4.3` s. The health price turns a drop into a resource decision, where a ladder is a time decision.
</details>

## Week 8: Environmental storytelling

29. *Week 8 · compute.* A beat has three clues with `p = 0.9`, `0.6` and `0.4`. Compute the understanding rate for "needs all", "needs any" and "needs at least two".

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0.216, 0.976 and 0.708.

All: `0.9 × 0.6 × 0.4 = 0.216`. Any: `1 − 0.1 × 0.4 × 0.6 = 0.976`. At least two: exactly two is `0.9 × 0.6 × 0.6 + 0.9 × 0.4 × 0.4 + 0.1 × 0.6 × 0.4 = 0.324 + 0.144 + 0.024 = 0.492`, plus all three 0.216, total 0.708.
</details>

30. *Week 8 · compute.* You want players to need at least two clues (`k = 2`), using tier-B clues at `p = 0.5`. What is the understanding rate with 5 clues? How many clues do you need for 90%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0.8125 with 5 clues. 7 clues for 90%.

At least two of `n` is `1 − P(none) − P(exactly one) = 1 − (1 + n) × 0.5ⁿ`. For `n = 5`: `1 − 6 / 32 = 0.8125`. For `n = 6`: `1 − 7 / 64 = 0.891`, short. For `n = 7`: `1 − 8 / 128 = 0.9375`. Raising `k` from 1 to 2 needs 7 clues where 4 would reach 0.9375 with `k = 1`.
</details>

31. *Week 8 · analysis.* In a 20-tester playtest, 12 testers read clue X, 8 read clue Y and 7 read both.
    (a) Estimate `p` for each clue.
    (b) What does independence predict for "needs any" and "needs both"? What was observed?
    (c) What explains the gap, and how would you change the placement?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.6 and 0.4. (b) Predicted 0.76 and 0.24; observed 0.65 and 0.35. (c) Positive correlation. Move one clue to where a different kind of player looks.

(a) `12 / 20 = 0.6`, `8 / 20 = 0.4`.

(b) Any: `1 − 0.4 × 0.6 = 0.76`. Both: `0.6 × 0.4 = 0.24`. Observed any: `(12 + 8 − 7) / 20 = 0.65`. Both: `7 / 20 = 0.35`.

(c) Most testers who read Y also read X, so the second clue added few new readers. That is positive correlation: "needs any" does worse than the formula and "needs all" does better. The fix is to make the clues reach different players, for example one on the critical path in the forward view and one tied to a sound that turns the camera, rather than two clues both found by careful explorers.
</details>

32. *Week 8 · code.* Trace this version of `p_at_least`, which prints the distribution after each clue. What does it print?

```python
def p_at_least(ps, k):
    dist = [1.0]
    for p in ps:
        new = [0.0] * (len(dist) + 1)
        for j, q in enumerate(dist):
            new[j] += q * (1 - p)
            new[j + 1] += q * p
        dist = new
        print([round(x, 3) for x in dist])
    return sum(dist[k:])

print(round(p_at_least([0.5, 0.8], 1), 3))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
[0.5, 0.5]
[0.1, 0.5, 0.4]
0.9
```

After the first clue, half the players have seen none and half have seen one. The second clue moves each group: none stays none with chance 0.2 (`0.5 × 0.2 = 0.1`), one of the "none" group moves to one (`0.5 × 0.8 = 0.4`), one of the "one" group stays at one (`0.5 × 0.2 = 0.1`), and the rest reach two (`0.5 × 0.8 = 0.4`). So `P(1) = 0.4 + 0.1 = 0.5`. At least one is `0.5 + 0.4 = 0.9`, the same as `1 − 0.5 × 0.2`.
</details>

## Week 9: Open-world structure: POI density

33. *Week 9 · compute.* A game's run speed is 5.5 m/s and the design gap between points of interest is 45 s. What spacing and density does that imply, and how many POIs fill a 3 km × 2 km zone?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Spacing 247.5 m, density 16.3 per km², about 98 POIs.

Spacing `a = v t = 5.5 × 45 = 247.5` m. Density `1 / 0.2475² = 16.3` per km². Area 6 km², so `6 × 16.3 = 97.9`, about 98.
</details>

34. *Week 9 · compute.* The same game adds a mount that is 80% faster. By what factor must density change to keep the 45-second gap while mounted? If the zone keeps the walker's density, what gap does the rider feel?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Density must fall to 0.31 of the walker's, from 16.3 to about 5.0 per km². At the walker's density, the rider's gap is 25 s.

Density scales as `1 / v²`: `1 / 1.8² = 1 / 3.24 = 0.309`. So `16.3 × 0.309 = 5.0` per km², about 30 POIs in the 6 km² zone instead of 98. At the old density the gap is `45 / 1.8 = 25` s. An 80% speed increase cuts the content needed by more than two thirds.
</details>

35. *Week 9 · compute.* At the walker's density of 16.3 per km² on a square grid, how far is the worst spot from the nearest POI? If the same number of POIs were placed at random, what fraction of the zone would be farther than that from any POI?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 175 m. About 21% of the zone.

Grid spacing `1000 / sqrt(16.3) = 247.7` m, and the worst spot is at a cell's centre, `247.7 / sqrt(2) = 175` m from a POI. For random placement, `P(no POI within r) = exp(−ρ π r²) = exp(−16.3 × π × 0.175²) = exp(−1.568) = 0.208`. One fifth of a random map is emptier than the grid's worst spot, the same result as the lecture's walker zone.
</details>

36. *Week 9 · compute.* A sparse mounted zone has 5 POIs per km².
    (a) How many POIs does a player expect to see within 400 m in open terrain?
    (b) How far must players see for 4 POIs to be in view?
    (c) Using week 4's model with a 90° view at 16:9 and `f_min = 2%`, how tall must a POI marker be to stay legible at that distance?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 2.5. (b) About 505 m. (c) About 11.4 m.

(a) `N = ρ π r² = 5 × π × 0.4² = 2.51`.

(b) `r = sqrt(4 / (5π)) = sqrt(0.2546) = 0.505` km.

(c) `h = 0.0225 × 505 = 11.4` m. A tree-sized silhouette, a lit beacon or a column of smoke does the job, which is why sparse zones rely on tall or glowing POI markers.
</details>

37. *Week 9 · analysis.* A zone has 80 POIs, each with a dwell time of 60 s. On foot the gap is 30 s. On a +100% mount it is 15 s. For each, what share of the player's time is spent at content, and how long does the zone last?

<details>
<summary>Answer and worked solution</summary>

**Answer:** On foot 66.7% and 2.0 hours. Mounted 80% and 1.67 hours.

On foot: `60 / (60 + 30) = 66.7%`, and `80 × 90 = 7,200` s = 2.0 h. Mounted: `60 / 75 = 80%`, and `80 × 75 = 6,000` s = 1.67 h. The rider spends more of their time at content and finishes 20 minutes sooner. Speed spends content faster, which is the cost side of every mount.
</details>

38. *Week 9 · compute.* Minecraft (Java Edition, 1.21 era) places villages with a `spacing` in chunks. A server config lowers village spacing from 34 to 24 chunks. How far apart are the generation attempts on average, how long is the walk between them at 4.317 blocks per second and at a 5.612 sprint, and what is the density of attempts per km² (one block is one metre)?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 384 blocks apart, 89.0 s walking, 68.4 s sprinting, 6.8 attempts per km².

`24 × 16 = 384` blocks. `384 / 4.317 = 89.0` s. `384 / 5.612 = 68.4` s. Density `1 / 0.384² = 6.8` per km², against 3.4 at the default spacing of 34. Not every attempt makes a village, so real gaps are longer.
</details>

## Week 10: Hubs, spokes, and gating

39. *Week 10 · compute.* A zone has 10 destinations joined by links of 120 m. Compute the mean errand cost for a chain with the hub at one end, a ring and a hub and spoke, in metres and in seconds at 6 m/s.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Chain 1,320 m (220 s). Ring 720 m (120 s). Hub 240 m (40 s).

Chain `E = L(n + 1) = 120 × 11 = 1,320` m. Ring, with `n` even, `E = L(n + 2) / 2 = 120 × 6 = 720` m. Hub `E = 2L = 240` m. Divide by 6 for seconds.
</details>

40. *Week 10 · compute.* A ring has 7 destinations and links of 100 m. The lecture's ring formula assumes `n` is even. Compute `E` by listing distances, and compare it with what the even formula would give.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `E = 457.1` m. The even formula would give 450 m.

The loop has 8 nodes, hub plus 7. Going the short way, the destinations are 1, 2, 3, 4, 3, 2, 1 links from the hub. Sum 16, mean `16 / 7 = 2.29` links, round trip `2 × 100 × 16 / 7 = 457.1` m. Plugging `n = 7` into `L(n + 2)/2` gives 450 m, slightly low, because with an odd count the far point of the loop is a single node at the maximum distance. When a closed form has a condition, compute from the distances.
</details>

41. *Week 10 · code.* A hub (node 0) has spokes to 1, 4 and 5. Node 1 continues to 2 and then 3, and 3 also links to 5. All links are 100 m. What does this code print?

```python
from collections import deque

def distances(graph, start):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist

links = [(0, 1), (1, 2), (2, 3), (0, 4), (0, 5), (3, 5)]
graph = {}
for a, b in links:
    graph.setdefault(a, set()).add(b)
    graph.setdefault(b, set()).add(a)

d = distances(graph, 0)
dests = [n for n in graph if n != 0]
print(2 * 100 * sum(d[n] for n in dests) / len(dests))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints `280.0`.

Breadth-first search from the hub gives 1, 4 and 5 at one link. Node 2 is two links via 1. Node 3 is two links via 5, not three via 1 and 2, because the link from 3 to 5 closes a loop. The sum is `1 + 2 + 2 + 1 + 1 = 7` over 5 destinations, so `E = 2 × 100 × 7 / 5 = 280` m. Without the 3 to 5 link, node 3 would be three links away and `E` would be 320 m.
</details>

42. *Week 10 · compute.* A hub has four spokes of 12 tokens each. Spoke A is open. Gates to B, C and D need 6, 16 and 30 tokens, and the final door needs 40.
    (a) Compute the slack at every gate.
    (b) Redesign the thresholds so each gate forces about 60% of what is available, and give the new slack.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 2.0, 1.5, 1.2 and 1.2. (b) 7, 14, 22 and 29, with slack 1.71, 1.71, 1.64 and 1.66.

(a) B: `12 / 6 = 2.0`. C: `24 / 16 = 1.5`. D: `36 / 30 = 1.2`. Final: `48 / 40 = 1.2`. The last two gates force 83% of the open content. The thresholds look like a staircase and play like a squeeze.

(b) `0.6 × 12 = 7.2`, `0.6 × 24 = 14.4`, `0.6 × 36 = 21.6` and `0.6 × 48 = 28.8`, rounded to 7, 14, 22 and 29. Slack `12/7 = 1.71`, `24/14 = 1.71`, `36/22 = 1.64`, `48/29 = 1.66`.
</details>

43. *Week 10 · compute.* In a hub and spoke zone, the key to spoke C lies at the far end of spoke A, which is a short chain of three 80 m links. Spoke C's door is at the hub. How many extra metres does the key add, and how many seconds at 6 m/s? What does moving the key to the first node of spoke A save?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 480 m, 80 s. Moving the key saves 320 m.

The key adds an errand to the end of spoke A and back: `2 × 3 × 80 = 480` m, which is 80 s. With the key one link out, the extra errand is `2 × 80 = 160` m, a saving of 320 m. If players want to finish spoke A anyway, the far key costs nothing extra, so placement depends on whether the trip is one they would make anyway.
</details>

## Week 11: Shared spaces: designing for many players at once

44. *Week 11 · compute.* A zone has `H = 12` camps, `f = 0.5`, 240 players, 1.5 km² of open ground and a view radius of 35 m. How many others does a player at a camp see, and a player in the open? What is the ratio?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 9 at a camp, 0.31 in the open, a ratio of about 29.

`N_camp = 0.5 × 240 / 12 − 1 = 9`. `N_open = 120 × π × 35² / 1,500,000 = 120 × 3,848 / 1,500,000 = 0.31`. Ratio `9 / 0.31 = 29`. The camps are busy while the open ground is nearly empty.
</details>

45. *Week 11 · compute.* For the zone in question 44, the team wants between 3 and 15 others at each camp.
    (a) What is the comfortable range of `P`?
    (b) Launch brings 5,000 players into the zone. How many copies are needed, and how crowded is each camp?
    (c) A year later, 300 players remain. What does a camp look like if the 14 copies stay, and how many copies should remain?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 96 to 384. (b) 14 copies, about 13.9 others per camp. (c) Camps are empty; merge to 3 copies of 100, giving 3.2 others per camp.

(a) `P_min = 12 × 4 / 0.5 = 96`. `P_max = 12 × 16 / 0.5 = 384`.

(b) `ceiling(5,000 / 384) = 14` copies of 357.1 players. `N_camp = 0.5 × 357.1 / 12 − 1 = 13.9`, inside the band.

(c) With 14 copies each holds 21.4 players, and `N_camp = 0.5 × 21.4 / 12 − 1 = −0.1`, which means most camps are empty. `floor(300 / 96) = 3` copies keeps each at or above `P_min`: 100 players each, `N_camp = 0.5 × 100 / 12 − 1 = 3.2`.
</details>

46. *Week 11 · analysis.* To make launch easier, a designer doubles the zone in question 44 from 12 camps to 24, with `f`, `n_min = 3` and `n_max = 15` unchanged. What happens to `P_min` and `P_max`? How many others does a camp hold at 150 players, before and after the change?

<details>
<summary>Answer and worked solution</summary>

**Answer:** The range moves from 96 to 384 to 192 to 768. At 150 players, a camp holds 5.25 others with 12 camps and 2.1 with 24.

`P_min = 24 × 4 / 0.5 = 192`, `P_max = 24 × 16 / 0.5 = 768`. At 150 players: `0.5 × 150 / 12 − 1 = 5.25` against `0.5 × 150 / 24 − 1 = 2.1`, below `n_min`. Doubling camps doubles both ends of the band. The zone copes with twice the launch crowd in half the copies, and it feels empty at populations that used to be comfortable. That costs content twice, once to build the camps and again when the zone empties sooner.
</details>

## Week 12: Spawn design and contested resources

47. *Week 12 · compute.* In an open arena with no inner walls and `R = 5`, a spawn sits far from every wall. What is `E` at the spawn? Roughly what happens to `E` if the spawn moves against a straight outer wall?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `E = 80`. Against a wall it drops to roughly half.

Count grid points with `dx² + dy² ≤ 25`, one column at a time. The column `dx = 0` holds 11 points, the columns `dx = ±1`, `±2` and `±3` hold 9 each, `±4` hold 7 and `±5` hold 1. That is `11 + 2 × (9 + 9 + 9 + 7 + 1) = 81`, and removing the spawn itself gives 80. Against a wall, the cells beyond it are not open floor, so about half of the circle is gone.
</details>

48. *Week 12 · code.* The lecture's line-of-sight test samples the segment between cell centres in quarter-cell steps. What does this print? If cell (1, 1) is a wall, is the line from (0, 0) to (2, 1) blocked? What if (1, 0) is the wall instead?

```python
from math import floor

def samples(a, b):
    (x0, y0), (x1, y1) = a, b
    n = max(1, 4 * max(abs(x1 - x0), abs(y1 - y0)))
    return [(floor(x0 + (x1 - x0) * i / n + 0.5), floor(y0 + (y1 - y0) * i / n + 0.5))
            for i in range(n + 1)]

print(samples((0, 0), (2, 1)))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints `[(0, 0), (0, 0), (1, 0), (1, 0), (1, 1), (1, 1), (2, 1), (2, 1), (2, 1)]`. The line is blocked by a wall at (1, 1) and also by a wall at (1, 0).

`n = 4 × 2 = 8`. At `i = 4` the sample sits at (1, 0.5), exactly on the border between (1, 0) and (1, 1). Adding 0.5 and taking the floor sends 0.5 to 1, so that sample lands in (1, 1). Samples 2 and 3 land in (1, 0). The segment passes through both cells, so a wall in either blocks it. In a blockout that means a doorway placed on a diagonal between two walls can be sealed by either wall. Test sightlines that graze corners in the engine, not only on the grid.
</details>

49. *Week 12 · design.* On the lecture's teaching map (`R = 8`), spawn C in the closet has `E = 2` at the spawn, one exit at (12, 11) with `E = 25`, and `K = 21`. You may open one wall cell to give it a second exit. Option 1 opens (12, 9), a door into the same lower courtyard. Option 2 opens (15, 8), a door north into the plaza's right alcove. Before computing, predict which one lowers `K` more. The lecture's code gives these results:

| Option | `E` at spawn | `E` at exits | `K` |
|---|---|---|---|
| Unchanged | 2 | 25 | 21 |
| 1: open (12, 9) | 8 | 25 and 38 | 17 |
| 2: open (15, 8) | 17 | 25 and 26 | 0 |

Which would you build, and what does option 2 cost?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Option 2. It removes every camp position but makes the spawn cell itself more exposed.

Option 1's second door faces the same courtyard as the first, so 17 courtyard cells still see both doors. It barely changes `K`. Option 2's door faces a different part of the map, and no cell outside the closet sees both exits, so `K = 0`. That is the lecture's rule: two exits that face different areas beat any amount of hiding.

The cost is that the spawn cell's exposure rises from 2 to 17, because the alcove can now see into the closet. That is still below the lab's design target of 20, and a player who appears can choose the door a camper is not watching. Recheck the walk from the new door to the objectives, since week 1's recovery time applies to every respawn.
</details>

50. *Week 12 · compute.* A quest needs 12 kills at a camp with 8 spawns that respawn every 75 s. Alone, a player kills one every 18 s.
    (a) What is `P*`?
    (b) How long does the quest take for 6 players?
    (c) What respawn time, or what number of spawns, brings 6 players down to 5 minutes?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 1.92. (b) 675 s, 11.25 minutes. (c) `T ≤ 33.3` s, or `M ≥ 18`.

(a) `P* = M t_k / T = 8 × 18 / 75 = 1.92`. Two players already make the camp supply-limited.

(b) Supply gives `T P / M = 75 × 6 / 8 = 56.25` s per kill, more than 18, so `time = 12 × 56.25 = 675` s.

(c) For 300 s you need `T × 6 / 8 ≤ 25`, so `T ≤ 33.3` s, or with `T = 75`, `M ≥ 75 × 6 / 25 = 18`. Check that skill doesn't bind: `12 × 18 = 216` s, under 300, so it doesn't.
</details>

51. *Week 12 · compute.* A world has 4 rare ore rocks, each respawning 15 minutes after it is mined. Five players mine them full time.
    (a) How much ore does each player get per hour?
    (b) The team wants each of the five to get 8 ore per hour. Give two ways to reach it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 3.2 ore per hour. (b) 10 rocks at 15 minutes, or 4 rocks at 6 minutes.

(a) Each rock gives `60 / 15 = 4` ore per hour, so 16 in all, split five ways: 3.2.

(b) Five players at 8 need 40 ore per hour. At 4 per rock per hour that is 10 rocks. With 4 rocks, each must give 10 per hour, a 6-minute respawn. The first spreads players across more places. The second keeps them together and makes each rock less of an event.
</details>

## Week 13: Metrics: player speed, jump, scale

52. *Week 13 · compute.* A controller has a launch speed of 5.4 m/s, gravity 18 m/s², run speed 7 m/s and a box 0.5 m wide.
    (a) Compute `h` and `t_h`.
    (b) Compute the widest gap on the flat and to a ledge 0.6 m up.
    (c) Under the course margins (80% of `G`, 90% of `h`), what is the comfortable gap to the 0.6 m ledge?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.81 m, 0.30 s. (b) 4.70 m and 3.67 m. (c) Up to 2.94 m.

(a) `h = 5.4² / 36 = 0.81` m. `t_h = 5.4 / 18 = 0.30` s.

(b) Rise distance `7 × 0.3 = 2.1` m. Flat `G = 2.1 × 2 + 0.5 = 4.70` m. For `Δy = 0.6`: `sqrt(1 − 0.6/0.81) = sqrt(0.259) = 0.509`, so `G = 2.1 × 1.509 + 0.5 = 3.67` m.

(c) The ledge is at `0.6 / 0.81 = 74%` of the jump height, under 90%, so the height is fine. The comfortable gap is `0.8 × 3.67 = 2.94` m.
</details>

53. *Week 13 · analysis.* Audit these Quake jumps at a run (`h = 45.56`, `t_h = 0.3375`, `v = 320`, `w = 32`). Classify each as comfortable (gap at most 80% of `G` and `Δy` at most 90% of `h`), skill or impossible.

| Jump | Gap | `Δy` |
|---|---|---|
| 1 | 190 | 30 |
| 2 | 120 | 42 |
| 3 | 150 | 20 |
| 4 | 260 | 0 |
| 5 | 280 | `−h` (a full jump height down) |

<details>
<summary>Answer and worked solution</summary>

**Answer:** 1 skill, 2 skill, 3 comfortable, 4 impossible, 5 skill.

| Jump | `Δy / h` | `G(Δy)` | Gap / `G` | Band |
|---|---|---|---|---|
| 1 | 0.66 | 203.1 | 93.5% | skill (gap above 80%) |
| 2 | 0.92 | 170.2 | 70.5% | skill (height above 90%) |
| 3 | 0.44 | 220.9 | 67.9% | comfortable |
| 4 | 0 | 248.0 | 104.8% | impossible |
| 5 | −1.0 | 292.7 | 95.6% | skill |

For example, jump 1: `108 × (1 + sqrt(1 − 30/45.56)) + 32 = 108 × 1.584 + 32 = 203.1`. Jump 2 has a short gap, but its ledge is so near the apex that a small timing error lands the player short, which is why the height rule exists. Jump 4 also fails the gym measurement: the measured Quake maximum is 244, and 260 is beyond it.
</details>

54. *Week 13 · compute.* A new character has a collision box 0.5 m wide and 1.8 m tall, a step height of 0.45 m, a jump of 1.3 m and a run speed of 7 m/s. Give the body-height ratios for step and jump, the speed in bodies per second, and the course's building metrics for corridors, ceiling and ledges.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Step 0.25, jump 0.72, speed 3.9 bodies per second. Minimum corridor 1.0 m, comfortable corridor 2.0 m, comfortable ceiling about 4.1 m, comfortable jump ledge at most 1.17 m, blocking wall taller than 1.3 m plus a margin.

Ratios: `0.45 / 1.8 = 0.25`, `1.3 / 1.8 = 0.72` and `7 / 1.8 = 3.9`. These sit in the range of the lecture's three games.

Building metrics: `2 × 0.5 = 1.0` m and `4 × 0.5 = 2.0` m for corridors, `2.3 × 1.8 = 4.1` m for a comfortable ceiling, `0.9 × 1.3 = 1.17` m for a comfortable jump ledge. A blocking wall must beat 1.3 m plus a stated margin and every other climbing verb the character has. A third-person camera needs more room than these first-person multipliers, so check them in the gym.
</details>

55. *Week 13 · analysis.* Minecraft's attributes give a jump strength of 0.42 blocks per tick and gravity of 0.08 blocks per tick². What jump height does `v₀² / 2g` predict, how far is that from the game's measured 1.2522 blocks, and which number should a designer use when sizing a fence?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 1.10 blocks, about 12% below the measured 1.2522. Use the measured value.

`0.42² / (2 × 0.08) = 0.1764 / 0.16 = 1.1025`. The error is `(1.2522 − 1.1025) / 1.2522 = 12%`. The game steps its physics once per tick, which the smooth formula leaves out. A fence sized from the formula (say 1.2 blocks) would be jumpable. Minecraft's fence collides at 1.5 blocks, 0.25 above the measured jump. Use the model to understand the shape of the envelope and the gym for the numbers.
</details>

## Week 14: Playtesting levels with heatmaps

56. *Week 14 · compute.* A playtest has a level-wide death rate `r̄ = 0.06`. Use `k = 15`. Cell A had 3 deaths in 8 visits, cell B 18 deaths in 150 visits and cell C 9 deaths in 60 visits.
    (a) Rank the cells by death count, raw rate and shrunk rate.
    (b) Which cell would you investigate first, and what would you do about the others?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Count: B, C, A. Raw: A (0.375), C (0.150), B (0.120). Shrunk: A (0.170), C (0.132), B (0.115). (b) Start with C and B, and send testers through A.

(a) `k r̄ = 0.9`. A: `(3 + 0.9) / (8 + 15) = 0.170`. B: `(18 + 0.9) / 165 = 0.115`. C: `(9 + 0.9) / 75 = 0.132`.

(b) A tops the shrunk ranking even after shrinkage, but it rests on 8 visits. C is more than twice the level rate over 60 visits, and B is twice the level rate over 150 visits, so both are real. Watch the recordings of deaths in C and B now, and run a targeted test through A to learn whether its rate holds. B also has the most deaths in total, so it wastes the most player time even though a single visit there is safer than in C.
</details>

57. *Week 14 · compute.* A cell's measured death rate is 0.15 over 36 visits. What is its standard error? How many visits would bring the standard error down to 0.03?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0.060. About 142 visits.

`sqrt(0.15 × 0.85 / 36) = sqrt(0.00354) = 0.060`. For 0.03: `v = 0.15 × 0.85 / 0.03² = 0.1275 / 0.0009 = 141.7`, so 142 visits. Halving the error takes four times the visits.
</details>

58. *Week 14 · analysis.* A single-player game logged 1,200 deaths on its first map, which all 800 testers played. Its third map logged 540 deaths, but only 300 testers reached it. A producer reads this as "map 3 is less than half as deadly." Correct the comparison.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Per player who reached it, map 3 is 20% more deadly: 1.8 deaths against 1.5.

Map 1: `1,200 / 800 = 1.5` deaths per player. Map 3: `540 / 300 = 1.8`. The raw count, `540 / 1,200 = 45%`, ignores attrition. Map 3 had fewer players, not fewer deaths per player. Always divide by the players or visits that reached the place.
</details>

59. *Week 14 · critique.* A teammate presents a heatmap from a 6-tester playtest. It is coloured by raw death rate (`k = 0`) on 1 m cells, and the hottest cell shows 100%. Asked about `k`, they say they tried several values and chose the one that "matched what we saw in testing." Name three problems and the fix for each.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Raw rates on thin data, cells too small for the sample, and `k` chosen after looking.

- **Raw rate with few visits.** A 100% cell is almost certainly one death in one visit, the least reliable cell on the map. Use the shrunk rate, report `v` beside every rate, or hide cells below a visit count.
- **Cell size.** With 6 testers, 1 m cells get very few visits each, so the standard error is huge. Choose the cell from the smallest feature you need to see, check that the routes you care about have more visits per cell than `k`, and compare two cell sizes.
- **`k` tuned to the expected answer.** Then the map can only confirm what the team already believed. Choose `k` before looking (often 10 to 30 for a class playtest), then check that the top of the ranking is stable when `k` doubles.

Finally, pair the hot cell with recordings of what players did there before proposing a change.
</details>

## Across weeks

60. *Weeks 1 and 12 · compute.* To lower its exposure, a spawn is moved so that the walk to the first challenge grows from 20 m to 60 m. The respawn delay is 3 s and the player runs at 6 m/s. For a challenge with `t = 10` s and `p = 0.4`, compute `r`, `E[T]` and the penalty ratio before and after.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Before, `r = 6.33` s, `E[T] = 34.5` s and a ratio of 1.38. After, `r = 13.0` s, `E[T] = 44.5` s and a ratio of 1.78.

`r = 3 + 20/6 = 6.33` and `3 + 60/6 = 13`. `E[T] = (10 + r × 0.6) / 0.4`, giving 34.5 and 44.5. Ratio `1 + (r/10) × 0.6`, giving 1.38 and 1.78. Safety from camping cost learners 10 s per clear. That trade is fine near a hard fight players attempt a few times. It is poor next to a beat where learners fail often.
</details>

61. *Weeks 11 and 12 · compute.* A zone with `H = 10` camps and `f = 0.5` has 260 players. One camp is competitive, with 10 spawns, a 40 s respawn and a lone kill time of 12 s. How many players are at that camp, what is `P*`, and how long does an 8-kill quest take?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 13 players, `P* = 3`, 416 s.

`N_camp = 0.5 × 260 / 10 − 1 = 12` others, so 13 players at the camp. `P* = 10 × 12 / 40 = 3`. Supply sets the pace: `40 × 13 / 10 = 52` s per kill, so `8 × 52 = 416` s, about 7 minutes for a quest a lone player finishes in 96 s. A population inside the week 11 band can still be a queue at a competitive camp.
</details>

62. *Weeks 3 and 9 · analysis.* Treat the travel gap between POIs as a rest in the week 3 intensity model, with `d = 0.5` per 10 s. What fraction of a POI's peak intensity is left when the next POI arrives for a walker with a 30 s gap, and for a rider with a 15 s gap? What does that say about mounts and pacing?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 12.5% for the walker, about 35% for the rider.

30 s is three half-lives: `0.5³ = 0.125`. 15 s is 1.5 half-lives: `0.5^1.5 = 0.354`. The rider arrives at each POI with a third of the last one's intensity still present, so fights stack as they did in the lecture's `E = 30, 0, 0, 30` example. A mount shortens every valley along with every gap. If a mounted zone should still breathe, space its intense POIs by time at the mounted speed, or add rests the rider must stop for.
</details>

63. *Weeks 4 and 7 · analysis.* A 30 m landmark tower stands on a clifftop 12 m above a valley. From the valley, 200 m from the cliff foot, the player's eye is 1.8 m above the ground. The tower stands 20 m back from the cliff edge. With a 90° view at 16:9 and `f_min = 2%`, is the tower legible by size? Ignoring the view angle, how much of the tower can the player see over the cliff edge?

<details>
<summary>Answer and worked solution</summary>

**Answer:** By size, yes: `d_max = 1,333` m. The edge hides the bottom metre, so about 29 m of the tower shows, which is still enough.

`d_max = 30 / 0.0225 = 1,333` m, far beyond 220 m. For occlusion, the sightline from the eye (1.8 m) over the cliff edge (12 m at 200 m) rises `10.2 / 200 = 0.051` per metre. At the tower, 220 m from the player, that line is at `1.8 + 0.051 × 220 = 13.02` m, 1.02 m above the clifftop. So the bottom 1 m of the tower is hidden and the top 28.98 m, about 29 m, is visible. Move the tower 100 m back from the edge and the hidden part grows to `1.8 + 0.051 × 300 − 12 = 5.1` m. Week 4's rule applies: check landmarks from the low positions, not only the high ones.
</details>
