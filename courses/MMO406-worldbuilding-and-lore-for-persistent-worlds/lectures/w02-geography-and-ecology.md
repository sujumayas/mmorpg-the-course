# MMO406 · Week 02 — Geography and Ecology

**Why this matters:** In an online world, the map decides who meets whom. Where you put ore, timber and grazing land sets the trade routes, the contested borders and the reasons players leave home. A map drawn only to look good produces a world where nobody needs to travel. A map drawn as a system gives every region a reason to need its neighbours, and gives your writers conflicts that renew themselves.

**You will be able to:**
- Compute the share of recipes a region can make from local resources, given how many resource types exist, how many the region holds and how many a recipe needs.
- Design a resource distribution for a set of regions that meets a target for local self-sufficiency and guarantees every recipe can be made somewhere.
- Critique shipped resource maps (Albion Online, EVE Online) and a historical one (Bronze Age tin) in the same terms.
- Check a zone's spawn table for ecological plausibility with the ten percent rule, and turn an implausible result into a story hook instead of a bug.

**Before class:** Wolf, *Building Imaginary Worlds* (2012), chapter 3, "World Structures and Systems of Relationships," the parts on maps and on the natural world. Reread [MMO301 week 3](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w03-ultima-online-the-simulation-dream-and-its-limits.md), section 3, on why Ultima Online's planned ecology never started.

**Prerequisites from earlier courses:** [MMO406 week 1, setting as system](w01-setting-as-system.md) (structural tensions and refill). [GD201 week 9, open-world structure and POI density](../../GD201-level-and-world-design/lectures/w09-open-world-structure-poi-density.md) (how far apart things should be). [GD201 week 12, spawn design and contested resources](../../GD201-level-and-world-design/lectures/w12-spawn-design-and-contested-resources.md) (the geometry of fighting over one node). [MMO401 week 9, regional economies and logistics](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w09-regional-economies-and-logistics.md) (what happens to prices once goods must travel). [GD201 week 8, environmental storytelling](../../GD201-level-and-world-design/lectures/w08-environmental-storytelling.md) (reading a story from a space).

**Interactive:** [Resource locality explorer](../examples/w02-resource-locality.html). Keep it open during section 2.

---

## 1. Geography is the first system

Last week you met the structural tension: a conflict the world keeps regenerating, so writers can draw new stories from it for years. The most reliable source of structural tension is geography. A border never resolves. A pass stays the only route through the mountains. A harbour stays deep. Players and writers can fight over these for a decade, and the map does the refilling.

Geography does three pieces of work in a persistent world.

**It sets travel.** Distance and obstacles decide how long it takes to go from one place to another, which decides which places are neighbours in practice. GD201 week 9 gave you the numbers for spacing points of interest. This week is about why a player would want to travel at all.

**It sets scarcity.** Whatever is found in one place and not another has to move. Movement means trade routes, and trade routes mean places where travellers can be taxed, robbed or protected. Scarcity by place is how geography feeds the economy, and it is the main subject of this lecture.

**It sets plausibility.** Players carry a lot of real-world geography in their heads, even if they couldn't name it. Rivers run downhill to the sea. Deserts sit behind mountains. Cities grow at fords and harbours. When your map breaks these patterns without a reason, players notice, often without knowing what bothers them. When you break one on purpose and give the reason, you have a story.

### A few physical rules worth keeping

You do not need a geography degree. A handful of rules catches most errors.

- **Rivers join as they go downhill.** Small streams (tributaries) flow into bigger ones. Rivers rarely split. The main exception is near the sea or a lake, where a river may divide into several channels (distributaries) and form a delta. A river that splits in the middle of a continent and runs to two different seas needs a reason.
- **Mountains make rain shadows.** Moist air from the sea rises over mountains, cools and drops its rain on the windward side. The far side, the leeward side, is dry. If your prevailing wind comes from the west, put forests on the western slopes and steppe or desert to the east.
- **Settlements follow water and crossings.** Towns grow where a road meets a river it can ford, where two rivers join, at natural harbours and at the mouths of passes. Placing a capital on a dry hilltop far from any route is allowed, but the bible should say why someone built it there.
- **Climate follows latitude and altitude.** Colder toward the poles and up the mountains. A snowy zone next to a jungle zone at the same altitude is a staple of MMO maps. It is also a place where your bible owes the player an explanation, or at least a mountain range between them.

