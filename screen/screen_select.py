import game_objects as g
from core.pyxi import Display
from screen.screen_command import ScreenSelectable


class ScreenSelect(ScreenSelectable):
    def __init__(self):
        width = self.window_width()
        height = self.window_height()
        ScreenSelectable.__init__(self, width, height)
        self.x = (Display.width_nes / 2) - 16
        self.y = 48
        self._magic_list = []

    def open(self):
        ScreenSelectable.open(self)
        self.select(g.GAME_PLAYER.magic_index + 1)

    def item_height(self):
        return 16

    def max_items(self):
        return len(self._magic_list)

    def window_width(self):
        return int(Display.width_nes / 2 - 16)

    def window_height(self):
        return int(Display.height_nes - 80)

    def update(self):
        ScreenSelectable.update(self)

    def make_item_list(self):
        self._magic_list = g.GAME_PLAYER.magic_list

    def process_cancel(self):
        self.close()
        g.GAME_PLAYER.magic_index = self._index - 1

    def draw_cursor_sprite(self):
        self._cursor_sprite.image.blit(self._screen_skin, (0, 0), (44, 4, 8, 8))

    def refresh(self):
        self.clear_sprite()
        self.refresh_sprites()
        self.make_item_list()
        self.draw_all_items()

    def draw_all_items(self):
        for index in range(self.max_items()):
            self.draw_item(index)

    def draw_item(self, index):
        rect = self.item_rect(index)
        item = self._magic_list[index]
        self.draw_text(item['name'], rect.x + 9, rect.y, rect.width, rect.height, False)
        self.draw_text(str(item['cost'][0]), rect.x + 78, rect.y, rect.width, rect.height, False)

    def set_cursor_pos(self, rect, align=1):
        padY = rect.height - 6 if align else 0
        self._cursor_sprite.x = self.x + rect.x
        self._cursor_sprite.y = self.y + rect.y + padY / 2
