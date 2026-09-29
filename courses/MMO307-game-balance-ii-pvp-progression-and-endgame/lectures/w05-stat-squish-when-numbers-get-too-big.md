# MMO307 · Week 05 — Stat Squish: When Numbers Get Too Big

**Why this matters:** A game that grows power by a steady ratio every tier will, after enough years, show players nine-digit damage numbers and hand its engineers an overflow bug. Shrinking the numbers sounds like a find-and-replace job. It is not, because a real squish cannot divide everything by the same amount, and every place it doesn't is a balance change you did not mean to make.

**You will be able to:**
- Compute whether a single divisor can squish a game's numbers into a target range, from the ratio of its largest to its smallest meaningful value.
- Design per-era divisors for a squish and compute the compensation multiplier each era of old content needs to keep its difficulty.
- Compute how long a squish lasts before numbers regrow, from the divisor and the growth rate.
- Critique a formula for squish safety by testing it for constants, floors and rounding that do not scale.

**Before class:** Warcraft Wiki, "Stat squish" (the History and "The original squish" sections, 15 minutes; you skimmed the item level table for week 2). Final Fantasy XIV Online Wiki, "Value downscaling" (5 minutes).

**Prerequisites from earlier courses:** [GD203 week 8, power curves and level scaling](../../GD203-combat-and-progression-design/lectures/w08-power-curves-and-level-scaling.md) (dividing every value by one factor leaves every power ratio unchanged; this lecture starts from that result). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (solving `R^t = d` for `t`). [MMO303 week 2, armor and damage mitigation](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md) (the constant `K` in `A / (A + K)`). [GD203 week 4, time to kill and time to die](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md). This course's [week 2](w02-vertical-progression-and-power-creep.md) (the item-level chart and its squishes) and [week 4](w04-gear-treadmills-and-item-level.md) (exponential and linear budgets).

**Interactive:** [`examples/w05-squish-map.html`](../examples/w05-squish-map.html). Keep it open during section 2.

---

## 1. Why numbers outgrow the game

Week 4 showed that an exponential budget turns a steady item-level creep into a steady power ratio per season. Ratios are what balance cares about, and a steady ratio is fine for balance. Raw numbers are a different matter. They multiply every season, and after ten years they are enormous.

Big numbers cause three kinds of trouble. Each one has been documented in a shipped game.

- **Storage.** A number stored in a fixed-size integer has a ceiling. Warcraft Wiki records that World of Warcraft stored health in signed 32-bit integers, whose maximum is 2,147,483,647. The Throne of Thunder boss Ra-den started at roughly 1.5 billion health, and player mistakes could push his health past the ceiling so that it wrapped to a negative value. The game moved health to 64-bit doubles in Legion (2016).
- **Systems built on top.** Final Fantasy XIV's director, Naoki Yoshida, gave the reasons for that game's 2021 downscaling when he announced Endwalker. The wiki lists calculations causing overflow errors, enmity (threat) caps being reached, and bosses with around 440 million health in patch 5.5.
- **Reading.** A damage number with nine digits is hard to take in at a glance. The same FFXIV list includes flying combat text becoming too long, and the WoW patch notes for 12.0.0 (January 2026) describe their squish as being for clarity and readability.

GD203 week 8 already told you the good news. If you divide every value in the game by the same factor `d`, every ratio is unchanged. Time to kill, time to die, the power gap between two players and the gap between a player and a boss all survive. A uniform squish is a change of units, like measuring in kilometres instead of metres.

The rest of this lecture is about why real squishes are not uniform, and what that costs.

## 2. Worked example: why a squish has to bend the past

### The hook

In The War Within (2024 to 2026), a level-80 World of Warcraft character attacking an ordinary open-world creature from the original 2004 game, The Burning Crusade or Wrath of the Lich King dealt 500 times the damage the same ability did against a creature from Battle for Azeroth or later. Against Cataclysm and Mists of Pandaria creatures the bonus was 250 times, against Warlords of Draenor 100 times, against Legion 10 times, and from Battle for Azeroth onward it was 1 times. Warcraft Wiki lists this table on its "Stat squish" page and explains the reason. Squishes are followed by a damage bonus against creatures from past expansions "to retain the ability to easily solo old content".

