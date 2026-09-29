# PR401 · Exam bank: viva and reflection questions

PR401 has no written exam. Each student sits a 20-minute individual viva in week 15, worth 5% of the course grade and not adjusted by the [peer factor](peer-assessment-brief.md). The same questions are prompts for sprint retrospectives and for the reflection each student writes for the [final package](m13-pre-production-review-and-package-brief.md).

## How the bank is used

- **In the viva.** Two examiners pick six questions and rewrite them with the team's own files: its claims sheet, fit sheet, budget sheet, economy tables, content plan, liquidity sheet, load tables, time log and stability report. At least two questions must be about a part of the capstone the student did not build. The repository and the slice build are open, and the student may look things up. Knowing where to look is part of the answer.
- **For practice.** Answer each question for your own capstone before week 15. If you need a teammate to answer, ask them now.
- **Types.** Each question is tagged **explain** (say why, with a number from your project), **compute** (redo a calculation with your data), **critique** (find the weakness in a decision) or **reflect** (what you would change, as a checkable action).

## Marking

Each question is marked 0 to 5.

| Mark | Meaning |
|---|---|
| 5 | Correct concept, applied with the team's real numbers or files, trade-off stated, limits of the evidence acknowledged |
| 4 | Correct and specific, but one of numbers, trade-off or limits is missing |
| 3 | Correct in general terms; could be about any project |
| 2 | Partly correct, or correct only for the part the student built |
| 1 | Vague, or relies on a teammate's explanation the student cannot extend |
| 0 | Wrong, or no answer |

The viva mark out of 100 combines the question marks with an overall judgment.

| Criterion | Points | Full marks when |
|---|---|---|
| Question marks | 60 | `total / (5 × questions asked) × 60` |
| Own numbers | 15 | Answers use the team's files without prompting, and the student finds figures in the repository quickly |
| Beyond own role | 15 | The two questions outside the student's discipline are answered at 4 or 5 |
| Honesty about evidence | 10 | The student says "we did not measure that" when true, and says how they would |
| **Total** | **100** | |

The guidance under each question lists what a 5 contains and what usually drags an answer down. Model numbers use the *Emberfall* sample team from the session guides unless the question says otherwise.

---

## A. The pitch and its claims

Links: [week 1](../lectures/w01-pitch-development.md), [PR301 week 1](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w01-pitch-and-world-pillars.md), [MMO403 week 14](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md).

1. *Compute.* From your week 1 pitch sheet, recompute the median player's exhaustion time `T` and locust ratio `L`. Which input did the result depend on most?

<details>
<summary>Marking guidance</summary>

A 5 recomputes `T = 7 × C × r / h` and `L = 28 / T` with the team's own values and names the input that decides it. For *Emberfall* that is `r`: at `r = 8` the median `L` is 0.49, at `r = 3` it is 1.30. The student should say the input was assumed in week 1 and what later measured it. A 3 states the formula correctly with made-up numbers. Drop to 2 if the student confuses one-pass content hours `C` with hours of play.

</details>

2. *Explain.* What was your pitch's replay threshold `r_needed` for the median player, and where did it end up in your claims sheet and risk sheet?

<details>
<summary>Marking guidance</summary>

A 5 gives the value (*Emberfall*: `r ≥ 5 × 28 / (7 × 5.1) = 3.9`), shows it as a load-bearing claim with an owner, and traces it to the week 4 risk list as R1. It also states what the evidence level was at greenlight. A 3 knows the threshold exists but cannot find it in the files.

</details>

3. *Critique.* Pick one claim your team tagged "estimated" in week 1. Was the tag honest? What would have made it "tested"?

<details>
<summary>Marking guidance</summary>

A 5 names the claim, the model or comparable it was estimated from, and a specific test with a threshold that would have moved it to "tested". Good answers admit when a claim was really assumed. A 2 describes the three levels without applying them.

</details>

4. *Reflect.* Your pitch had a rejected alternative. With what you know now, would the rejected pitch have passed greenlight? Answer with a number.

<details>
<summary>Marking guidance</summary>

A 5 reruns or reasons from the rejected pitch's saved output and applies at least one later measurement to it, such as the measured `k` from week 9 or the plan ratio from week 6. *Lanternfall*'s median `L` of 1.62 at the assumed `k = 20` would be worse at a measured `k` of 30. A 3 argues from taste.

</details>

## B. Market analysis

