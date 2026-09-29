# GD202 · Week 13 — Narrative in Multiplayer: Shared vs Personal Story

**Why this matters:** A single-player story can change the world because only one person lives in it. In an online game every change you write either reaches everyone, or it splits the world so that some players stop seeing each other. This week gives you one number that measures that split, so you can decide where your story is allowed to change things and what it costs in company.

**You will be able to:**
- Compute the visible share `V`, the expected number of visible players and the effective number of phases for a zone from its phase populations.
- Classify a story consequence by who sees it and how long it lasts, and predict the social cost of each class.
- Redesign a quest chain so that it keeps a visible world change while meeting a target for how many players stay visible to each other.
- Critique how shipped online games (World of Warcraft, Guild Wars 2, Star Wars: The Old Republic) divide story between the individual, the group and the whole server.

**Before class:** Bateman (ed.), *Game Writing: Narrative Skills for Videogames*, 2nd ed. (2021), the chapter on nonlinear structure (the course reader lists the pages). Reread it asking what happens when two players make different choices in the same place. Reread [MMO305 week 2, playing alone together](../../MMO305-social-systems-and-online-behaviour/lectures/w02-playing-alone-together.md), section 2. If you have a World of Warcraft or Guild Wars 2 account, spend 20 minutes in any zone with a long story chain and count how many other players you can see at each step.

**Prerequisites from earlier courses:** [MMO305 week 2, playing alone together](../../MMO305-social-systems-and-online-behaviour/lectures/w02-playing-alone-together.md) (why co-presence is not the same as playing together). [MMO301 week 12, persistence and time](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w12-persistence-and-time-what-should-last.md) (what a world should remember). [MA102 week 1, sample spaces and events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w01-sample-spaces-and-events.md) (the probability that two independent picks land in the same bucket). From this course, [week 4, dialogue systems and state flags](w04-dialogue-systems-and-state-flags.md) (flags as the memory of a choice) and [week 8, quest chains and zone storytelling](w08-quest-chains-and-zone-storytelling.md).

**Interactive:** [`examples/w13-phase-split.html`](../examples/w13-phase-split.html). Keep it open during section 2.

---

## 1. One world, many heroes

Every single-player story you studied this term rests on one quiet assumption. There is one protagonist, and the world bends around them. When you burn the village in a single-player game, the village is burned. Nobody else walks in the next day expecting it to be standing.

Put a thousand players on one server and that assumption breaks in two ways.

The first is the **hero problem**. Every player is told they are the one who saves the valley. They all kill the same bandit chief, and he is back ten minutes later for the next hero. Players accept a lot of this. They know the respawning chief is a convention, the way they know a stage play reuses its props. But the convention has a price. A world where nothing you do stays done is a world where your story choices feel like decoration.

The second is the **consistency problem**. Suppose you do let a player's action change the world. The bridge burns. Now what does the next player see? If they see the burned bridge, they have lost the quest that asked them to defend it. If they see the intact bridge, then two players standing side by side are looking at different worlds. The game has to decide which world each of them lives in, and whether they can still see each other.

Online games answer this with a small set of techniques. You will meet each in more detail below, but name them now.

- **Static world.** Nothing changes. Quests reset, bosses respawn, and the story is told *to* the player rather than *changed by* them. It is cheap and keeps everyone together.
- **Instanced personal story.** Story moments that change things happen in a private copy of a space. Only you and your party are inside. Outside, the shared world stays static.
- **Phasing.** The open world itself shows different versions to different players, based on their quest progress. You and a stranger can stand on the same spot and see different buildings, different NPCs, and sometimes not see each other at all.
- **Shared world change.** The server changes for everyone at once. Every player sees the same new world. Nobody is split off, but late arrivals missed the moment and cannot replay it.

Each technique puts consequence somewhere on two axes. One is who sees it. The other is how long it lasts. Section 3 turns that into a planning tool. First you need a way to measure what phasing costs, because it is the technique that looks free on paper and is not.

## 2. Worked example: the invisible friend