Why would a game that divided all its numbers need a 500-times multiplier to undo it? If the squish were a uniform division, GD203 week 8 says no correction would be needed at all. The multiplier table is evidence that the squish divided different eras by different amounts. This worked example shows why it had to.

### The model

A game's numbers come in **eras**: the content of each expansion or tier, with values that grew by a factor `R` per era. Call a typical value of era `e` (say, the health of an ordinary creature) `v_e`. The current era is `E`.

A squish divides each era's values by a **divisor** `d_e`:

```
new value = v_e / d_e
```

**Dynamic range.** The game wants every squished value to land between a smallest readable value `a` and a largest readable value `b`. The smallest bound is about resolution. A creature with 10 health cannot lose 3% of it to a weak attack, because health comes in whole points. The largest bound is about readability and storage.

A single divisor `d` for every era works only if it can fit both ends at once:

```
v_max / b ≤ d ≤ v_min / a
```

That is possible only when

```
v_max / v_min ≤ b / a
```

Read that as: the game's **dynamic range**, the ratio of its biggest value to its smallest, must fit inside the range the display can handle. With growth `R` per era over `n` eras, `v_max / v_min` is at least `R^n`. It grows every era. `b / a` does not. Sooner or later, no uniform divisor exists.

**The bend.** When no single `d` fits, the designer gives older eras smaller divisors, squeezing them less so their numbers stay above `a`. That keeps every era readable. It also changes every ratio between eras. A current-era player with value `p` fighting era-`e` content of value `v_e` had a ratio `p / v_e`. After the squish the ratio is

```
(p / d_E) / (v_e / d_e) = (p / v_e) × (d_e / d_E)
```

Because older eras get smaller divisors, `d_e / d_E < 1`, and the player is relatively weaker against old content than before.

**Compensation.** To restore the old ratio, the game multiplies the player's effect on era-`e` content by

```
m_e = d_E / d_e
```

That is the whole model. A non-uniform squish plus a compensation table of `m_e` is, for player-against-old-content fights, exactly equivalent to a uniform squish. Every symbol: `v_e` typical value in era `e`, `R` growth per era, `a` and `b` the readable range, `d_e` the era's divisor, `p` a current player's value, `m_e` the compensation multiplier.

### Numbers you can check

An invented game has four eras. Creature health grew by `R = 10` per era, from 2,000 to 2,000,000. A current player hits for 400,000. The team wants every creature's health between `a = 1,000` (fine enough resolution) and `b = 10,000` (readable at a glance).

First try one divisor. The dynamic range is `2,000,000 / 2,000 = 1,000`, and the display allows `10,000 / 1,000 = 10`. No uniform divisor works. `d = 200` makes the current era readable and turns era-1 creatures into 10-health scraps. `d = 2` keeps era 1 fine and leaves current creatures at 1,000,000.

So the team bends the squish.

| Era | Old health v_e | Divisor d_e | New health | Old ratio hit / health | New ratio (hit 2,000) | Hits to kill, old → new | Compensation m_e = 200 / d_e |
|---|---|---|---|---|---|---|---|
| 1 | 2,000 | 2 | 1,000 | 200 | 2.0 | 1 → 1 | 100 |
| 2 | 20,000 | 10 | 2,000 | 20 | 1.0 | 1 → 1 | 20 |
| 3 | 200,000 | 50 | 4,000 | 2 | 0.5 | 1 → 2 | 4 |
| 4 (current) | 2,000,000 | 200 | 10,000 | 0.2 | 0.2 | 5 → 5 | 1 |

The player's hit shrinks by the current era's divisor, from 400,000 to 2,000. Every creature's health now sits between 1,000 and 10,000. The current era is untouched: five hits before, five after.

