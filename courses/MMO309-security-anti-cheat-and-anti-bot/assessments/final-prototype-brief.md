# MMO309 · Final prototype brief: a detection prototype for one threat

**Weight:** 40% of the course grade.
**Work mode:** individual, or the same pair as your [threat model](threat-model-brief.md). Pairs add a half-page contribution statement and both partners answer in the viva.
**When:** milestone 1 at the end of week 9, milestone 2 at the end of week 12, final submission and a 20-minute demo and viva in week 15.

## What this component is for

The course's third outcome is "detect bots with behavioral analytics", and its second is "prevent classes of exploits by server design". This prototype shows both on one threat you chose from your own threat model. You build a small, honest version of what a studio's security team runs: a simulated population with attackers and innocent look-alikes, a detector, a measured error rate at a realistic base rate, and a policy that turns scores into actions. Then you attack your own detector and show what it costs the attacker to get past it.

The prototype works only on data you generate. It never touches a real game, a real player or a real service.

## What you build

### Choose one threat

Pick a threat from the top ten of your threat model's ledger that a server-side detector can address. Most students extend a lab.

| Track | Starts from | The detector decides |
|---|---|---|
| Movement cheating | [Lab 03](../labs/lab03.md) | which accounts are blinking, speeding or flying, from violation counts over sessions |
| Farming bots | [Lab 07](../labs/lab07.md) and [Lab 08](../labs/lab08.md) | which accounts are bots, from behavioral features |
| RMT networks | [Lab 10](../labs/lab10.md) | which accounts are hubs and farms in a gold-selling operation |
| Duplication | [Lab 04](../labs/lab04.md) | which value path and which accounts produced a conservation residual or a duplicate serial |
| Account takeover | week 9 lecture | which logins or trade bursts are takeovers, including credential stuffing across many accounts |

Another threat is fine if you agree it with the instructor at milestone 1.

### Technical rules

- Python 3.13 from the repository's `.venv`, standard library only. The prototype runs offline.
- One folder with a `README.md`, a single entry point (`prototype.py` or similar), and a test file. `python prototype.py --check` runs your tests. `python prototype.py --report` prints every table in your report. Both finish in under two minutes on a lab machine.
- Every random draw is seeded. Your report states the seeds, and the marker's run must reproduce your numbers exactly.
- No real player data, including your own. No code that reads another program's memory, injects into a process, drives a game client, calls a game's API or sends network traffic to any service. The "attacker" in this project is a class in your simulator.
- Reuse of lab code is expected. Mark what came from a starter file and what you wrote.

### Required features

