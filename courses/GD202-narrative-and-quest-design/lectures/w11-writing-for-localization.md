# GD202 · Week 11 — Writing for Localization

**Why this matters:** Most of your players may not read English. The way you write a line in English decides whether a translator can make it correct in Russian, Arabic or Japanese, or whether the game will print broken grammar that no translator can fix. This week you learn the handful of writing habits that make text translatable, and the math behind the most common bug, plurals.

**You will be able to:**
- Compute the plural category a number takes in English, French, Russian, Polish, Arabic and Japanese from the CLDR rules, and count how many forms a string needs in each language.
- Estimate the space a UI string needs after translation from its English length, and explain why short strings are the risky ones.
- Rewrite concatenated or English-only strings into whole-sentence strings with named placeholders and plural selectors.
- Critique a localization kit by listing what a translator would still have to guess.

**Before class:** W3C Internationalization, "Text size in translation" (free online, 10 minutes). ICU User Guide, "Formatting Messages", the overview and "Complex Argument Types" sections (free online, 15 minutes). From the course text, Bateman (ed.), *Game Writing: Narrative Skills for Videogames* (2nd ed., Bloomsbury, 2021), use the contents page to find its material on localization and read it.

**Prerequisites from earlier courses:** [GD202 week 4, dialogue systems and state flags](w04-dialogue-systems-and-state-flags.md) (how lines are selected and stored). [GD202 week 2, the player as co-author](w02-the-player-as-co-author.md) (the name problem, which this week finishes). [CS102 week 13, data-driven design](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w13-data-driven-design-stats-in-json-and-csv.md) (keeping content in data files instead of code). [UX201 week 10, HUD and information design](../../UX201-game-ux-and-player-psychology/lectures/w10-hud-and-information-design.md), running alongside this course, for text in the interface.

**Interactive:** [`examples/w11-plural-rules.html`](../examples/w11-plural-rules.html). Keep it open during section 2.

---

## 1. Localization is a writing problem

**Localization** (often shortened to l10n, for the 10 letters between l and n) is adapting a game for a language and region: translating text and voice, and also changing formats, fonts, references and sometimes content. **Internationalization** (i18n) is the engineering work that makes localization possible: strings kept out of code, fonts that cover the needed characters, layouts that grow.

Writers tend to think localization belongs to translators and programmers. It doesn't. Translators receive a **localization kit**: a spreadsheet or database of strings, each with an ID, the English text, sometimes a character limit, and sometimes a note. They often see the strings out of order and without the game running. Every decision you made while writing arrives with them as either something they can work with or something they have to guess.

Three kinds of English habit break localization:

1. **Grammar baked into code.** "You killed " + n + " wolf" + (n == 1 ? "" : "s"). This works in English and cannot be translated correctly into most other languages. Section 2 shows why with numbers.
2. **Sentences built from pieces.** "You found " + item + " in " + place + ".". Other languages reorder the pieces and change their endings to agree with each other. Section 4.
3. **No room to grow.** A button sized for "Accept" gets a translation twice as long. Section 3.

All three are cheap to avoid while writing and expensive to fix after the text ships to translators.

## 2. Worked example: the plural trap

### The hook

World of Warcraft's interface strings contain a small grammar language of their own, documented on the Warcraft Wiki. A code `|4` picks between a singular and a plural form based on the number before it, so a string can read "1 car" or "2 cars". For the Russian client the same code takes *three* forms instead of two. Other codes pick Korean object particles based on whether the previous word ends in a vowel, choose French "de" or "d'" before a vowel, decline Russian nouns into different grammatical cases, and choose English "a" or "an".

A game company built grammar into its string system for one reason. Its writers' strings would otherwise print wrong text in half its languages. The most common way they go wrong is the plural. So ask the question precisely. *For a count `n`, which form of the noun does each language need, and how many forms must a translator write?*

### The model

