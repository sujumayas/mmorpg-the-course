# MMO402 · Final paper brief: governance design paper

**Weight:** 50% of the course grade. The paper is worth 90 points and the viva 10.
**Due:** week 15. The viva is held in week 15 as well.
**Work mode:** individual.
**Labs that feed it:** nearly all of them. The table in "Structure of the paper" names which lab feeds which section. [Lab 08](../labs/lab08.md) (the player charter) is reused directly, and so is your lab 14 case file.
**Related briefs:** [case-analyses-brief.md](case-analyses-brief.md) and [debate-brief.md](debate-brief.md). Viva questions follow the style of the [exam bank](exam-bank.md).

## What this paper is for

This course has argued that a studio running an online world is a sovereign, and that its governance is a set of design decisions: who holds which keys, how voice reaches the developer, which losses are part of play, how reports become verdicts, what players are promised, and how the world ends. The final paper asks you to make all of those decisions for one world, consistently, with numbers, and to defend the hardest one.

It covers all three course outcomes: analyze emergent player governance, design moderation and justice systems, and argue ethical positions on world operation.

## The world

Choose one world and stay with it.

- **Saltmarch**, from [lab 08](../labs/lab08.md): a subscription sandbox with 120,000 monthly players on one shard, open-world PvP, guild vaults, a real-money token and a volunteer review team.
- **Grayhaven**, from [lab 09](../labs/lab09.md): a world with item lending, guild vaults and the lending bug from case C.
- **Harrowmere**, from [lab 13](../labs/lab13.md) and the week 13 lecture: a five-year-old MMO with a purchase history you have already priced.
- **Harbor**, from the week 4 lecture: a survival sandbox with player-owned towns and a premium item sellable in-game.
- **Your own world**, if you describe it in the proposal (see milestones) and the tutor approves it by the end of week 9. It must be an online world with at least player groups, a player economy and player-to-player chat.

You may add facts to the chosen world, such as population, report volumes, share of players under 13 or spend per month. Label every added number as an assumption in a single assumptions table (Appendix A), and use each one consistently. A world with 120,000 players cannot also receive 100,000 reports a day unless you explain why.

A real game may appear in the paper as a comparison or precedent, cited with its version or era, as the lectures do. The paper designs a fictional world, so it does not need new facts about real games. Do not introduce a real-game fact you cannot source.

## Structure of the paper

Length: 5,000 to 6,500 words for sections 1 to 9, plus appendices. Appendices do not count toward the word limit, but the paper must make sense without them.

