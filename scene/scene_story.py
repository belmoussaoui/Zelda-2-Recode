from core.pyxi import Display
from scene.scene_base import SceneBase
from scene.scene_game import SceneGame
from scene.scene_manager import SceneManager
from sprite.sprite_base import SpriteBase


class SceneStory(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.black_sprite = None
        self.story_sprite = None
        self.fade = None
        self.text = None
        self.wait_count = 1#420
        self.opacity = 255

    def create(self):
        SceneBase.create(self)
        self.create_background()
        self.create_story()

    def create_background(self):
        self.black_sprite = SpriteBase(*Display.screen_size_nes)
        self.black_sprite.image.fill((0, 0, 0))
        self.add(self.black_sprite)

    def create_story(self):
        self.story_sprite = SpriteBase(800, 480)
        self.story_sprite.image.load_image('story/story3.png')
        self.story_sprite.image = self.story_sprite.image.scale(int(800/4), int(480/4))
        self.story_sprite.x = (256 - 800/4) / 2
        self.story_sprite.y = 16
        self.add(self.story_sprite)
        self.fade = SpriteBase(*Display.screen_size_nes)
        self.fade.image.fill((0, 0, 0))
        self.add(self.fade)

    def start(self):
        SceneBase.start(self)

    def update(self):
        if self.opacity > 0 and self.wait_count > 150:
            self.opacity = max(self.opacity - 3, 0)
        self.fade.image.fill((0, 0, 0, self.opacity))
        SceneBase.update(self)
        self.update_wait()
        self.update_scene()
        if self.wait_count < 100:
            self.opacity = min(self.opacity + 3, 255)

    def update_wait(self):
        self.wait_count -= 1

    def update_scene(self):
        if self.wait_count <= 0:
            SceneManager.goto(SceneGame)

    def terminate(self):
        SceneBase.terminate(self)
