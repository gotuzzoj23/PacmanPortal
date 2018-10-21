import pygame
from pygame import gfxdraw
from eventloop import EventLoop
from maze import Maze
from pacman import Pacman
from red import Red
from blue import Blue
from orange import Orange
from pink import Pink
from start import Start
from settings import Settings
from stats import Stats
from scoreboard import Scoreboard


class Game:
    BLACK = (0, 0, 0)

    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        self.settings = Settings()
        self.settings.start_intro_music()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Pacman Portal")
        self.clock = pygame.time.Clock()
        self.radius = 1
        self.start = 1
        self.end = 10
        self.begin = pygame.time.get_ticks()
        self.wait = 800

        self.startup = Start(self.screen, self.settings)
        self.stats = Stats(self.settings)
        self.sb = Scoreboard(self.settings, self.screen, self.stats)

        self.maze = Maze(self.screen, mazefile='images/pacman_portal_maze.txt',
                         brickfile='square', orangeportalfile='portal_orange', blueportalfile='portal_blue',
                         shieldfile='shield', pointfile='point_pill', gatefile="gate")
        self.pacman = Pacman(self.screen, mazefile='images/pacman_portal_maze.txt')

        self.red = Red(self.screen, mazefile='images/pacman_portal_maze.txt')
        self.blue = Blue(self.screen, mazefile='images/pacman_portal_maze.txt')
        self.orange = Orange(self.screen, mazefile='images/pacman_portal_maze.txt')
        self.pink = Pink(self.screen, mazefile='images/pacman_portal_maze.txt')
        self.inc = 0

    def __str__(self): return 'Game(Pacman Portal), maze=' + str(self.maze) + ')'

    def open_portal(self, x, y, color):
        for r in range(self.start, self.end):
            pygame.gfxdraw.circle(self.screen, x, y, r, color)
        now = pygame.time.get_ticks()
        if now < self.begin + self.wait:
            self.inc = 1
        elif now < self.begin + 4 * self.wait:
            self.inc = 0
        else:
            self.inc = -1
        self.start += self.inc
        self.start = max(1, self.start)
        self.end += self.inc

    def play(self):
        clock = pygame.time.Clock()
        eloop = EventLoop(finished=False)
        while not eloop.finished:
            eloop.check_events(self.screen, self.pacman, self.startup)
            if self.startup.playing:
                pygame.mixer.music.stop()
                if not self.settings.flag_chomp:
                    self.settings.chomp_music()
                    self.settings.flag_chomp = True
                self.settings.chomp_music()
                self.pacman.update(self.maze, self.settings, self.stats, self.sb, self.red, self.blue, self.orange,
                                   self.pink)
                self.red.update(self.maze, self.settings, self.stats, self.pacman, self.startup, self.blue, self.pink,
                                self.orange, self.sb)
                self.blue.update(self.maze, self.settings, self.stats, self.pacman, self.startup, self.red, self.pink,
                                 self.orange, self.sb)
                self.orange.update(self.maze, self.settings, self.stats, self.pacman, self.startup, self.blue,
                                   self.pink, self.red, self.sb)
                self.pink.update(self.maze, self.settings, self.stats, self.pacman, self.startup, self.blue, self.red,
                                 self.orange, self.sb)

            self.update_screen()
            clock.tick(155)

    def update_screen(self):
        if not self.startup.playing:
            self.startup.draw_bg()
            self.startup.draw_button()
        else:
            self.screen.fill(Game.BLACK)
            self.maze.blitme()
            self.pacman.blitme()
            self.red.blitme()
            self.blue.blitme()
            self.orange.blitme()
            self.pink.blitme()
            self.open_portal(100, 100, (240, 100, 20))
            self.sb.show_score()
        pygame.display.flip()


game = Game()
game.play()
