# MMO303 · Week 10 — Game Theory: Payoff Matrices and Nash Equilibria

**Why this matters:** Players do what pays. When your system pays for behavior you do not want, such as two guilds fighting over one boss, asking players to behave does nothing. Game theory tells you which behavior your payoffs make stable, and which single number to change to get a different one.

**You will be able to:**
- Build a payoff matrix from a matchup chart or a shared-content situation, and identify dominated strategies.
- Find the pure and mixed Nash equilibria of a two-player game with the indifference method.
- Compute how a change to one payoff, such as a fight cost or a loot rule, moves the equilibrium.
- Critique a balance or reward proposal by separating what is stable from what is good for players.

**Before class:** Schreiber & Romero, *Game Balance* (2021), chapter 25 (Intransitive Mechanics and Payoff Matrices); Schreiber, "Level 9: Intransitive Mechanics" (*Game Balance Concepts*, 2010), the sections on solving payoff matrices.

**Prerequisites from earlier courses:** [MMO303 week 9, intransitivity and counters](w09-intransitivity-and-counters.md) (margins, the stable mix and population drift); [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md); the habit of asking "which quantity do you mean?" from [MMO303 week 2](w02-armor-and-damage-mitigation.md).

**Interactive:** [World boss game](../examples/w10-world-boss-game.html). Keep it open during section 2.

---

## 1. From a matchup chart to a payoff matrix

Last week you found the stable mix of a counter triangle by setting every class's expected margin to zero. That was game theory without the name. This week gives it the name, the vocabulary and a method that works on any table of payoffs, including games where both sides can lose.

Game theory is the mathematics of decisions where your best choice depends on what other people choose. Its vocabulary is small.

- A **player** is anyone making a choice. In a duel, the two duelists. At a world boss, the two guilds.
- A **strategy** is one option a player can pick. For us, usually a class, a build or a behavior.
- A **payoff** is what a player gets from a pair of choices.
- A **payoff matrix** is a table with your strategies as rows, your opponent's as columns, and your payoff in each cell.

### Margins as payoffs

For class matchups, the payoff is week 9's margin, `2w − 1`, where `w` is the row class's win rate against the column class. A 60/40 matchup is +0.2 for the winner and −0.2 for the loser. A fair matchup scores 0. Every cell has a mirror with the opposite sign, which makes the game **zero-sum**, meaning one player's gain is exactly the other's loss.

Here is week 9's launch arena, every favored matchup at 60/40.

| Row plays / column plays | Knight | Ranger | Mage |
|---|---|---|---|
| Knight | 0 | +0.2 | −0.2 |
| Ranger | −0.2 | 0 | +0.2 |
| Mage | +0.2 | −0.2 | 0 |

Read a row to answer "if I play this, what do I get against each opponent?" The table is **symmetric**. Both players pick from the same classes, and the column player's matrix is the row player's with signs flipped and rows and columns swapped. Most class-against-class PvP tables are like this.

### Week 9's stable mix is a Nash equilibrium

A **Nash equilibrium** is a set of choices, one per player, where no player can gain by changing only their own choice. When the choice is a probability mix over options, it is a **mixed-strategy** equilibrium. In a population, read the mix as the share of players on each option.

Week 9 already solved one. With `a` = Knight over Ranger, `b` = Mage over Knight and `c` = Ranger over Mage, all as margins, and `S = a + b + c`, the stable mix is Knight `c / S`, Mage `a / S`, Ranger `b / S`. At that mix every class earns an expected margin of 0, so no player gains by switching class. That is the definition of a Nash equilibrium. Week 9's result that a Knight buff to 70/30 moves the mix to 25% Knight, 50% Mage, 25% Ranger is a statement about how the equilibrium moves when one payoff changes.

The method week 9 used has a name, the **indifference method**. In a mixed equilibrium, every option a player uses must pay the same, or they would drop the worse one. So you write "every used option pays the same" as equations and solve. This lecture applies that method to a game that is not a triangle and not zero-sum.

### Dominated strategies

Before solving anything, remove options nobody should pick. A strategy is **strictly dominated** when some other strategy does better against every possible opponent choice. A player who notices this never picks the dominated option, because switching always helps.

