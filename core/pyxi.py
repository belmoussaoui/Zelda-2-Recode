import math
import os

import pygame
from scene.scene_manager import SceneManager


class Display:
    title = 'Zelda II: The Adventure of Link'
    fps = 60
    width = 800#768  # 766
    height = 600#720  # 600
    screen = None
    screen_size = (width, height)
    width_nes = 256
    height_nes = 240
    screen_size_nes = (width_nes, height_nes)
    clock = None
    render = None

    @classmethod
    def init(cls, scene):
        pygame.init()
        pygame.display.set_caption(cls.title)
        pygame.display.set_mode(cls.screen_size, pygame.RESIZABLE, 32)
        cls.screen = pygame.display.get_surface()
        cls.render = pygame.Surface(cls.screen_size_nes)
        SceneManager.run(scene, cls.render)

    @classmethod
    def game_loop(cls):
        cls.clock = pygame.time.Clock()
        accumulator = 0.0
        delta_time = 1.0 / 60
        while True:
            new_time = cls.clock.tick(cls.fps) / 1000
            accumulator += new_time
            SceneManager.draw()
            cls.render_screen()
            pygame.display.update()
            cls.update_caption()
            while accumulator >= delta_time:
                SceneManager.update()
                accumulator -= delta_time

    @classmethod
    def update_caption(cls):
        fps = cls.clock.get_fps()
        pygame.display.set_caption('{} - {:.2f} FPS'.format(cls.title, fps))

    @classmethod
    def render_screen(cls):
        cls.screen.blit(pygame.transform.scale(cls.render, cls.screen.get_size()), (0, 0))

    @classmethod
    def resize_screen(cls, event):
        cls.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


class Audio:
    music = ''
    music_path = 'audio/music/'
    sound_path = 'audio/sound/'
    sound = None

    @classmethod
    def play_bgm(cls, filename, type=-1):
        pygame.mixer.music.load(cls.music_path + filename)
        pygame.mixer.music.play(type)

    @classmethod
    def play_sound(cls, filename):
        cls.sound = pygame.mixer.Sound(cls.sound_path + filename)
        cls.sound.play()

    @classmethod
    def play_music_title(cls):
        cls.music = 'title'
        cls.play_bgm('01_-_Legend_of_Zelda_2_-_NES_-_Title_BGM.ogg', 0)

    @classmethod
    def play_music_ground(cls):
        if cls.music != 'ground':
            cls.play_bgm('02_-_Legend_of_Zelda_2_-_NES_-_Above_Ground_BGM.ogg')
            cls.music = 'ground'

    @classmethod
    def play_music_temple(cls):
        if cls.music != 'temple':
            cls.play_bgm('07_-_Legend_of_Zelda_2_-_NES_-_Temple_BGM.ogg')
            cls.music = 'temple'

    @classmethod
    def play_music_boss(cls):
        if cls.music != 'boss':
            cls.play_bgm('08_-_Legend_of_Zelda_2_-_NES_-_Boss.ogg')
            cls.music = 'boss'

    @classmethod
    def play_music_ending(cls):
        if cls.music != 'ending':
            cls.play_bgm('14_-_Legend_of_Zelda_2_-_NES_-_Princess_Zelda.ogg', 0)
            cls.music = 'ending'

    @classmethod
    def play_sound_hurt(cls):
        cls.play_sound('Sound Effect (1).wav')

    @classmethod
    def play_sound_stab(cls):
        cls.play_sound('Sound Effect (2).wav')

    @classmethod
    def play_sound_open(cls):
        cls.play_sound('Sound Effect (3).wav')

    @classmethod
    def play_sound_screen_open(cls):
        cls.play_sound('Sound Effect (4).wav')

    @classmethod
    def play_sound_elevator(cls):
        cls.stop_sound()
        cls.play_sound('Sound Effect (5).wav')

    @classmethod
    def play_sound_select(cls):
        cls.play_sound('Sound Effect (6).wav')

    @classmethod
    def play_sound_damage(cls):
        cls.play_sound('Sound Effect (9).wav')

    @classmethod
    def play_sound_collapse(cls):
        cls.play_sound('Sound Effect (12).wav')

    @classmethod
    def play_sound_shield(cls):
        cls.play_sound('Sound Effect (14).wav')

    @classmethod
    def play_sound_boss_collapse(cls):
        cls.play_sound('Sound Effect (19).wav')

    @classmethod
    def play_sound_gameover(cls):
        cls.play_sound('Sound Effect (25).wav')

    @classmethod
    def stop_music(cls):
        pygame.mixer.music.stop()
        cls.music = ''

    @classmethod
    def stop_sound(cls):
        if cls.sound != None:
            cls.sound.stop()


