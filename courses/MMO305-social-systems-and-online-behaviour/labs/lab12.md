# MMO305 · Lab 12: Reading a loud forum

**Week:** 12 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the field observation assessment (30%)

## Objective

Turn a forum dump into an estimate of how many players are really unhappy, using the voice-ratio model from [week 12](../lectures/w12-community-management.md). You will count posters rather than posts, estimate the voice ratio `ρ` for three topics from a linked random survey, report each topic's true unhappy share with a range, and write the community post that closes the loop.

## Starter materials

- Python 3 with pandas and matplotlib, or a spreadsheet.
- The model from week 12, section 2:
  - forward `o = dρ / (dρ + 1 − d)`
  - inverse `d = o / (o + ρ(1 − o))`
  - voice ratio from a known `d`: `ρ = o(1 − d) / (d(1 − o))`
- The data generator below. Run it once to create two files for a game with 50,000 active players.
  - `mmo305_lab12_forum.csv`: one row per post with `post_id`, `player_id`, `topic` and `sentiment` (`neg` or `pos`). Three topics: `class_rework`, `shop_mount`, `dungeon_timer`. Unhappy players tend to write several posts each.
  - `mmo305_lab12_survey.csv`: a random sample of 600 active players with a 0/1 column per topic saying whether that player is unhappy with it.
- Treat the parameters in `TOPICS` as hidden until step 6.

```python
import numpy as np, csv
rng = np.random.default_rng(12)
N = 50_000                      # active players
TOPICS = {                      # true unhappy share d, voice ratio rho
    "class_rework": (0.25, 4.0),
    "shop_mount":   (0.15, 6.0),
    "dungeon_timer": (0.40, 0.8),
}
P_CONTENT = 0.01                # chance a content player posts on a topic
SURVEY_N = 600

unhappy = {t: rng.random(N) < d for t, (d, rho) in TOPICS.items()}

with open("mmo305_lab12_forum.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["post_id", "player_id", "topic", "sentiment"])
    post_id = 0
    for t, (d, rho) in TOPICS.items():
        p = np.where(unhappy[t], min(1.0, rho * P_CONTENT), P_CONTENT)
        posters = np.nonzero(rng.random(N) < p)[0]
        for pid in posters:
            for _ in range(1 + rng.poisson(1.5 if unhappy[t][pid] else 0.5)):
                post_id += 1
                w.writerow([post_id, pid, t, "neg" if unhappy[t][pid] else "pos"])

sample = rng.choice(N, size=SURVEY_N, replace=False)
with open("mmo305_lab12_survey.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["player_id"] + [f"unhappy_{t}" for t in TOPICS])
    for pid in sample:
        w.writerow([pid] + [int(unhappy[t][pid]) for t in TOPICS])
```

## Steps

1. **Posts or posters.** For each topic, compute the negative share of posts and the negative share of distinct posters. Explain in two sentences why they differ and which one belongs in the model as `o`.
2. **Survey estimate.** For each topic, compute the survey's unhappy share `d̂` and its 95% interval (MA102 week 13).
3. **Voice ratio.** Using the posters' `o` and the survey's `d̂`, compute `ρ` for each topic. Then compute `ρ` at both ends of the survey interval to get a range.
4. **Classify.** For each topic, say whether the forum overstates (`ρ > 1`) or understates (`ρ < 1`) dissatisfaction, and by how much in percentage points.
5. **A topic with no survey.** Next month a fourth topic, a crafting change, has a forum with 62% negative posters and no survey. Using the range of `ρ` you found for the two topics most like it (`class_rework` and `shop_mount`), report a range for `d`. Write the one-sentence version you would send to the design team.
6. **Reveal.** Read the `TOPICS` parameters. How close were your `ρ` and `d` estimates? Which of your ranges contained the true value?
7. **Close the loop.** Write the community post for `class_rework` (at most 200 words). It must state what the team heard, what the survey showed, what the team will do, and when the next update comes.

## Deliverable

Your notebook or spreadsheet, a table with one row per topic (posts share, posters share, `d̂` with interval, `ρ` with range, overstate or understate), the step 5 estimate and sentence, the step 6 comparison, and the step 7 post.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Posts versus posters | Both shares correct, clear reason the posters' share belongs in the model | Shares correct, reason unclear | Uses post share as `o` without comment | 15% |
| Survey and intervals | Correct `d̂` and intervals for all topics | Minor arithmetic errors | Missing | 15% |
| Voice ratios | Correct `ρ` and ranges, correct direction for all three topics including the `ρ < 1` case | One topic wrong | Missing or wrong method | 25% |
| No-survey estimate | Range computed from the right `ρ` range, clear sentence for designers | Range computed, sentence vague | Missing | 20% |
| Community post | Specific, dated, reports the survey honestly, closes the loop, within the word limit | Mostly specific, missing one element | Generic PR text | 25% |

<details>
<summary>Instructor check values</summary>

With seed 12 as given (numpy `default_rng`, PCG64):

| Topic | Posts | Posters | Negative share of posts | Negative share of posters `o` | Survey `d̂` | `ρ` |
|---|---|---|---|---|---|---|
| class_rework | 1,833 | 870 | 66.8% | 54.8% | 21.3% | 4.48 |
| shop_mount | 1,754 | 873 | 64.8% | 51.7% | 16.2% | 5.54 |
| dungeon_timer | 777 | 423 | 49.5% | 36.4% | 41.3% | 0.81 |

- Survey intervals (n = 600): class_rework 18.0% to 24.6%, shop_mount 13.3% to 19.1%, dungeon_timer 37.4% to 45.2%.
- `ρ` ranges from the interval ends: class_rework 3.72 to 5.51, shop_mount 4.52 to 7.01, dungeon_timer 0.69 to 0.96.
- Step 5 with `ρ` from about 3.7 to 7.0: `d` from `0.62 / (0.62 + 7.0 × 0.38) ≈ 18.9%` to `0.62 / (0.62 + 3.7 × 0.38) ≈ 30.5%`. With the point estimates 4.48 and 5.54 only, 22.8% to 26.7%. Either range is acceptable if the method is stated.
- The post share overstates `o` because unhappy players write more posts each (1 + Poisson(1.5) against 1 + Poisson(0.5)). The model's `ρ` is about who posts, so count posters.
- True values: `d` 0.25, 0.15, 0.40 and `ρ` 4, 6, 0.8. The survey's class_rework estimate (21.3%) sits a little low but its interval nearly reaches 0.25; this is normal sampling error, worth one sentence.

</details>
