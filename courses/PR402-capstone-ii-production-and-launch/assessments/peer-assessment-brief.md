# PR402 · Peer assessment brief: from a team mark to your mark

**Weight:** none of its own. The ratings set a peer factor `F` that adjusts your share of every team-marked component (90% of the grade). How well you rate is marked in the [post-mortem brief](post-mortem-brief.md), Part B.
**Rounds:** week 4 after the alpha review (practice, no effect on marks), week 9 after launch, and week 15 after the showcase.
**Work mode:** individual and confidential. Nobody on your team sees your ratings.
**Builds on:** [PR101 week 11, communication and conflict in teams](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w11-communication-and-conflict-in-teams.md), section 2 (why a shared grade rewards free riding as teams grow), and [PR101 week 7, definitions of done](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md). The scheme is this program's own. It uses the same formula as the [PR201 peer assessment](../../PR201-studio-project-i-multiplayer-vertical-slice/assessments/peer-assessment-brief.md), with changes for a live game.

## Why PR402 adjusts team marks

Capstone teams are five to seven people, and most of the marks are team marks. A shared grade in a team of six gives each member a sixth of the value of every hour they put in, which is small enough to make free riding pay (PR101 week 11). So individual marks are adjusted. The adjustment rests on two things: teammates' ratings, and the team's records, which the instructor checks before any large adjustment counts.

PR402 adds one problem earlier studio courses did not have. From week 4, a large share of the team's hours goes to work that never appears as a closed story: on-call shifts, tester support, deploys, incident follow-up, moderation. Week 1 called it the ops tax, and week 11 measured it at more than half of some weeks. A rating scheme that only counts tickets would punish the people who kept the game running. The rating form and the evidence gate below count logged ops hours as delivered work.

## How the grade is built

Every component except the individual half of the post-mortem is marked once per team. Their weighted mean is the **team mark** `T`, out of 100.

```
T = (10·SR + 8·AL + 7·CB + 7·BR + 8·OB + 10·LA + 10·LO + 6·PA + 6·EC + 8·SH + 10·PMT) / 90
```

| Code | Component | Brief | Course weight | Assessment line |
|---|---|---|---|---|
| SR | Sprint reviews (sprints 1 to 4) | [m1](m1-sprint-reviews-brief.md) | 10% | Milestones, 40% |
| AL | Alpha | [m2](m2-alpha-brief.md) | 8% | Milestones |
| CB | Closed beta | [m3](m3-closed-beta-brief.md) | 7% | Milestones |
| BR | Telemetry and balance review | [m4](m4-telemetry-and-balance-review-brief.md) | 7% | Milestones |
| OB | Open beta | [m5](m5-open-beta-brief.md) | 8% | Milestones |
| LA | Launch | [g1](g1-launch-brief.md) | 10% | Launched game, 40% |
| LO | Live-ops operation (weeks 10 and 11) | [g2](g2-live-ops-operation-brief.md) | 10% | Launched game |
| PA | Patch | [g3](g3-patch-brief.md) | 6% | Launched game |
| EC | Economy review | [g4](g4-economy-review-brief.md) | 6% | Launched game |
| SH | The game at the public showcase | [g5](g5-public-showcase-brief.md) | 8% | Launched game |
| PMT | Post-mortem document (team part) | [post-mortem](post-mortem-brief.md) | 10% | Post-mortem, 20% |
| PMI | Reflection, viva and rating conduct (individual part) | [post-mortem](post-mortem-brief.md) | 10% | Post-mortem |

Milestones total 40%, the launched game 40% and the post-mortem 20%, which is the course's assessment line. The milestones are the pre-launch gates. The launched game covers launch, operating it, the patch, the economy review and the game as played at the showcase. Your course mark is

```
course mark = 0.90 × min(100, T × F) + 0.10 × PMI
```

where `F` is your **peer factor**.

## The rating form

In each round you rate every teammate, and yourself, on five criteria from 0 to 4. The anchors are fixed, so a 3 means the same on every team.

| Criterion | 0 | 2 | 4 |
|---|---|---|---|
| Committed work delivered, including logged ops work | Most commitments and rota shifts not done | About what was committed, some late or shifts swapped at short notice | Every commitment and rota shift done on time |
| Quality | Work often reopened, broke the build or caused an incident | Met the definition of done after rework | Met the definition of done first time; fixes held |
| Live operations share (on call, triage, support, deploys, postmortems) | None, or only when chased | Took the rota shifts assigned | Took a fair share, wrote postmortems, improved the runbook |
| Communication and reliability | Missed meetings and reviews; blockers or incidents hidden | Mostly present; blockers raised late | Present; blockers raised within a day; incidents announced on time |
| Supporting the team | Made others' work harder | Neutral | Unblocked others, taught, covered shifts as backup |

