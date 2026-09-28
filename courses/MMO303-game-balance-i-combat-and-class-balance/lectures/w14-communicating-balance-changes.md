# MMO303 · Week 14 — Communicating Balance Changes (Patch Notes)

**Why this matters:** Players never see your simulator. They see one line of patch notes, and they decide from it whether to reroll, rebuild or quit a class. If the line says one thing and the game does another, you lose their trust faster than any bug could.

**You will be able to:**
- Translate any patch-note line into the relative change of the outcome a player feels: damage at their rank, total damage, effective HP, shots to kill or the turn a card comes down.
- Compute a class's total damage change from per-ability changes and damage shares, and explain why a large-looking number can be a small change.
- Identify breakpoints, where a small number change produces a step change in time-to-kill, and flag them in the notes.
- Write and critique a balance entry that names its target audience, shows old and new values in consistent units, and states its intended effect.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on the balance process after launch; Riot Games, "/dev: Balance Framework Update" (2020, linked in Sources); skim one recent set of patch notes for a game you play and bring one line you found confusing.

**Prerequisites from earlier courses:** effective HP and armor from [MMO303 week 2](w02-armor-and-damage-mitigation.md); multiplicative layers from [MMO303 week 4](w04-stacking-mitigation-multiplicative-layers.md); simulator output and error bars from [MMO303 week 13](w13-combat-simulators.md); time-to-kill from [GD203 week 4](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md); stat weights from [MMO303 week 12](w12-stat-weights-and-theorycrafting.md).

**Interactive:** [`examples/w14-patch-line-translator.html`](../examples/w14-patch-line-translator.html). Keep it open during section 2.

---

## 1. Patch notes are part of the change

A balance change has two halves. The first half is the number you edit in the data. The second half is what players believe happened. The second half decides what they do next: who switches class, who buys a different item, who stops queuing as a healer. So the note is part of the change. A correct change with a misleading note will produce the wrong player behavior, and your next round of data will measure that behavior, not your change.

Three groups read patch notes, and they want different things.

- **Players of the changed class** want to know whether their character got stronger or weaker at the level and build they actually play. They care about their rank, their spec, their content.
- **Players of other classes** want to know whether their matchups changed. A tank cares about a DPS nerf only if it changes which DPS the raid brings.
- **Analysts and theorycrafters** want exact values so they can rerun their simulators. They will find any number you leave out, and they will notice if the game does something the notes did not say.

Studios formalize the first question, "who is this change for?", before they write a single note. Riot Games published its League of Legends champion balance framework in 2019 and updated it in 2020. It splits players into four audiences (Average, Skilled, Elite and Professional play) and sets thresholds for each. The rule that matters for this lecture is how the audiences combine. A champion needs nerfs if it is overperforming in any one audience, and it is ready for buffs only if it is underperforming in all four. That rule means many changes are aimed at one audience while trying to leave the others alone. The patch note then has to tell each audience whether the change is about them.

This week's worked example shows how one line of patch notes can be a buff for one group of players and a nerf for another, and how to read it correctly.

## 2. Worked example: buff or nerf? Reading one line

### The hook

League of Legends patch 14.5 (March 2024) changed the champion Zac. His W ability, Unstable Matter, deals flat damage that grows with the ability's rank (1 to 5), plus a percentage of the target's maximum health. The patch note line read, in Riot's usual format with an arrow between old and new:

```
Damage: 35/50/65/80/95 (+4/5/6/7/8% (+3% per 100 AP) of target's maximum health)
     ⇒ 40/50/60/70/80 (+4/5/6/7/8% (+3% per 100 AP) of target's maximum health)
```

Was that a buff or a nerf? Most players scan for the last number, see 95 become 80, and call it a nerf. But look at rank 1. It went up.

Riot's context paragraph explains the goal. Zac was too strong in the top lane but healthy in the jungle. Top-lane Zac raises W to rank 5 first. Jungle Zac raises a different ability first, so his W stays at a low rank through the early game. In paraphrase, the note describes top-lane nerfs that barely touch the jungle, possibly with a small early boost for jungle clearing. One line, two audiences, two opposite effects. You can only see that by translating the line into the numbers each player feels.

### The model

