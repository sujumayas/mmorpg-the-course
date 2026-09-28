# MMO303 · Question bank

MMO303 has no written exam. The course grade is problem sets (30%), the combat simulator (30%) and the final balance pass (40%). This bank feeds those three components in three ways.

- **Problem sets.** Each weekly problem set adds two or three questions from this bank to the lab (see [problem-sets-brief.md](problem-sets-brief.md)). Students receive them with new numbers, and the worked solutions here are the marking guide. Keep this file on the instructor side.
- **Quizzes.** The first ten minutes of some lab sessions are an ungraded quiz of two questions, used to check the class before the lab starts.
- **Vivas.** The simulator and the final balance pass each end with a short oral examination. Examiners pick questions from this bank that touch the student's own submission, and change the numbers on the spot.

Every question carries a tag with the week or weeks it draws on and one of four types.

- **compute**: apply a lecture model to new numbers and get a number out.
- **explain**: say why a model behaves as it does, in words, with at least one number.
- **design**: choose values or rules that meet a stated goal.
- **critique**: judge someone else's claim, proposal or note against a model.

All game settings are fictional unless the question names a shipped game, and those formulas are the ones cited in the matching lecture. Answers were recomputed for this bank. Rounding follows the lectures, usually to one decimal or three significant figures. Instructors changing numbers for a viva should rerun the arithmetic, not scale the old answer.

---

## Week 1: What "balanced" means

1. **[W01 · compute]** A six-spec ladder has pick shares of 30%, 25%, 20%, 10%, 10% and 5%. Compute `N_eff` and HHI. How many equally popular specs would produce the same concentration?

   <details>
   <summary>Answer</summary>

   `Σ p² = 0.09 + 0.0625 + 0.04 + 0.01 + 0.01 + 0.0025 = 0.215`. `N_eff = 1 / 0.215 = 4.65`. HHI `= 10,000 × 0.215 = 2,150`. The ladder behaves like 4.65 equally popular specs, although six are played.

   </details>

2. **[W01 · compute]** A spec shows a 52.5% observed win rate, and 35% of its games are mirrors. What is its non-mirror win rate? Is it inside a 48-53% viability band?

   <details>
   <summary>Answer</summary>

   `w = (observed − 0.5m) / (1 − m) = (0.525 − 0.175) / 0.65 = 0.538`, so 53.8%. It is outside the band on the high side. The observed number hid a spec that is too strong.

   </details>

3. **[W01 · critique]** A producer writes: "Every one of our eight specs won between 49% and 52% in the top bracket last week, so the top bracket is balanced." The top bracket's pick shares were 45%, 15%, 10%, 8%, 7%, 6%, 5% and 4%. The 45% spec showed 51.8% observed with 30% mirrors. Critique the claim with numbers.

   <details>
   <summary>Answer</summary>

   The claim uses win rate, which measures viability, and says nothing about diversity. `Σ p² = 0.254`, so `N_eff = 3.94` of 8. With one spec at 45%, `N_eff` can never exceed `1 / 0.45² = 4.94`, whatever the others do. The top spec's mirror-corrected rate is `(0.518 − 0.15) / 0.70 = 52.6%`, still inside the band but near its top edge, and its popularity means its observed rate understates it. The bracket passes a viability test and fails a diversity test. A good reply names both numbers and asks which target the producer meant.

   </details>

4. **[W01 · compute]** A raid boss has 9,000,000 health and a 5-minute enrage. The raid, at median play, deals 31,500 DPS. A patch nerfs one spec, which supplies 25% of the raid's damage, by 10%. Does the raid still clear? What is the largest nerf to that spec the raid can absorb?

   <details>
   <summary>Answer</summary>

   Required DPS is `9,000,000 / 300 = 30,000`. The spec supplies `0.25 × 31,500 = 7,875` DPS and loses 787.5, so the raid does 30,712.5 and still clears. The margin is 1,500 DPS, so the largest absorbable nerf is `1,500 / 7,875 = 19.0%`. A 5% tuning margin let one spec lose almost a fifth of its damage without a failed clear.

   </details>

## Week 2: Armor and damage mitigation

5. **[W02 · compute]** A game uses `A / (A + K)` with `K = 300`. How much armor gives 40% mitigation? What is the EHP multiplier there? How much armor doubles survival time?

   <details>
   <summary>Answer</summary>

   `A / (A + 300) = 0.4` gives `A = 0.4 × 300 / 0.6 = 200`. EHP multiplier `1 + 200/300 = 1.67`. Survival doubles at `A = K = 300`.

   </details>

6. **[W02 · compute]** In classic-era World of Warcraft (attacker levels 1-59), armor reduces physical damage by `A / (A + 400 + 85 × level)`, capped at 75%. A tank has 2,500 armor. Compute the reduction against a level 40 attacker and a level 55 attacker. How much armor would reach the cap against the level 55 attacker?

   <details>
   <summary>Answer</summary>

   Level 40: `K = 400 + 3,400 = 3,800`, reduction `2,500 / 6,300 = 39.7%`. Level 55: `K = 400 + 4,675 = 5,075`, reduction `2,500 / 7,575 = 33.0%`. The cap needs `A = 3K = 15,225`. The same armor is worth less against the stronger attacker because `K` grows with level.

   </details>

7. **[W02 · compute]** A character starts with 1,000 HP and 0 armor, `K = 100`. Health costs 2 gold per point and armor costs 40 gold per point. With 40,000 gold, what purchase maximizes EHP? Compare with spending everything on one stat.

   <details>
   <summary>Answer</summary>

   The optimum satisfies `HP × c_H = (A + K) × c_A`, so `2 HP = 40(A + 100)` and `HP = 20(A + 100)`. The budget is `2(HP − 1,000) + 40A = 40,000`. Substituting gives `80A + 4,000 = 42,000`, so `A = 475` and `HP = 11,500`. EHP `= 11,500 × 5.75 = 66,125`. All health gives 21,000 HP and EHP 21,000. All armor gives 1,000 armor and EHP `1,000 × 11 = 11,000`. The balanced split is more than three times better than either extreme.

   </details>

