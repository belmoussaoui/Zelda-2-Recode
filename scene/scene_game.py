import json

import game_objects as g
from core.input import Input
from core.pyxi import Audio
from scene.scene_base import SceneBase
from scene.scene_gameover import SceneGameover
from scene.scene_manager import SceneManager
from screen.screen_nextup import ScreenNextUp
from screen.screen_select import ScreenSelect
from screen.screen_status import ScreenStatus
from screen.screen_boss import ScreenBoss
from sprite.sprite_player import SpritePlayer
from sprite.spriteset_map import SpritesetMap


class SceneGame(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def create(self):
        SceneBase.create(self)
        self.load_map_data()
        self.create_display_object()

    def load_map_data(self, filename='northpalace', map_id=1):
        filename = g.GAME_MAP.map_name or filename
        map_id = g.GAME_MAP.map_id or map_id
        with open('data/maps/' + filename + '{:02d}.json'.format(map_id)) as json_file:
            tiled = json.load(json_file)
            g.GAME_MAP.setup(tiled)
        g.GAME_MAP.is_transferring = False

    def create_display_object(self):
        self.create_spriteset()
        self.create_player()
        self.create_screens()

    def create_screens(self):
        self.create_status_screen()
        self.create_nextup_screen()
        self.create_select_screen()
        self.create_boss_screen()

    def create_status_screen(self):
        self._statusScreen = ScreenStatus()
        self._statusScreen.x = 0
        self._statusScreen.y = 0
        self.add(self._statusScreen)

    def create_nextup_screen(self):
        self._nextup_screen = ScreenNextUp()
        self._statusScreen.set_nextup(self._nextup_screen)
        self._nextup_screen.set_handler('cancel', self.command_cancel)
        self._nextup_screen.set_handler('attack', self.command_attack)
        self._nextup_screen.set_handler('magic', self.command_magic)
        self._nextup_screen.set_handler('life', self.command_life)
        self.add(self._nextup_screen)

    def create_select_screen(self):
        self._select_screen = ScreenSelect()
        self.add(self._select_screen)

    def create_boss_screen(self):
        self._bossScreen = ScreenBoss()
        self.add(self._bossScreen)

    def create_spriteset(self):
        self._spriteset = SpritesetMap()
        self.add(self._spriteset)

    def create_player(self):
        self._player_sprite = SpritePlayer()
        self._spriteset._tilemap.add(self._player_sprite)
        self.add(self._spriteset._tilemap)

    def start(self):
        SceneBase.start(self)
        g.GAME_PLAYER.start()
        g.GAME_MAP.start()
        g.GAME_MAP.target = g.GAME_PLAYER  # camera
        self.start_audio()

    def start_audio(self):
        if g.GAME_MAP.map_name == 'northpalace':
            Audio.play_music_ground()
        else:
            Audio.play_music_temple()

    def update(self):
        if not self._nextup_screen._active and not self._select_screen._active:
            self.update_game()
            self.update_spriteset()
        SceneBase.update(self)
        self.update_screens()
        self.update_scene()
        self.update_debug()

    def update_game(self):
        if not self.is_busy():
            g.GAME_MAP.update()
            g.GAME_PLAYER.update()

    def update_spriteset(self):
        self._spriteset.update()
        #self.add(self._spriteset)

    def update_screens(self):
        update = self._select_screen._active or self._nextup_screen._active
        self._select_screen.update()
        if not self._spriteset.is_busy():
            self._statusScreen.update()
            self._nextup_screen.update()
            if Input.is_key_triggered('escape') and not update:
                self._select_screen.open()
        if g.GAME_MAP.boss() and not self._bossScreen.is_open():
            self._bossScreen.setup(g.GAME_MAP.boss())
        if self._bossScreen.is_open():
            self._bossScreen.refresh()

    def update_scene(self):
        if g.GAME_PLAYER.is_dead:
            SceneManager.goto(SceneGameover)
        if g.GAME_MAP.is_transferring:
            SceneManager.goto(SceneGame)

    def command_cancel(self):
        g.GAME_PLAYER.nextup = g.GAME_PLAYER.next_up()
        self._nextup_screen.close()

    def command_attack(self):
        g.GAME_PLAYER.next_attack()
        self._nextup_screen.close()

    def command_life(self):
        g.GAME_PLAYER.next_life()
        self._nextup_screen.close()

    def command_magic(self):
        g.GAME_PLAYER.next_magic()
        self._nextup_screen.close()

    def update_debug(self):
        if Input.is_key_triggered('i'):
            g.GAME_SYSTEM.call_debug()
