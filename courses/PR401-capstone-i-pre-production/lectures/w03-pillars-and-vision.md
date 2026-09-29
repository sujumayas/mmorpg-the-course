# PR401 · Week 03 — Pillars and Vision

**Why this matters:** Every team says it has pillars. Few teams check whether their plan spends any time on them. A pillar that gets 10% of the hours is a slogan, and a feature that serves no pillar is where your PR402 crunch will come from. This week you write the vision and pillars for the capstone and then audit them against the hours in your plan, the way a lead would before greenlight.

**You will be able to:**
- Write a one-sentence vision, two to four pillars and at least two anti-pillars for an MMO-scope pitch.
- Compute each pillar's share of feature hours and the orphan share from a feature list with pillar weights.
- Revise a feature list until every pillar clears its minimum share and orphans fall under the limit, and state what was cut.
- Write one playtest question per pillar that a prototype in week 4 or 5 can answer.

**Before class:** Reread [PR201 week 2, pillars and scope](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w02-pre-production-pillars-and-scope.md), section 3 (writing pillars that decide things, 10 minutes). Read [MMO406 week 1, setting as system](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w01-setting-as-system.md), sections 1 and 3 (25 minutes). Bring your week 1 pitch, your claims sheet, and a first feature list with rough hour estimates from each discipline's primary.

**Prerequisites from earlier courses:** [GD101 week 14](../../GD101-introduction-to-game-design/lectures/w14-design-documents-one-pagers-and-pitch.md) for the pillar-mechanic map. [PR201 week 2](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w02-pre-production-pillars-and-scope.md) for the three rules of a working pillar and the scope sheet. [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) for the cut line. Looking ahead, [MMO406 week 1](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w01-setting-as-system.md) (next semester) covers making the setting explain the systems. From this course, [week 1](w01-pitch-development.md) (the content budget) and [week 2](w02-market-analysis.md) (the positioning sentence).

---

## 1. Vision, pillars and anti-pillars

Three layers, each shorter than the last is long.

The **vision** is one sentence that says what a player will feel and do, for whom. It comes out of your week 2 positioning. "For players who left sandbox MMOs because towns felt empty, *Emberfall* is a small world where everything you use was made by someone you know."

A **pillar** is a short promise that lets you say no to a feature. PR201 week 2 gave three rules: at least one pillar is about players together, each pillar can be tested in a playtest, and each pillar rules something out. A capstone adds one more. **At least one pillar must depend on persistence**, something that only works because the world remembers. If every pillar would hold in a session-based co-op game, your server architecture is supporting nothing on the sheet.

An **anti-pillar** is something the game deliberately will not do, even though players of your comparables might expect it. "No solo story campaign." "No auction house that works across towns." Anti-pillars are cheap to write and save hours every week, because they end arguments before they start.

*Emberfall* pillars:

- **P1. Everything you use, someone made.** No vendor sells gear. Every tool and weapon comes from a player's crafting.
- **P2. Towns are held together.** A town is claimed, stocked and defended by a group across sessions. (Persistence and together.)
- **P3. Danger has a price.** Death costs something, and players can put a price on other players.

Anti-pillars: no solo story campaign; no global market; no character power bought with money.

## 2. Worked example: where do the hours actually go?

### The hook

*Albion Online* launched in July 2017 as a sandbox MMO in which, in Wikipedia's summary, all equipment and items are made by other players. That one promise decides a large part of the studio's plan. If no vendor sells gear, then gathering, refining, crafting, markets and the transport of goods all have to work and be balanced before anything else matters. The pillar is not a line in a document. It is a claim on the budget.

Student teams write pillars in week 3 and a feature list in week 3, and never put the two side by side. When they do, they usually find that the biggest single feature serves no pillar at all.

### The model

List every **feature** `f` in the plan with its estimated hours `h_f`. Leave out **foundation** work that every game needs whatever its pillars (login, persistence layer, networking, build pipeline), and list it separately. For each feature, give a weight `w_fp` to each pillar `p` it serves. Weights for one feature sum to 1, or to 0 if it serves no pillar.

```
share_p   = Σ_f h_f × w_fp / Σ_f h_f          pillar p's share of feature hours
orphan    = Σ_f h_f × (1 − Σ_p w_fp) / Σ_f h_f  share serving no pillar
passes    ⇔ every share_p ≥ s_min  and  orphan ≤ o_max
```

- `s_min = 0.20` for three pillars. With `k` pillars, a reasonable minimum is about `0.6 / k`: every pillar gets at least 60% of an equal split.
- `o_max = 0.10`. Some orphan work is honest (a settings menu). A lot of it means the plan is serving something the pillars do not name.
- Weights are a judgement by the team. Assign them together, quickly, and argue only over the large features.

### Numbers you can check

*Emberfall*'s first feature list, 540 feature hours in all.