8. **[W02 · compute]** Path of Exile 2 armour reduces a hit by `armour / (armour + 10 × damage)`, capped at 90%. A character has 2,000 armour. Compute the reduction and the damage taken for hits of 100, 500 and 2,000.

   <details>
   <summary>Answer</summary>

   100: `2,000 / 3,000 = 66.7%`, takes 33.3. 500: `2,000 / 7,000 = 28.6%`, takes 357.1. 2,000: `2,000 / 22,000 = 9.1%`, takes 1,818.2. No hit reaches the cap. Armour is strong against many small hits and weak against one large one because `K = 10 × damage`.

   </details>

9. **[W02 · critique]** A designer proposes "each point of armor reduces damage by 0.5%, capped at 75%" because players find the divisive formula confusing. Predict player behavior and name the cost. Then propose a presentation fix that keeps the divisive formula.

   <details>
   <summary>Answer</summary>

   The cap is reached at 150 armor, and every point past it is worthless, so players stack to exactly 150 and stop. Below the cap each point is worth more than the last in survival terms, because going from 70% to 75% cuts damage taken by a sixth. Items with armor become dead stats for capped players and builds converge. The cap also fixes the EHP multiplier at 4×. The fix is to keep `A / (A + K)` and show players EHP, or "survives N more hits," on the tooltip, since EHP is linear in armor and reads as constant value.

   </details>

## Week 3: Effective HP and effective DPS

10. **[W03 · compute]** A 2,500 HP character (`K = 100` for armor and MR) has 300 resist points and faces damage that is 70% physical and 30% magic. Find the EHP-maximizing split and its EHP. Compare all-armor, a proportional 210/90 split and an even 150/150 split.

    <details>
    <summary>Answer</summary>

    `√0.7 = 0.837`, `√0.3 = 0.548`, `S = 1.384`, `S² = 1.917`. `A* + K = 500 × 0.837 / 1.384 = 302.2`, so armor 202.2 and MR 97.8. `EHP* = 2,500 × 500 / (100 × 1.917) = 6,522`. All-armor has `m = 0.7 × 0.25 + 0.3 = 0.475`, EHP 5,263. Proportional 210/90 gives 6,515, within 0.1% of the optimum. Even 150/150 gives 6,250. The square-root rule puts slightly more into armor than the proportional split, and the peak is flat.

    </details>

11. **[W03 · compute]** With `K = 100` and a resist budget of 400, below what share of magic damage should a character buy no MR at all?

    <details>
    <summary>Answer</summary>

    All-armor is optimal when `w_m / w_p < (K / (K + R))² = (100/500)² = 0.04`. So `w_m < 0.04 / 1.04 = 3.85%`. A larger budget pushes the threshold down, because more armor makes each extra armor point less valuable relative to the first MR point.

    </details>

12. **[W03 · compute]** A tank with 12,000 HP faces 600 raw physical DPS (`K = 100`) and has a healer providing 180 HPS. How much armor makes the tank unkillable? What is time to die at 150 armor, with and without the healer?

    <details>
    <summary>Answer</summary>

    Unkillable when `600 × 100 / (100 + A) ≤ 180`, so `A ≥ 233.3`. At 150 armor, damage taken is `60,000 / 250 = 240` per second. Without the healer TTD is `12,000 / 240 = 50` s. With the healer it is `12,000 / (240 − 180) = 200` s. The healer quadruples survival at this armor, and 83 more armor makes the tank immortal.

    </details>

13. **[W03 · compute]** A class has sheet DPS 120, 90% hit chance, 25% crit chance with a 1.75× multiplier and 85% uptime. Compute its pre-defense eDPS, and its eDPS against a target with 60 armor and one with 30 armor (`K = 100`, physical damage).

    <details>
    <summary>Answer</summary>

    Crit factor `1 + 0.25 × 0.75 = 1.1875`. Pre-defense eDPS `= 120 × 0.9 × 1.1875 × 0.85 = 109.0`. Against 60 armor it deals `109.0 × 100/160 = 68.1`. Against 30 armor it deals `109.0 × 100/130 = 83.9`.

    </details>

14. **[W03 · compute, design]** Class X has 1,500 HP, 50 armor, 30 MR and 80 eDPS (physical). Class Y has 1,000 HP, 20 armor, 60 MR and 95 eDPS (magic). `K = 100`. Who wins the duel under the TTK matrix model? Give two single-number changes to Y that flip the result, and the size of each.

    <details>
    <summary>Answer</summary>

    X kills Y in `1,000 × 1.2 / 80 = 15.0` s. Y kills X in `1,500 × 1.3 / 95 = 20.5` s. X wins. Y wins if it kills X in under 15 s, which needs eDPS above `1,950 / 15 = 130`, a 36.8% buff. Or Y survives longer than 20.5 s, which needs physical EHP above `20.53 × 80 = 1,642`, so armor above 64.2 (from 20). The armor change is the smaller-looking number but is a 3.2× change to the stat. A good answer notes which one a player would notice more.

    </details>

15. **[W03 · compute]** A game adds a true-damage share of 15% to all incoming damage. What is the ceiling on EHP as a multiple of health? A 2,000 HP character with 100 armor and 100 MR (`K = 100`) faces an even physical/magic split of the remaining 85%. Compute its EHP.

    <details>
    <summary>Answer</summary>

    `m ≥ t`, so `EHP ≤ HP / 0.15 = 6.67 × HP`. Here `m = 0.85 × 0.5 + 0.15 = 0.575` and `EHP = 2,000 / 0.575 = 3,478`, down from 4,000 without true damage.

    </details>

## Week 4: Stacking mitigation

16. **[W04 · compute]** A tank has three layers, 35%, 25% and 15%, stacked multiplicatively. Compute the let-through fraction, the EHP multiplier and the total doublings. What multiplier would additive stacking give?

    <details>
    <summary>Answer</summary>

    `0.65 × 0.75 × 0.85 = 0.414`, so 41.4% gets through. `M = 2.41`. Doublings `= log2(2.41) = 1.27`, which equals `0.621 + 0.415 + 0.234`. Additive stacking gives 75% and `M = 4`.

    </details>