For any patch-note line, name the **outcome** a player feels, write it as a function `f` of the changed values, and compute the relative change:

```
δ = f(new) / f(old) − 1
```

- `δ` (delta) is the relative change in the outcome, as a fraction. `+0.05` means 5% more.
- `f` is the outcome: ability damage at a given rank, total damage over a fight, effective HP, shots to kill.

When the outcome is a sum of parts and only some parts change, the relative change of the whole is the **share-weighted** average of the parts' changes:

```
δ_total = Σ sᵢ × δᵢ
```

- `sᵢ` is part i's share of the old total (shares add to 1).
- `δᵢ` is the relative change of part i.
- Unchanged parts have `δᵢ = 0`, so they dilute the change.

This second formula is the whole reason patch notes mislead. A line changes one part. A player feels the total. The share is almost never printed.

### Numbers you can check

Take Zac's W at 0 ability power (AP), against a target with 2,000 maximum health. The max-health part is `4/5/6/7/8% × 2,000 = 80/100/120/140/160` at ranks 1 to 5 and is unchanged. Any magic resistance on the target multiplies old and new damage by the same factor, so it cancels in `δ` (the week 4 rule for multiplicative layers). We can ignore it.

| Rank | Flat part old ⇒ new | δ of the flat part | %HP part | Total W old ⇒ new | δ of total W |
|---|---|---|---|---|---|
| 1 | 35 ⇒ 40 | +14.3% | 80 | 115 ⇒ 120 | +4.3% |
| 2 | 50 ⇒ 50 | 0% | 100 | 150 ⇒ 150 | 0% |
| 3 | 65 ⇒ 60 | −7.7% | 120 | 185 ⇒ 180 | −2.7% |
| 4 | 80 ⇒ 70 | −12.5% | 140 | 220 ⇒ 210 | −4.5% |
| 5 | 95 ⇒ 80 | −15.8% | 160 | 255 ⇒ 240 | −5.9% |

Two things happened between the "flat part" column and the "total W" column. First, the sign depends on rank: a buff at rank 1, neutral at 2, a nerf from 3 up. Second, the unchanged max-health part dilutes everything. The eye-catching −15.8% at rank 5 is −5.9% of the ability.

Now dilute once more, to the player's whole damage. Suppose, for the exercise, that W is 25% of a top-lane Zac's damage in a typical mid-game fight, and 15% of a jungle Zac's. These shares are invented to show the method; real shares depend on build and matchup. Then:

| Player | W rank at that point | δ of W | Share of W, s | δ of total damage = s × δ |
|---|---|---|---|---|
| Top-lane Zac, W maxed | 5 | −5.9% | 0.25 | −1.5% |
| Jungle Zac, W at rank 1 | 1 | +4.3% | 0.15 | +0.6% |

The same line is a 1.5% total damage nerf for one player and a 0.6% buff for another. Change the target's maximum health and the numbers move. Against a 1,000-health target the %HP part is smaller, so dilution is weaker, and rank 5 becomes −8.6%. Against 3,000 health it is −4.5%. Squishy targets feel the nerf more.

### The visual

Open `examples/w14-patch-line-translator.html`. The left panel shows what the patch note shows: old and new flat values per rank as paired bars. It looks like a simple nerf with a small exception. The right panel shows what players feel: δ per rank for the flat part and for the whole ability, with a line at zero. Drag the target's maximum health slider and watch the "whole ability" bars shrink toward zero as the unchanged part grows. Then drag the "share of total damage" slider and watch the readout for total damage. At a share of 0.25, the rank-5 change reads −1.5%. The patch-note view never changes while you drag. Only the player's view does.

### Cross-game recognition

Every game formats its notes differently. Rewrite each into `δ = f(new)/f(old) − 1` and, where it applies, `δ_total = Σ sᵢ δᵢ`.

