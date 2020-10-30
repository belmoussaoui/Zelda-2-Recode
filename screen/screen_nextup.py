import game_objects as g
from core.pyxi import Audio
from core.pyxi import Display
from core.pyxi import Rectangle
from screen.screen_command import ScreenCommand


class ScreenNextUp(ScreenCommand):
    def __init__(self):
        width = int(Display.width_nes / 2 - 16)
        height = int(Display.height_nes - 80)
        ScreenCommand.__init__(self, width, height)
        self.x = Display.width_nes / 2 - 16
        self.y = 48

    def set_cursor_pos(self, rect, align=1):
        self._cursor_sprite.x = (rect.x - 9) + self.x
        self._cursor_sprite.y = (rect.y + (15 if self._index - 1 != 0 else 3)) + self.y

    def update(self):
        ScreenCommand.update(self)

    def open(self):
        ScreenCommand.open(self)
        self.select(self.first_index())

    def item_rect(self, index):
        width = self.item_width()
        height = self.item_height()
        x = index % self.max_cols() * width + self.padding + 48
        y = (index // self.max_cols()) * height + self.padding
        if index == 0:
            y += 10
        if index == 1:
            y -= 15
        if index == 2:
            y -= 11
        if index == 3:
            y -= 9
        rect = Rectangle(x, y, width, height)
        return rect

    def cursor_up(self):
        if self._index > -1:
            Audio.play_sound_select()
            index = self.next_index_up()
            self.select(index)

    def first_index(self):
        for index in range(0, self.max_rows()):
            if self.item_is_enabled(index):
                return index + 1
        return self._index

    def next_index_up(self):
        for index in range(self._index - 2, -1, -1):
            if self.item_is_enabled(index):
                return index + 1
        return self._index

    def cursor_down(self):
        if self._index < self.max_rows():
            Audio.play_sound_select()
            index = self.next_index_down()
            self.select(index)

    def next_index_down(self):
        for index in range(self._index, self.max_rows()):
            if self.item_is_enabled(index):
                return index + 1
        return self._index

    def item_is_enabled(self, index):
        if index == 0:
            return not self.item_is_enabled(1) or not self.item_is_enabled(2) or not self.item_is_enabled(3)
        if index == 1:
            return g.GAME_PLAYER.exp >= g.GAME_PLAYER.next_exp_attack()
        if index == 2:
            return g.GAME_PLAYER.exp >= g.GAME_PLAYER.next_exp_magic()
        if index == 3:
            return g.GAME_PLAYER.exp >= g.GAME_PLAYER.next_exp_life()

    def draw_cursor_sprite(self):
        self._cursor_sprite.image.blit(self._screen_skin, (0, 0), (28, 20, 8, 8))

    def draw_item(self, index):
        if index == 0:
            self.draw_cancel(index)
        elif index == 1:
            self.draw_attack(index)
        elif index == 2:
            self.draw_magic(index)
        else:
            self.draw_life(index)

    def draw_cancel(self, index):
        rect = self.item_rect(index)
        self.draw_nextup(index, rect)
        self.draw_frame(38, 0, 74, 36)
        self.draw_text(self.command_name(index), rect.x, rect.y, rect.width, rect.height, False, False)

    def draw_nextup(self, index, rect):
        self.draw_frame(0, 0, 46, 36)
        self.draw_text('Next\n up', rect.x - 48, rect.y - 10, rect.width, rect.height, False, False)

    def draw_attack(self, index):
        rect = self.item_rect(index)
        self.draw_frame(0, 36, 120 - 8, 48)
        self.draw_text(self.command_name(index), rect.x, rect.y, rect.width, rect.height, False)
        self.draw_text(str(g.GAME_PLAYER.next_exp_attack()).rjust(4, ' '), rect.x - 48, rect.y + 10, rect.width,
                       rect.height, False)

    def draw_magic(self, index):
        rect = self.item_rect(index)
        self.draw_frame(0, 36 + 38, 120 - 8, 48)
        self.draw_text(self.command_name(index), rect.x, rect.y, rect.width, rect.height, False)
        self.draw_text(str(g.GAME_PLAYER.next_exp_magic()).rjust(4, ' '), rect.x - 48, rect.y + 10, rect.width,
                       rect.height, False)

    def draw_life(self, index):
        rect = self.item_rect(index)
        self.draw_frame(0, 36 + 38 * 2, 120 - 8, 48)
        self.draw_text(self.command_name(index), rect.x, rect.y, rect.width, rect.height, False)
        self.draw_text(str(g.GAME_PLAYER.next_exp_life()).rjust(4, ' '), rect.x - 48, rect.y + 10, rect.width,
                       rect.height, False)

    def make_command_list(self):
        self.add_command('cancel', 'cancel')
        self.add_command('attack', 'attack')
        self.add_command('magic', 'magic')
        self.add_command('life', 'life')
