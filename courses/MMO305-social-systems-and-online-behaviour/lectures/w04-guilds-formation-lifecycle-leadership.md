# MMO305 · Week 04 — Guilds: Formation, Lifecycle, Leadership

**Why this matters:** Guilds keep players in an MMO long after the content runs out, and most of them die young. The rules you write for joining, leaving, ranks and group size decide whether a guild can recover from a bad month or falls apart after one argument. You can model that, and you can design against it.

**You will be able to:**
- Model a guild's active membership as a stock with a recruitment inflow and a churn outflow, and compute its steady state.
- Identify a critical-mass threshold in a guild's content and predict when losing a few members tips it into collapse.
- Critique a shipped guild system (charters, caps, ranks, succession, exit costs) by naming which term of the model each rule changes.
- Design leadership and succession tools that keep a guild alive when its founder stops playing.

**Before class:** Williams, Ducheneaut, Xiong, Zhang, Yee & Nickell (2006), "From Tree House to Barracks: The Social Life of Guilds in World of Warcraft", *Games and Culture* 1(4), the whole paper (about 30 pages). Ducheneaut, Yee, Nickell & Moore (2007), "The Life and Death of Online Gaming Communities", CHI 2007, sections 1 to 4. Taylor, *Play Between Worlds* (2006), chapter 2, "Gaming Lifeworlds: Social Play in Persistent Environments" (pp. 21-66), on social life and guilds in EverQuest.