Old content is another story. The overkill ratio against era 1 fell from 200 to 2, a factor of 100, which is exactly `d_1 / d_4 = 2 / 200`. Era 3 creatures, which the player used to kill in one hit, now take two. A player running old raids for transmogrification notices at once. The compensation column restores every old ratio. Multiply the player's damage against era 3 by 4 and the ratio is back to 2, so one hit kills again.

You can check the table in a few lines of Python.

```python
import math

health = [2_000, 20_000, 200_000, 2_000_000]
divisor = [2, 10, 50, 200]
hit_old = 400_000
hit_new = hit_old / divisor[-1]
for era, (v, d) in enumerate(zip(health, divisor), start=1):
    before = math.ceil(v / hit_old)
    after = math.ceil((v / d) / hit_new)
    print(f"era {era}: new health {v / d:>6.0f}, hits {before} -> {after}, m = {divisor[-1] / d:.0f}")
```

It prints:

```
era 1: new health   1000, hits 1 -> 1, m = 100
era 2: new health   2000, hits 1 -> 1, m = 20
era 3: new health   4000, hits 1 -> 2, m = 4
era 4: new health  10000, hits 5 -> 5, m = 1
```

Look at the shape of the divisors, 2, 10, 50, 200. Old health grew tenfold per era. New health grows about twofold per era. The squish took a tenfold-per-era curve and turned it into a roughly twofold-per-era curve, which is close to taking a cube root of the growth (`10^(1/3) ≈ 2.15`). A uniform squish divides. A bent squish takes a root. And a root changes ratios, which is why the compensation table is needed.

### A visual you can move

Open the interactive. The left panel shows the four eras' creature health before and after the squish, as bars on a logarithmic axis, with the readable band from `a` to `b` shaded. With the default divisors, every "after" bar sits inside the band. The squish looks like a clean success.

The right panel shows, for the same eras, the number of hits a current player needs to kill an ordinary creature: before the squish, after it, and after it with compensation. Here the era-3 bar jumps from 1 to 2. Toggle compensation and it drops back.

Now drag the "uniform" button. All four divisors become 200. The right panel goes flat, every ratio restored and no compensation needed. The left panel shows why nobody ships this: era 1's creatures sink to 10 health, far below the band. Drag the curve slider (which sets every divisor from a power law, section 3) from 1 toward 0 and watch the left panel's bars pull into the band while the right panel's old-era bars rise. You are trading readability of the past against fidelity of the past, and the compensation table is the bill.

### Cross-game recognition

**World of Warcraft, patch 6.0.2 (October 2014).** The first squish. Warcraft Wiki records that items from level 60 through Mists of Pandaria dungeon gear were moved from an exponential scale to a linear one, which is a bend of the kind above, applied to the oldest part of the budget curve (week 4). Blizzard said the squish would not change the relative difficulty of killing creatures or the ability to solo old content. The compensation came as bonus damage against lower-level creatures from past expansions, and the wiki notes the detail that shows it was per era. After the first squish, level-85 creatures in Cataclysm zones took bonus damage, while level-85 creatures in Mists of Pandaria zones did not. Same level, different era, different `m_e`. The table in the hook is the same idea after later squishes (8.0.1 in 2018, 9.0.1 in 2020): 500, 250, 100, 10, 1, stepping down by era.

**World of Warcraft, patch 12.0.0 (January 2026).** The wiki's item level table shows the bend directly in item levels. After the Midnight squish, The War Within's range of 623 to 730 became 86 to 170, a width of 84 levels. Dragonflight's range of 376 to 528, 152 levels wide, became 79 to 85, a width of 6. Everything from Classic through Dragonflight now fits between 38 and 85. The past was squeezed far more than the most recent expansion. The wiki adds that, as of Midnight, the damage bonus applies in all content through Dragonflight. That is the compensation table extending to cover the newly squeezed eras.

**Final Fantasy XIV, patch 6.0 (Endwalker, December 2021).** The wiki's "Value downscaling" page describes a squish that started at level 51 and was not linear, reaching about 20% of the old values at level 80. Levels 1 to 50 were left alone, which is `d = 1` for the oldest era. The developers aimed not to change balance, yet the wiki records that some content ended up slightly harder or easier, and patch 6.3 fixed a FATE (an open-world event, Steel Reign) that had become harder by accident. FFXIV's compensation is different in form and the same in purpose. A buff called Epic Echo lets unrestricted parties fight old duties using the values from before the downscaling. Instead of a multiplier table, it switches old content back to the old units.