Links: [week 2](../lectures/w02-market-analysis.md), [MMO403 week 2](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w02-unit-economics-ltv-cac-arppu.md), [MMO403 week 12](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w12-publishing-platforms-and-fees.md), [MMO405 week 6](../../MMO405-research-methods-in-online-games/lectures/w06-qualitative-methods-interviews.md).

5. *Explain.* Why does your comparables table report a range for each game rather than one figure? Which input widens it most?

<details>
<summary>Marking guidance</summary>

A 5 names the multiplier range (38 to 58 sales per review in the week 2 guide, a factor of about 1.5) and the realized-price factor `φ`, and says `φ = 0.5` is an assumption and the least reliable number. It points to the team's own widest row. Drop to 2 if the student presents the range midpoint as the answer.

</details>

6. *Critique.* Name one of your comparables for which the review-count method does not apply, and say what you did with that row.

<details>
<summary>Marking guidance</summary>

A 5 identifies the broken condition (free-to-play, sales off Steam, or a relaunch that resets reviews) and says the row was footnoted, not silently dropped. The week 2 example is *Pantheon*, whose early backers paid outside Steam. A 3 says "some games are different" without naming the condition.

</details>

7. *Compute.* From your `audience.csv`, how many daily players `D` does your target peak CCU need? What happens to `D` if your average session is half as long?

<details>
<summary>Marking guidance</summary>

A 5 recomputes `D` from peak CCU, the peak-to-average ratio `q` and daily hours `h_day`, and sees that halving `h_day` doubles `D`. It then says whether the team's recruitment plan for PR402 can supply that. A 3 computes correctly but does not connect it to recruitment.

</details>

8. *Explain.* Your review coding reported an agreement figure. Why is percent agreement alone not enough, and what did your kappa tell you?

<details>
<summary>Marking guidance</summary>

A 5 explains that two coders agree by chance more often when one code dominates, so kappa corrects for chance, as MMO405 week 6 showed with its 80% example. It gives the team's own kappa and names the code that caused most disagreement. Drop to 2 if the student cannot say what chance agreement means.

</details>

## C. Pillars, vision and setting

Links: [week 3](../lectures/w03-pillars-and-vision.md), [PR201 week 2](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w02-pre-production-pillars-and-scope.md), [MMO406 week 1](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w01-setting-as-system.md).

9. *Compute.* Take one pillar and recompute its share of feature hours from your `features.csv`. Did it clear `s_min` before and after the revision?

<details>
<summary>Marking guidance</summary>

A 5 sums hours times weights for that pillar over total feature hours, with foundation excluded, and gives both values. *Emberfall*'s P3 went from `70 / 540 = 13.0%` to `115 / 490 = 23.5%` against `s_min = 0.20`. A 3 recites the formula without the team's numbers.

</details>

10. *Critique.* Which of your features carried the most debatable pillar weights? How would the audit change if the weights were argued the other way?

<details>
<summary>Marking guidance</summary>

A 5 names the feature, shows the share change if the weight moved (for example the market stall split 0.5 and 0.5 between P1 and P2), and says whether the pass or fail would change. It notes that weights are a team judgment and that the audit is only as honest as they are. A 2 says the weights were "about right".

</details>

11. *Explain.* Name one anti-pillar and one thing it removed from your plan. What did it rule out that a comparable does?

<details>
<summary>Marking guidance</summary>

A 5 gives the anti-pillar, the cut it drove with hours, and the comparable it differs from. *Emberfall*'s "no solo campaign" line removed a 90-hour questline. A 3 gives an anti-pillar that nobody would want anyway.

</details>

12. *Explain.* How does your setting explain one of your systems, in the sense of MMO406 week 1?

<details>
<summary>Marking guidance</summary>

A 5 ties a rule of play to a fact of the world, such as *Emberfall*'s ash storms cutting the valley off, which explains why no vendor sells gear and players craft everything. It also names one piece of lore that was cut for serving no system. A 2 describes the lore without any system.

</details>

## D. Prototypes and evidence

Links: [week 4](../lectures/w04-prototype-1.md), [week 5](../lectures/w05-prototype-2.md), [PR201 week 11](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md), [MMO405 week 2](../../MMO405-research-methods-in-online-games/lectures/w02-quantitative-methods-overview.md), [MMO405 week 5](../../MMO405-research-methods-in-online-games/lectures/w05-experiments-and-quasi-experiments.md), [MMO405 week 10](../../MMO405-research-methods-in-online-games/lectures/w10-ethics-and-irb.md).

13. *Compute.* For your first prototype, recompute the exposure it removed per hour spent. Would it still be first if its cost had doubled?