The Unicode Common Locale Data Repository (**CLDR**) defines, for each language, a function from a number to a **plural category**. There are six category names: `zero`, `one`, `two`, `few`, `many` and `other`. Each language uses some of them. `other` is always present as the fallback.

For whole numbers `n ≥ 0`, the CLDR 48 rules for six languages are:

| Language | Categories used | Rule for whole numbers |
|---|---|---|
| English | one, other | `one` if n = 1, else `other` |
| French | one, many, other | `one` if n is 0 or 1; `many` if n is a nonzero multiple of 1,000,000; else `other` |
| Russian | one, few, many | `one` if n mod 10 = 1 and n mod 100 ≠ 11; `few` if n mod 10 is 2-4 and n mod 100 is not 12-14; else `many` |
| Polish | one, few, many | `one` if n = 1; `few` as Russian; else `many` |
| Arabic | zero, one, two, few, many, other | `zero` 0, `one` 1, `two` 2; `few` if n mod 100 is 3-10; `many` if n mod 100 is 11-99; else `other` |
| Japanese | other | `other` for every number |

(Russian and Polish also use `other`, but only for fractions, which a kill counter never shows.)

The number of forms a translator must write for a counted noun is the number of categories that the game's possible values of `n` can reach. For counts from 0 to 100, that is 2 for English, 2 for French, 3 for Russian, 3 for Polish, 6 for Arabic and 1 for Japanese.

The mistake an English writer makes is to assume every language has English's rule. In code, that looks like a two-slot system: one string for `n = 1`, another for everything else.

### Numbers you can check

Here is the model in Python, and its output for a few counts:

```python
def category(lang, n):
    """CLDR 48 cardinal plural category for a whole number n >= 0."""
    if lang == "en":
        return "one" if n == 1 else "other"
    if lang == "fr":
        if n in (0, 1):
            return "one"
        return "many" if n % 1_000_000 == 0 else "other"
    if lang in ("ru", "pl"):
        if lang == "pl" and n == 1:
            return "one"
        if lang == "ru" and n % 10 == 1 and n % 100 != 11:
            return "one"
        if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
            return "few"
        return "many"
    if lang == "ar":
        if n <= 2:
            return ["zero", "one", "two"][n]
        if 3 <= n % 100 <= 10:
            return "few"
        if 11 <= n % 100 <= 99:
            return "many"
        return "other"
    return "other"  # ja: one form for every number

for n in [0, 1, 2, 5, 11, 21, 22, 101]:
    print(n, [category(lang, n) for lang in ["en", "fr", "ru", "pl", "ar", "ja"]])
```

```
0 ['other', 'one', 'many', 'many', 'zero', 'other']
1 ['one', 'one', 'one', 'one', 'one', 'other']
2 ['other', 'other', 'few', 'few', 'two', 'other']
5 ['other', 'other', 'many', 'many', 'few', 'other']
11 ['other', 'other', 'many', 'many', 'many', 'other']
21 ['other', 'other', 'one', 'many', 'many', 'other']
22 ['other', 'other', 'few', 'few', 'many', 'other']
101 ['other', 'other', 'one', 'many', 'other', 'other']
```

Check three cells by hand. French 0 is `one`, so "0 loup" is singular in French, where English says "0 wolves". Russian 21 is `one`, since 21 mod 10 = 1 and 21 mod 100 = 21 ≠ 11, so 21 takes the same noun form as 1. Polish 21 is `many`, since Polish's `one` is only for 1 itself. Two languages that look alike to an English speaker disagree on a number as ordinary as 21.

Now measure the damage of a two-slot system. Give each language only a singular slot (used when `n = 1`) and a plural slot (used otherwise), and let the translator fill the plural slot with the single form that is right most often. Count the numbers from 0 to 100 that still come out wrong:

| Language | Forms needed (0-100) | Best form for the plural slot | Wrong counts out of 101 | Examples of wrong counts |
|---|---|---|---|---|
| English | 2 | other | 0 | none |
| French | 2 | other | 1 | 0 |
| Russian | 3 | many | 35 | 2, 3, 4, 21, 22, 31 |
| Polish | 3 | many | 27 | 2, 3, 4, 22, 23, 24 |
| Arabic | 6 | many | 11 | 0, 2, 3-10, 100 |
| Japanese | 1 | other | 0 | none (one slot is wasted) |

Check the Russian row. `few` covers three numbers in each decade (2-4, 22-24, and so on up to 92-94) except the teens, so 27 numbers. `one` covers 1, 21, 31, ..., 91. The singular slot catches only 1, so the other 8 are wrong. That makes 27 + 8 = 35.

**One Russian count in three prints the wrong noun form.** And look at *which* counts. A tester who checks 1, 2 and 10 sees one bug, at 2. A tester who checks 1, 5 and 10 sees none, then players at 21 kills see "21 wolves" in the wrong form.

### A visual you can move

Open the interactive. The left view is a 10 by 10 grid of the numbers 0 to 99 plus 100, colored by the chosen language's plural category, with a text label in each cell. The right view shows the same grid under a two-slot system, with every wrong cell marked. Switch from English to Russian and watch the few-stripes appear in every decade except the teens. Drag the count slider and read the category in all six languages at once.

### Cross-game recognition

Three systems, one idea. Each is a function from a number to a category, then a choice of string.

**World of Warcraft (retail client, grammar codes as documented on the Warcraft Wiki in 2026).** `|4singular:plural;` is a two-category rule. The Russian variant `|4form1:form2:form3;` is a three-category rule, matching the three categories Russian needs for whole numbers. The game's string system is a hand-built version of the CLDR function above.

**Yarn Spinner (version 3.x, the dialogue tool you meet in week 12).** Its `plural` markup takes a value and one string per CLDR category, such as `[plural value={$pie_count} one="a pie" other="% pies" /]`, and picks the category using the player's language. The documentation notes that English uses only `one` and `other`. A Russian translator adds `few` and `many` without touching the English line.

**ICU MessageFormat (the Unicode library many engines and apps use).** A `plural` argument selects a sub-message by category using the language's rules. The ICU guide adds that the translation system and the translator need to add `one`, `few` and the rest as each target language requires. Same function, same categories.

### Eyes-open design judgment

- **Strength of plural selectors:** they move the grammar decision to the translator, the only person who knows it. Your code stays the same for every language.
- **Strength:** the categories come from CLDR data, not from a programmer's memory of what they learned in school. CLDR is updated. When a rule changes, you update data, not code.
- **Cost:** every counted string grows from one line in the kit to up to six. Translators must understand the syntax, and a broken bracket breaks the string. Budget review time for it.
- **Cost:** plural selectors fix the noun. Adjectives and verbs agreeing with the count in the same sentence are the translator's job, and they need the whole sentence inside the selector to do it. ICU recommends putting full sentences in each branch for this reason.
- **Decide deliberately:** whether a count needs to be shown at all. "Wolves slain: 21" is a label and a number. It sidesteps agreement in many languages, at the cost of sounding like a spreadsheet. For a quest tracker, that trade is often right. For a character's spoken line, it isn't.

### Check yourself (worked example)

1. What category does 112 take in Russian? In Arabic? In Polish?
2. A quest tracker shows counts from 0 to 30. How many forms does a Polish translator need for "wolves"? How many for Arabic?
3. Your engine only supports two slots. A Russian translator fills the plural slot with the `few` form instead of `many`. For 0 to 100, how many counts are now wrong?

<details>
<summary>Answers</summary>

1. Russian: 112 mod 10 = 2, but 112 mod 100 = 12, which is excluded, so `many`. Arabic: 112 mod 100 = 12, in 11-99, so `many`. Polish: same test as Russian's `few`, so `many`.
2. Polish, 3 (`one` at 1, `few` at 2-4 and 22-24, `many` elsewhere). Arabic, 5 (`zero`, `one`, `two`, `few` for 3-10, `many` for 11-30). `other` needs a value like 100 and isn't reached.
3. The plural slot is right only for the 27 `few` numbers. Wrong: 65 `many` numbers plus 8 `one` numbers other than 1, so 73.

