import pygame


class Settings:

    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 900
        self.bg_color = (0, 0, 0)

        self.life_limit = 3

        self.points_coins = 10
        self.points_shields = 50
        self.points_ghost = 200

    @staticmethod
    def start_intro_music():
        pygame.mixer.music.load("sounds/intro.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
