import pygame.font


class Scoreboard:
    """A class to report scoring information."""
    score_rect: object
    high_score_rect: object

    def __init__(self, settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        # Font settings for scoring information.
        self.text_color = (250, 250, 250)
        self.font = pygame.font.SysFont(None, 100)
        self.pacmans = []

        self.hs_width, self.hs_height = 200, 50
        self.button_color_hs = (0, 0, 0)
        self.text_color_hs = (255, 255, 255)
        self.rect_hs = pygame.Rect(0, 0, self.hs_width, self.hs_height)
        self.rect_hs.right = self.screen_rect.right - 100
        self.rect_hs.top = 50
        self.font_hs = pygame.font.SysFont(None, 50)

        # Prepare the initial score image
        self.prep_score()
        self.prep_highscore()
        self.hs = self.font_hs.render("HIGHSCORE", True, self.text_color_hs, self.button_color_hs)
        self.hs_rect = self.hs.get_rect()
        self.hs_rect.right = self.screen_rect.right - 40
        self.hs_rect.top = 25

    def draw_hs(self):
        self.screen.fill(self.button_color_hs, self.hs_rect)
        self.screen.blit(self.hs, self.hs_rect)

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 125
        self.score_rect.top = 200

    def show_score(self):
        """Draw score and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.draw_hs()

    def prep_highscore(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 125
        self.high_score_rect.top = 60
