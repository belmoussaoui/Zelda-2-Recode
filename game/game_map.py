from importlib import import_module

import game_objects as g
from core.pyxi import Rectangle
from game.game_bridge import GameBridge
from game.game_door import GameDoor
from game.game_elevator import GameElevator
from game.game_enemy import GameEnemy
from game.game_item import GameItem


class GameMap:
    def __init__(self):
        self.map_name = ''
        self.map_id = 0
        self.x = 0
        self.y = 0
        self.enemies = []
        self.objects = []
        self.platforms = []
        self.doors = []
        self.display_x = 0
        self.display_y = 0
        self.tiled = {}
        self.tiles_rect = []
        self.gravity = .5
        self.target = None
        self.elevator = None
        self._collide = None
        self._script = None
        self.is_transferring = False
        self.starting_position()
        self.can_scroll = True
        self._boss = None

    def clear(self):
        self.can_scroll = True

    def starting_position(self):
        self.map_name = 'northpalace'
        self.map_id = 1
        self.x = 23.5
        self.y = 9
        self.load_script(self.map_name)
        self.ending_position()

    def ending_position(self):
        self.map_name = 'northpalace'
        self.map_id = 2
        self.x = 7.5
        self.y = 12
        self.load_script(self.map_name)

    def setup(self, tiled):
        self.tiled = tiled
        self.layers = tiled['layers']
        self.data = self.layers[0]['data']
        self.tilesets = tiled['tilesets']
        self.tileset = self.tilesets[0]
        self.enemies = []
        self.doors = []
        self.platforms = []
        self.elevator = None
        self.objects = []
        self.enemies = []
        self.setup_objects()
        self.setup_collisions()

    def setup_objects(self):
        self.enemies = []
        self.objects = []
        objects = self.layers[-1].get('objects', [])
        for data in objects:
            x, y = data['x'], data['y']
            object_id = data['id']
            if data['type'] == 'enemy':
                self.add_enemy(x, y, object_id, data)
            elif data['type'] == 'elevator':
                self.add_elevator(x, y, object_id, data)
            elif data['type'] == 'item':
                self.add_item(x, y, object_id, data)
            elif data['type'] == 'door':
                self.add_door(x, y, object_id, data)
            elif data['type'] == 'bridge':
                self.add_bridge(x, y, object_id, data)
            else:
                pass

    def add_enemy(self, x, y, object_id, data):
        enemy_id = data['properties'][0]['value']
        self.enemies.append(GameEnemy.create_enemy(x, y, enemy_id, data))

    def add_elevator(self, x, y, object_id, data):
        self.elevator = GameElevator(x, y, object_id)

    def add_item(self, x, y, object_id, data):
        item_id = data['properties'][0]['value']
        self.objects.append(GameItem(x, y, object_id, item_id))

    def add_door(self, x, y, object_id, data):
        self.doors.append(GameDoor(x, y, object_id))

    def add_bridge(self, x, y, object_id, data):
        self.platforms.append(GameBridge(x, y, object_id))

    def setup_collisions(self):
        self.tiles_rect = []
        tiles = self.tileset.get('tiles', [])
        for tile_data in tiles:
            self.find_tiles_rect(tile_data)

    def find_tiles_rect(self, tile_data):
        tile_collision = tile_data['id'] + 1
        for x in range(self.map_width()):
            for y in range(self.map_height()):
                tile = self.tile(x, y)
                if tile == tile_collision:
                    self.create_collision(x, y, tile_data)

    def create_collision(self, x, y, tile):
        tw = self.tile_width()
        th = self.tile_height()
        tile_type = tile.get('type', False)
        if tile_type:
            rect = Rectangle(x * tw, y * th, tw, th)
            self.tiles_rect.append({'rect': rect, 'type': tile_type})

    def tile_width(self):
        return self.tiled.get('tilewidth', 1)

    def tile_height(self):
        return self.tiled.get('tileheight', 1)

    def width(self):
        return self.map_width() * self.tile_width()

    def height(self):
        return self.map_height() * self.tile_height()

    def map_width(self):
        return self.tiled['width']

    def map_height(self):
        return self.tiled['height']

    def tile(self, x, y, z=0):
        return self.data[(z * self.map_height() + y) * self.map_width() + x]

    def canvas_to_map_x(self, x):
        return int(x / self.tile_width())

    def canvas_to_map_y(self, y):
        return int(y / self.tile_height())

    def is_valid(self, x):
        if not self.can_scroll:
            return self.display_x <= x <= self.display_x + 256
        return 0 <= x <= self.width()

    def is_passable(self, i_rect):
        self._collide = None
        if g.GAME_PLAYER.direction == -1:
            platforms = self.platforms
        else:
            platforms = self.platforms[::-1]
        for platform in platforms:
            if platform.rect.colliderect(i_rect):
                self._collide = {'rect': platform, 'type': 'platform'}
                return False
        for rect in self.tiles_rect:
            if rect['rect'].colliderect(i_rect):
                self._collide = rect
                return False
        for door in self.doors:
            if door.rect.colliderect(i_rect):
                self._collide = {'rect': door, 'type': 'door'}
                return False
        return True

    def round_x_with_map(self, d, is_player=False):
        rect = self._collide['rect']
        if self._collide.get('type', False) == 'door' and is_player:
            rect.on_touch()
        if d > 0:
            return rect.left
        else:
            return rect.right

    def round_y_with_map(self, d, is_player=True):
        rect = self._collide['rect']
        if self._collide.get('type', False) == 'platform' and is_player:
            rect.on_touch()
        if d > 0:
            return rect.top
        else:
            return rect.bottom

    def round_x_with_bounds(self, x):
        if not self.can_scroll:
            return self.display_x if x < self.display_x else self.display_x + 256
        return 0 if x < 0 else self.width()

    def scroll_right(self, distance):
        if self.display_x + distance < self.width() - 16 * 16:
            self.display_x += distance
        else:
            self.display_x = self.width() - 16 * 16

    def scroll_by_position(self, x):
        distance = min(abs(x - self.display_x - self.center_x()), 1.6)
        if x - self.display_x - self.center_x() < 0:
            distance = -distance
        self.scroll_horizontally(distance)

    def scroll_left(self, distance):
        if self.display_x + distance >= 0:
            self.display_x += distance
        else:
            self.display_x = 0

    def scroll_horizontally(self, distance):
        d = distance
        self.scroll_right(d) if d > 0 else self.scroll_left(d)

    def update(self):
        self.update_scroll()
        self.update_object()
        self.update_enemy()
        self.update_script()

    def update_scroll(self):
        if self.target and self.can_scroll:
            self.scroll_by_position(self.target.x)

    def update_object(self):
        for game_object in self.objects:
            game_object.update()
        if self.elevator:
            self.elevator.update()
        for door in self.doors:
            door.update()
        for platform in self.platforms:
            platform.update()

    def update_enemy(self):
        for enemy in self.enemies:
            if enemy.is_active():
                enemy.update()

    def update_script(self):
        method = 'map_{:02d}'.format(self.map_id)
        self.interpret_script(method)

    def deactivate_scroll(self):
        self.can_scroll = False

    def activate_scroll(self):
        self.can_scroll = True

    def adjust_x(self, x):
        return x - self.display_x

    def adjust_y(self, y):
        return y - self.display_y

    @staticmethod
    def center_x():
        return 256 / 2

    def transfer(self, map_name, map_id, x, y):
        self.is_transferring = True
        self.map_name = map_name
        self.map_id = map_id
        self.x = x
        self.y = y
        self.load_script(map_name)

    def start(self):
        self.display_x = min(self.width() - 256, max(0, self.x * 16 - (16 * 7.5)))

    def load_script(self, script='northpalace'):
        self._script = import_module('script.' + script)

    def interpret_script(self, method='map_01'):
        try:
            getattr(self._script, method)()
        except:
            pass

    def get_hit_collisions(self, box):
        self._collide = []
        for tile in self.tiles_rect:
            rect = tile['rect']
            if rect.colliderect(box):
                self._collide.append(tile)
        return self._collide

    def get_obj_collisions(self, box):
        self._collide = []
        for tile in self.objects:
            rect = tile.rect
            if rect.colliderect(box) and tile.active:
                self._collide.append(tile)
        return self._collide

    def get_hit_targets(self, box):
        self._collide = []
        for enemy in self.enemies:
            rect = enemy.rect
            if rect.colliderect(box):
                self._collide.append(enemy)
        if g.GAME_PLAYER.rect.colliderect(box):
            self._collide.append(g.GAME_PLAYER)
        return self._collide

    def get_hurt_targets(self, box):
        self._collide = []
        for enemy in self.enemies:
            rect = enemy.rect
            if rect.colliderect(box):
                self._collide.append(enemy)
        if g.GAME_PLAYER.rect.colliderect(box):
            self._collide.append(g.GAME_PLAYER)
        return self._collide

    def is_collided_with_characters(self, i_rect):
        return False

    def round_x_with_characters(self, d):
        rect = self._collide['rect']
        if d > 0:
            return rect.left
        else:
            return rect.right

    def round_y_with_characters(self, d):
        rect = self._collide['rect']
        if d > 0:
            return rect.top
        else:
            return rect.bottom

    def is_collided_with_objects(self, i_rect):
        if self.elevator:
            if self.elevator.rect.colliderect(i_rect):
                self._collide = {'rect': self.elevator, 'type': 'elevator'}
                return True
        return False

    def set_boss(self, boss):
        self._boss = boss

    def boss(self):
        return self._boss
