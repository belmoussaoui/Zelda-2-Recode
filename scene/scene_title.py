from core.input import Input
from core.pyxi import Display
from core.pyxi import Audio
from scene.scene_base import SceneBase
from scene.scene_manager import SceneManager
from scene.scene_story import SceneStory
from screen.screen_title import ScreenTitle
from screen.screen_credits import ScreenCredits
from sprite.sprite_base import SpriteBase


class SceneTitle(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self._title_sprite = None
        self._title_window = None
        self.state = 'start'

    def create(self):
        SceneBase.create(self)
        self.create_background()
        self.create_title_screen()
        self.create_credits_screen()

    def start(self):
        SceneBase.start(self)
        Audio.play_music_title()

    def update(self):
        SceneBase.update(self)
        self.update_window()
        self.update_state()

    def update_state(self):
        if self.state == 'start':
            self.process_start()
        if self.state == 'credits':
            self.process_credits()

    def process_start(self):
        if Input.is_key_triggered('return'):
            self._title_sprite.image.fill((0, 0, 0))
            self._title_screen.open()
            self.state = 'select'

    def process_credits(self):
        if Input.is_key_triggered('escape'):
            self._title_screen.open()
            self._title_screen.select(2)
            self._credits_screen.close()
            self.state = 'start'

    def update_window(self):
        self._title_screen.update()
        self._credits_screen.update()

    def terminate(self):
        SceneBase.terminate(self)

    def create_background(self):
        self._title_sprite = SpriteBase(*Display.screen_size_nes)
        self._title_sprite.image.load_image('titles/screen.png')
        self.add(self._title_sprite)

    def create_title_screen(self):
        self._title_screen = ScreenTitle()
        self._title_screen.set_handler('newGame', self.command_new_game)
        self._title_screen.set_handler('credits', self.command_credits)
        self.add(self._title_screen)

    def create_credits_screen(self):
        self._credits_screen = ScreenCredits()
        self.add(self._credits_screen)

    def command_new_game(self):
        SceneManager.goto(SceneStory)

    def command_credits(self):
        self._title_screen.close()
        self._credits_screen.open()
        self.state = 'credits'
