from core.pyxi import Sprite
from sprite.sprite_anim import SpriteAnim


class SpriteBase(Sprite):
    def __init__(self, width=800, height=600):
        Sprite.__init__(self, width, height)
        self.origin_x = 0
        self.origin_y = 0
        self.anim_sprites = []

    def update(self, *args):
        Sprite.update(self, *args)
        self.update_position()
        self.update_origin()

    def update_position(self):
        pass

    def update_origin(self):
        self.x -= self.rect.width * self.origin_x
        self.y -= self.rect.height * self.origin_y

    def show(self):
        pass

    def hide(self):
        pass

    def load_spritesheet(self, filename):
        self._spritesheet = self.load_image(filename)

    def load_window_image(self, filename):
        self._window_image = self.load_image(filename)

    def start_anim(self, anim_id, character, delay=0):
        sprite = SpriteAnim(self._width, self._height, anim_id, delay)
        sprite.setup(character)
        self.anim_sprites.append(sprite)
        self.add_sprite(sprite)

    def is_anim_busy(self):
        return any([anim.is_busy() for anim in self.anim_sprites])
