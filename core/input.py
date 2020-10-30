import pygame

import core.pyxi as pyretro
import scene.scene_manager as s_m

LEFT = 1
MIDDLE = 2
RIGHT = 3


class Object(object):
    pass


class Input:
    _mousePressed = False
    _pressedTime = 0
    _events = None
    _triggered = False
    _cancelled = False
    _moved = False
    _released = False
    _pos = (0, 0)
    _previousState = {}
    _currentState = {}
    _latestButton = None
    _dir2 = 0

    @classmethod
    def initialize(cls):
        cls.clear()

    @classmethod
    def clear(cls):
        cls._events = Object()
        cls._events.triggered = False
        cls._events.cancelled = False
        cls._events.moved = False
        cls._events.released = False

    @classmethod
    def update(cls):
        cls._triggered = cls._events.triggered
        cls._cancelled = cls._events.cancelled
        cls._moved = cls._events.moved
        cls._released = cls._events.released
        cls.clear()
        cls.event_handlers()
        cls.update_state()
        cls.update_direction()

    @classmethod
    def update_state(cls):
        if cls._currentState.get(cls._latestButton):
            cls._pressedTime += 1
        else:
            cls._latestButton = None
        for name in cls._currentState:
            if cls._currentState[name] and not cls._previousState.get(name):
                cls._latestButton = name
                cls._pressedTime = 0
            cls._previousState[name] = cls._currentState[name]

    @classmethod
    def update_direction(cls):
        cls.update_direction_x()
        cls.update_direction_y()

    @classmethod
    def update_direction_x(cls):
        d = 0
        if cls.is_key_pressed('right'):
            d = 1
        if cls.is_key_pressed('left'):
            d = -1
        cls._dirX = d

    @classmethod
    def update_direction_y(cls):
        d = 0
        if cls.is_key_pressed('down'):
            d = 1
        if cls.is_key_pressed('up'):
            d = -1
        cls._dirY = d

    @classmethod
    def event_handlers(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s_m.SceneManager.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                cls.on_mouse_down(event)
            if event.type == pygame.MOUSEBUTTONUP:
                cls.on_mouse_up(event)
            if event.type == pygame.MOUSEMOTION:
                cls.on_mouse_motion()
            if event.type == pygame.KEYDOWN:
                cls.on_key_down(event)
            if event.type == pygame.KEYUP:
                cls.on_key_up(event)
            if event.type == pygame.VIDEORESIZE:
                pyretro.Display.resize_screen(event)

    @classmethod
    def on_mouse_down(cls, event):
        if event.button == LEFT:
            cls.on_left_button_down()
        if event.button == MIDDLE:
            cls.on_middle_button_down()
        if event.button == RIGHT:
            cls.on_right_button_down()

    @classmethod
    def on_left_button_down(cls):
        cls._mousePressed = True
        cls._pressedTime = 0
        cls._on_trigger()

    @classmethod
    def on_middle_button_down(cls):
        pass

    @classmethod
    def on_right_button_down(cls):
        cls._on_cancel()

    @classmethod
    def on_mouse_up(cls, event):
        if event.button == LEFT:
            cls._mousePressed = False
            cls._on_released()

    @classmethod
    def on_mouse_motion(cls):
        cls._events.moved = True
        cls._pos = pygame.mouse.get_pos()

    @classmethod
    def on_key_down(cls, event):
        name = pygame.key.name(event.key)
        cls._currentState[name] = True

    @classmethod
    def on_key_up(cls, event):
        name = pygame.key.name(event.key)
        cls._currentState[name] = False

    @classmethod
    def _on_trigger(cls):
        cls._events.triggered = True

    @classmethod
    def _on_cancel(cls):
        cls._events.cancelled = True

    @classmethod
    def _on_released(cls):
        cls._events.released = True

    @classmethod
    def is_key_pressed(cls, key_name):
        return cls._currentState.get(key_name, False)

    @classmethod
    def is_key_triggered(cls, key_name):
        return cls._currentState.get(key_name, False) and cls._pressedTime == 0

    @classmethod
    def is_pressed(cls):
        return cls._mousePressed

    @classmethod
    def is_triggered(cls):
        return cls._triggered

    @classmethod
    def is_cancelled(cls):
        return cls._cancelled

    @classmethod
    def is_released(cls):
        return cls._released

    @classmethod
    def get_pos(cls):
        return cls._pos

    @classmethod
    def is_moved(cls):
        pass

    @classmethod
    def dirX(cls):
        return cls._dirX

    @classmethod
    def dirY(cls):
        return cls._dirY
