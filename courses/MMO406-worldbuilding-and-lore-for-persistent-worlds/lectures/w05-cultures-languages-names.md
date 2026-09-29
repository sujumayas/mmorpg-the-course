# MMO406 · Week 05 — Cultures, Languages, Names

**Why this matters:** Players meet your cultures mostly through names. They read hundreds of them on nameplates, quest logs and maps long before they read a word of your culture chapter. If two cultures' names blur together, the bible can say whatever it likes and players will still hear one people. This week you learn to predict, before a single NPC is named, whether players will be able to tell your cultures apart by ear.

**You will be able to:**
- Compute the chance that a name from one culture could pass for another's, from their syllable inventories, usage weights, name length and structural markers.
- Explain why a count of shared syllables misjudges how distinct two naming languages sound, and correct it with usage weights.
- Design a culture sheet whose answers are tied to your setting's geography, economy and factions, and a naming language that carries that culture's identity.
- Choose how deep to build a constructed language (naming language, glossed morphemes, grammar fragments, full language) and defend the cost.

**Before class:** Wolf, *Building Imaginary Worlds* (2012), chapter 3, skimming for what it says about culture and language. Mark Rosenfelder, *The Language Construction Kit* (2010), the opening material on sounds; skim for the idea of a phonology as a small inventory of sounds and syllable shapes. UESP, "Lore:Argonian Names" (the two sections on obtaining names, 5 minutes).

**Prerequisites from earlier courses:** [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) and [MA102 week 2, independent events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md). [MMO301 week 10, immersion, identity and the avatar](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w10-immersion-identity-and-the-avatar.md) used the birthday model for look and name collisions among players, and showed how popular choices shrink an identity space. This week reuses that idea of skewed shares for NPC naming languages and does not repeat the birthday model. [GD202 week 11, writing for localization](../../GD202-narrative-and-quest-design/lectures/w11-writing-for-localization.md) covers text expansion and why invented words need translator notes. [GS101 week 14, games and representation](../../GS101-history-and-critical-study-of-games/lectures/w14-games-and-representation.md) is the background for section 4's advice on borrowing from real cultures. From this course, [week 4](w04-history-and-timelines.md) gives cultures a past, and [week 2, geography](w02-geography-and-ecology.md) and [week 3, factions](w03-factions-and-conflict.md) give them land and rivals.

**Interactive:** [examples/w05-name-overlap.html](../examples/w05-name-overlap.html). Keep it open during section 2.

---

## 1. A culture is a set of answers

A **culture** in a setting bible is the shared way of life of a group of people: what they eat, make, trade, honour, fear and call things. That definition is too loose to design with, so turn it into questions. A culture sheet that works in an MMO answers each question with something that touches a system.

| Question | Answer should touch | Example for a river-trading people |
|---|---|---|
| What do they eat and grow? | Geography and ecology (week 2) | Eel, rice, reed crops. Their villages cluster where the river floods. |
| What do they make and sell? | Economy, crafting | Lacquered boats and reed rope. Their crafters sell to the hill clans. |
| Whom do they fear or fight? | Factions (week 3) | Hill clans who dam the upstream valleys in drought years. |
| What do they remember? | History (week 4) | The Drowning, when the river took the old capital. |
| What do they hold sacred? | Religion (week 6) | The river itself, and the dead it carries. |
| How do they name people and places? | Names, maps, UI | This week's model. |

Two things make this more than a form. First, every answer should create play. "They sell reed rope to the hill clans" gives the economy team a trade good and the quest team a caravan. "They are a proud people" gives nobody anything. Second, answers should connect to each other. The eels, the flood villages, the fear of upstream dams and the river worship all come from one fact, a people living on a river they cannot control. A culture whose answers share a cause feels real. A culture assembled from unrelated cool ideas feels like a costume.

The last row, naming, is special. It is the only answer players meet in every zone, in every quest and in chat. The rest of this lecture is about getting it right.

## 2. Worked example: will players hear the difference?

### The hook

