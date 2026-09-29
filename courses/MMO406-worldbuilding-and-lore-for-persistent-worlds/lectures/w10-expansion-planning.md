# MMO406 · Week 10 — Expansion Planning

**Why this matters:** Every expansion's big reveal works better if players met it earlier, and every early hint is a promise your team may not keep. Plant too late and the headline villain "comes out of nowhere". Plant too early and the plan changes under you, leaving a dangling thread or forcing a retcon. This week gives you a way to decide how far ahead to foreshadow, and a one-page expansion brief that makes the decision visible in your bible.

**You will be able to:**
- Compute the expected value of a foreshadowed payoff from its lead time, the value of each cycle of exposure, the cost of a broken promise and your team's plan-change rate.
- Derive the best lead time `d* = −1/ln(1 − ρ) − D/v` and explain why a public announcement shortens it.
- Critique how World of Warcraft, Final Fantasy XIV and Guild Wars 2 chose their planning horizons, in the terms of the model.
- Design a three-expansion arc for your own bible, with a stakes plan and a one-page brief per expansion.

**Before class:** Wolf, *Building Imaginary Worlds* (2012), chapter 4, "More Than a Story: Narrative Threads and Narrative Fabric" (about 20 pages). Wikipedia, "Final Fantasy XIV: Dawntrail", the Development section (10 minutes). Reread section 2 of [week 1](w01-setting-as-system.md) and the "in the dark" rule in section 3 of [week 4](w04-history-and-timelines.md).

