# CS203 · Lab 05: A navmesh by hand

**Week:** 5 ([Navigation meshes](../lectures/w05-navigation-meshes.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** in pairs for Parts A and B, individually for Part C

## Objective

Build the runtime half of a navigation mesh yourself: find which polygon a point is in, discover the portals between polygons, orient them for a walker, and pull a path tight with the funnel algorithm. Then use your code to measure how much the funnel saves over midpoint paths, and design a level where A* over polygons picks the wrong door. By the end you should be able to read a Detour-style path bug and say which stage caused it.

## Starter materials

- Python 3.10 or later, no packages. In this repository, `.venv/bin/python`.
- [`labs/lab05-starter/navmesh.py`](lab05-starter/navmesh.py). It contains `LEVEL`, the five-polygon level from lecture section 2 (with extra vertices where portals meet walls, so every portal is a full shared edge), the `cross()` and `length()` helpers, and finished `corridor()` (breadth-first search over polygons) and `plan()` functions that call yours. You write `point_in_convex()`, `find_poly()`, `find_portals()`, `oriented_portal()` and `funnel()`.
- [`labs/lab05-starter/check_lab05.py`](lab05-starter/check_lab05.py). Run `python check_lab05.py` from inside the starter folder. Five checks, all failing on the starter. The last one plans 200 random paths and verifies every one stays on the mesh and is no longer than the midpoint path.
- The interactive [`examples/w05-navmesh-funnel.html`](../examples/w05-navmesh-funnel.html) to compare your paths against.

## Steps

### Part A: the mesh (45 minutes)

1. Write `point_in_convex(poly, p)`: `True` when every edge `a → b` of the counter-clockwise polygon has `cross(a, b, p) ≥ 0`. Remember the closing edge from the last vertex back to the first. Then write `find_poly(mesh, p)`. Before running the checker, work out by hand which polygon contains (11, 8.5) and which contains (6, 5).
2. Write `find_portals(mesh)`. Record every directed edge `(a, b)` with the polygon that owns it. A portal exists wherever some other polygon owns `(b, a)`. Return both directions. The level has four portals, so eight entries.
3. Write `oriented_portal(mesh, portals, i, j)`. The edge `(a, b)` belongs to polygon `i` in counter-clockwise order, so the inside of `i` is on the left of `a → b`. Draw it for the portal from room A to the corridor and decide which of `a` and `b` is on the walker's left as they cross into `j`. Write that rule down in your report before you code it.

### Part B: the funnel (45 minutes)

4. Write `funnel(start, goal, portals)`. Work from the description in lecture section 2, not by copying the lecture code. When stuck, trace the default case on paper: apex, left and right after each portal. The step 4 check includes a reversed walk (goal to start) that catches swapped left and right.
5. Run the checker until all five checks pass. Then run `python navmesh.py` and confirm 17.78 m and 19.07 m.
6. Add a loop to a new script `measure.py` that plans 1,000 random start/goal pairs in different rooms (reuse the sampling boxes from `check_lab05.py`) and records the ratio `midpoint length / funnel length`. Report the mean, the maximum, and the start/goal pair that gave the maximum. Explain in two sentences why that pair is the worst case.

### Part C: the wrong door (at home)

7. Build a new mesh `TWO_DOORS` in `measure.py` for the situation in lecture section 3: start room, goal room, and a wall with a wide door and a narrow door. Your version must use convex polygons only and must satisfy `find_portals` (full shared edges). Replace `corridor()` for this part with a Dijkstra over polygons whose edge costs are distances between portal midpoints (start and goal count as the first and last points).
8. Show, with numbers, a start and goal for which the midpoint-cost corridor goes through the narrow door and the funnel path through it is longer than the funnel path through the wide door would be. Then change one thing about the mesh (not the algorithm) that makes the corridor choose the wide door, and report the new numbers.

## Deliverable

Your `navmesh.py` with `check_lab05.py` passing (paste its output), `measure.py`, and a PDF containing: the step 3 rule with a sketch, the step 6 statistics and explanation, and the step 7 and 8 mesh drawing with both sets of numbers and one paragraph on what a level designer should avoid.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Mesh queries (20%) | Steps 1-3 pass; the left/right rule is written and sketched before coding | Checks pass, rule stated without sketch | One of the three checks fails | Not attempted |
| Funnel (30%) | Step 4 and step 5 checks pass; code is readable and follows the apex/left/right description | Passes, hard to follow | Works on the default case only | Missing |
| Measurement (20%) | 1,000 pairs, mean and max ratio, worst pair identified and explained | Numbers present, explanation thin | Fewer samples or no worst case | Missing |
| Wrong-door study (20%) | Convex mesh, midpoint-cost Dijkstra, both routes measured, a mesh change that fixes it with new numbers | Bug shown, fix missing or unmeasured | Mesh built, bug not demonstrated | Missing |
| Designer advice (10%) | Concrete layout rule tied to the numbers | Generic advice | Advice unrelated to results | Missing |
