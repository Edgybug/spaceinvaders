import pygame 
import random

from constants import *
from sprites import *
from spaceship import Spaceship
from explosions import Explosion

class Game(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        
        pygame.mixer.init()
        pygame.init()

        #SETUP
        #Set up the clock and fps for the game
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = 0 #0 game is in progress, 1 - player won, -1 - player lost
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Space Invaders')
        

        #CREATE SPRITE GROUPS
        self.all_sprites = pygame.sprite.Group()
        self.spaceship_sprites = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.yamato_group = pygame.sprite.Group()
        self.alien_sprites = pygame.sprite.Group()
        self.side_aliens = pygame.sprite.Group()
        self.random_aliens = pygame.sprite.Group()
        self.alien_bullet_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        
        self.player = Spaceship((self.spaceship_sprites, self.all_sprites), x=int(SCREEN_WIDTH/2), y=int(SCREEN_HEIGHT - 100), health=3)
        self.create_alien_grid()
        #FONTS
        pygame.font.init()
        self.font30 = pygame.font.SysFont('Constantia', 30)
        self.font50 = pygame.font.SysFont('Constantia', 50)

        #SOUND
        self.explosion_fx = pygame.mixer.Sound("img/explosion.wav")
        self.explosion_fx.set_volume(0.2)

        self.explosion2_fx = pygame.mixer.Sound("img/explosion2.wav")
        self.explosion2_fx.set_volume(0.2)

        self.laser_fx = pygame.mixer.Sound("img/laser.wav")
        self.laser_fx.set_volume(0.2)

        #TIMERS
        #START of game countdown timer
        self.countdown = 3
        self.last_count = pygame.time.get_ticks()

        #player shooting timer
        self.last_shot = pygame.time.get_ticks()
        self.last_yamato_shot = pygame.time.get_ticks()

        #alien shooting timer
        self.last_alien_shot = pygame.time.get_ticks()

        #random alien spawn timer
        self.spawn_random_alien = pygame.event.custom_type()
        pygame.time.set_timer(self.spawn_random_alien, 5000)

        #kamikadze aliens  timer
        self.spawn_side_alien = pygame.event.custom_type()
        pygame.time.set_timer(self.spawn_side_alien, 8000)
    
    #ADDING TEXT
    def draw_text(self, text, font, text_col,x,y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x,y))
    
    #DRAW BG
    def draw_bg(self, img):
        bg = pygame.image.load(img)
        background = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(background, (0, 0))  

    #HANDLE SHOOTING
    def input(self):
        time_now = pygame.time.get_ticks()
        #get keypresses
        key = pygame.key.get_pressed()
        #shoot bullets
        if key[pygame.K_SPACE] and time_now - self.last_shot > SHOOT_COOLDOWN:
            self.laser_fx.play()
            Bullets(self.player.rect.centerx, self.player.rect.top,(self.all_sprites, self.bullet_group))
            self.last_shot = time_now
        #shoot yamato
        if key[pygame.K_LSHIFT] and time_now - self.last_yamato_shot > YAMATO_COOLDOWN:
            if self.player.yamato_charges > 0:
                self.laser_fx.play()
                Yamato_Cannon(self.player.rect.centerx, self.player.rect.top, (self.all_sprites, self.yamato_group))
                self.player.yamato_charges -= 1
                self.last_yamato_shot = time_now

    def healthbar(self):
        #draw health bar
        pygame.draw.rect(self.screen, RED, (self.player.rect.x, self.player.rect.bottom + 10, self.player.rect.width, 15))
        if self.player.health_remaining:
            pygame.draw.rect(self.screen, GREEN, (self.player.rect.x, (self.player.rect.bottom + 10), int(self.player.rect.width *(self.player.health_remaining / self.player.health_start)), 15))
    #GENERATE ALIENS
    def create_alien_grid(self):
        for row in range(ENEMY_ROWS):
            for item in range(ENEMY_COLS):
                Aliens(200 + item * 100, 100 + row * 80,(self.all_sprites, self.alien_sprites))

    #SPAWN RANDOM ALIENS
    def generate_random_aliens(self):
        #generate aliens
        x = random.randint(300, 900)
        y = random.randint(100, 450)    
        Aliens(x, y,(self.all_sprites, self.random_aliens, self.alien_sprites))
    
    def generate_kamikadze_aliens(self):
        x = random.randint(-200, 1400)
        Kamikadze_Aliens(x, -150, self.player ,(self.all_sprites, self.alien_sprites, self.side_aliens))
    #HANDLE COLLISIONS
    def collisions(self):
        time_now = pygame.time.get_ticks() #record_current_time 

        #ALIENS SHOOTING
        if len(self.alien_sprites) > 0:
            if time_now - self.last_alien_shot > ALIEN_SHOOT_COOLDOWN:
                attacking_alien = random.choice(self.alien_sprites.sprites()) #get random alien
                AlienBullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom,(self.all_sprites, self.alien_bullet_group))
                self.last_alien_shot = time_now
                    
            #COLLISION PLAYER BULLET -> ALIEN
            for bullet in self.bullet_group:
                    if pygame.sprite.spritecollide(bullet, self.alien_sprites, True, pygame.sprite.collide_mask):
                        bullet.kill() 
                        self.player.update_score()
                        Explosion(bullet.rect.x, bullet.rect.y, 2,(self.all_sprites, self.explosion_group))
                        self.explosion_fx.play()  

            #COLLISION PLAYER YAMATO -> ALIEN
            for yamato in self.yamato_group:
                if pygame.sprite.spritecollide(yamato, self.alien_sprites, True, pygame.sprite.collide_mask):
                    yamato.kill() 
                    self.player.update_score()
                    Explosion(yamato.rect.x, yamato.rect.y, 2,(self.all_sprites, self.explosion_group))

            #KAMIKADZE ALIENS
            for alien in self.side_aliens:
                if pygame.sprite.spritecollide(alien, self.spaceship_sprites, False, pygame.sprite.collide_mask):   
                    #reduce spaceship health
                    Explosion(self.player.rect.x, self.player.rect.y, 3,(self.all_sprites, self.explosion_group))
                    self.explosion2_fx.play()
                    self.player.health_remaining -= 1
                    alien.kill()
                    if self.player.health_remaining == 0:
                        Explosion(self.player.rect.x, self.player.rect.y, 3,(self.all_sprites, self.explosion_group))
                        self.explosion_fx.play()
                        self.player.kill()
                        self.game_over = 1

            #COLLISION ALIEN -> PLAYER
            for bullet in self.alien_bullet_group:
                if pygame.sprite.spritecollide(bullet, self.spaceship_sprites, False, pygame.sprite.collide_mask):
                    #reduce spaceship health
                    Explosion(self.player.rect.x, self.player.rect.y, 2,(self.all_sprites, self.explosion_group))
                    self.explosion2_fx.play()
                    self.player.health_remaining -= 1
                    bullet.kill()
                    if self.player.health_remaining == 0:
                        Explosion(self.player.rect.x, self.player.rect.y, 3,(self.all_sprites, self.explosion_group))
                        self.explosion_fx.play()
                        self.player.kill()
                        self.game_over = 1

    #CHECK IF ALL ALIENS ARE ELIMINATED
    def check_game_over(self):
        if len(self.alien_sprites) == 0 and len(self.random_aliens) == 0 and len(self.side_aliens) == 0:
            self.game_over = -1

    #GAME LOOP  - 1. Handle Events 2. Update Game State 3. Draw Game State
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.spawn_random_alien and len(self.alien_sprites) > 15 and len(self.random_aliens) < 10:
                    self.generate_random_aliens()       
                if event.type == self.spawn_side_alien and len(self.alien_sprites) > 5 and len(self.random_aliens) < 5:
                    self.generate_kamikadze_aliens()   

            self.draw_bg('img/bg.png')
        
            if self.countdown == 0:
                #CHECK GAME STATUS 
                if self.game_over == 0:
                    self.input()
                    self.collisions()
                    self.healthbar()
                    self.check_game_over()
                    self.all_sprites.update(dt)
                if self.game_over == -1:
                    self.draw_text(f'YOU WIN: Score: {self.player.score}', self.font50, WHITE, int(SCREEN_WIDTH / 2 - 200), int(SCREEN_HEIGHT / 2 + 150))
                if self.game_over == 1:
                    self.draw_text('GAME OVER!!!', self.font50, WHITE, int(SCREEN_WIDTH / 2 - 200), int(SCREEN_HEIGHT / 2 + 150))

            self.all_sprites.draw(self.screen)
            self.draw_text(f'Score: {self.player.score}', self.font30, WHITE, 10, 10)
            self.draw_text(f'Yamato Charges: {self.player.yamato_charges}', self.font30, WHITE, 300, 10)
            

            #UPDATE GAME START COUNDOWN
            if self.countdown > 0:
                self.draw_text("GET READY!", self.font50, WHITE, int(SCREEN_WIDTH / 2 - 150), int(SCREEN_HEIGHT / 2 + 150))
                self.draw_text(str(self.countdown), self.font50, WHITE, int(SCREEN_WIDTH / 2 - 40), int(SCREEN_HEIGHT / 2 + 200))
                count_timer = pygame.time.get_ticks()
                if count_timer - self.last_count > 1000:
                    self.countdown -= 1
                    self.last_count = count_timer
            pygame.display.flip()       
        pygame.quit()
if __name__ == '__main__':
    game = Game()
    game.run()

  
   

    