### The hook

World of Warcraft's Wrath of the Lich King expansion (November 2008) used phasing widely in its open world. A well-known case is the Wrathgate chain in Dragonblight. Players who have finished it see the area after the battle, scarred and burning. Players who have not see it untouched. The Warcraft Wiki describes how outdoor areas can look completely different depending on quest progress.

The feature made zones feel alive. It also produced a complaint that anyone who played with a friend at the time remembers. You log in together, you stand in the same camp, and you cannot see each other, because one of you is two quests further along. Players in different phases cannot see each other in the open world. Blizzard later added Party Sync in patch 8.2.5 (September 2019), which lets grouped players line up their quest state so they can play together. That fix exists because the problem was real.

So here is the puzzle. A zone has 41 players in it. You are one of them. How many of the other 40 can you actually see? Not 40. And the answer depends far more on *where* in the chain the phase changes happen than on how many there are.

### The model

Split the zone's players into phases. Phase `i` holds a share `p_i` of the zone's population, and the shares add up to 1.

Pick yourself and one other player at random. You are in phase `i` with probability `p_i`. The other player is in the same phase with probability `p_i`. Add over all phases:

```
V      = p_1² + p_2² + ... + p_n²      chance a random other player shares your phase
seen   = (N − 1) × V                   expected number of other players you can see
n_eff  = 1 / V                         effective number of phases
```

- `N` is the number of players in the zone, you included.
- `p_i` is the share of those players in phase `i`.
- `V` is the **visible share**. It runs from 1 (everyone together) down toward 0.
- `n_eff` is the **effective number of phases**. If the zone behaves like it has two equal halves, `n_eff = 2`, whatever the phase list says.

This treats players as landing in phases independently, which is close enough for a zone with dozens of people in it. It is the same sum Simpson proposed in 1949 to measure how concentrated a population is across species. You don't need that history, only the reading. `V` is the chance that a random stranger in the zone is in your world.

One more line matters as much as the average. A player standing in phase `i` sees about `p_i × (N − 1)` others. The average `V` can look fine while the players in the smallest phase are nearly alone.

### Numbers you can check

Take a zone of `N = 41`, so each player has 40 others around them. The chain has five steps. The shares below are a typical funnel. More players are early in the chain than late, because some quit, some leave the zone, and new players keep arriving.

```python
def visible_share(shares):
    """Chance that a random other player in the zone is in your phase."""
    return sum(p * p for p in shares)

zone = 41  # you plus 40 other players
cases = {
    "no phasing":            [1.0],
    "two equal phases":      [0.5, 0.5],
    "every step phases":     [0.30, 0.25, 0.20, 0.15, 0.10],
    "finale only":           [0.90, 0.10],
    "finale with a choice":  [0.90, 0.05, 0.05],
}
for name, shares in cases.items():
    v = visible_share(shares)
    print(f"{name:22s} V={v:.3f}  sees {v * (zone - 1):4.1f} of 40  "
          f"phases_eff={1 / v:.2f}")
```

It prints:

```
no phasing             V=1.000  sees 40.0 of 40  phases_eff=1.00
two equal phases       V=0.500  sees 20.0 of 40  phases_eff=2.00
every step phases      V=0.225  sees  9.0 of 40  phases_eff=4.44
finale only            V=0.820  sees 32.8 of 40  phases_eff=1.22
finale with a choice   V=0.815  sees 32.6 of 40  phases_eff=1.23
```

Check the "every step phases" row by hand: `0.09 + 0.0625 + 0.04 + 0.0225 + 0.01 = 0.225`, and `0.225 × 40 = 9`. A zone with 40 other people in it feels like it has 9.

Now compare rows. Here is the same information arranged the way a designer needs it:

| Design | Phases | V | Others you see (of 40) | Seen by a player in the smallest phase |
|---|---|---|---|---|
| No phasing | 1 | 1.000 | 40.0 | 40.0 |
| Two equal phases | 2 | 0.500 | 20.0 | 20.0 |
| Every step phases | 5 | 0.225 | 9.0 | 4.0 |
| Phase only at the finale | 2 | 0.820 | 32.8 | 4.0 |
| Finale with a two-way choice | 3 | 0.815 | 32.6 | 2.0 |

