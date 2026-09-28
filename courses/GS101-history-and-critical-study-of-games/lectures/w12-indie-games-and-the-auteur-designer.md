# GS101 · Week 12 — Indie games and the auteur designer

**Why this matters:** Between 2008 and 2017 it became possible for one person to make a game, sell it worldwide and be named as its author. That changed what games could be about, and it changed how critics talk about them. This week you learn where the indie scene came from, what the "auteur" label claims and hides, and how to show that a game's argument lives in its rules by computing one.

**You will be able to:**
- Explain, with dated evidence, how digital storefronts (Xbox Live Arcade, Steam Greenlight, Steam Direct) changed who could publish a game and how many games competed for attention.
- Critique the auteur label for a named indie game by listing who else made it and what the single name leaves out.
- Compute the daily budget of Papers, Please from its published rules and show how the rules make an argument without words.
- Apply procedural rhetoric in a close reading by naming the resource, the need and the price of the moral choice.

**Before class:** Ian Bogost, *Persuasive Games: The Expressive Power of Videogames* (MIT Press, 2007), chapter 1, "Procedural Rhetoric" (about 30 pages). Tristan Donovan, *Replay: The History of Video Games* (Yellow Ant, 2010), the late pages on the independent scene. The course reader lists the pages. If you own Papers, Please or can borrow a copy, play the first five in-game days. If not, watch someone play days 1 to 3 and keep notes on every number shown on the end-of-day screen.

**Prerequisites from earlier courses:** None formally. This lecture extends the close-reading method from [GS101 week 1, section 5](w01-play-before-computers.md) and reuses its Landlord's Game example. If you are taking them alongside, [GD101 week 4, MDA](../../GD101-introduction-to-game-design/lectures/w04-mda-mechanics-dynamics-aesthetics.md) gives you the mechanics-to-feeling chain this lecture uses, and [GD101 week 9, choice and meaningful decisions](../../GD101-introduction-to-game-design/lectures/w09-choice-and-meaningful-decisions.md) explains why a choice needs a cost to matter. [MA101 week 7, piecewise functions](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md) covers the rule shape of the Papers, Please fine schedule. You need only arithmetic here.