Add a fourth class, the Bard, to the arena. Playtesters love the Bard because it beats the Ranger 55/45. Here is the full matrix in margins.

| Row / column | Knight | Ranger | Mage | Bard |
|---|---|---|---|---|
| Knight | 0 | +0.2 | −0.2 | +0.05 |
| Ranger | −0.2 | 0 | +0.2 | −0.1 |
| Mage | +0.2 | −0.2 | 0 | +0.25 |
| Bard | −0.05 | +0.1 | −0.25 | 0 |

Compare the Bard row with the Knight row, cell by cell. Against Knight, 0 beats −0.05. Against Ranger, +0.2 beats +0.1. Against Mage, −0.2 beats −0.25. Against Bard, +0.05 beats 0. The Knight is better in every column. So the Bard is dominated by the Knight, and players who read the numbers will stop playing the Bard, even though it has a winning matchup against the Ranger.

"It has a good matchup" is not a defense of a class. Ask instead whether any other class is better against everyone. If yes, the class is dead in competitive play no matter how fun its good matchup feels. Removing dominated strategies and checking again is called **iterated elimination**. Once the Bard is gone, check whether anything else has become dominated.

## 2. Worked example: two guilds, one world boss

### The hook

In classic World of Warcraft, a creature's loot belongs to whoever **tapped** it, and the tap goes to the group of the first player to damage it. For a world boss, that is one raid of up to 40 players. A second raid that arrives at the same time and helps kill the boss gets nothing. So two guilds at the same spawn have a reason to fight each other before they fight the boss.

In patch 5.1.0 (Mists of Pandaria, 2012), Blizzard made that era's world bosses **tap-to-faction**: every player of the tapping faction who takes part is eligible for loot. In patch 7.0.3 (2016) it went further, and every creature in the game became tappable by up to five other characters.

Blizzard did not ask players to be nicer. It changed who gets paid. Why did that work, and what would a smaller change have done?

### The model

Two guilds reach the boss together. Each chooses one of two strategies.

- **Contest:** attack the other guild to secure the tap.
- **Yield:** leave and come back next spawn.

Three numbers set the payoffs.

- `V` is the value of the boss's loot to one guild.
- `C` is what a guild-against-guild fight costs each side, in repairs, time and lost players.
- If both yield, they take turns across spawns, which is worth `V / 2` each per spawn.

If both contest, each wins the fight half the time and both pay the cost, so each expects `V / 2 − C`. If one contests and the other yields, the contester gets `V` and the yielder gets 0. The first number in each cell is the row guild's payoff.

| Row guild / column guild | Contest | Yield |
|---|---|---|
| Contest | `V/2 − C`, `V/2 − C` | `V`, 0 |
| Yield | 0, `V` | `V/2`, `V/2` |

This is not zero-sum. Both guilds can lose at once (the fight), and both can do well at once (taking turns).

Look first for **pure** equilibria, cells where neither guild gains by switching alone. (Yield, Yield) is not one, because a guild that expects the other to yield gains by contesting, `V` instead of `V/2`. When the fight costs more than half the loot (`C > V/2`), (Contest, Contest) is not one either, because each guild would rather yield and take 0 than fight for a negative payoff. That leaves (Contest, Yield) and (Yield, Contest). In each, the yielder would get `V/2 − C < 0` by switching, and the contester would drop from `V` to `V/2`. Two pure equilibria, and each needs the guilds to agree in advance which one backs down.

Then find the **mixed** equilibrium with the indifference method. Suppose the other guild contests with probability `p`. Your two options pay:

```
Contest:  p × (V/2 − C) + (1 − p) × V
Yield:    p × 0         + (1 − p) × V/2
```

In a mixed equilibrium you must be indifferent, so set them equal. The `V/2` terms cancel and you get

```
p × (V/2 − C) + (1 − p) × V/2 = 0
p* = V / (2C)                         when C > V/2
payoff at equilibrium = (1 − p*) × V/2
```

If `C ≤ V/2`, the fight is cheap. Contest pays at least as much as Yield whatever the other guild does, so Contest is **dominant** and both guilds always fight.