Final Fantasy XIV's Miqo'te of the Seekers of the Sun clan have a naming scheme players can recognize at a glance. According to the game's lore book *Encyclopaedia Eorzea*, the twenty-six Seeker tribes that crossed the frozen sea each took one letter of the Eorzean alphabet, and the tribe's letter comes first in a member's name, followed by an apostrophe. The game's own NPC G'raha Tia shows the pattern: G for his tribe, and "Tia", the term for a male who has not become a tribe's breeding male. You can pick a Seeker out of a crowd of nameplates at a glance.

Compare two invented cultures from a student's bible. The bible lists the syllables each culture uses and says they share only a third of them. Playtesters still mix up the cultures' NPCs. The bible's number is correct. The playtesters are also right. Why?

### The model

Treat a **naming language** as a set of syllables, each with a **usage weight**, the share of all syllables in that culture's names that are this one. Weights add up to 1. Call culture A's set `S_A` and culture B's set `S_B`.

A player hearing a name from culture A can mistake it for culture B's if every syllable in it also occurs in B's names. Define:

```
o_count = |S_A ∩ S_B| / |S_A|            share of A's syllables that B also uses
o       = sum of w_s for s in S_A ∩ S_B  share of A's usage that B also uses
P_amb(L) = (1 − m) × o^L                 chance an L-syllable A-name could pass for B
I(L)     = 1 − P_amb(L)                  chance the name is identifiable as A
```

- `w_s` is syllable `s`'s usage weight in culture A.
- `L` is the number of syllables in the name.
- `m` is the share of A's names that carry a **structural marker**, a feature B's names never have: an apostrophe after a tribe letter, a fixed ending, a translated phrase. A marked name can never pass for B.
- `o^L` uses the multiplication rule for independent events (MA102 week 2): each syllable independently lands in the shared set with chance `o`.

Two points about the model. It is about **could pass for**, which is the most a single name can tell a listener. And it is **directional**. `o` from A to B is not `o` from B to A, because each culture uses the shared syllables with its own weights.

### Numbers you can check

Take two invented cultures. The river-trading Vessari use twelve syllables. The hill-clan Durhk use eight. Four syllables are shared: *an*, *el*, *ra*, *to*.

| Syllable | Vessari weight | Durhk weight |
|---|---|---|
| an | 0.20 | 0.05 |
| el | 0.15 | 0.05 |
| ra | 0.15 | 0.10 |
| to | 0.10 | 0.05 |
| 8 Vessari-only (ssa, vei, li, mae, sio, ne, qua, ith) | 0.05 each, 0.40 total | — |
| 4 Durhk-only (durh, kag, bor, gund) | — | 0.20, 0.20, 0.20, 0.15 |

The bible's view counts syllables. For the Vessari, 4 of 12 are shared, so `o_count = 0.333`. For the Durhk, 4 of 8, so `o_count = 0.5`. By this count, Durhk names should be the easier ones to confuse.

The weighted view counts usage. The Vessari lean on the shared syllables, `o = 0.20 + 0.15 + 0.15 + 0.10 = 0.60`. The Durhk barely use them, `o = 0.25`. This script computes both views.

```python
vessari = {"an": .20, "el": .15, "ra": .15, "to": .10,
           "ssa": .05, "vei": .05, "li": .05, "mae": .05,
           "sio": .05, "ne": .05, "qua": .05, "ith": .05}
durhk = {"an": .05, "el": .05, "ra": .10, "to": .05,
         "durh": .20, "kag": .20, "bor": .20, "gund": .15}

def overlap(a, b, weighted=True):
    shared = [s for s in a if s in b]
    if weighted:
        return sum(a[s] for s in shared)
    return len(shared) / len(a)

def ambiguity(o, L, m=0.0):
    """Chance an L-syllable name could pass for the other culture's."""
    return (1 - m) * o ** L

for name, a, b in [("Vessari", vessari, durhk), ("Durhk", durhk, vessari)]:
    oc, ow = overlap(a, b, False), overlap(a, b)
    print(name, f"count o={oc:.3f}  weighted o={ow:.2f}")
    for L in (1, 2, 3, 4):
        print(f"  L={L}  count view {ambiguity(oc, L):6.1%}   weighted {ambiguity(ow, L):6.1%}")
```

