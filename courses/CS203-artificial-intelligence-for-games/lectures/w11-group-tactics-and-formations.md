# CS203 · Week 11 — Group Tactics and Formations

**Why this matters:** One well-built NPC is a duel. Eight of them are a mob, and eight independent brains that each do the locally best thing will surround the player and hit at once. That is not hard, it is unfair, and it looks stupid when they bump into each other. Group AI is the layer that decides who gets to act, where each member stands and what role each plays, so that a crowd reads as a team and the fight stays winnable.

**You will be able to:**
- Compute which enemies a capacity-based attack manager admits, and which attacks they may use, from grid and attack weights.
- Derive how total damage taken grows with pack size with and without an attack cap, and use it to set difficulty.
- Compute formation slot positions from an anchor, a heading and offsets, and compare slot assignments by total distance and crossing paths.
- Critique a group tactic from a shipped game by rewriting it as a limited set of roles or tokens.

**Before class:** Michael Dawe, "Beyond the Kung-Fu Circle: A Flexible System for Managing NPC Attacks", *Game AI Pro* (2013), chapter 28 (free online, short). Travis McIntosh, "Human Enemy AI in The Last of Us", *Game AI Pro 2* (2015), chapter 34, sections 34.7 and 34.8. Tobias Karlsson, "Squad Coordination in Days Gone", *Game AI Pro Online Edition 2021*, chapter 12, sections 1, 2 and the part on advancing and flanking. Millington, *AI for Games* (3rd ed.), the section on coordinated movement and formations in the movement chapter.

