import random

import game_objects as g
from core.pyxi import Audio
from core.pyxi import Display
from core.pyxi import Rectangle
from game.game_battler import GameBattler
from game.game_skill import GameStab
from game.game_skill import GameTouch


class GameEnemy(GameBattler):
    def __init__(self, data):
        GameBattler.__init__(self)
        self.hurtbox = Rectangle(0, 0, 0, 0)
        self.exp = 0
        self.damage_exp = 0
        self.damage_mp = 0
        self.is_eternal = False
        self.id = data['id']
        self.is_boss = False

    def is_enemy(self):
        return True

    def is_player(self):
        return False

    @staticmethod
    def enemy(enemy_id):
        switcher = {
            1: {'name': 'Kobolt', 'exp': 0, 'life': 1, 'attack': 8, 'drop': {}},
            2: {'name': 'Bot', 'exp': 2, 'life': 4, 'attack': 16, 'drop': {}},
            3: {'name': 'Stalfos', 'exp': 30, 'life': 8, 'attack': 16, 'drop': {}}
        }
        return switcher.get(enemy_id)

    @staticmethod
    def create_enemy(x, y, enemy_id, data):
        switcher = {
            1: GameBot,
            2: GameStalfos,
            3: GameKobold,
            4: GameBubble,
            5: GameIronknuckle,
            6: GameGooma,
            7: GameHorsehead
        }
        GameEnemy = switcher.get(enemy_id)
        return GameEnemy(x, y, data)

    def is_inside_screen(self):
        return -self.center_x() < self.screen_x() < Display.width_nes + self.center_x()

    def is_active(self):
        return self.is_alive() and self.is_inside_screen() and not self.is_switch()

    def calc_distance_player(self):
        return g.GAME_PLAYER.x - self.x

    def on_dead(self):
        if not self.is_eternal:
            self.activate_switch()

    def perform_collapse(self):
        if self.is_boss:
            self.set_effect('boss_collapse')
        else:
            Audio.play_sound_collapse()
            self.set_effect('collapse')


class GameKobold(GameEnemy):
    def __init__(self, x, y, data):
        self.enemy_id = 3
        GameEnemy.__init__(self, data)
        self.skills = [None, GameTouch(self)]
        self.x = -100
        self.y = y
        self.power = 8
        self.damage_exp = 10
        self.hurtbox = Rectangle(0, 0, 14, 32)
        self.hitbox.x = -8
        self.hitbox.width = 16
        self.hitbox.y = 0
        self.hitbox.height = 32
        self.hp = 1
        self.exp = 0
        self.state = 'walk'
        self.hurt_count = 0
        self.jump_count = 0
        self.speed = 0
        self.setup_direction()
        self.is_eternal = True

    def setup_direction(self):
        self.direction = -1 if g.GAME_PLAYER.direction == 1 else 1
        self.speed = random.choice([1.8, 1.2])

    def is_collided_with_bounds_x(self):
        return False

    def update(self):
        GameEnemy.update(self)

    def on_collision_y(self, y):
        if self.sy > 0:
            self.on_ground()
            self.y = y
        if self.sy < 0:
            self.y = y + self.hitbox.height
        self.sy = 0

    def update_state(self):
        switcher = {
            'walk': self.state_walking,
            'hurt': self.state_hurting
        }
        switcher.get(self.state)()

    def update_skills(self):
        for skill in self.skills:
            if skill:
                skill.update()

    def state_hurting(self):
        pass

    def state_walking(self):
        self.sx = self.speed * self.direction
        if self.jump_count == 32:
            self.jump_count = 0
        if self.jump_count % 16 == 0:
            self.sy -= 2
        self.jump_count += 1
        self.update_skills()

    def state_sliding(self):
        self.sx = self.speed * self.direction
        self.state = 'walk'

    def relive(self):
        self.hurt_count -= 1
        if self.hurt_count == 0:
            self.setup_direction()
            self.hp = 1
            self.state = 'walk'

    def on_damage(self, subject=None):
        Audio.play_sound_damage()
        self.ivcb_count = 15
        self.hurt_count = 120
        self.state = 'hurt'


