"""CS102 Lab 02 starter: a working god class.

Everything any entity might do lives in Entity, switched on and off by flags.
It works. Your job is to refactor it into GameObject + components without
changing behaviour. Keep test_behaviour.py green after every step.
"""


class Entity:
    def __init__(self, name, x=0.0, y=0.0,
                 renders=False, sprite=None,
                 collides=False, radius=0.0,
                 moves=False, vx=0.0, vy=0.0,
                 has_health=False, max_hp=0,
                 has_ai=False, chase_speed=0.0,
                 explodes=False, blast_radius=0.0, blast_damage=0, fuse=None):
        self.name = name
        self.x, self.y = x, y
        # render
        self.renders = renders
        self.sprite = sprite
        # collision
        self.collides = collides
        self.radius = radius
        # movement
        self.moves = moves
        self.vx, self.vy = vx, vy
        # health
        self.has_health = has_health
        self.max_hp = max_hp
        self.hp = max_hp if has_health else None
        # ai
        self.has_ai = has_ai
        self.chase_speed = chase_speed
        self.target = None
        # explosion
        self.explodes = explodes
        self.blast_radius = blast_radius
        self.blast_damage = blast_damage
        self.fuse = fuse
        self.exploded = False
        # bookkeeping
        self.world = None
        self.removed = False

    # ---- health -------------------------------------------------------
    def take_damage(self, amount):
        if not self.has_health or self.removed:
            return 0
        before = self.hp
        self.hp = max(0, self.hp - amount)
        taken = before - self.hp
        if taken:
            self.world.log(f"{self.name} takes {taken}")
        if self.hp == 0 and not self.explodes:
            self.world.log(f"{self.name} is destroyed")
            self.removed = True
        return taken

    # ---- per-frame update ----------------------------------------------
    def update(self, dt):
        if self.removed:
            return
        if self.has_ai and self.target is not None and not self.target.removed:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = (dx * dx + dy * dy) ** 0.5
            if dist > 0:
                self.vx = self.chase_speed * dx / dist
                self.vy = self.chase_speed * dy / dist
        if self.moves:
            self.x += self.vx * dt
            self.y += self.vy * dt
        if self.explodes and not self.exploded:
            if self.fuse is not None:
                self.fuse -= dt
                if self.fuse <= 1e-9:
                    self._explode()
            elif self.has_health and self.hp == 0:
                self._explode()

    def _explode(self):
        self.exploded = True
        self.removed = True
        self.world.log(f"{self.name} explodes")
        for other in self.world.entities:
            if other is self or other.removed:
                continue
            dx, dy = other.x - self.x, other.y - self.y
            if (dx * dx + dy * dy) ** 0.5 <= self.blast_radius:
                other.take_damage(self.blast_damage)

    # ---- drawing (text stand-in for a renderer) --------------------------
    def draw(self):
        if not self.renders or self.removed:
            return None
        return f"{self.sprite}@({self.x:.1f},{self.y:.1f})"

    def overlaps(self, other):
        if not (self.collides and other.collides):
            return False
        dx, dy = other.x - self.x, other.y - self.y
        return (dx * dx + dy * dy) ** 0.5 <= self.radius + other.radius


class World:
    def __init__(self):
        self.entities = []
        self.events = []

    def add(self, e):
        e.world = self
        self.entities.append(e)
        return e

    def log(self, msg):
        self.events.append(msg)

    def step(self, dt):
        for e in list(self.entities):
            e.update(dt)