**Interactive:** [The inspector's budget](../examples/w12-papers-please-budget.html). Keep it open during section 3.

---

## 1. How one person got to ship a game

For most of the 1990s and early 2000s, a commercial game reached players on a disc in a box on a shop shelf. A publisher paid for manufacturing, shelf space and marketing, and in return it decided what got made. Small teams existed, and some sold games by mail or as shareware, but the route to a large audience ran through a publisher.

Three changes in distribution opened a second route. You should be able to date each one.

**Console download services.** Microsoft's Xbox Live Arcade let small teams sell downloadable games on a home console. Jonathan Blow's *Braid* launched there in August 2008. Blow spent about US$200,000 of his own money over three years of development, mostly on paying the artist David Hellman and on living costs. According to Blow, it was the second-best-selling Xbox Live Arcade game of 2008, and it earned him more than a well-paid job would have in the same time. That is the story the word "indie" started to carry. A person made a personal game and sold it through a store that did not need a publisher's approval of the idea.

**Steam opens its doors.** Valve's Steam had sold other companies' games for years, but Valve chose each one. In 2012 it launched Steam Greenlight, where users voted on which submitted games Valve should accept. On 13 June 2017 Valve replaced Greenlight with Steam Direct. Under Direct, a developer fills in identity and tax forms and pays a US$100 fee per game, which Valve refunds once the game passes US$1,000 in sales. Curation before release effectively ended.

**Early access and crowdfunding.** Markus Persson's *Minecraft* was sold as an unfinished alpha from 2009 and formally released in November 2011. Microsoft announced it would buy Mojang, Minecraft's studio, for US$2.5 billion on 15 September 2014. Toby Fox funded *Undertale* on Kickstarter in 2013. The campaign asked for US$5,000 and raised US$51,124 from 2,398 backers. Players could now pay for a game before it existed, and the money came without a publisher's conditions.

### The attention squeeze, in numbers

Opening the door changed the arithmetic of being noticed. Valve's own descriptions of each era give rough weekly release rates on Steam:

| Era | Approximate new games per week | Multiple of the pre-2012 rate |
|---|---|---|
| Before Greenlight (to 2012) | 5 | 1× |
| Greenlight (2012-2017) | 70 | 14× |
| Steam Direct (from June 2017) | 180 | 36× |

By the end of 2017 Steam listed about 19,000 games, and almost 40% of them had been released during 2017 alone. That is roughly 7,600 games in one year. A 2025 estimate by the analytics firm Gamalytic found about 13,000 games released from January to October 2025. It estimated that only 8% earned over US$100,000 and that 40% earned less than US$100, the cost of the Direct fee.

Read those two facts together. The same change that let *Stardew Valley* and *Undertale* find their audiences also produced a market where the typical release earns almost nothing. If players' total hours stay roughly fixed and the number of games grows 36-fold, the average attention each game gets falls to about 1/36 of what it was. The average is misleading here, as week 11 showed for spending. A few games take most of the attention and most games get almost none.

When you read a history of "the indie revolution," check which side of this table it describes. Both sides are true.

### What "indie" means

The word has three meanings that people mix up. It can mean **financially independent** (no publisher paid for it). It can mean **small** (one to a handful of people). And it can mean an **aesthetic**: personal subject matter, retro pixel art, short length, experimental mechanics. Many games meet one meaning and not the others. *Stardew Valley* was designed and built by one person, Eric Barone, but the studio Chucklefish approached him partway through development and published it. *Hollow Knight* was made by Team Cherry, a small Australian studio, partly funded by a Kickstarter that raised over A$57,000 in 2014. Jesper Juul's book *Handmade Pixels* argues that "indie" is a vague label whose use depends on subjective judgments about authenticity. Treat it as a claim someone is making, then ask which of the three meanings they intend.

## 2. The auteur designer

### Where the idea comes from

"Auteur" is French for author. The idea comes from French film criticism of the late 1940s and 1950s. In a 1954 essay, François Truffaut attacked the French "tradition of quality," films he saw as screenwriters' literature put on camera, and praised directors whose personal vision marked everything they made. In 1962 the American critic Andrew Sarris wrote "Notes on the Auteur Theory" in the journal *Film Culture*. He is credited with coining the English term "auteur theory" and made it popular in the United States.

The theory's claim is simple. A work made by many people can still have one author whose personal stamp you can read across their whole body of work. Critics who accept it study a director's films as a set, looking for recurring themes and techniques.

### How it moved into games

Game marketing and criticism took up the idea quickly once individual developers became visible. The 2012 documentary *Indie Game: The Movie*, by James Swirsky and Lisanne Pajot, follows Edmund McMillen and Tommy Refenes making *Super Meat Boy*, Phil Fish making *Fez*, and Jonathan Blow reflecting on *Braid*. It presents each game as the expression of its maker's personality and struggles. Blow described *Braid* as a personal critique of trends in contemporary game design. Lucas Pope designed and built *Papers, Please* almost entirely alone and released it through his own company, 3909 LLC, in 2013. Richard Hofmeier drew *Cart Life* from his own experience of working low-paid jobs.

### What the label hides

The auteur label is useful because it gives you a body of work to compare. It is misleading because almost no game has one maker. Check any "solo" game's credits:

- *Braid*'s look is David Hellman's painting, paid for out of Blow's budget.
- *Undertale*'s sprites and much of its concept art came from Temmie Chang, as well as other guest artists, though Fox wrote the script and music and programmed the game.
- *Stardew Valley* had a publisher, Chucklefish, from partway through development.
- Every Kickstarter-funded game had backers whose money shaped the scope.

Film scholars made the same objection to Sarris (the critic Pauline Kael attacked the theory in her essay "Circles and Squares"). Screenwriters, cinematographers and editors shape a film as much as a director. For games, add composers, testers, platform holders and, for online games, the players themselves.

So use the auteur lens deliberately. It lets you ask, "What does this designer keep returning to?" That question is productive. It does not let you assume that every choice in the game was one person's intention. The strongest close readings do not rely on what the author meant. They rely on what the rules do, which anyone can check. The rest of this lecture shows how.

## 3. Worked example: Papers, Please's budget is an argument

### The hook

Players of *Papers, Please* (Lucas Pope, 8 August 2013) often describe the same moment. It is the end of a work day, and they must decide which family member goes without heat. The game never tells you that a state can make an ordinary worker complicit in cruelty. No character says it. Yet players come away believing the game said exactly that. Where does the argument live?

It lives in a budget you can compute. You play an immigration inspector at a border checkpoint in a fictional authoritarian country. You check entrants' documents against a growing rulebook and stamp each one approved or denied. Your pay depends on how many you process correctly. At the end of each day you pay your family's bills.

### The model, stated once

Ian Bogost named the idea in *Persuasive Games* (2007). **Procedural rhetoric** is persuasion through rules and processes rather than through words or pictures. A game makes a claim about how some system works by making you operate a model of that system. You test the claim by computing what the model forces.

For *Papers, Please*, the model is one line. For one day in the starting Class-8 apartment with all four family members alive and healthy:

```
surplus = 5 × (n − c) − P(c) − (R + H + 5 × F)
```

- `n` is the number of entrants you process in the day.
- `c` is the number of citations (mistakes) you receive. A cited entrant earns you nothing, so only `n − c` are paid.
- `5` is your pay in credits per correctly processed entrant.
- `P(c)` is the total fine for `c` citations. The first two citations each day are warnings with no fine. The third and fourth cost 5 credits each. From the fifth on, each costs 5 more than the one before: 10, 15, 20 and so on.
- `R` is rent: 20 credits at first, 25 credits from the end of day 5. Rent is mandatory. If you cannot pay it, the game ends.
- `H` is heat: 10 credits a day in this apartment. It is optional.
- `F` is the number of living family members apart from you (four at the start: wife, son, mother-in-law, uncle). Food costs 5 credits each, and it is optional.
- Medicine costs 5 credits per sick family member. Leave it out of the steady-state model and add it when someone falls ill.

A hungry or cold family member eventually falls sick, and a sick member left without medicine eventually dies. The son can go only one day without food. The uncle can go three.

The fine schedule is a piecewise function of the kind you meet in MA101 week 7. Written as the cost of the k-th citation of the day:

```
fine(k) = 0              for k = 1, 2
fine(k) = 5              for k = 3, 4
fine(k) = 5 × (k − 3)    for k ≥ 5
```

### Numbers you can check

With rent at 25, full care for the family costs `25 + 10 + 5 × 4 = 55` credits a day. Divide by 5 and you need **11 correctly processed entrants every day** to break even.

| Entrants processed `n` | Citations `c` | Pay `5(n − c)` | Fines `P(c)` | Income | Surplus after full care (55) |
|---|---|---|---|---|---|
| 8 | 0 | 40 | 0 | 40 | −15 |
| 10 | 0 | 50 | 0 | 50 | −5 |
| 11 | 0 | 55 | 0 | 55 | 0 |
| 12 | 2 | 50 | 0 | 50 | −5 |
| 14 | 2 | 60 | 0 | 60 | +5 |
| 14 | 4 | 50 | 10 | 40 | −15 |
| 16 | 4 | 60 | 10 | 50 | −5 |
| 16 | 6 | 50 | 35 | 15 | −40 |

Check two rows by hand. For `n = 14, c = 4`, you are paid for 10 entrants (50 credits). The third and fourth citations cost 5 each, so fines are 10. Income is 40, and 40 − 55 = −15. For `n = 16, c = 6`, fines are `0 + 0 + 5 + 5 + 10 + 15 = 35`, pay is 50, and the surplus is −40.

Now read the table as an argument. Processing more people is the only way to earn more, but speed produces mistakes. Mistakes cost you twice, once in lost pay and once in fines that grow through the day. A careful inspector who processes 10 people perfectly falls 5 credits short every day. The system is set so that a careful, honest worker cannot quite afford to keep his family warm and fed.

### What a shortfall buys

Suppose you end a day 15 credits short, with income 40. Rent takes 25 and leaves 15. You can heat the flat (10) and feed one person (5), leaving three hungry. Or you can feed three people (15) and leave everyone cold. The son can go one day without food, so he has to be fed. Everyone else is a choice. The game makes you choose, by ticking boxes, who suffers. That is the moment players remember, and the budget above produces it with nothing but arithmetic.

### The price of mercy

Many entrants ask you to break a rule. A woman without the right papers wants to join her husband. Letting her through earns a citation. So the moral choice has a price, and you can compute it. The marginal cost of the k-th citation is the lost 5 credits of pay plus `fine(k)`:

| Citation of the day | Lost pay | Fine | Total cost of this act of mercy |
|---|---|---|---|
| 1st | 5 | 0 | 5 |
| 2nd | 5 | 0 | 5 |
| 3rd | 5 | 5 | 10 |
| 4th | 5 | 5 | 10 |
| 5th | 5 | 10 | 15 |
| 6th | 5 | 15 | 20 |

Mercy is cheap in the morning and expensive by evening, if you have already made mistakes. Compare it with the budget. The 5 credits of your first act of mercy equal one family member's food for a day. The 6th citation's 20 credits equal food for all four. The rule set places your family's needs and a stranger's needs on the same scale, in the same currency, and asks you to trade them. You do not have to agree with the game's view of the world to see that the view is in the numbers.

### A visual you can move

Open `examples/w12-papers-please-budget.html`. The left panel is a ten-day ledger. Set entrants per day and citations per day, and watch savings rise or fall against the 55-credit care line. The right panel is the citation staircase. Each bar is the cost of one more citation, and the running total climbs with it. Drag the citation slider from 2 to 3 and watch both panels move together. Then toggle Easy mode, which adds 20 credits to your funds each day. Most of the red disappears. Keep that result in mind for the judgment section.

### Cross-game recognition

Rewrite each of the following games in the same form: **income minus the household's needs leaves a surplus, and the moral choice spends that surplus on someone outside the household.**

**The Landlord's Game (Elizabeth Magie, patented 1904).** You met it in week 1. Under the monopolist rules, rent flows to whoever owns land, so one player's surplus is everyone else's shortfall. Magie's argument about land ownership is in the rent rule, exactly as Pope's argument is in the fine schedule. Her alternative rules changed the flow of money, and so changed the argument.

**Cart Life (Richard Hofmeier, 2010).** You run a street vendor's stall and look after the vendor's food, drink and sleep. Melanie sells coffee and is a single mother seeking custody of her daughter. She struggles to find time to walk the daughter to and from school. The budget here is **time** as well as money. Every hour at the stall is income, and every hour spent with the daughter is an hour without it. The "moral choice" is spending hours, not credits, on the person the rules make expensive. Cart Life won the Seumas McNally Grand Prize at the 2013 Independent Games Festival, the same prize *Papers, Please* won in 2014.

**This War of Mine (11 bit studios, 2014).** You keep a group of civilians alive in a besieged city, inspired among other conflicts by the 1992-96 Siege of Sarajevo. By day they must stay inside, because of snipers. By night one of them scavenges. You manage hunger, health and mood until a ceasefire comes after a random number of days. When a scavenger meets other survivors, you can give them food and medicine or rob them. The structure is the same again. The household's needs eat the income, and helping outsiders comes out of the same stock.

Three games from three decades and two media, and the argument sits in the same place each time. When you read a game critically, your first move should be to find its budget. Ask what resource is scarce, what the household needs, and what a moral act costs.

### Design judgment

Procedural rhetoric is powerful, and it has costs a designer should choose on purpose.

- **Tight budgets argue, and they also teach optimization.** The table shows the game's rules are tuned near the break-even line. That tightness makes the argument. It also invites players to treat the family as a resource problem and to stop feeling anything. Letting a relative die lowers the daily cost (check-yourself question 2 below computes it). One reader sees that as the argument landing hardest. Another sees the argument collapsing into a puzzle. The rules cannot control which reading a player takes.
- **Difficulty settings change the claim.** Easy mode's 20 extra credits a day turn a −15 day into a +5 day. The same game with a different number argues something milder: that the job is hard, not that it is impossible to be both good and solvent. If you add an accessibility option to a game that argues through scarcity, you are editing the argument. Decide whether you mind.
- **Rules only persuade players who notice them.** Players who never look at the end-of-day ledger never feel the squeeze. Pope put the ledger on its own screen with checkboxes, which forces you to look. A designer who wants a rule to carry meaning must make the rule visible.
- **A single-author game makes procedural rhetoric easier to attribute, but not more true.** Knowing Pope made it does not tell you whether its model of a bureaucracy is accurate. Judge the model on its own terms.

### Check yourself (worked example)

1. On a day with rent 25, an inspector processes 13 entrants with 3 citations. What is the surplus after full care for four relatives? What can they afford if they must pay rent first?
2. The uncle has died, so `F = 3`. How many correct entrants per day are now needed to break even with full care? Explain in one sentence what the rules imply about the family.
3. Using the marginal-cost table, how much does an inspector who already has 4 citations pay for an act of mercy, measured in days of food for one family member?

<details>
<summary>Answers</summary>

1. Pay is `5 × (13 − 3) = 50`. Fines are 5 (only the 3rd citation is fined). Income 45, so the surplus is 45 − 55 = −10. After rent (25) there are 20 credits left. That covers food for all four (20) with no heat, or heat (10) plus food for two (10).
2. Full care costs `25 + 10 + 15 = 50`, so 10 correct entrants break even, one fewer than before. The rules make a death in the family a financial relief. That is part of the argument, and it is uncomfortable on purpose.
3. It is the 5th citation, which costs 5 in lost pay plus a 10-credit fine, for 15 credits. That is three days of food for one family member.

</details>

## 4. Close reading, upgraded: find the budget

In week 1 you learned a five-step method for close reading. Step 2 was "find the machine." This week gives step 2 a sharper form for games that make arguments.

1. **Name the scarce resource.** Credits, hours, food, attention, health. Often there are two, and the interesting tension is between them.
2. **Write the income rule.** How does the player get more of it, and what does getting more cost (speed, risk, mistakes)?
3. **Write the needs.** What drains it every cycle, and which drains are mandatory versus optional?
4. **Compute the margin.** Is a careful player above or below break-even? By how much?
5. **Price the moral choice.** What does the kind or principled act cost, and does that price change during play?
6. **State the claim the numbers make.** One sentence, in the form "In this game's world, X costs Y, so Z."

Then return to week 1's steps 3 to 5, placing the game in context and making a claim a reader could dispute. The auteur lens belongs in step 4 of week 1's method (context), not in step 2. Who made the game can explain why a budget looks the way it does. It cannot tell you what the budget does.

Not every indie game argues through scarcity. *Braid* argues through its time-rewind mechanic, *Undertale* through the choice to spare or kill every enemy. The method still starts the same way. Find the rule that produces the feeling, then compute or trace it before you interpret it. Week 13 takes up the debate this raises, over whether games should be read mainly as rules or mainly as stories.

## In-class activity (25 min)

In groups of three. Materials: the budget model from section 3, the interactive, and one other small game each group has played (choose from *Cart Life*, *This War of Mine*, *Frostpunk*, *Stardew Valley*, or a game the group agrees on).

1. (10 min) Fill in the six-step "find the budget" table from section 4 for your chosen game. Where you do not know a number, write the rule in words and mark it as estimated.
2. (5 min) Find the price of one moral or kind act in that game, in its own resource.
3. (5 min) Write one sentence of the form "In this game's world, X costs Y, so Z."
4. (5 min) Swap with another group. Their job is to find one player behavior that would ignore your claim entirely (for example, a player who never looks at the ledger).

Expected output: the six-row table, the claim sentence, and the other group's counter-example.

## Common misconceptions

- **"Indie means one person."** It can mean financially independent, small, or an aesthetic. *Stardew Valley* had one developer and a publisher. *Hollow Knight* had a small team and crowdfunding. Say which meaning you intend.
- **"Opening Steam helped every small developer."** It helped the ones who got noticed. Weekly releases rose from about 5 to about 180, and a 2025 estimate found 40% of new games earned under US$100.
- **"The auteur's intention decides what the game means."** Intention is evidence about context. The argument a game makes to players lives in rules they can inspect, and it can differ from what the maker intended.
- **"A game can only make an argument through its story."** *Papers, Please* makes its central argument in a budget screen of numbers and checkboxes. Remove the text and the budget still pushes the same way.

## Check yourself

1. Using the release-rate table, by what factor did weekly Steam releases grow from the Greenlight era to the Direct era? If total player attention stayed flat, what happens to the average attention per new game?
2. A friend says *Undertale* shows that one person can make a great game alone. Using facts from this lecture, write a two-sentence reply that accepts the useful part of the claim and corrects the rest.
3. Papers, Please's Easy mode adds 20 credits a day. How many correct entrants a day does a four-relative family need to break even under Easy mode, with rent 25? What does the change do to the game's argument?
4. Design a one-rule change to the fine schedule that makes mercy equally priced all day. Show the cost of the 1st and 6th citations under your rule, and say what argument the game now makes.

<details>
<summary>Answers</summary>

1. 180 / 70 ≈ 2.6 times. With flat attention, the average per new game falls to about 1/2.6, or roughly 39% of its Greenlight-era level (and to about 1/36 of the pre-Greenlight level). The distribution matters more than the average, because a few games take most of the attention.
2. Toby Fox did write, program and compose Undertale largely alone, which shows how far one person's vision can carry a game. But its sprites and much of its concept art were by Temmie Chang and guest artists, and 2,398 Kickstarter backers funded it, so "alone" overstates the case.
3. Income needed is 55 − 20 = 35 credits, so 7 correct entrants. The game now says the job is demanding but survivable for an honest worker. The claim that decency and solvency cannot both be afforded mostly disappears.
4. One option is a flat 5-credit fine for every citation from the first. Then every citation costs 5 + 5 = 10, the 1st and the 6th alike. Mercy no longer gets more expensive as the day goes on, so the game stops saying that the system punishes people who have already slipped. It becomes a steady tax on kindness rather than an escalating one.

</details>

## Lab / assignment hook

[Lab 12, a procedural-rhetoric close reading](../labs/lab12.md). You pick an indie game, build its budget table with sourced numbers, and write a 900-word close reading using the six steps from section 4. The lab is a draft of your second graded close reading (the course's two close readings are worth 40% in total).

## Sources

- Papers Please Wiki (Fandom), "Bills", "Apartment", "Citation", "Credits", "Family" and "End of day screen" pages, describing story mode in version 1.1.x of the game. Salary of 5 credits per correctly processed entrant; Class-8 rent 20 credits rising to 25 at the end of day 5; heat 10; food 5 per living relative; medicine 5 per sick relative; hunger and cold limits; fine schedule 0, 0, 5, 5, 10, 15 and so on; Easy mode adds 20 credits a day; rent mandatory, unpaid rent ends the game.
- Wikipedia, "Papers, Please". Release on 8 August 2013 for Windows and OS X by Lucas Pope (3909 LLC); 2014 IGF Seumas McNally Grand Prize; 5 million units sold by the tenth anniversary in 2023.
- Bogost, I. (2007). *Persuasive Games: The Expressive Power of Videogames*. MIT Press. Origin and definition of "procedural rhetoric" (paraphrased; see also Wikipedia, "Procedural rhetoric").
- Wikipedia, "Braid (video game)". Xbox Live Arcade release in August 2008; about US$200,000 of Blow's money over three years, mostly for artist David Hellman; Blow's statement on 2008 sales.
- Wikipedia, "Steam (service)", sections "Steam Greenlight", "Steam Direct" and store statistics. Greenlight launched in 2012; Direct launched 13 June 2017 with a US$100 fee refunded after US$1,000 in sales; roughly 5, 70 and 180 new games per week in the three eras; about 19,000 games by end of 2017 with almost 40% released that year; Gamalytic's 2025 estimate (about 13,000 releases January to October 2025, 8% over US$100,000, 40% under US$100).
- Wikipedia, "Minecraft" and "Mojang Studios". Public alpha in 2009, full release November 2011; Microsoft's US$2.5 billion purchase announced 15 September 2014.
- Wikipedia, "Undertale". Release 15 September 2015; Kickstarter June-July 2013, goal US$5,000, raised US$51,124 from 2,398 backers; art by Temmie Chang and guest artists.
- Wikipedia, "Stardew Valley" and "Hollow Knight". Barone's solo development and Chucklefish as publisher; Team Cherry's crowdfunding of over A$57,000 in 2014 and 2017 release.
- Wikipedia, "Indie Game: The Movie". 2012 documentary by James Swirsky and Lisanne Pajot; its four developers.
- Wikipedia, "Cart Life". Richard Hofmeier, 2010; three vendors including Melanie; 2013 IGF Seumas McNally Grand Prize, Nuovo Award and Excellence in Narrative.
- Wikipedia, "This War of Mine". 11 bit studios, 2014; inspired partly by the 1992-96 Siege of Sarajevo; day/night structure and choices toward other survivors.
- Wikipedia, "Auteur" and "Andrew Sarris". Truffaut's 1954 essay; Sarris's 1962 "Notes on the Auteur Theory" in *Film Culture*; Kael's "Circles and Squares".
- Wikipedia, "Independent video game development". Juul's *Handmade Pixels* on the vagueness of "indie".
- Donovan, T. (2010). *Replay: The History of Video Games*. Yellow Ant, East Sussex (xiv + 501 pp.).

## Interactive spec: examples/w12-papers-please-budget.html

**Purpose.** Make it obvious that the game's rules put an honest, careful worker just below the cost of caring for his family, and that mercy gets more expensive as the day's mistakes pile up. Insight on first load: *with the default of 10 entrants and 0 citations, the savings line slopes down, 5 credits a day, below zero, even with no mistakes at all.*

**Layout.** Two linked panels side by side on desktop, stacked on mobile (ledger on top). Controls panel below, then a numbers table. No game art, no seal, no character portraits, no Papers, Please logo or fonts. Use plain rectangles, a generic ledger style and the text "Papers, Please (Lucas Pope, 2013)" only in the caption.

**Model (exact).**
```
fine(k) = 0 if k <= 2; 5 if k <= 4; 5*(k-3) otherwise      // k = 1, 2, 3, ...
P(c)    = sum of fine(k) for k = 1..c
income  = 5*(n - c) - P(c) + (easy ? 20 : 0)
care    = R + H + 5*F      // R = 25, H = 10 (Class-8 apartment), F = family size
surplus = income - care
savings(d) = savings(d-1) + surplus,   savings(0) = S0
```
All values are integer credits. Clamp `c` to `0..n`. The model is steady state, so it uses rent 25 on every day and ignores medicine and illness (state this in a visible footnote).

**Left panel, the ledger.** Line chart of `savings(d)` for days 0 to 10. A horizontal line at 0 labelled "cannot pay rent below here" (explain that the game ends only if rent cannot be paid, and optional bills can be dropped first). Behind the line, per-day bars showing income (one color) and the care cost (a second color with a dashed outline). When a day's surplus is negative, show under that day which bills the shortfall would force you to drop, using this fixed priority: rent first (mandatory), then feed the son, then heat, then feed the others one at a time. Print the result as text, for example "day 3: no heat, uncle and mother-in-law hungry".

**Right panel, the citation staircase.** Bars for k = 1 to 10: bar height = marginal cost `5 + fine(k)`, split into "lost pay" (5) and "fine". Highlight bars 1..c for the current slider value. A running-total line of `5c + P(c)` over the bars. Label the bar for the next citation "cost of the next act of mercy: X credits = Y days of food for one person" where Y = X / 5.

**Controls.**
- Entrants processed per day `n`: slider 0 to 25, default 10.
- Citations per day `c`: slider 0 to 10, default 0 (clamped to n).
- Family size `F`: stepper 1 to 5, default 4 (5 represents the adopted niece).
- Starting savings `S0`: slider 0 to 200 credits, step 5, default 0. Label: "set to your save's value; 0 for this lecture".
- Easy mode toggle (default off): adds 20 to income.
- Preset buttons: "Careful (10, 0)", "Break-even (11, 0)", "Rushed (16, 4)", "Falling apart (16, 6)". All keyboard operable. Every change redraws both panels immediately.

**Numbers panel.** Show `income`, `care`, `surplus`, the break-even `n` for zero citations (`ceil(care / 5)` with Easy mode subtracting 20 from care first), and the lecture table rows so students can compare.

**Test values (all with R = 25, H = 10, F = 4, S0 = 0, Easy off unless noted).**
- `n=8, c=0`: income 40, surplus −15, savings(10) = −150.
- `n=10, c=0`: income 50, surplus −5.
- `n=11, c=0`: surplus 0; break-even n = 11.
- `n=14, c=2`: income 60, surplus +5.
- `n=14, c=4`: P = 10, income 40, surplus −15.
- `n=16, c=6`: P = 35, income 15, surplus −40.
- `n=13, c=3`: P = 5, income 45, surplus −10.
- `n=8, c=0`, Easy on: income 60, surplus +5; break-even n = 7.
- `F=3, c=0`: break-even n = 10.
- Staircase for k = 1..6: 5, 5, 10, 10, 15, 20; running totals 5, 10, 20, 30, 45, 65.
- Shortfall text for income 40, F = 4 (surplus −15): rent 25, son fed 5, heat 10, leaving 0, so the text reads "no food for wife, mother-in-law, uncle". Priority order is rent, son, heat, wife, mother-in-law, uncle, then any niece.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Income and cost series differ by color and by pattern (solid vs dashed). Screen-reader summary sentence updates with the numbers. Respect reduced motion (no animated transitions when it is set).