Three things stand out.

**Where matters more than how many.** "Two equal phases" and "finale only" both have two phases. One halves the zone. The other costs about seven players. The difference is that the finale phase holds only 10% of the zone, so most people are never split from most other people. A phase change late in a chain is cheap for the zone. A phase change early is expensive, because it splits the crowd while it is still large.

**A choice at the end adds almost nothing to the average.** Splitting the finale 10% into two 5% halves moves `V` from 0.820 to 0.815. Branching feels like the dangerous part to writers, and in week 3 it was the dangerous part for scope. Here the branch barely shows, because squares of small numbers are tiny.

**The average hides who pays.** In every phased design, the players who went furthest are the loneliest. They are 10% of the zone, so they see about 4 others. With the choice, each ending holds 5% and sees 2. Those are your most invested players, at the climax of your zone's story, standing in an empty field. `V` can be 0.8 and the ending can still feel dead.

Open the interactive now. The left panel shows the zone as the server holds it, with 40 dots coloured by phase. The right panel shows what *you* see, which is only the dots in your phase. Drag the "phase at step" markers earlier and later in the chain and watch the right panel empty and fill. Then switch "you are in" to the last phase. The left view looks like a busy zone. The right view is the truth for the player who finished your story.

### Cross-game recognition

The formula does not care *why* players are split. Story phasing, capacity copies and private instances all fit it. Learning to see them as the same sum is the point.

**World of Warcraft Classic layering (2019).** [GD201 week 11](../../GD201-level-and-world-design/lectures/w11-shared-spaces-designing-for-many-players.md) met layering as a crowding tool. Here it is a phase split. When Classic launched in August 2019 (patch 1.13.2), each realm ran several **layers**, copies of the outdoor world, to spread crowds. The Warcraft Wiki notes that players can only see others on the same layer. That is phasing driven by capacity, not story. With `L` equally full layers, `V = L × (1/L)² = 1/L`. Three layers mean you see a third of the realm. Blizzard removed layering in November 2019, before the game's second content phase, so that realms became single shared worlds again. The layers solved crowding at launch and cost the realm's sense of one population, the exact trade this formula measures.

**Guild Wars 2 (2012): both ends of the scale in one game.** Guild Wars 2 splits its story on purpose. The **personal story** runs in instances tied to one character. Other players can join and help, but the Guild Wars 2 Wiki notes that they cannot make the choices that change the outcome. Inside, `V` is effectively 0 for strangers. The open world runs **dynamic events** instead. They are shared by everyone nearby, scale with how many players join, and chain so that success or failure changes what happens next. Every participant gets full credit. For the open world, `V = 1`. Everyone sees the same fort under attack and the same fort retaken. The price is that the change does not last. The event chain cycles, and the fort falls again later. Guild Wars 2 put permanent personal consequence where it costs no company, and shared consequence where it can afford to be temporary.

**Star Wars: The Old Republic (2011): collapsing a group back to one phase.** In a four-player group conversation, each player picks their own response, and the game makes a conversation roll among the group. The wiki sources cited below document the rolls but do not spell out what the winner gets. Players' accounts of the launch-era system say the winning player's response is the one the scene plays, and this section assumes that. Before Game Update 7.0, the game awarded social points for talking to NPCs in a group, with more for larger groups and for winning rolls. In phase terms, four people making four choices could produce four personal worlds. The roll forces them back into one, so `V = 1` inside the group. The cost is agency. Three players did not get their line. The social points pay them for accepting it.

