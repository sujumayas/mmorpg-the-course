# GD102 · Week 09 — Progression systems: skill vs power

**Why this matters:** When a player is stuck on a boss, your game gives them two ways forward: get better, or get stronger. How much of one buys how much of the other is a number you set, whether you meant to or not. Set it too low and stuck players quit. Set it too high and skill stops mattering, and so does the boss.

**You will be able to:**
- Classify any reward as skill, power or access progression, and say who owns it (the player or the save file).
- Compute a player's mistake budget from their health and damage and a boss's, and show that it tracks the ratio of the two sides' power.
- Compute the win probability of a skill and power combination with the binomial model, and read an iso-win curve off the interactive.
- Critique a design (level scaling, stat normalization, assist modes, failure-based power) by what it does to the exchange rate between skill and power.

**Before class:** Schreiber, *Game Balance Concepts* (2010 blog course), Level 7 "Advancement, Progression and Pacing". Adams & Dormans, *Game Mechanics: Advanced Game Design* (2012), chapter 11 "Progression Mechanisms", skim. Review MA102 week 6 on the binomial distribution before section 2.

**Prerequisites from earlier courses:** From this course, [week 3, positive feedback](w03-positive-feedback-loops-snowballing.md) and [week 8, core loops and meta loops](w08-core-loops-and-meta-loops.md). Chance versus skill from GD101 [week 10](../../GD101-introduction-to-game-design/lectures/w10-chance-vs-skill-and-randomness.md). The win probability uses the binomial model from MA102 [week 6, binomial crits over a fight](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md); do not re-derive it, use it. Hits-to-kill with a ceiling appears again, in far more detail, in GD203 [week 4, time to kill and time to die](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md).

**Interactive:** [Skill vs power map](../examples/w09-skill-power-map.html). Keep it open during section 2.

---

## 1. Three things that can progress

"Progression" is the sense that you are further along than you were. Games deliver it in three different stores, and each store behaves differently.

**Skill progression** lives in the player's head. You learn a boss's attack pattern, your timing improves, you stop wasting potions. Nothing in the save file records it. If you start a new character, you keep it. If you hand the controller to a friend, it leaves with you.

**Power progression** lives in the save file. Levels, stats, gear, upgrades. The character is stronger whether or not the player improved. Start a new character and it is gone. Hand the controller to a friend and they inherit it.

**Access progression** also lives in the save file, but it widens options instead of raising numbers. A new area, a new weapon type, a map, a recipe, a double jump. Week 10 on [emergence vs progression](w10-emergence-vs-progression.md) looks at access progression in depth, and GD203 week 14 on [horizontal vs vertical progression](../../GD203-combat-and-progression-design/lectures/w14-horizontal-vs-vertical-progression.md) separates power that goes up from options that go sideways.

The three stores have different costs for you as the designer.

| Store | Who owns it | What it costs to build | What it does over time |
|---|---|---|---|
| Skill | The player | Challenges that teach: readable attacks, fair failures | Grows fast early, then plateaus; never inflates |
| Power | The save file | Numbers: cheap to add, hard to take back | Grows as fast as you allow; can outrun all content |
| Access | The save file | New content, new mechanics: expensive | Ends when the content ends |

Power is the cheapest to produce and the easiest to overuse. It is also the only one you can hand out on a schedule. That is why almost every game with a meta loop (week 8) pays it in power. The question for this week is what that power does to the challenge.

## 2. Worked example: how many levels is one dodge worth?

### The hook

In Elden Ring (released February 2022), defeating enemies earns runes, and you spend runes at sites of grace to raise your attributes. When you die, you drop all the runes you were carrying where you fell. If you die again before getting back to them, they are gone.

Think about what that means for a player stuck on a boss. Every failed attempt offers a choice. Walk back in with the same numbers and a little more knowledge of the boss. Or leave, earn runes somewhere easier, and come back stronger. Both work, and communities argue endlessly about which one is "real". A designer should ask a sharper question. How much power buys how much skill? Is five levels worth one extra dodge, or ten?

