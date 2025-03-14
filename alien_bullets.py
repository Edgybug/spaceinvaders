import pygame
from pygame.locals import *
from constants import *

class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/alien_bullet.png')
        self.image = pygame.transform.scale(self.image, (15, 15))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self, screen = None):
        self.rect.y += 3
        if self.rect.top < 0:
           self.kill()
   