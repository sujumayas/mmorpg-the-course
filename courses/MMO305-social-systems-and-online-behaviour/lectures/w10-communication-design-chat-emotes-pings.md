# MMO305 · Week 10 — Communication Design: Chat, Emotes, Pings

**Why this matters:** Every social system you have studied in this course runs through a communication channel. Grouping, guild life, trust and toxicity all depend on who can say what, to whom, how fast and how loudly. The channel is a design decision, and players feel its limits long before they can name them.

**You will be able to:**
- Compute the message rate, on-screen lifetime and per-reader coverage of a chat channel from its size, posting rate and reading capacity.
- Explain why a saturated channel gives every message the same audience no matter how many players join, and predict the spam incentive this creates.
- Compare free text, restricted vocabularies (emotes, preset phrases) and contextual pings by speed, expressiveness and abuse surface, using keystroke-level estimates.
- Design a channel structure (scope, split, rate limit, vocabulary) for a stated social goal and defend its trade-offs.

**Before class:** Taylor, *Play Between Worlds* (2006), chapter 1, "Finding New Worlds" (pp. 1-20), Taylor's account of arriving in EverQuest and learning its public spaces. Nielsen, "Participation Inequality" (2006, Nielsen Norman Group), which you will reuse in week 12. Reread your UX201 notes on the keystroke-level model.

**Prerequisites from earlier courses:** [UX201 week 2, cognitive load and UI](../../UX201-game-ux-and-player-psychology/lectures/w02-cognitive-load-and-ui.md) (the keystroke-level model and its operator times). [UX201 week 1, perception, attention, memory](../../UX201-game-ux-and-player-psychology/lectures/w01-perception-attention-memory.md) (limited attention). [GD101 week 12, feedback, juice, clarity, readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md). [MMO304 week 10, market design](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w10-market-design-auction-houses-vendors-barter.md) (search cost, which comes back when we ask why Trade chat exists). From this course, [week 8, griefing](w08-griefing-typology-and-design-responses.md) and [week 9, toxicity](w09-toxicity-research-and-interventions.md). [Week 1, social capital](w01-mmos-as-societies-social-capital.md) and [week 3, grouping](w03-forced-vs-voluntary-grouping.md) come back in section 4.

**Interactive:** [examples/w10-chat-channel-load.html](../examples/w10-chat-channel-load.html). Use it during section 2.

---

## 1. What a channel is made of

A **channel** is any route a message can take from one player to others. Party chat, a guild's message board, a zone-wide shout, a raid's voice server, a ping on a map and a bow emote are all channels. Designers tend to think of "the chat system" as one feature. It is better to think of a game as offering a set of channels, each with its own settings, and to ask what each setting does to behaviour.

Five settings describe almost any channel.

1. **Audience.** Who receives the message. One person (a whisper), a fixed group (party, guild), everyone in a place (a zone channel), or everyone on the server.
2. **Vocabulary.** What can be said. Free text allows anything. A preset list (emotes, template phrases) allows only what the designer wrote. A contextual ping allows a small set of meanings attached to a location or object in the world.
3. **Speed.** How long it takes to compose and read one message. Typing a sentence mid-fight costs seconds. Pressing one key costs a fraction of one.
4. **Persistence.** How long a message stays visible. A line in a busy chat window may scroll off in seconds. A message carved into the floor of a dungeon can wait for weeks.
5. **Cost to the sender.** What stops a player from sending a thousand messages. Usually nothing, unless the designer adds a rate limit, a cooldown or a price.

Each setting trades one good against another. A wide audience helps a trader find a buyer and helps a harasser find a victim. Free text lets friends joke and lets strangers insult. Speed makes coordination possible in combat and makes spam cheap. You will see these trade-offs again in every example below, and your job as a designer is to choose them on purpose.

### What players use channels for

It helps to sort messages by purpose, because different purposes want different settings.

