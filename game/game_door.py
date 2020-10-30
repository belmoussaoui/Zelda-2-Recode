import game_objects as g
from core.pyxi import Audio
from game.game_object import GameObject
from sprite.sprite_base import SpriteBase


class GameDoor(GameObject):
    def __init__(self, x, y, object_id):
        GameObject.__init__(self, x + 8, y, object_id)
        self.hitbox.x = -12
        self.hitbox.height = 48
        self.hitbox.width = 8
        self.active = True
        self.opening = False
        self.openness = 0
        if self.is_switch():
            self.openness = 16
            self.opening = True

    def update(self):
        if self.opening:
            self.openness += 1
            if self.is_open():
                self.opening = False
                self.hitbox.height = 0
                self.activate_switch()

    def on_touch(self):
        if g.GAME_PLAYER.keys > 0 and not self.opening:
            g.GAME_PLAYER.keys -= 1
            self.open()

    def open(self):
        Audio.play_sound_open()
        self.opening = True

    def is_open(self):
        return self.openness >= 16


class SpriteDoor(SpriteBase):
    def __init__(self, door):
        SpriteBase.__init__(self, 24, 48)
        self.door = door
        self._create_image()
        self.origin_x = 0.5
        self.origin_y = 0

    def _create_image(self):
        self.load_spritesheet('system/items.png')
        self.set_frame(183, 42, 8, 48)

    def update_position(self):
        self.x = self.door.screen_x()
        self.y = self.door.screen_y()

    def update(self):
        SpriteBase.update(self)
        self.update_collide()
        self.update_opening()

    def update_collide(self):
        rect = self.door.hitbox
        x = self.width / 2 + rect.x
        y = rect.y
        w = rect.width - 1
        h = rect.height - 1
        self.image.draw_collide(x, y, w, h, (0, 0, 0))

    def update_opening(self):
        i = self.door.openness
        self.set_frame(183 + i * 9, 42, 8, 48)
        if self.door.is_open():
            self.start_anim(2, self.door)
            self.anim_sprites[0].origin_x = 0.5
            self.anim_sprites[0].origin_y = 0.5
            self.image.set_alpha(0)
            self.kill()
