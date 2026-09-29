# GD202 · Week 14 — Narrative Testing

**Why this matters:** A branching story is software with thousands of paths, and your players will walk paths nobody on the team ever walked. Playing it through a few times proves almost nothing. This week you learn to count how much a playthrough actually tests, to search a story's states with code instead of by hand, and to test the one thing code cannot check, which is whether players understood what happened.

**You will be able to:**
- Compute the chance that `N` random playthroughs reach a given path, and the number of runs needed to see it with 95% confidence.
- Compare random, enumerated and human testing for a branching story, and choose the right one for each kind of bug.
- Write a breadth-first search over (node, flags) states that finds unreachable content, dead ends and continuity errors.
- Design a comprehension test that measures whether players understood the story's key beats.

**Before class:** Bateman (ed.), *Game Writing: Narrative Skills for Videogames*, 2nd ed. (2021), the chapter on nonlinear structure, reread for how its branching examples would be tested (the course reader lists the pages). Reread [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md), section 2, and [CS102 week 8, graphs](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md), section 3.

**Prerequisites from earlier courses:** [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one success in `N` tries). [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md) (observe, don't explain). [CS102 week 8, graphs, maps and dialogue](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md) (breadth-first search and reachability). [CS102 week 14, unit testing gameplay rules](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w14-unit-testing-gameplay-rules.md). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md). From this course, [week 3 on the combinatorial explosion](w03-branching-structures-and-the-combinatorial-explosion.md), [week 4, dialogue systems and state flags](w04-dialogue-systems-and-state-flags.md), and [week 11 on writing for localization](w11-writing-for-localization.md).

**Interactive:** [`examples/w14-playthrough-coverage.html`](../examples/w14-playthrough-coverage.html). Keep it open during section 2.

---

## 1. What breaks in a story

Narrative bugs come in families, and each family is found by a different method. Knowing which family you are hunting tells you which tool to pick up.

| Family | What the player sees | Typical cause | Found best by |
|---|---|---|---|
| Unreachable content | Nothing. A scene, line or ending never plays. | A condition that can never be true, such as a typo in a flag name or "and" written where "or" was meant | State search (code) |
| Dead end | The story stops. No option to continue, quest cannot finish. | Every exit from a node is gated, and some reachable state satisfies none of the gates | State search (code) |
| Continuity error | A dead character speaks. An NPC thanks you for something you didn't do. | A line's conditions don't check a fact that another path changed | State search with invariants (code) |
| Cross-quest conflict | A quest never starts or breaks halfway | Another quest changed a flag or killed an NPC this one depends on | State search across quests, then players |
| Comprehension failure | Everything plays, and the player has no idea why the keeper died | The writing, pacing or signposting | Human playtests |
| Presentation failure | Text overflows a box, a voice line is missing, a name is untranslated | Localization and asset pipeline | Automated lint plus a loc pass (week 11) |

The first four are logic bugs. A computer can find them, because they are facts about which states exist. The fifth is a meaning bug, and only a person can find it. Teams that test stories badly usually use one method for everything. They play through the story a few times, which is poor at both jobs.

### A real cross-quest conflict

The Elder Scrolls V: Skyrim (Bethesda, November 2011) has a murder-mystery quest in Windhelm called Blood on the Ice. According to the Unofficial Elder Scrolls Pages, its start depends on a counter of visits to the city, the time of night, and certain townspeople being alive. One of them is Tova Shatter-Shield. In a Dark Brotherhood quest the player can be asked to kill Tova's daughter, and after that Tova takes her own life. With Tova dead, Blood on the Ice cannot start. UESP lists this among the quest's bugs and notes that the community-made Unofficial Skyrim Patch (version 1.2.1) fixes it.

Look at the shape of that bug. Each quest works on its own. The failure only exists in the combination "did the Dark Brotherhood contract, then visited Windhelm at night". A tester assigned to Blood on the Ice who played it on a fresh save would never see it. A tester assigned to the Dark Brotherhood would finish their quest and move on. The bug lived in a state neither of them visited. Keep that in mind for section 2. The question is always which states your testing reaches.

## 2. Worked example: the ending almost nobody saw

### The hook

Baldur's Gate 3 (Larian Studios, full release August 2023) has over 170 ending variations, as reported at launch. In August 2024, GamesRadar+ reported Larian as saying that one of those variations had been seen by only a few dozen players. The article is no longer online and we could not find Larian's own statement, so treat the count as an unchecked press report. Millions of people had played the game by then. If millions of players between them reached an ending only a few dozen times, how would a QA team of a few dozen people have ever seen it before launch?

They wouldn't, by playing normally. Let's count why, and then count what does work.

### The model

Treat a playthrough as a walk through the story's choices. At each choice point the player (or a test bot) picks one option. A specific path, say one particular ending, has a probability:

```
q = c_1 × c_2 × ... × c_d
```

- `d` is the number of choice points on the path.
- `c_k` is the chance that the tester picks the option this path needs at choice point `k`.
- `q` is the chance that a single playthrough follows the whole path.

A bot that picks uniformly among `b` options at every point has `c_k = 1/b`, so `q = 1/b^d`. That is the week 3 branch count turned upside down. A tree with `L` equally likely endings gives each one `q = 1/L`.

Now apply the complement rule from MA102 week 3. Each playthrough misses the path with probability `1 − q`, and playthroughs are independent, so:

```
P(seen at least once in N runs) = 1 − (1 − q)^N
N needed for confidence c        = ceil( ln(1 − c) / ln(1 − q) )  ≈  3 / q   for c = 0.95
```

One more formula covers the goal "see every ending at least once" when all `L` endings are equally likely. It is the coupon collector's problem, the same maths as collecting every card in a set:

```
expected runs to see all L endings = L × (1 + 1/2 + 1/3 + ... + 1/L)  ≈  L × (ln L + 0.58)
```

### Numbers you can check

A story with three options at each choice point, so `L = 3^d` endings:

```python
import math

def runs_to_see(q, confidence=0.95):
    """Random playthroughs needed to see one path of probability q."""
    return math.ceil(math.log(1 - confidence) / math.log(1 - q))

def runs_to_see_all(leaves):
    """Expected random playthroughs to see every one of `leaves` equal endings."""
    return leaves * sum(1 / k for k in range(1, leaves + 1))

print("depth  endings  one ending (95%)  all endings (mean)  coverage after 'endings' runs")
for depth in (2, 4, 6):
    L = 3 ** depth
    q = 1 / L
    cover = 1 - (1 - q) ** L
    print(f"{depth:5d}  {L:7d}  {runs_to_see(q):16d}  {runs_to_see_all(L):18.0f}  {cover:.1%}")
```

It prints:

```
depth  endings  one ending (95%)  all endings (mean)  coverage after 'endings' runs
    2        9                26                  25  65.4%
    4       81               242                 403  63.4%
    6      729              2183                5227  63.2%
```

Check the middle row by hand. `q = 1/81`, so `ln(1 − q) = ln(80/81) ≈ −0.01242`. And `ln(0.05) ≈ −2.996`. Dividing gives 241.2, which rounds up to 242. The shortcut `3/q = 243` is one run off.

Read the table as a test lead would.

**One run per ending covers only 63% of them.** If you run exactly as many random playthroughs as there are endings, you see about 63% of the endings (the limit is `1 − 1/e`). The other 37% are missed through bad luck alone, while some endings get seen three times.

**Seeing everything costs about `ln L` times more than the ending count.** For 729 endings, random play needs about 5,227 runs on average to see all of them, about 7 runs per ending. A directed test that enumerates every path needs exactly 729, one per ending, with no luck involved.

**Depth is what kills you.** Each extra choice point multiplies `L` by 3, and the runs needed grow a little faster than that. A team that can afford 250 random runs expects to see about 95% of a depth-4 story's 81 endings, which still leaves about 4 unseen (seeing all 81 takes 403 runs on average). The same 250 runs see only about 29% of a depth-6 story's 729 endings.

### Players are not uniform bots

Uniform bots are the best case for random testing. Real players are worse, because they choose unevenly. Most people pick the kind option. Most people keep the companion. Suppose players at each of 6 choice points split 70%, 20% and 10% across the three options. The path that takes the 10% option every time has:

```
q = 0.1^6 = 0.000001
```

With a million completed playthroughs, you expect about one player to see it, and the chance that anyone at all sees it is `1 − (1 − 10⁻⁶)^1,000,000 ≈ 63%`. The rare Baldur's Gate 3 ending is a real case of this, if the reported count is right. The game's full choice structure is far more complex than a uniform tree, so don't try to recover its `q`. The lesson is the shape. Human choices concentrate on a few paths and starve the rest.

This has two consequences for testing.

- **Human testers are the worst coverage tool you have.** A tester plays like a player, so they follow the popular paths. Ten testers playing normally are about ten samples from the 70% branch.
- **Your players are a huge random test run, and they will find what you did not.** A path with `q = 10⁻⁴` is essentially invisible to a 50-person test team. Across a million launch-week players, about 100 will see it. If it has a bug, it will be on a forum by the weekend.

Open the interactive now. The left panel plots the fraction of endings seen against the number of random runs, with a straight line for enumeration next to it. The right panel draws the tree and lights each ending as a run reaches it. Slide the depth to 6 and run 729 random playthroughs. The left curve stops near 63% (the default seed lands a little higher, about 65%). The right panel shows which endings are still dark. Switch "choice style" from uniform to player-like (70/20/10) and watch the dark endings cluster in the rare corners of the tree.

### Cross-game recognition

This is one formula you have met before, dressed differently each time.

**Playtest discovery (GD101 week 7).** In GD101 you asked how many testers it takes to see a usability problem that each tester hits with probability `p`. The answer was `1 − (1 − p)^n`. That is our formula with `p = q` and `n = N`. The difference is that a narrative path's `q` is a product of choice probabilities, so it shrinks fast with depth.

**Loot drops (MA102 week 3).** The chance of at least one 1% drop in `N` kills is `1 − 0.99^N`. Swap "kill" for "playthrough" and "drop" for "reached this ending". The same reasoning that says a 1% drop needs about 300 kills for 95% confidence says a path with `q = 1%` needs about 300 random runs.

**Skyrim's Blood on the Ice (2011).** The broken start needs two things to be true together: the player took the Dark Brotherhood contract and later came to Windhelm at night. That is a path through two quests, and its `q` is the product of the chance of each. A tester assigned to one quest has a `c` near zero for the other. Skyrim's players, in their millions, supplied the runs that QA could not, and a community patch fixed the conjunction afterwards.

**Baldur's Gate 3's early access (October 2020 to August 2023).** Larian released the game's first act in early access in October 2020, almost three years before full release, and the early access had over 2.5 million players. Whatever else it did (it also funded the studio), it turned the formula around. It raised `N` by several orders of magnitude for the part of the story that was playable.

### Design judgment

No single method wins. Each one answers a different question at a different cost.

- **Enumerate when you can.** If the story's state space is small enough to walk completely, walk all of it with code. It costs one run per state, finds every logic bug, and involves no luck. Section 3 shows how.
- **Design so that you can.** Week 3 argued that stories fold back to control scope. Folding back also keeps the state space small enough to enumerate. A design where every choice sets a permanent flag that every later scene reads cannot be fully searched, and you should know that when you choose it.
- **Use bots with a coverage goal when you can't enumerate.** Bots that prefer options they haven't taken yet reach rare paths far faster than uniform ones. Uniform bots are the baseline, and human-like bots are the worst case.
- **Use people for meaning, not coverage.** Human playtests are expensive samples from the popular paths. Spend them on the question only people can answer, which is whether the story landed. Section 4 covers how.
- **Watch the live game.** After launch, record which endings and major branches players reach. A branch with far fewer players than you expected is either unpopular or broken, and you need to know which.

## 3. Searching states, not nodes

In CS102 week 8 you used breadth-first search to ask "can the player reach this line?" on a dialogue graph. That search treats each node as a place. Stories with flags break it. A node is reachable in the graph if some path of arrows leads to it. But whether the player can actually take each arrow depends on the flags set earlier, and the same node can be visited in several different flag states.

The fix is to search **states**, where a state is the pair (node, set of flags). Two visits to the same node with different flags are different states. Everything else about the search stays the same.

Here is a tiny forge scene. The player can help or threaten a guard, which changes how the smith treats them. The writer made two mistakes. The reward node requires both `helped` and `threatened`, meaning "either" but writing "both". And the farewell scene never checks whether the smith is still alive.

```python
from collections import deque

# node: (speaker, [(label, target, requires, sets)])
STORY = {
    "gate":     ("Guard", [("offer help", "forge", set(), {"helped"}),
                           ("threaten", "forge", set(), {"threatened"})]),
    "forge":    ("Smith", [("ask about the blade", "blade", {"helped"}, set()),
                           ("draw steel", "duel", {"threatened"}, {"smith_dead"}),
                           ("leave", "square", set(), set())]),
    "blade":    ("Smith", [("thank him", "square", set(), set())]),
    "duel":     (None,    [("walk away", "square", set(), set())]),
    "square":   ("Mayor", [("claim reward", "reward", {"helped", "threatened"}, set()),
                           ("go back to the forge", "farewell", set(), set()),
                           ("leave town", "end", set(), set())]),
    "farewell": ("Smith", [("leave town", "end", set(), set())]),
    "reward":   ("Mayor", []),
    "end":      (None,    []),
}

def explore(story, start="gate"):
    """Breadth-first search over (node, flags) states, as in CS102 week 8."""
    first = (start, frozenset())
    seen, queue = {first}, deque([first])
    while queue:
        node, flags = queue.popleft()
        for _, target, needs, sets in story[node][1]:
            if needs <= flags:
                nxt = (target, flags | sets)
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return seen

states = explore(STORY)
print("nodes:", len(STORY), " reachable states:", len(states))
print("unreachable nodes:", sorted(set(STORY) - {n for n, _ in states}))
for node, flags in sorted(states, key=lambda s: (s[0], sorted(s[1]))):
    if STORY[node][0] == "Smith" and "smith_dead" in flags:
        print("dead speaker:", node, sorted(flags))
```

It prints:

```
nodes: 8  reachable states: 14
unreachable nodes: ['reward']
dead speaker: farewell ['smith_dead', 'threatened']
```

Count the 14 states by hand to make sure you believe it. The gate has one state (no flags). The forge has two (`helped` or `threatened`). The blade has one, and the duel has one. The square, the farewell and the end each have three: helped, threatened, and threatened with the smith dead. That makes `1 + 2 + 1 + 1 + 3 + 3 + 3 = 14`.

A graph-only search would report that `reward` is reachable, because an arrow leads to it from `square`. It would also see nothing wrong with `farewell`, because a node doesn't know who is dead. The state search catches both. It needed 14 states to do it, not 8 nodes.

### Why this scales better than it looks

With `F` flags, a node could in principle be visited in `2^F` flag states. Twenty flags would be a million states per node. This sounds hopeless, and for "all combinations of flags" it is. But the search only visits states that can actually happen. Most flags are set by one choice and never cleared, and most scenes can only be reached with a few combinations. Real quest scripts usually have far fewer reachable states than the worst case. The search tells you the real number, and when it is too big to finish, that tells you something about your design.

### Invariants: bugs you describe once

The dead-speaker check above is an **invariant**, a rule that must hold in every reachable state. You write it once, and the search checks it everywhere. Useful narrative invariants include these.

- Every node is reachable in some state.
- Every reachable state that is not an ending has at least one available choice (no dead ends).
- Every ending is reachable.
- A character flagged dead, absent or hostile never speaks a friendly line.
- Every flag that some condition reads is set by some choice, and every flag that is set is read somewhere. A flag read but never set is almost always a typo.
- Every line has a localization ID and, if the game is voiced, a recorded file (week 11).

The last two don't even need the search. They are **lint** checks, run on the script file itself. Put them on every build, because they cost milliseconds and catch the commonest mistake of all, the misspelled flag.

The lab uses exactly this setup on a larger story with three planted bugs. It also computes each ending's exact `q` for a uniform bot, which ties section 2 to section 3. A state search can tell you the precise chance that random testing would have found each bug.

## 4. Testing for understanding

Everything so far checks that the story runs as written. None of it checks whether the story works. A scene can be reachable, correctly gated and free of dead speakers and still leave players unsure who the villain was.

That needs people, and it needs them used well. GD101 week 7 gave you the core rule. Observe, and don't explain. For narrative, add a way to measure what players took away.

### A comprehension check

1. **Before the test, write the beats.** List three to five facts the player must understand for the story to work. "The keeper stayed because his daughter drowned here." "The ferrywoman lied about the oil." Keep them concrete and checkable.
2. **Let them play without help.** No hints, no answering questions during play. If you must intervene to unblock them, note where. Your notes are data.
3. **Ask open questions after.** "What happened at the lighthouse?" "Why do you think the keeper refused to leave?" Don't ask "Did you notice the letter?", because that teaches the answer.
4. **Score each beat.** For each tester and beat, mark understood, partly or missed. The result is a small table with beats down the side and testers across the top.
5. **Look for the missed beat, not the average.** A beat that three of five testers missed is a writing problem regardless of how well the others did.

Be careful with the numbers. With five testers, "3 of 5 understood" is compatible with a true rate anywhere from about 15% to 95%. MA102 week 13 shows why. Five testers are enough to *find* a beat that most people miss. They are not enough to *measure* how many people understand it. For that you need larger samples, which usually means a survey after a larger playtest (UX201 week 12).

### Reading and continuity

Two cheaper human methods catch a lot before any playtest.

- **A cold read.** Someone outside the writing team reads a path through the script aloud, in order, as a player would see it. People inside the team fill gaps from memory and can't see them.
- **A continuity bible check.** The team keeps a document of facts, such as who is alive when, who knows what, and what each flag means. Reviewers check each new scene against it. This is the human version of the invariants in section 3. Many facts in the bible can be turned into invariants later.

## 5. A narrative test plan

Put the pieces into a schedule. The cheap, automatic checks run most often. The expensive human ones run at milestones.

| When | What runs | Catches | Cost |
|---|---|---|---|
| Every script change | Lint: flags read and set, missing IDs, missing voice files | Typos, pipeline gaps | Seconds, automatic |
| Every build | State search with invariants | Unreachable content, dead ends, continuity | Minutes, automatic |
| Nightly | Bots, uniform and coverage-seeking; outcome rates compared with the design's intent | Branches much rarer than intended, crashes on odd paths | An hour of machine time |
| Each milestone | Comprehension playtests, cold reads | Meaning failures | Days of people's time |
| Before release | Localization pass in every language (week 11) | Overflow, untranslated names, grammar with variables | Days to weeks |
| After launch | Telemetry on endings and major branches | Real-world rare paths, broken cross-quest conflicts | Continuous; see [MMO308 week 4, funnels and churn](../../MMO308-live-operations-analytics-and-experimentation/lectures/w04-funnels-and-churn.md) |

One nightly check deserves a word. Your design has an intent for each branch. If you meant an ending to be common and bots reach it 7.8% of the time, something gates it harder than you thought. The lab's story has exactly this problem. An ending that feels like the natural goal turns out to have `q = 5/64` for a uniform bot. Comparing outcome rates with intent catches design bugs that no invariant describes.

## In-class activity (25 minutes)

Work in pairs. Your instructor hands out a printed copy of `lantern.json` from the lab starter as a flowchart, ten nodes with their conditions.

1. **Hunt by hand (10 min).** Without code, find every bug you can. Look for content that cannot play, places the story can stop, and lines that should not be spoken. Write each one with the path that shows it.
2. **Estimate (5 min).** For each bug you found, estimate the chance that a single uniform random playthrough hits it. Multiply the choice probabilities along its path.
3. **Compute (5 min).** For your rarest bug, compute how many random playthroughs a tester needs for 95% confidence of hitting it.
4. **Compare (5 min).** Your instructor runs the finished harness on the file. Compare its list with yours. Which bugs did you miss, and what kind of state were they in?

Expected output: a list of bugs with paths, a `q` for each, the runs-needed number, and one sentence on why hand checking missed what it missed. Most pairs find the unreachable ending and miss the dead end. That is the lesson.

## Common misconceptions

- **"We played it through five times and it works."** Five playthroughs by people on the team are five samples from the most popular paths. For a path with `q = 1/81`, five runs have a 6% chance of seeing it.
- **"Random bots will find everything if we run enough of them."** They will eventually, but the cost grows with `1/q`, and rare paths have tiny `q`. Enumerating the state space costs one run per state and involves no luck. Use bots only where enumeration is too big.
- **"If the node is reachable in the graph, the content is reachable."** Conditions on choices make some arrows impassable in some states. Only a search over (node, flags) states answers the question.
- **"A comprehension score from five testers tells us what percentage of players understand."** It tells you which beats are clearly failing. It cannot measure a rate with any precision.

## Check yourself

1. A path needs four specific choices, and a uniform bot faces 2, 3, 3 and 4 options at those points. What is `q`? How many random runs give 95% confidence of seeing it?
2. A story has 243 equally likely endings. About how many random runs does it take, on average, to see all of them? How does that compare with enumeration?
3. Players pick an option at a choice point 5% of the time, and the path you care about needs that option at three different points (all else being certain). With 400,000 completed playthroughs, how many players do you expect to see it?
4. The forge scene in section 3 has a reward node that requires `helped` and `threatened`. Fix the condition so that the reward is available to helpers only, and say how many reachable states the fixed story has.
5. Your nightly bot run shows an ending you designed as "the one most players get" reached in 4% of uniform playthroughs. Name two possible causes, one a bug and one not.

<details>
<summary>Answers</summary>

1. `q = 1/2 × 1/3 × 1/3 × 1/4 = 1/72`. Runs: `ceil(ln 0.05 / ln(71/72)) = ceil(2.996 / 0.01399) = ceil(214.2) = 215`. The shortcut `3/q = 216` is close.
2. `243 × (1 + 1/2 + ... + 1/243) ≈ 243 × (ln 243 + 0.58) ≈ 243 × 6.07 ≈ 1,476` runs. Enumeration needs 243, about six times fewer.
3. `q = 0.05³ = 0.000125`, so `400,000 × 0.000125 = 50` players expected.
4. Change the requirement to `{"helped"}`. The reward is then reached from the one `helped` square state, adding one state, so the story has 15 reachable states and no unreachable nodes. (The dead-speaker bug remains until the farewell checks `smith_dead`.)
5. A bug: a condition gates the ending harder than intended, such as a flag typo or an "and" that should be "or", or a dead end that swallows paths on the way. Not a bug: uniform bots do not choose like players, so an ending that players reach by following obvious choices can still be rare under uniform choice. Check the path's conditions, then compare with human-like bots or playtest data before deciding.

</details>

## Lab / assignment hook

[Lab 14, a narrative test harness](../labs/lab14.md). You implement state search, dead-end and continuity checks, exact outcome probabilities and a random-playthrough runner for a ten-node story with three planted bugs, then fix the story and run the harness on your own final-project quest chain. The harness report is a required appendix to the final quest-chain submission.

## Sources

- Unofficial Elder Scrolls Pages (UESP), "Skyrim:Blood on the Ice" (The Elder Scrolls V: Skyrim, 2011, original release with official patches to 1.9). Start conditions (Windhelm visit counter, night hours, required NPCs alive); the bug where Tova Shatter-Shield's death after the Dark Brotherhood contract on her daughter stops the quest from starting; fixed in Unofficial Skyrim Patch 1.2.1. https://en.uesp.net/wiki/Skyrim:Blood_on_the_Ice
- Schreier, J. (3 August 2023). "The Strange Story Behind 'Baldur's Gate 3,' One of the Year's Biggest Releases." *Bloomberg News*. Over 170 ending variations; early access player numbers, as cited by Wikipedia's "Baldur's Gate 3" article.
- Jones, A. (7 August 2024). "Baldur's Gate 3's least-popular Origin character has an ending so rare that Larian says only 34 players have ever even seen it." *GamesRadar+*. The URL returned 404 in September 2026 and the figure could not be checked against a Larian source, so the lecture does not rely on the exact count.
- Wikipedia, "Baldur's Gate 3" (accessed September 2026). Early access from October 2020 with over 2.5 million players; Windows release 3 August 2023.
- Bateman, C. (ed.) (2021). *Game Writing: Narrative Skills for Videogames*, 2nd ed. Bloomsbury.

## Interactive spec: examples/w14-playthrough-coverage.html

**The one insight the visual must make obvious:** random playthroughs cover a branching story slowly and unevenly. After as many random runs as there are endings, about a third of the endings are still unseen, and the unseen ones cluster where choices are rare. Enumeration covers everything in exactly `L` runs.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile.

- **Left, "Coverage vs runs".** x-axis: runs `N`, from 0 to `8L` (linear). y-axis: fraction of endings seen, 0 to 100%. Three lines:
  1. *Expected random coverage*, smooth: `(1/L) Σ_leaves [1 − (1 − q_leaf)^N]`.
  2. *This simulation*, stepped: the actual fraction seen by the runs done so far.
  3. *Enumeration*, straight: `min(N / L, 1)`.
  A vertical marker at `N = L` labelled "one run per ending", with the expected coverage printed beside it.
- **Right, "The tree".** A radial or top-down tree with branching `b` and depth `d`. Leaves are small squares, dark until a run reaches them, then filled; fill opacity grows with the number of hits (1, 2, 3+). With `d = 6, b = 3` (729 leaves) draw leaves as a dense band; no labels needed. Hovering or focusing a leaf shows its path and its `q`.
- **Readout row:** `L`, runs so far, endings seen (count and %), expected coverage at this `N`, runs needed for 95% on the rarest leaf (`ceil(ln 0.05 / ln(1 − q_min))`), and the coupon-collector mean `L × H_L` (uniform style only).

**Controls.**

1. **Branching `b`** slider 2 to 4 (default 3). **Depth `d`** slider 1 to 6 (default 6). Cap `L` at 4,096 (so `b = 4, d = 6` is the maximum).
2. **Choice style** select: "Uniform bot" (each option `1/b`), "Player-like" (option weights 70/20/10 for `b = 3`; 80/20 for `b = 2`; 60/20/15/5 for `b = 4`), "Coverage-seeking bot" (at each node, prefer the child subtree with the fewest hits so far, ties broken at random).
3. **Run** buttons: "+1", "+10", "+100", "Run to N = L", "Reset". Seeded RNG (seed shown, editable) so runs are reproducible.
4. **Enumerate** button: runs exactly `L` directed playthroughs in order, animating the tree filling left to right (instant if `prefers-reduced-motion`).

**Formulas.** `q_leaf` = product of the option weights along the leaf's path. Runs needed for 95%: `ceil(ln(0.05) / ln(1 − q))`. Coupon collector mean `L × Σ_{k=1..L} 1/k`.

**Test values (must match, uniform style).**

| b | d | L | Runs for 95% on one leaf | Mean runs to see all | Expected coverage at N = L |
|---|---|---|---|---|---|
| 3 | 2 | 9 | 26 | 25 | 65.4% |
| 3 | 4 | 81 | 242 | 403 | 63.4% |
| 3 | 6 | 729 | 2183 | 5227 | 63.2% |

Player-like, `b = 3, d = 6`: rarest leaf `q = 0.1^6 = 1e-6`, runs for 95% on it = 2,995,731 (show with thousands separators). Expected coverage at `N = 729` must be computed from the non-uniform `q` values and will be far below 63%; display it.

**First screen.** Load with `b = 3, d = 6`, uniform, 729 runs already done (seed 1), so the tree shows a speckled mix of lit and dark leaves and the left panel shows the simulated line near 63% against the enumeration line at 100%. Caption: "729 random playthroughs, 729 endings. K have never been seen.", where K is the simulated unseen count. The expected value is 268 with a standard deviation of about 8; seed 1 gives 253, so the simulated coverage line sits near 65% rather than exactly on 63%.