<details>
<summary>Marking guidance</summary>

A 5 uses `E = p × L`, `V = q × E` and `ratio = V / c` with the team's values (*Emberfall* R1: `0.6 × 100 / 24 = 2.5`) and reruns the ranking at double cost. It notes the ranking is robust only when ratios differ by a lot. A 3 computes the ratio but cannot say what it ranks.

</details>

14. *Explain.* Which risk did your team choose not to prototype, and what did it do with that risk instead?

<details>
<summary>Marking guidance</summary>

A 5 names the risk, its ratio below 1, and the response chosen: accept, cut, scope down or handle in production. *Emberfall* scoped the 10 against 10 siege down to a town raid and moved the market UI to usability sessions in PR402. A 2 says the team "ran out of time".

</details>

15. *Explain.* Was your prototype question a discovery question or a decision question? What sample did it need, and why?

<details>
<summary>Marking guidance</summary>

A 5 labels the question and applies the matching rule: `1 − (1 − λ)^n` for discovery, a sized interval for decisions. It explains why five testers can find most problems and still say nothing about a rate. A 3 knows the distinction but mislabels the team's own question.

</details>

16. *Compute.* Your prototype had players tested in groups. What design effect did you use, and what effective sample size did it leave you?

<details>
<summary>Marking guidance</summary>

A 5 computes `DE = 1 + (k − 1) × ρ` and `n_eff = n / DE`, states where `ρ` came from and says it is a planning value. With groups of 8 and `ρ = 1`, each group counts as one tester, as PR201 week 11 showed. Drop to 2 if the student treats testers in one trading group as independent.

</details>

17. *Critique.* Read the interval for your main decision question. Did it clear the threshold? If it did not, what did your team say at greenlight?

<details>
<summary>Marking guidance</summary>

A 5 reads the Wilson interval at effective sample size and states the verdict honestly. *Emberfall*'s prototype 1 gave 5 of 8 with an interval of 31% to 86% against 50%, which is unclear. Full marks for saying "unclear" when it was. A 1 reports the point estimate as the answer.

</details>

18. *Explain.* Your prototype 2 brief was committed before the first group played. Why does the course require that, and what would have gone wrong without it?

<details>
<summary>Marking guidance</summary>

A 5 explains that a stop rule or threshold chosen after seeing data turns into "stop when we like the answer", and connects this to preregistration in MMO405 week 2 and repeated looks in live A/B tests. It points to the commit dates. A 3 says it is "good practice" without the mechanism.

</details>

19. *Reflect.* What did you tell playtesters before they played, and what data did you keep? Would it pass an ethics review?

<details>
<summary>Marking guidance</summary>

A 5 describes what testers were told, what was recorded, how long it is kept and that testers could stop at any time, and compares this with MMO405 week 10's checklist. It names one gap and the fix. A 2 says "they were our friends".

</details>

## E. Greenlight

Links: [week 6](../lectures/w06-greenlight-review.md), [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md), [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), [MMO403 week 14](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md).

20. *Compute.* Recompute your team's capacity `C` and fit ratio `F` at greenlight. Where did `f` and `R` come from?

<details>
<summary>Marking guidance</summary>

A 5 computes `C = N × H × f` and `F = (S × R + E) / C` with the team's numbers and cites the PR301 totals (*Emberfall*: `f = 1,470 / 1,960 = 0.75`, `R = 1,470 / 1,131 = 1.30`, `C = 588`, `F = 0.97` after cuts). A 3 uses the right formula with the sample team's values. Drop to 2 if `R` was assumed and the student does not say so.

</details>

21. *Explain.* What was your tripwire `R*`, and has your measured plan ratio since greenlight stayed below it?

<details>
<summary>Marking guidance</summary>

A 5 gives `R* = (C − E) / S` (*Emberfall*: 1.35 for the cut plan) and compares it with the plan ratio measured in slice sprint 1. It says what the decision record required if the tripwire was crossed. A 2 cannot find the tripwire in the decision record.

</details>

22. *Critique.* Look at your cut list. Which cut would hurt a pillar most, and why is it where it is in the order?

<details>
<summary>Marking guidance</summary>

A 5 names the cut, the pillar it touches, and the ordering rule (distance from the pillars), and says whether the worst risk's full cost is covered. A 3 lists cuts without their order or hours.

</details>

23. *Reflect.* The week 6 guide read the Titan and Overwatch story as a question of fit between scope and team. Was there a point in PR401 when your scope and team stopped fitting? What signal told you?

