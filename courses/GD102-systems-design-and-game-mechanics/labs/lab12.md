# GD102 · Lab 12: Cave generator

**Week:** 12, emergent behavior from simple rules ([lecture](../lectures/w12-emergent-behavior-from-simple-rules.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the Machinations models and exercises component (30%).

## Objective

Run a cellular-automaton cave generator, reproduce the lecture's dial table, add a connectivity repair, and tune the generator to meet a design target. You practice the habit that matters most with emergent systems: measure the distribution over many seeds instead of judging one output by eye.

## Starter materials

The full starter program is below. Save it as `cave.py`. It needs only the Python standard library. The generator matches the lecture's interactive spec, so your numbers must match the lecture's tables exactly.

```python
# cave.py - GD102 lab 12 starter
W, H = 64, 40

def mulberry32(seed):
    a = seed & 0xFFFFFFFF
    def rand():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rand

def noise(p, seed):
    rand = mulberry32(seed)
    grid = []
    for y in range(H):
        row = []
        for x in range(W):
            v = rand()  # draw for every cell so the sequence is stable
            border = x == 0 or y == 0 or x == W - 1 or y == H - 1
            row.append(1 if border or v < p else 0)  # 1 = wall
        grid.append(row)
    return grid

def step(grid, threshold=5):
    new = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            n = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if not (0 <= yy < H and 0 <= xx < W) or grid[yy][xx]:
                        n += 1
            new[y][x] = 1 if n >= threshold else 0
    return new

def regions(grid):
    """Return a list of floor regions, each a list of (y, x) cells, 4-connected."""
    seen = [[False] * W for _ in range(H)]
    out = []
    for y in range(H):
        for x in range(W):
            if grid[y][x] == 0 and not seen[y][x]:
                stack, cells = [(y, x)], []
                seen[y][x] = True
                while stack:
                    cy, cx = stack.pop()
                    cells.append((cy, cx))
                    for ny, nx in ((cy+1, cx), (cy-1, cx), (cy, cx+1), (cy, cx-1)):
                        if 0 <= ny < H and 0 <= nx < W and grid[ny][nx] == 0 and not seen[ny][nx]:
                            seen[ny][nx] = True
                            stack.append((ny, nx))
                out.append(cells)
    return out

def stats(grid):
    walls = sum(map(sum, grid))
    floor = W * H - walls
    regs = regions(grid)
    largest = max((len(r) for r in regs), default=0)
    return walls / (W * H), (largest / floor if floor else 0.0), len(regs)

def generate(p, seed, steps=5):
    g = noise(p, seed)
    for _ in range(steps):
        g = step(g)
    return g

def show(grid):
    print("\n".join("".join("#" if c else "." for c in row) for row in grid))

if __name__ == "__main__":
    g = generate(0.45, 1)
    show(g)
    print(stats(g))  # expect about (0.4586, 0.9380, 3)
```

Also use: the [week 12 lecture](../lectures/w12-emergent-behavior-from-simple-rules.md) dial table and the lab 11 spreadsheet skills for charts (or `matplotlib` if your environment has it).

## Steps

1. **Run it.** Run `python cave.py`. The last line must read about `(0.4586, 0.938, 3)`. If it does not, stop and find out why before going on.
2. **Reproduce the dial.** Write a `sweep(ps, seeds=range(1, 21))` function that returns the mean wall share, mean largest-region share and mean region count for each `p`. Reproduce the lecture's rows for `p = 0.40, 0.45, 0.50` to the decimals the table shows (one for the percentages, two for the mean region count).
3. **Steps matter less than you think.** For `p = 0.45`, report the three statistics after 0, 1, 2, 3, 5 and 8 steps (averaged over 20 seeds). Where does most of the change happen?
4. **Break the in-place rule.** Write `step_in_place(grid)` that updates the grid while reading it. Run the sweep for `p = 0.45`. Report how the numbers change and describe what the maps look like. Then delete the function.
5. **Repair pass.** Write `keep_largest(grid)` that fills every floor region except the largest with wall. Report the new mean wall share at `p = 0.45` and `p = 0.50`. What did the repair cost you?
6. **Tune to a target.** The level designer asks for maps with exactly one floor region (after your repair pass) and a wall share between 30% and 45%. Find a combination of `p` and step count that meets both on at least 18 of seeds 1 to 20. Report your settings and the pass count. Then the designer tightens the band to 40% to 45%. Show whether any setting still reaches 18 of 20. If none does, propose a reject-and-reroll rule (generate, test, discard failures) and report how many seeds it discards per accepted map.
7. **One rule change.** Change `threshold` to 6, and separately to 4, and rerun the sweep at `p = 0.45`. Explain each result in terms of the positive feedback in the majority rule.

## Deliverable

Your `cave.py` with the new functions, a chart of the sweep (wall share and largest-region share against `p`, from 0.30 to 0.60), and a tuning memo of at most 400 words. The memo must give your step 6 settings and pass count, explain why you chose a `p` on the flat or the steep part of the curve, and name one risk of your settings that a level designer should know about.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Reproduction | Step 1 and the three dial rows match the table's decimals | One row off with a found cause | Values not reproduced | 20% |
| Experiments (steps 3, 4, 7) | All three done; results explained with feedback and the two-grid rule | Done with thin explanation | Missing or unexplained | 25% |
| Repair pass | Correct function; cost measured at two values of `p` | Works, cost not measured | Missing or wrong | 15% |
| Tuning to target | Wide band met on 18 or more of 20 seeds; tight band tested honestly with a working reroll rule and its discard rate | Wide band met, tight band not analyzed | Not attempted | 25% |
| Chart and memo | Readable chart; memo numeric, names a real risk, within limit | Chart or memo weak | Missing | 15% |
