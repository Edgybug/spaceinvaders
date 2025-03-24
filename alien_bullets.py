import pygame
from pygame.locals import *
from constants import *


class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load('img/alien_bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_frect(center = [x, y])
      
    def update(self, screen = None):
        self.rect.y += 3
        if self.rect.top < 0:
           self.kill()
   