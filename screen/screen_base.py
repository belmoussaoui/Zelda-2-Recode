from core.pyxi import Display
from core.pyxi import Screen


class ScreenBase(Screen):
    def __init__(self, width, height):
        Screen.__init__(self, width, height)
        self.move(0, 0)

    def update(self):
        Screen.update(self)

    def center_x(self):
        return (Display.width_nes - self.width) / 2

    def center_y(self):
        return (Display.height_nes - self.height) / 2

    @staticmethod
    def font_size():
        return 28

    def canvas_to_local_x(self, x):
        return x - self.x

    def canvas_to_local_y(self, y):
        return y - self.y

    def open(self):
        self._opening = True
        self.show()
        self.activate()
        self.refresh()

    def close(self):
        self._opening = False
        self.hide()
        self.deactivate()

    def show(self):
        self._visible = True

    def hide(self):
        self._visible = False

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    def refresh(self):
        pass

    def draw_text(self, text, x, y, width, height, alignX=True, alignY=True):
        self._main_sprite.image.draw_text(text, x, y, width, height, alignX, alignY)
