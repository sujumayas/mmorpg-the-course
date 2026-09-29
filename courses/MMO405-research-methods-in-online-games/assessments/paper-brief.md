# MMO405 · Final paper brief: research paper

**Weight:** 50% of the course grade. The paper is worth 90 points and a 10-minute oral check 10.
**Due:** week 15, day 1. The oral check is held in week 15.
**Work mode:** individual, or the approved pair from the proposal. A pair submits one paper with a contribution statement, and each partner takes the oral check alone.
**Labs that feed it:** most of them. The table in "Structure" names which lab feeds which section, and the ethics statement draws on your lab 10 application.
**Related briefs:** [proposal-brief.md](proposal-brief.md) plans the study this paper reports, and [methods-labs-brief.md](methods-labs-brief.md) covers the week 14 talk. Oral-check questions follow the style of the [exam bank](exam-bank.md).

## What this paper is for

The paper reports the study your proposal planned, in the form a reviewer at DiGRA, CHI PLAY or *Game Studies* would expect ([week 11](../lectures/w11-writing-and-presenting-research.md)). It shows both course outcomes at once. You ran an ethical study of an online game, and you combined a quantitative and a qualitative strand so that one changed how you read the other.

A good paper here is modest and checkable. It makes the claim its design supports and no stronger one. Every number can be recomputed from the others or from the supplement. Every player is protected in the way the approval promised.

## Data and routes

Use the route confirmed for your proposal.

- **Routes S and P** report the collected data.
- **Route R** reports the collected data if approval arrived. If it did not arrive by the end of week 11, the paper switches to route M without penalty.
- **Route M** reports the full design, the role-play pilot and the analysis run on simulated data. State every simulation assumption in a table, and say what the real study would add. The rubric applies unchanged: "results" means the results of the modelled analysis and the pilot.

**Two strands are required.** Every paper has at least one quantitative and one qualitative strand, integrated at a named step (connecting, building, merging or embedding, [week 8](../lectures/w08-mixed-methods.md)). One strand may be small: six interviews, three field hours, or a coded sample of 100 public posts paraphrased under your protocol. A paper with two strands that never meet scores at most "Adequate" on criterion E.

## Structure

Length: 5,000 to 7,000 words for the body (title to discussion), excluding references, tables, figure captions and appendices. The paper must make sense without the appendices.

| Section | Contents | Draws on | Labs that feed it |
|---|---|---|---|
| Title and abstract | Title names the population, the phenomenon and the finding. Abstract of 150 to 250 words answers the five questions: problem, what you did with whom and how many, the finding with its size and interval, what it means, what it cannot tell you. Every number in it appears identically in the results. | Week 11 | [Lab 11](../labs/lab11.md) |
| 1. Introduction | One argument: why the question matters, what prior work leaves open, what this study does. Ends with the question or hypotheses as on your question card, and the preregistration link. Verbs match the claim type. | Weeks 1, 2 and 11 | [Lab 01](../labs/lab01.md) |
| 2. Method | Game, servers or regions, patch or season, and dates. Participants and recruitment, with a flow of numbers from invited to analyzed and every exclusion. Measures with sources, adaptations and reliability in your sample; telemetry rules (unit, sessionization, cleaning); interview guide, coding process and IRR decision; recording plan and observer role; network boundary, tie, weight, threshold and window, as applicable. Design and the integration step. Analysis with software and version, planned versus exploratory. A deviations table comparing what you did with the proposal. Ethics statement (see below). | Weeks 3 to 10 | [Labs 03](../labs/lab03.md), [04](../labs/lab04.md), [06](../labs/lab06.md), [07](../labs/lab07.md), [09](../labs/lab09.md) |
| 3. Results | In the order of your questions. Quantitative: descriptives first, then each estimate with its effect size, interval and analyzed `n`, and its verdict against the SESOI you preregistered. Sensitivity analyses (another sessionization rule, another tie threshold, another exclusion rule). Qualitative: each theme as a claim with pseudonymized evidence, the number of participants it came from, and at least one case that complicates it. The joint display, with each row's fit named. | Weeks 2, 5, 6, 8, 9 and 11 | [Labs 02](../labs/lab02.md), [05](../labs/lab05.md), [08](../labs/lab08.md), [09](../labs/lab09.md), [11](../labs/lab11.md) |
| 4. Discussion | The answer to the question in one paragraph. Agreement and disagreement with prior work. Limitations that name the alternative explanation and its likely direction. What a replication would need to keep the same and what would change, including the game version. Implications that follow from the evidence and no further. | Weeks 11, 13 and 14 | [Lab 13](../labs/lab13.md) |
| Figures | The main result figure redrawn to the week 14 checklist: title as the claim with the number, natural units, labelled interval, the comparison drawn, `n` and unit, SESOI or reference line, readable and colour-safe. | Week 14 | [Lab 14](../labs/lab14.md) |

