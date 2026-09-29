# MMO406 · Week 13 — Community Lore and Roleplay

**Why this matters:** After launch, the people writing the most words in your world are your players. Roleplayers improvise scenes in your taverns every night, wiki editors decide which version of your history most players read, and guilds build histories you never planned. You can't control any of this, but your bible and your map decide whether it thrives. This week you learn to size the places where roleplay happens, and to write a setting that leaves room for players' stories without letting them overwrite yours.

**You will be able to:**
- Compute the chance that a roleplay hub has a scene running, and the share of roleplayers who find one, from the number of roleplayers online, the number of hubs and the cast a scene needs.
- Derive the number of hubs that gives the most live scenes, and explain why the answer depends on the hour and on the size of the scenes.
- Critique how World of Warcraft, Final Fantasy XIV and Guild Wars 2 concentrate or scatter their roleplay communities, in the terms of one model.
- Design a community chapter for your world bible with named hubs, open slots for player characters, a naming rule and a policy for absorbing player history.

**Before class:** Steinkuehler and Williams, "Where Everybody Knows Your (Screen) Name: Online Games as 'Third Places'" (*Journal of Computer-Mediated Communication*, 2006), the introduction and the section on Oldenburg's characteristics of third places (about 20 minutes). Warcraft Wiki, "Roleplaying" (the sections on basic expectations and roleplaying terms, 10 minutes). Wolf, *Building Imaginary Worlds* (2012), chapter 7, "Circles of Authorship," the parts on audiences and fans who add to a world (use the contents page, about 15 pages).