**World of Warcraft's Gates of Ahn'Qiraj (patch 1.9, January 2006).** Each realm ran a server-wide war effort, collecting resources, until a player holding the Scepter of the Shifting Sands rang the gong and opened the gates. A ten-hour war followed across the realm, and players who rang the gong during that window received a unique mount. The gates then stayed open for everyone on that realm. This is the other extreme from phasing. The change reached all players at once, so no one was split and `V` stayed at 1. The cost fell on time rather than space. A player who joined a month later lived in the changed world but never saw it change. After patch 3.0.8a (February 2009), new realms started with the gates already open.

Four games, one question. How does the design move `V`? Phasing lowers it to buy personal consequence. Layering lowers it to buy server capacity. Instances set it to zero for strangers and keep it at one for the party. Rolls and server-wide events hold it at one and pay in agency or in timing.

### Design judgment

`V` is not a score to maximise. A zone with `V = 1` and nothing changing is a zone where story choices do nothing. The question is where you spend the drop in `V`, and who pays for it.

- **Phase late, and phase small.** Put world-changing phases near the end of a chain, where few players are. A change at step 2 of 10 splits most of the zone for most of its life.
- **Make the phased area local.** A burned farmhouse can be a phased area of 50 metres. Players inside it are split. Players on the road outside are not. The formula applies to the population of the phased *area*, not the zone.
- **Fold phases back.** When a chain ends, return players to a common state. A phase that only exists for the length of a chain costs company only while players are in it.
- **Watch the smallest phase.** Before you ship, compute `p_i × (N − 1)` for the last phase at a realistic population. If it is under about 3, your climax happens alone. Either instance it honestly, so the player expects to be alone, or move it back into the shared world.
- **Give groups a way back in.** Party Sync is a fix after the fact. Build yours before launch. Let a group leader's phase win for the group, or let finished players "replay" into a friend's phase.
- **Decide what the latecomer sees.** For every shared change, write down what a player who arrives six months later experiences. If the answer is "a changed world with no explanation," you owe them a recap.

## 3. A consequence budget: who sees it, and how long

Every consequence in your quest design sits on two axes.

- **Scope.** Who sees the result: only me, my group, or everyone on the server.
- **Duration.** How long it lasts: until the chain ends, until the next reset, or for good.

| | Temporary | Permanent |
|---|---|---|
| **Only me (or my party)** | An instanced quest step. Private and safe, forgotten when you leave. | Phasing, personal story instances. Your world remembers. Costs `V`. |
| **Everyone** | Cycling world events, respawning bosses. Shared, then reset. | Server-wide one-time change. Shared history. Costs latecomers. |

Each cell has a natural use.

**Personal and temporary** is where you put action that would be absurd if others saw it. You escort the prisoner, and it would be strange if twenty other players escorted the same prisoner at the same time. The quest takes place in a private copy and resets.

**Personal and permanent** is where you put choices that define *your* character. Your faction, whom you spared, which companion trusts you. These are the choices week 2 called authorship. In an online game they must either live in instances and dialogue, where they cost nothing, or in phases, where they cost company.

**Shared and temporary** is where you put public drama. The dragon attacks the town every two hours. Everyone near the town fights it. The drama is real while it happens and the world returns to normal after. Guild Wars 2's dynamic events live here.

**Shared and permanent** is where you put history. A patch changes the capital. A realm opens its gates. These moments create the stories players tell each other for years, precisely because they happened once. They are also expensive to build, impossible to test fully (week 14 returns to this), and they leave late arrivals behind.

A good zone uses several cells on purpose. As a rule of thumb, a design that puts everything in one cell has a problem you can name. All personal-permanent, and the world empties. All shared-temporary, and nothing matters. All shared-permanent, and the game becomes a museum of events you missed.

### Filling in the budget

For each quest in a chain, write three answers before you write any dialogue.

1. **What changes?** A flag, an NPC's state, a visible piece of the world.
2. **Which cell?** Scope and duration.
3. **What does a stranger see?** Someone at a different point in the chain, standing next to this player. Do they see the change? Do they still see this player?

Question 3 catches most problems early. If the answer is "the stranger sees an NPC the player just killed," you have a continuity break. If the answer is "the stranger cannot see the player at all," you have a `V` cost, and it should be one you chose.

