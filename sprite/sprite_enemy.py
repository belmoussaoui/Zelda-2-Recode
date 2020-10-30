from sprite.sprite_character import SpriteCharacter
from sprite.sprite_exp import SpriteExp
from sprite.sprite_base import SpriteBase
from core.pyxi import Audio


class SpriteEnemy(SpriteCharacter):
    def __init__(self, width, height, enemy):
        SpriteCharacter.__init__(self, width, height, enemy)
        self._create_image()
        self.anim_count = 0
        self.effect = ''
        self.effect_duration = 0
        self.exp_request = False
        self.alpha = 255
        self.exp = None
        self.tone = False
        self.hide = False
        if self.character.is_switch():
            self.hide = True

    @staticmethod
    def create_enemy(enemy):
        switcher = {
            1: SpriteBot,
            2: SpriteStalfos,
            3: SpriteKobold,
            4: SpriteBubble,
            5: SpriteIronknuckle,
            6: SpriteBubble,
            7: SpriteHorsehead
        }
        SpriteEnemy = switcher.get(enemy.enemy_id)
        return SpriteEnemy(enemy)

    def collapse_anim_id(self):
        return 1

    def boss_collapse_anim_id(self):
        return 3

    def _create_image(self):
        pass

    def setup_effect(self):
        self.start_effect()
        self.character.clear_effect()

    def start_effect(self):
        self.effect = self.character.effect
        switch = {
            'collapse': self.start_collapse,
            'boss_collapse': self.start_boss_collapse
        }
        method = switch.get(self.effect)
        method()

    def start_collapse(self):
        self.start_anim(self.collapse_anim_id(), self.character)
        self.effect_duration = 12
        if self.character.exp > 0:
            self.exp_request = True

    def start_boss_collapse(self):
        self.effect_duration = 120

    def update_effect(self):
        if self.character.is_effect():
            self.setup_effect()
        if self.effect_duration > 0:
            self.effect_duration -= 1
            switch = {
                'collapse': self.update_collapse,
                'boss_collapse': self.update_boss_collapse
            }
            method = switch.get(self.effect)
            method()
            if self.effect_duration == 0:
                self.effect = ''

    def update_collapse(self):
        if self.effect_duration == 0:
            self.alpha = 0

    def update_boss_collapse(self):
        if self.effect_duration % 9 == 3:
            self.image.blink(240)
        if self.effect_duration % 9 == 6:
            self.image.blink(0)
        if self.effect_duration % 9 == 0:
            self.image.blink(120)
        if self.effect_duration == 0:
            Audio.play_sound_boss_collapse()
            for i in range(16):
                self.start_anim(self.boss_collapse_anim_id(), self.character, i * 8)
            self.alpha = 0
            self.exp_request = True

    def update(self):
        SpriteCharacter.update(self)
        self.update_effect()
        self.update_exp()
        self.update_hue()
        if self.hide:
            self.image.set_alpha(0)

    def update_hue(self):
        if (self.character.is_alive()):
            if (self.character.hurt_count > 0):
                if (self.character.hurt_count % 8 == 4):
                    self.image.blink(240)
                if (self.character.hurt_count % 8 == 0):
                    self.image.blink(0)
                if (self.character.hurt_count == 1):
                    self.image = self._base_image

    def update_exp(self):
        if self.exp_request:
            if not self.is_anim_busy():
                self.start_exp()
                self.exp_request = False

    def start_exp(self):
        sprite = SpriteExp()
        sprite.setup(self.character)
        self.exp = sprite
        self.add_sprite(sprite)

    def is_exp_busy(self):
        if self.exp != None:
            return self.exp.is_busy()
        return self.exp_request

    def is_busy(self):
        return self.effect != '' or self.is_anim_busy() or self.is_exp_busy()


class SpriteKobold(SpriteEnemy):
    def __init__(self, bot):
        SpriteEnemy.__init__(self, 16, 32, bot)
        self.direction = -1

    def _create_image(self):
        self.load_spritesheet('enemies/enemies1.png')
        self.set_frame(246, 448, 16, 32)

    def update_frame(self):
        if self.character.is_alive():
            self.alpha = 255
        self.anim_count += 1
        if self.anim_count == 0:
            self.set_frame(246, 448, 16, 32)
            self.direction = -1
        if self.anim_count == 32:
            self.set_frame(246 + 16 + 1, 448, 16, 32)
            self.direction = -1
        if self.character.direction != self.direction:
            self.direction *= -1
            self.image.flip()
        if self.anim_count == 64:
            self.anim_count = -1
        self.image.set_alpha(self.alpha)