### Numbers you can check

Take `V = 10`.

| Fight cost `C` | Both contest, each | Contest probability `p*` | Chance of a fight `p*²` | Expected payoff per guild |
|---|---|---|---|---|
| 2 | +3 | 1 (Contest dominant) | 100% | 3.00 |
| 6 | −1 | 5/6 = 0.833 | 69.4% | 0.83 |
| 8 | −3 | 0.625 | 39.1% | 1.88 |
| 10 | −5 | 0.500 | 25.0% | 2.50 |
| 20 | −15 | 0.250 | 6.3% | 3.75 |

Check the `C = 6` row by hand. `p* = 10 / 12 = 5/6`. Against that `p`, Contest pays `(5/6)(−1) + (1/6)(10) = −0.833 + 1.667 = 0.833`. Yield pays `(1/6)(5) = 0.833`. Equal, so neither guild gains by changing its mix. Each guild expects 0.83 points per spawn. If both always yielded, each would get 5.

Read down the table. Making fights more expensive makes both guilds better off. At `C = 6` they fight 69% of the time and waste most of the loot on repairs. At `C = 20` they fight 6% of the time. The cost did not change who gets loot. It changed how often it is worth fighting for.

### The payoff edit

Now model tap-to-faction for two guilds of the same faction. If both guilds hit the boss, both are eligible for loot, so each gets `V` whatever the other does. Rename Yield to **Share**: stay and help.

| Row guild / column guild | Contest | Share |
|---|---|---|
| Contest | `V − C`, `V − C` | `V`, `V` |
| Share | `V`, `V` | `V`, `V` |

With `V = 10` and `C = 6`, Contest pays 4 against a contester and 10 against a sharer. Share pays 10 against both. Share is never worse and sometimes better, so it **weakly dominates** Contest. The only cell that is not an equilibrium is (Contest, Contest), because either guild gains 6 by switching to Share. The other three cells are equilibria, and every one of them pays both guilds 10, twelve times the 0.83 of the old mixed equilibrium. Nobody changed the players. The loot rule removed the prize the fight was for, and the fight became pure cost.

Two limits keep the model honest. Tap-to-faction shares loot within a faction, so two guilds of opposite factions still face the old matrix. And a real guild may fight for reasons outside the matrix, such as rivalry or fun. The model predicts what the loot rule pays for, not what every player does.

### A visual you can move

Open the [world boss game interactive](../examples/w10-world-boss-game.html). The top view is the 2 × 2 payoff matrix. It recomputes as you drag the loot value `V` and the fight cost `C`, and it marks each pure equilibrium. The bottom view plots what Contest and Yield pay against the other guild's contest probability `p`. The two lines cross at `p*`. The crossing is the mixed equilibrium, and its height is what each guild expects.

Start at `V = 10`, `C = 6`. The lines cross at `p = 0.83`, height 0.83. Drag `C` up to 10 and watch the crossing slide left to 0.5 and rise to 2.5. Drag `C` down past 5 and the lines stop crossing inside the chart. Contest is above Yield everywhere, and the matrix highlights (Contest, Contest). Then switch on "Shared loot (tap-to-faction)". The Share line sits at `V` across the whole chart, never below Contest. Three cells are now outlined, and all of them pay 10 to both guilds. Only (Contest, Contest) is left out.

### Cross-game recognition

**World of Warcraft, patch 7.0.3.** The same edit, applied to every creature. Before it, two players questing near the same monster were in a small version of the world boss game. Whoever tapped first got the kill credit and the loot, and the other waited for a respawn. Letting up to five other characters tap a creature turned the (Share, Share) cell from "half value" into "full value" for everyone involved. Most of the contest over quest monsters went away, because there was little left to contest.

**Animal conflict: the Hawk-Dove game.** John Maynard Smith used the same matrix in biology. Two animals contest a resource worth `V`. A "hawk" escalates, a "dove" backs off, and two hawks risk injury costing `C`. In his form, when injury costs more than the resource, a stable population contains hawks in the proportion `V / C`. Rewrite his matrix into ours and his `C` is twice our per-guild cost, so his `V / C` is our `V / (2C)`. Same model, same prediction. Raising the cost of escalation lowers how often it happens, in animals and in guilds.