</details>

## 3. Text expansion: short strings break first

Translations are usually longer than English, and the difference is largest for short strings. The W3C's article on text size reproduces IBM's guideline table of average expansion for English text translated into European languages:

| English length (characters) | Average translated length, as a share of the English |
|---|---|
| Up to 10 | 200-300% |
| 11-20 | 180-200% |
| 21-30 | 160-180% |
| 31-50 | 140-160% |
| Over 70 | 130% |

The same article gives a real interface example: the English label "views" became "visualizzazioni" in Italian, three times as long. Short strings have little room for the grammar and compound words other languages need. Long strings average out.

The W3C table also has a row for 51-70 characters, but its printed value is higher than the 31-50 row and breaks the falling trend of every other band. It is most likely a transcription error, so this lecture leaves it out. For strings of 51-70 characters the code below keeps the 31-50 factor of 1.6. Expansion falls with length, so that errs large, and a budget that errs large is safer than one that errs small. If your team has its own measurements from past games, use those instead.

```python
def budget(text):
    """Characters to reserve for a translation of an English UI string,
    using the top of each band in the W3C copy of IBM's expansion table,
    with the doubtful 51-70 row replaced by the 31-50 factor."""
    n = len(text)
    if n <= 10:
        factor = 3.0
    elif n <= 20:
        factor = 2.0
    elif n <= 30:
        factor = 1.8
    elif n <= 70:
        factor = 1.6
    else:
        factor = 1.3
    return n, round(n * factor)

for s in ["OK", "Accept", "Quest Log", "Abandon quest", "Hand in the wolf pelts",
          "Speak to the ferryman at Low Crossing before dusk",
          "The bridge is gone. Cross at the ford, a mile south of the ruins, and hurry."]:
    print(budget(s), s)
```

```
(2, 6) OK
(6, 18) Accept
(9, 27) Quest Log
(13, 26) Abandon quest
(22, 40) Hand in the wolf pelts
(49, 78) Speak to the ferryman at Low Crossing before dusk
(76, 99) The bridge is gone. Cross at the ford, a mile south of the ruins, and hurry.
```

Two things stand out. "Accept" needs three times its width and the 76-character sentence needs 1.3 times. And "Quest Log" (9 characters) gets a larger budget than "Abandon quest" (13), because the bands are steps. In practice, take the larger of a string's own budget and the budget of the longest string in the band below.

**Pokémon, a shipped example of a length budget.** In the main-series Pokémon games of Generations I to V, a Pokémon's nickname can be at most 5 characters in Japanese and 10 in Western languages. From Generation VI the limits are 6 and 12. The ratio stays at 2 across the change, which is the kind of budget this section recommends. Japanese is compact because each kana character is a syllable, so the Western limit has to be double.

A technique to find layout problems before translators start is **pseudo-localization**. You generate a fake "language" from your English strings by lengthening each one (for example, padding it by the budget factor) and swapping letters for accented look-alikes, then play the game in it. Truncated text, overlapping labels and strings that stay plain English (because someone hard-coded them) show up at once.

## 4. Pieces, order and agreement

Here is a string a programmer might build:

```
"You found " + item + " in " + place + "."
```

It prints "You found a rusty key in the old mill." In English, the pieces come in that order and never change form. In other languages:

- **Word order moves.** Japanese normally puts the verb at the end, so "found" has to come after both the item and the place. No translation of the three fixed fragments can do that.
- **Articles and adjectives agree.** In French and German, the article in front of "key" depends on the noun's grammatical gender. In the concatenated string the article is either baked into the fragment (and wrong for half the items) or missing.
- **Nouns change form.** In Russian the item and the place take different case endings because of their roles in the sentence. That's why World of Warcraft has a declension code for Russian names, and a code for French "de" versus "d'", and one for Korean particles, which change depending on the sound at the end of the word before them.