class GameBot(GameEnemy):
    def __init__(self, x, y, data):
        self.enemy_id = 1
        GameEnemy.__init__(self, data)
        self.skills = [None, GameTouch(self)]
        self.x = x + 8
        self.y = y
        self.power = 16
        self.hurtbox = Rectangle(0, 0, 16, 16)
        self.hitbox.x = -7
        self.hitbox.width = 14
        self.hitbox.y = 0
        self.hitbox.height = 16
        self.hp = 4
        self.exp = 2
        self.state = 'wait'
        self.wait_count = 60
        self.flee_count = 120
        self.seek_count = 120
        self.jump_count = 12
        self.hurt_count = 0
        self.is_eternal = True

    def update(self):
        GameEnemy.update(self)
        self.update_skills()

    def update_state(self):
        switcher = {
            'jump': self.state_jumping,
            'flee': self.state_fleeing,
            'seek': self.state_seeking,
            'wait': self.state_waiting,
            'hurt': self.state_hurting,
            'fall': self.state_falling
        }
        switcher.get(self.state)()
        self.clamp_speed()

    def on_ground(self):
        self.is_on_ground = True
        if self.state == 'fall':
            self.state = 'wait'

    def state_seeking(self):
        if g.GAME_PLAYER.x < self.x:
            self.sx = -.2
        else:
            self.sx = .2
        self.seek_count -= 1
        if self.seek_count <= 0:
            self.state = 'wait'
            self.wait_count = random.randint(0, 180)
        else:
            if random.random() > .99:
                self.sx *= 5
                self.state = 'jump'

    def state_fleeing(self):
        if g.GAME_PLAYER.x < self.x:
            self.sx = .2
        else:
            self.sx = -.2
        self.flee_count -= 1
        if self.flee_count <= 0:
            self.state = 'wait'
            self.wait_count = random.randint(0, 180)

    def update_skills(self):
        for skill in self.skills:
            if skill:
                skill.update()

    def state_waiting(self):
        self.sx = 0
        self.wait_count -= 1
        if self.wait_count <= 0:
            if random.choice([True, False]):
                self.state = 'flee'
                self.flee_count = random.randint(60, 300)
            else:
                self.state = 'seek'
                self.seek_count = random.randint(60, 300)

    def state_hurting(self):
        self.sx = 0
        self.hurt_count -= 1
        if self.hurt_count <= 0:
            self.state = 'flee'

    def state_jumping(self):
        self.jump_count -= 1
        self.sy = -self.jump_count / self.jump_duration * self.jump_force
        if self.jump_count == 0:
            self.jump_count = 12
            self.state = 'fall'

    def on_damage(self, subject=None):
        Audio.play_sound_damage()
        self.ivcb_count = 15
        self.hurt_count = 60
        self.state = 'hurt'


class GameBubble(GameEnemy):
    def __init__(self, x, y, data):
        self.enemy_id = 4
        GameEnemy.__init__(self, data)
        self.skills = [None, GameTouch(self)]
        self.x = x
        self.y = y
        self.exp = 50
        self.hp = 255
        self.hurtbox = Rectangle(0, 0, 16, 16)
        self.power = 8
        self.hitbox.x = -8
        self.hitbox.width = 16
        self.hitbox.y = 0
        self.hitbox.height = 16
        self.hurt_count = 0
        self.state = 'idle'
        self.direction_x = 1
        self.direction_y = 1
        self.damage_mp = 12
        self.setup_direction()
        try:
            speed = data['properties'][1]['value']
        except:
            speed = 1.2
        self.speed = speed
        self.is_eternal = True

    def setup_direction(self):
        self.direction_x = -1 if g.GAME_PLAYER.direction == 1 else 1

    def update(self):
        GameEnemy.update(self)
        self.update_state()
        self.update_skills()

    def update_state(self):
        switcher = {
            'idle': self.state_standing,
            'hurt': self.state_hurting
        }
        switcher.get(self.state)()
        self.clamp_speed()

    def state_standing(self):
        self.sy = self.speed * self.direction_y
        self.sx = self.speed * self.direction_x

    def clamp_speed_x(self):
        return self.sx

    def state_hurting(self):
        self.sx = 0
        self.sy = 0
        self.hurt_count -= 1
        if self.hurt_count <= 0:
            self.state = 'idle'

    def execute_move_x(self):
        if self.can_pass_x():
            self.x += self.sx
        else:
            self.direction_x *= -1

    def execute_move_y(self):
        if self.can_pass_y():
            self.y += self.sy
        else:
            self.direction_y *= -1

    def update_skills(self):
        for skill in self.skills:
            if skill:
                skill.update()

    def on_collision_y(self, y):
        if self.sy > 0:
            self.y = y
        if self.sy < 0:
            self.y = y + self.hitbox.height
        self.sy = 0

    def on_damage(self, subject=None):
        Audio.play_sound_damage()
        self.ivcb_count = 40
        self.hurt_count = 90
        self.state = 'hurt'


