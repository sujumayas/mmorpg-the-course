# PR301 · Peer assessment brief: from a team mark to your mark

**Weight:** 10% of the course grade (the peer review half of the "post-mortem and peer review" component). The ratings and the team's records also set a factor that adjusts your share of the team components, which are 80% of the grade.
**Rounds:** week 4 (practice, no effect on marks), week 10 (after the alpha weekend) and week 15 (after the showcase).
**Work mode:** individual and confidential. Nobody on your team sees your ratings.
**Builds on:** the [PR201 peer assessment](../../PR201-studio-project-i-multiplayer-vertical-slice/assessments/peer-assessment-brief.md), which you used last year, and [PR101 week 11, communication and conflict in teams](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w11-communication-and-conflict-in-teams.md) (the free-rider model). The records half uses the focus factor from [week 3](../lectures/w03-sprint-1-world-server-and-login.md) and [week 4](../lectures/w04-sprint-1-review.md), and the on-call rota from [week 9](../lectures/w09-alpha-first-persistent-weekend.md).

## Why PR301 changes the PR201 scheme

The PR201 scheme rested on peer ratings, with records used only to check large adjustments. PR301 teams are larger, usually seven, and the course produces better records. Every story has an owner and an estimate in hours, the tracker says which ones met the definition of done, and the on-call rota and incident log say who held the pager at 3 am. So this course's scheme, which is its own and not taken from a published method, makes two changes.

- **Records count directly.** 30% of your score comes from your personal focus factor: estimated hours of done stories you owned, divided by the hours you agreed to in the team charter.
- **Operations duty is rated.** One of the five peer criteria is on-call shifts, drills and the incident log. A persistent world needs people who turn up when the alarm goes, and that work leaves no commits.

## How the grade is built

The team mark `T`, out of 100, is the weighted mean of the team components.

```
T = (4·M1 + 6·M2 + 14·SR + 10·A + 7·TR + 9·B + 30·F) / 80
```

| Symbol | Component | Brief | Course weight |
|---|---|---|---|
| M1 | Pitch and pillars | [m1](m1-pitch-and-pillars-brief.md) | 4% |
| M2 | Architecture review | [m2](m2-architecture-review-brief.md) | 6% |
| SR | Sprint reviews 1 to 5 (weighted 3, 3, 3, 2.5, 2.5) | [m3](m3-sprint-reviews-brief.md) | 14% |
| A | Alpha persistent weekend | [m4](m4-alpha-persistent-weekend-brief.md) | 10% |
| TR | Telemetry review | [m5](m5-telemetry-review-brief.md) | 7% |
| B | Beta open class playtest | [m6](m6-beta-open-class-playtest-brief.md) | 9% |
| F | Final world | [final](final-world-brief.md) | 30% |
| PM | Post-mortem and viva | [post-mortem](post-mortem-brief.md) | 10% |
| PR | Peer review component (this brief) | below | 10% |

Milestones total 50%, the final world 30%, and post-mortem plus peer review 20%, which is the course's assessment line. Your course mark is

```
course mark = 0.80 × min(100, T × F) + 0.10 × PM + 0.10 × PR
```

where `F` is your **contribution factor**, defined below.

## The rating form

In each round you rate every teammate, and yourself, on five criteria from 0 to 4. The anchors are fixed so that a 3 means the same on every team.

| Criterion | 0 | 2 | 4 |
|---|---|---|---|
| Committed work delivered | Most commitments not done | About what was committed, some late or dropped | Everything committed done, or dropped by the agreed drop order |
| Quality | Work often reopened, or broke the soak or the restart check | Met the definition of done after rework | Met every line (test host, restart, bot check) first time |
| Operations duty | Missed shifts or drills; no incident log entries | Covered shifts when asked; log kept | Covered a fair share of shifts and drills, ran the runbook, wrote clear log entries |
| Shared work (reviews, merges, triage, playtests) | None | Did a share when asked | Took a fair share without being asked |
| Communication and reliability | Blockers hidden; missed stand-ups | Blockers raised late | Blockers raised within a day; swaps made in the rota file |

