# PR201 · Week 07 — Sprint 2 Review and Playtest

**Why this matters:** This is the first week strangers play your multiplayer game. A multiplayer playtest is harder to run than a single-player one, because every session needs several players, a working server and a network that behaves. Teams that don't size the session beforehand spend half the slot waiting for a third player and leave with opinions instead of evidence.

**You will be able to:**
- Run a sprint review that inspects a playable increment and ends with backlog changes.
- Compute how many matches a playtest slot can hold from testers, players per match and match length.
- Compute the chance that a playtest reveals a problem of a given frequency, and the number of matches needed for a target confidence.
- Decide which problems to chase with human testers and which need automated soak runs.

**Before class:** Reread [UX201 week 8, section 4](../../UX201-game-ux-and-player-psychology/lectures/w08-usability-testing-methods.md) on how many testers a fix needs. Skim [UX201 week 12](../../UX201-game-ux-and-player-psychology/lectures/w12-surveys-and-interviews.md) on short post-session surveys. Bring your tagged sprint 2 build, installed and tested on two lab machines before class starts.

**Prerequisites from earlier courses:** [PR101 week 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md) (the sprint review and retrospective). [PR101 week 10](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) (bug reports, severity and the priority matrix). [UX201 week 8](../../UX201-game-ux-and-player-psychology/lectures/w08-usability-testing-methods.md) (think-aloud, the discovery formula). [CS202 week 14](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w14-testing-under-bad-networks-netem-clumsy.md) (network conditioner profiles and seeded soak runs).

---

## 1. The sprint review inspects the increment

The Scrum Guide describes the sprint review as a working session, not a presentation. The team shows what it built, the people with a stake in the product respond, and the product backlog changes as a result. For a student studio that means three things.

**Play, don't present.** Nobody opens slides. The build runs on lab machines, joined over the network, and the reviewers hold the controls. If the build does not start, that is the review's first finding, and a useful one.

**Measure against the sprint goal.** Week 6 set a one-sentence goal. At the review, read it aloud and answer it with yes or no. "Three players on three machines can fight a grunt, kill it, die, respawn and understand what happened." Then count what met the definition of done. A story that works in the editor but not in the tagged build is not done, and its estimate does not count toward velocity.

**End with backlog changes.** Every review produces a short list. It says which stories were added, which moved, which were cut and which goals change for sprint 3. If the list is empty, the review was a demo.

Read the sprint 2 burn-up from [week 4](w04-sprint-1-networking-skeleton.md) beside the goal. A done line that stays flat for a week and jumps in the last two days is the typical shape of a sprint where work was started in parallel and integrated late. [PR101 week 7](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md) explains why. If yours looks like that, the retrospective has its first topic.

## 2. A multiplayer playtest is a logistics problem

In a single-player test, one tester and one observer make a session. In yours, a session is a **match**, with `k` players, a server, possibly a host, and enough network to matter. Four things follow.

**Players come in groups.** With 11 testers and 3 players per match you can run 3 matches at once, and the 11th tester waits. Plan the waiting tester's job in advance. They can observe, or sit a second round.

**Every match needs an observer.** One team member per match watches screens, takes notes against the issue log and never helps unless a tester is completely stuck. A team of six can observe at most five matches at once and still have someone running the server.

**Time goes to setup and surveys, not just play.** A 12-minute match needs a minute or two to join and a few minutes for the survey. Budget the whole cycle.

**Round 1 and round 2 test different things.** A tester's first match shows onboarding problems. The second shows what happens once they know the controls. Problems that only first-timers hit can only be seen once per tester.

## 3. What to record

Use one **issue log** for the whole playtest, shared by all observers. Each row is a problem, not a sighting. Columns: id, short description, where it happened, severity (S1 to S4 from PR101 week 10), and a tally of matches in which it appeared. At the end you divide the tally by matches run to get an observed frequency.

Two rules keep the log clean. Log what the tester did and what the game did, not what you think the cause is. "Tester pressed attack next to grunt, no damage number, grunt health unchanged" is a finding. "Hit detection broken" is a guess. And log network problems with the match's conditions: which conditioner profile, which machine was host, the RTT shown on the debug overlay.

After play, each tester fills in a short survey of five to eight items (UX201 week 12). Ask about the sprint goal. Did you understand when you hit something? Did you understand why you died? Do not ask whether they liked it. At this stage the answer is always yes.

## 4. Worked example: sizing the playtest

### The hook

For *Halo 3* (2007), Microsoft's user research group analyzed more than 3,000 hours of play by about 600 players, according to *Wired*'s account that year. For *Halo 2* they had run weekly tests totaling 2,300 hours from 400 players in under two months. Three thousand hours is more than ten thousand 15-minute matches. At that volume, a problem that shows up once in a hundred matches is seen a hundred times.

You have 11 players from another team and 75 minutes. The question is not how to match Microsoft's lab. It is which questions 75 minutes can answer, and which it cannot.

### The model

A problem that appears in a match with probability `p` is seen at least once in `n` matches with probability