- **Coordination.** "Pull the boss after I buff." "Enemy behind the rock." These messages are short, urgent and useful only for seconds. They want speed and a small, known audience.
- **Exchange.** "Selling 20 iron ore." "Looking for a healer." These messages are about finding a match among strangers. They want a wide audience and some persistence.
- **Sociability.** Greetings, jokes, stories, arguments. These build the ties you studied in weeks 1 to 4. They want expressiveness and a stable audience of people who will meet again.
- **Expression and status.** Dancing on a mailbox, showing off a rare emote. These are closer to the display behaviour from week 7 than to talk.

A single free-text channel that tries to serve all four purposes at once serves none of them well. The next section shows why with numbers.

## 2. Worked example: why Trade chat scrolls faster than you can read

### The hook

In World of Warcraft, the Trade channel only works inside capital cities, and it is linked across every capital on a realm. Anyone standing in Stormwind or Orgrimmar can post and read. On a busy realm the channel moves so fast that a message is gone before most players have read it, and players respond by posting the same offer again and again. In patch 9.2.7 (2022) Blizzard split off a second channel, Trade (Services), for selling runs and boosts, and left the original channel for buying and selling goods.

Why would a bigger audience make each message *less* likely to be read? And why does splitting one channel into two help? A small model answers both questions.

### The model

Let a channel have `L` listeners. A share `s` of them post, each at an average rate `r` messages per minute. Every listener can read at most `R` messages per minute while also playing the game. The chat window shows `W` lines.

```
posters             N = s × L
channel rate        M = N × r = s × L × r          (messages per minute)
on-screen lifetime  T = 60 × W / M                  (seconds a message stays in the window)
coverage            c = min(1, R / M)               (share of messages one reader sees)
audience per message   A = L × c
```

- `L` counts everyone in the channel, including players who never post (the lurkers).
- `s × r` is the average posting rate per listener.
- `R` is a reading budget, not a reading speed. A player who is fighting, crafting or running reads only a few lines a minute.
- `T` assumes one line per message. Long messages wrap and scroll faster.

Two regimes appear. While `M < R`, every reader can keep up, so coverage is 100% and a message reaches all `L` listeners. Once `M > R`, readers fall behind and skim. Coverage drops as `R / M`.

Now look at the audience per message in the second regime:

```
A = L × R / M = L × R / (s × L × r) = R / (s × r)
```

**`L` cancels.** Once a channel is saturated, every message reaches the same number of readers, `R / (s × r)`, no matter how many players join. The channel keeps getting louder, and each voice in it keeps the same small audience. The saturation point is `L* = R / (s × r)`, and past it, adding listeners only adds noise.

### Numbers you can check

Take `s = 0.1` (one listener in ten posts), `r = 0.5` (a poster sends one message every two minutes), `R = 20` messages per minute and `W = 10` lines. Then `s × r = 0.05` and the saturation point is `L* = 20 / 0.05 = 400` listeners.

| Listeners `L` | Posters `N` | Rate `M` (per min) | Lifetime `T` (s) | Coverage `c` | Audience per message `A` |
|---|---|---|---|---|---|
| 50 | 5 | 2.5 | 240 | 100% | 50 |
| 200 | 20 | 10 | 60 | 100% | 200 |
| 400 | 40 | 20 | 30 | 100% | 400 |
| 1,000 | 100 | 50 | 12 | 40% | 400 |
| 3,000 | 300 | 150 | 4 | 13.3% | 400 |

Check one row by hand. At 1,000 listeners, 100 posters send 50 messages a minute. Ten lines at 50 per minute last `600 / 50 = 12` seconds each. A reader who can take in 20 lines a minute sees `20 / 50 = 40%` of them, so each message reaches `1,000 × 0.4 = 400` readers.

Look at the last column. From 400 listeners up, it does not move. A realm that grows from 400 to 3,000 people in its capitals gives no single trader a bigger market in chat. It only shortens the lifetime of each line from 30 seconds to 4.

