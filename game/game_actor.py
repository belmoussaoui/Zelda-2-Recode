import game_objects as g
from core.pyxi import Rectangle
from game.game_character import GameCharacter


class GameActor(GameCharacter):
    def __init__(self):
        GameCharacter.__init__(self, 0)
        self.state = 'idle'
        self.walk_speed = 1.6
        self.fall_speed = 4.0
        self.walk_force = .10
        self.jump_force = 4.5
        self.jump_duration = 23
        self.is_on_ground = False
        self.setup_count()

    def setup_count(self):
        self.jump_count = 0
        self.ivcb_count = 0

    def clamp_speed(self):
        self.sx = self.clamp_speed_x()
        self.sy = self.clamp_speed_y()

    def clamp_speed_x(self):
        return max(min(self.sx, self.walk_speed), -self.walk_speed)

    def clamp_speed_y(self):
        return min(self.sy, self.fall_speed) if self.sy > 0 else self.sy

    def on_ground(self):
        self.is_on_ground = True
        if self.state == 'fall':
            self.state = 'walk'

    def is_jumping(self):
        return self.jump_count > 0

    def update(self):
        self.sy += g.GAME_MAP.gravity
        self.update_state()
        GameCharacter.update(self)

    def update_state(self):
        switcher = {
            'idle': self.state_standing,
            'walk': self.state_walking,
            'jump': self.state_jumping,
            'fall': self.state_falling
        }
        switcher.get(self.state)()
        self.clamp_speed()

    def state_standing(self):
        self.state_walking()

    def state_walking(self):
        pass

    def state_jumping(self):
        self.update_jump()

    def state_falling(self):
        pass

    def sx_with_direction(self, d):
        return d * self.walk_force

    def stand_up(self):
        pass

    def update_jump(self):
        self.jump_count -= 1
        self.sy = -self.jump_count / self.jump_duration * self.jump_force
        if self.jump_count == 0:
            self.stand_up()
            self.y += 5
            self.state = 'fall'

    def on_collision_x(self, x):
        if self.sx > 0:
            self.x = x - self.center_x()
        if self.sx < 0:
            self.x = x + self.center_x()
        self.sx = 0

    def on_collision_y(self, y):
        if self.sy > 0:
            self.on_ground()
            self.y = y
        if self.sy < 0:
            if self.state != 'hurt':
                self.stand_up()
                self.y = y + self.hitbox.height
                self.state = 'fall'
        self.sy = 0

    def back_to_idle(self):
        force = self.walk_force / 2
        if self.sx > 0:
            self.sx = max(0, self.sx - force)
        elif self.sx < 0:
            self.sx = min(0, self.sx + force)
        else:
            if self.is_on_ground:
                self.state = 'idle'

    def has_shield(self):
        return hasattr(self, 'shield')

    def hit_shield(self, box):
        x = self.x
        y = self.top
        s = self.shield
        rect = Rectangle(x + s.x, y + s.y, s.width, s.height)
        return rect.colliderect(box)
