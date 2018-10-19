from typing import Optional, Any

import pygame.font
from imagerect import ImageRect


class Start:
    orange: ImageRect
    pink: ImageRect
    blue: ImageRect
    red: ImageRect
    pac: ImageRect
    portal_orange: ImageRect
    portal_blue: ImageRect
    msg_image_rect: object
    msg_image: Optional[Any]
    title_rect: object
    title: Optional[Any]

    def __init__(self, screen, settings):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.create_figures(self.screen)

        # Start screen
        self.bg_width, self.bg_height = settings.screen_width, settings.screen_height
        self.button_color_bg = (255, 255, 255)
        self.text_color_bg = (0, 0, 0)
        self.rect_bg = pygame.Rect(0, 0, self.bg_width, self.bg_height)
        self.rect_bg.center = self.screen_rect.center
        self.font_title = pygame.font.SysFont(None, 125)

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 180, 100)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.bottom - 50

        self.pacs = []
        self.reds = []
        self.blues = []
        self.pinks = []
        self.oranges = []

        self.playing = False
        # The button message and background needs to be prepped only once
        self.prep_msg('PLAY')
        self.prep_bg()

    # Start button
    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.update()
        self.draw_figures()

    # Start screen title and background
    def prep_bg(self):
        self.title = self.font_title.render("PACMAN PORTAL", True, self.text_color_bg, self.button_color_bg)
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (self.rect_bg.centerx, 200)

    def draw_bg(self):
        self.screen.fill(self.button_color_bg, self.rect_bg)
        self.screen.fill(self.button_color_bg, self.title_rect)
        self.screen.blit(self.title, self.title_rect)

    def update(self):
        if pygame.Rect.colliderect(self.red.rect, self.portal_blue):
            self.red.centerx = 100
        else:
            self.red.centerx += 1
        self.red.rect.centerx = self.red.centerx

        if pygame.Rect.colliderect(self.pac.rect, self.portal_blue):
            self.pac.centerx = 100
        else:
            self.pac.centerx += 1
        self.pac.rect.centerx = self.pac.centerx

        if pygame.Rect.colliderect(self.blue.rect, self.portal_blue):
            self.blue.centerx = 100
        else:
            self.blue.centerx += 1
        self.blue.rect.centerx = self.blue.centerx

        if pygame.Rect.colliderect(self.pink.rect, self.portal_blue):
            self.pink.centerx = 100
        else:
            self.pink.centerx += 1
        self.pink.rect.centerx = self.pink.centerx

        if pygame.Rect.colliderect(self.orange.rect, self.portal_blue):
            self.orange.centerx = 100
        else:
            self.orange.centerx += 1
        self.orange.rect.centerx = self.orange.centerx

    def draw_figures(self):
        self.screen.blit(self.reds[0].image, self.red.rect)
        self.screen.blit(self.blues[1].image, self.blue.rect)
        self.screen.blit(self.pinks[0].image, self.pink.rect)
        self.screen.blit(self.oranges[0].image, self.orange.rect)
        self.screen.blit(self.pacs[1].image, self.pac.rect)
        self.screen.blit(self.portal_blue.image, self.portal_blue.rect)
        self.screen.blit(self.portal_orange.image, self.portal_orange.rect)

    def create_figures(self, screen):
        self.pac = (ImageRect(screen, 'pacman/pac', int(5 * 5.1), int(5 * 5.1)))
        self.pacs.append(self.pac)
        self.pac = (ImageRect(screen, 'pacman/pac_right_1', int(5 * 5.1), int(5 * 5.1)))
        self.pacs.append(self.pac)
        self.pac = (ImageRect(screen, 'pacman/pac_right_2', int(5 * 5.1), int(5 * 5.1)))
        self.pacs.append(self.pac)
        self.pac.centerx = self.pac.rect.centerx
        self.pac.rect.centery = 500

        self.red = (ImageRect(screen, 'red/red_right_1', int(5 * 5.1), int(5 * 5.1)))
        self.reds.append(self.red)
        self.red = (ImageRect(screen, 'red/red_right_2', int(5 * 5.1), int(5 * 5.1)))
        self.reds.append(self.red)
        self.red.centerx = self.red.rect.centerx
        self.red.centerx = - 100
        self.red.rect.centery = 500

        self.blue = (ImageRect(screen, 'blue/blue_right_1', int(5 * 5.1), int(5 * 5.1)))
        self.blues.append(self.blue)
        self.blue = (ImageRect(screen, 'blue/blue_right_2', int(5 * 5.1), int(5 * 5.1)))
        self.blues.append(self.blue)
        self.blue.centerx = self.blue.rect.centerx
        self.blue.centerx = - 200
        self.blue.rect.centery = 500

        self.pink = (ImageRect(screen, 'pink/pink_right_1', int(5 * 5.1), int(5 * 5.1)))
        self.pinks.append(self.pink)
        self.pink = (ImageRect(screen, 'pink/pink_right_2', int(5 * 5.1), int(5 * 5.1)))
        self.pinks.append(self.pink)
        self.pink.centerx = self.pink.rect.centerx
        self.pink.centerx = -300
        self.pink.rect.centery = 500

        self.orange = (ImageRect(screen, 'orange/orange_right_1', int(5 * 5.1), int(5 * 5.1)))
        self.oranges.append(self.orange)
        self.orange = (ImageRect(screen, 'orange/orange_right_2', int(5 * 5.1), int(5 * 5.1)))
        self.oranges.append(self.orange)
        self.orange.centerx = self.orange.rect.centerx
        self.orange.centerx = -400
        self.orange.rect.centery = 500

        self.portal_blue = (ImageRect(screen, 'portal_blue', int(5 * 5.1), int(5 * 5.1)))
        self.portal_blue.rect.centerx = self.screen_rect.right - 100
        self.portal_blue.rect.centery = 500
        self.portal_orange = (ImageRect(screen, 'portal_orange', int(5 * 5.1), int(5 * 5.1)))
        self.portal_orange.rect.centerx = self.screen_rect.left + 100
        self.portal_orange.rect.centery = 500
