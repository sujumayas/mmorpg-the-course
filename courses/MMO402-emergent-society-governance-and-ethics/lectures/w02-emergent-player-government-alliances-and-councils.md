# MMO402 · Week 02 — Emergent Player Government: Alliances and Councils

**Why this matters:** Players build governments whether you design for it or not. Guilds grow ranks, alliances grow councils, coalitions grow treaties. The permission tools you ship decide how those governments fail: whether one disgruntled officer can empty the treasury, or whether nobody can act fast enough when it matters. That is a design decision, and it is yours.

**You will be able to:**
- Describe the structure of player government in EVE Online, from corporation to coalition, and name the powers the game hands to each level.
- Compute, with the binomial distribution, the chance that a K-of-N approval rule is hijacked and the chance that it acts in time.
- Choose a K for a given action by minimizing expected cost, and explain why duties and powers need different rules.
- Critique a guild or alliance permission system against Ostrom's design principles for self-governing groups.

**Before class:** Ostrom, *Governing the Commons* (1990), chapter 3, the section listing the design principles (about 20 pages). Groen, *Empires of Eve* (2016), the chapters on the rise of Band of Brothers. EVE University Wiki, "Alliance" (10 minutes). Buchanan and Tullock, *The Calculus of Consent* (1962), the chapters on the costs of decision rules (skim the figures).

**Prerequisites from earlier courses:** [MA102 week 6, the binomial distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md) (the tail sums used below). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (`1 − (1 − a)^N`). [MMO401 week 8, player banks, loans and scams](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w08-player-banks-loans-and-scams.md) (what the server enforces and what it leaves to trust). [MMO305 week 4, guilds](../../MMO305-social-systems-and-online-behaviour/lectures/w04-guilds-formation-lifecycle-leadership.md) and [MMO305 week 5, raiding and DKP](../../MMO305-social-systems-and-online-behaviour/lectures/w05-raiding-as-organization-dkp.md) (guild formation and raid loot rules). This course: [week 1, worlds as polities](w01-worlds-as-polities.md).

**Interactive:** [w02-keys-to-the-vault.html](../examples/w02-keys-to-the-vault.html)

---

## 1. From guild to coalition

Player government starts small. A **guild** (EVE calls it a corporation) is a named group with a leader, a roster, a chat channel and usually a shared bank. Nearly every MMO ships these. Once guilds need to cooperate, they form larger bodies. EVE Online gives the clearest example, because its designers built formal tools for each level.

- **Corporation.** A player-run company with a CEO, member roles and shared hangars and wallets. Roles decide who can take what out.
- **Alliance.** A group of corporations. According to the EVE University Wiki, founding one costs one billion ISK up front and a monthly fee per member corporation, and one corporation must act as the **executor**. The executor accepts or rejects corporations that apply, sets the alliance's standings toward everyone else, and pays the alliance's bills. If the bill goes unpaid, the alliance dissolves at the next server downtime. To become executor, a corporation needs the support of the CEOs of at least half the member corporations.
- **Coalition.** A group of alliances bound by agreements the game does not know about. Coalitions have no in-game tools at all. They run on shared chat servers, spreadsheets, treaties and trust.

Notice the pattern. The game enforces the lower levels and leaves the top level to players. A coalition is a government made entirely of norms, in Lessig's terms from week 1. That is why the famous collapses in EVE history are political stories more than combat stories.

### How big these get

On 27 and 28 January 2014, a corporation in the N3 and Pandemic Legion coalition failed to make a scheduled payment that kept its hold on the star system B-R5RB. The system became vulnerable, and the rival coalition attacked. The battle that followed lasted 21 hours and ended only when the server went down for maintenance. Wikipedia's account counts more than 7,548 player characters from 717 corporations in 55 alliances, 75 titans destroyed, and losses of about 11 trillion ISK, which it estimates at US$300,000 to 330,000 at the time's exchange rate through the game's subscription item.

The biggest battle in the game's history to that point started with a missed bill. Not a tactical error, an administrative one. Somebody was supposed to pay, and nobody did.

