# MMO305 · Week 12 — Community Management

**Why this matters:** The forum is on fire, the subreddit is calling for the lead designer to resign, and the patch is three days old. Is the game in trouble, or is a loud minority upset? Community managers answer that question every week, and the answer decides whether a team reverts good work or ignores a real crisis.

**You will be able to:**
- Compute the share of negative posts a forum will show from the true share of unhappy players and their relative posting rate, and invert it to estimate the true share.
- Explain why forum sentiment can overstate or understate real dissatisfaction, and name the evidence that tells you which.
- Design a feedback pipeline that combines self-selected channels (forums, social media) with representative ones (surveys, telemetry, elected councils).
- Critique a shipped studio's community communication, using timing, specificity and follow-through as criteria.

**Before class:** Nielsen, "Participation Inequality: Encouraging More Users to Contribute" (Nielsen Norman Group, 2006). Hirschman, *Exit, Voice, and Loyalty* (1970), chapter 1 and chapter 3 (the two responses to decline, and how they interact). Reread MA102 week 13, section 5 on bias.

**Prerequisites from earlier courses:** [MA102 week 13, sampling, confidence and why n=5 lies](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (sampling bias, which sample size cannot fix). [MMO303 week 14, communicating balance changes](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w14-communicating-balance-changes.md) (patch notes as part of the change). [MMO304 week 12, economic telemetry and dashboards](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md). [GS101 week 10, World of Warcraft and the mass-market MMO](../../GS101-history-and-critical-study-of-games/lectures/w10-world-of-warcraft-and-the-mass-market-mmo.md). [UX201 week 12, surveys and interviews](../../UX201-game-ux-and-player-psychology/lectures/w12-surveys-and-interviews.md). From this course, [week 10 on channels](w10-communication-design-chat-emotes-pings.md) and [week 11 on newcomers](w11-newcomers-and-mentoring-systems.md).

**Interactive:** [The loud forum](../examples/w12-forum-sentiment.html). Use it during section 2.

---

## 1. What community management is

**Community management** is the work of running the relationship between a game's developers and its players. In an MMO the job usually covers four things.

1. **Communication out.** Patch notes, developer blogs, roadmaps, livestreams, incident updates. MMO303 week 14 covered the patch note in detail. This week looks at the rest.
2. **Listening in.** Reading forums, social media, support tickets and in-game reports, and turning them into something a design team can act on.
3. **Stewardship of spaces.** Setting and enforcing the rules of official forums, Discord servers and in-game channels. Moderation at scale is MMO402's subject ([MMO402 week 6](../../MMO402-emergent-society-governance-and-ethics/lectures/w06-moderation-at-scale.md)). Here we focus on the design of feedback, not on enforcement.
4. **Programs.** Player councils, events, creator programs, community awards, the mentor programs from week 11.

A community manager sits between two groups who misread each other in predictable ways. Developers see a stream of angry posts and conclude the players hate the game. Players see silence from the developers and conclude nobody is listening. The first misreading is a statistics problem, and it is the subject of the worked example. The second is a communication problem, and section 3 turns to it.

### Voice and exit

Albert Hirschman's *Exit, Voice, and Loyalty* (1970) gives the vocabulary. When a product or organisation declines, its members can **exit** (leave, stop paying) or use **voice** (complain, argue, try to change it). **Loyalty** makes members more likely to use voice before exit. Hirschman wrote about firms and states, and his framework fits an MMO well.

- A forum is a voice channel. Players who post are players who care enough to try to change the game.
- Churn is exit. Players who leave quietly send you a signal you only see in telemetry.
- The two interact. If voice is ignored, loyal players exit. If exit is easy (another game is one download away), unhappy players may skip voice altogether.

This matters for reading a forum. The people you hear from are the ones who chose voice. The people who chose exit are not posting at all.

## 2. Worked example: the loud forum

### The hook

At BlizzCon 2013, a player asked about official servers for the original, "vanilla" version of World of Warcraft. J. Allen Brack answered from the panel with a line that became famous, to the effect that players think they want this but do not. Over the next years, demand showed up elsewhere. A fan-run private server, Nostalrius, reached, by its operators' count, about 800,000 registered accounts and 150,000 active players before Blizzard's legal notice shut it down in April 2016. A Change.org petition for official legacy servers, started in April 2016, passed 200,000 signatures and closed at 279,402. Blizzard announced World of Warcraft Classic at BlizzCon 2017 and launched it on August 26, 2019.

Now picture the opposite case, which every live team has lived through. A patch changes a popular ability, the official forum fills with threads calling it the worst patch ever, and the telemetry shows no change in playtime or churn.

In the first case, the studio underestimated a demand. In the second, a forum overstates a complaint. Both are the same mistake: treating a self-selected sample as if it were the player base. The model below lets you put a number on how wrong the sample can be.

### The model

Split the player base into two groups on some question (a patch change, a feature request):

- A share `d` of players are **unhappy** (or, for a request, want the feature).
- The rest, `1 − d`, are **content**.

Each group posts at its own rate. Let `p_u` be the chance an unhappy player posts about the issue and `p_c` the chance a content player does. The ratio `ρ = p_u / p_c` is the **voice ratio**: how many times more likely an unhappy player is to post.

The share of posts that are negative is

```
o = d × ρ / (d × ρ + (1 − d))
```

and, solving for `d`, the share of players who are really unhappy is

```
d = o / (o + ρ × (1 − o))
```

- `o` is what you observe: the negative share of posts.
- `d` is what you want: the unhappy share of players.
- `ρ` is the bias. When `ρ = 1`, the forum is a fair sample and `o = d`. When `ρ > 1`, the forum is louder than the player base. When `ρ < 1`, unhappy players are quieter than content ones, often because they have already exited.

This is Bayes' rule in a single line. MA102 week 13 warned you that bias is the error sample size cannot fix. This model shows how big that error gets.

### Numbers you can check

Forward direction: from the true share to what the forum shows.

| True unhappy share `d` | `ρ = 1` | `ρ = 2` | `ρ = 4` | `ρ = 8` |
|---|---|---|---|---|
| 10% | 10.0% | 18.2% | 30.8% | 47.1% |
| 20% | 20.0% | 33.3% | 50.0% | 66.7% |
| 30% | 30.0% | 46.2% | 63.2% | 77.4% |
| 50% | 50.0% | 66.7% | 80.0% | 88.9% |

Check one cell by hand. `d = 0.2`, `ρ = 4`: `o = 0.8 / (0.8 + 0.8) = 50%`. One player in five is unhappy, and half the forum is negative.

Now the inverse, the one you will use at work: the forum shows `o`, and you want `d`.

| Observed negative share `o` | `ρ = 1` | `ρ = 2` | `ρ = 4` | `ρ = 8` |
|---|---|---|---|---|
| 50% | 50.0% | 33.3% | 20.0% | 11.1% |
| 70% | 70.0% | 53.8% | 36.8% | 22.6% |
| 80% | 80.0% | 66.7% | 50.0% | 33.3% |

A forum that is 70% negative is consistent with anything from 23% to 70% of players being unhappy, depending on `ρ`. **The forum alone cannot tell you which.** That is the lesson: without an estimate of `ρ`, forum sentiment is not a measurement of the player base.

### Counting heads

The same model in counts makes the point concrete. A game has 100,000 active players. 20% are unhappy with a change and post at 4% (`p_u = 0.04`). The content 80% post at 1% (`p_c = 0.01`), so `ρ = 4`.

```
negative posters = 100,000 × 0.20 × 0.04 = 800
positive posters = 100,000 × 0.80 × 0.01 = 800
```

The forum is split evenly, 800 against 800, while four players in five are content. And only 1,600 of 100,000 players, 1.6%, posted at all. That fits Nielsen's participation inequality, the rough rule that in online communities about 90% of users never contribute, 9% contribute a little, and 1% produce most of the content.

### Estimating ρ

You cannot fix the bias without an estimate of `ρ`, and you can get one. Three methods, from cheapest to best:

1. **Link posters to accounts.** If forum accounts are linked to game accounts, compare the posters' telemetry with everyone else's. If posters who complained about a change also cut their playtime after it, and non-posters did not, the complaint is broad. If playtime moved the same for both, you are hearing a vocal subset.
2. **Run a representative survey.** Survey a random sample of active players (UX201 week 12). The survey gives you `d` directly, with a sampling error you can compute (MA102 week 13). Compare it with `o` and you have `ρ` for this topic, which you can reuse as a prior for similar topics.
3. **Watch exit.** Churn and playtime after a change are behaviour, not opinion. They measure what players did, including the ones who never post.

Each method has its own bias. Surveys miss players who already quit. Linked telemetry shows posters, not the silent unhappy. Exit data mixes the change with everything else in the patch. Use two, and look for agreement.

### A visual the student can move

Open `examples/w12-forum-sentiment.html`. The left panel is a "forum" of 100 post icons, coloured by sentiment. The right panel is the "player base" of 100 player icons. Set `d = 0.2` and slide `ρ` from 1 to 8. The forum turns red while the player base does not change at all. Then switch to inverse mode, fix the forum at 70% negative, and slide `ρ`: the player base changes under a forum that looks identical. The last control shows a band of plausible `d` for a range of `ρ` you are unsure of, which is how you should report forum sentiment to a design team.

### Cross-game and cross-context recognition

**World of Warcraft Classic (2013 to 2019).** The Classic story is `ρ < 1` on the official forum. Players who wanted the old game had largely exited to private servers, where their voice was not heard by Blizzard's official channels. The best evidence of `d` was behaviour elsewhere: 150,000 active players on one private server and 200,000 petition signatures. The model warns in both directions. A loud forum can overstate unhappiness, and a quiet one can hide demand that has already left.

**Steam user reviews (Valve, September 2017 and March 2019).** A review score is a forum average with a posting bias. Review bombs, sudden floods of negative reviews driven by an outside controversy, push `ρ` far above 1 for a few days. In September 2017 Valve added a histogram of reviews over time, so a buyer can see a short spike and discount it. In March 2019 Valve began flagging review-bomb periods and excluding all reviews from those periods, positive and negative, from the displayed score. Both changes are corrections for `ρ`, made by the platform rather than by the reader.

**EVE Online, the Council of Stellar Management (2008 onward).** CCP set up an elected player council in 2008. By Wikipedia's account, candidates were invited in March and the first council of nine was elected in May after a two-week vote. An elected council is a designed sample rather than a self-selected one. It is not a random sample either, because the players who vote are more engaged than average, but its bias is known and stable, and its members meet the developers in person. MMO402 studies the council in depth.

**Nielsen's participation inequality (2006).** The 90-9-1 rule is the population-level fact that makes `ρ` matter. If only 1% of players produce most posts, then even a small difference between the unhappy and the content in who belongs to that 1% becomes a large difference in what the forum shows.

### Eyes-open design judgment

- **Do not ignore the forum.** A biased sample is still a sample. Forums find bugs, exploits and confusing designs faster than any survey, because they are full of the most engaged players. The bias is in how many people hold an opinion, not in whether a problem exists.
- **Report a range, not a number.** "The forum is 70% negative, which with our usual voice ratio of 2 to 4 means 37% to 54% of players are unhappy" is a sentence a design team can act on. "The community hates it" is not.
- **Keep your `ρ` history.** Every time you have both a survey and a forum reading on the same topic, record the ratio. After a year you will know your community's voice ratio for balance changes, for monetisation and for bugs, and you can correct faster.
- **Remember exit.** When `ρ < 1`, the forum is quieter than the player base. That happens when unhappy players have given up on voice. A calm forum during a slow churn rise is a warning, not good news.
- **Representation changes behaviour.** Once players know that forum volume moves the studio, they organise to post more, and `ρ` rises. A studio that visibly weighs surveys and councils as well reduces the payoff of brigading.

### Check yourself (worked example)

1. 25% of players dislike a change and `ρ = 3`. What share of the forum will be negative?
2. The forum is 60% negative. A random survey finds 30% of players unhappy. What is `ρ`?
3. After a patch, the forum is only 20% negative, but churn has risen. Give a value of `ρ` that fits a true unhappy share of 40%, and explain what it means in Hirschman's terms.

<details>
<summary>Answers</summary>

1. `o = 0.75 / (0.75 + 0.75) = 50%`.
2. Rearrange `o = dρ / (dρ + 1 − d)`: `ρ = o(1 − d) / (d(1 − o)) = 0.6 × 0.7 / (0.3 × 0.4) = 0.42 / 0.12 = 3.5`.
3. `ρ = 0.2 × 0.6 / (0.4 × 0.8) = 0.12 / 0.32 = 0.375`. Unhappy players post at well under half the rate of content ones. In Hirschman's terms, they are choosing exit over voice, perhaps because they no longer believe voice works.

</details>

## 3. Communication out: timing, specificity, follow-through

The loud-forum model is about listening. The other half of the job is speaking, and players judge it on three things.

### Timing

Silence is a message. During an outage or a bad patch, players fill a gap in official communication with the worst available explanation. A short update that says what is known, what is not known yet and when the next update will come is better than a complete explanation three days late. Incident updates on a schedule ("next update at 18:00 UTC") keep trust even when the news is bad, because each update keeps a promise.

### Specificity

"We are looking into it" is a promise with no content. "We are reverting the cooldown change on Thursday and will re-evaluate after two weeks of data" is a promise players can check. MMO303 week 14 made this argument for patch notes: state the old value, the new value and the intended effect. The same rule applies to every message from the team. Specific messages can be wrong, and that is their value. A team that is sometimes visibly wrong and corrects itself earns more trust than a team that never says anything checkable.

### Follow-through

A community's trust in a studio is a stock, in the GD102 sense. Kept promises add to it slowly. Broken promises drain it fast. **Closing the loop**, telling players what happened to their feedback, is the cheapest inflow available. "You told us X, we did Y, and here is the data" turns a forum complaint into evidence that voice works, which keeps loyal players using voice rather than exit.

### A case: Final Fantasy XIV's relaunch (2010-2013)

The original Final Fantasy XIV launched in 2010 to a poor reception. In December 2010, Square Enix put Naoki Yoshida in charge as producer and director. He set up regular "Letters from the Producer" and live broadcasts, talked plainly about the game's problems, and laid out what the team would change. Square Enix suspended subscription fees for an extended period while the team rebuilt. Square Enix's CEO, Yoichi Wada, apologised publicly at Tokyo Game Show 2011. The original servers closed on November 11, 2012, and the rebuilt *A Realm Reborn* launched in August 2013 and went on to become a commercial success.

You cannot credit communication alone for that outcome. The rebuilt game was also far better. But the communication did something specific. It kept loyal players using voice during two years in which exit was easy, and it gave them checkable promises (dates, features, reasons) that the team then kept. In Hirschman's terms, it raised loyalty by making voice visibly effective.

## 4. A feedback pipeline

Put the pieces together into a pipeline your team can run weekly.

1. **Collect** from every channel: forums, social media, Discord, support tickets, in-game reports, surveys, telemetry.
2. **Tag** each item by topic (class balance, economy, bug, monetisation, social) and sentiment.
3. **Weigh.** For each topic, compute the forum's negative share `o` and apply your recorded range of `ρ` to estimate `d`. Where you have a survey or telemetry, use it to check.
4. **Report** to the design team a short list of topics, each with the estimated range of `d`, the evidence, and a recommended action.
5. **Close the loop** in public: what you heard, what you are doing, and what you are not doing, with reasons.

The pipeline does not decide for the designers. It gives them a number with an honest range instead of the loudest thread.

## In-class activity (25 minutes)

Pairs. Each pair gets a scenario card.

- **A.** A class rework. The class forum is 85% negative. Class play rate fell from 12% to 10% of characters after the patch. There is no survey.
- **B.** A cosmetic shop item. The main subreddit's top ten posts are all complaints. Sales are three times the forecast.
- **C.** A dungeon difficulty increase. Forum sentiment is mixed, 45% negative. Day-7 dungeon participation fell by a third.

Steps:

1. **Estimate (8 min).** Using `ρ` from 2 to 6, compute the range of `d` implied by the forum.
2. **Cross-check (7 min).** Use the behavioural evidence on the card. Does it agree with the low end or the high end of your range? Could `ρ` be below 1?
3. **Draft (10 min).** Write the community post you would publish this week, at most 150 words, that is specific, sets a date for the next update, and closes a loop.

Expected output: the `d` range, a one-sentence verdict on which evidence you trust, and the draft post.

## Common misconceptions

- **"The forum is the community."** It is the part of the community that chose voice, often around 1% of players producing most posts. Treat it as a biased sample and estimate the bias.
- **"Forums always exaggerate complaints."** Only when `ρ > 1`. When unhappy players exit rather than post, `ρ < 1` and the forum understates the problem. Classic demand was underestimated, not overestimated.
- **"More posts means a more accurate picture."** More posts reduce random error. They do nothing about bias, which is the bigger error here (MA102 week 13).
- **"Community management is public relations."** Half the job is listening and turning feedback into evidence the designers can act on. A team that only broadcasts has a megaphone, not a community manager.

## Check yourself

1. A forum is 75% negative about a change. Your recorded voice ratio for balance topics is between 3 and 5. What range of `d` should you report?
2. A studio has 250,000 active players. 12% are unhappy with a feature and post at 3%. Content players post at 0.5%. How many negative and positive posters are there, and what share of the forum is negative?
3. A survey of 400 random active players finds 22% unhappy. Using the MA102 week 13 standard error for a proportion, give an approximate 95% interval for `d`, and say whether a forum-based estimate of 45% is consistent with it.
4. Name one message a studio could publish that would lower `ρ` on a contested topic, and explain the mechanism.

<details>
<summary>Answers</summary>

1. `d = 0.75 / (0.75 + ρ × 0.25)`. At `ρ = 3`: `0.75 / 1.5 = 50%`. At `ρ = 5`: `0.75 / 2.0 = 37.5%`. Report 37.5% to 50%.
2. Negative: `250,000 × 0.12 × 0.03 = 900`. Positive: `250,000 × 0.88 × 0.005 = 1,100`. Negative share `900 / 2,000 = 45%`, while only 12% of players are unhappy (`ρ = 6`).
3. `SE = √(0.22 × 0.78 / 400) ≈ 0.0207`, so the interval is about `0.22 ± 0.041`, or 17.9% to 26.1%. A forum estimate of 45% is well outside it, so the forum has a voice ratio well above the one assumed, or the survey missed a group (for example players who already quit).
4. For example, a post announcing that the team will decide using a survey of random players plus telemetry, and publishing the results. It lowers the payoff of mass posting, so content and unhappy players' posting rates move closer together. It can also invite content players to post, which raises `p_c` directly.

</details>

## Lab / assignment hook

[Lab 12, reading a loud forum](../labs/lab12.md). You tag a synthetic forum dump, estimate `ρ` from a linked survey sample, report `d` with a range for three topics, and write a community post that closes the loop. The field observation assessment can reuse your tagging method on a real community.

## Sources

- Wikipedia, "World of Warcraft Classic" (accessed September 2026). J. Allen Brack's BlizzCon 2013 answer; Nostalrius launch February 2015, about 800,000 registered accounts and 150,000 active players, shut down April 10, 2016; petition of over 200,000 signatures; Classic announced November 3, 2017, released August 26, 2019.
- Nostalrius, press release "Nearly One Million Gaming Accounts Lost in Legacy Servers" (10 April 2016), https://en.nostalrius.org/pr1.pdf (fetched 29 September 2026). Self-reported: 150,000 active players on 800,000 accounts created over one year; international launch 28 February 2015; services stopped after a Blizzard cease-and-desist request.
- Change.org, "Legacy servers among World of Warcraft community" (created 6 April 2016; page viewed 29 September 2026). 279,402 supporters, marked as a victory.
- Wikipedia, "Review bomb" (accessed September 2026). Valve's review histograms (September 2017, with a statement by Alden Kroll) and its March 2019 policy of flagging review-bomb periods and excluding their reviews from the displayed score.
- Steamworks Documentation, "User Reviews" (partner.steamgames.com/doc/store/reviews, accessed 29 September 2026). Current policy: during an off-topic review bomb, "the reviews during that period will be bucketed" and "will not contribute to your overall score." The 2017 and 2019 dates rest on the Wikipedia entry above.
- Wikipedia, "Eve Online" (accessed September 2026). The Council of Stellar Management: candidates invited March 2008, 66 candidates for nine seats, first council elected in May 2008 after a two-week vote. Secondary only: the CCP announcements behind these citations were not reachable on 29 September 2026, so the lecture attributes the details to Wikipedia.
- Wikipedia, "Final Fantasy XIV (2010 video game)" (accessed September 2026). Naoki Yoshida as producer and director from December 2010; Letters from the Producer and live broadcasts; suspended fees; apology at Tokyo Game Show 2011; servers closed November 11, 2012; *A Realm Reborn* launched August 2013.
- Nielsen, J. (2006, October 9). "Participation Inequality: Encouraging More Users to Contribute." Nielsen Norman Group. The 90-9-1 rule and its consequence that postings are an unrepresentative sample of users.
- Hirschman, A. O. (1970). *Exit, Voice, and Loyalty: Responses to Decline in Firms, Organizations, and States*. Harvard University Press.

## Interactive spec: examples/w12-forum-sentiment.html

**The one insight:** the forum's negative share can look like a revolt while the player base barely changes, and one forum reading is consistent with a wide range of true dissatisfaction. The two panels must share the same `d` and show visibly different colour shares.

**Layout (mobile first):** two 10 × 10 icon grids, stacked on phones, side by side at 700px and wider. Controls above, numbers below.

**Left grid, "What the forum shows":** 100 post icons (generic speech bubbles), `round(100 × o)` of them marked negative (filled, with a minus glyph for colour-blind users), the rest positive (outline, plus glyph).

**Right grid, "Who your players are":** 100 player icons (generic circles), `round(100 × d)` marked unhappy with the same glyph convention.

**Mode toggle:**
- **Forward:** sliders `d` (0.01 to 0.99, step 0.01, default 0.20) and `ρ` (0.25 to 10, log scale, default 4). Compute `o = dρ / (dρ + 1 − d)`.
- **Inverse:** sliders `o` (0.01 to 0.99, default 0.70) and `ρ`. Compute `d = o / (o + ρ(1 − o))`. The left grid stays fixed while the right grid changes.
- **Range:** slider `o` and a two-handle range for `ρ` (default 2 to 4). Show the interval `[d(ρ_max), d(ρ_min)]` as a shaded band on a horizontal 0-100% bar, with both ends printed.

**Counts panel:** input `N` players (default 100,000) and `p_c` (default 0.01, so `p_u = ρ × p_c`, capped at 1). Print negative posters `N × d × p_u`, positive posters `N × (1 − d) × p_c`, total posters and the share of players who posted.

**Test values (must match):**
- Forward `d = 0.20, ρ = 4`: `o = 50.0%`. `d = 0.10, ρ = 8`: 47.1%. `d = 0.30, ρ = 2`: 46.2%. `d = 0.50, ρ = 1`: 50.0%.
- Inverse `o = 0.70`: `ρ = 2` gives 53.8%, `ρ = 4` gives 36.8%, `ρ = 8` gives 22.6%.
- Range `o = 0.75`, `ρ` 3 to 5: band 37.5% to 50.0%.
- Counts `N = 100,000, d = 0.20, p_c = 0.01, ρ = 4`: 800 negative, 800 positive, 1,600 posters, 1.6% posted.
- Forward `d = 0.40, ρ = 0.375`: `o = 20.0%` (the "quiet exit" case; label `ρ < 1` as "unhappy players quieter than content ones").

**Accessibility:** grids have text equivalents in an `aria-live` region ("Forum: 50 of 100 posts negative. Players: 20 of 100 unhappy."); sliders keyboard operable; glyphs as well as colour; reduced motion disables grid transitions.