1. **A simulator** that generates a seeded population with at least:
   - one honest majority;
   - two honest groups that look suspicious on a naive feature (for example rotation players, heavy grinders, honest repeaters, guild banks, giveaway guilds, players on bad connections, theft victims, a shared-tool group like Cedega's users);
   - two attacker variants, one of them adaptive (it changes behavior when a feature it can observe starts to cost it);
   - a prevalence you can set, with a default taken from your threat model.
2. **A detector** that produces a score or a violation count per account, built from at least three features or checks. Name each feature's cost to fake (week 7).
3. **An evaluation** that reports, with counts and not only rates:
   - recall, false positive rate and precision at the default prevalence, over at least 10 seeds (minimum, mean and maximum);
   - the same after a base-rate shift, such as the prevalence after a successful ban wave (week 8);
   - which honest groups are flagged, and how many of each;
   - a train-then-test split in time or by seed, never a random split of one run.
4. **A decision policy** that maps scores to actions:
   - three bands with `t_act` set from measured precision and a review band sized to a stated daily reviewer capacity;
   - a link from each band to a rung of your threat model's sanction ladder, with its `C` (week 12);
   - a timing choice. For cheats whose signature is the scarce thing, justify any ban delay with the week 5 model. For bots and farms, check that the delay does not carry the farm past its break-even lifetime (week 6).
5. **A red-team run inside your simulator.** Give the adaptive attacker the cheapest change that escapes your detector, measure what it costs the attacker (gold per hour, hours per day, accounts, extra layers), then harden the detector once and report the new numbers. Keep the attack at the level of simulated behavior. No part of it describes how to evade a real anti-cheat.
6. **An economic link.** Turn the detector's measured performance into the threat's ALE change (week 1) or the operator's profit per account (week 6), and say whether the detector plus your policy makes the attack stop paying.

## The report

At most 2,500 words plus tables and one or two charts. Suggested order: the threat and why you picked it (with its ledger row), the simulator and its honest look-alikes, the features and their cost to fake, evaluation tables, the decision policy, the red-team run, the economic link, and limits (what your simulator leaves out that a real game would not). Every number comes from `--report`.

## Deliverables

- The prototype folder, zipped or as a repository link, with `README.md`, tests and seeds.
- The report as PDF.
- A contribution statement if you work in a pair.

## Milestone 1: proposal (end of week 9, 10 points)

One page. The threat and its ledger row from your threat model, the track, the honest look-alike groups and attacker variants you will simulate, the features you plan to use with their cost to fake, the default prevalence and where it comes from, and the precision and recall targets you will aim for. Name the lab code you will start from.

## Milestone 2: working baseline (end of week 12, 10 points)

The simulator and a baseline detector that runs end to end with `--check` passing, plus one evaluation table at the default prevalence over at least five seeds. A half-page note on what surprised you and what you will change. Feedback comes back in the week 13 lab.

## Demo and viva (week 15, 20 minutes)

Five minutes of demo. Run `--check` and `--report` on the lab machine, show one flagged honest account and explain why it was flagged, and show the red-team before-and-after. Then fifteen minutes of questions in the style of the [exam bank](exam-bank.md), rewritten with your numbers. Typical questions: "Your prevalence halves after a wave. What is your automatic band's precision now?" "Which of your features would the adaptive attacker drop first, and what does that cost it per day?" "Your review team is cut by half. Is the farm still closed?" Two questions will be about your threat model.

## Rubric

Each criterion is marked in bands. Excellent earns the full points, Adequate earns half to three quarters, and Weak earns a quarter or less.

### Milestones (20 points)

| Criterion | Points | Excellent | Adequate | Weak |
|---|---|---|---|---|
| Milestone 1 proposal | 10 | Threat tied to a ledger row; look-alike groups and attacker variants named; features ranked by cost to fake; targets and prevalence justified | Complete, justifications thin | Late or missing parts |
| Milestone 2 baseline | 10 | Runs end to end, `--check` passes, five-seed table, honest note on surprises | Runs with small fixes, table on one seed | Does not run |

### Final submission, demo and viva (80 points)

| Criterion | Points | Excellent | Adequate | Weak |
|---|---|---|---|---|
| Simulator | 12 | Seeded and reproducible; two honest look-alike groups that trip a naive rule; an adaptive attacker; prevalence settable | Look-alikes present but easy, or no adaptive variant | Only bots and plain humans |
| Detector and code | 13 | Three or more features or checks, each with its cost to fake; tests meaningful and passing; code readable, lab reuse marked | Works, tests shallow or reuse unmarked | Fails `--check` or does not reproduce |
| Evaluation | 15 | Counts and rates over 10+ seeds; base-rate shift shown; flagged honest groups named; time or seed split | Correct numbers, one of these elements missing | Rates on a 50/50 set only, or a random split of one run |
| Decision policy | 10 | Bands set from measured precision and stated capacity; each band tied to a sanction rung with `C`; timing justified with the right week 5 or week 6 model | Bands present, links to sanctions or timing thin | Single threshold with no justification |
| Red team and hardening | 10 | Cheapest evasion found and costed in the attacker's units; one hardening with before-and-after numbers; stays inside the simulator | Evasion shown, cost or hardening missing | Missing, or strays outside the simulator |
| Economic link | 5 | ALE change or operator profit computed from measured rates, with a clear verdict on whether the attack still pays | Computed, verdict unclear | Missing |
| Report | 5 | Plain, numbers first, limits stated, within length | Complete but long or vague on limits | Hard to follow |
| Demo and viva | 10 | Runs on the lab machine; explains a false positive; answers rewritten questions with the model | Runs; answers partly | Cannot run or explain the work |
| **Total, both tables** | **100** | | | |

A submission that interacts with a real game, service or player data, or that contains instructions for evading a real anti-cheat, scores 0 for "Red team and hardening" and is referred to the instructor under the university's conduct rules.

## Rules and advice

- Build the honest look-alikes first. A detector that has only met obvious bots will look perfect and teach you nothing. Week 7's rotation player and week 10's giveaway guild are the kind of group you need.
- Measure precision at the prevalence your threat model estimates, never on a balanced test set (exam bank question 62 shows the gap).
- Keep your feature list in the report and out of any "player-facing" text you write. Week 7 explains why.
- You may use documentation, forums and AI assistants to understand an error or an API, and you must say so in one line in the README. You may not submit code you cannot explain in the viva.
- Late work follows the course policy in the [labs brief](labs-brief.md). The demo cannot be moved except for documented reasons under university policy.