These rules are not there to make your world realistic. They make it readable. A player who sees a dry plain east of a mountain range has learned something true about your world without reading a word, which is what GD202 week 10 asked of lore delivery.

## 2. Worked example: why would anyone leave Lymhurst?

### The hook

Albion Online (launched 2017) has five biomes: forest, highland, mountain, steppe and swamp. There are five gatherable raw resources: wood, stone, ore, fiber and hide. Each biome's zones are rich in three of the five, and the model below treats the other two as absent. Forest zones give wood, hide and stone. Highland zones give stone, ore and wood. Mountain zones give ore, stone and fiber. Steppe zones give hide, fiber and ore. Swamp zones give fiber, wood and hide. Each of the five royal cities sits in one biome (Lymhurst in the forest, for example), and the game's wiki describes the cities as depending on one another for resources.

Three of five sounds generous. A forest player has 60% of the resource types on their doorstep. So why does Albion have such busy trade roads between cities? The answer is that "60% of the resources" and "60% of the things you can make" are very different numbers.

### The model

Suppose a world has `M` resource types. A region holds `r` of them. A recipe needs `k` different types. If recipes draw their `k` types evenly from all possible combinations, the share of recipes the region can make without importing anything is

```
local share = C(r, k) / C(M, k)
```

where `C(n, k)` is "n choose k," the number of ways to pick `k` things from `n`, which you met in MA102. The top counts the recipes whose ingredients all lie inside the region's `r` types. The bottom counts all possible recipes. One minus the local share is the **travel pressure**: the share of recipes that force someone to move goods into the region.

The model assumes every combination of types is equally likely to appear in a recipe. Real recipe lists are not that even, and you will measure a real list in the lab. The model's value is that it tells you what your distribution does before any recipe exists.

### Numbers you can check

With `M = 5` resource types:

| Types held `r` | `k = 1` | `k = 2` | `k = 3` |
|---|---|---|---|
| 1 | 20% | 0% | 0% |
| 2 | 40% | 10% | 0% |
| 3 | 60% | 30% | 10% |
| 4 | 80% | 60% | 40% |
| 5 | 100% | 100% | 100% |

Check the Albion row by hand. With `r = 3` and `k = 2`, there are `C(3, 2) = 3` pairs a forest player can make at home (wood and hide, wood and stone, hide and stone) out of `C(5, 2) = 10` possible pairs, so 30%. With `k = 3` there is exactly one local triple out of 10, so 10%. The forest region holds 60% of the resource types and can make only 10% of the three-ingredient recipes.

Read down the columns as well as across the rows. Holding one more type (going from `r = 3` to `r = 4`) takes three-ingredient locality from 10% to 40%, four times as much. Recipe complexity multiplies travel pressure. A designer who adds a third ingredient to recipes "for depth" has, in this model, raised the share of recipes that need imports for a region with `r = 3` from 70% to 90%. That is a change to the world's geography made from a crafting spreadsheet.

The same table in code:

```python
from math import comb

def local_share(M, r, k):
    """Chance a recipe needing k different resource types can be made from a region holding r of M types."""
    return comb(r, k) / comb(M, k)

for r in range(1, 6):
    print(r, [f"{local_share(5, r, k):.0%}" for k in (1, 2, 3)])
```

It prints:

```
1 ['20%', '0%', '0%']
2 ['40%', '10%', '0%']
3 ['60%', '30%', '10%']
4 ['80%', '60%', '40%']
5 ['100%', '100%', '100%']
```

### Made here versus made anywhere

Local share answers "can I make this at home?" A second question matters as much: "can anyone make this from a single region?" For Albion's five biomes, check every pair of resources. Each of the 10 pairs appears together in at least one biome, so any two-ingredient recipe can be gathered in one place by someone. Now check the triples. Each biome holds exactly one triple, so only 5 of the 10 possible triples can be gathered in any single biome. The other half can only exist if goods cross biome borders.