Every 0, 1 or 4 needs a one-line comment naming the evidence: a ticket, a commit, a rota slot, an incident log entry or a date. A rating without it is treated as a 2 for that criterion.

Rate against the availability each person agreed in the charter. A teammate with a job who agreed to 6 hours a week and delivered them scores as well as one who agreed to 10 and delivered 10.

## The formula

For rater `r` and teammate `j`, let `t_rj` be the total of `r`'s five ratings for `j` (0 to 20). Self-ratings are collected but left out.

```
peer share    p_j = (n − 1) × mean over raters r ≠ j of ( t_rj / Σ_{k ≠ r} t_rk )
focus factor  φ_j = estimated hours of done stories owned by j / hours j agreed in the charter
records share q_j = φ_j / mean over the team of φ
blend         s_j = 0.7 × p_j + 0.3 × q_j
factor        F_j = clamp(1 + 0.5 × (s_j − 1), 0.70, 1.10)
```

- Each rater hands out a total of 1 across their teammates, so a rater who gives everyone 20 has the same effect as one who gives everyone 10. Only the differences a rater draws count.
- Both `p` and `q` average exactly 1 across a team, so an average contributor has `F = 1`.
- The records share uses hours of **done** stories at their **estimate**, as in the week 3 focus factor. A story finished late counts in the round it met the definition of done. A story dropped by the agreed drop order does not count against anyone.
- The factor is damped by 0.5 and clamped between 0.70 and 1.10, and `T × F` is capped at 100.
- The week 10 and week 15 rounds combine as `s = 0.4 × s_week10 + 0.6 × s_week15` before `F` is computed. The week 4 round is practice. Each student sees only their own result.

## Worked example

The *Saltmarsh* team from the session guides is seven people: Ana, Ben and Chen (programmers), Dee (designer), Eli and Fay (artists) and Gus (producer). The ratings, hours and marks below are invented for teaching, and nothing in the guides implies that any of them behaved this way.

The team scored M1 = 82, M2 = 78, SR = 71, A = 64, TR = 86, B = 74 and F = 72.

```
T = (4·82 + 6·78 + 14·71 + 10·64 + 7·86 + 9·74 + 30·72) / 80
  = (328 + 468 + 994 + 640 + 602 + 666 + 2160) / 80 = 5858 / 80 = 73.22
```

For brevity the example uses only the week 15 round. The table gives each rater's five criteria summed. Self-ratings are in brackets and ignored.

| Rater → rates | Ana | Ben | Chen | Dee | Eli | Fay | Gus |
|---|---|---|---|---|---|---|---|
| Ana | (17) | 16 | 17 | 15 | 8 | 16 | 15 |
| Ben | 17 | (18) | 9 | 15 | 9 | 15 | 16 |
| Chen | 18 | 15 | (16) | 16 | 7 | 16 | 15 |
| Dee | 17 | 15 | 17 | (15) | 9 | 17 | 16 |
| Eli | 16 | 16 | 16 | 16 | (18) | 16 | 16 |
| Fay | 17 | 16 | 18 | 15 | 8 | (16) | 16 |
| Gus | 17 | 16 | 17 | 16 | 9 | 16 | (17) |

From the tracker and the charter, weeks 3 to 14:

| | Ana | Ben | Chen | Dee | Eli | Fay | Gus |
|---|---|---|---|---|---|---|---|
| Done hours owned | 27 | 26 | 28 | 25 | 12 | 24 | 23 |
| Hours agreed | 78 | 78 | 78 | 74 | 78 | 78 | 78 |

The agreed hours are 6.5 a week for 12 weeks, the week 3 figure after coordination cost. Dee agreed 74 because of a mid-term week.

Check Ana's peer share by hand. Ben gives her `17 / 81 = 0.210` of his points, Chen `18 / 87 = 0.207`, Dee `17 / 91 = 0.187`, Eli `16 / 96 = 0.167`, Fay `17 / 90 = 0.189` and Gus `17 / 91 = 0.187`. The mean is 0.191, and `6 × 0.191 = 1.146`. Her focus factor is `27 / 78 = 0.346`, against a team mean of 0.305, so her records share is 1.136. Her blend is `0.7 × 1.146 + 0.3 × 1.136 = 1.143`, and `F = 1 + 0.5 × 0.143 = 1.072`.

