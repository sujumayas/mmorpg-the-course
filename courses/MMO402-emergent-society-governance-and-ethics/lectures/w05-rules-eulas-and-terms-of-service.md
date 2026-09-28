# MMO402 · Week 05 — Rules, EULAs and Terms of Service

**Why this matters:** Every player of your game has agreed to a contract that almost none of them read. That contract decides who owns their items, what gets them banned and whether they can ever take you to court. Last week you saw that a permissive world is only fair if players had notice of its rules. This week you measure how much notice a click really gives, and you learn to design rules that players actually meet.

**You will be able to:**
- Compute the reading time of a game's legal documents and the share of each document a typical player covers before clicking "accept".
- Locate the clauses that matter (licence, virtual items, conduct, termination, disputes) in a real document and predict whether a typical player ever reaches them.
- Explain what the rulings in *Bragg v. Linden Research* (2007) and *MDY v. Blizzard* (2010) mean for a game's terms, and what they do not mean.
- Design a layered rule set that puts each rule where players will meet it: in code, in a just-in-time notice, in a summary, or in the full contract.

**Before class:** Obar, J. A. & Oeldorf-Hirsch, A. (2020), "The biggest lie on the Internet: ignoring the privacy policies and terms of service policies of social networking services", *Information, Communication & Society* 23(1), pp. 128-147 (read sections 1, 4 and 5). McDonald, A. M. & Cranor, L. F. (2008), "The Cost of Reading Privacy Policies", *I/S: A Journal of Law and Policy for the Information Society* 4(3), pp. 543-568 (the abstract and the method section). Skim the Riot Games Terms of Service, version of 1 December 2024, for ten minutes, and note where you stopped.