```
Vessari count o=0.333  weighted o=0.60
  L=1  count view  33.3%   weighted  60.0%
  L=2  count view  11.1%   weighted  36.0%
  L=3  count view   3.7%   weighted  21.6%
  L=4  count view   1.2%   weighted  13.0%
Durhk count o=0.500  weighted o=0.25
  L=1  count view  50.0%   weighted  25.0%
  L=2  count view  25.0%   weighted   6.2%
  L=3  count view  12.5%   weighted   1.6%
  L=4  count view   6.2%   weighted   0.4%
```

(The Durhk two-syllable value is exactly 6.25%; the print rounds it.)

Read the two-syllable row. The bible's count says a Vessari name like *Anra* or *Elto* passes for Durhk 11% of the time. In play it is 36%, more than one Vessari name in three. And the count view got the ranking backwards. The Durhk, whose names "should" be the confusable ones, are in fact the distinctive ones, because their heavy syllables *durh*, *kag* and *bor* are theirs alone. That is what the playtesters heard.

This is the same lesson MMO301 week 10 taught about avatar looks. There, a creator's promised number of combinations shrank once you weighted by what players actually picked. Here, a bible's syllable list says little until you weight it by what the writers actually use. Writers reach for the easy syllables, and the easy syllables are the shared ones.

### Three ways to fix the Vessari

Each lever in the model is a design option. For two-syllable names:

| Fix | Change | P_amb(2) |
|---|---|---|
| None | `o = 0.60` | 36.0% |
| Lengthen names | `L = 3` | 21.6% |
| Reweight | Shared syllables cut to 0.30 of usage | 9.0% |
| Partial marker | Half of names end in a Vessari-only syllable, `m = 0.5` | 18.0% |
| Full marker | Every name ends in a Vessari-only syllable, `m = 1` | 0% |

Lengthening costs screen space and memorability. Reweighting costs nothing on screen but asks writers to break a habit, so it needs a name list or a generator rather than good intentions. A marker is the strongest lever, because it works at any length and any overlap.

### A visual you can move

Open [`examples/w05-name-overlap.html`](../examples/w05-name-overlap.html). The left panel, "What the bible says", shows the two syllable sets as a pair of overlapping boxes sized by syllable count, with `o_count` in the middle. The right panel, "What the player hears", shows the same syllables as bars sized by usage weight, the shared ones highlighted, and the curve of `P_amb` against name length. A strip of twelve generated Vessari names sits underneath, with each name that could pass for Durhk underlined. Drag the weight of *an* up. The left panel does not move at all. The right curve climbs and more names in the strip get underlined. Then switch on the marker and watch the underlines vanish regardless of the weights.

### Cross-game recognition

**Final Fantasy XIV, Seekers of the Sun (A Realm Reborn onward).** The tribe letter and apostrophe is a structural marker with `m = 1` within the clan. No other culture in the game uses that exact form, so a Seeker name is identifiable even when its syllables would fit elsewhere. The *Tia* or *Nunh* surname is a second marker that also carries social information. The same game's Lalafell show a different marker. Their names follow published rhyme schemes built on repeated syllables, one per clan and gender: male Plainsfolk AB-CB, female Plainsfolk ABB-AB, male Dunesfolk AAB-CCB, female Dunesfolk AAB-AB. Ikuku Iku, Nanamo Ul Namo and Teledji Adeledji show the echo. The developers say a reader can tell clan and gender from the name alone. Repetition is a pattern, not a syllable, so it survives heavy sound overlap with other cultures.

**The Elder Scrolls, Argonians (series lore, including ESO).** UESP describes two naming layers. Argonians receive a name in their own language, Jel, and many also carry a Tamrielic name that translates it. Its example is Haj-Ei, rendered as Hides His Eyes. The translated layer is a marker. A name shaped like a short English phrase marks an Argonian regardless of which sounds it contains. In model terms, the phrase form sets `m` close to 1 for that layer.

**English place names (historical toponymy).** Endings such as *-by* ("village") and *-thorp* ("hamlet") come from Old Norse. Their concentration in northern and eastern England is one of the lines of evidence historians use for where Scandinavian settlers lived in the Danelaw. An ending is a marker in exactly our sense. It identifies the naming culture no matter what the rest of the name is. Real naming systems have been doing this for a thousand years.

Three systems, one idea. When you want a culture's names to be recognizable, look first for a marker, then reduce the weight of shared sounds, and lengthen names last.