The whole calculation, with the leave-one-rater-out check described in the safeguards, runs with `.venv/bin/python` (Python 3.13):

```python
# PR301 peer adjustment, worked example (Saltmarsh, week 15 round)
# ratings[rater][ratee] = total over 5 criteria, each 0 to 4 (max 20). Self entries are ignored.
ratings = {
    "Ana":  {"Ana": 17, "Ben": 16, "Chen": 17, "Dee": 15, "Eli": 8,  "Fay": 16, "Gus": 15},
    "Ben":  {"Ana": 17, "Ben": 18, "Chen": 9,  "Dee": 15, "Eli": 9,  "Fay": 15, "Gus": 16},
    "Chen": {"Ana": 18, "Ben": 15, "Chen": 16, "Dee": 16, "Eli": 7,  "Fay": 16, "Gus": 15},
    "Dee":  {"Ana": 17, "Ben": 15, "Chen": 17, "Dee": 15, "Eli": 9,  "Fay": 17, "Gus": 16},
    "Eli":  {"Ana": 16, "Ben": 16, "Chen": 16, "Dee": 16, "Eli": 18, "Fay": 16, "Gus": 16},
    "Fay":  {"Ana": 17, "Ben": 16, "Chen": 18, "Dee": 15, "Eli": 8,  "Fay": 16, "Gus": 16},
    "Gus":  {"Ana": 17, "Ben": 16, "Chen": 17, "Dee": 16, "Eli": 9,  "Fay": 16, "Gus": 17},
}
# records: estimated hours of done stories owned (tracker) and hours agreed in the charter, weeks 3 to 14
done   = {"Ana": 27, "Ben": 26, "Chen": 28, "Dee": 25, "Eli": 12, "Fay": 24, "Gus": 23}
agreed = {"Ana": 78, "Ben": 78, "Chen": 78, "Dee": 74, "Eli": 78, "Fay": 78, "Gus": 78}
W_PEER, W_REC = 0.7, 0.3         # blend of peer share and records share
W, LO, HI = 0.5, 0.70, 1.10      # damping, factor floor and cap
REVIEW = 0.06                    # leave-one-rater-out threshold
marks   = {"M1": 82, "M2": 78, "SR": 71, "A": 64, "TR": 86, "B": 74, "F": 72}
weights = {"M1": 4,  "M2": 6,  "SR": 14, "A": 10, "TR": 7,  "B": 9,  "F": 30}
num = sum(weights[k] * marks[k] for k in marks)
T = num / 80
print(f"team mark T = {num} / 80 = {T:.2f}")

def peer_shares(ratings, skip=None):
    names = list(ratings); n = len(names)
    got = {j: [] for j in names}
    for r, row in ratings.items():
        if r == skip:
            continue
        peers = {j: v for j, v in row.items() if j != r}
        total = sum(peers.values())
        for j, v in peers.items():
            got[j].append(v / total)          # share of rater r's points given to j
    return {j: (n - 1) * sum(f) / len(f) for j, f in got.items()}

pf = {j: done[j] / agreed[j] for j in done}   # personal focus factor
mean_pf = sum(pf.values()) / len(pf)
rec = {j: pf[j] / mean_pf for j in pf}        # records share, team mean 1

def table(p, title):
    print(f"\n{title}")
    print("name  peer   pf     rec    blend  factor  team part")
    out = {}
    for j in p:
        s = W_PEER * p[j] + W_REC * rec[j]
        f = min(HI, max(LO, 1 + W * (s - 1)))
        out[j] = (s, f, min(100, T * f))
        print(f"{j:5} {p[j]:5.3f}  {pf[j]:5.3f}  {rec[j]:5.3f}  {s:5.3f}  {f:5.3f}   {min(100, T * f):6.1f}")
    return out

p = peer_shares(ratings)
table(p, "all raters")
print(f"mean peer share {sum(p.values()) / len(p):.3f}")

print("\nleave-one-rater-out: largest shift in anyone's peer share")
for r in ratings:
    p2 = peer_shares(ratings, skip=r)
    j = max(p, key=lambda k: abs(p2[k] - p[k]))
    flag = "  REVIEW" if abs(p2[j] - p[j]) > REVIEW else ""
    print(f"without {r:5} {j:5} {p[j]:.3f} -> {p2[j]:.3f} (shift {p2[j] - p[j]:+.3f}){flag}")

res = table(peer_shares(ratings, skip="Ben"), "after review: Ben's rating set excluded")
pm = {"Ana": 80, "Ben": 72, "Chen": 84, "Dee": 76, "Eli": 58, "Fay": 78, "Gus": 81}
pr = {"Ana": 90, "Ben": 45, "Chen": 88, "Dee": 92, "Eli": 70, "Fay": 85, "Gus": 86}
print("\nname  team part  PM  PR  course mark")
for j, (s, f, tp) in res.items():
    print(f"{j:5} {tp:9.1f}  {pm[j]:2}  {pr[j]:2}  {0.80 * tp + 0.10 * pm[j] + 0.10 * pr[j]:11.1f}")
```

