# PR401 · Week 10 — Social Systems Plan

**Why this matters:** Your social features will run with a few dozen people online, not thousands. A town, a guild or a group activity that needs four people at the same moment works in a big MMO by sheer numbers and fails in yours by arithmetic. This week you size every social system against the population you will really have, and you write the safety rules that must exist before strangers can talk to each other in your world.

**You will be able to:**
- Write a social systems plan that covers grouping, towns or guilds, communication, trade trust, conflict rules and player safety, each tied to a pillar.
- Compute the probability that a group of a given size has enough members online at a given hour, from membership, play time and the number needed.
- Choose between the four levers (a bigger pool, more time online, fewer people needed, a set time) to make a social system work at your population, and name what each costs players.
- Specify the minimum safety features for a public launch, with an owner for each.

**Before class:** Reread [MMO305 week 3, forced vs voluntary grouping](../../MMO305-social-systems-and-online-behaviour/lectures/w03-forced-vs-voluntary-grouping.md), section 3 (20 minutes). Read [MMO305 week 4, guilds](../../MMO305-social-systems-and-online-behaviour/lectures/w04-guilds-formation-lifecycle-leadership.md), section 1 (15 minutes). Skim [MMO402 week 6, moderation at scale](../../MMO402-emergent-society-governance-and-ethics/lectures/w06-moderation-at-scale.md). Bring your week 2 launch audience (`D` and peak CCU), the week 8 player-type table and your week 3 pillars.

**Interactive:** [Town defence odds](../examples/w10-town-defence.html). Use it during section 4.

**Prerequisites from earlier courses:** [MMO305 week 8](../../MMO305-social-systems-and-online-behaviour/lectures/w08-griefing-typology-and-design-responses.md) (griefing and design responses). [MMO305 week 10](../../MMO305-social-systems-and-online-behaviour/lectures/w10-communication-design-chat-emotes-pings.md) (communication design). [MMO305 week 11](../../MMO305-social-systems-and-online-behaviour/lectures/w11-newcomers-and-mentoring-systems.md) (newcomers). [MMO302 week 10](../../MMO302-mmo-server-architecture/lectures/w10-chat-guild-and-social-services.md) (chat and guild services). [MMO307 week 10](../../MMO307-game-balance-ii-pvp-progression-and-endgame/lectures/w10-matchmaking-quality-vs-queue-time.md) (queue size and wait). [MMO402 week 11](../../MMO402-emergent-society-governance-and-ethics/lectures/w11-minors-in-online-worlds.md) (minors). [MA102 week 6](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md) (the binomial distribution). Looking ahead, [MMO405 week 10](../../MMO405-research-methods-in-online-games/lectures/w10-ethics-and-irb.md) (next semester) covers consent when you study your players.

---

## 1. What the social plan covers

The social plan answers one question for each system: what do players do with or against each other, and what makes them do it? For a capstone it has six parts.

1. **Grouping.** How players find each other for an activity, how big a group is, and whether grouping is forced or voluntary (MMO305 week 3).
2. **Long-lived groups.** Guilds, towns, companies: how they form, what they own, how they end (MMO305 week 4).
3. **Communication.** Channels, emotes, pings, and what each channel costs the server (MMO305 week 10, MMO302 week 10).
4. **Trade and trust.** How players exchange items and how they know they will not be cheated. For *Emberfall* that is the market stall and the trade window.
5. **Conflict rules.** Where and when players can hurt each other, what it costs, and how griefing is limited. *Emberfall*'s pillar P3 (danger has a price) lives here.
6. **Safety.** Reporting, blocking, moderation and the rules strangers agree to (section 3).

Each part names the pillar it serves. A social system that serves none is a cost with no reason, and week 6's rule applies: it goes on the cut list.

## 2. Population is a design input

In a large MMO, a social system rarely fails for lack of people. Someone is always online to join the group, buy the item or defend the keep. That is **liquidity**: enough of the right people available at the same moment. Your capstone does not have it by default.

Week 2 set a target peak of about 60 concurrent players for *Emberfall*, and week 8 guessed 100 players in the launch week. Those numbers decide which social designs are possible. A 20-player raid needs a third of the peak crowd in one place. A five-role group finder with a 1-in-8 tank rate forms a group only as often as tanks arrive, as MMO307 week 10 showed for queues. A guild of 40 will have three people online on a Tuesday afternoon.

So every social system in the plan needs one number: how many of the right people must be online at the same time for it to work, and how often that happens. Section 4 computes it for *Emberfall*'s towns.

## 3. Safety before strangers

PR402 puts your world in front of the public. Before strangers can talk to each other, the following must exist. They are the course minimum, and the week 14 review will check each one.

