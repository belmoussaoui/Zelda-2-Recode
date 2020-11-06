import game_objects as g
from game.game_elevator import GameElevator
from scene.scene_manager import SceneManager
from sprite.sprite_base import SpriteBase


def map_01():
    transfer_01()


def transfer_01():
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        map_name = 'parapalace'
        g.GAME_MAP.transfer(map_name, 1, 1, g.GAME_PLAYER.y / 16 - 1)
        GameElevator.position_y = 12


triforce_count = 900
sprite_triforce1 = SpriteBase()
sprite_triforce2 = SpriteBase()
sprite_triforce3 = SpriteBase()
def map_02():
    global triforce_count
    global sprite_triforce1, sprite_triforce2, sprite_triforce3
    if g.GAME_PLAYER.can_input:
        g.GAME_PLAYER.can_input = False
        g.GAME_PLAYER.state = "pick"
        g.GAME_PLAYER.direction = -1
        g.GAME_PLAYER.x += 1
        create_triforce(sprite_triforce1)
        create_triforce(sprite_triforce2)
        create_triforce(sprite_triforce3)
        SceneManager.scene('hide_screens')
    else:
        triforce_count -= 1
        if triforce_count % 90 == 0:
            sprite_triforce1.set_frame(230, 100, 16, 16)
            sprite_triforce2.set_frame(230, 100, 16, 16)
            sprite_triforce3.set_frame(230, 100, 16, 16)
        if triforce_count % 90 == 30:
            sprite_triforce1.set_frame(230 + 16 + 3, 100, 16, 16)
            sprite_triforce2.set_frame(230 + 16 + 3, 100, 16, 16)
            sprite_triforce3.set_frame(230 + 16 + 3, 100, 16, 16)
        if triforce_count % 90 == 60:
            sprite_triforce1.set_frame(230 + 32 + 5, 100, 16, 16)
            sprite_triforce2.set_frame(230 + 32 + 5, 100, 16, 16)
            sprite_triforce3.set_frame(230 + 32 + 5, 100, 16, 16)
        if triforce_count % 5 == 0 and triforce_count > 570:
            sprite_triforce1.x -= 1
            sprite_triforce2.x += 1
            sprite_triforce3.y -= 1


def create_triforce(triforce):
    triforce.load_spritesheet('characters/characters.png')
    triforce.set_frame(230, 100, 16, 16)
    triforce.x = 256 / 2 - 8
    triforce.y = 240 / 2 - 8 + 48
    SceneManager.scene('add', triforce)

