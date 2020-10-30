from core.pyxi import Sprite


class SpriteExp(Sprite):
    def __init__(self):
        Sprite.__init__(self, 16, 16)
        self.duration = 90
        self.origin_x = .0
        self.origin_y = .0
        self.pos_y = 0
        self.duration = 60
        self._create_image()

    def load_spritesheet(self, filename):
        self._spritesheet = self.load_image(filename)

    def _create_image(self):
        self.load_spritesheet('system/items.png')

    def is_busy(self):
        return self.duration > 0

    def update(self):
        self.update_position()
        self.update_origin()
        self.duration -= 1
        if self.duration == 0:
            self.kill()

    def update_origin(self):
        self.x -= self.rect.width * self.origin_x
        self.y -= self.rect.height * self.origin_y

    def update_position(self):
        self.pos_y += 0.28
        self.x = self._target.screen_x()
        self.y = self._target.screen_y() - self.pos_y

    def setup(self, target):
        self._target = target
        self.create_digits(target.exp)
        self.update_position()

    def create_digits(self, exp):
        string = str(exp)
        pos_x = 0
        for char in string:
            self.create_digit(int(char), pos_x)
            pos_x += 4

    def create_digit(self, digit, pos_x):
        y = 42
        if digit == 0:
            x = 50
        elif digit == 1:
            x = 4
        elif digit == 2:
            x = 13
        elif digit == 3:
            x = 22
        elif digit == 5:
            x = 31
        elif digit == 7:
            x = 40
        else:
            x = 0
        self.set_frame(x, y, 4, 16, pos_x, 0, False)