class GameSwordsman(GameEnemy):
    def __init__(self, x, y, data):
        GameEnemy.__init__(self, data)
        stab = GameStab(self)
        stab.duration = 24
        self.skills = [None, GameTouch(self), stab]
        self.hurtbox = Rectangle(0, 0, 14, 32)
        self.hurt_count = 0
        self.x = x
        self.y = y
        self.power = 8
        self.hitbox.x = -8
        self.hitbox.width = 16
        self.hitbox.y = 0
        self.hitbox.height = 32
        self.shield = Rectangle(5, 9, 4, 6)
        self.sword = Rectangle(5, 9, 12, 8)
        self.hp = 8
        self.exp = 30
        self.state = 'seek'
        self.wait_count = 60
        self.flee_count = 300
        self.frame = 0
        self.shove_count = 0

    def stab_id(self):
        return 2

    def is_stabbing(self):
        return self.skills[self.stab_id()].is_executing()

    def set_direction(self, d):
        self.shield_direction(d)
        self.sword_direction(d)
        GameEnemy.set_direction(self, d)

    def shield_direction(self, d):
        if d != self.direction:
            self.shield.centerx = self.shield.centerx * -1

    def sword_direction(self, d):
        if d != self.direction:
            self.sword.centerx = self.sword.centerx * -1

    def update(self):
        self.frame += 1
        GameEnemy.update(self)
        self.update_skills()

    def update_state(self):
        switcher = {
            'idle': self.state_standing,
            'walk': self.state_walking,
            'jump': self.state_jumping,
            'fall': self.state_falling,
            'hurt': self.state_hurting,
            'seek': self.state_seeking
        }
        switcher.get(self.state)()
        self.clamp_speed()

    def state_falling(self):
        self.state = 'seek'

    def state_seeking(self):
        if not self.is_stabbing():
            distance = self.calc_distance_player()
            if distance > 0:
                self.set_direction(1)
            else:
                self.set_direction(-1)
            if abs(distance) > 24:
                if distance > 0:
                    self.sx = .8
                else:
                    self.sx = -.8
            else:
                if self.frame % 30 == 0 and random.random() > 0.5:
                    self.skills[2].setup()
                self.sx = 0

    def update_skills(self):
        for skill in self.skills:
            if skill:
                skill.update()

    def damage_direction(self):
        return -1 if self.x <= self.subject.x else 1

    def state_hurting(self):
        if self.hurt_count > 10 or self.shove_count > 10:
            self.sx = .8 * self.damage_direction()
        else:
            self.sx = 0
        self.hurt_count = max(0, self.hurt_count - 1)
        self.shove_count = max(0, self.shove_count - 1)
        if self.hurt_count <= 0 and self.shove_count <= 0:
            self.state = 'seek'

    def on_damage(self, subject=None):
        Audio.play_sound_damage()
        self.ivcb_count = 15
        self.hurt_count = 30
        self.state = 'hurt'
        self.subject = subject

    def on_shield(self, subject=None):
        if self.state != 'hurt':
            Audio.play_sound_shield()
        self.shove_count = 20
        self.state = 'hurt'
        self.subject = subject


class GameStalfos(GameSwordsman):
    def __init__(self, x, y, data):
        self.enemy_id = 2
        GameSwordsman.__init__(self, x, y, data)

    def stab_id(self):
        return 2

    def is_stabbing(self):
        return self.skills[self.stab_id()].is_executing()

    def set_direction(self, d):
        #self.sprite_direction(d)
        self.shield_direction(d)
        self.sword_direction(d)
        GameEnemy.set_direction(self, d)

    def sprite_direction(self, d):
        # Just because the sprite is not center x.
        pass

    def shield_direction(self, d):
        if d != self.direction:
            self.shield.centerx = self.shield.centerx * -1

    def sword_direction(self, d):
        if d != self.direction:
            self.sword.centerx = self.sword.centerx * -1

    def update_state(self):
        switcher = {
            'idle': self.state_standing,
            'walk': self.state_walking,
            'jump': self.state_jumping,
            'fall': self.state_falling,
            'hurt': self.state_hurting,
            'seek': self.state_seeking
        }
        switcher.get(self.state)()
        self.clamp_speed()

    def state_falling(self):
        self.state = 'seek'

    def state_seeking(self):
        if not self.is_stabbing():
            distance = self.calc_distance_player()
            if distance > 0:
                self.set_direction(1)
            else:
                self.set_direction(-1)
            if abs(distance) > 20:
                if distance > 0:
                    self.sx = .8
                else:
                    self.sx = -.8
            else:
                if self.frame % 30 == 0 and random.random() > 0.25:
                    self.skills[2].setup()
                self.sx = 0

    def update_skills(self):
        for skill in self.skills:
            if skill:
                skill.update()

    def damage_direction(self):
        return -1 if self.x <= self.subject.x else 1

    def on_damage(self, subject=None):
        Audio.play_sound_damage()
        self.ivcb_count = 15
        self.hurt_count = 30
        self.state = 'hurt'
        self.subject = subject