### Eyes-open design judgment

- **Markers become parody when overused.** An apostrophe in every name of every culture marks nothing, because the marker has to be absent from the other culture's names. Give each culture a different kind of marker, and at most one.
- **Distinct is not the same as good.** A culture with `o = 0` and harsh consonant clusters will be recognizable and also unpronounceable. Players who cannot say a name will not remember it, and will not type it into chat or a wiki search.
- **Some overlap is information.** Two cultures that share history should share some sounds. The Durhk and Vessari trading for centuries would borrow names. Decide which shared syllables tell that story, and keep their weight deliberate.
- **The model ignores rhythm and spelling.** Real listeners also hear stress, length and letter shapes. Treat `P_amb` as a lower bound on confusion and test with players, which the lab does.

## 3. Languages: how deep to go

A naming language is the shallowest constructed language, or **conlang**. There are deeper levels, and each costs more.

| Level | What exists | What it gives | Cost |
|---|---|---|---|
| 1. Naming language | Sound inventory, weights, syllable shapes, markers | Recognizable names | Days |
| 2. Glossed morphemes | 20 to 60 word pieces with meanings | Place and personal names that mean something | Weeks |
| 3. Grammar fragments | Word order, plurals, a few inflections | Inscriptions, chants, short phrases players can decode | Months |
| 4. Full language | Grammar, thousands of words, a speaker | Dialogue, songs, a community that learns it | A specialist, for years |

Most MMOs should build level 2 for every major culture and level 3 for one or two. Level 2 is where the payoff per hour is highest, because it connects names to geography and history. Give the Vessari a handful of glossed pieces, *mae* "reed", *sio* "flood", *ith* "house", *qua* "old", and their map writes itself. *Siomae* is a reed bed on the floodplain. *Quaith* is the old house, a fine name for a ruin from week 4's Drowning era. When a player learns two morphemes from a quest, every map label containing them becomes a small reward.

Level 3 is how Skyrim (2011) treated its Dragon Language. The game's dragon words appear carved on Word Walls in ancient sites, and the player's shouts are dragon words that produce magical effects when spoken. UESP, citing a 2011 Game Informer feature, reports that the language's grammar was built close to English with a few deliberate differences. That choice kept it learnable. The words are also a mechanic, so a player has a reason to learn what they mean.

Level 4 is rarely worth it for a game team. The exception is when the language itself is the product, for example a fan community that will teach it.

## 4. Names in a live world

Names in an MMO have practical jobs on top of cultural ones.

**Registry.** Keep one list of every NPC, place and item name, with culture, meaning (if glossed) and first appearance. Without it, a live team will reuse names by accident within two years. Search the registry before approving a new name.

**Length and localization.** Long names break nameplates, quest trackers and chat. Invented names also need translator notes, since a translator cannot guess whether *Quaith* is a place, a person or a curse. GD202 week 11 covers text expansion and translator notes in detail. Settle a maximum name length per UI element before writing any.

**Player names.** Players name their own characters, and they will ignore your naming language unless the game helps. Some games publish naming guidance per culture for roleplayers, and roleplay communities often enforce it among themselves. Uniqueness and collisions among player names are MMO301 week 10's topic, so this lecture only asks whether your character creator suggests culture-fitting names. A random-name button that uses the culture's generator is cheap and changes what a server sounds like.

**Borrowing from real cultures.** Many fantasy cultures borrow the sound of a real language: Norse for the northern warriors, Japanese for the island empire. Players will hear the borrowing, and with it every stereotype attached to the source culture. GS101 week 14 discusses representation. The practical advice is to borrow on purpose, from more than one source per culture, and to have someone from the source culture read your names before you ship.

## In-class activity (25 minutes)

In pairs, take two cultures from your own bible (or use the Durhk and a new culture of your own).

1. Write each culture's syllable inventory with usage weights, 8 to 14 syllables each. Mark the shared ones.
2. Compute `o_count` and the weighted `o` in both directions, and `P_amb(2)` and `P_amb(3)` for each.
3. Each partner writes ten names for their culture by hand, without looking at the weights. Count how many of the other's names could pass for yours. Compare with `P_amb`.
4. Choose one structural marker for one culture and say why it fits that culture's answers from section 1.

