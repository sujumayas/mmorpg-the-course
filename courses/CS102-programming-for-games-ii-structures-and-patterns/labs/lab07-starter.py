"""CS102 Lab 07 starter: a scene graph and a skill tree.

Run it with:  .venv/bin/python courses/CS102-programming-for-games-ii-structures-and-patterns/labs/lab07-starter.py

Every function marked TODO raises NotImplementedError. The tests at the bottom
print PASS or FAIL for each part, so you can work through the file top to bottom.
Do not change the tests. You may add helper functions.
"""
import math

# ---------------------------------------------------------------------------
# Part A. Scene graph (2D, translation + rotation, no scale)
# ---------------------------------------------------------------------------


class Node:
    """One node in a scene graph. Position and angle are LOCAL, relative to the parent."""

    def __init__(self, name, x=0.0, y=0.0, angle=0.0):
        self.name = name
        self.x = x              # local position, units
        self.y = y
        self.angle = angle      # local rotation, degrees, counter-clockwise
        self.parent = None
        self.children = []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return child

    def world(self):
        """Return (world_x, world_y, world_angle) for this node.

        Model from the lecture:
            world_angle = parent_world_angle + angle
            world_pos   = parent_world_pos + R(parent_world_angle) * (x, y)
        where R(t) * (x, y) = (x cos t - y sin t, x sin t + y cos t).
        A node with no parent has world = local.
        """
        raise NotImplementedError("A1: world transform")


def preorder(node):
    """Return the list of node names in pre-order (node, then each child subtree in order)."""
    raise NotImplementedError("A2: pre-order walk")


def postorder(node):
    """Return the list of node names in post-order (each child subtree in order, then the node)."""
    raise NotImplementedError("A3: post-order walk")


def subtree_size(node):
    """Number of nodes in the subtree rooted at node, including node itself."""
    raise NotImplementedError("A4: subtree size")


# ---------------------------------------------------------------------------
# Part B. Skill tree (every skill has at most one prerequisite)
# ---------------------------------------------------------------------------


class Skill:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost        # skill points to learn it
        self.learned = False
        self.parent = None      # the prerequisite, or None for a root skill
        self.children = []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return child


def can_learn(skill):
    """True if the skill is not yet learned and its prerequisite (if any) is learned."""
    raise NotImplementedError("B1: can_learn")


def path_cost(skill):
    """Total points to learn this skill from nothing: its cost plus every ancestor's cost."""
    raise NotImplementedError("B2: path_cost")


def refund(skill):
    """Unlearn this skill and every learned skill below it. Return the points refunded.

    Hint: this is a post-order job. Children first, then the node.
    """
    raise NotImplementedError("B3: refund")


# ---------------------------------------------------------------------------
# Tests. Do not edit below this line.
# ---------------------------------------------------------------------------


def build_tank():
    tank = Node("Tank", 100, 100, 0)
    turret = tank.add_child(Node("Turret", 10, 0, 0))
    barrel = turret.add_child(Node("Barrel", 30, 0, 0))
    barrel.add_child(Node("Muzzle", 20, 0, 0))
    tank.add_child(Node("TrackL", 0, 12, 0))
    tank.add_child(Node("TrackR", 0, -12, 0))
    return tank


def find(node, name):
    if node.name == name:
        return node
    for c in node.children:
        hit = find(c, name)
        if hit:
            return hit
    return None


def close(a, b, tol=0.05):
    return all(abs(p - q) <= tol for p, q in zip(a, b))


def build_frost():
    frost = Skill("Frost Bolt", 1)
    lance = frost.add_child(Skill("Ice Lance", 1))
    lance.add_child(Skill("Shatter", 2))
    nova = frost.add_child(Skill("Frost Nova", 1))
    nova.add_child(Skill("Deep Freeze", 3))
    return frost


def test_world():
    tank = build_tank()
    turret, muzzle = find(tank, "Turret"), find(tank, "Muzzle")
    assert close(muzzle.world(), (160, 100, 0)), muzzle.world()
    turret.angle = 30
    assert close(muzzle.world(), (153.3, 125.0, 30)), muzzle.world()
    turret.angle = 0
    tank.angle = 90
    assert close(muzzle.world(), (100, 160, 90)), muzzle.world()
    turret.angle = 30
    assert close(muzzle.world(), (75.0, 153.3, 120)), muzzle.world()


def test_walks():
    tank = build_tank()
    assert preorder(tank) == ["Tank", "Turret", "Barrel", "Muzzle", "TrackL", "TrackR"]
    assert postorder(tank) == ["Muzzle", "Barrel", "Turret", "TrackL", "TrackR", "Tank"]
    assert subtree_size(tank) == 6
    assert subtree_size(find(tank, "Turret")) == 3


def test_skills():
    frost = build_frost()
    shatter = frost.children[0].children[0]
    deep = frost.children[1].children[0]
    assert can_learn(frost) and not can_learn(shatter)
    assert path_cost(shatter) == 4 and path_cost(deep) == 5
    for s in (frost, frost.children[0], shatter, frost.children[1]):
        s.learned = True
    assert can_learn(deep)
    assert refund(frost.children[0]) == 3          # Ice Lance 1 + Shatter 2
    assert not shatter.learned and frost.learned
    assert refund(frost) == 2                       # Frost Bolt 1 + Frost Nova 1


if __name__ == "__main__":
    for test in (test_world, test_walks, test_skills):
        try:
            test()
            print(f"PASS  {test.__name__}")
        except NotImplementedError as e:
            print(f"TODO  {test.__name__}: {e}")
        except AssertionError as e:
            print(f"FAIL  {test.__name__}: got {e}")
