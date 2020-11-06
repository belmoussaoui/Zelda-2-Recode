from screen.screen_base import ScreenBase


class ScreenCredits(ScreenBase):
    def __init__(self):
        ScreenBase.__init__(self, 256-32, 128)
        self.x = 16
        self.y = (240-128)/2
        self.draw_screen()

    def draw_screen(self):
        self._main_sprite.image._textColor = (255, 0, 0)
        self.draw_text('Programming', 0, 0, 256-32, 8)
        self._main_sprite.image._textColor = (255, 255, 255)
        self.draw_text('@arleq1n', 0, 16, 256 - 32, 8)
        self._main_sprite.image._textColor = (255, 0, 0)
        self.draw_text('Sprites ripped', 0, 40, 256 - 32, 8)
        self._main_sprite.image._textColor = (255, 255, 255)
        self.draw_text('Mister Mike', 0, 40+16, 256 - 32, 8)
        self.draw_text('GaryCXJK', 0, 40 + 32, 256 - 32, 8)
        self.draw_text('LoZ741', 0, 40 + 48, 256 - 32, 8)
        self.draw_text('BruceJuice', 0, 40 + 48 + 16, 256 - 32, 8)
        self.hide_frame()

    def update(self):
        ScreenBase.update(self)
        self.hide_frame()