| Feature | Minimum | Owner |
|---|---|---|
| Code of conduct | One page, shown and accepted at account creation, with the sanction ladder | Producer |
| Report | In-game report on any player and any chat line, with a reason and the context captured automatically | Server programmer |
| Block and mute | Per player, persistent across sessions, takes effect immediately without a server round trip to a moderator | Gameplay programmer |
| Chat filter | Profanity and slur filter on by default, with an opt-out for adults | Gameplay programmer |
| Moderation rota | A named team member on call for every hour the server is open to the public, with a response target for reports | Producer |
| Sanctions | Mute, kick, temporary ban and permanent ban, each logged with who applied it and why (MMO402 week 7) | Server programmer |
| Age policy | A minimum age, stated and enforced at sign-up, and a decision on what data you collect from anyone under 18 (MMO402 week 11) | Producer |
| Data and consent | What telemetry you collect, why, how long you keep it, and consent for any research use (DB201 week 13, MMO405 week 10) | Producer |

Two notes. First, the moderation rota is real work, and it belongs in week 11's production plan. A team of seven with the server open four hours every evening for four weeks has 112 rota hours to cover. Second, conflict rules and safety are different things. A player who kills another in a raid window is playing the game. A player who follows someone across the map to kill them twenty times is griefing, and MMO305 week 8's typology helps you write the rule that tells them apart.

## 4. Worked example: can a town defend itself at 8 p.m.?

### The hook

Before December 2009, World of Warcraft players formed five-player dungeon groups from their own realm, mostly by asking in chat. On a busy realm at peak hours that worked. On a quiet realm, or late at night, the healer you needed might not be online at all. Patch 3.3.0, released on 8 December 2009, added the Dungeon Finder, which formed groups across every realm in a battlegroup. It did not make any player more willing to heal. It made the pool larger.

In patch 4.1.0, on 26 April 2011, Blizzard added Call to Arms, which gives a bonus reward to whichever role is least represented in the queue, usually tanks or healers. That lever does something different. It raises the chance that a given player shows up in the scarce role.

Both are answers to the same question you face with *Emberfall*'s towns. Pillar P2 says towns are held together: claimed, stocked and defended by a group. A town raid needs defenders online when it starts. Will they be?

### The model

A town has `M` members. At a given hour, each member is online with probability `p`. The town needs at least `m` defenders online to hold a raid. If members log in independently,

```
P(defended) = P(X ≥ m),   X ~ Binomial(M, p)
            = 1 − Σ_{j=0}^{m−1} C(M, j) × p^j × (1 − p)^(M − j)
```

- `C(M, j)` is the number of ways to choose `j` members out of `M`.
- `p` comes from play time. If a member plays `h` hours a week and a share `e` of it falls in a window of `W` hours a week, then during that window `p = e × h / W`.

Every social system with a "need `m` of `M` at once" rule has this shape: a group finder, a guild raid night, a town defence.

### Numbers you can check

*Emberfall*'s launch players average `h = 0.4 × 3 + 0.35 × 5 + 0.2 × 12 + 0.05 × 25 = 6.6` hours a week, from the week 8 player types. The team assumes 80% of play falls in the evening window, 19:00 to 22:00, which is 21 hours a week.

```
evening:   p = 0.8 × 6.6 / 21  = 0.25
off-peak:  p = 0.2 × 6.6 / 147 = 0.009
```

The draft design has 90 of the 100 launch players in six towns of 15, and a raid needs 4 defenders.

| Town size `M` | Expected online (evening) | `P(≥ 4)` evening | `P(≥ 4)` off-peak | `P(≥ 2)` evening |
|---|---|---|---|---|
| 6 | 1.5 | 0.04 | 0.00 | 0.47 |
| 10 | 2.5 | 0.22 | 0.00 | 0.76 |
| 15 | 3.75 | 0.54 | 0.00001 | 0.92 |
| 20 | 5.0 | 0.77 | 0.00003 | 0.98 |
| 30 | 7.5 | 0.96 | 0.00015 | 1.00 |

Check the draft cell by hand. `M = 15`, `p = 0.25`, `m = 4`. The chance of 0, 1, 2 or 3 online is `0.75^15 + 15 × 0.25 × 0.75^14 + 105 × 0.25² × 0.75^13 + 455 × 0.25³ × 0.75^12`. That is `0.0134 + 0.0668 + 0.1559 + 0.2252 = 0.4613`, so `P(≥ 4) = 0.539`.

Read it.

- **The draft is a coin flip.** A town of 15 can put four defenders in the field on about half of evenings. Expected online is 3.75, just under the 4 needed. Players will learn that defending is luck, and P2 stops meaning anything.
- **Off-peak raids are always undefended.** Even a town of 30 has a 0.015% chance of four members online at 4 a.m. If raids can start at any hour, the town that raids at dawn always wins. That is not a strategy players enjoy on either side.
- **Bigger towns work, but there are fewer of them.** Towns of 25 reach 90% in the evening. With 90 players that means three or four towns, not six, and fewer rivals means fewer raids.

