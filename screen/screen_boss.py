from core.pyxi import Display
from screen.screen_base import ScreenBase


class ScreenBoss(ScreenBase):
    def __init__(self):
        width = self.window_width()
        height = self.window_height()
        ScreenBase.__init__(self, width, height)
        self.x = 16
        self.y = 48
        self._boss = None
        self.close()
        self.clear_sprite()
        self.hide_frame()

    def setup(self, boss):
        self._boss = boss
        self.open()
        self.refresh()

    def window_width(self):
        return int(Display.width_nes / 2 - 16)

    def window_height(self):
        return int(Display.height_nes - 80)

    def refresh(self):
        self.clear_sprite()
        self.hide_frame()
        if self._boss and self._boss.is_alive():
            self.refresh_sprites()
            self.draw_screen()
        else:
            self._boss = None
            self.close()


    def draw_screen(self):
        self._main_sprite.image.clear()
        self.draw_life()

    def draw_life(self):
        x = 0
        fill_width = max((8 * 4) * (64 / 64), 0)
        for i in range(8):
            self._main_sprite.image.draw_rect(x, 23 + i * 7, 8, 5, (255, 255, 255, 255))
        for i in range(7, round(7-self._boss.hp/4), -1):
            self._main_sprite.image.draw_rect(x, 23 + i * 7, 8, 5, (216, 40, 0, 255))
