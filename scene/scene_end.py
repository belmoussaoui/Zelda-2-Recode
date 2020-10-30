from scene.scene_manager import SceneManager
from scene.scene_base import SceneBase
from sprite.sprite_player import SpritePlayer

class SceneEnd(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def create(self):
        SceneBase.create(self)
        self._player_sprite = SpritePlayer()
        self.add(self._player_sprite)