It prints:

```
team mark T = 5858 / 80 = 73.22

all raters
name  peer   pf     rec    blend  factor  team part
Ana   1.146  0.346  1.136  1.143  1.072     78.5
Ben   1.041  0.333  1.094  1.057  1.029     75.3
Chen  1.047  0.359  1.178  1.086  1.043     76.4
Dee   1.051  0.338  1.109  1.068  1.034     75.7
Eli   0.570  0.154  0.505  0.551  0.775     56.8
Fay   1.082  0.308  1.010  1.061  1.030     75.4
Gus   1.063  0.295  0.968  1.034  1.017     74.5
mean peer share 1.000

leave-one-rater-out: largest shift in anyone's peer share
without Ana   Chen  1.047 -> 1.022 (shift -0.025)
without Ben   Chen  1.047 -> 1.123 (shift +0.076)  REVIEW
without Chen  Ana   1.146 -> 1.127 (shift -0.019)
without Dee   Chen  1.047 -> 1.032 (shift -0.015)
without Eli   Ana   1.146 -> 1.175 (shift +0.029)
without Fay   Chen  1.047 -> 1.016 (shift -0.031)
without Gus   Chen  1.047 -> 1.032 (shift -0.015)

after review: Ben's rating set excluded
name  peer   pf     rec    blend  factor  team part
Ana   1.123  0.346  1.136  1.127  1.064     77.9
Ben   1.041  0.333  1.094  1.057  1.029     75.3
Chen  1.123  0.359  1.178  1.139  1.070     78.3
Dee   1.039  0.338  1.109  1.060  1.030     75.4
Eli   0.551  0.154  0.505  0.537  0.769     56.3
Fay   1.077  0.308  1.010  1.057  1.028     75.3
Gus   1.038  0.295  0.968  1.017  1.009     73.8

name  team part  PM  PR  course mark
Ana        77.9  80  90         79.3
Ben        75.3  72  45         72.0
Chen       78.3  84  88         79.9
Dee        75.4  76  92         77.1
Eli        56.3  58  70         57.8
Fay        75.3  78  85         76.5
Gus        73.8  81  86         75.8
```

### Reading the result

**Eli.** Six of six raters gave Eli 7 to 9 out of 20, and the tracker agrees. Eli owned 12 done hours against 78 agreed, a focus factor less than half the team's. Undamped, Eli's blend of 0.551 would cut the team part almost in half. With the damping it gives a factor of 0.775. That is below 0.90, so the evidence gate applies. The instructor opens the board, the rota and the hours log. Eli's week 3 character model (S12) was dropped by the drop order, which does not count against anyone. But the tracker shows two later stories reassigned to Fay after going untouched for a sprint, and the rota shows two alpha shifts swapped away in chat rather than in the rota file. Eli's week 10 round was 0.71, and Eli met the instructor in week 11 with a plan. No mitigating circumstances are on file. The factor stands. Eli rated everyone else at 16. That is allowed. It carries no information, so it has no effect on anyone's share.