**Currency redenomination (Turkey, 2005).** On 1 January 2005, Turkey introduced a new lira equal to one million old lira. Every price, wage and balance was divided by the same `d = 1,000,000` on the same day, so no price ratio changed. That is the uniform squish of GD203 week 8, done by a whole country. It worked because the dynamic range of prices at the time fit inside the new units. Games reach for the bent squish exactly when that stops being true.

Four cases, one model. When you meet a squish, ask what divisor each era got, and where the game pays the compensation `m_e`.

### Eyes-open design judgment

- **A uniform squish is the only one that is balance-neutral.** Use it whenever the dynamic range fits. Check `v_max / v_min` against `b / a` before you design anything more clever.
- **A bent squish is a balance patch to all old content.** Every era with `d_e ≠ d_E` has a ratio change of `d_e / d_E`. Either you ship the full compensation table `m_e`, or you accept that old content got harder, and you test it. FFXIV's Steel Reign FATE is what the untested case looks like.
- **Compensation is not free.** A table of per-era multipliers is a rule every designer, tooltip and theorycrafter must remember. WoW's hook table is invisible on tooltips, so players meet it only as "old content feels easy". Echo-style compensation, which swaps back to old values, keeps old content exact but means two sets of numbers live in the game.
- **You can change a ratio on purpose, in the same patch.** Section 4 shows WoW did in 2014. That is fine. Write it down as a balance change, not as part of the squish, so nobody later mistakes it for a side effect.

## 3. How long a squish lasts

A squish does not stop growth. If numbers grow by `R` per year and you divide by `d`, the numbers are back where they started after

```
T = ln d / ln R
```

years. Call `T` the squish's **headroom**. It is MA101 week 5's "how many levels until" question in time units.

Final Fantasy XIV gives a check. Its downscaling reduced level-80 values to about 20%, so `d ≈ 5`. The wiki notes that by patch 7.2 (25 March 2025) current gear already gave stats above the pre-downscaling maximum. From 7 December 2021 to 25 March 2025 is about 3.3 years, so the implied growth is at least `R ≈ 5^(1/3.3) ≈ 1.63` per year.

| Divisor d | Headroom at R = 1.3 per year | at R = 1.63 | at R = 2 |
|---|---|---|---|
| 5 | 6.1 years | 3.3 years | 2.3 years |
| 25 | 12.3 years | 6.6 years | 4.6 years |
| 100 | 17.6 years | 9.4 years | 6.6 years |

Headroom grows only with the logarithm of the divisor. Squishing four times harder (25 to 100) buys 2.8 extra years at `R = 1.63`. At some point a bigger squish costs more readability at the bottom than it buys at the top, which is the dynamic-range limit from section 2 again.

Storage limits follow the same arithmetic. Moving WoW's health from a 32-bit integer (ceiling about `2.1 × 10^9`) to a 64-bit double (exact integers up to `2^53 ≈ 9.0 × 10^15`, the limit the wiki quotes from a Blizzard developer's post) raised the ceiling by a factor of about 4 million. From Ra-den's 1.5 billion, at a hypothetical `R = 2` per year, the old ceiling was half a year away and the new one about 22 years away. A storage change buys headroom for the engine. It does nothing for readability, which is why WoW still squished again in 2018, 2020 and 2026.

The design lesson is that growth rate, not the squish, sets the calendar. Week 2's creep per tier and week 4's budget curve decide `R`. If you want squishes to be rare, lower `R`. If you accept `R`, plan the next squish when you plan the expansion, instead of discovering it when an integer wraps.

## 4. Is your formula squish-safe?

A uniform squish preserves ratios only for formulas where every quantity is divided together. Call a formula **squish-safe** if dividing all its inputs by `d` divides its output by `d` (or leaves it unchanged, for a ratio like mitigation). Test each formula with that question. Four things break it.

