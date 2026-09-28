# MMO402 · Lab 01: Governance audit of a live world

**Week:** 1 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** one of the case analyses (30% of the course in total)

## Objective

Audit one live MMO as a polity. You will map how its rules are enforced, list the channels players have for voice, estimate how responsive each one is, and estimate how high players' switching costs are. Then you will use the exit-voice model from [week 1](../lectures/w01-worlds-as-polities.md) to say where the game's cliff sits and what the developer could do to move it.

## Starter materials

- The week 1 lecture, section 1 (Lessig's four modalities) and section 2 (the exit-voice model).
- The interactive `examples/w01-exit-or-voice.html` once it is built. Until then, use the formulas below in any spreadsheet.
- The audit template below. Copy it into a document or spreadsheet.

**Template A: rules by modality.** At least eight rows.

| # | Rule or constraint | Modality (architecture, law, norms, market) | Who controls it | Evidence (URL, patch note, screenshot you took, or your own observation with date) | How players get around it |
|---|---|---|---|---|---|

**Template B: voice channels.** Every channel you can find, at least four.

| Channel | Who can use it | Cost to a player (minutes) | Evidence the developer responds | Your estimate of `p` (0-1) |
|---|---|---|---|---|

**Template C: switching costs.** Score each source from 0 (none) to 3 (very high) and give one sentence of evidence.

| Source | Score | Evidence |
|---|---|---|
| Character progress that cannot move to another game | | |
| Items and currency | | |
| Friends and guild | | |
| Paid purchases (cosmetics, expansions) | | |
| Skills and knowledge specific to this game | | |

**Spreadsheet formulas for the model.**

```
stay   = MAX(-g, -(1-p)*g - c)
R      = A - stay
r      = R / Smax
exit_uncoupled = MIN(1, MAX(0, r))
exit_coupled   = IF(r<=0, 0, IF(r>0.25, 1, (1 - SQRT(1 - 4*r)) / 2))
```

## Steps

1. **Pick a game.** Choose a live MMO with a public forum or official social channel and at least one patch in the last 12 months. Two students may not audit the same game in the same lab group.
2. **Fill Template A.** Include at least one rule from each modality. For norms, observe or ask players. Do not cite a wiki for a norm unless the wiki documents it with a date.
3. **Fill Template B.** Look for forums, bug trackers, public test realms, surveys, councils, developer streams and social media. For each channel, find one dated example of the developer responding to player input, or record that you found none.
4. **Estimate `p`.** Combine your channels into one estimate of the chance that a moderately popular request changes a decision within a year. Write two sentences explaining it.
5. **Fill Template C** and convert it to an `S_max` on the lecture's scale: add the five scores (0 to 15) and multiply by 20, giving 0 to 300.
6. **Find a real grievance.** Choose one change from the last 12 months that a visible group of players disliked. Estimate `g` on the lecture's scale (100 is "a change that removes most of what I liked about my main activity"), and `A` for the best alternative those players had.
7. **Run the model.** Using `c = 5` unless you have reason to change it, compute `R`, `r` and both exit shares. Then find the grievance level at which your game tips into a cascade (`r > 0.25`) at your estimated `p`.
8. **Recommend one change** the developer could make that moves that tipping point furthest. Show the before and after numbers.

## Deliverable

A report of 1,200 to 1,500 words with the three completed templates as an appendix. The report must name the game and the version or date of your observations, state your `p`, `S_max`, `g` and `A` estimates with reasons, give the model's results, and argue your recommendation. Cite every factual claim about the game.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Rules by modality | Eight or more rules, all four modalities, correct classification, dated evidence | Some rules misclassified or undated | Fewer than five rules or no evidence | 20% |
| Voice channels and `p` | Four or more channels, dated examples of response or non-response, reasoned `p` | Channels listed, `p` weakly argued | `p` asserted without evidence | 20% |
| Switching costs | All five sources scored with evidence, `S_max` computed | Scores given without evidence | Missing | 15% |
| Model use | Correct arithmetic, tipping point found, sensitivity to one estimate shown | Arithmetic correct, no tipping point | Errors or no model | 25% |
| Recommendation and writing | One concrete change, numbers before and after, trade-offs named, plain and cited | Recommendation vague or uncited | No recommendation | 20% |

<details>
<summary>Instructor check values</summary>

- With `g = 100`, `p = 0.2`, `c = 5`, `A = −60`, `S_max = 200`: stay = −85, `R = 25`, `r = 0.125`, exit 12.5% uncoupled and 14.6% coupled.
- A student with template C total 10 has `S_max = 200`. With `p = 0` and `A = −60`, the tipping point is `g = 110`.
- Common error: using silence when voice is better. Check that `stay` takes the larger of the two values.

</details>