## 4. Writing for a group

Even inside one phase, group play strains a story written for one person. Four players in a party hear the same quest text. Only one of them clicked "accept" first. Who is the hero?

### Shared credit, shared voice

The mechanical question is credit. Does everyone in the party get quest progress for the kill? Most modern games say yes, and Guild Wars 2 extends that to strangers who simply joined an event. The narrative question is harder. When an NPC thanks "you," which of four players do they mean?

Some patterns that work:

- **Write to the group.** Use "you and your companions" or plural address when a quest can be shared. It costs a few words and removes an obvious seam.
- **Give each player a role in the scene.** If a quest needs three levers pulled, three players have something to do and the NPC can refer to "whoever held the east gate."
- **Let one choice stand for the group, and say so.** If only the party leader's choice counts, show that before the choice, not after. Players accept being outvoted more easily than being surprised.
- **Record personal choices privately.** A group scene can play one outcome while each player's own flag records what *they* chose. The next time they talk to that NPC alone, the NPC can remember it. This keeps `V = 1` in the scene and gives authorship back afterwards.

### The latecomer and the veteran

The second group problem is time. A veteran helping a new friend has already seen the chain. The veteran's world is in the final phase. The friend's is in the first. Without a tool like Party Sync, they cannot even see each other. With one, the veteran replays content they know by heart.

You cannot remove this cost, but you can make it cheaper for the veteran. Give veterans something to do in early content, such as a mentor reward, alternate dialogue that acknowledges they know how this ends, or a small role the new player does not have. [MMO305 week 11](../../MMO305-social-systems-and-online-behaviour/lectures/w11-newcomers-and-mentoring-systems.md) covers mentoring systems in detail.

### The hero problem, written around

Players will always know that thousands of others killed the same boss. Games handle this in a few ways, and each is a writing choice rather than a technical one.

- **Make the player one of many.** Present the player as a member of an army, guild or order. The story is about the group winning, and the player is one hand in it.
- **Keep the villain's defeat inside an instance.** In the instance, you really did kill him. In the shared world, the story has moved on to what happens next, which everyone can share.
- **Let the world move on in patches.** Instead of letting each player end the story, end it for everyone at a fixed date with a shared change. This moves the climax from the personal-permanent cell to the shared-permanent cell.

None is correct. Each shifts where the story's weight sits, and each has a `V` cost, a timing cost or an agency cost you should be able to name.

## In-class activity (25 minutes)

Work in groups of three. You are the narrative designers for a zone with a six-step chain and a population of about 41 players during peak hours.

1. **Sketch (5 min).** Write a six-step chain for a zone of your choice. Mark every step that changes the visible world.
2. **Estimate the funnel (5 min).** Assign a share of the zone's players to each position (start, after step 1, ..., finished). Shares must add to 1. Assume more players early than late.
3. **Compute (5 min).** Treat each world change as a phase change. List the phase shares. Compute `V`, the expected number of visible others, and what a player in the smallest phase sees. Use the interactive's custom mode to check.
4. **Redesign (10 min).** Your producer sets two targets. A typical player sees at least 20 of the 40 others, and a player in the finale phase sees at least 3. Change the chain to meet both targets while keeping at least one visible world change. You may move changes later, make them local, fold them back, or move them into an instance.

Expected output: a before-and-after table with the phase shares, `V` and the smallest-phase number, plus two sentences on what the story lost and what it kept.

## Common misconceptions

- **"More phases always means a lonelier zone."** The number of phases matters much less than their sizes. A zone with five phases where 90% of players share one has `V` above 0.8. A zone with two equal phases has `V = 0.5`.
- **"If the average is fine, the zone is fine."** `V` is an average over all players. The players in the smallest phase see `p_i × (N − 1)` others, and in a phased chain those are the players at your climax.
- **"Instancing is the lazy option."** An instance is a phase with `V = 0` for strangers and `V = 1` for your party, and it tells the player honestly that they are alone. That is often better than a phase that pretends the world is shared while hiding everyone.
- **"A permanent server-wide change keeps everyone together, so it is free."** It keeps everyone in one world, but it splits players across time. The moment itself happens once, and every player who arrives later lives with the result without having seen it.

