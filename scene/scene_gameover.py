import game_objects as g
import scene.scene_game as s
from core.pyxi import Audio
from core.pyxi import Display
from scene.scene_base import SceneBase
from scene.scene_manager import SceneManager
from sprite.sprite_base import SpriteBase
from sprite.sprite_player import SpritePlayer


class SceneGameover(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.black_sprite = None
        self.wait_count = 0

    def create(self):
        SceneBase.create(self)
        self.create_background()
        self.create_display_object()

    def create_background(self):
        self.black_sprite = SpriteBase(*Display.screen_size_nes)
        self.black_sprite.image.fill((0, 0, 0))
        self.add(self.black_sprite)

    def create_display_object(self):
        self.create_player()

    def create_player(self):
        self._sprite = SpritePlayer()
        self.add(self._sprite)

    def start(self):
        SceneBase.start(self)
        Audio.stop_music()
        Audio.play_sound_gameover()

    def update(self):
        SceneBase.update(self)
        self.wait_count += 1
        if self.wait_count == 180:
            g.GAME_PLAYER.clear()
            g.GAME_MAP.clear()
            SceneManager.goto(s.SceneGame)
