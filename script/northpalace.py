import game_objects as g
from game.game_elevator import GameElevator
from scene.scene_manager import SceneManager
from sprite.sprite_base import SpriteBase
from scene.scene_title import SceneTitle


def map_01():
    transfer_01()


def transfer_01():
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        map_name = 'parapalace'
        g.GAME_MAP.transfer(map_name, 1, 1, g.GAME_PLAYER.y / 16 - 1)
        GameElevator.position_y = 12


triforce_count = 900
sprite_zelda = SpriteBase(32, 32)
sprite_triforce1 = SpriteBase(16, 16)
sprite_triforce2 = SpriteBase(16, 16)
sprite_triforce3 = SpriteBase(16, 16)
def map_02():
    global triforce_count
    global sprite_triforce1, sprite_triforce2, sprite_triforce3
    if g.GAME_PLAYER.can_input:
        g.GAME_PLAYER.can_input = False
        g.GAME_PLAYER.state = "pick"
        g.GAME_PLAYER.direction = -1
        g.GAME_PLAYER.x += 1
        create_zelda()
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
        if triforce_count == 500:
            sprite_zelda.set_frame(9 + 32 + 5, 100 - 16, 32, 32)
        if triforce_count == 380:
            SceneManager.scene('start_fade_out')
            g.GAME_MAP.transfer('northpalace', 3, 7.5, 12)



def create_triforce(triforce):
    triforce.load_spritesheet('characters/characters.png')
    triforce.set_frame(230, 100, 16, 16)
    triforce.x = 256 / 2 - 8
    triforce.y = 240 / 2 - 8 + 48
    SceneManager.scene('add', triforce)

def create_zelda():
    global sprite_zelda
    sprite_zelda.load_spritesheet('characters/characters.png')
    sprite_zelda.set_frame(9, 100-16, 32, 32)
    sprite_zelda.x = 256 / 2 - 16
    sprite_zelda.y = 240 / 2 - 8 + 16
    SceneManager.scene('add', sprite_zelda)

start_anim = False
anim_count = 900
def map_03():
    global start_anim, anim_count
    global sprite_zelda
    if not start_anim:
        SceneManager._scene._messageScreen.open()
        SceneManager._scene._messageScreen.draw_screen()
        start_anim = True
        g.GAME_PLAYER.can_input = False
        g.GAME_PLAYER.direction = 1
        g.GAME_PLAYER.x -= 8
        sprite_zelda.load_spritesheet('characters/characters.png')
        sprite_zelda.set_frame(82, 100 - 16, 16, 32)
        sprite_zelda.x = 256 / 2 - 16
        sprite_zelda.y = 240 / 2 - 8 + 64
        sprite_zelda.image.flip()
        SceneManager.scene('add', sprite_zelda)
        #create_zelda()
        SceneManager.scene('hide_screens')
        create_end_curtains()
        for curtain in curtains_up:
            curtain.set_frame(48, 240, 16, 16)
    else:
        if anim_count > 360:
            update_curtains()
        elif anim_count == 300:
            sprite_zelda.x -= 4
            g.GAME_PLAYER.x += 4
        elif anim_count == 120:
            SceneManager.scene('start_fade_out')


        anim_count -= 1

curtains_up = []
def create_curtains(offset=0):
    global curtains_up
    curtains_up = []
    for i in range(16):
        curtain = SpriteBase(16, 16)
        curtain.x = i * 16
        curtain.y = 16 * 3 + offset
        curtain.layer = 2
        curtain.load_spritesheet('tilesets/northpalace.png')
        curtain.set_frame(48, 240, 16, 1)
        SceneManager.scene('add', curtain)
        curtains_up.append(curtain)

curtains = []
def create_end_curtains():
    global curtains
    for i in range(16):
        curtain = SpriteBase(16, 16)
        curtain.x = i * 16
        curtain.y = 16 * 4
        curtain.layer = 3
        curtain.load_spritesheet('tilesets/northpalace.png')
        curtain.set_frame(48, 240 + 24, 16, 16)
        SceneManager.scene('add', curtain)
        curtains.append(curtain)

offset = 0
def update_curtains():
    global anim_count, curtains_up, offset, curtains
    if anim_count % 80 == 20 and anim_count >= 420:
        offset = 0
        create_curtains(16)
    if anim_count % 5 == 0:
        offset += 1
        for curtain in curtains:
            curtain.y += 1
        for curtain in curtains_up:
            curtain.set_frame(48, 240 + 16 - offset, 16, offset)
            if offset == 16:
                curtains.append(curtain)




