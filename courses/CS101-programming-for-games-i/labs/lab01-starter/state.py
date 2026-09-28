# CS101 Lab 01: the state of a text adventure
# Run:   python state.py
# Check: python check_lab01.py
#
# Fill in every TODO. Do not change the format of the STATUS line at the bottom,
# because the checker reads it.

# ---------------------------------------------------------------
# Part A: the starting state. Give each variable the right type.
# ---------------------------------------------------------------
GOLD_CAP = 999          # the most gold the player can carry
LEVEL_BITS = 8          # the level counter is an unsigned 8-bit value

room = "entrance"
gold = 990
lamp_oil = 100          # TODO: oil is a percentage with fractions. Which type should this be?
level = 250
lamp_lit = "False"      # TODO: this is a flag. Is a string the right type?

# ---------------------------------------------------------------
# Part B: read three values from the keyboard.
# input() always returns a string. Convert each one.
# ---------------------------------------------------------------
found_text = input("Coins found: ")
oil_text = input("Oil used (percent): ")
levels_text = input("Levels gained: ")

found = found_text      # TODO: convert to int
oil_used = oil_text     # TODO: convert to float
levels_gained = levels_text   # TODO: convert to int

# ---------------------------------------------------------------
# Part C: the player lights the lamp and walks north to the hall.
# ---------------------------------------------------------------
# TODO: set lamp_lit to the right boolean value
# TODO: set room to "hall"
# TODO: subtract oil_used from lamp_oil

# ---------------------------------------------------------------
# Part D: gold is CLAMPED at GOLD_CAP. It never goes above it.
# Hint: min(a, b) gives the smaller of two numbers.
# ---------------------------------------------------------------
gold = gold             # TODO: add found, but never exceed GOLD_CAP

# ---------------------------------------------------------------
# Part E: the level counter WRAPS like Pac-Man's 8-bit counter.
# Hint: the lecture's model is stored = true_value % 2 ** bits
# ---------------------------------------------------------------
level = level           # TODO: add levels_gained and wrap to LEVEL_BITS bits

# Do not edit below this line.
print(f"STATUS room={room} gold={gold} oil={float(lamp_oil):.1f} level={level} "
      f"lit={lamp_lit} types={type(lamp_oil).__name__},{type(lamp_lit).__name__}")
