import sys

from core.input import Input


class SceneManager:
    _screen = None
    _scene = None
    _next_scene = None
    _stack = []
    _scene_started = False
    _previous_scene = None
    _exiting = False

    @classmethod
    def run(cls, scene_class, screen):
        cls._scene = scene_class()
        cls._screen = screen
        cls.init()

    @classmethod
    def goto(cls, scene_class):
        if scene_class:
            cls._next_scene = scene_class()

    @classmethod
    def init(cls):
        cls.init_input()

    @staticmethod
    def init_input():
        Input.initialize()

    @classmethod
    def update(cls):
        cls.update_main()

    @classmethod
    def update_main(cls):
        cls.update_input()
        cls.update_scene()
        cls.update_next()

    @staticmethod
    def update_input():
        Input.update()

    @classmethod
    def update_next(cls):
        if cls._next_scene and not cls._scene.is_busy():
            cls._scene.terminate()
            cls._previous_scene = cls._scene.__class__
            cls._scene = cls._next_scene
            cls._scene.create()
            cls._next_scene = None
            cls._scene_started = False

    @classmethod
    def update_scene(cls):
        if not cls._scene_started:
            cls._scene.start()
            cls._scene_started = True
        if cls._scene_started:
            cls._scene.update()
        if cls._exiting:
            cls.terminate()

    @classmethod
    def draw(cls):
        if cls._scene_started:
            cls._scene.draw(cls._screen)

    @classmethod
    def pop(cls):
        if len(cls._stack) > 0:
            cls.goto(cls._stack.pop())
        else:
            cls.exit()

    @classmethod
    def exit(cls):
        cls.goto(None)
        cls._exiting = True

    @classmethod
    def scene(cls, message, *args):
        try:
            eval('cls._scene.' + message + str(args))
        except (SyntaxError, AttributeError):
           pass

    @staticmethod
    def terminate():
        sys.exit()
