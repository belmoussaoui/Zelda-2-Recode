import game_objects as g
from sprite.sprite_base import SpriteBase


class SpriteCharacter(SpriteBase):
    def __init__(self, width, height, character):
        SpriteBase.__init__(self, width, height)
        self._create_image()
        self.character = character
        self._direction = 1
        self.origin_x = .5
        self.origin_y = 0
        self.state = ''  # for debug

    def _create_image(self):
        pass

    def set_character(self, character):
        self.character = character

    def update(self):
        SpriteBase.update(self)
        self.update_frame()
        self.update_debug()

    def update_position(self):
        self.x = self.character.screen_x()
        self.y = self.character.screen_y()

    def update_frame(self):
        self.update_frame_state()

    def update_frame_state(self):
        pass

    def update_debug(self):
        if g.GAME_SYSTEM.is_debugging():
            self.image.draw_text(self.character.state, 0, 0, self.width, self.height, True)
