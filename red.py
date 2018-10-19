import pygame
from pygame.sprite import Sprite
from imagerect import ImageRect


class Red(Sprite):
    BRICK_SIZE = 12
    RED_SIZE = 5

    def __init__(self, screen, mazefile):
        """Initialize pacman and set its starting position"""
        super(Red, self).__init__()
        self.screen = screen

        self.filename = mazefile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.sz = Red.RED_SIZE
        self.reds = []
        for x in range(5):
            self.reds.append([])

        self.red = ImageRect(screen, 'red/red_down_1', int(self.sz * 5.1), int(self.sz * 5.1))
        self.create_reds(self.screen, self.sz)

        self.deltax = self.deltay = self.BRICK_SIZE

        self.starting_centerx = 0
        self.starting_centery = 0
        self.build()

        self.centerx = float(self.red.rect.centerx)
        self.centery = float(self.red.rect.centery)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.index = 0

        self.i = 0  # used for debug traversing image
        self.scared = False

    def __str__(self):
        return 'red(' + self.filename + ')'

    def build(self):
        dx, dy = self.deltax, self.deltay

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'R':
                    self.red.rect.centerx = ncol * dx
                    self.red.rect.centery = nrow * dy
                    self.starting_centerx = ncol * dx
                    self.starting_centery = nrow * dy

    def blitme(self):
        if self.scared == 1:
            self.scared_blitme()
        else:
            if self.index == 2:
                self.index = 0
            if not self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
                self.screen.blit(self.reds[0][0].image, self.red.rect)
            if self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
                self.screen.blit(self.reds[0][self.index].image, self.red.rect)
            if not self.moving_down and self.moving_left and not self.moving_right and not self.moving_up:
                self.screen.blit(self.reds[1][self.index].image, self.red.rect)
            if not self.moving_down and not self.moving_left and self.moving_right and not self.moving_up:
                self.screen.blit(self.reds[2][self.index].image, self.red.rect)
            if not self.moving_down and not self.moving_left and not self.moving_right and self.moving_up:
                self.screen.blit(self.reds[3][self.index].image, self.red.rect)
        self.index += 1

    def update(self, maze, stats, pacman, startup, blue, pink, orange, sb):
        """Update the red's position based on the movement flag."""
        x = int(self.red.rect.centerx / 12)
        y = int(self.red.rect.centery / 12)

        if self.i < 200 and self.rows[y][x+1] != 'x':
            self.moving_right = True
            self.moving_up = False
            self.moving_down = False
            self.moving_left = False
            self.centerx += 1.0
        elif self.i >= 200 and (self.i < 400) and self.rows[y][x-1] != 'x':
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.moving_left = True
            self.centerx -= 1.0
        elif self.i >= 400 and (self.i < 600) and self.rows[y+1][x] != 'x':
            self.centery += 1
            self.moving_down = True
            self.moving_right = False
            self.moving_up = False
            self.moving_left = False

        elif self.i >= 800 and (self.i < 1000) and self.rows[y-1][x] != 'x':
            self.centery -= 1
            self.moving_up = True
            self.moving_right = False
            self.moving_left = False
            self.moving_down = False

        if self.i >= 1000:
            self.i = 0
        self.i += 1
        self.red.rect.centerx = self.centerx
        self.red.rect.centery = self.centery

        if (pygame.Rect.colliderect(pacman.pacman.rect, self.red.rect)) and (not self.scared):
            pacman.reset_pacman()
            self.reset_red()
            stats.pacmans_left -= 1
            print(stats.pacmans_left)
            if stats.pacmans_left == 0:
                startup.playing = False
                self.reset_figures(blue, orange, pink, pacman)
                maze.reset_maze()
                if stats.score > stats.high_score:
                    stats.high_score = stats.score
                    stats.score = 0
                    sb.prep_highscore()

    def create_reds(self, screen, sz):
        self.reds[0].append(self.red)
        self.red = ImageRect(screen, 'red/red_down_2', int(sz * 5.1), int(sz * 5.1))
        self.reds[0].append(self.red)

        self.red = ImageRect(screen, 'red/red_left_1', int(sz * 5.1), int(sz * 5.1))
        self.reds[1].append(self.red)
        self.red = ImageRect(screen, 'red/red_left_2', int(sz * 5.1), int(sz * 5.1))
        self.reds[1].append(self.red)

        self.red = ImageRect(screen, 'red/red_right_1', int(sz * 5.1), int(sz * 5.1))
        self.reds[2].append(self.red)
        self.red = ImageRect(screen, 'red/red_right_2', int(sz * 5.1), int(sz * 5.1))
        self.reds[2].append(self.red)

        self.red = ImageRect(screen, 'red/red_up_1', int(sz * 5.1), int(sz * 5.1))
        self.reds[3].append(self.red)
        self.red = ImageRect(screen, 'red/red_up_2', int(sz * 5.1), int(sz * 5.1))
        self.reds[3].append(self.red)

        self.red = ImageRect(screen, 'scared/scared_1', int(sz * 5.1), int(sz * 5.1))
        self.reds[4].append(self.red)
        self.red = ImageRect(screen, 'scared/scared_2', int(sz * 5.1), int(sz * 5.1))
        self.reds[4].append(self.red)

    def reset_red(self):
        self.centerx = self.starting_centerx
        self.centery = self.starting_centery

    def scared_blitme(self):
        if self.index == 2:
            self.index = 0
        if not self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
            self.screen.blit(self.reds[4][0].image, self.red.rect)
        if self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
            self.screen.blit(self.reds[4][self.index].image, self.red.rect)
        if not self.moving_down and self.moving_left and not self.moving_right and not self.moving_up:
            self.screen.blit(self.reds[4][self.index].image, self.red.rect)
        if not self.moving_down and not self.moving_left and self.moving_right and not self.moving_up:
            self.screen.blit(self.reds[4][self.index].image, self.red.rect)
        if not self.moving_down and not self.moving_left and not self.moving_right and self.moving_up:
            self.screen.blit(self.reds[4][self.index].image, self.red.rect)

    def reset_figures(self, blue, orange, pink, pacman):
        self.reset_red()
        pacman.reset_pacman()
        blue.reset_blue()
        orange.reset_orange()
        pink.reset_pink()