We will not use Elden Ring's damage formulas, which are complex and change between patches. Instead we build a small boss fight with round numbers, so every step can be checked by hand, and then carry the result back to real games.

### The model

A fight is a sequence of exchanges. In each exchange the boss attacks once and you attack once. If you misread the attack, you get hit. Then you land your hit.

- The boss has `HP_b = 2,000` health and hits for `d_b = 250`.
- At character level `L`, you have `HP_p = 100 × L` health and deal `d_p = 10 × L` damage per hit.
- Your **mistake rate** `m` is the chance you get hit by any one boss attack. It is your skill, written backwards: a lower `m` is a better player.

Two counts decide the fight.

```
H = ceil( HP_b / d_p )          hits you must land to win
A = ceil( HP_p / d_b ) − 1      boss hits you can survive
```

You win if, over `H` exchanges, you get hit at most `A` times. Each exchange is an independent trial with chance `m`, so the number of hits you take is binomial, and

```
P(win) = P( X ≤ A ),   X ~ Binomial(H, m)
```

The **mistake budget** is `A / H`: the share of boss attacks you can afford to eat. If your mistake rate is well below your budget, you usually win. Well above, you usually lose. Now look at what the budget is made of, ignoring the ceilings for a moment:

```
A / H ≈ (HP_p / d_b) / (HP_b / d_p) = (HP_p × d_p) / (HP_b × d_b)
```

The numerator is your health times your damage. The denominator is the boss's health times its damage. GD203 calls health times damage a side's **power** in [week 8, power curves and level scaling](../../GD203-combat-and-progression-design/lectures/w08-power-curves-and-level-scaling.md). So:

> The share of attacks you can afford to fail is roughly your power divided by the boss's power.

That is the exchange rate between skill and power. Raise your health and damage by 10% each and your power rises by `1.1 × 1.1 = 1.21`, so you can afford 21% more mistakes. Double both and you can afford four times as many.

### Numbers you can check

At level 10, `d_p = 100`, so `H = ceil(2,000 / 100) = 20` hits. `HP_p = 1,000`, so the boss kills you on its fourth hit and `A = ceil(1,000 / 250) − 1 = 3`. Your budget is `3 / 20 = 15%`. The smooth approximation says `(1,000 × 100) / (2,000 × 250) = 20%`; the ceilings cost you a bit.

For a player with `m = 0.1` at level 10, the chance of taking at most 3 hits in 20 is

```
P(X ≤ 3) = 0.1216 + 0.2702 + 0.2852 + 0.1901 = 0.867
```

which you can check term by term with the MA102 week 6 formula `C(20, k) × 0.1^k × 0.9^(20 − k)`.

| Level | Hits to land `H` | Hits survivable `A` | Budget `A/H` | Power ratio | Win, m = 0.1 | Win, m = 0.2 | Win, m = 0.3 | Mistake rate for 50% win |
|---|---|---|---|---|---|---|---|---|
| 8 | 25 | 3 | 12.0% | 12.8% | 76.4% | 23.4% | 3.3% | 0.145 |
| 10 | 20 | 3 | 15.0% | 20.0% | 86.7% | 41.1% | 10.7% | 0.181 |
| 12 | 17 | 4 | 23.5% | 28.8% | 97.8% | 75.8% | 38.9% | 0.269 |
| 15 | 14 | 5 | 35.7% | 45.0% | 99.9% | 95.6% | 78.1% | 0.395 |
| 20 | 10 | 7 | 70.0% | 80.0% | 100% | 100% | 99.8% | 0.741 |

Read the table two ways.

**Across a row, skill matters a lot.** At level 10, going from `m = 0.2` to `m = 0.1` (halving your mistakes) takes you from 41% to 87%.

**Down a column, power matters a lot.** A player with `m = 0.2` wins 41% of attempts at level 10 and 96% at level 15. To get 96% at level 10 without any levels, that player would need to cut their mistake rate to about `0.068`, a third of what it was. Five levels bought the same result as learning to dodge three times as well.

The last column is the **iso-win curve**: every combination of skill and level that gives a 50% chance. From level 10 to level 15 the tolerable mistake rate more than doubles, from 0.181 to 0.395. By level 20 a player who gets hit by nearly three attacks in four still wins half the time. The boss has stopped testing anything.

