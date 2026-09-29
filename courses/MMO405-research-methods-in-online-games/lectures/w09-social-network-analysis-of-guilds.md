# MMO405 · Week 09 — Social Network Analysis of Guilds

**Why this matters:** Every guild has two structures. One is the rank chart the game shows you, with a guild master, officers and members. The other is who actually plays with whom, and it decides who holds the guild together, who can bring a raid to a stop, and whose departure will empty the roster. Social network analysis measures the second structure. As a researcher you also have to show that you built the network from the right data, because every number depends on that choice.

**You will be able to:**
- Build a guild network from co-play records, stating the boundary, the tie definition, the weight and the threshold.
- Compute degree, strength, betweenness and eigenvector centrality for a small guild by hand and in code, and say what question each one answers.
- Show how a tie threshold or time window changes who looks central, and report that sensitivity in a methods section.
- Critique a network study of an online game for how its ties were defined, whom it missed, and the ethics of mapping people who never consented.

**Before class:** Ducheneaut, Yee, Nickell and Moore, "The Life and Death of Online Gaming Communities" (CHI 2007), the sections on data collection and on the variables used to model guild survival (pp. 839-843). Williams et al., "From Tree House to Barracks" (2006), the section "The Roles of Central Players" and the methodological caveat that follows it (pp. 354-356). Freeman, "Centrality in Social Networks: Conceptual Clarification" (1978), pp. 215-221 on degree and betweenness.

**Prerequisites from earlier courses:** [MMO305 week 1, social capital](../../MMO305-social-systems-and-online-behaviour/lectures/w01-mmos-as-societies-social-capital.md) (nodes, ties, reach and brokers). [MMO305 week 2, playing alone together](../../MMO305-social-systems-and-online-behaviour/lectures/w02-playing-alone-together.md) (co-presence, co-location and co-activity layers, density, k-cores). [MMO305 week 4, guilds](../../MMO305-social-systems-and-online-behaviour/lectures/w04-guilds-formation-lifecycle-leadership.md) (what leaders do, rank permissions, succession). [MMO405 week 8, mixed methods](w08-mixed-methods.md) (connecting a network measure to interviews). [MMO405 week 3, telemetry as research data](w03-telemetry-as-research-data.md) (found data and the unit problem).

**Interactive:** [Guild centrality explorer](../examples/w09-guild-centrality.html). Keep it open during section 2.

---

## 1. Two structures in one guild

A guild's formal structure is written into the game. In World of Warcraft, the guild leader sets up to ten ranks, names them, and decides what each rank may do, such as inviting, removing, promoting, speaking in officer chat or withdrawing from the guild bank. MMO305 week 4 showed how those permissions spread a leader's work, or fail to. The rank list is an organisation chart.

The informal structure is not written anywhere. It is who groups with whom, who answers questions in guild chat, who organises the Tuesday dungeon run, and whom people follow when there is an argument. Organisation researchers found long ago that the chart and the working network differ. David Krackhardt and Jeffrey Hanson's 1993 *Harvard Business Review* article on informal networks made the point for managers. Its argument is that informal networks cut through formal reporting lines, and that mapping networks such as who asks whom for advice shows where work actually gets done.

**Social network analysis (SNA)** is the set of methods for measuring that informal structure. A **network** (or graph) has **nodes**, here guild members, and **ties** (or edges) between pairs of nodes. MMO305 weeks 1 and 2 used networks to measure whether a server is one society (reach), how tightly a guild plays together (density) and where its core is (k-cores). Those are properties of the whole network. This week is about **centrality**, a property of each node that says how important its position is. The research question behind the course's signature example is whether centrality finds the people who actually run a guild, whatever their rank.

## 2. Worked example: centrality finds the real leader

### The hook

In January 2006, a team from the University of Illinois and the Palo Alto Research Center ran a census of three World of Warcraft servers. For every guild they built a network in which two members were tied by the time they spent grouped together. They used each player's centrality in that network to choose whom to interview, expecting the most central players to be the social hubs of their guilds. Then they conducted 48 interviews.

