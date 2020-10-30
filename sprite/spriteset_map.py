import game_objects as g
from core.pyxi import Display
from core.pyxi import Tilemap
from game.game_bridge import SpriteBridge
from game.game_door import SpriteDoor
from game.game_elevator import SpriteElevator
from sprite.sprite_enemy import SpriteEnemy
from sprite.sprite_item import SpriteItem
from sprite.spriteset_base import SpritesetBase


class SpritesetMap(SpritesetBase):
    def __init__(self):
        self._tilemap = None
        SpritesetBase.__init__(self)
        # self.draw_collide()

    def create_lower_layer(self):
        SpritesetBase.create_lower_layer(self)
        self.create_tilemap()
        self.create_enemies()
        self.create_objects()

    def create_enemies(self):
        self._enemy_sprites = []
        for enemy in g.GAME_MAP.enemies:
            sprite = SpriteEnemy.create_enemy(enemy)
            self._enemy_sprites.append(sprite)
        for enemy in self._enemy_sprites:
            self._tilemap.add(enemy)

    def create_objects(self):
        self._object_sprites = []
        for game_object in g.GAME_MAP.objects:
            sprite = SpriteItem(game_object)
            self._object_sprites.append(sprite)
        if g.GAME_MAP.elevator:
            sprite = SpriteElevator(g.GAME_MAP.elevator)
            self._object_sprites.append(sprite)
        for game_door in g.GAME_MAP.doors:
            sprite = SpriteDoor(game_door)
            self._object_sprites.append(sprite)
        for platform in g.GAME_MAP.platforms:
            sprite = SpriteBridge(platform)
            self._object_sprites.append(sprite)
        for game_object in self._object_sprites:
            self._tilemap.add(game_object)

    def create_upper_layer(self):
        SpritesetBase.create_upper_layer(self)

    def create_tilemap(self):
        self._tilemap = Tilemap()
        self._tilemap.setup(g.GAME_MAP.tiled)

    def update(self):
        SpritesetBase.update(self)
        self.update_tilemap()

    def update_position(self):
        pass

    def update_tilemap(self):
        self._tilemap._lower_layer.x = -round(g.GAME_MAP.display_x)
        self._tilemap._upper_layer.x = -round(g.GAME_MAP.display_x)
        # self._tilemap.y = Game.map.displayY() * gGame.map.tile_height();

    def draw_collide(self):
        for tile in g.GAME_MAP.tiles_rect:
            rect = tile['rect']
            x = rect.x * Display.scale_x()
            y = rect.y * Display.scale_y()
            w = rect.width * Display.scale_x()
            h = rect.height * Display.scale_y()
            self._tilemap._lower_layer.image.draw_collide(x, y, w, h)

    def is_busy(self):
        for sprite in self._enemy_sprites:
            if sprite.is_busy():
                return True
        return False