That is a sharp design lever. Albion's arrangement is symmetric. Each resource appears in exactly three of the five biomes, and each biome misses exactly two. No region is special, and every region needs every other region for something.

### The visual

Open the interactive. The left view shows the regions of your world as a ring, each with the resource types it holds drawn as plain shapes. The right view shows two bars for the region you select: "resource types held" and "recipes makeable here," for `k` from 1 to 4. Start on the Albion preset with `k = 1`. The two bars match at 60%. Now step `k` up. The first bar stays put and the second collapses to 30% and then 10%. Switch on "makeable anywhere" to see which recipes no single region can make. Then try the "every region has everything" preset. Both bars read 100%, and the trade-route layer on the map goes blank, because nobody needs to go anywhere.

### Cross-game recognition

**Albion Online (biomes as documented 2023, checked 2026).** Five resources, five biomes, three per biome, each resource in three biomes. In the model, `M = 5` and `r = 3` everywhere, which gives 30% locality for pairs and 10% for triples. The world's five royal cities sit one per biome, so the geography of resources is also the political map. [MMO401 week 9](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w09-regional-economies-and-logistics.md) covers what Albion's full-loot zones then do to the price of moving those goods.

**EVE Online (current, checked September 2026).** EVE splits its asteroid ores two ways. Each of the four quarters of the map (Amarr, Caldari, Gallente and Minmatar space, with their pirate neighbours) has its own set of ore types in its asteroid belts. And the security level of a star system changes what spawns. Veldspar and Scordite appear in high-security belts in all four empires, while ores such as Arkonor and Bistot appear in belts only at negative security, and Mercoxit only at -0.8 and below. In the model, a region's `r` depends on both its empire and its danger, and the rarest ingredients sit where CONCORD, EVE's police, does not reach. Geography sets risk as well as locality, which is the subject of [MMO301 week 6](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w06-eve-online-the-single-shard-sandbox.md).