### The spam incentive

If the audience per message is fixed, how does one poster reach more people? By posting more. A seller who posts `k` times as often as everyone else gets about `k` times the readers, and since the channel is already saturated, those readers are taken from other posters. Everyone who follows the same logic raises `r`, which raises `M`, which lowers coverage for all. This is a public-goods problem, a shared resource that each user can degrade for private gain. Each individual repost is rational, and the sum of them ruins the channel.

Put numbers on it with the table's 1,000-listener row. Suppose ten of the 100 posters start reposting every 15 seconds (`r = 4`) while the other 90 stay at `r = 0.5`. The channel rate becomes `10 × 4 + 90 × 0.5 = 85` per minute. Coverage drops to `20 / 85 ≈ 23.5%`, so each message now reaches about 235 readers instead of 400. Each spammer collects about `4 × 235 = 941` reader-views per minute. A polite poster gets `0.5 × 235 ≈ 118`, down from 200 before the spam started. The spammers win eight times the attention, and everyone's lines now last `600 / 85 ≈ 7.1` seconds.

### A visual the student can move

Open `examples/w10-chat-channel-load.html`. The left panel plots channel rate `M` against listeners `L`. It is a straight line going up, and it looks like a lively community. The right panel plots the audience per message `A` on the same horizontal axis. It climbs until `L*` and then goes flat. Drag `L` past the knee and watch the scrolling chat preview at the bottom speed up while the audience number stays fixed. Then turn on the "spammers" control and watch coverage fall for everyone. Finally, split the channel in two with the "split" control and see the knee move right.

### Cross-game recognition

The model is simple enough that you can rewrite most channel designs in its terms. The question to ask each time is: which of `L`, `s`, `r` or `R` did the designer change?

**World of Warcraft, Trade and Trade (Services), patch 9.2.7 onward.** Splitting one channel into two by topic divides `M` between them. A player who only wants to buy goods listens to one channel and sees roughly half the traffic. In the model, a split into `k` topic channels, where each reader follows one, raises the saturation point to `k × L*`. The earlier design decision, limiting Trade to capital cities, cut `L` by geography. Linking all capitals on a realm raised it again, because one market is easier to search than six.

**World of Warcraft, "Barrens chat", classic era.** Before level scaling in patch 7.3.5, most Horde characters levelled through the Barrens from roughly level 10 to 20. The zone was large, with long runs between quests, so its General channel combined a large `L` with many idle players and a high `s`. The Warcraft Wiki describes the channel's reputation for off-topic noise and trolling. The model predicts exactly this: a funnel zone raises `L`, boredom raises `s × r`, and the channel saturates with messages that are not about the zone at all.

**League of Legends, ping limits (current patches, 2026).** Pings are a channel with a tiny vocabulary, and Riot rate-limits them directly. The League of Legends Wiki documents a cap of 2 to 7 pings per 5-second window depending on the player's Honor level, with a lockout of several seconds if a player exceeds it. That is a cap on `r`, and tying the cap to Honor makes the budget a reward for good conduct.

**Hearthstone, emotes.** Hearthstone gives each player six emotes and throttles them to one every few seconds. It also gives the receiver a **squelch** button that hides the opponent's emotes for the rest of the match. Squelch sets the receiver's own `R` for that sender to zero. The sender can still press the button, and it no longer reaches anyone. The cost of a spam attack falls on the attacker, not on the target.

**EVE Online, Local chat in wormhole space.** In most of EVE, the Local channel member list shows every pilot in the star system, so a glance at the list is intelligence about who is nearby. In wormhole space, a pilot appears in Local only after speaking. This is a change to what the channel reveals about its audience, not to its traffic. It shows that a channel's member list is a message in itself, and designers can switch it off.

### Eyes-open design judgment

The model tells you that a single shared channel has a natural size, `L* = R / (s × r)`, beyond which it stops working for everyone at once. It also tells you the four levers.