The interviews told a different story. Few of the high-centrality players turned out to be their guild's official leader. Many led smaller units, such as the raid or the regular dungeon group, and one described officers' work as helping whoever was leading the raid keep everyone working together. Some were former leaders who had stepped down and stayed on as advisors. And centrality did not always mean sociability, because raiding groups spend their time together focused on the fight.

So the network found someone, and it was not who the rank chart named. This section builds a small guild where you can see exactly why, and shows which measure picks out whom.

### The model

A guild network is a graph `G` with `n` members. Following Ducheneaut and colleagues' 2007 method, two members are tied when they were seen grouped in the same zone (outside cities), and the tie's weight is the time they spent together that month. Four centrality measures answer four different questions.

```
Degree centrality      C_D(v) = deg(v) / (n − 1)
Strength               s(v)   = Σ w(v, u) over v's ties
Betweenness            C_B(v) = Σ over pairs {s, t} not containing v of σ_st(v) / σ_st
   normalised          C_B(v) / ((n − 1)(n − 2) / 2)
Eigenvector            x(v)  ∝  Σ x(u) over v's neighbours u
```

- `deg(v)` is the number of members `v` is tied to. **Degree centrality** is the share of the guild `v` plays with. Ducheneaut and colleagues used exactly this measure and averaged it over each guild.
- `w(v, u)` is a tie's weight in hours. **Strength** is how much time `v` spends in groups with guildmates.
- `σ_st` is the number of shortest paths between members `s` and `t`, and `σ_st(v)` is how many of them pass through `v`. **Betweenness** (Freeman 1977) is how often `v` sits on the shortest route between two other members. It measures brokerage, the position of someone who joins groups that would otherwise not be connected. Dividing by the number of pairs not containing `v` scales it to 0-1.
- **Eigenvector centrality** gives a member a high score for being tied to members who themselves have high scores. It is the best-known member of the family of measures Bonacich (1987) described. You compute it by starting everyone at 1 and repeatedly replacing each score with the sum of the neighbours' scores, rescaling each round.

Degree, betweenness and eigenvector centrality here use the unweighted ties. Strength uses the weights. Section 3 explains why that is a choice you must report.

### Numbers you can check

Here is an invented guild of ten members and one month of co-play. Rowan is the guild master. Kest and Mira are officers. Everyone else has the rank "Member". The raiders (Tamsin, Kest, Bo, Ria, Juno) play mostly together, a group of casual players (Mira, Pell, Nox, Ash) plays mostly together, and Rowan logs in rarely.

| Tie | Hours | Tie | Hours |
|---|---|---|---|
| Tamsin-Kest | 20 | Mira-Pell | 9 |
| Tamsin-Bo | 18 | Mira-Nox | 7 |
| Tamsin-Ria | 15 | Pell-Nox | 6 |
| Tamsin-Juno | 12 | Nox-Ash | 5 |
| Kest-Bo | 10 | Pell-Ash | 3 |
| Bo-Ria | 8 | Tamsin-Mira | 5 |
| Ria-Juno | 6 | Tamsin-Pell | 4 |
| Rowan-Kest | 3 | Rowan-Mira | 2 |

The code below computes the four measures. It uses only the standard library and runs as shown with `.venv/bin/python`. Betweenness is computed pair by pair, straight from the definition. For each pair `(s, t)`, a member `v` lies on a shortest path when `dist(s, v) + dist(v, t) = dist(s, t)`, and the number of such paths through `v` is `σ_sv × σ_vt`.