The four levers, in the model's terms:

1. **Raise `M` (a bigger pool).** Fewer, larger towns. Costs rivalry and the sense of a small town where everyone knows you.
2. **Raise `p` (more time online in the window).** Rewards for defending, like Call to Arms rewarding the scarce role. Costs little, and moves `p` a few points at most.
3. **Lower `m` (fewer people needed).** An NPC militia that fills two defender slots, so two humans can hold. With `m = 2`, a town of 15 holds 92% of evenings.
4. **Fix the window.** Let each town choose a two-hour raid window inside the evening, so `p` is always the evening value. Off-peak raids simply cannot start.

*Emberfall* uses levers 1, 3 and 4. It builds four towns, the slice town plus three more (week 11 costs them), so its 90 town players make towns of about 22. At `M = 22`, four defenders are online on 84% of evenings, better than the draft but still short of the 0.9 guide. So each town also chooses a raid window inside 19:00 to 22:00, and a militia of two NPC defenders scales down as human defenders arrive. With `m = 2`, a town of 22 holds 99% of evenings (0.985). The plan records one more rule. A town with fewer than 10 members cannot be claimed, because at `M = 10` even `m = 2` holds only 76% of evenings.

### Cross-game recognition

- **World of Warcraft, Dungeon Finder (2009).** Pooling realms raised `M`, the number of players the finder could draw from, without changing anyone's behaviour.
- **World of Warcraft, Call to Arms (2011), and Final Fantasy XIV's "In Need" bonus.** Both reward whichever role the queue lacks. In this model they raise `p` for the scarce role.
- **EverQuest, mercenaries (Seeds of Destruction, 2008).** NPC companions that join a group in place of a human, added because players found it harder to find others of the right level. That lowers `m`, exactly as *Emberfall*'s militia does.
- **Guild Wars 2, dynamic events.** Open-world events scale to whoever is present and reward each participant without a party, as MMO305 week 3 describes. That sets `m = 1`: the activity works with whoever turns up.

### Eyes-open judgment

The binomial model assumes members log in independently. Friends do not. They log in together, which makes both full evenings and empty ones more likely than the model says. A town of 15 made of three friend groups of five is closer to three members than fifteen. Ask your vertical slice testers who they play with, and treat the table as optimistic for small towns.

Each lever costs something. The militia makes defence possible and makes it less about the town. If two NPCs can hold the gate, P2's "held together" has become "held by the server". *Emberfall* caps the militia at two and removes one for each human defender who arrives, so the humans always matter. Fixed raid windows remove the dawn raid and also remove surprise. Decide which of these your pillars can afford.

Finally, the population numbers are week 2's guesses. If launch brings 40 players instead of 100, four towns of 22 become four towns of 9, under the claim minimum, and even the militia holds a town of 9 on fewer than three evenings in four. Write the fallback now: at what population do towns merge, and who decides?

## 5. From plan to backlog

Every social system in the plan becomes backlog items for week 11, with the server work MMO302 week 10 describes. For *Emberfall*: town membership and roles, the raid window setting, the militia, town chat, the report and block features, the moderation tools and the rota. Estimate them the way you estimated week 6's features, and check them against the fit ratio. Social features are easy to underestimate because each looks small. Check your PR301 tracker for how many hours chat and grouping really took.

## Studio session plan

Week 10 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:25 | Six-part social plan drafted on one page, each part tied to a pillar | Draft `docs/social-plan.md` |
| 0:25-1:05 | Liquidity sheet: every "need `m` of `M` at once" system, with `p` from your player types (lab 10) | `liquidity.csv` and checker run |
| 1:05-1:15 | Break | |
| 1:15-1:45 | Levers: for every system under 80%, choose a lever and state its cost to players | Revised rows with responses |
| 1:45-2:20 | Safety: fill the section 3 table with owners; draft the code of conduct; plan the moderation rota hours | `safety.csv` and rota hours |
| 2:20-2:45 | Red team: another team plays griefers against your conflict rules on paper and tries to break the trade window | List of holes with owners |
| 2:45-3:00 | Backlog: social features estimated and handed to the producer for week 11 | Estimates added to the plan |

## Deliverables

Due at the start of week 11, in `docs/social-plan.md` and `preproduction/week10/`:

1. **Social systems plan**: the six parts, each tied to a pillar, with the fallback rule for low population.
2. **Liquidity and safety sheets** in the [lab 10](../labs/lab10.md) format. The checker `social_check.py` must print `PASS`.
3. **Code of conduct** (one page) and the moderation rota with hours.
4. **Social backlog**: every social feature estimated, ready for the week 11 production plan.

## Common failure modes