<details>
<summary>Marking guidance</summary>

A 5 names the moment, the number that showed it (a load, a plan ratio, a prototype result), and the action taken, with a date. It does not retell the Blizzard history at length. A 2 says the team "always fitted" with no evidence.

</details>

## F. Technical design

Links: [week 7](../lectures/w07-technical-design.md), [PR301 week 2](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w02-technical-architecture-review.md), [PR201 week 3](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w03-technical-design-document.md).

24. *Compute.* From your budget sheet, recompute the replication time per tick for your 2× load-test hub case, with and without your interest cap.

<details>
<summary>Marking guidance</summary>

A 5 computes `U = N × e × r` and `(U / r) × t` with the team's measured `s` and `t`. *Emberfall* at 120 players: 71.4 ms per 100 ms tick uncapped, 24.0 ms with `k = 40`. It explains why doubling `N` quadrupled the uncapped cost. A 3 computes one case only.

</details>

25. *Explain.* Your interest cap limits what each player can see in a crowd. What does that cost the player, and how did your design hide or accept it?

<details>
<summary>Marking guidance</summary>

A 5 names the visible effect (distant players in the market not drawn, or drawn at a lower rate) and the design response, and ties it to a pillar. A 2 treats the cap as free.

</details>

26. *Explain.* Name one piece of state your process map says a process may never touch, and why.

<details>
<summary>Marking guidance</summary>

A 5 names the state and the rule, such as the world server never writing currency except through a transactional ledger call, and links it to the authority table and to PR301 week 2's persistence promise. A 3 describes the map without any "never" rule.

</details>

27. *Critique.* Which input in your budget sheet was least well measured? What did the spike find, and did it change a decision?

<details>
<summary>Marking guidance</summary>

A 5 names `s`, `t` or the crowd size, the spike's result and the decision it moved, with the decisions log entry. Full marks are available for a spike that confirmed the estimate. A 1 has no spike result.

</details>

## G. Economy and balance

Links: [week 8](../lectures/w08-economy-and-balance-design.md), [PR301 week 7](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w07-sprint-3-economy-and-crafting.md), [PR301 week 10](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w10-telemetry-review.md), [MMO403 week 4](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w04-cosmetics-vs-power.md).

28. *Compute.* For your key purchase, compute the hours to afford it and the week of the live period in which the light and median players reach it.

<details>
<summary>Marking guidance</summary>

A 5 computes `T = price / n` and `week = T / h` with the team's rates. *Emberfall*'s revised house plot: `1,200 / 80 = 15` hours, week 3 for the median, never for the light player, who gets a 400-mark banner instead. A 3 computes correctly and does not mention the light player.

</details>

29. *Explain.* Which player types hold most of the currency created in your live period, and which sink reaches them?

<details>
<summary>Marking guidance</summary>

A 5 computes each type's share of hours played (*Emberfall*: keen and heavy are 25% of players and about 55% of hours) and names a sink that scales with activity, such as a 5% stall fee. It explains why a flat sink misses them. A 2 says "sinks remove money" without saying whose.

</details>

30. *Explain.* Show where one balance target lives in your data files and what it takes to change it.

<details>
<summary>Marking guidance</summary>

A 5 opens `data/balance.csv` or the equivalent, names the target, its value, unit and reason, and shows that a restart without a rebuild applies a change. A 2 finds the value hard-coded.

</details>

31. *Critique.* Four weeks is short for inflation. What economic failure is most likely in your live period instead, and which telemetry event would show it first?

<details>
<summary>Marking guidance</summary>

A 5 names a failure that fits four weeks, such as a purchase nobody reaches, a sink that never fires, or a crafting leak like the one PR301 week 10 traced, and the exact event and property that would reveal it. A 3 names inflation anyway.

</details>

## H. Content plan

Links: [week 9](../lectures/w09-content-plan.md), [MMO406 week 7](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w07-lore-delivery-in-mmos.md), [MMO406 week 9](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w09-living-world-events.md).

32. *Compute.* Recompute the yield of your highest-yield and lowest-yield units. Why did you keep the lowest one, if you did?

<details>
<summary>Marking guidance</summary>

A 5 computes `y = c × r / cost` for both from `content.csv` and justifies any must-have that sits low in yield, as *Emberfall* kept its tutorial chain at 0.033 because every player passes through it. A 3 computes without judging.

</details>

33. *Compute.* Which one replay claim carries most of your median player's content? What is the median drought if it halves?

<details>
<summary>Marking guidance</summary>

