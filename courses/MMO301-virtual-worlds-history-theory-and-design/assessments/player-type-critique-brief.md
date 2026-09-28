# MMO301 · Player-type critique brief

**Weight:** 20% of the course grade.
**Part A:** [Lab 08, the Bartle population model](../labs/lab08.md). 5% of the course.
**Part B:** [Lab 09, a motivation survey study](../labs/lab09.md). 5% of the course.
**Part C:** the critique essay, specified below. 10% of the course. Due at the start of week 11.
**Lectures:** [week 8, player types and the hero's journey](../lectures/w08-player-types-bartle-1996-and-the-heros-journey.md) and [week 9, motivation research beyond Bartle](../lectures/w09-motivation-research-beyond-bartle-yee.md). Part C may also draw on [week 7](../lectures/w07-themepark-vs-sandbox.md) (players as content) and [week 10](../lectures/w10-immersion-identity-and-the-avatar.md) (Bartle's immersion ladder, which is a different idea from Yee's Immersion component).

## What this component is for

The second course outcome is "apply player-type models critically." Critically does not mean dismissively. Bartle's 1996 paper is a careful argument about how groups of players change each other's numbers, and parts of it still predict real design moves, such as splitting a world to fence off player killers. Yee's surveys measured what the paper could not, and found that most players have no single dominant motivation. Studios still write "this feature is for achievers."

This component asks you to take one real use of player types in design and test it with both kinds of evidence. Lab 08 gives you Bartle's dynamics as a model you can run. Lab 09 gives you your own small measured sample. The essay puts them together.

## Parts A and B: labs 08 and 09

Follow each lab as written. Each is marked out of 100 with the rubric printed in the lab and scaled to 25 points of this component. Neither can be dropped, because the essay depends on both.

| Lab | Assigned | Due |
|---|---|---|
| [08](../labs/lab08.md) | Week 8 | Start of week 9 |
| [09](../labs/lab09.md) | Week 9 | Start of week 10 |

## Part C: the critique essay (50 points)

### The task

Pick one **artifact** that uses player types to make a design or business decision. Say what it assumes about players, test those assumptions with the week 8 model, Yee's findings and your own Lab 09 data, and replace it with something better.

### Choosing an artifact

Any of these, approved at the week 9 milestone:

- A published persona set, segmentation or design document excerpt that names Bartle types (or their descendants) and makes a decision with them. Cite it with its date.
- A public talk, article or postmortem in which a developer attributes a feature to a player type.
- An online type test and the claims made about its results.
- **The course default, "Ironvale personas."** Use this if you cannot find a public artifact you are allowed to cite. It is invented.

> *Ironvale* is a planned fantasy MMO. Its design document defines four personas and splits the first year's content budget by them.
> **Ada the Achiever** (40% of players, 40% of budget): wants levels, gear and leaderboards; hates chat; plays alone.
> **Sam the Socialiser** (30%, 20%): wants guild halls and emotes; does not care about gear.
> **Eli the Explorer** (20%, 30%): wants hidden areas and lore.
> **Kit the Killer** (10%, 10%): wants open PvP everywhere; "keep Kit away from Sam."
> The document says the shares came from "a Bartle Test we ran on 600 beta sign-ups." It plans open PvP in two of eight zones.

### Required sections

1,800 to 2,200 words, plus tables and charts. Use these headings.

1. **The artifact and its claim.** What it says about players, what decision it makes with that claim, and the assumptions the decision needs. Name each assumption in one sentence (for example "types are exclusive", "shares measured by a forced-choice test are headcounts", "killers only harm socialisers").
2. **What Bartle said.** Paraphrase the parts of the 1996 paper the artifact relies on, and the parts it ignores. Quote at most one short phrase. Be fair to the paper. It says most players lean a little toward all four types, and it describes balance as similar influence, not similar numbers.
3. **What the model shows.** Use your Lab 08 runs. Which of the artifact's expectations follow from Bartle's signs alone, and which depend on coefficients nobody measured? If the artifact makes a rule decision (such as "PvP in two of eight zones"), translate it into a `protection` value and show what your model does with it.
4. **What measurement shows.** Use Yee's findings (the 43% with no primary motivation, the near-independent components, the achievement and competition link, the gender and sample caveats) and your Lab 09 data, including your labelled shares at three values of `c` and the margin of error on your unlabelled share. Say plainly what your sample of 20 or more can and cannot show.
5. **What the artifact hides.** At least three specific players it misdescribes, shown as rows of component scores. At least one must be a boundary case whose label flips under a small change in answers, and one must be unlabelled.
6. **The replacement.** Rewrite the artifact's decision using component scores. For a persona set, that means profiles with scores on each component and features scored by the components they serve. For a budget split, show the new split and the reasoning. For a rule decision, show the new rule and its model result.
7. **Limits.** What your own critique cannot show, and one question a better-designed study could answer.

### Rules

- Every claim about Bartle's or Yee's work cites the paper and section. Claims about a real game or studio need a source with its date or era.
- Do not reproduce another survey's items. Your Lab 09 items are your own.
- Treat your Lab 09 respondents' data as anonymous. Report no names and nothing that could identify a respondent.

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| Start of week 9 | Lab 08 submitted | Part A |
| Week 9 lab session | **Artifact approved.** Show the marker your artifact (or choose Ironvale) and list its assumptions in bullet form. Five minutes. | Required |
| Start of week 10 | Lab 09 submitted, with at least 20 responses | Part B |
| Week 10 lab session | **Outline check.** Section headings with two lines each, and the three "hidden players" as score rows. The marker signs off or names one fix. | Required, not graded |
| Start of week 11 | **Essay submitted** | Part C |
| Week 12 lab session | Essay returned; 5-minute spot check on one of your numbers, drawn in the style of the [exam bank](exam-bank.md) (weeks 8 and 9) | No, but see below |

The spot check is not graded on its own. If you cannot explain a number you submitted, the marker can move your "Model and data" line down one band.

## Part C rubric (50 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Claim and assumptions | 8 | 7-8: the artifact's decision and every assumption behind it named precisely; artifact cited | 5-6: assumptions named, one missing or vague | 4: claim summarized, assumptions implied | 0-3: no clear claim |
| Reading of Bartle | 8 | 7-8: accurate paraphrase of what the paper says and does not say, including its own caveats; fair to the source | 5-6: accurate but selective | 4: loose paraphrase or one misreading | 0-3: misrepresents the paper |
| Model and data | 14 | 13-14: Lab 08 runs separate sign-driven from number-driven conclusions; Lab 09 data and Yee's figures used with the margin of error; the artifact's rule translated and run | 10-12: both sources used, one thinly | 7-9: one source used well, the other named only | 0-6: no runs or data used |
| Hidden players | 6 | 6: three or more score rows, including a boundary case and an unlabelled player, each explained | 4-5: three rows, one explanation weak | 3: fewer than three rows | 0-2: missing |
| Replacement | 10 | 9-10: a component-based replacement that makes the same kind of decision, with numbers, and says what it costs the team | 7-8: replacement present, decision thinly argued | 5-6: replacement in words only | 0-4: missing, or "don't use types" with nothing in its place |
| Limits and writing | 4 | 4: honest limits with a testable question; plain, within length | 3: limits generic | 2: limits missing or length badly off | 0-1: both |

## Late work

The essay may be submitted up to 48 hours late for a loss of 5 of its 50 points. After that it is marked for feedback only and scores 0 on Part C. Labs 08 and 09 follow the lab late rule in the [case studies brief](case-studies-brief.md#late-work-and-integrity), including its one free extension.
