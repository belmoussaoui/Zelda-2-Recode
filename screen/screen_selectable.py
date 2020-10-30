import math

from core.pyxi import Audio
from core.input import Input
from core.pyxi import Rectangle
from screen.screen_base import ScreenBase


class ScreenSelectable(ScreenBase):
    def __init__(self, width, height):
        ScreenBase.__init__(self, width, height)
        self._index = 0
        self._handlers = {}

    def update(self):
        ScreenBase.update(self)
        if (self._active):
            self.process_input()
            # self.process_touch()

    def index(self):
        return self._index

    def open(self):
        ScreenBase.open(self)
        Audio.play_sound_screen_open()
        self.select(1)

    def select(self, index):
        self._index = index
        self.select_cursor()

    def select_cursor(self):
        rect = self.item_rect(self._index - 1)
        self.set_cursor_pos(rect)

    def deselect(self):
        self._index = 0

    def is_active(self):
        return self._active

    @staticmethod
    def max_cols():
        return 1

    def max_rows(self):
        return max(math.ceil(self.max_items() / self.max_cols()), 1)

    def max_items(self):
        return 0

    def item_width(self):
        return (self._real_width - self.padding * 2) / self.max_cols()

    def item_height(self):
        return (self._real_height - self.padding * 2) / self.max_rows()

    def item_rect(self, index):
        width = self.item_width()
        height = self.item_height()
        x = index % self.max_cols() * width + self.padding
        y = (index // self.max_cols()) * height + self.padding
        rect = Rectangle(x, y, width, height)
        return rect

    def process_input(self):
        self.update_ok()
        self.update_cancel()
        self.update_cursor()

    def update_ok(self):
        if Input.is_key_triggered('return'):
            self.process_ok()

    def update_cancel(self):
        if Input.is_key_triggered('escape'):
            self.process_cancel()

    def process_touch(self):
        self.on_touch()
        if Input.is_triggered():
            self.process_ok()

    def on_touch(self):
        index = self.touch_item_index()
        if index > 0:
            self.select(index)

    def touch_item_index(self):
        if self.is_inside_frame():
            for index in range(self.max_items()):
                if self.is_inside_rect(index):
                    return index + 1
        return 0

    def is_inside_frame(self):
        x, y = Input.get_pos()
        x = self.canvas_to_local_x(x)
        y = self.canvas_to_local_y(y)
        width = self.width - self.padding
        height = self.height - self.padding
        return 0 <= x <= width and 0 <= y <= height

    def is_inside_rect(self, index):
        x, y = Input.get_pos()
        x = self.canvas_to_local_x(x)
        y = self.canvas_to_local_y(y)
        rect = self.item_rect(index)
        return rect.x <= x <= rect.x + rect.width and rect.y <= y <= rect.y + rect.height

    def update_cursor(self):
        if (Input.is_key_triggered('down')):
            self.cursor_down()
        if (Input.is_key_triggered('up')):
            self.cursor_up()

    def cursor_down(self):
        if self._index < self.max_rows():
            Audio.play_sound_select()
            self.select(self._index + 1)

    def cursor_up(self):
        if self._index - 1 > 0:
            Audio.play_sound_select()
            self.select(self._index - 1)

    def process_ok(self):
        self.call_ok_handler()

    def process_cancel(self):
        pass

    def set_handler(self, symbol, method):
        self._handlers[symbol] = method

    def call_handler(self, symbol):
        self._handlers[symbol]()

    def call_ok_handler(self):
        self.call_handler('ok')

    def call_cancel_handler(self):
        self.call_handler('cancel')

    def set_cursor_pos(self, rect, align=1):
        padY = rect.height - 16 if align else 0
        self._cursor_sprite.x = self.x + (rect.x)
        self._cursor_sprite.y = self.y + (rect.y + padY / 2)