## Check yourself

1. A zone has 31 players. Phase shares are 0.6, 0.3 and 0.1. How many others does a typical player see? How many does a player in the 0.1 phase see?
2. Layering puts a realm's players into 4 equal layers. What is `V`? If one layer is closed and its players spread evenly over the other three, what does `V` become?
3. A designer says: "Our chain has eight phase changes, but they are all in the last two quests." Estimate whether this is a problem, and name the one number you would want to see before deciding.
4. Place each of these in the consequence table (scope, duration): a town raid that repeats every three hours; a companion who leaves you forever if you insult her; a capital city rebuilt in a patch.
5. In a four-player group conversation decided by a roll, what is `V` for the group? What does the design give up to reach that value, and how could it return some of it?

<details>
<summary>Answers</summary>

1. `V = 0.36 + 0.09 + 0.01 = 0.46`. With 30 others, a typical player sees `0.46 × 30 = 13.8`. A player in the 0.1 phase sees `0.1 × 30 = 3`.
2. `V = 4 × 0.25² = 0.25`. After closing one, three equal layers give `V = 1/3`, about 0.333. You see a third of the realm instead of a quarter.
3. Probably not a problem for the average, because few players are in the last two quests at any time, so most of the zone shares the base phase and `V` stays high. The number to check is the population of the smallest phase near the end, `p_i × (N − 1)`. Eight changes near the end can split the finishing players into many tiny phases where each sees one or two others.
4. Town raid: shared, temporary. Companion leaving: personal, permanent. Rebuilt capital: shared, permanent.
5. `V = 1` inside the group, since the roll forces one outcome. The design gives up agency for the three players whose responses lost. It can return some of it by recording each player's own choice in a private flag and letting NPCs remember it in later solo conversations.

</details>

## Lab / assignment hook

[Lab 13, phase budget for a zone](../labs/lab13.md). You implement the visible-share model in Python for a quest chain with choices, run it on a zone that fails its targets, and redesign the zone until it passes. The redesigned chain and its consequence table feed the final quest-chain project.

## Sources

- Warcraft Wiki, "Phasing". Players in different phases cannot see each other unless grouped with Party Sync; phasing used widely from Wrath of the Lich King; the Wrathgate example of outdoor areas changing with quest progress; terrain phasing added in Cataclysm. https://warcraft.wiki.gg/wiki/Phasing
- Warcraft Wiki, "Wrath of the Lich King". Release date 13 November 2008.
- Warcraft Wiki, "Party Sync". Added in patch 8.2.5 (24 September 2019).
- Warcraft Wiki, "Layering". Added with WoW Classic in patch 1.13.2 (26 August 2019); players only see others on the same layer; layering disabled from 13 November 2019, before Phase 2.
- Warcraft Wiki, "Ahn'Qiraj War Effort" and "Gates of Ahn'Qiraj". Patch 1.9.0 (3 January 2006), per-realm war effort, gong rung with the Scepter of the Shifting Sands, ten-hour war, gates open on new realms after patch 3.0.8a (February 2009).
- Guild Wars 2 Wiki, "Personal story". Character-specific instances; helpers cannot make choices that affect the outcome. "Event": dynamic events shared by nearby players, scaling, chained outcomes, full participation credit. "Guild Wars 2": release 28 August 2012.
- Star Wars: The Old Republic Wiki (Fandom), "Social tier", and the in-game codex entries "Conversations" and "Social Points" (launch era, December 2011). Social points earned by talking to NPCs in a group, more for larger groups and for winning conversation rolls; system replaced in Game Update 7.0.0. Wookieepedia, "Star Wars: The Old Republic", for the 20 December 2011 release.
- Simpson, E. H. (1949). "Measurement of diversity." *Nature* 163, 688. The sum of squared shares as a concentration measure.
- Bateman, C. (ed.) (2021). *Game Writing: Narrative Skills for Videogames*, 2nd ed. Bloomsbury.

