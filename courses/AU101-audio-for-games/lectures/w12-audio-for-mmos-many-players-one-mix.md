# AU101 · Week 12 — Audio for MMOs: Many Players, One Mix

**Why this matters:** In a single-player game, every sound that plays was put there for you. In an MMO, most of the sounds around you belong to other people: their spells, their mounts, their emotes, their legendary weapons. Forty players in a raid can ask for twice as many voices as the engine has. If the mix treats all of them equally, your own spell is the one that goes missing, and the game feels broken in exactly the moment it should feel best.

**You will be able to:**
- Estimate the average number of simultaneous voices a group of players demands, using Little's law, and compare it with a voice budget.
- Design a relevance-tier budget (you, the boss, your party, everyone else) and compute what share of each tier's sounds survive.
- Compute how loud a crowd bed should get as player count grows, and decide when to replace individual sounds with one.
- Critique an MMO's audio options menu in terms of these tiers.

**Before class:** Collins, *Game Sound* (2008), chapters 1-3 (the course reading), for the history of voice limits you are about to meet again at scale. Log into any MMO you have access to (a free trial is fine) and stand in its busiest city for five minutes with your eyes closed. Write down every sound you can name and whose it is.

**Prerequisites from earlier courses:** [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (averages of random quantities; this week's demand numbers are expected values). [CS101 week 14, polish pass](../../CS101-programming-for-games-i/lectures/w14-polish-pass-sound-particles-screen-shake.md) (`max_polyphony`). From this course, [week 10](w10-mixing-ducking-and-priority.md) (the power sum, priority, voice limits and "discard oldest or newest"; this week builds on all four), [week 11](w11-ui-sound-design.md) (sounds for your actions versus sounds for the world), and [week 7](w07-spatial-audio-and-attenuation.md) (attenuation curves, and why "inaudible" is not "not playing"). Looking ahead, [MMO302 week 3, area of interest](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md) explains how the server decides which players your client even knows about.

**Interactive:** [examples/w12-raid-voice-budget.html](../examples/w12-raid-voice-budget.html). Keep it open during section 2.

---

## 1. What changes when the world is shared

Three things make MMO audio different from the games you have mixed so far.

**Most sounds are not yours.** In a 40-player raid, your character makes perhaps 2 or 3% of the combat sounds. The rest come from 39 other players and the boss. The player still expects their own actions to feel as crisp as in a single-player game.

**You cannot author the scene.** In a level of a linear game, the sound designer knows how many enemies appear and when. In an MMO, the number of players at a world boss, in a capital city or in a battleground is decided by the players. The mix has to work for 1 player and for 200.

**Some sounds are identity.** Players buy and earn cosmetic sounds: a legendary weapon with its own hum, a mount with a signature call, an instrument they can play for others. Those sounds matter socially to their owner and are noise to everyone else.

The client can only play what it knows about. The server already filters the world down to players in your **area of interest** (the region around you whose updates it sends, MMO302 week 3). Audio is a second, tighter filter on top. Of everything the client knows is happening, what should the player actually hear?

## 2. Worked example: forty players, thirty-two voices

### The hook

In World of Warcraft, a raid group can hold up to 40 characters. Classic-era raids such as Molten Core were built for 40, and today's Mythic difficulty is fixed at 20. Most abilities trigger a **global cooldown** (GCD), a short lockout before the next ability can be used. Its base length for most abilities is 1.5 seconds, and haste can shorten it to 0.75 seconds. So a raid is a crowd in which every player presses a button that makes noise roughly every second and a half, for minutes at a time.

Suppose your engine can afford 32 voices for combat sounds. (Week 14 covers why a real budget is some number like this, and how to measure yours.) How many voices does the raid ask for? And when it asks for more than 32, whose sounds disappear?

### The model

**Little's law** comes from queueing theory and says that, on average,

```
L = λ · W
```

- `L` is the average number of items in the system (here, voices playing at once).
- `λ` (lambda) is the average arrival rate (new sounds per second).
- `W` is the average time each item stays (the sound's duration in seconds).

For a group of players:

```
λ = N · a / g
L = N · a · W / g
```

- `N` is the number of players.
- `a` is the number of sounds each action starts (a cast sound and an impact, for example).
- `g` is the average time between actions in seconds (the GCD if players act on every one).
- `W` is the average sound duration in seconds.

Little's law holds for averages whatever the pattern of arrivals, as long as the system is stable. That makes it a quick, honest first estimate. It says nothing about peaks. The moment a raid pulls the boss, everyone fires their opening abilities at once. The lab simulates those bursts.

### Numbers you can check

Take `a = 2` sounds per action, `g = 1.5` s and `W = 1.2` s. These are illustrative values, not measurements from any game.

```python
def expected_voices(players, sounds_per_action, action_interval, duration):
    return players * sounds_per_action / action_interval * duration

for n in (1, 5, 10, 20, 40, 100):
    print(f"{n:3d} players -> {expected_voices(n, 2, 1.5, 1.2):5.1f} voices")
```

```
  1 players ->   1.6 voices
  5 players ->   8.0 voices
 10 players ->  16.0 voices
 20 players ->  32.0 voices
 40 players ->  64.0 voices
100 players -> 160.0 voices
```

Each player costs 1.6 voices on average. At 20 players the raid alone fills the 32-voice budget. At 40 it asks for twice the budget, before the boss makes a sound.

Now split the raid into **relevance tiers**, most important first: you, the boss, your party (4 other players), and everyone else (35 players). The boss wants 4 voices of its own (a looping roar, footsteps, two spell layers).

| Tier | Players | Average demand (voices) |
|---|---|---|
| You | 1 | 1.6 |
| Boss | — | 4.0 |
| Your party | 4 | 6.4 |
| Others | 35 | 56.0 |
| **Total** | 40 | **68.0** |

**Policy 1, flat.** Every sound is equal and the engine applies week 10's "discard newest" rule: the oldest sounds keep their voices and new ones are refused. The boss's loops started at the pull, so they are always oldest and always play. The remaining 28 voices are shared among 64 voices' worth of player sounds, so each player sound plays about 28 / 64 = 44% of the time. Your own spell is refused more than half the time. The lab's simulation of this exact raid measures 41% for your sounds.

**Policy 2, tiered reservations.** Each tier gets reserved slots. Any reserved slot a tier does not use is handed down to the next tier.

| Tier | Reserved | Demand | Kept | Share kept |
|---|---|---|---|---|
| You | 4 | 1.6 | 1.6 | 100% |
| Boss | 6 | 4.0 | 4.0 | 100% |
| Your party | 8 | 6.4 | 6.4 | 100% |
| Others | 14 | 56.0 | 14 + 6 unused = 20 | 36% |
| **Total** | 32 | 68.0 | 32 | |

The unused reservation is `(4 − 1.6) + (6 − 4) + (8 − 6.4) = 6` voices, and it flows to the others. The budget is the same 32 voices. The raid sounds almost as busy. But now every one of your sounds plays, and the missing ones belong to strangers at the far end of the room.

Why reserve 4 for you when you only need 1.6 on average? Because averages lie about peaks. With `W = 1.2` s shorter than `g = 1.5` s, one player's action is over before the next starts, so a single player never needs more than 2 voices from combat alone. The reservation of 4 covers that plus a proc or a pet. Reserve for your tier's peak and let the unused part flow down.

### A visual you can move

Open the interactive. The left view is a top-down room with 40 dots: you in the centre, your party in one colour, everyone else in grey, the boss as a large shape. Each dot flashes when it starts a sound and stays lit while that sound holds a voice. A dot that wanted a voice and was refused shows a hollow ring. The right view is a strip chart of demand per tier against the budget line.

Start in Flat mode. Watch your own dot. About half of your flashes are rings. Switch to Tiered and your dot never rings again, while the rings move to the edge of the room. Now drag the "others' sound length" slider from 1.2 s down to 0.6 s. The grey demand halves, and the share of others' sounds kept roughly doubles, without adding a single voice.

### Cross-game recognition

**Guild Wars 2 (ArenaNet, current live game).** The sound options include separate settings for "My Unique Item Sounds" and "Other Players' Unique Item Sounds", each with All, Limited, Mute Projectiles Only and Off. There is a separate volume for players' musical instruments and a switch to disable player chatter. This is the tier model handed to the player: the "others" tier gets its own controls, and the "you" tier keeps its identity sounds.

**Final Fantasy XIV (Square Enix, current live game).** The official UI guide describes a Battle Effects setting with separate choices for your own character, party members and other players ("Show All", "Show Limited" or "Show None", plus an "Enemy PC" option). That setting is for visual effects, not sound, but its three tiers are exactly ours. The game's designers solved the visual version of the same crowd problem with the same relevance order. When you design audio options for an MMO, the players will already understand this split.

**Overwatch (Blizzard, 2016).** The sound team's GDC talk describes its "Play by Sound" goal for matches of 12 players. With 12 players and `a · W / g` around 1.6 per player, a match asks for about 19 voices. That fits a typical budget with room to spare. So a 12-player shooter can afford to hear everyone and spend its effort on making each sound informative. A 40-player raid cannot. Same model, different `N`, and a different design problem falls out of it.

### Eyes-open design judgment

- **Duration is a cheaper lever than voice count.** `L` is proportional to `W`. Giving other players a shorter version of each ability sound (the cast without the long tail) cuts their demand in proportion. Halving the tail can be worth more than doubling the budget, and it costs no CPU.
- **Tiers encode a social promise.** Putting your party above other players tells the player "your team matters more than the crowd". That is usually right. In a world-versus-world battle, though, enemy players may matter more than your own party. Tiers should come from the game's goals, not from habit.
- **Reserve for the peak, share the rest.** Hard reservations with spill-down protect the tiers you care about and waste nothing. Pure priority numbers can do the same, but they are harder to reason about when 60 requests compete.
- **The boss is not a player.** Boss tells are gameplay information. They belong near the top tier, with a duck on the others tier while they play (week 10).
- **Test at the worst real case.** Take your busiest scene from live data: the largest world boss, the capital on patch day. A mix tuned for a 20-player raid can collapse in a 150-player event.

### Check yourself (worked example)

1. With the same values, how many players does it take to fill a 48-voice budget from player sounds alone?
2. In the tiered table, the others' sounds are shortened to 0.6 s. What is their demand now, and what share survives?
3. A designer proposes giving each of the 40 players an equal reservation of 0.8 voices. What is wrong with that as a policy?

<details>
<summary>Answers</summary>

1. `48 / 1.6 = 30` players.
2. `35 × 2 / 1.5 × 0.6 = 28` voices. The others still get 14 reserved plus 6 unused, 20 voices, so `20 / 28 ≈ 71%` survive.
3. It is the flat policy in disguise. It ignores relevance, so your sounds get the same 0.8 as a stranger's (half your average demand), and it wastes slots when players are idle, because nothing spills down.

</details>

## 3. The crowd bed: when to stop playing individuals

The tiered budget handles a raid. It does not handle a capital city with 200 players standing around, mounting, emoting and crafting. Even at 36%, the others' tier would be a random scatter of fragments.

Past some density, stop playing individual sounds for the crowd and play a **crowd bed** instead: a looping ambience of many overlapping sounds (voices, footsteps, armour, mounts) whose level follows the number of active players nearby.

How loud should the bed get? Week 10 gave you the rule. `N` equal, uncorrelated sources sum to `10 · log10(N)` dB above one of them:

```python
import math

for n in (1, 10, 35, 100, 300):
    print(f"{n:3d} active players -> crowd bed {10 * math.log10(n):+5.1f} dB")
```

```
  1 active players -> crowd bed  +0.0 dB
 10 active players -> crowd bed +10.0 dB
 35 active players -> crowd bed +15.4 dB
100 active players -> crowd bed +20.0 dB
300 active players -> crowd bed +24.8 dB
```

Going from 100 to 300 players adds under 5 dB. A bed whose level grows linearly with player count would be far too loud at 300 and inaudible at 10. Many games also blend between two or three crowd loops by density (sparse, busy, packed) rather than only turning one up, because a packed square has a different *texture*, not just a different level.

A practical hybrid:

1. The **nearest few** other players (for example, the 6 closest within 10 m) keep individual sounds, so someone walking right past you still sounds like a person.
2. **Everyone else** feeds a single number, the count of active players within the bed radius, which drives the bed's level and blend.
3. **Identity sounds** (legendary weapons, instruments) are subject to the player's "others" setting, as in Guild Wars 2.

## 4. Your sounds versus their sounds

Tiering decides *whether* a sound plays. You can also change *what* plays depending on whose it is. This is level of detail (LOD) for audio, the same idea graphics uses for distant models.

| Aspect | Your version | Party version | Others' version |
|---|---|---|---|
| Layers | Full: cast, whoosh, impact, tail | Cast and impact | Impact only |
| Length | 1.2 s | 0.9 s | 0.4 s |
| Level | Reference | −3 dB | −8 dB and distance attenuated |
| Spatial | Centred or wide stereo | Positioned (week 7) | Positioned, low-pass beyond 25 m |
| Priority | Top tier | Second | Lowest, nearest first |

These numbers are a starting point for your own design, not measurements from a shipped game. Two principles sit underneath them. First, your own sounds carry feedback (week 11's "confirm"), so they must be complete and immediate. Second, other players' sounds carry information about the world ("a healer is casting behind me"), which needs only the most identifiable part of the sound. The impact alone usually tells you what happened.

Notice how the table combines with Little's law. The others' version at 0.4 s instead of 1.2 s cuts that tier's demand to a third before any priority rule runs.

### Voice chat and callouts

Many MMO groups run voice chat during raids, either built into the game or through a separate app. When the voice goes through the game, it is a sidechain key. Duck the others' tier and the music under it, as week 10 did for dialogue. When it goes through a separate app, the game cannot see it, so leave headroom. A raid mix already pushed to the ceiling leaves no room for the raid leader's voice.

## 5. Designing the options menu

The tier model gives you a principled options menu. Every slider should map onto one tier or one category, and the player should be able to predict what each does.

- **Master, Music, Ambience, Dialogue, UI, Effects.** The usual bus faders from week 6.
- **Effects from other players.** A volume fader for the others' tier, plus a density option (All, Nearby only, Off) that changes the reservation and the crowd-bed threshold.
- **Party effects.** Sometimes its own fader, sometimes merged with yours.
- **Identity sounds from others.** Unique items, instruments, mount calls, following Guild Wars 2's model.
- **Chatter.** Voiced barks from your own and others' characters.

Test the menu with the question "a player says the raid is too noisy and they can't hear the boss". If there is no single setting they can change that fixes it without muting their own spells, the menu is missing a tier.

## In-class activity (25 minutes)

In groups of three, design the audio budget for a world boss event in a fantasy MMO. Expect between 20 and 120 players. Your engine budget is 48 combat voices.

1. Choose values for `a`, `g` and `W` for your game's combat and write them down with a sentence of justification each.
2. Compute the demand at 20, 60 and 120 players.
3. Design tiers with reservations. Include the boss. Compute the share kept per tier at 60 and 120 players.
4. Set the crowd-bed threshold: above how many "others" do you switch from individual sounds to the bed? Give the bed level at your threshold and at 120 players relative to a single player's sound.
5. Write the "others" row of the LOD table for your game.

Expected output: one page with the demand calculation, the tier table at two player counts, the crowd-bed rule and the LOD row. Swap with another group and find the player count at which their design first refuses one of the player's own sounds.

## Common misconceptions

- **"More voices fixes it."** Doubling the budget from 32 to 64 still fails at 80 players, and costs CPU on every platform. Relevance tiers and shorter sounds for others scale; raw voice count does not.
- **"Distance is enough."** Nearest-first protects you (you are at distance 0) but can drop the boss, which is often 20 m or more away and is the most important thing in the room. Distance is a good tie-breaker within a tier, not a replacement for tiers.
- **"The average demand is the budget I need."** Little's law gives averages. Pulls, bursts and synchronised cooldowns create peaks well above the average. Reserve for your important tiers' peaks.
- **"A crowd of 100 should sound 100 times louder than one person."** It sounds about 20 dB louder, following the power sum. Scale beds in decibels, not linearly.

## Check yourself

1. A battleground has 40 players, 20 per side. Each player triggers 3 sounds per action, every 1.2 s on average, lasting 0.8 s. What is the average demand? How much of a 64-voice budget is left for everything else?
2. In a capital city, 180 players are within 30 m. Your rule keeps the nearest 6 as individual sounds and feeds the rest into a crowd bed. How many dB above a single player's sound is the bed?
3. In the tiered worked example, your party grows from 4 other players to 9 (a 10-player group), and the others shrink to 30. With the same reservations, which tier loses sounds first, and what share does it keep?
4. A player complains that their own legendary weapon sound "sometimes doesn't play in raids", while a friend's does. Using this lecture's model, name two likely causes.
5. Your game's world boss fights moved from 40 players to 150 in a new expansion. Which parts of the design in section 2 still hold and which need to change?

<details>
<summary>Answers</summary>

1. `40 × 3 / 1.2 × 0.8 = 80` voices. That exceeds the 64-voice budget on its own, before ambience, UI or music stingers, so tiers or shorter sounds are required.
2. `180 − 6 = 174` players feed the bed: `10 · log10(174) ≈ 22.4` dB.
3. Party demand becomes `9 × 1.6 = 14.4`, above its reservation of 8. Unused slots from you and the boss are `2.4 + 2 = 4.4`, so the party gets `8 + 4.4 = 12.4` of 14.4, about 86%, and nothing spills to the others beyond their 14 (others' demand `30 × 1.6 = 48`, kept 14, about 29%). The party loses sounds first, so raise its reservation (taking from the others) if a 10-player group is a normal case.
4. First, the weapon sound may be tagged as an identity sound with a fixed low priority, instead of taking the tier of whoever is listening, so on its owner's client it loses to older sounds under a first-come rule. Second, the "you" reservation may cover your spells' average but not the peak when the weapon hum, a cast and an impact all start together, and nothing spills down to you because you are the top tier.
5. Little's law and the tier structure still hold. The numbers change. Others' demand grows almost fourfold, so the others' share collapses. You need a crowd bed threshold, a shorter others' LOD, and possibly a larger reservation for the boss's tells.

</details>

## Lab / assignment hook

[Lab 12, the raid voice budget](../labs/lab12.md). You implement Little's law, the crowd-bed gain and two allocators (flat first-come and tiered with spill-down), then use the provided raid simulator to measure how much of each tier survives, find the burst peaks that averages hide, and tune a budget for a world boss event. It reuses your week 10 thinking about priority and feeds the final sound pass.

## Sources

- Warcraft Wiki, "Raid" (current retail World of Warcraft, accessed September 2026). Raid groups hold up to 40 characters; flexible raids for most difficulties; Mythic difficulty is 20 players only. Warcraft Wiki, "Molten Core": a 40-player raid (classic era).
- Warcraft Wiki, "Cooldown", global cooldown section (current retail World of Warcraft, accessed September 2026). Base GCD of 1.5 seconds for most abilities, 1.0 second for some classes; haste can reduce the 1.5-second GCD to a minimum of 0.75 seconds (1.0 before Legion).
- Guild Wars 2 Wiki, "Options", Sound Options section (live game, accessed September 2026). "My Unique Item Sounds" and "Other Players' Unique Item Sounds" with All, Limited, Mute Projectiles Only and Off; Player Instrument Volume; Disable Player Chatter.
- Square Enix, *Final Fantasy XIV* official UI guide, "How do I adjust the graphical effects displayed in battle?" (Lodestone, na.finalfantasyxiv.com/uiguide/faq/faq-other/setting_bteffect.html, checked 29 September 2026). Character Configuration, Control Settings, Character tab: Battle Effects set separately for your own character, party members and other players.
- Lawlor, S. & Neumann, T. (2016). "Overwatch: The Elusive Goal, Play by Sound". GDC 2016, GDC Vault session overview. 12 players with unique weapons and abilities.
- Little, J. D. C. (1961). "A Proof for the Queuing Formula: L = λW". *Operations Research* 9(3), 383-387.
- Collins, K. (2008). *Game Sound*. MIT Press.

## Interactive spec: examples/w12-raid-voice-budget.html

**Purpose.** Show that under a fixed voice budget a flat policy drops the player's own sounds at the same rate as strangers', while relevance tiers with spill-down protect the player and party at almost no cost to how busy the raid sounds. Show that shortening others' sounds is as powerful as adding voices.

**Layout.** Two linked views, side by side on desktop, stacked on phones.

- *Left, "The room":* a top-down circle (radius 40 m to scale). "You" at the centre (distinct colour, larger). Party members (default 4) at seeded random positions 3-15 m away. Others at seeded random positions 3-40 m away, grey. The boss as a larger generic shape at 20 m. A dot flashes filled when it holds a voice and shows a hollow ring when it wanted one and was refused. Draw everything generically; no game art.
- *Right, "Demand vs budget":* a 10-second scrolling stacked-area chart of voices demanded per tier (you, boss, party, others) with a horizontal budget line, and a second thin line for voices actually kept. Under it, a table per tier: average demand (Little's law), simulated average demand over the last 10 s, share kept (last 10 s).

**Controls.**
- Policy: Flat (first come, discard newest) / Tiered (reservations with spill-down in tier order, nearest first within a tier).
- Players `N`: 1-100, default 40.
- Budget: 8-96, default 32.
- Sounds per action `a`: 1-4, default 2. Action interval `g`: 0.75-3.0 s, default 1.5. Sound length `W` (you and party): 0.2-2.0 s, default 1.2. Others' sound length: 0.2-2.0 s, default 1.2.
- Reservations (Tiered only): you 0-8 (4), boss 0-12 (6), party 0-16 (8), others 0-48 (14). Warn when the sum exceeds the budget.
- Button "Pull!": all players act at once at the next tick, to show a burst peak above the average.
- Toggle "Hear it" (off by default): you = a bright two-tone blip (Web Audio oscillators, 1.2 s envelope), party = a softer single tone, others = short filtered noise ticks, boss = a low looping drone. Only voices actually kept are rendered, so the player hears the policy. Master gain 0.2. No audio files.

**Exact rules.** Fixed 20 Hz simulation tick (`dt = 0.05`). Each player has a seeded random phase in `[0, g)`, acts every `g` seconds, and each action starts `a` requests lasting `W` (others use the others' length). Boss holds 4 requests permanently (start time 0). Flat: sort all live requests by start time (stable) and keep the first `budget`. Tiered: pass 1 keeps up to each tier's reservation, nearest first; pass 2 fills remaining slots in tier order (you, boss, party, others), nearest first. Allocation is recomputed every tick.

**Readouts.** Little's-law demand per tier (1 decimal), measured demand (1 decimal), share kept per tier (whole percent), peak demand since last reset.

**Test values (defaults, seed 1).** Little's law: you 1.6, party 6.4, others 56.0, total with boss 68.0. Flat: your share kept about 40-45%. Tiered: you 100%, party 100%, boss 100%, others about 36%. Others' length 0.6 s under Tiered: others' demand 28.0, model share `20 / 28 ≈ 71%`; the simulated readout at seed 1 shows 70%, because the unused reservation that spills down changes from tick to tick and averages about 5.6 voices rather than 6. `N = 20`, `a = 2`, `g = 1.5`, `W = 1.2`: player demand 32.0.

**The one insight.** Load in Flat mode, running, with the "you" dot's refused rings visible within the first two seconds and a banner showing "Your sounds kept: 4x%". The first click on "Tiered" should flip that number to 100% while the room still looks busy.

**Accessibility.** Keyboard-operable controls with visible focus; every flash also updates the text table; `prefers-reduced-motion` pauses the room animation and shows a static snapshot updated every 500 ms; light and dark palettes from `templates/interactive-tokens.css`.