**World of Warcraft, percentage lines and shares.** Blizzard usually writes class tuning as a percentage change to one ability. In the March 4, 2025 hotfixes for The War Within season 2, Devastation Evoker's Firestorm got "damage increased by 40%" and Elemental Shaman got "all damage dealt increased by 5%". The 40% line looks eight times bigger. But the Elemental line has share `s = 1`, so `δ_total = 5%`. The Firestorm line has share equal to Firestorm's slice of the Evoker's damage. If that slice were 4%, `δ_total = 0.04 × 40% = 1.6%`. The smaller-looking line is the bigger change. The same hotfix list also changed Havoc Demon Hunter's Thrill of the Fight bonus to ability damage from 20% to 15%. That is a percentage-point change on a multiplier. Ability damage during the buff goes from `1.20×` to `1.15×`, so `δ = 1.15 / 1.20 − 1 = −4.2%`, not −5% and not −25%. The same number supports three readings, and only one is right.

**League of Legends, a base stat through effective HP.** The same patch 14.5 raised Sivir's base armor from 26 to 30. Using week 2, effective HP against physical damage is `HP × (1 + A/100)`. At level 1, before items, `δ = 1.30 / 1.26 − 1 = +3.2%`. Later, with 100 total armor from growth and items, the same +4 gives `(100 + 104) / (100 + 100) − 1 = +2.0%`. A flat change is worth more early and less late, the same pattern as Zac's rank 1. The note says "26 ⇒ 30", which is +15% armor. What a Sivir player feels is +3.2% survival in lane.

**Hearthstone, cost and tempo.** In patch 34.2.2 (December 2025), Blizzard changed the card Cardboard Golem from 4 mana with 4 attack and 4 health to 3 mana with 3 attack and 3 health, and the notes called it a buff aimed at Aura Paladin decks. Stats per mana stayed exactly the same, `8 / 4 = 6 / 3 = 2`. So what changed? The outcome players feel is the turn the card can be played, and `δ` of cost is −25%. One turn earlier matters in a game where you gain one mana per turn. The note named its audience (one deck type), as Riot's Zac note did.

**Overwatch 2, a breakpoint.** On September 17, 2024, Blizzard raised the maximum damage of Hanzo's Storm Bow arrow from 120 to 125 and raised its full-draw time from 0.72 to 0.87 seconds. The developer comment tied the change to restoring a one-shot headshot on 250-health heroes. With the standard 2× headshot multiplier, 120 gives 240, which leaves a 250-health target alive; 125 gives exactly 250. Here the share formula breaks, because the outcome is not a sum. It is shots to kill, `⌈H / damage⌉`, a step function.

| Outcome against a 250-health hero | Old (120) | New (125) | δ |
|---|---|---|---|
| Damage per arrow | 120 | 125 | +4.2% |
| Headshots to kill | 2 | 1 | −50% |
| Body shots to kill | 3 | 2 | −33% |
| Draw time per shot | 0.72 s | 0.87 s | +21% |
| Draw time for body-shot kill (draw only) | 2.16 s | 1.74 s | −19% |

A +4.2% number crossed two thresholds at once. Against a 300-health hero, neither kill count changes, and the only effect is the slower draw, a nerf. The note had to say which heroes the change was for, and it did.

In all four games, the printed number and the felt number differ. The model is the same each time: pick the outcome, compute `δ`, and weight by share unless a threshold makes the outcome a step.

### Eyes-open design judgment

- **Choose the format per line, not per patch.** "Old ⇒ new" per rank (League's style) is exact and lets theorycrafters rerun sims, but hides the per-rank sign flip unless the reader does arithmetic. "Increased by X%" (WoW's style) is easy to read but hides the share. For a change whose effect depends on rank or level, show old and new. For a change to a whole spec, a percentage is clearer. Either way, add the context sentence.
- **State the intended audience.** Riot's Zac note said top lane and jungle. The Hearthstone note named a deck. The Overwatch note named a health threshold. That sentence prevents the wrong players from overreacting.
- **Say whether the unit is relative or additive.** "Crit chance increased by 5%" can mean 20% to 25% or 20% to 21%. Write "20% ⇒ 25%" and the ambiguity disappears.
- **Flag breakpoints.** If a change crosses a shots-to-kill or hits-to-kill threshold against common health values, the note must say so. A 4% number that halves time-to-kill against some targets is not a 4% change.
- **Do not print the total effect you have not measured.** "This is roughly a 2% DPS increase" is helpful when your simulator gives `+2.0% ± 0.2%` for a standard build. It is harmful when you guessed. Players will quote it back at you.

