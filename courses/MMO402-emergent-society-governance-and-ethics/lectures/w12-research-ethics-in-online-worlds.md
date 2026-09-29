# MMO402 · Week 12 — Research Ethics in Online Worlds

**Why this matters:** An MMO records everything its residents do, which makes it one of the richest research sites ever built. Studios run experiments on players every week, and academics ask for data every month. Both can harm people who never agreed to be studied, and the most common harm comes from a dataset someone called "anonymized."

**You will be able to:**
- Compute the expected share of unique records in a released dataset from its size and the number of possible combinations of its fields.
- Test a release against k-anonymity and choose generalizations (coarser fields) that make it pass.
- Apply the Belmont principles and the difference between product testing and research to a live-game experiment.
- Critique a proposed study of players, including consent, the researcher's role in the world, and data release.

**Before class:** The Belmont Report (1979), part B, "Basic Ethical Principles," and part C, "Applications" (about 20 minutes). Association of Internet Researchers, *Internet Research: Ethical Guidelines 3.0* (2019), the introduction and the section on consent. Sweeney, "k-Anonymity: A Model for Protecting Privacy," *International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems* 10(5), 2002, sections 1 to 3.

**Prerequisites from earlier courses:** [MMO305 week 13, ethnography of online worlds](../../MMO305-social-systems-and-online-behaviour/lectures/w13-ethnography-of-online-worlds.md) (fieldwork, the researcher's role, and AoIR's working rules). [UX201 week 12, surveys and interviews](../../UX201-game-ux-and-player-psychology/lectures/w12-surveys-and-interviews.md) (who answers and why). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the uniqueness formula is a complement-rule calculation). [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md). [MMO308 week 5, A/B testing design](../../MMO308-live-operations-analytics-and-experimentation/lectures/w05-ab-testing-design.md). [DB201 week 13, privacy, GDPR and data retention](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md). [MMO402 week 11, minors in online worlds](w11-minors-in-online-worlds.md) (false positives and base rates).

**Interactive:** [Unique players in an anonymized release](../examples/w12-unique-players.html).

---

## 1. Worlds as laboratories

### An accidental epidemic

On 13 September 2005, World of Warcraft added a raid boss, Hakkar the Soulflayer, whose spell Corrupted Blood drained health and jumped between nearby characters. It was meant to stay inside the raid. It escaped through hunters' pets, which players dismissed while infected and summoned again in the cities. Non-player characters in the cities carried it without dying. For several weeks, crowded capitals filled with corpses. Blizzard ended the outbreak with server resets and a patch on 8 October 2005.

Epidemiologists noticed. Ran Balicer, writing in *Epidemiology* in March 2007, compared the pets to animal carriers of avian flu and fast travel between cities to the air travel that spread SARS. Eric Lofgren and Nina Fefferman argued in *The Lancet Infectious Diseases* in September 2007 that virtual worlds could show how real people behave during an epidemic, which computer models of the time could not: some players rushed in to help, some came to watch, and some spread the disease on purpose. The Centers for Disease Control and Prevention reportedly asked Blizzard for data. There was little to give, because it had been a bug, not a study.

That story contains most of this lecture's questions. Were the players research subjects? They did not know they were being studied, and they could not have agreed. Nobody was harmed outside the game, so does it matter? And if a studio ran the same outbreak on purpose next month to collect data, what would change?

### A deliberate experiment

The answer to that last question has a real example outside games. In January 2012, Facebook changed the news feeds of 689,003 users for a week, showing some fewer positive posts and some fewer negative ones, to see whether their own posts became more negative or positive. Adam Kramer, Jamie Guillory and Jeffrey Hancock published the result in the *Proceedings of the National Academy of Sciences* in June 2014. The finding was small. The reaction was large. Users had agreed to Facebook's data use policy, but no one had agreed to have their emotions manipulated for a study, and critics argued that academics working with a company could not step around the protections that would bind them in a university.