### Ostrom's principles for groups that last

Elinor Ostrom won the 2009 Nobel Prize in economics for showing that communities can manage shared resources, such as fisheries, forests and irrigation water, without either a central government or private ownership. In *Governing the Commons* (1990) she listed eight features that long-lived community institutions tended to share. A guild bank is a shared resource, and a guild is a community managing it, so the list transfers well.

| Ostrom's principle (paraphrased) | What it looks like in a guild or alliance |
|---|---|
| 1. Clear boundaries: who may use the resource is defined | A roster, ranks, and a rule for who can see which bank tab |
| 2. Rules fit local conditions | Loot rules suited to the group's raid size and schedule |
| 3. Those affected can help change the rules | Members vote on or discuss loot and dues changes |
| 4. Monitors are accountable to the members | Officers who audit the bank log report to the guild |
| 5. Graduated sanctions | Warning, then demotion, then removal, not instant expulsion |
| 6. Cheap, fast conflict resolution | An officer channel for disputes, with an agreed arbiter |
| 7. Outside authority accepts the group's right to organize | The developer does not override guild decisions |
| 8. Nested layers | Squads inside guilds inside alliances inside coalitions |

Principles 1, 4 and 5 depend on tools the developer ships: rank systems, bank logs and permission settings. Principle 7 is a developer policy. Principle 8 is exactly what EVE's corporation, alliance and coalition levels provide. The rest are up to the players, but you can make them easier or harder.

The worked example takes principle 4 seriously. Monitors must be accountable, and the officers who hold the keys must not be able to act alone. The question is how many should have to act together.

## 2. Worked example: how many keys should open the vault?

### The hook

In 2009, a director of Band of Brothers, one of EVE Online's largest alliances at the time, defected to its enemies in Goonswarm. According to the account on Wikipedia's EVE Online page, he stripped the alliance of ships, money and territory and then disbanded it. One person, using powers the game gave his role, erased an organization that thousands of players had built over years.

Five years later, the B-R5RB battle started because one payment was missed.

These two failures look like opposites. In the first, one person could do too much. In the second, the people who needed to act did not. They are the same design problem seen from two sides: **how many people must agree before a group acts?** Require one signature and a single traitor can do anything. Require everyone's and nothing happens on time.

### The model

A group has `N` officers who hold keys to some power: withdrawing from the treasury, disbanding the alliance, declaring war. A rule says **K of the N** must approve before the action goes through. Model two risks.

- Each officer is independently a **traitor** (a spy, a thief, or someone whose account was stolen) with probability `q`.
- Each officer is independently **available** to approve a legitimate action within the time it is needed with probability `a`.

A **hijack** happens if at least `K` officers are traitors, because they can approve a harmful action on their own. From MA102 week 6, that is a binomial tail:

```
P(hijack) = Σ from j = K to N of  C(N, j) × q^j × (1 − q)^(N − j)
```

A **timely** legitimate action needs at least `K` officers available:

```
P(timely) = Σ from j = K to N of  C(N, j) × a^j × (1 − a)^(N − j)
```

(For simplicity, a traitor who is available still approves legitimate actions, to keep their cover. Changing that assumption lowers `P(timely)` a little and changes no conclusion below.)

To pick `K`, give each failure a cost. `H` is the damage from a hijack, `L` is the damage from a late legitimate action. The expected cost of a rule is

```
cost(K) = H × P(hijack) + L × (1 − P(timely))
```

This is James Buchanan and Gordon Tullock's argument from *The Calculus of Consent* (1962) in miniature. They showed that requiring more people to agree lowers **external costs** (the harm a decision does to people who did not agree to it) and raises **decision costs** (the effort and delay of reaching agreement). The best rule minimizes the sum. A hijack is an external cost. Lateness is a decision cost.

### Numbers you can check

Take a guild with `N = 5` officers. Each has a 10% chance of being a traitor (`q = 0.1`) and a 60% chance of being around when needed (`a = 0.6`).

