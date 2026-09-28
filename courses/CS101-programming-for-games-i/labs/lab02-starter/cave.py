# CS101 Lab 02: a cave with a way out
# Run:   python cave.py
# Check: python check_lab02.py
#
# The program handles ONE decision and prints ONE line, so the checker can test
# many situations. Week 3 wraps it in a loop.
#
# Map (arrows are legal moves):
#
#            [vault]            the vault door is locked unless has_key is "yes"
#               ^ north
#               | south
#  [well] <-west-- [hall] --east-> [armory]
#         --east->        <-west--
#               ^ north
#               | south
#          [entrance]
#
# Output formats (exactly one line):
#   ROOM <room>                 after a legal move
#   LOCKED                      trying to go north from the hall without the key
#   BLOCKED                     any other command or direction with no arrow
#   RESULT <result>             for a duel: "P1 wins", "P2 wins", "sudden death" or "keep playing"

mode = input("Mode (move/duel): ").strip().lower()

if mode == "move":
    room = input("Room: ").strip().lower()
    has_key = input("Has key (yes/no): ").strip().lower() == "yes"
    command = input("> ").strip().lower()

    # -----------------------------------------------------------
    # Part A: movement. Two moves are done for you. Add the rest.
    # Part B: the vault is north of the hall and needs the key.
    #         Without the key, print LOCKED and stay put.
    #         Watch the order of your branches.
    # -----------------------------------------------------------
    if room == "entrance" and command == "north":
        print("ROOM hall")
    elif room == "hall" and command == "south":
        print("ROOM entrance")
    # TODO: hall <-> well, hall <-> armory, hall <-> vault (with the key rule)
    else:
        print("BLOCKED")

elif mode == "duel":
    p1_hp = int(input("P1 hp after damage: "))
    p2_hp = int(input("P2 hp after damage: "))

    # -----------------------------------------------------------
    # Part C: resolve the duel for ALL FOUR cases, including overkill
    # (negative hp). This naive chain is wrong in some of them.
    # -----------------------------------------------------------
    if p2_hp == 0:
        print("RESULT P1 wins")
    elif p1_hp == 0:
        print("RESULT P2 wins")
    else:
        print("RESULT keep playing")

else:
    print("BLOCKED")
