# PR201 · Week 14 — Release Candidate

**Why this matters:** Next week strangers play your slice at the showcase, and the instructor grades the build you submit, not the one you meant to make. This week you produce a release candidate, a build you would be willing to submit as it stands. The hardest decision of the week is which bugs *not* to fix. Every fix is a change to working code, and changes break things. This week shows how to decide with numbers which fixes are worth their risk.

**You will be able to:**
- Produce a release candidate from a tagged commit, run the RC checklist on it, and hold a go/no-go meeting with a written rule.
- Compute the chance that a set of RC fixes introduces no regression, using a regression rate for each kind of change.
- Choose which fixes enter the RC and which bugs ship as known issues, and defend the choice to a teammate who wants to fix everything.
- Assemble the submission package and freeze the data your post-mortem will need.

**Before class:** Your known issues list from week 13 with every open bug's priority, and your tracker's record of which sprint 3 and 4 fixes were reopened or caused new tickets. Reread PR101 week 13, section 4 on the release checklist stage by stage (15 minutes). Read the abstract and section 1 of Yin, Yuan, Zhou, Pasupathy and Bairavasundaram, "How Do Fixes Become Bugs?" (ESEC/FSE 2011), free on the authors' pages (15 minutes). Skim PR101 week 14 on post-mortems, so you know what data to keep (10 minutes).

**Prerequisites from earlier courses:** [PR101 week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md) (release candidates, versioning, catch rate and coverage, go/no-go). [PR101 week 14, post-mortems as a practice](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md). [PR101 week 10, bug tracking and QA basics](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) (priority and the regression rate). [CS202 week 14, testing under bad networks](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w14-testing-under-bad-networks-netem-clumsy.md). [DB201 week 13, privacy, GDPR and data retention](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md) (what to do with playtest telemetry before you submit). From this course, [week 12, sprint 4](w12-sprint-4-polish.md) and [week 13, beta milestone](w13-beta-milestone.md).

---

## 1. From beta to release candidate

PR101 week 13 defined a **release candidate** (RC) as a build you would release if no blocking bug is found. In this course the RC is tagged `v1.0.0-rc.1` at the start of this week, built from a clean checkout with your export script, and treated as the thing you might submit. Three rules follow.

- **Code freeze.** From `rc.1`, the only changes allowed are fixes approved at triage for the next RC. No polish, no tuning, no "while I'm in here". The week 12 polish list is closed.
- **Every change makes a new RC.** If you fix anything, you tag `rc.2`, build it from a clean checkout, and run the RC checklist again. You never patch an RC by hand.
- **The RC is the showcase build.** The build that plays at the showcase is the last RC that passed go/no-go. Not a newer one from the night before.

The freeze feels painful because your team can see bugs it could fix in ten minutes. The rest of this guide is about why many of those ten-minute fixes should wait.

## 2. Worked example: which fixes are worth their risk?

### The hook

The Elder Scrolls V: Skyrim received patch 1.2 on 28 November 2011 for PlayStation 3 and on 30 November for Xbox 360 and PC. The patch fixed a list of problems. It also introduced new ones, and the one players remember is that dragons would sometimes fly backwards. Patch 1.3.7.0 fixed it about a week later on PC and two weeks later on consoles. A large, experienced team fixed bugs and made a new, very visible one.

That is not bad luck. In 2011, Zuoning Yin and colleagues studied bug fixes in Linux, OpenSolaris, FreeBSD and a commercial operating system. At least 14.8% to 24.4% of the sampled fixes for bugs found after release were themselves incorrect and affected users. For concurrency bugs, the kind where timing between threads or machines matters, 39% of fixes were incorrect. And 27% of the incorrect fixes were made by developers who had never touched the files involved before. Your networked slice is concurrency all the way down, and in RC week the person with free time is often not the person who wrote the code.

### The model

Give each proposed fix a **regression rate** `r_i`, the chance that it introduces a new defect. If fixes fail independently, then for a set of fixes:

```
P(no regression)       = Π (1 − r_i)
E[new defects]         = Σ r_i
E[escaping to submit]  = Σ r_i × (1 − c)
```

