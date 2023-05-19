class GameStats():

    def __init__(self, settings) -> None:
        self.settings = settings
        self.reset_stats()

        self.game_active = True

    def reset_stats(self):
        self.ships_left = self.settings["ship_limit"]
        self.score = 0