17. **[W04 · compute]** A boss hits for 80,000 raw every 30 seconds. The tank has 30,000 HP, a passive armor layer of 55% and a stance of 10%. How many doublings does the tank need to survive the hit from full health? Does the passive kit survive? What is the smallest cooldown reduction that makes it survive?

    <details>
    <summary>Answer</summary>

    Needed `M ≥ 80,000 / 30,000 = 2.67`, which is `log2(2.67) = 1.415` doublings. Passive let-through is `0.45 × 0.9 = 0.405`, `M = 2.47`, 1.304 doublings. It fails, since the tank dies at `30,000 / 0.405 = 74,074` raw. The cooldown must bring let-through down to `0.375`, a factor of `0.375 / 0.405 = 0.926`, so a reduction of at least 7.4% (0.111 doublings).

    </details>

18. **[W04 · compute]** A 2,500-damage hit meets a flat block of 400 and a 60% layer. Compute damage taken with the block before the layer and after it. Then a 3,000-point absorb sits after the layer. How much raw damage does it soak?

    <details>
    <summary>Answer</summary>

    Block first: `(2,500 − 400) × 0.4 = 840`. Layer first: `2,500 × 0.4 − 400 = 600`. The block is worth 160 raw damage in the first order and 400 in the second. The absorb soaks `3,000 / 0.4 = 7,500` raw damage.

    </details>

19. **[W04 · compute]** A tank has layers of 60%, 50% and a 30% cooldown, and the game has a total cap of 85% reduction. What EHP multiplier does the tank reach? By what factor does the cooldown actually raise survival, compared with the factor its tooltip implies?

    <details>
    <summary>Answer</summary>

    Uncapped let-through is `0.4 × 0.5 × 0.7 = 0.14`, 86% reduction, which the cap clips to 85%, so `M = 6.67` instead of 7.14. Without the cooldown, `M = 1 / 0.2 = 5`. The cooldown raises survival by `6.67 / 5 = 1.33`, not the `1 / 0.7 = 1.43` a 30% layer should give. The total cap silently shrank it.

    </details>

20. **[W04 · explain]** Explain why additive stacking is fairly safe for damage bonuses and dangerous for damage reduction. Use one number for each side.

    <details>
    <summary>Answer</summary>

    On offense an additive pool dilutes. With +200% already, another +20% takes the factor from 3.0 to 3.2, only 6.7% more damage, so growth slows by itself. On defense an additive pool concentrates. Four 20% layers leave 20% let-through and a fifth leaves 0%, so each layer is worth more than the last and the fifth grants immunity. The same rule brakes power on one side and runs away on the other.

    </details>

## Week 5: The holy trinity

21. **[W05 · compute]** Use the lecture's role table (tank 400 DPS, 60% mitigation, 6,000 HP; healer 100 DPS, 700 HPS, 20%, 3,000 HP; DPS 1,000 DPS, 20%, 3,000 HP). A 5-player boss has `H = 630,000`, `T = 200 s`, `B = 900`, `R = 250`, `S = 4,500`. Which compositions pass? Then `S` is lowered to 3,500. Which pass now?

    <details>
    <summary>Answer</summary>

    Damage check `630,000 / 200 = 3,150`. With a tank, needed healing is `900 × 0.4 + 250 = 610` and the tank takes `1,800` from the spike. Without a tank, needed healing is `900 × 0.8 + 250 = 970` and a DPS takes 3,600, more than its 3,000 HP. At `S = 4,500` only 1-1-3 passes (3,500 DPS, 700 HPS). 1-2-2 (2,600) and 2-1-2 (2,900) fail damage, and every tankless group fails the spike. At `S = 3,500` the tankless spike is 2,800 and survivable, so 0-2-3 also passes (3,200 DPS, 1,400 HPS against 970). 0-1-4 still fails healing (700 against 970). Two compositions pass, and one of them has no tank.

    </details>

22. **[W05 · compute]** A boss deals `B = 1,200` raw DPS to its target. A tank has 65% mitigation and every other role 20%. How much healing does one tank slot save, and what fraction of a 700 HPS healer is that?

    <details>
    <summary>Answer</summary>

    `1,200 × (0.65 − 0.20) = 540` HPS, which is `540 / 700 = 77%` of a healer. The tank also passes spike checks that no healing can, which this number does not count.

    </details>

23. **[W05 · compute]** A queue holds 120 tanks, 200 healers and 900 DPS, recipe 1-1-3. How many groups form and who waits? A hybrid class lets 108 waiting DPS switch to tanking. How many groups form now, and what is the new bottleneck?

    <details>
    <summary>Answer</summary>

    `min(120, 200, 300) = 120` groups. Tanks are the bottleneck, and 80 healers and 540 DPS wait. After the switch there are 228 tanks and 792 DPS, so `min(228, 200, 264) = 200` groups, and healers become the bottleneck. Fixing one scarce role exposes the next.

    </details>

24. **[W05 · compute]** A 25-player raid boss deals `R = 4,200` spread HPS after mitigation and `B = 2,500` raw DPS on its tank (60% mitigation). Healers produce 700 HPS each and the raid runs 3 tanks. How many healers are needed and how many DPS slots remain? Which number would you change to free two more DPS slots?

    <details>
    <summary>Answer</summary>

    Needed healing `2,500 × 0.4 + 4,200 = 5,200`, so 8 healers (5,600). DPS slots `25 − 3 − 8 = 14`. Freeing two slots means 6 healers (4,200 HPS), so `R` must fall to `4,200 − 1,000 = 3,200` or less. Lowering `B` cannot do it alone, since the tank's whole share is 1,000 of the 5,200, so `B` would have to fall to zero.

    </details>

25. **[W05 · design]** Starting from the lecture's default encounter (`H = 600,000`, `T = 180`, `B = 1,000`, `R = 200`, `S = 5,000`), change as few numbers as possible so that a tankless 0-1-4 group passes alongside 1-1-3. State the new numbers and the check each one fixes.

    <details>
    <summary>Answer</summary>

    Two numbers must move. The spike must be survivable by a 3,000 HP, 20% character, so `S ≤ 3,000 / 0.8 = 3,750`. One healer must cover the untanked boss, so `0.8B + 200 ≤ 700`, which gives `B ≤ 625`. 0-1-4 then deals 4,100 against 3,333 and passes. Lowering only one of the two leaves 0-1-4 failing the other check. 0-2-3 is not an alternative, since it deals 3,200 and fails damage.

    </details>