class GameIronknuckle(GameSwordsman):
    def __init__(self, x, y, data):
        self.enemy_id = 5
        GameSwordsman.__init__(self, x, y, data)
        self.power = 24
        self.hp = 16
        self.exp = 50
        self.state = 'seek'
        self.post_count = 0
        self.sword = Rectangle(5, 9, 16, 8)
        self.set_direction(-1)

    def update(self):
        GameSwordsman.update(self)
        if self.post_count > 0:
            self.post_count -= 1
            if self.post_count == 1:
                self.skills[2].setup()

    def state_seeking(self):
        distance = self.calc_distance_player()
        if not self.is_stabbing():
            if distance > 0:
                self.set_direction(1)
            else:
                self.set_direction(-1)
        if abs(distance) > 20 and not self.is_stabbing():
            self.sx = .8 if distance > 0 else -.8
        else:
            self.sx = 0
        if abs(distance) < 30:
            if random.random() > 0.1 and not self.is_post_stabbing() and not self.is_stabbing():
                self.sword.y = 18 if random.random() > 0.5 else 9
                self.post_count = 24
        if g.GAME_PLAYER.state == 'crch':
            if random.random() > 0.1:
                self.shield.y = 20
        else:
            if random.random() > 0.1:
                self.shield.y = 9

    def is_shield_up(self):
        return self.shield.y == 9

    def is_stabbing_down(self):
        return self.sword.y == 18

    def is_stabbing_up(self):
        return self.sword.y == 9

    def is_post_stabbing(self):
        return self.post_count > 0

    def on_shield(self, subject=None):
        if self.state != 'hurt':
            Audio.play_sound_shield()
        self.shove_count = 15
        self.state = 'hurt'
        self.subject = subject


class GameGooma(GameEnemy):
    def __init__(self, x, y, data):
        pass


class GameHorsehead(GameEnemy):
    def __init__(self, x, y, data):
        self.enemy_id = 7
        GameEnemy.__init__(self, data)
        stab = GameStab(self)
        stab.duration = 24
        self.skills = [None, GameTouch(self), stab]
        self.x = x + 8
        self.y = y
        self.power = 24
        self.hurtbox = Rectangle(0, 0, 16, -48)
        self.shield = Rectangle(-8, 8, 16, 40)
        self.sword = Rectangle(-24, 32, 24, 1)
        self.hitbox.x = -7
        self.hitbox.width = 14
        self.hitbox.y = 0
        self.hitbox.height = 48
        self.hp = 32
        self.exp = 50
        self.state = 'idle'
        self.wait_count = 30
        self.hurt_count = 0
        self.post_count = 0
        self.direction = -1
        self.is_boss = True

    def update(self):
        GameEnemy.update(self)
        self.update_skills()
        if self.post_count > 0:
            self.post_count -= 1
            if self.post_count == 1:
                self.skills[2].setup()

    def stab_id(self):
        return 2

    def is_active(self):
        return self.is_alive() and not self.is_switch()

    def is_stabbing(self):
        return self.skills[self.stab_id()].is_executing()

    def is_post_stabbing(self):
        return self.post_count > 0

    def update_state(self):
        switcher = {
            'idle': self.state_idling,
            'wait': self.state_waiting,
            'hurt': self.state_hurting,
            'shove': self.state_shoving,
            'seek': self.state_seeking
        }
        switcher.get(self.state)()
        self.clamp_speed()

    def state_idling(self):
        pass

    def state_seeking(self):
        self.seek_count -= 1
        if not self.is_stabbing() and not self.is_post_stabbing():
            distance = self.calc_distance_player()
            if abs(distance) > 24:
                self.sx = -.5
            else:
                self.post_count = 24
                self.sx = 0
        if self.seek_count <= 0:
            self.state = 'wait'
            self.wait_count = random.randint(0, 60)

    def update_skills(self):
        for skill in self.skills:
            if skill:
                skill.update()

    def state_waiting(self):
        self.sx = 0
        self.wait_count -= 1
        if self.wait_count <= 0:
            self.seek_count = random.randint(30, 90)
            self.state = 'seek'

    def state_hurting(self):
        self.sx = .8
        self.hurt_count = max(0, self.hurt_count - 1)
        if self.hurt_count <= 0:
            self.wait_count = 45
            self.state = 'wait'

    def on_damage(self, subject=None):
        Audio.play_sound_damage()
        self.ivcb_count = 30
        self.hurt_count = 30
        self.state = 'hurt'

    def state_shoving(self):
        self.sx = .6
        self.shove_count -= 1
        if self.shove_count <= 0:
            self.wait_count = random.randint(0, 60)
            self.state = 'wait'

    def on_shield(self, subject=None):
        if self.state != 'shove':
            Audio.play_sound_shield()
        self.shove_count = 10
        self.state = 'shove'

    def is_post_stabbing(self):
        return self.post_count > 0
