from core.pyxi import Sprite
from core.pyxi import Stage


class SpritesetBase(Stage):
    def __init__(self):
        Stage.__init__(self)
        self.create_lower_layer()
        self.create_upper_layer()

    def create_lower_layer(self):
        self.create_black_sprite()

    def create_black_sprite(self):
        self._black_sprite = Sprite(800, 600)
        self._black_sprite.image.fill((0, 0, 0))
        self.add(self._black_sprite)

    def create_upper_layer(self):
        self.create_pictures()

    def create_pictures(self):
        pass

    def update(self):
        Stage.update(self)
        self.update_position()

    def update_position(self):
        pass