```
P(seen) = 1 − (1 − p)^n
```

This is the discovery formula from UX201 week 8, counted in matches instead of testers. Solve it for `n` to get the matches needed for confidence `c`:

```
n = ceil( ln(1 − c) / ln(1 − p) )
```

The number of matches the slot holds is

```
matches per round = min( floor(testers / k), observers )
rounds            = floor( window / (match + turnaround) )
n                 = matches per round × rounds
```

where `k` is players per match, `window` is the minutes of the slot given to play, and `turnaround` is join time plus survey.

Two kinds of problem need different counts. **Per-match problems** (a desync, a respawn that fails, a server crash) can appear in any match, so their `n` is the total number of matches. **First-time problems** (not finding the attack button, not understanding the health bar) can only appear in a tester's first match, so their `n` is the number of testers in round 1.

### Numbers you can check

The *Hollowmarch* slot: 11 testers, `k = 3`, 5 observers available (the sixth team member runs the server), 12-minute matches, 6 minutes of turnaround, a 75-minute window.

```
matches per round = min( floor(11 / 3), 5 ) = min(3, 5) = 3
rounds            = floor( 75 / (12 + 6) ) = floor(4.17) = 4
n (per-match)     = 3 × 4 = 12 matches
n (first-time)    = 9 testers   (3 matches × 3 players in round 1)
```

The 11th and 10th testers wait in round 1 and play from round 2, so only 9 testers are first-timers in a match you observed. Rotate them in so everyone plays at least three rounds.

Now the chance of seeing a problem at least once:

| Frequency `p` | `n = 3` | `n = 9` | `n = 12` | Matches for 90% |
|---|---|---|---|---|
| 0.05 | 0.14 | 0.37 | 0.46 | 45 |
| 0.10 | 0.27 | 0.61 | 0.72 | 22 |
| 0.20 | 0.49 | 0.87 | 0.93 | 11 |
| 0.30 | 0.66 | 0.96 | 0.99 | 7 |
| 0.50 | 0.88 | 1.00 | 1.00 | 4 |

Check one cell by hand, `p = 0.1` and `n = 12`. `0.9^12 = 0.282`, so `1 − 0.282 = 0.718`, shown as 0.72. And the last column for `p = 0.2`: `ln(0.1) / ln(0.8) = −2.303 / −0.223 = 10.3`, rounded up to 11.

Read the table as a plan.

- **The slot is good at common problems.** Anything that happens in a fifth of matches or more will almost surely show up in 12 matches. Most "I didn't understand why I died" problems are like that.
- **The slot is poor at rare network problems.** A desync that hits 1 match in 20 has a 46% chance of appearing, worse than a coin toss. If it does not appear, you have learned almost nothing.
- **First-time problems get 9 chances, not 12.** A confusing control that trips 1 tester in 10 has a 61% chance of being seen.

So the team splits the work. Human testers answer questions about understanding and feel, where problems are common and only humans can report them. Rare network faults go to a **soak test**, in which bots or scripted clients play matches overnight under the conditioner, as in CS202 week 14. Forty-five scripted matches on a lab machine cost a night. Forty-five human matches cost the whole cohort.

One more decision follows. The team wanted half the matches under CS202's Mobile network profile. That halves `n` for each condition to 6. At `n = 6`, a 20% problem is seen with probability `1 − 0.8^6 = 0.74`. The team decides to run rounds 3 and 4 under the Mobile profile (6 matches) and rounds 1 and 2 clean. It records in advance that a problem seen only under the Mobile profile needs a soak run to confirm its frequency.

### Cross-game recognition

The same arithmetic runs through other contexts. In the *Age of Empires II* tutorial study that defined the RITE method (Medlock and colleagues, 2002), the team used `1 − (1 − p)^m` to say how confident they were that a fix worked after six more participants saw no recurrence. They reported 88% for problems at `p = 0.3` and 47% at `p = 0.1`, the same shape as this table. In CS202 week 14, the bug that needs three lost packets in a row is hunted with the same formula applied to seeded soak runs, which is why that lecture asks for hundreds of runs, not a few. And in PR101 week 10, the capture-recapture estimate asks the reverse question. Given what two testers found, how many bugs are still unseen?

### Eyes-open judgment

The formula assumes each match is an independent draw with the same `p`. Real matches are not independent. The same testers learn, the same machine may be host every time, and a problem tied to one machine's network card appears in every match that machine hosts or in none. Rotate hosts between rounds so machine-specific problems get a chance.

"Not seen" is also not "not there". After 12 clean matches, all you can say is that a problem with `p` above about 0.18 would probably have appeared (`1 − 0.82^12 = 0.91`). State the playtest's reach in your report in exactly that form. And resist fixing everything in the log. The playtest ranks problems by frequency and severity so that sprint 3 fixes the ones players will meet, which is the priority matrix from PR101 week 10 fed with measured frequencies instead of guesses.

## 5. From findings to sprint 3

Turn the issue log into backlog items the same afternoon, while observers remember what they saw.

