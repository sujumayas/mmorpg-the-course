# CS101 Lab 03, part 1: loop the cave
# Run:   python loop_cave.py
# Check: python check_lab03.py
#
# Same map as Lab 02, plus a key lying in the armory.
#
#            [vault]
#               |
#  [well] --- [hall] --- [armory]   (type "take key" in the armory)
#               |
#          [entrance]
#
# Rules
#   - Every command, legal or not, costs one move (except "quit").
#   - Reaching the vault wins.        Print: WIN in <moves> moves
#   - After MAX_MOVES moves, you lose. Print: LOSE lamp out
#     If the move that reaches the vault is also move MAX_MOVES, you WIN.
#   - "quit" ends the game.           Print: QUIT
#   - After every other command print one line: ROOM <room>, LOCKED, KEY or BLOCKED
#
# Right now the program plays exactly ONE turn. Part A: wrap the turn in a
# while loop controlled by the flag `playing`, so it keeps going until the game ends.

MAX_MOVES = 15

room = "entrance"
has_key = False
moves = 0
playing = True

# TODO (Part A): put the turn below inside a loop that runs while playing is True.
# Indent the whole turn by four spaces.

command = input("> ").strip().lower()

if command == "quit":
    print("QUIT")
    playing = False
else:
    moves = moves + 1

    # Change the state
    if room == "entrance" and command == "north":
        room = "hall"
        print("ROOM hall")
    elif room == "hall" and command == "south":
        room = "entrance"
        print("ROOM entrance")
    elif room == "hall" and command == "west":
        room = "well"
        print("ROOM well")
    elif room == "well" and command == "east":
        room = "hall"
        print("ROOM hall")
    elif room == "hall" and command == "east":
        room = "armory"
        print("ROOM armory")
    elif room == "armory" and command == "west":
        room = "hall"
        print("ROOM hall")
    # TODO (Part B): "take key" in the armory sets has_key and prints KEY.
    # TODO (Part B): north from the hall goes to the vault with the key, else prints LOCKED.
    else:
        print("BLOCKED")

    # Check the outcome once per turn
    # TODO (Part C): win if the room is the vault, lose when moves reaches MAX_MOVES.
    # Both must set playing to False. Think about which check goes first.
