import pygame
from pygame.sprite import Sprite
from imagerect import ImageRect


class Blue(Sprite):
    BRICK_SIZE = 12
    BLUE_SIZE = 5

    def __init__(self, screen, mazefile):
        """Initialize pacman and set its starting position"""
        super(Blue, self).__init__()
        self.screen = screen

        self.filename = mazefile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.sz = Blue.BLUE_SIZE
        self.blues = []
        for x in range(5):
            self.blues.append([])

        self.blue = ImageRect(screen, 'blue/blue_down_1', int(self.sz * 5.1), int(self.sz * 5.1))
        self.create_blues(self.screen, self.sz)

        self.deltax = self.deltay = self.BRICK_SIZE
        self.starting_centerx = 0
        self.starting_centery = 0
        self.build()

        self.centerx = float(self.blue.rect.centerx)
        self.centery = float(self.blue.rect.centery)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.index = 0

        self.i = 0  # used for debug traversing image
        self.scared = False

    def __str__(self):
        return 'blue(' + self.filename + ')'

    def build(self):
        dx, dy = self.deltax, self.deltay
        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'B':
                    self.blue.rect.centerx = ncol * dx
                    self.blue.rect.centery = nrow * dy
                    self.starting_centerx = ncol * dx
                    self.starting_centery = nrow * dy

    def blitme(self):
        if self.scared == 1:
            self.scared_blitme()
        else:
            if self.index == 2:
                self.index = 0
            if not self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
                self.screen.blit(self.blues[0][0].image, self.blue.rect)
            if self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
                self.screen.blit(self.blues[0][self.index].image, self.blue.rect)
            if not self.moving_down and self.moving_left and not self.moving_right and not self.moving_up:
                self.screen.blit(self.blues[1][self.index].image, self.blue.rect)
            if not self.moving_down and not self.moving_left and self.moving_right and not self.moving_up:
                self.screen.blit(self.blues[2][self.index].image, self.blue.rect)
            if not self.moving_down and not self.moving_left and not self.moving_right and self.moving_up:
                self.screen.blit(self.blues[3][self.index].image, self.blue.rect)
        self.index += 1

    def update(self, maze, settings, stats, pacman, startup, red, pink, orange, sb):
        """Update the blue's position based on the movement flag."""
        x = int(self.blue.rect.centerx / 12)
        y = int(self.blue.rect.centery / 12)

        if self.i < 200 and self.rows[y][x + 1] != 'x':
            self.moving_right = True
            self.moving_up = False
            self.moving_down = False
            self.moving_left = False
            self.centerx += 1.0
        elif self.i >= 200 and (self.i < 400) and self.rows[y][x - 1] != 'x':
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.moving_left = True
            self.centerx -= 1.0
        elif self.i >= 400 and (self.i < 600) and self.rows[y + 1][x] != 'x':
            self.centery += 1
            self.moving_down = True
            self.moving_right = False
            self.moving_up = False
            self.moving_left = False

        elif self.i >= 800 and (self.i < 1000) and self.rows[y - 1][x] != 'x':
            self.centery -= 1
            self.moving_up = True
            self.moving_right = False
            self.moving_left = False
            self.moving_down = False

        if self.i >= 1000:
            self.i = 0
        self.i += 1
        self.blue.rect.centerx = self.centerx
        self.blue.rect.centery = self.centery

        if (pygame.Rect.colliderect(pacman.pacman.rect, self.blue.rect)) and (not self.scared):
            if stats.pacmans_left == 0:
                startup.playing = False
                self.reset_figures(red, orange, pink, pacman)
                maze.reset_maze()
                stats.pacmans_left = 3
                pygame.mixer.music.stop()
                settings.start_intro_music()
                settings.flag_chomp = False
                sb.prep_pac_lives()
                if stats.score > stats.high_score:
                    stats.high_score = stats.score
                    stats.score = 0
                    sb.prep_highscore()
                    sb.prep_score()
            else:
                pacman.reset_pacman()
                self.reset_blue()
                stats.pacmans_left -= 1
                sb.prep_pac_lives()
            #    print(stats.pacmans_left)

    def create_blues(self, screen, sz):
        self.blues[0].append(self.blue)
        self.blue = ImageRect(screen, 'blue/blue_down_2', int(sz * 5.1), int(sz * 5.1))
        self.blues[0].append(self.blue)

        self.blue = ImageRect(screen, 'blue/blue_left_1', int(sz * 5.1), int(sz * 5.1))
        self.blues[1].append(self.blue)
        self.blue = ImageRect(screen, 'blue/blue_left_2', int(sz * 5.1), int(sz * 5.1))
        self.blues[1].append(self.blue)

        self.blue = ImageRect(screen, 'blue/blue_right_1', int(sz * 5.1), int(sz * 5.1))
        self.blues[2].append(self.blue)
        self.blue = ImageRect(screen, 'blue/blue_right_2', int(sz * 5.1), int(sz * 5.1))
        self.blues[2].append(self.blue)

        self.blue = ImageRect(screen, 'blue/blue_up_1', int(sz * 5.1), int(sz * 5.1))
        self.blues[3].append(self.blue)
        self.blue = ImageRect(screen, 'blue/blue_up_2', int(sz * 5.1), int(sz * 5.1))
        self.blues[3].append(self.blue)

        self.blue = ImageRect(screen, 'scared/scared_1', int(sz * 5.1), int(sz * 5.1))
        self.blues[4].append(self.blue)
        self.blue = ImageRect(screen, 'scared/scared_2', int(sz * 5.1), int(sz * 5.1))
        self.blues[4].append(self.blue)

    def reset_blue(self):
        self.centerx = self.starting_centerx
        self.centery = self.starting_centery

    def scared_blitme(self):
        if self.index == 2:
            self.index = 0
        if not self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
            self.screen.blit(self.blues[4][0].image, self.blue.rect)
        if self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
            self.screen.blit(self.blues[4][self.index].image, self.blue.rect)
        if not self.moving_down and self.moving_left and not self.moving_right and not self.moving_up:
            self.screen.blit(self.blues[4][self.index].image, self.blue.rect)
        if not self.moving_down and not self.moving_left and self.moving_right and not self.moving_up:
            self.screen.blit(self.blues[4][self.index].image, self.blue.rect)
        if not self.moving_down and not self.moving_left and not self.moving_right and self.moving_up:
            self.screen.blit(self.blues[4][self.index].image, self.blue.rect)

    def reset_figures(self, red, orange, pink, pacman):
        self.reset_blue()
        pacman.reset_pacman()
        red.reset_red()
        orange.reset_orange()
        pink.reset_pink()