| Feature | Hours | P1 | P2 | P3 | Orphan hours |
|---|---|---|---|---|---|
| Gathering nodes and tools | 60 | 1 | | | 0 |
| Crafting stations and recipes | 90 | 1 | | | 0 |
| Town market stall | 70 | 0.5 | 0.5 | | 0 |
| Town claim and shared storage | 80 | | 1 | | 0 |
| Town siege event | 60 | | 0.5 | 0.5 | 0 |
| Death drop and insurance | 40 | | | 1 | 0 |
| Solo story questline | 90 | | | | 90 |
| Character customization | 50 | | | | 50 |
| **Share of 540 h** | | **34.3%** | **26.9%** | **13.0%** | **25.9%** |

Check P3 by hand. `60 × 0.5 + 40 × 1 = 70` hours, and `70 / 540 = 13.0%`. The orphan share is `(90 + 50) / 540 = 25.9%`.

Two failures. P3 is below 20%, so "danger has a price" is a promise the plan barely funds. And more than a quarter of feature hours serve nothing on the sheet. The solo questline is the single biggest item after crafting, and it contradicts an anti-pillar the team wrote the same afternoon.

The team made three changes:

1. **Cut the solo questline to a 25-hour tutorial chain** that teaches gathering and crafting by having new players make their first tool. It now serves P1 fully.
2. **Cut customization from 50 to 20 hours.** Keep it as an honest orphan, with a note.
3. **Add a 45-hour bounty board** where players post rewards for a named player killer. It serves P3 fully.

| Feature list | Total h | P1 | P2 | P3 | Orphan |
|---|---|---|---|---|---|
| First draft | 540 | 34.3% | 26.9% | 13.0% | 25.9% |
| Revised | 490 | 42.9% | 29.6% | 23.5% | 4.1% |

Check the revised P3. `60 × 0.5 + 40 + 45 = 115` hours, and `115 / 490 = 23.5%`. The revised plan passes, and it is 50 hours smaller. Those 50 hours go back into the week 1 budget, where *Emberfall* was short of replay for keen players. Cutting orphans rarely costs the vision anything. It usually pays for a pillar.

The lab 03 checker computes these shares from `features.csv`.

The list leaves out foundation work, as the model says, and that includes combat for the two classes and the dungeon instance. Week 6 adds the foundation back when it checks the plan against capacity, and week 9 costs the dungeon's content.

### The same idea elsewhere

**Public pillars of shipped games.** *Mortal Online 2*'s Steam description leads with a player-driven economy, housing, crafting and full-loot PvP. *Pantheon: Rise of the Fallen* calls itself a "deeply social" MMORPG that challenges players. Each of those phrases is a claim on the budget in the same way. A game that promises full-loot PvP has to fund death, loot and anti-griefing work before it funds anything cosmetic.

**GD101 week 14.** The pillar-mechanic map drew lines from pillars to mechanics. The share table is the same map with hours on the lines. A pillar with thin lines on the map will have a small share here.

**Budgeting outside games.** Any organisation that states priorities and then publishes a budget invites the same check: does the money follow the stated priorities? The share table is that check for a feature list.

### Eyes-open judgment

The share test catches pillars that are unfunded. It cannot tell you whether the hours are well spent. A pillar can have 40% of the hours and still fail in the playtest because the features serving it are dull. Section 4 handles that.

Weights can be gamed. A team that wants its questline can give it `P2 = 0.3` because "players might do it together". Guard against this by asking one question for every partial weight: if we cut this feature, would the pillar be visibly weaker in the vertical slice? If not, the weight is 0.

Do not make the thresholds a ritual either. A two-pillar game with one dominant pillar (70/30) can be a strong design. Pick `s_min` and `o_max` deliberately and write them down, so the reviewer can see what you decided rather than what you forgot.

### Check yourself

1. The team adds a 60-hour "town decoration" feature to the revised list and weights it `P2 = 1`. Recompute all four shares. Does the list still pass?
2. A different team has four pillars. What `s_min` does the `0.6 / k` rule give? If their smallest pillar has 12%, how many hours must move to it on a 600-hour list?

<details><summary>Answers</summary>

1. Total 550 hours. P1 `210 / 550 = 38.2%`, P2 `(145 + 60) / 550 = 37.3%`, P3 `115 / 550 = 20.9%`, orphan `20 / 550 = 3.6%`. It still passes, but P3 is now barely above 20% and the plan is 60 hours larger. Check it against week 1 capacity before accepting it.
2. `0.6 / 4 = 0.15`. The pillar needs `0.15 × 600 = 90` hours and has `0.12 × 600 = 72`, so 18 hours must move to it (if total hours stay fixed).

</details>

## 3. Pillars and the setting

MMO406 week 1 argued that a setting does work: it explains why the systems are the way they are, so that players accept rules they would otherwise call arbitrary. Your pillars need that support. If *Emberfall* has no vendors, the world has to say why. Perhaps the Emberfall valley is cut off by ash storms and every nail is precious. Then P1 reads as the world, not as a design constraint, and players forgive the extra walking.

For each pillar, write one line of setting that makes it feel natural. Then check the reverse. Every major lore element you plan should serve at least one pillar, or it is an orphan too, just in words instead of hours. Keep the setting to one page this week. MMO406 has the tools for the full bible, and week 9 of this course will ask for it in the content plan.