- **Shrink `L` by scope.** Zone channels, city channels, per-instance channels. The cost is that exchange needs a wide audience, so a narrow scope makes it harder to find a buyer or a group. This is why WoW linked the capitals.
- **Split by topic.** Separate channels for trade, services, groups and general talk. A split helps readers, who see a larger share of the channel they care about. It does not help posters while each new channel is still saturated, because audience per message stays at `R / (s × r)` (lab 10 tests this). The cost is fragmentation. Players must know which channel to join, and the quiet ones die.
- **Cap `r`.** Rate limits, cooldowns, slow modes, a price per message. The cost is that legitimate bursts (a raid leader giving orders) get throttled too, so apply the cap per channel and exempt small group channels.
- **Remove the need to post.** The biggest lever of all. An auction house (MMO304 week 10) turns "WTS 20 iron ore" posts into listings a buyer can search, which lowers `s` in Trade to almost nothing. A group finder does the same for "LFG healer". Structured tools beat any amount of chat tuning, because they replace a broadcast with a search.

What the model does not do is tell you how much noise is acceptable. A little chatter in a city can be a sign of life, which you want, and overheard talk is one way newcomers pick up a server's norms (week 11). The designer's decision is which purposes each channel should serve, and then which settings serve that purpose. Do not tune a channel's numbers before you have decided what it is for.

### Check yourself (worked example)

1. A channel has `s = 0.2`, `r = 1` and readers who manage `R = 15` messages per minute. What is `L*`? What coverage does a reader get at `L = 300`?
2. The same channel is split into three topic channels and each listener follows exactly one of them, with listeners spread evenly. What is the new coverage at `L = 300`?
3. A game adds a cooldown so no player can post more than once per 90 seconds. For the table's numbers (`s = 0.1`, `r = 0.5`), does this change `L*`? Why or why not?

<details>
<summary>Answers</summary>

1. `L* = 15 / (0.2 × 1) = 75`. At `L = 300`, `M = 0.2 × 300 × 1 = 60` per minute, so coverage is `15 / 60 = 25%`.
2. Each channel has 100 listeners and `M = 0.2 × 100 × 1 = 20`, so coverage is `15 / 20 = 75%`. The split tripled coverage.
3. No. A cooldown of 90 seconds caps `r` at `0.67` per minute, and the average poster already sends `0.5`. The cap only binds on heavy posters, so it matters for the spam scenario and not for the baseline.

</details>

## 3. Vocabulary: free text, preset phrases and pings

The Trade example was about traffic. The second design question is vocabulary. What can a message contain at all?

### Free text

Free text is maximally expressive. It lets players invent jokes, negotiate prices, plan a raid and form friendships, all of which you want. It also has the largest **abuse surface**, the set of harmful things a message can carry: insults, slurs, scams, personal information, links to phishing sites. Every free-text system needs filters, reporting and moderation, and all three are imperfect (weeks 8 and 9, and [MMO402 week 6 on moderation at scale](../../MMO402-emergent-society-governance-and-ethics/lectures/w06-moderation-at-scale.md)).

Free text also has a speed problem. Use the keystroke-level model from UX201 week 2 to price a typed callout in combat. "enemy healer behind the left pillar" is 35 characters. With one mental operator `M = 1.35 s`, a key to open chat, 35 keystrokes, a key to send, and `K = 0.28 s` for an average typist:

```
T_typed = 1.35 + 37 × 0.28 = 1.35 + 10.36 = 11.71 s
```

Nearly twelve seconds with both hands on the keyboard, in a game where a fight may last twenty.

### Preset phrases and emotes

A **restricted vocabulary** gives players a menu of messages the designer wrote. Its abuse surface is limited to the worst thing a preset can mean in context, and its speed is a menu choice rather than a sentence.

