import game_objects as g
from scene.scene_base import SceneBase
from scene.scene_manager import SceneManager
from scene.scene_title import SceneTitle


class SceneBoot(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def start(self):
        SceneBase.start(self)
        self.boot_game()
        SceneManager.goto(SceneTitle)

    def boot_game(self):
        g.create_game_objects()
