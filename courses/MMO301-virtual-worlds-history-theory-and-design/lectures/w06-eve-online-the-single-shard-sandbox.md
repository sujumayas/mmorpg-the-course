# MMO301 · Week 06 — EVE Online: the Single-Shard Sandbox

**Why this matters:** EVE Online runs almost its entire player base in one universe and lets players attack, rob and betray each other nearly everywhere. It does not ban crime in its safest space. It puts a price on it. Once you see how that price is set, you can read every "safe zone" and "PvP zone" in other games as a choice of price, and you can set one on purpose in your own world.

**You will be able to:**
- Explain what a single shard changes about a world (market, reputation, history, scale) compared with the sharded worlds of weeks 3 to 5.
- Compute the cost of a suicide gank from CONCORD response time, target toughness and attacker damage, and the cargo value above which a gank pays.
- Rewrite the aggression rules of EVE, Ultima Online and Old School RuneScape as a price of aggression that changes across zones.
- Design a risk gradient for a world and justify where its prices change.

**Before class:** Castronova, *Synthetic Worlds* (2005), chapters 1 and 2, on what makes a synthetic world a place with its own rules and stakes. EVE University Wiki, "CONCORD" and "Hauling" (about 20 minutes together).

**Prerequisites from earlier courses:** [GS101 week 9, graphical MMOs](../../GS101-history-and-critical-study-of-games/lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md) gives EVE's release and its record of 65,303 players in one world, and the subscriber and world-size model. [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) is used for loot. [MMO303 week 3, effective HP](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w03-effective-hp-and-effective-dps.md) defines effective HP (EHP). [MMO304 week 13, case studies](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w13-case-studies-eve-diablo-runescape-grand-exchange.md) covers EVE's economy. Looking ahead to year 4, [MMO401 week 9, regional economies and logistics](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w09-regional-economies-and-logistics.md) and [MMO401 week 10, full loot and destruction](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w10-scarcity-by-design-full-loot-and-destruction.md) treat hauling risk and the loot rules as economics. This course: [week 5](w05-world-of-warcraft-accessibility-and-the-themepark.md) for the themepark this week contrasts with, and [week 3 on Ultima Online](w03-ultima-online-the-simulation-dream-and-its-limits.md) for the Trammel split.

**Interactive:** [The price of a crime](../examples/w06-gank-price.html). Keep it open during section 2.

---

## 1. One universe

### What "single shard" means

Weeks 3 to 5 studied worlds that ran as many copies. EverQuest and World of Warcraft players chose a server, and players on different servers never met. EVE Online (CCP Games, released 6 May 2003) took the other path. Wikipedia describes it as functionally a single-universe game. The main server, Tranquility, hosts players worldwide except China, where the separate Serenity server runs. The other copies are a public test server and a tournament server. The universe has about 7,800 star systems.

"Server" is a simplification. The EVE University Wiki notes that Tranquility is split across many machines, each running part of the universe. What makes it one shard is that the player sees one world. Any player can fly to any system, trade with any other player and meet them in space.

A single shard changes four things.

- **One market.** Prices are set by the whole player base, not by one server's few thousand. EVE splits its market by region, but the regions are connected, and hauling between them is a profession. MMO401 week 9 models that.
- **One reputation.** A scammer or a famous fleet commander cannot move to a fresh server. What you did follows you, and other players can look it up.
- **One history.** A war happens once, for everyone. The largest battles are events the whole community watched, and MMO401 week 10 analyzes the loss accounting of one of them.
- **Scale in one place.** GS101 week 9 put EVE's record of 65,303 players in one world beside EverQuest's servers of a few thousand. Running thousands of players in one fight needs its own engineering. MMO302 week 12 covers single-shard architecture and time dilation ([lecture](../../MMO302-mmo-server-architecture/lectures/w12-single-shard-architectures-and-time-dilation.md)).

### What "sandbox" means

Week 5 defined the themepark as a world of authored rides. A **sandbox** gives players systems and lets them set their own goals. EVE's systems are mining, manufacturing, trade, exploration and combat, plus corporations (player guilds), alliances of corporations, and sovereignty, the right to claim and hold star systems. Most of what happens in EVE's news is players using those systems against each other.

