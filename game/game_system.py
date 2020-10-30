class GameSystem:
    def __init__(self):
        self.debug_enabled = False

    def is_debugging(self):
        return self.debug_enabled

    def call_debug(self):
        self.debug_enabled = not self.debug_enabled
