from core.pyxi import Display
from scene.scene_boot import SceneBoot


def main():
    Display.init(SceneBoot)
    Display.game_loop()


if __name__ == '__main__':
    main()