A sandbox also needs rules about what players may do to each other, because in a sandbox other players are the main content. Wikipedia notes that CCP does not refund in-game losses, so confidence tricks and scams are a risk players accept. MMO401 week 8 studies player banks and scams ([link](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w08-player-banks-loans-and-scams.md)). This week focuses on the rule that shapes daily life in EVE, the rule about attacking other players.

### The security gradient

Every EVE star system has a security level from −1.0 to 1.0.

- **High security, 0.5 to 1.0.** CONCORD, the NPC police, responds to illegal attacks by destroying the attacker's ship. The attacker also loses security standing, their character's legal reputation.
- **Low security, 0.1 to 0.4.** CONCORD does not respond. Stargate and station guns still shoot aggressors.
- **Null security, 0.0 and below.** No NPC enforcement. Players can claim sovereignty.
- **Wormhole space.** Lawless like null security, reached only through wormholes that open and close. The EVE University Wiki notes that players there do not appear in the local chat list until they speak, so you cannot see who is nearby.

The part to notice is that high security space is not safe. Attacking another player there is illegal, and CONCORD will destroy you for it. But the game lets you do it. CCP did not build a wall. It built a price.

## 2. Worked example: the price of a crime

### The hook

In EVE's high security space, a group of players can destroy a cargo ship, lose all their own ships to the police a few seconds later, and still come out ahead. Players call this a **suicide gank**. Wikipedia describes gankers using cheap, high-damage ships, knowing that some targets carry enough cargo to repay the ships they will lose. The EVE University Wiki's hauling guide gives cargo pilots a rule of thumb: keep the value of your cargo and fitted modules below about 3,000 ISK (EVE's currency) per point of effective HP.

Where does a number like 3,000 come from? And what does the security level of a system have to do with it? The model makes the rule of thumb something you can derive.

### The model

Let:

- `H` be the target's effective HP, the damage needed to destroy it (MMO303 week 3).
- `a` be the damage per second of one attacking ship.
- `T` be CONCORD's response time in seconds.
- `c` be the net cost to the attackers of one ship lost to CONCORD. The EVE University Wiki lists CONCORD destruction among the ways a pilot loses purchased insurance, so `c` is close to the ship's full price.
- `V` be the value of the target's cargo.
- `p` be the chance each cargo item survives into the wreck. The EVE University Wiki's "Loot Fairy" page gives 50% for most of EVE's history, so `p = 0.5`.

Each attacking ship deals `a × T` damage before CONCORD destroys it. The attackers need enough ships to reach `H`:

```
n = ceil(H / (a × T))       ships needed
C = n × c                   cost of the gank
E = p × V                   expected loot
gank pays when  p × V > C,  so  V* = C / p = 2 × n × c
```

`V*` is the **safe cargo value**. Below it, a rational ganker loses money. Above it, the hauler is a target.

Divide by `H` and ignore the rounding in `n`:

```
V* / H ≈ c / (p × a × T) = 2c / (a × T)
```

That is the rule of thumb's form, ISK of cargo per point of EHP. It is proportional to the cost of a gank ship and inversely proportional to CONCORD's response time. The security level enters the model only through `T`.

### Numbers you can check

The EVE University Wiki gives CONCORD's response times when it has just spawned in the system, by security level: roughly 6 seconds at 1.0 and 0.9, 7 at 0.8, 10 at 0.7, 14 at 0.6 and 19 at 0.5. The ship numbers below are assumptions for the example, not measured values: gank ships of `a = 500` damage per second costing `c = 12` million ISK each, against a hauler with `H = 60,000` EHP.

| Security | `T` (s) | Damage per ship `a × T` | Ships `n` | Gank cost `C` | Safe cargo `V*` | `V* / H` (ISK per EHP) |
|---|---|---|---|---|---|---|
| 1.0 | 6 | 3,000 | 20 | 240M | 480M | 8,000 |
| 0.8 | 7 | 3,500 | 18 | 216M | 432M | 7,200 |
| 0.7 | 10 | 5,000 | 12 | 144M | 288M | 4,800 |
| 0.6 | 14 | 7,000 | 9 | 108M | 216M | 3,600 |
| 0.5 | 19 | 9,500 | 7 | 84M | 168M | 2,800 |

Check the 0.5 row. Each ship deals `500 × 19 = 9,500` damage. `60,000 / 9,500 ≈ 6.3`, so 7 ships. `C = 7 × 12M = 84M`, and `V* = 84M / 0.5 = 168M`. Per EHP, `168,000,000 / 60,000 = 2,800` ISK.

With these assumed ships, the model at 0.5 lands close to the wiki's rule of thumb of 3,000 ISK per EHP. That is a sanity check on the model, not a measurement. It says a cautious hauler should plan for the most dangerous high security space, which is what a rule of thumb should do.

### The hauler's lever and the ganker's lever

Both sides can move the numbers.

**The hauler adds tank.** Double `H` to 120,000 in a 0.5 system. `120,000 / 9,500 ≈ 12.6`, so `n = 13`, `C = 156M` and `V* = 312M`. Because `n` is rounded up, the safe value rises in steps. A hauler who adds EHP just past a step boundary buys a whole extra gank ship of protection.

**The ganker delays the police.** The EVE University Wiki's suicide-ganking page explains that if CONCORD is already in the system but far from the attack, it despawns and respawns next to the attacker, adding roughly 6 seconds. At 0.5 that makes `T ≈ 25`. Each ship now deals 12,500 damage, `n = 5`, `C = 60M` and `V* = 120M`, about 2,000 ISK per EHP. Players who know the rule can move the price by about 30%.

**The ganker's profit.** Against a hauler carrying 300M in a 0.5 system with fresh CONCORD, the expected loot is `0.5 × 300M = 150M`, the cost is 84M, and the expected profit is 66M. The loot is random. With a 50% drop per item, a cargo of one expensive item is a coin flip, and a cargo of many cheap items is close to the average.

### A visual you can move

Open `examples/w06-gank-price.html`. The left panel is a staircase of gank ships needed against the hauler's EHP, for the security level you select. The right panel plots safe cargo value `V*` for every high security level at once, as bars, with the hauler's actual cargo drawn as a horizontal line. Any bar below the line is a system where this hauler is worth killing. Drag the cargo up and watch the 0.5 bar fall under it first, then 0.6, then 0.7. Toggle "CONCORD pulled" and watch every bar drop.

### Cross-game recognition

Write each game's rule as a price of aggression, and ask how the price changes across the map.

**EVE outside high security.** In low security space, CONCORD does not respond, so `T` is effectively unlimited for the model. Gate and station guns still add a cost near those structures. In null security there is no NPC price at all, only the price other players set by defending. EVE's legal route in high security space is a war declaration between corporations or alliances, which Wikipedia describes as available for a weekly fee. That converts the price of aggression from ships into ISK paid up front.

**Ultima Online (current rules, and the 2000 split).** UOGuide describes murder counts. A player who kills other players becomes a murderer at 5 long-term counts, and each count takes 40 hours of logged-in time to decay. In town guard zones, guards can be called on anyone who breaks the law. So Ultima Online prices aggression twice, with a quick NPC response in towns (like CONCORD) and a reputation cost that follows you everywhere (like EVE's security standing). In May 2000 the Renaissance expansion added Trammel, where one player could not attack another without consent. In the model, the price of aggression in Trammel is infinite. Week 3 studied why that split happened.

**Old School RuneScape's Wilderness (current).** The Old School RuneScape Wiki says two players can fight if their combat levels differ by no more than the current Wilderness level, which rises to 56 in the far north. Most teleports stop working above level 20, and nearly all above level 30. The deeper you go, the wider the range of players who can attack you and the harder it is to leave. The price of aggression falls with depth, and the price of escape rises. It is the same gradient as EVE's security levels, drawn on one region instead of a galaxy.

Three worlds, one design. Aggression is allowed but priced, and the price changes with place. Players read the price and choose where to live.

### Eyes-open design judgment

- **What a price buys that a wall does not.** Consequences with room for choice. A hauler weighs cargo against tank against route. A ganker weighs loot against ships. Both are playing, and the story of a gank is shared by the whole community. A wall, like Trammel's consent rule, gives safety with no decisions in it.
- **What a price costs.** Some players will pay it, and their targets will not enjoy it. New players in EVE's high security space can be ganked. That shapes who stays. Ultima Online's player-killing problem in week 3 was the same issue with a lower price.
- **Where to set the price.** Price aggression relative to what players carry. If the most valuable thing a new player can carry is worth less than one gank ship, new players are safe in practice, even without a wall. Tie the price to something you can tune, like response time, and publish it so players can plan.
- **What the designer must watch.** Players find ways to lower the price, such as pulling CONCORD away. Each one moves `V*`, and pulling CONCORD alone moves it by nearly 30%. Monitor the realized price, not the intended one.
- **What a single shard adds.** In a sharded world, a player who dislikes the price can move servers. In EVE they cannot. That raises the stakes of every price you set, and it makes the price part of the world's culture.

### Check yourself (worked example)

1. A hauler with 80,000 EHP flies through a 0.7 system. Gank ships deal 600 damage per second and cost 10M ISK each. How many ships does a gank need, and what is the safe cargo value?
2. The same hauler moves through a 1.0 system instead. What is `V*` now?
3. A designer wants the safe cargo value per EHP in 0.5 space to be 5,000 ISK, with `a = 500` and `p = 0.5`. What gank-ship cost `c` would produce that? Name another lever the designer could pull instead.

<details>
<summary>Answers</summary>

1. `a × T = 600 × 10 = 6,000`. `80,000 / 6,000 ≈ 13.3`, so `n = 14`. `C = 140M`, `V* = 280M`.
2. `a × T = 600 × 6 = 3,600`. `80,000 / 3,600 ≈ 22.2`, so `n = 23`. `C = 230M`, `V* = 460M`.
3. `V* / H ≈ 2c / (a × T)`, so `c = 5,000 × 500 × 19 / 2 ≈ 23.75M` ISK. Alternatively shorten `T` (faster police), or lower `p` (less cargo survives), which raises `V* = C / p`.

</details>

## 3. Designing a risk gradient

EVE's security map is a design pattern you can reuse. It has three parts.

**A price that varies by place.** High security space has a high price, low security a lower one, null security none from the NPCs. The reward side runs the other way. Player-owned territory exists only in null security. The EVE University Wiki's page on system security lists what a lower security level raises: more lucrative asteroids, harder and better-paying NPC pirates and combat sites, and larger loyalty-point rewards from mission agents. A gradient works when risk and reward rise together, so that every player can find the level they want.

**Travel between prices.** A gradient only matters if players cross it. Haulers carry goods from the lawless regions to the markets in safe space, which is where MMO401 week 9's transport cost comes from. The model predicts that the danger concentrates where valuable cargo meets a low price of aggression, such as the busy lowest-security routes into trade hubs. MMO401 week 9 notes players waiting outside the largest hub to attack haulers.

**A price players can read.** EVE shows every system's security level on the map and in the interface. Players can compute their own `V*`, and the community publishes rules of thumb. If the price were hidden, the gradient would feel random and players could not choose.

Compare the themepark from week 5. A themepark usually prices aggression by consent, with two steps, off and on, chosen by the player. EVE's gradient has many steps, and the step you stand on changes as you fly.

### Governance at the scale of one world

A single-shard sandbox has one more problem. When the world's rules are this important and every player lives under the same ones, the players want a voice in them. In March 2008, CCP invited players to stand for the first Council of Stellar Management, a player-elected body that advises the developer. Wikipedia reports 66 candidates for nine seats. In 2007 CCP had hired an economist, Eyjólfur Guðmundsson, to oversee the in-game economy. Both steps treat the world as a society with institutions, not a product with settings. [MMO402 week 3](../../MMO402-emergent-society-governance-and-ethics/lectures/w03-eves-council-of-stellar-management.md) returns to the CSM in depth, and [MMO401 week 1](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w01-the-in-house-economist-role.md) discusses the in-house economist's role.

## In-class activity (25 minutes)

In groups of three. Design the risk gradient for a fantasy world with three regions: a capital, a frontier and a wilderness.

1. (8 min) For each region, choose how aggression is priced: an NPC response time, a reputation cost, a fee, or none. Give a number for each.
2. (7 min) Choose one thing a new player might carry, and its value. Using the gank model with your own damage and ship-cost numbers, check that attacking that player in the capital does not pay.
3. (5 min) Name the most valuable resource in each region. Check that risk and reward rise together.
4. (5 min) Find one way players could lower your capital's price, like pulling CONCORD. Decide whether to allow it.

Expected output: a three-row table (region, price rule, number, best resource), the new-player check with its arithmetic, and your decision on the exploit. Keep it for Lab 06.

## Common misconceptions

- **"High security space is safe."** It is policed. Attacks are punished, not prevented. Whether an attack pays depends on the cargo and the numbers in section 2.
- **"Single shard means one computer."** Tranquility runs across many machines, each hosting part of the universe. Single shard describes what the player sees, one connected world.
- **"Sandbox means no rules."** A sandbox has detailed rules about what players can do to each other. It prices behavior instead of scripting it.
- **"Ganking is a bug CCP tolerates."** The response times, loot chance and insurance rules are documented design. CCP set a price for aggression in safe space on purpose, and players respond to that price.

## Check yourself

1. A system's security drops from 0.6 to 0.5. By what factor does the damage each gank ship deals change? What happens to the number of gank ships needed against a 42,000 EHP hauler with 500-damage ships?
2. Using `V* ≈ 2c / (a × T) × H`, explain in one sentence why cheaper gank ships make every hauler less safe.
3. Rewrite the Old School RuneScape Wilderness rule as a gradient. What rises with depth, and what falls?
4. Give one thing a single shard makes possible that a sharded world cannot, and one problem it creates.
5. A designer proposes "no player combat anywhere except arenas." In the model, what is the price of aggression, and what does the world lose compared with EVE's gradient?

<details>
<summary>Answers</summary>

1. `T` goes from 14 to 19 seconds, so damage per ship rises by `19 / 14 ≈ 1.36`. At 0.6, `42,000 / 7,000 = 6` ships. At 0.5, `42,000 / 9,500 ≈ 4.4`, so 5 ships.
2. `V*` is proportional to `c`, so if gank ships cost less, the cargo value at which a gank pays falls for every hauler at every security level.
3. The range of combat levels that can attack you rises with depth, and so does the difficulty of teleporting out. The effective price of attacking someone falls with depth, and the price of escape rises.
4. Possible: one market, one reputation that follows a player, battles with tens of thousands in one world, a shared history. Problem: players cannot escape a bad situation by changing servers, and the whole player base must fit on one world's technology.
5. The price is infinite outside arenas, like Trammel. The world loses decisions about risk (cargo, route, tank), the profession of hauling through danger, and the shared stories that come from priced conflict.

</details>

## Lab / assignment hook

[Lab 06, pricing aggression](../labs/lab06.md). You build a gank calculator from section 2, reproduce the security table, then design and test a three-zone risk gradient for your own world concept. The zone table becomes the risk section of the world design bible (40%).

## Sources

- Wikipedia, "Eve Online" (accessed September 2026). Release 6 May 2003; functionally a single-universe game with Tranquility as the main server, Serenity for China, Singularity as test server and Thunderdome for tournaments; about 7,800 star systems; security from −1.0 to 1.0 with 0.5 to 1.0 as high security; CONCORD destroys illegal aggressors and the aggressor loses security standing; war declarations for a weekly fee; suicide ganking with cheap high-damage ships; no refunds, so scams are a risk; the first Council of Stellar Management in March 2008 with 66 candidates for nine positions; CCP hired economist Eyjólfur Guðmundsson in 2007.
- EVE University Wiki, "CONCORD" (current). Response times when CONCORD has just spawned: roughly 6 s at 1.0 and 0.9, 7 s at 0.8, 10 s at 0.7, 14 s at 0.6, 19 s at 0.5.
- EVE University Wiki, "System security" (current). Low security 0.1 to 0.4 with no CONCORD response but active gate and station guns; null security −1.0 to 0.0 with no NPC response; wormhole space not shown in local chat until a pilot speaks; lower true security raises asteroid value, NPC pirate and anomaly difficulty, and mission loyalty-point rewards. (The same page gives CONCORD response "up to 24 seconds" at 0.5, consistent with the respawn delay below.)
- EVE University Wiki, "Suicide ganking" (current). The aim of trading cheaper ships for a more valuable target; CONCORD already in system but more than 150 km away despawns and respawns, adding roughly 6 seconds.
- EVE University Wiki, "Hauling" (current). Rule of thumb of under 3,000 ISK of cargo plus fitted modules per point of EHP; the attacker's goal of trading ships for cargo.
- EVE University Wiki, "Insurance" (current). Destruction by CONCORD in high security space listed among the ways to lose purchased insurance.
- EVE University Wiki, "Loot Fairy" (current). Drop chance usually fixed at 50%.
- EVE University Wiki, "Tranquility" (current). A cluster serving the global player base except China, split into nodes but experienced as one server.
- UOGuide, "Murderer" (current Ultima Online rules). Murderer status at 5 long-term counts; 40 logged-in hours per count to decay; guards can be summoned on lawbreakers in guard zones.
- Wikipedia, "Ultima Online" (accessed September 2026). Renaissance expansion (May 2000) and the Trammel rule set without non-consensual player combat.
- Old School RuneScape Wiki, "Wilderness" (current). Attack range equals combat level plus or minus Wilderness level; maximum level 56; teleport limits above levels 20 and 30.
- Castronova, E. (2005). *Synthetic Worlds: The Business and Culture of Online Games*. University of Chicago Press.

## Interactive spec: examples/w06-gank-price.html

**Insight the visual must make obvious:** high security space does not forbid attacks, it prices them. The price is set by CONCORD's response time, so the same hauler with the same cargo is safe in 1.0 space and a profitable target in 0.5 space. Tank raises the price in steps.

**Layout.** Two panels side by side at 1280px, stacked at 390px. Left: "Gank ships needed" staircase. Right: "Safe cargo value by security level" bars. Controls above; number panel and data table below.

**Left panel.**
- x axis: hauler EHP `H`, 0 to 200,000. y axis: ships needed `n`, 0 to 40.
- Staircase `n(H) = ceil(H / (a × T_sel))` for the selected security level. A second, lighter staircase for 1.0 space for comparison.
- A marker at the current `H` with `n` printed. Hovering or focusing a step shows the EHP range it covers.

**Right panel.**
- One bar per security level 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, height `V* = n × c / p` at the current `H`, in millions of ISK.
- A horizontal line at the hauler's cargo value `V`, labelled.
- Bars whose `V*` is below `V` are drawn with a hatch pattern and labelled "gank pays", so the state does not rely on color.
- A second value per bar: `V* / H` in ISK per EHP, with a reference line at 3,000 labelled "EVE University rule of thumb".

**Controls.**
- Hauler EHP `H`: 10,000 to 200,000, step 1,000, default 60,000.
- Cargo value `V`: 0 to 1,000M ISK, step 5M, default 150M.
- Gank ship damage per second `a`: 100 to 1,500, step 50, default 500 (label "assumed").
- Gank ship net cost `c`: 1M to 50M, step 0.5M, default 12M (label "assumed").
- Drop chance `p`: 0.1 to 1.0, step 0.05, default 0.5.
- Selected security level for the left panel: 1.0 to 0.5, default 0.5.
- "CONCORD pulled" toggle: adds 6 s to every `T`.

**Response times `T` (seconds).** 1.0: 6; 0.9: 6; 0.8: 7; 0.7: 10; 0.6: 14; 0.5: 19. With "CONCORD pulled", add 6 to each.

**Number panel.** For the selected level: `T`, `a × T`, `n`, `C = n × c`, `V* = C / p`, `V* / H`, expected loot `p × V`, expected profit `p × V − C` (signed, with "gank pays" or "gank loses" in text).

**Formulas.** `n = ceil(H / (a × T))`, `C = n × c`, `V* = C / p`, expected profit `p × V − C`.

**Test values.**
- Defaults (`H = 60,000`, `a = 500`, `c = 12M`, `p = 0.5`): `n` = 20, 20, 18, 12, 9, 7 for 1.0 to 0.5; `V*` = 480M, 480M, 432M, 288M, 216M, 168M; `V*/H` = 8,000, 8,000, 7,200, 4,800, 3,600, 2,800.
- `H = 120,000` at 0.5: `n = 13`, `V* = 312M`.
- CONCORD pulled at 0.5 (`T = 25`), `H = 60,000`: `n = 5`, `V* = 120M`, `V*/H = 2,000`.
- `V = 300M` at 0.5, defaults: expected profit `150M − 84M = 66M`.
- `H = 80,000`, `a = 600`, `c = 10M`: at 0.7 `n = 14`, `V* = 280M`; at 1.0 `n = 23`, `V* = 460M`.

**Style and accessibility.** Tokens from `templates/interactive-tokens.css`. Hatching for "gank pays" bars; the two staircases differ by line weight and a text label. All controls keyboard operable with visible values. Respect `prefers-reduced-motion` (no bar-height transitions). No ship models, logos or game art; ships are drawn as plain markers and named generically ("gank ship", "hauler").
