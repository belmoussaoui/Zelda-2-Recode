import game_objects as g
from core.pyxi import Rectangle
from game.game_object import GameObject


class GameCharacter(GameObject):
    def __init__(self, object_id):
        GameObject.__init__(self, 0, 0, object_id)
        self._x = 0.
        self._y = 0.
        self.sx = 0.
        self.sy = 0.
        self.frame_count = 0
        self.direction = 1
        self.setup_box()

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

    @property
    def box(self):
        x = self.x - self.hurtbox.width / 2
        y = self.y - self.hurtbox.y
        w = self.hurtbox.width
        h = self.hurtbox.height
        return Rectangle(x, y, w, h)

    def center_x(self):
        return self.hitbox.width / 2

    def set_direction(self, d):
        self.direction = d

    def screen_x(self):
        return g.GAME_MAP.adjust_x(self.x) - self.hitbox.centerx

    def screen_y(self):
        return g.GAME_MAP.adjust_y(self.y) - self.hitbox.height - self.hitbox.y

    def _create_rect_for_collision_x(self):
        x = self._round_rect_x()
        y = self.y - self.hitbox.height
        w = self.hitbox.width
        h = self.hitbox.height
        x -= w / 2
        return Rectangle(x, y, w, h)

    def _create_rect_for_collision_y(self):
        # to fix when fall with pixel perfect to right
        x = round(self.x - self.center_x())
        y = self._round_rect_y()
        w = self.hitbox.width
        h = self.hitbox.height
        y -= h
        return Rectangle(x, y, w, h)

    def _round_rect_x(self):
        return round(self.x + self.sx + self.ceil_and_floor(self.sx))

    def _round_rect_y(self):
        return round(self.y + self.sy + self.ceil_and_floor(self.sy))

    # in Rectangle ?
    def ceil_and_floor(self, speed):
        # rectangle can't have float numbers
        # it's necessary to round with sx or sy
        return .5 * (1 if speed > 0 else -1)

    def update(self):
        self.update_move()
        self.update_frame()

    def update_move(self):
        self.execute_move_x()
        self.execute_move_y()

    def update_frame(self):
        if self.state == 'walk':
            self.frame_count += 1
        if self.frame_count >= 18:
            self.frame_count = 0

    def execute_move_x(self):
        if self.can_pass_x():
            self.x += self.sx

    def can_pass_x(self):
        if self.is_collided_with_map_x():
            return False
        return True

    def is_collided_with_bounds_x(self):
        rect = self._create_rect_for_collision_x()
        x = self.side_x_with_sx(rect)
        if not g.GAME_MAP.is_valid(x):
            x = self.round_x_with_bounds(x)
            self.on_collision_x(x)
            return True
        return False

    def side_x_with_sx(self, r):
        return r.left if self.sx < 0 else r.right if self.sx > 0 else r.centerx

    def round_x_with_bounds(self, x):
        return g.GAME_MAP.round_x_with_bounds(x)

    def is_collided_with_map_x(self):
        rect = self._create_rect_for_collision_x()
        if not g.GAME_MAP.is_passable(rect):
            x = self.round_x_with_map()
            self.on_collision_x(x)
            return True
        return False

    def round_x_with_map(self):
        return g.GAME_MAP.round_x_with_map(self.sx)

    def on_collision_x(self, x):
        if self.sx > 0:
            self.x = x - self.center_x()
        if self.sx < 0:
            self.x = x + self.center_x()
        self.sx = 0

    def execute_move_y(self):
        if self.can_pass_y():
            if not self.is_jumping():
                # self.stand_up()
                self.state = 'fall'
            self.y += self.sy

    def can_pass_y(self):
        if self.is_collided_with_map_y():
            return False
        return True

    def is_collided_with_map_y(self):
        rect = self._create_rect_for_collision_y()
        if not g.GAME_MAP.is_passable(rect):
            y = self.round_y_with_map()
            self.on_collision_y(y)
            return True
        return False

    def round_y_with_map(self):
        return g.GAME_MAP.round_y_with_map(self.sy)

    def on_collision_y(self, y):
        pass