## Week 6: Threat, aggro and control

26. **[W06 · compute]** A tank generates 600 TPS with a 2,400 head start. A DPS generates 800 TPS. When does it pull aggro in melee range? At range?

    <details>
    <summary>Answer</summary>

    Melee: `k τT = 660`, `t = 1.1 × 2,400 / (800 − 660) = 18.9` s. Ranged: `k τT = 780`, `t = 1.3 × 2,400 / 20 = 156` s. The same player pulls eight times sooner in melee.

    </details>

27. **[W06 · compute]** A tank generates 650 TPS. What is the most raw damage per second a ranged DPS with a 0.7 threat modifier can deal forever? A melee DPS with the same modifier?

    <details>
    <summary>Answer</summary>

    Ranged: `1.3 × 650 / 0.7 = 1,207` damage per second. Melee: `1.1 × 650 / 0.7 = 1,021`. Head start does not enter the speed limit.

    </details>

28. **[W06 · compute]** A melee DPS pulls aggro at 15,000 threat while generating 1,000 TPS against an 800 TPS tank. The tank taunts. How long until the DPS pulls again? What did the taunt change, and what did it leave alone?

    <details>
    <summary>Answer</summary>

    `k τT = 880`. After the taunt both have 15,000, so `t = 0.1 × 15,000 / (1,000 − 880) = 12.5` s. The taunt reset the leader but not the slopes, so the DPS takes the boss again. Only lowering `τD` below 880, or raising `τT`, ends the problem.

    </details>

29. **[W06 · compute, design]** A tank deals 500 damage with a 1.5 threat modifier and 200 bonus TPS from abilities. The group is 1-1-3 with two melee and one ranged DPS at 1,200 raw each, the healer deals 100. The boss needs `720,000 / 180 = 4,000` group DPS. Compute the threat-limited group DPS. What tank threat modifier is the smallest that passes the check?

    <details>
    <summary>Answer</summary>

    `τT = 500 × 1.5 + 200 = 950`. Melee limit `1.1 × 950 = 1,045`, ranged limit `1.3 × 950 = 1,235`. Group DPS `= 2 × 1,045 + 1,200 + 500 + 100 = 3,890`, which fails 4,000. The melee players need a limit of at least 1,100, so `τT ≥ 1,000` and `500c + 200 ≥ 1,000`, which gives `c ≥ 1.6`. The ranged limit is then 1,300, above its 1,200, so it does not bind.

    </details>

30. **[W06 · design]** You want tanks to have a threat job in 5-player dungeons, and you never want a DPS to hold back more than 10% of its damage. The typical tank makes 1,000 TPS and the strongest DPS deals 1,500 raw with modifier 1.0. Pick melee and ranged thresholds `k` that meet both goals, or explain why no single `k` does.

    <details>
    <summary>Answer</summary>

    The strongest DPS may lose at most 10%, so its limit must be at least 1,350 TPS. That needs `k × 1,000 ≥ 1,350`, so `k ≥ 1.35` for anyone who deals 1,500. With `k = 1.35` to about 1.5, a 1,500 DPS player holds back 0-10% and weaker ones not at all, so threat binds only for the top players. Classic values (1.1 melee) would make the top melee player hold back 27%. A good answer also notes the other lever, raising the tank's multiplier, and that at `k ≥ 1.5` threat stops binding at all and the tank's threat job disappears.

    </details>

## Week 7: Healing throughput and mana economy

31. **[W07 · compute]** A healer has `M = 15,000` and `r = 30`. Balm heals 3,000 for 400 mana in 3.0 s. Rush heals 1,600 for 400 mana in 1.25 s. Compute each spell's HPS, MPS and HPM, the OOM time when casting each alone, the marginal HPM of moving from Balm to Rush, and the sustainable HPS at 90 s and 300 s.

    <details>
    <summary>Answer</summary>

    Balm: HPS 1,000, MPS 133.3, HPM 7.5. Rush: HPS 1,280, MPS 320, HPM 4.0. Rush alone lasts `15,000 / 290 = 51.7` s, Balm alone `15,000 / 103.3 = 145.2` s. Marginal HPM `= 280 / 186.7 = 1.5`. At 90 s, `B = 166.7 + 30 = 196.7`, region 2, `f = (196.7 − 133.3) / 186.7 = 0.339`, HPS `= 1,000 + 0.339 × 280 = 1,095`. At 300 s, `B = 80`, region 3, HPS `= 80 × 7.5 = 600`.

    </details>

32. **[W07 · compute]** The healer from question 31 faces a boss that deals 800 DTPS to the tank after mitigation. When does the hidden enrage clock start?

    <details>
    <summary>Answer</summary>

    Region 3 gives `7.5 × B = 800`, so `B = 106.7`, below Balm's MPS of 133.3, which confirms the region. `M / T = 76.7`, so `T = 195.7` s. After about 3 minutes 16 seconds the tank starts losing health.

    </details>

33. **[W07 · compute]** A designer adds Pulse to the question 31 kit: 1,400 healing, 250 mana, 1.5 s. Is it on the efficient frontier?

    <details>
    <summary>Answer</summary>

    Pulse has HPS 933.3, MPS 166.7, HPM 5.6. At 166.7 MPS the Balm-Rush segment reaches `1,000 + 1.5 × 33.3 = 1,050` HPS. Pulse sits 117 HPS below the frontier and has lower HPS than Balm while burning more mana, so no fight length makes it right. It is a trap button.

    </details>