```python
from collections import deque
from itertools import combinations

# Hours two guild members spent grouped in the same non-city zone, one month.
TIES = [("Tamsin", "Kest", 20), ("Tamsin", "Bo", 18), ("Tamsin", "Ria", 15),
        ("Tamsin", "Juno", 12), ("Kest", "Bo", 10), ("Bo", "Ria", 8),
        ("Ria", "Juno", 6), ("Tamsin", "Mira", 5), ("Tamsin", "Pell", 4),
        ("Mira", "Pell", 9), ("Mira", "Nox", 7), ("Pell", "Nox", 6),
        ("Nox", "Ash", 5), ("Pell", "Ash", 3), ("Rowan", "Kest", 3),
        ("Rowan", "Mira", 2)]
RANK = {"Rowan": "Guild Master", "Kest": "Officer", "Mira": "Officer"}

def graph(ties, min_hours=0):
    adj = {p: set() for a, b, _ in ties for p in (a, b)}
    for a, b, h in ties:
        if h >= min_hours:
            adj[a].add(b)
            adj[b].add(a)
    return adj

def bfs(adj, s):
    """Distance from s and number of shortest paths from s to every reachable node."""
    dist, paths, q = {s: 0}, {s: 1}, deque([s])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in dist:
                dist[w], paths[w] = dist[v] + 1, 0
                q.append(w)
            if dist[w] == dist[v] + 1:
                paths[w] += paths[v]
    return dist, paths

def betweenness(adj):
    sp = {v: bfs(adj, v) for v in adj}
    score = dict.fromkeys(adj, 0.0)
    for s, t in combinations(adj, 2):
        ds, ps = sp[s]
        if t not in ds:
            continue
        dt, pt = sp[t]
        for v in adj:
            if v not in (s, t) and v in ds and v in dt and ds[v] + dt[v] == ds[t]:
                score[v] += ps[v] * pt[v] / ps[t]
    return score

def eigenvector(adj, rounds=200):
    x = dict.fromkeys(adj, 1.0)
    for _ in range(rounds):
        y = {v: x[v] + sum(x[u] for u in adj[v]) for v in adj}
        top = max(y.values())
        x = {v: y[v] / top for v in adj}
    return x

adj = graph(TIES)
n = len(adj)
btw, eig = betweenness(adj), eigenvector(adj)
print(f"{'member':7} {'rank':12} {'degree':>6} {'hours':>5} {'betw':>6} {'eig':>5}")
for v in sorted(adj, key=lambda v: -btw[v]):
    hours = sum(h for a, b, h in TIES if v in (a, b))
    print(f"{v:7} {RANK.get(v, 'Member'):12} {len(adj[v]) / (n - 1):6.2f} {hours:5}"
          f" {btw[v] / ((n - 1) * (n - 2) / 2):6.3f} {eig[v]:5.2f}")
```

```
member  rank         degree hours   betw   eig
Tamsin  Member         0.67    74  0.523  1.00
Pell    Member         0.44    22  0.231  0.71
Mira    Officer        0.44    23  0.194  0.72
Kest    Officer        0.33    33  0.074  0.54
Nox     Member         0.33    18  0.028  0.50
Bo      Member         0.33    36  0.023  0.59
Rowan   Guild Master   0.22     5  0.023  0.35
Ria     Member         0.33    29  0.014  0.57
Juno    Member         0.22    18  0.000  0.44
Ash     Member         0.22     8  0.000  0.34
```

The eigenvector loop adds each member's own score (`x[v] + ...`) before rescaling. On a connected guild this gives the same ranking as the plain definition and stops the scores from flipping back and forth between rounds.

Check three rows by hand.

- **Tamsin's degree.** Tamsin is tied to Kest, Bo, Ria, Juno, Mira and Pell, which is 6 of the 9 other members, so `6/9 = 0.67`. Her strength is `20 + 18 + 15 + 12 + 5 + 4 = 74` hours.
- **Rowan's betweenness.** Rowan's two neighbours, Kest and Mira, are not tied to each other. Between Kest and Mira there are two shortest paths of length 2, through Tamsin and through Rowan, so Rowan gets `1/2`. Between Kest and Nox there are three paths of length 3 (via Tamsin and Mira, via Tamsin and Pell, via Rowan and Mira), so Rowan gets `1/3`. No other pair has a shortest path through Rowan. His total is `0.833`, and `0.833 / 36 = 0.023`.
- **Juno's betweenness.** Juno's two neighbours, Tamsin and Ria, are tied to each other, so no shortest path ever needs to pass through Juno. It is 0.