### A visual you can move

Open the interactive. The main view is a map. Level runs along the horizontal axis, mistake rate up the vertical axis, and each cell is shaded by win probability. The 50% iso-win curve is drawn over it. A dot marks "you": drag it, or use the level and skill sliders. A side panel shows the exact `H`, `A`, budget and win chance for the dot, and a bar chart of the binomial distribution of hits taken with the survivable region shaded.

Try three things.

1. Put the dot at level 10, `m = 0.2`. Move it right, one level at a time. The win chance jumps at levels 11 (41% to 67%) and 13 (76% to 92%) and moves much less at 12 and 14. The jumps are the ceilings in `H` and `A`: a level only helps when it removes a hit you must land or adds a hit you can survive.
2. Switch "Boss scales with your level" on. Every column of the map becomes the same. Levels no longer buy anything; only moving the dot down helps.
3. Switch "Assist after each loss" on. Each failed attempt gives the player 2% damage reduction. Watch the first failure help a lot and the next nine help not at all. At level 10, 2% reduction drops the boss's hit to 245, so `ceil(1,000 / 245) = 5` and you now survive 4 hits instead of 3: the win chance goes from 41% to 63%. The next useful step is only after 20% reduction, when the hit falls below 200.

### Cross-game recognition

Real games choose very different exchange rates between skill and power. Put each into the model by asking what it does to `A / H`.

**The Elder Scrolls IV: Oblivion (2006).** Enemies and loot scale with the player's level, so the boss's power rises with yours. In the model that is `HP_b` and `d_b` growing with `L`, which holds `A / H` constant: levels stop substituting for skill. The design aim was steady difficulty, and it was widely criticized. Wikipedia's summary notes that characters who raise skills that level up involuntarily, such as athletics or armor, can level faster than they grow stronger, making enemies "disproportionately harder than intended". In model terms, the enemies' power grew with `L` but the player's `HP_p × d_p` did not keep up, so the budget fell as the player leveled.

**Guild Wars 2, structured PvP (current game).** In structured PvP, every character is boosted to level 80, and attributes and equipment are normalized, with players choosing from a PvP-specific set of runes, sigils and amulets. Both sides get the same power. The ratio `A / H` is fixed by the build choices, and only skill (and the build) decides the match. This is the deliberate opposite of Oblivion's failure: the designers want power to buy nothing, because in competitive play a power gap reads as unfairness.

**Celeste (January 2018).** Celeste's Assist Mode lets players lower the game speed, dash without limit, or become invincible. None of these raises the character's numbers. Lower game speed gives the player more time per decision, which in the model lowers `m` directly. Invincibility sets `A` to infinity. Celeste lets the player move the dot downward without ever touching the power axis, and leaves it to the player to decide.

**Hades (September 2020).** Hades' God Mode makes the player character stronger after each failed run. That converts failure into power, the "assist after each loss" toggle in the interactive. Each loss moves the dot to the right a little. It is the same logic as the pity timers in MA102 [week 10](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w10-pseudo-random-distribution-and-pity-timers.md): bad luck (or bad play) is converted into a guaranteed eventual success.

Four games, four positions on one map. Oblivion flattens the power axis. Guild Wars 2 removes it for PvP. Celeste lets the player slide down the skill axis. Hades slides the player along the power axis with each loss.

### Eyes-open design judgment

- **Strength of letting power substitute for skill:** stuck players have a way forward that does not depend on talent they may not have. Power is also predictable: the designer can promise "five more levels and you'll be fine".
- **Cost:** power that substitutes too well makes skill optional. From level 15 onward in our table, a mediocre player wins almost every time, so the boss teaches nothing. If your meta loop from week 8 keeps paying power, every old challenge becomes trivial.
- **Cost of removing substitution (scaling or normalization):** no one can grind past a wall. That is right for competitive play and harsh for single-player games, where it turns a hard boss into a hard stop.
- **Breakpoints decide how substitution feels.** Because `H` and `A` are whole numbers, power arrives in jumps. A level that removes a required hit feels great; the next one may do nothing. Tune stats so that the levels players are likely to grind give visible jumps, or use smooth damage models where jumps do not matter.
- **Decide deliberately:** where on the map you want your intended player at each point in the game, how steep the iso-win curve should be, and whether help arrives as power (the player may never learn the fight) or as time and forgiveness (the player still learns it).