## 3. Anatomy of a balance entry

With the model in hand, a good balance entry has five parts. Use them as a checklist.

1. **Target.** The class, spec or item, and the ability or stat by its in-game name.
2. **Old ⇒ new, in the game's units.** Every changed value, with ranks or levels if they differ by rank. Keep scaling terms in the line even when unchanged, as Riot did with the max-health term in the Zac note, so readers can see what dilutes the change.
3. **Context.** One to three sentences on why. What problem did the data show, and for which audience?
4. **Intended effect.** What you expect to happen, stated as an outcome: "top-lane win rate down; jungle roughly unchanged", or "one-shot headshots on 250-health heroes restored". When you have simulator output, a measured total change with its error bar belongs here.
5. **What did not change.** When players might assume a related thing changed, say it did not. "The max-health portion is unchanged" saves a thousand forum threads.

A small entry for an invented game, written to this checklist:

```
Warden
  Shield Bash
  - Damage: 60/80/100 ⇒ 70/85/100
  - Cooldown: unchanged (8 s)
  Context: Wardens fall behind in the first ten minutes of dungeons, then
  catch up once Shield Bash is rank 3. We are raising early ranks only.
  Intended effect: +16.7% Shield Bash damage at rank 1, +6.3% at rank 2,
  no change at rank 3. Our dungeon simulation shows +1.4% ± 0.3% total
  damage at level 10 and no change at level 30.
```

Notice that the intended-effect line uses exactly this week's model. `70 / 60 − 1 = +16.7%`. `85 / 80 − 1 = +6.3%`. The total is the share-weighted result from the simulator, reported with its week 13 error bar.

### Percent and percentage points

This is the single most common source of confusion in patch notes, so it gets its own subsection. A **percentage point** is an absolute change in a quantity that is itself a percentage. Going from 20% crit to 25% crit is +5 percentage points and +25% relative. Going from a 20% damage bonus to a 15% damage bonus is −5 points, −25% relative to the bonus, and −4.2% relative to damage. Three numbers, one change.

Rules for your notes:

- Write the old and new value of a percentage stat: "20% ⇒ 25%".
- Never write "increased by 5%" for a percentage stat. Readers will split between the two meanings.
- When a bonus is a multiplier, compute `δ` on the multiplied outcome, as in the Thrill of the Fight case, and put that in the intended-effect line if it matters.

### Tooltips must match

