# MMO402 · Week 11 — Minors in Online Worlds

**Why this matters:** Children play MMOs whether or not you built the game for them, and the law treats you differently the moment you know they are there. The age check you choose and the defaults you ship decide how many children meet strangers in your world and how many adults you lock out by mistake. Those numbers are yours to compute before a regulator computes them for you.

**You will be able to:**
- Compute how many under-13 players reach unrestricted features, and how many older players are wrongly restricted, under a self-declared age gate and under an age-estimation check.
- Explain, using base rates, why an accurate age check can still flag more older players than children when children are a small share of sign-ups.
- Compare the effect of the age gate with the effect of the default setting on children's exposure to stranger chat.
- Critique a real child-safety design (Club Penguin, Toontown, Fortnite after 2022, Roblox after 2025) in terms of gate, default and fallback.

**Before class:** U.S. Federal Trade Commission, press release "Fortnite Video Game Maker Epic Games to Pay More Than Half a Billion Dollars over FTC Allegations of Privacy Violations and Unwanted Charges" (19 December 2022), about 10 minutes. UK Information Commissioner's Office, *Age appropriate design: a code of practice for online services*, the summary of the 15 standards and standards 3 (age appropriate application) and 7 (default settings). Reread the section on chat channels and filters in [MMO305 week 10](../../MMO305-social-systems-and-online-behaviour/lectures/w10-communication-design-chat-emotes-pings.md).

