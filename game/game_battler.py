from game.game_actor import GameActor


class GameBattler(GameActor):
    def __init__(self):
        GameActor.__init__(self)
        self.hp = 0
        self.mp = 0
        self.attack = 0
        self.life = 0
        self.power = 0
        self._spells = []
        self.skills = []
        self.anims = []
        self.effect = ''

    def gain_hp(self, value):
        self.hp += value
        self.hp = max(min(self.hp, self.mhp), 0)

    def perform_collapse(self):
        self.set_effect('collapse')

    def clear_anim(self):
        self.anims = []

    def is_anim(self):
        return len(self.anims) > 0

    def start_anim(self, anim_id):
        self.anims.append(anim_id)

    def clear_effect(self):
        self.effect = ''

    def set_effect(self, effect):
        self.effect = effect

    def is_effect(self):
        return self.effect != ''

    def on_damage(self, subject=None):
        self.ivcb_count = 15
        self.hurt_count = 30
        self.state = 'hurt'

    def is_vunerable(self):
        return self.ivcb_count < 0

    def set_hp(self, hp):
        self.hp = hp
        if self.hp <= 0:
            self.on_dead()

    def set_mp(self, mp):
        self.mp = mp

    def die(self):
        self.set_hp(0)

    def on_dead(self):
        pass

    def is_alive(self):
        return self.hp > 0

    def is_shield(self):
        return self.special_flag()

    def special_flag(self):
        return False

    def update(self):
        GameActor.update(self)
        if self.ivcb_count >= 0:
            self.ivcb_count -= 1

    def recover_hp(self, value):
        self.hp += value