The artist writes a second page beside it, the **art direction page**. It is the first version of the team's art bible: a palette, the shape language, a scale reference (a player beside a door, a stall and a town gate), and three or four reference images the team made itself or has the right to use. Tie each choice to a pillar or a setting line. "Salvaged, patched metal everywhere" follows from P1 and the ash storms. Add one readability rule, such as "a player's silhouette and town colours read at 30 metres", because week 4 turns that rule into a risk and week 12's slice quality bar dresses the slice town to this page.

## 4. A pillar you can test

A pillar that cannot fail a playtest cannot guide one. For each pillar write:

- **A question.** "Do players use items other players made, by choice?"
- **An observable.** What you will count or watch. "Share of equipped items crafted by a different player, at the end of session 2."
- **A threshold, set now.** "At least 50%." Write it before any prototype exists, so the data cannot move it.

These questions feed next week's risk list. A load-bearing pillar with no evidence is the same thing as a load-bearing claim tagged "assumed", and it goes to the top of the prototype queue. Week 5 shows how many testers you need to answer a question like this with a threshold.

## Studio session plan

The studio meets for 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:15 | Brief: the persistence rule, anti-pillars, the share audit | Questions answered |
| 0:15 to 0:50 | Vision and pillars. Each team drafts its vision from the week 2 positioning, two to four pillars and at least two anti-pillars. Pair with another team and try to break each pillar with a feature it fails to rule out | Draft `pillars.csv` |
| 0:50 to 1:20 | Feature list. Each discipline's primary lists its features with hours. The producer separates foundation work | Draft `features.csv` |
| 1:20 to 1:30 | Break | |
| 1:30 to 2:00 | Weights and audit. The team assigns weights feature by feature, runs the lab 03 checker, and reads the shares | First audit output |
| 2:00 to 2:30 | Revise. Cut, reshape or add features until the audit passes. Record every change and where the freed hours go | Passing audit, change log |
| 2:30 to 2:50 | Test questions. One question, observable and threshold per pillar | Pillar test lines |
| 2:50 to 3:00 | Round. Each team reads its vision, names its orphan share before and after, and its biggest cut | Instructor sign-off or a named concern |

## Deliverables

Due before next week's studio session, in `preproduction/week03/` in your team repository. The vision page and the art direction page go in `docs/vision.md` and `docs/art-direction.md`, because later weeks build on them.

- **Vision and pillars page** (one page): vision sentence, pillars, anti-pillars, one setting line per pillar.
- **Art direction page** (one page, the start of the art bible): palette, shape language, scale reference, reference images the team may use, and a readability rule, each tied to a pillar or setting line.
- **Pillar sheet** (`pillars.csv`) with each pillar's question, observable and threshold.
- **Feature sheet** (`features.csv`) with hours and weights, the foundation list, and the checker output before and after revision.
- **Change log** listing each cut or addition and where the freed hours went.
- **Claims sheet update.** Each pillar's test question appears as a claim.

See [lab 03](../labs/lab03.md).

## Common failure modes

- **Adjective pillars.** "Immersive", "epic", "social". Fix: rewrite each as a promise a feature could break.
- **No persistence pillar.** The pillars would fit a lobby game. Fix: name what only works because the world remembers.
- **Weights as wishes.** Every feature serves every pillar a little. Fix: apply the cut question to every partial weight.
- **Foundation hidden in features.** Networking and login are spread across pillar features and inflate them. Fix: list foundation separately, and check its size against week 1 capacity on its own.
- **Thresholds set after data.** Fix: commit `pillars.csv` with thresholds before the week 4 prototype starts. The commit date is the evidence.

## Review checklist

The instructor checks the vision milestone when:

- [ ] The vision is one sentence and comes from the week 2 positioning.
- [ ] Two to four pillars, at least one about players together and one that depends on persistence.
- [ ] At least two anti-pillars, each of which rules out something a comparable does.
- [ ] `check_pillars.py` prints `PASS`, with `s_min` and `o_max` stated.
- [ ] The change log shows what was cut and where freed hours went.
- [ ] Every pillar has a question, an observable and a threshold committed before week 4.
- [ ] Each pillar has a setting line, and the setting page has no orphan lore of any size.
- [ ] The art direction page exists, and each choice on it names the pillar or setting line it serves.

## Sources

- Wikipedia, "Albion Online" (accessed September 2026). Sandbox Interactive; full release 17 July 2017; all equipment and items made by players; player-driven economy.
- Steam store pages for *Mortal Online 2* (app 1170950) and *Pantheon: Rise of the Fallen* (app 3107230), short descriptions, accessed 29 September 2026. Store descriptions change; the phrases cited are from that date.
- PR201 week 2 and GD101 week 14 in this repository for pillar rules and the pillar-mechanic map.
- The *Emberfall* pillars, features, hours and weights, and the thresholds `s_min = 0.20` and `o_max = 0.10`, are invented for teaching or are course conventions.