A live MMO can run that experiment tomorrow. It already changes drop rates for one server, tests two tutorial designs, and varies matchmaking rules to see what keeps players longest. Most of that is ordinary product work. Some of it is research on people.

### When product testing becomes research

The U.S. federal rule for human-subjects research, the Common Rule (45 CFR 46, 2018 revision), binds federally funded research and, in practice, most U.S. universities. It defines research as a systematic investigation, including testing and evaluation, designed to develop or contribute to generalizable knowledge. Other countries use other rules, but most draw a similar line. That definition gives a practical line.

- A studio tests two tutorial designs to pick the better one for its own game. That is product testing. Its purpose is a decision about this game.
- The same studio, or an academic partner, runs the test to learn something about human behavior and publish it. That is research. Its purpose is knowledge that applies beyond this game.

The line matters because research on people carries duties that product testing, in most places, does not: review by an ethics board, informed consent or a justified waiver, and a plan for risks. The line is also blurry in practice. A product test that later turns out to be interesting becomes a paper. A paper written by an employee on company data may never go near a university ethics board. MMO405 week 10 covers institutional review in detail; see the [MMO405 week 10 lecture](../../MMO405-research-methods-in-online-games/lectures/w10-ethics-and-irb.md).

### The three principles

The Belmont Report, published in the U.S. Federal Register in April 1979, gives the principles that most research ethics still starts from. Written for medical and behavioral research after scandals such as the Tuskegee syphilis study, it translates well to worlds.