| Section | Contents | Draws on | Labs that feed it | Target words |
|---|---|---|---|---|
| 1. The world as a polity | The world in one paragraph. Its rules sorted by Lessig's four modalities, with who controls each. Voice channels with an estimate of `p`. Switching costs and the grievance at which the exit-voice model tips into a cascade. | Week 1 | [Lab 01](../labs/lab01.md) | 500 |
| 2. Player government | The guild and alliance permission table with `K` for each action, duties handled as "any of N", and at least one delay or rate limit. The player council, if any, with its voting rule, seats, powers and information rules, and the seats a disciplined bloc would guarantee at two turnouts. If you choose no council, show with week 1 and week 3 numbers what replaces it. | Weeks 2 and 3 | [Lab 02](../labs/lab02.md), [lab 03](../labs/lab03.md) | 800 |
| 3. The line between play and violation | The world's allowed-play policy in the four tests, applied to at least three cases including one that mirrors the Bank of EVE. The loss policy table from the week 9 layer test, with no route left between layers. Where each of the five most surprising rules lives among the four layers (code, just-in-time notice, summary, full contract). | Weeks 4, 5 and 9 | [Lab 04](../labs/lab04.md), [lab 05](../labs/lab05.md), [lab 09](../labs/lab09.md) | 900 |
| 4. Moderation and justice | Report volume and capacity `C`, the thresholds `(h, l)` and their correct, wrong and missed actions, and a surge policy. The review panel `n` and `t` for at least two sanctions, with the error ratio you chose for each and why. The strike ladder, the appeal stage with its workload, and a check against the Santa Clara Notice and Appeal sections and DSA Article 20. | Weeks 6 and 7 | [Lab 06](../labs/lab06.md), [lab 07](../labs/lab07.md) | 1,000 |
| 5. The player charter | Your lab 08 charter, revised for this world: at least eight checkable commitments, each with a measure, a cost and a collision. The exploit policy with the explorer and casual ban risks, and the obviousness test. Two commitments about staff conduct. | Week 8 | [Lab 08](../labs/lab08.md) | 600 |
| 6. Duties of care | Pacing: the clock each pacing rule reads and the obligation test on each. Minors: the gate, the default and the fallback, with children exposed and older players wrongly restricted at your world's `π`. Research and data: a research protocol with a purpose test, consent plan and release plan, including a `λ` calculation for one proposed release. | Weeks 10, 11 and 12 | [Lab 10](../labs/lab10.md), case analysis 11, [lab 12](../labs/lab12.md) | 1,000 |
| 7. The sunset charter | The notice period `N*` from the stranded-value model at your world's numbers, the currency policy, refunds, exports, preservation (`ρ`) and data deletion, published as a charter at launch. | Week 13 | [Lab 13](../labs/lab13.md) | 500 |
| 8. The hardest trade-off | One decision from sections 2 to 7 on which reasonable people disagree. A criteria table, its crux weight and crux score, a decision map with both positions placed and the gap labelled fact or value, and a steelman of the position you rejected. | Week 14 | [Lab 14](../labs/lab14.md) | 500 |
| 9. Coherence | Where two of your own decisions pull against each other (for example, a permissive allowed-play line and a strict minors policy, or a small review team and a notice-first exploit policy), and how you resolved it. | All weeks | | 300 |

**Appendices.**

- **A. Assumptions table.** Every invented number, with its unit and the section that uses it.
- **B. Calculations.** The spreadsheet or scripts behind every number in the paper. Reused lab code is welcome if it is cited as your own earlier lab.
- **C. Sources.** Every real-game fact and every reading, with version, era or access date.

## Rules for the whole paper

- **One number, one source.** Every number in the body traces either to Appendix A or to a calculation in Appendix B.
- **State the model once.** Each section names the lecture model it uses and defines its symbols. Link the lecture instead of re-deriving it.
- **Every commitment is checkable.** "We will do Y within Z, and publish W." Slogans score nothing.
- **Constraints are not criteria.** Protecting minors and obeying the law are constraints (week 14). Do not trade them against fun.
- **Reuse, then revise.** You may reuse your lab text and tables, and you should. Revise them for the chosen world and fix what the lab feedback flagged. Say in a footnote which lab a table came from.
- **Plain writing.** Second person or first person plural, short paragraphs, jargon defined on first use. No long quotations from sources.

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| End of week 9 | **Proposal**, 300 words. The world you chose, three facts you will add to it, and the decision you expect to be your hardest trade-off. The tutor approves your own world or asks for changes. | Required, not graded. A missing proposal costs 5 points from the paper. |
| End of week 12 | **Draft of sections 1 to 4**, with Appendix A started. Written feedback within one week. | Feedback only |
| Week 13 lab session | **Peer review.** Swap drafts with one classmate. Each reviewer checks three things: can every number be traced to Appendix A or B, does section 3's loss policy leave any route between layers, and is section 4's review load stable under the stated `C`? Return a one-page review. | Required, not graded. The review you write counts toward the Coherence criterion of your own paper. |
| Week 14 | Your lab 14 case file becomes the raw material for section 8. You may choose a different trade-off from your debate motion. | No |
| Week 15, day 1 | **Final paper** submitted as one PDF with appendices, plus the calculation files. | Yes, 90 points |
| Week 15 | **Viva**, 10 minutes. | Yes, 10 points |

## The viva

The viva checks that the paper is yours and that you can use its models. It runs like this.

| Minutes | What happens |
|---|---|
| 0 to 2 | You state your hardest trade-off and its crux in two sentences. |
| 2 to 5 | The examiner changes one number in your assumptions table (report volume, share of children, spend rate, officer availability). You predict which section's decision changes and in which direction, then recompute the key figure. |
| 5 to 8 | One question from the [exam bank](exam-bank.md) for a week your paper relies on, rewritten with your world's numbers. |
| 8 to 10 | The examiner states the strongest objection to one of your commitments. You respond. |