- `r_i` depends on the kind of change more than on the bug's priority. A text fix in a data file almost never breaks anything else. A fix to message ordering between client and server often does.
- `c` is the **catch rate** of your RC regression pass, the share of regressions it finds before submission (PR101 week 13's `c`).

Where do the `r_i` come from? From your own tracker. Count, for each kind of change in sprints 3 and 4, how many fixes were reopened or caused a new ticket. Yin and colleagues' figures give you a sanity check. If your netcode fixes show a regression rate far below 39%, you are probably not finding the regressions yet.

### Numbers you can check

Hollowmarch has nine open bugs at `rc.1`. Their tracker gives these regression rates by change type for sprints 3 and 4: netcode 0.39 (their data happens to match the Yin study's concurrency figure), gameplay 0.20, UI 0.15, art 0.05, audio 0.05, text and data 0.02. Their RC regression pass catches about `c = 0.7` of regressions.

| Bug | Priority | Change type | `r_i` |
|---|---|---|---|
| F1 Crash when two players loot the same chest | P1 | netcode | 0.39 |
| F2 Boss soft-locks if the party wipes mid-attack | P1 | gameplay | 0.20 |
| F3 Revive heals 0 under 150 ms lag | P2 | netcode | 0.39 |
| F4 Tooltip shows the wrong cooldown | P2 | data | 0.02 |
| F5 Hit sound doubled on the remote client | P2 | netcode | 0.39 |
| F6 Typo in quest text | P3 | data | 0.02 |
| F7 Menu button misaligned at 1366 × 768 | P3 | UI | 0.15 |
| F8 Loot sparkle flickers against the floor | P3 | art | 0.05 |
| F9 Seam in the title music loop | P4 | audio | 0.05 |

Four plans.

| Plan | Fixes | `P(no regression)` | Expected new defects | Expected escaping the RC pass |
|---|---|---|---|---|
| Fix all nine | 9 | 13.4% | 1.66 | 0.50 |
| Fix P1 and P2 | 5 | 17.8% | 1.39 | 0.42 |
| Fix P1 only | 2 | 48.8% | 0.59 | 0.18 |
| Fix P1 plus changes with `r ≤ 0.05` | 6 | 42.3% | 0.73 | 0.22 |

Check the P1-only row by hand. `(1 − 0.39) × (1 − 0.20) = 0.61 × 0.80 = 0.488`. Expected new defects `0.39 + 0.20 = 0.59`. Escaping `0.59 × 0.3 = 0.18`.

Now read the table the way a producer would.

**Fixing everything is the riskiest plan.** With all nine fixes, the RC has only a 13.4% chance of introducing no regression, and on average half a new defect gets past your regression pass into the submission. The team would be trading P3 cosmetic bugs for an unknown new bug, which could be a P1.

**Priority alone is the wrong filter.** Going from "P1 only" to "P1 and P2" adds three fixes and drops `P(no regression)` from 48.8% to 17.8%. Two of those three are netcode fixes at 0.39 each. Meanwhile "P1 plus low-risk" adds *four* fixes and costs only 6.5 points, because the four are a tooltip value, a typo, an art fix and an audio fix.

**The P2 netcode bugs are the real decision.** F3 (revive fails under lag) and F5 (doubled hit sound) are each a 39% gamble. F3 hits a core action the week 11 review fought to make visible. F5 is annoying but harmless. A sensible call is to take F3 into `rc.2` alone, with its author making the fix and a second programmer reviewing it, then run the full network test matrix from CS202 week 14. F5 ships as a known issue.

This script reproduces the table. Run it with `.venv/bin/python` and replace the fixes and rates with your own.

```python
fixes = [("F1", "P1", "netcode"), ("F2", "P1", "gameplay"), ("F3", "P2", "netcode"),
         ("F4", "P2", "data"), ("F5", "P2", "netcode"), ("F6", "P3", "data"),
         ("F7", "P3", "ui"), ("F8", "P3", "art"), ("F9", "P4", "audio")]
r = {"netcode": 0.39, "gameplay": 0.20, "ui": 0.15, "art": 0.05, "audio": 0.05, "data": 0.02}
catch = 0.7  # share of regressions the RC regression pass finds before submission

def risk(selected):
    p_clean, expected = 1.0, 0.0
    for _, _, kind in selected:
        p_clean *= 1 - r[kind]
        expected += r[kind]
    return p_clean, expected

options = [("all nine", fixes),
           ("P1 and P2", [f for f in fixes if f[1] in ("P1", "P2")]),
           ("P1 only", [f for f in fixes if f[1] == "P1"]),
           ("P1 + low-risk", [f for f in fixes if f[1] == "P1" or r[f[2]] <= 0.05])]
for name, sel in options:
    p, e = risk(sel)
    print(f"{name:14} k={len(sel)}  P(no regression) {p:5.1%}  "
          f"expected {e:.2f}  escaping the RC pass {e * (1 - catch):.2f}")
```

It prints:

```
all nine       k=9  P(no regression) 13.4%  expected 1.66  escaping the RC pass 0.50
P1 and P2      k=5  P(no regression) 17.8%  expected 1.39  escaping the RC pass 0.42
P1 only        k=2  P(no regression) 48.8%  expected 0.59  escaping the RC pass 0.18
P1 + low-risk  k=6  P(no regression) 42.3%  expected 0.73  escaping the RC pass 0.22
```

### Cross-game recognition

**Skyrim patch 1.2 (2011).** A fix release introduced a visible new defect and needed a second patch to repair it. In the model, the patch had a large `k`, and one of its `r_i` came up. Big patches late in a cycle are the "fix all nine" row at studio scale.

**Operating system maintenance (Yin et al., 2011).** Mature teams on mature code saw 14.8% to 24.4% of post-release fixes go wrong, and 39% for concurrency fixes. Their finding that many bad fixes came from developers new to the code is a direct argument for the rule "the author fixes, a second person reviews" in RC week.

**Your release checklist, PR101 week 13.** There, every build carried `N` failure items, and checks divided their risk by `(1 − c)`. Here, every fix *adds* a failure item with its own `r_i`. The RC pass divides that risk too, but it can't remove it. Fewer fixes is the only way to add fewer items.

### Eyes-open design judgment

- **Filter by change type, then by priority.** A P1 must be fixed or its feature removed. Below P1, take low-risk changes freely and treat every high-risk change as a separate decision with its own RC.
- **Removing is a fix too.** If a feature has a P1 whose fix is high-risk, switching the feature off can have a far lower `r` than fixing it. A slice without emotes is better than a slice that crashes when two players emote at once.
- **One risky fix per RC.** If `rc.2` carries one netcode fix and it regresses, you know which change did it. If it carries three, you spend the showcase eve bisecting.
- **Measure your own `r`.** The rates above are one team's. Yours come from your tracker. If you have no data, use 0.2 for code and 0.4 for anything touching network timing, and say so.
- **Known issues are honest, not shameful.** A known issues list tells the grader you found the bug and decided not to risk the build for it. Players and graders forgive a known cosmetic bug. They don't forgive a crash that a late fix introduced.

### Check this example

1. A team plans three fixes with `r` of 0.39, 0.02 and 0.15. What is `P(no regression)` and the expected number that escape a pass with `c = 0.7`?
2. A P1 crash is in the chat feature. Fixing it is a netcode change (`r = 0.39`). Turning chat off is a one-line configuration change (`r = 0.02`). The showcase doesn't need chat. What should the team do, and what goes on the known issues list?
3. Why is "one risky fix per RC" worth an extra RC cycle?

<details>
<summary>Answers</summary>

1. `0.61 × 0.98 × 0.85 = 0.508`, so about 50.8%. Expected new defects `0.56`, escaping `0.56 × 0.3 = 0.17`.
2. Turn chat off for the RC. The chance of a regression drops from 39% to 2%. The known issues list says chat is disabled in this build because of a crash, with the ticket number. The fix can go into a later version after the course.
3. If the RC regresses, you know which change caused it, so you can revert that one change and return to the previous RC's state immediately. With several risky fixes in one RC, a regression can come from any of them, and finding which costs hours you don't have.

</details>

## 3. Go/no-go and the known issues list

Hold the go/no-go meeting on the last RC before the submission deadline, as PR101 week 13 describes. The producer asks each checklist owner whether their section passed. The rule is written before the meeting. For this course: no open P1, the build passes the RC checklist from a clean download, and `soak_target.py` from week 13 shows `PASS` on this build or the team has rehearsed its recovery plan.

The **known issues list** ships with the build, in the README or a `KNOWN_ISSUES.md`. For each item: what the player sees, how to avoid it if there is a way, and the ticket number. Write it for a player, not for the team. "Hit sounds may play twice when another player attacks" is useful. "F5 remote SFX dupe" is not.

## 4. The submission package

The graders receive one folder or one store page, and nothing else. It holds:

- **The build** for each platform, named with the version (`hollowmarch-1.0.0-windows.zip`), and the server build with the command that starts it.
- **README** with the engine version, how to start a server and join it, the controls, and the minimum number of players.
- **CHANGELOG** with a heading per RC, written for players (PR101 week 13).
- **KNOWN_ISSUES.md**, as in section 3.
- **Credits**, including every asset's source and licence. Any asset without a licence you can name comes out before submission.
- **Telemetry note.** Your playtest telemetry holds data about people. Before you submit, remove or anonymise player identifiers in anything you hand in, and switch the build's telemetry endpoint off or point it at a server you control, following DB201 week 13. The showcase build should not send strangers' data to a free-tier service nobody will look after once the course ends.

## 5. Freezing what the post-mortem needs

Your post-mortem in week 15 (PR101 week 14 sets out the method) will ask what went right, what went wrong, and why. Answering that with evidence is much easier if you freeze the data now, before people clean up their machines.

- **Tracker export** with every ticket, its priority, dates, and whether it was reopened.
- **Sprint boards** for sprints 1 to 4, with estimates and actual hours.
- **Every milestone review sheet** (alpha, beta) and the week 11 evidence table.
- **The soak log and the RC decisions** from this week, including the fixes you chose not to make.
- **Tags** for every milestone build, so anyone can rebuild what was reviewed.

Put the exports in `production/postmortem-data/` and commit them. Estimate against actual per sprint, and `r` by change type, are the two numbers most post-mortems wish they had and don't.

## Studio session plan

Week 14 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Briefing: freeze rules, the regression model, go/no-go rule | — |
| 0:15-0:45 | Measure `r` by change type from the tracker; classify every open bug (lab 14, part A) | `fixes.csv` with types and rates |
| 0:45-1:15 | RC triage: choose the fix set for `rc.2`; run `check_rc.py` | Decision per bug, known issues list drafted |
| 1:15-1:25 | Break | — |
| 1:25-2:10 | Cross-team RC check: another team downloads `rc.1` and runs your RC checklist from the README only | Checklist results, new tickets |
| 2:10-2:35 | Instructor round: each team defends one fix it took and one it didn't | Notes |
| 2:35-3:00 | Submission package review against section 4; commit post-mortem data | Package checklist ticked |

## Deliverables

Due at the end of the week 14 meeting, in `production/week14/`:

1. **RC fix log** in the lab 14 format ([`labs/lab14.md`](../labs/lab14.md)): every open bug with priority, change type, `r_i`, decision (fix, remove, known issue) and, for each fix, author and reviewer. Checked by running `check_rc.py`, which must print `PASS`.
2. **Known issues list** written for players.

Due before the week 15 showcase:

3. **Final RC** tagged `v1.0.0-rc.N` and the go/no-go record naming it, plus the submission package from section 4.
4. **Post-mortem data** committed under `production/postmortem-data/`.

## Common failure modes

- **"It's a one-line fix."** The size of the diff says little about its risk. A one-line change to message ordering is the riskiest change in the build.
- **Fixing on the showcase morning.** A fix after the last go/no-go makes an untested build. The showcase plays the last RC that passed.
- **Batching risky fixes.** Three netcode fixes in one RC, a regression, and no idea which one caused it.
- **The fixer is new to the code.** Pair the fix with its original author, or have the author review it.
- **Known issues written for the team.** Ticket jargon helps nobody who plays the build.
- **Losing the post-mortem data.** Boards archived, branches deleted, and the post-mortem runs on memory.

## Review checklist

The instructor checks at the end of week 14 and at submission:

- [ ] `rc.1` exists as a tag and its build starts from a clean download using only the README.
- [ ] `check_rc.py` prints `PASS`: every open bug has a change type, `r_i` and a decision; every P1 is fixed or its feature removed; every high-risk fix is alone in its RC and has a reviewer who is not the author.
- [ ] The regression rates cite the tracker, or are marked as defaults with the reason.
- [ ] The go/no-go rule was written before the meeting, and the record names the RC that passed.
- [ ] The known issues list is written for players and matches the tracker.
- [ ] The submission package has every item in section 4, including licences and the telemetry note.
- [ ] Post-mortem data is committed.

## Sources

- UESP, "Skyrim:Patch" (read September 2026). Version 1.2 released 28 November 2011 for PlayStation 3 and 30 November 2011 for Xbox 360 and PC; "dragons occasionally flying backwards" listed as a bug the patch introduced; fixed in 1.3.7.0, released 7 December 2011 for PC and 15 December 2011 for consoles. https://en.uesp.net/wiki/Skyrim:Patch
- Yin, Z., Yuan, D., Zhou, Y., Pasupathy, S. & Bairavasundaram, L. (2011). "How Do Fixes Become Bugs? A Comprehensive Characteristic Study on Incorrect Fixes in Commercial and Open Source Operating Systems." *Proceedings of ESEC/FSE 2011*, 26-36. doi:10.1145/2025113.2025121. At least 14.8% to 24.4% of sampled post-release fixes incorrect; 39% of concurrency bug fixes incorrect; 27% of incorrect fixes made by developers who had never touched the files involved.
- The Hollowmarch bug list and regression rates by change type are a constructed teaching example. Only the 0.39 netcode figure borrows a published number (Yin et al.'s concurrency result).