| K of 5 | P(hijack) | P(timely) | cost, H = 100 and L = 10 | cost, H = 100 and L = 50 |
|---|---|---|---|---|
| 1 | 40.95% | 98.98% | 41.05 | 41.46 |
| 2 | 8.15% | 91.30% | 9.02 | **12.50** |
| 3 | 0.86% | 68.26% | **4.03** | 16.73 |
| 4 | 0.046% | 33.70% | 6.68 | 33.20 |
| 5 | 0.001% | 7.78% | 9.22 | 46.11 |

Check two cells by hand.

- `K = 1`: a hijack needs at least one traitor, so `P = 1 − 0.9^5 = 1 − 0.59049 = 0.40951`. That is the complement rule from MA102 week 3.
- `K = 2`, timely: `P = 1 − P(0 available) − P(1 available) = 1 − 0.4^5 − 5 × 0.6 × 0.4^4 = 1 − 0.01024 − 0.0768 = 0.91296`.

And one cost: with `K = 3`, `H = 100`, `L = 10`, the cost is `100 × 0.00856 + 10 × (1 − 0.68256) = 0.856 + 3.174 = 4.03`.

### The insight

Look at how the two probability columns move. Going from one key to two cuts hijack risk fivefold, from 41% to 8%, and costs only 8 points of timeliness. Going from two to three cuts it almost tenfold again and costs 23 points. After that, each extra key buys a vanishing amount of safety for a large loss of speed.

The two risks fall at different rates. Hijack risk drops roughly by a factor of `q` for each extra key, which is geometric. Timeliness holds up while `K` stays below the expected number of available officers, `N × a = 3`, and then falls off steeply. So the sweet spot sits at or just below `N × a`.

The cost columns add the second lesson. **The best K depends on the action.** For an action where lateness is cheap (`L = 10`, say moving surplus materials between bank tabs), three keys win. For an action where lateness is expensive (`L = 50`, say paying the bill that keeps your territory), two keys win.

And for a pure **duty**, something that must happen and does no harm if done twice, the right rule is the opposite of a key. Let any one of the `N` officers do it. The chance nobody does is `(1 − a)^N = 0.4^5 = 1.0%`. Duties need "any of N." Powers need "K of N." The B-R5RB battle is what happens when a duty is left to one person.

### The visual

Open the interactive. The top panel plots `P(hijack)` and `P(timely)` against `K` for the current `N`, `q` and `a`, on a logarithmic hijack axis so the geometric fall shows as a straight line. The bottom panel plots the expected cost against `K`, with the minimum marked. Drag `L` up and watch the best `K` step down. Drag `N` from 5 to 7 and notice that a bigger council lets you raise `K` and get both more safety and better timeliness than a small one.

### Cross-game recognition

**EVE Online's executor rule.** The alliance executor needs the support of CEOs from at least half the member corporations. That is a K-of-N rule with `K = N/2`, applied to the choice of who governs, which is the rare case where the game itself sets `K`. Everything below that level, such as who can withdraw from a corporation wallet or hangar, is left to how the CEO assigns roles, which is where the Band of Brothers director's power came from.

**World of Warcraft's guild bank (since patch 2.3).** Warcraft Wiki describes permissions set per bank tab and per guild rank, including limits on withdrawals. This is a different tool for the same problem. Instead of requiring several people to agree, it caps how much any one person can take. In model terms it lowers `H`, the damage a single hijack can do, and leaves `K = 1`. Rate limits and co-signing are substitutes. You can trade one for the other.

**LambdaMOO's ballots (1993 onward).** A ballot needed a two-to-one majority of votes cast to pass. That is a K-of-N rule where N is whoever turns up, a detail that matters in week 3.

**Outside games: multisignature wallets.** Bitcoin's BIP 11 (2011) standardized "M-of-N" transactions, where coins can move only if M of N named keys sign. The common 2-of-3 setup lets one key be lost or stolen without losing the funds, which is exactly the trade-off in the table, with a small `N`.

Four systems, four presentations, one idea: the number of people who must act together sets both how safe and how slow a group is.