Expected output: two weighted inventories, four `P_amb` values, the hand-written name counts, and the marker with a one-sentence justification. Most pairs find their hand-written names are more ambiguous than their inventories predicted. Discuss why.

## Common misconceptions

- **"We share only a third of our syllables, so our names are distinct."** Counting syllables ignores how often each is used. If the shared syllables are the common ones, names blur far more than the count suggests. Weight by usage.
- **"Overlap is symmetric."** A's names can pass for B's much more often than B's pass for A's. The Vessari and Durhk example has 36% one way and 6.25% the other at two syllables.
- **"More apostrophes make a name more fantasy."** An apostrophe is only a marker if other cultures do not use it. Used everywhere, it adds typing cost and no information.
- **"A real conlang makes a better world."** For most MMOs a naming language plus glossed morphemes gives almost all of the player-facing benefit. A full language pays off only when players use it.

## Check yourself

1. Culture C uses 10 syllables, 5 of them shared with culture D. The shared syllables carry 0.3 of C's usage. Compute `P_amb` for a two-syllable and a three-syllable C-name, and the count-view value for two syllables.
2. For the Vessari (`o = 0.6`), what share `m` of names must carry a marker so that `P_amb(2)` is at most 10%?
3. A designer says "the Durhk are more confusable, because half their syllables are shared." Using the lecture's weights, show why they are wrong for two-syllable names.
4. You can either lengthen all Vessari names from two syllables to three, or cut the shared syllables' weight from 0.6 to 0.4 and keep two syllables. Which gives lower `P_amb`, and what else would you weigh?
5. Pick three glossed Vessari morphemes from section 3 and build a name for a riverside temple dedicated to the dead. Explain what a player who knows the morphemes learns from it.

<details>
<summary>Answers</summary>

1. Weighted: `0.3² = 9%` and `0.3³ = 2.7%`. Count view: `(5/10)² = 25%`. The count view overstates confusion here, because C mostly uses its own syllables.
2. `(1 − m) × 0.36 ≤ 0.10` gives `m ≥ 0.722`, so about 73% of names or more.
3. The Durhk weighted overlap is `0.25`, so `P_amb(2) = 6.25%`, against 36% for the Vessari. The Durhk rarely use the shared syllables; their names are built from *durh*, *kag*, *bor* and *gund*, which no Vessari name contains.
4. Lengthening: `0.6³ = 21.6%`. Reweighting: `0.4² = 16%`. Reweighting wins and costs no screen space, but it constrains writers and needs a generator or name list to hold. Also weigh pronounceability and whether the shared syllables carry history you want to keep.
5. For example *Quasio-ith* or *Siomaeith* built from "flood", "reed" and "house". Any answer works if it uses the given glosses. A player who knows them learns where the temple is (on the floodplain, among reeds) and what it is (a house) before arriving, and may guess its tie to the Drowning.

</details>

## Lab / assignment hook

[Lab 05, naming languages that players can tell apart](../labs/lab05.md). You implement the weighted overlap model and a small name generator, then design naming languages for two cultures of your own, tune them to a target ambiguity, and run a blind listening test with classmates. The culture sheets and naming languages go into the cultures chapter of your world bible.

## Sources

- Final Fantasy XIV Online Wiki (consolegameswiki), "Seekers of the Sun" (accessed September 2026), citing *Encyclopaedia Eorzea* vol. 1 pp. 029 and 086-087 and Square Enix forum posts on race naming conventions (2012). Twenty-six tribes each took one letter of the Eorzean alphabet; nunh and tia; G'raha Tia of the G tribe.
- Final Fantasy XIV Online Wiki, "Plainsfolk" and "Dunesfolk", Nomenclature sections (accessed September 2026), citing *Encyclopaedia Eorzea* vol. 1, pp. 84-85, and the Square Enix forum developer post "Race Naming Conventions" (A Realm Reborn era). Rhyme schemes AB-CB and ABB-AB (Plainsfolk), AAB-CCB and AAB-AB (Dunesfolk); clan and gender readable from the name; NPC names Ikuku Iku, Nanamo Ul Namo, Teledji Adeledji.
- UESP, "Lore:Argonian Names" (accessed September 2026). Jel and Tamrielic names; Haj-Ei translated as Hides His Eyes (from *Morrowind* dialogue).
- UESP, "Lore:Dragon Language" (accessed September 2026). Dragon words on Word Walls; the Thu'um; grammar close to English with stated exceptions, citing Game Informer, "Skyrim's Dragon Shouts" (January 2011).
- Wikipedia, "Danelaw" (accessed September 2026). Old Norse place-name endings *-by*, *-thorp* and *-howe* as evidence of Scandinavian settlement.
- Rosenfelder, M. (2010). *The Language Construction Kit*. Yonagu Books.
- Wolf, M. J. P. (2012). *Building Imaginary Worlds: The Theory and History of Subcreation*. Routledge. Chapter 3.

