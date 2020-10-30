import game.game_map as game_map
import game.game_player as game_player
import game.game_system as game_system
import game.game_object as game_object

GAME_MAP = None
GAME_PLAYER = None
GAME_SYSTEM = None


def create_game_objects():
    global GAME_MAP
    global GAME_PLAYER
    global GAME_SYSTEM
    game_object.GameObject.SWITCH = {}
    GAME_MAP = game_map.GameMap()
    GAME_PLAYER = game_player.GameLink()
    GAME_SYSTEM = game_system.GameSystem()
