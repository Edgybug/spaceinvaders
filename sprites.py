import pygame
import random
from constants import *


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("img/alien" + str(random.randint(1,9)) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_frect(center = (x,y))
        
        self.move_direction = 1
        self.move_counter = 0
        
    def update(self, dt):
        self.rect.x += self.move_direction
        self.move_counter += 1

        if abs(self.move_counter) > 150:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

class Kamikadze_Aliens(Aliens):
    def __init__(self, x, y, player, *groups):
        super().__init__(x, y, *groups)
        self.player = player
        self.direction = pygame.Vector2()
        self.speed = 200
    
    def move(self, dt):
        #get direction
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()

        #update rect position + collision logic
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt
    
    def update(self, dt):
        self.move(dt)
        
class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('img/alien_bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_frect(center = (x, y))
      
    def update(self, dt):
        self.rect.y += 3
        if self.rect.top < 0:
           self.kill()
   
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y,*groups):
        super().__init__(*groups)
        self.image = pygame.image.load('img/bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_frect(center = [x, y])

    def update(self, dt):
        self.rect.y -= 5
        if self.rect.bottom < 0:
           self.kill()

class Yamato_Cannon(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('img/yamato.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_frect(center = [x, y])

    def update(self, dt):
        self.rect.y -= 7
        if self.rect.bottom < 0:
           self.kill()

        