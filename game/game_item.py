import game_objects as g
from core.pyxi import Rectangle
from game.game_object import GameObject


class GameItem(GameObject):
    EFFECT_GAIN_MP = 1
    EFFECT_GAIN_EXP = 2
    EFFECT_OBTAIN_KEY = 3
    EFFECT_OBTAIN_ITEM = 4

    def __init__(self, x, y, object_id, item_id):
        GameObject.__init__(self, x + 8, y, object_id)
        self.item_id = item_id
        self.subject = None
        self.hitbox.x = -4
        self.hitbox.height = 16
        self.hitbox.width = 8
        self.active = True
        self.exp = 0
        self.object_id = object_id
        key = str(g.GAME_MAP.map_id) + str(self.object_id)
        if self.is_switch():
            self.active = False

    def on_damage(self, subject):
        self.subject = subject
        item = GameItem.item(self.item_id)
        self.apply_item_effects(item)
        self.deactivate()

    def update(self):
        self.sy = 1.6
        self.execute_move_y()

    def execute_move_y(self):
        if self.can_pass_y():
            self.y += self.sy

    def can_pass_y(self):
        if self.is_collided_with_map_y():
            return False
        return True

    def is_collided_with_map_y(self):
        rect = self._create_rect_for_collision_y()
        if not g.GAME_MAP.is_passable(rect):
            y = self.round_y_with_map()
            return True
        return False

    def round_y_with_map(self):
        return g.GAME_MAP.round_y_with_map(self.sy, False)

    def _create_rect_for_collision_y(self):
        # to fix when fall with pixel perfect to right
        x = round(self.x - self.center_x())
        y = self._round_rect_y()
        w = self.hitbox.width
        h = self.hitbox.height
        y -= h
        return Rectangle(x, y, w, h)

    def _round_rect_y(self):
        return round(self.y + self.sy + self.ceil_and_floor(self.sy))

    def ceil_and_floor(self, speed):
        # rectangle can't have float numbers
        # it's necessary to round with sx or sy
        return .5 * (1 if speed > 0 else -1)

    @staticmethod
    def item(item_id):
        data = {
            1: {'name': 'Magic Jar Blue', 'effects': [{'code': 1, 'value': 16}]},
            2: {'name': 'Magic Jar Red', 'effects': [{'code': 1, 'value': 128}]},
            3: {'name': 'Treasure bag', 'effects': [{'code': 2, 'value': 50}]},
            4: {'name': 'Key', 'effects': [{'code': 3, 'value': 1}]},
            5: {'name': 'Candle', 'effects': [{'code': 4, 'value': 1}]}
        }
        return data.get(item_id)

    def apply_item_effects(self, item):
        effects = item['effects']
        for effect in effects:
            self.apply_item_effect(effect)

    def apply_item_effect(self, effect):
        code = effect['code']
        value = effect['value']
        switcher = {
            1: self.recover_mp,
            2: self.gain_exp,
            3: self.obtain_key,
            4: self.obtain_item
        }
        switcher.get(code)(value)

    def recover_mp(self, value):
        self.subject.gain_mp(value)

    def gain_exp(self, value):
        self.exp = value
        self.subject.gain_exp(value)

    def obtain_key(self, value):
        self.subject.add_key()

    def obtain_item(self, item_id):
        self.subject.add_item(item_id)

    def deactivate(self):
        self.active = False
        self.activate_switch()
