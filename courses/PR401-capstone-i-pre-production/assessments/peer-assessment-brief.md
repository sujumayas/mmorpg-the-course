# PR401 · Peer assessment brief: from a team mark to your mark

**Applies to:** every team component, 95% of the course grade. The other 5% is the individual viva in the [exam bank](exam-bank.md), which is not adjusted.
**Rounds:** week 6 (after the greenlight), week 11 (after the production plan) and week 15 (with the package).
**Work mode:** individual and confidential. Nobody on your team sees your allocation.
**Builds on:** [PR101 week 11, communication and conflict in teams](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w11-communication-and-conflict-in-teams.md), section 2 (why shared grades invite free riding), [PR101 week 7, task tracking](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md) (the records that back a rating), [PR201's peer assessment brief](../../PR201-studio-project-i-multiplayer-vertical-slice/assessments/peer-assessment-brief.md) (the scheme you used in year 2), and [MMO405 week 4, survey design](../../MMO405-research-methods-in-online-games/lectures/w04-survey-design-and-validated-scales.md) (what a rating form can and cannot measure).

## Why the course adjusts team marks

A capstone team of seven shares one mark on thirteen milestones. Most members work hard, and a few do not, and PR101 week 11 showed that a shared grade pays the ones who do not. The course therefore turns the team mark into an individual mark with a **peer factor**. The scheme below is the course's own. It changes the PR201 scheme in two ways that suit a larger team and a longer project.

- **You split 100 points** among your teammates instead of rating each on a scale. A fixed budget forces you to say who carried more, and makes "everyone gets top marks" impossible.
- **Your score is the median** of the shares your teammates gave you, not the mean. With six raters, one hostile or one friendly rater cannot move the median far. The worked example shows the difference.

The factor is also checked against the team's tracker records. PR401 already requires every hour to be logged and tagged from week 12 (lab 12), so the evidence exists.

## How the team mark is built

Each milestone brief sets a mark out of 100. The **team mark** `T` is their weighted mean:

```
T = (6·M1 + 4·M2 + 4·M3 + 15·M4 + 15·M5 + 6·M6 + 6·M7 + 6·M8 + 5·M9 + 5·M10 + 7·M11 + 10·M12 + 6·M13) / 95
```

| Component (assessment line) | Milestone | Brief | Course weight |
|---|---|---|---|
| Pitch (20%) | M1 Pitch | [m01](m01-pitch-brief.md) | 6% |
| | M2 Market analysis | [m02](m02-market-analysis-brief.md) | 4% |
| | M3 Pillars and vision | [m03](m03-pillars-and-vision-brief.md) | 4% |
| | M6 Greenlight review | [m06](m06-greenlight-review-brief.md) | 6% |
| Prototypes (30%) | M4 Prototype 1 | [m04](m04-prototype-1-brief.md) | 15% |
| | M5 Prototype 2 and evidence table | [m05](m05-prototype-2-brief.md) | 15% |
| Pre-production package (50%) | M7 Technical design | [m07](m07-technical-design-brief.md) | 6% |
| | M8 Economy and balance design | [m08](m08-economy-and-balance-design-brief.md) | 6% |
| | M9 Content plan | [m09](m09-content-plan-brief.md) | 5% |
| | M10 Social systems plan | [m10](m10-social-systems-plan-brief.md) | 5% |
| | M11 Production plan | [m11](m11-production-plan-brief.md) | 7% |
| | M12 Vertical slice | [m12](m12-vertical-slice-brief.md) | 10% |
| | M13 Review and final package | [m13](m13-pre-production-review-and-package-brief.md) | 6% |
| | Individual viva (not peer-adjusted) | [exam bank](exam-bank.md) | 5% |

The components total 20%, 30% and 50%, matching the course's assessment line. Your course mark is

```
course mark = 0.95 × min(100, T × F) + 0.05 × V
```

where `F` is your peer factor and `V` your viva mark out of 100.

## The allocation form

In each round you split exactly 100 points among the other members of your team. You do not rate yourself. An equal split in a team of seven is about 16.7 each.

Allocate for **contribution against the availability agreed in the charter**, looking at four things: committed work delivered, its quality against the definition of done, shared work (builds, merges, reviews, playtests, moderation rota), and reliability in meetings and in raising blockers. A teammate who agreed to 6 hours a week and delivered 6 hours of good work deserves an equal share.

Any allocation below 10 or above 25 needs a one-line comment naming the evidence: a ticket, a commit, a date, a meeting. An allocation outside that range with no comment is reset to the equal share before scores are computed.

## The formula

For rater `r` and teammate `j` in a team of `n`, with `a_rj` the points `r` gave `j`:

```
share_rj = a_rj × (n − 1) / 100          1.0 is an equal share
s_j      = median over raters r ≠ j of share_rj
s        = 0.2 × s_week6 + 0.3 × s_week11 + 0.5 × s_week15
F        = clamp(1 + w × (s − 1), 0.80, 1.10),   w = 0.5
```

- The later rounds count more, because they cover more of the work and because a teammate who had a slow start and recovered should not carry it all semester.
- `w = 0.5` halves the adjustment. A combined score of 0.70 gives a factor of 0.85, not 0.70.
- The factor stays between 0.80 and 1.10, and `T × F` is capped at 100.
- Medians do not average to exactly 1 across a team, so the factors do not either. That is accepted. The cap and floor keep the effect small.

## Worked example: the *Emberfall* team

*Emberfall* is the course's sample team. Its seven members here are invented for this example: Aiko (server), Bruno (gameplay), Carmen (tools and UI), Dmitri (systems and economy design), Efua (content design), Farid (the one artist) and Greta (audio and technical art). The milestone marks are also invented: M1 to M13 = 78, 72, 80, 74, 70, 76, 68, 75, 72, 70, 80, 66, 74. So

```
T = (6·78 + 4·72 + 4·80 + 15·74 + 15·70 + 6·76 + 6·68 + 6·75 + 5·72 + 5·70 + 7·80 + 10·66 + 6·74) / 95
  = 6924 / 95 = 72.88
```

The week 15 allocations (rows are raters, columns the teammates they gave points to):

| Rater | Aiko | Bruno | Carmen | Dmitri | Efua | Farid | Greta |
|---|---|---|---|---|---|---|---|
| Aiko | | 19 | 9 | 17 | 17 | 22 | 16 |
| Bruno | 19 | | 10 | 17 | 16 | 22 | 16 |
| Carmen | 20 | 19 | | 18 | 16 | 12 | 15 |
| Dmitri | 18 | 18 | 9 | | 17 | 22 | 16 |
| Efua | 21 | 20 | 11 | 22 | | 5 | 21 |
| Farid | 19 | 19 | 9 | 17 | 18 | | 18 |
| Greta | 18 | 18 | 10 | 17 | 21 | 16 | |

Check Farid's week 15 score by hand. His column is 22, 22, 12, 22, 5 and 16. Times `6 / 100` gives shares 1.32, 1.32, 0.72, 1.32, 0.30 and 0.96. Sorted, the middle two are 0.96 and 1.32, so the median is 1.14. The mean would be 0.99. Efua's 5 points alone pull the mean down by 0.14.

The full calculation runs with `.venv/bin/python` (Python 3.13.5). The week 6 and week 11 tables are in the script.

```python
# PR401 peer adjustment, worked example for the Emberfall sample team (invented people).
# Each rater splits 100 points across the other six members. Self is not rated.
from statistics import median, mean

NAMES = ["Aiko", "Bruno", "Carmen", "Dmitri", "Efua", "Farid", "Greta"]
N = len(NAMES)

def table(rows):
    """rows: one list per rater, points for the other members in NAMES order (self skipped)."""
    out = {}
    for r, pts in zip(NAMES, rows):
        assert sum(pts) == 100, (r, sum(pts))
        others = [j for j in NAMES if j != r]
        out[r] = dict(zip(others, pts))
    return out

#                  columns = the other six members, in NAMES order
round6 = table([
    [17, 17, 16, 17, 17, 16],   # Aiko  -> Bruno Carmen Dmitri Efua Farid Greta
    [17, 16, 17, 16, 17, 17],   # Bruno -> Aiko Carmen Dmitri Efua Farid Greta
    [17, 17, 16, 17, 17, 16],   # Carmen
    [17, 16, 16, 17, 17, 17],   # Dmitri
    [16, 17, 17, 17, 17, 16],   # Efua
    [17, 17, 16, 16, 17, 17],   # Farid
    [16, 17, 17, 17, 16, 17],   # Greta
])
round11 = table([
    [18, 14, 17, 17, 18, 16],
    [18, 14, 17, 16, 19, 16],
    [18, 17, 17, 16, 17, 15],
    [17, 17, 13, 17, 19, 17],
    [17, 17, 14, 17, 18, 17],
    [18, 17, 13, 17, 18, 17],
    [17, 17, 14, 17, 17, 18],
])
round15 = table([
    [19, 9, 17, 17, 22, 16],    # Aiko
    [19, 10, 17, 16, 22, 16],   # Bruno
    [20, 19, 18, 16, 12, 15],   # Carmen
    [18, 18, 9, 17, 22, 16],    # Dmitri
    [21, 20, 11, 22, 5, 21],    # Efua
    [19, 19, 9, 17, 18, 18],    # Farid
    [18, 18, 10, 17, 21, 16],   # Greta
])
ROUNDS = {"w6": (round6, 0.2), "w11": (round11, 0.3), "w15": (round15, 0.5)}
W, LO, HI = 0.5, 0.80, 1.10

def received(tab, j, skip=None):
    """Shares j received, scaled so an equal split is 1.0."""
    return [tab[r][j] * (N - 1) / 100 for r in NAMES if r != j and r != skip]

def score(tab, j, how=median, skip=None):
    return how(received(tab, j, skip))

def factor(s):
    return min(HI, max(LO, 1 + W * (s - 1)))

# Team mark from the 13 milestone briefs (weights are course percentages, sum 95).
weights = [6, 4, 4, 15, 15, 6, 6, 6, 5, 5, 7, 10, 6]
marks   = [78, 72, 80, 74, 70, 76, 68, 75, 72, 70, 80, 66, 74]
T = sum(w * m for w, m in zip(weights, marks)) / sum(weights)
print(f"team mark T = {sum(w * m for w, m in zip(weights, marks))} / {sum(weights)} = {T:.2f}")

print("\nround 15 scores, mean of shares vs median of shares")
for j in NAMES:
    print(f"{j:7} mean {score(round15, j, mean):.3f}  median {score(round15, j):.3f}")

print("\ncombined score s = 0.2*w6 + 0.3*w11 + 0.5*w15 (medians)")
S = {}
for j in NAMES:
    parts = {k: score(t, j) for k, (t, _) in ROUNDS.items()}
    S[j] = sum(score(t, j) * wt for t, wt in ROUNDS.values())
    print(f"{j:7} w6 {parts['w6']:.3f}  w11 {parts['w11']:.3f}  w15 {parts['w15']:.3f}  s {S[j]:.3f}")

# Evidence cross-check: task hours logged in the tracker during slice sprints 1-2
# (weeks 12-13) against the hours each member agreed in the charter for those weeks.
agreed = {j: 16 for j in NAMES}
logged = {"Aiko": 13.5, "Bruno": 12.5, "Carmen": 6.0, "Dmitri": 12.0,
          "Efua": 11.5, "Farid": 14.0, "Greta": 12.0}
ratio = {j: logged[j] / agreed[j] for j in NAMES}
team_ratio = mean(ratio.values())
print("\nfactor, evidence check and team part")
print("name    s      F      hours-index  flag              team part")
for j in NAMES:
    F = factor(S[j])
    hi = ratio[j] / team_ratio
    flags = []
    if F < 0.90 or F > 1.05:
        flags.append("gate")
    if abs(S[j] - hi) > 0.25:
        flags.append("mismatch")
    print(f"{j:7} {S[j]:.3f}  {F:.3f}  {hi:11.3f}  {','.join(flags) or '-':16}  {min(100, T * F):6.1f}")

print("\noutlier allocations in round 15 (share more than 0.50 from the member's median)")
for j in NAMES:
    m = score(round15, j)
    for r in NAMES:
        if r != j and abs(round15[r][j] * (N - 1) / 100 - m) > 0.50:
            print(f"{r} -> {j}: {round15[r][j]} points, share {round15[r][j] * (N - 1) / 100:.2f}, median {m:.2f}")

V = {"Aiko": 82, "Bruno": 74, "Carmen": 58, "Dmitri": 77, "Efua": 70, "Farid": 88, "Greta": 72}
print("\ncourse mark = 0.95 * min(100, T*F) + 0.05 * V")
for j in NAMES:
    F = factor(S[j])
    print(f"{j:7} {0.95 * min(100, T * F) + 0.05 * V[j]:5.1f}")
```

It prints:

```
team mark T = 6924 / 95 = 72.88

round 15 scores, mean of shares vs median of shares
Aiko    mean 1.150  median 1.140
Bruno   mean 1.130  median 1.140
Carmen  mean 0.580  median 0.570
Dmitri  mean 1.080  median 1.020
Efua    mean 1.050  median 1.020
Farid   mean 0.990  median 1.140
Greta   mean 1.020  median 0.960

combined score s = 0.2*w6 + 0.3*w11 + 0.5*w15 (medians)
Aiko    w6 1.020  w11 1.050  w15 1.140  s 1.089
Bruno   w6 1.020  w11 1.020  w15 1.140  s 1.080
Carmen  w6 0.990  w11 0.840  w15 0.570  s 0.735
Dmitri  w6 0.990  w11 1.020  w15 1.020  s 1.014
Efua    w6 1.020  w11 1.020  w15 1.020  s 1.020
Farid   w6 1.020  w11 1.080  w15 1.140  s 1.098
Greta   w6 0.990  w11 0.990  w15 0.960  s 0.975

factor, evidence check and team part
name    s      F      hours-index  flag              team part
Aiko    1.089  1.044        1.160  -                   76.1
Bruno   1.080  1.040        1.074  -                   75.8
Carmen  0.735  0.868        0.515  gate                63.2
Dmitri  1.014  1.007        1.031  -                   73.4
Efua    1.020  1.010        0.988  -                   73.6
Farid   1.098  1.049        1.202  -                   76.5
Greta   0.975  0.988        1.031  -                   72.0

outlier allocations in round 15 (share more than 0.50 from the member's median)
Efua -> Farid: 5 points, share 0.30, median 1.14

course mark = 0.95 * min(100, T*F) + 0.05 * V
Aiko     76.4
Bruno    75.7
Carmen   63.0
Dmitri   73.6
Efua     73.4
Farid    77.0
Greta    72.0
```

### Reading the result

**Farid and the median.** Five of six raters gave Farid 12 to 22 points. Efua gave him 5, and her comment said he "ignored the content team's requests". Under a mean, Farid's week 15 score would be 0.99, an average share, for the member the other five saw as the team's strongest. Under the median it is 1.14. The outlier check flags Efua's allocation for review anyway. The instructor reads the week 12 tool decision and the week 11 constraint log. Both record the team agreeing that Farid's hours go to towns first, because art was the constraint. Efua's comment describes a team decision, not Farid's conduct. The allocation stays in the data, since under the median it has no effect, and Efua is told why in her week 15 feedback.

**Carmen and the evidence gate.** Carmen's shares fell each round: 0.99, then 0.84, then 0.57. Her combined score is 0.735 and her factor 0.868. Because that is below 0.90, the gate applies and the instructor opens the records before releasing it. Carmen logged 6 of her 16 agreed hours across slice sprints 1 and 2, an hours index of 0.52 against the team's average. The peer score and the log agree to within 0.25, so there is no mismatch flag. Her week 11 score of 0.84 had triggered the early-warning meeting, and she had no mitigating circumstances on file. The factor stands, and her team part is `72.88 × 0.868 = 63.2`.

**Final course marks** add the viva. Carmen's viva is 58, so her course mark is `0.95 × 63.2 + 0.05 × 58 = 63.0`. Farid's is `0.95 × 76.5 + 0.05 × 88 = 77.0`. The printed figures come from unrounded values, so a hand calculation can differ by 0.1.

## Safeguards

1. **No self-rating.** You cannot give yourself points. A private self-assessment is collected in weeks 6 and 11 and shown back to you next to your median as feedback.
2. **Fixed budget.** Every rater hands out 100 points, so generous and harsh raters have the same total effect. Only the differences a rater draws count.
3. **Median, damping and limits.** The median resists a single outlier, `w = 0.5` halves the adjustment, and the factor stays between 0.80 and 1.10.
4. **Evidence gate.** Any factor below 0.90 or above 1.05 is checked against the tracker, the tagged time log, commits and the decision records before release. The instructor may confirm it, move it toward 1 or set it to 1, and writes down the reason.
5. **Mismatch check.** If a member's combined score and their hours index (logged hours over agreed hours, relative to the team average) differ by more than 0.25, the instructor reviews both. Hours are not contribution, but a large gap needs an explanation.
6. **Outlier check.** Any single allocation whose share is more than 0.50 from the median share that member received is reviewed against the records. Allocations found to be unsupported are removed for that round, and the median is recomputed.
7. **No surprises.** A member whose week 6 or week 11 score is below 0.85 meets the instructor within a week and agrees a written plan. A factor below 0.90 at week 15 stands only if that meeting happened, or if the drop came from events after week 11 that are on record.
8. **Mitigating circumstances.** Allocations measure contribution against agreed availability. A member with documented circumstances has their factor computed against revised availability, or set to 1.
9. **Missing allocations.** Scores are computed from the raters who submitted. A member who does not submit in a round cannot have a factor above 1.00.
10. **Collusion.** Identical allocations with copied comments from several raters trigger a review of the team's records.
11. **Appeals.** A member may appeal their factor within 10 working days of release. A second member of staff hears it, with the records but without knowing who gave which allocation.
