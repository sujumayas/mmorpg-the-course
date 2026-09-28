# MMO305 · Week 01 — MMOs as Societies: Social Capital, Bridging and Bonding

**Why this matters:** Players say they stay in an MMO "for the people," and your retention numbers will agree with them. But "the people" is two different things. One is the small group that would notice if you quit. The other is the wide web of strangers and acquaintances that makes the world feel inhabited. Your guild rules, chat channels and membership caps decide how much of each your game produces, and a design that maximizes one can starve the other.

**You will be able to:**
- Define social capital and distinguish bonding from bridging ties, using Putnam's and Granovetter's terms.
- Compute the E-I index and the reachable share of player pairs for a small server network, and explain why the two numbers can disagree.
- Identify brokers (players whose departure splits a network) and predict how fragile a server's connections are.
- Critique a shipped game's group-membership rules (WoW, Final Fantasy XIV, Guild Wars 2, EVE Online) by the kind of ties they produce.

**Before class:** Constance Steinkuehler and Dmitri Williams, "Where Everybody Knows Your (Screen) Name: Online Games as 'Third Places'," *Journal of Computer-Mediated Communication* 11(4), 885-909 (2006). Read the whole paper; it is this course's first core reading. Mark Granovetter, "The Strength of Weak Ties," *American Journal of Sociology* 78(6), 1360-1380 (1973), the first four pages (the argument about bridges). Optional: Robert Putnam, *Bowling Alone* (2000), chapter 1.

**Prerequisites from earlier courses:** [GD102 week 1, systems thinking](../../GD102-systems-design-and-game-mechanics/lectures/w01-systems-thinking-parts-relationships-emergence.md), because a player network is a system of parts and relationships. [GD102 week 12, emergent behavior from simple rules](../../GD102-systems-design-and-game-mechanics/lectures/w12-emergent-behavior-from-simple-rules.md), because a society is what emerges when your rules meet thousands of players. [GS101 week 9, graphical MMOs](../../GS101-history-and-critical-study-of-games/lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md) and [GS101 week 10, World of Warcraft](../../GS101-history-and-critical-study-of-games/lectures/w10-world-of-warcraft-and-the-mass-market-mmo.md) for the games we discuss. [UX201 week 4, self-determination theory](../../UX201-game-ux-and-player-psychology/lectures/w04-self-determination-theory.md), for relatedness and why social ties feel rewarding at all. [MMO301 week 6, EVE Online](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w06-eve-online-the-single-shard-sandbox.md), for the corporations and alliances in section 3.

**Interactive:** [examples/w01-bridging-ties.html](../examples/w01-bridging-ties.html). Use it during section 2.

---

## 1. The puzzle in the membership rules

Open the social menu in three popular MMOs and count how many groups a player may join.

