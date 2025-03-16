import pygame
from pygame.locals import *
from constants import *
from explosions import Explosion
from timer import RepeatedTimer

class Yamato_Cannon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/yamato.png')
        self.image = pygame.transform.scale(self.image, (150, 150))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self, screen = None):
        self.rect.y -= 7
        if self.rect.bottom < 0:
           self.kill()

        #update mask
        self.mask = pygame.mask.from_surface(self.image)