Every 0, 1 or 4 needs a one-line comment naming the evidence: a ticket, a commit, a rota date, an incident ID. A rating without it counts as a 2 for that criterion.

Rate contribution **against the availability agreed in the team charter**. Someone who agreed to 10 hours a week and delivered 10 hours of good work scores as well as someone who agreed to 14 and delivered 14. Hours spent on call count as hours, whether or not a page came.

Keep your entries in the team time log (date, hours, ticket or rota ID, tag `feature`, `content` or `ops`), started in [lab 01](../labs/lab01.md). It is the record the instructor checks.

## The formula

For rater `r` and teammate `j`, let `t_rj` be the total of `r`'s five ratings for `j`, from 0 to 20. Self-ratings are collected but left out of the score. With `n` students on the team:

```
f_rj = t_rj / Σ_{k ≠ r} t_rk                    share of r's points given to j
s_j  = (n − 1) × mean over raters r ≠ j of f_rj  peer score, 1 = an average share
F_j  = clamp(1 + w × (s_j − 1), 0.75, 1.10),     w = 0.5
s    = 0.4 × s_week9 + 0.6 × s_week15            rounds combined before F is computed
```

- Each rater hands out a total of 1 across their teammates, so a rater who scores everyone 20 has the same effect as one who scores everyone 10. Only the differences a rater draws between teammates count.
- When everyone submits, the scores in a team average exactly 1.
- `w = 0.5` halves the adjustment. A peer score of 0.6 gives a factor of 0.8, not 0.6.
- `F` is clamped to the range 0.75 to 1.10, and `T × F` is capped at 100.
- The week 4 round is practice. Each student sees only their own score, as early feedback.

## Worked example

A six-person team (Ada, Bo, Cai, Dara, Emre and Fen, all invented) received these component marks.

| SR | AL | CB | BR | OB | LA | LO | PA | EC | SH | PMT |
|---|---|---|---|---|---|---|---|---|---|---|
| 74 | 80 | 70 | 68 | 76 | 82 | 72 | 78 | 66 | 75 | 70 |

Their team mark is `T = 6,658 / 90 = 73.98`. Each cell below is one rater's total for one teammate, out of 20. Self-ratings are in the tables but ignored.

**Week 9 round**

| Rater → rates | Ada | Bo | Cai | Dara | Emre | Fen |
|---|---|---|---|---|---|---|
| Ada | (17) | 16 | 15 | 10 | 15 | 16 |
| Bo | 16 | (18) | 15 | 11 | 12 | 16 |
| Cai | 17 | 15 | (16) | 10 | 16 | 15 |
| Dara | 15 | 15 | 15 | (17) | 15 | 15 |
| Emre | 16 | 14 | 16 | 11 | (16) | 17 |
| Fen | 17 | 16 | 15 | 9 | 16 | (16) |

**Week 15 round**

| Rater → rates | Ada | Bo | Cai | Dara | Emre | Fen |
|---|---|---|---|---|---|---|
| Ada | (17) | 16 | 16 | 9 | 17 | 16 |
| Bo | 16 | (19) | 15 | 10 | 8 | 16 |
| Cai | 17 | 15 | (16) | 8 | 17 | 16 |
| Dara | 14 | 14 | 14 | (18) | 14 | 14 |
| Emre | 16 | 14 | 16 | 9 | (17) | 17 |
| Fen | 17 | 15 | 16 | 8 | 18 | (16) |

Check Dara's week 15 score by hand. Ada gives Dara `9 / 74 = 0.122` of her points, Bo `10 / 65 = 0.154`, Cai `8 / 73 = 0.110`, Emre `9 / 72 = 0.125` and Fen `8 / 74 = 0.108`. The mean is 0.124, and `5 × 0.124 = 0.618`.

The whole calculation, with the leave-one-rater-out check from the safeguards, runs with `.venv/bin/python` (Python 3.13):