**Constants that are not squished.** MMO303 week 2's armor formula is `A / (A + K)`. Divide armor `A` by 25 and forget `K`, and a player with `A = K`, who took half damage before, now has `A / (A + 25A) = 1/26`, about 4% mitigation. Every constant that shares units with a squished stat must be divided too. That includes level-based constants such as classic WoW's `400 + 85 × level`.

**Floors.** Warcraft Wiki notes that boss-level creatures' damage against much stronger players is reduced down to a minimum of one point. A floor of 1 is a constant. Squish everything by 20 and a 7-damage hit becomes 0.35, which the floor raises to 1, almost three times what it should be. Any `max(1, ...)` in a formula needs checking after a squish.

**Rounding.** Whole-number values lose precision when divided.

| Old tick | Divided by 20 | Rounded | Relative error |
|---|---|---|---|
| 3 | 0.15 | 0 | −100% |
| 7 | 0.35 | 0 | −100% |
| 12 | 0.60 | 1 | +67% |
| 45 | 2.25 | 2 | −11% |
| 1,000 | 50.0 | 50 | 0% |

Small values are the ones that break. This is the resolution bound `a` from section 2 again, seen from a single formula. Damage-over-time ticks, small heals and trickle regeneration are the usual casualties.

**Deliberate asymmetry.** Sometimes a squish divides two quantities by different amounts on purpose. Warcraft Wiki quotes a Blizzard developer on the 2014 squish: numbers went to about 4% of their old values, except player health, which went to about 8%. Damage was divided by about 25 and player health by about 12.5. In GD203 week 4's terms, time to die is health over incoming damage per second, so every player's time to die doubled. Blizzard's stated aim was less burst, making damage and healing less spiky. That is a balance change riding along with a squish. It is fine when intended. It is a bug when it comes from a forgotten constant.

A practical check before any squish: list every formula, mark each constant with its units, and run the old and new versions side by side on a sample of fights from every era. Any ratio that moves by more than rounding is either on your intended-changes list or a bug.

## 5. Labels and values

Item level is a label, as week 2 and week 4 stressed. A squish can act on labels, on values, or both, and the difference matters.

Warcraft Wiki's squish overview makes the distinction explicit. Patch 6.0.2 squished stats but not item levels: an item kept its item level and got a smaller stat budget. Patches 8.0.1, 9.0.1 and 12.0.0 squished item levels directly. Patch 9.0.1 also squished character levels, from 120 to 50, with a mapping table that sends two or three old levels onto each new level for most of the range.

- **Squishing values** (stats, health, damage) is what fixes storage and readability. It is where section 4's safety checks apply.
- **Squishing labels** (item levels, character levels) fixes nothing by itself. It shortens the numbers players compare, resets week 2's chart, and lets week 4's ladders start from small numbers again. It also merges labels. When 9.0.1 mapped levels 2 to 4 onto new level 2, three different old levels became one, so any content or reward gated on those old levels had to be re-gated.

Keep the two separate in your plan. A label squish is a user-interface and content-gating project. A value squish is a balance project.

## In-class activity (25 minutes)

In pairs, plan the squish for a fictional MMO with five eras. Typical creature health by era is 800; 6,000; 45,000; 340,000; 2,600,000. The current player hits for 520,000. Your readable band is 500 to 20,000.

1. Compute the dynamic range and decide whether a uniform divisor exists. If it does, find the range of valid `d`.
2. If not, choose one divisor per era so every era lands in the band. Aim for new health that still grows from era to era.
3. Build the compensation table `m_e` and check that current-era hits to kill are unchanged.
4. Your lead wants player health to squish half as much as damage, as WoW did in 2014. What happens to time to die? Name one encounter type this helps and one it hurts.

Expected output: divisors, a before/after/compensated hits table, and two sentences on the health change.

## Common misconceptions

