import pygame
import sys


class EventLoop:
    def __init__(self, finished):
        self.finished = finished

    def __str__(self): return 'eventloop, finished=' + str(self.finished) + ')'

    # def check_events(screen, pacman, ghosts):
    @staticmethod
    def check_events(screen, pacman, start):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                EventLoop.check_keydown_events(event, pacman)
            elif event.type == pygame.KEYUP:
                EventLoop.check_keyup_events(event, pacman)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                EventLoop.check_play_button(screen, start, mouse_x, mouse_y)

    @staticmethod
    def check_keydown_events(event, pacman):
        """Respond to keypresses"""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_RIGHT:
            pacman.moving_right = True
        elif event.key == pygame.K_LEFT:
            pacman.moving_left = True
        elif event.key == pygame.K_UP:
            pacman.moving_up = True
        elif event.key == pygame.K_DOWN:
            pacman.moving_down = True

    @staticmethod
    def check_keyup_events(event, pacman):
        if event.key == pygame.K_RIGHT:
            pacman.moving_right = False
        elif event.key == pygame.K_LEFT:
            pacman.moving_left = False
        elif event.key == pygame.K_UP:
            pacman.moving_up = False
        elif event.key == pygame.K_DOWN:
            pacman.moving_down = False

    @staticmethod
    def check_play_button(screen, start, mouse_x, mouse_y):
        button_clicked = start.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not start.playing:
            start.playing = True