class Stage(pygame.sprite.LayeredUpdates):
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)

    # because group define __nonzero__ with length of sprites !
    def __bool__(self):
        return True

    def update(self):
        pygame.sprite.LayeredUpdates.update(self)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, width=0, height=0):
        pygame.sprite.Sprite.__init__(self)
        self._x = 0
        self._y = 0
        self._width = width
        self._height = height
        self.image = Image(width, height)
        self.rect = Rectangle(0, 0, width, height)
        self._spritesheet = None
        self.spritedict = {}
        #self.lostsprites = []

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, x):
        self.rect.x = x

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, y):
        self.rect.y = y

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, width):
        self.rect.width = width

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, height):
        self.rect.height = height

    def _create_image(self):
        pass

    def load_image(self, filename):
        return pygame.image.load(os.path.join('assets', filename)).convert_alpha()

    def load_tileset(self, filename):
        self.image = pygame.image.load(os.path.join('', filename)).convert_alpha()

    def set_frame(self, x, y, width, height, pos_x=0, pos_y=0, clear=True):
        if clear:
            self.image.clear()
        self.image = self.image.scale(self._width, self._height)
        self.image.blit(self._spritesheet, (pos_x, pos_y), (x, y, width, height))
        self._base_image = self.image

    def sprites(self):
        return list(self.spritedict)

    def __iter__(self):
        return iter(self.sprites())

    def add_sprite(self, *sprites):
        for sprite in sprites:
            self.add_internal_sprite(sprite)

    def add_internal_sprite(self, sprite, layer=0):
        self.spritedict[sprite] = layer
        for parents in self.groups():
            parents.add(sprite)

    def update(self, *args):
        pass


class Image(pygame.Surface):
    def __init__(self, width, height):
        super().__init__((width, height), pygame.SRCALPHA, 32)
        self._fontSize = 10
        self._font = 'fonts/PixelEmulator-xq08.ttf'
        self._textColor = (255, 255, 255)

    def draw_line(self, start, end, color=(0, 0, 0)):
        pygame.draw.line(self, color, start, end, 1)

    def draw_rect(self, x, y, width, height, color=(0, 0, 0, 0)):
        rect = Rectangle(x, y, width, height)
        pygame.draw.rect(self, color, rect)

    def draw_collide(self, x, y, w, h, color=(255, 0, 0)):
        self.draw_line((x, y), (x + w, y), color)
        self.draw_line((x + w, y), (x + w, y + h), color)
        self.draw_line((x + w, y + h), (x, y + h), color)
        self.draw_line((x, y + h), (x, y), color)

    def draw_text(self, text, x, y, width=0, height=0, alignX=0, alignY=0):
        font = pygame.font.Font(self._font, self._fontSize)
        text = text.split('\n')
        pos_y = 0
        new_x = x
        new_y = y
        for line in text:
            surface = font.render(line, True, self._textColor)
            if alignX:
                new_x = x + (width - surface.get_rect().width) / 2
            if alignY:
                new_y = y + (height - surface.get_rect().height) / 2
            new_y += pos_y
            pos_y += 10
            self.blit(surface, (new_x, new_y))

    def load_image(self, filename):
        surface = pygame.image.load(os.path.join('assets', filename)).convert_alpha()
        self.blit(surface, surface.get_rect())

    def scale(self, width, height):
        image = Image(width, height)
        pygame.transform.scale(self, (width, height), image)
        return image

    def clear(self):
        self.fill((0, 0, 0, 0))

    def flip(self, xbool=True, ybool=False):
        surface = pygame.transform.flip(self, xbool, ybool)
        self.clear()
        self.blit(surface, (0, 0))

    def set_color(self, color=(255, 255, 255)):
        self.fill(color, None, special_flags=pygame.BLEND_RGBA_MULT)

    def blink(self, h):
        width, height = self.get_size()
        for x in range(width):
            for y in range(height):
                c = self.get_at((x, y))
                hsla = (h, c.hsla[1], c.hsla[2] , c.hsla[3])
                c.hsla = hsla
                self.set_at((x, y), c)

    # require to use pygame.RLEACCEL in version 2.0 of pygame on mac!
    def set_alpha(self, alpha=0, **kwargs):
        super().set_alpha(alpha, pygame.RLEACCEL)


