# PR201 · Peer assessment brief: from a team mark to your mark

**Weight:** 10% of the course grade (the peer review half of the "post-mortem and peer review" component). The ratings also set a factor that adjusts your share of the team components (80% of the grade).
**Rounds:** week 5 (practice, no effect on marks), week 10 (after alpha) and week 15 (after the showcase).
**Work mode:** individual and confidential. Nobody on your team sees your ratings.
**Builds on:** [PR101 week 11, communication and conflict in teams](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w11-communication-and-conflict-in-teams.md), section 2 (the free-rider model and why individual credit `k` has to grow with team size), and [PR101 week 7, definitions of done](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md).

## Why the course adjusts team marks

PR201 teams have five to seven members. PR101 week 11 showed that with a shared grade each member gets `m / n` of the value of every hour they work, and in a team of six that share is small enough to make free riding pay. Individual credit fixes that, but only if it rests on records and cannot be won by being loud. So this scheme has two parts. Teammates rate each other on five criteria, and the instructor checks every large adjustment against the team's records before it counts.

## How the grade is built

The team components are the five milestones and the final slice. Their weighted mean is the **team mark** `T`, out of 100:

```
T = (8·M1 + 10·M2 + 14·M3 + 12·M4 + 6·M5 + 30·S) / 80
```

| Symbol | Component | Brief | Course weight |
|---|---|---|---|
| M1 | Pitch and pre-production | [m1](m1-pitch-and-preproduction-brief.md) | 8% |
| M2 | Technical design document | [m2](m2-technical-design-document-brief.md) | 10% |
| M3 | Alpha | [m3](m3-alpha-brief.md) | 14% |
| M4 | Beta | [m4](m4-beta-brief.md) | 12% |
| M5 | Release candidate | [m5](m5-release-candidate-brief.md) | 6% |
| S | Final slice | [final](final-slice-brief.md) | 30% |
| PM | Post-mortem and viva (individual parts) | [post-mortem](post-mortem-brief.md) | 10% |
| PR | Peer review component (this brief) | below | 10% |

Milestones total 50%, the final slice 30%, and post-mortem plus peer review 20%, which matches the course's assessment line. Your course mark is

```
course mark = 0.80 × min(100, T × F) + 0.10 × PM + 0.10 × PR
```

where `F` is your **peer factor**, defined below.

## The rating form

In each round you rate every teammate, and yourself, on five criteria from 0 to 4. The anchors are fixed so that a 3 means the same thing on every team.

| Criterion | 0 | 2 | 4 |
|---|---|---|---|
| Committed work delivered | Most commitments not done | About what was committed, some late | Everything committed done, on time |
| Quality | Work often reopened or broke the build | Met the definition of done after rework | Met the definition of done first time |
| Shared work (builds, merges, reviews, playtests, triage) | None | Did a share when asked | Took a fair share without being asked |
| Communication and reliability | Missed meetings; blockers hidden | Mostly present; blockers raised late | Present; blockers raised within a day |
| Supporting the team | Made others' work harder | Neutral | Unblocked others, taught, covered as backup |

Every 0, 1 or 4 needs a one-line comment naming the evidence: a ticket, a commit, a date, a meeting. A rating without it is treated as a 2 for that criterion.

Rate contribution **against the availability agreed in the charter**. A teammate who agreed to 6 hours a week because of a job and delivered 6 hours of good work scores as well as one who agreed to 10 and delivered 10.

You also keep a weekly **hours log** in the team repository (date, hours, ticket IDs). It is the record the instructor checks.

## The formula

For rater `r` and teammate `j`, let `t_rj` be the total of `r`'s five ratings for `j` (0 to 20). Self-ratings are collected but left out of the score.

```
f_rj = t_rj / Σ_{k ≠ r} t_rk          share of r's points given to j
s_j  = (n − 1) × mean over raters r ≠ j of f_rj
F_j  = clamp(1 + w × (s_j − 1), 0.75, 1.10),   w = 0.5
```

- Each rater hands out a total of 1 across their `n − 1` teammates, so a rater who scores everyone 20 has the same effect as one who scores everyone 10. Only the **differences** a rater draws between teammates count. This removes the generous rater and the harsh rater.
- `s_j = 1` means an average share. The scores in a team average exactly 1 when everyone submits.
- `w = 0.5` damps the adjustment. A peer score of 0.6 lowers your factor to 0.8, not to 0.6.
- The factor is clamped between 0.75 and 1.10, and `T × F` is capped at 100.
- The week 10 and week 15 rounds are combined as `s = 0.4 × s_week10 + 0.6 × s_week15` before `F` is computed. The week 5 round is practice and each student sees only their own score.