**Prerequisites from earlier courses:** [MA102 week 6, the binomial distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md) (this week uses its limit for many players and small chances) and [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md). [GD201 week 11, shared spaces](../../GD201-level-and-world-design/lectures/w11-shared-spaces-designing-for-many-players.md) (the average crowd at a camp, `f × P / H`; this week adds chance and a minimum cast). [MMO301 week 11, Koster's laws](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w11-kosters-laws-of-online-world-design.md) (why roleplay quality falls as crowds grow, `(1 − f)^n`). [MMO305 week 4, guilds](../../MMO305-social-systems-and-online-behaviour/lectures/w04-guilds-formation-lifecycle-leadership.md) (critical mass in a group over weeks). From this course, [week 5](w05-cultures-languages-names.md) (naming languages), [week 8](w08-player-agency-vs-canon.md) (world canon and personal canon) and [week 11](w11-retcons-and-continuity.md) (canon tiers).

**Interactive:** [Roleplay hubs](../examples/w13-rp-hubs.html). Keep it open during section 2.

---

## 1. Two kinds of authors

Until now, every author in this course worked for you or under your licence. Four kinds of community lore come from people who don't.

1. **Roleplay (RP).** Players act as their characters, in character (IC), usually through chat, emotes and positioning. What they say out of character (OOC) is marked off, often with double parentheses. Roleplay is improvised fiction set in your world and performed in your spaces.
2. **Headcanon and fanon.** A **headcanon** is one player's private belief about something the canon leaves open: what their character's village is called, why a minor noble house fell. When a headcanon spreads through a community and becomes a shared assumption, it is called **fanon**. Fanon behaves like canon inside the community that holds it, and it can clash with the next patch.
3. **Community reference works.** Fan wikis often become the de facto bible for players. WoWWiki, the ancestor of today's Warcraft Wiki, launched on 24 November 2004, the day after World of Warcraft released. The Unofficial Elder Scrolls Pages began in 1995 and switched to a wiki in 2005. What those pages say, and which contradictions they flag, shapes what most players believe your canon is.
4. **Player history.** Things players actually did: wars, betrayals, record battles. EVE Online's battle of B-R5RB in January 2014 destroyed 75 titans, and CCP placed a permanent monument of wrecks, the Titanomachy, in the system where it happened.

All four share a property that week 8 named. They are **personal or community canon**, true for the people who made them, and they live alongside your **world canon**. Your job is not to police them. Your job is to give them places to happen, room to grow, and a clear rule for how, if ever, they cross into your canon.

The worked example starts with places, because roleplay needs other roleplayers present, and whether a gathering place works is arithmetic.

## 2. Worked example: why everyone roleplays in one tavern

### The hook

Final Fantasy XIV has dozens of worlds (its word for servers) in North America, and none of them is officially a roleplay world. Roleplayers picked one anyway. By players' own accounts, Balmung, on the Crystal data center, became the community's de facto roleplay world. Square Enix has never said so, and the evidence is player posts. By 2022, posters on a roleplay forum named Balmung and Mateus, both on Crystal, as the two most active. When a world gets too full, the game marks it "Congested" and blocks new characters and transfers. Players on Square Enix's own forums have complained about Balmung's congestion since at least 2017, and roleplayers name their own community as part of the cause. A 2017 forum post asked Square Enix to designate an official roleplay world, arguing that roleplayers need a central place to find each other.

And inside those worlds, the pull goes further. Roleplay community forums describe most walk-up roleplay happening in one city, Ul'dah, and much of it around a single tavern, the Quicksand.

So a community with dozens of servers and hundreds of rooms chooses one server, one city and one bar, and accepts the queues and the lockouts that follow. Is this herd behavior, or is it the only arrangement that works?

### The model

A roleplay scene needs a cast. A tavern scene might need four people: someone to serve, someone with a problem, and at least two to react. Call that minimum cast `k`.

Suppose that at a given hour, `Λ` (capital lambda) roleplayers are in your capital looking for a scene, and the city offers `H` hubs where roleplay happens: taverns, plazas, the temple steps. Each roleplayer drifts to one of the hubs. Assume, for now, that they choose evenly and independently.

Then the number of roleplayers at one hub follows a **Poisson distribution**. You met the binomial in MA102 week 6: `n` independent trials, each succeeding with probability `p`. When `n` is large and `p` is small, the binomial count is almost exactly Poisson with mean `λ = n × p`. Here each of the `Λ` roleplayers picks this hub with chance `1/H`, so the mean crowd is `λ = Λ / H`.

```
Mean crowd at a hub:               λ = Λ / H
Chance a hub has j roleplayers:     P(N = j) = e^(−λ) × λ^j / j!
Chance a hub has a scene:           P_k(λ) = P(N ≥ k) = 1 − Σ_{j=0}^{k−1} e^(−λ) λ^j / j!
Live hubs (expected):               V = H × P_k(λ)
Share of roleplayers in a scene:    S = P_{k−1}(λ)
```

- `Λ` is the number of roleplayers looking for a scene in the city at that hour.
- `H` is the number of hubs they spread across.
- `k` is the minimum cast for a scene.
- `V` counts **live hubs**, the hubs where a scene can run. It is the designer's number: how many stages are active tonight.
- `S` is the share of roleplayers standing in a live hub. It is the player's number: when I walk in, is anything happening?

The last line needs one step. A roleplayer is in a scene if their hub has at least `k` people, counting themselves. The Poisson distribution has a convenient property: seen from one of the people at a hub, the number of *others* there is again Poisson with the same mean. So "at least `k` including me" is "at least `k − 1` others", and `S = P_{k−1}(λ)`.

GD201 week 11 computed the average crowd at a camp, `f × P / H`. This model keeps that average and asks a sharper question. A scene doesn't care about the average. It cares whether tonight's crowd reaches `k`.

### Numbers you can check

Take *Thornmere*'s capital at prime time. Call it Dikeholm, the city built after the Drowning took the old capital. The community team estimates `Λ = 24` roleplayers in the city looking for scenes at 9 p.m., and scenes need `k = 4`.

| Hubs `H` | Mean crowd `λ` | Chance a hub is live `P_4` | Live hubs `V` | Roleplayers in a scene `S` |
|---|---|---|---|---|
| 1 | 24.0 | 100.0% | 1.00 | 100.0% |
| 2 | 12.0 | 99.8% | 2.00 | 99.9% |
| 3 | 8.0 | 95.8% | 2.87 | 98.6% |
| 4 | 6.0 | 84.9% | 3.40 | 93.8% |
| 5 | 4.8 | 70.6% | 3.53 | 85.7% |
| 6 | 4.0 | 56.7% | 3.40 | 76.2% |
| 8 | 3.0 | 35.3% | 2.82 | 57.7% |
| 12 | 2.0 | 14.3% | 1.71 | 32.3% |

Check the `H = 6` row by hand. The mean crowd is `24 / 6 = 4`. The chance of fewer than four is `e^(−4) × (1 + 4 + 16/2 + 64/6) = 0.01832 × 23.667 = 0.4335`, so `P_4 = 0.567`, and `V = 6 × 0.567 = 3.40`. For `S` you need fewer than three others, `e^(−4) × (1 + 4 + 8) = 0.238`, so `S = 76.2%`.

Read the two right-hand columns separately.

- **Live hubs rise, peak and fall.** More hubs mean more stages, until they spread the crowd too thin. The peak here is five hubs, with 3.5 live scenes on an average night. At twelve hubs, the city has fewer live scenes than it had with two.
- **Roleplayers in a scene only fall.** Every hub you add lowers the chance that the person walking in finds something happening. At five hubs, one roleplayer in seven sits in an empty room. At twelve, two in three do.

You can reproduce the table:

```python
from math import exp, factorial

def p_at_least(lam, k):
    """Chance a Poisson count with mean lam is at least k."""
    return 1 - sum(exp(-lam) * lam**j / factorial(j) for j in range(k))

LAMBDA, k = 24, 4
for H in (1, 2, 3, 4, 5, 6, 8, 12):
    lam = LAMBDA / H
    live = H * p_at_least(lam, k)
    share = p_at_least(lam, k - 1)
    print(f"H={H:>2}  lam={lam:5.2f}  P={p_at_least(lam, k):6.1%}  V={live:4.2f}  S={share:6.1%}")
```

It prints:

```
H= 1  lam=24.00  P=100.0%  V=1.00  S=100.0%
H= 2  lam=12.00  P= 99.8%  V=2.00  S= 99.9%
H= 3  lam= 8.00  P= 95.8%  V=2.87  S= 98.6%
H= 4  lam= 6.00  P= 84.9%  V=3.40  S= 93.8%
H= 5  lam= 4.80  P= 70.6%  V=3.53  S= 85.7%
H= 6  lam= 4.00  P= 56.7%  V=3.40  S= 76.2%
H= 8  lam= 3.00  P= 35.3%  V=2.82  S= 57.7%
H=12  lam= 2.00  P= 14.3%  V=1.71  S= 32.3%
```

### The best crowd per hub

Where is the peak of `V`? Write `V = Λ × P_k(λ) / λ`. For a fixed `Λ`, the best number of hubs is the one that makes `P_k(λ) / λ` largest, and that depends only on `k`. Maximizing it numerically gives a **best crowd per hub** `λ*`:

| Minimum cast `k` | Best mean crowd `λ*` | Chance a hub is live at `λ*` | Roleplayers in a scene at `λ*` |
|---|---|---|---|
| 2 | 1.79 | 53.5% | 83.4% |
| 3 | 3.38 | 65.7% | 85.1% |
| 4 | 4.88 | 71.8% | 86.5% |
| 5 | 6.32 | 75.6% | 87.5% |
| 6 | 7.72 | 78.2% | 88.4% |

So a rule of thumb: **plan hubs for a mean crowd a little above the cast size**, about 4.9 for four-person scenes. The number of hubs follows, `H* ≈ Λ / λ*`. With 24 roleplayers that is `24 / 4.88 ≈ 4.9`, so five hubs, as the table showed. With 48 it is ten. With 6 it is about one.

And look at the last column. Even at the best `λ*`, about one roleplayer in eight sits in a hub that isn't live. Maximizing stages always leaves some people alone.

### The hour changes the answer

`Λ` is not a constant. It rises through the evening and collapses after midnight. Take the same city at 2 a.m. with `Λ = 6`:

| Hubs `H` | `λ` | Live hubs `V` | Roleplayers in a scene `S` |
|---|---|---|---|
| 1 | 6.0 | 0.85 | 93.8% |
| 2 | 3.0 | 0.71 | 57.7% |
| 3 | 2.0 | 0.43 | 32.3% |

Five hubs at 2 a.m. give each hub a mean crowd of 1.2, and live hubs drop to 0.17. The same map that is perfect at 9 p.m. is dead at 2 a.m. The fix is not a different map. It is a convention that tells people which hub to use when the city is quiet. Communities invent one on their own. Your bible can supply it: a tavern that is "the one that never closes", a watch-fire where night-shift characters gather.

### A visual you can move

Open the interactive. The left panel, "The map", shows the capital with `H` hub markers and a caption listing them. It looks better with every hub you add: more places, more variety. The right panel, "Tonight", shows each hub as a room with dots for the roleplayers who drifted there on one simulated night, live rooms lit and dead rooms grey, with `V` and `S` above. Slide `H` from 1 to 12 with `Λ = 24`. The map keeps improving. Tonight's rooms light up to about five, then go dark one by one. Now move the clock to 2 a.m. and watch almost every room go grey unless you drop to one hub.

### Cross-game recognition

**Final Fantasy XIV (A Realm Reborn onward, 2013 to the present).** No official roleplay worlds. The community concentrated itself on one or two worlds per data center, then on one city and a few venues within it. In the model, the community pushed `H` down at every level (world, city, room) to keep `λ` above `λ*`. The game's congestion system pushes the other way. By blocking new characters on a full world, it spreads new roleplayers across other worlds and lowers `Λ` per world. Travel between worlds on the same data center lets players visit Balmung for an evening without living there, which raises the hub's `Λ` at the hours that matter without adding permanent residents.

**World of Warcraft (2004 to the present).** Blizzard did the concentrating for its players. At launch, players could choose Normal, PvP or RP realms, and an RP-PvP type followed in patch 1.8. RP realms run the normal rules plus roleplay behavior rules and a stricter naming policy. Designating a few RP realms per region sets `H` at the realm level on purpose, so that `Λ` per realm is large. Moon Guard, a US RP realm, was one of the most populated realms in the game by census-site estimates around 2010. The cost shows up at the hub level. Goldshire, a village in the human starting zone whose inn draws crowds on Moon Guard, became notorious for disruptive and adult public play, to the point that the wiki's page on the realm warns that Goldshire does not represent its roleplay community. That is MMO301 week 11's `(1 − f)^n` at work: the bigger and more public the hub, the more certain it is that someone breaks the scene.

**Guild Wars 2 (megaserver system, completed April 2014).** Guild Wars 2 has no roleplay worlds. Players tagged some home worlds informally as roleplay worlds, and the official wiki declines to list them because they are unofficial and unverifiable. Since 2014, open-world maps are shared copies across a whole region, and the game places each player in a copy using heuristics that include party, guild, language and home world. For roleplayers, the placement rule is the hub rule. A roleplay guild that plays together is placed together, so the guild supplies `Λ` for its copy of the map. The engine chooses `H` (how many copies of a map exist), and communities work around it by joining a guildmate's copy. [MMO302 week 2](../../MMO302-mmo-server-architecture/lectures/w02-shards-realms-zones-instances-layers.md) covers how megaserver copies work.

**Outside games: the third place.** The sociologist Ray Oldenburg called informal public gathering places, the pub or café between home and work, **third places**, and stressed that they depend on regulars you can count on finding. Steinkuehler and Williams (2006) argued that MMOs can function as third places. A café with too few regulars tonight is a tavern with `λ` below `k`.

Four cases, one rule. A scene needs `k` people in one place at one time. Whoever sets `H` (the community, the studio, the engine or the neighborhood) decides whether the crowd per place clears `k`.

### Eyes-open design judgment

- **Name few hubs, and make them good.** A capital needs a small number of places designed as stages: seats, corners for private talk, something to look at, sit and drink animations. Scale the count with the expected `Λ / λ*`, not with how big the city looks.
- **Write the fallback into the fiction.** Give the quiet hours a canonical gathering place, such as the tavern that never closes, so the community's convention has an in-world reason.
- **Concentration has a price.** A famous public hub draws spectators and trolls as well as roleplayers, and each extra person is one more chance that a scene breaks (MMO301 week 11). Offer semi-private stages: player housing, instanced rooms, a flag that roleplayers can set, and a way to report people who break a roleplay realm's rules.
- **Don't fight the pull without a reason.** Final Fantasy XIV's congestion shows how strongly a community will concentrate. If you need to spread people for server capacity, give them a designated second home. Spreading them evenly by force breaks every scene at once.
- **`S` and `V` disagree, so pick deliberately.** At `Λ = 8` and `k = 4`, two hubs give more live scenes (1.13 against 0.96) but drop the share of roleplayers in a scene from 98.6% to 76.2%. A newer or smaller community needs `S` more, because people who walk into empty rooms stop coming. A large one can afford to optimize `V`.

### Check yourself (worked example)

1. A plaza needs `k = 3` for a scene. At 8 p.m., 10 roleplayers are in the city across 2 hubs. What is the chance a hub is live, and what share of roleplayers are in a scene?
2. A festival scene needs `k = 10`. With `Λ = 30`, is it better to run the festival in 2 districts or 3? Use `V`.

<details>
<summary>Answers</summary>

1. `λ = 5`. Fewer than three: `e^(−5) × (1 + 5 + 12.5) = 0.00674 × 18.5 = 0.125`, so a hub is live with 87.5%. For `S`, fewer than two others: `e^(−5) × (1 + 5) = 0.040`, so `S = 96.0%`.
2. Two districts, `λ = 15`: `P_10 = 93.0%`, `V = 1.86`. Three, `λ = 10`: `P_10 = 54.2%`, `V = 1.63`. Two is better, and far better for the players, since `S` is 96.3% against 66.7%. Large scenes need large crowds, so big events belong in few places.

</details>

## 3. Community lore and the canon ladder

Roleplay produces stories every night. Most of them should stay where they were made. A few rise, and your bible needs a rule for how.

### Where community lore sits

Week 11 gave you canon tiers. Community lore needs rungs below and beside them.

| Rung | Example | Who can change it | How official content treats it |
|---|---|---|---|
| World canon | The Drowning began in 912 | The lore team, in patches | Everything depends on it |
| Personal canon | My character's village and family | The player | Official content never contradicts it by name, because it never names it |
| Server or community canon | A guild's war with another guild on one realm | The community | Official content may nod to it in general terms |
| Fanon | "Everyone knows the Tidewardens keep a secret archive" | Nobody, it spreads | Official content may adopt it, contradict it, or leave it open |
| Community reference | A wiki page summarizing the Drowning | Wiki editors | Correct your own sources, not the wiki |

When a fan wiki summarizes your history wrongly, don't argue with the wiki. Find which of your own sources is ambiguous and fix it (week 11). Wiki editors cite what you publish.

### Acknowledging player history

CCP's Titanomachy monument records that a real battle happened without inventing lore about it. In 2025, Bethesda asked a group of UESP editors to design a character for The Elder Scrolls VI, and the editors chose to create a memorial for a deceased member of their forum. Both put community history into official content at a clearly marked level.

A safe pattern for your bible has three rules.

1. **Commemorate events, don't canonize interpretations.** A monument says "a great battle was fought here." It doesn't say who was right.
2. **Credit the community, not individual characters, in world-canon text,** unless the players concerned agree. A named player character in canon becomes a fact every later writer must respect, tied to a real person who may quit or change their mind.
3. **Keep it at a low tier.** Put acknowledgements at the flavor tier (week 11), so a later story can reinterpret them.

### When fanon meets a patch

Fanon grows fastest where canon is silent and interesting, which is where your hooks live (week 10). When a patch must answer a question the community already answered differently, you have three choices, in order of preference.

- **Leave it open** if the hook isn't due yet. Silence is free.
- **Adopt it** if it fits. Log it like any new fact, with dependencies and a tier.
- **Contradict it cleanly** if the plan needs something else, once and in main-path content. A vague contradiction produces years of argument.

## 4. Writing a bible players can live in

Roleplayers read your bible, or the wiki's version of it, more closely than anyone else. They need three things your plot writers don't: room, rules and places.

### Room: open slots

An **open slot** is a part of the setting that is defined in outline but deliberately left unpopulated, so players can fill it without contradicting canon. Good open slots have a clear shape and no named members.

- **Orders with open membership.** "The Tidewardens take anyone who swears the dike oath" gives every player a way in. "The Tidewardens are seven named masters" gives none.
- **Minor houses and villages by the dozen.** "There are over forty landed houses in the river counties" invites players to invent one. Naming all forty closes the space.
- **Vague periods and distant places.** A frontier described in outline, or the reserved gaps in your timeline from week 4, let player backstories happen offstage.

Watch for the **"last of" trap**. Lore that says a people or an order was wiped out except for one survivor creates the most attractive character concept in the setting and forbids it. Players will play the last survivor anyway, and each of them contradicts the others. If you need a near-extinction, leave a scattered remnant of unknown size.

### Rules: naming and conduct

Blizzard publishes a separate roleplay naming policy for its RP realms, on top of the general one. Build yours from the week 5 naming languages. Publish a short naming guide per culture with a few syllables, example names and a list of reserved names (canon characters and gods). If you run roleplay realms or flags, add the conduct rules: what counts as in character in public channels, and how to mark out-of-character talk.

### Places: hubs as lore

Section 2 said how many hubs. The bible says which, and gives each one a reason to exist in the fiction:

- a name, a location and an owner (an innkeeper, a temple, a guild);
- what kinds of scene it suits (trade, intrigue, worship, a quiet drink);
- when it is busy in the fiction (market days, the night watch), which gives the community a reason for its conventions;
- a small set of standing tensions from your ledger (week 1), such as a smuggler who drinks there or a feud between two guild tables, that give walk-up scenes something to start from.

Such an entry tells level designers what to build and hands roleplayers a scene premise on their first visit.

## In-class activity (25 minutes)

In groups of three, you write the roleplay plan for Dikeholm, *Thornmere*'s capital.

1. **(5 min) Size it.** The community team expects `Λ = 30` roleplayers at 9 p.m. and `Λ = 8` at 2 a.m. Tavern scenes need `k = 4`. Using the `λ*` table, how many hubs does prime time support? Compute `V` and `S` at 2 a.m. for one and two hubs.
2. **(10 min) Name the hubs.** Write a four-line entry for each prime-time hub: name, owner, scene types, busy hours. Choose one of them as the "never closes" fallback and give it a reason in the fiction.
3. **(5 min) Open slots.** Write three open slots for player characters: one order, one set of houses or villages, one place or period. Check none of them is a "last of" trap.
4. **(5 min) Festival.** The spring festival draws 30 roleplayers for scenes needing 10. Decide between one, two and three districts using `V` and `S`.

Expected output: prime time `30 / 4.88 ≈ 6` hubs (`V = 4.41`, the peak; five gives 4.24 and seven 4.34). At 2 a.m., one hub gives `V = 0.96`, `S = 98.6%`; two give `V = 1.13`, `S = 76.2%`. Pick one hub for the night and defend it with `S`. Festival: one district `V = 1.00`, `S = 100%`; two `V = 1.86`, `S = 96.3%`; three `V = 1.63`, `S = 66.7%`. Two districts is the best choice.

## Common misconceptions

- **"More roleplay spaces mean more roleplay."** Only while each space keeps a mean crowd above about `k + 1`. Past the peak, every new hub lowers the number of live scenes, and every hub at all lowers the chance a newcomer finds one.
- **"The average crowd tells you whether a hub works."** A hub with an average of four works only 57% of the time for four-person scenes. Scenes need the crowd tonight, and the Poisson spread around the average decides that.
- **"Roleplayers crowd one server because nobody told them where else to go."** Concentration is the rational response to the threshold. Final Fantasy XIV's congestion system blocks new characters, and the community still gathers there.
- **"Player-made lore is a threat to canon."** It sits on its own rungs. It threatens canon only when official content names player characters or contradicts fanon vaguely. Open slots and clean contradictions keep both working.

## Check yourself

1. At 11 p.m., 15 roleplayers are in your capital and scenes need `k = 3`. Using the `λ*` table, how many hubs give the most live scenes? What are `V` and `S` there?
2. Your capital has eight taverns and your community team measures that most of them are empty most nights. Name two fixes, one on the map and one in the bible.
3. A player guild wins a server-first victory over a raid boss, and the community asks for a statue. Write the one-sentence inscription under the rules of section 3, and state its tier.
4. The bible says, "The Order of the Lantern was destroyed; only Brother Aymon escaped." What will roleplayers do, and how would you rewrite the line?

<details>
<summary>Answers</summary>

1. `λ* = 3.38`, so `H ≈ 15 / 3.38 ≈ 4.4`. Check four and five: `H = 4` gives `λ = 3.75`, `P_3 = 72.3%`, `V = 2.89`. `H = 5` gives `λ = 3`, `P_3 = 57.7%`, `V = 2.88`. Four hubs, just ahead of five, with `S = P_2(3.75) = 1 − e^(−3.75) × 4.75 = 88.8%`.
2. Map: close or down-grade some taverns to set dressing, and make the remaining two or three better stages. Bible: name one as the "never closes" hub and give the others busy hours in the fiction (market days, shift changes), so the crowd moves together.
3. Something like "Here the champions of this realm first brought down the Drowned King," with no names in world canon (the achievement list credits players). Flavor tier, since it is an in-world monument and a later story may reinterpret it.
4. Many will play surviving members of the Order, contradicting canon and each other. Rewrite it as "The Order was broken at the Lantern Hall; its scattered brothers still keep the oath in secret, and no one knows how many survive."

</details>

## Lab / assignment hook

[Lab 13, roleplay hubs and the community chapter](../labs/lab13.md). You implement the hub model, run it over a full day of hourly roleplayer counts for Dikeholm, and choose a hub plan with a night-time fallback. Then you write the community chapter of your world bible: named hubs, open slots, a naming guide and a player-history policy. It counts toward the exercises (40%) and becomes a chapter of the final world bible (60%).

## Sources

- Final Fantasy XIV Online Wiki (consolegameswiki), "World" (the "Server" page redirects there; current, accessed September 2026). World list by data center, including Balmung and Mateus on Crystal (Balmung active from 16 August 2013; the Crystal data center formed on 23 April 2019), with no roleplay category; "Congested" worlds block character creation and transfers. https://ffxiv.consolegameswiki.com/wiki/World
- Square Enix official Final Fantasy XIV forums, player thread "Resolving the Balmung Population Issue at Minimal Cost to the Benefit of All Players" (28 June 2017). Balmung's queues and congestion; the proposal for an official roleplay world; roleplayers' need for a central place to find each other. Player posts, not a staff statement. https://forum.square-enix.com/ffxiv/threads/332802
- Hydaelyn Role-Players forum, "Most active RP server?" (April 2022). Balmung and Mateus as the de facto roleplay worlds on Crystal; open-world roleplay concentrated in Ul'dah around the Quicksand; cross-world travel to reach events. https://ffxiv-roleplayers.com/topic/25205-most-active-rp-server/
- Warcraft Wiki, "Roleplaying" (current). IC and OOC, double-parenthesis convention, RP realms as PvE realms with added social rules and stricter naming enforcement; Goldshire's reputation. https://warcraft.wiki.gg/wiki/Roleplaying
- Warcraft Wiki, "RP-PvP" (current). Launch realm choices Normal, PvP and RP; RP-PvP introduced in patch 1.8. https://warcraft.wiki.gg/wiki/RP-PvP
- Warcraft Wiki, "Moon Guard US" (current). An RP realm, one of the most populated (2010 census estimates); the note that Goldshire does not represent the realm's roleplay community. https://warcraft.wiki.gg/wiki/Moon_Guard_US
- Warcraft Wiki, "Naming policy" (current). Links to Blizzard's separate Role Play Naming Policy. https://warcraft.wiki.gg/wiki/Naming_policy
- Guild Wars 2 Wiki, "Megaserver" (accessed September 2026). Region-wide map copies; placement heuristics including party, guild, language and home world; roll-out completed 21 April 2014. https://wiki.guildwars2.com/wiki/Megaserver
- Guild Wars 2 Wiki, "World" (accessed September 2026). Players' unofficial world tags such as roleplaying, which the wiki declines to list. https://wiki.guildwars2.com/wiki/World
- Wikipedia, "Wowpedia" (accessed September 2026). WoWWiki launched 24 November 2004, the day after World of Warcraft's release; now Warcraft Wiki.
- Wikipedia, "Unofficial Elder Scrolls Pages" (accessed September 2026). Founded 1995, a wiki since 2005; in 2025 Bethesda asked UESP editors to design a character for The Elder Scrolls VI, and they chose a memorial character.
- Wikipedia, "Bloodbath of B-R5RB" (accessed September 2026). 27 to 28 January 2014; 75 titans lost; CCP's permanent Titanomachy monument.
- Steinkuehler, C. A. & Williams, D. (2006). "Where Everybody Knows Your (Screen) Name: Online Games as 'Third Places'". *Journal of Computer-Mediated Communication*, 11(4), 885-909. https://doi.org/10.1111/j.1083-6101.2006.00300.x
- Oldenburg, R. (1989). *The Great Good Place*. Paragon House. Third places and their regulars, as summarized by Steinkuehler and Williams.
- Wolf, M. J. P. (2012). *Building Imaginary Worlds: The Theory and History of Subcreation*. Routledge.
- The Poisson limit of the binomial and the "others at my hub" property are standard probability; the `λ*` table is computed from the model in section 2.

## Interactive spec: examples/w13-rp-hubs.html

**The one insight the visual must make obvious:** adding roleplay hubs makes the map look richer, but live scenes rise only until the mean crowd per hub falls to about the cast size, then fall, and the chance a newcomer finds a scene falls from the very first extra hub. The right number of hubs depends on the hour.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (left on top).

- **Left, "The map".** A simple generic city outline (a circle or rounded rectangle with a river line) with `H` hub markers placed on a fixed ring. Each marker is a small tavern glyph drawn with basic shapes. Below: "Hubs on the map: H" in large type, and a list of hub labels ("Hub 1", "Hub 2", ...). This panel never shows `V` or `S`.
- **Right, "Tonight".** `H` rooms in a grid (up to 12). Each room shows dots for the roleplayers who ended up there on one simulated night. A room with at least `k` dots is drawn lit (accent fill, label "live"); otherwise grey (label "waiting"). Above the grid, two large counters: "Live hubs V" (the model's expected value, 2 decimals) and "Roleplayers in a scene S" (percent, 1 decimal). Beside each, in small text, the simulated night's count ("tonight: 4 live, 21 of 24 in a scene") so students see the random spread around the expectation.
- **Below the right panel, a small chart.** x-axis `H` from 1 to 12, two lines: `V(H)` on the left axis (0 to max) and `S(H)` on the right axis (0% to 100%). A vertical marker at the current `H`, and a dot at the peak of `V` labelled "most live hubs".

**Controls.**

1. Hubs `H`: slider 1 to 12, step 1, default 5.
2. Roleplayers in the city `Λ`: slider 1 to 60, step 1, default 24.
3. Minimum cast `k`: slider 2 to 10, step 1, default 4.
4. Clock: segmented control with "9 p.m." (sets `Λ` to 24), "2 a.m." (sets `Λ` to 6) and "Custom" (uses the slider).
5. "Another night" button: redraws the simulated night with the next seed. Seeded generator (mulberry32, first seed 13), so the first screen is reproducible.
6. Preset buttons: "Lecture table" (`Λ = 24, k = 4, H = 5`), "Night" (`Λ = 6, k = 4, H = 1`), "Festival" (`Λ = 30, k = 10, H = 2`).

All controls are labelled native inputs, keyboard operable. An `aria-live` region states, for example, "5 hubs. Expected live hubs 3.53. Roleplayers in a scene 85.7%. Best for this crowd: 5 hubs."

**Simulation.** For the right-panel dots only: each of `Λ` roleplayers picks a hub uniformly at random with the seeded generator. Counters always show the exact model values; the simulated counts appear in small text.

**Formulas.**

```
λ = Λ / H
P_k(λ) = 1 − Σ_{j=0}^{k−1} e^(−λ) λ^j / j!      (P_0 = 1)
V = H × P_k(λ)
S = P_{k−1}(λ)
best H = the H in 1..60 with the largest V (ties to the smaller H)
```

**Test values (must match).**

| `Λ` | `k` | `H` | `V` | `S` |
|---|---|---|---|---|
| 24 | 4 | 1 | 1.00 | 100.0% |
| 24 | 4 | 5 | 3.53 | 85.7% |
| 24 | 4 | 6 | 3.40 | 76.2% |
| 24 | 4 | 12 | 1.71 | 32.3% |
| 6 | 4 | 1 | 0.85 | 93.8% |
| 6 | 4 | 2 | 0.71 | 57.7% |
| 30 | 10 | 2 | 1.86 | 96.3% |
| 30 | 10 | 3 | 1.63 | 66.7% |
| 8 | 4 | 2 | 1.13 | 76.2% |

Best `H` for (24, 4) is 5; for (6, 4) is 1; for (30, 4) is 6; for (30, 10) is 2.

**First screen.** Lecture table preset with `H = 5`, and one caption line: "More taverns on the map. Fewer scenes tonight?" The first thing a student does, dragging `H` up, lights no new rooms after 5 while the map keeps gaining markers.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css` inline, light and dark themes, `prefers-reduced-motion` respected (no dot animation when set). Live and waiting rooms differ by label and border style, not only colour. No game art, logos or real city maps.
