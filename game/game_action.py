class GameAction:
    def __init__(self, subject, target, item):
        self.subject = subject
        self.target = target
        self.item = item

    def process(self):
        self.execute_damage()

    def execute_damage(self):
        value = self.calc_damage_value()
        if not self.hit_shield():
            self.target.on_damage(self.subject)
            self.target.set_hp(self.target.hp - value)
        else:
            self.target.on_shield(self.subject)
        if self.subject.is_enemy() and self.target.is_player():
            self.target.gain_exp(self.calc_damage_exp_value())
            self.target.gain_mp(self.calc_damage_mp_value())
        self.execute_dead()

    def calc_damage_exp_value(self):
        value = -self.subject.damage_exp
        return value

    def execute_dead(self):
        if self.target.hp <= 0:
            if self.subject.is_player():
                self.subject.gain_exp(self.target.exp)
                self.target.perform_collapse()

    def hit_shield(self):
        if self.target.has_shield() and self.item.type != 1:
            return self.target.hit_shield(self.item.box)
        else:
            return False

    def calc_damage_value(self):
        value = self.subject.power
        return value

    def calc_damage_mp_value(self):
        value = -self.subject.damage_mp
        return value
