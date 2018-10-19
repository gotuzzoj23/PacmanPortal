import pygame
from pygame.sprite import Sprite
from imagerect import ImageRect


class Pacman(Sprite):
    BRICK_SIZE = 12
    PACMAN_SIZE = 5

    def __init__(self, screen, mazefile):
        """Initialize pacman and set its starting position"""
        super(Pacman, self).__init__()
        self.screen = screen

        self.filename = mazefile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        sz = Pacman.PACMAN_SIZE
        self.pacmans = []
        for x in range(5):
            self.pacmans.append([])

        self.pacman = ImageRect(screen, 'pacman/pac', int(sz * 5.1), int(sz * 5.1))
        self.pacmans[0].append(self.pacman)

        self.pacmans[1].append(self.pacman)
        self.pacman = ImageRect(screen, 'pacman/pac_down_1', int(sz * 5.1), int(sz * 5.1))
        self.pacmans[1].append(self.pacman)
        self.pacman = ImageRect(screen, 'pacman/pac_down_2', int(sz * 5.1), int(sz * 5.1))
        self.pacmans[1].append(self.pacman)

        self.pacman = ImageRect(screen, 'pacman/pac', int(sz * 5.1), int(sz * 5.1))
        self.pacmans[2].append(self.pacman)
        self.pacman = ImageRect(screen, 'pacman/pac_left_1', int(sz * 5.1), int(sz * 5.1))
        self.pacmans[2].append(self.pacman)
        self.pacman = ImageRect(screen, 'pacman/pac_left_2', int(sz * 5.1), int(sz * 5.1))
        self.pacmans[2].append(self.pacman)

        self.pacman = ImageRect(screen, 'pacman/pac', int(sz * 5.1), int(sz * 5.1))
        self.pacmans[3].append(self.pacman)
        self.pacman = ImageRect(screen, 'pacman/pac_right_1', int(sz * 5.1), int(sz * 5.1))
        self.pacmans[3].append(self.pacman)
        self.pacman = ImageRect(screen, 'pacman/pac_right_2', int(sz * 5.1), int(sz * 5.1))
        self.pacmans[3].append(self.pacman)

        self.pacman = ImageRect(screen, 'pacman/pac', int(sz * 5.1), int(sz * 5.1))
        self.pacmans[4].append(self.pacman)
        self.pacman = ImageRect(screen, 'pacman/pac_up_1', int(sz * 5.1), int(sz * 5.1))
        self.pacmans[4].append(self.pacman)
        self.pacman = ImageRect(screen, 'pacman/pac_up_2', int(sz * 5.1), int(sz * 5.1))
        self.pacmans[4].append(self.pacman)

        self.deltax = self.deltay = self.BRICK_SIZE

        self.starting_centerx = 0
        self.starting_centery = 0

        self.build()
        self.centerx = float(self.pacman.rect.centerx)
        self.centery = float(self.pacman.rect.centery)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.index = 0
        self.scared_timer = 0
        self.scared_flag = False

    def __str__(self):
        return 'pacman(' + self.filename + ')'

    def build(self):
        dx, dy = self.deltax, self.deltay
        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == '@':
                    self.pacman.rect.centerx = ncol * dx
                    self.pacman.rect.centery = nrow * dy
                    self.starting_centerx = ncol * dx
                    self.starting_centery = nrow * dy

    def blitme(self):
        if not self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
            self.screen.blit(self.pacmans[0][0].image, self.pacman.rect)
        elif self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
            if self.index == 3:
                self.index = 0
            self.screen.blit(self.pacmans[1][self.index].image, self.pacman.rect)
            self.index += 1
        elif not self.moving_down and self.moving_left and not self.moving_right and not self.moving_up:
            if self.index == 3:
                self.index = 0
            self.screen.blit(self.pacmans[2][self.index].image, self.pacman.rect)
            self.index += 1
        elif not self.moving_down and not self.moving_left and self.moving_right and not self.moving_up:
            if self.index == 3:
                self.index = 0
            self.screen.blit(self.pacmans[3][self.index].image, self.pacman.rect)
            self.index += 1
        elif not self.moving_down and not self.moving_left and not self.moving_right and self.moving_up:
            if self.index == 3:
                self.index = 0
            self.screen.blit(self.pacmans[4][self.index].image, self.pacman.rect)
            self.index += 1
        else:
            self.screen.blit(self.pacmans[0][0].image, self.pacman.rect)

    def update(self, maze, settings, stats, sb, red, blue, orange, pink):
        """Update the pacman's position based on the movement flag."""
        # Update pacman's center value, not rect.
        x = int(self.pacman.rect.centerx / 12)
        y = int(self.pacman.rect.centery / 12)

        if self.moving_right and (self.rows[y][x+1] != 'x'):
                self.centerx += 1.0
        if self.moving_left and (self.rows[y][x-1] != 'x'):
            self.centerx -= 1.0
        if self.moving_down and (self.rows[y+1][x] != 'x'):
            self.centery += 1.0
        if self.moving_up and (self.rows[y-1][x-1] != 'x'):
            self.centery -= 1.0
        self.pacman.rect.centerx = self.centerx
        self.pacman.rect.centery = self.centery
        self.scared_timer += 1

        for x in maze.shields:
            if pygame.Rect.colliderect(self.pacman.rect, x):
                maze.shields.remove(x)
                stats.score += settings.points_shields
                sb.prep_score()
                self.scared_ghost_t(red, blue, orange, pink)
                if len(maze.points) == 0 and len(maze.shields) == 0:
                    self.reset_pacman()
                    self.scared_ghost_f(red, blue, orange, pink)
                    self.reset_ghost(red, blue, orange, pink)
                    maze.reset_maze()

        if self.scared_flag:
            if (pygame.Rect.colliderect(self.pacman.rect, red.red.rect)) and red.scared:
                stats.score += settings.points_ghost
                red.reset_red()
                red.scared = False
            if (pygame.Rect.colliderect(self.pacman.rect, blue.blue.rect)) and blue.scared:
                stats.score += settings.points_ghost
                blue.reset_blue()
                blue.scared = False
            if (pygame.Rect.colliderect(self.pacman.rect, orange.orange.rect)) and orange.scared:
                stats.score += settings.points_ghost
                orange.reset_orange()
                orange.scared = False
            if (pygame.Rect.colliderect(self.pacman.rect, pink.pink.rect)) and pink.scared:
                stats.score += settings.points_ghost
                pink.reset_pink()
                pink.scared = False
            sb.prep_score()

        if self.scared_timer == 1500 and self.scared_flag:
            self.scared_ghost_f(red, blue, orange, pink)

        for x in maze.points:
            if pygame.Rect.colliderect(self.pacman.rect, x):
                maze.points.remove(x)
                stats.score += settings.points_coins
                sb.prep_score()
                if len(maze.points) == 0 and len(maze.shields) == 0:
                    self.reset_pacman()
                    self.scared_ghost_f(red, blue, orange, pink)
                    self.reset_ghost(red, blue, orange, pink)
                    maze.reset_maze()

    def reset_pacman(self):
        self.centerx = self.starting_centerx
        self.centery = self.starting_centery

    @staticmethod
    def reset_ghost(red, blue, orange, pink):
        red.reset_red()
        blue.reset_blue()
        orange.reset_orange()
        pink.reset_pink()

    def scared_ghost_t(self, red, blue, orange, pink):
        self.scared_timer = 0
        self.scared_flag = True
        pink.scared = True
        blue.scared = True
        orange.scared = True
        red.scared = True

    def scared_ghost_f(self, red, blue, orange, pink):
        self.scared_flag = False
        pink.scared = False
        blue.scared = False
        orange.scared = False
        red.scared = False
        self.scared_flag = False
