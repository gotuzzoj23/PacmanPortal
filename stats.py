class Stats:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.high_score = 0
        self.pacmans_left = self.settings.life_limit
        self.score = 0
        self.level = 1

    def reset_stats(self):
        self.pacmans_left = self.settings.life_limit
        self.score = 0
        self.level = 1