34. **[W07 · compute, explain]** The question 31 healer gains a cooldown that restores 3,000 mana once per 60 s. Treat it as extra regeneration. How does it change sustainable HPS in a 30-second fight and in a very long fight? Why the difference?

    <details>
    <summary>Answer</summary>

    Averaged, it adds `3,000 / 60 = 50` mana per second, so `r = 80`. In a 30 s fight `B = 500 + 30 = 530`, above Rush's 320, so the healer was already limited by casting time and stays at 1,280 HPS. The cooldown adds nothing. In a very long fight output settles at `r × HPM_Balm`, which rises from `30 × 7.5 = 225` to `80 × 7.5 = 600`. Regeneration only helps once the mana budget binds.

    </details>

## Week 8: Crowd control and diminishing returns

35. **[W08 · compute]** Under `m = (1, 0.5, 0.25, 0)`, a target takes stuns of 2 s, 5 s and 7 s in that order within one reset window. Compute total stun time. What order maximizes it, and by how much?

    <details>
    <summary>Answer</summary>

    Given order: `2 + 2.5 + 1.75 = 6.25` s. Longest first (7, 5, 2): `7 + 2.5 + 0.5 = 10.0` s, 3.75 s more. This is the rearrangement inequality. Pair the largest durations with the largest multipliers.

    </details>

36. **[W08 · compute]** Compute the uptime ceiling for a 5-second stun under `m = (1, 0.5, 0)` with `R = 20`, and under `m = (1, 0.5, 0.25, 0)` with `R = 18`.

    <details>
    <summary>Answer</summary>

    First rule: `7.5 / (7.5 + 20) = 27.3%`. Second rule: `8.75 / (8.75 + 18) = 32.7%`.

    </details>

37. **[W08 · compute]** A League of Legends champion has two tenacity sources in the same group, 35% and 25%, and one 10% source in another group. Groups add. How long do a 3-second stun and a 0.6-second stun last?

    <details>
    <summary>Answer</summary>

    Same group: `1 − 0.65 × 0.75 = 0.5125`. Adding the other group gives 0.6125. The 3 s stun lasts `3 × 0.3875 = 1.16` s. The 0.6 s stun would last 0.23 s, but the 0.3 s floor applies, so 0.3 s.

    </details>

38. **[W08 · compute]** A team deals 2,000 DPS to a target with 30,000 EHP. The target heals itself for 800 HPS whenever it is not controlled. Compute time to kill at control fractions `u = 0`, `0.3` and `0.5`.

    <details>
    <summary>Answer</summary>

    Net damage `= 2,000u + 1,200(1 − u) = 1,200 + 800u`. `u = 0`: 25.0 s. `u = 0.3`: 1,440 net, 20.8 s. `u = 0.5`: 1,600 net, 18.75 s. Full control would give 15.0 s. Every point of uptime is worth 800 HPS of denied healing.

    </details>

39. **[W08 · design]** You want a 4-second stun to have an uptime ceiling of exactly 25%. Find `R` under `m = (1, 0.5, 0.25, 0)` and under `m = (1, 0.5, 0)`. Which would you ship, and why?

    <details>
    <summary>Answer</summary>

    Under the three-step list, total is `1.75 × 4 = 7` s, so `7 / (7 + R) = 0.25` gives `R = 21` s. Under the two-step list, total is 6 s, so `R = 18` s. Both give the same ceiling. The two-step rule makes each chain shorter and resets sooner, so players see control more often in smaller bursts. The three-step rule gives longer chains and rarer cycles. Either is defensible if the answer names what the player experiences.

    </details>

## Week 9: Intransitivity and counters

40. **[W09 · compute]** Knight beats Ranger 65%, Mage beats Knight 58%, Ranger beats Mage 62%. Compute the stable mix.

    <details>
    <summary>Answer</summary>

    `a = 0.30` (Knight over Ranger), `b = 0.16` (Mage over Knight), `c = 0.24` (Ranger over Mage), total 0.70. Knight `c / 0.70 = 34.3%`, Mage `a / 0.70 = 42.9%`, Ranger `b / 0.70 = 22.9%`.

    </details>

41. **[W09 · compute, critique]** From the symmetric launch (all favorable links 60%, one third each), a patch raises Mage over Knight to 68%. Compute week-1 win rates at the old mix and the new stable mix. Which class will players complain about in week 1, and which class grows in the long run?

    <details>
    <summary>Answer</summary>

    Week 1: Knight `(0.50 + 0.32 + 0.60) / 3 = 47.3%`, Mage `(0.68 + 0.50 + 0.40) / 3 = 52.7%`, Ranger `(0.40 + 0.60 + 0.50) / 3 = 50.0%`. Players complain about the Mage. New stable mix with `a = 0.2`, `b = 0.36`, `c = 0.2`: Knight 26.3%, Mage 26.3%, Ranger 47.4%. The Ranger, which counters the Mage, grows. The Mage ends up rarer than at launch.

    </details>

42. **[W09 · compute]** For question 41's patch, run one replicator step with `η = 1` from one third each. Give each class's `E` and new share.

    <details>
    <summary>Answer</summary>

    `E(Knight) = (−0.36 + 0.20) / 3 = −0.053`, `E(Mage) = (0.36 − 0.20) / 3 = +0.053`, `E(Ranger) = (−0.20 + 0.20) / 3 = 0`. New shares: Knight 31.6%, Mage 35.1%, Ranger 33.3%. Mages rise first, as the week-1 dashboard suggested, before Rangers overtake them.

    </details>

43. **[W09 · design]** Design a five-class counter graph with no dominant and no dominated class. Say what the stable mix is when every favorable link is 60%, and what happens to that property if you make it six classes.

    <details>
    <summary>Answer</summary>

    Number the classes 0 to 4 and let class `i` beat classes `i + 1` and `i + 2` (mod 5). Each beats two and loses to two, a regular tournament. With equal links, symmetry gives every class `E = 0` at 20% each. Six classes cannot do this, because each class plays five others and cannot beat exactly half. You then need even matchups, uneven link strengths or counters between compositions instead of classes.

    </details>

## Week 10: Payoff matrices and Nash equilibria

