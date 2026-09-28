# MMO305 · Week 08 — Griefing: Typology and Design Responses

**Why this matters:** Every shared world attracts players who enjoy ruining other people's time. You cannot ban your way out of it, and the loudest fixes often fail. If you can say what a griefer gains, what they use to do it and who they reach, you can pick the one change that stops the harm instead of three that only look busy.

**You will be able to:**
- Classify a griefing incident with Foo and Koivisto's four types and name what the griefer gains.
- Model a harm that spreads through contact with a reservoir-fed SIS model, and compute its steady level from `β`, `γ` and the reservoir size `C`.
- Explain, with numbers, why reducing contact alone fails when griefers or other carriers keep a reservoir alive, and why removing the reservoir alone fails when contact is high.
- Critique a design response (consent flags, segregation, removing the route, raising the cost) by the parameter it changes and the players it costs.

**Before class:** Foo, C. Y. & Koivisto, E. M. I. (2004), "Defining grief play in MMORPGs: player and developer perceptions", *Proceedings of ACE 2004*, pp. 245-250. Lofgren, E. T. & Fefferman, N. H. (2007), "The untapped potential of virtual game worlds to shed light on real world epidemics", *The Lancet Infectious Diseases* 7(9), pp. 625-629. Read both in full; each is short.

**Prerequisites from earlier courses:** [MMO401 week 2, agent-based modeling I](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w02-agent-based-modeling-i.md) tells the Corrupted Blood story as a case for agent models. This week treats it as a griefing case and uses a simpler aggregate model. [GD102 week 3, positive feedback loops](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md) and [GD102 week 4, negative feedback loops](../../GD102-systems-design-and-game-mechanics/lectures/w04-negative-feedback-loops-rubber-banding.md) (an epidemic is one of each). [MMO303 week 10, payoff matrices](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md). [GS101 week 9, graphical MMOs](../../GS101-history-and-critical-study-of-games/lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md) (Ultima Online's player-killing era). [MMO305 week 7, status and display](w07-status-prestige-and-conspicuous-display.md), since many griefers want an audience.

**Interactive:** [Plague reservoir](../examples/w08-plague-reservoir.html) (spec at the end of this lecture). Keep it open during section 2.

---

## 1. What counts as griefing

### A working definition

Foo and Koivisto (2004) interviewed players and developers and defined grief play as play styles that disrupt another player's gaming experience. Their definition has three parts that matter for design:

- The act is **intentional**. A new player who blocks a doorway by accident is not griefing.
- The griefer **enjoys** or benefits from the disruption. The victim's frustration is part of the payoff, or the disruption is the price the griefer pays for some other gain.
- The act usually stays **inside the game's rules** or exploits gaps in them. That is what makes griefing a design problem and not only a policy one. A hacker breaks the rules. A griefer finds what the rules allow.

Griefing is related to toxicity (next week), but it is not the same thing. Toxicity in team games is mostly about how teammates treat each other in a match. Griefing covers any use of the world's systems to spoil someone else's time, whether the victim is a teammate, an opponent or a stranger across the map.

### Four types

Foo and Koivisto sorted the incidents they collected into four categories. The labels and short descriptions below follow how later papers citing them summarise the scheme; we could not check the original's exact wording, so compare it when you read the paper. Each has a different payoff for the griefer, and so a different set of fixes.

| Type | What happens | Griefer's payoff | Typical system used |
|---|---|---|---|
| Harassment | Repeated unwanted attention: following, spamming, blocking, insulting, killing the same low-level player over and over | The victim's reaction | Chat, collision, open PvP |
| Power imposition | Showing power over a weaker player, often through unequal PvP or corpse camping | Feeling dominant, often with an audience | Level gaps, open PvP, respawn points |
| Scamming | Deceiving a player to take their items or money | Material gain | Trade, contracts, trust |
| Greed play | Following the rules to one's own advantage while ignoring others: kill stealing, ninja looting, hogging spawns | Material gain, with disruption as a side effect | Loot rules, shared spawns, need/greed rolls |

Two payoffs are hiding in that table. Harassment and power imposition are **reaction-driven**. The griefer wants the victim to notice, get angry and ideally complain in public. Scamming and greed play are **gain-driven**. The griefer wants the item, and the victim's pain is incidental. The distinction matters because the fixes differ:

- To stop reaction-driven griefing, remove the reaction or the audience. Mute, block, ignore, hide the griefer's messages, and deny them a stage.
- To stop gain-driven griefing, remove the gain. Change loot rules so a ninja looter cannot take items (personal loot), add trade confirmations, and make scams unprofitable.

A designer who answers harassment with loot changes, or scams with a mute button, is solving the wrong problem.

### A payoff view

It helps to write the griefer's decision like any other choice in MMO303 week 10's terms. A griefer acts when:

```
benefit (reaction, dominance, gain) > cost (time, risk of punishment, lost reputation)
```

Every design response changes one side of that inequality. Personal loot sets the gain from ninja looting to zero. A reputation system (MMO305 week 6) raises the cost of scamming by making it visible. A consent flag for PvP raises the cost of reaching a victim to infinity, since the victim can refuse. But there is a third lever that the payoff view hides, which is how many victims each griefer can reach. That lever is the subject of the worked example.

## 2. Worked example: Corrupted Blood and the griefer reservoir

### The hook

On 13 September 2005, World of Warcraft opened Zul'Gurub, a raid whose final boss, Hakkar the Soulflayer, cast a debuff called Corrupted Blood. The debuff drained health and jumped to nearby players. It was meant to last a few seconds, or until Hakkar died, and to stay inside the raid.

It escaped. Players could dismiss their pets while the pets carried the debuff, and when the pets were summoned again in a city, the debuff came with them. The developers had not included a way for the debuff to end on a dismissed pet. In crowded capitals like Ironforge and Orgrimmar it spread from player to player. Non-player characters could catch it and pass it on, but they could not die, so they became carriers. Low-level characters died almost at once.

Players behaved like a real population. Some fled to the countryside. Some healers rushed in to help and caught it themselves. And some players did the thing this week is about. They caught the plague on purpose and carried it into the busiest places they could find, to watch others die.

Blizzard tried voluntary quarantines, asking players to keep away from infected areas, which did little. Rolling server restarts cleared outbreaks that then came back. On 8 October 2005 a hard reset and a patch that made pets immune ended it. In 2007, epidemiologists Eric Lofgren and Nina Fefferman argued in *The Lancet Infectious Diseases* that the incident showed what real epidemic models leave out, which is the choices individuals make, from curiosity to deliberate spreading.

The puzzle for a designer is this. Why did asking players to avoid the cities fail, while a patch that touched only pets worked?

### The model

We use an **SIS model**: every player is either **Susceptible** (can catch it) or **Infected**. There is no lasting immunity. A player who dies resurrects at a graveyard and walks back into town as susceptible as before, which is why SIS fits better than models with a "recovered" group.

Take one city with `N` players present. Time moves in steps of one minute.

```
new infections per minute = β × S × (I + C) / N
leaving the infected group = γ × I

I(t+1) = I(t) + β × (N − I(t)) × (I(t) + C) / N − γ × I(t)
S = N − I
```

- `N` is the number of players in the city. We hold it constant.
- `I` is the number of infected players. `S = N − I` are susceptible.
- `β` (beta) is the **contact rate**: how many infections one infected carrier would cause per minute in a fully susceptible city. Crowding raises it. Players spreading out lowers it.
- `γ` (gamma) is the **exit rate**: the share of infected players who stop being infected each minute, because they die, are cured or leave. `1/γ` is the average time a player stays infected.
- `C` is the **reservoir**: carriers who spread the plague but never leave the infected group. In 2005, `C` was made of three things: infectious NPCs that could not die, pets re-summoned with the debuff, and griefers who kept themselves alive (often with healing) to carry it on purpose.
- `R0 = β / γ` is the **basic reproduction number**, the number of new infections one infected player causes before leaving, in a fully susceptible city.

Without a reservoir (`C = 0`), the rule from epidemiology holds. If `R0 < 1` the outbreak dies out. If `R0 > 1` it settles at `I* = N × (1 − 1/R0)`.

With a reservoir, the steady level `I*` solves `β × (N − I) × (I + C) / N = γ × I`, a quadratic:

```
a  = β × (N − C) − γ × N
I* = [a + sqrt(a² + 4 × β² × N × C)] / (2 × β)
```

When `I*` is small compared with `N` and `R0` is well below 1, a simpler approximation works:

```
I* ≈ C × R0 / (1 − R0)
```

That fraction, `R0 / (1 − R0)`, is the **reservoir amplifier**. Each permanent carrier keeps that many ordinary players sick at any moment.

### Numbers you can check

Use `N = 1,000` players in the city and `γ = 0.5` per minute (an infected player stays infected about two minutes, then dies or is healed). Start with 10 infected. These numbers are invented to show the mechanism, not measured from the 2005 servers.

**One step by hand.** With `β = 0.4` and `C = 20`, the first minute gives new infections `0.4 × 990 × 30 / 1,000 = 11.88` and exits `0.5 × 10 = 5`, so `I(1) = 10 + 11.88 − 5 = 16.88`.

**Steady states.**

| Contact `β` | `R0` | Reservoir `C` = 0 | `C` = 5 | `C` = 20 |
|---|---|---|---|---|
| 0.4 | 0.8 | 0 | 18.3 | 60.5 |
| 0.6 | 1.2 | 166.7 | 188.2 | 232.6 |
| 1.0 | 2.0 | 500.0 | 504.9 | 518.6 |

Check the top-right cell. `a = 0.4 × 980 − 500 = −108`. `a² + 4 × 0.16 × 1,000 × 20 = 11,664 + 12,800 = 24,464`, whose square root is 156.4. So `I* = (−108 + 156.4) / 0.8 = 60.5`. The approximation gives `20 × 0.8 / 0.2 = 80`, in the right range but high, because at 60 infected the susceptible pool has shrunk a little.

**Over time.** Infected players at selected minutes:

| Minute | `β` 0.4, `C` 0 | `β` 0.4, `C` 20 | `β` 1.0, `C` 0 | `β` 1.0, `C` 20 |
|---|---|---|---|---|
| 0 | 10 | 10 | 10 | 10 |
| 1 | 9.0 | 16.9 | 14.9 | 34.7 |
| 5 | 5.8 | 36.9 | 69.7 | 256.1 |
| 10 | 3.4 | 50.0 | 311.2 | 502.9 |
| 30 | 0.4 | 60.2 | 500.0 | 518.6 |

Now read the answer to the puzzle out of the tables.

- **Asking players to stay away** lowers `β`. Suppose a plea cut contact from 1.0 to 0.4. With no reservoir, the outbreak would die (first column). With a reservoir of 20, the city settles at about 60 infected and stays there for as long as the reservoir lasts (second column). To players standing in town, the plague "never goes away".
- **Removing the reservoir alone** while the city stays crowded (`β = 1.0`) barely helps. The fourth column settles at 519 and the third at 500. When `R0 > 1` the plague sustains itself.
- **Only both together** end it. Contact must fall below the threshold and the reservoir must go. Server restarts cleared `I` for a while but left the causes. The October patch removed the pet part of `C`, and the hard reset cleared the rest.

The reservoir matters most exactly when the other measures are working. As `R0` approaches 1, the amplifier `R0 / (1 − R0)` grows fast. At `R0 = 0.9` the approximation says each permanent carrier keeps nine players sick, and the exact model with a single carrier gives 8.3. That is the griefer's power. A handful of people who refuse to stop spreading a harm can undo a population-wide effort to contain it.

### A visual you can move

Open `examples/w08-plague-reservoir.html`. The top view plots infected players over 60 minutes for the current settings, with the no-reservoir curve drawn faintly behind it. The bottom view is a map of steady states: `R0` on the x-axis, `I*` on the y-axis, with one curve per reservoir size. Drag `β` down past the `R0 = 1` line and watch the `C = 0` curve drop to zero while the `C = 20` curve stays up. Then toggle "remove pets" and "remove griefers" separately to see how much of `C` each accounts for in the preset.

### Cross-game recognition

The SIS-with-reservoir shape turns up whenever a harm passes from player to player and some source keeps feeding it.

**Ultima Online, the Trammel and Felucca split (Renaissance expansion, May 2000).** Unrestricted player killing had driven many players out of Ultima Online's open world (GS101 week 9). Renaissance copied the map into two worlds. In Trammel, a player could not attack another without consent. Felucca kept open PvP. In our model, the split set `β` between killers and unwilling victims to zero in Trammel, since contact without consent became impossible. It did not remove the killers, who stayed in Felucca. Segregation works by lowering contact across groups, not by shrinking `C`.

**Second Life, self-replicating "grey goo" objects (2006).** Griefers built scripted objects that copied themselves until they overwhelmed the servers, and a November 2006 attack was reported by the BBC as a worm. In our terms this is a harm with a built-in reservoir that grows on its own. Each object makes more objects, so `C` is not fixed but rises every step. No contact-based measure helps. The only fixes act on the replication itself or remove the objects.

**World of Warcraft, the zombie plague event (22-28 October 2008).** Before Wrath of the Lich King launched, Blizzard ran a deliberate plague event. Infected players had ten minutes to find a cure or turn into zombies that could spread the infection further. Blizzard ended the event on 28 October after player complaints. This is Corrupted Blood rerun on purpose, with the designer setting `β` and `γ`. Even as a planned event, the zombies spread into areas where other players simply wanted to play, and the spreading was fun for exactly the players whose fun came from others' disruption. Designing a contagion mechanic means designing for griefers from the start.

Three games, one model. A harm spreads by contact. Some players or objects keep feeding it. The designer has two levers, contact and the reservoir, and needs to know which one is binding.

### Eyes-open design judgment

- **Find the reservoir first.** When a harm persists despite players avoiding it, look for something that never leaves the infected group. It may be an NPC, a bug or a small group of committed griefers. Removing a reservoir is often a small code change. Lowering everyone's contact rate is a large behaviour change.
- **Contact limits cost the innocent.** Quarantine requests, segregation and consent flags lower `β` for everyone, including the players who were never harmed. Trammel protected players who hated PvP and also emptied the world where PvP players found victims.
- **Be honest about the amplifier.** Near the threshold, a few griefers matter a lot. If moderation resources are limited, spend them on the carriers who never stop, not on the many who spread a harm once and quit.
- **Contagion mechanics are griefer mechanics.** Any effect that passes from player to player, including debuffs, curses, disguises and chat trends, will be used against unwilling players. Ask before launch who can carry it into places where people did not choose to play.
- **The Lancet paper's point cuts both ways.** Lofgren and Fefferman found the incident valuable because it included human choices. For you, those choices are the design material. Players who flee, help or spread are responding to what your systems make easy.

## 3. The toolbox of design responses

Here are the main responses a designer has, organised by which part of the problem they act on. Every one has a cost.

### Consent

Let players choose whether they can be affected. PvP flags, duel invitations, opt-in trading and Trammel-style rulesets all work this way. Consent defeats harassment and power imposition almost completely, because the griefer needs an unwilling victim. The cost is that some play only exists without consent. Ambushes, territory wars and the tension of an open world all depend on it. Games that sell those experiences, such as EVE Online, deliberately fold much of what other games call griefing (theft, scams, espionage) into legitimate play and expect players to stay cautious. That is a coherent design choice, but it has to be advertised so that players know which world they entered.

### Segregation

Put griefers and victims in different pools. Separate rule sets (Trammel and Felucca), separate servers, and matchmaking pools for players with bad records all do this. Next week you will see Dota 2's low-priority queue, where reported and abandoning players play only with each other until they win enough games. Segregation lowers contact across groups without banning anyone. The cost is that the griefer pool becomes miserable for any innocent player sent there by mistake, and population splits can make each side feel empty.

### Remove the route

Change the system that carries the harm. Pets that cannot hold debuffs. Collision turned off in towns so nobody can block a quest giver. Personal loot so ninja looting is impossible. Trade windows that show the full exchange before confirming. This is usually the cheapest and most complete fix when you can find the route. The cost is that the same system often supports legitimate play. Collision lets defenders hold a bridge, and group loot lets friends share items.

### Remove the payoff

Deny the griefer what they came for. Hide a harasser's messages from the victim without telling the harasser (a "shadow mute"). Make corpse camping pointless by letting a victim respawn elsewhere. Keep kill credit with whoever tagged a monster first so kill stealing gains nothing. Reaction-driven griefers stop when there is no reaction, and gain-driven griefers stop when there is no gain.

### Raise the cost

Make griefing expensive after the fact: reports, penalties, bans, reputation marks. Many games flag disruptive players and restrict who they play with, for example by marking them as bad sports and matching them with each other. Punishment works best on gain-driven griefers, who weigh costs. It works less well on reaction-driven griefers, for whom being punished can itself be a reaction worth provoking. The cost is moderation labour and false positives, which week 9 quantifies.

### Choosing among them

A useful order of questions:

1. What does the griefer gain? That tells you which payoff to remove.
2. What carries the harm? That tells you which route to change.
3. How many victims does each griefer reach? That tells you whether contact or the reservoir is binding.
4. Only then, what punishment backs it up?

Designers often start with step 4 because it is visible and feels decisive. The Corrupted Blood numbers show why that order is backwards. Punishing the spreaders one by one would have shrunk `C` slowly, while a patch to the route removed most of it at once.

## In-class activity (25 minutes)

In groups of three, take one of these griefing cases, or one from a game you play:

- A player follows new players around a starting zone and trains monsters onto them.
- A player in a crafting game buys every cheap copy of an ingredient and relists it at ten times the price.
- A group sits on a quest objective and kills it the moment it respawns, so no one else can finish the quest.

For your case:

1. Classify it with Foo and Koivisto's four types, and say whether it is reaction-driven or gain-driven.
2. Write the griefer's payoff inequality with the actual benefit and cost.
3. Name the route (the system that makes it possible) and the reservoir (what keeps it going if some griefers stop).
4. Propose two responses from section 3 that act on different parts of the problem. For each, name one group of innocent players it costs.

Expected output: a short card per case with the classification, the inequality, the route and reservoir, and two responses with their costs. One group presents; the others try to break their fix.

## Common misconceptions

- **"Griefers are just breaking the rules, so moderation is enough."** Griefers mostly use what the rules allow. Moderation handles the worst cases, but the systems decide how many cases there are.
- **"If we lower contact enough, the problem goes away."** Only if there is no reservoir. With 20 permanent carriers and `R0 = 0.8`, the model settles at about 60 infected, not zero.
- **"Removing the source is always enough."** Only if contact is below the threshold. With `R0 = 2`, removing all 20 carriers takes the steady state from 519 to 500.
- **"All griefing is about the victim's pain."** Scamming and greed play are about gain. The victim's pain is a side effect, so mute buttons do nothing and loot or trade rules do everything.

## Check yourself

1. A city has `N = 1,000`, `γ = 0.5` and `β = 0.45`. What is `R0`? Use the approximation to estimate `I*` with a reservoir of 10 carriers. What happens to the estimate if griefers push `β` up to 0.48?
2. With `β = 0.4`, `C = 20` and `I(0) = 60`, compute `I(1)`. Explain why the answer tells you 60 is close to the steady state.
3. A designer proposes that infected players cannot enter cities at all. Which parameter does this change, and what does the model predict if a single NPC in the city stays infectious?
4. Classify each as harassment, power imposition, scamming or greed play, and say which response in section 3 fits best. (a) A level-60 player repeatedly kills level-15 players at their respawn point. (b) A player promises to enchant an item, takes it and logs off. (c) A player rolls "need" on every item in a group dungeon, including items for other classes.

<details>
<summary>Answers</summary>

1. `R0 = 0.45 / 0.5 = 0.9`. The approximation gives `I* ≈ 10 × 0.9 / 0.1 = 90`. At `β = 0.48`, `R0 = 0.96` and the approximation gives `10 × 0.96 / 0.04 = 240`. The exact quadratic gives 56.4 and 77.4. Near the threshold the approximation overshoots, because inflow and outflow almost cancel and even a small drop in susceptible players matters. Both methods agree on the point. A 7% rise in contact raises the steady harm by about 37% (exact) because the system sits close to `R0 = 1`.
2. New infections `= 0.4 × 940 × 80 / 1,000 = 30.08`. Exits `= 0.5 × 60 = 30`. So `I(1) = 60.08`. Inflow and outflow almost cancel, which is what a steady state means.
3. It lowers `β` for players who carry the infection into the city, to zero in the ideal case. But a single infectious NPC is a reservoir with `C = 1` inside the city. If the city's own contact rate keeps `R0 < 1`, the city settles at a small positive level, roughly `R0 / (1 − R0)` players. If `R0 > 1`, that one NPC is enough to restart a full outbreak.
4. (a) Power imposition. Consent or respawn-location changes remove the payoff and the route; a level-gap PvP rule is the classic fix. (b) Scamming. Remove the route with a trade window that holds both sides' items until the service is done. (c) Greed play. Remove the payoff with personal loot or class restrictions on need rolls.

</details>

## Lab / assignment hook

[Lab 08, plague and reservoir](../labs/lab08.md). You build the reservoir SIS model in a spreadsheet, reproduce this lecture's tables, then plan a response to a new contagion mechanic under a fixed budget of "fix points" that can lower `β`, shrink `C` or raise `γ`. Deliverable: the sheet, a chart of your plan against the do-nothing curve, and a 300-word memo naming which lever was binding.

## Sources

- Foo, C. Y. & Koivisto, E. M. I. (2004). "Defining grief play in MMORPGs: player and developer perceptions." *Proceedings of the 2004 ACM SIGCHI International Conference on Advances in Computer Entertainment Technology (ACE '04)*, pp. 245-250. doi:10.1145/1067343.1067375. The definition and the four categories (harassment, power imposition, scamming, greed play), as summarised in later papers citing it.
- Lofgren, E. T. & Fefferman, N. H. (2007). "The untapped potential of virtual game worlds to shed light on real world epidemics." *The Lancet Infectious Diseases* 7(9), pp. 625-629. doi:10.1016/S1473-3099(07)70212-8.
- Balicer, R. D. (2007). "Modeling infectious diseases dissemination through online role-playing games." *Epidemiology* 18(2), pp. 260-261. Compares pet transmission and fast travel to real-world disease spread.
- Wikipedia, "Corrupted Blood incident" (accessed September 2026). Zul'Gurub opening on 13 September 2005; Hakkar the Soulflayer; pets and NPCs as carriers; deliberate spreading by players; self-quarantine and healers; rolling restarts; hard reset and pet immunity patch on 8 October 2005; the October 2008 zombie plague event (22-28 October 2008).
- Wikipedia, "Ultima Online" (accessed September 2026). Renaissance expansion on 4 May 2000 splitting the world into Trammel (no non-consensual player killing) and Felucca (open PvP).
- Wikipedia, "Second Life" (accessed September 2026). Self-replicating "grey goo" objects and the November 2006 attack reported by BBC News.
- Wikipedia, "Griefer" (accessed September 2026). EVE Online's inclusion of theft, scams and espionage in normal play; separate realms for consensual and non-consensual PvP; Grand Theft Auto Online marking disruptive players as "bad sports" who play in lobbies with each other.
- Liquipedia Dota 2 Wiki, "Priority" (accessed September 2026). Low priority triggers and restrictions, referenced in section 3.

## Interactive spec: examples/w08-plague-reservoir.html

**Purpose.** Show that a contact-spread harm with a permanent reservoir behaves differently from one without, and that the two levers (contact `β` and reservoir `C`) each fail alone.

**The one insight.** When contact is below the threshold, the reservoir sets the harm; when contact is above it, the reservoir hardly matters. You need to know which regime you are in.

**Model (exact).** Discrete time, one step = one minute, 60 steps.

```
I[0] = I0
I[t+1] = I[t] + beta*(N - I[t])*(I[t] + C)/N - gamma*I[t]
clamp I[t+1] to [0, N]
R0 = beta / gamma
steady state:  a = beta*(N - C) - gamma*N
               Istar = (a + sqrt(a*a + 4*beta*beta*N*C)) / (2*beta)
C = C_npc + C_pets + C_griefers
```

**Layout.**
- Top chart: infected `I[t]` for t = 0..60 (x: minutes, y: players 0..N). Solid line for current settings, faint line for the same settings with `C = 0`. Show the numeric `I[60]` and `Istar` beside the chart.
- Bottom chart: steady-state map. x-axis `R0` from 0 to 3, y-axis `Istar` from 0 to N. Three curves for `C = 0`, `C = 5`, `C = 20` (computed with the current `gamma` and `N`), plus a dot at the current `(R0, Istar)`. Vertical dashed line at `R0 = 1` labelled "threshold".
- Readout: `R0`, `Istar`, amplifier `R0/(1−R0)` (show "n/a above threshold" when `R0 >= 1`).

**Controls.**
- Slider `beta`, 0.05 to 1.5, step 0.01. Default 0.4.
- Slider `gamma`, 0.1 to 1.0, step 0.05. Default 0.5.
- Slider `N`, 200 to 2,000, step 100. Default 1,000.
- Slider `I0`, 1 to 100. Default 10.
- Three number inputs for the reservoir parts, each 0 to 50: `C_npc` (default 5), `C_pets` (default 10), `C_griefers` (default 5). Three checkboxes "remove NPC carriers", "remove pets (patch)", "remove griefers (ban)" that zero each part.
- Preset buttons: "2005 city" (beta 1.0, all reservoir parts on), "Stay-away plea" (beta 0.4, all on), "Pet patch only" (beta 1.0, pets removed), "Plea + patch + reset" (beta 0.4, all removed).

**Test values (N = 1,000, gamma = 0.5, I0 = 10).**

| beta | C | I[1] | I[10] | Istar |
|---|---|---|---|---|
| 0.4 | 0 | 9.0 | 3.4 | 0 |
| 0.4 | 20 | 16.9 | 50.0 | 60.5 |
| 1.0 | 0 | 14.9 | 311.2 | 500.0 |
| 1.0 | 20 | 34.7 | 502.9 | 518.6 |
| 0.6 | 5 | — | — | 188.2 |

**First screen.** Load the "Stay-away plea" preset so the student first sees a curve that levels off above zero next to a faint curve that dies out.

**Accessibility.** Keyboard-operable controls with visible focus; checkbox labels name the effect; chart lines distinguished by dash pattern as well as colour. Respect `prefers-reduced-motion` (no animated drawing of curves). No game art; players drawn as generic dots.
