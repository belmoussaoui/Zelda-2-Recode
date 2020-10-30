import game_objects as g
from game.game_elevator import GameElevator


def map_01():
    transfer_01()


def transfer_01():
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        map_name = 'parapalace'
        g.GAME_MAP.transfer(map_name, 1, 1, g.GAME_PLAYER.y / 16 - 1)
        GameElevator.position_y = 12;