### Eyes-open design judgment

- **Ship tiers, not one switch.** A guild system with one "officer" rank that can do everything forces players into `K = 1` for every power. Offer per-action permissions so players can match `K` to the cost of the action.
- **Ship rate limits and delays.** A daily withdrawal cap lowers `H`. A 24-hour delay on disbanding an alliance, visible to all members, turns a hijack into something others can stop. Both are cheaper to use than co-signing.
- **Duties should be "any of N."** Recurring payments that keep territory or structures alive should be payable by any authorized member and should warn loudly before they lapse.
- **Decide how much betrayal you want.** EVE's designers treat theft and betrayal inside the game as part of the world (MMO401 week 8 covers the bank heists). Tight co-signing would have prevented the Band of Brothers collapse, and it would also have removed one of the game's most famous stories. A cozy guild game should protect groups from their officers. A sandbox about politics may choose not to. Either way, choose it.
- **The model assumes independence.** Traitors recruit each other, and officers in the same time zone are unavailable together. Correlated risk makes both columns worse than the table says. Designers should assume officers are less independent than they look.

## 3. How alliance councils actually decide

The executor corporation is the only body the game recognizes, but most large alliances run a council of some kind: the CEOs of member corporations, or a smaller group of directors. The game does not know the council exists. The executor's CEO could ignore it. Why do they not?

Because every alliance faces the exit-voice trade-off from week 1, one level up. A member corporation that dislikes the council's decisions can leave the alliance and take its pilots, territory and income with it. Its switching cost is low compared with an individual player's: the corporation keeps its members, its roles and its assets. So alliance leaders must keep corporations inside by giving them voice. A council is the price of keeping exit costs low for your members.

This produces a common life cycle, and you will see it in lab.

1. **Founding.** A few corporations with personal trust form an alliance. Decisions are informal. `N` is small and `q` is low because everyone knows each other.
2. **Growth.** New corporations join for protection or income. `q` rises, because the leaders do not know the new members. Informal rules become written ones, and the leadership adds keys.
3. **Strain.** A decision hurts a subset of members, such as a war that takes one region's pilots away from their home. Voice happens in the council. If `p` is low for that subset, they exit, and their exit lowers the switching cost of their friends in other corporations, the cascade from week 1.
4. **Split or reform.** The alliance either loses a wing or changes its rules to give that wing more say.

### Coalitions as treaties without enforcement

A coalition has no executor, no shared wallet and no in-game rules. It is a set of promises between alliances, of the kind MMO401 week 8 called trust exchanges: one side helps now in return for help later. Game theory from MMO303 week 10 predicts when such promises hold. Cooperation is stable when each alliance expects to keep dealing with the others long enough that breaking a promise costs more than it gains. Coalitions therefore last while the shared enemy lasts, and they break when the enemy is gone or when one member sees a large one-time gain from betrayal.

### What the developer controls

You do not write alliance politics. You write the tools politics runs on:

| Tool | Effect on player government |
|---|---|
| Permission granularity | Sets the achievable K for each action |
| Audit logs | Makes Ostrom's principle 4 (accountable monitors) possible |
| Bills and upkeep | Creates duties, and so creates the B-R5RB failure mode |
| Delays on irreversible actions | Turns hijacks into contests others can see and stop |
| Cost of leaving a group | Sets member corporations' switching cost, and so the need for councils |
| Size caps on groups | Pushes players to build unenforced coalitions above the cap |

The last row deserves a note. If you cap guild size to keep groups manageable, players who want more scale will build an alliance of guilds outside your tools, with worse security and no logs. A cap does not stop large governments. It moves them into chat servers you cannot see.

## In-class activity (25 minutes)

In pairs, design the permission system for guilds in a new MMO with shared guild halls and a guild treasury that pays weekly upkeep on the hall.