## 3. Pacing skill and power together

Across a whole game, skill and power also grow at different rates, and the gap between them decides what the game feels like.

Player skill usually follows a **learning curve**: fast gains in the first hours as players learn the controls and patterns, then slower gains as they approach their personal ceiling. Power follows whatever curve you design. MA101's week on exponentials and GD203's week 7 on XP curves both show how quickly designed power can grow.

Put the two on one chart, with the content's difficulty as a third line, and three patterns appear.

- **Power tracks difficulty and skill is extra.** Enemies grow as fast as the player's numbers. Skill is what makes the difference between scraping through and cruising. Many MMOs aim here in their levelling content.
- **Power outruns difficulty.** The meta loop pays more than the content demands. The game gets easier the longer you play, and the late game feels hollow. This is the week 8 warning about meta loops overtaking core loops, measured in `A / H`.
- **Difficulty outruns power.** Skill must carry the gap. Players who learn fast are delighted; players who plateau early hit a wall. Games in this pattern usually add a substitution valve (summons, assist modes, co-op) so the wall has a door.

A practical check for your own design: at each major boss, compute the mistake budget for a character at the expected level, then at five levels above. If the budget at +5 is above about 50%, grinding makes the fight trivial. If it barely moves, grinding does not help and stuck players have no way out.

## 4. Where the progression lives changes the social game

In persistent online games, skill and power also change who can play with whom. Power is visible and compared: gear scores and item levels are used to decide who gets invited to a group. Skill is hard to see, so groups use power as a stand-in for it. A game with large power gaps will split its players by power even if skill matters more to success.

Two consequences follow. First, catch-up mechanics (which raise new players' power quickly) are often social tools more than balance tools: they let new players join groups. Second, normalizing power in some modes (as Guild Wars 2 does in structured PvP) is a way to make skill visible, because once power is equal, results come from skill. MMO307 treats catch-up and progression in endgame play in detail (see the [MMO307 syllabus](../../MMO307-game-balance-ii-pvp-progression-and-endgame/syllabus.md)).

## In-class activity (25 minutes)

Work in pairs with the interactive open and one device between you.

1. **Find your target (8 min).** You are designing this boss for a player you expect to arrive at level 12 with a mistake rate of 0.25. Using the map, find that player's win chance. It is 57.4% with the default boss. The team wants a harder first boss, between 30% and 40% on the first attempt. Change the boss's health or damage (sliders in the "Boss" panel) to hit that range. Record the values.
2. **Grind test (7 min).** With your tuned boss, move the player to level 17. What is the win chance now? If it is above 90%, the fight becomes trivial with five levels of grinding. Decide whether that is what you want, and write one sentence why.
3. **Pick a valve (10 min).** Choose one of these valves for players who are stuck: boss scales with level, assist after each loss, or a summon that adds 30% to the player's damage. Test it at level 12, `m = 0.35`. Report the win chance with and without it, and one group of players it serves badly.

Expected output: a boss tuning (health, damage), three win chances, one valve choice with its effect and its cost in one sentence.

## Common misconceptions

- **"Grinding is for bad players; real players rely on skill."** In the model, skill and power are interchangeable at a rate the designer sets. Every player uses both. The designer decides how much one buys of the other.
- **"More levels always make the fight easier."** Only levels that cross a breakpoint in `H` or `A` change the fight. In our model level 12 to 13 raises the win chance at `m = 0.2` from 76% to 92%, and 13 to 14 raises it only to 94%.
- **"Level scaling keeps the game balanced."** Scaling enemies to the player holds `A / H` constant only if the player's power keeps pace. If the player levels without getting stronger (Oblivion's involuntary skills), scaling makes the game harder as they level.
- **"Assist modes make games easier in the same way as levels."** Some assists add power (damage reduction), others change the skill axis (slower game speed). They are different moves on the map, and they teach different things.

