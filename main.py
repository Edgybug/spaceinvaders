import pygame 
import random

from constants import *
from pygame.locals import *
from spaceship import Spaceship
from bullets import Bullets
from aliens import Aliens
from alien_bullets import AlienBullets
from explosions import Explosion
from timer import RepeatedTimer

def main():


    pygame.init()
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    

    #Add sound
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()

    explosion_fx = pygame.mixer.Sound("img/explosion.wav")
    explosion_fx.set_volume(0.2)

    explosion2_fx = pygame.mixer.Sound("img/explosion2.wav")
    explosion2_fx.set_volume(0.2)

    
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
    explosion_group = pygame.sprite.Group()

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
    Explosion.containers = (explosion_group, drawables, updatables)

    #CREATE ALIENS
    def create_aliens():
        #generate aliens
        for row in range(ENEMY_ROWS):
            for item in range(ENEMY_COLS):
                alien = Aliens(200 + item * 100, 100 + row * 80)
                #add to groups
                alien_group.add(alien), drawables.add(alien), updatables.add(alien)

    def random_aliens():
        #generate aliens
        x = random.randint(250, int(SCREEN_WIDTH - 250))
        y = random.randint(200, int(SCREEN_HEIGHT/2))
        alien = Aliens(x, y)
        alien_group.add(alien), drawables.add(alien), updatables.add(alien)
  
    create_aliens() #create initial aliens
    timer = RepeatedTimer(ENEMY_SPAWN_TIME, random_aliens) #spawn random aliens every 5 secs
    
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

        #COLLISION PLAYER -> ALIEN
        for bullet in bullet_group:
            if pygame.sprite.spritecollide(bullet, alien_group, True):
                bullet.kill() 
                spaceship.update_score()
                explosion = Explosion(bullet.rect.x, bullet.rect.y, 2)
                explosion_group.add(explosion),drawables.add(explosion), updatables.add(explosion) 
                explosion_fx.play()  

        #COLLISION ALIEN -> PLAYER
        for bullet in alien_bullet_group:
            if pygame.sprite.spritecollide(bullet, spaceship_group, False, pygame.sprite.collide_mask):
                #reduce spaceship health
                explosion = Explosion(spaceship.rect.x, spaceship.rect.y, 2)
                explosion_group.add(explosion),drawables.add(explosion), updatables.add(explosion)
                explosion2_fx.play()
                spaceship.health_remaining -= 1
                bullet.kill()
                if spaceship.health_remaining == 0:
                    explosion = Explosion(spaceship.rect.x, spaceship.rect.y, 3)
                    explosion_group.add(explosion),drawables.add(explosion), updatables.add(explosion)
                    explosion_fx.play()
                    spaceship.kill()

        if len(alien_group) < 10:
            timer.stop()
        
        if len(alien_group) == 0:
            score_text = font.render(f'YOU WIN: Score: {spaceship.score}', True, (255, 255, 255))
            screen.blit(score_text, (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2)))

        for event in pygame.event.get():
            if event.type == QUIT:
                timer.stop()
                return

        #update sprite groups
        updatables.update(screen)
        drawables.draw(screen)
        
        score_text = font.render(f'Score: {spaceship.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        #update sprite groups   
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()