A 5 names the unit, its share of `Σ E` and the drought at half `r`. *Emberfall*'s recipe set is 8 of 19.2 hours; at `r = 4` the median drought grows from 1.1 to 6.7 days. It then says what the slice test found. A 2 cannot name the claim.

</details>

34. *Explain.* Where did your measured authoring ratio `k` differ most from week 1's assumed 20, and why?

<details>
<summary>Marking guidance</summary>

A 5 gives the measured `k` per content type with the hours and play times behind it, and the reason for the gap (tuning, bugs, second passes). *Emberfall*'s dungeon measured 120. A 3 says "estimates were optimistic".

</details>

35. *Explain.* Your patch-week content arrives after launch. How is its lore written for players who joined in week 3 and missed the setup?

<details>
<summary>Marking guidance</summary>

A 5 uses MMO406 week 7's point that lore must work for a population that turns over, and names the delivery (world state, item text, NPC barks) that lets a late joiner understand the event. For *Emberfall*'s ash-storm event, the storm itself carries the story. A 2 relies on a one-time cinematic.

</details>

## I. Social systems and safety

Links: [week 10](../lectures/w10-social-systems-plan.md), [PR301 week 11](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w11-sprint-4-social-systems.md), [MMO406 week 8](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w08-player-agency-vs-canon.md), [MMO405 week 10](../../MMO405-research-methods-in-online-games/lectures/w10-ethics-and-irb.md).

36. *Compute.* For one system that needs several players at once, compute the probability it works in your evening window, from `M`, `p` and `m`.

<details>
<summary>Marking guidance</summary>

A 5 derives `p = e × h / W`, then `P(X ≥ m)` from the binomial, with the team's inputs. *Emberfall*: `p = 0.25`, the draft town of 15 needing 4 holds 54% of evenings; the final design of four towns of 22, with a militia filling two slots, holds 99%. A 3 runs the script without knowing what `p` means.

</details>

37. *Explain.* Which of the four levers did you use, and what does it cost players?

<details>
<summary>Marking guidance</summary>

A 5 names the lever (bigger pool, more time online, fewer needed, fixed window) and its cost in the player's terms, such as fewer rival towns or raids that can only start in the evening. A 2 names a lever with no cost.

</details>

38. *Explain.* Walk through what happens, step by step, when a player reports another player's chat line in your game at 23:00.

<details>
<summary>Marking guidance</summary>

A 5 traces the report through capture of context, the rota member on call, the response target, the sanction ladder and the log entry, using the team's safety sheet and code of conduct. If nobody is on the rota at 23:00, the student says what the fallback is. A 1 describes a report button that goes nowhere.

</details>

39. *Critique.* When players change your world (take a town, win a raid), what does the world record, and what happens to that record if the server population collapses?

<details>
<summary>Marking guidance</summary>

A 5 separates world state from canon as in MMO406 week 8, names what persists, and links it to the low-population fallback with its trigger and decision owner. A 3 answers only one half.

</details>

## J. Production plan

Links: [week 11](../lectures/w11-production-plan.md), [PR101 week 12](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md), [MMO403 week 13](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w13-team-and-budget-planning.md).

40. *Compute.* Recompute the load of your team's constraint discipline, before and after your moves.

<details>
<summary>Marking guidance</summary>

A 5 computes `C_d = n_d × H × W × f`, `D_d = S_d × R` and `L_d = D_d / C_d`. *Emberfall*'s art went from `80 × 1.30 / 72 = 1.44` to 0.94 after moving 20 hours at a 1.5 conversion factor and buying a prop kit. It explains why the whole-team load of 0.80 hid this. Drop to 2 if the student uses only the team total.

</details>

41. *Explain.* Who paid for the move that relieved your constraint? Did it create a new constraint?

<details>
<summary>Marking guidance</summary>