The ICU guide states the fix plainly. A message has to be written and translated as one unit, a whole string with placeholders, because translators can't rearrange fragments. So write this instead:

```
FOUND_ITEM = "You found {item} in {place}."
```

The translator can now move `{item}` and `{place}` wherever their language wants them. When agreement matters, give the translator what they need: the grammatical gender of each item name as data, and a `select` on that gender inside the string (ICU's `select` argument does this), or a set of full sentences per gender. The ICU guide recommends putting such selectors on the outside of the message with full sentences in each branch, and nesting at most one plural inside.

Even English grammar is hard to compute. Any code that picks "a" or "an", like WoW's `|5`, has to decide from the next word. English picks the article by the *sound* at the start of that word, not the letter, so "an hour" and "a university" defeat a rule that only checks for a vowel letter. That is one more reason to hand grammar to translators with the whole sentence in view instead of computing it.

**The player's name.** Week 2 raised the name problem for voiced games. For text games, a typed name is a placeholder whose grammatical gender and case the game doesn't know. The safest lines use the name alone, as an address or a label ("Aldo, the gate is open."), not in positions where the language would have to inflect it. If the game asks the player to choose a pronoun or gendered form, store that choice and let translators `select` on it.

## 5. Habits that help every translator

These cost little while writing, and each one removes a guess.

- **One string, one context note.** "Close" could be a verb (close the window) or an adjective (the enemy is close). A note of ten words ("Button: closes the map screen") saves a bug report.
- **Stable string IDs.** A translation is attached to an ID, not to the English text, so a typo fix in English doesn't orphan every translation. Yarn Spinner adds a `#line:` tag with a unique ID to every line for exactly this reason (week 12).
- **Character limits in the kit.** If a string must fit a button, say so, and give the limit in characters or, better, in pixels with the font named.
- **No text in images.** Every piece of text baked into a texture needs an artist to redo the image for each language. Keep text as live strings over the art.
- **Numbers, dates and money through the formatter.** Decimal separators differ: 4.51 in English is 4,51 in German. Yarn Spinner's documentation gives this exact example and adds a `format_invariant` function for numbers that go to game code rather than to the screen.
- **Puns and wordplay flagged, with the intent.** A translator can replace an English pun with a local one if they know it's a pun and what it does in the scene. Write the intent in the note ("a joke about the ferryman's fear of water").
- **Proper nouns listed.** Give translators a glossary: which names are translated (a place called "the Drowned Market" probably is) and which are kept (a character called "Orsa Venn" probably is not). Inconsistent names across 10,000 strings are a common complaint in translated games.
- **Consistent verbs for UI actions.** If the button says "Hand in", the quest text shouldn't say "turn in" and the tutorial "deliver". Each synonym becomes a separate choice for each translator.

## In-class activity (25 minutes)

Groups of three. Your instructor hands out 12 strings from an invented quest, as a programmer wrote them (with concatenation, English plurals and no notes), plus the UI widths in characters for four of them.

1. Mark every string that breaks in at least one of the six languages in section 2, and say which rule it breaks (plural, concatenation, agreement, expansion or ambiguity).
2. Rewrite each broken string as a whole sentence with named placeholders. Use a plural selector with the categories each language needs. For one counted string, write out the Russian and Arabic category lists a translator would fill in (in English, as notes on which form goes where; you don't need to know the languages).
3. Run the four UI strings through the budget rule from section 3. Which ones overflow their widths?
4. Write a context note of at most 12 words for each string.

Expected output: the rewritten strings with notes, the category lists, and the list of overflowing UI strings with their budgets.

## Common misconceptions

- **"Plural means adding s, so the translator just changes the ending."** The number of forms and the rule that picks between them change from language to language. Russian needs three forms for whole numbers and Arabic six, and the right one for 21 differs between Russian and Polish.
- **"Short strings are easy to localize."** Short strings expand the most, up to three times, and have no room to reflow.
- **"Concatenation is fine if every fragment is translated."** Fragments can't be reordered, and they can't agree with each other. Translate whole sentences.
- **"Testing 1, 2 and 10 covers plurals."** In Russian, 21, 22 and 25 fall in three different categories. Test with a spread across decades and teens: 0, 1, 2, 5, 11, 21, 22, 25, 101, 111.

## Check yourself

1. Which of these counts take the same category as 1 in Russian: 11, 21, 101, 111, 1001?
2. A button is 24 characters wide. Which of these English labels will need a wider button after translation into European languages, using the section 3 budget: "Save" (4 characters), "Continue" (8), "Return to camp" (14)?
3. Rewrite `"Deliver " + n + " pelt" + (n == 1 ? "" : "s") + " to " + npc` as a string a translator can localize. Name the placeholders.
4. A writer wants to avoid plural selectors entirely by writing "Pelts: 3/10" in the tracker. Give one advantage and one cost.
5. A string system picks "a" or "an" by checking whether the next word starts with a vowel letter. What does it print before "university" and before "hour", and what is the general lesson?

<details>
<summary>Answers</summary>

1. 21, 101 and 1001 (last digit 1, last two digits not 11). 11 and 111 end in 11, so they are `many`.
2. "Save": budget 12, fits. "Continue": budget 24, just fits. "Return to camp": 14 characters, budget 28, needs a wider button or a shorter label.
3. `DELIVER_PELTS = "{n, plural, one {Deliver # pelt to {npc}.} other {Deliver # pelts to {npc}.}}"` in ICU style, with `n` and `npc` as named placeholders. Translators add `few`, `many` and other categories as their language needs, and can reorder `{npc}` freely. Any equivalent with whole sentences per category is right.
4. Advantage: no agreement between number and noun in most languages, and a short string. Cost: it reads like a spreadsheet and the label "Pelts" still needs a form chosen by the translator. It works for trackers and fails for dialogue.
5. "an university" and "a hour", both wrong, because the article depends on the sound at the start of the word, not the letter. Grammar computed from spelling by code is fragile. Give translators and writers the whole sentence.

</details>

## Lab hook

[Lab 11, localization linter](../labs/lab11.md). You implement the CLDR plural function for six languages, a width-budget check and a concatenation detector, run the linter on a supplied 30-string quest file, and fix every string it flags. Deliverable: the passing linter, the fixed string file with context notes, and a one-page report.

## Sources

- Warcraft Wiki, "UI escape sequences", Grammar section (World of Warcraft retail client, retrieved September 2026). `|4` singular and plural, with a three-form variant for ruRU; `|1` Korean particles; `|2` French de/d'; `|3` Russian declension; `|5` English a/an.
- Unicode CLDR, "Language Plural Rules" chart, and `cldr-json` `plurals.json` (CLDR version 48). Cardinal plural categories and rules for English, French, Russian, Polish, Arabic and Japanese.
- W3C Internationalization, "Text size in translation" (retrieved September 2026). IBM's expansion table for English into European languages; the "views" to "visualizzazioni" example.
- ICU User Guide, "Formatting Messages" (ICU documentation, retrieved September 2026). Messages as single units with placeholders; plural and select arguments; select outside, full sentences inside; translators add plural categories per language.
- Yarn Spinner documentation, version 3.1: "Markup" (`plural` and `ordinal` markers using CLDR categories), "Tags and Metadata" (`#line` IDs for localization) and "Functions" (`format_invariant` and the 4,51 versus 4.51 example).
- Bulbapedia, "Nickname" (retrieved September 2026). Maximum nickname length of 10 characters in Western languages and 5 in Japanese in Generations I to V; 12 and 6 from Generation VI.

## Interactive spec: examples/w11-plural-rules.html

**Purpose.** Let students see that plural categories are a function of the number that differs by language, and that a two-slot (English-style) system produces errors scattered through every decade, not only at small numbers.

**The one insight the visual must make obvious.** Under a two-slot system, Russian gets one count in three wrong, and the wrong counts form stripes (2-4, 22-24, ... and 21, 31, ...) that a tester checking 1, 5 and 10 would never hit.

**Layout.** Two linked views, side by side at 1280 px, stacked at 390 px. A strip of six language chips underneath.

- Left, "What the language needs": the numbers 0 to 99 as a 10 by 10 grid (row = tens digit, column = ones digit), plus a separate cell for 100 under the grid. Each cell shows the number and a short category label (`one`, `few`, `many`, `two`, `zero`, `other`) and is colored by category using six palette tokens. Color is never the only cue: the label is always printed, and `few` and `many` also get distinct hatch patterns. A legend lists the categories this language uses and how many cells each covers.
- Right, "What a two-slot system prints": the same grid. Each cell is marked correct (plain) or wrong (strong outline, negative token and a cross glyph). Above it print "Wrong: W of 101 (x%)" and "Best plural-slot form: F".
- Language chips (below both views): one chip per language (English, French, Russian, Polish, Arabic, Japanese) showing the category the current slider value `n` takes in that language. Clicking a chip selects that language for both grids.

**Controls** (keyboard accessible, values printed):

- Language: radio group, default Russian.
- Count `n`: slider 0 to 200 plus a number input accepting up to 10,000,000. The cell for `n` (if at most 100) is highlighted in both grids; the chips update.
- Plural slot form: a select with "best (automatic)" and each category the language uses. Changing it recomputes the right grid, so students can see what happens if a translator picks `few` for Russian.
- "Tester's picks" toggle: overlays small dots on 1, 2, 5, 10 (a typical manual test), and prints how many of the wrong cells those four hit.
- Reset button.

**Formulas.** The six rules for whole numbers from lecture section 2 (CLDR 48):

- en: `one` if n = 1, else `other`.
- fr: `one` if n ∈ {0, 1}; `many` if n ≠ 0 and n mod 1,000,000 = 0; else `other`.
- ru: `one` if n mod 10 = 1 and n mod 100 ≠ 11; `few` if n mod 10 ∈ {2, 3, 4} and n mod 100 ∉ {12, 13, 14}; else `many`.
- pl: `one` if n = 1; `few` as ru; else `many`.
- ar: `zero` 0; `one` 1; `two` 2; `few` if n mod 100 ∈ [3, 10]; `many` if n mod 100 ∈ [11, 99]; else `other`.
- ja: `other`.
- Two-slot system: for n = 1 it prints the form for category(1); for every other n it prints the plural-slot form. A cell is wrong if that form's category differs from category(n). "Best" is the category that minimizes wrong cells over 0 to 100 (ties go to the one listed first in the language's category list).

**Test values** (0 to 100, best automatic slot).

| Language | Categories (counts over 0-100) | Best slot | Wrong |
|---|---|---|---|
| en | one 1, other 100 | other | 0 |
| fr | one 2, other 99 | other | 1 |
| ru | one 9, few 27, many 65 | many | 35 |
| pl | one 1, few 27, many 73 | many | 27 |
| ar | zero 1, one 1, two 1, few 8, many 89, other 1 | many | 11 |
| ja | other 101 | other | 0 |

Russian with the plural slot forced to `few`: 73 wrong. Tester's picks (1, 2, 5, 10) on Russian with `many`: they hit 1 wrong cell (2). Spot checks for the chips: n = 21 gives en other, fr other, ru one, pl many, ar many, ja other; n = 1,000,000 gives fr many; n = 111 gives ru many, ar many.

**First screen.** Russian selected, `n = 21`, best slot. The right grid already shows 35 wrong cells. Caption above the views: "Two plural forms work in English. Here is what they do in Russian."

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css` inline, light and dark themes, reduced motion respected. Grids are real tables with row and column headers so screen readers can read a cell's number and category. The results line is an `aria-live` region. No game art; no game names in the visual.