**Prerequisites from earlier courses:** [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (weighting outcomes by their chance). [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (why a per-step survival `s` becomes `s^d` over `d` steps). [MMO306 week 13, content budgets and cadence planning](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w13-content-budgets-and-cadence-planning.md) (how many teams and months an expansion takes; we take the dates as given). [MMO406 week 1](w01-setting-as-system.md) (the tension ledger: how many stories a setting can supply) and [week 7](w07-lore-delivery-in-mmos.md) (who in today's population still knows a beat).

**Interactive:** [w10-foreshadow-horizon.html](../examples/w10-foreshadow-horizon.html). Keep it open during section 2.

---

## 1. What an expansion plan has to decide

Week 1 asked how many stories your setting can supply. Week 7 asked who is still around to remember them. Expansion planning asks a third question. **In what order do you promise things, and how far ahead?**

An expansion in a live MMO usually arrives every eighteen months to two and a half years. Between expansions come patches, seasons and events. Your bible has to answer, for each future expansion:

1. **The headline.** The threat, place or mystery the box art and trailer sell.
2. **The stakes.** How much of the world is at risk, and for whom.
3. **The lead-in.** Where players first met the headline, and how many releases before it arrived.
4. **What it closes and what it opens.** Which hooks it pays off, and which new ones it plants for later.

The first two are creative choices that the rest of this course has prepared you to make. The third is a planning choice with numbers behind it, and it is where most teams go wrong. Some never plant their headline, so it arrives cold. Others plant a detailed promise years ahead and then change their minds.

Two terms for the rest of the lecture. A **hook** is anything you show players that points at a future story: a sealed door, a named but unseen enemy, a prophecy, a faction that vanishes, a map edge with a ship sailing toward it. A **payoff** is the release where that story is told. The **lead time** `d` is the number of expansion cycles between the hook's first appearance and its payoff. A cycle is one expansion plus the patches that follow it.

## 2. Worked example: how far ahead to foreshadow

### The hook

In 2007, World of Warcraft: The Burning Crusade made the draenei a playable race. Players had barely met them. Earlier Warcraft games had mentioned them, and a few corrupted draenei appeared in Warcraft III's expansion, but the noble, crystal-themed exiles of The Burning Crusade were new. In a 2009 interview, game director Tom Chilton said Blizzard learned from this. Players found the draenei harder to "get" because they came out of nowhere, while blood elves, whose high-elf ancestors players had known for years, were easier. His lesson was to seed a future race in the world, even in a small way, before making it playable.

The same expansion carried a second lesson in the other direction. The draenei's new history contradicted what the Warcraft III manual had said about the eredar four years earlier. The lead writer, Chris Metzen, publicly admitted he had forgotten that text and chose to keep the new version. Week 11 covers that kind of repair. For now, notice the pair. **A payoff with no lead-in lands cold. A hook with a long lead-in gives the plan more time to change.** Somewhere in between is a best lead time, and you can compute it.

### The model

Take one hook, planted `d` cycles before its payoff.

```
s     = 1 − ρ
E(d)  = s^d × v × d  −  (1 − s^d) × D
d*    = −1 / ln(s)  −  D / v          (continuous best lead time, floored at 0)
```

- `d` is the **lead time**, in expansion cycles, from first appearance to payoff. `d = 0` is a surprise: the hook appears in the same expansion that pays it off.
- `v` is the **exposure value**: how much a payoff gains from each cycle in which players lived with the hook. It stands for recognition, speculation, attachment, and the feeling that the world was consistent all along. Chilton's lesson is that `v` is positive.
- `ρ` (rho) is the **plan-change rate**: the chance that, in any one cycle, the plan for this hook changes. Teams turn over, a patch is badly received, a business decision moves a zone, someone has a better idea. `s = 1 − ρ` is the chance the plan survives one cycle, and `s^d` is the chance it survives all `d`.
- `D` is the **broken-promise cost**, paid when the plan changes after the hook is planted. The hook dangles, or it must be retconned, or players who theorized about it for years feel cheated. It is in the same units as `v`.
- `E(d)` is the expected value of planting the hook `d` cycles ahead, compared with not foreshadowing at all.

Read `E(d)` as two outcomes weighted by their chances, exactly as in MA102 week 4. With probability `s^d` the plan holds and the payoff collects `v × d`. With probability `1 − s^d` the plan breaks and you pay `D`.

The best lead time comes from setting the derivative of `E(d)` to zero. The first term's derivative is `s^d × (v + v × d × ln s)`, the second's is `s^d × D × ln s`. Setting their sum to zero gives `v + (v × d + D) × ln s = 0`, which rearranges to the formula for `d*`. Two things follow from it straight away:

- Only `ρ` and the ratio `D / v` matter. Doubling both costs and values changes nothing.
- `−1 / ln(1 − ρ)` is close to `1 / ρ` for small `ρ`. **A hook that costs nothing to break should be planted about `1 / ρ` cycles ahead. Each unit of breakage cost, measured in cycles of exposure value, pulls that in by one cycle.**

The model is crude on purpose. Real exposure value probably saturates (the tenth cycle of hints adds less than the second), and plan changes are not independent coin flips. Section 3 covers both. The simple version has one job: to show that your team's stability, not your ambition, sets how far ahead you can promise.

### Numbers you can check

Fix `v = 1` and `D = 2`, so a broken promise costs as much as two cycles of exposure earn. Compare three teams.

| Lead time `d` | `E(d)`, stable team `ρ = 0.1` | `E(d)`, typical team `ρ = 0.2` | `E(d)`, volatile team `ρ = 0.3` |
|---|---|---|---|
| 0 | 0.00 | 0.00 | 0.00 |
| 1 | 0.70 | 0.40 | 0.10 |
| 2 | 1.24 | 0.56 | −0.04 |
| 3 | 1.65 | 0.56 | −0.29 |
| 4 | 1.94 | 0.46 | −0.56 |
| 5 | 2.13 | 0.29 | −0.82 |
| 6 | 2.25 | 0.10 | −1.06 |
| 7 | 2.30 | −0.11 | −1.26 |
| 8 | 2.30 | −0.32 | −1.42 |
| `d*` (continuous) | 7.49 | 2.48 | 0.80 |

Check the typical team at `d = 2` by hand. `s = 0.8`, `s^2 = 0.64`. The plan holds with probability 0.64 and earns `1 × 2 = 2`, worth `1.28`. It breaks with probability `0.36` and costs 2, worth `0.72`. `E = 1.28 − 0.72 = 0.56`. The formula gives `d* = −1 / ln 0.8 − 2 = 4.48 − 2 = 2.48`, and the table peaks between 2 and 3, as it should.

Three things stand out.

First, the curves are humps. Every team gains from some foreshadowing, and every team loses if it foreshadows too far. The value if the plan holds, `v × d`, climbs forever. The expected value does not.

Second, the optimum moves a lot with `ρ`. Going from a plan-change rate of 10% to 20% cuts the best lead time from about seven and a half cycles to two and a half. At 30% the best you can do is barely positive at one cycle. A volatile team should foreshadow very little, and whatever it does plant should be cheap to break.

Third, `D` is something you choose. Now hold the typical team at `ρ = 0.2` and vary how specific the hook is.

| Hook type | Example | `D` | `d*` | Best integer `d` and `E` |
|---|---|---|---|---|
| Vague | "Something stirs beneath the sea" | 0.5 | 3.98 | 4, `E = 1.34` |
| Named | A villain's name and face in a cutscene | 2 | 2.48 | 2 or 3, `E = 0.56` |
| Announced | A dated three-expansion roadmap on stage | 4 | 0.48 | 0 or 1, `E = 0.00` |

A vague hook can be planted twice as far ahead as a named one, and it earns more in expectation, because breaking it costs little. This is week 4's precision gradient applied to the future. A reserved gap "in the dark" is a hook with a low `D`.

The same table in code, which you will extend in the lab:

```python
import math

def expected_value(d, v, D, rho):
    """Expected value of a payoff foreshadowed d cycles ahead."""
    s = 1 - rho
    return s**d * v * d - (1 - s**d) * D

def best_horizon(v, D, rho):
    """Continuous optimum d* = -1/ln(s) - D/v, never below 0."""
    return max(0.0, -1 / math.log(1 - rho) - D / v)

for rho in (0.1, 0.2, 0.3):
    row = [f"{expected_value(d, 1, 2, rho):.2f}" for d in range(0, 9)]
    print(f"rho={rho}: {' '.join(row)}  d*={best_horizon(1, 2, rho):.2f}")
```

It prints:

```
rho=0.1: 0.00 0.70 1.24 1.65 1.94 2.13 2.25 2.30 2.30  d*=7.49
rho=0.2: 0.00 0.40 0.56 0.56 0.46 0.29 0.10 -0.11 -0.32  d*=2.48
rho=0.3: 0.00 0.10 -0.04 -0.29 -0.56 -0.82 -1.06 -1.26 -1.42  d*=0.80
```

### A visual you can move

Open the interactive. The left panel shows what a writers' room sees when it pitches a long arc: the value if the plan holds, `v × d`, a straight line rising to the right. The right panel shows the same hook in expectation, `E(d)`, with the plan-survival curve `s^d` drawn faintly behind it. Drag the lead-time slider to 8 with `ρ = 0.1` and both panels agree the long arc is good. Now move `ρ` to 0.2. The left panel does not change at all. The right panel's hump slides left and the point at `d = 8` drops below zero. Then switch the hook type from "named" to "vague" and watch the hump move back out. The pitch looks the same whatever your team's stability. The expected value does not.

### Cross-game recognition

**Guild Wars 2 (2012 to 2022, and after).** At launch, the game's lore named five awakened Elder Dragons, one of them known only as the Deep Sea Dragon. The story never gave its name, and it stayed a vague hook for almost a decade until End of Dragons (February 2022) revealed it as Soo-Won. That is a low-`D` hook with a very long lead time, and it paid off. Mordremoth went the other way. It was unknown at launch, awakened at the end of Living World Season 1 (March 2014), and headlined Heart of Thorns (October 2015), a lead time of about one cycle. After End of Dragons, ArenaNet announced that future storylines would be self-contained, with characters and plots introduced and concluded within their own expansion. In the model, that is a deliberate choice of `d ≈ 0`. It gives up exposure value to remove broken-promise risk from a release model that was changing at the same time. (Week 1 counted the same dragons as a stock of tensions. Here we care about when each one was first shown.)

**World of Warcraft (2023 onward).** At BlizzCon in November 2023, Blizzard announced three expansions at once as the Worldsoul Saga: The War Within (released August 2024), Midnight (released March 2026) and The Last Titan. An on-stage, named, three-expansion roadmap is the "announced" row of the table, with a high `D`, because players and press will hold the studio to it. The model says that commitment only pays if the team's `ρ` is low for that stretch. Announcing is a bet on your own stability. Two of the three have shipped as announced, so far.

**Final Fantasy XIV (2013 to 2024).** The Hydaelyn and Zodiark arc ran from A Realm Reborn (2013) to Endwalker (December 2021), about five cycles, with its core mysteries planted in the first one. FFXIV kept one director and producer, Naoki Yoshida, across the whole arc, which is about as low a `ρ` as a live game gets. The long horizon matched the stable team. When Dawntrail (July 2024) opened the next arc, Yoshida described it as the start of a "season two" and said he hoped to lay the groundwork for another ten years. That is a team choosing a long horizon again, and planting early.

**The draenei, once more.** The Burning Crusade's draenei were close to `d = 0`: a headline race with almost no lead-in. Chilton's fix, seeding a race before it becomes playable, is a statement that `v` is large for playable races, because players will spend hundreds of hours as them. A large `v` pushes `d*` outward, since `D / v` shrinks.

Four cases, one trade-off. Guild Wars 2 moved to `d ≈ 0` when it changed its release model. World of Warcraft raised `D` on purpose by announcing. Final Fantasy XIV used a stable team to afford a long `d`. The draenei show what `d = 0` costs when `v` is high.

### Eyes-open design judgment

- **Estimate `ρ` from your own history, not your hopes.** Take the last bible or roadmap your team wrote. Count the hooks planned for the next cycle and how many paid off as planned. If 4 of 20 changed, `ρ ≈ 0.2`. A new studio with no history should assume at least that.
- **Lower `D` before you plant far.** Plant vague hooks early and specific ones late. A sealed door, a ship that never returns, or a rumor in a tavern can be paid off many ways. A named villain with a face, a voice actor and a date cannot.
- **Keep `D` low by writing hooks with more than one exit.** A prophecy that could fit two different expansions has a lower breakage cost than one that fits only one. Ambiguity is a planning tool, not only a style.
- **Announcements are a separate decision from foreshadowing.** In-game hooks are read by players. Roadmaps are read by players, press and investors, so they carry a higher `D`. Announce only what your `ρ` supports.
- **Don't use `d = 0` everywhere.** Self-contained expansions are easy to plan and easy to enter. They also give up the recognition that makes a payoff land, and they leave week 7's knowledge share with nothing to accumulate. Use surprise for the stories that benefit from surprise.

### Check yourself (worked example)

1. A team has `ρ = 0.15`, `v = 1`, and a named villain with `D = 1.5`. Compute `d*` and `E(d)` at the two nearest whole numbers.
2. Your producer wants to announce a three-expansion arc on stage (`D = 4`). What plan-change rate would make `d* = 3` for that announcement?

<details>
<summary>Answers</summary>

1. `s = 0.85`, `−1 / ln 0.85 = 6.15`, so `d* = 6.15 − 1.5 = 4.65`. `E(4) = 0.522 × 4 − 0.478 × 1.5 = 2.088 − 0.717 = 1.37`. `E(5) = 0.444 × 5 − 0.556 × 1.5 = 2.219 − 0.834 = 1.38`. Plant five cycles ahead, though four is almost as good.
2. You need `−1 / ln s = 3 + 4 = 7`, so `ln s = −1/7`, `s = 0.867`, `ρ ≈ 0.13`. The team would have to keep 87% of its plans each cycle.

</details>

## 3. Where the simple model breaks

**Exposure saturates.** The model gives each cycle of exposure the same value. In practice the first cycle, when players first meet the hook, is worth the most, and later cycles add less unless the hook grows. A saturating value such as `v × (1 − e^(−d/τ))` moves the optimum inward. Treat the linear `d*` as an upper bound.

**Plan changes cluster.** A new creative director or a failed expansion changes many hooks at once. Independent coin flips understate the chance that everything breaks together. That argues for spreading your hooks across different future expansions, so a single change does not break them all.

**Not all players see every cycle.** Exposure value only accrues for players who were there. Week 7's knowledge share `K(m)` falls as the population turns over, so a hook planted long ago may have been seen first-hand by a small share of the people present at its payoff. Long lead times need re-planting: a scene one cycle before the payoff that reminds everyone. That reminder resets exposure for newcomers without raising `D`.

**Breaking a promise is not always a loss.** Sometimes the changed plan is better. Metzen argued the new draenei history was stronger than the one it replaced. `D` measures the cost of the break itself (the retcon work, the theorists' disappointment), not the quality of the new idea.

## 4. Stakes: the other axis of an expansion plan

Lead time is about when players meet a threat. Stakes are about how big it is. Every expansion sits somewhere on a **stakes ladder**:

| Rung | At risk | Typical headline |
|---|---|---|
| 1 | A person or a family | A succession, a missing sibling, a personal debt |
| 2 | A town or guild | A siege, a plague, a betrayal |
| 3 | A region or nation | A war, an invasion, a collapse |
| 4 | The world | A world-ending creature or cataclysm |
| 5 | Everything | The gods, the afterlife, the fabric of reality |

Most MMO sagas climb. Each expansion has to feel bigger than the last, and a climb of one rung per expansion reaches the top in four or five cycles. The trouble starts at the top. After the fabric of reality, a return to a regional war can feel like a letdown, so teams either invent a rung above the top or step down on purpose.

Final Fantasy XIV stepped down on purpose. After Endwalker's universe-scale finale, Dawntrail was designed, in the development team's words, as a "summer vacation" for the player's character. It centers on a contest of succession for the throne of Tuliyollal on a new continent. Yoshida said it was important to reset the stakes from a universe-ending threat to a more personal one. The expansion was received well, though less warmly than its two predecessors. That result is consistent with the risk of stepping down. Players who arrived for the climb may miss it. The step-down still bought the game room to climb again, and the Dawntrail patch story has already begun to plant a world-scale threat for the next climb.

Three ways to keep stakes from running out:

- **Plan the descent in advance.** Put the step-down in the bible at the same time as the climax, so it reads as a new season, not as a loss of nerve.
- **Change the kind of stakes, not only the size.** Moving from "the world will end" to "the person you've traveled with will lose her home" is a change of kind. Players feel it as different, not as smaller.
- **Run two ladders.** A personal story at rung 1 or 2 alongside a world story at rung 4 lets each expansion climb one ladder while resting the other.

Stakes connect back to the model. High-rung threats are usually specific and named, with a high `D`, and they take long lead times to feel earned. Plan the top of the ladder when your team is stable. Use low rungs, with low `D` and short lead times, when it isn't.

## 5. The expansion brief

Every future expansion gets a one-page brief in your bible. It is the document that turns the model into a plan that writers, level designers and producers can check. A brief holds:

| Field | Content | Checked against |
|---|---|---|
| Headline | One sentence: the threat, place or mystery | Week 1 tension ledger (is there stock for it?) |
| Stakes rung | 1 to 5, and the previous expansion's rung | Section 4 |
| Lead-in hooks | Each hook, where it was first shown, its type (vague, named, announced) and `d` | Section 2: is `d` within one of `d*` for the hook's `D`? |
| Pays off | Hooks this expansion closes | The hook table |
| Plants | New hooks, each with a target payoff expansion and a type | Next brief's lead-in |
| Map | New regions, and which reserved gaps from week 4 they use | Week 2 geography |
| Factions | Which existing factions it changes, and how | Week 3 |
| Assumed knowledge | What players must already know, and how newcomers learn it | Week 7 retelling rule |
| Escape hatch | For each named hook, one alternative payoff if the plan changes | Keeps `D` down |

The escape-hatch row is the one teams skip. Writing one alternative payoff for each named hook costs an hour, and it lowers `D` because a change of plan now has somewhere to go.

Keep the brief separate from the production schedule. MMO306 week 13 decides when the expansion ships and how many teams build it. The brief decides what it promises and when those promises were first made. When the production date slips, the brief tells you which hooks now have a longer `d` than planned.

## In-class activity (25 minutes)

In groups of three, plan the lead-in for an invented setting's next three expansions. The setting is *Thornmere* from week 4: a lowland kingdom rebuilt after the Drowning, with Princess Ysolde as its young heir.

1. (5 min) Estimate your team's `ρ`. Your studio's last roadmap planned 15 hooks for the next cycle and 5 changed. Compute `ρ` and `−1 / ln(1 − ρ)`.
2. (10 min) Draft one headline per expansion, at stakes rungs you choose. For each, write one hook that will lead into it, and classify the hook as vague (`D = 0.5`), named (`D = 2`) or announced (`D = 4`), with `v = 1`.
3. (5 min) Compute `d*` for each hook. Decide in which expansion (0 = launch, 1, 2) each hook first appears, so that its actual `d` is within one cycle of `d*`.
4. (5 min) Write one escape hatch for your one named hook.

Expected output: a three-row table (headline, rung, hook, type, `d*`, planting expansion), with one escape hatch. With `ρ = 1/3`, `−1 / ln(2/3) = 2.47`. A named hook then gets `d* = 0.47`, so it should appear in the same expansion or one before. Most groups find they must turn a named villain into a vague hook to plant it early.

## Common misconceptions

- **"More foreshadowing is always better."** Only if the plan holds. The value if the plan holds rises forever, but the expected value is a hump, and for a volatile team it peaks at one cycle or less.
- **"Surprise means we didn't plan."** `d = 0` is a legitimate choice with zero broken-promise risk. It is the right choice when `ρ` is high or when the surprise is the point.
- **"A vague hook is a lazy hook."** A vague hook has a low `D`, which is why it can be planted far ahead. Specificity is something you add as the payoff approaches.
- **"The roadmap is marketing, not lore."** A public roadmap is the most expensive hook you can plant, because more people will notice if you break it. Treat it as a hook with a high `D`.

## Check yourself

1. A team with `ρ = 0.25` plants a vague hook with `D = 0` and `v = 1`. What is `d*`? What is `E` at the nearest whole number?
2. Two hooks lead into the same expansion, three cycles away. One is a named villain (`D = 2`), the other a sealed door (`D = 0.5`). With `ρ = 0.2` and `v = 1`, which has higher expected value, and by how much?
3. Your studio doubles the value of exposure (`v = 2`) by making the hook a playable race's homeland, as Chilton recommended. Keep `ρ = 0.2` and `D = 2`. How does `d*` change?
4. A designer says: "Our last expansion topped out at rung 5. The next one must too, or players will be disappointed." Give one plan that avoids both a letdown and an invented rung 6.

<details>
<summary>Answers</summary>

1. `s = 0.75`, `−1 / ln 0.75 = 3.48`, so `d* = 3.48`. `E(3) = 0.4219 × 3 = 1.27`, `E(4) = 0.3164 × 4 = 1.27`. Both round to the same value, so plant three or four cycles ahead.
2. `s^3 = 0.512`. Named: `0.512 × 3 − 0.488 × 2 = 1.536 − 0.976 = 0.56`. Door: `1.536 − 0.488 × 0.5 = 1.536 − 0.244 = 1.29`. The door is worth 0.73 more.
3. `D / v` falls from 2 to 1, so `d* = 4.48 − 1 = 3.48`, up from 2.48. A high-value hook earns the right to be planted earlier.
4. Change the kind of stakes, or run two ladders. For example, keep the world-scale threat alive in patches while the expansion's headline is a personal succession story at rung 1, planned in the bible alongside the climax so it reads as a new season.

</details>

## Lab / assignment hook

[Lab 10, the foreshadowing plan](../labs/lab10.md). You implement the model, run it on a sample three-expansion plan for *Thornmere* that plants several hooks too early or too late, fix the plan, and then write expansion briefs for your own world bible. It feeds the "expansions" chapter of the final world bible (60%).

## Sources

- Warcraft Wiki, "Draenei", sections "Design and retcon". Chris Metzen's statement (Burning Crusade development, about 2006) that the new draenei history contradicted the Warcraft III manual, which he had forgotten, and that Blizzard would keep the new version. Tom Chilton's 2009 interview on seeding races before making them playable, citing W. Yin-Poole, "Blizzard's Tom Chilton on the future of WoW", VideoGamer.com, 3 July 2009. https://warcraft.wiki.gg/wiki/Draenei
- Guild Wars 2 Wiki, "Elder Dragon" (current). Status table listing the Deep Sea Dragon, unnamed until End of Dragons, and a quoted interview in which writer Jeff Grubb notes how little the game had said about it; its reveal as Soo-Won in End of Dragons. https://wiki.guildwars2.com/wiki/Elder_Dragon
- Guild Wars 2 Wiki, "Living World" (current). Season dates (Season 1, January 2013 to March 2014) and End of Dragons (28 February 2022). https://wiki.guildwars2.com/wiki/Living_World
- Wikipedia, "Guild Wars 2" (accessed September 2026). Mordremoth awakened at the end of Living World Season 1; Heart of Thorns (2015); the Elder Dragon Saga concluding in End of Dragons (2022); the announcement that later storylines would be self-contained within each expansion.
- Wikipedia, "World of Warcraft: The War Within" and "World of Warcraft: Midnight" (accessed September 2026). Worldsoul Saga announced at BlizzCon, 3 November 2023; The War Within released 26 August 2024; Midnight released 2 March 2026; The Last Titan announced as the third part.
- Wikipedia, "Final Fantasy XIV: Endwalker" (accessed September 2026). Released 7 December 2021 as the finale of the Hydaelyn and Zodiark arc begun in A Realm Reborn.
- Wikipedia, "Final Fantasy XIV: Dawntrail" (accessed September 2026). Released 2 July 2024; setting in Tural and the succession contest; the "summer vacation" framing; Yoshida's "season two" comment, hope for another ten years, and intent to reset stakes from a universe-ending threat to a personal one; reception compared with Shadowbringers and Endwalker; patch-story setup of a new threat.
- Wolf, M. J. P. (2012). *Building Imaginary Worlds: The Theory and History of Subcreation*. Routledge. Chapter titles checked against the publisher's table of contents (Routledge, September 2026): 1 "Worlds within the World", 3 "World Structures and Systems of Relationships", 4 "More Than a Story: Narrative Threads and Narrative Fabric", 6 "Transmedial Growth and Adaptation", 7 "Circles of Authorship".

## Interactive spec: examples/w10-foreshadow-horizon.html

**The one insight the visual must make obvious:** the pitch for a long arc (value if the plan holds) looks the same for every team, but the expected value is a hump whose peak is set by the team's plan-change rate and the hook's breakage cost. The same lead time can be the best choice for one team and a loss for another.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (left panel on top).

- **Left, "The pitch: value if the plan holds".** A line chart of `v × d` for `d` from 0 to 10 (x axis "lead time, cycles", y axis "value"). A marker at the current lead time. It must not change when `ρ` or `D` change. Fixed y range from −4 to 10 shared with the right panel, so the two are comparable.
- **Right, "Expected value".** A line chart of `E(d)` for `d` from 0 to 10, same axes as the left. Behind it, faint and on a secondary 0-to-1 axis at the right edge, the survival curve `s^d`, labeled "plan still holds". A vertical dashed line at the continuous `d*`, labeled with its value. A horizontal zero line. Points below zero drawn in the warning colour. A marker at the current lead time.
- **Stat row under both panels:** `s`, `s^d`, value if held `v × d`, `E(d)`, `d*` (2 decimals), best whole `d` and its `E`. Numbers to 2 decimals.

**Controls.**

1. **Lead time `d`**, slider 0 to 10, step 1, default 8.
2. **Plan-change rate `ρ`**, slider 0.02 to 0.50, step 0.01, default 0.10.
3. **Hook type**, three-way segmented control: Vague (`D = 0.5`), Named (`D = 2`, default), Announced (`D = 4`). A fourth option "Custom" reveals a `D` slider 0 to 6, step 0.1.
4. **Exposure value `v`**, slider 0.5 to 3, step 0.1, default 1.
5. **Presets** (buttons): "Stable team" (`ρ = 0.1`, Named), "Typical team" (`ρ = 0.2`, Named), "Volatile team" (`ρ = 0.3`, Named), "Vague hook, typical team" (`ρ = 0.2`, Vague).

All controls are native inputs with labels, keyboard operable. An `aria-live` region under the stat row states in one sentence: "At lead time 8, the pitch is worth 8.00 but the expected value is 2.30. Best lead time: 7.49 cycles."

**Formulas.**

```
s    = 1 − ρ
E(d) = s^d × v × d − (1 − s^d) × D
d*   = max(0, −1 / ln(s) − D / v)
best whole d = argmax over d in 0..10 of E(d) (lowest d on ties)
```

**Test values (must match to 2 decimals).**

| `ρ` | `D` | `v` | `d` | `E(d)` | `d*` |
|---|---|---|---|---|---|
| 0.10 | 2 | 1 | 8 | 2.30 | 7.49 |
| 0.20 | 2 | 1 | 2 | 0.56 | 2.48 |
| 0.20 | 2 | 1 | 8 | −0.32 | 2.48 |
| 0.30 | 2 | 1 | 1 | 0.10 | 0.80 |
| 0.20 | 0.5 | 1 | 4 | 1.34 | 3.98 |
| 0.20 | 4 | 1 | 1 | 0.00 | 0.48 |
| 0.15 | 1.5 | 1 | 5 | 1.38 | 4.65 |

**First screen.** Load with the "Stable team" preset and `d = 8`, so both panels show a good long arc. A one-line caption above the panels: "Same pitch, different teams. Move the plan-change rate." The moment a student moves `ρ` to 0.2, the right panel's point at `d = 8` drops below zero while the left panel stays still.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css` inline, light and dark themes, `prefers-reduced-motion` respected (no animated curve transitions when set). No game art or logos; charts only.
