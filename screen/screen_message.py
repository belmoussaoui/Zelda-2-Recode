from screen.screen_base import ScreenBase


class ScreenMessage(ScreenBase):
    def __init__(self):
        ScreenBase.__init__(self, 256-128, 56)
        self.x = 64
        self.y = (240-64)/2 + 32
        self.draw_screen()
        self.close()
        self.clear_sprite()
        self.hide_frame()

    def draw_screen(self):
        self.clear_sprite()
        self.hide_frame()
        self.draw_text('You saved\nHyrule and\nyou are a\nreal hero', 0, 8, 256 - 128, 8)

    def update(self):
        ScreenBase.update(self)

