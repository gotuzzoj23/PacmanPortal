import pygame


class ImageRect:
    def __init__(self, screen, imagename, height, width):
        self.screen = screen
        name = 'images/' + imagename + '.png'

        img = pygame.image.load(name)
        img = pygame.transform.scale(img, (height, width))
        self. rect = img.get_rect()
        self.rect.left -= self.rect.width
        self.rect.right -= self.rect.height
        self.image = img

    def ___str__(self):
        return 'imagerect(' + str(self.image) + str(self.rect) + ')'

    def blit(self):
        self.screen.blit(self.image, self.rect)