## Interactive spec: examples/w13-phase-split.html

**The one insight the visual must make obvious:** the same zone looks full to the server and empty to the player, and *where* a phase change sits in the chain decides how empty, far more than how many phase changes there are. The player at the end of the story is the loneliest.

**Layout.** Two linked panels side by side on desktop, stacked on mobile (server view on top).

- **Left, "The zone (server view)".** `N − 1` dots (default 40) plus one outlined dot for "you", scattered in a fixed pseudo-random layout (seeded, so positions do not jump when controls change). Each dot is coloured by its phase. Legend lists phases with their share and count.
- **Right, "What you see".** The same layout, but only dots in your phase are drawn; the rest fade to 8% opacity outlines (with reduced motion, no fade animation). A large number above it: "You can see K of 40 players", where K is the count of dots actually in your phase in this layout. Under it, smaller: "Expected: (N − 1) × p_you = X.X".
- **Below both, a stat row:** `V`, expected visible others `(N − 1) × V`, `n_eff = 1 / V`, and "smallest phase sees" `min_i p_i × (N − 1)`. `V` to 3 decimals; counts to up to 2 decimals, with a trailing zero dropped (so 11.04 and 32.8), because the Saltmarsh test value needs 2.

**Controls.**

1. **Chain strip.** Six step buttons in a row (steps 1 to 6). Clicking a step toggles "this step changes the world" (a phase change). Keyboard: each is a toggle button with `aria-pressed`.
2. **Choice toggle** on any phase-changing step: "splits players 50/50" (two options). Later phase changes multiply the phases, as in the lab.
3. **Funnel shape** select: "Front-loaded" `[0.20, 0.20, 0.15, 0.15, 0.10, 0.10, 0.10]` (default), "Even" (7 × 1/7), "Back-loaded" `[0.10, 0.10, 0.10, 0.15, 0.15, 0.20, 0.20]`. Position k means "completed steps 1..k"; position 0 is "not started".
4. **Zone population N** slider, 5 to 101, default 41.
5. **"You are in"** select listing current phases, default the largest phase.
6. **Presets** (buttons): "No phasing", "Every step phases" (steps 1 to 4 phase, funnel set so shares are 0.30, 0.25, 0.20, 0.15, 0.10 by using a custom funnel `[0.30, 0.25, 0.20, 0.15, 0.10, 0, 0]` with steps 1, 2, 3, 4 phasing), "Finale only" (step 6 phases, custom funnel `[0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.10]`, giving 0.9 / 0.1), "Saltmarsh" (the lab zone: step 2 phases "flooded", step 4 is a 60/40 choice, step 5 phases "knight_dead", front-loaded funnel).

**Dot assignment.** Assign dots to phases by largest-remainder rounding of `p_i × (N − 1)` so counts sum to `N − 1`; put "you" in the selected phase. This makes K match the expected value to within rounding.

**Formulas.** Phase shares computed exactly as `phase_shares` in the lab (players at position k have completed steps 1..k; each phase-changing step appends a flag; a choice splits by its fractions). `V = Σ p_i²`; `seen = (N − 1) V`; `n_eff = 1/V`.

**Test values (must match).**

| Setting | V | Expected seen (N = 41) | Smallest phase sees |
|---|---|---|---|
| No phasing | 1.000 | 40.0 | 40.0 |
| Shares 0.30/0.25/0.20/0.15/0.10 | 0.225 | 9.0 | 4.0 |
| Finale only 0.9/0.1 | 0.820 | 32.8 | 4.0 |
| Finale 0.9/0.05/0.05 | 0.815 | 32.6 | 2.0 |
| Saltmarsh preset | 0.276 | 11.04 | 1.6 |

**First screen.** Load with the "Every step phases" preset and "you are in" set to the last phase, so the right panel shows about 4 dots against a full left panel. One line of caption: "40 players in the zone. You can see 4 of them."