**Prerequisites from earlier courses:** [GD101 week 2, players, objectives, procedures and rules](../../GD101-introduction-to-game-design/lectures/w02-players-objectives-procedures-rules.md) (rules as a formal element of a game). [MMO304 week 11, real-money trade](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) (why terms ban selling items for money). [MMO305 week 12, community management](../../MMO305-social-systems-and-online-behaviour/lectures/w12-community-management.md) (communicating rule changes). This course: [week 1, worlds as polities](w01-worlds-as-polities.md) (Lessig's four modalities; this lecture looks inside the "law" modality) and [week 4, wars, betrayals and meta-gaming](w04-wars-betrayals-and-meta-gaming.md) (the notice test `N`). Later: [week 8, rights of avatars](w08-rights-of-avatars-koster-2000.md) and [week 9, virtual property and law](w09-virtual-property-and-law.md).

**Interactive:** [w05-reading-budget.html](../examples/w05-reading-budget.html)

---

## 1. Four layers of rules

In week 1 you sorted a world's rules by Lessig's four modalities: code, law, norms and market. This week zooms into the "law" layer, which in a game is mostly a stack of documents written by the operator. Before the numbers, get the vocabulary straight, because players and even developers mix these terms up.

- **End-user licence agreement (EULA).** A licence to use the software. It says what you may do with the client on your machine: install it, run it, not decompile it, not use cheats. Its central move is that you get a licence, not a copy you own.
- **Terms of service (ToS)**, also called terms of use. The contract for the online service: your account, your conduct, purchases, termination and how disputes are resolved. Some companies fold the EULA and the ToS into one document. Blizzard's EULA, for example, covers accounts and conduct as well as the software.
- **Code of conduct, or rules.** A shorter, plain-language list of behavior rules, usually made part of the contract by reference ("you agree to follow the rules at this address"). Old School RuneScape's numbered Code of Conduct is one. It is the document players actually quote at each other.
- **Privacy policy or privacy notice.** What data the operator collects and what it does with it. Often it is not a contract at all but a disclosure that the law requires.

Two more terms. A **clickwrap** agreement is one you accept by clicking a button or ticking a box. A **browsewrap** agreement claims you accept just by using the service. Courts in the United States usually enforce clickwraps and are more skeptical of browsewraps. And a **contract of adhesion** is a standard-form contract offered on a take-it-or-leave-it basis, with no chance to negotiate. Every game's terms are one.

Now the question. When a player clicks "accept", how much of the contract have they met?

## 2. Worked example: the 51-second contract

### The hook

In a study published in 2018, Jonathan Obar and Anne Oeldorf-Hirsch invited 543 people to join a new social network called NameDrop. NameDrop did not exist; the researchers built the sign-up flow for the study. Its terms of service included two clauses they called "gotcha clauses". One said users' data would be shared with the NSA and with employers. The other said that users would give up their first-born child as payment for access.

Participants spent an average of 51 seconds on the terms of service. At an average adult reading speed of 250 to 280 words per minute, the authors estimated the document needed 15 to 17 minutes. Ninety-three percent agreed to it, and 98% missed the gotcha clauses.

NameDrop was a fake network with a short ToS. Game terms are longer. So what does 51 seconds buy in a real game's contract?

### The model

Three quantities describe a player's contact with a document.

```
required time      T  = W / R
words covered      w  = t × R
coverage           c  = min(1, w / W)
a clause at word x is reached if x ≤ w
```

- `W` is the document's length in words.
- `R` is reading speed in words per minute. Use 250, the figure both McDonald and Cranor (2008) and Obar and Oeldorf-Hirsch used as a typical adult rate.
- `t` is the time the player actually spends, in minutes. Use 51 seconds (0.85 minutes) from the NameDrop study.
- `x` is the position of a clause, counted in words from the start of the document.

The last line is the one designers forget. A reader who skims from the top covers the first `w` words and nothing else. Whether a clause is "in the contract" and whether it is ever read are different questions, and the second one depends on where you put it.

### Numbers you can check

We measured four current documents in September 2026 by extracting the page text and counting words. Page navigation adds a few dozen words, so treat the counts as accurate to about 1%. Your own counts in the lab should land within that range.

| Document (version) | Words `W` | `T` at 250 wpm | Coverage in 51 s if read on its own (`w ≈ 212`) |
|---|---|---|---|
| Blizzard End User License Agreement (last revised 21 March 2024) | about 10,250 | 41 min | 2.1% |
| Blizzard Online Privacy Policy (last updated 27 June 2025) | about 8,200 | 33 min | 2.6% |
| Riot Games Terms of Service (last modified 1 December 2024) | about 12,800 | 51 min | 1.7% |
| Riot Games Privacy Notice (last modified 28 April 2026) | about 9,300 | 37 min | 2.3% |

Check a row by hand. For the Riot ToS, `T = 12,800 / 250 = 51.2` minutes. A 51-second reader covers `0.85 × 250 = 212.5` words, which is `212.5 / 12,800 = 1.7%` of it.

The last column assumes the player spends the whole 51 seconds on that one document. A player who meets the terms and then the privacy document in sequence, in 51 seconds total, never starts the second one, so its coverage in stack order is 0%. The interactive shows both columns.

A new League of Legends player who meets both Riot documents faces about 22,100 words, or 88 minutes of reading. A new Blizzard player faces about 18,450 words, or 74 minutes. Scale that up. One million new accounts reading the Blizzard pair in full would spend `1,000,000 × 74 / 60 ≈ 1.23 million` hours. McDonald and Cranor made the same kind of estimate for privacy policies across the whole web. At about 10 minutes per policy, they put the national cost of reading them in the United States on the order of US$781 billion a year in time.

Now find where the clauses sit. The positions below are word counts from the start of each document, measured the same way.

| Clause | Riot ToS: position (share through) | Blizzard EULA: position (share through) | Reached in 51 s? |
|---|---|---|---|
| Notice that disputes go to binding arbitration with a class-action waiver | about 137 (1%), a pointer to section 16 | about 27 (0.3%), in capital letters | Yes, in both |
| You get a licence to virtual items, not ownership | about 170 (1%) | about 6,100 (60%), in the list of things Blizzard owns | Riot yes, Blizzard no |
| What happens when your account is terminated | about 1,410 (11%) | about 1,410 (14%), on fees and termination of game licences | No |
| Ban on cheats and bots | about 4,140 (32%), alongside the ban on scamming other players | about 2,440 (24%) | No |
| How to opt out of arbitration (Riot: 30 days after accepting) | about 10,830 (85%) | — | No |

The 51-second reader of Riot's terms learns that arbitration exists and that they do not own their skins. They never reach the part that says they can opt out of arbitration within 30 days. Riot's 85% position for that clause and its 1% position for the pointer are both deliberate choices.

### The visual

Open the interactive. The left view, "What you agreed to", draws each document as a long horizontal bar scaled to its word count, stacked by game, with a tick for each clause in the table. The right view, "What you read", zooms into the part of the stack your reading time covers. Drag the reading-time slider from 51 seconds up to 90 minutes and watch the shaded region crawl along the left bars. At 51 seconds it is a sliver. Then switch on "move clause to top" for any clause, and watch it jump into the right view without the reading time changing. Coverage is set by the reader. Reach is set by the writer.

### The insight

Clicking "accept" is a legal act, and courts usually treat it as consent. As a description of what players know, it is a fiction. A typical player meets 1% to 3% of the text, and which 1% to 3% is up to you. The ethical and practical question for a designer is not "is the clause in the contract?" but "will the player meet this rule before it matters to them?"

That is week 4's notice test, `N`, made measurable. A permissive world that allows scams, or a strict one that bans selling items, is only fair to players who meet that rule. Burying it at word 4,000 meets almost nobody.

### Cross-game and cross-context recognition

**NameDrop (research study, 2018).** The same model: `W` short enough to need 15 to 17 minutes, `t = 51` seconds, and the gotcha clauses placed beyond `w`. 98% missed them.

**Privacy policies on the web (McDonald and Cranor, 2008).** The model run at the scale of a society. They used 250 words per minute and a lower bound of 119 sites visited per person per year, and found the cost of reading was larger than the online advertising market the policies served.

**Riot Games (current terms).** A deliberate attempt to move key clauses to the front. The document opens with a short list of items it asks readers to pay particular attention to. The list points to arbitration, states that virtual content is licensed, not owned, and flags the refund policy and the user rules. Each section heading is a plain question followed by a one-line answer in parentheses. For example, the answer to "What happens if Riot terminates my account?" begins "(No games for you...". A skimming reader who reads only headings and their answers covers far more rules per second than one who reads from the top.

**Blizzard (current EULA).** The dispute notice is at the very top in capital letters, which is where courts expect it. The ownership of virtual goods sits in a long list more than halfway through. The document is legally careful, and a skimmer will not meet its item rules.

**EVE Online (week 4).** CCP's statement that most scams are allowed does its work only if players meet it. Protected starter systems are EVE's way of buying time until they do. That is a rule placed in code and geography rather than text.

## 3. What courts have said

This course does not teach law, and nothing here is legal advice. But two cases show what game terms can and cannot do, and designers should know both.

### *Bragg v. Linden Research, Inc.* (E.D. Pa., 2007)

Linden Lab closed the Second Life account of Marc Bragg after he bought virtual land below market price by exploiting its auctions. His virtual assets, which he valued at US$4,000 to 6,000, were removed with the account. He sued, and Linden Lab asked the court to send the case to arbitration, as its terms required.

Judge Eduardo Robreno refused. The terms were a contract of adhesion offered take-it-or-leave-it, and he found the arbitration clause unconscionable. One reason was that Second Life, unlike its competitors, told users they held property rights in virtual land. So a user had no real market alternative for what Second Life offered. The parties later settled, and Bragg's account was restored.

Two lessons follow. What you promise in marketing ("you own your land") can undercut what your contract says. And Bragg turned out to be an outlier. Later courts have usually enforced online terms, including arbitration clauses, when users had a fair chance to read them and a clear accept-or-reject step. That is exactly why Blizzard and Riot put their arbitration notices in the first 150 words.

### *MDY Industries v. Blizzard Entertainment* (9th Cir., 2010)

MDY sold Glider, a bot that played World of Warcraft unattended. Blizzard's terms banned bots. Blizzard argued that a player running Glider broke the licence, so every copy of the game in memory was an infringing copy, which made MDY liable for copyright infringement.

The Ninth Circuit disagreed on that point. Breaking a term of a licence is copyright infringement only when the term is connected to the rights copyright protects, such as copying and distribution. A ban on bots is a promise about how you play, so breaking it is a breach of contract, not infringement. MDY still lost on other grounds. The court held that Glider was built to get around Warden, Blizzard's anti-cheat program, and that trafficking in such a tool violated the Digital Millennium Copyright Act.

The lesson for designers is that the contract alone is a weak weapon against cheats. The strong enforcement came from code (Warden), and the law protected the code. That is Lessig's modalities working together.

## 4. Designing rules players meet

Put the model to work. For every rule, ask when it matters to the player and where they will be at that moment. Then place the rule there.

### Four places a rule can live

1. **In code.** The rule cannot be broken, so nobody needs to read it. A trade window that shows both sides and needs both confirmations does more against scams than any clause. The cost is rigidity and engineering time, and some rules cannot be coded ("don't harass other players").
2. **At the moment of action.** A just-in-time notice appears when the rule becomes relevant. Examples include "This contract's price is 40% above the market average", "You are leaving protected space; other players can attack you here", or "Selling gold outside the game breaks our terms and can close your account". It covers very few words, but every word is read at the right moment.
3. **In a short summary.** A code of conduct, or a short list of key points at the top of the contract. It is short enough to be read and quoted in community spaces, and players enforce norms with it.
4. **In the full contract.** Everything a court needs. It is complete and precise, and read by almost no one.

A good rule set uses all four and keeps them consistent. Each rule should appear in the cheapest place that reaches the players it affects before it affects them.

### The ethical floor

Three commitments follow from this week's numbers. They are a floor, not a ceiling.

- **Nothing that surprises a reasonable player lives only in the full contract.** If a clause would make a player say "I never agreed to that", move it up a layer or delete it.
- **Changes need notice in proportion to their effect.** Terms change after launch, and a player who read version 1 has not read version 7. Tell players what changed in plain words, in the client, before it applies.
- **Enforcement follows the published rules.** If support staff act on an unpublished rule, the contract has stopped describing the world. Week 7 looks at how appeals catch this.

## In-class activity (25 minutes)

Pairs. Each pair gets one current game document (the instructor assigns Blizzard, Riot, Jagex, CCP, Roblox or Valve so that every document is covered twice).

1. Paste the document into the word counter from lab 05 (or count one page and multiply). Record `W` and the version date (5 minutes).
2. Find four clauses: licence or ownership of items, the ban on cheating, termination, and dispute resolution. Record each clause's position `x` as a share of the document (10 minutes).
3. Pick the clause that most deserves to move. Write the just-in-time notice that would replace it: at most 25 words, and name the exact screen where it appears (10 minutes).

Expected output: `W`, four positions, one 25-word notice with its screen. The two pairs with the same document compare positions at the end; they should agree within 2%.

## Common misconceptions

- **"If it's in the terms, the player agreed to it, so it's fair."** It is usually enforceable, which is a legal question. Whether it is fair depends on whether a reasonable player met it before it mattered, which is the design question.
- **"Shorter terms fix the problem."** Halving `W` from 12,800 to 6,400 words raises 51-second coverage from 1.7% to 3.3%. Position and layering matter far more than length.
- **"Breaking the ToS is illegal."** Usually it is a breach of contract. The operator can close your account, but *MDY v. Blizzard* shows that a breached term does not automatically become a copyright violation.
- **"The EULA and the ToS are the same thing."** They often overlap, and some companies merge them. The EULA licenses software; the ToS governs the service and your account.

## Check yourself

1. A game's terms are 15,000 words. At 250 words per minute, how long do they take to read? What share does a 51-second reader cover? How many words must the reader cover to reach a clause placed 60% of the way through?
2. Your terms state that items are licensed, not owned, at word 7,500 of 10,000. You can either cut the document to 5,000 words, keeping the clause's relative position, or move that one clause to word 100. Which choice makes a 51-second reader meet the clause? Show the numbers.
3. A studio ships 400,000 new accounts in launch week. Its legal stack is 20,000 words. How many hours of reading does full reading require across those players? Why is the answer an argument for layering rather than for a longer summary?
4. A designer says, "*Bragg* shows arbitration clauses in game terms are unenforceable." What does the case actually show, and what happened in later cases?
5. Using week 4's four tests, explain why a sandbox that allows scams needs its scam rule at layers 2 or 3, not only in the full contract.

<details>
<summary>Answers</summary>

1. `T = 15,000 / 250 = 60` minutes. Coverage `212.5 / 15,000 ≈ 1.4%`. The clause sits at word 9,000, so the reader needs 9,000 words, which takes 36 minutes.
2. Cutting the document puts the clause at word 3,750, far past 212, so it is still missed. Moving the clause to word 100 means `100 ≤ 212.5`, so it is reached. Position wins.
3. Each player needs `20,000 / 250 = 80` minutes. `400,000 × 80 / 60 ≈ 533,000` hours. No player will spend 80 minutes, so the real choice is which 200 words each player meets. A longer summary still has to fit that budget. Just-in-time notices spend the budget at the moment each rule matters.
4. In *Bragg* (2007), a federal district court found Second Life's arbitration clause unconscionable, partly because the terms were take-it-or-leave-it and Second Life promised unique property rights, leaving no market alternative. The case was an outlier. Later courts have usually enforced online terms, arbitration included, when users had a fair chance to read them and a clear accept step.
5. The scam rule is what makes a victim's loss fair under `N`. A rule met by 2% of readers gives notice to almost nobody. It must appear where players act (warnings on contracts and trades) or in a short code everyone meets (layer 3), or `N` fails for most victims.

</details>

## Lab / assignment hook

[Lab 05, terms-of-service audit](../labs/lab05.md). You measure one game's full legal stack, locate its key clauses, score how much a 51-second reader meets, and redesign it as a four-layer rule set with at least three just-in-time notices. It counts toward the case analyses (30%).

## Sources

- Obar, J. A. & Oeldorf-Hirsch, A. (2020). "The biggest lie on the Internet: ignoring the privacy policies and terms of service policies of social networking services." *Information, Communication & Society* 23(1), 128-147 (online 2018). doi:10.1080/1369118X.2018.1486870. N = 543; fictitious network NameDrop; 250-280 words per minute; ToS estimated at 15-17 minutes, read for 51 seconds on average; 93% agreed to the ToS; 98% missed the gotcha clauses (NSA and employer data sharing, first-born child).
- McDonald, A. M. & Cranor, L. F. (2008). "The Cost of Reading Privacy Policies." *I/S: A Journal of Law and Policy for the Information Society* 4(3). Author's pre-press version, lorrie.cranor.org. 250 words per minute; about 10 minutes per policy for the 75 most popular sites; a lower bound of 119 unique sites per user per year; national opportunity cost on the order of US$781 billion.
- Blizzard Entertainment, End User License Agreement, last revised 21 March 2024 (accessed and counted September 2026). Arbitration and class-action notice at the top; licence grant; cheating ban; list of Blizzard-owned components including virtual goods.
- Blizzard Entertainment, Online Privacy Policy, last updated 27 June 2025 (accessed and counted September 2026).
- Riot Games, Terms of Service, last modified 1 December 2024 (accessed and counted September 2026). Opening list of items to pay particular attention to, with a pointer to the arbitration clause and class-action waiver in section 16; virtual content licensed, not owned; question-and-answer headings; ban on scamming and social engineering and on cheats and bots; 30-day arbitration opt-out in section 16.20.
- Riot Games, Privacy Notice, last modified 28 April 2026 (accessed and counted September 2026).
- *Bragg v. Linden Research, Inc.*, 487 F. Supp. 2d 593 (E.D. Pa. 2007), as summarized in Wikipedia, "Bragg v. Linden Research, Inc." (accessed September 2026). Account closed after an auction exploit; assets claimed at US$4,000-6,000; arbitration clause held unconscionable; later settlement; an outlier in later case law.
- *MDY Industries, LLC v. Blizzard Entertainment, Inc.*, 629 F.3d 928 (9th Cir. 2010), as summarized in Wikipedia, "MDY Industries, LLC v. Blizzard Entertainment, Inc." (accessed September 2026). Glider bot; the required connection between a licence term and copyright; DMCA liability for circumventing Warden.
- Old School RuneScape Wiki, "Scams" (accessed September 2026). The numbered Code of Conduct (Rule 2 on scamming).
- Lessig, L. (2006). *Code: Version 2.0*. Basic Books. Chapter 7.

## Interactive spec: examples/w05-reading-budget.html

**The one insight:** a typical player covers only the first couple of hundred words of any legal document, so whether a rule is met depends on where the writer puts it, not on whether it is "in the contract". Moving one clause changes what the player meets far more than any realistic change in reading time.

**Layout.** Two linked views, side by side on desktop and stacked on mobile ("What you agreed to" first). Controls above them.

- **Controls.** Reading time `t`: slider from 10 seconds to 90 minutes on a log scale, default 51 s, with a marker at 51 s labelled "NameDrop average". Reading speed `R`: 150 to 400 wpm, default 250. Game selector: "Riot (ToS + Privacy Notice)", "Blizzard (EULA + Privacy Policy)", "Both". A checkbox list of clauses, each with a "move to top" toggle.
- **Left view, "What you agreed to".** One horizontal bar per document, length proportional to `W` (a shared scale, so Riot's ToS bar is 12,800 / 10,250 times Blizzard's EULA bar). Clause ticks at their positions, each labelled with a short name. A shaded region from word 0 to `w = t × R` on the first document of the selected game, continuing into the next document if `w` exceeds the first document's length (the reader reads the stack in order).
- **Right view, "What you read".** A zoom of words 0 to `max(w, 300)` of the stack, with the same clause ticks, and a list "Clauses you met" and "Clauses you missed".
- **Readout table** (copyable). For each document: `W`, `T = W / R` in minutes (one decimal), coverage if read alone `min(1, w/W)` (the lecture table's column) and coverage in stack order (formula below), both as a percent with one decimal. Totals for the selected game.

**Data.**

| doc | W | clauses (name: position x) |
|---|---|---|
| Riot ToS (1 Dec 2024) | 12,800 | Arbitration pointer: 137; Virtual items licensed: 170; Termination: 1,410; Scams, cheats and bots: 4,140; Arbitration opt-out: 10,830 |
| Riot Privacy Notice (28 Apr 2026) | 9,300 | none |
| Blizzard EULA (21 Mar 2024) | 10,250 | Arbitration notice: 27; Termination and fees: 1,410; Cheating ban: 2,440; Virtual goods owned by Blizzard: 6,100 |
| Blizzard Privacy Policy (27 Jun 2025) | 8,200 | none |

"Move to top" sets that clause's `x` to 50 and shifts nothing else (the model treats the clause as a short insert).

**Formulas.**

```
w = t_minutes × R
T_doc = W_doc / R
coverage_alone_doc = min(1, w / W_doc)                 // the lecture table's column
coverage_stack_doc = clamp((w − start_doc) / W_doc, 0, 1)   // start_doc = words in earlier docs of the stack
met(clause) = start_doc + x ≤ w
```

**Test values.**

- `t` = 51 s, `R` = 250: `w` = 212.5. Riot ToS `T` = 51.2 min, coverage 1.7%. Blizzard EULA `T` = 41.0 min, coverage 2.1%. Privacy documents: alone 2.3% (Riot) and 2.6% (Blizzard), in stack order 0%. Riot met: arbitration pointer, virtual items licensed. Blizzard met: arbitration notice.
- `t` = 51 s, "move to top" on Blizzard "Virtual goods owned by Blizzard": now met.
- `t` = 20 min, `R` = 250: `w` = 5,000. Riot met adds termination and scams, cheats and bots; opt-out still missed. Blizzard met adds termination, cheating ban; virtual goods (6,100) still missed.
- `t` = 88.4 min, `R` = 250, Riot: `w` = 22,100 = the whole stack, coverage 100% on both documents.

**Accessibility.** Sliders keyboard-operable with visible focus and text values; clause ticks have text labels, not colour alone; the met/missed lists are real lists read by screen readers; `prefers-reduced-motion` disables the shading animation. No company logos.