- In World of Warcraft a character belongs to one guild at a time. To join another, you leave the first.
- In Final Fantasy XIV a character belongs to one Free Company (the game's guild, up to 512 members). The same character can also sit in several ordinary linkshells (chat groups) and in up to eight cross-world linkshells of up to 64 members each, which span every world on a data center.
- In Guild Wars 2 an account can belong to up to six guilds. Each character chooses one of them to "represent," which decides whose guild bank and bonuses it uses.

These are deliberate choices, and they look like small UI decisions. They are not. Each rule decides how many ties can run *between* groups instead of *inside* them. By the end of this lecture you will be able to put a number on that difference and say what it does to a server.

### What "society" means here

A **society** in this course is a population whose members are connected by relationships that last longer than a single encounter, together with the shared rules and expectations that make those relationships predictable. An MMO server qualifies. Players meet the same names again, they learn who can be trusted, and they build institutions (guilds, alliances, markets, raid schedules) that outlive any single session.

The lens we use this week comes from sociology. It is called social capital.

## 2. Social capital, bonding and bridging

**Social capital** is the value a person or group gets from their relationships. Putnam's short version is networks plus the norms of reciprocity and trust that grow in them. Money is capital because you can spend it to get things done. Relationships are capital for the same reason. A guildmate who lends you gold, a stranger who answers your question in general chat, and a rival guild that honors a raid schedule are all returns on social capital.

Putnam separates two kinds, crediting the distinction to Ross Gittell and Avis Vidal.

- **Bonding social capital** comes from ties inside a group of similar people who know each other well. It gives emotional support, loans, favors and loyalty. Your static raid group is bonding capital.
- **Bridging social capital** comes from ties that cross between groups. It gives information, new contacts, exposure to other ways of playing, and access to resources your own group lacks. The player from another guild who tells you a crafting recipe is bridging capital.

Granovetter's 1973 paper explains why these differ in structure, and it names the key idea. A **tie** is a relationship between two people. A **strong tie** has a lot of time, emotional intensity, intimacy and mutual favors in it. A **weak tie** has little. Granovetter observed that if you have strong ties to two people, those two are very likely to know each other too. Strong ties close into tight clusters. So the ties that cross from one cluster to another, which he called **bridges**, are almost always weak ones. His famous finding was that people heard about new jobs more often through acquaintances than through close friends, because acquaintances sit in other clusters and hear different news.

In network terms we can say it more precisely.

- A **node** is a player. An **edge** is a tie between two players.
- A **group** is a set of nodes the designer or the players define (a guild, a Free Company, a corporation).
- An **internal tie** joins two members of the same group. An **external tie** joins members of different groups.
- A **bridge** in the strict sense is an edge whose removal disconnects part of the network. A **broker** is a node whose removal does the same. (Network scientists call it an articulation point.)

Bonding capital lives in internal ties. Bridging capital lives in external ties, and above all in bridges.

### What the research found in MMOs

Steinkuehler and Williams combined a year-long survey and interview study of Asheron's Call players with two years of participant observation in Lineage. Their conclusion, which frames this course, is that MMOs work as **third places**, the sociologist Ray Oldenburg's term (1989) for informal public spaces outside home and work such as cafés, pubs and barbershops. Third places are open without appointment, put everyone on equal footing, have regulars, and are built around conversation.

Their main claim about social capital is specific. MMOs are good at producing bridging capital. Players meet people of different ages, jobs and backgrounds as rough equals, and they hear views they would not meet at home. MMOs are much weaker at producing bonding capital. Deep, supportive friendships did form, mostly through long guild membership, and some moved offline, but they were the exception.

Keep that finding in mind. It says that the default MMO produces many weak ties across groups and few strong ones. Next week's reading will complicate it by measuring how few ties of either kind exist inside a typical World of Warcraft guild. To measure social capital in surveys, Williams (2006) built two short scales, one for bridging (for example, how much contact with online acquaintances makes you curious about other places and people) and one for bonding (for example, whether there is someone online you could turn to for help with a serious problem). You will use items like these in the field observation later in the course.

## 3. Worked example: three ties that make a server

### The hook

Here is the observable fact. Most players on a large server never meet most other players, and nearly all of their ties are inside their own guild. Yet the server still behaves like one society. News of a world boss spawn, a scam, or a price crash moves across it in minutes. How can a network that is 95% internal ties behave as one connected place?

### The model

Take a server of `n` players split into groups. Count two kinds of edges.

```
I  = number of internal ties (both ends in the same group)
E  = number of external ties (ends in different groups)

E-I index = (E − I) / (E + I)

reach = (pairs of players connected by some path) / (all pairs of players)
all pairs = n × (n − 1) / 2
```

- The **E-I index** (Krackhardt and Stern, 1988) runs from −1 (every tie is internal, pure bonding) to +1 (every tie is external, pure bridging). It measures the *mix* of ties.
- **Reach** is the share of player pairs that can reach each other through any chain of ties, however long. It measures whether the server is one society or several islands.
- **Average steps** is the mean length of the shortest path between connected pairs. It says how many hand-offs a piece of news needs.
- A **broker** is a player whose removal splits the network into more pieces than before (the articulation point of section 2). Removing a broker always lowers reach.

### Numbers you can check

Build a small server by hand. Four guilds, A, B, C and D, have six members each, so `n = 24`. Everyone in a guild knows everyone else in it. Each guild then has `6 × 5 / 2 = 15` internal ties, so `I = 60`. The server has `24 × 23 / 2 = 276` pairs of players.

Now add a few cross-guild ties in different patterns. Player A6 is the sixth member of guild A, and so on.

| Design | Internal ties | External ties | E-I index | Reach | Average steps | Brokers |
|---|---|---|---|---|---|---|
| Four closed guilds | 60 | 0 | −1.000 | 60 of 276 (21.7%) | 1.00 | — |
| One broker: A6 knows B1, C1 and D1 | 60 | 3 | −0.905 | 276 of 276 (100%) | 2.70 | 4 |
| A chain: A6–B1, B6–C1, C6–D1 | 60 | 3 | −0.905 | 276 of 276 (100%) | 3.35 | 6 |
| Every pair of guilds linked once (6 ties) | 60 | 6 | −0.818 | 276 of 276 (100%) | 2.30 | 0 |
| Three dual members: A6 joins B, B6 joins C, C6 joins D | 60 | 18 | −0.538 | 276 of 276 (100%) | 2.17 | 3 |

Check the first two rows yourself. With no external ties, only pairs inside a guild are connected. That is `4 × 15 = 60` pairs, and `60 / 276 = 21.7%`. Add three external ties and the E-I index moves from −1 to `(3 − 60) / (3 + 60) = −57 / 63 = −0.905`. Almost nothing changed in the mix. But now every pair can reach every other pair, and reach jumps from 21.7% to 100%.

That is the lesson of this example. **Three ties out of 63, under 5% of the network, turn four islands into one society.** The E-I index barely notices. Reach notices everything.

The "dual members" row shows what multiple membership does. When A6 joins guild B as a second guild, A6 gains a tie to all six B members at once. Three players doing this add 18 external ties. Membership rules are the most powerful bridging lever you have, because one decision by one player creates many cross-group ties.

### The visual

Open the interactive. The left view draws the 24 players as four clusters, with internal ties in one color and external ties in another. The right view shows two bars side by side, the share of ties that are external and the share of pairs that can reach each other. Start with four closed guilds and add one external tie at a time. The left bar creeps up by a few percent. The right bar leaps. Then click any player to "log them out for good" and watch which removals collapse reach.

### Why the few ties matter so much

A path needs only one crossing point between two clusters. Once one A player knows one B player, all 6 A members can reach all 6 B members, which is 36 new connected pairs from a single tie. That is why Granovetter cared about bridges. The first tie between two groups connects whole groups. The second tie between the same two groups connects nobody new. It shortens paths and adds backup, but it adds zero reach.

Watts and Strogatz (1998) showed the same effect at scale. In a network of tight local clusters, a small number of random long-range ties drops the average path length sharply while leaving the clusters intact. They called this a **small world**. A healthy MMO server is a small world. Its guilds do the bonding, and a thin layer of cross-guild ties makes it one place.

### Brokers and fragility

Look at the "one broker" row again. Reach is 100%, but it depends on one player. If A6 quits, reach falls back to 55 of the 253 pairs that remain, 21.7%, the same as four closed guilds. The server did not lose 1 player out of 24. It lost its connection.

The chain is less fragile but still has six brokers. Losing B6 or C1, in the middle of the chain, cuts reach to `121 / 253 = 47.8%`, because it splits the server into two halves of 11 and 12 players.

The "every pair of guilds linked once" design has no broker at all. Any single player can leave and every remaining pair can still reach each other. It uses six external ties instead of three. **Redundant bridges cost you ties but buy you resilience.** In live games this matters, because the players who connect groups are often the most active and social, and active players churn too. [Week 4](w04-guilds-formation-lifecycle-leadership.md) returns to this when guild leaders burn out.

### Cross-game recognition

Rewrite each game's rules as answers to the model's question. How many external ties can one player create, and which layer of the game creates them?

**World of Warcraft (current and all eras).** One guild per character means a player's guild ties are all internal. External ties come from other layers, such as friends lists, pick-up groups, trade and cross-guild raid groups. The guild layer contributes nothing to the E-I index except internal ties. A player with several characters can be in several guilds, one per character, and those players become the dual members of our table. So the rule does not forbid bridging. It pushes it into alts and informal channels the designer does not see.

**Final Fantasy XIV (patch 4.3 onward, current era).** One Free Company, plus several linkshells, plus up to eight cross-world linkshells of up to 64 members. This is our "dual members" design built into the UI. The Free Company is the bonding layer. Each linkshell a player joins adds ties to people in other Free Companies and, for cross-world linkshells, on other worlds. A player in three linkshells is a potential broker between four groups.

**Guild Wars 2 (current era).** Up to six guilds per account, one represented per character, and guild membership is not limited to one world. A player can keep a small bonding guild, a large event guild and a guild for a single game mode at once. In model terms, GW2 raises the cap on memberships per player from 1 to 6, which raises the ceiling on external ties per player about sixfold.

**EVE Online (current era).** The layers stack. Players join a corporation, and corporations join alliances, which are groups of corporations that can do things one corporation cannot, such as holding sovereignty over space. A corporation can belong to only one alliance. The alliance is a formal bridging structure between bonding groups. It turns what would be informal ties between corporations into an institution with a leader (the executor corporation) and costs.

Four games, one idea. Each designer decided how many groups a player may bond with, and how many bridges the rules allow between them. When you meet a new game, ask the model's two questions. How many memberships does a player get, and which layer of the game creates cross-group ties?

### Eyes-open design judgment

- **Bridging is cheap to create and has outsized effects.** A few cross-group ties connect a whole server. Features that create them (cross-guild events, open-world bosses where anyone can help, multi-guild membership, shared chat channels) give a lot of reach per unit of design effort.
- **Bonding is expensive and slow.** Strong ties need repeated time together. You cannot create them with a menu. You can only create conditions where the same people meet again and depend on each other. Weeks 2 and 3 measure how rarely this happens by default.
- **Multiple membership has a cost.** When a player can be in six guilds, each guild gets a smaller share of their attention and loyalty. Guild leaders in GW2 often ask members to "represent" during guild events for this reason. A single-membership rule gives stronger commitment to one group and pushes bridging elsewhere.
- **Watch for brokers.** If your server's cross-group connections depend on a handful of people (market traders, alliance diplomats, the one officer who runs cross-guild raids), your society is fragile. Redundant bridges are the fix.
- **Pure bonding has a dark side.** A network of closed clusters with no bridges breeds cliques, rumors that nobody can check, and hostility toward outsiders. Pure bridging has one too. A world of acquaintances with no one to turn to is a lonely place and an easy one to quit.

## 4. What each kind of capital does for a game

The two kinds of capital pay off in different ways, and it helps to name them.

**Bonding capital keeps players.** A player whose five closest friends play on Tuesday nights has a reason to log in that has nothing to do with your content calendar. Next week's reading reports that guilded WoW players played more hours and grouped more often than unguilded ones. Bonding ties are also where players get help with hard things, such as a raid mechanic, a loan, or a bad week in real life.

**Bridging capital moves information and makes the world feel alive.** Market prices, strategies, rumors and new-player help all travel along weak ties. A new player with no guild still benefits from a world full of bridging ties, because someone in general chat answers questions. Bridging ties are also how players find a guild in the first place.

**The two depend on each other.** Guilds recruit through bridging ties. Bridging ties are safer when there are bonding groups behind them that vouch for their members and can punish scammers. Week 6 (trust and reputation) builds on this.

A useful design check is to list your game's social features in two columns, "creates internal ties" and "creates external ties." Most MMOs have a long first column (guild ranks, guild banks, guild halls, guild raids) and a short second one. If the second column is short, your server is likely several societies sharing one map.

## 5. Designing for both

Here are the levers designers have, grouped by which capital they build.

**Levers for bonding.**
- Content sized for a stable small group that repeats weekly (dungeon teams, raid statics).
- Group-owned resources and places (guild banks, halls, housing), which create shared stakes.
- Rewards for playing with the *same* people again, not just with anyone.
- Memory features, such as recently-played-with lists and notes on other players, that help strangers become acquaintances.

**Levers for bridging.**
- Multiple membership (FFXIV linkshells, GW2 guilds).
- Open public events where anyone nearby can join and everyone is rewarded, so strangers help each other without negotiating a group.
- Server-wide or cross-server channels for trade, help and looking-for-group.
- Formal alliances between groups (EVE alliances).
- Economies where players need goods from other groups (MMO304 covers this).

**Levers that hurt one to help the other.** Cross-server matchmaking gives bridging reach, since you meet more people, but it almost removes repeat encounters, so no bonding follows. Week 3 puts numbers on this. A strict one-guild rule strengthens guild loyalty but pushes bridging into informal channels you do not control.

## In-class activity (25 minutes)

In groups of three. Materials: the table from section 3, the interactive on one laptop, and paper.

1. (8 min) Your team is designing a new MMO for a server of about 2,000 active players. Write down your membership rules in one line each. How many guilds per character? Are there chat groups outside guilds? Is there an alliance layer?
2. (7 min) Draw a toy version of your server with 4 groups of 6 on paper. Using your rules, add the external ties you would expect in a typical week. Compute the E-I index and the reach. Use the interactive to check.
3. (5 min) Find every broker in your drawing. Say who they are in your game's terms ("the crafter who sells to all four guilds").
4. (5 min) Propose one feature that adds a redundant bridge without weakening the guilds. Swap with another group and find one way the other group's feature could backfire.

Expected output: your rules, a drawing with E-I and reach written on it, your brokers named, and one feature with its risk.

## Common misconceptions

- **"More social features means more social capital."** Features that only add internal ties (more guild ranks, more guild perks) make the E-I index more negative and do nothing for reach. Count which kind of tie a feature creates.
- **"Bridging ties are the weak, less valuable ones."** They are weak per tie and powerful per network. Three weak ties in section 3 connected 216 new pairs. Granovetter's title is not ironic.
- **"The E-I index tells you whether the server is connected."** It measures the mix of ties, not the structure. A server at −0.905 can be fully connected or split into islands, depending on where the few external ties sit.
- **"If reach is 100%, the network is healthy."** Reach can hang on one broker. Always ask what happens when your most connected player quits.

## Check yourself

1. A server has five guilds of 8 members, each fully connected inside. How many internal ties are there? What is the reach with no external ties?
2. Add four external ties to the server in question 1, arranged as a chain linking the five guilds. What is the new E-I index? What is the new reach?
3. In the chain from question 2, which player removal hurts reach the most, and roughly what share of the remaining pairs can still reach each other?
4. A designer proposes letting each character join up to three guilds. Using the dual-members row of section 3, explain what happens to the E-I index and to the number of brokers. Name one risk for guild leaders.
5. Steinkuehler and Williams say MMOs produce more bridging than bonding capital. Name one design feature that would move a game toward more bonding, and say which network number you would expect to change.

<details>
<summary>Answers</summary>

1. Each guild has `8 × 7 / 2 = 28` internal ties, so `I = 5 × 28 = 140`. The server has `40 × 39 / 2 = 780` pairs. Connected pairs are the 140 internal ones, so reach is `140 / 780 = 17.9%`.
2. `E-I = (4 − 140) / (4 + 140) = −136 / 144 = −0.944`. The chain connects every guild, so reach is 100%.
3. One of the two link players in the middle guild, C. Removing the player who holds the tie to guild B leaves A and B on one side (16 players) and the 7 other C members plus D and E on the other (23 players). The remaining 39 players have `39 × 38 / 2 = 741` pairs, of which `16 × 15 / 2 + 23 × 22 / 2 = 120 + 253 = 373` stay connected, 50.3%. Removing a link player in guild B or D is slightly less damaging (51.4%), and a link player in an end guild less still.
4. Each dual member adds ties to every member of their second group, so external ties rise fast and the E-I index moves toward zero. With more players holding memberships in several groups, there are many parallel bridges, so the number of brokers usually falls. The risk for leaders is divided attention. A member of three guilds may not turn up for any of them.
5. For example, a weekly group activity that gives a bonus for repeating it with the same people, or a guild-owned house that members build together. You would expect more internal ties, a more negative E-I index, and no change in reach. On a survey, bonding-scale scores should rise.

</details>

## Lab / assignment hook

[Lab 01, mapping bridging and bonding on a server](../labs/lab01.md). You will load a 40-player server edge list, compute the E-I index, reach and brokers, then redesign the membership rules to remove every broker while keeping the E-I index below −0.7. Deliverable: the computations and a 300-word design memo.

## Sources

- Steinkuehler, C. A. & Williams, D. (2006). "Where Everybody Knows Your (Screen) Name: Online Games as 'Third Places'." *Journal of Computer-Mediated Communication* 11(4), 885-909. https://doi.org/10.1111/j.1083-6101.2006.00300.x. Games studied (Lineage I and II, Asheron's Call I and II), methods (a media-effects study of Asheron's Call players combined with two years of participant observation in Lineage; the abstract confirms the two strands, sample sizes are in the full paper) and the conclusion that MMOs produce mostly bridging and rarely bonding capital.
- Putnam, R. D. (2000). *Bowling Alone: The Collapse and Revival of American Community*. Simon & Schuster. Definition of social capital and the bonding and bridging distinction, which Putnam credits to Ross Gittell and Avis Vidal (as summarized in Wikipedia, "Social capital").
- Granovetter, M. S. (1973). "The Strength of Weak Ties." *American Journal of Sociology* 78(6), 1360-1380. Tie strength, closure among strong ties, bridges as weak ties, and the job-search finding.
- Oldenburg, R. (1989). *The Great Good Place*. Paragon House. The third-place concept and its characteristics (as summarized in Wikipedia, "Third place").
- Williams, D. (2006). "On and Off the 'Net: Scales for Social Capital in an Online Era." *Journal of Computer-Mediated Communication* 11(2), 593-628. https://doi.org/10.1111/j.1083-6101.2006.00029.x. Bridging and bonding survey scales.
- Krackhardt, D. & Stern, R. N. (1988). "Informal Networks and Organizational Crises: An Experimental Simulation." *Social Psychology Quarterly* 51(2), 123-140. The E-I index.
- Watts, D. J. & Strogatz, S. H. (1998). "Collective Dynamics of 'Small-World' Networks." *Nature* 393, 440-442. Short paths from a few long-range ties in clustered networks.
- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2006). "'Alone Together?' Exploring the Social Dynamics of Massively Multiplayer Online Games." *Proceedings of CHI 2006*, ACM, 407-416. https://doi.org/10.1145/1124772.1124834. Guilded WoW characters played more and grouped more (World of Warcraft, data from June 2005 onward).
- Warcraft Wiki, "Guild" (FAQ section, current era). Changing guilds means leaving the current one and joining another. https://warcraft.wiki.gg/wiki/Guild
- Final Fantasy XIV Online Wiki (consolegameswiki), "Free Company" and "Linkshell" (current era, patch 7.x). One Free Company at a time, 512-member limit; multiple linkshells regardless of Free Company; cross-world linkshells added in patch 4.3, up to 64 members, up to 8 per player, same data center. https://ffxiv.consolegameswiki.com/wiki/Linkshell
- Guild Wars 2 Wiki, "Guild" (current era). Membership at account level in up to 6 guilds; representation chosen per character; membership not limited to one world. https://wiki.guildwars2.com/wiki/Guild
- EVE University Wiki, "Alliances" (current era). An alliance is a group of corporations; alliances can hold sovereignty; a corporation can apply to only one alliance at a time; executor corporation. https://wiki.eveuniversity.org/Alliances
- The network numbers in section 3 are computed for this lecture from the invented four-guild server and can be checked by hand or with the lab's script.

