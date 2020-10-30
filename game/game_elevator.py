from core.input import Input
from core.pyxi import Audio
from core.pyxi import Rectangle
from game.game_object import GameObject
from sprite.sprite_base import SpriteBase


class GameElevator(GameObject):
    position_y = 12

    def __init__(self, x, y, object_id):
        x = x + 16
        y = GameElevator.position_y * 16 + 1
        GameObject.__init__(self, x, y, object_id)
        self.hitbox = Rectangle(0, 0, 0, 0)
        self.hitbox.x = -12
        self.hitbox.width = 24
        self.hitbox.y = 40
        self.hitbox.height = 1
        self.sound_count = 0

    def update(self):
        self.sound_count -= 1
        self.update_move()

    def update_move(self):
        d = self.get_input_direction()
        sy = g.GAME_PLAYER.sy
        g.GAME_PLAYER.sy = d * 1.6
        if g.GAME_PLAYER.ground_type == 'elevator':
            if self.can_pass_y(d) and d != 0:
                if self.sound_count < 0:
                    self.sound_count = 10
                    Audio.play_sound_elevator()
                g.GAME_PLAYER.y += d * 1.6
                self._y += d * 1.6
        g.GAME_PLAYER.sy = sy

    def can_pass_y(self, d):
        if self.is_collided_with_map_y(d):
            return False
        return True

    def is_collided_with_map_y(self, d):
        rect = g.GAME_PLAYER._create_rect_for_collision_y()
        if not g.GAME_MAP.is_passable(rect):
            # y = self.round_y_with_map()
            return True
        return False

    def get_input_direction(self):
        return Input.dirY()


import game_objects as g


class SpriteElevator(SpriteBase):
    def __init__(self, elevator):
        SpriteBase.__init__(self, 24, 48)
        self.elevator = elevator
        self._create_image()
        self.origin_x = .5
        self.origin_y = 0

    def _create_image(self):
        self.load_spritesheet('tilesets/parapapalace-tiles.png')
        self.set_frame(135, 12, 24, 48)

    def update_position(self):
        self.x = self.elevator.screen_x()
        self.y = self.elevator.screen_y()

    def update(self):
        SpriteBase.update(self)
        self.update_collide()

    def update_collide(self):
        rect = self.elevator.hitbox
        x = self.width / 2 + rect.x
        y = rect.y
        w = rect.width - 1
        h = rect.height - 1
        self.image.draw_collide(x, y, w, h, (0, 0, 0))
