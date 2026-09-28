# MMO303 · Week 10 — Game Theory: Payoff Matrices and Nash Equilibria

**Why this matters:** When you buff a class, players do not simply play more of it. They move toward whatever beats it, and the class you meant to help can end up rarer than before. Game theory lets you predict that shift on paper instead of discovering it a week after the patch.

**You will be able to:**
- Build a payoff matrix from a class matchup chart and identify dominated classes.
- Compute the mixed-strategy Nash equilibrium of a three-class counter triangle with unequal matchups.
- Predict which class's share of the meta rises or falls after a change to one matchup.
- Critique a balance proposal by separating play rate from power.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on intransitive mechanics and payoff matrices; Sirlin, "Balancing Multiplayer Competitive Games" (GDC 2009 talk or handout), the parts on viable options and fairness.

**Prerequisites from earlier courses:** [MMO303 week 9, intransitivity and counters](w09-intransitivity-and-counters.md); [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md); the effective-HP habit of asking "which quantity do you mean?" from [MMO303 week 2](w02-armor-and-damage-mitigation.md).

**Interactive:** [Counter triangle equilibrium](../examples/w10-counter-triangle.html). Keep it open during section 2.

---

## 1. From a matchup chart to a payoff matrix

Last week you built counter relationships by hand. You drew arrows between classes and decided which one beats which. This week you learn to put numbers on those arrows and ask what a whole population of competent players will do with them.

Game theory is the mathematics of decisions where your best choice depends on what other people choose. It has a small vocabulary, and you need all of it.

- A **player** is anyone making a choice. In a duel, the two duelists.
- A **strategy** is one option a player can pick. For us, usually a class or a build.
- A **payoff** is what a player gets from a pair of choices. We will use win-rate margin.
- A **payoff matrix** is a table with your strategies as rows, your opponent's as columns, and your payoff in each cell.

### Win-rate margin as payoff

Suppose your duel data says a Knight beats a Ranger 60% of the time. The natural payoff for the Knight in that cell is not 0.60. It is how far that result sits above a coin flip, so 0.60 − 0.50 = +0.10. The Ranger's payoff in the mirror cell is −0.10. We call this the **win-rate margin**. Using margins has two advantages. A fair matchup scores 0, which makes imbalance easy to spot. And every cell has an exact mirror with the opposite sign, which makes the game **zero-sum**, meaning one player's gain is exactly the other's loss.

To keep the arithmetic readable, this lecture uses the doubled margin, `2 × (win rate − 0.5)`. A 60/40 matchup becomes +0.2 and a 70/30 matchup becomes +0.4. Doubling every cell changes no conclusion; it only removes a lot of decimals.

Our running example is a fictional MMO with three duel classes. The Knight beats the Ranger, the Ranger beats the Mage, and the Mage beats the Knight. Each favored matchup is 60/40, and mirror matches are 50/50.

| Row plays / column plays | Knight | Ranger | Mage |
|---|---|---|---|
| Knight | 0 | +0.2 | −0.2 |
| Ranger | −0.2 | 0 | +0.2 |
| Mage | +0.2 | −0.2 | 0 |

Read a row to answer the question "if I play this, what do I get against each opponent?" The table is **symmetric**, which means both players pick from the same classes and the matrix for the column player is the row player's matrix with signs flipped and rows and columns swapped. Most class-vs-class PvP tables are like this.

### Dominated strategies

A strategy is **strictly dominated** when some other strategy does better against every possible opponent choice. A player who notices this never picks the dominated option, because switching always helps.

Add a fourth class, the Bard, to our table. Playtesters love the Bard because it beats the Ranger 55/45. Here is the full matrix in doubled margins.

| Row / column | Knight | Ranger | Mage | Bard |
|---|---|---|---|---|
| Knight | 0 | +0.2 | −0.2 | +0.05 |
| Ranger | −0.2 | 0 | +0.2 | −0.1 |
| Mage | +0.2 | −0.2 | 0 | +0.25 |
| Bard | −0.05 | +0.1 | −0.25 | 0 |