- **Hearthstone** (2014 onward) offers six emotes: Greetings, Well Played, Thanks, Wow, Oops and Threaten. ("Wow" replaced "Sorry" in April 2016.) Even this tiny list has an abuse surface. A "Well Played" sent after an opponent's misplay is sarcasm, which is why the game also ships squelch and a cooldown.
- **Dark Souls** (2011) lets players leave messages on the ground for other players to find, built from preset phrases. The templates allow hints and warnings. Nothing in a template stops a player from placing a true phrase in a false place, such as a hint to jump written beside a lethal drop. A restricted vocabulary narrows abuse. It does not remove it, because meaning comes from context.
- **Toontown Online** (2003-2013), a Disney MMO aimed at children, started with **SpeedChat**, a menu of pre-approved phrases. It later added SpeedChat Plus, which let players type against a filter, with blocked words replaced by an animal noise, and "True Friends" codes for less-filtered chat between people who had exchanged a code outside the game. Players under 13 needed a parent's account to enable the typed modes. The design is a ladder: the smallest abuse surface for strangers, a wider one for people with an out-of-game relationship.
- **Final Fantasy XIV** offers an auto-translate dictionary. A player picks a phrase from a menu and each reader sees it in their own client language (English, Japanese, French or German). A restricted vocabulary here solves a different problem, cross-language coordination, which free text cannot.

### Contextual pings

A **ping** attaches a meaning to a point in the game world. The player looks or points at something and presses a key, and teammates see a marker plus a short spoken or written label. The vocabulary is small, and the location does most of the work.

Apex Legends (Respawn, February 2019) made the ping system famous. Its pings let a squad mark directions, loot, enemies and plans with one button, and reviewers wrote that it made voice chat with strangers largely unnecessary. Electronic Arts received a US patent on the system in August 2021 (US 11,097,189), and press coverage that month reported that EA would let other developers use it for free as part of an accessibility patent pledge.

Price the ping with the same model. The player is usually already looking at the target, so there is no pointing cost:

```
T_ping = M + K = 1.35 + 0.28 = 1.63 s
```

That is about one seventh of the typed callout. Add a pointing operator (`P = 1.1 s`) for a ping on the minimap and it is still `2.73 s`, less than a quarter.

The ping also wins on **reading** speed. A marker in the world is read with the eyes already on the play space, while a chat line pulls attention to a corner of the screen (UX201 week 1). And it wins on language: a ping means the same thing to a player in any locale.

Pings lose on expressiveness. You cannot tell a joke with a ping, and you cannot make a friend. That is the central trade-off of vocabulary design:

| Channel type | Compose time (KLM estimate) | Expressiveness | Abuse surface | Works across languages |
|---|---|---|---|---|
| Free text | 10-15 s for one callout | Unlimited | Largest | No |
| Preset phrases | 2-4 s (menu) | Designer's list | Small, sarcasm remains | Yes, if translated |
| Contextual ping | 1.5-3 s | A few meanings plus a location | Smallest, spam remains | Yes |
| Voice | 2-4 s | Unlimited, plus tone | Large and hard to moderate | No |

No row wins on all columns. A good communication design offers several channels and lets each carry the messages it is best at.

### Pings as a new abuse surface

Small vocabularies are not immune to abuse. A ping repeated ten times on a teammate's character says something no ping was designed to say. League of Legends answers with a general rate limit and a tighter per-type limit (3 uses per 6 seconds) on the Generic, Alert and Enemy Missing pings, the ones most easily turned into nagging. The lesson generalises: any channel that can deliver a message to someone who did not ask for it can be used to harass. Rate limits and receiver-side muting are the two tools that work across all vocabularies, because they do not depend on what the message means.

## 4. Persistence, audience and the social graph

The last two settings, persistence and audience, decide whether a channel builds relationships or only carries information.

### Persistent and ephemeral channels

A chat line in a city channel lives for seconds. A post on a guild board lives for weeks. A Dark Souls message lives until the server removes it. Persistence changes behaviour in two directions.