**Bronze Age tin (roughly 3000 BC onward).** Bronze needs copper and tin, a `k = 2` recipe. Copper is fairly common in the earth's crust. Tin is rare, about two parts per million against copper's seventy. Known ancient tin sources were few and far apart (Cornwall and Devon, Brittany, the Iberian peninsula, the Ore Mountains between today's Germany and Czech Republic, Afghanistan, and a belt from Yunnan to the Malay Peninsula). Most bronze-making regions held copper but not tin (`r` included only one of the two), so their local share for bronze was zero, and tin was traded over very long distances. The real world ran the model thousands of years before Albion did.

Three contexts, one model. Albion sets `r` evenly and uses it to tie five cities together. EVE sets `r` by empire and by danger, so the richest recipes require risk. Bronze Age Eurasia had a tiny `r` for one ingredient, and long-distance trade grew around it.

### Eyes-open design judgment

- **High locality looks generous and produces isolation.** If every region can make everything, you have removed the main reason for players to meet. Decide your target locality for common recipes on purpose. Many worlds want solo players to make basic gear at home (`k = 1` or `k = 2` with high locality) and want group or trade play for advanced gear (`k = 3` or more, low locality).
- **Symmetry is fair and a little flat.** Albion's even distribution means no region is richer than another. An uneven distribution (one region holds a rare type, like tin) creates a strong structural tension that week 1 would value highly. It also creates a region everyone must control, which can decide a server's politics for years. Choose which one you want.
- **Recipe design is map design.** When the crafting team adds ingredients, travel pressure rises. Put locality targets in the bible so crafting and world teams share one number.
- **Guarantee "makeable somewhere" or accept "made only by trade."** A recipe no single region can supply exists only if goods travel. That is fine if you want it. It is a bug if a new server has not built its trade routes yet and players cannot make their starter gear.
- **Players change `r`.** Gatherers who strip a region, like Ultima Online's players emptying its resource system (MMO301 week 3), lower the effective `r` of a region. Your model is a starting point, not a guarantee.

## 3. Ecology: who eats whom

The second half of this week is the living layer on top of the map. An **ecology** is the set of relationships between the creatures and plants in a place, above all who eats whom. In a game, the ecology is mostly expressed through spawn tables, the lists of what creatures appear in a zone and how many.

Players read spawn tables as ecology whether you intend it or not. A zone full of wolves and bears with three deer reads as a place where something is wrong. That is a problem if you did not intend it and a hook if you did.

### The ten percent rule as a design check

Ecologists have a rough rule for how much life each level of a food chain can support. Energy passes up the chain inefficiently. Plants capture it, plant-eaters (herbivores) eat the plants, and meat-eaters (carnivores) eat the herbivores. At each step much of the energy is lost to movement, waste and heat. As a rule of thumb, each level produces only about ten percent as much as the level below it. The rule is usually traced to Raymond Lindeman's 1942 paper on the trophic-dynamic view of ecology. It is an average, and real ecosystems vary a lot around it.

For a designer, the rule gives a quick plausibility check. Take an invented forest zone and illustrative body masses.

| Creature | Level | Count | Mass each | Total mass |
|---|---|---|---|---|
| Deer | herbivore | 40 | 60 kg | 2,400 kg |
| Wolf | carnivore | 30 | 40 kg | 1,200 kg |
| Bear | top carnivore | 6 | 200 kg | 1,200 kg |

Predators total 2,400 kg, the same as their prey. The ten percent rule speaks about production over time, not about how much is standing in the zone at one moment, so treat it as a loose guide. Even so, a ratio of one to one is far past anything a real forest supports. A rough plausible count would be closer to 240 kg of predators, about six wolves, and bears only if the zone has much more prey or plant food than it shows.

### Why games break the rule, and what to do about it

Games break this rule for good reasons. Players want to fight predators, and deer are not much of a fight. A spawn table built for combat will always be predator-heavy. You have three honest options.

**Accept it and keep it quiet.** Most players will not count. If the zone is not about nature, don't draw attention to its food chain. Don't put a quest about the delicate balance of the forest in a zone that has none.

**Explain it with the setting.** An upside-down ecology is a fact that needs a cause, and a cause is a tension, which is week 1's unit of story. The wolves are here because a hard winter drove them down from the mountains. They are eating the farmers' sheep, which aren't in your spawn table because they are behind fences in the village. A necromancer is raising them. Each of these turns a spawn table problem into a quest hub.

**Make the ecology a system.** A predator population that falls when players hunt its prey, or prey that recovers when players thin the wolves, is a real ecology. Ultima Online planned one and never shipped it, because players hunted faster than any population could recover (MMO301 week 3 gives the rate model; don't rebuild it here). If you try, budget for player hunting as the largest force in your ecology. It will be.

### Ecology as environmental storytelling

GD201 week 8 taught you to tell stories with what players find in a space. Ecology gives you material for that. Bones near a cave say a large predator lives there, before the player sees it. Stripped bark says too many deer. A dry riverbed with fish skeletons says the upstream dam from the quest hub in the next zone is real. These cost a prop or two and connect the zone's spawns to the setting's history.

## 4. Building a region: a procedure for your bible

Put sections 1 to 3 together into a procedure you can run for each region of your world.

1. **Place the physical frame.** Mountains, prevailing wind, rivers, coast. Check the rules in section 1. Mark any deliberate break and write its reason.
2. **Assign resources by biome.** Decide `M`, the number of raw resource types. Give each biome a set whose size `r` you choose on purpose. Compute local share for the recipe complexities your crafting team plans.
3. **Check coverage.** List which `k`-type recipes are makeable in at least one region and which need trade. Decide whether you want any recipe that no single region can supply.
4. **Place settlements.** Put towns at crossings, harbours and resource edges. The most contested place is usually where two biomes meet, because it gives access to both sets.
5. **Stock the ecology.** Write a spawn table. Run the ten percent check. For each large break, choose accept, explain or simulate, and write the explanation as a tension in your week 1 ledger.

A small example. A world with `M = 6` resource types and four regions, each holding three. Local share for pairs is `C(3, 2) / C(6, 2) = 3 / 15 = 20%`, and for triples `1 / 20 = 5%`. With only four regions of three types each, at most four of the twenty triples can be gathered in one place, so at least 80% of triples need trade. That may be exactly what the design wants for endgame crafting. It will be a disaster for starter gear if starter recipes use three types.

## In-class activity (25 minutes)

Pairs. You are given a blank map outline with a coast to the west and a mountain chain running north to south through the middle.

1. **Frame (5 min).** Mark the prevailing wind from the west. Shade the wet and dry sides. Draw one river system that obeys the joining rule.
2. **Distribute (10 min).** Use `M = 5` resource types and 4 regions. Your target is: every region can make at least 30% of two-type recipes at home, and at least one three-type recipe can be made nowhere without trade. Assign resources to regions and compute both numbers.
3. **Hook (10 min).** Write a spawn table of three creatures for one region that fails the ten percent check. Write one sentence that turns the failure into a tension.

Expected output: the annotated map, the resource table with the two computed numbers, and the spawn table with its tension sentence.

## Common misconceptions

- **"If a region has 60% of the resources, it can make 60% of the items."** Only for single-ingredient recipes. For `k` ingredients, local share falls at least as fast as the resource share raised to the power `k`. Albion's forest holds 60% of types and makes 10% of three-type recipes.
- **"More resources everywhere is friendlier."** It makes regions self-sufficient, which removes trade, travel and contested borders. Decide how much meeting you want and set locality to match.
- **"The ten percent rule means a zone can only have a few predators."** It is a rough average about production, not a hard cap on how many animals stand in a zone. Use it to notice an extreme spawn table, then decide whether to accept, explain or simulate.
- **"Realistic geography is the goal."** Readable geography is the goal. Break a physical rule when you want to, and give the reason in the world.

## Check yourself

1. A world has `M = 6` resource types. A region holds `r = 4`. What share of two-type recipes and three-type recipes can it make at home?
2. A designer wants a region holding 3 of 5 types to make at least half of all two-type recipes locally. Is that possible with `M = 5`? What is the smallest `r` that reaches it?
3. Albion's five biomes each hold three of five resources. Suppose a sixth biome held all five. How many of the ten three-type triples could now be gathered in one place, and what would that biome do to the politics of the map?
4. A swamp zone's spawn table has 50 frogs (1 kg each), 20 giant snakes (30 kg each) and 4 crocodiles (300 kg each). Compute predator and prey mass. Is it plausible? Give one setting reason that would make it acceptable.

<details>
<summary>Answers</summary>

1. Pairs: `C(4, 2) / C(6, 2) = 6 / 15 = 40%`. Triples: `C(4, 3) / C(6, 3) = 4 / 20 = 20%`.
2. With `r = 3`, locality for pairs is 30%, so no. With `r = 4`, it is `6 / 10 = 60%`, which reaches the target. The smallest `r` is 4.
3. All ten, since the sixth biome holds every triple. Everyone would want that biome. It becomes the one region every faction must control, a strong structural tension and a likely source of one dominant alliance.
4. Prey 50 kg (frogs). Predators 600 kg (snakes) plus 1,200 kg (crocodiles), 1,800 kg in total, 36 times the prey. Far from plausible if frogs are the only food. Reasons: the snakes and crocodiles feed on fish in the water, which the spawn table does not show; or the swamp is a breeding ground where they gather once a year; or a cult feeds them. Each reason can become a quest.

</details>

## Lab / assignment hook

[Lab 02, a map that needs its neighbours](../labs/lab02.md). You write a resource-distribution checker, run it on a recipe list, and design the regions of your own world to hit locality and coverage targets. The resulting region sheet goes into your world bible.

## Sources

- Wolf, M. J. P. (2012). *Building Imaginary Worlds: The Theory and History of Subcreation*. Routledge. Chapter 3, "World Structures and Systems of Relationships" (publisher's table of contents).
- Albion Online Wiki, "Biomes" (archived snapshot of 4 February 2023, web.archive.org, page last edited 24 July 2021; snapshot reread September 2026; the live wiki blocks automated reads). Each zone is "rich in three resources" set by its biome. Five biomes; resources per biome (forest: wood, hide, stone; highland: stone, ore, wood; mountain: ore, stone, fiber; steppe: hide, fiber, ore; swamp: fiber, wood, hide); the royal city of each biome.
- Albion Online Wiki, "Royal Continent" (archived snapshot of 7 February 2023, web.archive.org, reread September 2026). Each royal city governs a region defined by its biome, and the cities rely on one another for resources.
- Wikipedia, "Albion Online" (checked September 2026). Released for Windows, macOS and Linux on 17 July 2017.
- EVE University Wiki, "Asteroids and ore" (checked September 2026). Ore types differ by empire quarter and by security rating; Veldspar and Scordite in all high-security belts; Arkonor and Bistot in belts at negative security; Mercoxit at -0.8 and below.
- EVE University Wiki, "System security" (checked September 2026). Security classes: high security 0.5 and above, low 0.1 to 0.4, null 0.0 and below; changes introduced with the Exordium starter region in 2026.
- Wikipedia, "Tin sources and trade during antiquity" (checked September 2026). Tin at about 2 ppm in the crust against copper at about 70 ppm; list of known ancient sources; long-distance trade to regions without tin.
- Wikipedia, "Rain shadow" and "Distributary" (checked September 2026). Definitions used in section 1.
- Wikipedia, "Ecological efficiency" (checked September 2026), and Lindeman, R. L. (1942). "The trophic-dynamic aspect of ecology." *Ecology* 23(4), 399-418. The ten percent rule as an average transfer between trophic levels.

## Interactive spec: examples/w02-resource-locality.html

**Purpose.** Make visible that holding a large share of resource types does not mean being able to make a large share of recipes, and that recipe complexity is what drives travel.

**The one insight the visual must make obvious.** At Albion's settings (`M = 5`, `r = 3`), the "types held" bar stays at 60% while the "recipes makeable here" bar drops to 30% at `k = 2` and 10% at `k = 3`.

**Model (exact).**
- `local(M, r, k) = C(r, k) / C(M, k)`, with `C(n, k) = 0` when `k > n`.
- Travel pressure `= 1 − local`.
- "Makeable anywhere" for a concrete distribution: enumerate all `C(M, k)` combinations of resource types; a combination is makeable anywhere if it is a subset of at least one region's set. Report the count and list those that are not.

**Controls.**
- Preset selector: "Albion Online biomes (2023 wiki)" (5 regions: Forest {wood, hide, stone}, Highland {stone, ore, wood}, Mountain {ore, stone, fiber}, Steppe {hide, fiber, ore}, Swamp {fiber, wood, hide}); "Everything everywhere" (4 regions, all 5 types); "One rare type" (5 regions over 5 types where "tin" appears in only one region, the others hold 3 of the remaining 4); "Custom".
- In Custom mode: `M` slider 3 to 8, number of regions 2 to 8, and a grid of toggle buttons (region by resource) to set which types each region holds.
- `k` slider 1 to 4.
- Toggle "Show makeable anywhere".
- Region selector (click a region on the ring or use arrow keys).

**Views.**
- Left: regions on a ring, each a labelled circle with small generic shapes for its resource types (circle, square, triangle, diamond, hexagon, and so on; each type also has a text label). When "Show makeable anywhere" is on, draw a line between two regions whenever a recipe that no single region in the world can make could be made by combining their two sets. A recipe some third region can make on its own does not demand a route. The line count should read as "trade routes the recipes demand."
- Right: for the selected region, two horizontal bars: "types held" (`r / M`) and "recipes makeable here" (`local`). Below, a small line chart of `local` against `k` for `k = 1 … 4`, with the current `k` marked.
- Numbers table under the charts: `M`, `r`, `k`, `C(r, k)`, `C(M, k)`, local share, travel pressure, and "makeable anywhere: x of y".

**Test values (must match exactly).**
- `M = 5, r = 3`: `k = 1` 60%, `k = 2` 30%, `k = 3` 10%.
- `M = 5, r = 4`: `k = 2` 60%, `k = 3` 40%.
- `M = 6, r = 4`: `k = 2` 40%, `k = 3` 20%.
- Albion preset: makeable anywhere, `k = 2`: 10 of 10 with 0 trade lines; `k = 3`: 5 of 10 (the five biome triples) with lines on all 10 region pairs.
- "Everything everywhere": all local shares 100%; no trade lines drawn.

**Style.** Shared tokens from `templates/interactive-tokens.css`. No game art, logos or map screenshots. Biome names appear as text labels only.
