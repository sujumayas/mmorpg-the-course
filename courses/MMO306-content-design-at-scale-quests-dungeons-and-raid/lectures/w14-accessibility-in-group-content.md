# MMO306 · Week 14 — Accessibility in Group Content

**Why this matters:** A single-player game can let one player slow down, skip a fight or turn on an assist, and nobody else is affected. A raid can't slow the boss for one member. Group content takes the needs of every member at once, so a cue that fails one player in twenty fails most raids. This week you learn to find those cues before launch and to decide which fixes belong to one player's settings and which belong in the encounter.

**You will be able to:**
- Compute the share of players a fight shuts out from a cue table of mechanics, channels and player profiles, and the share of groups that contain at least one of them.
- Design redundant cues that cover every profile with the fewest added channels, and rank fixes by the players they recover.
- Classify an accessibility fix as a per-player setting, a shared encounter change or an alternative way to play, and critique a shipped game's choices in those terms.
- Audit a boss fight for perception, timing, communication and memory barriers and write the fix list.

**Before class:** Microsoft Learn, Xbox Accessibility Guideline 103, "Additional channels for visual and audio cues" (20 minutes, read the implementation guidelines and the "Potential player impact" table). Game Accessibility Guidelines, the vision and hearing categories at basic and intermediate level (15 minutes). Reread [week 5, section 3](w05-telegraphing-and-readability.md) on readability.

**Prerequisites from earlier courses:** [UX201 week 11, accessibility guidelines](../../UX201-game-ux-and-player-psychology/lectures/w11-accessibility-guidelines.md) covered the guideline sets, contrast and why colour alone is not a signal. This week applies them to groups and does not repeat them. [MMO306 week 5, telegraphing and readability](w05-telegraphing-and-readability.md) gave you the raid multiplier for timing and the idea that redundancy trims the tail. [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) is the "at least one" calculation used here. [GD203 week 13, difficulty modes and scaling](../../GD203-combat-and-progression-design/lectures/w13-difficulty-modes-and-scaling.md) covered single-player assists. [MMO305 week 10, communication design](../../MMO305-social-systems-and-online-behaviour/lectures/w10-communication-design-chat-emotes-pings.md) covered pings and non-verbal communication.

**Interactive:** [`examples/w14-cue-coverage.html`](../examples/w14-cue-coverage.html). Keep it open during section 2.

---

## 1. What changes when the content is shared

**Accessibility** is how well people with disabilities can play your game. UX201 week 11 defined a disability as a mismatch between a person and a design. A colour-deficient player is not shut out by debuffs that carry a colour and a symbol, but is shut out by debuffs that differ only in colour.

Four kinds of barrier show up in group content.

- **Perception.** The player can't see, hear or tell apart a cue. A colour-only marker, a sound-only warning, a tiny icon.
- **Timing and input.** The player can't respond fast enough, hold a button long enough, or press keys fast enough. Week 5 covered the timing half with the raid multiplier.
- **Communication.** The fight can only be done with voice chat, fast typing or reading a stream of text.
- **Memory and attention.** The fight asks the player to track too many rules at once, or to learn a new visual language for one boss.

A single-player game can slow down, extend a window or skip a fight. Group content mostly can't, for two reasons.

**The world is shared.** The boss exists once, on the server, for every player in the group. You can't give one player a slower boss. Anything that changes the fight changes it for everyone.

**The group takes the union of its members' needs.** A raid of 20 must accommodate every barrier any of its 20 members has. If a cue fails one member, that member fails the mechanic, and depending on the mechanic (week 5, section 5), the group may wipe. So a barrier that affects few players affects many groups. That multiplication is this week's worked example.

A **player profile** is a group of players who read cues in the same way. It covers the person and their setup (screen, sound, settings). A player who is hard of hearing and one who raids with the sound off share a profile here, because neither receives a sound cue.

## 2. Worked example: the weakest cue, the widest group

### The hook

According to the US National Eye Institute, about 1 in 12 men has a colour vision deficiency. The most common kind makes red and green hard to tell apart.