## Check yourself

1. A boss has 3,000 health and hits for 300. Your character has 1,200 health and deals 150 per hit. Compute `H`, `A` and the mistake budget. Then raise both your health and damage by 10% and recompute. By what factor did the budget change, and what does the power ratio predict?
2. Using the table in section 2, a player at level 10 wins 41% of attempts. They can either grind to level 12 or practice until their mistake rate falls to 0.15. Which gives the higher win chance? (Use the interactive or the binomial formula for `m = 0.15`, `H = 20`, `A = 3`.)
3. A designer wants a boss where "levels help but never make it trivial". Using the model, name two changes (to the boss or to how the boss responds to the player's level) that achieve this, and describe the shape of the iso-win curve each produces.

<details>
<summary>Answers</summary>

1. `H = ceil(3,000 / 150) = 20`, `A = ceil(1,200 / 300) − 1 = 3`, budget 15%. After +10%: `H = ceil(3,000 / 165) = 19`, `A = ceil(1,320 / 300) − 1 = 4`, budget `4/19 = 21.1%`. The budget grew by `21.1 / 15 = 1.40`. The power ratio predicts `1.1 × 1.1 = 1.21`; the actual jump is bigger because the change crossed a breakpoint in `A`. With `m = 0.15`, the win chance goes from 64.8% to 85.6%.
2. Level 12 at `m = 0.2`: 75.8%. Level 10 at `m = 0.15`: `P(X ≤ 3)` for `Binomial(20, 0.15)` is about 64.8%. Grinding to level 12 gives the higher chance in this model. (The practiced player also keeps the skill for every later fight, which the table does not show.)
3. Option one: scale the boss partially with the player's level, for example boss health and damage grow at half the rate of the player's. The iso-win curve still rises with level, but more slowly, so levels help without ever pushing the budget near 100%. Option two: cap how much power counts, for example the boss ignores player levels above a threshold (a soft cap). The iso-win curve rises until the cap and then goes flat, so beyond that point only skill helps.

</details>

## Lab hook

**Lab 09, skill and power table** ([labs/lab09.md](../labs/lab09.md)). You build the win-probability table in a spreadsheet, tune a boss to a target player, test three valves, and run a five-minute playtest of a paper version of the fight to estimate a real mistake rate. The lab feeds the progression section of the final system design document.

## Sources

- Wikipedia, "Elden Ring" (released 25 February 2022): runes earned from enemies, spent at sites of grace to raise attributes, dropped on death and lost if the player dies again before recovering them; spirit summons.
- Wikipedia, "The Elder Scrolls IV: Oblivion" (2006 release, accessed September 2026): enemies and items scale with player level; criticism that involuntary skills such as athletics and armor can make enemies disproportionately harder.
- Guild Wars 2 Wiki, "Structured PvP" (current game, accessed September 2026): characters boosted to level 80; attributes and equipment normalized; PvP build of runes, sigils, amulet and specializations.
- Wikipedia, "Celeste (video game)" (released 25 January 2018, accessed September 2026): Assist Mode exists to make the game less challenging.
- Celeste Wiki (celeste.ink), "Assist Mode" (accessed September 2026): game speed down to 50% in 10% steps, infinite stamina, air dashes set to default, 2 or infinite, dash assist, invincibility.
- Wikipedia, "Hades (video game)" (full release 17 September 2020, accessed September 2026): God Mode makes the character stronger after each failed run. The exact per-run numbers were not verified for this lecture, so the interactive's assist toggle uses its own stated values rather than the game's.
- Schreiber, I. (2010). *Game Balance Concepts*, Level 7 "Advancement, Progression and Pacing".
- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 11.

## Interactive spec: examples/w09-skill-power-map.html

**The one insight.** Skill and power are two axes of one map, and the 50% iso-win curve shows the exchange rate between them. Each design choice (scaling, normalization, assist) reshapes that curve in a way you can see immediately.

**Layout.** Main heatmap on the left (desktop) or top (mobile). Side panel with the "you" readout and a binomial bar chart. Controls under the side panel.

**Heatmap, "Win chance".** x = player level `L` from 5 to 25 (integer columns). y = mistake rate `m` from 0 at the bottom to 0.8 at the top (steps of 0.01; top is "worse player"). Cell color = `P(win)` on a sequential scale from the shared palette, with a legend. Overlay the 50% iso-win curve as a line (for each column, the `m` where `P(win) = 0.5`, found by bisection) and label it "50% win". Optional toggle to also show the 90% curve. A draggable dot marks the current player; it snaps to integer levels and 0.01 steps of `m`, and responds to arrow keys when focused.

**Side panel.**
- Readouts: `H`, `A`, budget `A/H`, power ratio `(HP_p × d_p) / (HP_b × d_b)`, `P(win)` to 1 decimal place, expected attempts to first win `1 / P(win)`.
- Bar chart: `P(X = k)` for `k = 0 … H` with `X ~ Binomial(H, m)`. Bars for `k ≤ A` in the accent color with the label "you survive"; bars for `k > A` muted.

**Controls.**
- Level slider 5 to 25, default 10. Mistake rate slider 0 to 0.8, step 0.01, default 0.20.
- Boss panel: boss health 500 to 5,000 (step 50, default 2,000); boss hit 50 to 600 (step 5, default 250).
- Player growth panel: health per level (default 100), damage per level (default 10).
- Toggle "Boss scales with your level": boss health and hit are multiplied by `L / L_ref` with `L_ref = 10`.
- Toggle "Assist after each loss" with a "failed attempts" stepper 0 to 40: damage reduction `r = min(0.02 × attempts, 0.80)`, applied to the boss hit before computing `A`. State in the panel that these numbers are the example's own, not a shipped game's.
- Toggle "Summon": multiplies player damage by 1.3.
- Preset buttons: "Default", "Oblivion-style scaling" (scaling on), "Assist, 1 loss", "Assist, 10 losses".

**Formulas.**
- `HP_p = hpPerLevel × L`, `d_p = dmgPerLevel × L × (summon ? 1.3 : 1)`.
- `d_b_eff = d_b × scale × (1 − r)`, `HP_b_eff = HP_b × scale`, with `scale = L / 10` if scaling is on, else 1.
- `H = ceil(HP_b_eff / d_p)`, `A = ceil(HP_p / d_b_eff) − 1`.
- `P(win) = Σ_{k=0}^{min(A,H)} C(H, k) m^k (1 − m)^(H − k)`; if `A ≥ H`, `P(win) = 1`.
- Guard floating-point ceilings: compute `ceil(x − 1e-9)`.

**Test values (defaults unless stated; must match).**
- L = 10, m = 0.1: `H = 20`, `A = 3`, budget 15.0%, power ratio 20.0%, `P(win) = 86.7%`.
- L = 10, m = 0.2: 41.1%. L = 12, m = 0.2: 75.8%. L = 15, m = 0.2: 95.6%. L = 20, m = 0.3: 99.8%. L = 8, m = 0.3: 3.3%.
- 50% iso-win mistake rate: L = 8, 0.145; L = 10, 0.181; L = 12, 0.269; L = 15, 0.395; L = 20, 0.741.
- Scaling on, m = 0.2: `H = 20`, `A = 3`, 41.1% at every level.
- Assist, L = 10, m = 0.2: 1 loss → `A = 4`, 63.0%; 10 losses → `A = 4`, 63.0%; 11 losses (r = 0.22) → `A = 5`, 80.4%; 20 losses (r = 0.40) → `A = 6`, 91.3%.
- Level 13, m = 0.2: `H = 16`, `A = 5`, 91.8%. Level 14, m = 0.2: `H = 15`, `A = 5`, 93.9%.

**Accessibility.** The heatmap has a text alternative: an `aria-live` sentence with the dot's level, mistake rate, win chance and the 50% mistake rate at that level. The dot and all sliders are keyboard operable. Colors from `templates/interactive-tokens.css`; the iso-win line is drawn with a contrasting outline so it reads in both color schemes. No animation under `prefers-reduced-motion`.
