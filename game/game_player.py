import game_objects as g
from core.input import Input
from core.pyxi import Rectangle
from core.pyxi import Audio
from game.game_actor import GameActor
from game.game_battler import GameBattler
from game.game_skill import GameStab


class GamePlayer(GameBattler):
    def __init__(self):
        GameBattler.__init__(self)
        self.attack = 0
        self.exp = 0
        self.life = 0
        self.magic = 0
        self.magic_index = 0
        self.magic_list = []#{'name': 'shield', 'cost': [32], 'id': 1},
                           #{'name': 'jump', 'cost': [48], 'id': 2}]
        self.ground_type = ''
        self.nextup = 0
        self.attack_next = [200, 500, 1000, 2000, 3000, 5000, 8000]
        self.magic_next = [100, 300, 700, 1200, 2200, 3500, 6000, 9000]
        self.life_next = [50, 150, 400, 800, 1500, 2500, 4000, 9000]
        self.power_level = [2, 3, 4, 6, 9, 12, 18, 24]
        self.power = self.power_level[self.attack]
        self.next_up()
        self.keys = 0
        self.hurt_dir = 0
        self.hurt_count = 30

    def next_up(self):
        next_exp = 9000
        if self.nextup < self.next_exp_attack():
            next_exp = min(next_exp, self.next_exp_attack())
        if self.nextup < self.next_exp_magic():
            next_exp = min(next_exp, self.next_exp_magic())
        if self.nextup < self.next_exp_life():
            next_exp = min(next_exp, self.next_exp_life())
        return next_exp

    def next_exp_attack(self):
        return self.attack_next[self.attack]

    def next_exp_magic(self):
        return self.magic_next[self.magic]

    def next_exp_life(self):
        return self.life_next[self.life]

    def next_attack(self):
        self.exp -= self.attack_next[self.attack]
        self.nextup = 0
        self.attack += 1
        self.power = self.power_level[self.attack]

    def next_life(self):
        self.exp -= self.life_next[self.life]
        self.nextup = 0
        self.gain_hp(self.mhp)
        self.life += 1

    def next_magic(self):
        self.exp -= self.magic_next[self.magic]
        self.nextup = 0
        self.magic += 1

    def is_player(self):
        return True

    def is_enemy(self):
        return False

    def gain_mp(self, mp):
        self.mp += mp
        self.mp = max(self.mp, 0)

    def gain_exp(self, exp):
        self.exp += exp
        self.exp = max(self.exp, 0)

    def level_up(self):
        pass

    def move_by_input(self):
        pass

    def can_pass_x(self):
        if self.is_collided_with_bounds_x():
            return False
        if self.is_collided_with_map_x():
            return False
        if self.is_collided_with_characters_x():
            return False
        return True

    def can_pass_y(self):
        if self.is_collided_with_characters_y():
            return False
        if self.is_collided_with_map_y():
            return False
        return True

    def is_collided_with_characters_x(self):
        rect = self._create_rect_for_collision_x()
        if g.GAME_MAP.is_collided_with_characters(rect):
            x = g.GAME_MAP.round_x_with_characters(self.sx)
            self.on_collision_x(x)
            return True
        return False

    def is_collided_with_characters_y(self):
        rect = self._create_rect_for_collision_y()
        if g.GAME_MAP.is_collided_with_objects(rect):
            y = g.GAME_MAP.round_y_with_characters(self.sy)
            self.on_collision_y(y)
            return True
        if g.GAME_MAP.is_collided_with_characters(rect):
            y = g.GAME_MAP.round_y_with_characters(self.sy)
            self.on_collision_y(y)
            return True
        return False

    def execute_move_y(self):
        if self.can_pass_y():
            if not self.is_jumping() and self.state != 'hurt':
                # self.stand_up()
                self.state = 'fall'
            self.ground_type = ''
            self.y += self.sy

    def add_key(self):
        self.keys += 1

    def round_x_with_map(self):
        return g.GAME_MAP.round_x_with_map(self.sx, True)