**Penalty kicks in professional football.** Ignacio Palacios-Huerta studied over 1,400 penalty kicks. The kicker wants a mismatch, and the keeper wants to guess the same side. He found that kickers and goalkeepers mix left and right in proportions close to the mixed Nash equilibrium, and that their choices look serially independent. That is the indifference method's prediction holding for people who play the same game many times with money on the line. MMO guilds meeting at the same spawn every week are that kind of population.

The pattern across all three is the same. The equilibrium mix follows the payoffs, so to change behavior you change `V`, `C` or who gets paid.

### Eyes-open design judgment

- **Stable is not good.** The mixed equilibrium at `C = 6` gives each guild 0.83 when cooperation would give 5. Nothing inside the game pushes players toward the better outcome. A designer has to.
- **Raising the cost of conflict is a blunt tool.** It lowers the fight rate, but it also makes every fight that does happen more painful, and it punishes PvP players who want the fight. Shared credit removes the reason to fight without touching PvP at all.
- **Removing the conflict removes a story.** Contested world bosses produced rivalries players remember. If you want contest, keep a prize worth fighting over and make the fight's cost something you tuned on purpose.
- **Check every group the rule does not cover.** Tap-to-faction left cross-faction contests in place. A payoff edit fixes the cells it touches and nothing else.
- **Look for the pure equilibria first.** Two pure equilibria mean players must coordinate on who backs down. Guild agreements, schedules and server culture often do that. The mixed equilibrium describes strangers who cannot coordinate.

## 3. Nash equilibrium beyond two strategies

The definition applies to any game with any number of players and payoffs. A Nash equilibrium is stable against one player deviating. It says nothing about fairness, happiness or the best total outcome.

John Nash proved in 1950 that every game with a finite number of players and strategies has at least one equilibrium, if you allow mixed strategies. Rock-paper-scissors has no pure equilibrium at all, because whatever you commit to, your opponent should switch to its counter. Its only equilibrium is the one-third mix.

### A weighted triangle, solved the week 9 way

Ian Schreiber's *Game Balance Concepts* course works through a rock-paper-scissors variant in which a win with Rock is worth 2 points and other wins are worth 1. The solution he derives is Paper 50%, Rock 25%, Scissors 25%. Map it onto week 9's arena. Rock is the Knight, beating Scissors (the Ranger) with `a = 2`. Paper is the Mage, beating Rock with `b = 1`. Scissors beats Paper, so `c = 1`. With `S = 4`, the Knight gets `c / S = 25%`, the Mage `a / S = 50%` and the Ranger `b / S = 25%`. Same answer. Making Rock's wins more valuable made Paper, Rock's counter, the most common throw.

### Solving bigger matrices

Three classes can be solved by hand. Real rosters have five, ten or forty options. There are three practical tools.

1. **Remove dominated strategies first.** It shrinks the matrix and finds dead classes for free.
2. **Solve with linear programming.** A two-player zero-sum game can be solved exactly as a linear program. Find shares `p` and a value `v` that maximize `v`, such that every column gives the row player at least `v`. Spreadsheet solvers handle any matrix you will meet in this course. Lab 10 walks you through it.
3. **Simulate adaptation.** "Fictitious play" lets each simulated player best-respond to the historical average of the other's choices. The averages converge to equilibrium in two-player zero-sum games. It is slower and approximate, and it shows you the path, which is what live players experience.

One more check after solving. A class that is not dominated can still sit at 0% in the equilibrium. Compute every class's expected payoff against the equilibrium mix. Classes in the mix all earn the game's value (0 in a symmetric zero-sum game). A class outside it earns less, which is why nobody picks it. Lab 10's Warden is a case: it beats one class and is dominated by none, and it still earns −0.021 against the solved meta.

## 4. The meta as a population

Week 9 moved the population one week at a time with `share × (1 + η × E)` and watched it circle the stable mix. The continuous version of that rule is the **replicator equation** from evolutionary game theory:

```
d(p_i)/dt = p_i × (payoff_i − average payoff)
```

