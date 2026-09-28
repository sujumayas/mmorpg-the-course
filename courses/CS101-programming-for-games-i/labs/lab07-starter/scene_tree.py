"""CS101 Lab 07: a scene tree you can test.

A tiny model of how Godot calls your scripts. Standard-library Python 3.10+.

Part A (done for you): the Node class and the two concrete node types used in
the lecture, a Mover (like the Enemy) and a Follower (like the HealthBar).
Part B (you write): traversal orders, a frame runner that honours
process_priority, and lag counting.
Part C (you run): the experiments from the lab sheet.
"""

# ---------------------------------------------------------------- Part A ---

class Node:
    def __init__(self, name, children=(), priority=0):
        self.name = name
        self.children = list(children)
        self.priority = priority     # like Godot's process_priority: lower runs first
        self.x = 0.0
        self.log = None              # set by run_frames so nodes can record calls

    def add(self, child):
        self.children.append(child)
        return child

    def process(self, dt):
        pass

    def __repr__(self):
        return f"Node({self.name!r})"


class Mover(Node):
    """Moves right at `speed` pixels per second."""
    def __init__(self, name, speed, children=(), priority=0):
        super().__init__(name, children, priority)
        self.speed = speed

    def process(self, dt):
        self.x += self.speed * dt


class Follower(Node):
    """Copies the x of `target` every frame, like the lecture's health bar."""
    def __init__(self, name, target, children=(), priority=0):
        super().__init__(name, children, priority)
        self.target = target

    def process(self, dt):
        self.x = self.target.x


# ---------------------------------------------------------------- Part B ---

def pre_order(root):
    """Return a list of nodes: each node, then its children in order, recursively.
    This is Godot's 'tree order' (used by _enter_tree and _process)."""
    raise NotImplementedError


def post_order(root):
    """Return a list of nodes: all children (recursively) first, then the node.
    This is the order of _ready."""
    raise NotImplementedError


def process_order(root):
    """Return the order in which _process runs: sorted by `priority` (lower
    first); nodes with equal priority keep their pre-order position.
    Hint: Python's sorted() is stable."""
    raise NotImplementedError


def run_frames(root, frames, fps):
    """Call process(dt) on every node in process_order(root), `frames` times,
    with dt = 1 / fps. Return nothing."""
    raise NotImplementedError


def lag_frames(root, follower):
    """Count the links in the chain follower -> target -> target ... -> (a node
    that is not a Follower) where the copying node runs BEFORE the node it
    copies, according to process_order(root). Return that count."""
    raise NotImplementedError


def predicted_gap(lag, speed, fps):
    """Pixels a follower trails a mover by: lag x speed / fps."""
    raise NotImplementedError


# ---------------------------------------------------------------- Part C ---

def build_lecture_tree():
    """Main > Player > (Sprite, HealthBar), Main > Enemy. Section 4's tree."""
    main = Node("Main")
    player = main.add(Node("Player"))
    player.add(Node("Sprite"))
    player.add(Node("HealthBar"))
    main.add(Node("Enemy"))
    return main


if __name__ == "__main__":
    tree = build_lecture_tree()
    print("enter/process:", [n.name for n in pre_order(tree)])
    print("ready:        ", [n.name for n in post_order(tree)])

    for order in (["bar", "enemy"], ["enemy", "bar"]):
        enemy = Mover("Enemy", speed=300)
        bar = Follower("HealthBar", enemy)
        main = Node("Main", [bar, enemy] if order[0] == "bar" else [enemy, bar])
        run_frames(main, frames=3, fps=60)
        print(order, "gap after 3 frames:", round(enemy.x - bar.x, 2),
              "predicted:", predicted_gap(lag_frames(main, bar), 300, 60))