**Ben and Chen.** Ben rated Chen 9 while the other five rated Chen 15 to 18. Removing Ben moves Chen's peer share by 0.076, above the 0.06 threshold, so Ben's ratings are reviewed. Ben's comment said Chen "changed the protocol without asking". The repository shows the change went through a pull request that Ana and Ben approved, as the week 3 contract rule requires. Chen's done hours put Chen first on the records share. Ben's rating set is excluded for this round, which gives the second table. Chen's factor rises from 1.043 to 1.070. Ben's own factor does not change, because it depends only on how others rated Ben. Ben's peer review component (PR) scores 45, because his ratings were not supported by the records.

**Why the records half matters here.** Eli's peer share and records share agree, so the blend changes little. They would disagree for a teammate who does quiet, well-estimated work that others do not see. The 30% records share protects that person from a popularity vote. The 70% peer share protects the artist whose best week went into reviewing everyone else's assets, which the tracker does not see.

**Final course marks** use the second table. Chen, for example, gets `0.80 × 78.3 + 0.10 × 84 + 0.10 × 88 = 79.9`. The printed figures come from unrounded values, so a hand calculation may differ by 0.1.

## Safeguards

1. **Self-ratings do not count.** They are collected, and the gap between your self-rating and your peers' view is shown to you after weeks 4 and 10.
2. **Normalisation per rater.** High or low raters have no effect. Only the differences a rater draws count.
3. **Records in the score.** 30% of the blend comes from the tracker, so a rating campaign cannot move a factor far on its own.
4. **Damping and limits.** Damping 0.5, floor 0.70, cap 1.10, and no team part above 100.
5. **Evidence gate.** Any factor below 0.90 or above 1.05 is checked by the instructor against the board, the tracker, the hours log, the rota and the incident log before it is released. The instructor can confirm it, move it toward 1 or set it to 1, and records the reason.
6. **Leave-one-rater-out check.** If removing one rater moves anyone's peer share by more than 0.06, that rater's set is reviewed against the records. Unsupported sets are excluded for that round. The threshold is lower than PR201's 0.08 because with seven members each rater carries less weight.
7. **Estimates are owned.** Records use the estimate the owner gave at planning. An estimate raised after planning counts at its planning value. The instructor spot-checks one sprint per team against the saved lab 03 or lab 11 plan.
8. **On-call is recorded where it happens.** Shift swaps count only if they were made in the rota file (week 9). The instructor's random spot-check message during the alpha weekend is evidence for the operations criterion.
9. **No surprises.** A student whose week 10 score is below 0.85 meets the instructor in week 11 with a written plan. A factor below 0.90 at week 15 is allowed only if the student was warned at week 10 or the drop comes from events after week 10 that are on record.
10. **Mitigating circumstances.** A student with documented circumstances has their agreed hours revised, which changes the records share, and their ratings read against the revised availability, or their factor set to 1.
11. **Missing ratings.** Shares are computed from the raters who submitted. A student who does not submit scores 0 on that round's rows in the PR rubric.
12. **Appeals.** A student may appeal their factor within 10 working days of release. A second member of staff hears it, with the records but without knowing who gave which rating.

## Peer review component rubric (PR, 10% of the course)

This rubric marks how you review and keep records, not how you were rated.

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Rounds submitted on time | 15 | Week 10 and week 15 rounds by the deadline, and the week 4 practice round | A round missing |
| Evidence in comments | 30 | Every 0, 1 or 4 cites a ticket, commit, rota slot, log entry or date; comments describe behaviour, not character | Comments missing, vague or personal |
| Hours log and ownership | 20 | Weekly from week 2 with ticket IDs; every story you owned has your estimate from planning | Filled in at the end, or estimates changed after planning |
| Consistency with records | 20 | Ratings agree with the tracker, rota and incident log, or the difference is explained | Set excluded by a safeguard review |
| Week 10 feedback | 15 | One specific, actionable note to each teammate through the form | Generic praise or blame |
| **Total** | **100** | | |