**Appendices.**

- **A. Number audit.** GRIM on every mean of integer data, every p-value recomputed from its statistic, and every `n` traced to the participant flow, produced with your lab 11 checker. List anything you changed because of it.
- **B. Code and data.** Analysis code that runs with `.venv/bin/python`. Data if your approval allows sharing; otherwise a synthetic dataset with the same columns and similar distributions, plus the aggregates needed to recompute the main table ([week 13](../lectures/w13-replication.md), "Data you cannot share").
- **C. Instruments and codebook.** As used, with any changes since the proposal marked.
- **D. Data availability statement.** What is shared, where, and how a reviewer could get controlled access to the rest.

## Ethics and consent requirements

The paper must match what your proposal and approval promised ([week 10](../lectures/w10-ethics-and-irb.md)). Criterion F checks each item.

1. **Ethics statement in the method.** The approving body and its reference number (or the course protocol number for route P, or a statement that route S or M involved no human participants), how consent was obtained, any waiver granted, and the age screen.
2. **Only approved data.** Report only data collected after sign-off or approval, under the procedures approved. Any deviation appears in the deviations table with its date and reason, and any deviation that affected participants was reported to the instructor or board when it happened.
3. **Identifiability.** No real character, guild or server names. Quotes from public sources are paraphrased unless the protocol and the author allow otherwise ([week 14](../lectures/w14-research-presentations.md), section 4). Network figures suppress or merge unique positions ([week 9](../lectures/w09-social-network-analysis-of-guilds.md)). Screenshots are cropped or redrawn.
4. **Withdrawals and deletions.** State how many participants withdrew and confirm their data were removed. State the deletion date for recordings and the linkage key, as in the approved plan.
5. **Incidental findings and distress.** Say whether the distress protocol or incidental-findings procedure was used, without details that identify anyone.
6. **Data sharing.** The data availability statement matches the consent form. If participants did not agree to data sharing, no participant-level data leaves your storage.

A paper that reports data collected without sign-off, or that identifies a participant, scores 0 on criterion F and is referred to the instructor. Data collected without sign-off cannot be reported.

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| Week 11 lab | Results paragraph and abstract for your main finding, audited with your GRIM checker ([lab 11](../labs/lab11.md)). | Counted in lab 11 |
| End of week 12 | Final proposal submitted. Data collection under way for routes P and R. | Proposal brief |
| End of week 13 | **Optional draft** of the method and results. Written feedback within one week if submitted on time. | Feedback only |
| Week 14 session | **Research talk**, 12 minutes plus questions, with your redrawn main figure ([lab 14](../labs/lab14.md)). | Counted in lab 14 |
| Week 15, day 1 | **Final paper** as one PDF, plus a zip of appendix B. | Yes, 90 points |
| Week 15 | **Oral check**, 10 minutes. | Yes, 10 points |

## The oral check

The oral check confirms that the paper is yours and that you can use its models.