- Persistent messages are read by people who were not there when they were written. That makes them good for knowledge (guides, rules, guild calendars) and good for reputation, because a player's words follow them.
- Ephemeral messages are cheap to send and cheap to regret. Players say more, and more carelessly.

Guild and friend channels combine a stable audience with enough persistence that people learn each other's names. That combination is what turns strangers into acquaintances, the bonding social capital you met in week 1. A zone channel almost never does this, because its audience changes every few minutes and nobody expects to meet again. Week 3's argument about forced grouping applies here too: repeated contact with the same small set of people is what produces ties, and a channel's audience rules decide whether contact repeats.

### Who can hear you is also a message

EVE's Local list shows that the audience of a channel can carry information of its own. The same is true of "seen" markers, typing indicators and online-status lists in friend panels. Each one tells other players something about you, whether or not you speak. Players ask for privacy settings on these features for good reason. When you design a channel, list what it reveals about its members as well as what it carries.

### Voice

Voice chat is the fastest free channel for coordination and the hardest to moderate. It carries tone, which helps friendly play, and it carries accent, age and gender cues, which expose some players to harassment. Most shipped MMOs leave voice to third-party tools or offer it only in parties and guilds, where the audience is chosen. If you add voice, decide the default audience deliberately. An opt-in voice channel for a pre-made group and an always-on voice channel for random teammates are different social systems.

## In-class activity (25 minutes)

Work in groups of three. You are designing the communication channels for a small fantasy MMO with one server of about 4,000 concurrent players, four cities, twelve zones, five-player dungeons and 20-player raids.

1. **List the purposes (5 min).** For each of coordination, exchange, sociability and expression, name one message players will want to send.
2. **Assign channels (10 min).** Propose a set of channels. For each, give its audience, vocabulary, persistence and rate limit. At least one channel must be a restricted vocabulary or a ping.
3. **Load test (5 min).** For your busiest public channel, estimate `L`, `s`, `r` and `R`. Compute `M`, `T` and coverage with the section 2 model. If coverage is under 50%, apply one lever and recompute.
4. **Abuse pass (5 min).** Swap designs with another group. Find one way to harass another player through their channels and name the tool (filter, rate limit, receiver mute, audience restriction) that would stop it.

Expected output: a one-page table of channels, one load calculation with numbers, and the harassment route your partners found.

## Common misconceptions

- **"More players in chat means a livelier community."** Past the saturation point, it means each message reaches the same number of readers and scrolls away faster. Activity and conversation are different quantities.
- **"Restricted vocabularies prevent toxicity."** They shrink the abuse surface. Context still turns "Well Played" or a question-mark ping into mockery, so you still need rate limits and receiver-side muting.
- **"Pings replace chat."** They replace chat for coordination. They do almost nothing for sociability, so a game that offers only pings will have efficient teams and few friendships.
- **"A rate limit punishes spammers."** A rate limit applies to everyone who hits it. Set it above the rate of legitimate use for that channel, and remember that raid leaders and traders have legitimate bursts.

## Check yourself

1. A zone channel has 600 listeners, `s = 0.05`, `r = 0.8` and `R = 12`. Compute `M`, coverage and the audience per message. Is the channel saturated?
2. Use the keystroke-level model with `K = 0.28 s` and `M = 1.35 s` to compare a typed "need heal" (9 characters plus open and send) with a one-key ping. By what factor is the ping faster?
3. A designer wants new players to make friends in the starting zone and proposes replacing zone chat with pings only. Using the four purposes of section 1, explain what this gains and what it costs.
4. In the spam scenario of section 2, what rate limit per poster would bring the channel back to 50 messages per minute, assuming the ten spammers post at the cap and the other 90 stay at 0.5?

<details>
<summary>Answers</summary>