44. **[W10 · compute]** Four classes have this doubled-margin matrix (row against column).

    | | A | B | C | D |
    |---|---|---|---|---|
    | A | 0 | +0.30 | −0.20 | +0.10 |
    | B | −0.30 | 0 | +0.20 | −0.05 |
    | C | +0.20 | −0.20 | 0 | +0.25 |
    | D | −0.10 | +0.05 | −0.25 | 0 |

    Is any class strictly dominated? Solve the equilibrium of what remains and check the removed class earns less against it.

    <details>
    <summary>Answer</summary>

    Compare A and D column by column: 0 > −0.10, +0.30 > +0.05, −0.20 > −0.25, +0.10 > 0. A dominates D. The rest is a triangle with A over B `a = 0.3`, B over C `b = 0.2`, C over A `c = 0.2`. Shares follow `(b, c, a) / 0.7`: A 28.6%, B 28.6%, C 42.9%. Against this mix A, B and C each earn 0, and D earns `−0.10 × 0.286 + 0.05 × 0.286 − 0.25 × 0.429 = −0.121`. D stays out.

    </details>

45. **[W01, W10 · compute]** Compute `N_eff` of the equilibrium in question 44 and of the stable mix in question 40. What does each tell a designer?

    <details>
    <summary>Answer</summary>

    Question 44: `1 / (0.286² + 0.286² + 0.429²) = 2.88` effective classes from a roster of four. Question 40: `1 / (0.343² + 0.429² + 0.229²) = 2.83` of three. The first number exposes the dominated class, which costs a full class of diversity. The second shows unequal links costing only a small amount of diversity. Equal links would give 3.00.

    </details>

46. **[W10 · compute]** Two guilds meet at a world boss worth 12 points. Fighting costs each guild 8, and each wins a fight half the time. Yielding gives half value next spawn, 6. Find the mixed-equilibrium contest probability and each guild's expected payoff.

    <details>
    <summary>Answer</summary>

    Both contest: `12 × 0.5 − 8 = −2` each. If the other contests with probability `p`, Contest pays `−2p + 12(1 − p)` and Yield pays `6(1 − p)`. Setting equal gives `12 − 14p = 6 − 6p`, so `p = 0.75`. Each guild expects `6 × 0.25 = 1.5` points, against 6 each if both always yielded.

    </details>

47. **[W10 · compute]** From the launch triangle (all 60/40), a patch nerfs Knight over Ranger to 56/44. Compute the new equilibrium shares. What happens to the Knight's share, and why?

    <details>
    <summary>Answer</summary>

    `a = 0.12`, `b = c = 0.2`, total 0.52. Knight `b / 0.52 = 38.5%`, Ranger `c / 0.52 = 38.5%`, Mage `a / 0.52 = 23.1%`. Nerfing the Knight's winning edge raised its share, because fewer Mages are needed to hold it at break-even.

    </details>

48. **[W10 · critique]** The meta dashboard shows Knight at 25% of duels (the lowest), Mage at 50%, Ranger at 25%, all classes at 50% overall win rate. Matchups are Knight over Ranger 70%, the other links 60%. A designer proposes buffing Knight over Ranger to 75% "because nobody plays Knight." Critique the proposal and suggest what to change instead.

    <details>
    <summary>Answer</summary>

    The dashboard is already at equilibrium, since all overall win rates are 50%. The Knight is rare because the Mage, its counter, is common, not because it is weak. The buff raises `a` to 0.5, and the new equilibrium is Knight `0.2 / 0.9 = 22.2%`, Mage 55.6%, Ranger 22.2%. Knights become rarer still. To raise the Knight's share, strengthen the link it is not in, Ranger over Mage, or weaken the Mage's edge over the Knight.

    </details>

## Week 11: Lanchester's laws and group combat

49. **[W11 · compute]** Twenty players fight sixteen, all identical with 120 DPS and 1,500 HP, aimed fire. Compute the winners' survivors under the square law and the linear law, and the fight length under the square law.

    <details>
    <summary>Answer</summary>

    Square: `sqrt(400 − 256) = 12` survivors. Linear: `20 − 16 = 4`. Kill rate `k = 120 / 1,500 = 0.08`, so `t_end = artanh(16/20) / 0.08 = 1.0986 / 0.08 = 13.7` s.

    </details>

50. **[W11 · compute]** Nine defenders face twelve attackers. Design an outnumbered buff that lets them tie. Give it as an equal DPS and HP percentage, and as a DPS-only percentage.

    <details>
    <summary>Answer</summary>

    Strength ratio `144 / 81 = 1.778`. Equal DPS and HP buffs must each be `sqrt(1.778) = 1.333`, so +33.3% to both. DPS alone must be +77.8%. A flat 20% damage bonus would close less than a quarter of the gap.

    </details>

51. **[W11 · compute]** Seven veterans with 1.3× DPS and 1.25× HP fight nine ordinary players (100 DPS, 1,000 HP). Who wins under the square law, and how many of the winners survive?

    <details>
    <summary>Answer</summary>

    Veteran strength `1.3 × 1.25 × 49 = 79.6`, ordinary `81`. The ordinary side wins narrowly. Veterans kill at `α = 130 / 1,000 = 0.13` per second and ordinary players at `β = 100 / 1,250 = 0.08`. Survivors `= sqrt(81 − (0.13/0.08) × 49) = sqrt(1.375) = 1.2`, so about one ordinary player survives, badly hurt.

    </details>

52. **[W11 · explain]** A game has area skills that hit at most 5 targets. Explain which Lanchester law governs a 30-player blob against a 20-player group and why. Then say what changes if the cap is removed.

    <details>
    <summary>Answer</summary>

    With the cap, each area skill kills at a rate that no longer grows once the enemy has more than 5 alive, so each attacker's kill rate is fixed. That is aimed fire, and the square law applies. Strength is `900 : 400`, so the blob wins by a factor of 2.25. Without the cap, each attacker's damage scales with how many enemies stand in the area, which gives the linear law. Then strength is `30 : 20`, and the smaller group can win with better quality or position. The cap decides which law runs large fights.

    </details>