Tamsin's raw betweenness is 18.83 of a possible 36, and 15.17 of it comes from the 16 pairs that join a raider to a casual player. She is the main route between the guild's two halves. She tops every measure, and her rank is "Member".

Look at what each measure says about the officers and the guild master. Kest has the second-highest strength (33 hours), because he raids every week, but he sits inside the raid group and brokers almost nothing. Mira ranks high on degree and eigenvector as the centre of the casual group, and third on betweenness. Rowan, the guild master, is near the bottom on every measure. That does not prove Rowan is unimportant. It proves that whatever Rowan does is not visible in co-play, and section 3 returns to that.

### A visual you can move

Open the interactive. The left panel draws the guild with each member's rank shown as a badge, and node size set by the centrality you choose from a menu (degree, strength, betweenness or eigenvector). Tie thickness shows hours. The right panel is a ranked bar chart of the same measure with the rank badges beside the names, so you can see the rank chart and the centrality ranking side by side. Switch between measures and watch the order change. Then drag the "minimum hours for a tie" slider from 0 up to 10. At 5 hours Rowan drops out of the network entirely, and Mira's betweenness jumps from 0.194 to 0.417, because the 4-hour tie between Tamsin and Pell is gone and Mira becomes the only way into the casual group.

| Minimum hours | Tamsin betw. | Mira betw. | Pell betw. | Rowan |
|---|---|---|---|---|
| 0 (all ties) | 0.523 | 0.194 | 0.231 | 0.023, degree 0.22 |
| 5 | 0.500 | 0.417 | 0.000 | isolated, degree 0 |

Nothing about the guild changed between the two rows. Only the researcher's threshold did.

### Cross-game recognition

Rewrite each study as three answers. What is a tie? Which centrality was used? What did it find that rank or common sense did not?

**World of Warcraft, guild survival (Ducheneaut et al., CHI 2007, data from June 2005 onward).** Ties: guildmates grouped in the same non-city zone, weighted by cumulative time together. Measures: each member's degree centrality averaged over the guild, and guild density, along with size and the largest subgroup. Finding: better-connected guilds survived more often. The authors proposed a "Social Dashboard" that would show guild leaders and community managers such metrics, since the game's own rank tools showed none of this structure.

**World of Warcraft, interviews (Williams et al., Tree House, January to March 2006).** Ties: time spent grouped with guildmates. Measure: centrality, used to stratify the interview sample. Finding: centrality did not imply authority or sociability, as the hook described. It found team leaders, advisors and self-described "networkers", people whose influence the rank chart does not record.

**Pardus (Szell, Lambiotte and Thurner, *PNAS* 2010, first 445 days of the Artemis universe).** Pardus is a science-fiction MMO online since 2004. The team mapped 18,819 players across six networks built from one-to-one interactions. Three were positive (friendship, private messages and trades) and three negative (enmity, attacks and bounties). Finding: individuals tend to play different roles in different networks. Someone central in one network can be peripheral in another. So "who is central?" has no answer until you name the tie.

**Companies (Krackhardt and Hanson, 1993).** Ties: relationships such as who goes to whom for advice. Argument: informal networks cut through the formal reporting lines on the organisation chart, so the chart is a poor guide to who holds a company together. It is the Tree House lesson, stated for offices.

Four settings, one idea. Rank is assigned and centrality is observed, and centrality always belongs to one kind of tie. When you read "the most central player", ask which network and which measure.

### Eyes-open design judgment

- **Pick the measure from the question.** Who spends the most time with the guild? Use strength. Who connects the guild's subgroups, and whose departure would split them? Use betweenness, and connect it to MMO305 week 1's brokers. Who is tied to the other well-connected members? Use eigenvector. Reporting all four and circling the biggest number is not analysis.
- **Rank tells you who holds permissions, and centrality tells you who is positioned in play.** A guild master who handles recruitment in Discord and the bank in the interface may be essential and still peripheral in co-play. If your research question is "who leads?", co-play centrality is evidence, not an answer. Interview or observe the leader's other work (week 8's connecting design).
- **Brokers are fragile points.** Tamsin's betweenness says that if she leaves, the raiders and the casual players lose their main connection. A designer reading this would ask what features create redundant bridges, such as guild events open to all levels. A guild leader reading it might put a second person in touch with both groups.
- **Do not hand centrality scores to guild leaders without thinking.** A list of "peripheral members" can become a list of people to remove. Section 5 comes back to this.