| Minutes | What happens |
|---|---|
| 0 to 2 | You state your claim in one sentence, its claim type, and why your design supports that type and no stronger one. |
| 2 to 5 | The examiner changes one input from your paper: the SESOI, a sessionization gap, a tie threshold, an exclusion rule, a coder's table. You predict which result changes and in which direction, then recompute the key figure by hand or with your own code. |
| 5 to 8 | One question from the [exam bank](exam-bank.md) for a week your paper relies on, rewritten with your study's numbers. |
| 8 to 10 | An ethics question about your own study, for example what your consent form allowed you to share, or what you would do if a studio asked for your raw data. |

## Rubric (100 points)

Two markers score independently and agree a mark. A missing section scores 0 on its criterion.

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| A. Title, abstract and introduction | 10 | 9-10: abstract answers all five questions with the size and interval; introduction argues to a gap; verbs match the claim type | 7-8: one abstract question missing, or introduction partly a list | 5-6: abstract without numbers, or a causal verb on associational data | 0-4: topic only |
| B. Method and reproducibility | 15 | 13-15: another team could repeat the study; game version and dates, participant flow, every derivation rule, reliability in this sample, observer role, analysis software; deviations table complete | 10-12: one rule or number missing | 7-9: several details missing; replication would need emails | 0-6: method cannot be followed |
| C. Quantitative results | 15 | 13-15: every key estimate with effect size, interval, `n` and a SESOI verdict; sensitivity analyses reported and interpreted; no bare "significant" | 10-12: sensitivity thin, or one estimate without an interval | 7-9: p-values without sizes, or SESOI chosen after the data | 0-6: missing or wrong |
| D. Qualitative results and warrant | 10 | 9-10: themes as claims with pseudonymized evidence, participant counts and complicating cases; coding process and IRR decision fit the method; reflexive note on the researcher's position | 7-8: evidence thin for one theme | 5-6: quotes without a claim, or counts turned into prevalence | 0-4: missing |
| E. Integration of methods | 10 | 9-10: a named integration step that shaped the analysis; joint display with fit named per row; at least one discordance or expansion followed up | 7-8: joint display present, fits asserted without evidence | 5-6: both strands present but meeting only in the discussion | 0-4: one strand, or two unrelated studies |
| F. Ethics and handling of people | 10 | 9-10: statement complete; everything matches the approval; no identifying detail anywhere, including figures; withdrawals, deletions and data sharing reported | 7-8: one item missing from the statement | 5-6: statement generic, or a minor identifiability lapse fixed on request | 0-4: data outside approval, or a participant identifiable |
| G. Discussion and limitations | 8 | 7-8: limitations name alternative explanations and their direction; replication requirements stated; implications within the evidence | 6: one generic limitation | 4-5: limitations as disclaimers ("the sample was small") | 0-3: missing or overclaiming |
| H. Figures, number audit and data availability | 12 | 11-12: main figure meets all seven checklist items; appendix A audit complete and clean; code runs; data or synthetic data and aggregates shared as the statement says | 9-10: one checklist item missing, or a minor audit error | 6-8: unlabelled bars, or code that needs fixes to run | 0-5: numbers inconsistent across the paper, or no code |
| Oral check | 10 | 9-10: claim and type stated precisely; correct direction and recomputation after the change; exam-bank question correct with the model named; ethics answer matches the protocol | 7-8: one part partly wrong | 5-6: two parts partly wrong | 0-4: cannot explain the paper's own numbers |

## Late work and extensions

- The paper may be submitted up to 72 hours late with a penalty of 5 points out of 90 per 24 hours. After 72 hours it scores 0.
- Extensions are granted for documented illness or emergency. A board's late decision is handled by the switch to route M, not by an extension.
- A missed oral check without a documented reason scores 0 on the oral check. The paper is still marked.

## Academic integrity

Discuss your study with anyone and use the feedback you receive. The paper, analysis and code must be your own, or your pair's. Reusing your own lab and proposal text is expected; mark it with a footnote naming the source. Cite every study and every real-game fact with its version or date. If you use a generative AI tool, say how, verify every number and citation it gives you, and never give it participant data or a classmate's draft. Fabricating or altering data is the most serious offence in research and is referred under the university's misconduct procedure.