One in twelve sounds like a small minority. Now form a raid of 20 men and ask how likely it is that at least one of them has it. The chance that nobody does is `(11/12)^20 ≈ 0.175`. So in about **82% of those raids**, at least one member cannot reliably tell a red debuff from a green one. In a five-player dungeon group, the figure is 35%.

World of Warcraft added a suite of colourblind filter options under its accessibility settings in patch 6.1.0, in February 2015, more than ten years after launch. In January 2026, patch 12.0.0 built boss warnings into the game, with a timeline of upcoming casts and centre-screen text alerts at three levels of urgency. Both changes make more sense once you see how a group multiplies a single player's barrier.

### The model

Describe a fight by its **cue table**. For each mechanic `j`, list the set of **channels** `S_j` that carry its message. This lecture uses five channels. **Colour** is hue. **Shape** is the drawn area on the ground or a position. **Icon** is a symbol over a player's head or on their frame. **Text** is an on-screen alert. **Sound** is a distinct audio cue.

Describe the players by profiles. Profile `k` makes up a share `w_k` of the population and can read a set of channels `R_k`.

```
profile k is shut out of mechanic j    if  S_j ∩ R_k is empty
shut-out share of the fight           E = sum of w_k over profiles shut out of at least one mechanic
blocked groups of size N              G = 1 − (1 − E)^N
```

- `S_j ∩ R_k` is the set of channels of mechanic `j` that profile `k` can read. If it is empty, the message never reaches them.
- `E` is the share of players who cannot read at least one mechanic of the fight. It is a sum over profiles, so profiles must not overlap. We treat each player as having one profile, which is a simplification for players with more than one barrier.
- `G` is the share of groups of `N` randomly matched players that contain at least one shut-out member. It is MA102 week 3's complement rule, and it is week 5's raid multiplier applied to people instead of casts.

Two properties of the model do all the work. **Within a mechanic, channels combine by "or".** A profile is shut out only if it can read none of the channels, so each added channel removes whole profiles from the problem. **Across mechanics, barriers combine by "and".** A player must read every mechanic, so the fight is as accessible as its worst mechanic for each profile.

### Numbers you can check

Use four profiles. The shares are for teaching.

| Profile | Share `w` | Cannot read | Can read |
|---|---|---|---|
| Typical | 78% | — | colour, shape, icon, text, sound |
| Colour-deficient | 5% | colour | shape, icon, text, sound |
| Sound off | 15% | sound | colour, shape, icon, text |
| Low vision | 2% | icon, text | colour, shape, sound |

