class GameSpell:
    def __init__(self, subject):
        self.x = 0
        self.y = 0
        self._width = 0
        self._height = 0
        self.set_subject(subject)

    def set_subject(self, subject):
        self.subject = subject

    def setup(self, data):
        self._duration = data['duration']
        self._type = data['type']

    def update(self):
        self._duration -= 1
        self.update_move()
        self.process()
        if self._duration == 0:
            self.is_terminate = True

    def update_move(self):
        self.update_sword()

    def update_masse():
        pass

    def update_sword(self):
        sword = self.subject.sword
        self.x = self.subject.x + sword.x
        self.y = self.subject.y + sword.y
        self.w = sword.width
        self.h = sword.height

    def update_beam(self):
        self.x += 1

    def process(self):
        pass

    def update_projectile(self):
        self.update_beam()
        self.update_mace()

    def execute_damage(self, target, damage):
        target.on_damage(value)

    def update_beam(self):
        self.x += 1

    def update_mace(self):
        self.y += 1
        self.x += 1