## Worked example

A five-person team from another cohort (not the *Hollowmarch* sample team; Ana, Ben, Chloe, Dev and Eli are invented) scored M1 = 80, M2 = 70, M3 = 68, M4 = 74, M5 = 85 and S = 69. Their team mark is

```
T = (8·80 + 10·70 + 14·68 + 12·74 + 6·85 + 30·69) / 80 = 5760 / 80 = 72.0
```

For brevity the example uses only the week 15 round. The combined score applies the same steps to each round. The totals below are each rater's five criteria summed. Self-ratings are shown but ignored.

| Rater → rates | Ana | Ben | Chloe | Dev | Eli |
|---|---|---|---|---|---|
| Ana | (18) | 16 | 17 | 8 | 16 |
| Ben | 17 | (17) | 16 | 9 | 15 |
| Chloe | 18 | 15 | (16) | 7 | 16 |
| Dev | 16 | 16 | 16 | (16) | 16 |
| Eli | 10 | 16 | 17 | 9 | (19) |

Check Ana's score by hand. Ben gives her `17 / 57 = 0.298` of his points, Chloe `18 / 56 = 0.321`, Dev `16 / 64 = 0.250` and Eli `10 / 52 = 0.192`. The mean is 0.2655, and `4 × 0.2655 = 1.062`.

The whole calculation, with the leave-one-rater-out safeguard described below, runs with `.venv/bin/python` (Python 3.13):

```python
# PR201 peer adjustment, worked example (week 15 round)
# ratings[rater][ratee] = total over 5 criteria, each 0 to 4 (max 20). Self rows are ignored.
ratings = {
    "Ana":   {"Ana": 18, "Ben": 16, "Chloe": 17, "Dev": 8,  "Eli": 16},
    "Ben":   {"Ana": 17, "Ben": 17, "Chloe": 16, "Dev": 9,  "Eli": 15},
    "Chloe": {"Ana": 18, "Ben": 15, "Chloe": 16, "Dev": 7,  "Eli": 16},
    "Dev":   {"Ana": 16, "Ben": 16, "Chloe": 16, "Dev": 16, "Eli": 16},
    "Eli":   {"Ana": 10, "Ben": 16, "Chloe": 17, "Dev": 9,  "Eli": 19},
}
W, LO, HI = 0.5, 0.75, 1.10     # weight of the adjustment, factor floor and cap
TEAM = 72.0                      # team mark on the team components (out of 100)

def scores(ratings, skip=None):
    names = list(ratings)
    n = len(names)
    got = {j: [] for j in names}
    for r, row in ratings.items():
        if r == skip:
            continue
        peers = {j: v for j, v in row.items() if j != r}
        total = sum(peers.values())
        for j, v in peers.items():
            got[j].append(v / total)          # fraction of rater r's points
    return {j: (n - 1) * sum(f) / len(f) for j, f in got.items()}

s = scores(ratings)
print("name   score  factor  mark")
for j, sj in s.items():
    f = min(HI, max(LO, 1 + W * (sj - 1)))
    print(f"{j:6} {sj:5.3f}  {f:5.3f}  {min(100, TEAM * f):5.1f}")
print(f"mean score {sum(s.values()) / len(s):.3f}")

print("\nleave-one-rater-out: largest shift in anyone's score")
for r in ratings:
    s2 = scores(ratings, skip=r)
    j = max(s, key=lambda k: abs(s2[k] - s[k]))
    print(f"without {r:6} {j:6} {s[j]:.3f} -> {s2[j]:.3f} (shift {s2[j] - s[j]:+.3f})")

print("\nafter review: Eli's rating set excluded")
s3 = scores(ratings, skip="Eli")
pm = {"Ana": 78, "Ben": 70, "Chloe": 82, "Dev": 64, "Eli": 74}   # post-mortem component
pr = {"Ana": 90, "Ben": 85, "Chloe": 95, "Dev": 80, "Eli": 40}   # peer review component
print("name   score  factor  team part  course mark")
for j, sj in s3.items():
    f = min(HI, max(LO, 1 + W * (sj - 1)))
    team_part = min(100, TEAM * f)
    course = 0.80 * team_part + 0.10 * pm[j] + 0.10 * pr[j]
    print(f"{j:6} {sj:5.3f}  {f:5.3f}  {team_part:9.1f}  {course:11.1f}")
```

It prints:

```
name   score  factor  mark
Ana    1.062  1.031   74.2
Ben    1.106  1.053   75.8
Chloe  1.156  1.078   77.6
Dev    0.596  0.798   57.5
Eli    1.080  1.040   74.9
mean score 1.000

leave-one-rater-out: largest shift in anyone's score
without Ana    Eli    1.080 -> 1.065 (shift -0.014)
without Ben    Ana    1.062 -> 1.018 (shift -0.044)
without Chloe  Ana    1.062 -> 0.987 (shift -0.075)
without Dev    Chloe  1.156 -> 1.208 (shift +0.052)
without Eli    Ana    1.062 -> 1.160 (shift +0.098)

after review: Eli's rating set excluded
name   score  factor  team part  course mark
Ana    1.160  1.080       77.7         79.0
Ben    1.065  1.032       74.3         75.0
Chloe  1.105  1.053       75.8         78.3
Dev    0.564  0.782       56.3         59.5
Eli    1.080  1.040       74.9         71.3
```

### Reading the result

**Dev.** Three of four raters gave Dev 7 to 9 out of 20, and Dev's score is 0.596. Undamped, that would be a factor of 0.60. With `w = 0.5` it is 0.798. Because 0.798 is below 0.90, the evidence gate applies. The instructor opens the board and the hours log. Dev closed 9 of the 31 estimated hours committed to him across sprints 3 and 4, logged 3 to 4 hours a week against 8 in the charter, and had no mitigating circumstances on file. His week 10 score had been 0.71, and he met the instructor then. The factor stands. Dev also rated everyone, himself included, at 16. That is allowed, and it gives no information, so it has no effect on anyone's score.

**Eli and Ana.** Eli rated Ana 10 while the other three rated her 16 to 18. Removing Eli moves Ana's score by 0.098, above the 0.08 review threshold. Eli's comment said Ana "ignored my art feedback". The records show Ana, as product owner, logged a scope decision on that asset in the decision log with the team's agreement, and her ticket and commit record matches her peers' ratings. The instructor excludes Eli's rating set for this round, which gives the second table. Ana's factor rises from 1.031 to 1.080. Eli's own factor does not change, because it depends only on how others rated Eli. Eli's peer review component (PR) scores 40, because the ratings Eli submitted were not supported by evidence.

**Final course marks** use the second table. Chloe, for example, gets `0.80 × 75.8 + 0.10 × 82 + 0.10 × 95 = 78.3`. The printed figures come from unrounded values, so a hand calculation can differ by 0.1.

## Safeguards

1. **Self-ratings do not count.** They are collected, and a gap between your self-rating and your peers' view is shown to you in weeks 5 and 10 as feedback.
2. **Normalisation per rater.** Handing everyone high or low marks changes nothing. Only differences count.
3. **Damping and limits.** `w = 0.5`, floor 0.75, cap 1.10, and no team part above 100.
4. **Evidence gate.** Any factor below 0.90 or above 1.05 is checked by the instructor against the board, the hours log, commits and the decision log before it is released. The instructor can confirm it, move it toward 1 or set it to 1, and writes down the reason.
5. **Leave-one-rater-out check.** If removing a single rater moves anyone's score by more than 0.08, that rater's ratings are reviewed against the records. Ratings found to be unsupported are excluded for that round.
6. **No surprises.** A student whose week 10 score is below 0.85 meets the instructor in week 11 with a written plan. A factor below 0.90 at week 15 is only allowed if the student was warned at week 10, or if the drop came from events after week 10 that are on record.
7. **Mitigating circumstances.** Ratings measure contribution against agreed availability. A student with documented circumstances has their factor computed against revised availability, or set to 1.
8. **Missing ratings.** Scores are computed from the raters who submitted. A student who does not submit scores 0 for that round's rows in the PR rubric.
9. **Collusion.** Identical rating sets with copied comments from several raters trigger a review of the team's records.
10. **Appeals.** A student may appeal their factor within 10 working days of release. The appeal is heard by a second member of staff, who sees the records but not who gave which rating.

## Peer review component rubric (PR, 10% of the course)

This rubric marks how you review, not how you were rated.

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Rounds submitted on time | 20 | All three rounds by the deadline | A round missing |
| Evidence in comments | 30 | Every 0, 1 or 4 cites a ticket, commit, date or meeting; comments describe behaviour, not character | Comments missing, vague or personal |
| Hours log | 20 | Kept weekly from week 2, with ticket IDs | Filled in at the end, or missing weeks |
| Consistency with records | 15 | Ratings agree with what the board and logs show, or the difference is explained | Ratings excluded by a safeguard review |
| Week 10 feedback | 15 | One specific, actionable note to each teammate, given through the form | Generic praise or blame |
| **Total** | **100** | | |