## Interactive spec: examples/w05-name-overlap.html

**The one insight.** Counting shared syllables tells you almost nothing about whether two cultures' names sound alike. What matters is how much of each culture's usage falls on the shared syllables. The count view can even rank the two cultures the wrong way round. A structural marker removes confusion regardless of the weights.

**Model.**

```
o_count(A→B) = |S_A ∩ S_B| / |S_A|
o(A→B)       = Σ w_s over s in S_A ∩ S_B      (A's weights)
P_amb(L)     = (1 − m) × o^L
I(L)         = 1 − P_amb(L)
```

**Default data (the lecture's Vessari and Durhk).**

- Vessari: an 0.20, el 0.15, ra 0.15, to 0.10, ssa, vei, li, mae, sio, ne, qua, ith at 0.05 each.
- Durhk: an 0.05, el 0.05, ra 0.10, to 0.05, durh 0.20, kag 0.20, bor 0.20, gund 0.15.
- Shared: an, el, ra, to.
- `L = 2`, `m = 0`, direction A = Vessari, B = Durhk.

**Layout: two linked views plus a name strip.**

1. *What the bible says* (left, or top on mobile). Two overlapping rounded boxes, one per culture, each divided into equal cells, one per syllable, with the shared cells in the overlap. Label `o_count` for each direction.
2. *What the player hears* (right, or below). For the selected direction, one horizontal bar per syllable of culture A, length proportional to its weight, shared ones in the accent colour. Below the bars, a line chart of `P_amb(L)` for `L = 1..5` (weighted, solid) with the count-view curve `(1 − m) × o_count^L` dashed. A dot marks the selected `L`.
3. *Name strip* (full width, bottom). Twelve names generated from culture A: each name is `L` syllables drawn by weight with a fixed seed (seed 1, "reroll" button changes it). When the marker is on, a share `m` of names (the first `round(12m)` names in the strip) end with a syllable drawn from A-only syllables, renormalized by weight. Underline each name whose syllables all lie in the shared set.

**Readouts.** `o_count` and `o` in both directions; `P_amb(L)` and `I(L)` for the selected direction to one decimal percent; the number of underlined names out of 12.

**Controls.**
- Direction toggle: Vessari→Durhk / Durhk→Vessari.
- One slider per syllable weight for culture A (0 to 0.40, step 0.01); after any change, the other weights of that culture are rescaled proportionally so the total stays 1. A "reset weights" button.
- Name length `L`: 1 to 5.
- Marker share `m`: 0 to 1, step 0.05.
- Keyboard accessible; each slider labelled with its syllable and value.

**Test values.**

| Setting | o_count | o | P_amb(L) |
|---|---|---|---|
| Vessari→Durhk, L=2 | 0.333 | 0.60 | 36.0% (count view 11.1%) |
| Vessari→Durhk, L=3 | 0.333 | 0.60 | 21.6% |
| Durhk→Vessari, L=2 | 0.500 | 0.25 | 6.25% (count view 25.0%) |
| Vessari, L=2, m=0.5 | 0.333 | 0.60 | 18.0% |
| Vessari, L=2, m=1 | 0.333 | 0.60 | 0% |
| Vessari, shared weights rescaled to total 0.30, L=2 | 0.333 | 0.30 | 9.0% |

**Visual notes.** First screen shows the default direction and `L = 2`, with the gap between 11.1% and 36.0% labelled. Use the shared palette tokens. Draw everything generically; no game names in the graphics, which use only the invented cultures.