- **Designing for a population you will not have.** A 20-player raid in a world of 60. Compute the liquidity first.
- **Assuming play is spread across the day.** It is not. Use an evening window and an off-peak rate, and decide what happens off-peak.
- **The militia that plays the game.** NPC help that makes human players unnecessary. Cap it and scale it down as players arrive.
- **Safety as a stretch goal.** Report and block are not polish. Without them you cannot open the server to strangers.
- **No one on call.** A report button that sends reports nowhere is worse than none. Name the person for every open hour.
- **Collecting data you cannot justify.** Chat logs, IP addresses and play times are personal data. Say what you keep, why and for how long.

## Review checklist

The instructor checks in the submission and at the week 11 stand-up:

- [ ] The social plan has all six parts, each tied to a pillar.
- [ ] Every system that needs several players at once has a liquidity row, and `social_check.py` prints `PASS`.
- [ ] Every row under 80% has a lever chosen, with its cost to players stated.
- [ ] Off-peak behaviour is decided for every conflict system.
- [ ] A low-population fallback is written, with a trigger and a decision owner.
- [ ] Every safety feature in section 3 has an owner, and the rota covers every open hour.
- [ ] The code of conduct exists and is shown at sign-up.
- [ ] Social features are estimated and in the backlog for week 11.

## Sources

- Warcraft Wiki, "Patch 3.3.0" (accessed September 2026). Released 8 December 2009; cross-realm Dungeon Finder connecting the realms in each battlegroup. https://warcraft.wiki.gg/wiki/Patch_3.3.0
- Warcraft Wiki, "Call to Arms (dungeon)" (accessed September 2026). Introduced in patch 4.1.0 on 26 April 2011; a reward satchel for queuing in the least represented role. https://warcraft.wiki.gg/wiki/Call_to_Arms_(dungeon)
- Final Fantasy XIV Online Wiki (consolegameswiki), "Duty Roulette" (accessed September 2026). "In Need" bonus for the role most needed in a roulette. https://ffxiv.consolegameswiki.com/wiki/Duty_Roulette
- Wikipedia, "EverQuest" (accessed September 2026). Seeds of Destruction (2008) introduced mercenaries that join groups in place of human players, in response to growing difficulty finding group members.
- MMO305 week 3 of this program, for Guild Wars 2's dynamic events and its sources.
- The *Emberfall* population, play-time split, town sizes and raid rules are invented for teaching and continue weeks 1 to 9. The safety minimums are this course's requirements.

## Interactive spec: examples/w10-town-defence.html

**The one insight:** the average number of members online can sit just below what a town needs while the chance of having enough swings from near zero to near certain, and each design lever moves a different term.

**Layout.** Two linked views, side by side at 1280px, stacked at 390px.

- **Left: the distribution.** A bar chart of `P(X = j)` for `j = 0` to `M`, members online. Bars at or above `m` in the "defended" color, the rest in a neutral color. A vertical line at the mean `M × p`. The shaded total is printed as `P(defended)`.
- **Right: P(defended) against M.** x-axis town size `M` from 2 to 40. y-axis 0 to 1. Two lines: evening `p` and off-peak `p`. A horizontal guide at 0.8 and 0.9. The current `M` is marked. Beneath the chart, the number of towns the population supports, `floor(players in towns / M)`.

**Controls.** Sliders for town size `M` (2 to 40), defenders needed `m` (1 to 8), average weekly hours `h` (1 to 20, step 0.1), evening share `e` (0.5 to 1.0, step 0.05), evening window `W` (7 to 42 hours a week), players in towns (20 to 200). A militia toggle with a size slider (0 to 3) that lowers `m` by the militia size, with a floor of 1. Buttons "Emberfall draft" and "Emberfall final" that set the values below.

**Formulas.** `p_evening = e × h / W`. `p_offpeak = (1 − e) × h / (168 − W)`. `P(X ≥ m) = 1 − Σ_{j=0}^{m−1} C(M, j) p^j (1 − p)^(M − j)`, computed with a numerically stable loop (multiply successive terms by `(M − j) / (j + 1) × p / (1 − p)`).

**Test values.** Draft: `h = 6.6`, `e = 0.8`, `W = 21`, `M = 15`, `m = 4`, 90 players: `p_evening = 0.251`, `P = 0.54`, mean 3.77, 6 towns; off-peak `p = 0.009`, `P ≈ 0.00001`. Set `M = 25`: evening `P = 0.91`, 3 towns. Final: `M = 22`, militia 2 (so `m = 2`), 90 players: evening `P = 0.986`, 4 towns; with the militia off, `P = 0.84`. Set `M = 15` with militia 2: `P = 0.92`. Set `M = 10` with militia 2: `P = 0.76`. Use `p = 0.25` exactly to reproduce the guide's table: `M = 15`, `m = 4` gives 0.539.