- **Respect for persons.** Treat people as able to make their own choices, and protect those who cannot (week 11's children). In practice: **informed consent**, meaning the person understands what will happen and agrees freely.
- **Beneficence.** Do no harm, and weigh the remaining risks against the benefits. In practice: an honest **assessment of risks and benefits**.
- **Justice.** Share the burdens and benefits of research fairly. In practice: **fair selection of subjects**. Do not study only the players who are easiest to study, or burden one group so another benefits.

Every question in this lecture is one of those three in game clothing. The next section takes on the one that game studios most often get wrong, because it looks like a solved technical problem. That is data release, which falls under beneficence: what harm can a dataset do after it leaves your hands?

## 2. Worked example: anonymized is not anonymous

### The hook

Latanya Sweeney showed in the late 1990s that about 87% of the U.S. population could be uniquely identified by three fields: five-digit ZIP code, gender and date of birth. None of the three identifies anyone. Together they usually do. In 1997 she used that fact to find the medical records of the Governor of Massachusetts in a "de-identified" hospital dataset.

Games have the same fields under other names. In 2011, Yeng-Ting Lee, Kuan-Ta Chen and colleagues published the World of Warcraft Avatar History dataset, a long record of characters on one server with their level, race, class, zone and guild over time. Researchers have used it to study play time, churn and guild life. The question for you as a designer is not about that dataset in particular. It is this: if you release rows of `class, race, level, guild`, with names removed, how many rows still point to exactly one character? Anyone can look up a character's class, race, level and guild on a public profile page, so a unique row is a named row.

Most students guess "a few percent." For a typical server the answer is over 90%.

### The model

A **quasi-identifier** is a field that does not name anyone on its own but can narrow down who a record belongs to. An **equivalence class** is the set of records that share the same values for all quasi-identifiers. A release is **k-anonymous** if every equivalence class has at least `k` records, so each person hides among at least `k − 1` others. (Pierangela Samarati and Latanya Sweeney introduced the term in 1998.)

Suppose the release has `N` records, and the quasi-identifiers can take `C` combinations in total. `C` is the product of the number of values each field can take. Assume, for a first estimate, that each record lands in a combination uniformly at random.

Fix one record. It is unique if none of the other `N − 1` records lands in its combination. Each of them misses with probability `1 − 1/C`, so by the complement reasoning of MA102 week 3:

```
P(unique) = (1 − 1/C)^(N − 1)  ≈  e^(−λ),   where λ = (N − 1) / C
```

`λ` is the expected number of *other* records in your combination. More generally, the number of others follows (approximately) a Poisson distribution with mean `λ`, so the chance that a record sits in an equivalence class smaller than `k` is

```
P(class size < k) = Σ_{j=0}^{k−2}  e^(−λ) × λ^j / j!
```

The whole model rests on one number: `λ = N / C`, records per combination. When `λ` is large, everyone has company. When `λ` drops below about 1, most records are alone.

### Numbers you can check

Take a server with `N = 10,000` characters. The fields have these numbers of possible values: class 10, race 10, level 60 (or 6 if you report it in 10-level brackets), guild 200 (or 3 if you report only the guild's size band: small, medium, large). These counts are invented, but they are the right size for a mid-sized MMO.

| Quasi-identifiers released | C | λ | Unique records | Unique share | In a class smaller than 5 |
|---|---|---|---|---|---|
| class | 10 | 999.9 | 0 | 0% | 0% |
| class, race | 100 | 99.99 | 0 | 0% | 0% |
| class, race, level | 6,000 | 1.667 | 1,889 | 18.9% | 91.2% |
| class, race, level bracket | 600 | 16.67 | 0 | about 0% | 0.01% |
| class, race, level, guild | 1,200,000 | 0.008 | 9,917 | 99.2% | about 100% |
| class, race, level bracket, guild | 120,000 | 0.083 | 9,201 | 92.0% | about 100% |
| class, race, level bracket, guild size band | 1,800 | 5.56 | 39 | 0.39% | 19.6% |

Check the third row by hand. `λ = 9,999 / 6,000 = 1.6665`, and `e^(−1.6665) = 0.1889`, so 18.9% of records are unique, about 1,889 characters. For `k = 5`, sum the Poisson terms for 0 to 3 others: `0.1889 × (1 + 1.6665 + 1.3886 + 0.7714) = 0.1889 × 4.8265 = 0.912`. So 91.2% of records sit in a class of fewer than 5, and the release fails 5-anonymity for almost everyone.

### What the table shows

**Harmless fields multiply.** Class alone and class with race are perfectly safe. Adding exact level takes the release from safe to 18.9% unique. Adding guild on top makes it 99.2% unique. No single field is dangerous. The product `C` is.

**Coarsening works, and you can compute how much.** Level brackets instead of exact levels divide `C` by 10 and take the third row from 18.9% unique to effectively zero. Guild size bands instead of guild names divide `C` by about 67. This is **generalization**, the main tool of k-anonymity: replace a value with a range or a category. The other tool is **suppression**: delete the rows or cells that remain rare.

**Even the safest useful row still fails at k = 5 for a fifth of records.** The last row has only 39 unique records, but 19.6% of records sit in classes smaller than 5. You would still suppress or generalize further, or decide `k = 5` is more than the risk needs. That is a judgment, and it belongs in the release plan with a reason.

**Real data are not uniform, and the skew cuts both ways.** In a real game, popular class and race combinations crowd together and many characters sit at the level cap. That crowding usually lowers the overall unique share below the uniform estimate. It also leaves rare combinations rarer, so the rare-class, rare-race character in a small guild is unique under almost any release, and those are often the players a study cares about. Treat the formula as a first estimate and audit the actual counts (lab 12 does both, and you will see the two disagree).

**Time makes everyone unique.** The Avatar History dataset records characters again and again, with zone and timestamp. A sequence of where a character was and when is far more distinctive than any single row. Even with coarse fields, a few snapshots usually single out a character. Trajectories need stronger protection than rows.

Open the interactive. The left view has a checklist of fields with a coarseness control for each, and plots the distribution of equivalence-class sizes for a simulated server (a histogram of how many records sit in classes of size 1, 2, 3 and so on). The right view plots unique share against `C` on a log axis, as the smooth curve `e^(−N/C)`, with a dot for the current release. Tick "guild" and watch the dot jump along the curve and the histogram pile up at size 1. Then switch guild to size bands and watch it slide back.

### Cross-game recognition

**U.S. census data (Sweeney, 1990s).** ZIP code, gender and date of birth. Rewrite it in our model: roughly 40,000 ZIP codes, 2 genders and about 36,500 possible birth dates over a century give `C` near 3 billion, and each ZIP code holds a few thousand people. `λ` for a typical person is far below 1, so most people are unique. Same formula, same result. The 87% figure is Sweeney's estimate from real data. Our model only explains why it is high.

**The Netflix Prize (2006 to 2010).** Netflix released movie ratings with user names removed for a public contest. In 2007, Arvind Narayanan and Vitaly Shmatikov showed that users could be re-identified by matching their ratings and dates with public reviews on the Internet Movie Database. In our model each rated movie is another field, and ratings with dates form a trajectory, so `C` is astronomical after a handful of movies. After a lawsuit and concerns from the Federal Trade Commission, Netflix cancelled a planned second contest in March 2010.

**AOL search logs (2006).** On 4 August 2006, AOL released about 20 million search queries from more than 650,000 users, with numbers in place of names. Within days *The New York Times* identified user 4417749 as a 62-year-old woman in Georgia from her searches alone. Search queries are free text, so they are not even quasi-identifiers you can count. They are the extreme case of a trajectory.

**Ducheneaut and colleagues' World of Warcraft census (2005).** This is the good example. The researchers ran the game's `/who` command every 5 to 15 minutes on five servers and recorded 129,372 unique characters. Their published results are aggregates such as play time per week and group sizes. Aggregates of large groups have `λ` in the thousands and carry almost no re-identification risk. The same raw data, released row by row, would have been a different ethical act.

Four contexts, one number: records per combination. When someone offers you an "anonymized" dataset, count the combinations before you count anything else.

### Design judgment

- **Release aggregates by default.** Most research questions (how long do players play, how fast do guilds dissolve) can be answered with counts and averages over large groups. Rows are for questions that need them.
- **Compute `λ` before release.** Multiply the value counts, divide into `N`, and then run the actual equivalence-class count. If `λ < 5`, expect trouble.
- **Generalize first, suppress second.** Coarsening keeps every record, with less detail. Suppression keeps detail and removes records, which biases the data toward common players. Suppressing rare characters removes exactly the unusual players researchers may want to study.
- **Treat trajectories as identifying.** Any per-character time series needs access control (a data enclave, a signed agreement, no copies) rather than a public download.
- **Know the stronger tools.** k-anonymity protects against linking by known fields. It does not protect against an attacker who learns something from the fact that a whole class shares a value. **Differential privacy**, introduced by Cynthia Dwork and colleagues in 2006, adds calibrated random noise to published statistics so that no single person's presence changes the output much. It gives a mathematical guarantee and costs accuracy. MMO405 and DB201 week 13 go further.

## 3. Consent and presence in a world

Data release is the harm you can compute. The others need judgment. Here are the ones specific to worlds.

### Terms of service are not informed consent

Every MMO player agrees to a terms of service and privacy policy that allow the studio to collect and analyze gameplay data. The Facebook case shows the limit of that agreement. Consent under Belmont requires that the person understands what will happen and agrees freely. A 40-page document accepted to reach a login screen meets neither test for an experiment that manipulates the player's experience to study them. Studios that run research partnerships should use a separate, short, specific opt-in, and should allow players to decline without losing anything in the game.

Some studies can justify a waiver of consent: the risk is minimal, the study could not be done otherwise, and the waiver does not affect players' rights. A test of which of two quest texts players read more closely might qualify. A test that raises some players' drop rates to see whether they spend more money does not, because the harm lands on the players in the worse group.

### The researcher inside the world

MMO305 week 13 introduced participant observation and AoIR's working rules: public is not the same as fair game, pseudonyms need pseudonyms, and consent scales with intimacy. Three more issues come up in governance research specifically.

- **Researchers change politics.** A researcher who joins a player council, a guild's leadership or a war alliance to study it changes decisions. Declare the role to the group, and do not vote on questions you are studying.
- **Covert research needs a strong reason.** Studying scammers, cheaters or extremist groups in a world may be impossible with full disclosure. Ethics boards can approve covert research when the value is high and no other method works, but the researcher then carries a heavy duty to protect everyone they observed.
- **Developers are powerful subjects too.** A study of how a studio moderates its world needs the studio's cooperation, and the studio can withdraw it. Publishing results the studio dislikes may end the relationship. Plan for that before you start, and put publication rights in writing.

### Vulnerable players

Some players need extra care: children (week 11), players showing signs of problem play (week 10), players in crisis who talk about it in chat, and players whose in-game identity differs from their offline one in ways that could harm them if revealed. Research designs should exclude or protect these groups on purpose, not discover them after the data are collected. The justice principle cuts both ways here. Excluding a group entirely also means the research never benefits them.

### A studio's research protocol

If you run a studio, you are the institution. Write down a protocol before the first partnership request arrives. At minimum:

1. **Purpose test.** Is this product testing or research? If research, who reviews it?
2. **Consent plan.** Opt-in, waiver with reasons, or aggregate-only data that needs neither.
3. **Harm assessment.** Who could be worse off, including players in a control group?
4. **Release plan.** Aggregates, k-anonymous rows with a stated `k`, or enclave access. Include the `λ` calculation.
5. **Debrief.** For experiments, tell the players afterwards what was done and why.
6. **Retention.** When the data are deleted, and who confirms it.

## In-class activity (25 minutes)

Groups of four. A university team asks your studio for data to study how guild membership predicts quitting. They request, per character, `class, race, exact level, guild name, zone, daily play minutes` for 90 days, on a server of 25,000 characters with 12 classes, 8 races, 70 levels, 400 guilds and 40 zones.

1. Compute `C` and `λ` for one day's snapshot of `class, race, level, guild`. Estimate the unique share with `e^(−λ)`. (6 min)
2. Propose a release that answers the research question with `λ ≥ 5` per snapshot. Say which fields you coarsen or drop and why the question survives. (8 min)
3. Decide whether 90 days of daily minutes per character can be released at all. If not, what do you offer instead? (6 min)
4. Write the consent line players would see, in one sentence. (5 min)

Expected output: a `C` and `λ` calculation, a revised field list with its `λ`, a decision on the time series, and a one-sentence consent line.

## Common misconceptions

- **"We removed the names, so it's anonymous."** Anonymity depends on how many records share each combination of the remaining fields. With class, race, level and guild on a 10,000-character server, 99% of rows are unique.
- **"The players agreed to the terms of service."** Terms of service allow data collection. They are not informed consent to an experiment designed to change players' experience for research.
- **"Public data are fair game."** Character profiles are public, which is exactly what makes a row linkable. Public availability raises the re-identification risk of anything you release alongside it.
- **"k-anonymity makes a release safe."** It blocks linking on the listed fields. It does not protect trajectories, free text, or inferences about whole classes, and it says nothing about consent.

## Check yourself

1. A release has `N = 50,000` records and `C = 200,000` combinations. Estimate the unique share. What `C` would bring the unique share below 1%?
2. On the lecture's 10,000-character server, you release `class, race, level bracket, zone` where zone has 40 values. Compute `λ` and the unique share.
3. A studio tests two loot tables, one more generous, on two servers for a month, and a designer wants to publish the retention results at a conference. Using the Common Rule definition, is this research? What should have happened before the test?
4. Why does suppressing all rows in classes smaller than 5 bias a study of rare builds? Give one alternative.

<details>
<summary>Answers</summary>

1. `λ ≈ 50,000 / 200,000 = 0.25`, unique share `e^(−0.25) ≈ 77.9%`. For under 1%, need `e^(−λ) < 0.01`, so `λ > 4.61`, meaning `C < 50,000 / 4.61 ≈ 10,850`.
2. `C = 10 × 10 × 6 × 40 = 24,000`, `λ = 9,999 / 24,000 ≈ 0.417`, unique share `e^(−0.417) ≈ 65.9%`. Zone is as identifying as exact level, and more, because it changes over time.
3. Once the purpose includes publishing generalizable findings, it meets the definition. The team should have decided that before the test, sought ethics review (through a partner university or an internal board), and considered the players on the less generous server, who bore a cost. Publishing product results after the fact is common and still raises the same questions.
4. Rare builds live in small classes, so suppression deletes them. Generalize other fields instead (coarser level, guild size band), or give the researchers enclave access to full rows under an agreement, with only aggregates leaving the enclave.

</details>

## Lab / assignment hook

[Lab 12, release audit](../labs/lab12.md). Generate a synthetic 10,000-character server with realistic skew, measure its equivalence classes, run a linkage attack against a list of public profiles, and generalize the release until it is 5-anonymous while still answering a stated research question. Deliverable: the script, a before-and-after table, and a one-page release memo.

## Sources

- Wikipedia, "Corrupted Blood incident" (accessed September 2026). World of Warcraft, 13 September to 8 October 2005; Hakkar the Soulflayer in Zul'Gurub; spread through pets and non-player characters; resets and patch; CDC request for data.
- Balicer, R. D. (2007). "Modeling infectious diseases dissemination through online role-playing games." *Epidemiology* 18(2), March 2007.
- Lofgren, E. T. & Fefferman, N. H. (2007). "The untapped potential of virtual game worlds to shed light on real world epidemics." *The Lancet Infectious Diseases* 7(9), September 2007.
- Kramer, A. D. I., Guillory, J. E. & Hancock, J. T. (2014). "Experimental evidence of massive-scale emotional contagion through social networks." *PNAS* 111(24), 8788-8790. N = 689,003. https://doi.org/10.1073/pnas.1320040111. Experiment date (January 2012) and consent criticism from Wikipedia, "Emotional contagion" (accessed September 2026).
- Wikipedia, "Belmont Report" (accessed September 2026). Published in the Federal Register on 18 April 1979; three principles and three applications; the Common Rule (1991, revised 2017).
- U.S. Code of Federal Regulations, 45 CFR 46.102(l) (Common Rule, 2018 requirements), text via Cornell Legal Information Institute, law.cornell.edu/cfr/text/45/46.102 (accessed September 2026). Research means a systematic investigation, including research development, testing and evaluation, designed to develop or contribute to generalizable knowledge.
- Association of Internet Researchers, "Ethics" (accessed September 2026). *Internet Research: Ethical Guidelines 3.0* (2019), replacing the 2002 and 2012 guidance. https://aoir.org/ethics/
- Wikipedia, "Latanya Sweeney" (accessed September 2026). The 87% finding for date of birth, gender and ZIP code; re-identification of Governor William Weld's medical records in 1997.
- Sweeney, L. (2002). "k-Anonymity: A Model for Protecting Privacy." *International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems* 10(5), 557-570. Term introduced by Samarati and Sweeney in 1998 (Wikipedia, "K-anonymity", accessed September 2026).
- Lee, Y.-T., Chen, K.-T., Cheng, Y.-M. & Lei, C.-L. (2011). "World of Warcraft Avatar History Dataset." *Proceedings of the Second Annual ACM Conference on Multimedia Systems*. https://doi.org/10.1145/1943552.1943569. Field list (level, race, class, zone, guild, timestamp) from the Kaggle mirror's description (2008 data, one server).
- Wikipedia, "Netflix Prize" (accessed September 2026). Narayanan and Shmatikov's 2007 re-identification via IMDb; December 2009 lawsuit; sequel cancelled 12 March 2010.
- Wikipedia, "AOL search log release" (accessed September 2026). 4 August 2006; about 20 million queries from more than 650,000 users; user 4417749 identified by *The New York Times*.
- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2006). "Alone Together? Exploring the Social Dynamics of Massively Multiplayer Online Games." *Proceedings of CHI 2006*. `/who` census on five World of Warcraft servers, 129,372 unique characters (as summarized in MMO305 week 13).
- Dwork, C., McSherry, F., Nissim, K. & Smith, A. (2006). "Calibrating Noise to Sensitivity in Private Data Analysis." *Theory of Cryptography Conference*.
- The server size, field value counts and the in-class request are invented for teaching.

## Interactive spec: examples/w12-unique-players.html

**The one insight.** Uniqueness depends on one number, records per combination `λ = N / C`. Adding one harmless-looking field (guild) multiplies `C` and pushes almost every record to uniqueness; coarsening a field slides it back. The histogram of class sizes and the smooth curve `e^(−λ)` show the same fact two ways.

**Layout.** Controls on the left at 1280px (on top at 390px). Two panels: class-size histogram and the uniqueness curve. Numbers readout under both.

**Controls (keyboard operable).**
- Server size `N`: 1,000 to 100,000 (log slider), default 10,000.
- Field checkboxes, each with a coarseness select:
  - class (10 values), on by default;
  - race (10 values), on;
  - level: off / exact (60) / brackets of 10 (6) / brackets of 20 (3), default exact;
  - guild: off / name (200) / size band (3), default off;
  - zone: off / 40 values, default off.
- Skew toggle: "uniform" (default) or "realistic". Realistic draws class and race from Zipf weights with exponent 1 (value `i` has weight `1/i`), level from a distribution with 40% of characters at the maximum level and the rest uniform, and guild sizes from Zipf weights with exponent 1.
- "Resample" button (new random seed; seed shown so a state can be reproduced).
- Threshold `k`: 2 to 20, default 5.

**Computation.** `C` = product of selected value counts. `λ = (N − 1) / C`. Formula unique share `(1 − 1/C)^(N − 1)`. Formula share below `k`: `Σ_{j=0}^{k−2} e^{−λ} λ^j / j!`. Simulation: draw `N` records from the selected distributions, count equivalence classes, and report the simulated unique share and share in classes smaller than `k`.

**Left panel, class-size histogram.** Horizontal axis class size 1 to 30 (last bin "30+"), vertical axis number of records. Bars for sizes below `k` in a warning fill with hatching. Label the size-1 bar with its count.

**Right panel, uniqueness curve.** Horizontal axis `C` on a log scale from 1 to 10^8, vertical axis unique share 0 to 100%. Draw `e^(−N/C)`. Place a dot for the current release (formula value) and a hollow dot for the simulated value. Label the dot with the field list.

**Readout.** `C`, `λ`, formula unique share, simulated unique share, formula and simulated share below `k`, and "passes k-anonymity: yes/no".

**Test values (uniform, formula; the builder must check these).**
- `N = 10,000`, class+race+level exact: `C = 6,000`, `λ = 1.667`, unique 18.9%, below 5: 91.2%.
- Add guild by name: `C = 1,200,000`, unique 99.2%.
- Level brackets of 10 + guild name: `C = 120,000`, unique 92.0%.
- Level brackets of 10 + guild size band: `C = 1,800`, `λ = 5.56`, unique 0.39%, below 5: 19.6%.
- Class+race+level brackets of 10+zone: `C = 24,000`, unique 65.9%.
- Simulated uniform values should fall within 2 percentage points of the formula at `N = 10,000`.

**Accessibility and style.** Use `templates/interactive-tokens.css`. Warning bars differ by hatching as well as color. Numbers selectable for copying. Respect reduced motion. No game logos or art.
