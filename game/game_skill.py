import game_objects as g
from core.pyxi import Rectangle
from game.game_action import GameAction


class GameSkill:
    def __init__(self, subject):
        self.skill_id = 0
        self.type = 0  # 0: normal, 1: ignore shield
        self.name = ''
        self.subject = None
        self.box = Rectangle(0, 0, 0, 0)
        self.set_subject(subject)

    def set_subject(self, subject):
        self.subject = subject

    def is_stab(self):
        return self.skill_id == 1

    def is_shield(self):
        return self.skill_id == 2

    def is_down_thrust(self):
        return self.skill_id == 3

    def is_up_thrust(self):
        return self.skill_id == 4

    @property
    def x(self):
        return self.box.x

    @property
    def y(self):
        return self.box.y

    @x.setter
    def x(self, x):
        self.box.x = x

    @y.setter
    def y(self, y):
        self.box.y = y

    @property
    def w(self):
        return self.box.width

    @property
    def h(self):
        return self.box.height

    @x.setter
    def h(self, h):
        self.box.height = h

    @y.setter
    def w(self, w):
        self.box.width = w

    def _create_self_for_hit(self):
        rect = self.subject.rect
        self.x = rect.x
        self.y = rect.y
        self.w = rect.width
        self.h = rect.height

    def _create_sword_for_hit(self):
        x = self.subject.x
        y = self.subject.top
        s = self.subject.sword
        self.x = x + s.x
        self.y = y + s.y
        self.w = s.width
        self.h = s.height

    def update(self):
        pass

    def update_hit(self):
        pass

    def is_executing(self):
        return False


class GameStab(GameSkill):
    def __init__(self, subject):
        GameSkill.__init__(self, subject)
        self.skill_id = 1
        self.duration = 12
        self.stab_count = 0

    def setup(self):
        self.stab_count = self.duration

    def update(self):
        self.stab_count -= 1
        if self.stab_count > 0:
            self.apply()

    def apply(self):
        self._create_sword_for_hit()
        self.create_actions()

    def create_actions(self):
        targets = g.GAME_MAP.get_hit_collisions(self.box)
        if len(targets) > 0:
            self.on_collision()
        targets = g.GAME_MAP.get_obj_collisions(self.box)
        for target in targets:
            target.on_damage(self.subject)
        targets = g.GAME_MAP.get_hurt_targets(self.box)
        for target in targets:
            if target != self.subject and target.is_vunerable():
                action = GameAction(self.subject, target, self)
                action.process()

    def is_executing(self):
        return self.stab_count > 0

    def on_collision(self):
        self.subject.x -= .5 * self.subject.direction


class GameTouch(GameSkill):
    def __init__(self, subject):
        GameSkill.__init__(self, subject)
        self.skill_id = 2
        self.type = 1

    def update(self):
        self.apply()

    def apply(self):
        self._create_self_for_hit()
        self.create_actions()

    def create_actions(self):
        targets = g.GAME_MAP.get_hit_collisions(self.box)
        if len(targets) > 0:
            self.on_collision()
        targets = g.GAME_MAP.get_hit_targets(self.box)
        for target in targets:
            if not self.subject.is_enemy() or not target.is_enemy():
                if target != self.subject and target.is_vunerable():
                    action = GameAction(self.subject, target, self)
                    action.process()

    def is_executing(self):
        return self.stab_count > 0

    def on_collision(self):
        pass