### Check yourself (worked example)

1. Add a 6-hour tie between Kest and Mira. Without code, say whose betweenness falls and why.
2. A member has degree centrality 0.9 and betweenness 0. Describe the network around them.
3. A researcher reports that "the guild master has the lowest eigenvector centrality, so the guild master has no influence." Give two reasons the conclusion does not follow.

<details>
<summary>Answers</summary>

1. Rowan's falls to 0, because Kest and Mira are now tied directly and nothing needs to route through him. Tamsin's also falls, since the Kest-Mira pair and pairs such as Kest-Nox and Bo-Mira now have shortest paths through the new tie. Kest and Mira gain betweenness, because they now carry some raider-to-casual traffic.
2. They are tied to almost everyone, and all of their neighbours are tied to each other directly, so no shortest path needs them. They are in the middle of a dense, fully connected group, for example a tight raid team where everyone plays with everyone.
3. The network measures co-play only. The guild master's influence may run through permissions, voice chat, Discord or the bank, none of which create ties here. Eigenvector centrality also depends on the threshold and time window. A guild master who was away that month, or who plays briefly with many people, can score low.

</details>

## 3. Building the network is the method

Every number in section 2 depends on four decisions made before any computation. A methods section must state all four, and a good one tests how sensitive the results are to them.

### Boundary: who counts as a node

The simplest boundary is the guild roster. Rosters include characters who have not logged in for months, and players' alts. Ducheneaut and colleagues noted that a player's alts usually sit in the same guild. The Tree House team found that alts had been counted in their census as if they were separate players, which distorted their cut-points for low centrality. Decide whether a node is a character or a player. If you can, merge alts, and state a minimum activity level for inclusion.

### Tie definition: which layer

MMO305 week 2 separated co-presence (online at the same time), co-location (same zone) and co-activity (same group). Each gives a different network. Other layers include guild chat replies, whispers, trades, mail and shared voice sessions. Pardus shows that people take different roles in different layers, so name the layer you study and justify it by your question. If the question is about coordination in raids, co-activity in raid instances is right. If it is about who gives advice, chat replies are closer.

Every tie definition also has errors. Ducheneaut and colleagues excluded cities because characters idle there, and noted that two guildmates in the same zone may each be grouped with strangers. They judged that this effect faded at higher levels. Write down the errors of your definition, and which direction they push.

### Weight and threshold

Unweighted measures treat a 2-hour tie and a 20-hour tie the same. Thresholds remove weak ties, which can drop a node out of the network or turn someone into the only bridge, as the table in section 2 showed. There is no correct threshold. Choose one with a reason (for example "at least one full dungeon run"), then report the main results at two or three thresholds. If your headline finding survives, say so. If it does not, that is your finding.

### Time window

A month of data is a snapshot. The Tree House team met a player who looked peripheral because his guild had gone quiet around him. He had been active before it faded, and a longer window would have shown it. Choose the window by the rhythm of what you study. Raid teams run on weekly lockouts, and guild social life changes over months. Where you can, compute centrality in successive windows and report how stable the ranking is.

### Observed or reported ties

Server logs record behaviour. Surveys and interviews record what people say about their ties. In a series of studies from 1976 onward, H. Russell Bernard, Peter Killworth and colleagues compared people's reports of whom they communicated with against recorded communication. The reports were often wrong, and their 1984 review made informant accuracy a standing problem for network research. That does not make reported networks useless. People's beliefs about who matters shape what they do. But reported and observed networks answer different questions, and you should not substitute one for the other.

## 4. Reading centrality in a guild

A few patterns come up again and again when you compare centrality with rank.