1. List five guild actions, from minor (edit the message of the day) to severe (disband the guild, spend the whole treasury). For each, estimate `H` and `L` on a 0 to 100 scale (6 minutes).
2. Assume a typical guild has `N = 6` officers, `q = 0.05`, and `a = 0.5`. Use the interactive to choose `K` for each action. Mark which actions are duties that should be "any of N" (10 minutes).
3. For the two most severe actions, add one rate limit or delay that lets you lower `K` without raising risk. State the new numbers (5 minutes).
4. Swap with another pair and find one action in their design that a single traitor can still abuse (4 minutes).

Expected output: a table of five actions with `H`, `L`, `K` and any limits, plus one weakness found by the other pair.

## Common misconceptions

- **"More keys is always safer."** More keys lowers hijack risk and raises the risk that nothing happens in time. Past `K ≈ N × a`, a group mostly loses the ability to act. The B-R5RB battle is the cost of inaction, not of theft.
- **"The alliance leader rules the alliance."** The game gives the executor corporation real powers, but corporations can leave. Leaders who ignore their council see the exit cascade from week 1.
- **"A bigger council is slower."** At the same `K`, yes. But a bigger council supports a higher `K` at the same timeliness. With `q = 0.1` and `a = 0.6`, 3-of-7 is both safer and faster than 2-of-5 (see Check yourself).
- **"Player government only exists in sandbox games."** Any game with shared guild resources has it. A raid guild with a loot council is a small government with a constitution, even if it is a pinned message.

## Check yourself

1. With `q = 0.1` and `a = 0.6`, compute `P(hijack)` and `P(timely)` for a 3-of-7 rule. Compare them with 2-of-5.
2. A guild has 4 officers who are each online when needed with `a = 0.3`. The hall's upkeep is paid by one designated treasurer. What is the chance the payment is missed? What if any of the four can pay?
3. For `N = 5`, `q = 0.1`, `a = 0.6` and `H = 100`, how large must `L` be before 1-of-5 has a lower expected cost than 2-of-5?
4. A designer proposes "disbanding a guild requires all officers to agree." Using the model, describe what happens when an officer quits the game without handing over their rank. What single tool would fix it?

<details>
<summary>Answers</summary>

1. 3-of-7: `P(hijack) = P(at least 3 traitors of 7) ≈ 2.57%`, `P(timely) = P(at least 3 available of 7) ≈ 90.37%`. 2-of-5 gives 8.15% and 91.30%. The bigger council is about three times safer for a one-point loss in timeliness.
2. One treasurer misses with probability `1 − 0.3 = 70%`. With any of four, the miss chance is `0.7^4 = 24.0%`. Still too high for a duty with a large `L`, so add a warning and a longer payment window, which raises `a`.
3. The costs are equal when `100 × 0.40951 + L × 0.01024 = 100 × 0.08146 + L × 0.08704`. So `32.805 = 0.0768 × L` and `L ≈ 427`. Lateness would have to cost more than four times a hijack.
4. Unanimity (`K = N`) needs every officer, so one absent officer makes `P(timely) = 0` forever. The guild can never disband, or never do anything else protected by that rule. Fix it with an inactivity rule: officers who have not logged in for a set period lose their key, which lowers `N` to the active officers.

</details>

## Lab / assignment hook

[Lab 02, keys to the vault](../labs/lab02.md). You build a small calculator for K-of-N rules, then design and defend the full permission table for a guild system, including at least one rate limit and one duty handled as "any of N." Deliverable: the calculator, the permission table and a 400-word design memo.

## Sources