1. `N = 30`, `M = 30 × 0.8 = 24` per minute. Coverage `12 / 24 = 50%`. Audience `600 × 0.5 = 300`, which equals `R / (s × r) = 12 / 0.04 = 300`. Yes, it is saturated (`L* = 300`).
2. Typed: `1.35 + 11 × 0.28 = 4.43 s`. Ping: `1.35 + 0.28 = 1.63 s`. The ping is about 2.7 times faster. The gap is smaller than in section 3 because the message is short, which is why short typed macros survive in games with pings.
3. It gains coordination speed and removes most of the abuse surface for new players. It loses sociability, the purpose the designer named, because pings cannot carry greetings, questions or jokes. A better design keeps a restricted, well-moderated chat for newcomers (week 11 looks at such channels) and adds pings for coordination.
4. The 90 polite posters send 45 per minute, so the ten spammers may send only 5 in total, or 0.5 each. The cap would be one message per two minutes, equal to the average rate. That is a strict cap, and it shows why caps alone are blunt. Splitting the channel or adding structured tools may be the better fix.

</details>

## Lab / assignment hook

[Lab 10, chat channel load and design](../labs/lab10.md). You simulate a channel message by message, check the section 2 formulas against the simulation, add spammers and a rate limit, and then write a channel design for a brief. The design memo counts toward the field observation assessment, because step 1 asks you to measure a real channel in a game you play.

## Sources

- Warcraft Wiki, "Trade chat" (accessed September 2026). Trade works only in capital cities and is linked across them on a realm; patch 9.2.7 (2022) added the Trade (Services) channel for services, leaving Trade for items and professions.
- Warcraft Wiki, "Barrens chat" (accessed September 2026). The Barrens as the level 10-20 route for most Horde characters before patch 7.3.5; the channel's reputation for off-topic chatter and trolling.
- League of Legends Wiki, "Ping" (accessed September 2026, current patches). Ping types; a limit of 2 to 7 pings per 5 seconds depending on Honor level, with a temporary lockout; per-type limits for some pings.
- Hearthstone Wiki (wiki.gg), "Emote" (accessed September 2026). The six voluntary emotes; squelch hides an opponent's emotes; emotes limited to one every few seconds.
- Blizzard, "Hearthstone Patch Notes 5.0.0.12574, Whispers of the Old Gods" (24 April 2016), as reproduced with its original battle.net URL on the Hearthstone Wiki page "Patch 5.0.0.12574": "The 'Sorry' emote has been replaced with a new 'Wow' emote."
- EVE University Wiki, "Wormhole space" (accessed September 2026). In wormhole space a pilot appears in Local only after speaking.
- Wikipedia, "Apex Legends" (accessed September 2026). Release February 4, 2019; the ping system and its critical reception; EA's 2021 US patent and its free availability to developers (EA's own pledge page was not reachable on 29 September 2026).
- Electronic Arts Inc., US Patent 11,097,189 B2, "Contextually aware communications system in video games", granted 24 August 2021 (Google Patents). One-button "smart ping" chosen from game state.
- Wikipedia, "Dark Souls (video game)" (accessed September 2026). 2011 release; messages left for other players using preset phrases.
- Wikipedia, "Toontown Online" (accessed September 2026). Launch June 2, 2003, closure September 19, 2013; SpeedChat, SpeedChat Plus with a word filter, True Friends codes, parental enablement for players under 13.
- Final Fantasy XIV Online Wiki (consolegameswiki), "Auto-Translate" (accessed September 2026). Preset phrases shown in each reader's language, in English, Japanese, French and German.
- Card, S., Moran, T. & Newell, A. (1983). *The Psychology of Human-Computer Interaction*. Erlbaum. Keystroke-level operator times as used in UX201 week 2.
- Nielsen, J. (2006). "Participation Inequality: Encouraging More Users to Contribute." Nielsen Norman Group.
- Taylor, T. L. (2006). *Play Between Worlds: Exploring Online Game Culture*. MIT Press.

## Interactive spec: examples/w10-chat-channel-load.html

