from screen.screen_selectable import ScreenSelectable


class ScreenCommand(ScreenSelectable):
    def __init__(self, width, height):
        ScreenSelectable.__init__(self, width, height)
        self._list = []
        self.make_command_list()

    def update(self):
        ScreenSelectable.update(self)

    def max_items(self):
        return len(self._list)

    def clear_command_list(self):
        self._list = []

    def make_command_list(self):
        pass

    def add_command(self, name, symbol):
        self._list.append({"name": name, "symbol": symbol})

    def current_data(self):
        return self._list[self.index() - 1] if self.index() > 0 else None

    def current_symbol(self):
        return self.current_data()["symbol"] if self.current_data() else None

    def command_name(self, index):
        return self._list[index]["name"]

    def draw_item(self, index):
        rect = self.item_rect(index)
        self.draw_text(self.command_name(index), rect.x, rect.y, rect.width, rect.height)

    def call_ok_handler(self):
        symbol = self.current_symbol()
        self.call_handler(symbol)

    def draw_all_items(self):
        for index in range(self.max_items()):
            self.draw_item(index)

    def refresh(self):
        self.clear_sprite()
        if self._visible:
            self.refresh_sprites()
            self.draw_all_items()
