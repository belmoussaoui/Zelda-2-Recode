import game_objects as g
from sprite.sprite_character import SpriteCharacter


class SpritePlayer(SpriteCharacter):
    def __init__(self):
        self._layer = 1
        SpriteCharacter.__init__(self, 39, 40, g.GAME_PLAYER)
        self._frame_count = 0

    def _create_image(self):
        self.load_spritesheet('player/link.png')
        self.set_frame(39 * 3 + 3, 0, 39, 40)

    def update(self):
        SpriteCharacter.update(self)
        #self.update_collide()

    def update_frame(self):
        self._frame_count = g.GAME_PLAYER.frame
        f = self._frame_count // 6
        d = self.character_direction()
        sx = 1 if d == 1 else -1
        if (g.GAME_PLAYER.state == 'walk'):
            p = 4 if d == 1 else 3
            p = p + f * sx * 1
            self.set_frame(39 * p + 1 * p, 0, 39, 40)
        elif g.GAME_PLAYER.state == 'jump':
            p = 6 if d == 1 else 1
            self.set_frame(39 * p + 1 * p, 40, 39, 40)
            if g.GAME_PLAYER.is_stabbing():
                p = 5 if d == 1 else 2
                y = 40
                self.set_frame(39 * p + 1 * p, y, 39, 40)
            else:
                self.set_frame(39 * p + 1 * p, 40, 39, 40)
        elif g.GAME_PLAYER.state == 'fall':
            p = 6 if d == 1 else 1
            if g.GAME_PLAYER.is_stabbing():
                p = 5 if d == 1 else 2
                y = 40
                self.set_frame(39 * p + 1 * p, y, 39, 40)
            else:
                self.set_frame(39 * p + 1 * p, 0, 39, 40)
        elif g.GAME_PLAYER.state == 'crch':
            p = 6 if d == 1 else 1
            if g.GAME_PLAYER.is_stabbing():
                p = 7 if d == 1 else 0
            self.set_frame(39 * p + 1 * p, 40, 39, 40)
        elif g.GAME_PLAYER.state == 'hurt':
            p = 6 if d == 1 else 1
            self.set_frame(39 * p + 1 * p, 40 * 9, 39, 40)
        else:
            p = 4 if d == 1 else 3
            y = 0
            if g.GAME_PLAYER.is_stabbing():
                p = 5 if d == 1 else 2
                y = 40
            self.set_frame(39 * p + 1 * p, y, 39, 40)

    def character_direction(self):
        return g.GAME_PLAYER.direction

    def update_collide(self):
        rect = g.GAME_PLAYER.hitbox
        x = self.width / 2 + rect.x
        y = rect.y
        w = rect.width
        h = rect.height
        self.image.draw_collide(x, y, w, h)
        cx = self.width / 2 + rect.centerx
        rect = g.GAME_PLAYER.sword
        x = cx + rect.x
        y = rect.y
        w = rect.width
        h = rect.height
        self.image.draw_collide(x, y, w, h)