class SpriteBot(SpriteEnemy):
    def __init__(self, bot):
        SpriteEnemy.__init__(self, 16, 16, bot)

    def _create_image(self):
        self.load_spritesheet('enemies/enemies1.png')
        self.set_frame(177, 11, 16, 16)

    def update_frame(self):
        self.anim_count += 1
        if self.anim_count == 1:
            self.set_frame(177, 11, 16, 16)
        if self.anim_count == 16:
            self.set_frame(195, 11, 16, 16)
        if self.anim_count == 32:
            self.anim_count = 0
        self.image.set_alpha(self.alpha)


class SpriteStalfos(SpriteEnemy):
    def __init__(self, stalfos):
        self.weapon = SpriteBase(16, 16)
        SpriteEnemy.__init__(self, 16, 32, stalfos)
        self.direction = 1

    def _create_image(self):
        self.load_spritesheet('enemies/enemies2.gif')
        self.set_frame(300, 454, 16, 32)
        self.weapon.load_spritesheet('enemies/enemies2.gif')
        self.set_frame(410, 454, 32, 32)

    def update(self):
        self.update_weapon()
        SpriteEnemy.update(self)

    def update_weapon(self):
        self.add_sprite(self.weapon)
        if self.character.is_stabbing():
            self.weapon.set_frame(394+16, 454, 16, 16)
            self.weapon.x = self.character.screen_x()
            self.weapon.y = self.character.screen_y()
            self.weapon.image.set_alpha(255)
        else:
            self.weapon.image.set_alpha(0)
        if self.direction == -1:
            self.weapon.x -= 24
        else:
            self.weapon.x += 8

    def update_frame(self):
        self.anim_count += 1
        if self.anim_count < 32:
            self.set_frame(300, 454, 16, 32)
            self.direction = 1
        if self.anim_count >= 32:
            self.set_frame(324, 454, 16, 32)
            self.direction = 1
        if self.character.is_stabbing():
            self.set_frame(394, 454, 16, 32)
            self.direction = 1
        if self.anim_count == 64:
            self.anim_count = -1
        self.image.set_alpha(self.alpha)
        if self.character.direction != self.direction:
            self.direction *= -1
            self.image.flip()
            self.weapon.image.flip()


class SpriteBubble(SpriteEnemy):
    def __init__(self, bubble):
        SpriteEnemy.__init__(self, 16, 16, bubble)
        self.color = (1, .01, .2, 1)

    def _create_image(self):
        self.load_spritesheet('enemies/enemies1.png')
        self.set_frame(264, 12, 16, 16)

    def update_frame(self):
        self.anim_count += 1
        if self.anim_count == 0:
            self.set_frame(230, 12, 16, 16)
        if self.anim_count == 16:
            self.set_frame(247, 12, 16, 16)
        if self.anim_count == 32:
            self.set_frame(264, 12, 16, 16)
        if self.anim_count == 48:
            self.set_frame(281, 12, 16, 16)
        if self.anim_count == 64:
            self.anim_count = -1
        self.image.set_alpha(self.alpha)