`payoff_i` is class i's expected payoff against the current population, and the average is weighted by the shares. In a symmetric zero-sum game the average payoff is always 0, so a class grows exactly when its expected margin is positive. That is week 9's rule with the week shrunk to an instant.

Two results from the mathematics of this equation add to what week 9 showed. First, the interior Nash equilibrium is a rest point, so a population that starts there stays there. Second, for a zero-sum counter triangle, the population neither spirals in nor out. It orbits the equilibrium on a closed loop, and **the long-run average of each share equals the equilibrium share**. The weekly rule from week 9 spirals slowly outward because it takes whole-week steps. The smooth-orbit mode of the [week 9 interactive](../examples/w09-counter-triangle.html) shows the closed loop.

This has consequences for live balance.

- **A snapshot of play rates is not the equilibrium.** The equilibrium is where the meta averages out, not where it sits on a given day. Average over a full cycle before you compare telemetry against the model.
- **Reacting to the surge makes it worse.** If you nerf a class during its post-patch surge, you move the equilibrium again while the population is still swinging. Designers call this chasing the meta.
- **Real populations have friction.** Players stay with a favorite class, and some never switch. Friction damps the orbits, and real metas usually settle closer to the equilibrium than the frictionless model predicts.

## 5. Using game theory as a balance tool

Put the pieces together into a workflow you can run on any class roster or reward rule.

1. Gather payoffs. For classes, matchup win rates from telemetry or simulation (week 13 builds the simulator), with players of similar skill so the numbers describe the classes. For shared content, estimate `V` and `C` in the same unit, such as minutes of play.
2. Build the payoff matrix. For matchups, check that mirror cells are opposites. If they are not, your data has a bug.
3. Remove dominated strategies. Each one is a class or behavior players will abandon. Fix it before anything else.
4. Solve for the equilibrium. For classes, every class should appear with a share you can live with. A common target is that no class falls below half its "fair" share (for five classes, below 10%) and none rises above twice it. For shared content, ask whether the equilibrium behavior is the one you want.
5. Before shipping a change, re-solve with the new numbers. Write down what you expect to rise and what to fall. After the patch, compare against telemetry over several weeks, not several days.

Remember the limits. Duels and two-guild standoffs are the clean cases. In a battleground a class's value depends on its allies as well as its enemies, and a world boss may draw five guilds, not two. MMO307 takes these ideas into PvP ladders and rating systems ([MMO307 syllabus](../../MMO307-game-balance-ii-pvp-progression-and-endgame/syllabus.md)).

## In-class activity (25 minutes)

Work in groups of three. Each group gets one of three printed scenarios: a contested gathering node, a contested rare spawn, or a four-class duel table.

1. Build the payoff matrix. For the two contest scenarios, estimate `V` and `C` in minutes of play from the handout. For the duel table, convert win rates to margins and check it is zero-sum. (5 min)
2. Remove dominated strategies. Write one sentence explaining each removal. (5 min)
3. Find every equilibrium. For a 2 × 2 contest, list the pure equilibria and compute `p* = V / (2C)` if it applies. For the duel table, use week 9's rule if three classes remain in a cycle, or the Lab 10 spreadsheet if four remain. (10 min)
4. Propose one payoff change, a single number or a loot rule, that moves the equilibrium to the behavior you want. Predict the new equilibrium and one side effect. (5 min)

Expected output: one card per group with the matrix, removed strategies, the equilibrium before and after the change, and the one-sentence prediction. Groups swap cards and check each other's arithmetic.

## Common misconceptions

- **"A Nash equilibrium is the best outcome."** It is only the stable one. In the world boss game, the equilibrium gives each guild 0.83 points when cooperation would give 5. Stability and quality are different questions.
- **"If cooperating is better for everyone, players will find it."** Not if a single player gains by defecting from it. "Always yield" pays 5 each, and it still falls apart because one guild gains by contesting. The fix is a payoff change, not a request.
- **"A mixed equilibrium means players act at random."** In a population it means shares. At `p* = 0.83`, it can be that 83% of guilds always contest and 17% always yield. What matters is the mix a guild meets.
- **"A class that is not dominated will be played."** It can still earn less than the others against the equilibrium mix and sit at 0%. Check its payoff against the solved mix, not only its pairwise comparisons.