53. **[W11 · critique]** A PvP team reports "fights with two healers per side last forever" and proposes raising healing by 20% "so healers feel better." Using the lecture's 10-versus-6+2 table, where the winner flips between 200 and 250 HPS per healer, critique the proposal for healers currently at 200 HPS.

    <details>
    <summary>Answer</summary>

    200 HPS is next to the threshold, where fights are longest (37.1 s in the table). A 20% buff moves healers to 240, inside the flip region, so fights near the threshold get longer still or flip to the healing side. The complaint is a stalemate, and the proposal moves toward it. Better levers are a PvP-only healing reduction or a healing-reduction effect for attackers, which move healers below the threshold. A good answer quotes the table's fight lengths.

    </details>

## Week 12: Stat weights and theorycrafting

54. **[W12 · compute]** Using the week 12 class (5% base crit, 0% base haste, 40 rating per 1%, `m = 2`), a character has 2,000 power, 800 crit rating and 400 haste rating. Compute DPS and the normalized crit and haste weights. Which stat should the player buy next?

    <details>
    <summary>Answer</summary>

    Crit 25%, haste 10%. DPS `= 2,000 × 1.25 × 1.10 = 2,750`. Crit weight `= 2,000 / (4,000 × 1.25) = 0.400`. Haste weight `= 2,000 / (4,000 × 1.10) = 0.455`. Buy haste.

    </details>

55. **[W12 · compute]** Same class, 1,000 power and 2,400 secondary rating. Find the best crit/haste split, the DPS there and the weights at that point.

    <details>
    <summary>Answer</summary>

    Equal factors: `1.05 + crit/4000 = 1 + haste/4000` with `crit + haste = 2,400`, so `haste − crit = 200`. Crit 1,100, haste 1,300. Both factors are 1.325, DPS `= 1,000 × 1.325² = 1,755.6`. Both weights are `1,000 / (4,000 × 1.325) = 0.189`.

    </details>

56. **[W12 · compute]** The character in question 55 takes a talent that sets `m = 2.5`. Find the new best split and DPS. How much DPS does the player lose by keeping the old 1,100/1,300 split?

    <details>
    <summary>Answer</summary>

    The crit factor is `1 + 1.5c = 1.5(0.667 + c)`. Setting `0.667 + c = 1 + h` with `c = 0.05 + x/4000` and `h = (2,400 − x)/4000` gives `x = 1,767` crit rating and 633 haste. Then `c = 49.2%`, `h = 15.8%`, DPS `= 1,000 × 1.7375 × 1.1583 = 2,012.6`. The old split gives 1,970.9, which is 2.1% lower.

    </details>

57. **[W12 · compute]** A Path of Exile character has 150% increased damage and no more modifiers. It can take 40% increased or 25% more. Which is larger, and by how much?

    <details>
    <summary>Answer</summary>

    40% increased takes the factor from 2.5 to 2.9, a 16.0% gain. 25% more is a 25% gain. Take the more modifier.

    </details>

58. **[W12 · compute]** A damage-over-time effect lasts 10 s and ticks every `2 / (1 + h)` seconds. At 0% haste it ticks 5 times. How much haste rating (40 per 1%) earns a sixth tick? What is the stat weight of haste for this effect just below and just above that point?

    <details>
    <summary>Answer</summary>

    Six ticks need an interval of at most `10 / 6 = 1.667` s, so `1 + h ≥ 1.2`, `h = 20%`, which is 800 rating. Just below, extra haste adds nothing to this effect, so its weight is zero. Crossing 800 adds a whole tick, 20% more damage from the effect. A weight measured with a small delta near 800 is either zero or very large depending on the side.

    </details>

59. **[W12 · compute]** A sim measures stat gains for `Δ = 100` with a per-run standard error of 10 DPS. Crit gains 40 DPS, haste gains 34. Treat the two gains as independent. Can you rank them? How large a `Δ` do you need for the gap to reach twice its own standard error, if the gains scale linearly?

    <details>
    <summary>Answer</summary>

    Each gain is a difference of two runs, error `sqrt(2) × 10 = 14.1`. The gap between the gains has error `sqrt(2) × 14.1 = 20`. A 6 DPS gap is 0.3 standard errors, so no ranking. The gap grows at 0.06 DPS per point of `Δ`, so reaching 40 DPS takes `Δ ≈ 667`. That is large enough to blur any cap or breakpoint, so more iterations may be the better fix.

    </details>

## Week 13: Combat simulators

60. **[W13 · compute]** A class hits 50 times in a 75-second fight for `D = 120`, crit chance 30%, crit multiplier 2. Compute mean DPS and the standard deviation of single-fight DPS.

    <details>
    <summary>Answer</summary>

    `μ = 50 × 120 × 1.3 / 75 = 104.0`. `σ = 120 × sqrt(50 × 0.3 × 0.7) / 75 = 120 × 3.240 / 75 = 5.18`.

    </details>

61. **[W13 · compute]** The class from question 60 is compared with another whose single-fight SD is 4.0, and the true gap is 1.0 DPS. How many fights per class do you need for the 95% interval of the difference to be narrower than the gap?

    <details>
    <summary>Answer</summary>

    `σ_diff = sqrt(5.18² + 4.0²) = 6.55`. `N = (1.96 × 6.55 / 1.0)² = 164.7`, so 165 fights per class.

    </details>

62. **[W13 · compute]** Your simulator runs the question 60 class for 5,000 fights and reports a mean of 104.3 with SD 5.2. Is that consistent with the closed form? How many fights would pin the mean within 0.5% at 95%?

    <details>
    <summary>Answer</summary>

    `SE = 5.18 / sqrt(5,000) = 0.073`, so the 95% band is `104.0 ± 0.14`. The reported 104.3 is 4.1 standard errors high while the SD matches. Look for a bug that adds damage without adding spread, such as an extra hit or a fight-end off-by-one. For ±0.5% (±0.52 DPS), `N = (1.96 × 5.18 / 0.52)² = 382` fights.

    </details>