The 5% comes from the published prevalence. About 8% of men and 0.4% of women of Northern European ancestry have a congenital colour vision deficiency. For a player base that is 60% men, `0.6 × 8% + 0.4 × 0.4% = 4.96%`, about 5%. The gender split is an assumption. The 15% for sound off combines players with hearing loss (the WHO estimates that over 5% of the world's population has disabling hearing loss) with players who raid with the game muted. That figure is a teaching value, and you should replace it with telemetry from your own game. The 2% for low vision is also invented. It stands for players who can see large shapes and colours but not small icons and text.

Now an invented boss, the Twin Wardens, with four mechanics.

| Mechanic | What happens | Channels `S` | Profiles shut out |
|---|---|---|---|
| Polarity | Each player gets a red or green debuff and must stand with their colour | colour | Colour-deficient |
| Burning ground | Orange circles appear under players | colour, shape | None |
| Whisper | A sound plays and the targeted player must face away from the boss | sound | Sound off |
| Chains | Two players get a tether and an icon, and a text alert names them | icon, text | Low vision |

Every profile except the typical one is shut out of exactly one mechanic, so `E = 5% + 15% + 2% = 22%`. Now fix the fight one cell at a time.

| Fight | `E` | Groups of 5 | Groups of 10 | Groups of 20 |
|---|---|---|---|---|
| As designed | 22.0% | 71.1% | 91.7% | 99.3% |
| + icon on polarity | 17.0% | 60.6% | 84.5% | 97.6% |
| + text on whisper | 2.0% | 9.6% | 18.3% | 33.2% |
| + sound on chains | 0.0% | 0.0% | 0.0% | 0.0% |

Check one cell by hand. After two fixes, only the low-vision profile is shut out, so `E = 2%`. For a group of 20, `1 − 0.98^20 = 1 − 0.668 = 0.332`. One raid in three still has a member who can't read the chains.

Three things stand out.

**A fight is as good as its worst cue.** The burning ground was already fine, so fixing it would change nothing. Each fix removed one profile, and the best order targets the largest shut-out profile first. Text on the whisper recovered 15% of players on its own.

**Small shares become large group shares.** A fight that fails 2% of players looks fine in a playtest of one. It blocks a third of 20-player raids. That is why a raid must get to zero on the essential mechanics, not "low."

**Each fix is one cell.** Three extra channels, an icon, a text line and a sound, took the fight from 99% of raids blocked to none. None of them changed the fight's difficulty for anyone.

The same table from code:

```python
# Share of players in each profile, and the channels each profile can read.
PROFILES = {
    "typical":          (0.78, {"colour", "shape", "icon", "text", "sound"}),
    "colour-deficient": (0.05, {"shape", "icon", "text", "sound"}),
    "sound off":        (0.15, {"colour", "shape", "icon", "text"}),
    "low vision":       (0.02, {"colour", "shape", "sound"}),
}

def shut_out(fight):
    """Share of players who cannot read at least one mechanic of the fight."""
    return sum(w for w, reads in PROFILES.values()
               if any(not (channels & reads) for channels in fight.values()))

def blocked(E, N):
    """Share of random N-player groups with at least one shut-out member."""
    return 1 - (1 - E) ** N

fight = {"polarity": {"colour"}, "burning ground": {"colour", "shape"},
         "whisper": {"sound"}, "chains": {"icon", "text"}}
fixes = [("as designed", None, None), ("+ icon on polarity", "polarity", "icon"),
         ("+ text on whisper", "whisper", "text"), ("+ sound on chains", "chains", "sound")]

for label, mech, channel in fixes:
    if mech:
        fight[mech] = fight[mech] | {channel}
    E = shut_out(fight)
    print(f"{label:20s} E={E:5.1%}  groups of 5: {blocked(E, 5):5.1%}"
          f"  10: {blocked(E, 10):5.1%}  20: {blocked(E, 20):5.1%}")
```

It prints:

```
as designed          E=22.0%  groups of 5: 71.1%  10: 91.7%  20: 99.3%
+ icon on polarity   E=17.0%  groups of 5: 60.6%  10: 84.5%  20: 97.6%
+ text on whisper    E= 2.0%  groups of 5:  9.6%  10: 18.3%  20: 33.2%
+ sound on chains    E= 0.0%  groups of 5:  0.0%  10:  0.0%  20:  0.0%
```

### A visual you can move

Open the interactive. The left view is the cue table as a grid, mechanics down the side and channels across the top. Click a cell to add or remove a channel. Under the grid, each profile has a row that turns hatched on every mechanic it can't read, and shows its share.

The right view plots `G`, the share of blocked groups, against group size from 1 to 40. It keeps a faint copy of the "as designed" curve for comparison, and marks 5, 10, 20 and 40 players.

Start with the fight as designed. The curve on the right is nearly a wall. It is above 70% by five players. Add text to the whisper. The curve falls, and for small groups it drops close to the floor. But look at 20 and 40 players, where the curve still climbs. Then add sound to the chains and it lies flat on zero. The shape of the right-hand view is the lesson. Small groups forgive a small `E`. Large groups don't.

### Cross-game recognition

**World of Warcraft, patch 6.1.0 (Warlords of Draenor, February 2015).** Blizzard added colourblind filter options to the accessibility settings. A filter changes a profile, not a mechanic. It tries to make colour readable for the colour-deficient profile by remapping the screen's colours. In model terms, it adds "colour" to `R_k` for one profile, partly, and for every mechanic at once. The Game Accessibility Guidelines are wary of whole-screen filters. The guideline against colour-only information notes that colourblind players often dislike them, and recommends adding shapes, symbols or text to the cues themselves. That is the model's preference too. A second channel in `S_j` works for every profile that can read it, while a filter works for one profile, and only as well as the remapping does.

**World of Warcraft, patch 12.0.0 (Midnight systems patch, January 2026).** The Boss Warnings feature adds a Boss Timeline of upcoming casts and centre-screen text alerts at Minor, Medium and Critical levels, enabled by default. The same patch lets the Cooldown Manager's sound alerts use text-to-speech. In model terms, the game adds the text channel to every boss mechanic that has an alert, across the whole game, from the client. Week 5 told the history of players adding those channels themselves with addons for nearly two decades.

**Xbox Accessibility Guideline 103 (Microsoft, current).** The guideline asks that any visual content critical to gameplay also be expressed through at least one other sensory method, and the same for audio. It adds that haptic feedback should not be the only extra channel, because some players use devices without it or turn it off. In model terms, it says `S_j` must span two senses. That rule guarantees that no single-sense profile is shut out. It is stronger than "two channels", because two visual channels (colour and icon) still both fail a player who can't see the screen well.

**Outside games, the traffic light.** Red is on top and green is at the bottom, in almost every country. Position carries the same message as colour, so a driver with red-green deficiency reads the light by where it is lit. That is a two-channel cue, `S = {colour, shape}` in this lecture's terms.

### Eyes-open design judgment

- **Design the cue table before the art.** The cheapest time to add an icon to a mechanic is before the effects team has built it. Write the channel set for every mechanic in the encounter document (week 4) and check it against your profiles.
- **Count senses, not channels.** Colour plus icon is two channels and one sense. It fixes the colour-deficient profile but not low vision or a player who is not looking at that part of the screen. For essential mechanics, aim for one visual and one audio channel at least, as XAG 103 asks.
- **More channels is not free.** Every added cue is also clutter for the typical profile, and week 5 showed that clutter hides warnings. Add channels to essential mechanics first, and keep the added cues in the game's shared grammar so they don't compete for attention.
- **The group share is not the player's share.** `G` treats groups as random. But a colour-deficient player in a fixed guild is in every one of that guild's raids. From that player's side, the colour-only mechanic fails 100% of their raids. Random groups spread the barrier. Fixed groups concentrate it on the same people week after week.
- **Profiles are estimates.** The shares in this lecture are teaching values. Use your own telemetry (how many players raid with sound off?), surveys and the published prevalence figures. And test with players who have the barriers. Microsoft's guideline points out that colourblind simulators are useful during development but do not replace testing with colourblind players.

### Check yourself (worked example)

1. A fight has three mechanics with channels {colour, sound}, {shape} and {text}. Using the four profiles above, compute `E` and the share of blocked 8-player groups.
2. You want at most 10% of 20-player raids to contain a shut-out player. What is the largest `E` you can accept?

<details>
<summary>Answers</summary>

1. {colour, sound}: colour-deficient reads sound, sound off reads colour, low vision reads both. No one is shut out. {shape}: every profile reads shape. {text}: low vision is shut out. So `E = 2%`, and `G = 1 − 0.98^8 = 14.9%`.
2. `1 − (1 − E)^20 ≤ 0.10` gives `(1 − E)^20 ≥ 0.9`, so `1 − E ≥ 0.9^(1/20) = 0.99475` and `E ≤ 0.53%`. For a raid, "almost everyone can read it" is not good enough. Only zero is.

</details>

## 3. What one player can change, and what the group shares

Every accessibility fix in group content falls into one of three kinds. Knowing which one you are building tells you who pays for it.

| Kind | Who it affects | Examples | Cost to other players |
|---|---|---|---|
| Per-player setting | One player's client | Colour filters, custom alert colours, text size, alert text, text-to-speech, sound cue volume, key remapping, toggles instead of holds | None |
| Shared encounter change | Everyone in the fight | Adding a channel to a mechanic, longer telegraphs (week 5), turning a wipe mechanic into a damage mechanic, fewer simultaneous rules | Changes the fight for all |
| Alternative way to play | Players who choose it | Easier tiers (week 6), NPC party members, solo story versions | Splits players across versions |

**Per-player settings are the first line.** They cost nothing to anyone else, because they change what one client draws or plays. Almost every perception fix can be one. A client can add a text alert to a sound cue, turn a colour into a shape, or read an alert aloud. World of Warcraft's Boss Warnings and colourblind filters are both per-player. They also have a limit. A setting can only present information the client has. If a mechanic's target is known to the server only at the last moment, no client setting can warn earlier.

**Shared encounter changes are what the cue table is for.** Adding an icon to a mechanic is shared in a technical sense, since every player sees it, but it costs no one anything. That is why channel fixes are the cheapest shared changes you have. Timing changes are different. A longer telegraph makes the fight easier for every player. Week 5 showed how to size a telegraph for the raid, and week 6 showed how difficulty tiers can hold different telegraph lengths. The accessibility question is whether your easiest tier's timing is achievable for the players you intend it for.

**Alternative ways to play remove the group.** Some barriers are about the group itself. A player may not be able to commit to a fixed raid night, may find voice chat with strangers stressful, or may need to pause without letting four people down. For them, the most accessible group content is content they can do without a group.

- Final Fantasy XIV introduced **Trust** in Shadowbringers (patch 5.0), letting players run main-scenario dungeons with NPC party members. In patch 6.1 the NPC party system for story dungeons became **Duty Support**, which by patch 7.5 covers every main-scenario dungeon, the dungeons in the levelling roulette, and the 4-player main-scenario trials.
- World of Warcraft added **Follower Dungeons** in patch 10.2.5 (January 2024). Up to four NPC followers fill a party, the queue is instant, and the loot matches Normal difficulty. With The War Within, **Story** raid difficulty extended the idea to raids, starting with Nerub-ar Palace. The player and nine NPCs face a simplified final boss, with no loot. Week 6 placed this tier on the difficulty ladder.

These systems cost production (NPC behaviour for every boss) and they split players across versions of the content. But they are the only kind of fix that reaches barriers no setting can touch, such as schedules and social anxiety. They are also the only fix for a mechanic that needs a group by design.

## 4. Timing and input

Week 5 sized telegraphs for a raid. Two more questions apply to accessibility.

**What does the mechanic ask of the hands?** A response can be a single press, a held button, a rapid series of presses, a precise movement or several inputs at once. The Game Accessibility Guidelines ask designers to avoid requiring buttons to be held down, or to offer alternatives such as toggles, because holding demands motor ability and can cause pain over long sessions. In group content the question is whether the requirement is essential to the mechanic. "Hold to channel the beam" can almost always become "press to start, press to stop" in the client, with no change to the fight.

**When is success judged?** Week 5 recommended mechanics judged by position over a window over those judged at an exact moment. The accessibility reason is that a window turns a reaction-time requirement into a planning requirement. A player who is slower to react but understands the mechanic can still reach the safe zone in time, because they started earlier.

**Which role carries the demand?** In a group, demands are not spread evenly. Week 4, section 5, looked at which roles pay for each mechanic. If one role takes most of the fast responses, players who can't meet them are effectively barred from that role. Look at the demand per role as well as per fight, and check that each role has a version of the fight a slower player can do.

## 5. Talking, reading and remembering

**Communication.** A fight that needs a caller shouting "swap now" in voice chat is shut to players who are deaf, who can't use a microphone, or who don't share a language with the group. MMO305 week 10 showed that pings and markers can carry most coordination without voice. The design rule is that every essential call in a fight should be possible with in-game tools, such as markers on players, a countdown and a raid warning. If your fight can only be done with voice, you have added a communication channel to a mechanic that no setting can replace.

**Reading.** Text alerts are a good second channel, but a fight that sends a stream of text is a reading test. Keep essential alerts short, few and in a fixed place, and let players move and resize them. Translated alerts run longer than the English ones, so size the alert box for the longest language ([GD202 week 11, writing for localization](../../GD202-narrative-and-quest-design/lectures/w11-writing-for-localization.md)).

**Memory and attention.** Every rule a player must hold in mind costs attention. UX201 week 2 treated this as cognitive load. Week 5 showed that a consistent visual grammar lets players carry what they learned from one boss to the next. For accessibility, count the rules active at the same moment in each phase. A phase that asks for five simultaneous rules is harder for everyone. It is much harder for players with attention or memory impairments, and no per-player setting fixes it. The fix is in the encounter design, by spreading rules across phases (week 4).

## 6. Auditing a fight

Put sections 2 to 5 together into an audit you can run on any encounter document.

1. **Write the cue table.** One row per mechanic, with the channels that carry it, whether it is essential (failure costs a death or a wipe) and its telegraph length.
2. **Choose your profiles and shares.** Start with the four in section 2 and add any your game needs, for example "controller only" or "no voice chat." Replace the teaching shares with your data where you have it.
3. **Compute `E` and `G`** for your group sizes. Any essential mechanic that shuts out a profile is a blocker for group content. Aim for `E = 0` on essential mechanics.
4. **Classify each fix** as a setting, a shared change or an alternative, using the section 3 table. Prefer settings, then channel additions, then timing changes, then alternatives.
5. **List the non-perception barriers.** Holds and rapid presses, exact-moment checks, voice-only calls, the peak number of simultaneous rules per phase.
6. **Test with players** who have the barriers. The cue table only prepares you.

## In-class activity (25 minutes)

Work in groups of three. Take the encounter you designed for lab 04 (or the week 4 example if you have none).

1. **(8 min)** Write its cue table: every mechanic, its channels, and whether it is essential.
2. **(5 min)** Using the four profiles from section 2, compute `E`, and `G` for your intended group size. Check with the interactive.
3. **(7 min)** Find the cheapest set of channel additions that brings `E` to zero on essential mechanics. Order them by players recovered.
4. **(5 min)** Name one barrier in your fight that no channel fixes (timing, input, communication or memory). Classify your fix as a setting, a shared change or an alternative, and say who pays for it.

Expected output: a cue table, `E` and `G` before and after, an ordered fix list, and one non-perception barrier with its fix.

## Common misconceptions

- **"Only a few percent of players are affected, so it's a niche feature."** The share of groups affected is `1 − (1 − E)^N`. A 2% barrier touches a third of 20-player raids, and a 5% barrier touches 64% of them.
- **"A colourblind filter solves colour problems."** A filter changes one profile's view of the whole screen, and players often dislike them. A second channel on the mechanic solves the problem for every profile that can read that channel.
- **"Accessibility means making the fight easier."** Most perception fixes change what players are told, not what they must do. The Twin Wardens went from 99% of raids blocked to none with three added cues and no change to difficulty.
- **"Two channels are always enough."** Two visual channels both fail a player who can't see that part of the screen. Essential mechanics need channels in two senses.

## Check yourself

1. In a five-player dungeon, what share of groups of men contains at least one man with colour vision deficiency, using the NEI's 1 in 12?
2. A fight's mechanics are {sound}, {colour, icon} and {shape, text}. Using the section 2 profiles, compute `E`. Which single channel addition recovers the most players, and what is `E` after it?
3. A designer says: "We'll add a text alert to every mechanic in the client, so we don't need to change any encounter." Using the profiles, say which profiles this fixes and which it doesn't, and name one barrier it cannot touch.
4. A guild of 20 has one colour-deficient member and a boss with a colour-only essential mechanic. What share of this guild's raids is affected? Why does `G` give a different answer?
5. Classify each fix as a per-player setting, a shared encounter change or an alternative way to play: (a) a toggle option for a channelled ability; (b) a longer telegraph on the easiest tier; (c) an NPC healer for story dungeons; (d) an icon added to a debuff.

<details>
<summary>Answers</summary>

1. `1 − (11/12)^5 = 1 − 0.647 = 35.3%`.
2. {sound} shuts out sound off (15%). {colour, icon}: colour-deficient reads the icon, and low vision reads the colour, so no one is shut out. {shape, text}: everyone reads shape. So `E = 15%`. Adding text (or an icon) to the sound mechanic recovers all 15%, giving `E = 0`.
3. Text reaches the sound-off and colour-deficient profiles, so every mechanic that shut them out is fixed. It does not help low vision, which can't read text. A mechanic carried only by icon and text still shuts them out, so it needs a sound or a shape. Text can't touch timing, input, voice-only calls or memory load, and it can only warn about what the client knows in time.
4. 100%. The member is in every raid. `G` assumes random groups, where the chance of drawing a shut-out player is `E` per slot. Fixed groups concentrate the barrier on the same people.
5. (a) Per-player setting. (b) Shared encounter change, limited to one tier. (c) Alternative way to play. (d) Shared encounter change, but one that costs no one anything.

</details>

## Lab / assignment hook

[Lab 14, an accessibility audit](../labs/lab14.md). You implement the cue-table model, run it on a three-boss encounter file, find the cheapest set of channel additions that brings every essential mechanic to zero, and write an audit of the non-perception barriers. The audit goes into your final dungeon document, where each of your three bosses must have a cue table with `E = 0` on essential mechanics.

## Sources

- National Eye Institute (NIH), "Color Blindness" (retrieved September 2026). About 1 in 12 men have colour vision deficiency; the most common type affects red and green. https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/color-blindness
- Wikipedia, "Color blindness" (retrieved September 2026). As many as 8% of men and 0.4% of women of Northern European ancestry have congenital colour deficiency. https://en.wikipedia.org/wiki/Color_blindness
- World Health Organization, "Deafness and hearing loss" fact sheet (retrieved September 2026). Over 430 million people, more than 5% of the world's population, need rehabilitation for disabling hearing loss. https://www.who.int/news-room/fact-sheets/detail/deafness-and-hearing-loss
- Warcraft Wiki, "Patch 6.1.0" (Warlords of Draenor, released 24 February 2015). Added a suite of colourblind filter options under the Accessibility settings of the Interface menu. https://warcraft.wiki.gg/wiki/Patch_6.1.0
- Warcraft Wiki, "Patch 12.0.0" (Midnight systems patch, released 20 January 2026). Boss Warnings with a Boss Timeline and Minor, Medium and Critical text alerts, on by default; text-to-speech option for Cooldown Manager sound alerts. https://warcraft.wiki.gg/wiki/Patch_12.0.0
- Warcraft Wiki, "Follower Dungeon" (as of the Midnight era, 2026). Introduced in patch 10.2.5 (16 January 2024); up to four NPC followers; instant queue; Normal difficulty loot. https://warcraft.wiki.gg/wiki/Follower_Dungeon
- Warcraft Wiki, "Story Mode" (The War Within and later raids, read September 2026). Extension of Follower Dungeons to raids, first with Nerub-ar Palace; simplified final boss; nine accompanying NPCs listed; no loot; available from week two of the raid. https://warcraft.wiki.gg/wiki/Story_Mode
- Final Fantasy XIV Online Wiki (consolegameswiki), "Trust System" and "Duty Support" (as of patch 7.5, read September 2026). Trust introduced in patch 5.0; Duty Support separated from it in patch 6.1; coverage of main-scenario dungeons, levelling-roulette dungeons and 4-player main-scenario trials. https://ffxiv.consolegameswiki.com/wiki/Duty_Support
- Microsoft Learn, "Xbox Accessibility Guideline 103: Additional channels for visual and audio cues" (current version). Critical visual or audio content expressed through at least one other sensory method; haptics not as the only additional channel; simulators do not replace testing with colourblind players. https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/103
- Game Accessibility Guidelines, "Ensure no essential information is conveyed by a fixed colour alone" (basic, vision); "Ensure that all important supplementary information conveyed by audio is replicated in text / visuals" (intermediate, hearing); "Avoid / provide alternatives to requiring buttons to be held down" (intermediate, motor). https://gameaccessibilityguidelines.com
- The profile shares other than the colour-vision figure, the gender split, the Twin Wardens encounter and its mechanics are invented for teaching.

## Interactive spec: examples/w14-cue-coverage.html

**The one insight.** A fight is only as accessible as its worst cue for each player profile, and group size turns a small shut-out share into a large share of blocked groups. The student must see the blocked-groups curve stand like a wall at the "as designed" setting, then collapse to zero after three single-cell fixes, with a 2% intermediate step still blocking a third of 20-player raids.

**Layout.** Two linked views side by side on wide screens, stacked on phones (grid first).

- **Left view, "Cue table".** A grid with mechanics as rows (Polarity, Burning ground, Whisper, Chains) and channels as columns (colour, shape, icon, text, sound). Each cell is a toggle button showing a filled mark when the channel is on. Below the grid, a profile panel with one row per profile (Typical 78%, Colour-deficient 5%, Sound off 15%, Low vision 2%). For each profile, show one small box per mechanic: plain when the profile can read at least one of that mechanic's channels, hatched with the word "blocked" when it cannot. The profile's share is shown at the row end, struck through when the profile is fully covered.
- **Right view, "Groups with a shut-out member".** x axis group size `N` from 1 to 40, y axis `G` from 0 to 100%. The current curve `G(N) = 1 − (1 − E)^N` as a solid line, and the "as designed" curve as a faint dashed line. Markers with values at N = 5, 10, 20 and 40. A large readout of `E`.
- **Readout under both views.** `E` and `G` at 5, 10, 20 and 40 to one decimal percent, and a list of fixes applied so far with the players each recovered. Copyable as text.

**Controls.**
- Grid cell toggles (click, Enter or Space).
- Preset buttons: "As designed", "+ icon on polarity", "+ text on whisper", "+ sound on chains" (cumulative, in that order), and "Reset".
- Profile share sliders in an "Edit shares" drawer: colour-deficient 0 to 15% (default 5), sound off 0 to 40% (default 15), low vision 0 to 10% (default 2). Typical is the remainder, and the sliders are constrained so the remainder stays at or above 0.
- Toggle "Hook mode": replaces the fight with one colour-only mechanic and one profile at 1/12 (8.33%), to reproduce the lecture's hook.

**Formulas.**
- Profile `k` is shut out of mechanic `j` if `S_j ∩ R_k` is empty. `R` sets: Typical all five; Colour-deficient all but colour; Sound off all but sound; Low vision colour, shape, sound.
- `E = Σ w_k` over profiles shut out of at least one mechanic.
- `G(N) = 1 − (1 − E)^N`.

**Test values.**
- As designed (Polarity {colour}, Burning ground {colour, shape}, Whisper {sound}, Chains {icon, text}): `E = 22.0%`; `G` = 71.1%, 91.7%, 99.3%, 100.0% at N = 5, 10, 20, 40.
- + icon on polarity: `E = 17.0%`; `G` = 60.6%, 84.5%, 97.6%.
- + text on whisper: `E = 2.0%`; `G` = 9.6%, 18.3%, 33.2%, 55.4% at N = 5, 10, 20, 40.
- + sound on chains: `E = 0.0%`; `G = 0` for all N.
- Hook mode: `G` = 35.3% at N = 5, 50.1% at N = 8, 82.5% at N = 20 (exact 0.8245).
- Check-yourself Q1 of section 2 (mechanics {colour, sound}, {shape}, {text}): `E = 2.0%`, `G(8) = 14.9%`.

**First screen.** "As designed", so the student sees three hatched "blocked" boxes in the profile panel and a curve on the right that is above 70% by five players.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. The page must pass its own audit: blocked states use hatching and the word "blocked", never colour alone; the two curves differ by dash pattern and direct labels; every toggle has a text label and a visible focus ring; readouts in an `aria-live="polite"` region; transitions off under `prefers-reduced-motion`.