## Check yourself

1. In the world boss game with `V = 10`, the designer raises the fight cost to `C = 10`. Find the contest probability, the chance a given meeting turns into a fight, and each guild's expected payoff.
2. A four-class table has a class whose row is (−0.1, +0.3, −0.3, 0) against (A, B, C, itself), and class A's row against the same columns is (0, +0.35, −0.2, +0.1). Is the fourth class dominated? Show the comparison.
3. In the world boss game with `V = 10`, the designer lowers the fight cost from 6 to 2. Recompute the equilibrium and explain the change in plain words.
4. Knight beats Ranger 75/25, Mage beats Knight 60/40 and Ranger beats Mage 60/40. State the Nash equilibrium and show that the Knight earns 0 against it.

<details>
<summary>Answers</summary>

1. `p* = 10 / 20 = 0.5`. A fight needs both to contest, `0.5² = 25%`. Expected payoff `(1 − 0.5) × 5 = 2.5` each, three times the 0.83 at `C = 6`.
2. Compare column by column: against A, 0 > −0.1; against B, +0.35 > +0.3; against C, −0.2 > −0.3; against the fourth class, +0.1 > 0. A is better in every column, so the fourth class is strictly dominated and should vanish from the meta.
3. Both contesting now gives `10 × 0.5 − 2 = 3` each. Setting Contest equal to Yield gives `p = V / (2C) = 2.5`, which is above 1, so there is no mixed equilibrium. Contest beats Yield whatever the other guild does (3 > 0 and 10 > 5), so Contest is dominant and both guilds always fight. Cheaper fighting turned a game of chicken into a brawl every time.
4. Margins `a = 0.5` (Knight over Ranger), `b = 0.2` (Mage over Knight), `c = 0.2` (Ranger over Mage), `S = 0.9`. Knight `c / S = 22.2%`, Mage `a / S = 55.6%`, Ranger `b / S = 22.2%`. The Knight earns `−b × m + a × r = −0.2 × 0.556 + 0.5 × 0.222 = −0.111 + 0.111 = 0`.

</details>

## Lab hook

**Lab 10: Solving a class meta.** You build a spreadsheet that takes a matchup win-rate table for up to five classes, removes dominated classes, solves the equilibrium with a linear-programming solver, and reports the predicted share change for a proposed patch. See [`labs/lab10.md`](../labs/lab10.md).

## Sources

- Warcraft Wiki, "Tap" (accessed September 2026). Classic: the first player to cause damage taps a mob for their entire party. Patch 5.1.0: world bosses (Sha of Anger, Galleon, Nalak, Oondasta) made tap-to-faction. Patch 7.0.3: all creatures can be tapped by up to 5 other characters. https://warcraft.wiki.gg/wiki/Tap
- Maynard Smith, J. (1982). *Evolution and the Theory of Games*. Cambridge University Press. The Hawk-Dove game; with injury cost above resource value, the stable hawk proportion is `V / C`.
- Palacios-Huerta, I. (2003). "Professionals Play Minimax." *Review of Economic Studies* 70(2), 395–415. Over 1,400 penalty kicks; mixing proportions consistent with the mixed equilibrium, serial independence not rejected.
- Schreiber, I. (2010). "Level 9: Intransitive Mechanics," *Game Balance Concepts* course blog. Weighted rock-paper-scissors (Rock wins worth 2) solved to Paper 50%, Rock 25%, Scissors 25%. https://gamebalanceconcepts.wordpress.com/2010/09/01/level-9-intransitive-mechanics/
- Nash, J. (1950). "Equilibrium points in n-person games." *Proceedings of the National Academy of Sciences* 36(1), 48–49.
- Hofbauer, J. & Sigmund, K. (1998). *Evolutionary Games and Population Dynamics*. Cambridge University Press. Replicator dynamics, closed orbits around the interior equilibrium in zero-sum rock-paper-scissors, time averages converging to the equilibrium.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter 25, Intransitive Mechanics and Payoff Matrices.
- The Knight, Ranger, Mage and Bard arena, and the world boss payoffs, are invented for teaching.