**Prerequisites from earlier courses:** [CS203 week 2, steering behaviors](w02-steering-behaviors.md) (arrive, separation and why blended steering alone does not make a formation). [CS203 week 10, perception](w10-perception-systems.md) (Mark of the Ninja's interest sources, used here for group roles). [CS102 week 6, queues and stacks](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w06-queues-and-stacks-undo-and-command-buffers.md) (the waiting queue). [MA101 week 10, angles, sin and cos](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) and [week 12, 2D vectors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w12-2d-vectors.md) (rotating an offset by a heading).

**Interactive:** [`examples/w11-attack-grid.html`](../examples/w11-attack-grid.html). Keep it open during section 2.

---

## 1. Why groups need a manager

In week 2 you saw Reynolds's boids: separation, alignment and cohesion, three local rules that make a flock. Flocks are good at looking like a crowd. They are bad at tactics, because no bird knows what the others intend. Put eight melee enemies around the player with a "close in and attack" behavior each, and every one of them reaches the player and swings. Nobody decided that should happen. It is what eight copies of the same local rule produce.

Game teams solve this with a small amount of central coordination. The pattern appears under different names in every reading this week:

- a **stage manager** in Kingdoms of Amalur: Reckoning,
- a **Combat Coordinator** in The Last of Us,
- a **Squad** entity in Days Gone,
- the **sensory manager** in Mark of the Ninja, which you met last week.

All of them do the same job. They own a limited set of **permissions** (an attack slot, the flanker role, the job of investigating a noise) and hand them to individual NPCs. Each NPC still runs its own behavior tree or state machine from weeks 6 and 7. The manager only answers the question "may I?".

Two terms for the week.

- A **token** is a permission an NPC must hold to perform an action. Tokens are limited. An NPC that wants to attack asks for a token, and if none is free it does something else: circles, taunts, waits.
- A **role** is a named token with its own behavior attached: Flanker, Investigator, Opportunistic Shooter. Holding the role switches on a sub-behavior.

Central coordination sounds like the opposite of the emergent group behavior from week 2. In practice the two combine. The manager decides *who* and *how many*. Steering decides *how they move* once they know.

## 2. Worked example: the attack grid

### The hook

Kingdoms of Amalur: Reckoning (38 Studios and Big Huge Games, 2012) put action-game combat inside an open-world RPG, with many enemies taking on the player at once. Watch a fight with a large group and something odd happens. You are surrounded, yet only two or three enemies are actually swinging at you. The others hang back at a distance, move around you, and step in when one of the attackers finishes. Turn the difficulty up and more of them engage.

Dawe, who worked on the game's AI, explains the classic version of this trick first. The **Kung-Fu Circle**, named after martial-arts film scenes where a hero faces dozens of foes who attack one at a time, lets exactly one enemy attack. Reckoning needed something looser, to allow faster combat and to give the player reasons to use area attacks. So the team built a system internally called "Belgian AI", after the waffle-like grid sketches used to explain it.

Why does it matter how many enemies attack? The hook is in a number you can compute. Without a cap, the damage a player takes over a fight grows with the *square* of the pack size. With a cap, it grows in a straight line.

### The model

The player carries a grid centered on them with eight slots around it, like a tic-tac-toe board with the player in the middle. The grid has two budgets.

- **Grid capacity** `C_g` limits who may come close and attack at all.
- **Attack capacity** `C_a` limits which attacks may be in progress at once.

Every creature type has a **grid weight** `w` (its cost to occupy a slot) and every attack has an **attack weight** `a`. The rules:

```
admit creature i to the grid      if  w_i ≤ C_g − Σ w of creatures already on the grid
allow attack j by an admitted one if  a_j ≤ C_a − Σ a of attacks now in progress
release both when the attack ends
```

A central **stage manager** processes requests in order. An admitted creature moves to its slot on an outer "approach" circle. When it gets an attack, it steps into the inner "attack" circle, whose radius is set by the minimum and maximum melee distances. A creature without a slot must stay outside the approach circle. Dawe notes that creatures without slots were still given an unoccupied slot's location to stand in front of, which produced natural-looking flanking without any creature knowing about the others. After launching an attack, a creature gives its slot back, so the manager rotates attackers through the fight.

Dawe's own example, in code:

```python
class StageManager:
    """Hands out places around one target (the player), in request order."""

    def __init__(self, grid_capacity, attack_capacity):
        self.grid_free = grid_capacity
        self.attack_free = attack_capacity
        self.on_grid = {}                      # name -> grid weight

    def request_slot(self, name, weight):
        if weight <= self.grid_free:
            self.grid_free -= weight
            self.on_grid[name] = weight
            return True
        return False                           # wait outside the circle

    def choose_attack(self, name, attacks):
        """attacks: (attack, weight) pairs, strongest first. Returns one or None."""
        for attack, weight in attacks:
            if weight <= self.attack_free:
                self.attack_free -= weight
                return attack
        return None

stage = StageManager(grid_capacity=12, attack_capacity=10)
for name, weight in [("soldier A", 4), ("troll", 8), ("soldier B", 4)]:
    print(name, "gets a slot" if stage.request_slot(name, weight) else "waits",
          "| grid left", stage.grid_free)
print("troll uses", stage.choose_attack("troll", [("charge", 6), ("club", 4)]),
      "| attack left", stage.attack_free)
print("soldier A uses", stage.choose_attack("soldier A", [("lunge", 5), ("swing", 3)]),
      "| attack left", stage.attack_free)
```

Output:

```
soldier A gets a slot | grid left 8
troll gets a slot | grid left 0
soldier B waits | grid left 0
troll uses charge | attack left 4
soldier A uses swing | attack left 1
```

The soldier costs 4 of the player's 12 grid capacity. The troll, bigger and more dangerous, costs 8, which uses up the rest. The second soldier is refused and waits outside. Then attacks. The troll takes its charge (weight 6) and leaves 4. The soldier cannot afford its lunge (5), so it swings (3). Nothing in either creature's own AI knows about the other. The manager's two subtractions produce the whole pattern.

### Numbers you can check

Now the hook's claim. Use a simple fight so the arithmetic stays visible.

- A pack of `N` identical soldiers, grid weight 4, each dealing 10 damage per second while on the grid and attacking.
- The player kills one soldier every 5 seconds, and nothing else changes.
- "Normal" difficulty: `C_g = 12`, so at most `12 / 4 = 3` soldiers attack. "Hard": `C_g = 16`, so at most 4. "No grid": everyone attacks.

While `n` soldiers are alive and at most `c` may attack, the player takes `min(n, c) × 10` damage per second for 5 seconds. Summing over the fight, as the pack shrinks from `N` to 1:

```
total damage = 10 × 5 × Σ_{n=1..N} min(n, c)
no grid:       50 × N(N + 1) / 2          (grows with N²)
capped at c:   50 × [c(c + 1)/2 + c(N − c)]   for N ≥ c   (grows with N)
```

```python
def damage_taken(pack, max_attackers, dps=10, kill_time=5):
    """Player kills one enemy every kill_time seconds; the rest keep attacking."""
    total = 0
    for alive in range(pack, 0, -1):
        attackers = alive if max_attackers is None else min(alive, max_attackers)
        total += attackers * dps * kill_time
    return total

print(" pack  no grid  normal(3)  hard(4)")
for n in range(1, 9):
    print(f"{n:>5} {damage_taken(n, None):>8} {damage_taken(n, 3):>10} {damage_taken(n, 4):>8}")
```

Output:

```
 pack  no grid  normal(3)  hard(4)
    1       50         50       50
    2      150        150      150
    3      300        300      300
    4      500        450      500
    5      750        600      700
    6     1050        750      900
    7     1400        900     1100
    8     1800       1050     1300
```

Check the 8-soldier Normal row by hand. As the pack shrinks from 8 to 1, the number attacking is 3, 3, 3, 3, 3, 3, 2, 1, which sums to 21. Times 50 gives 1,050.

Give the player 1,000 health. With no grid, a pack of 6 kills them (1,050). On Normal the player survives a pack of 7 (900) and dies to 8. On Hard they survive 6 (900) and die to 7 (1,100). Each extra enemy on Normal costs a flat 150 health once the pack is larger than 3. Without the grid, the eighth enemy costs 400 by itself, because every enemy attacks from the start and each one lives longer while the player kills the others.

Read the two columns as a designer. Without the grid, pack size is a **burst** knob. Add enemies and the fight gets deadlier fast. With the grid, pack size becomes a **duration** knob. More enemies make the fight longer at the same intensity. Difficulty moves to `C_g` and `C_a`, which Dawe says Reckoning scaled up with the difficulty setting, leaving every creature's individual weights alone.

### Move it yourself

Open [the interactive](../examples/w11-attack-grid.html). The left view shows the player, the approach and attack circles, eight grid slots and a pack of enemies. Soldiers are small squares, trolls large ones. Admitted enemies sit on the approach circle. An enemy that holds an attack steps into the inner circle and flashes. Refused enemies wait outside. The right view plots total damage taken against pack size, with the no-grid curve bending upward and the capped lines running straight.

Add soldiers one at a time and watch the grid-capacity bar fill. Add a troll and watch it push a soldier out. Now drag grid capacity from 12 to 16. One more enemy steps in, and the capped line on the right tilts up. Switch the attack budget low enough that the troll's charge (6) cannot fit next to a soldier's swing (3) and watch the troll fall back to its club. The first screen already shows the curve and the line, and the gap between them at a pack of 8.

### Cross-game recognition

The same budget appears in other games as a count of named roles. Rewrite each one as "tokens, with a capacity".

**The Last of Us (Naughty Dog, 2013), the Combat Coordinator.** McIntosh describes a global object that manages roles such as Flanker, Approacher, Investigator, StayUpAndAimer and OpportunisticShooter. An NPC calls `RequestRole()`. If the role is free it gets it, acknowledges it, and no other NPC can take it until it is released. The Flanker role goes only to the NPC the coordinator rates as the best flanker that frame, from a path cost. The OpportunisticShooter role exists so that at least one NPC is always shooting at the player, and goes first come, first served. In our form, each role is a token pool with capacity 1, and the Flanker pool uses "best candidate" instead of "first requester" as its admission rule.

**Days Gone (Bend Studio, 2019), the Squad.** Karlsson describes a Squad entity that decides what the group is trying to achieve, which role each member takes, and where. When advancing, the members farthest from the frontline move while the others give covering fire. When flanking, the members farthest from the frontline's center are chosen first to minimize movement. Two details are design choices in token form. Flankers always leave an opening at the rear, so the enemy has somewhere to retreat. In token terms, the rear slot has capacity 0. And when the player tries to flank the AI, the AI will often let it happen, to give the player a small win.

**Mark of the Ninja (Klei Entertainment, 2012), roles from perception.** When several guards detect the same interest source, Miles's system assigns roles on the spot. One guard becomes the "sentry" who tells the others to check it out and hangs back. One or more get "investigate". The rest become "bystanders" who acknowledge the event and hold position. After assignment there is no group object to manage. Each guard acts alone, but the roles make them look coordinated. The investigate role is a token whose capacity the manager chooses from the group size, and Klei's stated reason was gameplay. The player should be able to split guards up and deal with them one at a time.

Four games, one mechanism. A small central budget of permissions turns a crowd of independent agents into something the player can read and fight.

### Eyes-open design judgment

- **Choose what the cap should feel like.** A cap of one (the Kung-Fu Circle) is readable and dramatic, and it can look staged when five enemies politely wait. Reckoning's weighted budget lets a troll take the space of two soldiers, so danger reads from size. Decide whether you want the player to notice the rule.
- **Waiting enemies need something to do.** A refused enemy that stands still looks broken, which is week 1's artificial stupidity. Reckoning moved waiting creatures toward free slots. Days Gone keeps non-advancing members shooting. Budget animation and behavior for the waiting state as seriously as for the attack.
- **The cap moves difficulty to one place.** That is a strength for tuning and a risk for variety. With the grid, a pack of 20 soldiers is a long fight at the same intensity as a pack of 6. You will need other tools, such as ranged attackers who do not use melee slots or cooldowns across the group, to make big packs feel different. Dawe mentions per-creature, creature-wide and global cooldowns added for that reason at the highest difficulty.
- **Letting the player win is a choice.** Days Gone's AI allowing player flanks, and Mark of the Ninja sending one guard to investigate, both give up some "optimal" group play to create moments where the player feels clever. That is week 1's rule applied to groups.

## 3. Formations: slots that move

A **formation** is a set of positions defined relative to a moving reference. The reference is called the **anchor**. It may be the leader's position, or an invisible point that moves along the group's path. Each member has a **slot**, written as an **offset** from the anchor in the anchor's own frame: so many meters to the right, so many forward.

To find a slot in the world, rotate its offset by the anchor's heading `θ` and add the anchor position. With forward `f = (cos θ, sin θ)` and right `r = (sin θ, −cos θ)`:

```
slot = anchor + right_offset × r + forward_offset × f
```

A line of four, 2 m apart, with offsets `(−3, 0), (−1, 0), (1, 0), (3, 0)`, anchored at `(0, 10)` and facing north (`θ = 90°`, so `f = (0, 1)`, `r = (1, 0)`), puts its slots at `(−3, 10), (−1, 10), (1, 10), (3, 10)`. Turn the anchor to face east (`θ = 0°`, `f = (1, 0)`, `r = (0, −1)`) and the same offsets give `(0, 13), (0, 11), (0, 9), (0, 7)`. The shape is stored once and follows the anchor. Each member then uses week 2's arrive behavior to reach its moving slot.

### Who goes to which slot?

When a scattered group forms up, you must **assign** members to slots. The obvious choices go wrong in a way players see at once. Members walk through each other.

```python
from itertools import permutations
from math import dist, cos, sin, radians

def slot_positions(anchor, heading_deg, offsets):
    """Rotate each (right, forward) offset by the heading and add the anchor."""
    h = radians(heading_deg)
    fx, fy = cos(h), sin(h)                  # forward
    rx, ry = fy, -fx                         # right-hand side
    return [(anchor[0] + r * rx + f * fx, anchor[1] + r * ry + f * fy)
            for r, f in offsets]

def crosses(p1, p2, q1, q2):
    """True if segment p1-p2 properly crosses segment q1-q2."""
    def side(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (side(p1, p2, q1) * side(p1, p2, q2) < 0 and
            side(q1, q2, p1) * side(q1, q2, p2) < 0)

def report(label, units, slots, order):
    paths = [(units[i], slots[s]) for i, s in enumerate(order)]
    total = sum(dist(a, b) for a, b in paths)
    x = sum(crosses(*paths[i], *paths[j])
            for i in range(len(paths)) for j in range(i + 1, len(paths)))
    print(f"{label:<9} slots {order}  total {total:6.2f} m  crossings {x}")

# a line of four, 2 m apart, facing north (+y), anchored at (0, 10)
offsets = [(-3, 0), (-1, 0), (1, 0), (3, 0)]
slots = slot_positions((0, 10), 90, offsets)
units = [(2, 2), (-1, 1), (-1, 4), (-4, 3)]  # where the four units stand now

print("slots", [(round(x, 1), round(y, 1)) for x, y in slots])
report("by index", units, slots, (0, 1, 2, 3))
greedy, free = [], [0, 1, 2, 3]
for u in units:                              # each unit grabs its nearest free slot
    best = min(free, key=lambda s: dist(u, slots[s]))
    greedy.append(best)
    free.remove(best)
report("greedy", units, slots, tuple(greedy))
best = min(permutations(range(4)),
           key=lambda o: sum(dist(units[i], slots[s]) for i, s in enumerate(o)))
report("best sum", units, slots, best)
```

Output:

```
slots [(-3.0, 10.0), (-1.0, 10.0), (1.0, 10.0), (3.0, 10.0)]
by index  slots (0, 1, 2, 3)  total  34.66 m  crossings 5
greedy    slots (2, 1, 0, 3)  total  33.29 m  crossings 3
best sum  slots (3, 2, 1, 0)  total  30.35 m  crossings 0
```

Three assignments of the same four units:

| Rule | Total distance | Crossing pairs |
|---|---|---|
| By index (unit 0 to slot 0, and so on) | 34.66 m | 5 of 6 |
| Greedy (each unit in turn takes its nearest free slot) | 33.29 m | 3 of 6 |
| Smallest total distance (all 24 orders tried) | 30.35 m | 0 |

Check the best row by hand. Unit `(2, 2)` goes to `(3, 10)`: `√(1 + 64) = 8.06`. Unit `(−1, 1)` to `(1, 10)`: `√(4 + 81) = 9.22`. Unit `(−1, 4)` to `(−1, 10)`: 6. Unit `(−4, 3)` to `(−3, 10)`: `√(1 + 49) = 7.07`. Sum 30.35 m.

The zero is not luck. **An assignment with the smallest total straight-line distance never has two crossing paths.** Suppose paths A→X and B→Y cross at a point P. Swap them to A→Y and B→X. By the triangle inequality, `|AY| ≤ |AP| + |PY|` and `|BX| ≤ |BP| + |PX|`, and the right-hand sides add up to exactly the old total `|AX| + |BY|`. The inequality is strict unless the points line up, so the swap makes the total shorter. An assignment with a crossing therefore cannot be the shortest. Minimize total distance and you get uncrossed paths for free.

Trying every order costs `n!`: 24 for four units, 40,320 for eight. For bigger groups use a polynomial assignment algorithm such as the Hungarian method, or accept greedy and add separation steering to hide the collisions. Dawe's stage manager did a version of this, shifting slot assignments to reduce the total travel for all creatures while never taking the slot of one that was mid-attack.

### Formations and steering together

Rigid slots look wrong in cluttered terrain, where a slot may sit inside a wall. The usual compromise has three parts. Members arrive at their slots with steering. Separation keeps them from overlapping when slots are blocked. The anchor moves no faster than the slowest member can follow, so the shape holds. Bjore's *Game AI Pro* chapter on formation movement with steering circles, building on Chris Jurney's 2007 GDC talk on Company of Heroes, is a good next read if you want formations that turn like a single vehicle.

## 4. Choosing a coordination style

You now have three tools that sit on a line from loose to tight.

| Style | Who decides | Cost | Reads as |
|---|---|---|---|
| Emergent (week 2 flocking) | each agent, local rules only | cheapest | a crowd |
| Tokens and roles (this week) | each agent decides, a manager grants permission | small | a team taking turns |
| Squad planner (Days Gone's Squad) | a group entity sets goals and positions | largest | a unit with a plan |

Start from the experience you want. A horde of zombies should look like a crowd, so flocking plus a light attack cap is enough. A police squad in a shooter should look like a team, so it needs roles and a frontline. Whatever you pick, apply week 1's five tests to the *group*, not only to the members. A group can be readable when each member is not, and the other way round.

The same token idea reappears at MMO scale. An MMO boss that can be hit by forty players has the opposite problem. The question is not how many enemies attack the player but which player the enemy attacks. That is next week's threat table. [MMO303 week 11, Lanchester's laws](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w11-lanchesters-laws-and-group-combat.md) returns to the square-law growth you saw in section 2 from the balance side.

## In-class activity (25 minutes)

Groups of three. Each group gets a card with an encounter: a player with 1,200 health who kills one enemy every 4 seconds, facing a mixed pack of 4 soldiers (grid weight 4, 10 damage per second) and 1 troll (grid weight 8, 25 damage per second). Assume the stage manager admits enemies in the order troll, then soldiers, and that the troll is killed last.

1. **Budget (8 min).** With grid capacity 12, list who is on the grid in each 4-second period as the player kills soldiers one by one. Compute total damage taken.
2. **Difficulty (7 min).** Find the smallest grid capacity (a multiple of 4) at which this pack kills the player. Show the damage total.
3. **Roles (7 min).** Replace the grid with Last of Us-style roles: one Flanker and one OpportunisticShooter token, and everyone else waits. Describe in two sentences what the player sees, and whether it passes the "readable" test.
4. **Share (3 min).** One group presents its step 2 number. The class checks it.

Expected output: a period-by-period table, one capacity with its damage total, and a two-sentence role description.

## Common misconceptions

- **"More enemies attacking at once is more realistic, so it is better AI."** It is more lethal, and the growth is quadratic in pack size. Games cap attackers because a fight the player cannot read is not fun, and players rarely notice the cap when waiting enemies stay busy.
- **"Group AI means one brain controls everyone."** In every system this week, each NPC still runs its own behavior. The manager only grants permissions or roles.
- **"Nearest-slot assignment is good enough."** Greedy assignment can cross paths, as the table in section 3 shows. The shortest total distance cannot, by the triangle inequality.
- **"If the player flanks the AI, the AI did something wrong."** Days Gone lets it happen on purpose, to reward active play.

## Check yourself

1. A player's grid capacity is 16 and attack capacity 12. Requests arrive in the order troll (grid 8), soldier (4), soldier (4), soldier (4). Who is admitted? The troll picks first between charge (6) and club (4), then the admitted soldiers in order pick between lunge (5) and swing (3). What attacks are in progress, and how much attack capacity is left?
2. Using the section 2 fight (10 damage per second per soldier, one kill every 5 s), what is the total damage from a pack of 10 soldiers with at most 3 attackers? With no cap?
3. A wedge formation has offsets `(0, 0)`, `(−2, −2)` and `(2, −2)` as (right, forward). The anchor is at `(10, 10)` facing east. Where are the three slots?
4. Two units at `(0, 0)` and `(4, 0)` must fill slots at `(4, 3)` and `(0, 3)`. Give both possible assignments, their total distances, and say which has crossing paths.
5. A designer wants a big pack to feel more dangerous than a small one without raising the attacker cap. Name two changes that do this, with a reason for each.

<details>
<summary>Answers</summary>

1. Troll (8, leaves 8), soldier (4, leaves 4), soldier (4, leaves 0). The third soldier waits. Troll takes charge (6, leaves 6). First soldier takes lunge (5, leaves 1). Second soldier cannot afford lunge (5) or swing (3), so it gets no attack this time. In progress: charge and lunge, 1 attack capacity left.
2. With cap 3: the number attacking goes 3 (eight times, for packs of 10 down to 3), then 2, then 1, total 24 + 3 = 27, times 50 = 1,350. No cap: `50 × 10 × 11 / 2 = 2,750`.
3. Facing east: `f = (1, 0)`, `r = (0, −1)`. `(0, 0)` gives `(10, 10)`. `(−2, −2)` gives `(10, 10) + (−2)(0, −1) + (−2)(1, 0) = (8, 12)`. `(2, −2)` gives `(10, 10) + 2(0, −1) + (−2)(1, 0) = (8, 8)`.
4. Straight across: `(0, 0)→(0, 3)` and `(4, 0)→(4, 3)`, total 6, no crossing. Swapped: `(0, 0)→(4, 3)` and `(4, 0)→(0, 3)`, each 5, total 10, and the paths cross in the middle. The shorter one is uncrossed, as the swap argument predicts.
5. Any two with reasons, for example: add ranged enemies that do not use melee slots, so pressure grows with pack size through a different channel; shorten the time between attackers rotating in, so the cap is used more fully; let waiting enemies buff attackers; add a group cooldown that unlocks a pack-only attack when the pack is larger than some size.

</details>

## Lab / assignment hook

[Lab 11, the stage manager](../labs/lab11.md). Implement grid and attack capacity with releases, a rotating queue of waiting enemies, nearest-free-slot assignment and a minimum-total-distance reassignment, until the provided checker passes. Then run the provided fight simulation at three difficulty settings and tune the capacities for a target fight length. Deliverable: the passing code, a tuning table and a 300-word note.

## Sources

- Dawe, M. (2013). "Beyond the Kung-Fu Circle: A Flexible System for Managing NPC Attacks." In S. Rabin (ed.), *Game AI Pro*, chapter 28. CRC Press. Free at gameaipro.com. Kingdoms of Amalur: Reckoning (2012): the Kung-Fu Circle; the "Belgian AI" name; the eight-slot grid with grid capacity and attack capacity; the worked example with capacity 12, soldier weight 4, troll weight 8, attack capacity 10, charge 6, club 4, lunge 5 and swing 3; approach and attack circles; waiting creatures standing in front of free slots; releasing slots after attacks; capacities scaled with difficulty; shifting assignments to reduce total travel; individual, creature-wide and global cooldowns.
- McIntosh, T. (2015). "Human Enemy AI in The Last of Us." In S. Rabin (ed.), *Game AI Pro 2*, chapter 34. CRC Press. Free at gameaipro.com. The Last of Us (2013): the Combat Coordinator, its roles, `RequestRole()` and `AcknowledgeRole()`; one ideal Flanker per frame chosen by path cost; the OpportunisticShooter role assigned first come, first served.
- Karlsson, T. (2021). "Squad Coordination in Days Gone." *Game AI Pro Online Edition 2021*, chapter 12. Free at gameaipro.com. Days Gone (2019): Squads as AI entities that set goals, roles and locations; advancing and flanking members chosen by distance from the frontline; flankers leaving the rear open; the AI allowing player flanks.
- Miles, B. (2013). "How to Catch a Ninja: NPC Awareness in a 2D Stealth Platformer." In S. Rabin (ed.), *Game AI Pro*, chapter 32. Mark of the Ninja (2012): sentry, investigate and bystander roles assigned per interest source.
- Bjore, S. (2013). "Techniques for Formation Movement Using Steering Circles." In S. Rabin (ed.), *Game AI Pro*, chapter 21. Cites Jurney et al., GDC 2007, on Company of Heroes.
- Millington, I. (2019). *AI for Games*, 3rd ed. CRC Press. Coordinated movement and formations.
- The damage-per-second, kill-time and health values, the unit and slot positions, the formation offsets and the activity encounter are invented for teaching.

## Interactive spec: examples/w11-attack-grid.html

**The one insight:** without an attack cap, total damage taken grows with the square of pack size; with a grid capacity it grows in a straight line, so pack size stops being a lethality knob and becomes a fight-length knob. Seeing enemies queue outside the circle on the left while the right-hand curve and line separate is the moment the lesson lands.

**Layout.** Two linked views, side by side at 1280 px, stacked at 390 px (arena on top).

- **Left, "Arena":** the player as a circle at the center. An inner "attack" circle (radius 2 m) and an outer "approach" circle (radius 5 m), both dashed. Eight slot markers on the approach circle at 45° intervals starting at east. Soldiers are small squares labelled "S", trolls large squares labelled "T" (shape and label, never color alone). Admitted enemies sit on their slots. An enemy with an attack in progress moves to the inner circle and shows its attack name. Refused enemies wait in a ring at 8 m. Two horizontal bars under the arena: "Grid capacity used X / C_g" and "Attack capacity used Y / C_a".
- **Right, "Damage over the fight":** x-axis pack size N from 1 to 12, y-axis total damage taken. Three series: "No grid" (curve), "Capped at c" for the current grid capacity (line), and a horizontal line at player health. Mark the smallest N that kills the player on each series. Readout table below with the exact numbers for N = 1 to 12.

**Controls (keyboard accessible, labelled):**

1. Buttons "Add soldier", "Add troll", "Remove last", "Clear". Requests are processed in the order added.
2. Grid capacity `C_g` slider, 4 to 32, step 4, default 12.
3. Attack capacity `C_a` slider, 3 to 20, step 1, default 10.
4. "Step" button: advances the arena one attack round. Each admitted enemy picks its strongest affordable attack (troll: charge 6, club 4; soldier: lunge 5, swing 3), heaviest grid weight first and ties in admission order. That order is what makes Dawe's example come out as the lecture prints it. The troll charges before soldier A, who can then only swing. At the end of the round every attack ends, attack capacity is fully released, each attacker gives its slot back and joins the back of the waiting queue, and the manager goes through the queue in order, admitting every enemy that fits and leaving the rest waiting.
5. Right-view inputs: soldier DPS (default 10), kill time in seconds (default 5), player health (default 1,000). The right view uses soldiers only, grid weight 4, so the cap is `c = floor(C_g / 4)`.

**Formulas.** Admission: admit if `w ≤ C_g − used_grid`. Attack: first attack in the list with `a ≤ C_a − used_attack`, else none. Damage: `total(N, c) = dps × kill_time × Σ_{n=1..N} min(n, c)`; no grid uses `c = ∞`, giving `dps × kill_time × N(N + 1)/2`.

**Test values (must match the lecture's code).**

- `C_g = 12`, `C_a = 10`; add soldier, troll, soldier: soldier A admitted (grid left 8), troll admitted (0), soldier B waits. Step: troll charge (attack left 4), soldier A swing (attack left 1).
- Check yourself 1: `C_g = 16`, `C_a = 12`; troll, soldier, soldier, soldier: first three admitted, last waits; troll charge, soldier lunge, second soldier no attack; 1 left.
- Right view at defaults (10 DPS, 5 s, 1,000 HP): N = 8 gives 1,800 (no grid), 1,050 (`C_g = 12`), 1,300 (`C_g = 16`). N = 4: 500, 450, 500. Smallest lethal N: no grid 6, `C_g = 12` 8, `C_g = 16` 7.
- N = 10, `C_g = 12`: 1,350; no grid: 2,750.

**First screen.** Six soldiers and one troll added in the order S, S, T, S, S, S, S (troll third), `C_g = 12`, `C_a = 10`: two soldiers admitted, then the troll refused (8 > 4 left), then one more soldier admitted, rest waiting. Right view shows the curve and the line with the gap at N = 8 labelled "750 health saved". Caption: "Seven enemies, three on the grid. Watch what the cap does to the damage." After one Step, two of the three soldiers lunge (5 + 5 of 10) and the third has no attack left to use.

**Accessibility.** All controls reachable by Tab with visible focus. A live region announces admissions and refusals in text ("troll waits: needs 8, 4 free"). Respects `prefers-reduced-motion` (enemies jump to positions instead of sliding) and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`. No game art: squares and circles only.
