from sprite.sprite_base import SpriteBase


class SpriteItem(SpriteBase):
    def __init__(self, item):
        SpriteBase.__init__(self, 16, 16)
        self.item = item
        self._create_image()
        self._direction = 1
        self.origin_x = .5
        self.origin_y = 0

    def _create_image(self):
        self.load_spritesheet('tilesets/parapalace-objects.png')
        if self.item.item_id == 3:
            self.set_frame(0, 16, 16, 16)
        if self.item.item_id == 4:
            self.set_frame(48, 16, 16, 16)

    def set_character(self, character):
        self.character = character

    def update(self):
        SpriteBase.update(self)
        self.update_frame()
        if not self.item.active:
            self.kill()

    def update_position(self):
        self.x = self.item.screen_x()
        self.y = self.item.screen_y()

    def update_frame(self):
        self.update_frame_state()

    def update_frame_state(self):
        pass