class Rectangle(pygame.Rect):
    def __init__(self, x, y, width, height):
        pygame.Rect.__init__(self, x, y, width, height)


class Screen(pygame.sprite.Group):
    def __init__(self, width, height):
        pygame.sprite.Group.__init__(self)
        self._real_width = width
        self._real_height = height
        self._opening = False
        self._visible = False
        self._active = False
        self._main_sprite = None
        self.padding = 8
        self.paddingX = 8
        self.paddingY = 8
        self.load_screen_skin()
        self.create_sprites(width, height)

    @property
    def x(self):
        return self._main_sprite.x

    @x.setter
    def x(self, x):
        self._main_sprite.x = x
        self._frame_sprite.x = x

    @property
    def y(self):
        return self._main_sprite.y

    @y.setter
    def y(self, y):
        self._main_sprite.y = y
        self._frame_sprite.y = y

    @property
    def width(self):
        return self._main_sprite.width

    @width.setter
    def width(self, width):
        self._main_sprite.width = width

    @property
    def height(self):
        return self._main_sprite.height

    @height.setter
    def height(self, height):
        self._main_sprite.height = height

    def load_screen_skin(self):
        self._screen_skin = Sprite(40, 24)
        self._screen_skin = self._screen_skin.load_image('system/screen.png')

    def create_sprites(self, width, height):
        self.create_main_sprite(width, height)
        self.create_frame_sprite(width, height)
        self.create_cursor_sprite()

    def create_main_sprite(self, width, height):
        self._main_sprite = Sprite(width, height)
        self.draw_main_sprite(width, height)
        self.add(self._main_sprite)

    def draw_main_sprite(self, width, height):
        self._main_sprite.image.draw_rect(8, 8, width - 16, height - 16, (0, 0, 0))

    def create_frame_sprite(self, width, height):
        self._frame_sprite = Sprite(width, height)
        self.draw_frame_sprite(width, height)
        self.add(self._frame_sprite)

    def draw_frame_sprite(self, width, height):
        self.draw_frame(0, 0, width, height)

    def draw_frame(self, x, y, width, height):
        self.draw_frame_corners(x, y, width, height)
        self.draw_frame_edges(x, y, width, height)

    def draw_frame_corners(self, x, y, width, height):
        sx = [0, 16, 0, 16]
        sy = [0, 0, 16, 16]
        dx = [x, x + width - 8, x, x + width - 8]
        dy = [y, y, y + height - 8, y + height - 8]
        for i in range(4):
            self._frame_sprite.image.blit(self._screen_skin, (dx[i], dy[i]), (sx[i], sy[i], 8, 8))

    def draw_frame_edges(self, x, y, width, height):
        sx = [8, 0, 16, 8]
        sy = [0, 8, 8, 16]
        dx = [8 + x, x, x + width - 8, 8 + x]
        dy = [y, 8 + y, 8 + y, y + height - 8]
        for i in range(4):
            frame = Image(8, 8)
            frame.blit(self._screen_skin, (0, 0), (sx[i], sy[i], 8, 8))
            scale_width = width - 16 if i == 0 or i == 3 else 8
            scale_height = height - 16 if i == 1 or i == 2 else 8
            new_frame = pygame.transform.scale(frame, (scale_width, scale_height))
            self._frame_sprite.image.blit(new_frame, (dx[i], dy[i]))

    def create_cursor_sprite(self):
        self._cursor_sprite = Sprite(16, 16)
        self.draw_cursor_sprite()
        self.add(self._cursor_sprite)

    def draw_cursor_sprite(self):
        self._cursor_sprite.image.blit(self._screen_skin, (0, 0), (24, 0, 16, 16))

    def refresh_sprites(self):
        self.draw_main_sprite(self._real_width, self._real_height)
        self.draw_frame_sprite(self._real_width, self._real_height)
        self.draw_cursor_sprite()

    def clear_sprite(self):
        for sprite in self.sprites():
            sprite.image = Image(sprite._width, sprite._height)

    def update(self):
        pygame.sprite.Group.update(self)
        self.update_visibility()

    def hide_frame(self):
        self._cursor_sprite.image.set_alpha(0)
        self._frame_sprite.image.set_alpha(0)

    def show_frame(self):
        self._frame_sprite.image.set_alpha(255)
        self._frame_sprite.image.set_alpha(255)

    def update_visibility(self):
        if not self._visible:
            self._cursor_sprite.image.set_alpha(0)
            self._main_sprite.image.set_alpha(0)
            self._frame_sprite.image.set_alpha(0)
        else:
            self._cursor_sprite.image.set_alpha(255)
            self._main_sprite.image.set_alpha(255)
            self._frame_sprite.image.set_alpha(255)

    def move(self, x, y):
        for sprite in self.sprites():
            sprite.x = x or 0
            sprite.y = y or 0

    def is_open(self):
        return self._opening