- **"A squish is a balance-neutral find-and-replace."** Only a uniform squish is. Any era, stat or constant divided by a different amount changes a ratio, and the game has to compensate or accept the change.
- **"Old content felt easy before the squish and still does, so the squish didn't touch it."** It may feel the same because a compensation table is doing the work. Remove the table and the bend shows.
- **"A bigger squish buys a lot more time."** Headroom is `ln d / ln R`. Dividing four times harder adds a fixed amount of time, not four times as much.
- **"Moving to 64-bit numbers removes the need to squish."** It removes the overflow problem. Readability, resolution and systems built on raw values (threat caps, for example) remain.

## Check yourself

1. A game's smallest meaningful creature health is 300 and its largest is 9,000,000. The display wants values between 100 and 50,000. Does a uniform divisor exist? If so, give its range.
2. In the section 2 table, the team changes era 2's divisor from 10 to 40. What is era 2's new health, its new hits to kill, and its compensation multiplier?
3. Numbers in a game grow by 1.8 per year. The team squishes by 40. How many years until the numbers are back to their old size?
4. A formula is `damage = max(5, attack − defense)`. The team divides attack and defense by 10 and leaves the 5. For attack 120 and defense 100, compute damage before and after, and explain the ratio change.
5. WoW's 2014 squish divided damage by about 25 and player health by about 12.5. A fight where a player survived 6 seconds under a boss's damage before the squish: how long do they survive after it, if nothing else changed?

<details>
<summary>Answers</summary>

1. Dynamic range `9,000,000 / 300 = 30,000`. Display range `50,000 / 100 = 500`. No uniform divisor exists. (Check: `d` would need to be at least `9,000,000 / 50,000 = 180` and at most `300 / 100 = 3`.)
2. New health `20,000 / 40 = 500`, which is below the band's lower edge of 1,000. The ratio is `2,000 / 500 = 4`, so it is still one hit. The compensation is `m_2 = 200 / 40 = 5`, and `4 × 5 = 20` restores the old ratio.
3. `T = ln 40 / ln 1.8 = 3.689 / 0.588 ≈ 6.3` years.
4. Before: `max(5, 20) = 20`. After: `max(5, 12 − 10) = max(5, 2) = 5`. The correct squished value is 2, so the floor makes the hit 2.5 times too strong. The floor is a constant that was not squished.
5. Time to die is health over damage per second. Health is divided by 12.5 and damage by 25, so time to die doubles, to 12 seconds.

</details>

## Lab / assignment hook

[Lab 05, the squish planner](../labs/lab05.md). You receive a small game's era data and formula list, test each formula for squish safety, choose per-era divisors that fit a readable band, generate the compensation table, and verify with a battery of sample fights that current-era outcomes are unchanged and old-era outcomes are restored. The results feed the progression analysis assignment (30%).

## Sources

- Warcraft Wiki, "Stat squish" (current, updated for Midnight, accessed September 2026). Squishes in patches 6.0.2, 8.0.1, 9.0.1 and 12.0.0; stats-only vs item-level squishes; item level table after each squish (The War Within 623 to 730 becoming 86 to 170, Dragonflight 376 to 528 becoming 79 to 85); bonus damage table by expansion for a level-80 character in The War Within (500, 250, 100, 10, 1); damage bonus through Dragonflight as of Midnight; 32-bit health and Ra-den's roughly 1.5 billion health; move to 64-bit doubles in Legion with a 2^53 limit (Blizzard developer's post, May 2016); patch 6.0.2 moving old items from an exponential to a linear scale; Cataclysm vs Mists of Pandaria creatures after the first squish; minimum damage of one point; level squish mapping in 9.0.1. https://warcraft.wiki.gg/wiki/Stat_squish
- Celestalon (Blizzard), posts on Twitter, March and June 2014, as quoted by Warcraft Wiki "Stat squish". Numbers squished to about 4%, player health to about 8%, for less burst.
- Warcraft Wiki, "Patch 6.0.2" (14 October 2014), "Patch 8.0.1" (17 July 2018), "Patch 9.0.1" (13 October 2020), "Patch 12.0.0" (20 January 2026, stat and item squish for clarity and readability, power relative to enemies unchanged). https://warcraft.wiki.gg/wiki/Patch_12.0.0
- Final Fantasy XIV Online Wiki (consolegameswiki), "Value downscaling" (Endwalker, patch 6.0). Reasons cited by Naoki Yoshida (overflow, enmity caps, long flying text, bosses near 440,000,000 HP in patch 5.5); nonlinear from level 51, about 20% at level 80; Steel Reign FATE fixed in patch 6.3; Epic Echo in unrestricted parties; stats above the old maximum by patch 7.2. https://ffxiv.consolegameswiki.com/wiki/Value_downscaling
- Final Fantasy XIV Online Wiki, "Patch 6.0" (7 December 2021) and "Patch 7.2" (25 March 2025). Release dates.
- Wikipedia, "Turkish lira" (accessed September 2026). Redenomination removing six zeros, introduced 1 January 2005. https://en.wikipedia.org/wiki/Turkish_lira

