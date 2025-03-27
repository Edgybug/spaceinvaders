import pygame
from pygame.locals import *
from constants import *


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y, health = 3):
        super().__init__(*groups)
        self.image = pygame.image.load('img/spaceship2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 58))
        self.rect = self.image.get_frect(center = (x, y)) #get the rectangle of the image

        #HEALTH
        self.health_start = health
        self.health_remaining = health 
        self.last_shot = pygame.time.get_ticks()

        self.last_yamato_shot = pygame.time.get_ticks()
        self.yamato_charges = 2
        self.score = 0 
        
        self.direction = pygame.Vector2()
        self.speed = 400
        print(self.direction)

    def add_yamato_charges(self):
        if self.score == 100 or self.score == 200 or self.score == 300:
            self.yamato_charges += 1

    def update_score(self):
        self.score += SCORE_INCREMENT
        self.add_yamato_charges()
    
    def input(self):
        keys = pygame.key.get_pressed()  
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a]) # if right 1-0 = 1 going +1, if left 0 - 1 = -1 going -1

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt 

    def update(self, dt):
        self.input()
        self.move(dt)
       
        
  

            

        
        
            
        
  