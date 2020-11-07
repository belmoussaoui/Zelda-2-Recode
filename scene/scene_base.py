from core.pyxi import Display
from core.pyxi import Stage
from scene.scene_manager import SceneManager
from sprite.sprite_base import SpriteBase


class SceneBase(Stage):
    def __init__(self):
        Stage.__init__(self)
        self.black_sprite = None
        self._active = False
        self.fade_count = 0
        self.fade_sprite = None

    def create(self):
        self.create_background()

    def create_background(self):
        self.black_sprite = SpriteBase(*Display.screen_size_nes)
        self.black_sprite.image.fill((0, 0, 0))
        self.add(self.black_sprite)

    def start_fade(self, duration):
        self.create_fade_sprite()
        self.opacity = self.fade_sprite.image.get_alpha()
        self.duration = duration
        self.fade_count = duration

    def start_fade_in(self, duration=60):
        self.start_fade(duration)
        self.fade_sign = 1

    def start_fade_out(self, duration=60):
        self.start_fade(duration)
        self.fade_sign = -1

    def create_fade_sprite(self):
        if not self.fade_sprite:
            self.fade_sprite = SpriteBase(*Display.screen_size_nes)
            self.fade_sprite.image.fill((0, 0, 0))
            self.fade_sprite.image.set_alpha(0)
            self.fade_sprite.layer = 99
            self.add(self.fade_sprite)

    def update_fade(self):
        if self.fade_count > 0:
            if self.fade_sign == 1:
                self.opacity = max(int(self.opacity / self.fade_count), 0)
            else:
                self.opacity = min(self.opacity + 255 / self.duration, 255)
            self.fade_count -= 1
            self.fade_sprite.image.set_alpha(self.opacity)

    def start(self):
        self._active = True

    def is_active(self):
        return self._active

    def is_ready(self):
        return True

    def update(self):
        Stage.update(self)
        self.update_fade()

    def draw(self, screen):
        # screen.fill((251, 194, 68))
        screen.fill((237, 237, 237))
        Stage.draw(self, screen)

    def is_busy(self):
        return self.fade_count > 0

    def terminate(self):
        pass

    def pop_scene(self):
        SceneManager.pop()
