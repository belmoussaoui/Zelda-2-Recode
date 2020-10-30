import game_objects as g
from core.pyxi import Rectangle


class GameObject:
    SWITCH = {}

    def __init__(self, x, y, object_id):
        self.x = x
        self.y = y
        self.id = object_id
        self.setup_box()
        self.direction = 0

    def key(self):
        return str(g.GAME_MAP.map_id) + str(self.id)

    def activate_switch(self):
        GameObject.SWITCH[self.key()] = True

    def deactivate_switch(self):
        GameObject.SWITCH[self.key()] = False

    def is_switch(self):
        return GameObject.SWITCH.get(self.key(), False)

    def setup_box(self):
        self.hitbox = Rectangle(0, 0, 0, 0)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def left(self):
        return self.x - self.center_x()

    @property
    def right(self):
        return self.x + self.center_x()

    @property
    def bottom(self):
        return self.y

    @property
    def top(self):
        return self.y - self.hitbox.height

    @property
    def width(self):
        return self.hitbox.width

    @property
    def height(self):
        return self.hitbox.height

    @property
    def rect(self):
        x = self.left
        y = self.top
        w = self.width
        h = self.height
        return Rectangle(x, y, w, h)

    def center_x(self):
        return self.hitbox.width / 2

    def screen_x(self):
        return g.GAME_MAP.adjust_x(self.x) - self.hitbox.centerx

    def screen_y(self):
        return g.GAME_MAP.adjust_y(self.y) - self.hitbox.height - self.hitbox.y

    def update(self):
        pass
