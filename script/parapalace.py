import game_objects as g
from game.game_elevator import GameElevator
from core.pyxi import Audio
from scene.scene_manager import SceneManager
from scene.scene_end import SceneEnd


def map_01():
    transfer_01()


def transfer_01():
    if g.GAME_PLAYER.left <= 0:
        g.GAME_MAP.transfer('northpalace', 1, 43, 12)

    if g.GAME_PLAYER.top >= g.GAME_MAP.height():
        g.GAME_MAP.transfer('parapalace', 2, 39.5, 4)
        GameElevator.position_y = 4


def map_02():
    transfer_02()
    enemy_02()


def transfer_02():
    if g.GAME_PLAYER.left <= 0:
        g.GAME_MAP.transfer('parapalace', 3, 62, 12)
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        g.GAME_MAP.transfer('parapalace', 4, 1, 12)
    if g.GAME_PLAYER.top < 2 * 16 and g.GAME_PLAYER.is_on_elevator():
        g.GAME_MAP.transfer('parapalace', 1, 39.5, 15)
        GameElevator.position_y = 15


def enemy_02():
    if not g.GAME_PLAYER.is_on_elevator():
        kobolds = []
        for enemy in g.GAME_MAP.enemies:
            if enemy.enemy_id == 3:
                kobolds.append(enemy)
        if g.GAME_MAP.display_x != 0 and g.GAME_MAP.display_x < g.GAME_MAP.width() - 256:
            if g.GAME_PLAYER.direction == 1:
                enemy = kobolds[0]
                if enemy.x > g.GAME_MAP.display_x + 256 + 7 or enemy.x < g.GAME_MAP.display_x - 7 or \
                        enemy.hurt_count == 1:
                    enemy.setup_direction()
                    enemy.x = g.GAME_MAP.display_x + 256 + 7
            else:
                enemy = kobolds[1]
                if enemy.x > g.GAME_MAP.display_x + 256 + 7 or enemy.x < g.GAME_MAP.display_x - 7 or \
                        enemy.hurt_count == 1:
                    enemy.setup_direction()
                    enemy.x = g.GAME_MAP.display_x - 6
            if not enemy.is_alive():
                enemy.relive()



def map_03():
    transfer_03()
    enemy_03()


def enemy_03():
    kobolds = []
    for enemy in g.GAME_MAP.enemies:
        if enemy.enemy_id == 3:
            kobolds.append(enemy)
    enemy = kobolds[0]
    if enemy.x > g.GAME_MAP.display_x + 256 + 7 or enemy.x < g.GAME_MAP.display_x - 7 and \
            g.GAME_MAP.canvas_to_map_x(g.GAME_PLAYER.x) == 17 or enemy.hurt_count == 1:
        enemy.direction = 1
        enemy.speed = 1.8
        enemy.x = g.GAME_MAP.display_x - 7
    if not enemy.is_alive():
        enemy.relive()
        enemy.direction = 1
        enemy.speed = 1.8


def transfer_03():
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        g.GAME_MAP.transfer('parapalace', 2, 1, 12)
        GameElevator.position_y = 13


def map_04():
    transfer_04()
    kobolds = []
    for enemy in g.GAME_MAP.enemies:
        if enemy.enemy_id == 3:
            kobolds.append(enemy)
    if g.GAME_MAP.display_x != 0 and g.GAME_MAP.display_x != g.GAME_MAP.width() - 256:
        if g.GAME_PLAYER.direction == 1:
            enemy = kobolds[0]
            if enemy.x > g.GAME_MAP.display_x + 256 + 7 or enemy.x < g.GAME_MAP.display_x - 7 or \
                    enemy.hurt_count == 1:
                enemy.setup_direction()
                enemy.x = g.GAME_MAP.display_x + 256 + 7
        else:
            enemy = kobolds[1]
            if enemy.x > g.GAME_MAP.display_x + 256 + 7 or enemy.x < g.GAME_MAP.display_x - 7 or \
                    enemy.hurt_count == 1:
                enemy.setup_direction()
                enemy.x = g.GAME_MAP.display_x - 6
        if not enemy.is_alive():
            enemy.relive()


def transfer_04():
    if g.GAME_PLAYER.left <= 0:
        g.GAME_MAP.transfer('parapalace', 2, 62, 12)
        GameElevator.position_y = 13
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        g.GAME_MAP.transfer('parapalace', 5, 1, 12)
        GameElevator.position_y = 12


def map_05():
    transfer_05()