```python
# PR402 peer adjustment, worked example (six-person team, invented)
marks = {"SR": 74, "AL": 80, "CB": 70, "BR": 68, "OB": 76,    # milestones, 40%
         "LA": 82, "LO": 72, "PA": 78, "EC": 66, "SH": 75,    # launched game, 40%
         "PMT": 70}                                          # post-mortem, team part, 10%
weights = {"SR": 10, "AL": 8, "CB": 7, "BR": 7, "OB": 8,
           "LA": 10, "LO": 10, "PA": 6, "EC": 6, "SH": 8, "PMT": 10}
T = sum(weights[k] * marks[k] for k in marks) / sum(weights.values())
print(f"team mark T = {T:.2f} (weights sum to {sum(weights.values())})")

# ratings[round][rater][ratee] = total of five criteria, each 0-4 (max 20). Self ratings ignored.
ratings = {
    "wk9": {
        "Ada":  {"Ada": 17, "Bo": 16, "Cai": 15, "Dara": 10, "Emre": 15, "Fen": 16},
        "Bo":   {"Ada": 16, "Bo": 18, "Cai": 15, "Dara": 11, "Emre": 12, "Fen": 16},
        "Cai":  {"Ada": 17, "Bo": 15, "Cai": 16, "Dara": 10, "Emre": 16, "Fen": 15},
        "Dara": {"Ada": 15, "Bo": 15, "Cai": 15, "Dara": 17, "Emre": 15, "Fen": 15},
        "Emre": {"Ada": 16, "Bo": 14, "Cai": 16, "Dara": 11, "Emre": 16, "Fen": 17},
        "Fen":  {"Ada": 17, "Bo": 16, "Cai": 15, "Dara": 9,  "Emre": 16, "Fen": 16},
    },
    "wk15": {
        "Ada":  {"Ada": 17, "Bo": 16, "Cai": 16, "Dara": 9,  "Emre": 17, "Fen": 16},
        "Bo":   {"Ada": 16, "Bo": 19, "Cai": 15, "Dara": 10, "Emre": 8,  "Fen": 16},
        "Cai":  {"Ada": 17, "Bo": 15, "Cai": 16, "Dara": 8,  "Emre": 17, "Fen": 16},
        "Dara": {"Ada": 14, "Bo": 14, "Cai": 14, "Dara": 18, "Emre": 14, "Fen": 14},
        "Emre": {"Ada": 16, "Bo": 14, "Cai": 16, "Dara": 9,  "Emre": 17, "Fen": 17},
        "Fen":  {"Ada": 17, "Bo": 15, "Cai": 16, "Dara": 8,  "Emre": 18, "Fen": 16},
    },
}
W, LO, HI = 0.5, 0.75, 1.10            # damping, factor floor, factor cap
ROUND = {"wk9": 0.4, "wk15": 0.6}      # weight of each counted round
PMI = {"Ada": 76, "Bo": 71, "Cai": 80, "Dara": 58, "Emre": 74, "Fen": 69}  # individual post-mortem part


def scores(table, skip=None):
    """Peer score per student: (n - 1) x mean share of each rater's points."""
    n = len(table)
    got = {j: [] for j in table}
    for r, row in table.items():
        if r == skip:
            continue
        peers = {j: v for j, v in row.items() if j != r}
        total = sum(peers.values())
        for j, v in peers.items():
            got[j].append(v / total)
    return {j: (n - 1) * sum(f) / len(f) for j, f in got.items()}


def factor(s):
    return min(HI, max(LO, 1 + W * (s - 1)))


def report(s9, s15, title):
    print(f"\n{title}")
    print("name   s9     s15    s      F      team part  course mark")
    for j in s9:
        s = ROUND["wk9"] * s9[j] + ROUND["wk15"] * s15[j]
        part = min(100, T * factor(s))
        course = 0.90 * part + 0.10 * PMI[j]
        print(f"{j:5} {s9[j]:6.3f} {s15[j]:6.3f} {s:6.3f} {factor(s):6.3f} {part:9.1f} {course:11.1f}")


s9, s15 = scores(ratings["wk9"]), scores(ratings["wk15"])
report(s9, s15, "all ratings")

print("\nleave-one-rater-out, week 15 (review if any shift > 0.08)")
for r in ratings["wk15"]:
    alt = scores(ratings["wk15"], skip=r)
    j = max(s15, key=lambda k: abs(alt[k] - s15[k]))
    flag = "  <- review" if abs(alt[j] - s15[j]) > 0.08 else ""
    print(f"without {r:5} largest shift {j:5} {s15[j]:.3f} -> {alt[j]:.3f} ({alt[j] - s15[j]:+.3f}){flag}")

report(s9, scores(ratings["wk15"], skip="Bo"), "after review: Bo's week 15 set excluded")
```

It prints:

```
team mark T = 73.98 (weights sum to 90)

all ratings
name   s9     s15    s      F      team part  course mark
Ada    1.111  1.131  1.123  1.061      78.5        78.3
Bo     1.036  1.019  1.026  1.013      74.9        74.5
Cai    1.044  1.085  1.069  1.034      76.5        76.9
Dara   0.705  0.618  0.653  0.826      61.1        60.8
Emre   1.018  1.029  1.025  1.012      74.9        74.8
Fen    1.086  1.118  1.105  1.052      77.9        77.0

leave-one-rater-out, week 15 (review if any shift > 0.08)
without Ada   largest shift Emre  1.029 -> 0.999 (-0.030)
without Bo    largest shift Emre  1.029 -> 1.132 (+0.103)  <- review
without Cai   largest shift Emre  1.029 -> 0.995 (-0.034)
without Dara  largest shift Ada   1.131 -> 1.164 (+0.033)
without Emre  largest shift Fen   1.118 -> 1.102 (-0.016)
without Fen   largest shift Emre  1.029 -> 0.982 (-0.047)

after review: Bo's week 15 set excluded
name   s9     s15    s      F      team part  course mark
Ada    1.111  1.106  1.108  1.054      78.0        77.8
Bo     1.036  1.019  1.026  1.013      74.9        74.5
Cai    1.044  1.068  1.059  1.029      76.1        76.5
Dara   0.705  0.580  0.630  0.815      60.3        60.1
Emre   1.018  1.132  1.087  1.043      77.2        76.9
Fen    1.086  1.089  1.088  1.044      77.2        76.4
```

### Reading the result

**Dara.** Every other rater gave Dara 8 to 11 out of 20 in both rounds. The combined score is 0.653. Undamped, that would be a factor of 0.65. With `w = 0.5` it is 0.826. That is below 0.90, so the evidence gate applies. The instructor opens the board, the time log and the rota. Dara closed 6 of 24 committed points across sprints 3 and 4, logged 4 to 5 hours a week against 12 in the charter, and swapped out of three on-call shifts during launch week without cover. Her week 9 score of 0.705 had triggered a meeting in week 10 with a written plan, so the drop is no surprise. There are no mitigating circumstances on file. The factor stands. Dara rated everyone at 14, which is allowed and carries no information, so it has no effect on anyone's score.

**Bo and Emre.** In week 15 Bo rated Emre 8 while the other four rated him 17 or 18. Removing Bo moves Emre's score by 0.103, above the 0.08 review threshold. Bo's comment said Emre "closed almost no tickets after launch". The records agree about tickets and disagree about work. The team time log and the rota show Emre took 31 on-call hours in weeks 10 to 13, the most on the team, wrote four of the six incident postmortems, and built the watchdog from the week 11 buy-back plan. Bo judged a live-ops role by feature tickets, which the rating form says not to do. The instructor excludes Bo's week 15 rating set, which gives the second table. Emre's factor rises from 1.012 to 1.043. Bo's own factor does not change, because it depends only on how others rated Bo. Bo loses the peer rating conduct row in the post-mortem brief for that round.

**Final course marks** use the second table. Cai, for example, gets `0.90 × 76.1 + 0.10 × 80 = 76.5`. The printed figures come from unrounded values, so a hand calculation can differ by 0.1.

## Safeguards

1. **Self-ratings do not count.** They are collected, and the gap between your self-rating and your peers' view is shown to you after weeks 4 and 9.
2. **Normalisation per rater.** Rating everyone high or everyone low changes nothing. Only differences count.
3. **Damping and limits.** `w = 0.5`, floor 0.75, cap 1.10, and no team part above 100.
4. **Ops work is work.** On-call hours, support, deploys, triage and postmortems logged in the time log count as delivered work. A rating that scores a live-ops role by closed feature tickets is treated as unsupported.
5. **Evidence gate.** Any factor below 0.90 or above 1.05 is checked by the instructor against the board, the time log, the rota, commits, incident records and the decision log before it is released. The instructor can confirm it, move it toward 1, or set it to 1, and writes down the reason.
6. **Leave-one-rater-out check.** If removing a single rater moves anyone's score by more than 0.08 in a round, that rater's ratings are reviewed against the records. A rating set found to be unsupported is excluded for that round.
7. **No surprises.** A student whose week 9 score is below 0.85 meets the instructor in week 10 and agrees a written plan. A factor below 0.90 at week 15 is only allowed if the student was warned after week 9, or if the drop came from events after week 9 that are on record.
8. **Mitigating circumstances.** Ratings measure contribution against agreed availability. A student with documented circumstances has their factor computed against revised availability, or set to 1. Nobody is asked to disclose details to teammates.
9. **Missing ratings.** Scores are computed from the raters who submitted. A student who does not submit loses the rating conduct points for that round.
10. **Collusion.** Identical rating sets with copied comments from several raters trigger a review of the team's records.
11. **Appeals.** A student may appeal their factor within 10 working days of release. A second member of staff hears the appeal with the records but without seeing who gave which rating.
