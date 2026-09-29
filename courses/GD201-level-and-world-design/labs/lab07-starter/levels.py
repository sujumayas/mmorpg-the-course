"""Level data for GD201 Lab 07. Do not edit; copy a level if you want to change it.

Each level has `heights` (metres above the valley floor) and `edges`:
  ("run",    a, b, d)  flat, two-way, d metres
  ("slope",  a, b, d)  two-way path of length d; slower going uphill (decided by heights)
  ("drop",   a, b)     one-way, from the higher node down to the lower one
  ("ladder", a, b)     two-way, climbing up and climbing down at different speeds
"""

CLIFF_RUIN = {  # the lecture's level, with the ledge and without the ladder
    "heights": {"Camp": 12, "Overlook": 12, "Ledge": 6, "Ruin": 0, "Gate": 0},
    "edges": [
        ("run", "Camp", "Overlook", 30),
        ("drop", "Overlook", "Ledge"),
        ("drop", "Ledge", "Ruin"),
        ("drop", "Overlook", "Ruin"),      # 12 m: unsafe, must not become an edge
        ("run", "Ruin", "Gate", 60),
        ("slope", "Camp", "Gate", 150),
    ],
}

QUARRY = {
    "heights": {"Hub": 20, "Scaffold": 20, "Office": 14, "Shelf": 14,
                "Pit": 7, "Sump": 0, "Crusher": 0, "Road": 0},
    "edges": [
        ("run", "Hub", "Scaffold", 24),
        ("drop", "Scaffold", "Shelf"),     # 6 m
        ("drop", "Scaffold", "Pit"),       # 13 m, unsafe
        ("slope", "Hub", "Office", 40),
        ("run", "Office", "Shelf", 30),
        ("drop", "Shelf", "Pit"),          # 7 m
        ("drop", "Pit", "Sump"),           # 7 m
        ("slope", "Pit", "Crusher", 50),
        ("run", "Sump", "Crusher", 30),
        ("run", "Crusher", "Road", 80),
        ("slope", "Road", "Hub", 200),
    ],
}

# Shortcuts the art team can afford to build. Pick one.
QUARRY_CANDIDATES = [
    ("ladder", "Pit", "Shelf"),
    ("ladder", "Sump", "Scaffold"),
    ("ladder", "Crusher", "Office"),
    ("slope", "Crusher", "Hub", 140),
]
