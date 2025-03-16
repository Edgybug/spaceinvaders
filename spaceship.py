import pygame
from pygame.locals import *
from constants import *
from bullets import Bullets
from yamato_cannon import Yamato_Cannon

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.2)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health = 3):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/spaceship2.png')
        self.image = pygame.transform.scale(self.image, (48, 58))
        self.rect = self.image.get_rect() #get the rectangle of the image
        self.rect.center = [x, y] #position
        self.health_start = health
        self.health_remaining = health 
        self.last_shot = pygame.time.get_ticks()

        self.last_yamato_shot = pygame.time.get_ticks()
        self.yamato_charges = 2
        self.score = 0 
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def healthbar(self, screen):
        #draw health bar
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.bottom + 10, self.rect.width, 15))
        if self.health_remaining:
            pygame.draw.rect(screen, GREEN, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width *(self.health_remaining / self.health_start)), 15))

    def add_yamato_charges(self):
        if self.score == 100 or self.score == 200 or self.score == 300:
            self.yamato_charges += 1

    def update_score(self):
        self.score += SCORE_INCREMENT
        self.add_yamato_charges()
        

    def shoot(self):
        
        bullet = Bullets(self.rect.centerx, self.rect.top)
        if hasattr(self, 'containers') and Bullets.containers:
            for container in Bullets.containers:
                container.add(bullet)
        return bullet
    
    def shootYamato(self):
        yamato = Yamato_Cannon(self.rect.centerx, self.rect.top)
        if hasattr(self, 'containers') and Yamato_Cannon.containers:
            for container in Yamato_Cannon.containers:
                container.add(yamato)
        self.yamato_charges -= 1
        return yamato

    def update(self, screen = None):
        time_now = pygame.time.get_ticks()
        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left  > 0:
            self.rect.x -= PLAYER_SPEED
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED
         
        #shoot bullets
        if key[pygame.K_SPACE] and time_now - self.last_shot > SHOOT_COOLDOWN:
            laser_fx.play()
            self.shoot()
            self.last_shot = time_now

        #shoot yamato
        if key[pygame.K_LSHIFT] and time_now - self.last_yamato_shot > YAMATO_COOLDOWN:
            if self.yamato_charges > 0:
                laser_fx.play()
                self.shootYamato()
                self.last_yamato_shot = time_now
    
        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        if screen:
            self.healthbar(screen)
            

        
        
            
        
  