class Tilemap(pygame.sprite.LayeredUpdates):
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)
        self._width = 0
        self._height = 0
        self._map_width = 0
        self._map_height = 0
        self._tile_width = 16
        self._tile_height = 16
        self._layer_data = {}
        self._lower_layer = None
        self._layers_count = 0
        self._tileset_data = {}
        self._tileset = None
        self._animation_count = 0

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def tile_width(self):
        return self._tileWidth

    @tile_width.setter
    def tile_width(self, tile_width):
        self._tileWidth = tile_width

    @property
    def tile_height(self):
        return self._tileHeight

    @tile_height.setter
    def tile_height(self, tile_height):
        self._tileHeight = tile_height

    def update(self):
        pass

    def setup(self, tiled):
        self._set_data(tiled)
        self._set_map_data()
        self._load_tilesets()
        self._create_layers()
        self._draw_all_tiles()

    def _set_data(self, tiled):
        self._map_width = tiled['width']
        self._map_height = tiled['height']
        self._tile_width = tiled['tilewidth']
        self._tile_height = tiled['tileheight']
        self._width = self._map_width * self._tile_width
        self._height = self._map_height * self._tile_height
        self._layer_data = tiled['layers'][:-1]
        self._tileset_data = tiled['tilesets'][0]
        self._layers_count = len(self._layer_data)

    def _set_map_data(self):
        self._data = [data for layer in self._layer_data for data in layer['data']]

    def _load_tilesets(self):
        width = self._tileset_data['imagewidth']
        height = self._tileset_data['imageheight']
        self._tileset = Sprite(width, height)
        self._tileset.load_tileset("data/maps/" + self._tileset_data['image'])

    def _create_layers(self):
        self._lower_layer = Sprite(self._width, self._height)
        self._lower_layer._layer = 0
        self.add(self._lower_layer)
        self._upper_layer = Sprite(self._width, self._height)
        self._upper_layer._layer = 3
        self.add(self._upper_layer)

    def _draw_all_tiles(self):
        for z in range(self._layers_count):
            for y in range(self._map_height):
                for x in range(self._map_width):
                    tile_id = self._real_map_data(x, y, z)
                    self._draw_tile(x, y, z, tile_id)

    def _draw_tile(self, x, y, z, tile_id):
        src_x = tile_id % (round(self._tileset_data['imagewidth'] / 16))
        src_y = math.floor(tile_id / round(self._tileset_data['imagewidth'] / 16))
        layer = self._lower_layer if z == 0 else self._upper_layer
        layer.image.blit(self._tileset.image, (x * 16, y * 16), (src_x * 16, src_y * 16, 16, 16))

    def update(self):
        self._animation_count += 1
        tiles = self._tileset_data.get('tiles', [])
        for tile_data in tiles:
            if tile_data.get('animation', False):
                self.update_anim(tile_data)

    def update_anim(self, tile_data):
        for y in range(self._map_height):
            for x in range(self._map_width):
                tile_id = self._real_map_data(x, y)
                if tile_id == tile_data["id"]:
                    if self._animation_count % 20 == 0:
                        id1 = tile_data["animation"][0]["tileid"]
                        self._draw_tile(x, y, 0, id1)
                    if self._animation_count % 20 == 10:
                        id2 = tile_data["animation"][1]["tileid"]
                        self._draw_tile(x, y, 0, id2)


    def _real_map_data(self, x, y, z=0):
        return self._data[(z * self._map_height + y) * self._map_width + x] - 1