A 5 names the discipline or budget that absorbed the work and its new load (*Emberfall*'s audio and tech art went from 0.36 to 0.90). It also checks the move against the conversion factor and shows what would happen at a larger move. A 3 names the move but not who paid.

</details>

42. *Critique.* Someone on your team suggests the artist works extra hours instead of cutting. Answer them with numbers.

<details>
<summary>Marking guidance</summary>

A 5 computes the extra hours per week the load implies (at 1.44, 44% more every week for eight weeks) and cites PR101 week 12 on what crunch costs in quality and later hours. It proposes a move from the four options. A 2 objects on principle without numbers.

</details>

## K. Vertical slice

Links: [week 12](../lectures/w12-vertical-slice-sprint-1.md), [week 13](../lectures/w13-vertical-slice-sprint-2.md), [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), [PR301 week 14](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w14-stabilization.md).

43. *Explain.* Show one row of your time log you tagged "one-time" and one you tagged "per-unit". Why does the difference matter for PR402?

<details>
<summary>Marking guidance</summary>

A 5 finds both rows, applies the team's written edge-case rules and explains that per-unit cost drives the production estimate while one-time work does not repeat. *Emberfall*'s slice town: 14 hours logged, 4 one-time, `u_1 = 10`. A 2 cannot find the tag rules.

</details>

44. *Compute.* For a tool you decided on, recompute the break-even count at your plan ratio and say what it did to each discipline's load.

<details>
<summary>Marking guidance</summary>

A 5 computes `n* = F / (u_m − u_t)` with `F` and `u_t` scaled by `R` (*Emberfall*'s bounty tool: `15.6 / 0.85 = 18.4` against 21 bounties) and shows the load change per discipline. A 3 gives the break-even without scaling or without the load check.

</details>

45. *Compute.* From your stability report, give the 95% upper bound on the server crash rate and the pessimistic chance of a clean review demo. How many server-hours at load were behind it?

<details>
<summary>Marking guidance</summary>

A 5 uses `λ_up = U(k) / E` with server-hours at demo load, not player-hours, and `P = exp(−(N × λ_c + λ_s) × t)`. *Emberfall* before soaking: 3 server-hours, upper bound 1.0 per hour, 30% chance of a clean demo. A 1 says "it never crashed".

</details>

46. *Critique.* What was on your slice quality bar that you would now remove, and what was missing?

<details>
<summary>Marking guidance</summary>

A 5 names one line per case with a reason from the review: a line that cost hours and the panel did not notice, and a gap the panel found. It turns the answer into a rule for PR402's alpha bar. A 2 says the bar was fine.

</details>

## L. Review, replan and reflection

Links: [week 14](../lectures/w14-pre-production-review.md), [PR101 week 14](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md), [PR101 week 11](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w11-communication-and-conflict-in-teams.md), [MMO406 week 14](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w14-bible-workshop.md).

47. *Compute.* Project the cost of your next three units of one content type from the slice's measured first unit, flat and at your planned learning rate.

<details>
<summary>Marking guidance</summary>

A 5 uses `u_x = u_1 × x^(log2 LR)` and sums units 2 to 4. *Emberfall*'s towns: 30.0 hours flat, 27.7 at 0.95, 25.6 at 0.90, against 19.5 planned. It then states the resulting load. A 3 computes flat only.

</details>

48. *Explain.* Defend the learning rate you planned with. What result on unit 2 would make you change it, in each direction?

<details>
<summary>Marking guidance</summary>

A 5 argues that one measured unit has no slope, so 0.95 or flat is the default, and gives numeric triggers for unit 2. *Emberfall*: at or below 8.5 hours reinstate the fourth town; above 9.5 hours take the boss cut. Drop to 1 for "0.8 because Wright's law".

</details>

49. *Explain.* Read one of your review conditions aloud. Is it checkable? Who owns it, by when, and what will show it is done?

<details>
<summary>Marking guidance</summary>

A 5 reads a condition from `review-decision.md` with owner, date and observable result, and shows the evidence in the week 15 package. A 2 reads a condition that cannot be checked ("improve stability").

</details>

50. *Reflect.* Name one decision in PR401 you would make differently, as a checkable action item for PR402 with an owner, a date and an observable result.

<details>
<summary>Marking guidance</summary>

A 5 writes the action item in PR101 week 14's form and ties it to a number from PR401 (a plan ratio, a load, a crash bound). It is blameless: it names a process, not a person. A 2 is a wish ("communicate better").

</details>

51. *Reflect.* Which part of the capstone you did not build do you understand least? Explain it as well as you can now.

<details>
<summary>Marking guidance</summary>

A 5 picks honestly, explains the part's main number or mechanism from the team's files, and says how the student will close the gap before PR402. Examiners reward candour; a student who picks their own discipline to avoid the question scores 2 at most.

</details>

52. *Explain.* Pick one number that appears in two of your package documents (CCU, town count, a price, an hours total). Do they agree? If they changed, which document leads?

<details>
<summary>Marking guidance</summary>

A 5 finds the number in both places, confirms or explains the difference, and names the document the team treats as the source of truth with a "changed since" note. A 1 finds a mismatch and cannot explain it.

</details>