**Prerequisites from earlier courses:** [MA102 week 1, sample spaces and events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w01-sample-spaces-and-events.md) (splitting a population into disjoint groups). [MA102 week 14, intro to hypothesis testing](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (false positives and false negatives). [MMO305 week 10, communication design](../../MMO305-social-systems-and-online-behaviour/lectures/w10-communication-design-chat-emotes-pings.md) (chat channels, filters and emotes). [MMO305 week 8, griefing typology](../../MMO305-social-systems-and-online-behaviour/lectures/w08-griefing-typology-and-design-responses.md). [MMO402 week 10, addiction and wellbeing](w10-addiction-wellbeing-and-responsible-design.md) (China's fatigue system, which this week's time limits replaced). [DB201 week 13, privacy, GDPR and data retention](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md).

**Interactive:** [The gate and the default](../examples/w11-age-gate.html)

---

## 1. Why minors change the rules

Three things change when a player is a child. The law changes, the risks change, and the player's ability to judge those risks changes. A world built for adults assumes the reverse on all three.

### The law

Two legal regimes shape most game design for children, and both are worth knowing in outline. (This is design knowledge, not legal advice. A studio shipping to children needs counsel.)

**The United States, COPPA.** The Children's Online Privacy Protection Act was passed in 1998 and took effect on 21 April 2000. It applies to online services directed at children under 13, and to general-audience services that have actual knowledge that a user is under 13. Such a service must obtain verifiable parental consent before collecting, using or disclosing personal information from the child. "Actual knowledge" is the part designers trip over. If your sign-up form asks for a birth date, or asks "what grade are you in?", and the answer says 11, you now know. A 2013 update widened "personal information" to include persistent identifiers used for tracking, geolocation, and photos, video or audio containing the child's image or voice. Voice chat records a child's voice.

**The United Kingdom, the Age Appropriate Design Code** (often called the Children's Code). It took effect on 2 September 2020, with enforcement from 2 September 2021 after a one-year transition. It applies to online services likely to be accessed by anyone under 18, which is a much wider net than COPPA's "directed to children under 13." Its 15 standards include best interests of the child, age appropriate application, default settings, data minimisation, geolocation, profiling, and nudge techniques. Standard 7 says settings must be high privacy by default unless there is a compelling reason otherwise. California adapted the code in 2022 as AB 2273, and a federal judge blocked that law in September 2023 on free-speech grounds, so its status differs across jurisdictions and years.

Read those two together and you get the design problem. COPPA is triggered by knowledge, so the cheapest legal strategy is to know as little as possible. The UK code is triggered by likelihood, so not knowing does not protect you. A studio that sells worldwide ends up designing for the stricter rule.

**China** took a third route, direct limits on time. A 2019 rule limited players under 18 to 90 minutes on most days and 3 hours on weekends and holidays, with no play from 22:00 to 08:00. In September 2020 the government made its own name-based authentication system available to game companies. From 30 August 2021, the National Press and Publication Administration limited minors to one hour, from 20:00 to 21:00, on Fridays, weekends and legal holidays. Real-name registration is the gate. The time window is the rule behind it.

### The risks

For an MMO the main risks to children are contact risks (strangers who talk to them, including adults seeking to groom them), content risks (what other players say and show), and commercial risks (spending they do not understand). The Epic Games case in 2022 touched two of those three. The FTC alleged that Fortnite turned on live text and voice communication by default and matched children and teens with strangers, exposing them to bullying, harassment and threats. It also alleged that Epic used interface design to push players into unwanted purchases. Epic agreed to a $275 million civil penalty for COPPA violations, the largest ever for breaking an FTC rule, plus $245 million in refunds over the purchase design. The order requires voice and text chat to be off by default for children and teens, with affirmative parental consent needed for under-13s.

### The player's judgment

Adults in an MMO can be expected, roughly, to know that a stranger offering free gold for their password is a scammer. Children often cannot, and that is the reason for the other rules. It also means the ethical question is not only "what does the law require?" In week 8 you read Koster's rights of players, which assume a player who can consent to the world's terms. A nine-year-old cannot meaningfully consent to a terms of service. The world has to be safe by construction for players who cannot yet protect themselves.

## 2. Worked example: the gate and the default

### The hook

The FTC's order against Epic did two things. It required the company to switch chat off by default for children and teens. It also required an age gate, a neutral one that lets users identify as 13 or older without being steered toward any answer. Three years later, Roblox went further. According to Wikipedia's account of its safety changes, from December 2025 in a few countries and globally from January 2026, Roblox required an age check for chat, using either an ID or a video selfie analyzed by age-estimation software, and limited chat to players in similar age bands.

These are two different levers. One is the **gate**: how you find out who is a child. The other is the **default**: what a player gets if nobody has proved anything. Which lever protects more children? And what does each cost the players who are not children?

### The model

Take `N` new sign-ups. A share `π` are under 13. Call them children and everyone else "13+". An age check is a test with two error rates, the same two you met in MA102 week 14.

- **Sensitivity `se`**: the share of children the check correctly places in child mode. The rest, `1 − se`, are **missed** and reach the 13+ experience.
- **Specificity `sp`**: the share of 13+ players the check correctly lets through. The rest, `1 − sp`, are **wrongly restricted**.

A **self-declared gate** (type your birth date) has `sp ≈ 1`, because older players rarely claim to be younger, and `se = 1 − ℓ`, where `ℓ` is the share of children who lie. An **age-estimation check** has both error rates below 1.

Then:

```
children missed        = N × π × (1 − se)
13+ wrongly restricted = N × (1 − π) × (1 − sp)
share of "child" flags that are children = π × se / (π × se + (1 − π) × (1 − sp))
```

The last line is the **precision** of the child flag. It depends on `π`, the base rate, and that dependence is the first surprise of this example.

Now add the default. In child mode, assume stranger chat is off and cannot be turned on without a parent (so exposure is zero). In 13+ mode, stranger chat is either **on by default**, and a share `k_on` of players keep it on, or **off by default**, and a share `k_off` switch it on. Default settings are sticky. Most users keep whatever they are given, which is why the UK code and the FTC order both target defaults. The children exposed to stranger chat are the missed children who end up with chat on:

```
children exposed = children missed × k      (k = k_on or k_off)
```

All the rates in this example are invented for teaching: `ℓ = 0.5`, `se = 0.90`, `sp = 0.95`, `k_on = 0.9`, `k_off = 0.3`. Real age-estimation accuracy varies by vendor, age band and population, and real lie rates vary by service. The interactive lets you change every one of them. The structure of the result does not depend on these particular values.

### Numbers you can check

**Case A: a game where 20% of sign-ups are under 13** (`N = 100,000`, `π = 0.20`, so 20,000 children and 80,000 13+).

| Gate | Children missed | 13+ wrongly restricted | Precision of child flag | Exposed, default on | Exposed, default off |
|---|---|---|---|---|---|
| Self-declared (`ℓ = 0.5`) | 10,000 | 0 | 100% | 9,000 | 3,000 |
| Age estimation (`se = 0.9`, `sp = 0.95`) | 2,000 | 4,000 | 81.8% | 1,800 | 600 |

**Case B: a game where 5% of sign-ups are under 13** (`π = 0.05`, so 5,000 children and 95,000 13+).

| Gate | Children missed | 13+ wrongly restricted | Precision of child flag | Exposed, default on | Exposed, default off |
|---|---|---|---|---|---|
| Self-declared (`ℓ = 0.5`) | 2,500 | 0 | 100% | 2,250 | 750 |
| Age estimation (`se = 0.9`, `sp = 0.95`) | 500 | 4,750 | 48.6% | 450 | 150 |

Check the harder cells by hand. In case A with estimation, `20,000 × 0.1 = 2,000` children are missed and `80,000 × 0.05 = 4,000` older players are wrongly restricted. The check flags `18,000 + 4,000 = 22,000` players as children, and `18,000 / 22,000 = 81.8%` of them really are. In case B the same check flags `4,500 + 4,750 = 9,250`, and only `4,500 / 9,250 = 48.6%` are children. The check did not get worse. The population did.

### Three things the tables show

**First, base rates rule precision.** When children are 5% of sign-ups, an estimator that is right 95% of the time about older players still restricts more older players (4,750) than it catches children (4,500). Every one of those 4,750 players gets a restricted account and a support ticket. This is the same arithmetic that makes medical screening for rare conditions produce mostly false alarms. Before you choose a check, find out your `π`.

**Second, the default is a lever of the same size as the gate.** In case A, going from self-declared to estimation cuts exposure from 9,000 to 1,800, an 80% drop. Going from default on to default off, with the cheap self-declared gate, cuts it from 9,000 to 3,000, a 67% drop. The default costs older players one extra click in a settings menu. The estimator costs 4,000 of them a wrong restriction, and costs every player a biometric check. Doing both gets you to 600.

**Third, the two levers multiply.** Exposure is `N × π × (1 − se) × k`. Halving `1 − se` and halving `k` each halve exposure, and together they quarter it. There is no single fix, and there does not need to be. You are stacking layers the same way MMO303 week 4 stacked mitigation layers, and the same multiplicative rule applies.

Open the interactive. The left view is a population bar split into four blocks (children caught, children missed, 13+ passed, 13+ restricted), with the missed block split again by chat setting. The right view plots children exposed against 13+ wrongly restricted, with one point per design. Drag `π` down from 20% to 5% and watch the restricted count overtake the caught count on the left, while the points on the right slide sideways. Then flip the default and watch every point drop by the same factor.

### Cross-game recognition

**Club Penguin (Disney, 2005 to 2017).** Designed for children aged 6 to 14. It offered two chat modes. Ultimate Safe Chat let players pick only from a menu of fixed phrases. Standard Safe Chat let them type, behind a filter that blocked profanity and personal information such as phone numbers and email addresses. Blocked messages were shown only to the sender, so a child trying to share a phone number saw it sent while nobody else did. In May 2007, about 70 of the company's 100 staff worked on moderation. In our model, Club Penguin set `π` very high (it was a children's world), treated every player as a possible child, and made its 13+ mode itself child-safe. When the whole world is child mode, `se` does not matter, and the price is paid by older players' freedom to talk.

**Toontown Online (Disney, 2003 to 2013).** SpeedChat gave every player a menu of approved phrases. SpeedChat Plus allowed typing against a filter that replaced forbidden words with animal sounds. Open chat between friends ("Secret Friends," later "True Friends") required exchanging a code outside the game, and for under-13 players required parental approval. That code exchange is a gate built on real-world relationships. The design assumption is that people who can swap a code in person or by phone already know each other, so the check targets strangers rather than age.

**Fortnite after the 2022 FTC order.** Voice and text off by default for children and teens, a neutral age gate, and parental consent for under-13 communication. That is our model's "self-declared plus default off" row, the cheap combination, made mandatory. In case A it moves exposure from 9,000 to 3,000 without any biometric check.

**Roblox from 2025 to 2026.** An age check (ID or facial age estimation) required for chat. That moves from the self-declared row to the estimation row. Our tables predict what it trades: fewer children in open chat, and some older players placed in the wrong band. How many depends on the estimator's error rates and on Roblox's own `π`, which is high. High `π` favors estimation, because precision rises with the base rate.

**China from 2021.** Real-name registration linked to a government identity system. In our model that pushes `se` close to 1, at the cost of every player's anonymity. It is the extreme corner of the design space: the fewest missed children and the most data collected about every player.

Five worlds, one model: a gate with two error rates, a default with a keep rate, and a base rate that decides how the costs split.

### Design judgment

- **Measure your base rate first.** A game with 30% children and a game with 3% children need different checks. Survey data, parental accounts and support tickets all give rough estimates.
- **Change the default before you buy an estimator.** Off-by-default chat for everyone until they choose it is cheap, it is what regulators ask for, and it cuts exposure by the same factor whatever your gate.
- **Give wrongly restricted players a way out.** With any real check, thousands of older players will be misclassified. An appeal path (ID, a parent's account, a second check) turns a support crisis into a queue. Week 7's appeal design applies here directly.
- **Count what the check collects.** Facial estimation and ID checks collect sensitive data about everyone, including the children you were protecting. The UK code's data minimisation standard asks you to keep only what you need. Delete images after the estimate.
- **Do not let the gate decide alone.** Behavior after sign-up (reports, what players say about school and age, friend-graph patterns) updates your estimate of who is a child. COPPA's actual-knowledge rule means those signals can trigger legal duties too, so build the process for handling them before you collect them.

## 3. Design patterns for worlds with children in them

The worked example covered contact. Here are the patterns for the other risks, and for the tensions they create.

### Communication tiers

Most child-safe worlds use a ladder of communication rather than a switch.

1. **Menu chat.** Fixed phrases only (Club Penguin's Ultimate Safe Chat, Toontown's SpeedChat). Nothing personal can be said. Emotes and pings, from MMO305 week 10, live here too.
2. **Filtered chat.** Typing against an allow-list (only approved words pass) or a block-list (listed words are stopped). Allow-lists are safer and more frustrating. Block-lists are easier and always leak, because players invent spellings faster than you can list them.
3. **Friend chat.** Open chat with people the player already knows, established by a code exchange or parental approval.
4. **Open chat.** Anyone, anywhere, subject to moderation.

Each rung needs its own gate. The practice the FTC's Fortnite complaint targeted was putting every player on rung 4 by default.

### Spending

Children do not reason about premium currencies the way adults do, and a currency that hides the real price makes it worse. The Epic settlement's $245 million refund was about interface design that led to unwanted purchases, including purchases made by children without parents knowing. Patterns that help: real-money prices shown next to currency prices, a confirmation step for every purchase, a parent-set monthly limit, and easy refunds. MMO403 week 8 covers dark patterns in detail; see the [MMO403 week 8 lecture](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w08-dark-patterns.md).

### Time

China's approach is a hard window. Western games mostly offer parental time controls instead: a parent sets a daily limit, and the game enforces it. Last week's pacing models apply. A parental daily limit reads the same "time in session" clock as a fatigue system, and it has the same weakness, a second account, unless it is tied to an identity.

### Data

Collect less. A child's account needs a login, a display name and a parent's contact. It rarely needs a birth date stored forever (store the age band), a precise location, or voice recordings. Everything you keep is something you may have to disclose, secure and delete. DB201 week 13 covers retention policy.

### Tensions you will not resolve, only choose

- **Safety against privacy.** Every stronger gate collects more about everyone. Real-name registration is the most accurate gate and the largest dataset.
- **Protection against inclusion.** Strict child modes push children toward other games with fewer protections, or toward lying about their age. A gate that is too costly to pass honestly raises `ℓ`.
- **Protection against autonomy for teenagers.** A 16-year-old is not a 9-year-old. The UK code covers everyone under 18 but asks for age-appropriate treatment, which means different defaults for different bands, not one child mode.
- **Separation against community.** A separate world or server for children keeps strangers out. It also splits families, classrooms and siblings who want to play together, and the older child in the family usually leaves for the main world.

## In-class activity (25 minutes)

Pairs. You are the safety lead for a new fantasy MMO. Marketing expects `π = 10%` under-13 sign-ups.

1. Using the interactive or the formulas, compute children missed, 13+ wrongly restricted and children exposed for all four combinations of gate (self-declared with `ℓ = 0.5`, estimation with `se = 0.9`, `sp = 0.95`) and default (on at `k = 0.9`, off at `k = 0.3`). Use `N = 100,000`. (10 min)
2. Your budget allows either the estimator or a moderation team that halves the harm to exposed children. Which do you choose? Show the numbers. (7 min)
3. Write the one-sentence message a wrongly restricted 13+ player sees, and the appeal step it offers. (5 min)
4. Swap with another pair and find one situation their plan handles badly.

Expected output: a 2 × 2 table, a choice with a number behind it, and a one-sentence message.

## Common misconceptions

- **"A 95% accurate age check means 95% of flagged players are children."** Precision depends on the base rate. At 5% children, the lecture's check flags more older players than children.
- **"If we never ask for age, COPPA doesn't apply."** Not asking may avoid actual knowledge in the US, but the UK code applies to services likely to be accessed by children, and child-directed content can bring COPPA in regardless.
- **"The age gate is the safety system."** The gate and the default multiply. An off-by-default setting cuts exposure by the same factor whatever gate you use, at almost no cost.
- **"Menu chat is overcautious."** It has a real cost in expressiveness, but it is the only design in which nothing personal can be typed. Worlds with very high child shares have chosen it for that reason.

## Check yourself

1. A game has `π = 0.30`, `N = 50,000`, and an estimator with `se = 0.85`, `sp = 0.90`. Compute children missed, 13+ wrongly restricted, and the precision of the child flag.
2. With the same numbers, chat defaults on with `k_on = 0.8`. How many children are exposed? A colleague says a good enough default makes the estimator unnecessary. Using the formula, what `k` would the default need to match a perfect estimator (`se = 1`), and what does that tell you?
3. A self-declared gate has `ℓ = 0.6`. By how much must the default's keep rate fall to match the exposure of an estimator with `se = 0.9` and `k = 0.9`?
4. Toontown's True Friends code does not check age at all. Rewrite it in the model: which rate does it change, and for which kind of risk?

<details>
<summary>Answers</summary>

1. Children `15,000`, missed `15,000 × 0.15 = 2,250`. Older players `35,000`, restricted `35,000 × 0.10 = 3,500`. Flagged children `12,750`, total flags `16,250`, precision `12,750 / 16,250 ≈ 78.5%`.
2. Exposed `2,250 × 0.8 = 1,800`. A perfect estimator misses nobody, so its exposure is 0 whatever the default. The default would need `k = 0`, meaning no missed child ever turns chat on, which no setting achieves. Each lever shrinks exposure by a factor, and only the product reaches small numbers. They are complements, not substitutes.
3. Estimator exposure per 100 children is `100 × 0.1 × 0.9 = 9`. The gate misses 60 per 100, so `60 × k = 9` gives `k = 0.15`.
4. It leaves the age gate alone and adds a second gate on the contact itself. Open chat needs a code exchanged outside the game, so strangers rarely have one. It sharply cuts the chance that a missed child's chat partner is a stranger, which targets contact risk. It does nothing about spending or content risk.

</details>

## Lab / assignment hook

This week feeds the case-analysis portfolio (30%). Write a two-page case analysis of one real world from section 2 (Club Penguin, Toontown, Fortnite or Roblox) that states its gate, default and fallback in the lecture's model, estimates plausible values for each rate with your reasoning, and recommends one change with a computed effect. Lab 12's data audit reuses the same false-positive reasoning; see [lab 12](../labs/lab12.md).

## Sources

- Wikipedia, "Children's Online Privacy Protection Act" (accessed September 2026). Enacted 1998, effective 21 April 2000; under-13 threshold; verifiable parental consent; actual-knowledge examples; 2013 amendments on persistent identifiers, geolocation, photos, video and audio.
- UK Information Commissioner's Office, *Age appropriate design: a code of practice for online services*. The 15 standards; high privacy by default. https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/
- Wikipedia, "Age appropriate design code" (accessed September 2026). In force 2 September 2020, enforcement from 2 September 2021, applies to services likely to be accessed by under-18s; California AB 2273 (2022) preliminarily blocked by a federal district court in September 2023 on First Amendment grounds.
- Wikipedia, "Video game addiction in China" (accessed September 2026). November 2019 limits (90 minutes on weekdays, 3 hours on weekends, no play 22:00 to 08:00); September 2020 government name-based authentication; August 2021 limits.
- Wikipedia, "Shutdown law" (accessed September 2026). 30 August 2021 rule: under-18s may play one hour, 20:00 to 21:00, on Fridays, weekends and legal holidays.
- U.S. Federal Trade Commission (19 December 2022). "Fortnite Video Game Maker Epic Games to Pay More Than Half a Billion Dollars over FTC Allegations of Privacy Violations and Unwanted Charges." $275 million COPPA penalty; $245 million refunds; on-by-default voice and text; required off-by-default settings, parental consent for under-13s, neutral age gate. https://www.ftc.gov/news-events/news/press-releases/2022/12/fortnite-video-game-maker-epic-games-pay-more-half-billion-dollars-over-ftc-allegations
- Wikipedia, "Club Penguin" (accessed September 2026). Launched 24 October 2005, closed 30 March 2017; designed for ages 6 to 14; Ultimate Safe Chat and Standard Safe Chat; filter behavior; about 70 of 100 staff on moderation in May 2007.
- Wikipedia, "Toontown Online" (accessed September 2026). Launched 2 June 2003, closed 19 September 2013; SpeedChat, SpeedChat Plus, Secret/True Friends codes with parental approval for under-13s.
- Wikipedia, "Roblox" (accessed September 2026). November 2024 parental-control changes for under-13s; age checks for communication (ID or facial age estimation), with chat limited to similar age bands, from December 2025 in Australia, New Zealand and the Netherlands and globally from January 2026. Treated here as reported by that article; the lecture does not rely on any accuracy figure for Roblox's check.
- All rates in the worked example (`π`, `ℓ`, `se`, `sp`, `k_on`, `k_off`) are invented for teaching.

## Interactive spec: examples/w11-age-gate.html

**The one insight.** Exposure of children to stranger chat equals `N × π × (1 − se) × k`. The gate and the default multiply, the default is nearly free, and when children are rare even an accurate check restricts more older players than it catches children.

**Layout.** Controls on top. Two linked panels, side by side at 1280px, stacked at 390px (population bar first). A results table under both.

**Controls (keyboard operable, numeric readouts).**
- Sign-ups `N`: 10,000 to 1,000,000 (log slider), default 100,000.
- Child share `π`: 0.01 to 0.60, step 0.01, default 0.20.
- Gate: radio "Self-declared" or "Estimation". Self-declared shows lie rate `ℓ` (0 to 1, step 0.05, default 0.5) and fixes `sp = 1`, `se = 1 − ℓ`. Estimation shows `se` (0.5 to 1, step 0.01, default 0.90) and `sp` (0.5 to 1, step 0.01, default 0.95).
- Default: radio "Chat on" or "Chat off", with `k_on` (0 to 1, default 0.9) and `k_off` (0 to 1, default 0.3).
- Preset buttons: Case A (π 0.20), Case B (π 0.05), "Fortnite-style" (self-declared, off), "Estimation + off".

**Formulas.** `children = N π`; `missed = children (1 − se)`; `caught = children se`; `restricted = N (1 − π)(1 − sp)`; `passed = N (1 − π) sp`; `precision = caught / (caught + restricted)`; `exposed = missed × k`.

**Left panel, population bar.** One horizontal bar of length `N`, split into caught, missed, passed, restricted, each labeled with its count. The missed block is split into "chat on" (`missed × k`) and "chat off". Blocks use distinct fills plus hatching for the "wrong" outcomes (missed, restricted). Under the bar, a second small bar shows only the flagged-as-child group (caught + restricted) with the precision printed.

**Right panel, trade-off plot.** Horizontal axis "13+ wrongly restricted", vertical axis "children exposed", both linear from 0. Plot four points for the current `π`, `N` and rates: self-declared/on, self-declared/off, estimation/on, estimation/off, labeled. Highlight the currently selected combination. When `π` changes, points move smoothly (instantly under reduced motion).

**Results table.** All four combinations with missed, restricted, precision, exposed.

**Test values (the builder must check these).**
- Case A, self-declared `ℓ = 0.5`: missed 10,000, restricted 0, exposed 9,000 (on) / 3,000 (off).
- Case A, estimation 0.9/0.95: missed 2,000, restricted 4,000, precision 81.8%, exposed 1,800 / 600.
- Case B, self-declared: missed 2,500, exposed 2,250 / 750.
- Case B, estimation: missed 500, restricted 4,750, precision 48.6%, exposed 450 / 150.
- `N = 50,000`, `π = 0.30`, `se = 0.85`, `sp = 0.90`: missed 2,250, restricted 3,500, precision 78.5%.

**Accessibility and style.** Use `templates/interactive-tokens.css`. Blocks labeled with text and pattern, not color alone. Counts formatted with thousands separators. Respect reduced motion. No game logos, mascots or art.