## Rubric (100 points)

Two markers score independently and agree a mark. Each criterion has four bands. A section that is missing scores 0 on its criterion.

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| A. Polity and voice (section 1) | 8 | 7-8: modalities correct with controllers, `p` argued from channels, cliff computed and one change shown to move it | 6: cliff computed, change not tested | 4-5: model used with errors, or `p` asserted | 0-3: no model |
| B. Player government (section 2) | 12 | 11-12: every `K` is the cost minimum at stated `q`, `a`, `H`, `L`; duties any-of-N; a delay or limit priced; council seats computed at two turnouts or a no-council choice argued with numbers | 9-10: one `K` unjustified, or council numbers at one turnout only | 6-8: permission table without calculations, or council without a voting rule | 0-5: missing or wrong model |
| C. Play, rules and property (section 3) | 14 | 12-14: allowed-play policy applied to three cases with the failing test named, including a Bank of EVE mirror; loss table with no route between layers; five rules placed in layers with at least three just-in-time notices | 10-11: one case misjudged, or one route left between layers | 7-9: policy stated but not applied, or layers missing | 0-6: missing |
| D. Moderation and justice (section 4) | 14 | 12-14: `C` and thresholds consistent with Appendix A and stable; panel and error ratio set per sanction and defended; appeal workload computed; compliance check complete | 10-11: one number inconsistent, or one sanction lacks an error ratio | 7-9: design stated with few numbers, or queue unstable without comment | 0-6: missing |
| E. Player charter (section 5) | 10 | 9-10: eight or more checkable commitments with measures, costs and collisions; exploit risks computed; obviousness test and staff-conduct commitments present | 7-8: one or two rows vague | 5-6: several slogans, or exploit numbers wrong | 0-4: missing |
| F. Duties of care (section 6) | 12 | 11-12: pacing, minors and research each modelled with numbers at the world's own values; obligation test done; `λ` computed; consent basis stated | 9-10: one of the three thin | 6-8: two of the three thin, or numbers copied from the lecture unchanged | 0-5: missing |
| G. Sunset charter (section 7) | 8 | 7-8: `N*` computed from the world's numbers, currency and data policies set, preservation decision made, charter lines costed | 6: one policy missing | 4-5: charter without the model | 0-3: missing |
| H. The hardest trade-off (section 8) | 6 | 6: crux weight and crux score computed, gap labelled fact or value with a reason, steelman the other side would accept | 5: one element thin | 3-4: crux stated without numbers, or no steelman | 0-2: missing |
| I. Coherence, sources and writing (section 9 and throughout) | 6 | 6: a real internal tension named and resolved; every number traceable; sources cited with version or date; peer review completed | 5: one untraceable number or thin tension | 3-4: several untraceable numbers, or peer review missing | 0-2: inconsistent or unsourced |
| Viva | 10 | 9-10: crux stated clearly; correct direction and recomputation after the change; exam-bank question correct with the model named; objection engaged | 7-8: one part partly wrong | 5-6: two parts partly wrong | 0-4: cannot explain the paper's own numbers |

## Late work and extensions

- The final paper may be submitted up to 72 hours late with a penalty of 5 points out of 90 per 24 hours. After 72 hours it scores 0.
- Extensions are granted only for documented illness or emergency. Free lab extensions from the case analyses brief do not apply to the paper.
- A missed viva without a documented reason scores 0 on the viva. The paper is still marked.

## Academic integrity

Discuss your world and your design with classmates, and use the peer review. The paper, its tables and its calculations must be your own. Reusing your own lab work is expected and must be marked in a footnote. Reusing a lab partner's shared work from a pair lab (labs 05, 06 and 10) is allowed if you name the partner and say which table came from the pair. Cite every real-game fact. If you use a generative AI tool, say how, and verify every number and source it gives you yourself. The viva exists partly to confirm that you can reproduce your own numbers.