- EVE University Wiki, "Alliance" (accessed September 2026). Executor corporation needs support from CEOs of at least 50% of member corporations; its powers over applications, standings and the maintenance bill; dissolution at downtime if the bill is unpaid; one billion ISK founding cost.
- Wikipedia, "Battle of B-R5RB" (accessed September 2026). 27-28 January 2014; missed payment by an N3/Pandemic Legion corporation; 7,548+ characters, 717 corporations, 55 alliances; 75 titans; about 11 trillion ISK, estimated at US$300,000-330,000; 21 hours, ended by maintenance downtime.
- Wikipedia, "Eve Online" (accessed September 2026). The 2009 Band of Brothers collapse: a disgruntled director contacted Goonswarm, stripped assets and disbanded the alliance.
- Groen, A. (2016). *Empires of Eve: A History of the Great Wars of EVE Online*. Lightburn Industries. Band of Brothers' formation and history, 2003-2009.
- Warcraft Wiki, "Guild bank" (accessed September 2026). Introduced in patch 2.3; per-tab, per-rank permissions and withdrawal limits.
- Ostrom, E. (1990). *Governing the Commons: The Evolution of Institutions for Collective Action*. Cambridge University Press. The eight design principles, paraphrased here. Nobel Prize in economics, 2009.
- Buchanan, J. M. & Tullock, G. (1962). *The Calculus of Consent*. University of Michigan Press. External costs, decision costs and the choice of voting rule.
- Mnookin, J. L. (1996). "Virtual(ly) Law: The Emergence of Law in LambdaMOO." *Journal of Computer-Mediated Communication* 2(1). Two-to-one ballot margin.
- Andresen, G. (2011). BIP 11, "M-of-N Standard Transactions." github.com/bitcoin/bips.

## Interactive spec: examples/w02-keys-to-the-vault.html

**The one insight.** As K rises, hijack risk falls geometrically while timeliness holds up and then collapses near `K = N × a`. The cheapest rule depends on how costly lateness is, and pure duties want "any of N."

**Layout.** Control strip on top. Two stacked panels: probabilities against K (top), expected cost against K (bottom). A numbers table beneath with one row per K. At 390px everything stacks; the table scrolls inside its own container, never the page.

**Controls.**
- `N` officers: integer slider 1 to 12, default 5.
- `q` traitor probability: 0 to 0.5, step 0.01, default 0.10.
- `a` availability: 0.05 to 1, step 0.01, default 0.60.
- `H` hijack cost: 0 to 200, step 5, default 100.
- `L` lateness cost: 0 to 200, step 5, default 10.
- Preset buttons: "Guild (5, 0.10, 0.60)", "Big council (7, 0.10, 0.60)", "Upkeep duty (L = 50)".
- Toggle "log scale" for the hijack axis (on by default).

**Formulas.**
- `tail(N, K, p) = Σ_{j=K}^{N} C(N, j) p^j (1 − p)^(N − j)`, computed exactly with integer binomial coefficients.
- `P(hijack) = tail(N, K, q)`; `P(timely) = tail(N, K, a)`.
- `cost(K) = H × P(hijack) + L × (1 − P(timely))`.
- Duty line: `P(missed duty, any of N) = (1 − a)^N`, shown as a single readout.
- Reference marker at `K = N × a` (may be fractional).

**Top panel.** Horizontal axis K from 1 to N (discrete points joined by lines). Two series: `P(hijack)` (left axis, log scale from 0.0001% to 100%, or linear when the toggle is off) and `P(timely)` (right axis, linear 0 to 100%). Vertical dashed marker at `N × a` labelled "expected officers available."

**Bottom panel.** Expected cost against K as bars, the minimum bar highlighted and labelled "best K". Ties go to the smaller K.

**Table.** Columns K, P(hijack) to 3 decimals in percent, P(timely) to 2 decimals in percent, cost to 2 decimals.

**Test values.**
- N = 5, q = 0.1, a = 0.6: K = 1 gives 40.951% and 98.98%; K = 2 gives 8.146% and 91.30%; K = 3 gives 0.856% and 68.26%; K = 4 gives 0.046% and 33.70%; K = 5 gives 0.001% and 7.78%.
- With H = 100, L = 10: costs 41.05, 9.02, 4.03, 6.68, 9.22, best K = 3.
- With H = 100, L = 50: costs 41.46, 12.50, 16.73, 33.20, 46.11, best K = 2.
- N = 7, K = 3: 2.569% and 90.37%.
- Duty readout for N = 5, a = 0.6: 1.024%.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Series differ by dash style as well as color. All sliders keyboard operable with visible focus. No animation when reduced motion is set. No game logos or art.
