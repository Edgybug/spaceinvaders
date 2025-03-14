import pygame
import random
from pygame.locals import *
from constants import *


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1,5)) + ".png")
        self.image = pygame.transform.scale(self.image, (35, 35))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.move_direction = 1
        self.move_counter = 0

        self.last_alien_shot = pygame.time.get_ticks()

    def update(self, screen = None):
        self.rect.x += self.move_direction
        self.move_counter += 1

        if abs(self.move_counter) > 150:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

  
 


           
