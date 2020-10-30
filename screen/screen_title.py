from screen.screen_command import ScreenCommand


class ScreenTitle(ScreenCommand):
    def __init__(self):
        ScreenCommand.__init__(self, 130, 75)
        self.x = self.center_x()
        self.y = self.center_y()

    def update(self):
        ScreenCommand.update(self)

    def make_command_list(self):
        self.add_command('new game', 'newGame')
        self.add_command('credits', 'credits')