**Prerequisites from earlier courses:** [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) (a pile, the rate that fills it, the rate that drains it). [GD102 week 3, positive feedback loops](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md) and [GD102 week 4, negative feedback loops](../../GD102-systems-design-and-game-mechanics/lectures/w04-negative-feedback-loops-rubber-banding.md). [GS101 week 9, graphical MMOs](../../GS101-history-and-critical-study-of-games/lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md) (EverQuest's guilds and raids). [MA102 week 6, the binomial distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md) (how many of `n` people show up). [UX201 week 4, Self-Determination Theory](../../UX201-game-ux-and-player-psychology/lectures/w04-self-determination-theory.md) (relatedness). This course: [week 1, social capital](w01-mmos-as-societies-social-capital.md), [week 2, playing alone together](w02-playing-alone-together.md) and [week 3, forced versus voluntary grouping](w03-forced-vs-voluntary-grouping.md).

**Interactive:** [examples/w04-guild-tipping-point.html](../examples/w04-guild-tipping-point.html). Keep it open during section 2.

---

## 1. What a guild is, and what the game gives it

A **guild** is a persistent, named group of players that the game recognizes as a unit. EverQuest (1999) was the first MMORPG with a built-in guild system, and the name stuck. Other games use other names. Final Fantasy XIV calls them Free Companies, EVE Online calls them corporations, and some games call them clans. The idea is the same.

The word "recognizes" is doing the work. Players formed groups long before any game supported them. What a guild system adds is a set of tools:

- a **roster**, the list of members, visible to all of them;
- a private **chat channel** and often a message of the day;
- **ranks** with permissions (who may invite, who may remove members, who may withdraw from the bank);
- shared **property**, such as a guild bank or a house;
- a **tag** shown next to each member's name, which tells strangers who you belong to.

Each tool changes what is cheap and what is expensive for players. That is the lesson of Williams and colleagues' 2006 interview study of World of Warcraft guilds. Players used guilds to extend friendships they already had, to meet new people, and sometimes to treat other members as background. The authors found that the game's mechanics were the main thing moderating which of these happened. Code shapes the social life. Your job this week is to see which piece of code does what.

### Formation rules are a minimum group size

Most games make you prove a guild is a group before it exists. World of Warcraft sells a guild charter for 10 gold. Until patch 4.0.3a (2010) the founder needed 10 other players to sign it, and since then 5. Final Fantasy XIV asks for signatures from 3 other players and a 15,000 gil registration fee, and a founder cannot have been in a Free Company during the previous 24 hours.

Read those as design parameters. A signature requirement is a floor on founding size. A higher floor means fewer one-player "guilds" made only for a private bank, and fewer guilds overall. The fee is a small sink (MMO304) and a signal of intent. Neither rule keeps a guild alive after founding, and that is the harder problem.

## 2. Worked example: the guild that dies at 19

### The hook

In World of Warcraft since Warlords of Draenor (patch 6.0.2, 2014), Normal and Heroic raids scale for any group of 10 to 30 players. Mythic, the hardest difficulty, is fixed at exactly 20. Raid leaders tell a familiar story. A guild with 30 raiders is fine. Then an officer quits after an argument and takes a few friends. The guild can no longer field 20 on a raid night. Raids are cancelled, the next best players leave for a guild that is still raiding, and within a month or two the guild is a name with no one behind it.

Ducheneaut and colleagues followed guilds on five World of Warcraft servers for more than a year and summarized it in their abstract. Managing a guild is hard, and many guilds do not survive very long. The puzzle is why losing a few members should be fatal. A guild with 30 members that loses 12 still has 18, which is 90% of the 20 it needs. Why doesn't it just recruit two more and carry on?

### The model

Treat the guild's **active membership** `N` as a stock, as you did in GD102 week 2. Count members who show up for guild content in a given week, not names on the roster.

Each week:

```
N(next week) = N + R − c(N) × N
```

- `R` is **recruitment**, the number of new active members who join per week.
- `c` is **churn**, the fraction of active members who leave or go inactive per week.
- `M` is the **critical mass**, the active count the guild's main activity needs. For a Mythic raiding guild, that is 20 players plus enough spares to cover absences.

The key assumption is that churn depends on whether the guild can do what it exists to do:

```
c(N) = c_low   if N ≥ M   (the activity runs, members are content)
c(N) = c_high  if N < M   (the activity is cancelled, members drift away)
```

A stock with a constant inflow and a proportional outflow settles where inflow equals outflow, `R = c × N`. So each branch has its own **steady state**:

```
N_high = R / c_low     (valid only if it is at least M)
N_low  = R / c_high    (valid only if it is below M)
```

If both are valid, the guild has **two** stable states, a thriving one and a dying one, and the threshold `M` is the line between them. That line is a **tipping point**: a small push across it sends the guild to the other state, and it will not come back on its own.

### Numbers you can check

Take a raiding guild with `R = 2` recruits a week, `c_low = 5%` a week above the threshold, `c_high = 20%` a week below it, and `M = 20`.

- Thriving state: `N_high = 2 / 0.05 = 40`. That is at least 20, so it is valid.
- Dying state: `N_low = 2 / 0.20 = 10`. That is below 20, so it is valid too.

Both exist. Now run the model week by week. Column A is a healthy guild at 30. Column B is the same guild after a walkout drops it to 18. Column C is the same walkout followed by a one-week recruitment drive that brings in 6 members instead of 2, then back to normal. Fractions are averages; a real guild moves in whole players around these values.

| Week | A: healthy (start 30) | B: after walkout (start 18) | C: walkout, then 6 recruits in week 1 |
|---|---|---|---|
| 0 | 30.0 | 18.0 | 18.0 |
| 1 | 30.5 | 16.4 | 20.4 |
| 2 | 31.0 | 15.1 | 21.4 |
| 3 | 31.4 | 14.1 | 22.3 |
| 4 | 31.9 | 13.3 | 23.2 |
| 6 | 32.7 | 12.1 | 24.8 |
| 8 | 33.4 | 11.3 | 26.3 |

Check the first rows by hand. Week 1 of column B is `18 + 2 − 0.20 × 18 = 16.4`. Week 1 of column C is `18 + 6 − 0.20 × 18 = 20.4`, which is above `M`, so week 2 uses `c_low`: `20.4 + 2 − 0.05 × 20.4 = 21.38`.

Guilds A and B have the same recruiting, the same members and the same leaders. B is heading for 10 and A for 40. The only difference is which side of 20 they started on.

### Why a small loss is fatal

Below `M`, the guild loses `0.20 × 18 = 3.6` members a week and gains 2. It shrinks by 1.6 a week, and shrinking makes the next week no better, because it stays below the line. Above `M`, it loses `0.05 × 30 = 1.5` and gains 2. It grows.

The rescue condition is one line. To climb back from just below the threshold, recruitment must beat churn at the threshold:

```
R > c_high × M = 0.20 × 20 = 4 per week
```

Normal recruiting of 2 a week is half of that. So "just recruit two more" fails because two more won't stay. They join a guild that is cancelling raids, and they leave at the high rate like everyone else. Column C works because the drive puts the guild over the line in a single week, after which the ordinary low churn takes over. A slow drive that brings in 2 extra a week spread over a month would not.

This is a **positive feedback loop** from GD102 week 3 with a switch in it. Above `M`, the loop is mild and the guild's growth is capped by the outflow (a negative loop). Below `M`, cancellations cause departures, which cause more cancellations.

### The visual

Open the interactive. The left panel plots `N` against weeks for a guild you can shock with a "walkout" button. The right panel plots the **net flow** `R − c(N) × N` against `N`. That right-hand plot is the one to stare at. It is a line that crosses zero twice, once at 10 and once at 40, with a jump at 20 where churn switches. Anywhere the net flow is positive, the guild grows toward the right. Anywhere it is negative, it shrinks toward the left. Drag the walkout size and watch the dot on the right panel cross the jump. Drag `R` to 4 and watch the dying equilibrium touch the threshold and vanish.

### Cross-game recognition

The same model explains design choices in games that never talked about tipping points. For each, ask which term the rule moves.

**World of Warcraft, flexible raid size (Mists of Pandaria patch 5.4 and Warlords of Draenor patch 6.0.2).** Patch 5.4 let flexible raids scale from 10 to 25 players, and 6.0.2 extended scaling to 10 to 30 for Normal and Heroic, leaving only Mythic fixed at 20. In model terms, flex raiding lowers `M` for most guilds from "exactly 10 or exactly 25" to 10. Run column B with `M = 10` and the guild at 18 is above the line. After 8 weeks it has grown to about 25, not shrunk to 11. The walkout that kills a Mythic guild is survivable for a Heroic one.

**World of Warcraft, classic era (2004 to 2006).** Molten Core and the other original raids took 40 players. With `R = 2` and `c_low = 5%`, the thriving steady state is exactly 40, with no spares. A 40-player raid guild needed recruitment far above what a 20-player guild needs just to reach its threshold, which is one reason classic-era raiding guilds were famous for constant recruiting.

**World of Warcraft, guild reputation (Cataclysm, patch 4.0.1).** Cataclysm added guild levels and guild reputation. A character who leaves a guild has their guild reputation reset to 0. That is a cost of leaving, so it lowers `c` in both branches. Patch 6.0.2 removed guild levels, and all guilds now get the same benefits on creation. That raised `c` a little, and it removed a reason for small guilds to merge into large ones.

**Guild Wars 2 (current).** An account can belong to up to 6 guilds at once and chooses, per character, which one to represent. The cost of joining a second guild is close to zero, so a player can stay in a small social guild and join a large raiding one. In model terms, membership stops being exclusive. A walkout from the raiding guild no longer removes the player from their friends, which lowers the social cost of leaving (higher `c`) but also means players are rarely left with no guild at all.

**Final Fantasy XIV (current).** Free Companies hold up to 512 members, and players may belong to only one. The game's 8-player raids are usually run by a **static**, a fixed group of 8 that often forms across Free Companies. The raiding threshold `M = 8` lives in the static, and the Free Company's own threshold for its social activities is much lower. Splitting the group that needs critical mass from the group that holds the social ties protects the social group from raiding collapses.

Five games, one model. When you meet a new guild rule, ask whether it moves `R`, `c` or `M`, and on which side of the threshold.

### Eyes-open design judgment

The model tells you what to worry about. It does not tell you what to want.

- **A fixed group size creates a cliff.** Fixed sizes are good for encounter design, because you can tune a fight for exactly 20. They also create the threshold that kills guilds. If your hardest content has a fixed size, give guilds a way down. Lower difficulties with flexible size are one way. A merge or alliance tool is another.
- **Exit costs are double-edged.** Guild reputation that resets on leaving lowers churn in a healthy guild. It also traps members in a dying one, and those members are the ones most likely to quit the game instead of switching guilds. An exit cost keeps members in the guild when you want the game to keep them.
- **Big guilds are not the goal.** A game whose rewards scale with guild size (Cataclysm's guild perks) pushes players into large guilds whose members don't know each other. Williams and colleagues' interviewees describe the resulting weak ties. Decide whether you want many small guilds with strong ties or few large ones with weak ties, then price guild features to match.
- **The model is a caricature.** Real churn does not switch at a single number. It rises as raids get cancelled more often. Use the model to find where your guild system has a cliff, then measure the real curve with telemetry (MMO308).

### Check yourself (worked example)

1. A guild has `R = 3`, `c_low = 6%`, `c_high = 25%`, `M = 20`. List its steady states and say which are valid.
2. For the guild in question 1, what weekly recruitment gets it out of the dying state from just below 20?
3. A designer proposes lowering Mythic raid size from 20 to 15 to save guilds. Using the model, name one thing that change does and one thing it does not do.

<details>
<summary>Answers</summary>

1. `N_high = 3 / 0.06 = 50` (valid, above 20). `N_low = 3 / 0.25 = 12` (valid, below 20). Two stable states.
2. Recruitment must exceed `c_high × M = 0.25 × 20 = 5` per week.
3. It lowers `M`, so a guild with 16 to 19 active members is now above the line and uses the low churn. It does not change `R` or the churn rates, so a guild that falls below 15 still collapses. The cliff moves, it doesn't disappear.

</details>

## 3. The lifecycle of a guild

The model describes a guild that already exists. Guilds also go through stages, and each stage has its own failure mode.

A useful frame comes from small-group psychology. Tuckman (1965) described groups as **forming** (members meet and test each other), **storming** (conflict over goals and status), **norming** (the group agrees on rules), and **performing** (the group does its work). Tuckman and Jensen (1977) added **adjourning**, the group's end. Guilds show all five, and you can map each onto the model.

| Stage | What happens in a guild | Model term under pressure | Typical failure |
|---|---|---|---|
| Forming | Founder recruits friends and strangers, sets a goal | `R` must be high, `N` is below `M` | Never reaches critical mass |
| Storming | Arguments over loot, ranks, raid spots, schedules | `c` spikes | Walkout pushes `N` below `M` |
| Norming | Written rules, loot system, attendance policy | `c` falls | Rules seen as unfair, quiet departures |
| Performing | Regular content, stable roster | Guild sits near `N_high` | Burnout of leaders, content drought |
| Adjourning | Guild merges, goes dormant, or disbands | `R` falls to near 0 | Members quit the game instead of moving |

Two stages matter most for design. **Forming** is where most guilds die, because a new guild starts below its own threshold and needs a burst of recruitment to cross it. Recruitment tools (a guild finder, a public listing, a recruitment channel) raise `R` exactly when it matters. **Storming** is where a healthy guild dies, because one argument can remove a cluster of friends at once. Next week's loot rules exist largely to prevent the storming that loot causes.

### Size and the cost of coordination

Why don't successful guilds just keep growing? One reason is coordination cost. In a group of `n` people, the number of pairs who might need to get along is

```
pairs = n × (n − 1) / 2
```

Ten members make 45 pairs. Forty make 780. Two hundred make 19,900. Nobody can hold 19,900 relationships in their head. Dunbar (1992) argued from primate brain sizes that humans can keep track of stable relationships with about 150 people. The exact figure is disputed, but the shape of the problem is not. Past a few dozen members, a guild must split into subgroups (raid teams, officer councils, social circles) or become a crowd of strangers sharing a tag.

Guild caps are where designers take a position on this. World of Warcraft caps a guild at 1,000 members, from patch 4.0.1. Final Fantasy XIV caps a Free Company at 512. Guild Wars 2 guilds start at 50 and can be upgraded to 500. None of these caps is near the size where a guild works as one social group. They are limits on the database and on the guild's power, not on its social health. The social limit comes from the players.

## 4. Leadership: the single point of failure

A guild leader in most games holds every permission. They set ranks, invite and remove, and control the bank. The leader is also, in practice, the recruiter, the dispute judge, the raid scheduler and the person who logs in when nobody else wants to. This makes the leader the component whose failure the model hides. When a leader burns out, `R` drops (nobody recruits), `c` rises (nobody resolves disputes), and the guild slides whatever its current `N`.

### What leaders do

Break the leader's job into tasks, and you can design tools for each:

- **Recruiting**: finding and vetting players. Tools: guild finder listings, applications, trial ranks.
- **Scheduling**: getting `M` players online at the same time. Tools: in-game calendars with sign-ups, attendance records.
- **Allocating**: deciding who gets raid spots and loot. Tools: loot systems (next week), bench rotation.
- **Judging**: resolving conflict and removing members who harm the group. Tools: rank permissions, officer notes, a log of who did what with the bank.
- **Representing**: dealing with other guilds, alliances and the community.

A guild with one person doing all five survives exactly as long as that person does. Rank permissions are the game's way of letting a leader delegate. Every permission you let a leader hand to an officer is a way of spreading the load. Every permission that only the leader can hold is a bottleneck.

### Succession

The hardest leadership problem is the leader who stops playing without handing over the guild. Before a fix, a guild whose leader went inactive was stuck. Nobody could promote officers, change ranks or fix permissions, so active members had to found a new guild and move everyone, which is a forced walkout and a loss of the guild's bank and history.

World of Warcraft added a fix in patch 4.3.0 (2011). If the leader has been inactive long enough, a member of a senior rank can claim leadership through the guild interface. The inactivity window was set at 30 days and then raised to 90 by a 2012 hotfix, and only members of the top ranks below the leader may claim it. That is a real trade-off. A short window protects guilds from absent leaders but lets an officer seize a guild while the leader is on a month's holiday. A long window protects the leader but leaves the guild stuck for three months, which, from the model, is long enough to lose it.

### Leadership styles

Research on guild leadership is mostly interview-based, and it points to a spread of styles rather than one best way. Some guilds run as a benevolent dictatorship around a founder. Some run as an officer council. Some have written charters with votes. For design purposes the style matters less than whether your tools support it. A game that has only "leader" and "member" forces dictatorship. A game with configurable ranks and permissions lets players build a council. A game with a voting tool makes votes cheap. What your guild interface makes easy is what most guilds will do.

## In-class activity (25 minutes)

In groups of three, you are the social systems team for a new MMO with 5-player dungeons and one 15-player raid tier at fixed size.

1. Set values for `R`, `c_low` and `c_high` that you think fit a mid-sized raiding guild, and compute both steady states with `M = 15`. Justify each number in one sentence.
2. Using the interactive, find the smallest walkout that sends your guild into the dying state from its thriving state.
3. Propose one rule change that makes that walkout survivable. Name the term it moves (`R`, `c_low`, `c_high` or `M`) and one side effect.
4. Write the one-paragraph design note you would send to the raid designers explaining why a fixed 15-player size worries you, or why it doesn't.

Expected output: the parameter table with justifications, the walkout number, the rule change with its side effect, and the design note.

## Common misconceptions

- **"A guild that lost 10% of its members is 10% weaker."** Not near a threshold. A guild at 22 with `M = 20` that loses 3 goes from growing to shrinking. Losses matter by which side of `M` they leave you on.
- **"Recruit harder" fixes a dying guild.** Only if recruitment beats churn at the threshold (`R > c_high × M`). Recruits who join a guild that can't run its content leave at the high churn rate.
- **"Bigger guild caps make healthier guilds."** Caps limit the database and guild power, not social health. Coordination cost grows with the number of pairs, roughly with `n²`.
- **"Exit costs keep players in the game."** They keep players in the guild. In a dying guild, that can mean they leave the game instead.

## Check yourself

1. A social guild has no raid and no critical mass, so churn is always 8% a week. Recruitment is 1.2 a week. Where does it settle, and how does a walkout that halves it change the long-run outcome?
2. A raiding guild has `R = 2.5`, `c_low = 5%`, `c_high = 20%`, and `M = 20`. Is it bistable? If a walkout takes it to 15, how many recruits does it need in one week to cross back over 20?
3. Your game adds a feature that lets two guilds form an alliance and raid together, pooling members. Explain which model term this changes and why it makes the dying state easier to escape.
4. A guild's active membership has been flat at 24 for three months, and `M = 20`. The leader announces they are quitting in two weeks, and no succession tool exists. Name two model terms likely to change and in which direction.

<details>
<summary>Answers</summary>

1. With one churn rate there is one steady state, `1.2 / 0.08 = 15`. A walkout to 7.5 is temporary: the guild grows back toward 15 at a net rate of `1.2 − 0.08 × N` per week. Without a threshold there is no tipping point.
2. `N_high = 2.5 / 0.05 = 50` (valid) and `N_low = 2.5 / 0.20 = 12.5` (valid, below 20), so it is bistable. From 15 it needs `N + R − 0.20 × 15 ≥ 20`, so `R ≥ 20 − 15 + 3 = 8` recruits that week.
3. It raises the effective `N` counted against `M`, since two guilds below 20 each may be above 20 together, or equivalently lowers the `M` each guild must meet alone. Both guilds move to the low-churn branch.
4. `R` falls (nobody recruits or runs the guild finder) and `c` rises (nobody resolves disputes, members anticipate collapse). Both push `N` down toward `M`, and with 24 active the guild has only 4 members of margin.

</details>

## Lab / assignment hook

[Lab 04, guild health model](../labs/lab04.md). You fit the model in this lecture to 16 weeks of roster data from a fictional guild, find its threshold, and write a rescue plan for its officers. It also prepares the field observation assignment, where you will describe a real guild's rules and name the model term each rule moves.

## Sources

- Williams, D., Ducheneaut, N., Xiong, L., Zhang, Y., Yee, N. & Nickell, E. (2006). "From Tree House to Barracks: The Social Life of Guilds in World of Warcraft." *Games and Culture* 1(4), 338-361. doi:10.1177/1555412006292616. Interview study; players extend real-life ties, meet new people, or treat others as backdrop, moderated by game mechanics.
- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2007). "The Life and Death of Online Gaming Communities: A Look at Guilds in World of Warcraft." *Proceedings of CHI 2007*, 839-848. doi:10.1145/1240624.1240750. More than a year of data from five World of Warcraft servers; many guilds do not survive long.
- Taylor, T. L. (2006). *Play Between Worlds: Exploring Online Game Culture*. MIT Press. Chapter 2, "Gaming Lifeworlds: Social Play in Persistent Environments", pp. 21-66 (chapter list from the MIT Press Direct records, doi:10.7551/mitpress/5418.003.0003).
- Tuckman, B. W. (1965). "Developmental Sequence in Small Groups." *Psychological Bulletin* 63(6), 384-399. Tuckman, B. W. & Jensen, M. A. C. (1977). "Stages of Small-Group Development Revisited." *Group & Organization Studies* 2(4), 419-427.
- Dunbar, R. I. M. (1992). "Neocortex Size as a Constraint on Group Size in Primates." *Journal of Human Evolution* 22(6), 469-493.
- Warcraft Wiki, "Guild" (patch history). Charter signatures reduced from 10 to 5 in patch 4.0.3a; 1,000-member cap from patch 4.0.1; guild advancement and levels removed in patch 6.0.2; guild reputation resets to 0 on leaving (Cataclysm); inactive leader replacement added in patch 4.3.0, window raised from 30 to 90 days by hotfix of 17 April 2012.
- Warcraft Wiki, "Raid" and "Flexible Raid". 40-player raids such as Molten Core in the original game; flexible raids of 10 to 25 players in patch 5.4.0; 10 to 30 players on all difficulties except Mythic from patch 6.0.2; Mythic fixed at 20.
- Guild Wars 2 Wiki, "Guild" (current). Up to 6 guild memberships per account, representation chosen per character, 50-member start upgradable to 500.
- Final Fantasy XIV Wiki (consolegameswiki), "Free Company" (current). 512-member cap, one Free Company per player, 3 other signatures and a 15,000 gil fee to found.
- GS101 week 9 of this program, for EverQuest's 2011 Game Developers Choice Online Hall of Fame citation as the first MMORPG with a guild system and raiding.

## Interactive spec: examples/w04-guild-tipping-point.html

**The one insight:** a guild with a critical-mass threshold has two stable sizes, and a walkout that crosses the threshold sends it to the small one even though recruiting and churn rates are unchanged. The net-flow plot makes the two zero crossings and the jump at `M` visible.

**Layout.** Two linked panels, side by side at 1280px, stacked at 390px (trajectory first).

- **Left panel, trajectory.** x-axis weeks 0 to 52, y-axis active members 0 to 60. One line for the current run. A dashed horizontal line at `M` labelled "critical mass". Dotted horizontal lines at `N_high` and `N_low` when they are valid, labelled with their values. When the "compare" toggle is on, a second, lighter line shows the same guild with no walkout.
- **Right panel, net flow.** x-axis `N` from 0 to 60, y-axis net flow `R − c(N) × N` in members per week. Draw the two branches as line segments with a vertical jump at `M`. Draw y = 0 as a reference line. Mark stable steady states as filled circles and the threshold as an open circle. A dot shows the guild's current `N` (it moves as the simulation week slider moves). Shade positive net flow in the "grow" token colour and negative in the "shrink" token colour, with arrows on the x-axis pointing in the direction of motion.

**Controls** (all keyboard accessible, each with a visible numeric readout):

- `R` recruits per week, 0 to 8, step 0.5, default 2.
- `c_low` percent per week, 1 to 20, step 1, default 5.
- `c_high` percent per week, 5 to 50, step 1, default 20.
- `M` critical mass, 5 to 40, step 1, default 20.
- Starting `N`, 0 to 60, step 1, default 30.
- Walkout size, 0 to 30, step 1, default 12, and walkout week, 0 to 26, step 1, default 4. The walkout subtracts that many members at the start of that week (floor at 0).
- Recruitment drive: extra recruits, 0 to 10, step 1, default 0. They are added once, in the step from walkout week `w` to week `w + 1` (the first update after the walkout), and never again.
- Preset buttons: "Mythic (M = 20)", "Flex (M = 10)", "Classic 40 (M = 40)". Presets set `M` only.
- Week slider 0 to 52 that moves the dot on the right panel along the trajectory.

**Formulas.**

```
c(N) = c_low if N ≥ M else c_high
N(t+1) = max(0, N(t) + R − c(N(t)) × N(t))
walkout: at the start of week w, N(w) = max(0, N(w) − walkout)
drive: in the step from week w to week w + 1, R is replaced by R + extra (that step only)
N_high = R / c_low, shown only if N_high ≥ M
N_low  = R / c_high, shown only if N_low < M
rescue threshold shown as text: R > c_high × M
```

**Readouts beside the panels:** current `N` at the selected week, `N_high` and `N_low` (or "none"), the rescue threshold `c_high × M`, and a one-line verdict: "Heading for N_high", "Heading for N_low", or "At threshold".

**Test values** (defaults `R = 2`, `c_low = 5%`, `c_high = 20%`, `M = 20`, walkout at week 0):

| Start | Walkout | Drive | N at week 1 | N at week 2 | N at week 8 |
|---|---|---|---|---|---|
| 30 | 0 | 0 | 30.5 | 30.98 | 33.37 |
| 30 | 12 | 0 | 16.4 | 15.12 | 11.34 |
| 30 | 12 | 4 (so 6 in week 1) | 20.4 | 21.38 | 26.31 |

With `M = 10` and start 18, no walkout: week 8 is about 25.4. With `R = 4`, `N_low = 20`, which is not below `M`, so only `N_high = 80` is shown (y-axis must extend or clip with a label). The trajectory readout shows two decimals, so that the test values above (30.98, 15.12, 33.37) can be checked; steady states and thresholds may show one decimal.

**Accessibility and style.** Palette from `templates/interactive-tokens.css`, inline. Respect `prefers-reduced-motion` (no animated line drawing). Every chart has a text summary for screen readers giving the steady states and the verdict. No game logos or art; the presets are named in text only.