Patch notes describe a change once. Tooltips describe it forever. If the tooltip rounds, or shows the value against one reference target (as week 2's armor tooltips did), make sure it still matches the notes after the change. A mismatch between notes, tooltip and actual behavior is the fastest way to teach players to ignore all three.

## 4. Timing, trust and undocumented changes

### Hotfix, patch or preview

Studios ship balance through different channels, and each sets expectations.

- A **patch** bundles many changes on a schedule. League of Legends ships numbered patches like 14.5. Players expect full notes with context.
- A **hotfix** is a server-side change applied between patches, often without a client download. WoW's class tuning in the example above came as a hotfix list. Players expect shorter notes, sometimes with developer notes attached.
- A **preview** or test-server release lets players see changes before they go live. It turns patch notes into a conversation, and theorycrafters will sim the proposed numbers and report back before you ship.

A useful rule of thumb: the faster the channel, the more important the context sentence. A hotfix that lands mid-week, mid-raid-tier, with only numbers, reads like a mistake even when it is deliberate.

### Undocumented changes

Every live game eventually ships a change that is missing from the notes. Sometimes a bug fix alters damage. Sometimes a refactor changes rounding. Players will find it, because analysts compare logs across patches. Treat any undocumented change that alters an outcome by more than your tolerance band as a communication failure and publish a correction. Your credibility on the next patch depends on it.

### Say what you are watching

Notes can also say what you did not change and why. "We know Warden is weak in raids; we are waiting for a week of data before tuning." That sentence answers the most common forum question and commits you to a timeline. Only write it if you will keep the promise.

## 5. Checking whether the change and the note worked

After a patch, you have two questions. Did the change do what you intended? Did players understand it?

For the first, compare the outcome you predicted with live data. For a DPS change, compare simulated and logged damage before and after. For a champion or class change in a competitive game, compare win rate and pick rate per audience, the way Riot's framework defines them. MMO307 week 14 covers measuring balance with win and pick rates in depth, and MMO308 week 9 covers patch management and hotfix process; see the [MMO307 syllabus](../../MMO307-game-balance-ii-pvp-progression-and-endgame/syllabus.md) and the [MMO308 syllabus](../../MMO308-live-operations-analytics-and-experimentation/syllabus.md).

For the second, look for a mismatch between the size of the change and the size of the reaction. If a class got a +0.6% total change and its pick rate fell 30% the next day, the note was probably read as a nerf. That happens often with lines like Zac's, where the last number went down. Players react to the note first and to the game second. A change that is small in the game and large in the reaction is a communication bug, and your next note is the fix.

A practical habit: before publishing, give the draft notes to someone who did not work on the change, and ask them to write down, for each line, "buff or nerf, for whom, and by about how much." Compare their answers with your simulator's. Every line where they differ needs rewriting.

## In-class activity (25 minutes)

Work in pairs. You will translate lines and rewrite a bad note.

**Materials:** the interactive, a calculator, and the invented class below.

The Pyromancer's damage, in a standard 300-second single-target simulation, comes from four abilities: Fireball 50%, Ignite (a damage-over-time effect) 25%, Flame Wave 15%, Meteor 10%. The draft patch note says:

```
Pyromancer
- Fireball damage reduced by 6%.
- Ignite damage increased by 10%.
- Meteor critical strike chance increased by 10%.
- Flame Wave: 100/140/180 ⇒ 110/140/170.
```

1. **(8 min)** For each line, compute `δ` of the ability and `δ_total = s × δ` at max rank. For Meteor, assume its current crit chance is 20% and crits deal 2× damage, and do it twice: once reading the line as +10 points, once as +10% relative.
2. **(5 min)** Sum the total change for the whole patch under each Meteor reading. Is the Pyromancer buffed or nerfed overall?
3. **(12 min)** Rewrite the note to the section 3 checklist. Include old and new values, a context sentence you invent, and an intended-effect line with the total change.

**Expected output:** Fireball `0.50 × −6% = −3.0%`. Ignite `0.25 × +10% = +2.5%`. Flame Wave at rank 3 `170 / 180 − 1 = −5.6%`, times 0.15 gives `−0.8%`. Meteor at +10 points: expected damage per cast goes from `1.20×` to `1.30×`, `δ = +8.3%`, times 0.10 gives `+0.8%`. At +10% relative: crit 20% to 22%, `δ = 1.22 / 1.20 − 1 = +1.7%`, times 0.10 gives `+0.2%`. The patch total is `−0.5%` or `−1.2%` depending on the reading. A patch that looks like two buffs and two nerfs is a small nerf, and its size depends on a word the draft left ambiguous.

## Common misconceptions

- **"The bigger percentage is the bigger change."** Only if both lines have the same share. A 40% change to a 4% ability is smaller than a 5% change to all damage.
- **"If the last rank went down, it is a nerf."** Per-rank changes can flip sign by rank, as Zac's W did. Check every rank that some player uses.
- **"+5% crit means 5% more crits."** It depends whether the note means points or relative percent, and the effect on damage is different again. Write old ⇒ new.
- **"Small numbers mean small changes."** Near a breakpoint, a 4% damage change can halve shots to kill. Near a cap, a small armor change can do nothing. Check for thresholds before you trust linear intuition.

## Check yourself

1. A patch note reads "Frost Lance: 50/70/90/110 ⇒ 60/75/90/105". Frost Lance also deals a fixed 40 bonus damage at every rank, unchanged. Compute `δ` of the whole ability at ranks 1 and 4. Which players does this help?
2. A tank has 3,000 HP and 300 armor in a game with `K = 150`. A patch raises its base armor by 30. Compute `δ` of effective HP against physical damage. Would a tank with 600 armor gain more or less?
3. A sniper deals 110 damage per body shot and the most common health pool is 225. A proposed buff raises damage to 113. What happens to body shots to kill? At what damage would it drop to 2 shots, and what should the patch note say if you pick that value?
4. A spec's damage is 60% ability A and 40% ability B. You want a total change of −3% without touching B. What change to A do you write in the notes?

<details>
<summary>Answers</summary>

1. Rank 1: `(60 + 40) / (50 + 40) − 1 = +11.1%`. Rank 4: `(105 + 40) / (110 + 40) − 1 = −3.3%`. It helps players who have the ability at low rank (early levels, or builds that do not max it) and slightly nerfs those who max it.
2. EHP is `HP × (1 + A / K)`. Old multiplier `1 + 300 / 150 = 3.0`; new `1 + 330 / 150 = 3.2`. `δ = 3.2 / 3.0 − 1 = +6.7%`. With 600 armor, `(1 + 630/150) / (1 + 600/150) = 5.2 / 5.0`, so `+4.0%`. Flat armor is worth less, relatively, the more you already have.
3. `⌈225 / 110⌉ = 3` and `⌈225 / 113⌉ = 2`, since `2 × 113 = 226 ≥ 225`. So 113 already crosses the breakpoint; the threshold is 112.5, which means 113 in whole numbers. Body shots to kill fall from 3 to 2, a 33% cut to shots, from a +2.7% damage change. The note should say something like "Body-shot damage 110 ⇒ 113. Two body shots now defeat 225-health heroes." If you did not intend the breakpoint, choose 112.
4. `δ_total = s_A × δ_A`, so `−0.03 = 0.60 × δ_A`, giving `δ_A = −5%`. Write "Ability A damage reduced by 5%" or the old ⇒ new values, and add "about 3% lower total damage in single-target play" in the intended-effect line.

</details>

## Lab hook

**Lab 14: Patch notes from simulation evidence.** Using your Lab 13 balance matrix, you will propose changes that bring all four classes inside a ±3% band, rerun the simulator to confirm, and publish the changes as patch notes following the section 3 checklist, with an intended-effect line backed by your error bars. A classmate then reads your notes blind and predicts each change, and you score the mismatch. See [labs/lab14.md](../labs/lab14.md). This lab is practice for the final 4-class balance pass in week 15.

## Sources

- Riot Games, "Patch 14.5 Notes," League of Legends (March 2024). Zac W damage `35/50/65/80/95 ⇒ 40/50/60/70/80` with the max-health term unchanged, and the context paragraph on top lane versus jungle; Sivir base armor `26 ⇒ 30`. https://www.leagueoflegends.com/en-us/news/game-updates/patch-14-5-notes/
- Riot Games, "/dev: Champion Balance Framework" (May 2019) and "/dev: Balance Framework Update" (June 30, 2020). Four audiences; overperforming in any audience means nerfs, underperforming in all means buffs. https://www.leagueoflegends.com/en-us/news/dev/dev-balance-framework-update/
- League of Legends Wiki, "Armor" (current). Damage multiplier `100 / (100 + armor)` for non-negative armor, used for the Sivir EHP calculation (see week 2).
- Warcraft Tavern, "The War Within Hotfixes for March 4: Class Tuning for Season 2" (March 2025). Firestorm damage increased by 40%; Elemental Shaman all damage dealt increased by 5%; Thrill of the Fight's increase to ability damage 20% to 15%. https://www.warcrafttavern.com/wow/news/the-war-within-hotfixes-for-march-4-class-tuning-for-season-2/
- Blizzard Entertainment, "34.2.2 Patch Notes," Hearthstone (December 12, 2025). Cardboard Golem 4 mana 4/4 to 3 mana 3/3, described as a buff for Aura Paladin. https://hearthstone.blizzard.com/en-us/news/24250382/34-2-2-patch-notes
- Blizzard Entertainment, "Overwatch 2 Patch Notes," September 17, 2024. Hanzo Storm Bow maximum damage 120 to 125, full-draw time 0.72 to 0.87 s, developer comment on restoring one-shot headshots against 250-health heroes. https://overwatch.blizzard.com/en-gb/news/patch-notes/live/2024/09/
- Overwatch Wiki, "Hanzo" (Overwatch 2 era). Standard 2× headshot multiplier; fully drawn headshot deals 250. https://overwatch.fandom.com/wiki/Hanzo
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.
- Damage shares for Zac and Firestorm, the Warden and Pyromancer classes, and the check-yourself classes are invented for teaching and labeled as such.

## Interactive spec: examples/w14-patch-line-translator.html

**Insight the visual must make obvious:** the patch-note number and the number a player feels are different, because of rank, dilution by unchanged parts, share of total damage, and breakpoints. The patch-note view stays fixed while the player view moves.

**Layout:** two tabs. Each tab has two linked panels, side by side on desktop, stacked on mobile.

### Tab 1: "Per-rank line" (default)

- **Left panel, "What the note says":** paired bars per rank (1 to 5) for the flat part, old (steel) and new (damage red), with the values printed above each bar. Under the chart, render the line in patch-note form: `35/50/65/80/95 ⇒ 40/50/60/70/80 (+4/5/6/7/8% max HP)`.
- **Right panel, "What the player feels":** per rank, two bars of `δ` in percent: the flat part only (light) and the whole ability (solid), with a zero line. Positive bars go up in ochre, negative down in damage red. Printed values on each bar to one decimal.
- **Readout below:** for the selected rank, old total, new total, `δ` of the ability, share `s`, and `δ_total = s × δ`.

**Controls:**
- Old and new flat values per rank (five number inputs each; default Zac 14.5 values).
- Max-health percent per rank (default 4/5/6/7/8).
- Target maximum health slider, 500 to 5,000, step 100, default 2,000.
- Share of total damage slider, 0 to 1, step 0.01, default 0.25.
- Selected rank (1-5 segmented control, default 5).
- Presets: "Zac W, patch 14.5" (defaults), "Warden Shield Bash" (3 ranks: 60/80/100 ⇒ 70/85/100, no %HP part, share 0.3), "Frost Lance" (4 ranks: 50/70/90/110 ⇒ 60/75/90/105, fixed +40 bonus implemented as a constant extra part, share 0.3).

**Formulas:** `extra_r = pct_r / 100 × maxHP` (or the fixed bonus); `old_r = flat_old_r + extra_r`; `new_r = flat_new_r + extra_r`; `δ_flat_r = flat_new_r / flat_old_r − 1`; `δ_r = new_r / old_r − 1`; `δ_total = s × δ_r`.

**Test values (Zac preset, maxHP 2,000):** δ_flat = +14.3, 0, −7.7, −12.5, −15.8%; δ whole = +4.3, 0, −2.7, −4.5, −5.9%. At share 0.25, rank 5: δ_total = −1.5%. At maxHP 1,000, rank 5 δ whole = −8.6%; at 3,000, −4.5%. Frost Lance preset: rank 1 +11.1%, rank 4 −3.3%.

### Tab 2: "Breakpoints"

- **Left panel, "What the note says":** a single number line for damage per shot from 80 to 160 with markers at the old and new values (default 120 and 125) and the text `Damage: 120 ⇒ 125 (+4.2%)`.
- **Right panel, "What the player feels":** a step chart of shots to kill `⌈H / (d × mult)⌉` against damage per shot `d` from 80 to 160, one line for body shots (mult 1) and one for headshots (mult = headshot multiplier). Vertical markers at old and new damage. Shade the interval between them and label any step it crosses ("crosses 3 ⇒ 2 body shots").
- **Readout:** old and new shots to kill for body and head; draw time per shot old and new; draw-only time to kill for body shots `shots × draw`; δ for each.

**Controls:** old damage and new damage (number inputs, defaults 120 and 125), target health slider (100 to 600, step 25, default 250), headshot multiplier (1.0 to 3.0, step 0.1, default 2.0), old and new draw time (defaults 0.72 and 0.87 s). Presets: "Hanzo, Sep 2024" (defaults), "Check yourself 3" (110 ⇒ 113, health 225, headshot 2.0, draw times both 1.0).

**Test values (Hanzo preset):** body shots 3 ⇒ 2; headshots 2 ⇒ 1; draw-only body kill time 2.16 s ⇒ 1.74 s (−19.4%); draw time +20.8%; damage +4.2%. At health 300: body shots 3 ⇒ 3, headshots 2 ⇒ 2, draw-only body kill 2.16 ⇒ 2.61 s (+20.8%). "Check yourself 3": body shots 3 ⇒ 2.