## Interactive spec: examples/w05-squish-map.html

**Insight the visual must make obvious:** a squish that makes every era's numbers readable must divide older eras by less, and that silently makes old content harder unless a compensation multiplier `m_e = d_E / d_e` is applied. A uniform squish keeps every ratio but cannot fit the numbers.

**Data (defaults).** Four eras with creature health `v = [2000, 20000, 200000, 2000000]`, current player hit `h = 400000`, readable band `a = 1000`, `b = 10000`, divisors `d = [2, 10, 50, 200]`.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (left first).

- **Left panel, "The numbers".** For each era, two horizontal bars on a log10 axis from 1 to 10^7: "before" (`v_e`, muted colour) and "after" (`v_e / d_e`, accent colour). Shade the band `[a, b]`. Any "after" bar outside the band gets a warning marker and a label "too small to resolve" or "too big to read". Print each new value next to its bar, rounded to whole numbers. Above the panel print "Dynamic range: v_max / v_min = X; band allows b / a = Y" and "Uniform squish possible: yes/no".
- **Right panel, "Hits to kill an ordinary creature".** Grouped bars per era: before (`ceil(v_e / h)`), after (`ceil((v_e / d_e) / (h / d_E))`), after with compensation (`ceil((v_e / d_e) / (m_e × h / d_E))`, which equals "before"). Show the compensation `m_e` under each group. Highlight any era where "after" differs from "before".

**Controls (keyboard accessible, values visible).**
- Mode: "Per-era divisors" (default) or "Curve".
- Per-era mode: four number sliders for `d_1..d_4` on a log scale from 1 to 1,000 (defaults 2, 10, 50, 200).
- Curve mode: slider `p` from 0.2 to 1.0, step 0.01, default 0.33. New values are `v_e^p × (b / v_max^p)`, so the top era lands exactly at `b`; the implied divisor is `d_e = v_e / new_e`, shown in a small table.
- Button "Uniform": sets every divisor to `d_E` (200 by default) in per-era mode, or `p = 1` in curve mode.
- Toggle "Apply compensation".
- Number inputs for `a`, `b` and `h`.

**Exact test values.**
- Defaults: new health 1000, 2000, 4000, 10000; hits before 1, 1, 1, 5; hits after 1, 1, 2, 5; compensation 100, 20, 4, 1; dynamic range 1000, band allows 10, uniform possible: no.
- Uniform (all 200): new health 10, 100, 1000, 10000 (eras 1 and 2 flagged too small); hits after 1, 1, 1, 5; compensation all 1.
- Curve mode at `p = 1/3` (add a "1/3" preset button, since the slider step is 0.01): new health 1000, 2154, 4642, 10000; hits after 1, 2, 3, 5; compensation (implied divisors 2, 9.28, 43.1, 200) 100, 21.5, 4.64, 1.
- Era 2 divisor 40: new health 500 (flagged too small), hits after 1, `m_2 = 5`.

**First screen:** the defaults, with the era-3 group in the right panel highlighted ("1 hit before, 2 after"). Caption: "Every number now fits. Old content quietly got harder."