## Interactive spec: examples/w01-bridging-ties.html

**The one insight.** A handful of cross-group ties changes the tie mix by a few percent but connects the whole server. The E-I bar barely moves while the reach bar jumps from about 22% to 100%. Removing one broker can undo it all.

**Model.** Four groups (A, B, C, D) of `s` members each (slider `s` from 4 to 10, default 6). Every group is a complete graph, so `I = 4 × s(s − 1)/2`. External ties are added by the student. All metrics are recomputed on every change.

```
n = 4s          pairs = n(n − 1)/2
E-I = (E − I) / (E + I)
reach = connected pairs / pairs        (BFS from every node)
avg steps = mean shortest-path length over connected pairs
broker = articulation point: a node whose removal increases the number of connected components
                (test: count components with and without the node; do NOT use "lowers the
                connected-pair share", which flags ordinary members of partly connected clusters)
```

**Layout.** Two linked views, side by side on desktop and stacked on mobile.

- **Left, "Who knows whom."** The four groups drawn as four circles of nodes in the four quadrants. Internal ties thin and neutral; external ties thick in the accent color. Nodes labelled A1 to D`s`. Brokers get a ring marker (and the text "broker" in the node's accessible label).
- **Right, "What the server can do."** Two horizontal bars on the same 0-100% scale: "external share of ties `E / (E + I)`" and "reach." Under them, a readout table with I, E, E-I index (3 decimals), reach as "x of y (z%)", average steps (2 decimals), number of brokers.

**Controls.**
- Preset buttons: "Closed guilds", "One broker", "Chain", "Every pair once", "Dual members". Presets for `s = 6` must match the lecture table exactly.
- Add a tie: select two nodes (click or keyboard: Tab to a node, Enter to select, then the second node). Selecting an existing tie removes it.
- "Log out for good" mode toggle: in this mode, clicking a node removes it and its ties; the readout shows reach among remaining nodes. A "restore all" button undoes removals.
- Slider `s` (4 to 10). Changing `s` keeps the preset pattern (a preset is defined by which member index links, for example "last member of A to first of B").

**Preset definitions (for `s = 6`, members numbered 1 to 6).**
- One broker: A6–B1, A6–C1, A6–D1.
- Chain: A6–B1, B6–C1, C6–D1.
- Every pair once: A6–B1, B6–C1, C6–D1, D6–A1, A5–C5, B5–D5.
- Dual members: A6 tied to all of B1-B6, B6 tied to all of C1-C6, C6 tied to all of D1-D6 (B6–C6 counts once).

**Test values (`s = 6`, must match).**
- Closed guilds: I 60, E 0, E-I −1.000, reach 60 of 276 (21.7%), avg steps 1.00, brokers 0.
- One broker: E 3, E-I −0.905, reach 276 of 276 (100.0%), avg steps 2.70, brokers 4. Remove A6: reach 55 of 253 (21.7%).
- Chain: E 3, E-I −0.905, reach 100.0%, avg steps 3.35, brokers 6. Remove B6: 121 of 253 (47.8%). Remove A6: 163 of 253 (64.4%).
- Every pair once: E 6, E-I −0.818, reach 100.0%, avg steps 2.30, brokers 0.
- Dual members: E 18, E-I −0.538, reach 100.0%, avg steps 2.17, brokers 3 (A6, B6, C6).

**Edge cases.** With `E + I = 0` after removals, show E-I as "n/a". Average steps over zero connected pairs shows "n/a". Ties from a node to itself are ignored.

**Accessibility.** Internal and external ties differ by thickness and dash pattern as well as color. Every node is focusable with a label such as "A6, guild A, 5 internal ties, 1 external tie, broker." Readout updates in an `aria-live="polite"` region. Respect `prefers-reduced-motion` (no animated layout) and `prefers-color-scheme`.
