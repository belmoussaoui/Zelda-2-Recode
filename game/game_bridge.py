from game.game_object import GameObject
from sprite.sprite_base import SpriteBase


class GameBridge(GameObject):
    def __init__(self, x, y, object_id):
        GameObject.__init__(self, x + 8, y, object_id)
        self.hitbox.x = 0
        self.hitbox.height = 16
        self.hitbox.width = 16
        self.wait_count = 30
        self.activate = False

    def on_touch(self):
        self.activate = True

    def update(self):
        GameObject.update(self)
        if self.activate:
            self.wait_count -= 1
            if self.wait_count == 0:
                self.setup_box()


class SpriteBridge(SpriteBase):
    def __init__(self, bridge):
        SpriteBase.__init__(self, 16, 16)
        self.bridge = bridge
        self._create_image()
        self.origin_x = 0
        self.origin_y = 0

    def _create_image(self):
        self.load_spritesheet('tilesets/parapapalace-tiles.png')
        self.set_frame(18, 90, 16, 16)

    def update_position(self):
        self.x = self.bridge.screen_x()
        self.y = self.bridge.screen_y()

    def update(self):
        SpriteBase.update(self)
        self.update_collide()
        self.update_destruction()
        if self.bridge.wait_count == 0:
            self.kill()

    def update_collide(self):
        rect = self.bridge.hitbox
        x = self.width / 2 + rect.x
        y = rect.y
        w = rect.width
        h = rect.height
        self.image.draw_collide(x, y, w, h, (0, 0, 0))

    def update_destruction(self):
        if self.bridge.wait_count == 20:
            self.set_frame(35, 90, 16, 16)
        if self.bridge.wait_count == 10:
            self.set_frame(51, 90, 16, 16)