Compare the Bard row with the Knight row, cell by cell. Against Knight, 0 beats −0.05. Against Ranger, +0.2 beats +0.1. Against Mage, −0.2 beats −0.25. Against Bard, +0.05 beats 0. The Knight is better in every column. So the Bard is dominated by the Knight, and a population of players who read the numbers will stop playing the Bard, even though it has a winning matchup against the Ranger.

This is the first practical use of a payoff matrix. "It has a good matchup" is not a defense of a class. Ask instead whether any other class is better against everyone. If yes, the class is dead in competitive play no matter how fun its good matchup feels. Removing dominated strategies and checking again is called **iterated elimination**; once the Bard is gone, check whether anything else has become dominated.

## 2. Worked example: buff a class and its counter rises

### The hook

Nearly every main-series Pokémon game since the originals offers a starter trio of Fire, Water and Grass types. (The *Yellow* and *Let's Go* versions are the exceptions.) Fire moves deal double damage to Grass, Grass moves deal double to Water, and Water moves deal double to Fire. The reverse matchups deal half damage. It is a perfect counter triangle with three identical edges, and anyone who has played rock-paper-scissors knows the answer for a triangle like that. If your opponent can adapt, you pick each option a third of the time.

Now change one edge. Suppose Fire's advantage over Grass got bigger than the other two advantages. Which of the three becomes more popular among players who adapt to each other?

Nearly everyone answers "Fire." The model says the answer is Water, the type that beats Fire, and that Fire's own share goes down. In MMO terms, if you buff the Knight's matchup against the Ranger, the Mage (which beats the Knight) becomes the most played class, and the Knight becomes rarer. That is the claim of this section. By the end you should be able to derive it in five lines and see it in the interactive.

### The model

Name the three classes A, B and C in counter order: A beats B, B beats C, C beats A. Let each favored matchup have its own margin.

- `a` is how strongly A beats B.
- `b` is how strongly B beats C.
- `c` is how strongly C beats A.

The payoff matrix is:

```
        A     B     C
A   [   0    +a    −c ]
B   [  −a     0    +b ]
C   [  +c    −b     0 ]
```

Now suppose the opponent population plays A, B and C with shares `pA`, `pB`, `pC` that sum to 1. Your expected payoff for each choice is the row times the shares:

```
payoff(A) =        a·pB − c·pC
payoff(B) = −a·pA        + b·pC
payoff(C) =  c·pA − b·pB
```

A **Nash equilibrium** is a set of choices where nobody can gain by switching alone. In a symmetric zero-sum game like this, the equilibrium population is one where every class earns the same expected payoff, and that payoff is 0. If any class earned more than the others, players would switch toward it, and the population would not be at rest. This "make everyone indifferent" idea is the whole trick for solving mixed equilibria, and it is worth memorizing as a method rather than a formula.

Set all three payoffs to 0 and solve:

```
a·pB = c·pC   →   pB = (c/a)·pC
a·pA = b·pC   →   pA = (b/a)·pC
```

So the equilibrium shares are proportional to `(b, c, a)`:

```
pA = b / (a + b + c)
pB = c / (a + b + c)
pC = a / (a + b + c)
```

Read that result slowly, because it is not what intuition expects. **Each class's share at equilibrium is set by the edge it is not part of.** A's share depends on how strongly B beats C. C's share depends on how strongly A beats B. When you make A's winning matchup stronger (raise `a`), the class that rises is C, the counter to A.

The reason is the indifference condition. If A's matchup against B gets better, then more people will play A unless something makes A worse. The only thing that makes A worse is more C in the population. So C's share has to rise until A is back to earning zero. Meanwhile A's raw weight `b` has not changed at all, and since the total `a + b + c` grew, A's share falls.

### Numbers you can check

Apply this to the Knight (A), Ranger (B) and Mage (C). Margins are doubled win-rate margins, so a 60/40 matchup is 0.2 and a 70/30 matchup is 0.4.

| Scenario | a: Knight beats Ranger | b: Ranger beats Mage | c: Mage beats Knight | Knight share | Ranger share | Mage share |
|---|---|---|---|---|---|---|
| Launch, all 60/40 | 0.2 | 0.2 | 0.2 | 33.3% | 33.3% | 33.3% |
| Buff Knight vs Ranger to 70/30 | 0.4 | 0.2 | 0.2 | 25.0% | 25.0% | 50.0% |
| Buff Ranger vs Mage to 70/30 | 0.2 | 0.4 | 0.2 | 50.0% | 25.0% | 25.0% |
| Nerf Mage vs Knight to 55/45 | 0.2 | 0.2 | 0.1 | 40.0% | 20.0% | 40.0% |
| Knight 65/35, Mage 55/45 | 0.3 | 0.2 | 0.1 | 33.3% | 16.7% | 50.0% |

Check the second row by hand. With shares (0.25, 0.25, 0.50):

- Knight earns `0.4 × 0.25 − 0.2 × 0.50 = 0.10 − 0.10 = 0`.
- Ranger earns `−0.4 × 0.25 + 0.2 × 0.50 = −0.10 + 0.10 = 0`.
- Mage earns `0.2 × 0.25 − 0.2 × 0.25 = 0`.

Every class breaks even, so no player gains by switching. That is the equilibrium.

Look at the fourth row too. The patch nerfed the Mage's win over the Knight. The class that lost share is the Ranger, the Mage's prey, while the Knight and Mage both went up. Balance changes ripple one step around the triangle. If you only watch the class you changed, you miss the effect.

### A visual you can move

Open `examples/w10-counter-triangle.html`. On the left, the three classes sit at the corners of a triangle, and each arrow's thickness shows the strength of that counter. On the right, bars show the equilibrium shares. Drag the Knight-vs-Ranger slider from 60% to 70%. The Knight's arrow thickens, and the bar that jumps is the Mage's. The Knight's own bar shrinks.

Then press "Run the meta." The third panel simulates a population of players who drift toward whatever is winning right now. Starting from the old one-third split, the population does not settle neatly at the new equilibrium. It circles it: Knights surge, then Mages punish them, then Rangers punish the Mages, then Knights return. The dashed line tracks the running average of each share, and that average homes in on the equilibrium numbers from the table. This is the second insight of the example. The equilibrium is where the meta averages out, not a place it necessarily sits.

### Cross-game recognition

The same indifference trick solves counter systems across many games once you write them as a triangle with weighted edges.

**Schreiber's weighted rock-paper-scissors.** Ian Schreiber's *Game Balance Concepts* course works through a variant of rock-paper-scissors in which a win with Rock is worth 2 points and other wins are worth 1. The solution he derives is Paper 50%, Rock 25%, Scissors 25%. Map it onto our model: A = Rock with `a = 2` over Scissors, B = Scissors with `b = 1` over Paper, C = Paper with `c = 1` over Rock. The formula gives shares proportional to (1, 1, 2), so Rock 25%, Scissors 25%, Paper 50%. Same answer. Making Rock's wins more valuable made Paper, Rock's counter, the most common throw. Schreiber relates this to fighting games, where moves in a counter cycle deal different amounts of damage.

**Fire Emblem's weapon triangle.** Most Fire Emblem entries use a triangle in which swords beat axes, axes beat lances and lances beat swords. The size of the advantage changes by game and by system. Some entries grant only accuracy, later entries starting with *The Binding Blade* also adjust damage, and *Three Houses* dropped the triangle. Treat each version as a weighted triangle and the model tells you which weapon type a player facing a mixed enemy force should favor. It also tells a designer that making one weapon's advantage larger will make its counter the better general-purpose pick.

**Penalty kicks in professional football.** Outside games, Ignacio Palacios-Huerta studied over 1,400 penalty kicks and found that professional kickers and goalkeepers mix their left and right choices in proportions close to the mixed Nash equilibrium, with choices that look serially independent. A penalty kick is a two-option counter game: the kicker wants a mismatch and the keeper wants a match, and kickers are more accurate to their natural side. That unequal accuracy is the same thing as our unequal edges, and the equilibrium shifts in the same indifference-driven way. This is evidence that the model describes real people who play the same game repeatedly with money on the line, and MMO duelists are that kind of population.

Three contexts, one idea. When a counter relationship gets stronger, the population responds by playing more of whatever punishes the strengthened option.

### Eyes-open design judgment

Knowing the equilibrium is useful. Treating it as the truth about your live game is a mistake. Weigh these points before you use the model on a patch.

- **Use it to predict direction, not exact shares.** Real players do not all read the matrix, class choice in an MMO is sticky because leveling and gearing a character takes weeks, and skill varies. The model is reliable about which way shares move after a change. The exact percentages are a rough guide.
- **Play rate is not power.** In the buffed-Knight row, the Knight has the best single matchup in the game and the lowest play rate. A designer who reads "Knight is 25% of duels, lowest in the game" and buffs the Knight again makes the Mage even more common. Always ask whether a class is rare because it is weak or because its counter is popular.
- **Win rate in the live game is not matchup strength either.** At equilibrium every class has an overall win rate of exactly 50%, whatever its matchups. A flat 50% across the board is what equilibrium looks like even when one edge is 90/10. You need matchup-level data to see the imbalance.
- **Large edges are fragile.** A 90/10 matchup means the loser of the class draft cannot win by playing well. Sirlin argues that a balanced game has many viable options at high-level play. A triangle with very unequal edges keeps all three options in the equilibrium on paper, but it makes individual matches feel decided at character select. My advice is to keep favored matchups between about 55/45 and 65/35 unless you want a class to be a hard counter on purpose.
- **Decide whether you want the meta to cycle.** A cycling population keeps the game fresh, and many players enjoy the churn. It also means a snapshot of play rates taken on one day can mislead you. Measure over several cycles before you act.

## 3. Nash equilibrium beyond counter triangles

The triangle is a special case. The general definition applies to any game with any number of players and any payoffs.

A **Nash equilibrium** is a combination of strategies, one per player, where no player can raise their own payoff by changing only their own strategy. It says nothing about fairness, about everyone being happy, or about the best total outcome. It only says the situation is stable against one player deviating.

There are two kinds.

- A **pure-strategy equilibrium** has each player committed to a single option.
- A **mixed-strategy equilibrium** has at least one player choosing randomly among options with set probabilities. In a population, a mixed strategy can equally be read as the share of players picking each option.

John Nash proved in 1950 that every game with a finite number of players and strategies has at least one equilibrium, if you allow mixed strategies. Rock-paper-scissors has no pure equilibrium at all, because whatever you commit to, your opponent should switch to its counter. The only equilibrium is the one-third mix.

### A non-zero-sum example: two guilds and one world boss

Many MMO situations are not zero-sum. Consider a hypothetical world boss that drops loot worth 10 points to whichever guild kills it. Two guilds arrive together. Each can **Contest** (attack the other guild to claim the kill) or **Yield** (leave and come back next spawn, which we will count as half the value).

- If both Contest, they fight, each wins the boss half the time and each pays 6 points in repair costs and lost time. Expected payoff `10 × 0.5 − 6 = −1` each.
- If one Contests and the other Yields, the contester gets 10, the yielder gets 0.
- If both Yield, they take turns and each gets 5.

| Row guild / column guild | Contest | Yield |
|---|---|---|
| Contest | −1, −1 | 10, 0 |
| Yield | 0, 10 | 5, 5 |

The first number in each cell is the row guild's payoff. There are two pure equilibria: (Contest, Yield) and (Yield, Contest). In each, the yielding guild would do worse by switching to Contest (−1 instead of 0), and the contesting guild would do worse by switching to Yield (5 instead of 10). There is also a mixed equilibrium. Use the indifference method. If the other guild contests with probability `p`, your Contest payoff is `−p + 10(1 − p)` and your Yield payoff is `5(1 − p)`. Setting them equal gives `10 − 11p = 5 − 5p`, so `p = 5/6`. Each guild contests about 83% of the time, and each expects `5 × (1/6) ≈ 0.83` points per encounter.

Notice what that means. Both guilds would be far better off always yielding (5 points each), but "always Yield" is not an equilibrium, because either guild gains by switching to Contest when it expects the other to yield. Game theorists call this structure Hawk-Dove or Chicken. For a designer, the lesson is direct. **If the equilibrium of your system is a behavior you do not want, changing the players will not work. Changing the payoffs will.** Give both guilds full credit for a shared kill and "cooperate" becomes the dominant strategy. Raise the cost of fighting and the contest probability falls. Every tagging, loot-sharing and griefing rule in an MMO is a payoff edit to a game like this one.

### Solving bigger matrices

Three classes can be solved by hand. Real games have five, ten or forty options. You have three practical tools.

1. **Remove dominated strategies first.** It shrinks the matrix and finds dead classes for free.
2. **Solve with linear programming.** A two-player zero-sum game can be solved exactly as a linear program: maximize the value `v` such that every column gives the row player at least `v`. Spreadsheet solvers handle this for a matrix of any size you will meet in this course. Lab 10 walks you through it.
3. **Simulate adaptation.** "Fictitious play" lets each simulated player best-respond to the historical average of the other's choices. The averages converge to equilibrium in two-player zero-sum games. It is slower and approximate, and it has one advantage: it shows you the path, which is what live players experience.

## 4. The meta as a population

A single duel is a two-player game. An MMO's ranked ladder is a population of thousands of players, each choosing a class and each drifting toward what seems to be working. Evolutionary game theory models that drift directly.

The simplest model is the **replicator equation**. Each class's share grows in proportion to how much better it is doing than the average:

```
d(p_i)/dt = p_i × (payoff_i − average payoff)
```

where `payoff_i` is class i's expected payoff against the current population and the average is weighted by the shares. In a symmetric zero-sum game the average payoff is always 0, so a class grows exactly when it has a positive expected payoff.

Two facts from the mathematics of this equation matter for designers. First, the interior Nash equilibrium is a rest point. If the population starts there, it stays there. Second, for a zero-sum counter triangle like ours, the population does not spiral into the equilibrium. It orbits around it on a closed loop, and the long-run average of each share equals the equilibrium share. The interactive's third panel shows exactly this.

This has consequences for live balance.

- **Play-rate swings after a patch are expected.** A change to one matchup moves the equilibrium, and a population that was at rest at the old equilibrium is now off-center and will orbit the new one. Knights surge first because they just got stronger against the current mix, and the Mage correction arrives a few weeks later.
- **Reacting to the surge makes it worse.** If you nerf the Knight during the surge, you move the equilibrium again while the population is still swinging. Designers call this chasing the meta.
- **Real populations have friction.** Players stop at a favorite class, and some never switch. Friction damps the orbits, and real metas usually settle closer to the equilibrium than the frictionless model predicts. The direction of the first swing is still a reliable forecast.

## 5. Using game theory as a balance tool

Put the pieces together into a workflow you can run on any class roster.

1. Gather matchup win rates from telemetry or simulation (week 13 builds the simulator). Use players of similar skill so that the numbers describe the classes, not the players.
2. Convert them to margins and build the payoff matrix. Check that mirror cells are opposites; if they are not, your data has a bug.
3. Remove dominated classes. Each one is a class players will abandon. Fix it before anything else.
4. Solve for the equilibrium. Every class should appear with a share you can live with. A common target is that no class falls below half its "fair" share (for five classes, below 10%) and none rises above twice it.
5. Before shipping a change, re-solve with the new numbers. Write down which class you expect to rise and which to fall. After the patch, compare against telemetry over several weeks, not several days.

Remember the limits. Duels are the cleanest case. Group content, team compositions and PvE encounters change the payoffs, because in a battleground a class's value depends on its allies as well as its enemies. MMO307 takes these ideas into PvP ladders and rating systems ([MMO307 syllabus](../../MMO307-game-balance-ii-pvp-progression-and-endgame/syllabus.md)).

## In-class activity (25 minutes)

Work in groups of three. Each group gets a printed four-class matchup table (the instructor hands out one of three versions) with win rates for every pairing.

1. Convert the table to doubled margins and check it is zero-sum. (5 min)
2. Look for dominated classes and remove them. Write one sentence explaining the dominance. (5 min)
3. If three classes remain in a cycle, compute the equilibrium shares with `p ∝ (b, c, a)`. If four remain, use the interactive's four-class mode or the Lab 10 spreadsheet. (10 min)
4. Propose one change to a single matchup that brings every class to at least 20% share. Predict which class will rise most after your change and why. (5 min)

Expected output: one card per group with the matrix, the eliminated class (if any), the equilibrium shares before and after, and the one-sentence prediction. Groups swap cards and check each other's arithmetic.

## Common misconceptions

- **"If I buff a class, more people will play it."** In a counter system, the buffed class's equilibrium share usually falls, and its counter's rises. Players may pile in for a few weeks during the first swing, then the counter catches up.
- **"The least-played class is the weakest."** Play rate reflects the whole matrix. A class can be rare because its counter is popular, as the Knight is in the buffed scenario.
- **"All classes have a 50% win rate, so the game is balanced."** At equilibrium every class breaks even overall, even with a 90/10 matchup in the table. Overall win rate hides matchup imbalance. Look at the matchups.
- **"A Nash equilibrium is the best outcome."** It is only the stable one. In the world-boss game, the equilibrium gives each guild 0.83 points when cooperation would give 5. Stability and quality are different questions.

## Check yourself

1. A triangle has Knight beats Ranger at 75/25, Ranger beats Mage at 60/40, and Mage beats Knight at 60/40. Compute the equilibrium shares. Which class is most common, and why?
2. In the launch roster (all 60/40), a designer nerfs the Ranger's matchup against the Mage to 55/45. Without computing, say which class's share falls. Then compute all three shares to check.
3. A four-class table has a class whose row is (−0.1, +0.3, −0.3, 0) against (A, B, C, itself), and class A's row against the same columns is (0, +0.35, −0.2, +0.1). Is the fourth class dominated? Show the comparison.
4. In the world-boss game, the designer lowers the cost of fighting from 6 to 2. Recompute the mixed-equilibrium contest probability and explain the change in plain words.

<details>
<summary>Answers</summary>

1. Doubled margins are `a = 0.5`, `b = 0.2`, `c = 0.2`, total 0.9. Knight `b/0.9 = 22.2%`, Ranger `c/0.9 = 22.2%`, Mage `a/0.9 = 55.6%`. The Mage is most common because it is the counter to the Knight, whose winning edge is the largest. More Mages are needed to keep the Knight at break-even.
2. The Ranger-beats-Mage edge `b` sets the Knight's share, so the Knight's share falls. With `a = 0.2`, `b = 0.1`, `c = 0.2`, total 0.5: Knight 20%, Ranger 40%, Mage 40%.
3. Compare column by column: against A, 0 > −0.1; against B, +0.35 > +0.3; against C, −0.2 > −0.3; against the fourth class, +0.1 > 0. A is better in every column, so the fourth class is strictly dominated and should vanish from the meta.
4. Both contesting now gives `10 × 0.5 − 2 = 3` each. Contest payoff `3p + 10(1 − p)`, Yield payoff `5(1 − p)`. Setting equal: `10 − 7p = 5 − 5p`, so `p = 2.5`, which is above 1. There is no mixed equilibrium any more: Contest now beats Yield whatever the other guild does (3 > 0 and 10 > 5), so Contest is dominant and both guilds always fight. Cheaper fighting turned a game of chicken into a brawl every time.

</details>

## Lab hook

**Lab 10: Solving a class meta.** You build a spreadsheet that takes a matchup win-rate table for up to five classes, removes dominated classes, solves the equilibrium with a linear-programming solver, and reports the predicted share change for a proposed patch. See [`labs/lab10.md`](../labs/lab10.md).

## Sources

- Pokémon type chart, Pokémon Database, "Pokémon type chart: strengths and weaknesses" (checked 2026; the Fire, Water and Grass relationships have been unchanged since the first generation): super effective moves deal 2× damage, not very effective moves 0.5×. https://pokemondb.net/type
- Schreiber, I. (2010). "Level 9: Intransitive Mechanics," *Game Balance Concepts* course blog. Weighted rock-paper-scissors (Rock wins worth 2) solved to Paper 50%, Rock 25%, Scissors 25%, and the fighting-game analogy. https://gamebalanceconcepts.wordpress.com/2010/09/01/level-9-intransitive-mechanics/
- Fire Emblem Wiki, "Weapon triangle." Swords beat axes, axes beat lances, lances beat swords; hit bonuses in early entries, damage modifiers from *The Binding Blade* onward, the triangle absent in *Three Houses*. https://fireemblemwiki.org/wiki/Weapon_triangle
- Palacios-Huerta, I. (2003). "Professionals Play Minimax." *Review of Economic Studies* 70(2), 395–415. Over 1,400 penalty kicks; mixing proportions consistent with the mixed equilibrium, serial independence not rejected.
- Sirlin, D. (2009). "Balancing Multiplayer Competitive Games." Game Developers Conference talk and handout; the definition of balance as many viable options at high-level play. https://www.gdcvault.com/play/1570/Balancing-Multiplayer-Competitive
- Nash, J. (1950). "Equilibrium points in n-person games." *Proceedings of the National Academy of Sciences* 36(1), 48–49.
- Hofbauer, J. & Sigmund, K. (1998). *Evolutionary Games and Population Dynamics*. Cambridge University Press. Replicator dynamics, closed orbits around the interior equilibrium in zero-sum rock-paper-scissors, time averages converging to the equilibrium.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter on intransitive mechanics and payoff matrices.

## Interactive spec: examples/w10-counter-triangle.html

**The one insight:** strengthening one counter raises the share of the class that beats the buffed class, and the buffed class's own share falls. Secondary insight: the live meta orbits the equilibrium and only its running average matches it.

**Layout.** Three panels. On mobile they stack; at 1024px and wider, panels 1 and 2 sit side by side above panel 3.

1. **Counter triangle (left).** An equilateral triangle with the three classes at the corners, drawn as generic colored circles labeled Knight (top), Ranger (bottom right), Mage (bottom left). Arrows run Knight → Ranger, Ranger → Mage, Mage → Knight. Arrow stroke width is proportional to the doubled margin of that edge (margin 0.0 = 1px, margin 0.9 = 14px). Each arrow carries its win-rate label, e.g. "70 / 30".
2. **Equilibrium shares (right).** Three horizontal bars, one per class, showing the equilibrium share in percent with one decimal. A faint ghost bar shows the share under the launch settings (all 60/40) so change is visible. Beside each bar, show the change in percentage points with a sign, e.g. "+16.7 pts".
3. **Meta over time (bottom).** A ternary (simplex) plot of population shares with the equilibrium marked as a cross. When the simulation runs, draw the population's path as a line and the running time-average as a dashed line with a dot at its current position. Under the plot, a small line chart of the three shares against time.

**Controls.**
- Slider "Knight vs Ranger win rate", 50% to 95%, step 1, default 60.
- Slider "Ranger vs Mage win rate", same range, default 60.
- Slider "Mage vs Knight win rate", same range, default 60.
- Button "Run the meta" / "Pause". Button "Reset population" returns the population to the start point.
- Select "Start population from": "Launch equilibrium (1/3 each)" (default), "Knight-heavy (50/25/25)", "Custom" (three linked number inputs normalized to sum 1).
- Toggle "Four-class mode" adds a Bard (see below).
- Every control is keyboard operable, with visible focus. Sliders update panels 1 and 2 immediately.

**Formulas.**
- Doubled margins: `a = 2·(wKR − 0.5)`, `b = 2·(wRM − 0.5)`, `c = 2·(wMK − 0.5)`, where each `w` is the slider value as a fraction.
- Equilibrium: `pK = b/(a+b+c)`, `pR = c/(a+b+c)`, `pM = a/(a+b+c)`. If `a+b+c = 0` (all sliders at 50), show 33.3% each with the note "every matchup is even; any mix is an equilibrium".
- If exactly one or two margins are 0, the formula still applies but some shares hit 0; show the note "a zero edge removes a class from the equilibrium".
- Payoff matrix `M` = [[0, a, −c], [−a, 0, b], [c, −b, 0]] with rows/columns in the order Knight, Ranger, Mage.
- Replicator: `dx_i/dt = x_i·((M x)_i − xᵀ M x)`. Integrate with fourth-order Runge-Kutta, `dt = 0.02`, 10 steps per animation frame, speed control optional. After each step clamp shares at ≥ 1e−9 and renormalize to sum 1.
- Running average: time-weighted mean of each share since the last reset.
- Show under panel 3: "Time-average: Knight x% · Ranger y% · Mage z%" with one decimal.
- Four-class mode: use the four-class matrix from section 1 of the lecture (doubled margins) with the three-class sliders controlling the K/R/M edges and the Bard row fixed at (−0.05, +0.1, −0.25, 0) against (K, R, M, B). Solve the equilibrium by simple fictitious play (20,000 iterations) or a small LP; show the Bard's share and a label "dominated by Knight" whenever every Knight cell exceeds the corresponding Bard cell. Replace the ternary plot with the line chart only in this mode.

**Test values (the builder must reproduce these).**
| wKR | wRM | wMK | Knight | Ranger | Mage |
|---|---|---|---|---|---|
| 60 | 60 | 60 | 33.3% | 33.3% | 33.3% |
| 70 | 60 | 60 | 25.0% | 25.0% | 50.0% |
| 60 | 70 | 60 | 50.0% | 25.0% | 25.0% |
| 60 | 60 | 55 | 40.0% | 20.0% | 40.0% |
| 65 | 60 | 55 | 33.3% | 16.7% | 50.0% |
| 75 | 60 | 60 | 22.2% | 22.2% | 55.6% |

- Replicator check: with sliders at 70/60/60 and start at 1/3 each, the path is a closed loop around (25, 25, 50); after at least three loops the time-average is within 1 percentage point of (25.0, 25.0, 50.0).
- Four-class check: with sliders at 60/60/60, the Bard share is 0.0% and the other three are 33.3% each.

**First screen.** Load with wKR = 70, the others 60, so the Mage bar is already visibly the longest with a "+16.7 pts" label, and the Knight bar shows "−8.3 pts". A one-line caption: "The Knight got stronger. The Mage became the most played class."

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, light and dark modes, reduced-motion disables the animated path (show the completed loop instantly instead). No game art or logos; the classes are generic shapes.
