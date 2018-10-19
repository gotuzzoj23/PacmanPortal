import pygame
from pygame.sprite import Sprite
from imagerect import ImageRect


class Orange(Sprite):
    BRICK_SIZE = 12
    ORANGE_SIZE = 5

    def __init__(self, screen, mazefile):
        """Initialize pacman and set its starting position"""
        super(Orange, self).__init__()
        self.screen = screen

        self.filename = mazefile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.sz = Orange.ORANGE_SIZE
        self.oranges = []
        for x in range(5):
            self.oranges.append([])

        self.orange = ImageRect(screen, 'orange/orange_down_1', int(self.sz * 5.1), int(self.sz * 5.1))
        self.create_oranges(self.screen, self.sz)

        self.deltax = self.deltay = self.BRICK_SIZE
        self.starting_centerx = 0
        self.starting_centery = 0
        self.build()

        self.centerx = float(self.orange.rect.centerx)
        self.centery = float(self.orange.rect.centery)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.index = 0

        self.i = 0  # used for debug traversing image
        self.scared = False

    def __str__(self):
        return 'orange(' + self.filename + ')'

    def build(self):
        dx, dy = self.deltax, self.deltay

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'O':
                    self.orange.rect.centerx = ncol * dx
                    self.orange.rect.centery = nrow * dy
                    self.starting_centerx = ncol * dx
                    self.starting_centery = nrow * dy

    def blitme(self):
        if self.scared == 1:
            self.scared_blitme()
        else:
            if self.index == 2:
                self.index = 0
            if not self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
                self.screen.blit(self.oranges[0][0].image, self.orange.rect)
            if self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
                self.screen.blit(self.oranges[0][self.index].image, self.orange.rect)
            if not self.moving_down and self.moving_left and not self.moving_right and not self.moving_up:
                self.screen.blit(self.oranges[1][self.index].image, self.orange.rect)
            if not self.moving_down and not self.moving_left and self.moving_right and not self.moving_up:
                self.screen.blit(self.oranges[2][self.index].image, self.orange.rect)
            if not self.moving_down and not self.moving_left and not self.moving_right and self.moving_up:
                self.screen.blit(self.oranges[3][self.index].image, self.orange.rect)
        self.index += 1

    def update(self, maze, stats, pacman, startup, blue, pink, red, sb):
        """Update the orange's position based on the movement flag."""
        x = int(self.orange.rect.centerx / 12)
        y = int(self.orange.rect.centery / 12)

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
        self.orange.rect.centerx = self.centerx
        self.orange.rect.centery = self.centery

        if (pygame.Rect.colliderect(pacman.pacman.rect, self.orange.rect)) and (not self.scared):
            pacman.reset_pacman()
            self.reset_orange()
            stats.pacmans_left -= 1
            print(stats.pacmans_left)
            if stats.pacmans_left == 0:
                if stats.pacmans_left == 0:
                    startup.playing = False
                    self.reset_figures(blue, red, pink, pacman)
                    maze.reset_maze()
                    if stats.score > stats.high_score:
                        stats.high_score = stats.score
                        stats.score = 0
                        sb.prep_score()
                        sb.prep_highscore()

    def create_oranges(self, screen, sz):
        self.oranges[0].append(self.orange)
        self.orange = ImageRect(screen, 'orange/orange_down_2', int(sz * 5.1), int(sz * 5.1))
        self.oranges[0].append(self.orange)

        self.orange = ImageRect(screen, 'orange/orange_left_1', int(sz * 5.1), int(sz * 5.1))
        self.oranges[1].append(self.orange)
        self.orange = ImageRect(screen, 'orange/orange_left_2', int(sz * 5.1), int(sz * 5.1))
        self.oranges[1].append(self.orange)

        self.orange = ImageRect(screen, 'orange/orange_right_1', int(sz * 5.1), int(sz * 5.1))
        self.oranges[2].append(self.orange)
        self.orange = ImageRect(screen, 'orange/orange_right_2', int(sz * 5.1), int(sz * 5.1))
        self.oranges[2].append(self.orange)

        self.orange = ImageRect(screen, 'orange/orange_up_1', int(sz * 5.1), int(sz * 5.1))
        self.oranges[3].append(self.orange)
        self.orange = ImageRect(screen, 'orange/orange_up_2', int(sz * 5.1), int(sz * 5.1))
        self.oranges[3].append(self.orange)

        self.orange = ImageRect(screen, 'scared/scared_1', int(sz * 5.1), int(sz * 5.1))
        self.oranges[4].append(self.orange)
        self.orange = ImageRect(screen, 'scared/scared_2', int(sz * 5.1), int(sz * 5.1))
        self.oranges[4].append(self.orange)

    def reset_orange(self):
        self.centerx = self.starting_centerx
        self.centery = self.starting_centery

    def scared_blitme(self):
        if self.index == 2:
            self.index = 0
        if not self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
            self.screen.blit(self.oranges[4][0].image, self.orange.rect)
        if self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
            self.screen.blit(self.oranges[4][self.index].image, self.orange.rect)
        if not self.moving_down and self.moving_left and not self.moving_right and not self.moving_up:
            self.screen.blit(self.oranges[4][self.index].image, self.orange.rect)
        if not self.moving_down and not self.moving_left and self.moving_right and not self.moving_up:
            self.screen.blit(self.oranges[4][self.index].image, self.orange.rect)
        if not self.moving_down and not self.moving_left and not self.moving_right and self.moving_up:
            self.screen.blit(self.oranges[4][self.index].image, self.orange.rect)

    def reset_figures(self, blue, red, pink, pacman):
        self.reset_orange()
        pacman.reset_pacman()
        blue.reset_blue()
        red.reset_red()
        pink.reset_pink()