- **The raid leader without a title.** High strength and betweenness, member rank. Often the person who runs the content the guild exists for. This is the Tamsin pattern and the Tree House "team leaders".
- **The absent guild master.** High rank, low centrality in every play layer. Possibly an inactive leader (MMO305 week 4 discussed WoW's mechanism for claiming leadership from an inactive guild master), possibly a leader who works through other channels. Only other data can tell which.
- **The officer inside one clique.** High strength, low betweenness. Important to one subgroup, invisible to the rest.
- **The bridge nobody named.** A member with modest degree but high betweenness, often someone who plays at unusual times or with two groups of friends. Losing them splits the guild, and nobody notices until it has happened.

Two cautions apply to all of them. Centrality is relative to the network, so a score of 0.5 in a 10-person guild is not comparable to 0.5 in a 200-person guild without care. And centrality describes a position, not a person's intentions or skills. It tells you where to look and whom to ask. Interviews and observation tell you what the person in that position does.

## 5. Ethics of network data

Network studies raise a problem other methods do not. When you record a tie, you record information about both people, and only one of them may have agreed to take part. If you interview Tamsin about whom she plays with, you learn about Kest, Bo and Pell, who never consented. If you build a network from logs, nobody consented unless the game or your study asked them.

- **Third parties.** Plan how you will handle information about people who are not participants. Report their data only in aggregate or pseudonymised form.
- **Structural re-identification.** Even with names removed, a network can identify people. The only member tied to both halves of a small guild is easy to spot for anyone in that guild. Publish structure at a level of detail the community cannot trace back to individuals, or with the community's agreement.
- **Awareness.** The Pardus authors described their data as free of interviewer effects because players were not conscious of their actions being logged. That is a methodological strength and an ethical question at once. Week 10 covers how an ethics board weighs research on existing data collected without participants' knowledge.
- **Consequences inside the community.** Handing a guild leader a centrality table can change how members are treated. Before you share results with a community, decide what you will share and with whom, and say so in your consent materials.

## In-class activity (25 minutes)

Work in groups of three. Each group receives a printed log of 40 grouping records from an invented 8-member guild (who grouped with whom, for how many minutes, in which zone) and the guild's rank list.

1. (8 min) Build the network. Agree on and write down the boundary, tie definition (exclude cities, as in Ducheneaut and colleagues' method), weight and threshold. Draw the graph.
2. (7 min) Compute degree centrality and strength by hand for every member. Identify the member with the highest betweenness by inspection and justify it with at least two pairs whose shortest paths pass through them.
3. (5 min) Raise your threshold to the median tie weight and redraw. Who changed position?
4. (5 min) Compare with the rank list. Write two sentences on who you would interview first to learn how the guild is led, and why.

Expected output: two drawings (before and after the threshold), a table of degree and strength, a named broker with evidence, and the two sentences.

## Common misconceptions

- **"The most central member is the leader."** Centrality measures position in one kind of tie. Tree House found high-centrality players who were not official leaders, and leaders whose work did not show up in co-play.
- **"There is one centrality score."** Degree, strength, betweenness and eigenvector answer different questions and can rank the same people differently. Kest and Mira swap places depending on the measure.
- **"The network is in the data."** The network is built by the researcher's boundary, tie, weight, threshold and window. Change any of them and centrality can change, as a single threshold moved Mira from third to second on betweenness and removed the guild master.
- **"Removing names makes network data anonymous."** Structure alone can identify people in small groups.

## Check yourself

1. In a 6-member guild, A is tied to B, C, D and E, and F is tied only to E. Compute everyone's degree centrality. Which member has the highest betweenness, and what is its raw value?
2. A study builds guild networks from co-presence (online at the same time) instead of co-activity. Predict what happens to density and to the ranking by degree, and explain why a night-shift player might be misread.
3. You report "Tamsin is the key broker" from one month at a threshold of 0 hours. A reviewer asks whether the result is robust. What two analyses do you add?
4. Explain why a guild master can have high rank and near-zero betweenness while still being the person without whom the guild would collapse.
5. Your ethics application for a guild network study says, "all data are anonymised." What two further protections should a reviewer ask for?

<details>
<summary>Answers</summary>

1. With `n − 1 = 5`: A 4/5 = 0.8, E 2/5 = 0.4, B, C, D and F 1/5 = 0.2. A has the highest betweenness. Every pair among B, C, D and E routes through A (6 pairs), and F to each of B, C and D routes through E and then A (3 more), so A's raw betweenness is 9. E has 4, from F's pairs with A, B, C and D.
2. Density rises and degrees rise for everyone who plays at popular times, because co-presence ties anyone who is online together, whether or not they play together. Prime-time players climb the degree ranking. A night-shift player who plays every night with the same partner looks peripheral, even if that partnership is the guild's strongest tie.
3. Recompute betweenness at two or three thresholds (for example 3 and 5 hours) and in successive monthly windows, then report whether Tamsin stays at the top. Optionally compute weighted betweenness too.
4. Betweenness measures position on shortest paths in the co-play network only. A guild master who holds the permissions, runs recruitment and settles disputes through other channels does work that creates no co-play ties. If they leave, the guild may lose its bank, its recruiter and its rules, as MMO305 week 4's succession problem shows.
5. Protection against structural re-identification, meaning aggregate reporting or suppression of small, unique positions. And a plan for third parties who did not consent, including what will and will not be shared with the guild's leaders.

</details>

## Lab / assignment hook

[Lab 09, a guild network from census snapshots](../labs/lab09.md). You turn supplied `/who`-style snapshot data into a weighted guild network, implement degree, strength, betweenness and eigenvector centrality, test how rankings change with the tie threshold, and write a 400-word memo comparing centrality with the guild's rank list and naming whom you would interview. Your code and the memo's sensitivity table feed the analysis section of the final paper.

## Sources

- Williams, D., Ducheneaut, N., Xiong, L., Zhang, Y., Yee, N. & Nickell, E. (2006). "From Tree House to Barracks: The Social Life of Guilds in World of Warcraft." *Games and Culture* 1(4), 338-361. https://doi.org/10.1177/1555412006292616. Census of three WoW servers in January 2006; centrality from time grouped with guildmates; 48 interviews in February and March 2006; few high-centrality interviewees were official leaders; team leaders and advisors; the caveat on low-centrality players and alts.
- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2007). "The Life and Death of Online Gaming Communities: A Look at Guilds in World of Warcraft." *Proceedings of CHI 2007*, 839-848. https://doi.org/10.1145/1240624.1240750. Ties from the zone, grouped flag and guild in `/who` data, weighted by time together, cities excluded; degree centrality defined as connections over guild size minus one, averaged per guild; density associated with guild survival; the Social Dashboard prototype. Data from five servers, June 2005 onward.
- Szell, M., Lambiotte, R. & Thurner, S. (2010). "Multirelational Organization of Large-Scale Social Networks in an Online World." *PNAS* 107(31), 13636-13641. https://doi.org/10.1073/pnas.1004008107. Pardus, online since 2004; Artemis universe, 18,819 players, first 445 days; six networks; individuals play different roles in different networks; data collected without players being conscious of logging.
- Freeman, L. C. (1977). "A Set of Measures of Centrality Based on Betweenness." *Sociometry* 40(1), 35-41. https://doi.org/10.2307/3033543.
- Freeman, L. C. (1978). "Centrality in Social Networks: Conceptual Clarification." *Social Networks* 1(3), 215-239. https://doi.org/10.1016/0378-8733(78)90021-7.
- Bonacich, P. (1987). "Power and Centrality: A Family of Measures." *American Journal of Sociology* 92(5), 1170-1182. https://doi.org/10.1086/228631.
- Krackhardt, D. & Hanson, J. R. (1993). "Informal Networks: The Company Behind the Chart." *Harvard Business Review* 71(4), 104-111 (July-August 1993). Only the abstract was checked (hbr.org, September 2026); the lecture uses the article's general argument, not its case details. Reprinted in *Networks in the Knowledge Economy* (Oxford University Press, 2003), https://doi.org/10.1093/oso/9780195159509.003.0016.
- Bernard, H. R., Killworth, P., Kronenfeld, D. & Sailer, L. (1984). "The Problem of Informant Accuracy: The Validity of Retrospective Data." *Annual Review of Anthropology* 13, 495-517. https://doi.org/10.1146/annurev.an.13.100184.002431. Also Killworth, P. & Bernard, H. R. (1976). "Informant Accuracy in Social Network Data." *Human Organization* 35(3), 269-286.
- Wowpedia, "Guild" (read September 2026). World of Warcraft guild control: leaders set rank titles and privileges, up to ten ranks; officer chat.

## Interactive spec: examples/w09-guild-centrality.html

**The one insight:** the member at the top of the rank chart and the member at the centre of the co-play network are different people, and which member looks most central depends on the measure and on the researcher's tie threshold.

**Layout.** Two linked panels side by side at 1280px, stacked at 390px (graph first).

- **Left panel, the guild graph.** Ten nodes at fixed positions (no force simulation, so layout never jumps): raiders on the left (Tamsin centre-left, Kest, Bo, Ria, Juno around her), casual players on the right (Mira, Pell, Nox, Ash), Rowan at the top centre. Node radius scales with the selected measure (min 10px, max 28px). Tie width scales with hours (1px at 2 hours to 7px at 20). Ties below the threshold are drawn faint and dashed, not removed, so students see what was cut. A small rank badge on each node: "GM" for Rowan, "Off" for Kest and Mira, none for Members. Clicking or pressing Enter on a node highlights it and shows every shortest path through it for the pair chosen in the pair picker.
- **Right panel, ranking.** Horizontal bars for all ten members sorted by the selected measure, with the rank badge beside each name and the exact value at the bar end (degree and betweenness to 3 decimals, strength as an integer, eigenvector to 2 decimals). Isolated members show "isolated" instead of a bar.

**Controls** (keyboard accessible, visible readouts):

- Measure: degree, strength, betweenness (normalised), eigenvector. Default betweenness.
- Minimum hours for a tie: 0 to 10, step 1, default 0.
- Pair picker (two dropdowns, source and target) that lists the shortest paths between them and `σ_st`.
- Toggle "sort by rank" that reorders bars by formal rank (GM, officers, members alphabetical) so the mismatch is visible.
- Reset.

**Data.** The 16 ties and hours in section 2's table. Ranks: Rowan Guild Master, Kest and Mira Officer, others Member.

**Formulas.** Ties with `hours ≥ threshold` are kept (threshold 0 keeps all). `n = 10` always, including isolated members.

```
degree(v)   = |N(v)| / (n − 1)
strength(v) = Σ hours of kept ties at v
betw(v)     = Σ_{s<t, s,t≠v, t reachable from s} σ_sv σ_vt / σ_st   [when d(s,v)+d(v,t)=d(s,t)]
betw_norm   = betw / ((n − 1)(n − 2)/2) = betw / 36
eig: x ← 1 for all; repeat 200 times: y(v) = x(v) + Σ_{u∈N(v)} x(u); x = y / max(y)
```

**Test values.** Threshold 0: Tamsin degree 0.667, strength 74, betweenness 0.523 (raw 18.83), eigenvector 1.00; Pell betweenness 0.231; Mira 0.194, eigenvector 0.72; Kest 0.074; Rowan 0.023 (raw 0.833), eigenvector 0.35; Juno and Ash 0. Threshold 5: Tamsin betweenness 0.500 (raw 18), Mira 0.417 (raw 15), Nox 0.194 (raw 7), Bo and Ria 0.014, Pell 0, Rowan isolated with degree 0. Pair picker at threshold 0, Kest to Nox: `σ = 3`, paths Kest-Tamsin-Mira-Nox, Kest-Tamsin-Pell-Nox, Kest-Rowan-Mira-Nox.

**Accessibility and style.** Palette from `templates/interactive-tokens.css`, inline. Rank badges use text, not colour alone. A screen-reader table mirrors the bar chart. Respect `prefers-reduced-motion` (no animated re-sorting). No game art, logos or class icons; members are named circles.