def transfer_05():
    if g.GAME_PLAYER.left <= 0:
        g.GAME_MAP.transfer('parapalace', 4, 62, 12)
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        GameElevator.position_y = 12
        g.GAME_MAP.transfer('parapalace', 9, 1, 12)
    if g.GAME_PLAYER.top >= g.GAME_MAP.height():
        g.GAME_MAP.transfer('parapalace', 6, 55.5, 4)
        GameElevator.position_y = 4


def map_06():
    if g.GAME_PLAYER.left <= 0:
        g.GAME_MAP.transfer('parapalace', 7, 62, 12)
    if g.GAME_PLAYER.top < 2 * 16 and g.GAME_PLAYER.is_on_elevator():
        g.GAME_MAP.transfer('parapalace', 5, 39.5, 15)
        GameElevator.position_y = 15


def map_07():
    transfer_07()
    if g.GAME_PLAYER.y > 216:
        if g.GAME_PLAYER.state != 'hurt':
            g.GAME_PLAYER.state = 'hurt'
            g.GAME_PLAYER.hurt_count = 30
        g.GAME_PLAYER.sy = 0.16
        g.GAME_PLAYER.sx = 0
        g.GAME_PLAYER.set_hp(0)
    if g.GAME_MAP.objects[0].y > 216:
        g.GAME_MAP.objects[0].activate_switch()



def transfer_07():
    if g.GAME_PLAYER.left <= 0:
        g.GAME_MAP.transfer('parapalace', 8, 62, 12)
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        g.GAME_MAP.transfer('parapalace', 6, 1, 12)
        GameElevator.position_y = 13


def map_08():
    transfer_08()


def transfer_08():
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        g.GAME_MAP.transfer('parapalace', 7, 1, 12)
        GameElevator.position_y = 15


def map_09():
    transfer_09()


def transfer_09():
    if g.GAME_PLAYER.left <= 0:
        g.GAME_MAP.transfer('parapalace', 5, 62, 12)
        GameElevator.position_y = 12
    if g.GAME_PLAYER.top < 2 * 16 and g.GAME_PLAYER.is_on_elevator():
        g.GAME_MAP.transfer('parapalace', 10, 7.5, 15)
        GameElevator.position_y = 15
    if g.GAME_PLAYER.top >= g.GAME_MAP.height():
        g.GAME_MAP.transfer('parapalace', 12, 7.5, 4)
        GameElevator.position_y = 4


def map_10():
    if g.GAME_PLAYER.top >= g.GAME_MAP.height():
        g.GAME_MAP.transfer('parapalace', 9, 39.5, 4)
        GameElevator.position_y = 4
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        g.GAME_MAP.transfer('parapalace', 11, 1, 12)


def map_11():
    if g.GAME_PLAYER.top >= g.GAME_MAP.height():
        g.GAME_MAP.transfer('parapalace', 9, 39.5, 4)
        GameElevator.position_y = 4
    if g.GAME_PLAYER.left <= 0:
        g.GAME_MAP.transfer('parapalace', 10, 62, 12)
        GameElevator.position_y = 12


def map_12():
    if g.GAME_PLAYER.top < 2 * 16 and g.GAME_PLAYER.is_on_elevator():
        g.GAME_MAP.transfer('parapalace', 9, 39.5, 15)
        GameElevator.position_y = 15
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        g.GAME_MAP.transfer('parapalace', 13, 1, 12)


def map_13():
    if g.GAME_PLAYER.left <= 0:
        g.GAME_MAP.transfer('parapalace', 12, 62, 12)
        GameElevator.position_y = 13
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        g.GAME_MAP.transfer('parapalace', 14, 1, 12)


switch14 = False
def map_14():
    global switch14, end
    if g.GAME_PLAYER.left <= 0:
        g.GAME_MAP.transfer('parapalace', 13, 62, 12)
    if g.GAME_PLAYER.x >= 24 * 16 and not switch14 and g.GAME_PLAYER.is_alive():
        Audio.play_music_boss()
        switch14 = True
        g.GAME_MAP.display_x = 256
        g.GAME_MAP.deactivate_scroll()
        g.GAME_MAP.enemies[0].state = 'wait'
        g.GAME_MAP.set_boss(g.GAME_MAP.enemies[0])
    if not g.GAME_PLAYER.is_alive():
        switch14 = False
        g.GAME_MAP.set_boss(None)
    if not g.GAME_MAP.enemies[0].is_alive():
        Audio.stop_music()
        g.GAME_MAP.activate_scroll()
        g.GAME_MAP.set_boss(None)
    if g.GAME_PLAYER.right >= g.GAME_MAP.width():
        switch14 = False
        SceneManager.scene('start_fade_out')
        SceneManager.goto(SceneEnd)