## Interactive spec: examples/w10-world-boss-game.html

**The one insight:** the behavior players settle on follows the payoffs. Raising the cost of fighting lowers the contest rate and raises everyone's payoff, and sharing the loot removes the reason to fight at all.

**Layout.** Two linked views. On mobile they stack; at 900px and wider they sit side by side. Controls above, number panel below.

1. **Payoff matrix (left).** A 2 × 2 grid. Rows "You: Contest", "You: Yield" (or "Share" when shared loot is on); columns the same for the other guild. Each cell shows "your payoff, their payoff" to two decimals. In each cell, mark best responses: underline your payoff if it is your best response to that column, and their payoff if it is theirs to that row. Cells where both are best responses are pure equilibria: give them a thick outline and the label "equilibrium". Below the grid, a one-line verdict: "Two pure equilibria and one mixed", "Contest is dominant", or "Share weakly dominates Contest".
2. **Payoff against the other guild's mix (right).** x-axis: the other guild's contest probability `p`, 0 to 1. y-axis: your expected payoff, range fixed from `min(V/2 − C, 0) − 1` to `V + 1`. Two lines: Contest `p (cell CC) + (1 − p)(cell CY)` and Yield/Share `p (cell YC) + (1 − p)(cell YY)`, where each cell is your payoff. If the lines cross strictly inside 0 < p < 1, mark the crossing with a dot, a vertical dashed line down to the axis, and the label "p* = x.xx, payoff y.yy".

**Controls.**
- Slider "Loot value V", 2 to 20, step 1, default 10.
- Slider "Fight cost C (per guild)", 0 to 20, step 0.5, default 6.
- Toggle "Shared loot (tap-to-faction)", default off.
- Preset buttons: "Classic tapping (V 10, C 6)", "Expensive fights (V 10, C 10)", "Cheap fights (V 10, C 2)", "Tap-to-faction (V 10, C 6, shared)".
- Every control is keyboard operable with visible focus. Views update on input.

**Formulas.**
- Unshared: CC = `V/2 − C`, CY = `V`, YC = 0, YY = `V/2` (your payoffs; the matrix is symmetric, so theirs mirror).
- Shared: CC = `V − C`, CY = `V`, YC = `V`, YY = `V`. Row and column labels read "Share" instead of "Yield".
- Mixed equilibrium (unshared, `C > V/2`): `p* = V / (2C)`, payoff `(1 − p*) V / 2`, chance of a fight `p*²`.
- If `C ≤ V/2` (unshared): no interior crossing; verdict "Contest is dominant"; highlight (Contest, Contest). At exactly `C = V/2` the lines meet at p = 1; treat as dominant.

**Number panel.** `V`, `C`; the verdict; `p*` to three decimals (or "none"); chance of a fight in percent to one decimal; expected payoff per guild to two decimals; and "Always yield would pay V/2 each" for comparison.

**Test values.**
| V | C | Shared | p* | Chance of fight | Payoff each |
|---|---|---|---|---|---|
| 10 | 6 | off | 0.833 | 69.4% | 0.83 |
| 10 | 8 | off | 0.625 | 39.1% | 1.88 |
| 10 | 10 | off | 0.500 | 25.0% | 2.50 |
| 10 | 20 | off | 0.250 | 6.3% | 3.75 |
| 10 | 2 | off | none, Contest dominant | 100% | 3.00 |
| 12 | 8 | off | 0.750 | 56.3% | 1.50 |
| 10 | 6 | on | none, Share weakly dominates | 0% | 10.00 |

- At V 10, C 6 unshared, the outlined cells are (Contest, Yield) and (Yield, Contest).
- At V 10, C 6 shared, three cells are outlined, (Contest, Share), (Share, Contest) and (Share, Share), each paying 10.00 to both. (Contest, Contest) is not outlined.

**First screen.** Load "Classic tapping (V 10, C 6)". Caption: "Each guild contests 83% of the time and expects 0.83 points. Taking turns would pay 5."

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, light and dark modes. Lines distinguished by dash pattern as well as color. Equilibrium cells marked by outline and text label, not color alone. No game art or logos.
