import game_objects as g
from screen.screen_base import ScreenBase


class ScreenStatus(ScreenBase):
    def __init__(self):
        ScreenBase.__init__(self, 256, 32)
        self.nextup = None
        self.exp = g.GAME_PLAYER.exp
        self.next_up = g.GAME_PLAYER.next_up()
        self.attack = 0
        self.hp = 0
        self.magic = 0
        self.wait_count = 0
        self.show()
        self.refresh()

    def set_nextup(self, nextup):
        self._nextup = nextup

    def update(self):
        self.refresh()
        ScreenBase.update(self)
        if self.exp >= self.next_up and not self._nextup._active:
            self._nextup.open()
            self.refresh()
        self.hide_frame()

    def update_position(self):
        pass

    def draw_screen(self):
        self.draw_attack()
        self.draw_life()
        self.draw_magic()
        self.draw_exp()

    def draw_exp(self):
        self.draw_text('Next', 204, 10, 8 * 4, 8, False, False)
        label = '{:04d}'.format(self.exp) + '/' + '{:04d}'.format(self.next_up)
        self.draw_text(label, 172, 21, 8 * 4, 8, False, False)

    def draw_attack(self):
        x = 8
        self._main_sprite.image.blit(self._screen_skin, (x, 24), (0, 24, 8, 8))
        self.draw_text(str(g.GAME_PLAYER.attack + 1), x + 8 + 1, 21, 8 * 4, 8, False, False)

    def draw_life(self):
        x = 256 / 2 - 16
        self.draw_text('Life-' + str(g.GAME_PLAYER.life + 1), x - 8, 10, 8 * 4, 8, False, False)
        self._main_sprite.image.draw_rect(x - 8, 22, 8, 9, (35, 59, 239))
        fill_width = max((8 * 4) * (g.GAME_PLAYER.hp / 64), 0)
        self._main_sprite.image.draw_rect(x, 23, fill_width, 7, (216, 40, 0, 255))
        self._main_sprite.image.blit(self._screen_skin, (x - 8, 22), (16, 24, 8, 8))
        self.draw_meter(x)

    def draw_magic(self):
        self.draw_text('Magic-' + str(g.GAME_PLAYER.magic + 1), 40 - 8, 10, 8 * 4, 8, False, False)
        self._main_sprite.image.draw_rect(32, 22, 8, 9, (35, 59, 239))
        self._main_sprite.image.blit(self._screen_skin, (32, 22), (8, 24, 8, 8))
        fill_width = max((8 * 4) * (g.GAME_PLAYER.mp / 64), 0)
        self._main_sprite.image.draw_rect(40, 22, fill_width, 8, (255, 255, 255, 255))
        self.draw_meter(40, (35, 59, 239, 255))

    def draw_meter(self, x, color=(255, 255, 255, 255)):
        for i in range(4):
            self.draw_block(x + 8 * i, 22, 8, 8, color)

    def draw_block(self, x, y, w, h, color):
        image = self._main_sprite.image
        image.draw_line((x, y), (x + w, y), color)
        image.draw_line((x + w, y), (x + w, y + h), color)
        image.draw_line((x + w, y + h), (x, y + h), color)
        image.draw_line((x, y + h), (x, y), color)

    def need_refresh(self):
        return self.hp != g.GAME_PLAYER.hp or self.magic != g.GAME_PLAYER.magic or \
               self.attack != g.GAME_PLAYER.attack or self.exp != g.GAME_PLAYER.exp or \
               self.next_up != g.GAME_PLAYER.next_up()

    def update_status(self):
        self.hp = g.GAME_PLAYER.hp
        self.magic = g.GAME_PLAYER.magic
        self.attack = g.GAME_PLAYER.attack
        self.next_up = g.GAME_PLAYER.next_up()
        if g.GAME_PLAYER.exp > self.exp:
            if g.GAME_PLAYER.exp - self.exp >= 10:
                self.wait_count += 1
                if self.wait_count == 5:
                    self.wait_count = 0
                    self.exp += 10
            else:
                self.exp += 1
        if g.GAME_PLAYER.exp < self.exp:
            self.exp = g.GAME_PLAYER.exp

    def refresh(self):
        # some issue with draw_text on mac catalina
        if (self.need_refresh()):
            self.clear_sprite()
            self.refresh_sprites()
            self.update_status()
            self.draw_screen()
