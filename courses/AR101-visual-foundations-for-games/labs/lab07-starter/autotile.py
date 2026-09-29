"""AR101 Lab 07 starter: autotile indices and the seam ratio. Standard library only.

Fill in the four TODO functions, then run the tests from the repository root:

    .venv/bin/python courses/AR101-visual-foundations-for-games/labs/lab07-starter/test_autotile.py

A map is a list of rows. 1 is the painted terrain (path), 0 is anything else.
Cells outside the map count as 0. Bit values follow the week 7 lecture:

    edge rule  N=1  E=2  S=4  W=8
    blob rule  N=1  NE=2  E=4  SE=8  S=16  SW=32  W=64  NW=128
"""

EDGE = [(-1, 0, 1), (0, 1, 2), (1, 0, 4), (0, -1, 8)]
BLOB = [(-1, 0, 1), (-1, 1, 2), (0, 1, 4), (1, 1, 8),
        (1, 0, 16), (1, -1, 32), (0, -1, 64), (-1, -1, 128)]


def filled(grid, r, c):
    """True if (r, c) is inside the map and painted."""
    return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == 1


def edge_index(grid, r, c):
    """TODO 1. Return the 4-bit edge index (0-15) of cell (r, c)."""
    raise NotImplementedError("edge_index() is yours to write")


def corner_rule(raw):
    """TODO 2. Take a raw 8-bit neighbour pattern (0-255) and clear every corner
    bit (NE, SE, SW, NW) whose two neighbouring edge bits are not both set.
    Return the reduced pattern."""
    raise NotImplementedError("corner_rule() is yours to write")


def blob_index(grid, r, c):
    """TODO 3. Return the blob index of cell (r, c): the raw 8-bit pattern of its
    neighbours, passed through corner_rule()."""
    raise NotImplementedError("blob_index() is yours to write")


def seam_ratio(tile):
    """TODO 4. tile is a square list of rows of lightness values (0-100).

    d_in   = mean absolute difference over every pair of horizontally or
             vertically adjacent pixels inside the tile.
    d_wrap = mean absolute difference over the pairs that meet when the tile
             repeats: tile[r][-1] with tile[r][0] for every row, and
             tile[-1][c] with tile[0][c] for every column.

    Return d_wrap / d_in. If d_in is 0, return float('inf') when d_wrap > 0
    and 1.0 when both are 0 (a flat tile has no seam)."""
    raise NotImplementedError("seam_ratio() is yours to write")


def tiles_used(grid, rule="blob"):
    """Sorted list of distinct indices a map needs (painted cells only)."""
    f = blob_index if rule == "blob" else edge_index
    return sorted({f(grid, r, c) for r in range(len(grid))
                   for c in range(len(grid[0])) if grid[r][c] == 1})


if __name__ == "__main__":
    plaza = [[0, 0, 0, 0, 0],
             [0, 1, 1, 1, 0],
             [0, 1, 1, 1, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0]]
    print("edge tiles used:", tiles_used(plaza, "edge"))
    print("blob tiles used:", tiles_used(plaza, "blob"))