**The one insight:** past a saturation point, a bigger channel gets louder but each message reaches the same number of readers, `R / (s × r)`. The left panel must look like growth and the right panel must show the flat line.

**Layout (mobile first):** two charts stacked on phones, side by side at 900px and wider. Below them, a live number panel and a scrolling chat preview strip.

**Left chart, "Channel rate":** x axis listeners `L` from 0 to 5,000 (linear). y axis messages per minute `M`, auto-scaled with a minimum of 0 to 100. Plot `M = s × L × r_eff` as a line, where `r_eff` includes spammers (below). Draw a horizontal dashed line at `R` labelled "reading budget". Mark the current `L` with a vertical cursor and a dot.

**Right chart, "Audience per message":** same x axis. y axis readers per message from 0 to `max(L)` of the axis range, clipped to 1,000 by default with an "auto" toggle. Plot `A = L × min(1, R / M)`. Mark `L* = R / (s × r_eff)` with a vertical dashed line labelled "saturation". When split is on, plot the per-channel curve (see below) as a second line and keep the unsplit one faded.

**Controls:**
- `L` listeners: slider 10 to 5,000, step 10, default 1,000.
- `s` share who post: slider 0.01 to 0.5, step 0.01, default 0.10.
- `r` posts per poster per minute: slider 0.1 to 4, step 0.1, default 0.5.
- `R` reading budget per minute: slider 2 to 60, step 1, default 20.
- `W` window lines: select 5, 8, 10, 15, 20, default 10.
- Spammers: number input 0 to 50, default 0, and spam rate slider 0.5 to 6 per minute, default 2. Spammers are part of the `N` posters; the rest post at `r`.
- Split: select 1, 2, 3, 4 channels, default 1. Listeners and posters are divided evenly across channels; each reader follows one channel.
- Rate cap: checkbox plus slider 0.1 to 4 per minute, default off. When on, every poster's rate is `min(rate, cap)`.

**Formulas (per channel when split = k):**
```
L_c = L / k
N = s × L_c
spam_c = spammers / k          (fractional allowed)
r_spam = min(spam rate, cap)   r_norm = min(r, cap)
M = (N − spam_c) × r_norm + spam_c × r_spam      (if N < spam_c, set spam_c = N)
T = 60 × W / M
c = min(1, R / M)
A = L_c × c
views per minute, polite poster = r_norm × A
views per minute, spammer = r_spam × A
```

**Number panel:** `N`, `M`, `T` (1 decimal), coverage (%, 1 decimal), `A` (integer), `L*` (integer), views per minute for a polite poster and for a spammer, and their ratio.

**Chat preview:** a strip of `W` lines that scrolls at the computed rate `M` (one generic line per message, e.g. "Player### : WTS item" with random neutral words; spammer lines use a distinct but accessible marker, not colour alone). Pause button. With `prefers-reduced-motion`, show a static frame and print "a line every X s".

**Test values (must match exactly):**
- `s = 0.1, r = 0.5, R = 20, W = 10`, no spam, split 1. `L = 50`: M 2.5, T 240, c 100%, A 50. `L = 400`: M 20, T 30, A 400. `L = 1,000`: M 50, T 12, c 40.0%, A 400. `L = 3,000`: M 150, T 4, c 13.3%, A 400. `L*` = 400.
- Spam: `L = 1,000`, 10 spammers at 4 per minute, others at 0.5: M 85, T 7.1, c 23.5%, A 235, polite 118 views/min, spammer 941 views/min, ratio 8. With spam rate 2: M 65, T 9.2, c 30.8%, A 308, polite 154, spammer 615.
- Rate cap 0.5 on, same spammers: M 50, back to the no-spam row.
- Split 3 with `s = 0.2, r = 1, R = 15, L = 300`: per channel `M = 20`, c 75%, A 75.

**Accessibility:** all sliders keyboard operable with visible labels and values; charts have text summaries updated live in an `aria-live="polite"` region ("Audience per message 400, saturated").