1. **Compute observed frequency** for each issue: tally divided by matches (or by first-time testers, for onboarding issues).
2. **Map to the frequency bands** used in PR101 week 10: always (at least 0.8), often (0.3 to 0.8), rare (below 0.3). Then compute priority with `P = S + F − 1`.
3. **Write each P1 and P2 as a bug report** with steps, build number and the match conditions.
4. **Bring the list to sprint 3 planning** in week 8. Bugs from this playtest compete with content for the same hours. Reserve a share of sprint 3's forecast for them rather than hoping they fit.

## Studio session plan

Week 7 meeting, 3 hours. Two teams are paired. Team A tests team B's build in the first half and the roles swap in the second.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Setup: builds installed, server up, conditioner profiles loaded, issue log shared | All machines join a lobby |
| 0:15-0:30 | Sprint review, team B: goal read aloud, yes or no, estimated hours done counted | Sprint 2 velocity recorded |
| 0:30-1:15 | Playtest of team B's build by team A (four rounds as in section 4, adjusted to your numbers) | Issue log with tallies, surveys |
| 1:15-1:25 | Break and swap | |
| 1:25-1:40 | Sprint review, team A | Sprint 2 velocity recorded |
| 1:40-2:25 | Playtest of team A's build by team B | Issue log with tallies, surveys |
| 2:25-2:50 | Each team alone: frequencies, priorities, top five findings, backlog changes | Lab 07 part C filled in |
| 2:50-3:00 | Retrospective, 10 minutes, one change for sprint 3 | One written team agreement change |

## Deliverables

Due 48 hours after the meeting:

1. **Playtest plan and report** in the lab 07 format ([`labs/lab07.md`](../labs/lab07.md)): the slot inputs, the computed matches, the reach statement ("a problem with `p` above X would have been seen with 90% confidence"), the issue log with tallies and priorities, and the survey summary. Checked with `check_playtest.py`.
2. **Sprint 2 review record**: goal met (yes or no), estimated hours committed and done, the burn-up, and the list of backlog changes.
3. **Retrospective note**: one thing the team will change in sprint 3, with the owner and how you will know it worked.
4. **Soak test plan** for the rare network problems the playtest cannot reach: which checks, which profile, how many runs.

## Common failure modes

- **The review is a slideshow.** Nobody from outside the team touches the build. The fix is to hand over the controls in the first minute.
- **"Done" in the editor.** Hours are counted for stories that only work in the editor. Count only what runs in the tagged build.
- **The third player never arrives.** A match cannot start and the slot shrinks. Plan `floor(testers / k)` matches and give spare testers a job.
- **Observers help.** The tester gets stuck, the observer points at the key, and the problem vanishes from the log. Observers write it down and wait.
- **A rare problem not seen means fixed.** Twelve clean matches say nothing about a 5% desync. Report the playtest's reach, and send rare problems to a soak run.
- **Opinions logged as findings.** "Combat feels floaty" goes nowhere. Log what happened and let the designer interpret it.
- **Every issue becomes a story.** Sprint 3 drowns. Rank by priority and fix the top of the list.

## Review checklist

The instructor checks at the meeting and in the submission:

- [ ] The build started on lab machines from the tagged version, without the editor, and three machines joined.
- [ ] The sprint goal was answered yes or no, and velocity counts only stories that met the definition of done.
- [ ] The playtest plan computes matches per round, rounds and `n` from stated inputs, and the checker agrees.
- [ ] The report states the playtest's reach as a frequency threshold at 90% confidence.
- [ ] The issue log has tallies, observed frequencies, severities and computed priorities, and every P1 and P2 has a reproducible report.
- [ ] Network conditions are recorded for every match, and hosts rotated between rounds.
- [ ] A soak test plan exists for problems below the playtest's reach.
- [ ] The retrospective produced one owned change for sprint 3.

## Sources

- Thompson, C. "Halo 3: How Microsoft Labs Invented a New Science of Play." *Wired*, issue 15.09, published online 21 August 2007. More than 3,000 hours of *Halo 3* play analyzed from about 600 players; weekly *Halo 2* tests totaling 2,300 hours from 400 players in under two months. Read via the Internet Archive copy of wired.com/2007/08/ff-halo-2.
- Medlock, M. C., Wixon, D., Terrano, M., Romero, R. L. & Fulton, B. (2002). "Using the RITE method to improve products: a definition and a case study." Usability Professionals Association annual conference. The *Age of Empires II* (1999) tutorial study; confidence after six further participants of 88% at `p = 0.3` and 47% at `p = 0.1`, as used in UX201 week 8.
- Schwaber, K. and Sutherland, J. (2020). *The Scrum Guide*, November 2020 edition. The sprint review as a working session that inspects the increment and adapts the product backlog.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Background on sprint reviews in game teams.
- The *Hollowmarch* playtest slot, its tester counts and timings are invented for teaching. The frequency bands for mapping observed frequency to PR101's always, often and rare are this course's convention.
