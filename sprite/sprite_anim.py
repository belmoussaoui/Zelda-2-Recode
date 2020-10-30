from core.pyxi import Sprite
import random


class SpriteAnim(Sprite):
    def __init__(self, width, height, anim_id, delay=0):
        Sprite.__init__(self, width, height)
        self.anim_id = anim_id
        self._create_image()
        self._target = None
        self._anim_id = None
        self._duration = 0
        self.origin_x = .5
        self.origin_y = .0
        self._duration = len(self.anim(anim_id)['frames'])
        self.frame_count = 0
        self.direction = 1
        self.delay = delay
        if anim_id == 3:
            self.ax = random.randint(-12, 12)
            self.ay = random.randint(-4, 20)

    def is_collapse(self):
        return self.anim_id == 1

    def anim(self, anim_id):
        switcher = {
            1: {'frames': self.basic_anim()},
            2: {'frames': [[103, 99, 9, 10], [103, 99, 9, 10], [103, 99, 9, 10], [103, 99, 9, 10], [112, 99, 9, 10],
                           [112, 99, 9, 10],
                           [122, 99, 8, 10], [122, 99, 8, 10], [122, 99, 8, 10], [122, 99, 8, 10], [103, 99, 9, 10],
                           [103, 99, 9, 10],
                           [103, 99, 9, 10], [103, 99, 9, 10]]},
            3: {'frames': self.basic_anim()}
        }
        return switcher.get(anim_id)

    def basic_anim(self):
        return [[86, 42, 16, 15], [86, 42, 16, 15], [103, 42, 16, 15], [103, 42, 16, 15],
                [120, 42, 16, 15], [120, 42, 16, 15], [120, 42, 16, 15], [120, 42, 16, 15],
                [137, 42, 16, 15], [137, 42, 16, 15], [137, 42, 16, 15], [137, 42, 16, 15],
                [120, 59, 16, 15], [120, 59, 16, 15], [120, 59, 16, 15], [120, 59, 16, 15],
                [137, 59, 16, 15], [137, 59, 16, 15], [137, 59, 16, 15], [137, 59, 16, 15],
                [120, 75, 16, 15], [120, 75, 16, 15], [120, 75, 16, 15], [120, 75, 16, 15],
                [137, 75, 16, 15], [137, 75, 16, 15], [137, 75, 16, 15], [137, 75, 16, 15],
                [86, 42, 16, 15], [86, 42, 16, 15], [103, 42, 16, 15], [103, 42, 16, 15]]

    def setup(self, target):
        self._target = target

    def _create_image(self):
        self.load_spritesheet('system/items.png')
        # self.set_frame(39*3 + 3, 42, 16, 16)

    def load_spritesheet(self, filename):
        self._spritesheet = self.load_image(filename)

    def update(self):
        Sprite.update(self)
        self.update_position()
        self.update_origin()
        self.update_main()
        self.update_animation()

    def update_origin(self):
        self.x -= self.rect.width * self.origin_x
        self.y -= self.rect.height * self.origin_y

    def update_position(self):
        self.x = self._target.screen_x()
        self.y = self._target.screen_y()
        if self.anim_id == 3:
            self.random_position()

    def random_position(self):
        self.x += self.ax
        self.y += self.ay

    def update_main(self):
        if self.delay <= 0:
            if self._duration > 0:
                self._duration -= 1
                self.update_frame()
                self.frame_count += 1
            else:
                self.kill()
        else:
            self.delay -= 1

    def is_busy(self):
        return self._duration > 0

    def update_frame(self):
        frame = self.anim(self.anim_id)['frames'][self.frame_count]
        self.image.clear()
        self.set_frame(*frame, 0, 0, False)
        if self._target.height == 32:
            self.set_frame(*frame, 0, 16, False)

    def update_animation(self):
        pass
