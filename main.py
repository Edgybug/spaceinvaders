import pygame 
import random

from constants import *

from pygame.locals import *

from spaceship import Spaceship
from bullets import Bullets
from aliens import Aliens
from alien_bullets import AlienBullets

def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    #Set up the clock and fps for the game
    clock = pygame.time.Clock()
    fps = 60
    
    #Define window and background 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Space Invaders')
    bg = pygame.image.load('img/bg.png')
    background = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    #CREATE SPRITE GROUPS
    drawables = pygame.sprite.Group()
    updatables = pygame.sprite.Group()
    spaceship_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    alien_group = pygame.sprite.Group()
    alien_bullet_group = pygame.sprite.Group()

    #PLAYER
    Spaceship.containers = (spaceship_group, drawables, updatables)
    spaceship = Spaceship(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT - 100)) #adding player in the middle of the screen
    spaceship_group.add(spaceship)
    drawables.add(spaceship)
    updatables.add(spaceship)

    Bullets.containers = (bullet_group, drawables, updatables)

    #ALIENS 
    Aliens.containers = (alien_group, drawables, updatables)
    AlienBullets.containers = (alien_bullet_group, drawables, updatables)

    #CREATE ALIENS
    def create_aliens():
        #generate aliens
        for row in range(ENEMY_ROWS):
            for item in range(ENEMY_COLS):
                alien = Aliens(200 + item * 100, 100 + row * 80)
                #add to groups
                alien_group.add(alien), drawables.add(alien), updatables.add(alien)
    create_aliens()
    
    last_alien_shot = pygame.time.get_ticks()

    #GAME LOOP  - 1. Handle Events 2. Update Game State 3. Draw Game State
    while True:
        clock.tick(fps)

        #add background
        screen.blit(background, (0, 0)) 

        #create random alien bullets
        time_now = pygame.time.get_ticks() #record_current_time 
        if time_now - last_alien_shot > ALIEN_SHOOT_COOLDOWN:
            attacking_alien = random.choice(alien_group.sprites()) #get random alien
            alien_bullet = AlienBullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)

            #add to groups 
            alien_bullet_group.add(alien_bullet), drawables.add(alien_bullet), updatables.add(alien_bullet)
            last_alien_shot = time_now

        #COLLISION
        for bullet in bullet_group:
            if pygame.sprite.spritecollide(bullet, alien_group, True):
                bullet.kill()
        
        for bullet in alien_bullet_group:
            if pygame.sprite.spritecollide(bullet, spaceship_group, False, pygame.sprite.collide_mask):
                #reduce spaceship health
                spaceship.health_remaining -= 1
                bullet.kill()
                if spaceship.health_remaining == 0:
                    spaceship.kill()

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        #update sprite groups
        updatables.update(screen)
        drawables.draw(screen)
        
        #update sprite groups   
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()