class SpriteIronknuckle(SpriteEnemy):
    def __init__(self, ironknuckle):
        self.weapon = SpriteBase(16, 16)
        SpriteEnemy.__init__(self, 16, 32, ironknuckle)
        self.direction = -1

    def _create_image(self):
        self.load_spritesheet('enemies/enemies1.png')
        self.set_frame(1, 106, 16, 32)
        self.weapon.load_spritesheet('enemies/enemies1.png')
        self.weapon.set_frame(69, 106, 16, 16)

    def update(self):
        SpriteEnemy.update(self)
        self.add_sprite(self.weapon)
        self.update_anim()
        self.update_weapon()
        self.update_direction()
        self.update_collide()

    def update_weapon(self):
        if self.character.is_stabbing():
            self.weapon.image.set_alpha(255)
            self.weapon.x = self.character.screen_x() - 24
            self.weapon.set_frame(69, 106, 16, 16)
            if self.character.direction == 1:
                self.weapon.x += 32
        elif self.character.is_post_stabbing():
            self.weapon.image.set_alpha(255)
            self.weapon.x = self.character.screen_x()
            self.weapon.set_frame(86, 106, 16, 16)
            if self.character.direction == 1:
                self.weapon.x -= 20
            if self.character.is_stabbing_down():
                self.weapon.x += 8
                if self.character.direction == 1:
                    self.weapon.x -= 12
                self.weapon.set_frame(103, 106, 8, 16)

        else:
            self.weapon.image.set_alpha(0)
        if self.character.is_stabbing_down():
            self.weapon.y = self.character.screen_y() + 8
            if self.character.is_post_stabbing():
                self.weapon.y += 8
        else:
            self.weapon.y = self.character.screen_y()
        if self.alpha == 0:
            self.weapon.image.set_alpha(0)

    def update_frame(self):
        self.image.clear()
        self.update_block1()
        self.update_block2()
        self.image.set_alpha(self.alpha)

    def update_anim(self):
        self.anim_count += 1
        if self.anim_count == 32:
            self.anim_count = -1

    def update_direction(self):
        if self.character.direction != self.direction:
            self.direction *= -1
            self.image.flip()
            self.weapon.image.flip()

    def set_frame(self, x, y, width, height, pos_x=0, pos_y=0, clear=True):
        self.direction = -1
        SpriteCharacter.set_frame(self, x, y, width, height, pos_x, pos_y, clear)

    def update_block1(self):
        if self.character.is_shield_up():
            self.update_block1_shield_up()
        else:
            self.update_block1_shield_down()

    def update_block1_shield_up(self):
        if self.character.is_stabbing_up():
            self.set_frame(96-16, 139, 32, 16, 0, 0, False)
        else:
            self.set_frame(1, 106, 16, 16, 0, 0, False)

    def update_block1_shield_down(self):
        if self.character.is_stabbing_up():
            self.set_frame(96-16, 205, 32, 16, 0, 0, False)
        else:
            self.set_frame(35, 106, 16, 16, 0, 0, False)

    def update_block2(self):
        if self.character.is_shield_up():
            self.update_block2_shield_up()
        else:
            self.update_block2_shield_down()

    def update_block2_shield_up(self):
        if self.anim_count < 16:
            self.set_frame(1, 122, 16, 16, 0, 16, False)
        else:
            self.set_frame(18, 122, 16, 16, 0, 16, False)

    def update_block2_shield_down(self):
        if self.anim_count < 16:
            self.set_frame(35, 122, 16, 16, 0, 16, False)
        else:
            self.set_frame(52, 122, 16, 16, 0, 16, False)

    def update_collide(self):
        rect = self.character.hitbox
        x = self.width / 2 + rect.x
        y = rect.y
        w = rect.width
        h = rect.height
        self.image.draw_collide(x, y, w, h)
        cx = self.width / 2 + rect.centerx
        rect = self.character.sword
        x = cx + rect.x
        y = rect.y
        w = rect.width
        h = rect.height
        self.image.draw_collide(x, y, w, h)


class SpriteHorsehead(SpriteEnemy):
    def __init__(self, horsehead):
        self.weapon = SpriteBase(16, 16)
        SpriteEnemy.__init__(self, 16, 48, horsehead)

    def _create_image(self):
        self.load_spritesheet('enemies/boss.png')
        self.set_frame(1, 11, 16, 48)
        self.weapon.load_spritesheet('enemies/boss.png')
        self.weapon.set_frame(61, 60, 16, 16)

    def update(self):
        self.add_sprite(self.weapon)
        SpriteEnemy.update(self)
        self.update_anim()
        self.update_weapon()

    def update_weapon(self):
        self.weapon.set_frame(61, 60, 16, 16)
        self.weapon.x = self.character.screen_x() - 24
        self.weapon.y = self.character.screen_y() + 16
        if self.character.is_stabbing() or self.character.is_post_stabbing():
            self.weapon.image.set_alpha(255)
        else:
            self.weapon.image.set_alpha(0)
        if self.character.is_post_stabbing():
            self.weapon.set_frame(51, 60, 16, 16, 8)
            self.weapon.x += 24
        if self.alpha == 0:
            self.weapon.image.set_alpha(0)

    def update_frame(self):
        if self.anim_count < 16:
            self.set_frame(1, 11, 16, 48)
        else:
            self.set_frame(18, 11, 16, 48)
        if self.character.state == 'wait':
            self.set_frame(1, 11, 16, 48)
        if self.character.is_stabbing():
            self.set_frame(101, 11, 16, 48)
        if self.character.is_post_stabbing():
            self.set_frame(35, 11, 16, 48)
        self.image.set_alpha(self.alpha)

    def update_anim(self):
        self.anim_count += 1
        if self.anim_count == 32:
            self.anim_count = -1