63. **[W13 · critique]** A balance report reads "Class X 101.2 DPS, Class Y 100.1 DPS (50 fights each). X is overtuned; nerf 1%." Each class has a single-fight SD of 5. Critique the report and say what it should contain.

    <details>
    <summary>Answer</summary>

    `SE_diff = sqrt(25 + 25) / sqrt(50) = 1.0`, so the 1.1 DPS gap is 1.1 standard errors. A gap that size appears by chance about 27% of the time when the classes are equal. The report gives no error bars, no seed, no policy and no fight style. It needs `μ̂ ± 1.96 SE` for each class, about `(1.96 × 7.07 / 1.1)² = 159` fights per class to resolve a 1.1 gap, and common random numbers if it compares two versions of one class. It should also check the result against a closed-form case before anyone acts on it.

    </details>

64. **[W13 · explain]** Explain why common random numbers shrink the error of a buff comparison, and give one way to write a simulator that breaks them.

    <details>
    <summary>Answer</summary>

    With the same stream, fight 17 has the same crit rolls in both versions, so the shared noise cancels in the difference and only the effect of the change remains. `σ_diff` falls far below `sqrt(σ_A² + σ_B²)`. A simulator breaks this when the two versions consume random numbers in different orders, for example one shared generator for all actors, or a buff that adds a proc roll only in the new version. Then every later roll shifts. One generator per actor, and a fixed number of draws per action, keeps the streams aligned.

    </details>

## Week 14: Communicating balance changes

65. **[W14 · compute]** A patch line reads "Ember Lash: 30/45/60/75 ⇒ 40/50/60/70." The ability also deals 3% of the target's maximum health, unchanged, and the target has 1,500 health. Compute the change to the whole ability at each rank. The ability is 20% of a rank-4 player's damage. What is that player's total change?

    <details>
    <summary>Answer</summary>

    The %HP part is 45 at every rank. Rank 1: `85 / 75 − 1 = +13.3%`. Rank 2: `95 / 90 − 1 = +5.6%`. Rank 3: 0%. Rank 4: `115 / 120 − 1 = −4.2%`. The rank-4 player's total is `0.2 × −4.2% = −0.8%`.

    </details>

66. **[W14 · compute]** Crit chance is 15% and crits deal 2× damage. Compute the change in expected damage if a note means "crit chance 15% ⇒ 20%" and if it means "crit chance increased by 5% (relative)."

    <details>
    <summary>Answer</summary>

    Points: factor 1.15 to 1.20, `+4.3%`. Relative: 15% to 15.75%, factor 1.1575, `+0.65%`. The same words describe changes six times apart in size. Write "15% ⇒ 20%".

    </details>

67. **[W14 · compute]** A sniper deals 95 per body shot, and the common health pool is 300. The proposed buff is 100. Compute shots to kill before and after, and the percentage changes in damage and in shots.

    <details>
    <summary>Answer</summary>

    `⌈300 / 95⌉ = 4` and `⌈300 / 100⌉ = 3`. Damage rises 5.3%, shots to kill fall 25%. The note must say "three body shots now defeat 300-health heroes."

    </details>

68. **[W14 · compute]** A spec's damage is 45% ability A, 35% ability B and 20% ability C. The patch reduces A by 8%, raises B by 6% and raises C by 15%. Is the spec buffed or nerfed overall, and by how much?

    <details>
    <summary>Answer</summary>

    `0.45 × −8% + 0.35 × 6% + 0.20 × 15% = −3.6% + 2.1% + 3.0% = +1.5%`. The note with the largest single number is a nerf, and the spec is buffed.

    </details>

69. **[W14 · critique]** Critique this note and rewrite it to the five-part checklist: "Berserker: Frenzy bonus increased by 5%. Rage generation adjusted."

    <details>
    <summary>Answer</summary>

    "Increased by 5%" is ambiguous between 30% ⇒ 35% (points) and 30% ⇒ 31.5% (relative). "Adjusted" gives no direction or value. There is no context, no audience, no intended effect and no statement of what did not change. A rewrite: "Berserker. Frenzy damage bonus 30% ⇒ 35%. Rage generation per hit 10 ⇒ 12. Context: Berserkers fall 5% behind other melee in fights with movement. Intended effect: about +2% total damage in single-target play (simulated, ±0.3%, 300 s). Frenzy duration and internal cooldown are unchanged." The exact numbers are the student's, but every part must be present.

    </details>

## Across weeks

70. **[W03, W07 · compute]** The week 7 Mend and Surge healer (`M = 10,000`, `r = 20`) heals a 20,000 HP tank in a 240-second fight, sustaining 493.3 HPS. The boss deals 1,200 raw physical DPS, `K = 100`, and the tank has 120 armor. Does the tank survive the fight? How much armor makes it unkillable?

    <details>
    <summary>Answer</summary>

    Damage taken is `1,200 × 100 / 220 = 545.5` per second, a deficit of 52.1. TTD `= 20,000 / 52.1 = 384` s, longer than the fight, so the tank survives with about 7,500 HP left. Unkillable needs `120,000 / (100 + A) ≤ 493.3`, so `A ≥ 143.2`. A deficit is not a death if the fight ends first, which is why fight length links healer mana and tank armor.

    </details>

71. **[W12, W14 · compute]** A spec's damage bonus while Fury is active goes from 25% to 30%. 40% of the spec's damage is dealt while Fury is active. What is the change to damage during Fury, and to total damage? What would a careless note reader think it was?

    <details>
    <summary>Answer</summary>

    During Fury the multiplier goes from 1.25 to 1.30, `δ = +4.0%`. Total `= 0.4 × 4.0% = +1.6%`. A careless reader sees "+5%" (points) or "+20%" (relative to the bonus). The honest intended-effect line says about +1.6% total.

    </details>

72. **[W04, W14 · explain]** A patch lowers a boss's magic resistance, and players ask whether this "buffs casters by the same percent" in every raid. Use multiplicative layers to explain what the patch does to relative damage changes computed from other lines in the same notes.

    <details>
    <summary>Answer</summary>

    Resistance is a multiplicative layer, so it scales old and new caster damage by the same factor and cancels in any `δ` computed from another line, as it did for Zac's W. The resistance change itself is a separate multiplier on all magic damage against that boss, `δ = (K + M_old) / (K + M_new) − 1` under a divisive formula. It is the same percentage for every caster facing that boss, and zero elsewhere. Casters in other raids see no change, and a spec whose damage is only part magic sees it weighted by its magic share.

    </details>