class GameLink(GamePlayer):
    def __init__(self):
        GamePlayer.__init__(self)
        self.mhp = 16 * 4
        self.hp = 16 * 4
        self.mmp = 16 * 4
        self.mp = 16 * 4
        self.skills = [None, GameStab(self)]
        self.is_dead = False
        self.frame = 0  # ! see game character frame count
        self.shield_count = 0

    def clear(self):
        self.hp = 16 * 4
        self.is_dead = False
        self.sx = 0
        self.set_direction(1)
        self.hurt_count = 30

    def set_ground(self, ground):
        self.ground_type = ground

    def on_ground(self):
        self.is_on_ground = True
        self.ground_type = g.GAME_MAP._collide['type']
        if self.state == 'crch' and self.ground_type == 'elevator':
            self.stand_up()
            self.state = 'walk'
        if self.state == 'fall':
            self.state = 'walk'

    def stab_id(self):
        return 1

    def is_stabbing(self):
        return self.skills[self.stab_id()].is_executing()

    def can_move(self):
        return not self.is_stabbing()

    def setup_box(self):
        self.hitbox = Rectangle(-11, 0, 16, 30)
        self.hurtbox = Rectangle(-11, 0, 16, 30)
        self.sword = Rectangle(5, 9, 12, 0)
        self.shield = Rectangle(5, 4, 4, 13)

    def set_direction(self, d):
        self.shield_direction(d)
        self.sword_direction(d)
        GameActor.set_direction(self, d)

    def shield_direction(self, d):
        if d != self.direction:
            self.shield.centerx = self.shield.centerx * -1

    def sword_direction(self, d):
        if d != self.direction:
            self.sword.centerx = self.sword.centerx * -1

    def start(self):
        self.x = (g.GAME_MAP.x + .5) * g.GAME_MAP.tile_width()
        self.y = (g.GAME_MAP.y + 1.) * g.GAME_MAP.tile_height()
        self.state = 'idle'
        self.setup_count()
        self.stand_up()

    def stab(self):
        Audio.play_sound_stab()
        self.sword.height = 5
        if self.state == 'walk':
            self.state = 'idle'
            self.sx = 0
        if self.state == 'crch':
            self.sx = 0
        if self.state == 'jump':
            self.stand_up()
        # if self.hp == self.life:
        # self.create_beam()

    def crouch(self):
        self.hitbox.y = 5
        self.hitbox.height = 27
        self.shield.y = 16
        self.sword.y = 19

    def stand_up(self):
        self.hitbox.y = 2
        self.hitbox.height = 30
        self.sword.y = 9
        self.shield.y = 0

    def update(self):
        GamePlayer.update(self)
        self.update_skills()
        self.shield_count -= 1
        self.frame -= 1
        if self.frame <= 0:
            self.frame = 18

    def update_skill(self):
        if self.skill:
            self.skill.update()
            if self.skill_is_terminate:
                self.skill = None

    def update_state(self):
        switcher = {
            'idle': self.state_standing,
            'walk': self.state_walking,
            'jump': self.state_jumping,
            'fall': self.state_falling,
            'crch': self.state_crouching,
            'hurt': self.state_hurting
        }
        switcher.get(self.state)()
        self.clamp_speed()

    def state_standing(self):
        if self.can_move():
            self.state_walking()

    def state_walking(self):
        self.move_by_input()
        self.stab_by_input()
        if not self.is_on_elevator():
            self.crouch_by_input()
            self.jump_by_input()

    def is_on_elevator(self):
        return self.ground_type == 'elevator'

    def state_jumping(self):
        self.move_by_input()
        self.update_jump()
        self.stab_by_input()

    def state_falling(self):
        self.move_by_input()
        self.stab_by_input()

    def state_crouching(self):
        if self.can_move():
            self.update_crouching()

    def state_hurting(self):
        self.update_hurting()

    def update_hurting(self):
        self.sx = 0.8 * self.hurt_dir
        self.jump_count -= 1
        self.hurt_count -= 1
        if self.jump_count >= 20:
            self.sy = -self.jump_count / 30 * 1
        if self.hurt_count <= 0:
            self.subject = None
            self.hurt_dir = 0
            if self.hp <= 0:
                self.is_dead = True
            else:
                self.state = 'idle'
                self.hitbox.height = 30

    def update_crouching(self):
        self.crouch_by_input()
        self.jump_by_input()
        self.stab_by_input()

    def move_by_input(self):
        d = self.get_input_direction()
        if d != 0:
            if self.is_on_ground:
                self.state = 'walk'
            self.sx += self.sx_with_direction(d)
            self.set_direction(d)
        else:
            self.back_to_idle()

    def stab_by_input(self):
        if not self.is_stabbing():
            if Input.is_key_triggered('x'):
                self.stab()
                self.setup_stab()

    def get_input_direction(self):
        return Input.dirX()

    def jump_by_input(self):
        if self.is_jump_triggered():
            self.crouch()
            self.ground_type = ''
            self.is_on_ground = False
            self.jump_count = self.jump_duration
            self.update_jump()
            self.state = 'jump'

    def crouch_by_input(self):
        if Input.is_key_pressed('down'):
            self.back_to_idle()
            self.crouch()
            self.state = 'crch'
        else:
            if self.state == 'crch':
                self.stand_up()
                self.state = 'idle'

    def is_jump_triggered(self):
        return Input.is_key_triggered('up') or Input.is_key_triggered('space')

    def update_skills(self):
        for skill in self.skills:
            if skill:
                skill.update()

    def setup_stab(self):
        self.skills[1].setup()

    def on_damage(self, subject=None):
        Audio.play_sound_hurt()
        self.stand_up()
        self.hitbox.height = 30
        self.ivcb_count = 60
        self.hurt_count = 30
        self.jump_count = 30
        self.state = 'hurt'
        self.subject = subject
        self.hurt_dir = self.damage_direction()

    def damage_direction(self):
        if not self.subject:
            return 0
        return -1 if self.x <= self.subject.x else 1

    def on_shield(self, subject=None):
        if self.shield_count < 0:
            Audio.play_sound_shield()
            self.shield_count = 30
        self.sx = .8 * subject.direction
