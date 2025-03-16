import pygame 
import random

from constants import *
from pygame.locals import *
from spaceship import Spaceship
from bullets import Bullets
from yamato_cannon import Yamato_Cannon
from aliens import Aliens
from alien_bullets import AlienBullets
from explosions import Explosion
from timer import RepeatedTimer

def main():

    pygame.init()

    #FONTS
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    font30 = pygame.font.SysFont('Constantia', 30)
    font50 = pygame.font.SysFont('Constantia', 50)

    #Set up the clock and fps for the game
    clock = pygame.time.Clock()
    fps = 60
    countdown = 0
    last_count = pygame.time.get_ticks()
    game_over = 0 #0 game is in progress, 1 - player won, -1 - player lost
   
    
    #function for adding text
    def draw_text(text, font, text_col,x,y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x,y))
    
    #function for drawing backgorund
    def draw_bg(img):
        bg = pygame.image.load(img)
        background = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0, 0))  

    #Add sound
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()

    explosion_fx = pygame.mixer.Sound("img/explosion.wav")
    explosion_fx.set_volume(0.2)

    explosion2_fx = pygame.mixer.Sound("img/explosion2.wav")
    explosion2_fx.set_volume(0.2)

    
    #Define window and background 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Space Invaders')
    

    #CREATE SPRITE GROUPS
    drawables = pygame.sprite.Group()
    updatables = pygame.sprite.Group()
    spaceship_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    yamato_group = pygame.sprite.Group()
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
    Yamato_Cannon.containers = (yamato_group, drawables, updatables)
    

    #ALIENS 
    Aliens.containers = (alien_group, drawables, updatables)
    AlienBullets.containers = (alien_bullet_group, drawables, updatables)
    Explosion.containers = (explosion_group, drawables, updatables)

    #CREATE ALIENS
    last_alien_shot = pygame.time.get_ticks()
    last_random_alien_atack = pygame.time.get_ticks()

    def create_aliens():
        #generate aliens
        for row in range(ENEMY_ROWS):
            for item in range(ENEMY_COLS):
                alien = Aliens(200 + item * 100, 100 + row * 80)
                #add to groups
                alien_group.add(alien), drawables.add(alien), updatables.add(alien)

    #SPAWN RANDOM ALIENS
    def random_aliens():
        #generate aliens
        x = random.randint(250, int(SCREEN_WIDTH - 250))
        y = random.randint(200, int(SCREEN_HEIGHT/2))
        alien = Aliens(x, y)
        alien_group.add(alien), drawables.add(alien), updatables.add(alien)

    def random_attack():
        
        attacking_alien = random.choice(alien_group.sprites()) #get random alien
        attacking_alien.rect.y += 5
        attacking_alien.rect.x += 5
        last_random_alien_atack = time_now

    def reverse_attack():
        
        attacking_alien = random.choice(alien_group.sprites()) #get random alien
        attacking_alien.rect.y -= 5
        attacking_alien.rect.x -= 5
        last_random_alien_atack = time_now
  
    create_aliens() #create initial aliens
    timer = RepeatedTimer(ENEMY_SPAWN_TIME, random_aliens) #spawn random aliens every 5 secs
    
   
    #GAME LOOP  - 1. Handle Events 2. Update Game State 3. Draw Game State
    while True:
        clock.tick(fps)
        #add background                          
        draw_bg('img/bg.png')

        if countdown == 0 or game_over == 0:

           
            time_now = pygame.time.get_ticks() #record_current_time 

            #ALIENS SHOOTING
            if len(alien_group) > 0:
                if time_now - last_alien_shot > ALIEN_SHOOT_COOLDOWN:
                    attacking_alien = random.choice(alien_group.sprites()) #get random alien
                    alien_bullet = AlienBullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
                    #add to groups 
                    alien_bullet_group.add(alien_bullet), drawables.add(alien_bullet), updatables.add(alien_bullet)
                    last_alien_shot = time_now
                
                #if time_now - last_random_alien_atack > ALIEN_ATTACK_COOLDOWN:
                    #random_attack()
                    #reverse_attack()
                
            #COLLISION PLAYER BULLET -> ALIEN
            for bullet in bullet_group:
                if pygame.sprite.spritecollide(bullet, alien_group, True):
                    bullet.kill() 
                    spaceship.update_score()
                    explosion = Explosion(bullet.rect.x, bullet.rect.y, 2)
                    explosion_group.add(explosion),drawables.add(explosion), updatables.add(explosion) 
                    explosion_fx.play()  

            for yamato in yamato_group:
                if pygame.sprite.spritecollide(yamato, alien_group, True):
                    yamato.kill() 
                    spaceship.update_score()
                    explosion = Explosion(bullet.rect.x, bullet.rect.y, 2)
                    explosion_group.add(explosion), drawables.add(explosion), updatables.add(explosion) 
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
                        game_over = 1

            #STOP SPAWNING RANDOM ALIENS
            if len(alien_group) < 10:
                timer.stop()
            
            #CHECK IF ALL ALIENS ARE ELIMINATED
            if len(alien_group) == 0:
                game_over = -1
                
            for event in pygame.event.get():
                if event.type == QUIT:
                    timer.stop()
                    return

        #CHECK GAME STATUS 
        if game_over == 0:
             updatables.update(screen)
        else:
            if game_over == -1:
                draw_text(f'YOU WIN: Score: {spaceship.score}', font50, WHITE, int(SCREEN_WIDTH / 2 - 110), int(SCREEN_HEIGHT / 2 + 150))
            if game_over == 1:
                draw_text('GAME OVER!!!', font50, WHITE, int(SCREEN_WIDTH / 2 - 110), int(SCREEN_HEIGHT / 2 + 150))

        drawables.draw(screen)
        draw_text(f'Score: {spaceship.score}', font30, WHITE, 10, 10)
        draw_text(f'Yamato Charges: {spaceship.yamato_charges}', font30, WHITE, 300, 10)
        #update sprite groups   
        pygame.display.flip()   

        #UPDATE GAME START COUNDOWN
        if countdown > 0:
                pass
            #draw_text("GET READY!", font50, WHITE, int(SCREEN_WIDTH / 2 - 110), int(SCREEN_HEIGHT / 2 + 150))
            #draw_text(str(countdown), font50, WHITE, int(SCREEN_WIDTH / 2 + 20), int(SCREEN_HEIGHT / 2 + 200))
            #count_timer = pygame.time.get_ticks()
            #if count_timer - last_count > 1000:
                #countdown -= 1
                #last_count = count_timer
            
         
    pygame.quit()

if __name__ == "__main__":
    main()